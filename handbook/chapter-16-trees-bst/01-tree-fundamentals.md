# 01. Tree Fundamentals, Hierarchical Node Structural Anatomy & Memory Overhead

## 1. Introduction
A **Tree** is a non-linear hierarchical data structure consisting of **Nodes** connected by directed or undirected **Edges**, containing zero cycles. Trees represent hierarchical relationships—such as file system directory trees, HTML Document Object Models (DOM), decision trees, and database index B-Trees—enabling logarithmic **$O(\log N)$ search, insertion, and deletion operations** when balanced.

> **Important:** In a valid Tree with $N$ nodes:
> * There is EXACTLY $N - 1$ edges!
> * There is EXACTLY 1 unique simple path from the **Root Node** to any other node.
> * Adding even a single extra edge creates a cycle, transforming the Tree into a general **Graph**!

```
Hierarchical Tree Structural Anatomy Topology:
                    [ Root Node (Level 0, Depth 0) ]
                              /          \
                             /            \
          [ Left Child (Depth 1) ]   [ Right Child (Depth 1) ]
                  /        \                       \
                 /          \                       \
        [ Leaf Node ]    [ Leaf Node ]         [ Leaf Node (Height 0) ]
        (Depth 2)        (Depth 2)             (Depth 2)

Tree Height H = 2 (Max Depth). Total Nodes N = 6. Total Edges E = 5 (N - 1)! ⚡
```

---

## 2. Core Concepts & Structural Terminology

### 2.1 The 12 Canonical Tree Metrics & Terminology
1. **Root**: The topmost node of the tree with no parent (In-degree = 0).
2. **Parent**: A node that has child nodes connected below it.
3. **Child**: A node connected directly below a parent node.
4. **Leaf Node (External Node)**: A node with ZERO children (Out-degree = 0).
5. **Internal Node**: A node with at least one child node.
6. **Siblings**: Nodes that share the exact same parent node.
7. **Ancestors**: All nodes along the path from the root down to a given node.
8. **Descendants**: All nodes along paths extending below a given node.
9. **Degree of a Node**: The total number of children connected to that node.
10. **Degree of a Tree**: The maximum degree of any node in the tree (e.g. Binary Tree Degree = 2).
11. **Depth of a Node**: The number of edges along the path from the **Root** to that node (Root Depth = 0).
12. **Height of a Node**: The number of edges along the longest downward path from that node to a **Leaf** (Leaf Height = 0).
13. **Height of a Tree**: The height of the **Root Node** (Max Depth of any node).

```
Depth vs Height Distinction Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Structural Metric     | Reference Point   | Direction of Count| Value at Root     |
+-----------------------+-------------------+-------------------+-------------------+
| **Depth**             | Measured from **Root**| Top-Down Counting | **Depth = 0**     |
| **Height**            | Measured from **Leaf**| Bottom-Up Counting| **Height = H**    |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Depth goes Top-Down from Root (Root Depth = 0)! Height goes Bottom-Up from Leaf (Leaf Height = 0)!"**

---

## 3. Characteristics & Binary Tree Classifications

### 3.1 The 5 Canonical Binary Tree Classifications
A **Binary Tree** is a tree where every node has AT MOST 2 children (Left Child and Right Child):

1. **Full Binary Tree (Strict Binary Tree)**: Every node has either EXACTLY 0 children or EXACTLY 2 children. No node has only 1 child!
2. **Complete Binary Tree**: Every level is completely filled except possibly the last level, and all nodes in the last level are filled as far **LEFT** as possible. (Crucial property of Binary Heaps!).
3. **Perfect Binary Tree**: All internal nodes have 2 children, and ALL leaf nodes reside at the exact same depth level.
   - Total Nodes $N = 2^{H+1} - 1$ (where $H$ is height).
   - Total Leaves $L = 2^H$.
4. **Balanced Binary Tree**: For EVERY node in the tree, the height difference between its left and right subtrees is AT MOST 1 ($|H_{\text{left}} - H_{\text{right}}| \le 1$).
5. **Degenerate (Skewed) Binary Tree**: Every parent node has only 1 child, collapsing the tree structure into a linear **Singly Linked List** ($O(N)$ height).

```
Perfect Binary Tree Level and Node Growth (Height H = 3):
Level 0: 1 Node  (2^0)
Level 1: 2 Nodes (2^1)
Level 2: 4 Nodes (2^2)
Level 3: 8 Nodes (2^3)
Total Nodes N = 1 + 2 + 4 + 8 = 15 = 2^(3+1) - 1 = 2^4 - 1! ⚡
```

---

## 4. Internal Working Mechanics
Tracing 64-bit JVM Node Memory Footprint for `TreeNode`:

```
JVM 64-Bit Object Layout for TreeNode<T>:
- Object Header (Mark Word + Klass Word) : 16 Bytes
- T data Reference (Compressed OOP)     :  4 Bytes
- TreeNode left Reference               :  4 Bytes
- TreeNode right Reference              :  4 Bytes
- Padding                               :  4 Bytes
--------------------------------------------------
Total Memory per TreeNode = 32 Bytes!

For a tree with N = 1,000,000 nodes:
Total Heap Memory = 32 MB!
Pointer chasing across 1M heap nodes causes L1/L2 CPU cache line misses.
```

---

## 5. Visual Diagram
Tree Classifications Structural Topography:

```
Full Binary Tree:         Complete Binary Tree:       Perfect Binary Tree:
       (1)                        (1)                         (1)
      /   \                      /   \                       /   \
    (2)   (3)                  (2)   (3)                   (2)   (3)
   /   \                      /   \  /                    /  \   /  \
 (4)   (5)                  (4)  (5)(6)                 (4)  (5)(6) (7)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing `TreeNode` data structure, recursive tree height/depth calculations, and tree property verifiers:

```java
import java.util.*;

public class TreeFundamentalsMaster {

    // Standard Production Binary Tree Node Class
    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
            this.left = null;
            this.right = null;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // 1. Calculate Maximum Height of Tree (Height of Root) O(N) Time, O(H) Space
    public static int maxDepth(TreeNode root) {
        if (root == null) return 0;
        int leftHeight = maxDepth(root.left);
        int rightHeight = maxDepth(root.right);
        return 1 + Math.max(leftHeight, rightHeight);
    }

    // 2. Verify Height-Balanced Tree (LeetCode 110) O(N) Time, O(H) Space
    public static boolean isBalanced(TreeNode root) {
        return checkHeight(root) != -1;
    }

    private static int checkHeight(TreeNode node) {
        if (node == null) return 0;

        int leftH = checkHeight(node.left);
        if (leftH == -1) return -1;

        int rightH = checkHeight(node.right);
        if (rightH == -1) return -1;

        if (Math.abs(leftH - rightH) > 1) return -1; // Unbalanced!

        return 1 + Math.max(leftH, rightH);
    }

    // 3. Count Total Nodes in Complete Binary Tree (LeetCode 222) O((log N)^2) Time
    public static int countNodesCompleteTree(TreeNode root) {
        if (root == null) return 0;

        int leftDepth = getLeftDepth(root);
        int rightDepth = getRightDepth(root);

        // If left depth == right depth, tree is PERFECT!
        if (leftDepth == rightDepth) {
            return (1 << leftDepth) - 1; // 2^H - 1
        }

        return 1 + countNodesCompleteTree(root.left) + countNodesCompleteTree(root.right);
    }

    private static int getLeftDepth(TreeNode node) {
        int depth = 0;
        while (node != null) {
            depth++;
            node = node.left;
        }
        return depth;
    }

    private static int getRightDepth(TreeNode node) {
        int depth = 0;
        while (node != null) {
            depth++;
            node = node.right;
        }
        return depth;
    }
}
```

> **Quick Syntax:**
```java
// Standard Tree Height Line
int height = (root == null) ? 0 : 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
```

---

## 7. Concrete Problem Examples
* **LeetCode 104 - Maximum Depth of Binary Tree**: Tree height calculation.
* **LeetCode 110 - Balanced Binary Tree**: Subtree height balance check.
* **LeetCode 222 - Count Complete Tree Nodes**: $O((\log N)^2)$ binary search count.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing tree depth and balance checks:

```java
public class TreeFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Tree Building & Height Calculation ===");
        // Build Perfect Binary Tree:
        //       1
        //     /   \
        //    2     3
        //   / \   / \
        //  4   5 6   7
        TreeFundamentalsMaster.TreeNode root = new TreeFundamentalsMaster.TreeNode(1);
        root.left = new TreeFundamentalsMaster.TreeNode(2, 
            new TreeFundamentalsMaster.TreeNode(4), new TreeFundamentalsMaster.TreeNode(5));
        root.right = new TreeFundamentalsMaster.TreeNode(3, 
            new TreeFundamentalsMaster.TreeNode(6), new TreeFundamentalsMaster.TreeNode(7));

        int height = TreeFundamentalsMaster.maxDepth(root);
        System.out.println("Tree Max Depth: " + height); // Output: 3
        System.out.println("Is Balanced? " + TreeFundamentalsMaster.isBalanced(root)); // Output: true

        int count = TreeFundamentalsMaster.countNodesCompleteTree(root);
        System.out.println("Total Nodes in Complete Tree: " + count); // Output: 7 (2^3 - 1)
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Max Depth (104)** | **$O(N)$ Linear ⚡** | $O(H)$ Recursion Stack | Bottom-up `1 + max(left, right)` |
| **Is Balanced (110)** | **$O(N)$ Linear ⚡** | $O(H)$ Recursion Stack | Early exit `-1` height check |
| **Complete Node Count (222)**| **$O((\log N)^2)$ ⚡** | $O(\log N)$ Stack Space | Bitwise `(1 << H) - 1` perfect trees |

---

## 10. Edge Cases & Boundary Handling
* **Null Root (`root == null`)**: Depth is `0`, balanced is `true`.
* **Single Node Tree (`root.left == null && root.right == null`)**: Height is `1`, depth is `0`.

---

## 11. Common Mistakes & Anti-Patterns
* **Confusing Depth and Height Definitions**:
  - Depth is measured Top-Down from Root (Root depth = 0). Height is measured Bottom-Up from Leaf (Leaf height = 0).
* **Using $O(N^2)$ Unoptimized Balance Check**:
  - Calling `maxDepth(node.left)` and `maxDepth(node.right)` at every node calculates height redundantly ($O(N^2)$ time).
  - **Pass `-1` up during bottom-up recursion for $O(N)$ linear time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Perfect Binary Tree Mathematical Formulas:
> For a Perfect Binary Tree of height $H$ (where root is level 1):
> 1. Total Nodes $N = 2^H - 1$.
> 2. Total Leaf Nodes $L = 2^{H-1}$.
> 3. Total Internal Nodes $I = 2^{H-1} - 1 = N - L$.
> 4. Height $H = \lfloor \log_2 N \rfloor + 1$.

> **Memory Trick:** **"Perfect Binary Tree of height H has 2^H - 1 total nodes and 2^(H-1) leaf nodes!"**

---

## 13. System & Implementation Comparisons

| Feature | Pointer-Based Node Tree | Array-Backed Complete Tree |
| :--- | :--- | :--- |
| **Child Navigation** | `node.left`, `node.right` | `left = 2*i + 1`, `right = 2*i + 2` |
| **CPU Cache Locality** | Poor (Heap Pointer Chasing) | **Optimal (Contiguous Array) ⚡** |
| **Flexibility** | Any arbitrary tree shape | Best for Complete Trees (Heaps) |

---

## 14. How to Recognize This in Questions
* **"Check if tree is height balanced in O(N) time"** $\rightarrow$ LeetCode 110 (Bottom-up recursion returning `-1` for unbalanced).
* **"Count total nodes in a complete binary tree in sub-linear time"** $\rightarrow$ LeetCode 222 ($O((\log N)^2)$ perfect subtree check).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the relationship between tree height $H$ and node count $N$ in a balanced binary tree?**  
  *A:* In a balanced binary tree, height $H = O(\log_2 N)$. In a skewed binary tree, height $H = O(N)$.
* **Q: Why does `countNodesCompleteTree` run in $O((\log N)^2)$ time?**  
  *A:* At each step, checking left and right depths takes $O(\log N)$ time. At least one of the two subtrees is guaranteed to be a Perfect Binary Tree, whose node count is computed in $O(1)$ time using `(1 << H) - 1`. The algorithm recurses into the non-perfect subtree at most $\log N$ times, yielding $O(\log N \cdot \log N) = \mathbf{O((\log N)^2)\text{ Time}}$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE FUNDAMENTALS & METRICS                           |
+-----------------------------------------------------------------------+
| • Edges Formula: E = N - 1 edges for any valid tree with N nodes      |
| • Depth vs Height: Depth goes Top-Down from Root; Height Bottom-Up    |
| • Perfect Tree Nodes: N = 2^H - 1 (Leaf count L = 2^(H-1))            |
| • Balanced Check: |leftH - rightH| <= 1 for EVERY node                |
| • Bottom-Up Balance Trick: Return -1 immediately on unbalanced subtree|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can state the 12 tree terms and metrics.
- [ ] I can write Maximum Depth of Binary Tree (LeetCode 104) recursively.
- [ ] I can write Balanced Binary Tree (LeetCode 110) in $O(N)$ time.
- [ ] I can write Count Complete Tree Nodes (LeetCode 222) in $O((\log N)^2)$ time.
- [ ] I can explain the 5 binary tree classifications.
