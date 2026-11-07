# 10. Lowest Common Ancestor (LCA), Subtree Branching & BST Partitioning Mechanics

## 1. Introduction
The **Lowest Common Ancestor (LCA)** of two nodes $P$ and $Q$ in a Binary Tree is defined as the deepest node $T$ that has both $P$ and $Q$ as descendants (where a node is allowed to be a descendant of itself). LCA algorithms—including **Lowest Common Ancestor of a Binary Tree (LeetCode 236)**, **Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)**, and **Lowest Common Ancestor with Parent Pointers (LeetCode 1650)**—are fundamental to network routing protocols, inheritance hierarchies, and tree distance computations in **$O(N)$ linear time** or **$O(H)$ BST search time**.

> **Important:** Why does LCA in a Binary Search Tree (LeetCode 235) run in **$O(H)$ time and $O(1)$ auxiliary space**?
> In a BST, values $P.val$ and $Q.val$ dictate tree branching!
> * If BOTH $P.val$ and $Q.val$ are LESS than `curr.val`: LCA MUST lie in the **LEFT subtree**!
> * If BOTH $P.val$ and $Q.val$ are GREATER than `curr.val`: LCA MUST lie in the **RIGHT subtree**!
> * If $P.val$ and $Q.val$ **SPLIT** across `curr.val` (or one matches `curr.val`): `curr` is the **LOWEST COMMON ANCESTOR**! ⚡

```
BST LCA Split Point Topology (LeetCode 235):
Target Nodes P = 2, Q = 8
Current Root = 6  --->  P (2) < 6 AND Q (8) > 6  (SPLIT CONDITION DETECTED!)
Node 6 is the Lowest Common Ancestor! ⚡
```

---

## 2. Core Concepts & Binary Tree LCA (LeetCode 236)

### 2.1 Lowest Common Ancestor of a General Binary Tree (LeetCode 236)
Given a binary tree (NOT a BST) and two nodes $P$ and $Q$:

#### Bottom-Up Divide-and-Conquer Algorithm ($O(N)$ Time, $O(H)$ Auxiliary Space):
1. Base Case: If `root == null` OR `root == p` OR `root == q`, return `root`!
2. Recurse into left subtree: `left = lowestCommonAncestor(root.left, p, q)`.
3. Recurse into right subtree: `right = lowestCommonAncestor(root.right, p, q)`.
4. **Decision Conditions**:
   - **Case A**: Both `left != null` AND `right != null` $\rightarrow$ $P$ and $Q$ were found in separate subtrees! **`root` IS THE LCA**! Return `root`!
   - **Case B**: `left != null` AND `right == null` $\rightarrow$ Both nodes reside in the left subtree. Return `left`.
   - **Case C**: `left == null` AND `right != null` $\rightarrow$ Both nodes reside in the right subtree. Return `right`.
   - **Case D**: Both `null` $\rightarrow$ Return `null`.

```
Binary Tree LCA Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Left Return           | Right Return      | LCA Result        | Interpretation    |
+-----------------------+-------------------+-------------------+-------------------+
| **Non-Null**          | **Non-Null**      | **`root` ⚡**     | P & Q split here  |
| Non-Null              | Null              | `left`            | Both in Left tree |
| Null                  | Non-Null          | `right`           | Both in Right tree|
| Null                  | Null              | `null`            | Neither found     |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Binary Tree LCA: If left != null AND right != null, root is the LCA! Else return non-null side!"**

---

## 3. Characteristics & LCA with Parent Pointers (LeetCode 1650)

### 3.1 LCA with Parent Pointers (LeetCode 1650 - Two Pointer Intersection)
Given two nodes $P$ and $Q$ where each node has a pointer to its `.parent`:
* **Analogy**: Finding LCA of two nodes with parent pointers is IDENTICAL to finding the **Intersection Point of Two Linked Lists (LeetCode 160)**!
* **Two-Pointer Algorithm ($O(H)$ Time, $O(1)$ Auxiliary Space)**:
  1. Set `p1 = p`, `p2 = q`.
  2. While `p1 != p2`:
     - `p1 = (p1 == null) ? q : p1.parent;`
     - `p2 = (p2 == null) ? p : p2.parent;`
  3. Return `p1`.

```
Two-Pointer Parent Traversal Equality:
Path(P -> Root) + Path(Q -> Root) == Path(Q -> Root) + Path(P -> Root)
Both pointers traverse equal total distances and meet at the LCA node in O(H) time! ⚡
```

---

## 4. Internal Working Mechanics
Tracing LCA of a BST (LeetCode 235) on `root = 6`, `p = 2`, `q = 8`:

```
Init: curr = 6

Check 1: p.val (2) < curr.val (6) AND q.val (8) > curr.val (6).
  - Split condition triggered! Node 2 is in left subtree; Node 8 is in right subtree.
  - Node 6 is the Lowest Common Ancestor!

Returns Node 6 in O(1) Search Steps! ✅
```

---

## 5. Visual Diagram
LCA Binary Tree Subtree Split Point Topography:

```
                      [ Root 3 (LCA!) ]  <--- Left & Right returns NON-NULL!
                      /               \
            (Left != null)          (Right != null)
                 /                         \
           [ Node P (5) ]            [ Node Q (1) ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LCA of Binary Tree (LeetCode 236), LCA of BST (LeetCode 235), and LCA with Parent Pointers (LeetCode 1650):

```java
import java.util.*;

public class LowestCommonAncestorMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    public static class Node {
        public int val;
        public Node left;
        public Node right;
        public Node parent;

        public Node(int val) {
            this.val = val;
        }
    }

    // 1. LCA of a General Binary Tree (LeetCode 236) O(N) Time, O(H) Space
    public static TreeNode lowestCommonAncestorBT(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root; // Base case: target node found or null reached
        }

        TreeNode left = lowestCommonAncestorBT(root.left, p, q);
        TreeNode right = lowestCommonAncestorBT(root.right, p, q);

        // If p and q are found in different subtrees, root is the LCA!
        if (left != null && right != null) {
            return root;
        }

        // Otherwise return the non-null subtree result
        return (left != null) ? left : right;
    }

    // 2. LCA of a Binary Search Tree (LeetCode 235) O(H) Time, O(1) Auxiliary Space
    public static TreeNode lowestCommonAncestorBST(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val && q.val < curr.val) {
                curr = curr.left; // Both nodes in left subtree
            } else if (p.val > curr.val && q.val > curr.val) {
                curr = curr.right; // Both nodes in right subtree
            } else {
                return curr; // Split point or match found -> LCA!
            }
        }

        return null;
    }

    // 3. LCA with Parent Pointers (LeetCode 1650) O(H) Time, O(1) Auxiliary Space
    public static Node lowestCommonAncestorParent(Node p, Node q) {
        Node p1 = p;
        Node p2 = q;

        // Two-pointer linked list intersection algorithm
        while (p1 != p2) {
            p1 = (p1 == null) ? q : p1.parent;
            p2 = (p2 == null) ? p : p2.parent;
        }

        return p1;
    }
}
```

> **Quick Syntax:**
```java
// General Binary Tree LCA Split Line
if (left != null && right != null) return root;
return (left != null) ? left : right;
```

---

## 7. Concrete Problem Examples
* **LeetCode 236 - Lowest Common Ancestor of a Binary Tree**: Bottom-up DFS recursion.
* **LeetCode 235 - Lowest Common Ancestor of a Binary Search Tree**: $O(H)$ BST split search.
* **LeetCode 1650 - Lowest Common Ancestor of a Binary Tree III**: Two-pointer parent traversal.
* **LeetCode 865 - Smallest Subtree with all the Deepest Nodes**: LCA of deepest leaves.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LCA in BST and General Binary Tree:

```java
public class LowestCommonAncestorDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LCA of Binary Search Tree (LeetCode 235) ===");
        LowestCommonAncestorMaster.TreeNode rootBST = new LowestCommonAncestorMaster.TreeNode(6);
        rootBST.left = new LowestCommonAncestorMaster.TreeNode(2);
        rootBST.right = new LowestCommonAncestorMaster.TreeNode(8);
        rootBST.left.left = new LowestCommonAncestorMaster.TreeNode(0);
        rootBST.left.right = new LowestCommonAncestorMaster.TreeNode(4);

        LowestCommonAncestorMaster.TreeNode lcaBST = 
            LowestCommonAncestorMaster.lowestCommonAncestorBST(rootBST, rootBST.left, rootBST.right);
        System.out.println("LCA of 2 and 8 in BST: " + lcaBST.val); // Output: 6

        System.out.println("\n=== 2. LCA of General Binary Tree (LeetCode 236) ===");
        LowestCommonAncestorMaster.TreeNode lcaBT = 
            LowestCommonAncestorMaster.lowestCommonAncestorBT(rootBST, rootBST.left.left, rootBST.left.right);
        System.out.println("LCA of 0 and 4 in Tree: " + lcaBT.val); // Output: 2 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Variant | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Binary Tree LCA (236)** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Bottom-up DFS split check |
| **BST LCA (235)** | **$O(H)$ Logarithmic ⚡**| **$O(1)$ Strict Constant ⚡**| Value split `p.val < curr < q.val` |
| **Parent Pointer LCA (1650)**| **$O(H)$ Logarithmic ⚡**| **$O(1)$ Strict Constant ⚡**| Two-pointer parent intersection |

---

## 10. Edge Cases & Boundary Handling
* **One Node is Ancestor of Other**: If $P$ is parent of $Q$, $P$ itself is the LCA. Handled cleanly by base check `root == p || root == q`.
* **Nodes Not Present in Tree**: Standard LeetCode 236 assumes $P$ and $Q$ exist. If nodes may not exist, a 2-pass verification check is required.

---

## 11. Common Mistakes & Anti-Patterns
* **Using $O(N)$ General Binary Tree LCA for a BST**:
  - Running LeetCode 236 DFS on a BST wastes BST search ordering.
  - **Use BST value branching (LeetCode 235) for $O(H)$ time and $O(1)$ space**.
* **Forgetting Base Case `root == p || root == q`**:
  - Missing the target node check returns `null` prematurely.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `left != null && right != null` Proves Root is LCA:
> `left != null` means target node $P$ (or $Q$) was found in the left subtree.
> `right != null` means target node $Q$ (or $P$) was found in the right subtree.
> Since $P$ and $Q$ reside in OPPOSITE subtrees of `root`, `root` is the LOWEST common node that unites them!

> **Memory Trick:** **"If left and right DFS calls both return non-null, root IS the LCA!"**

---

## 13. System & Implementation Comparisons

| Feature | Binary Tree LCA (236) | BST LCA (235) |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ Full Tree Traversal | **$O(H)$ Logarithmic Search ⚡** |
| **Auxiliary Memory** | $O(H)$ Recursion Stack | **$O(1)$ Iterative Space ⚡** |
| **Branch Decision** | Bottom-up recursion returns | Top-down `p.val` vs `curr.val` |

---

## 14. How to Recognize This in Questions
* **"Find lowest common ancestor of two nodes in binary tree"** $\rightarrow$ LeetCode 236.
* **"Find lowest common ancestor in Binary Search Tree"** $\rightarrow$ LeetCode 235 ($O(H)$ BST split search).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the two-pointer algorithm solve LCA with parent pointers (LeetCode 1650)?**  
  *A:* Because resetting `p1 = q` when reaching root and `p2 = p` when reaching root forces both pointers to traverse a total distance of `depth(P) + depth(Q)`. They arrive at the intersection node (LCA) at the exact same step.
* **Q: What is the distance between two nodes $P$ and $Q$ in a Binary Tree?**  
  *A:* $\text{Distance}(P, Q) = \text{Depth}(P) + \text{Depth}(Q) - 2 \cdot \text{Depth}(\text{LCA}(P, Q))$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LOWEST COMMON ANCESTOR (LCA)                          |
+-----------------------------------------------------------------------+
| • General Tree LCA (236): If left != null && right != null -> root!   |
| • Base Check Rule: If root == null || root == p || root == q -> root  |
| • BST LCA (235): Move left if p,q < curr; move right if p,q > curr    |
| • BST Split Rule: If p and q split across curr, curr IS the LCA!      |
| • Parent Pointers (1650): p1 = (p1==null)?q:p1.parent (2-pointer)     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LCA of a Binary Tree (LeetCode 236) in 10 lines.
- [ ] I can write LCA of a BST (LeetCode 235) in $O(1)$ space.
- [ ] I can write LCA with Parent Pointers (LeetCode 1650).
- [ ] I know why `left != null && right != null` identifies the LCA.
- [ ] I know how to compute node-to-node distance using LCA.
