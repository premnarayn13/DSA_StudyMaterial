# 07. Two Heaps Pattern, Continuous Stream Median & Dual-Heap Balancing Invariants

## 1. Introduction
The **Two Heaps Pattern** divides a dataset into two halves to continuously track partition statistics (such as the **Median**) in dynamic data streams. By pairing a **Max-Heap (`small`)** to store the smaller half of numbers with a **Min-Heap (`large`)** to store the larger half of numbers, algorithms like **Find Median from Data Stream (LeetCode 295)**, **Sliding Window Median (LeetCode 480)**, and **IPO (LeetCode 502)** compute running medians in **$O(1)$ Time** while processing insertions in **$O(\log N)$ Time**.

> **Important:** The Two Invariants of Dual-Heap Median Balancing (LeetCode 295):
> 1. **Partition Ordering Invariant**: EVERY element in `small` (Max-Heap) MUST be less than or equal to EVERY element in `large` (Min-Heap):
>    $$\forall x \in \text{small}, \quad \forall y \in \text{large}, \quad x \le y \implies \mathbf{\text{small.peek}() \le \text{large.peek}()}$$
> 2. **Size Balancing Invariant**: The size of `small` (Max-Heap) is allowed to be equal to or AT MOST 1 greater than `large` (Min-Heap):
>    $$\mathbf{0 \le \text{small.size}() - \text{large.size}() \le 1}$$ ⚡

```
Two Heaps Dual-Partition Topology:
Smaller Half Elements (Max-Heap 'small'):   Larger Half Elements (Min-Heap 'large'):
          [ Max: 5 ]  <======================>  [ Min: 10 ]
         /          \                         /           \
     [ 2 ]          [ 3 ]                 [ 15 ]          [ 20 ]

Median Calculation:
- If Total Elements is ODD  : Median = small.peek() (Val 5)
- If Total Elements is EVEN : Median = (small.peek() + large.peek()) / 2.0 = (5 + 10) / 2.0 = 7.5! ⚡
```

---

## 2. Core Concepts & Dual-Heap Balancing Protocol

### 2.1 Dual-Heap Insertion & Balancing Protocol
When a new value `num` arrives in `addNum(num)`:
1. **Insertion Phase**:
   - If `small.isEmpty()` OR `num <= small.peek()`: `small.offer(num)`.
   - Else: `large.offer(num)`.
2. **Re-balancing Phase** (Restore Size Invariant $0 \le \text{small.size}() - \text{large.size}() \le 1$):
   - If `small.size() > large.size() + 1`:
     `large.offer(small.poll())`!
   - If `small.size() < large.size()`:
     `small.offer(large.poll())`!

```
Dual-Heap Operational Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation / Method    | Average Time      | Worst Case Time   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **`addNum(num)`**     | **$O(\log N)$ ⚡**| **$O(\log N)$ ⚡**| $O(N)$ Space      |
| **`findMedian()`**    | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ Space      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Small Max-Heap holds lower half; Large Min-Heap holds upper half! Small size can be 0 or 1 greater than Large!"**

---

## 3. Characteristics & Maximizing Capital (LeetCode 502 IPO)

### 3.1 Two Heaps for Maximizing Capital (LeetCode 502 IPO)
Given initial capital $W$, projects with `(capital[i], profit[i])`, and $K$ selections:
* **Min-Heap `minCapital`**: Ordered by `capital[i]` ascending. Holds unfeasible projects.
* **Max-Heap `maxProfit`**: Ordered by `profit[i]` descending. Holds currently affordable projects!
* **Algorithm**:
  1. Move all projects from `minCapital` where `capital <= W` into `maxProfit`.
  2. If `maxProfit.isEmpty()`, stop.
  3. `W += maxProfit.poll().profit`. Repeat $K$ times!

---

## 4. Internal Working Mechanics
Tracing Find Median from Data Stream (LeetCode 295) on `addNum(1)`, `addNum(2)`, `addNum(3)`:

```
Step 1: addNum(1) -> small: [1], large: [].
  - Sizes: small=1, large=0. Valid!
  - findMedian() = 1.0 (Odd total).

Step 2: addNum(2) -> 2 > small.peek(1) -> large: [2].
  - Heap State: small: [1] (Max-Heap), large: [2] (Min-Heap).
  - Sizes: small=1, large=1. Valid!
  - findMedian() = (1 + 2) / 2.0 = 1.5 (Even total).

Step 3: addNum(3) -> 3 > small.peek(1) -> large: [2, 3].
  - Sizes: small=1, large=2 -> Rebalance! large.poll() (2) offered to small!
  - Heap State: small: [2, 1], large: [3].
  - Sizes: small=2, large=1. Valid!
  - findMedian() = small.peek() = 2.0 (Odd total)!

Median calculated in O(1) Time at every step! ✅
```

---

## 5. Visual Diagram
Dual-Heap Partition Balancing Mechanics Topography:

```
Odd Total Elements (Median = small.peek()):
          small (Max-Heap, Size=3)               large (Min-Heap, Size=2)
             [ Head: 5 (MEDIAN!) ]              [ Head: 8 ]

Even Total Elements (Median = (small.peek() + large.peek()) / 2.0):
          small (Max-Heap, Size=2)               large (Min-Heap, Size=2)
             [ Head: 5 ] <====================> [ Head: 8 ]
                               Median = (5 + 8) / 2.0 = 6.5! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Find Median from Data Stream (LeetCode 295) and IPO Maximizing Capital (LeetCode 502):

```java
import java.util.*;

public class TwoHeapsPatternMaster {

    // 1. Find Median from Data Stream (LeetCode 295) O(log N) add, O(1) median
    public static class MedianFinder {
        private final PriorityQueue<Integer> small; // Max-Heap for lower half
        private final PriorityQueue<Integer> large; // Min-Heap for upper half

        public MedianFinder() {
            this.small = new PriorityQueue<>(Collections.reverseOrder()); // Max-Heap
            this.large = new PriorityQueue<>();                            // Min-Heap
        }

        public void addNum(int num) {
            // Step 1: Insert into appropriate heap
            if (small.isEmpty() || num <= small.peek()) {
                small.offer(num);
            } else {
                large.offer(num);
            }

            // Step 2: Rebalance heap sizes so 0 <= small.size() - large.size() <= 1
            if (small.size() > large.size() + 1) {
                large.offer(small.poll());
            } else if (small.size() < large.size()) {
                small.offer(large.poll());
            }
        }

        public double findMedian() {
            if (small.size() > large.size()) {
                return small.peek(); // Odd total elements
            } else {
                return (small.peek() + (double) large.peek()) / 2.0; // Even total
            }
        }
    }

    // 2. IPO Maximizing Capital (LeetCode 502) O(N log N + K log N) Time
    public static int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;

        // Min-Heap ordered by capital requirements
        PriorityQueue<int[]> minCapital = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        // Max-Heap ordered by profits
        PriorityQueue<Integer> maxProfit = new PriorityQueue<>(
            Collections.reverseOrder()
        );

        for (int i = 0; i < n; i++) {
            minCapital.offer(new int[]{capital[i], profits[i]});
        }

        // Select up to k projects
        for (int i = 0; i < k; i++) {
            // Move all affordable projects from minCapital to maxProfit
            while (!minCapital.isEmpty() && minCapital.peek()[0] <= w) {
                maxProfit.offer(minCapital.poll()[1]);
            }

            if (maxProfit.isEmpty()) {
                break; // No more affordable projects available!
            }

            w += maxProfit.poll(); // Select project with highest profit
        }

        return w;
    }
}
```

> **Quick Syntax:**
```java
// Dual-Heap Rebalancing Block
if (small.size() > large.size() + 1) large.offer(small.poll());
else if (small.size() < large.size()) small.offer(large.poll());
```

---

## 7. Concrete Problem Examples
* **LeetCode 295 - Find Median from Data Stream**: Dual-Heap running median.
* **LeetCode 480 - Sliding Window Median**: Dual-Heap sliding window with lazy deletion.
* **LeetCode 502 - IPO**: Min-Capital Heap + Max-Profit Heap.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `MedianFinder` and `findMaximizedCapital`:

```java
public class TwoHeapsPatternDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Find Median from Data Stream (LeetCode 295) ===");
        TwoHeapsPatternMaster.MedianFinder mf = new TwoHeapsPatternMaster.MedianFinder();

        mf.addNum(1);
        mf.addNum(2);
        System.out.println("Median after [1, 2]: " + mf.findMedian()); // Output: 1.5

        mf.addNum(3);
        System.out.println("Median after [1, 2, 3]: " + mf.findMedian()); // Output: 2.0 ✅

        System.out.println("\n=== 2. IPO Maximizing Capital (LeetCode 502) ===");
        int[] profits = {1, 2, 3};
        int[] capital = {0, 1, 1};
        int finalCapital = TwoHeapsPatternMaster.findMaximizedCapital(2, 0, profits, capital);
        System.out.println("Maximized Capital: " + finalCapital); // Output: 4 (Projects 0 then 2) ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | `add` / Insert Time | Query Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Data Stream Median (295)**| **$O(\log N)$ ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Space | Dual-Heap size balancing |
| **IPO Capital (502)** | **$O(N \log N)$ ⚡** | **$O(K \log N)$ ⚡** | $O(N)$ Space | Min-Capital + Max-Profit Heaps |
| **Naive Sorted List Median**| $O(N)$ | $O(1)$ Space | $O(N)$ Space | Linear insertion sort |

---

## 10. Edge Cases & Boundary Handling
* **Floating-Point Division in Median**: Casting `(double) large.peek()` prevents integer division truncations (e.g. `(1 + 2) / 2 = 1`, but `(1 + 2) / 2.0 = 1.5`).
* **Insufficient Projects in IPO**: Handled cleanly by `if (maxProfit.isEmpty()) break`.

---

## 11. Common Mistakes & Anti-Patterns
* **Allowing Size Disparity Between `small` and `large`**:
  - Letting `small.size() - large.size() > 1` causes `small.peek()` to represent a non-median value.
  - **Enforce strict balancing: `0 <= small.size() - large.size() <= 1`**.
* **Integer Division Truncation `(a + b) / 2`**:
  - Writing `(small.peek() + large.peek()) / 2` returns an `int`, stripping the `.5` decimal!
  - **Always divide by `2.0` or cast to `double`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Dual-Heap Balancing Contract:
> 1. `small` (Max-Heap) stores elements $\le \text{median}$.
> 2. `large` (Min-Heap) stores elements $> \text{median}$.
> 3. After every insertion, ensure `small.size()` is either EQUAL TO or 1 GREATER THAN `large.size()`.
> 4. `findMedian()` executes in **$O(1)$ constant time** by querying heap heads!

> **Memory Trick:** **"Small Max-Heap head is lower median; Large Min-Heap head is upper median!"**

---

## 13. System & Implementation Comparisons

| Feature | Two Heaps Pattern | Single Balanced BST (`TreeSet`) |
| :--- | :--- | :--- |
| **Find Median Time** | **$O(1)$ Constant ⚡** | $O(\log N)$ or Iterator Step |
| **Duplicate Keys** | **Supports Duplicates ⚡** | Ignores Duplicates |
| **Add Element Time** | **$O(\log N)$ ⚡** | $O(\log N)$ |

---

## 14. How to Recognize This in Questions
* **"Find running median of a data stream"** $\rightarrow$ LeetCode 295 (Max-Heap `small` + Min-Heap `large`).
* **"Maximize profit given capital constraints"** $\rightarrow$ LeetCode 502 (Min-Capital Heap + Max-Profit Heap).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `MedianFinder` use a Max-Heap for the smaller half and a Min-Heap for the larger half?**  
  *A:* Because the median sits at the boundary between the two halves. The MAX element of the smaller half (`small.peek()`) and the MIN element of the larger half (`large.peek()`) form the exact median boundary.
* **Q: How does Sliding Window Median (LeetCode 480) handle window elements eviction?**  
  *A:* By using Dual-Heaps combined with **Lazy Deletion** (storing evicted elements in a frequency map and purging them from heap tops when they reach `peek()`).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO HEAPS PATTERN & RUNNING MEDIAN                    |
+-----------------------------------------------------------------------+
| • Dual-Heap Setup: Max-Heap 'small' (lower half) + Min-Heap 'large' (upper half)|
| • Size Rule      : 0 <= small.size() - large.size() <= 1             |
| • Odd Total      : Median = small.peek()                              |
| • Even Total     : Median = (small.peek() + large.peek()) / 2.0       |
| • Division Trap  : Use 2.0 to prevent integer truncation!             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Find Median from Data Stream (LeetCode 295) in $O(1)$ median time.
- [ ] I can write IPO Maximizing Capital (LeetCode 502).
- [ ] I know why small uses Max-Heap and large uses Min-Heap.
- [ ] I know how to enforce size balance `0 <= small.size() - large.size() <= 1`.
- [ ] I know why dividing by `2.0` prevents median truncation bugs.
