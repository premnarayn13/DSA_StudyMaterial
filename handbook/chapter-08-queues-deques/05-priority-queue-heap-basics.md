# 05. Priority Queue Fundamentals & Binary Heap Architecture

## 1. Introduction
A **Priority Queue** is an abstract data type where each element has an associated priority, and elements are served in order of their priority rather than insertion order. In Java, `java.util.PriorityQueue` is backed by a **Complete Binary Min-Heap** stored as a dynamic contiguous array. In technical coding interviews, Priority Queues enable $O(\log N)$ insertions and $O(1)$ priority lookups for Top-$K$ elements, Dijkstra's Shortest Path algorithm, and Huffman Coding.

> **Important:** By default, Java's `java.util.PriorityQueue` is a **Min-Heap** (smallest element at root). To construct a **Max-Heap** (largest element at root), pass **`Collections.reverseOrder()`** or a custom lambda comparator `(a, b) -> Integer.compare(b, a)`!

## 2. Core Concepts
* **Complete Binary Heap Condition**: A binary tree filled entirely at all levels except possibly the last level, which is filled from left to right.
* **Array Index Mapping**: Stored as array `Object[] queue` without explicit node pointers:
  * **Parent Index**: $\text{parent}(i) = \frac{i - 1}{2}$
  * **Left Child Index**: $\text{left}(i) = 2i + 1$
  * **Right Child Index**: $\text{right}(i) = 2i + 2$
* **Heap Operations**:
  * **Sift-Up (`siftUp`)**: Used during `offer(val)` ($O(\log N)$ time) to float a newly added element up to its valid heap position.
  * **Sift-Down (`siftDown`)**: Used during `poll()` ($O(\log N)$ time) to sink the replaced root element down to restore heap property.

> **Memory Trick:** **"Default PriorityQueue = Min-Heap! For Max-Heap, use PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder())"**.

## 3. Characteristics / Properties
* **Min-Heap Property**: For every node $i$ (except root), $\text{val}(\text{parent}(i)) \le \text{val}(i)$. Root is ALWAYS the minimum element ($O(1)$ peek).
* **Linear Heap Construction (`Heapify`)**: Building a Min-Heap from an unsorted array of size $N$ using bottom-up sift-down takes **$O(N)$ linear time** (not $O(N \log N)$!).

```
Priority Queue / Binary Heap Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Heap Operation        | Time Complexity   | Auxiliary Space   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| `peek()` / `element()`| O(1) Constant ⚡  | O(1) Constant     | Read root index 0 |
| `offer(val)` / `add()`| O(log N)          | O(1) Constant     | Sift-Up bubble    |
| `poll()` / `remove()` | O(log N)          | O(1) Constant     | Swap root & sink  |
| Heapify Array (`N`)   | O(N) Linear ⚡    | O(N) Space         | Bottom-Up SiftDown|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Sift-Up Insertion on Min-Heap `[10, 20, 15]` when offering `5`:

```
Step 1: Append 5 at end of array -> Array: [10, 20, 15, 5] (index 3)
Step 2: Parent of index 3 is (3-1)/2 = index 1 (value 20).
        5 < 20 -> Swap index 3 & 1! Array: [10, 5, 15, 20]
Step 3: Parent of index 1 is (1-1)/2 = index 0 (value 10).
        5 < 10 -> Swap index 1 & 0! Array: [5, 10, 15, 20]

Result Heap: Root is 5 (Valid Min-Heap in O(log N) time!) ✅
```

## 5. Visual Diagram
Array-to-Binary-Tree Heap Index Layout:

```
Array Indices:     [ 0 ]         <- Root (Min Element = 5)
                  /     \
             [ 1 ]       [ 2 ]   <- Left=2(0)+1=1, Right=2(0)+2=2
            /     \
       [ 3 ]       [ 4 ]         <- Children of Index 1
```

## 6. Operations / Algorithms
Min-Heap vs Max-Heap Setup & Comparator Idioms:

```java
// 1. Min-Heap (Default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// 2. Max-Heap (Reverse Order)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// 3. Custom Object Heap (Comparator safely handling negative values)
PriorityQueue<int[]> customHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
```

> **Quick Syntax:**
```java
// Always use Integer.compare to prevent underflow!
PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
```

## 7. Examples
* **LeetCode 703 - Kth Largest Element in a Stream**: Min-Heap of size $K$.
* **LeetCode 295 - Find Median from Data Stream**: Dual Heap (Max-Heap for left half, Min-Heap for right half).
* **Dijkstra's Algorithm**: Min-Heap priority queue for minimum distance node expansion.

## 8. Java Code
Complete interview-ready Java suite implementing Kth Largest Element in a Stream (LeetCode 703) using Min-Heap:

```java
import java.util.PriorityQueue;

public class PriorityQueueHeapBasicsMaster {

    // LeetCode 703: Kth Largest Element in a Stream O(log K) per Add
    public static class KthLargest {
        private final PriorityQueue<Integer> minHeap;
        private final int k;

        public KthLargest(int k, int[] nums) {
            this.k = k;
            this.minHeap = new PriorityQueue<>(k);

            for (int num : nums) {
                add(num);
            }
        }

        public int add(int val) {
            minHeap.offer(val);

            // Maintain minHeap size to at most K
            if (minHeap.size() > k) {
                minHeap.poll(); // Evict smallest element outside Top-K
            }

            return minHeap.peek(); // Top of Min-Heap of size K is K-th largest!
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums = {4, 5, 8, 2};
        KthLargest kthLargest = new KthLargest(3, nums); // K = 3

        System.out.println("Add 3: "  + kthLargest.add(3));  // Output: 4 (Heap: [4, 5, 8])
        System.out.println("Add 5: "  + kthLargest.add(5));  // Output: 5 (Heap: [5, 5, 8])
        System.out.println("Add 10: " + kthLargest.add(10)); // Output: 5 (Heap: [5, 8, 10])
        System.out.println("Add 9: "  + kthLargest.add(9));  // Output: 8 (Heap: [8, 9, 10])
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`peek()` / Root Query** | **$O(1)$ Constant** | $O(1)$ Constant | Direct array index 0 lookup |
| **`offer(val)` / Sift-Up** | **$O(\log N)$** | $O(1)$ Constant | Tree height $\log_2 N$ |
| **`poll()` / Sift-Down** | **$O(\log N)$** | $O(1)$ Constant | Tree height $\log_2 N$ |
| **Stream Top-K Maintenance**| **$O(\log K)$ per Add**| **$O(K)$ Heap Space**| Bounded Min-Heap size $K$ |

## 10. Edge Cases
* **Empty PriorityQueue**: `poll()` and `peek()` return `null` safely (whereas `remove()` and `element()` throw `NoSuchElementException`).
* **Null Element Insertion**: Passing `null` to `PriorityQueue.offer(null)` throws `NullPointerException` (nulls forbidden in Java PQ!).
* **Comparator Underflow**: Writing `(a, b) -> a - b` crashes when `a` is large negative and `b` is positive. Use `Integer.compare(a, b)`.

## 11. Common Mistakes
* Using a Max-Heap when finding **$K$-th Largest** element (using a Min-Heap of size $K$ keeps the $K$-th largest at root in $O(\log K)$ time!).
* Writing `a - b` in custom comparators instead of `Integer.compare(a, b)`.
* Assuming iterating `PriorityQueue` via `for (int val : pq)` yields sorted elements (it iterates array in heap-array order, NOT sorted order!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** $K$-th Largest vs $K$-th Smallest Rule:
> * **To find $K$-th LARGEST element**: Use a **MIN-HEAP of size $K$**! (`minHeap.peek()` holds $K$-th largest).
> * **To find $K$-th SMALLEST element**: Use a **MAX-HEAP of size $K$**! (`maxHeap.peek()` holds $K$-th smallest).

> **Memory Trick:** **"K-th LARGEST needs MIN-HEAP of size K! K-th SMALLEST needs MAX-HEAP of size K!"**

## 13. Comparisons
| Metric | Min-Heap of Size $K$ | Sorting Entire Array ($O(N \log N)$) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \log K)$** | $O(N \log N)$ |
| **Auxiliary Space** | **$O(K)$ Heap Memory** | $O(N)$ Copy Array |
| **Stream Support** | **YES (Real-Time Add)** | NO (Static Array Only) |

## 14. How to Recognize This in Questions
* **"Find K-th largest / smallest element in stream"** $\rightarrow$ PriorityQueue of size $K$.
* **"Find median from data stream"** $\rightarrow$ Dual Heap (Max-Heap + Min-Heap).
* **"Find shortest path in weighted graph"** $\rightarrow$ Dijkstra's Algorithm using Min-Heap.

## 15. Frequently Asked Interview Questions
* **Q: Why does building a heap from an array take $O(N)$ time instead of $O(N \log N)$?**  
  *A:* Bottom-up heapify calls sift-down on nodes. Most nodes are near the leaves where height $h$ is small. Summing $n/2^{h+1} \cdot h$ across all heights converges to $O(N)$ mathematically.
* **Q: Why does iterating a `PriorityQueue` with a `for-each` loop NOT output sorted elements?**  
  *A:* The `iterator()` of `PriorityQueue` returns elements in raw internal array order (binary heap tree structure), NOT in prioritized order. To extract elements in sorted order, you MUST call `poll()` sequentially.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRIORITY QUEUE & BINARY HEAP BASICS                   |
+-----------------------------------------------------------------------+
| • Min-Heap (Default): PriorityQueue<Integer> pq = new PriorityQueue<>();|
| • Max-Heap: PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());|
| • Parent Index: (i - 1) / 2 | Left Child: 2i + 1 | Right Child: 2i + 2|
| • K-th Largest Rule: Maintain Min-Heap of size K (peek is K-th largest)|
| • Comparator Rule: Always use Integer.compare(a, b) to avoid underflow|
| • Operations: offer O(log N), poll O(log N), peek O(1) Constant       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why $K$-th Largest requires a Min-Heap of size $K$.
- [ ] I can write the parent and child index math for binary heaps.
- [ ] I know why `Integer.compare(a, b)` is mandatory in comparators.
- [ ] I can implement Kth Largest in Stream (LeetCode 703) in under 3 minutes.
- [ ] I know why `for-each` on `PriorityQueue` does NOT yield sorted output.
