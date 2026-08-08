# 07. Lowest Common Ancestor (LCA) Architecture & Subtree Match Patterns

## 1. Introduction
The **Lowest Common Ancestor (LCA)** of two nodes $P$ and $Q$ in a tree is defined as the deepest node $T$ that has both $P$ and $Q$ as descendants (where a node is allowed to be a descendant of itself). In technical coding interviews and graph algorithms, LCA is a landmark problem. Variants range from **LCA in a General Binary Tree (LeetCode 236)** using bottom-up Post-Order DFS, **LCA with Parent Pointers (LeetCode 1650)** using the Two-Pointer Linked List Intersection technique, to **LCA of Deepest Leaves (LeetCode 1123)**.

> **Important:** In general binary trees without search properties, LCA MUST be solved using **Post-Order DFS** (bottom-up processing). Subtrees return non-null references if target nodes are found, enabling the parent node to detect when both left and right subtrees match!

```
LCA Algorithmic Variants:
+-----------------------------------------------------------------------------------+
| General Binary Tree LCA (236) : Post-Order DFS Bottom-Up Match    -> O(N) Time ⚡ |
| Parent Pointer LCA (1650)     : Two Pointers Cycle Intersection   -> O(H) Time ⚡ |
| BST LCA (235)                 : Value Comparison Splitting        -> O(H) Time ⚡ |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Post-Order Subtree Match Logic

### 2.1 Post-Order DFS Subtree Match Principle
In a General Binary Tree, searching for $\text{LCA}(P, Q)$ evaluates subtrees recursively:
1. **Base Case**: If `curr == null || curr == p || curr == q`, return `curr`.
2. **Post-Order Subtree Search**:
   - `leftMatch = lowestCommonAncestor(curr.left, p, q)`
   - `rightMatch = lowestCommonAncestor(curr.right, p, q)`
3. **Synthesis Logic**:
   - **Case 1 (Split Point)**: If `leftMatch != null` AND `rightMatch != null`, node `curr` is the **Lowest Common Ancestor**! Return `curr`.
   - **Case 2 (Single Subtree Match)**: If only one subtree returns a non-null node, return `leftMatch != null ? leftMatch : rightMatch`.
   - **Case 3 (No Match)**: If both subtrees return `null`, return `null`.

### 2.2 Parent Pointer LCA (LeetCode 1650)
If nodes contain a `.parent` pointer, finding LCA reduces to the **Intersection Point of Two Linked Lists (LeetCode 160)**!
* Pointer $A$ starts at $P$ and moves up `a = a.parent`. When reaching `null`, redirect to $Q$.
* Pointer $B$ starts at $Q$ and moves up `b = b.parent`. When reaching `null`, redirect to $P$.
* Pointer $A$ and Pointer $B$ will meet at the LCA node in **$O(H)$ time and $O(1)$ space**!

```
Parent Pointer LCA Linked List Analogy:
Path P -> Root:  P -> ... -> LCA -> ... -> Root
Path Q -> Root:  Q -> ... -> LCA -> ... -> Root

Pointer A: P -> Root -> Q -> Root
Pointer B: Q -> Root -> P -> Root
Pointers meet at LCA after (dist(P, LCA) + dist(Q, LCA) + dist(LCA, Root)) steps!
```

> **Memory Trick:** **"General Tree LCA: If both left and right matches non-null -> return curr! If parent pointers exist -> Two Pointers Linked List Intersection!"**

---

## 3. Characteristics & Problem Variations

### 3.1 LCA of Deepest Leaves (LeetCode 1123)
* Return a tuple `Result{TreeNode lca, int maxDepth}`.
* At each node `curr`:
  - Recurse left: `leftResult = dfs(curr.left, depth + 1)`.
  - Recurse right: `rightResult = dfs(curr.right, depth + 1)`.
* If `leftResult.maxDepth == rightResult.maxDepth`, `curr` is the **LCA of the deepest leaves** at that level!

```
LCA Strategy Selection Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Tree Information  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| General Binary Tree(236)| No Search Order  | O(N) Linear ⚡    | O(H) Call Stack   |
| BST LCA (235)         | BST Value Order   | O(H) Logarithmic⚡| O(1) Iterative ⚡ |
| Parent Pointers (1650)| `.parent` Field   | O(H) Logarithmic⚡| O(1) Auxiliary ⚡ |
| Deepest Leaves (1123) | Deepest Depth     | O(N) Linear ⚡    | O(H) Call Stack   |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing General Binary Tree LCA (LeetCode 236) on `P = 5, Q = 1`:

```
          ( 3 )  <- Both leftMatch(5) and rightMatch(1) non-null -> RETURNS 3 as LCA!
         /     \
       ( 5 )   ( 1 )
      /     \
    ( 6 )   ( 2 )

1. Recurse Node 3:
   - Call left: lowestCommonAncestor(5, 5, 1) -> Returns Node 5 (Base case curr == p!).
   - Call right: lowestCommonAncestor(1, 5, 1) -> Returns Node 1 (Base case curr == q!).
2. Evaluate Node 3 Synthesis:
   - leftMatch = Node 5, rightMatch = Node 1.
   - Both non-null! Node 3 is the LCA.

Result: LCA(5, 1) = Node 3 ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Post-Order Subtree Synthesis Cases Topography:

```
[ CASE 1: SPLIT POINT LCA ]            [ CASE 2: ANCESTOR IS TARGET NODE ]
           ( LCA )                                ( P / LCA )
          /       \                                  /
      [ P Match ]  [ Q Match ]                     ( ... )
                                                     /
                                                  ( Q )

leftMatch != null && rightMatch != null   leftMatch (Q) != null, curr == P!
=> Returns LCA!                           => Returns P as LCA!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing General Tree LCA (LeetCode 236), Parent Pointer LCA (LeetCode 1650), and LCA of Deepest Leaves (LeetCode 1123):

```java
import java.util.*;

public class LCAMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // Node with Parent Pointer for LeetCode 1650
    public static class Node {
        public int val;
        public Node left;
        public Node right;
        public Node parent;

        public Node(int val) {
            this.val = val;
        }
    }

    // 1. Lowest Common Ancestor of a Binary Tree (LeetCode 236) O(N) Time, O(H) Space
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        // Base Cases: null or found target node p/q
        if (root == null || root == p || root == q) {
            return root;
        }

        // Bottom-Up Post-Order Subtree Traversal
        TreeNode leftMatch = lowestCommonAncestor(root.left, p, q);
        TreeNode rightMatch = lowestCommonAncestor(root.right, p, q);

        // Synthesis Logic
        if (leftMatch != null && rightMatch != null) {
            return root; // Both subtrees matched -> root is LCA!
        }

        return leftMatch != null ? leftMatch : rightMatch;
    }

    // 2. Lowest Common Ancestor with Parent Pointers (LeetCode 1650) O(H) Time, O(1) Space
    public static Node lowestCommonAncestorParent(Node p, Node q) {
        Node a = p;
        Node b = q;

        // Two Pointers Linked List Intersection Technique
        while (a != b) {
            a = (a == null) ? q : a.parent;
            b = (b == null) ? p : b.parent;
        }

        return a; // Intersection point is LCA!
    }

    // 3. LCA of Deepest Leaves (LeetCode 1123 / LeetCode 865) O(N) Time, O(H) Space
    static class DeepestResult {
        TreeNode lca;
        int maxDepth;

        DeepestResult(TreeNode lca, int maxDepth) {
            this.lca = lca;
            this.maxDepth = maxDepth;
        }
    }

    public static TreeNode lcaDeepestLeaves(TreeNode root) {
        return dfsDeepest(root, 0).lca;
    }

    private static DeepestResult dfsDeepest(TreeNode node, int depth) {
        if (node == null) {
            return new DeepestResult(null, depth);
        }

        DeepestResult left = dfsDeepest(node.left, depth + 1);
        DeepestResult right = dfsDeepest(node.right, depth + 1);

        if (left.maxDepth == right.maxDepth) {
            return new DeepestResult(node, left.maxDepth); // Current node is LCA of deepest leaves!
        } else if (left.maxDepth > right.maxDepth) {
            return left;
        } else {
            return right;
        }
    }
}
```

> **Quick Syntax:**
```java
// Parent Pointer LCA Loop Syntax
while (a != b) {
    a = (a == null) ? q : a.parent;
    b = (b == null) ? p : b.parent;
}
return a;
```

---

## 7. Concrete Problem Examples
* **LeetCode 236 - Lowest Common Ancestor of a Binary Tree**: Post-order DFS.
* **LeetCode 1650 - Lowest Common Ancestor of a Binary Tree III**: Parent pointers.
* **LeetCode 1123 - Lowest Common Ancestor of Deepest Leaves**: Depth tuple tracking.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing General LCA and Parent Pointer LCA:

```java
public class LCADemo {

    public static void main(String[] args) {
        // Build General Tree: [3, 5, 1, 6, 2, 0, 8]
        LCAMaster.TreeNode root = new LCAMaster.TreeNode(3);
        root.left = new LCAMaster.TreeNode(5);
        root.right = new LCAMaster.TreeNode(1);
        root.left.left = new LCAMaster.TreeNode(6);
        root.left.right = new LCAMaster.TreeNode(2);

        System.out.println("=== 1. General Binary Tree LCA (LeetCode 236) ===");
        LCAMaster.TreeNode lca1 = LCAMaster.lowestCommonAncestor(root, root.left, root.right);
        System.out.println("LCA(5, 1): " + lca1.val); // Output: 3

        LCAMaster.TreeNode lca2 = LCAMaster.lowestCommonAncestor(root, root.left, root.left.right);
        System.out.println("LCA(5, 2): " + lca2.val); // Output: 5 (Node 5 is ancestor of 2!)

        System.out.println("\n=== 2. Parent Pointer LCA (LeetCode 1650) ===");
        LCAMaster.Node n3 = new LCAMaster.Node(3);
        LCAMaster.Node n5 = new LCAMaster.Node(5);
        LCAMaster.Node n1 = new LCAMaster.Node(1);
        n5.parent = n3;
        n1.parent = n3;

        LCAMaster.Node parentLCA = LCAMaster.lowestCommonAncestorParent(n5, n1);
        System.out.println("Parent LCA(5, 1): " + parentLCA.val); // Output: 3
    }
}
```

---

## 9. Complexity Analysis

| LCA Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **General Tree LCA (236)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Post-Order Subtree Synthesis |
| **Parent Pointers (1650)** | **$O(H)$ Logarithmic⚡**| **$O(1)$ Auxiliary ⚡**| Linked List Intersection |
| **Deepest Leaves (1123)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Depth Result Tuple DFS |

---

## 10. Edge Cases & Boundary Handling
* **One Target Node is Ancestor of Other (e.g. $P$ is parent of $Q$)**: `lowestCommonAncestor` returns $P$ immediately when base case `root == p` matches!
* **Nodes $P$ or $Q$ Do Not Exist in Tree**: Standard LeetCode 236 guarantees $P$ and $Q$ exist. If nodes might not exist, a preliminary validation pass or counting boolean return is required.

---

## 11. Common Mistakes & Anti-Patterns
* **Continuing Search After Matching Both Subtrees**: Once `leftMatch != null && rightMatch != null` evaluates `true`, returning `root` immediately stops unnecessary subtree processing.
* **Using Extra Memory in Parent Pointer LCA**: Storing ancestor paths in a `HashSet` takes $O(H)$ space. Using the Two-Pointer intersection technique requires **$O(1)$ space**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Parent Pointer LCA (1650) vs General LCA (236):
> If parent pointers exist, NEVER build a full DFS recursion stack!
> Treat parent pointers as linked list `.next` references and apply the **Two-Pointer Cycle/Intersection Algorithm** to achieve $O(H)$ time and $O(1)$ auxiliary space!

> **Memory Trick:** **"Parent pointers present? It's a Linked List Intersection problem! Move pointers up to parent; redirect to opposite node on null!"**

---

## 13. System & Implementation Comparisons

| Feature | General Tree LCA (236) | Parent Pointer LCA (1650) |
| :--- | :--- | :--- |
| **Pointers Required** | `left`, `right` | `parent` |
| **Time Complexity** | $O(N)$ Full Tree Visit | **$O(H)$ Path Height ⚡** |
| **Space Complexity** | $O(H)$ Stack | **$O(1)$ Auxiliary ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find lowest common ancestor of two nodes in a general binary tree"** $\rightarrow$ LeetCode 236 (Post-order DFS subtree match).
* **"Find LCA given nodes with parent pointers"** $\rightarrow$ LeetCode 1650 (Two pointers linked list intersection).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `lowestCommonAncestor` return $P$ if $P$ is an ancestor of $Q$?**  
  *A:* Because base case `if (root == p)` returns `p` immediately. The call stack for $Q$ higher up will return `null` for $Q$'s subtree, causing the synthesis check `leftMatch != null ? leftMatch : rightMatch` to pass $P$ all the way up to the root.
* **Q: How does Binary Lifting compute LCA in $O(\log N)$ time for general trees?**  
  *A:* Binary Lifting pre-computes an ancestor table `up[v][j]` storing the $2^j$-th ancestor of node $v$. Using binary jump steps, it lifts nodes to equal depth and finds LCA in $O(\log N)$ time per query.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LOWEST COMMON ANCESTOR (LCA) ARCHITECTURE             |
+-----------------------------------------------------------------------+
| • General Tree LCA Base Case: if (root == null || root == p || root == q) return root;|
| • Subtree Match Logic: leftMatch = LCA(left), rightMatch = LCA(right) |
| • Split Point: if (leftMatch != null && rightMatch != null) return root;|
| • Single Match: return (leftMatch != null) ? leftMatch : rightMatch;  |
| • Parent Pointers (1650): a = (a==null)? q : a.parent; b = (b==null)? p : b.parent;|
| • Deepest Leaves (1123): Left & Right depth equality check            |
| • Complexity: General LCA O(N) Time | Parent LCA O(H) Time, O(1) Space|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write General Tree LCA (LeetCode 236) in under 3 minutes.
- [ ] I know why base case `root == p || root == q` handles ancestor containment.
- [ ] I can write Parent Pointer LCA (LeetCode 1650) using the Two-Pointer intersection trick.
- [ ] I can write LCA of Deepest Leaves (LeetCode 1123).
- [ ] I know how Binary Lifting accelerates multiple LCA queries to $O(\log N)$.
