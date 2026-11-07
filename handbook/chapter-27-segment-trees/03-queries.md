# 03. Segment Tree Range Queries, 3 Overlap Cases & Identity Element Baselines

## 1. Introduction
A **Range Query** on a **Segment Tree** extracts summary values (such as Range Sum, Range Minimum, or Range Maximum) for an arbitrary query interval $[qL \dots qR]$ over an array of size $N$. By classifying each segment node $[L \dots R]$ against $[qL \dots qR]$ into **3 Overlap Cases**, the query algorithm prunes irrelevant branches and aggregates matching subsegment results in **$O(\log N)$ Logarithmic Time** and **$O(\log N)$ Auxiliary Stack Space**.

> **Important:** The 3 Overlap Cases for Segment Tree Range Queries:
> 1. **Case 1: Total Overlap ($qL \le L \text{ and } R \le qR$)**: The node's entire range is FULLY CONTAINED within query $[qL \dots qR]$! **Return `tree[treeIdx]` immediately** without recursing deeper!
> 2. **Case 2: No Overlap ($R < qL \text{ or } L > qR$)**: The node's range is COMPLETELY OUTSIDE query $[qL \dots qR]$! **Return Identity Element** (`0` for Sum, `\infty` for Min, `-\infty` for Max) immediately!
> 3. **Case 3: Partial Overlap**: The node's range overlaps partially with $[qL \dots qR]$. Recurse into both left and right children, and **Merge Child Results**! ⚡

```
Segment Tree 3-Case Range Query Pipeline Topology:
Query Range [qL ... qR] = [1 ... 2] vs Node Range [L ... R]:
- Node [0 ... 3]: Partial Overlap -> Recurse Left [0...1] & Right [2...3]
  - Node [0 ... 1]: Partial Overlap -> Recurse Left [0...0] & Right [1...1]
    - Node [0 ... 0]: NO OVERLAP (0 < 1) -------------> Return 0 (Identity) ⚡
    - Node [1 ... 1]: TOTAL OVERLAP (1 <= 1 <= 2) ----> Return tree[node] (Val) ⚡
  - Node [2 ... 3]: Partial Overlap -> Recurse Left [2...2] & Right [3...3]
    - Node [2 ... 2]: TOTAL OVERLAP (1 <= 2 <= 2) ----> Return tree[node] (Val) ⚡
    - Node [3 ... 3]: NO OVERLAP (3 > 2) -------------> Return 0 (Identity) ⚡
```

---

## 2. Core Concepts & Identity Base Values Across Query Functions

### 2.1 The 3 Overlap Case Query Matrix
```
Segment Tree Query Case Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Overlap Case          | Condition Check   | Return Action     | Recurse Deeper?   |
+-----------------------+-------------------+-------------------+-------------------+
| **Case 1: Total**     | $qL \le L \land R \le qR$| **`return tree[treeIdx]` ⚡**| **NO (Pruned!) ⚡**|
| **Case 2: None**      | $R < qL \lor L > qR$| **`return Identity` ⚡** | **NO (Pruned!) ⚡**|
| **Case 3: Partial**   | Otherwise         | `Merge(left, right)`| **YES (Recurse Both)**|
+-----------------------+-------------------+-------------------+-------------------+
```

#### Identity Base Values by Query Type:
* **Range Sum Query (RSQ)**: Identity $= \mathbf{0}$ ($X + 0 = X$).
* **Range Minimum Query (RMQ)**: Identity $= \mathbf{+\infty}$ (`Integer.MAX_VALUE`, $\min(X, \infty) = X$).
* **Range Maximum Query (RMaxQ)**: Identity $= \mathbf{-\infty}$ (`Integer.MIN_VALUE`, $\max(X, -\infty) = X$).
* **Range Greatest Common Divisor (GCD)**: Identity $= \mathbf{0}$ ($\gcd(X, 0) = X$).

> **Memory Trick:** **"Query Case 1 Total Overlap: return tree[i]! Case 2 No Overlap: return Identity! Case 3 Partial: merge recursion!"**

---

## 3. Characteristics & Mathematical Proof of $O(\log N)$ Time

### 3.1 Mathematical Proof of $O(\log N)$ Query Complexity
* At any depth $d$ in the Segment Tree, at most **4 nodes** can experience Partial Overlap (Case 3).
* All other nodes at depth $d$ are either Total Overlap (Case 1) or No Overlap (Case 2), both of which return immediately without recursing deeper!
* Because tree height $H = \lceil \log_2 N \rceil$, the query algorithm visits at most $4 H = 4 \lceil \log_2 N \rceil$ nodes total.
* Total Time Complexity: $\mathbf{O(\log N) \text{ Logarithmic Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Range Sum Query $[1 \dots 2]$ on Array `[2, 1, 5, 3]` ($N=4$):

```
Tree: Root 0..3 (Sum=11). Left 0..1 (Sum=3). Right 2..3 (Sum=8).

Query sumRange(qL=1, qR=2):
1. Root [0..3]: Partial Overlap (0 < 1 and 3 > 2).
   - Recurse Left child [0..1] and Right child [2..3].

2. Left Child [0..1]: Partial Overlap (0 < 1 and 1 <= 2).
   - Leaf [0..0]: NO OVERLAP (0 < 1) -> Returns 0 (Identity).
   - Leaf [1..1]: TOTAL OVERLAP (1 <= 1 <= 2) -> Returns tree[4] = 1.
   - Left Child Sum = 0 + 1 = 1.

3. Right Child [2..3]: Partial Overlap (2 >= 1 and 3 > 2).
   - Leaf [2..2]: TOTAL OVERLAP (1 <= 2 <= 2) -> Returns tree[5] = 5.
   - Leaf [3..3]: NO OVERLAP (3 > 2) -> Returns 0 (Identity).
   - Right Child Sum = 5 + 0 = 5.

4. Root Merge: Sum = 1 + 5 = 6!

Result = 6 (1 + 5)! Executed in 4 node visits! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Segment Tree 3-Case Overlap Query Topography:

```
                      [ Node 0: Range 0..3 ] (Partial -> Recurse)
                     /                      \
      [ Node 1: Range 0..1 ]            [ Node 2: Range 2..3 ] (Partial -> Recurse)
     /                     \           /                     \
[0..0: NO OVERLAP]   [1..1: TOTAL] [2..2: TOTAL]       [3..3: NO OVERLAP]
 (Returns 0)         (Returns 1)   (Returns 5)         (Returns 0)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Range Query algorithms across Range Sum, Minimum, and Maximum:

```java
import java.util.*;

public class SegmentTreeQueriesMaster {

    public enum QueryType { SUM, MIN, MAX }

    private final int[] tree;
    private final int n;
    private final QueryType type;

    public SegmentTreeQueriesMaster(int[] nums, QueryType type) {
        this.n = nums.length;
        this.type = type;
        this.tree = new int[4 * n];
        if (n > 0) build(nums, 0, 0, n - 1);
    }

    private void build(int[] nums, int treeIdx, int l, int r) {
        if (l == r) { tree[treeIdx] = nums[l]; return; }
        int mid = l + (r - l) / 2;
        build(nums, 2 * treeIdx + 1, l, mid);
        build(nums, 2 * treeIdx + 2, mid + 1, r);
        tree[treeIdx] = merge(tree[2 * treeIdx + 1], tree[2 * treeIdx + 2]);
    }

    // Public Query Interface O(log N) Time
    public int query(int ql, int qr) {
        return queryHelper(0, 0, n - 1, ql, qr);
    }

    private int queryHelper(int treeIdx, int l, int r, int ql, int qr) {
        // Case 1: Total Overlap -> Return node value immediately!
        if (ql <= l && r <= qr) {
            return tree[treeIdx];
        }

        // Case 2: No Overlap -> Return Identity element immediately!
        if (r < ql || l > qr) {
            return getIdentity();
        }

        // Case 3: Partial Overlap -> Recurse into both children & merge
        int mid = l + (r - l) / 2;
        int leftResult = queryHelper(2 * treeIdx + 1, l, mid, ql, qr);
        int rightResult = queryHelper(2 * treeIdx + 2, mid + 1, r, ql, qr);

        return merge(leftResult, rightResult);
    }

    private int getIdentity() {
        switch (type) {
            case SUM: return 0;
            case MIN: return Integer.MAX_VALUE;
            case MAX: return Integer.MIN_VALUE;
            default: return 0;
        }
    }

    private int merge(int a, int b) {
        switch (type) {
            case SUM: return a + b;
            case MIN: return Math.min(a, b);
            case MAX: return Math.max(a, b);
            default: return 0;
        }
    }
}
```

> **Quick Syntax:**
```java
// Segment Tree 3-Case Query Block
if (ql <= l && r <= qr) return tree[treeIdx]; // Case 1: Total Overlap
if (r < ql || l > qr) return getIdentity();   // Case 2: No Overlap
int mid = l + (r - l) / 2;
return merge(query(left, l, mid, ql, qr), query(right, mid + 1, r, ql, qr)); // Case 3: Partial
```

---

## 7. Concrete Problem Examples
* **LeetCode 307 - `sumRange(left, right)`**: Range Sum Query.
* **Range Minimum Query (RMQ)**: Finding smallest value in subarray $[qL \dots qR]$.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `query(ql, qr)` across Sum, Minimum, and Maximum trees:

```java
public class SegmentTreeQueriesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Segment Tree Range Query Test ===");
        int[] nums = {2, 1, 5, 3};

        SegmentTreeQueriesMaster sumTree = 
            new SegmentTreeQueriesMaster(nums, SegmentTreeQueriesMaster.QueryType.SUM);
        System.out.println("Sum Range [1 ... 2]: " + sumTree.query(1, 2)); // Output: 6 (1+5)

        SegmentTreeQueriesMaster minTree = 
            new SegmentTreeQueriesMaster(nums, SegmentTreeQueriesMaster.QueryType.MIN);
        System.out.println("Min Range [1 ... 3]: " + minTree.query(1, 3)); // Output: 1 (Min of 1,5,3)

        SegmentTreeQueriesMaster maxTree = 
            new SegmentTreeQueriesMaster(nums, SegmentTreeQueriesMaster.QueryType.MAX);
        System.out.println("Max Range [0 ... 2]: " + maxTree.query(0, 2)); // Output: 5 (Max of 2,1,5) ✅
    }
}
```

---

## 9. Complexity Analysis

| Query Type | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Range Query ($qL, qR$)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Query Out of Bounds ($qL < 0$ or $qR \ge N$)**: Handled safely by Case 2 No Overlap check `r < ql || l > qr`.
* **Single Element Query Range ($qL == qR$)**: Executes in $O(\log N)$ time, returning single leaf value.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `0` as Identity Base Value for Range Minimum Query (RMQ)**:
  - Returning `0` for No Overlap in RMQ causes negative numbers or positive values to be masked by `0`!
  - **ALWAYS use `Integer.MAX_VALUE` as the identity element for RMQ**.
* **Confusing Query Range `ql, qr` with Segment Node Range `l, r`**:
  - `ql, qr` remain CONSTANT across all recursive call stack frames. Only `l, r` change as we navigate down the tree.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Case 1 Total Overlap Prunes Search Work:
> If node range $[L \dots R]$ is completely inside query $[qL \dots qR]$, `tree[treeIdx]` ALREADY STORES the pre-computed summary value for ALL elements in $[L \dots R]$.
> Returning `tree[treeIdx]` immediately avoids visiting any descendant nodes, guaranteeing **$O(\log N)$ query speed**!

> **Memory Trick:** **"Total Overlap returns pre-computed tree[i] value immediately, pruning deeper recursion!"**

---

## 13. System & Implementation Comparisons

| Feature | Segment Tree Range Query | Prefix Sum Array Range Query |
| :--- | :--- | :--- |
| **Query Speed** | **$O(\log N)$ Logarithmic ⚡** | **$O(1)$ Constant Time ⚡** |
| **Point Update Speed**| **$O(\log N)$ Dynamic ⚡** | $O(N)$ Linear Time ❌ |
| **Query Versatility** | Sum, Min, Max, GCD, Custom | Sum Only |

---

## 14. How to Recognize This in Questions
* **"Query summary value over subarray [qL ... qR] in dynamic mutable array"** $\rightarrow$ Segment Tree Query.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Range Minimum Query (RMQ) return `Integer.MAX_VALUE` for No Overlap?**  
  *A:* Because $\min(X, \text{Integer.MAX\_VALUE}) = X$. It acts as the mathematical identity element for the minimum operation.
* **Q: What is the maximum number of nodes visited during a range query?**  
  *A:* At most $4 \lceil \log_2 N \rceil$ nodes.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEGMENT TREE RANGE QUERIES                            |
+-----------------------------------------------------------------------+
| • Case 1: Total Overlap (ql <= l && r <= qr) -> Return tree[treeIdx]  |
| • Case 2: No Overlap    (r < ql || l > qr)   -> Return Identity       |
| • Case 3: Partial      (Otherwise)           -> Recurse & Merge       |
| • Identities: RSQ = 0 | RMQ = Integer.MAX_VALUE | RMaxQ = Integer.MIN_VALUE|
| • Time Bounds: O(log N) Logarithmic Time (At most 4 * log2 N nodes) ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the 3 overlap query cases in Java.
- [ ] I know the correct identity element for Sum, Min, Max, and GCD.
- [ ] I know why Total Overlap prunes deeper recursion.
- [ ] I can prove why range queries visit at most $4 \log_2 N$ nodes.
- [ ] I can trace a range query step by step on a Segment Tree.
