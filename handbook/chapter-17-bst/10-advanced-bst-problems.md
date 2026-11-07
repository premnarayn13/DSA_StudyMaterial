# 10. Advanced BST Problems, Catalan Numbers & Augmented Size Trees

## 1. Introduction
**Advanced BST Problems** solve complex combinatorial counting, structural balance restoration, and order statistic problems. Algorithms like **Unique Binary Search Trees (LeetCode 96 - Catalan Number Counting)**, **Unique Binary Search Trees II (LeetCode 95 - Structural Construction)**, **Balance a Binary Search Tree (LeetCode 1382)**, and **Count of Smaller Numbers After Self (LeetCode 315 - Augmented BST)** execute in **$O(N)$ linear or $O(N \log N)$ logarithmic time** using Catalan recurrence formulas, divide-and-conquer midpoint partitioning, and augmented node size attributes.

> **Important:** Core Advanced BST Patterns:
> 1. **Catalan Number Counting (LeetCode 96)**: The total number of structurally unique BSTs formed by $N$ distinct keys is given by the **$N$-th Catalan Number**:
>    $$C_N = \frac{1}{N + 1} \binom{2N}{N} = \sum_{i=0}^{N-1} C_i \cdot C_{N-1-i}$$
> 2. **Balance a BST (LeetCode 1382)**: Extract sorted keys via In-Order traversal ($O(N)$), then reconstruct a perfectly balanced BST using **Midpoint Selection (`mid = (left + right) / 2`)** in **$O(N)$ linear time**! ⚡

```
Catalan Structural Permutations (N = 3 Keys: [1, 2, 3] -> C3 = 5 Unique BSTs):
    1         1         2         3         3
     \         \       / \       /         /
      3         2     1   3     2         1
     /           \             /           \
    2             3           1             2
```

---

## 2. Core Concepts & Catalan Number Counting (LeetCode 96)

### 2.1 Unique Binary Search Trees (LeetCode 96)
Given an integer $N$, return the number of structurally unique BSTs that store values $1 \dots N$:

#### DP Recurrence ($O(N^2)$ Time, $O(N)$ Auxiliary Space):
* Choose key $i$ ($1 \le i \le N$) as the root.
* Number of nodes in Left Subtree = $i - 1$. (Number of valid left tree shapes = `dp[i - 1]`).
* Number of nodes in Right Subtree = $N - i$. (Number of valid right tree shapes = `dp[N - i]`).
* Combination rule for root $i$: `dp[i - 1] * dp[N - i]`.

$$\mathbf{dp[N] = \sum_{i=1}^{N} dp[i - 1] \cdot dp[N - i]}$$

```
Advanced BST Problem Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem               | Core Pattern      | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Unique BSTs I (96)**| Catalan DP        | **$O(N^2)$ ⚡**   | $O(N)$ DP Array   |
| **Unique BSTs II (95)**| Subtree Generator | **$O(C_N)$ ⚡**   | $O(C_N)$ List     |
| **Balance BST (1382)**| In-Order + Mid    | **$O(N)$ Linear ⚡**| $O(N)$ Array Space|
| **Smaller After (315)**| Augmented BST     | **$O(N \log N)$ ⚡**| $O(N)$ Tree Space |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Unique BST count = N-th Catalan Number C_N! dp[n] = sum(dp[i - 1] * dp[n - i])!"**

---

## 3. Characteristics & Balance a BST (LeetCode 1382)

### 3.1 Balance a Binary Search Tree (LeetCode 1382)
Given the root of an arbitrary (possibly skewed) BST, return a **Height-Balanced BST**:
1. **In-Order Traversal Pass**: Extract all node references into an `ArrayList<TreeNode> sortedNodes` in strictly ascending order ($O(N)$ time).
2. **Divide-and-Conquer Midpoint Reconstruction**:
   `buildBalanced(sortedNodes, left, right)`:
   - Base Case: `if (left > right) return null;`
   - `mid = left + (right - left) / 2;`
   - `root = sortedNodes.get(mid);`
   - `root.left = buildBalanced(sortedNodes, left, mid - 1);`
   - `root.right = buildBalanced(sortedNodes, mid + 1, right);`
   - Return `root`.
3. Total Time: **$O(N)$ Linear Time**, Auxiliary Space: **$O(N)$ Array Space**.

---

## 4. Internal Working Mechanics
Tracing Balance a BST (LeetCode 1382) on Skewed Tree `1 -> 2 -> 3 -> 4`:

```
Step 1: In-Order Traversal -> sortedNodes = [Node(1), Node(2), Node(3), Node(4)].

Step 2: buildBalanced(0, 3):
  - mid = 1 -> Root = Node(2).
  - Left Call (0, 0)   -> Node(1).
  - Right Call (2, 3)  -> mid = 2 -> Node(3), Right Child Node(4).

Reconstructed Tree = [2, 1, 3, null, null, null, 4] (Height H = 3, Perfectly Balanced!) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Balance a BST In-Order + Midpoint Partition Topography:

```
Skewed Input Tree:                  Sorted Array: [ 1 | 2 | 3 | 4 ]
    (1)                                                 ^ (Mid = Index 1)
      \                                               Root
      (2)                            Balanced Resulting BST:
        \                                       (2)
        (3)                                    /   \
          \                                  (1)   (3)
          (4)                                        \
                                                     (4)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Unique BSTs I (LeetCode 96), Unique BSTs II (LeetCode 95), and Balance a BST (LeetCode 1382):

```java
import java.util.*;

public class AdvancedBSTProblemsMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // 1. Unique Binary Search Trees Count (LeetCode 96) Catalan DP O(N^2) Time, O(N) Space
    public static int numTrees(int n) {
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = 1;

        for (int i = 2; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                // dp[j - 1] = left subtrees; dp[i - j] = right subtrees
                dp[i] += dp[j - 1] * dp[i - j];
            }
        }

        return dp[n];
    }

    // 2. Unique Binary Search Trees II Generator (LeetCode 95) O(C_N) Time
    public static List<TreeNode> generateTrees(int n) {
        if (n == 0) return new ArrayList<>();
        return buildTreeList(1, n);
    }

    private static List<TreeNode> buildTreeList(int start, int end) {
        List<TreeNode> list = new ArrayList<>();
        if (start > end) {
            list.add(null);
            return list;
        }

        for (int i = start; i <= end; i++) {
            List<TreeNode> leftSubtrees = buildTreeList(start, i - 1);
            List<TreeNode> rightSubtrees = buildTreeList(i + 1, end);

            // Permute all left and right subtree combinations
            for (TreeNode left : leftSubtrees) {
                for (TreeNode right : rightSubtrees) {
                    TreeNode root = new TreeNode(i);
                    root.left = left;
                    root.right = right;
                    list.add(root);
                }
            }
        }

        return list;
    }

    // 3. Balance a Binary Search Tree (LeetCode 1382) O(N) Time, O(N) Space
    public static TreeNode balanceBST(TreeNode root) {
        List<TreeNode> sortedNodes = new ArrayList<>();
        inorderExtract(root, sortedNodes);
        return buildBalancedBST(sortedNodes, 0, sortedNodes.size() - 1);
    }

    private static void inorderExtract(TreeNode node, List<TreeNode> list) {
        if (node == null) return;
        inorderExtract(node.left, list);
        list.add(node);
        inorderExtract(node.right, list);
    }

    private static TreeNode buildBalancedBST(List<TreeNode> list, int left, int right) {
        if (left > right) return null;

        int mid = left + (right - left) / 2;
        TreeNode node = list.get(mid);

        node.left = buildBalancedBST(list, left, mid - 1);
        node.right = buildBalancedBST(list, mid + 1, right);

        return node;
    }
}
```

> **Quick Syntax:**
```java
// Balance BST Midpoint Build Line
int mid = left + (right - left) / 2;
TreeNode node = list.get(mid);
node.left = build(list, left, mid - 1); node.right = build(list, mid + 1, right);
```

---

## 7. Concrete Problem Examples
* **LeetCode 96 - Unique Binary Search Trees**: Catalan DP counting.
* **LeetCode 95 - Unique Binary Search Trees II**: Structural tree list generator.
* **LeetCode 1382 - Balance a Binary Search Tree**: In-order + midpoint partition.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Unique BSTs count and Balance a BST:

```java
public class AdvancedBSTProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Unique BSTs Count (LeetCode 96) ===");
        System.out.println("Unique BSTs for N = 3: " + 
            AdvancedBSTProblemsMaster.numTrees(3)); // Output: 5 (C3 Catalan Number!)

        System.out.println("\n=== 2. Balance a BST (LeetCode 1382) ===");
        // Build Skewed BST: 1 -> 2 -> 3 -> 4
        AdvancedBSTProblemsMaster.TreeNode skewed = new AdvancedBSTProblemsMaster.TreeNode(1);
        skewed.right = new AdvancedBSTProblemsMaster.TreeNode(2);
        skewed.right.right = new AdvancedBSTProblemsMaster.TreeNode(3);
        skewed.right.right.right = new AdvancedBSTProblemsMaster.TreeNode(4);

        AdvancedBSTProblemsMaster.TreeNode balanced = 
            AdvancedBSTProblemsMaster.balanceBST(skewed);

        System.out.println("New Balanced Root Val: " + balanced.val); // Output: 2 (Midpoint!)
        System.out.println("New Root Left Val:     " + balanced.left.val); // Output: 1 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Unique BSTs I (96)** | **$O(N^2)$ Quadratic ⚡** | $O(N)$ DP Array Space | Catalan DP recurrence |
| **Unique BSTs II (95)**| **$O(C_N)$ Catalan ⚡** | $O(C_N)$ Tree List Space| Permuting subtrees |
| **Balance a BST (1382)**| **$O(N)$ Linear ⚡** | **$O(N)$ Array Space ⚡**| In-order extract + midpoint build |

---

## 10. Edge Cases & Boundary Handling
* **$N = 0$ or $N = 1$**: `numTrees` returns 1. `generateTrees` handles base cases cleanly.
* **Already Balanced BST**: `balanceBST` returns an equivalent balanced tree structure.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting In-Place Rotations for LeetCode 1382**:
  - Writing complex AVL rotations to rebalance a severely skewed BST is prone to pointer bugs and runs in $O(N \log N)$ time.
  - **Extract nodes into a sorted list ($O(N)$) and build via midpoint partition ($O(N)$)**.
* **Forgetting `list.add(null)` Base Case in LeetCode 95**:
  - Missing `list.add(null)` when `start > end` breaks nested loops permuting left and right subtrees.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why In-Order + Midpoint Partition Balances ANY BST in $O(N)$ Time:
> 1. In-Order traversal extracts all BST nodes into a sorted array in **$O(N)$ time**.
> 2. Selecting `mid = (left + right) / 2` as the root of every range guarantees left and right subtrees have equal node counts (differing by at most 1).
> 3. Recursively constructing subtrees from left and right halves builds a perfectly balanced tree of height $H = \lfloor \log_2 N \rfloor$ in **$O(N)$ time**!

> **Memory Trick:** **"To balance any BST: In-Order extract to sorted list -> Build via midpoint partition!"**

---

## 13. System & Implementation Comparisons

| Feature | In-Order + Midpoint Rebalance | Dynamic Rotation Rebalance (AVL) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡** | $O(N \log N)$ Repeated Rotations |
| **Auxiliary Memory** | $O(N)$ Array Space | **$O(\log N)$ Call Stack ⚡** |
| **Code Simplicity** | **High (Simple 2-pass) ⚡** | Low (Complex 4-case rotation logic) |

---

## 14. How to Recognize This in Questions
* **"Find number of structurally unique BSTs for N keys"** $\rightarrow$ LeetCode 96 (Catalan DP).
* **"Balance a Binary Search Tree in O(N) time"** $\rightarrow$ LeetCode 1382 (In-order extract + midpoint build).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Catalan Number formula for $N$ keys?**  
  *A:* $C_N = \frac{1}{N+1} \binom{2N}{N} = \frac{(2N)!}{(N+1)! N!}$.
* **Q: Why does `buildBalancedBST` reuse existing `TreeNode` objects?**  
  *A:* Re-assigning `node.left` and `node.right` pointers on existing `TreeNode` instances avoids allocating new memory, optimizing heap performance.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED BST PROBLEMS & CATALAN RECURRENCE            |
+-----------------------------------------------------------------------+
| • Unique BST Count (96): dp[i] += dp[j - 1] * dp[i - j] (Catalan DP)  |
| • Unique BST List (95) : Permute leftSubtrees * rightSubtrees         |
| • Balance BST (1382)   : Step 1: In-order extract to sorted list        |
|                          Step 2: Build tree picking mid = (left+right)/2|
| • Time Bounds          : Balance BST runs in O(N) Linear Time ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Unique Binary Search Trees (LeetCode 96) using Catalan DP.
- [ ] I can write Unique Binary Search Trees II (LeetCode 95) tree generator.
- [ ] I can write Balance a Binary Search Tree (LeetCode 1382) in $O(N)$ time.
- [ ] I know why midpoint selection guarantees height balance.
- [ ] I can state the $N$-th Catalan Number formula.
