# 08. Two Heaps Pattern & Dual Heap Balancing

## 1. Introduction
The **Two Heaps Pattern** is a specialized algorithmic technique designed to track running medians and order statistics over dynamic data streams. In technical coding interviews, problems such as Find Median from Data Stream (LeetCode 295) and Sliding Window Median (LeetCode 480) combine a **Max-Heap** (storing the smaller half of numbers) and a **Min-Heap** (storing the larger half of numbers) to compute median values in **$O(1)$ constant time** and process new elements in **$O(\log N)$ time**.

> **Important:** The Two Heaps Pattern partitions data into two equal (or off-by-one) halves:
> * **`maxHeap` (Max-Heap)** holds the **Smaller Half** of elements (top is maximum of small half).
> * **`minHeap` (Min-Heap)** holds the **Larger Half** of elements (top is minimum of large half).
> The running median is either the average of both roots or `maxHeap.peek()`!

## 2. Core Concepts
* **Dual Heap Invariants**:
  1. **Ordering Invariant**: Every element in `maxHeap` is $\le$ every element in `minHeap` (`maxHeap.peek() <= minHeap.peek()`).
  2. **Size Balancing Invariant**: `maxHeap.size()` is either equal to `minHeap.size()` or greater by exactly 1 (`maxHeap.size() == minHeap.size() + 1`).
* **Insertion & Balancing Pipeline (`addNum(num)`)**:
  * **Step 1 (Route)**: If `maxHeap` is empty or `num <= maxHeap.peek()`, offer to `maxHeap`. Else offer to `minHeap`.
  * **Step 2 (Rebalance)**:
    * If `maxHeap.size() > minHeap.size() + 1`: `minHeap.offer(maxHeap.poll())`.
    * If `maxHeap.size() < minHeap.size()`: `maxHeap.offer(minHeap.poll())`.
* **Median Calculation (`findMedian()`)**:
  * If `maxHeap.size() > minHeap.size()` $\implies$ `return maxHeap.peek()`.
  * Else $\implies$ `return (maxHeap.peek() + minHeap.peek()) / 2.0`.

> **Memory Trick:** **"Max-Heap for Left Small Half, Min-Heap for Right Large Half! Size off-by-one maxHeap >= minHeap!"**

## 3. Characteristics / Properties
* **$O(1)$ Median Retrieval**: Eliminates the need to re-sort an array on every stream insertion ($O(N \log N)$) or insert into an ordered list ($O(N)$).
* **Balanced Dual Partitioning**: The roots of both heaps meet at the median boundary of the stream.

```
Two Heaps Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation / Query     | Time Complexity   | Auxiliary Space   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| `addNum(num)`         | O(log N) ⚡      | O(N) Total Heap   | Route & Rebalance |
| `findMedian()`        | O(1) Constant ⚡  | O(1) Constant     | Inspect heap roots|
| Sliding Window Median | O(N log K) ⚡     | O(K) Heap Space   | Dual Heap + Evict |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Find Median from Data Stream (LeetCode 295) on `addNum(1), addNum(2), findMedian(), addNum(3), findMedian()`:

```
Init: maxHeap = [] (Max-Heap), minHeap = [] (Min-Heap)

addNum(1): 1 <= maxHeap (empty) -> maxHeap: [1], minHeap: [] (Size OK: 1 vs 0)
addNum(2): 2 > maxHeap.peek()(1) -> offer to minHeap -> maxHeap: [1], minHeap: [2] (Size OK: 1 vs 1)

findMedian(): Sizes equal -> (maxHeap.peek() + minHeap.peek()) / 2.0 = (1 + 2) / 2.0 = 1.5 ✅

addNum(3): 3 > maxHeap.peek()(1) -> minHeap: [2, 3]
           Rebalance: minHeap size (2) > maxHeap size (1)!
           maxHeap.offer(minHeap.poll(2)) -> maxHeap: [2, 1], minHeap: [3] (Size OK: 2 vs 1)

findMedian(): maxHeap.size() > minHeap.size() -> maxHeap.peek() = 2.0 ✅
```

## 5. Visual Diagram
Two Heaps Dual Partition Architecture:

```
           [ SMALLER HALF ]                  [ LARGER HALF ]
        maxHeap (Max-Heap)                minHeap (Min-Heap)
       +------------------+              +------------------+
       |   Top = 2 (MAX)  |              |   Top = 3 (MIN)  |
       |     [ 1, 2 ]     |              |      [ 3, 5 ]    |
       +------------------+              +------------------+
                 \                                /
                  +====== MEDIAN BOUNDARY =======+
                  Median = (2 + 3) / 2.0 = 2.5
```

## 6. Operations / Algorithms
LeetCode 295 Master Implementation:

```java
public class MedianFinder {
    private final PriorityQueue<Integer> maxHeap; // Smaller half
    private final PriorityQueue<Integer> minHeap; // Larger half

    public MedianFinder() {
        this.maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        this.minHeap = new PriorityQueue<>();
    }

    // O(log N) Time
    public void addNum(int num) {
        if (maxHeap.isEmpty() || num <= maxHeap.peek()) {
            maxHeap.offer(num);
        } else {
            minHeap.offer(num);
        }

        // Rebalance size invariant: maxHeap size can be equal or 1 greater than minHeap
        if (maxHeap.size() > minHeap.size() + 1) {
            minHeap.offer(maxHeap.poll());
        } else if (maxHeap.size() < minHeap.size()) {
            maxHeap.offer(minHeap.poll());
        }
    }

    // O(1) Time
    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) {
            return maxHeap.peek();
        } else {
            return (maxHeap.peek() + minHeap.peek()) / 2.0;
        }
    }
}
```

> **Quick Syntax:**
```java
// Integer Overflow Safe Average Calculation
double median = (maxHeap.size() > minHeap.size()) 
    ? maxHeap.peek() 
    : ((double) maxHeap.peek() + minHeap.peek()) / 2.0;
```

## 7. Examples
* **LeetCode 295 - Find Median from Data Stream**: Classic Two Heaps implementation.
* **LeetCode 480 - Sliding Window Median**: Two Heaps + Dual Balance Tracking for window size $K$.
* **LeetCode 502 - IPO**: Max-Heap for capital profits, Min-Heap for project capital requirements.

## 8. Java Code
Complete interview-ready Java suite implementing MedianFinder (LeetCode 295) and IPO Maximized Capital (LeetCode 502):

```java
import java.util.Collections;
import java.util.PriorityQueue;

public class TwoHeapsPatternMaster {

    // 1. Find Median from Data Stream (LeetCode 295) O(log N) Add, O(1) Find
    public static class MedianFinder {
        private final PriorityQueue<Integer> maxHeap; // Smaller half
        private final PriorityQueue<Integer> minHeap; // Larger half

        public MedianFinder() {
            this.maxHeap = new PriorityQueue<>(Collections.reverseOrder());
            this.minHeap = new PriorityQueue<>();
        }

        public void addNum(int num) {
            if (maxHeap.isEmpty() || num <= maxHeap.peek()) {
                maxHeap.offer(num);
            } else {
                minHeap.offer(num);
            }

            // Rebalance sizes
            if (maxHeap.size() > minHeap.size() + 1) {
                minHeap.offer(maxHeap.poll());
            } else if (maxHeap.size() < minHeap.size()) {
                maxHeap.offer(minHeap.poll());
            }
        }

        public double findMedian() {
            if (maxHeap.size() > minHeap.size()) {
                return maxHeap.peek();
            } else {
                return ((double) maxHeap.peek() + minHeap.peek()) / 2.0;
            }
        }
    }

    // 2. IPO Maximized Capital (LeetCode 502) O(N log N) Time, O(N) Space
    public static int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;

        // Min-Heap ordered by capital requirement
        PriorityQueue<int[]> minCapitalHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        // Max-Heap ordered by profit yield
        PriorityQueue<Integer> maxProfitHeap = new PriorityQueue<>(Collections.reverseOrder());

        for (int i = 0; i < n; i++) {
            minCapitalHeap.offer(new int[]{capital[i], profits[i]});
        }

        for (int i = 0; i < k; i++) {
            // Move all affordable projects to maxProfitHeap
            while (!minCapitalHeap.isEmpty() && minCapitalHeap.peek()[0] <= w) {
                maxProfitHeap.offer(minCapitalHeap.poll()[1]);
            }

            if (maxProfitHeap.isEmpty()) break; // No affordable projects left

            w += maxProfitHeap.poll(); // Pick project with max profit
        }

        return w;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        MedianFinder medianFinder = new MedianFinder();
        medianFinder.addNum(1);
        medianFinder.addNum(2);
        System.out.println("Median (1, 2):    " + medianFinder.findMedian()); // Output: 1.5

        medianFinder.addNum(3);
        System.out.println("Median (1, 2, 3): " + medianFinder.findMedian()); // Output: 2.0

        int[] profits = {1, 2, 3}, capital = {0, 1, 1};
        System.out.println("Maximized Capital (k=2, w=0): " + findMaximizedCapital(2, 0, profits, capital)); // Output: 4
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`addNum(num)`** | **$O(\log N)$** | $O(N)$ Heap Space | Rebalance requires 1 poll/offer |
| **`findMedian()`** | **$O(1)$ Constant ⚡**| $O(1)$ Constant | Inspect root values |
| **IPO Capital Search** | **$O(N \log N)$** | $O(N)$ Heap Space | Sort capital & max profit poll |

## 10. Edge Cases
* **Integer Overflow in Median Average**: Writing `(maxHeap.peek() + minHeap.peek()) / 2.0` can overflow if `maxHeap.peek() = Integer.MAX_VALUE`. Write `((double) maxHeap.peek() + minHeap.peek()) / 2.0` to force double precision arithmetic before addition.
* **Stream with All Identical Elements**: Equal elements route to `maxHeap` and trigger rebalancing cleanly.
* **Single Element Stream**: `findMedian()` returns `maxHeap.peek()` as double cleanly.

## 11. Common Mistakes
* Rebalancing `maxHeap.size() > minHeap.size()` without allowing `maxHeap` to be 1 element larger (causes endless bouncing between heaps!).
* Performing integer division `(a + b) / 2` returning an `int` instead of `double` `1.5` $\to$ `1.0`.
* Re-instantiating heaps on every query instead of maintaining dynamic instance heaps.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Two Heaps Partition Strategy:
> * `maxHeap` (Max-Heap) stores **Smaller Half** $\implies$ `PriorityQueue<>(Collections.reverseOrder())`
> * `minHeap` (Min-Heap) stores **Larger Half** $\implies$ `PriorityQueue<>()`
> Heap Size Constraint: **`maxHeap.size()` must equal `minHeap.size()` OR `minHeap.size() + 1`**.

> **Memory Trick:** **"Left is Max-Heap (small numbers), Right is Min-Heap (large numbers)! Max-Heap size >= Min-Heap size!"**

## 13. Comparisons
| Feature | Single Sorted ArrayList | Two Heaps Pattern |
| :--- | :--- | :--- |
| **Insertion Time** | $O(N)$ (Array shifting) | **$O(\log N)$ ⚡** |
| **Median Query Time** | $O(1)$ Direct index | **$O(1)$ Root Inspection ⚡** |
| **Overall Stream Performance**| $O(N^2)$ for $N$ inputs | **$O(N \log N)$ Total** |

## 14. How to Recognize This in Questions
* **"Find median from continuous data stream in O(1) time"** $\rightarrow$ Two Heaps Pattern (LeetCode 295).
* **"Maximize profit given capital requirements and available capital"** $\rightarrow$ Dual Heap (Min Capital + Max Profit).

## 15. Frequently Asked Interview Questions
* **Q: Why is `maxHeap` allowed to have 1 more element than `minHeap`, but not vice versa?**  
  *A:* This is an arbitrary convention to simplify odd-length stream handling. When the total number of elements is odd, `maxHeap.size()` is $N/2 + 1$ and `minHeap.size()` is $N/2$, placing the exact median at `maxHeap.peek()`.
* **Q: How does LeetCode 502 (IPO) use two heaps?**  
  *A:* `minCapitalHeap` (Min-Heap) organizes projects by capital requirement. On each turn, all projects with `capital <= w` are transferred to `maxProfitHeap` (Max-Heap). The top project from `maxProfitHeap` is picked to maximize capital growth.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO HEAPS PATTERN & DUAL HEAP BALANCING               |
+-----------------------------------------------------------------------+
| • Max-Heap (maxHeap): Stores smaller half | Top = max of small half   |
| • Min-Heap (minHeap): Stores larger half  | Top = min of large half   |
| • Invariant: maxHeap.peek() <= minHeap.peek()                         |
| • Size Rule: maxHeap.size() == minHeap.size() OR minHeap.size() + 1   |
| • Median: If maxHeap > minHeap => maxHeap.peek(); else => avg of roots|
| • Complexity: O(log N) Add | O(1) Constant Median Query               |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can set up Max-Heap (`maxHeap`) and Min-Heap (`minHeap`) for median tracking.
- [ ] I can write the route & rebalance logic for `addNum(num)`.
- [ ] I know why `((double) maxHeap.peek() + minHeap.peek()) / 2.0` prevents integer overflow.
- [ ] I can implement Find Median from Data Stream (LeetCode 295) in under 5 minutes.
- [ ] I can solve IPO Maximized Capital (LeetCode 502) using dual heaps.
