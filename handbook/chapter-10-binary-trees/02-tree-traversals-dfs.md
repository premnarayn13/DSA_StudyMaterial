# 02. Depth-First Search (DFS) Traversals: Pre-Order, In-Order & Post-Order

## 1. Introduction
**Depth-First Search (DFS)** tree traversals form the backbone of binary tree algorithmic problem-solving in technical coding interviews. DFS explores a binary tree by traversing as deep as possible along each branch before backtracking. The three fundamental DFS traversal orders—**Pre-Order (Root $\to$ Left $\to$ Right)**, **In-Order (Left $\to$ Root $\to$ Right)**, and **Post-Order (Left $\to$ Right $\to$ Root)**—govern how subproblems are decomposed, evaluated, and synthesized across tree algorithms.

> **Important:** In-Order Traversal of a Binary Search Tree (BST) visits nodes in **strictly non-decreasing sorted order**! Post-Order Traversal evaluates subtrees bottom-up, making it the required traversal for tree deletion, height computation, and sub-tree aggregation problems.

```
DFS Traversal Priority Order:
+-----------------------------------------------------------------------------------+
| Pre-Order  : ROOT -> Left Subtree -> Right Subtree  (Top-Down Processing)        |
| In-Order   : Left Subtree -> ROOT -> Right Subtree  (Sorted BST Order ⚡)        |
| Post-Order  : Left Subtree -> Right Subtree -> ROOT  (Bottom-Up Processing ⚡)    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Execution Mechanics

### 2.1 The Three Classical DFS Orders
Let `N` be the current node, `L` be the left subtree, and `R` be the right subtree:

1. **Pre-Order Traversal (N-L-R)**:
   - Visit current node `N`.
   - Traverse left subtree `L`.
   - Traverse right subtree `R`.
   - *Use Case*: Tree serialization, deep copying, root-to-leaf path problems.
2. **In-Order Traversal (L-N-R)**:
   - Traverse left subtree `L`.
   - Visit current node `N`.
   - Traverse right subtree `R`.
   - *Use Case*: BST validation, finding $K$-th smallest in BST, sorted output generation.
3. **Post-Order Traversal (L-R-N)**:
   - Traverse left subtree `L`.
   - Traverse right subtree `R`.
   - Visit current node `N`.
   - *Use Case*: Bottom-up tree height computation, tree deletion, expression evaluation trees.

### 2.2 Iterative DFS Architecture (Stack-Based)
While recursive implementations rely on the JVM Call Stack (consuming $O(H)$ implicit memory), iterative implementations explicitly use an explicit `ArrayDeque<TreeNode>` stack:
* **Iterative Pre-Order**: Push Root $\to$ Pop Node $\to$ Push Right Child $\to$ Push Left Child (pushing Right first ensures Left is popped and processed first!).
* **Iterative In-Order**: Push all Left nodes to stack until `null` $\to$ Pop & Visit $\to$ Move to Right child.
* **Iterative Post-Order**: Two-stack method OR Single-stack with `lastVisited` tracking node.

> **Memory Trick:** **"Pre-Order = Top-Down (N-L-R)! In-Order = Sorted BST (L-N-R)! Post-Order = Bottom-Up Subtrees (L-R-N)!"**

---

## 3. Characteristics & Morris Traversal ($O(1)$ Space)

### 3.1 Morris In-Order Traversal Architecture ($O(N)$ Time, $O(1)$ Space)
Standard recursive and iterative traversals require $O(H)$ stack space. **Morris Traversal** achieves **$O(1)$ auxiliary constant space** by utilizing temporary **Threaded Binary Tree Pointers**!

#### Morris In-Order Algorithm Rules:
1. Initialize `curr = root`.
2. While `curr != null`:
   - If `curr.left == null`:
     - Process/Visit `curr.val`.
     - Move to `curr = curr.right`.
   - Else (`curr.left != null`):
     - Find the **In-Order Predecessor** of `curr` (the right-most node in `curr`'s left subtree): `pred = curr.left; while (pred.right != null && pred.right != curr) pred = pred.right;`
     - If `pred.right == null`:
       - Create temporary thread pointer: `pred.right = curr`.
       - Move `curr = curr.left`.
     - Else (`pred.right == curr`):
       - Remove temporary thread pointer: `pred.right = null`.
       - Process/Visit `curr.val`.
       - Move `curr = curr.right`.

```
Morris Traversal Threaded Pointer Concept:
Before:       (2)                      After Threading:        (2) <------+
             /   \                                            /   \       |
           (1)   (3)                                        (1)   (3)     |
                                                               \          |
                                                     pred.right = curr ---+
```

---

## 4. Internal Working Mechanics
Tracing Pre-Order, In-Order, and Post-Order on Binary Tree `[1, 2, 3, 4, 5]`:

```
          ( 1 )
         /     \
       ( 2 )   ( 3 )
      /     \
    ( 4 )   ( 5 )

1. Pre-Order (N-L-R)  : [ 1, 2, 4, 5, 3 ]
   - Visit 1 -> Visit 2 -> Visit 4 -> Visit 5 -> Visit 3.

2. In-Order (L-N-R)   : [ 4, 2, 5, 1, 3 ]
   - Visit 4 -> Visit 2 -> Visit 5 -> Visit 1 -> Visit 3.

3. Post-Order (L-R-N) : [ 4, 5, 2, 3, 1 ]
   - Visit 4 -> Visit 5 -> Visit 2 -> Visit 3 -> Visit 1.
```

---

## 5. Visual Diagram
DFS Traversal State Flow & Call Stack State Tracing:

```
               [ 1 ]
             /       \
         [ 2 ]       [ 3 ]
        /     \
     [ 4 ]   [ 5 ]

Pre-Order (N-L-R) Sequence : 1  ---> 2 ---> 4 ---> 5 ---> 3
In-Order (L-N-R) Sequence  : 4  ---> 2 ---> 5 ---> 1 ---> 3
Post-Order (L-R-N) Sequence : 4  ---> 5 ---> 2 ---> 3 ---> 1
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Recursive DFS, Iterative DFS (using Stack), and Morris Traversal ($O(1)$ Space):

```java
import java.util.*;

public class TreeTraversalsDFSMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // ==========================================
    // 1. RECURSIVE DFS TRAVERSALS O(N) Time, O(H) Space
    // ==========================================

    public static List<Integer> preorderRecursive(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }

    private static void preorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        result.add(node.val);              // N
        preorderHelper(node.left, result);  // L
        preorderHelper(node.right, result); // R
    }

    public static List<Integer> inorderRecursive(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }

    private static void inorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        inorderHelper(node.left, result);  // L
        result.add(node.val);              // N
        inorderHelper(node.right, result); // R
    }

    public static List<Integer> postorderRecursive(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }

    private static void postorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return;
        postorderHelper(node.left, result);  // L
        postorderHelper(node.right, result); // R
        result.add(node.val);               // N
    }

    // ==========================================
    // 2. ITERATIVE DFS TRAVERSALS (STACK-BASED) O(N) Time, O(H) Space
    // ==========================================

    // Iterative Pre-Order (LeetCode 144)
    public static List<Integer> preorderIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            TreeNode curr = stack.pop();
            result.add(curr.val);

            // Push RIGHT child first so LEFT child is popped and processed first!
            if (curr.right != null) stack.push(curr.right);
            if (curr.left != null)  stack.push(curr.left);
        }

        return result;
    }

    // Iterative In-Order (LeetCode 94)
    public static List<Integer> inorderIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;

        while (curr != null || !stack.isEmpty()) {
            // Push all left nodes
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            result.add(curr.val); // Process node
            curr = curr.right;    // Move to right subtree
        }

        return result;
    }

    // Iterative Post-Order Single Stack (LeetCode 145)
    public static List<Integer> postorderIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;
        TreeNode lastVisited = null;

        while (curr != null || !stack.isEmpty()) {
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            TreeNode peekNode = stack.peek();
            // If right child exists and traversing from left child, move to right child
            if (peekNode.right != null && lastVisited != peekNode.right) {
                curr = peekNode.right;
            } else {
                result.add(peekNode.val);
                lastVisited = stack.pop();
            }
        }

        return result;
    }

    // ==========================================
    // 3. MORRIS IN-ORDER TRAVERSAL O(N) Time, O(1) Auxiliary Space
    // ==========================================

    public static List<Integer> morrisInorder(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        TreeNode curr = root;

        while (curr != null) {
            if (curr.left == null) {
                result.add(curr.val);
                curr = curr.right;
            } else {
                // Find in-order predecessor
                TreeNode pred = curr.left;
                while (pred.right != null && pred.right != curr) {
                    pred = pred.right;
                }

                if (pred.right == null) {
                    pred.right = curr; // Create temporary thread
                    curr = curr.left;
                } else {
                    pred.right = null; // Revert temporary thread
                    result.add(curr.val);
                    curr = curr.right;
                }
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Iterative Pre-Order Push Sequence
if (curr.right != null) stack.push(curr.right); // Push Right FIRST!
if (curr.left != null)  stack.push(curr.left);  // Left popped FIRST!
```

---

## 7. Concrete Problem Examples
* **LeetCode 144 - Binary Tree Preorder Traversal**: Iterative and recursive pre-order.
* **LeetCode 94 - Binary Tree Inorder Traversal**: In-order traversal & Morris traversal.
* **LeetCode 145 - Binary Tree Postorder Traversal**: Single-stack and two-stack post-order.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Recursive DFS, Iterative DFS, and Morris Traversal on identical tree:

```java
public class TreeTraversalsDFSDemo {

    public static void main(String[] args) {
        // Build Tree: [1, 2, 3, 4, 5]
        TreeTraversalsDFSMaster.TreeNode root = new TreeTraversalsDFSMaster.TreeNode(1);
        root.left = new TreeTraversalsDFSMaster.TreeNode(2);
        root.right = new TreeTraversalsDFSMaster.TreeNode(3);
        root.left.left = new TreeTraversalsDFSMaster.TreeNode(4);
        root.left.right = new TreeTraversalsDFSMaster.TreeNode(5);

        System.out.println("=== 1. Pre-Order Traversal (N-L-R) ===");
        System.out.println("Recursive: " + TreeTraversalsDFSMaster.preorderRecursive(root));
        System.out.println("Iterative: " + TreeTraversalsDFSMaster.preorderIterative(root));

        System.out.println("\n=== 2. In-Order Traversal (L-N-R) ===");
        System.out.println("Recursive: " + TreeTraversalsDFSMaster.inorderRecursive(root));
        System.out.println("Iterative: " + TreeTraversalsDFSMaster.inorderIterative(root));
        System.out.println("Morris O(1):" + TreeTraversalsDFSMaster.morrisInorder(root));

        System.out.println("\n=== 3. Post-Order Traversal (L-R-N) ===");
        System.out.println("Recursive: " + TreeTraversalsDFSMaster.postorderRecursive(root));
        System.out.println("Iterative: " + TreeTraversalsDFSMaster.postorderIterative(root));
    }
}
```

---

## 9. Complexity Analysis

| Traversal Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Recursive DFS (All)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Implicit JVM call stack memory |
| **Iterative DFS (Stack)** | **$O(N)$ Linear ⚡** | $O(H)$ Explicit Stack | Explicit `ArrayDeque` stack memory |
| **Morris Traversal** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Temporary predecessor thread pointers |

---

## 10. Edge Cases & Boundary Handling
* **Empty Tree (`root == null`)**: Return empty `ArrayList` immediately.
* **Single Node Tree**: Return single-element list `[val]`.
* **Skewed Tree (Height $H = N$)**: Recursive DFS consumes $O(N)$ stack memory, taking maximum call stack space.

---

## 11. Common Mistakes & Anti-Patterns
* **In Iterative Pre-Order, Pushing Left Child Before Right Child**:
  - `stack.push(curr.left); stack.push(curr.right);` $\implies$ Right child is popped FIRST! Produces incorrect N-R-L order instead of N-L-R. **Always push Right child FIRST**!
* **Modifying Tree Structure in Morris Traversal without Restoring Threads**: Forgetting to set `pred.right = null` corrupts the original binary tree structure permanently!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Which Traversal Order to Choose?
> 1. **Top-Down Node Processing / Path Copying** $\implies$ **Pre-Order Traversal**.
> 2. **BST Validation / Non-Decreasing Sorted Processing** $\implies$ **In-Order Traversal**.
> 3. **Bottom-Up Subtree Calculation / Deletion / Height Calculation** $\implies$ **Post-Order Traversal**.

> **Memory Trick:** **"Top-Down = Pre-Order! Sorted BST = In-Order! Bottom-Up Subtrees = Post-Order!"**

---

## 13. System & Implementation Comparisons

| Feature | Recursive DFS | Iterative DFS | Morris Traversal |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ | **$O(N)$ Linear ⚡** |
| **Auxiliary Space** | $O(H)$ Call Stack | $O(H)$ Explicit Stack | **$O(1)$ Constant ⚡** |
| **Code Length** | ~5 lines | ~15 lines | ~25 lines |
| **Modifies Tree** | NO | NO | **Temporarily during traversal** |

---

## 14. How to Recognize This in Questions
* **"Traverse a BST in sorted non-decreasing order"** $\rightarrow$ In-Order Traversal (`inorder(left) -> process(node) -> inorder(right)`).
* **"Evaluate subtrees bottom-up before processing parent"** $\rightarrow$ Post-Order Traversal (`postorder(left) -> postorder(right) -> process(node)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Morris Traversal achieve $O(1)$ auxiliary space?**  
  *A:* By temporarily linking the right pointer of each node's in-order predecessor (`pred.right`) back to the node itself (`curr`), creating a thread pointer that allows backtracking to parent nodes without maintaining an explicit or implicit stack.
* **Q: Why is Post-Order Traversal required for Binary Tree Height / Subtree Deletion?**  
  *A:* Height calculation requires knowing the height of both left and right subtrees BEFORE calculating parent height (`1 + max(leftH, rightH)`). Post-Order guarantees subtrees are completely evaluated before processing the parent node.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DFS TRAVERSALS (PRE, IN, POST & MORRIS)               |
+-----------------------------------------------------------------------+
| • Pre-Order (N-L-R) : Process Root FIRST, then Left, then Right       |
| • In-Order (L-N-R)  : Process Left, then Root, then Right (Sorted BST!)|
| • Post-Order (L-R-N): Process Left, then Right, then Root (Bottom-Up!)|
| • Iterative Pre-Order: Push RIGHT child first so LEFT pops first!     |
| • Morris Traversal: Uses pred.right = curr thread pointers for O(1) space|
| • BST Rule: In-Order traversal of a BST yields non-decreasing order  |
| • Subtree Rule: Post-Order processes subtrees before parent           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write recursive Pre-Order, In-Order, and Post-Order in under 2 minutes.
- [ ] I can write iterative Pre-Order and know why Right child is pushed first.
- [ ] I can write iterative In-Order using a stack.
- [ ] I can write Morris In-Order Traversal in $O(1)$ constant space.
- [ ] I know why In-Order traversal of a BST yields sorted elements.
- [ ] I know why Post-Order is used for bottom-up subtree calculations.
