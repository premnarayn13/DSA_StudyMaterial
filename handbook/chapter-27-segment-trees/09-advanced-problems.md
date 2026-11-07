# 09. Advanced Segment Tree Problems: Count of Smaller After Self (LeetCode 315) & Falling Squares

## 1. Introduction
**Advanced Segment Tree Problems** combine Segment Trees with **Coordinate Compression**, **Dynamic Lazy Range Updates**, and **Coordinate Offset Mapping** to solve complex hard-level algorithmic challenges. Problems like **Count of Smaller Numbers After Self (LeetCode 315 - Frequency Segment Tree)**, **Falling Squares (LeetCode 699 - Dynamic Max Range Update)**, and **Count of Range Sum (LeetCode 327)** execute in **$O(N \log N)$ Time** and **$O(N)$ Auxiliary Space**, outperforming naive $O(N^2)$ brute-force solutions.

> **Important:** Why Coordinate Compression Enables Segment Trees on Arbitrary Value Ranges (LeetCode 315):
> Input values in LeetCode 315 can range from $-10^9$ to $+10^9$.
> 1. **Coordinate Compression Strategy**: Sort all unique input values and map them to compressed rank indices $0 \dots U-1$ ($U \le N$).
> 2. **Frequency Segment Tree**: Traverse array backwards from right to left ($i = N-1 \dots 0$). For number $X$ with rank $R$:
>    - Query count of smaller numbers in range $[0 \dots R-1]$ in **$O(\log N)$ time**!
>    - Increment frequency count at rank $R$ by $+1$ in **$O(\log N)$ time**! 3. Total Time: **$O(N \log N)$ Time**, Space: **$O(N)$ Space**! ⚡

```
LeetCode 315 Count of Smaller After Self Pipeline Topology:
Input Array = [5, 2, 6, 1] ---> Sorted Unique Ranks: [1 (Rank 0), 2 (Rank 1), 5 (Rank 2), 6 (Rank 3)]

Traverse Right-to-Left:
1. Process 1 (Rank 0): Query Range [0...-1] -> Sum = 0. Insert Rank 0 (+1). Result for 1 = 0.
2. Process 6 (Rank 3): Query Range [0...2]  -> Sum = 1. Insert Rank 3 (+1). Result for 6 = 1.
3. Process 2 (Rank 1): Query Range [0...0]  -> Sum = 1. Insert Rank 1 (+1). Result for 2 = 1.
4. Process 5 (Rank 2): Query Range [0...1]  -> Sum = 2. Insert Rank 2 (+1). Result for 5 = 2.

Final Result = [2, 1, 1, 0]! Executed in O(N log N) time! ⚡
```

---

## 2. Core Concepts & LeetCode 315 Coordinate Compression Architecture

### 2.1 LeetCode 315 Frequency Segment Tree Algorithm
1. Extract and sort unique values from `nums[]` to create `uniqueSorted[]`.
2. Map each original number to its compressed 0-indexed rank: `getRank(val) = binarySearch(uniqueSorted, val)`.
3. Construct a Frequency Segment Tree over range $[0 \dots U-1]$ initialized to 0.
4. Traverse `nums[]` backwards from $i = N-1$ down to $0$:
   - `int rank = getRank(nums[i])`.
   - `int smallerCount = query(0, rank - 1)` (Query sum of all frequencies smaller than rank!).
   - `result.add(0, smallerCount)`.
   - `update(rank, +1)` (Increment frequency at rank $R$).
5. Return `result`.

```
Advanced Segment Tree Pattern Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Smaller After (315)**| Compression + Freq| **$O(N \log N)$ ⚡**| $O(N)$ Tree Space |
| **Falling Squares (699)**| Lazy Range Max Update| **$O(N \log N)$ ⚡**| $O(N)$ Tree Space |
| **Skyline Problem (218)**| Range Max Update| **$O(N \log N)$ ⚡**| $O(N)$ Tree Space |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 315: Compress coordinates to ranks 0...U-1 -> Traverse right-to-left -> Query sum [0...rank-1] -> Update rank!"**

---

## 3. Characteristics & Falling Squares (LeetCode 699)

### 3.1 Falling Squares (LeetCode 699 - Range Max Update)
Squares fall onto 2D space. Each square has `[left, sideLength]`, occupying interval `[left ... left + sideLength - 1]`.
* **Goal**: Maintain max height over active interval.
* **Mechanism**:
  - Compress all X-coordinates.
  - Query maximum height in range `[L ... R]`: `maxH = queryMax(L, R)`.
  - Update range `[L ... R]` to new height `maxH + sideLength` using Lazy Propagation!
  - Record max global height after each block falls in **$O(N \log N)$ Time**.

---

## 4. Internal Working Mechanics
Tracing Count of Smaller Numbers After Self (LeetCode 315) on `[5, 2, 6, 1]`:

```
Input: nums = [5, 2, 6, 1].

Step 1: Coordinate Compression:
- Sorted Unique Array: [1, 2, 5, 6] (U = 4).
- Ranks: 1 -> 0, 2 -> 1, 5 -> 2, 6 -> 3.

Step 2: Backward Traversal (Segment Tree Size 4):
- i = 3 (val = 1, rank = 0): query(0, -1) -> 0. update(0, +1). ans[3] = 0.
- i = 2 (val = 6, rank = 3): query(0, 2)  -> 1 (rank 0 has count 1). update(3, +1). ans[2] = 1.
- i = 1 (val = 2, rank = 1): query(0, 0)  -> 1 (rank 0 has count 1). update(1, +1). ans[1] = 1.
- i = 0 (val = 5, rank = 2): query(0, 1)  -> 2 (ranks 0 and 1 have count 2). update(2, +1). ans[0] = 2.

Final Result = [2, 1, 1, 0]! ✅ (O(N log N) Time!)
```

---

## 5. Visual Diagram
Coordinate Compression Rank Mapping Topography:

```
Original Values:    [ 5  |  2  |  6  |  1 ]
                     |      |      |      |
Compressed Ranks:   [ 2  |  1  |  3  |  0 ]  <--- Index Range [0 ... 3] inside Segment Tree!

Backward Traversal: Query Range [0 ... rank-1] -> Sum = Count of Smaller Elements After Self! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 315 (Count of Smaller Numbers After Self using Coordinate Compression & Segment Tree):

```java
import java.util.*;

// LeetCode 315: Count of Smaller Numbers After Self
public class AdvancedSegmentTreeProblemsMaster {

    // Segment Tree for Frequency Range Sum
    private static class FrequencySegmentTree {
        private final int[] tree;
        private final int n;

        public FrequencySegmentTree(int n) {
            this.n = n;
            this.tree = new int[4 * n];
        }

        public void update(int treeIdx, int l, int r, int arrIdx, int delta) {
            if (l == r) {
                tree[treeIdx] += delta;
                return;
            }
            int mid = l + (r - l) / 2;
            if (arrIdx <= mid) update(2 * treeIdx + 1, l, mid, arrIdx, delta);
            else update(2 * treeIdx + 2, mid + 1, r, arrIdx, delta);
            tree[treeIdx] = tree[2 * treeIdx + 1] + tree[2 * treeIdx + 2];
        }

        public int query(int treeIdx, int l, int r, int ql, int qr) {
            if (ql <= l && r <= qr) return tree[treeIdx];
            if (r < ql || l > qr) return 0;
            int mid = l + (r - l) / 2;
            return query(2 * treeIdx + 1, l, mid, ql, qr) + 
                   query(2 * treeIdx + 2, mid + 1, r, ql, qr);
        }
    }

    // LeetCode 315 Solution O(N log N) Time, O(N) Space
    public List<Integer> countSmaller(int[] nums) {
        List<Integer> result = new ArrayList<>();
        if (nums == null || nums.length == 0) return result;

        int n = nums.length;

        // Step 1: Coordinate Compression
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        
        // Remove duplicate values to build unique rank array
        List<Integer> unique = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (i == 0 || sorted[i] != sorted[i - 1]) {
                unique.add(sorted[i]);
            }
        }

        int u = unique.size(); // Number of unique ranks
        FrequencySegmentTree segTree = new FrequencySegmentTree(u);

        Integer[] counts = new Integer[n];

        // Step 2: Backward Traversal (N-1 down to 0)
        for (int i = n - 1; i >= 0; i--) {
            int rank = getRank(unique, nums[i]);

            // Query sum of frequencies strictly smaller than rank [0 ... rank-1]
            int smallerCount = (rank > 0) ? segTree.query(0, 0, u - 1, 0, rank - 1) : 0;
            counts[i] = smallerCount;

            // Increment frequency at rank
            segTree.update(0, 0, u - 1, rank, 1);
        }

        return Arrays.asList(counts);
    }

    private int getRank(List<Integer> sortedList, int target) {
        return Collections.binarySearch(sortedList, target);
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 315 Backward Query Line
int smallerCount = (rank > 0) ? segTree.query(0, 0, u - 1, 0, rank - 1) : 0;
segTree.update(0, 0, u - 1, rank, 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 315 - Count of Smaller Numbers After Self**: Core problem.
* **LeetCode 699 - Falling Squares**: Dynamic Range Max Update with Lazy Propagation.
* **LeetCode 327 - Count of Range Sum**: Prefix sum compression + Segment Tree query.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 315 `countSmaller`:

```java
public class AdvancedSegmentTreeProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 315 Count of Smaller After Self Test ===");
        AdvancedSegmentTreeProblemsMaster solver = new AdvancedSegmentTreeProblemsMaster();

        int[] nums = {5, 2, 6, 1};
        List<Integer> result = solver.countSmaller(nums);

        System.out.println("Input Array:  " + Arrays.toString(nums));
        System.out.println("Result Counts: " + result); 
        // Output: [2, 1, 1, 0] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Smaller After Self (315)**| **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | Compression + Backward SegTree |
| **Falling Squares (699)** | **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | Lazy Range Max Update |
| **Count Range Sum (327)** | **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | Prefix Sum Compression |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Numbers in Input Array**: Handled by deduplicating `unique` list so all equal values share the same rank.
* **Negative Input Numbers (`-10^9`)**: Handled seamlessly by coordinate compression rank mapping.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Raw Input Values directly as Segment Tree Array Indices**:
  - Input numbers can be negative (`-5`) or huge (`10^9`), causing array allocation crashes.
  - **ALWAYS use Coordinate Compression to map arbitrary values to compressed ranks $0 \dots U-1$**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Backward Traversal Solves LeetCode 315:
> By iterating right-to-left ($i = N-1 \dots 0$), the Segment Tree contains ONLY numbers that appear to the RIGHT of index $i$ in the original array.
> Querying range $[0 \dots \text{rank}-1]$ fetches the exact count of numbers that are BOTH smaller than `nums[i]` AND located to its right!

> **Memory Trick:** **"Backward traversal guarantees the Segment Tree contains ONLY elements to the right of index i!"**

---

## 13. System & Implementation Comparisons

| Feature | Segment Tree + Coordinate Compression | Merge Sort Inversion Count |
| :--- | :--- | :--- |
| **Code Structure** | **Modular (Trie/Tree reusable) ⚡**| Complex Merge Modification |
| **Time Complexity** | **$O(N \log N)$ Linear-Logarithmic ⚡**| **$O(N \log N)$ Linear-Logarithmic ⚡**|
| **Dynamic Capability**| **Supports dynamic element updates ⚡**| Static array only |

---

## 14. How to Recognize This in Questions
* **"Count how many elements to the right of nums[i] are smaller than nums[i]"** $\rightarrow$ LeetCode 315.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is coordinate compression necessary for LeetCode 315?**  
  *A:* Because `nums[i]` values can range from $-10^9$ to $+10^9$. Coordinate compression maps values to compact ranks $0 \dots U-1$ where $U \le N \le 100,000$.
* **Q: What is the time complexity of coordinate compression?**  
  *A:* $O(N \log N)$ to sort unique values and binary search ranks.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED SEGMENT TREE PROBLEMS (LEETCODE 315)         |
+-----------------------------------------------------------------------+
| • Step 1: Coordinate Compression: Sort unique values -> map to ranks  |
| • Step 2: Build Frequency Segment Tree of size U (unique count)       |
| • Step 3: Iterate backwards (N-1 down to 0):                          |
|           smallerCount = query(0, 0, U-1, 0, rank - 1);               |
|           update(0, 0, U-1, rank, +1);                                |
| • Time Bounds: O(N log N) Time | O(N) Space (Optimal!) ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 315 (`Count of Smaller Numbers After Self`) in Java.
- [ ] I can implement Coordinate Compression using `Arrays.sort` and `binarySearch`.
- [ ] I know why right-to-left backward traversal is mandatory.
- [ ] I can write a Frequency Segment Tree for rank counting.
- [ ] I can trace LeetCode 315 step by step.
