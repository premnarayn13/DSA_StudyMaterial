# 05. Prefix Sum Queries, Downward Traversal & Disjoint Range Partitioning Proofs

## 1. Introduction
A **Prefix Sum Query** on a **Fenwick Tree (Binary Indexed Tree)** computes the cumulative sum of elements from the beginning of the array up to index `idx` (range $[1 \dots \text{idx}]$) in **$O(\log N)$ Logarithmic Time**. By decomposing the query range $[1 \dots \text{idx}]$ into a small set of disjoint subsegments stored in `tree[]` nodes and iterating downward using **`i -= i & (-i)`**, the query algorithm accumulates the total prefix sum in at most $\lceil \log_2 N \rceil$ loop steps with **zero recursion or call stack memory**.

> **Important:** The Disjoint Subsegment Partitioning Principle:
> 1. **Disjoint Subsegments**: Any prefix range $[1 \dots \text{idx}]$ can be uniquely partitioned into at most $\log_2 N$ disjoint subsegments stored inside individual `tree[]` entries!
> 2. **Downward Hop Traversal**: `i -= i & (-i)`.
>    - Step 1: Accumulate current node sum: `sum += tree[i]`.
>    - Step 2: Hop to previous adjacent subsegment: `i -= (i & -i)`.
>    - Step 3: Repeat until $i = 0$ (Empty prefix)! ⚡

```
Fenwick Tree Downward Prefix Query Pipeline Topology:
Computing Prefix Sum up to 1-Based Index 7 (Binary 0111):
Step 1: i = 7 (0111) ---> sum += tree[7] (Range [7..7]). Next i = 7 - LSB(7) = 7 - 1 = 6 (0110)
Step 2: i = 6 (0110) ---> sum += tree[6] (Range [5..6]). Next i = 6 - LSB(6) = 6 - 2 = 4 (0100)
Step 3: i = 4 (0100) ---> sum += tree[4] (Range [1..4]). Next i = 4 - LSB(4) = 4 - 4 = 0 (0000)
Step 4: i = 0        ---> Loop terminates!

Total Accumulated Range = [1..4] + [5..6] + [7..7] = Range [1..7]! Executed in 3 hops! ⚡
```

---

## 2. Core Concepts & Disjoint Partitioning Proof

### 2.1 Mathematical Proof of Disjoint Range Partitioning
Let $i$ be a 1-based index with binary representation $i = b_k b_{k-1} \dots b_0$.
* Node `tree[i]` stores the sum over range $[i - \text{LSB}(i) + 1 \dots i]$.
* Subtracting $\text{LSB}(i)$ produces $i' = i - \text{LSB}(i)$, which represents the index immediately to the left of `tree[i]`'s range.
* The subsegment of $i'$ ends at $i'$, which is strictly adjacent to the start of $i$'s range ($i' + 1$).
* Repeating $i \leftarrow i - \text{LSB}(i)$ generates a sequence of strictly non-overlapping, adjacent ranges whose union spans $[1 \dots i]$:
  $$\bigcup \text{Ranges} = [1 \dots i] \quad \text{and} \quad \text{Range}_a \cap \text{Range}_b = \emptyset \quad (\forall a \ne b)$$

Thus, **summing `tree[i]` entries during downward hops yields the EXACT prefix sum without double-counting!** ⚡

```
Prefix Query Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Query Function        | Range Calculated  | Traversal Loop    | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **`query(idx)`**      | $[1 \dots \text{idx}]$ | `i -= i & (-i)`   | **$O(\log N)$ Logarithmic ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Prefix Query: Loop i -= i & -i, add tree[i] to sum until i = 0 in O(log N) time!"**

---

## 3. Characteristics & $O(\log N)$ Hop Upper Bounds

### 3.1 Mathematical Proof of $O(\log N)$ Downward Traversal Bounds
* Subtracting $\text{LSB}(i)$ clears the lowest set bit in the binary representation of $i$.
* A 32-bit integer index $i \le N$ has at most $\lceil \log_2 N \rceil$ set bits.
* Each loop iteration clears 1 set bit.
* The loop `while (i > 0)` executes at most $\lceil \log_2 N \rceil$ iterations, strictly guaranteeing **$O(\log N)$ Logarithmic Time**! ⚡

---

## 4. Internal Working Mechanics
Tracing Prefix Query `query(idx = 7)` on Array `[3, 2, -1, 6, 5, 4, -3, 3]` ($N=8$):

```
1-Based Tree Array = [0, 3, 5, -1, 10, 5, 9, -3, 19].

Call query(7):
- Start sum = 0, i = 7 (0111).
- Iteration 1: sum += tree[7] (-3) = -3. Next i = 7 - 1 = 6 (0110).
- Iteration 2: sum += tree[6] (9) = -3 + 9 = 6. Next i = 6 - 2 = 4 (0100).
- Iteration 3: sum += tree[4] (10) = 6 + 10 = 16. Next i = 4 - 4 = 0 (0000).
- i = 0 -> Loop terminates!

Resulting Prefix Sum [1..7] = 16 (3 + 2 + -1 + 6 + 5 + 4 + -3 = 16).
Calculated in 3 loop steps! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Prefix Query Downward Disjoint Partition Topography:

```
                          [ Index 7 (0111): tree[7] = -3 ]
                                         |
                                         v (i -= LSB(7) = 6)
                          [ Index 6 (0110): tree[6] = 9 ]
                                         |
                                         v (i -= LSB(6) = 4)
                          [ Index 4 (0100): tree[4] = 10 ]
                                         |
                                         v (i -= LSB(4) = 0)
                                    [ i = 0: DONE ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Fenwick Tree Prefix Sum Queries:

```java
import java.util.*;

public class PrefixSumQueriesMaster {

    private final int[] tree;
    private final int n;

    public PrefixSumQueriesMaster(int[] nums) {
        this.n = nums.length;
        this.tree = new int[n + 1];

        // Optimal O(N) Construction
        for (int i = 0; i < n; i++) tree[i + 1] = nums[i];
        for (int i = 1; i <= n; i++) {
            int parent = i + (i & -i);
            if (parent <= n) tree[parent] += tree[i];
        }
    }

    // 1-Based Prefix Query [1 ... idx] O(log N) Time
    public int query1Based(int idx) {
        int sum = 0;
        int i = idx;
        while (i > 0) {
            sum += tree[i];
            i -= (i & -i); // Hop to previous adjacent subsegment
        }
        return sum;
    }

    // 0-Based Prefix Query [0 ... 0basedIdx] O(log N) Time
    public int query0Based(int 0basedIdx) {
        return query1Based(0basedIdx + 1);
    }

    public int[] getTree() { return tree; }
}
```

> **Quick Syntax:**
```java
// Prefix Query Loop Line
public int query(int i) { int sum = 0; while (i > 0) { sum += tree[i]; i -= (i & -i); } return sum; }
```

---

## 7. Concrete Problem Examples
* **Cumulative Probability Arrays**: Sampling from discrete probability distributions.
* **Rank Query Systems**: Counting elements smaller than $X$.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `query0Based` and `query1Based`:

```java
public class PrefixSumQueriesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Fenwick Tree Prefix Sum Query Test ===");
        int[] nums = {3, 2, -1, 6, 5, 4, -3, 3};
        PrefixSumQueriesMaster bit = new PrefixSumQueriesMaster(nums);

        System.out.println("Prefix Sum up to 1-Based Index 4 (1..4): " + 
            bit.query1Based(4)); // Output: 10 (3+2+-1+6)

        System.out.println("Prefix Sum up to 1-Based Index 7 (1..7): " + 
            bit.query1Based(7)); // Output: 16 (3+2+-1+6+5+4+-3)

        System.out.println("Prefix Sum up to 0-Based Index 2 (0..2): " + 
            bit.query0Based(2)); // Output: 4 (3+2+-1) ✅
    }
}
```

---

## 9. Complexity Analysis

| Prefix Query Aspect | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`query(idx)`** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Auxiliary Space**|

---

## 10. Edge Cases & Boundary Handling
* **Query `idx = 0` (Empty Prefix)**: Loop `while (i > 0)` does not execute, returning `0` immediately.
* **Query `idx = N` (Entire Array)**: Returns cumulative sum of all $N$ elements.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `i += i & (-i)` Instead of `i -= i & (-i)` During Query**:
  - Adding LSB during query navigates UP to ancestors, missing lower subsegments and risking index out-of-bounds!
  - **Remember: QUERY goes DOWN (`-=`), UPDATE goes UP (`+=`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Prefix Query Requires Zero Recursion Stack:
> Unlike Segment Tree queries that use recursive divide-and-conquer, a Fenwick Tree prefix query iterates strictly downward via `i -= i & (-i)`.
> It uses **$O(1)$ Auxiliary Stack Memory**, making it immune to `StackOverflowError` regardless of array size $N$! ⚡

> **Memory Trick:** **"Fenwick Tree prefix query is iterative (zero stack) and uses i -= i & -i!"**

---

## 13. System & Implementation Comparisons

| Feature | Fenwick Tree Prefix Query | Segment Tree Range Query |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\log N)$ Logarithmic ⚡** | **$O(\log N)$ Logarithmic ⚡** |
| **Call Stack Memory**| **$O(1)$ Zero Stack ⚡** | $O(\log N)$ Call Stack |
| **Code Lines** | **3 Lines Iterative Loop ⚡** | 15 Lines 3-Case Recursion |

---

## 14. How to Recognize This in Questions
* **"Query cumulative sum of first K elements in dynamic array in minimum memory"** $\rightarrow$ Fenwick Tree Prefix Query.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `i -= i & (-i)` generate non-overlapping disjoint subsegments?**  
  *A:* Because subtracting $\text{LSB}(i)$ steps to index $i - \text{LSB}(i)$, which is the exact upper endpoint of the adjacent left subsegment.
* **Q: What is the maximum number of loop iterations in `query(idx)` for an array of size $N$?**  
  *A:* At most $\lceil \log_2 N \rceil$ iterations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FENWICK TREE PREFIX SUM QUERIES                       |
+-----------------------------------------------------------------------+
| • Downward Loop: int sum = 0; while (i > 0) { sum += tree[i]; i -= (i & -i); }|
| • Disjoint     : Accumulates non-overlapping adjacent subsegment ranges|
| • 0-Based Map  : query0Based(idx) = query1Based(idx + 1)              |
| • Time Bounds  : O(log N) Logarithmic Time (At most log2 N hops) ⚡   |
| • Memory Bounds: O(1) Zero Stack Memory (Iterative loop!) ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `query(idx)` in Java in 3 lines.
- [ ] I can prove why subsegments summed during query are disjoint.
- [ ] I know why `query0Based(idx)` takes `idx + 1`.
- [ ] I can trace downward query hops for Index 7.
- [ ] I can state the space complexity ($O(1)$ auxiliary memory).
