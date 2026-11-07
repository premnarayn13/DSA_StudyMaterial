# 09. Advanced Fenwick Tree Problems: Frequency Fenwick Trees & Inversion Counting

## 1. Introduction
**Advanced Fenwick Tree Problems** combine Frequency Fenwick Trees with **Coordinate Compression** and **Backward Right-to-Left Array Traversals** to solve hard-level counting and inversion challenges. Problems like **Inversion Count in Array**, **Count of Smaller Numbers After Self (LeetCode 315 - Frequency BIT)**, and **Reverse Pairs (LeetCode 493)** execute in **$O(N \log N)$ Time** and **$O(N)$ Auxiliary Space**, outperforming $O(N^2)$ brute-force solutions while using 75% less code than Segment Trees!

> **Important:** Why Frequency Fenwick Trees Count Inversions in $O(N \log N)$ Time:
> 1. **Frequency Fenwick Tree Concept**: `tree[rank]` stores the frequency count of elements with compressed rank `rank`.
> 2. **Backward Traversal Invariant**: Iterate through array right-to-left ($i = N-1 \dots 0$):
>    - For element `nums[i]` with compressed rank $R$:
>    - `query(R - 1)` computes the total count of numbers ALREADY PROCESSED to the right of index $i$ that are STRICTLY SMALLER than `nums[i]` in **$O(\log N)$ time**!
>    - `add(R, +1)` increments the frequency count at rank $R$ in **$O(\log N)$ time**!
> 3. Total Time: **$O(N \log N)$ Time**, Space: **$O(N)$ Space**! ⚡

```
Frequency Fenwick Tree Inversion Counting Pipeline Topology:
Input = [5, 2, 6, 1] ---> Sorted Unique Ranks: [1 (Rank 1), 2 (Rank 2), 5 (Rank 3), 6 (Rank 4)]

Traverse Right-to-Left:
1. Process 1 (Rank 1): query(0) -> 0. add(1, +1). Count for 1 = 0.
2. Process 6 (Rank 4): query(3) -> 1 (Rank 1 has count 1). add(4, +1). Count for 6 = 1.
3. Process 2 (Rank 2): query(1) -> 1 (Rank 1 has count 1). add(2, +1). Count for 2 = 1.
4. Process 5 (Rank 3): query(2) -> 2 (Ranks 1 and 2 have count 2). add(3, +1). Count for 5 = 2.

Final Result Array = [2, 1, 1, 0]! Total Inversions = 4! ⚡
```

---

## 2. Core Concepts & LeetCode 493 Reverse Pairs Architecture

### 2.1 LeetCode 493 Reverse Pairs Algorithm ($A[i] > 2 \cdot A[j]$)
Given array `nums`: count pairs $(i, j)$ such that $i < j$ and $\text{nums}[i] > 2 \cdot \text{nums}[j]$:
1. Collect all values `nums[i]` AND target search values $2 \cdot \text{nums}[j]$.
2. Sort and deduplicate to build Coordinate Compression ranks $1 \dots U$.
3. Traverse `nums[]` right-to-left ($i = N-1 \dots 0$):
   - `int rankTarget = getRank(nums[i])`.
   - `count += bit.query(rankTarget - 1)` (Count elements to the right where $2 \cdot \text{nums}[j] < \text{nums}[i]$).
   - `int rankSelf = getRank(2 * nums[i])`.
   - `bit.add(rankSelf, +1)`.
4. Return total count in **$O(N \log N)$ Time**.

```
Advanced Fenwick Tree Pattern Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Inversion Count**   | Frequency BIT     | **$O(N \log N)$ ⚡**| $O(N)$ BIT Space  |
| **Smaller After (315)**| Compression + BIT | **$O(N \log N)$ ⚡**| $O(N)$ BIT Space  |
| **Reverse Pairs (493)**| 2x Value Compression| **$O(N \log N)$ ⚡**| $O(N)$ BIT Space  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Frequency BIT: Loop right-to-left -> query(rank-1) for smaller right elements -> add(rank, +1)!"**

---

## 3. Characteristics & 75% Code Reduction vs Segment Trees

### 3.1 Code Length & Speed Comparison
Solving LeetCode 315 (`Count of Smaller Numbers After Self`) using a Fenwick Tree requires **ONLY 15 lines of code**, compared to ~60 lines for a Segment Tree, while executing 2x faster in hardware due to simple iterative LSB loops (`i += i & -i`)!

---

## 4. Internal Working Mechanics
Tracing Inversion Count on Array `[2, 4, 1, 3, 5]`:

```
Input: nums = [2, 4, 1, 3, 5].

Step 1: Coordinate Compression:
- Sorted Unique Array: [1, 2, 3, 4, 5] -> Ranks: 1->1, 2->2, 3->3, 4->4, 5->5.

Step 2: Backward Traversal (BIT Size 5):
- i = 4 (val=5, rank=5): query(4) = 0. add(5, +1). Inversions = 0.
- i = 3 (val=3, rank=3): query(2) = 0. add(3, +1). Inversions = 0.
- i = 2 (val=1, rank=1): query(0) = 0. add(1, +1). Inversions = 0.
- i = 1 (val=4, rank=4): query(3) = 2 (ranks 1 and 3 count 2). add(4, +1). Inversions = 2.
- i = 0 (val=2, rank=2): query(1) = 1 (rank 1 count 1). add(2, +1). Inversions = 1.

Total Inversions = 0 + 0 + 0 + 2 + 1 = 3 (Pairs: (4,1), (4,3), (2,1))! ✅
```

---

## 5. Visual Diagram
Frequency Fenwick Tree Inversion Counting Topography:

```
Ranks:      [ 1  |  2  |  3  |  4  |  5 ]
Frequency:  [ 1  |  1  |  1  |  1  |  1 ]

query(rank - 1) calculates sum of frequencies to the left of current rank! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 315 (Count of Smaller Numbers After Self using Frequency Fenwick Tree and Coordinate Compression):

```java
import java.util.*;

// LeetCode 315: Count of Smaller Numbers After Self (Frequency Fenwick Tree)
public class AdvancedFenwickProblemsMaster {

    private static class FenwickTree {
        private final int[] tree;
        private final int n;

        public FenwickTree(int n) {
            this.n = n;
            this.tree = new int[n + 1];
        }

        public void add(int i, int delta) {
            while (i <= n) {
                tree[i] += delta;
                i += (i & -i);
            }
        }

        public int query(int i) {
            int sum = 0;
            while (i > 0) {
                sum += tree[i];
                i -= (i & -i);
            }
            return sum;
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

        List<Integer> unique = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if (i == 0 || sorted[i] != sorted[i - 1]) {
                unique.add(sorted[i]);
            }
        }

        int u = unique.size();
        FenwickTree bit = new FenwickTree(u);

        Integer[] counts = new Integer[n];

        // Step 2: Backward Traversal (N-1 down to 0)
        for (int i = n - 1; i >= 0; i--) {
            int rank = getRank(unique, nums[i]); // 1-based rank

            // Query sum of frequencies strictly smaller than rank [1 ... rank - 1]
            int smallerCount = bit.query(rank - 1);
            counts[i] = smallerCount;

            // Increment frequency at 1-based rank
            bit.add(rank, 1);
        }

        return Arrays.asList(counts);
    }

    private int getRank(List<Integer> sortedList, int target) {
        return Collections.binarySearch(sortedList, target) + 1; // 1-based index
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 315 Frequency BIT Traversal Line
int rank = Collections.binarySearch(unique, nums[i]) + 1;
counts[i] = bit.query(rank - 1);
bit.add(rank, 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 315 - Count of Smaller Numbers After Self**: Core problem.
* **LeetCode 493 - Reverse Pairs**: Modified $2 \times$ value inversion count.
* **Global Inversion Count**: Total inversions in array.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 315 `countSmaller`:

```java
public class AdvancedFenwickProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 315 Frequency BIT Test ===");
        AdvancedFenwickProblemsMaster solver = new AdvancedFenwickProblemsMaster();

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
| **Smaller After Self (315)**| **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | Compression + Frequency BIT |
| **Reverse Pairs (493)** | **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | $2 \times$ Compression + Frequency BIT |
| **Array Inversions**  | **$O(N \log N)$ Optimal ⚡**| **$O(N)$ Array Space** | Frequency BIT query sum |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Numbers in Array**: Deduplicated by `unique` list, assigning equal values to the exact same 1-based rank.
* **Negative Numbers (`-10^9`)**: Compression maps negative values to positive 1-based ranks $1 \dots U$.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `getRank(nums[i])` as 0-Based Index in `bit.query()`**:
  - Fenwick Trees strictly require 1-based indexing. Passing rank 0 into `query()` returns `0` incorrectly.
  - **ALWAYS add $+1$ to `binarySearch` result to get 1-based ranks**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Fenwick Trees Are Preferred Over Segment Trees for LeetCode 315:
> Both structures run in $O(N \log N)$ time. However:
> 1. Fenwick Tree uses 75% less memory ($N + 1$ space vs $4N$ space).
> 2. Fenwick Tree requires ONLY 15 lines of code (vs 60 lines for Segment Tree).
> 3. Fenwick Tree uses simple iterative LSB loops, avoiding call stack recursion! ⚡

> **Memory Trick:** **"LeetCode 315: Use Frequency BIT for 75% cleaner code and 2x faster execution!"**

---

## 13. System & Implementation Comparisons

| Feature | Frequency Fenwick Tree | Merge Sort Inversion Count |
| :--- | :--- | :--- |
| **Code Length** | **~15 Lines Clean Code ⚡**| ~50 Lines Complex Merge |
| **Time Complexity** | **$O(N \log N)$ Linear-Logarithmic ⚡**| **$O(N \log N)$ Linear-Logarithmic ⚡**|
| **Dynamic Capability**| **Supports dynamic element insertions ⚡**| Static Array Only |

---

## 14. How to Recognize This in Questions
* **"Count inversions or smaller numbers to the right of each element"** $\rightarrow$ LeetCode 315 (Frequency Fenwick Tree).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does iterating right-to-left solve LeetCode 315?**  
  *A:* Because iterating backwards guarantees that the Frequency BIT contains ONLY elements that appear to the right of index $i$.
* **Q: How does LeetCode 493 (Reverse Pairs) differ from LeetCode 315?**  
  *A:* LeetCode 493 searches for elements $2 \cdot \text{nums}[j] < \text{nums}[i]$, requiring coordinate compression over both `nums[i]` and $2 \cdot \text{nums}[j]$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FREQUENCY FENWICK TREES (LEETCODE 315)                |
+-----------------------------------------------------------------------+
| • Step 1: Compress unique values to 1-based ranks (1 ... U)           |
| • Step 2: Initialize Frequency Fenwick Tree of size U                 |
| • Step 3: Iterate backwards (N-1 down to 0):                          |
|           rank = binarySearch(unique, nums[i]) + 1;                   |
|           result[i] = bit.query(rank - 1);                            |
|           bit.add(rank, 1);                                           |
| • Performance: $O(N \log N)$ Time | $O(N)$ Space | 15 Lines Code! ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 315 (`Count of Smaller Numbers After Self`) using a Fenwick Tree.
- [ ] I can implement Coordinate Compression for 1-based ranks.
- [ ] I know why right-to-left backward traversal is mandatory.
- [ ] I can write LeetCode 493 (`Reverse Pairs`) using Frequency BIT.
- [ ] I can trace inversion counting step by step.
