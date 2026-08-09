# 02. Segment Tree Construction, Divide-and-Conquer Build & Merge Invariants

## 1. Introduction
Constructing a **Segment Tree** builds a 1D heap-indexed array representation of an input array of size $N$ using a **Divide-and-Conquer Post-Order Recursion**. By partitioning the array range $[L \dots R]$ into left subsegment $[L \dots \text{mid}]$ and right subsegment $[\text{mid}+1 \dots R]$, the construction algorithm builds child subtrees first, then merges their values into the parent node in **$O(N)$ Linear Time** and **$O(N)$ Call Stack Space**.

> **Important:** The Universal Merge Invariants of Segment Tree Construction:
> 1. **Base Case (Leaf Assignment)**: When $L == R$, node `treeIdx` is a LEAF representing single element `nums[L]`: `tree[treeIdx] = nums[L]`.
> 2. **Post-Order Merge Phase**: Parent node value is computed by combining left and right child values according to the target query function:
>    - **Range Sum Query (RSQ)**: `tree[treeIdx] = tree[left] + tree[right]`.
>    - **Range Minimum Query (RMQ)**: `tree[treeIdx] = Math.min(tree[left], tree[right])`.
>    - **Range Maximum Query (RMaxQ)**: `tree[treeIdx] = Math.max(tree[left], tree[right])`. ⚡

```
Segment Tree Divide-and-Conquer Construction Pipeline Topology:
Step 1: Divide Range [L ... R] ------> Calculate mid = L + (R - L) / 2
Step 2: Recurse Left Subsegment -----> buildTree(2 * i + 1, L, mid)
Step 3: Recurse Right Subsegment ----> buildTree(2 * i + 2, mid + 1, R)
Step 4: Post-Order Merge -----------> tree[i] = Merge(tree[2*i+1], tree[2*i+2]) ⚡
```

---

## 2. Core Concepts & Generic Merge Operation Architecture

### 2.1 The General `buildTree` Algorithm ($O(N)$ Time)
To construct a Segment Tree for input `nums` over range `[L ... R]` at `treeIdx`:
1. If `L == R`:
   - `tree[treeIdx] = nums[L]`.
   - Return.
2. `mid = L + (R - L) / 2`.
3. `buildTree(2 * treeIdx + 1, L, mid)`.
4. `buildTree(2 * treeIdx + 2, mid + 1, R)`.
5. **Merge Phase**:
   - `tree[treeIdx] = merge(tree[2 * treeIdx + 1], tree[2 * treeIdx + 2])`.

```
Segment Tree Merge Function Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Target Range Query    | Leaf Assignment   | Parent Merge Logic| Identity Base Val |
+-----------------------+-------------------+-------------------+-------------------+
| **Range Sum Query**   | `nums[L]`         | `left + right`    | `0`               |
| **Range Minimum (RMQ)**| `nums[L]`        | `Math.min(l, r)`  | `Integer.MAX_VAL` |
| **Range Maximum**     | `nums[L]`         | `Math.max(l, r)`  | `Integer.MIN_VAL` |
| **Range GCD Query**   | `nums[L]`         | `gcd(left, right)`| `0`               |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Segment Tree Build: Recurse left, recurse right, merge children post-order in O(N) time!"**

---

## 3. Characteristics & Mathematical Proof of $O(N)$ Build Time

### 3.1 Mathematical Proof of $O(N)$ Linear Build Complexity
Let $T(N)$ be the time to build a Segment Tree for $N$ elements:

$$T(N) = 2 T(N / 2) + O(1)$$

By Case 1 of the **Master Theorem** ($a = 2, b = 2, f(N) = O(1) \implies \log_b a = 1$):

$$T(N) = \Theta(N)$$

Total number of recursive function calls equals total nodes in the tree ($2N - 1$), executing in **$O(N)$ Linear Time**! ⚡

---

## 4. Internal Working Mechanics
Tracing Range Minimum Query (RMQ) Segment Tree Build on Array `[5, 2, 4, 7]`:

```
Input nums = [5, 2, 4, 7] (N = 4).

Build Step 1: Root [0..3] -> mid = 1.
  - Recurse Left [0..1] -> mid = 0.
    - Leaf [0..0]: tree[3] = 5.
    - Leaf [1..1]: tree[4] = 2.
    - Merge [0..1]: tree[1] = Math.min(5, 2) = 2.
  - Recurse Right [2..3] -> mid = 2.
    - Leaf [2..2]: tree[5] = 4.
    - Leaf [3..3]: tree[6] = 7.
    - Merge [2..3]: tree[2] = Math.min(4, 7) = 4.

  - Merge Root [0..3]: tree[0] = Math.min(2, 4) = 2.

RMQ Segment Tree Built! Root stores global minimum = 2! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
RMQ Segment Tree Post-Order Merge Topography:

```
                      [ Root 0..3: Min=2 ] (Node 0)
                     /                    \
      [ Range 0..1: Min=2 ] (Node 1)    [ Range 2..3: Min=4 ] (Node 2)
     /                     \           /                     \
[0..0: Val=5]        [1..1: Val=2] [2..2: Val=4]        [3..3: Val=7]
 (Node 3)              (Node 4)      (Node 5)              (Node 6)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Range Sum, Range Minimum (RMQ), and Range Maximum Segment Tree Construction:

```java
import java.util.*;

public class SegmentTreeConstructionMaster {

    public enum QueryType { SUM, MIN, MAX }

    private final int[] tree;
    private final int[] nums;
    private final int n;
    private final QueryType type;

    public SegmentTreeConstructionMaster(int[] nums, QueryType type) {
        this.nums = nums;
        this.n = nums.length;
        this.type = type;
        this.tree = new int[4 * n];

        if (n > 0) {
            build(0, 0, n - 1);
        }
    }

    private void build(int treeIdx, int l, int r) {
        if (l == r) {
            tree[treeIdx] = nums[l]; // Base Case: Leaf assignment
            return;
        }

        int mid = l + (r - l) / 2;
        int leftChild = 2 * treeIdx + 1;
        int rightChild = 2 * treeIdx + 2;

        build(leftChild, l, mid);
        build(rightChild, mid + 1, r);

        // Merge Phase based on Query Type
        tree[treeIdx] = merge(tree[leftChild], tree[rightChild]);
    }

    private int merge(int leftVal, int rightVal) {
        switch (type) {
            case SUM: return leftVal + rightVal;
            case MIN: return Math.min(leftVal, rightVal);
            case MAX: return Math.max(leftVal, rightVal);
            default: return 0;
        }
    }

    public int getRootVal() { return tree[0]; }
    public int[] getTree() { return tree; }
}
```

> **Quick Syntax:**
```java
// Segment Tree Merge Line
tree[treeIdx] = merge(tree[leftChild], tree[rightChild]);
```

---

## 7. Concrete Problem Examples
* **Range Minimum Query (RMQ)**: Constructing RMQ trees for static/dynamic arrays.
* **Range Greatest Common Divisor (GCD)**: Merging `gcd(left, right)` across ranges.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Range Sum, Minimum, and Maximum Construction:

```java
public class SegmentTreeConstructionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Segment Tree Construction Test ===");
        int[] nums = {5, 2, 4, 7};

        SegmentTreeConstructionMaster sumTree = 
            new SegmentTreeConstructionMaster(nums, SegmentTreeConstructionMaster.QueryType.SUM);
        System.out.println("Range Sum Root: " + sumTree.getRootVal()); // Output: 18 (5+2+4+7)

        SegmentTreeConstructionMaster minTree = 
            new SegmentTreeConstructionMaster(nums, SegmentTreeConstructionMaster.QueryType.MIN);
        System.out.println("Range Min Root: " + minTree.getRootVal()); // Output: 2 (Min)

        SegmentTreeConstructionMaster maxTree = 
            new SegmentTreeConstructionMaster(nums, SegmentTreeConstructionMaster.QueryType.MAX);
        System.out.println("Range Max Root: " + maxTree.getRootVal()); // Output: 7 (Max) ✅
    }
}
```

---

## 9. Complexity Analysis

| Construction Aspect | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`build()` Time** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Call Stack Space |
| **Memory Allocation**| **$4N$ Array Space** | **$4N$ Array Space** | **$4N$ Array Space** | $4N$ Integers |

---

## 10. Edge Cases & Boundary Handling
* **Single Element Input ($N = 1$)**: Base case `l == r` sets `tree[0] = nums[0]`, recursion terminates immediately.
* **Negative Numbers in Array**: `Math.min` and `Math.max` handle negative values cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Performing Pre-Order Merging Before Recursing**:
  - Merging left and right values *before* building child subtrees uses uninitialized `0` values.
  - **ALWAYS execute parent merge logic in the POST-ORDER phase after child recursion calls complete**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Segment Tree Construction Runs in $O(N)$ Time:
> A Segment Tree for $N$ elements contains exactly $2N - 1$ total nodes.
> Because `build()` visits every node exactly once and performs $O(1)$ merge work per node, total construction time is strictly **$O(N)$ Linear Time**!

> **Memory Trick:** **"Building a Segment Tree takes O(N) time because it visits 2N - 1 nodes once!"**

---

## 13. System & Implementation Comparisons

| Feature | Dynamic Recursive `build()` | Iterative Bottom-Up Build |
| :--- | :--- | :--- |
| **Code Simplicity** | **High (Clean Divide-and-Conquer) ⚡**| Complex Index Bit-Shifting |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Flexibility** | **Supports Lazy Propagation ⚡**| Hard to add Lazy Propagation |

---

## 14. How to Recognize This in Questions
* **"Construct a data structure to answer range min/max queries in O(log N) time"** $\rightarrow$ Segment Tree Construction.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the post-order merge step in Segment Tree construction?**  
  *A:* Computing `tree[treeIdx] = merge(tree[leftChild], tree[rightChild])` after left and right subsegments have finished building.
* **Q: How many recursive calls are made during `build()` for an array of size $N$?**  
  *A:* Exactly $2N - 1$ calls (one for each node in the Segment Tree).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEGMENT TREE CONSTRUCTION                             |
+-----------------------------------------------------------------------+
| • Divide Step  : mid = l + (r - l) / 2                                |
| • Recurse Left : build(2 * i + 1, l, mid)                             |
| • Recurse Right: build(2 * i + 2, mid + 1, r)                         |
| • Post-Order   : tree[i] = merge(tree[2*i+1], tree[2*i+2]) (SUM/MIN/MAX)|
| • Time Bounds  : O(N) Linear Time (2N - 1 total nodes visited) ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `build()` for Range Sum, Range Min, and Range Max in Java.
- [ ] I can prove why Segment Tree construction takes $O(N)$ time.
- [ ] I know why the merge phase MUST be post-order.
- [ ] I can handle custom merge functions (e.g. GCD).
- [ ] I can trace `build()` step by step on an array of size 4.
