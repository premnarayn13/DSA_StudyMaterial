# 03. Java PriorityQueue Internals, Custom Comparators & Dynamic Resizing Architecture

## 1. Introduction
**`java.util.PriorityQueue`** is one of the most frequently utilized collections in Java for competitive programming and technical coding interviews. It implements an unbounded priority queue based on a binary min-heap stored in a dynamic array (`Object[] queue`). Understanding its underlying JDK source code implementation, dynamic array growth policy, custom `Comparator` lambda mechanics, and performance traps (such as $O(N)$ arbitrary removal) is essential for writing high-performance algorithm code in Java.

> **Important:** By default, Java's `PriorityQueue` is a **Min-Heap** (smallest element at root). To construct a **Max-Heap**, you MUST pass a reverse order comparator (`Collections.reverseOrder()` or `(a, b) -> b - a` / `Integer.compare(b, a)`).

```
Java PriorityQueue Architecture:
+-----------------------------------------------------------------------------------+
| Underlying Storage : Object[] queue (Dynamic Array, Default Capacity = 11)       |
| Default Order     : Min-Heap (Natural Ordering via Comparable / Comparator)      |
| Resizing Policy   : Double (+2) if size < 64; 50% Growth if size >= 64 ⚡           |
+-----------------------------------------------------------------------------------+
```

---

## 2. JDK Source Code Internals & Resizing Formula

### 2.1 Core Fields in `java.util.PriorityQueue`
Extracted directly from OpenJDK source code:

```java
transient Object[] queue; // Non-private to simplify nested class access
int size = 0;
private final Comparator<? super E> comparator;
transient int modCount = 0; // Fail-fast iterator check
```

* **Default Initial Capacity**: `DEFAULT_INITIAL_CAPACITY = 11`.

### 2.2 Dynamic Resizing Growth Strategy (`grow(int minCapacity)`)
When `size >= queue.length`, `PriorityQueue` executes dynamic expansion:

```java
private void grow(int minCapacity) {
    int oldCapacity = queue.length;
    // Double size if small (<64); else grow by 50%
    int newCapacity = oldCapacity + ((oldCapacity < 64) ?
                                     (oldCapacity + 2) :
                                     (oldCapacity >> 1));
    // Overflow-conscious code
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    queue = Arrays.copyOf(queue, newCapacity);
}
```

* **Growth Policy**:
  - If `oldCapacity < 64`: New capacity = $2 \times \text{oldCapacity} + 2$ (More aggressive doubling for small heaps!).
  - If `oldCapacity \ge 64`: New capacity = $\text{oldCapacity} + (\text{oldCapacity} \gg 1) = \mathbf{1.5 \times \text{oldCapacity}}$ (50% growth).

### 2.3 `siftUp` and `siftDown` Implementation Variants
JDK source code separates heap percolation into two branches depending on whether a custom `Comparator` was provided:
1. `siftUpComparable`: Casts elements to `Comparable<? super E>` and calls `c.compareTo(parent)`.
2. `siftUpUsingComparator`: Invokes `comparator.compare(e, parent)`.

```
JDK PriorityQueue Internals Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operations / Methods  | Time Complexity   | Source Method     | Invariant Impact  |
+-----------------------+-------------------+-------------------+-------------------+
| `offer(e)` / `add(e)` | Amortized $O(\log N)$| `siftUp(size, e)`| Append + Percolate Up |
| `poll()`              | $O(\log N)$       | `siftDown(0, e)`  | Root swap + Percolate Dn |
| `peek()`              | **$O(1)$ Constant⚡**| `(E) queue[0]`  | Zero mutation     |
| `remove(Object o)`    | **$O(N)$ Linear ❌**| `indexOf(o)` scan | Linear array search|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"PriorityQueue default size is 11! Grows by doubling (+2) if <64, 50% if >=64! Default is Min-Heap!"**

---

## 3. Custom Comparators & Lambda Expressions

### 3.1 Primitive & Object Custom Orderings

```java
// 1. Min-Heap (Default Natural Order)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// 2. Max-Heap (Reverse Order)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
// Lambda Equivalent (Use Integer.compare to avoid integer overflow!):
PriorityQueue<Integer> maxHeapLambda = new PriorityQueue<>((a, b) -> Integer.compare(b, a));

// 3. Custom Object Sorting (e.g., Point objects sorted by distance from origin)
class Point { int x, y; Point(int x, int y) { this.x = x; this.y = y; } }

PriorityQueue<Point> pointHeap = new PriorityQueue<>(
    (p1, p2) -> Integer.compare(p1.x * p1.x + p1.y * p1.y, p2.x * p2.x + p2.y * p2.y)
);

// 4. Frequency Map Sorting (LeetCode 347 - Top K Frequent Elements)
Map<Integer, Integer> freqMap = new HashMap<>();
PriorityQueue<Integer> freqHeap = new PriorityQueue<>(
    (a, b) -> Integer.compare(freqMap.get(a), freqMap.get(b)) // Min-Heap based on frequency
);
```

### 3.2 Overflow Pitfall with `(a, b) -> a - b`
Using `(a, b) -> a - b` for custom comparators causes **Integer Overflow Bugs** when comparing negative numbers!
* Example: `a = -2,147,483,648` (`Integer.MIN_VALUE`) and `b = 1`.
  - `a - b` overflows to `2,147,483,647`, returning a POSITIVE result $\implies$ Incorrect order!
* **Rule**: ALWAYS use `Integer.compare(a, b)` or `Double.compare(a, b)`.

---

## 4. Internal Working Mechanics
Tracing `PriorityQueue.offer()` and dynamic resizing from capacity 11 to 24:

```
Initial State: Capacity = 11, Size = 11.
Calling offer(12th element):

Step 1: Size == queue.length (11 == 11) -> Trigger grow(12).
Step 2: Calculate new capacity:
        oldCapacity = 11 (< 64).
        newCapacity = 11 + (11 + 2) = 24.
Step 3: Copy old array [11] into new array [24] using Arrays.copyOf.
Step 4: Execute siftUp(11, val) to place 12th element in valid min-heap position.

Result: Capacity expanded to 24 seamlessly in Amortized O(log N) time! ✅
```

---

## 5. Visual Diagram
PriorityQueue Method Hierarchy & Thread Safety Spectrum:

```
                 java.util.Collection
                          |
                 java.util.Queue
                          |
       +------------------+------------------+
       |                                     |
java.util.PriorityQueue           java.util.concurrent.PriorityBlockingQueue
(Thread Unsafe, Unbounded)        (Thread Safe, ReentrantLock + Condition)
       |                                     |
Min-Heap Object[] Array           Min-Heap Object[] Array (Thread Safe)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite demonstrating PriorityQueue internals, custom comparators, and Top K Frequent Elements (LeetCode 347):

```java
import java.util.*;

public class PriorityQueueInternalsMaster {

    // 1. Top K Frequent Elements (LeetCode 347) O(N log K) Time, O(N) Space
    public static int[] topKFrequent(int[] nums, int k) {
        // Step 1: Count element frequencies
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);
        }

        // Step 2: Min-Heap storing numbers sorted by FREQUENCY
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(freqMap.get(a), freqMap.get(b))
        );

        // Step 3: Maintain heap of size K
        for (int num : freqMap.keySet()) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll(); // Evict smallest frequency element!
            }
        }

        // Step 4: Build output array
        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) {
            result[i] = minHeap.poll();
        }

        return result;
    }

    // 2. Kth Largest Element in an Array (LeetCode 215) O(N log K) Time, O(K) Space
    public static int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);

        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        return minHeap.peek(); // Top of Min-Heap of size K is K-th largest!
    }

    // 3. Merge K Sorted Lists (LeetCode 23) Node Reference Heap
    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a.val, b.val)
        );

        // Add head of each non-empty list to heap
        for (ListNode node : lists) {
            if (node != null) minHeap.offer(node);
        }

        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (!minHeap.isEmpty()) {
            ListNode minNode = minHeap.poll();
            curr.next = minNode;
            curr = curr.next;

            if (minNode.next != null) {
                minHeap.offer(minNode.next);
            }
        }

        return dummy.next;
    }
}
```

> **Quick Syntax:**
```java
// Maintain Heap of Size K Pattern (Keep Top K Largest)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll(); // Polls smallest element!
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 347 - Top K Frequent Elements**: Min-Heap based on frequency.
* **LeetCode 215 - Kth Largest Element in an Array**: Min-Heap of size $K$.
* **LeetCode 23 - Merge k Sorted Lists**: Priority queue storing list node references.

---

## 8. Java Code Demonstration & Dry Run
Demonstration finding Top 2 Frequent Elements and merging sorted list nodes:

```java
public class PriorityQueueInternalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Top K Frequent Elements (LeetCode 347) ===");
        int[] nums = {1, 1, 1, 2, 2, 3};
        int[] top2 = PriorityQueueInternalsMaster.topKFrequent(nums, 2);
        System.out.println("Top 2 Frequent Elements: " + Arrays.toString(top2)); // Output: [1, 2]

        System.out.println("\n=== 2. Kth Largest Element (LeetCode 215) ===");
        int[] arr = {3, 2, 1, 5, 6, 4};
        int kthLargest = PriorityQueueInternalsMaster.findKthLargest(arr, 2);
        System.out.println("2nd Largest Element: " + kthLargest); // Output: 5
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`offer(e)` / `add(e)`** | Amortized $O(\log N)$ | $O(1)$ | Sift-Up percolation |
| **`poll()`** | **$O(\log N)$ Logarithmic⚡**| $O(1)$ | Sift-Down root eviction |
| **`peek()`** | **$O(1)$ Constant ⚡** | $O(1)$ | Direct `queue[0]` read |
| **`remove(Object o)`** | **$O(N)$ Linear ❌** | $O(1)$ | Linear array search for `o` |

---

## 10. Edge Cases & Boundary Handling
* **Null Element Insertion (`pq.offer(null)`)**: Throws `NullPointerException`! Java's `PriorityQueue` DOES NOT allow `null` elements.
* **Thread Safety**: `PriorityQueue` is NOT thread-safe. Concurrent modifications throw `ConcurrentModificationException` or corrupt state. Use **`PriorityBlockingQueue`** for concurrent applications.

---

## 11. Common Mistakes & Anti-Patterns
* **Calling `pq.remove(element)` Frequently**:
  - `remove(element)` must search the underlying array linearly to find the object $\implies \mathbf{O(N)\text{ Linear Time}}$!
  - Calling `pq.remove(e)` in a loop degrades overall algorithm performance to $O(N^2)$.
* **Using `(a, b) -> a - b` with Negative Numbers**: Causes integer overflow bugs. Always use `Integer.compare(a, b)`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** `PriorityQueue.remove(o)` is $O(N)$ Linear Time!
> Beginners often assume `pq.remove(o)` runs in $O(\log N)$ time.
> Because the underlying array is a Heap (NOT a Hash Table or BST), finding an arbitrary element `o` requires searching the array linearly $\implies \mathbf{O(N)\text{ Time}}$.
> If fast arbitrary deletion is required, pair the heap with a `HashMap<Element, Index>` (Lazy Deletion or Index Min-Heap!).

> **Memory Trick:** **"PriorityQueue.remove(o) is O(N) linear! Use Integer.compare(a, b) to avoid subtraction overflow!"**

---

## 13. System & Implementation Comparisons

| Feature | `PriorityQueue` | `PriorityBlockingQueue` |
| :--- | :--- | :--- |
| **Thread Safety** | Thread Unsafe | **Thread Safe (Locking) ⚡** |
| **Null Storage** | Forbidden (`NPE`) | Forbidden (`NPE`) |
| **Concurrency Lock**| None | `ReentrantLock` + `Condition` |

---

## 14. How to Recognize This in Questions
* **"Maintain Top K largest/smallest elements dynamically in a stream"** $\rightarrow$ `PriorityQueue` of size $K$.
* **"Merge K sorted lists/arrays efficiently"** $\rightarrow$ `PriorityQueue` storing current head node of each list.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java's `PriorityQueue` growth formula use `oldCapacity + 2` when `oldCapacity < 64`?**  
  *A:* Small initial heaps (default size 11) benefit from aggressive capacity expansion to reduce the frequency of re-allocations during initial population.
* **Q: How to maintain the Top K Largest elements in a stream using a Min-Heap of size K?**  
  *A:* Keep pushing incoming numbers into a Min-Heap of size $K$. Whenever `heap.size() > K`, call `heap.poll()`. The `poll()` operation evicts the smallest element among the $K+1$ numbers, ensuring the heap always retains the $K$ LARGEST numbers!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA PRIORITYQUEUE INTERNALS                          |
+-----------------------------------------------------------------------+
| • Default Capacity: 11 | Growth: Double (+2) if <64, 50% if >=64       |
| • Default Order: Min-Heap (Smallest element at root queue[0])         |
| • Max-Heap Syntax: PriorityQueue<>(Collections.reverseOrder())        |
| • Lambda Safeguard: (a, b) -> Integer.compare(a, b) (Prevents overflow)|
| • Removal Pitfall: pq.remove(obj) is O(N) LINEAR time search! ❌       |
| • Top K Pattern: Min-Heap of size K -> poll() when size > K           |
| • Thread-Safe Alternative: PriorityBlockingQueue                      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can state the default capacity (11) and growth formula of `PriorityQueue`.
- [ ] I know why `Integer.compare(a, b)` MUST be used over `a - b`.
- [ ] I can solve Top K Frequent Elements (LeetCode 347).
- [ ] I can solve Merge K Sorted Lists (LeetCode 23).
- [ ] I know why `PriorityQueue.remove(o)` takes $O(N)$ linear time.
