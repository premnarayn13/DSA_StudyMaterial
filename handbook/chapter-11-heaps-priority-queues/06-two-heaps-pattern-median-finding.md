# 06. Two-Heaps Pattern: Continuous Median Finding & Sliding Window Streams

## 1. Introduction
The **Two-Heaps Pattern** is a landmark architectural pattern in data structures and algorithm design. It partitions a continuous stream of numbers into two halves using a **Max-Heap** (storing the smaller half of elements) and a **Min-Heap** (storing the larger half of elements). This pattern powers **Find Median from Data Stream (LeetCode 295)**, achieving **$O(\log N)$ insertion time and strict $O(1)$ constant time median queries**, as well as **Sliding Window Median (LeetCode 480)**.

> **Important:** In the Two-Heaps pattern:
> * `maxHeap` (Small Half): Stores the smaller $N/2$ elements. `maxHeap.peek()` gives the **Largest of the Small Half**.
> * `minHeap` (Large Half): Stores the larger $N/2$ elements. `minHeap.peek()` gives the **Smallest of the Large Half**.
> * **Median Computation**: If total elements $N$ is EVEN, $\text{Median} = \frac{\text{maxHeap.peek()} + \text{minHeap.peek()}}{2.0}$. If $N$ is ODD, $\text{Median} = \text{maxHeap.peek()}$ (when `maxHeap` holds 1 extra element).

```
Two-Heaps Stream Partitioning Topology:
+-----------------------------------------------------------------------------------+
| Max-Heap (Small Half) : Stores [1, 2, 3]  -> maxHeap.peek() = 3 (Max of Small) ⚡  |
| Min-Heap (Large Half) : Stores [4, 5, 6]  -> minHeap.peek() = 4 (Min of Large) ⚡  |
| Stream Balance Invariant: maxHeap.size() == minHeap.size() OR maxHeap.size()+1    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Stream Balance Invariants

### 2.1 Heap Size Balance Rules
To ensure the median is accessible in $O(1)$ constant time at the roots of both heaps:
1. **Size Invariant**: `maxHeap.size()` MUST equal `minHeap.size()` (when total elements $N$ is even), OR `maxHeap.size() == minHeap.size() + 1` (when total elements $N$ is odd).
2. **Order Invariant**: Every element in `maxHeap` MUST be $\le$ every element in `minHeap`:

$$\forall x \in \text{maxHeap}, \forall y \in \text{minHeap}, \quad x \le y \implies \mathbf{\text{maxHeap.peek()} \le \text{minHeap.peek()}}$$

### 2.2 Algorithm for `addNum(int num)`
1. **Initial Insertion**:
   - Push `num` into `maxHeap` (`maxHeap.offer(num)`).
2. **Order Balance Check**:
   - Transfer top of `maxHeap` to `minHeap` (`minHeap.offer(maxHeap.poll())`).
3. **Size Rebalancing**:
   - If `minHeap.size() > maxHeap.size()`, rebalance by moving top of `minHeap` back to `maxHeap` (`maxHeap.offer(minHeap.poll())`).

```
Add Number Step Summary:
Step 1: Offer to maxHeap.
Step 2: Balance Order -> minHeap.offer(maxHeap.poll()).
Step 3: Balance Size  -> if (minHeap.size() > maxHeap.size()) maxHeap.offer(minHeap.poll()).
```

### 2.3 Algorithm for `findMedian()`
* If `maxHeap.size() > minHeap.size()`:
  $$\text{Median} = \mathbf{\text{maxHeap.peek()}}$$
* Else (`maxHeap.size() == minHeap.size()`):
  $$\text{Median} = \mathbf{\frac{\text{maxHeap.peek()} + \text{minHeap.peek()}}{2.0}}$$

> **Memory Trick:** **"maxHeap stores smaller half; minHeap stores larger half! Always push to maxHeap first, then balance to minHeap!"**

---

## 3. Characteristics & Sliding Window Median (LeetCode 480)

### 3.1 The $O(N \log K)$ Removal Problem in Sliding Window Median
In Sliding Window Median (LeetCode 480), a window of size $K$ slides across an array of length $N$. As the window shifts, the outgoing element $E_{\text{out}}$ must be REMOVED from the heaps.
* Standard `PriorityQueue.remove(Object o)` takes **$O(K)$ linear time search**, degrading sliding window median performance to $O(N \cdot K)$ time!

### 3.2 Solutions for Fast Removal in Sliding Window
1. **Lazy Deletion with Hash Map ($O(N \log K)$ Time)**:
   - Mark outgoing elements in a `HashMap<Integer, Integer> lazyInvalid` map instead of deleting immediately.
   - When a peeked element at `maxHeap.peek()` or `minHeap.peek()` is marked invalid, `poll()` and prune it lazily!
2. **Dual TreeMap Balance ($O(N \log K)$ Time)**:
   - Use `TreeMap<Integer, Integer>` for `small` and `large` partitions, tracking element frequencies for $O(\log K)$ insertions and $O(\log K)$ deletions!

```
Sliding Window Median Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Implementation Style  | Insert Time       | Delete Outgoing   | Median Time       |
+-----------------------+-------------------+-------------------+-------------------+
| Standard Heaps + Remove| $O(\log K)$      | **$O(K)$ Linear❌**| $O(1)$ Constant   |
| Lazy Deletion Heaps   | $O(\log K)$       | **$O(\log K)$ ⚡** | $O(1)$ Amortized  |
| Dual TreeMap Strategy | $O(\log K)$       | **$O(\log K)$ ⚡** | $O(\log K)$      |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing `addNum` stream `[5, 15, 1, 3]` on Two-Heaps Median Finder:

```
Init: maxHeap = [], minHeap = []

1. addNum(5):
   - maxHeap.offer(5) -> maxHeap: [5]
   - minHeap.offer(maxHeap.poll()) -> maxHeap: [], minHeap: [5]
   - Rebalance: minHeap.size() > maxHeap.size() -> maxHeap.offer(minHeap.poll())
   Result: maxHeap = [5], minHeap = [] | Median = 5.0

2. addNum(15):
   - maxHeap.offer(15) -> maxHeap: [15, 5]
   - minHeap.offer(maxHeap.poll()) -> maxHeap: [5], minHeap: [15]
   - Rebalance: maxHeap.size() == minHeap.size() (1 == 1)
   Result: maxHeap = [5], minHeap = [15] | Median = (5 + 15)/2.0 = 10.0

3. addNum(1):
   - maxHeap.offer(1) -> maxHeap: [5, 1]
   - minHeap.offer(maxHeap.poll()) -> maxHeap: [1], minHeap: [5, 15]
   - Rebalance: minHeap > maxHeap -> maxHeap.offer(minHeap.poll())
   Result: maxHeap = [5, 1], minHeap = [15] | Median = 5.0 (maxHeap.peek())

4. addNum(3):
   - maxHeap.offer(3) -> maxHeap: [5, 1, 3]
   - minHeap.offer(maxHeap.poll()) -> maxHeap: [3, 1], minHeap: [5, 15]
   - Rebalance: maxHeap.size() == minHeap.size() (2 == 2)
   Result: maxHeap = [3, 1], minHeap = [5, 15] | Median = (3 + 5)/2.0 = 4.0 ✅
```

---

## 5. Visual Diagram
Two-Heaps Stream Partitioning & Median Peak Alignment Topology:

```
Stream Elements (Sorted Order): [ 1,  3,  5  |  15, 20, 25 ]
                                |----------|  |-----------|
                                 Small Half    Large Half

Max-Heap (Small Half):          ( 5 ) <--- maxHeap.peek() = 5
                               /     \
                             ( 3 )   ( 1 )

Min-Heap (Large Half):          ( 15 ) <--- minHeap.peek() = 15
                               /      \
                             ( 20 )   ( 25 )

Median = (maxHeap.peek() + minHeap.peek()) / 2.0 = (5 + 15) / 2.0 = 10.0 ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Find Median from Data Stream (LeetCode 295) and Sliding Window Median (LeetCode 480):

```java
import java.util.*;

public class TwoHeapsMaster {

    // 1. Find Median from Data Stream (LeetCode 295) O(log N) Add, O(1) Median
    public static class MedianFinder {
        private final PriorityQueue<Integer> maxHeap; // Small half (Max-Heap)
        private final PriorityQueue<Integer> minHeap; // Large half (Min-Heap)

        public MedianFinder() {
            maxHeap = new PriorityQueue<>(Collections.reverseOrder());
            minHeap = new PriorityQueue<>();
        }

        // Adds a number into the data structure. O(log N) Time
        public void addNum(int num) {
            maxHeap.offer(num);

            // Step 1: Enforce order invariant (maxHeap.peek() <= minHeap.peek())
            minHeap.offer(maxHeap.poll());

            // Step 2: Enforce size invariant (maxHeap.size() >= minHeap.size())
            if (minHeap.size() > maxHeap.size()) {
                maxHeap.offer(minHeap.poll());
            }
        }

        // Returns the median of all elements so far. O(1) Time
        public double findMedian() {
            if (maxHeap.size() > minHeap.size()) {
                return maxHeap.peek();
            } else {
                // Cast to double before addition to prevent integer overflow!
                return ((double) maxHeap.peek() + (double) minHeap.peek()) / 2.0;
            }
        }
    }

    // 2. Sliding Window Median (LeetCode 480) O(N log K) Time, O(K) Space (Dual TreeMap Strategy)
    public static class SlidingWindowMedian {
        private final TreeMap<Integer, Integer> small = new TreeMap<>();
        private final TreeMap<Integer, Integer> large = new TreeMap<>();
        private int smallSize = 0;
        private int largeSize = 0;

        public double[] medianSlidingWindow(int[] nums, int k) {
            int n = nums.length;
            double[] result = new double[n - k + 1];

            for (int i = 0; i < n; i++) {
                add(nums[i]);

                if (i >= k - 1) {
                    result[i - k + 1] = getMedian(k);
                    remove(nums[i - k + 1]); // Remove outgoing element
                }
            }

            return result;
        }

        private void add(int val) {
            if (smallSize == 0 || val <= small.lastKey()) {
                small.put(val, small.getOrDefault(val, 0) + 1);
                smallSize++;
            } else {
                large.put(val, large.getOrDefault(val, 0) + 1);
                largeSize++;
            }
            rebalance();
        }

        private void remove(int val) {
            if (small.containsKey(val)) {
                removeMapKey(small, val);
                smallSize--;
            } else {
                removeMapKey(large, val);
                largeSize--;
            }
            rebalance();
        }

        private void rebalance() {
            if (smallSize > largeSize + 1) {
                int val = small.lastKey();
                removeMapKey(small, val);
                smallSize--;
                large.put(val, large.getOrDefault(val, 0) + 1);
                largeSize++;
            } else if (smallSize < largeSize) {
                int val = large.firstKey();
                removeMapKey(large, val);
                largeSize--;
                small.put(val, small.getOrDefault(val, 0) + 1);
                smallSize++;
            }
        }

        private double getMedian(int k) {
            if (k % 2 == 1) {
                return (double) small.lastKey();
            } else {
                return ((double) small.lastKey() + (double) large.firstKey()) / 2.0;
            }
        }

        private void removeMapKey(TreeMap<Integer, Integer> map, int val) {
            int count = map.get(val);
            if (count == 1) map.remove(val);
            else map.put(val, count - 1);
        }
    }
}
```

> **Quick Syntax:**
```java
// Prevent 32-bit Integer Overflow on Median Addition
return ((double) maxHeap.peek() + (double) minHeap.peek()) / 2.0;
```

---

## 7. Concrete Problem Examples
* **LeetCode 295 - Find Median from Data Stream**: Classic Two-Heaps stream median.
* **LeetCode 480 - Sliding Window Median**: $O(N \log K)$ window median calculation.
* **LeetCode 502 - IPO (Capital / Profit Optimization)**: Dual heap project selection.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing MedianFinder and SlidingWindowMedian:

```java
public class TwoHeapsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Find Median from Data Stream (LeetCode 295) ===");
        TwoHeapsMaster.MedianFinder mf = new TwoHeapsMaster.MedianFinder();

        mf.addNum(1);
        mf.addNum(2);
        System.out.println("Median after [1, 2]: " + mf.findMedian()); // Output: 1.5

        mf.addNum(3);
        System.out.println("Median after [1, 2, 3]: " + mf.findMedian()); // Output: 2.0

        System.out.println("\n=== 2. Sliding Window Median (LeetCode 480, K = 3) ===");
        TwoHeapsMaster.SlidingWindowMedian swm = new TwoHeapsMaster.SlidingWindowMedian();
        int[] nums = {1, 3, -1, -3, 5, 3, 6, 7};
        double[] medians = swm.medianSlidingWindow(nums, 3);
        System.out.println("Sliding Window Medians: " + Arrays.toString(medians)); // Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    }
}
```

---

## 9. Complexity Analysis

| Two-Heaps Operation | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **`addNum(val)` (295)** | **$O(\log N)$ Logarithmic⚡**| $O(N)$ Heap Memory | Max-Heap offer + Min-Heap balance |
| **`findMedian()` (295)** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Peeks `maxHeap.peek()` & `minHeap.peek()` |
| **Sliding Window (480)**| **$O(N \log K)$ Time ⚡** | $O(K)$ Window Space | Dual `TreeMap` balance $O(\log K)$ deletion |

---

## 10. Edge Cases & Boundary Handling
* **32-Bit Integer Overflow in Median Calculation**:
  - `(maxHeap.peek() + minHeap.peek()) / 2.0` can overflow 32-bit `int` if both elements are near `Integer.MAX_VALUE`!
  - **Fix**: Cast to `double` BEFORE addition: `((double) maxHeap.peek() + (double) minHeap.peek()) / 2.0`.
* **Single Element Stream**: `maxHeap.size() == 1, minHeap.size() == 0` $\implies$ returns `maxHeap.peek()`.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting the Size Rebalancing Step**:
  - `minHeap` must never be larger than `maxHeap`. If `minHeap.size() > maxHeap.size()`, move `minHeap.poll()` to `maxHeap`.
* **Calling `PriorityQueue.remove(outgoing)` in Sliding Window**:
  - Calling `pq.remove(val)` on every sliding window step takes $O(K)$ linear search time, degrading total time to $O(N \cdot K)$. Always use **Lazy Deletion** or **Dual TreeMaps** for $O(N \log K)$ performance!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Two-Heaps Alignment Invariant:
> 1. `maxHeap` stores **Smaller Half** (Max of small half at root).
> 2. `minHeap` stores **Larger Half** (Min of large half at root).
> 3. `maxHeap.size() >= minHeap.size()` ALWAYS!

> **Memory Trick:** **"Cast to double BEFORE addition to prevent median overflow! Dual TreeMap enables O(log K) deletion!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard PriorityQueue Two-Heaps | Dual TreeMap Strategy |
| :--- | :--- | :--- |
| **Median Time** | **Strict $O(1)$ Constant ⚡** | $O(\log K)$ |
| **Arbitrary Removal**| $O(K)$ Linear ❌ | **$O(\log K)$ Logarithmic ⚡** |
| **Best Use Case** | Continuous Stream (LeetCode 295) | Sliding Window (LeetCode 480) |

---

## 14. How to Recognize This in Questions
* **"Find median from a continuous stream of data dynamically"** $\rightarrow$ LeetCode 295 (Two-Heaps: `maxHeap` small, `minHeap` large).
* **"Find median of every contiguous subarray of size K"** $\rightarrow$ LeetCode 480 (Dual TreeMap / Lazy Deletion Heaps).

---

## 15. Frequently Asked Interview Questions
* **Q: Why do we push incoming numbers into `maxHeap` first before balancing to `minHeap`?**  
  *A:* Because `maxHeap` acts as the entry filter. By pushing to `maxHeap` and immediately transferring `maxHeap.poll()` to `minHeap`, we ensure that the largest element among the small half moves to the large half, maintaining the order invariant $\text{maxHeap.peek()} \le \text{minHeap.peek()}$.
* **Q: How does Lazy Deletion work in Sliding Window Median?**  
  *A:* Instead of searching the priority queue array linearly to delete an outgoing element, we increment its count in a `lazyMap`. During subsequent `peek()` calls, if the root element exists in `lazyMap`, we poll and decrement `lazyMap` count until a valid non-deleted root is at the top.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO-HEAPS PATTERN (CONTINUOUS MEDIAN & SLIDING WINDOW)|
+-----------------------------------------------------------------------+
| • Two-Heaps Mapping: maxHeap (Small Half) & minHeap (Large Half)      |
| • Size Invariant: maxHeap.size() == minHeap.size() OR minHeap.size()+1|
| • Order Invariant: maxHeap.peek() <= minHeap.peek()                   |
| • Add Routine: maxHeap.offer(x) -> minHeap.offer(maxHeap.poll()) ->    |
|   if (minHeap.size() > maxHeap.size()) maxHeap.offer(minHeap.poll())  |
| • Median Rule: Odd -> maxHeap.peek() | Even -> ((double)max + min)/2.0|
| • Overflow Guard: Cast to (double) BEFORE adding peak values!         |
| • Sliding Window (480): Dual TreeMap for O(log K) removal             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `MedianFinder` (LeetCode 295) from memory in 3 minutes.
- [ ] I know why `(max + min) / 2.0` can overflow without `(double)` casting.
- [ ] I know why `maxHeap` stores the small half and `minHeap` stores the large half.
- [ ] I can solve Sliding Window Median (LeetCode 480) using Dual TreeMaps.
- [ ] I know how Lazy Deletion eliminates $O(K)$ removal overhead.
