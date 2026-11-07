# 04. Segment Tree Point Updates, Top-Down Path Traversal & Post-Order Merging

## 1. Introduction
A **Point Update** on a **Segment Tree** (specifically **Range Sum Query - Mutable LeetCode 307**) modifies the value of a single element at index `arrIdx` in the input array and updates all ancestor segment nodes along its path. Because a single point update follows a single top-down path from root to leaf and re-computes parent segment values bottom-up, it executes in **$O(\log N)$ Logarithmic Time** and **$O(\log N)$ Auxiliary Call Stack Space**.

> **Important:** The 2-Phase Mechanics of Segment Tree Point Updates:
> 1. **Phase 1: Top-Down Path Traversal**: Binary search down to the target leaf node $[arrIdx \dots arrIdx]$ by comparing `arrIdx` with `mid = L + (R - L) / 2`.
> 2. **Phase 2: Post-Order Parent Merging**: Upon updating leaf `tree[leafIdx] = newVal`, return up the call stack and re-calculate every ancestor's summary value using `tree[treeIdx] = merge(left, right)`! ⚡

```
Segment Tree Point Update Top-Down & Bottom-Up Pipeline Topology:
Updating Index = 2 to New Value = 9 in Array size N = 4:
Phase 1: Top-Down Search Path ----------------> Node 0 [0..3] -> Node 2 [2..3] -> Node 5 [2..2] (Leaf!)
Phase 2: Update Leaf ------------------------> tree[5] = 9 (Old val 5 replaced by 9)
Phase 3: Bottom-Up Post-Order Re-merging -----> Node 2 [2..3] = 9 + 3 = 12
                                                Node 0 [0..3] = 3 + 12 = 15! ⚡
```

---

## 2. Core Concepts & Point Update Algorithm (LeetCode 307)

### 2.1 The Point Update Algorithm ($O(\log N)$ Time)
To update index `arrIdx` to `val` in Segment Tree range $[L \dots R]$ at `treeIdx`:
1. **Base Case (Leaf Reached)**:
   - If $L == R$:
     - `tree[treeIdx] = val` (Update leaf node value directly!).
     - `nums[arrIdx] = val`.
     - Return.
2. **Top-Down Navigation**:
   - `mid = L + (R - L) / 2`.
   - If `arrIdx <= mid`: Recurse Left $\implies$ `update(2 * treeIdx + 1, L, mid, arrIdx, val)`.
   - Else (`arrIdx > mid`): Recurse Right $\implies$ `update(2 * treeIdx + 2, mid + 1, R, arrIdx, val)`.
3. **Post-Order Re-merge**:
   - Re-compute parent summary value: `tree[treeIdx] = merge(tree[2 * treeIdx + 1], tree[2 * treeIdx + 2])`.

```
Point Update Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Traversal Phase       | Index Condition   | Action Taken      | Return State      |
+-----------------------+-------------------+-------------------+-------------------+
| **Leaf Target**       | $L == R$          | `tree[i] = val`   | Base Case Return  |
| **Go Left**           | $arrIdx \le mid$  | Recurse Left Child| Top-down search   |
| **Go Right**          | $arrIdx > mid$    | Recurse Right Child| Top-down search   |
| **Post-Order Merge**  | On Return Path    | `tree[i] = merge` | Re-merges ancestor|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Point Update: Go left if arrIdx <= mid, else right! Update leaf, re-merge parents on return in O(log N) time!"**

---

## 3. Characteristics & $O(\log N)$ Path Bounds

### 3.1 Mathematical Proof of $O(\log N)$ Point Update Complexity
* A single array element `nums[arrIdx]` belongs to exactly 1 leaf node in the Segment Tree.
* There is exactly **1 path** from the root node $[0 \dots N-1]$ down to leaf $[arrIdx \dots arrIdx]$.
* The length of this path equals the height of the tree $H = \lceil \log_2 N \rceil$.
* Exactly $H$ nodes are visited during top-down traversal, and $H$ parent merge operations are executed on return.
* Total Time Complexity: $\mathbf{O(\log N) \text{ Logarithmic Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Update of Index 2 to Value 9 in Segment Tree `[2, 1, 5, 3]` ($N=4$):

```
Initial Tree: Root 0..3 (11). Left 0..1 (3). Right 2..3 (8). Leaf 2..2 (5).

Call update(arrIdx=2, val=9):
1. Root [0..3]: mid = 1. arrIdx (2) > 1 -> Recurse Right child [2..3] (node 2).
2. Node 2 [2..3]: mid = 2. arrIdx (2) <= 2 -> Recurse Left child [2..2] (node 5).
3. Leaf Node 5 [2..2]: L == R (2 == 2) -> Set tree[5] = 9. Return!

Post-Order Re-merging:
4. Return to Node 2 [2..3]: Re-merge tree[2] = tree[5] (9) + tree[6] (3) = 12.
5. Return to Root Node 0 [0..3]: Re-merge tree[0] = tree[1] (3) + tree[2] (12) = 15.

Array element updated and all ancestors re-merged in 3 steps! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Segment Tree Point Update Top-Down & Bottom-Up Path Topography:

```
                      [ Node 0: Sum 11 -> 15 ] (Re-merged!)
                     /                        \
      [ Node 1: Range 0..1 ]               [ Node 2: Sum 8 -> 12 ] (Re-merged!)
     /                     \              /                       \
[0..0: Val=2]        [1..1: Val=1]    [2..2: Val 5 -> 9]       [3..3: Val=3]
                                      (Leaf Updated!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 307 (Range Sum Query - Mutable with Point Update and Range Query):

```java
import java.util.*;

// LeetCode 307: Range Sum Query - Mutable
public class NumArray {

    private final int[] tree;
    private final int[] nums;
    private final int n;

    public NumArray(int[] nums) {
        this.nums = nums;
        this.n = nums.length;
        this.tree = new int[4 * n];

        if (n > 0) {
            build(0, 0, n - 1);
        }
    }

    private void build(int treeIdx, int l, int r) {
        if (l == r) {
            tree[treeIdx] = nums[l];
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * treeIdx + 1, l, mid);
        build(2 * treeIdx + 2, mid + 1, r);
        tree[treeIdx] = tree[2 * treeIdx + 1] + tree[2 * treeIdx + 2];
    }

    // Point Update LeetCode 307 O(log N) Time
    public void update(int index, int val) {
        if (index < 0 || index >= n) return;
        updateHelper(0, 0, n - 1, index, val);
    }

    private void updateHelper(int treeIdx, int l, int r, int arrIdx, int val) {
        // Base Case: Target Leaf Node Reached
        if (l == r) {
            nums[arrIdx] = val;
            tree[treeIdx] = val; // Direct leaf update
            return;
        }

        int mid = l + (r - l) / 2;
        int leftChild = 2 * treeIdx + 1;
        int rightChild = 2 * treeIdx + 2;

        // Top-Down Navigation
        if (arrIdx <= mid) {
            updateHelper(leftChild, l, mid, arrIdx, val);
        } else {
            updateHelper(rightChild, mid + 1, r, arrIdx, val);
        }

        // Post-Order Re-merge Phase: Re-calculate parent summary value
        tree[treeIdx] = tree[leftChild] + tree[rightChild];
    }

    // Range Sum Query LeetCode 307 O(log N) Time
    public int sumRange(int left, int right) {
        return queryHelper(0, 0, n - 1, left, right);
    }

    private int queryHelper(int treeIdx, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tree[treeIdx]; // Total Overlap
        if (r < ql || l > qr) return 0;               // No Overlap

        int mid = l + (r - l) / 2;
        return queryHelper(2 * treeIdx + 1, l, mid, ql, qr) + 
               queryHelper(2 * treeIdx + 2, mid + 1, r, ql, qr);
    }
}
```

> **Quick Syntax:**
```java
// Segment Tree Point Update Directional Check
if (arrIdx <= mid) updateHelper(leftChild, l, mid, arrIdx, val);
else updateHelper(rightChild, mid + 1, r, arrIdx, val);
tree[treeIdx] = tree[leftChild] + tree[rightChild]; // Re-merge
```

---

## 7. Concrete Problem Examples
* **LeetCode 307 - Range Sum Query - Mutable**: Primary point update problem.
* **Dynamic Leaderboard Engines**: Updating player scores dynamically.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 307 `NumArray`:

```java
public class SegmentTreeUpdatesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 307 Point Update Test ===");
        int[] nums = {1, 3, 5};
        NumArray numArray = new NumArray(nums);

        System.out.println("Sum Range [0 ... 2]: " + numArray.sumRange(0, 2)); // Output: 9 (1+3+5)

        System.out.println("\nUpdating Index 1 to Value 2...");
        numArray.update(1, 2); // Array becomes [1, 2, 5]

        System.out.println("Sum Range [0 ... 2] AFTER Update: " + 
            numArray.sumRange(0, 2)); // Output: 8 (1+2+5) ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Method | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`update(index, val)`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space |
| **`sumRange(l, r)`**   | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Updating First Index (`index = 0`)**: Follows leftmost path down to leaf 0.
* **Updating Last Index (`index = N - 1`)**: Follows rightmost path down to leaf $N - 1$.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting the Post-Order Re-merge Step After Recursing**:
  - Updating the leaf node without re-calculating `tree[treeIdx] = tree[left] + tree[right]` on the return path leaves ancestor nodes with stale values!
  - **ALWAYS execute parent re-merge logic after the child recursive call returns**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Point Updates Execute in $O(\log N)$ Time:
> A point update affects ONLY the single target leaf node and its direct ancestors.
> Because there are at most $\lceil \log_2 N \rceil$ ancestors along the path from root to leaf, the algorithm updates at most $\log_2 N$ nodes in **$O(\log N)$ time**!

> **Memory Trick:** **"Point update modifies 1 leaf and its log N ancestors! Always re-merge parents on return!"**

---

## 13. System & Implementation Comparisons

| Feature | Segment Tree Point Update | Prefix Sum Array Update |
| :--- | :--- | :--- |
| **Point Update Speed** | **$O(\log N)$ Logarithmic ⚡** | $O(N)$ Linear Scan ❌ |
| **Range Query Speed** | **$O(\log N)$ Logarithmic ⚡** | **$O(1)$ Constant Time ⚡** |
| **Affected Elements** | Only $\log_2 N$ Ancestors | All $N - \text{index}$ Downstream Elements |

---

## 14. How to Recognize This in Questions
* **"Modify single element at index i and query range sum in O(log N) time"** $\rightarrow$ LeetCode 307 (Segment Tree Point Update).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is binary navigation `arrIdx <= mid` used for point update?**  
  *A:* Because `mid` partitions the array into left range $[L \dots \text{mid}]$ and right range $[\text{mid}+1 \dots R]$. If `arrIdx <= mid`, the target leaf is strictly in the left subtree.
* **Q: Can point update be written iteratively?**  
  *A:* Yes! By navigating to leaf node `treeIdx = leafPos` and looping upwards `treeIdx /= 2` until reaching root.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEGMENT TREE POINT UPDATES (LEETCODE 307)             |
+-----------------------------------------------------------------------+
| • Base Case    : If (l == r) { tree[treeIdx] = val; return; }         |
| • Top-Down     : If (arrIdx <= mid) recurse left; else recurse right  |
| • Post-Order   : tree[treeIdx] = tree[leftChild] + tree[rightChild]   |
| • Time Bounds  : O(log N) Logarithmic Time (Updates log2 N ancestors) ⚡|
| • Space Bounds : O(log N) Call Stack Auxiliary Space                  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 307 (`NumArray`) from memory in 4 minutes.
- [ ] I can write `updateHelper` with directional checking (`arrIdx <= mid`).
- [ ] I know why parent re-merging MUST be executed post-order.
- [ ] I can prove why point update visits at most $\log_2 N$ nodes.
- [ ] I can trace a point update step by step.
