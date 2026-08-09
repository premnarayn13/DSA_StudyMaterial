# 04. PriorityQueue in Java, Comparator Invariants & Subtraction Overflow Traps

## 1. Introduction
The **`java.util.PriorityQueue<E>`** class in the Java Collections Framework provides a production-grade, array-backed Binary Heap implementation. By default, `PriorityQueue` instantiates an unbounded **Min-Heap** where elements are ordered according to their **Natural Ordering** (`Comparable`) or by an explicit **`Comparator`** passed at construction time. Mastering `PriorityQueue` API methods (`offer`, `poll`, `peek`, `remove`), custom lambda comparators, and integer overflow traps enables solving priority scheduling and top-K streaming problems in **$O(1)$ peek time and $O(\log N)$ insert/delete time**.

> **Important:** Critical Rules for `PriorityQueue` in Java:
> 1. **Default Heap Type**: `new PriorityQueue<>()` creates a **MIN-HEAP** (Smallest element at head!).
> 2. **Max-Heap Instantiation**: Pass **`Collections.reverseOrder()`** OR lambda **`(a, b) -> Integer.compare(b, a)`**!
> 3. **The Subtraction Overflow Bug**: NEVER use `(a, b) -> a - b` for custom comparators! If `a = Integer.MIN_VALUE` and `b = 1`, `a - b` overflows to `Integer.MAX_VALUE`, corrupting heap order! Always use **`Integer.compare(a, b)`**! ⚡

```
Java PriorityQueue Min-Heap vs Max-Heap Comparator Spectrum:
Min-Heap (Default) : PriorityQueue<Integer> minHeap = new PriorityQueue<>();
Max-Heap (Reverse) : PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
Lambda Max-Heap    : PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
Custom Object Heap : PriorityQueue<Pair> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
```

---

## 2. Core Concepts & `PriorityQueue` API Operations

### 2.1 API Method Complexity Matrix
Unlike standard LinkedList queues, `PriorityQueue` methods operate on a Binary Heap:

```
Java PriorityQueue Method Contract:
+-----------------------+-------------------+-------------------+-------------------+
| PriorityQueue Method  | Equivalent Action | Time Complexity   | Null / Empty Rule |
+-----------------------+-------------------+-------------------+-------------------+
| **`offer(e)` / `add(e)`**| Insert Element   | **$O(\log N)$ ⚡**| Throws NPE if `e == null`|
| **`poll()`**          | Remove Head Element| **$O(\log N)$ ⚡**| Returns `null` if empty|
| **`remove()`**        | Remove Head Element| **$O(\log N)$ ⚡**| Throws `NoSuchElementException`|
| **`peek()`**          | Inspect Head Elem | **$O(1)$ Constant ⚡**| Returns `null` if empty|
| **`element()`**       | Inspect Head Elem | **$O(1)$ Constant ⚡**| Throws `NoSuchElementException`|
| **`remove(Object o)`**| Remove Arbitrary  | **$O(N)$ Linear ❌**| Linear search scan |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"PriorityQueue offer() and poll() run in O(log N) time! peek() runs in O(1) constant time!"**

---

## 3. Characteristics & Custom Object Comparators

### 3.1 Multi-Property Sorting Comparators
When storing custom objects e.g. `Element(val, frequency)` in a `PriorityQueue`:
* Primary Sort: Frequency descending (Max-Heap by frequency).
* Secondary Sort (Tie-breaker): Value ascending (Min-Heap by value).

```java
// Production-Grade Multi-Property Comparator
PriorityQueue<Element> pq = new PriorityQueue<>((a, b) -> {
    if (a.freq != b.freq) {
        return Integer.compare(b.freq, a.freq); // Primary: Higher frequency first
    }
    return Integer.compare(a.val, b.val);       // Secondary: Smaller value first
});
```

---

## 4. Internal Working Mechanics
Tracing `PriorityQueue` Max-Heap extraction on values `[10, 50, 20]`:

```
Init Max-Heap: PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());

pq.offer(10); // Array: [10]
pq.offer(50); // Sifts up 50 -> Array: [50, 10]
pq.offer(20); // Sifts up 20 -> Array: [50, 10, 20] (Head is 50!)

pq.poll();    // Removes and returns 50! Re-heaps -> Array: [20, 10] (Head is 20!)
pq.poll();    // Removes and returns 20!

Strict Priority Order Guaranteed! ✅
```

---

## 5. Visual Diagram
Java `PriorityQueue` Resizing Array Mechanics Topography:

```
Initial Array (Cap = 11):  [ E1 | E2 | E3 | E4 | E5 | ... | E11 ]
                                            |
On Overflow (Size > Cap) : Automatically Resizes by 1.5x (or 2x if small)!
New Array (Cap = 16)     : Copy of elements into expanded contiguous memory ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite demonstrating Min-Heap, Max-Heap, Custom Object PriorityQueues, Multi-Property Comparators, and Top-K extraction:

```java
import java.util.*;

public class PriorityQueueJavaMaster {

    // Custom Record / Class for Heap Element
    public static class Pair {
        public int val;
        public int freq;

        public Pair(int val, int freq) {
            this.val = val;
            this.freq = freq;
        }

        @Override
        public String toString() {
            return "(" + val + ", freq=" + freq + ")";
        }
    }

    // 1. Min-Heap Example (Natural Ascending Order)
    public static List<Integer> minHeapDemo(int[] nums) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
        }

        List<Integer> sorted = new ArrayList<>();
        while (!minHeap.isEmpty()) {
            sorted.add(minHeap.poll()); // Extracts elements in ascending order
        }
        return sorted;
    }

    // 2. Max-Heap Example (Reverse Descending Order)
    public static List<Integer> maxHeapDemo(int[] nums) {
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int num : nums) {
            maxHeap.offer(num);
        }

        List<Integer> sorted = new ArrayList<>();
        while (!maxHeap.isEmpty()) {
            sorted.add(maxHeap.poll()); // Extracts elements in descending order
        }
        return sorted;
    }

    // 3. Multi-Property Custom Object PriorityQueue
    public static List<Pair> customPairHeap(List<Pair> pairs) {
        // Sort by Freq Descending; Tie-breaker by Val Ascending
        PriorityQueue<Pair> pq = new PriorityQueue<>((a, b) -> {
            if (a.freq != b.freq) {
                return Integer.compare(b.freq, a.freq); // Primary: Higher freq first
            }
            return Integer.compare(a.val, b.val);       // Secondary: Smaller val first
        });

        pq.addAll(pairs);

        List<Pair> result = new ArrayList<>();
        while (!pq.isEmpty()) {
            result.add(pq.poll());
        }
        return result;
    }

    // 4. Safe Comparator vs Overflow Bug Comparison
    public static int safeCompare(int a, int b) {
        return Integer.compare(a, b); // Safe against Integer overflow!
    }
}
```

> **Quick Syntax:**
```java
// Safe Max-Heap Instantiation
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
```

---

## 7. Concrete Problem Examples
* **LeetCode 347 - Top K Frequent Elements**: Max-Heap / Min-Heap by frequency.
* **LeetCode 23 - Merge k Sorted Lists**: Min-Heap priority queue of list nodes.
* **LeetCode 295 - Find Median from Data Stream**: Two Heaps (Max-Heap + Min-Heap).

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Min-Heap, Max-Heap, and Multi-Property Pair Heap:

```java
public class PriorityQueueJavaDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Min-Heap & Max-Heap Demo ===");
        int[] nums = {15, 5, 20, 10, 30};

        System.out.println("Min-Heap Ascending Output: " + 
            PriorityQueueJavaMaster.minHeapDemo(nums)); // [5, 10, 15, 20, 30]

        System.out.println("Max-Heap Descending Output: " + 
            PriorityQueueJavaMaster.maxHeapDemo(nums)); // [30, 20, 15, 10, 5]

        System.out.println("\n=== 2. Multi-Property Custom Object Heap Demo ===");
        List<PriorityQueueJavaMaster.Pair> pairs = Arrays.asList(
            new PriorityQueueJavaMaster.Pair(10, 2),
            new PriorityQueueJavaMaster.Pair(5, 5),
            new PriorityQueueJavaMaster.Pair(20, 5) // Same freq 5 as (5), but larger val 20
        );

        List<PriorityQueueJavaMaster.Pair> sortedPairs = 
            PriorityQueueJavaMaster.customPairHeap(pairs);
        System.out.println("Sorted Pairs: " + sortedPairs);
        // Output: [(5, freq=5), (20, freq=5), (10, freq=2)] ✅
    }
}
```

---

## 9. Complexity Analysis

| API Operation / Method | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`offer(e)` / `add(e)`**| **$O(\log N)$ ⚡** | $O(1)$ Amortized | Sift-up insertion |
| **`poll()` / `remove()`**| **$O(\log N)$ ⚡** | $O(1)$ Space | Sift-down extraction |
| **`peek()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Inspect `queue[0]` |
| **`remove(Object o)`** | $O(N)$ Linear ❌ | $O(1)$ Space | Linear array search + sift |
| **`contains(Object o)`**| $O(N)$ Linear ❌ | $O(1)$ Space | Linear array search |

---

## 10. Edge Cases & Boundary Handling
* **Inserting `null` Elements**: `PriorityQueue` throws `NullPointerException` immediately! `null` values are NOT allowed.
* **Mutating Objects Inside PriorityQueue**: Modifying properties of an object while it is inside a `PriorityQueue` corrupts heap order! (Re-sorting requires polling, mutating, and re-offering!).

---

## 11. Common Mistakes & Anti-Patterns
* **Using Subtraction `(a, b) -> a - b` in Comparators (Integer Overflow Bug)**:
  - If `a = -2147483648` (`Integer.MIN_VALUE`) and `b = 1`:
  - `a - b` evaluates to `2147483647` (positive!), reversing comparison logic completely!
  - **ALWAYS use `Integer.compare(a, b)` or `Long.compare(a, b)`**.
* **Calling `pq.remove(object)` Inside Loops ($O(N^2)$ Penalty)**:
  - `PriorityQueue.remove(obj)` performs a linear $O(N)$ scan to find the object before deleting.
  - **Use Lazy Deletion (ignore stale objects on `poll()`) to maintain $O(N \log N)$ total time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Modifying Objects Inside a `PriorityQueue` Fails:
> `PriorityQueue` does NOT automatically listen for state changes on contained objects!
> If you alter `pair.freq = 10` while `pair` resides in the heap, the heap structure becomes stale and corrupt.
> **Rule**: To update an element's priority:
> 1. `pq.remove(pair)` (or mark as stale for lazy deletion).
> 2. Update `pair.freq = 10`.
> 3. `pq.offer(pair)`.

> **Memory Trick:** **"NEVER use (a, b) -> a - b! Always use Integer.compare(a, b) to prevent Integer overflow!"**

---

## 13. System & Implementation Comparisons

| Feature | `java.util.PriorityQueue` | `java.util.TreeSet` |
| :--- | :--- | :--- |
| **Duplicates Allowed** | **YES (Allows Duplicate Keys)** | NO (Strictly Unique Keys) |
| **Head Access Time** | **$O(1)$ Constant ⚡** | $O(\log N)$ Logarithmic |
| **Arbitrary Removal** | $O(N)$ Linear Scan | **$O(\log N)$ Logarithmic ⚡** |

---

## 14. How to Recognize This in Questions
* **"Maintain Top K elements in a streaming dataset"** $\rightarrow$ Min-Heap `PriorityQueue` of size $K$.
* **"Merge K sorted lists/arrays into one single sorted list"** $\rightarrow$ Min-Heap `PriorityQueue` holding list head nodes.

---

## 15. Frequently Asked Interview Questions
* **Q: How does Java `PriorityQueue` resize its internal array dynamically?**  
  *A:* If capacity is $< 64$, capacity doubles ($cap + 2$). If capacity is $\ge 64$, capacity grows by 50% ($cap + (cap >> 1)$).
* **Q: Why is `PriorityQueue.contains(o)` an $O(N)$ operation?**  
  *A:* Because a heap is NOT a hash table or binary search tree. Finding an arbitrary non-root element requires a linear scan across the internal array.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA PRIORITYQUEUE & COMPARATOR RULES                 |
+-----------------------------------------------------------------------+
| • Default Instantiation: Min-Heap (Smallest element at head)          |
| • Max-Heap Instantiation: PriorityQueue<>(Collections.reverseOrder()) |
| • Safe Comparator Rule : (a, b) -> Integer.compare(a, b)             |
| • Overflow Trap        : NEVER use (a, b) -> a - b!                   |
| • Null Invariant       : PriorityQueue DOES NOT ALLOW null elements!  |
| • Complexity           : offer/poll O(log N) | peek O(1) ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can instantiate Min-Heap and Max-Heap `PriorityQueue` in Java.
- [ ] I can write multi-property custom object comparators.
- [ ] I know why `(a, b) -> a - b` causes Integer overflow bugs.
- [ ] I know why `pq.remove(obj)` takes $O(N)$ time.
- [ ] I know how lazy deletion avoids $O(N)$ removal overheads.
