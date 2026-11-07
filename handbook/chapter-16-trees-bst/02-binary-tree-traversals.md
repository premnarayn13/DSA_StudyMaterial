# 02. Binary Tree Traversals, Iterative DFS Stacks & Morris $O(1)$ Space Threading

## 1. Introduction
**Depth-First Search (DFS) Tree Traversals** visit every node in a Binary Tree systematically. The three classical DFS traversals—**Pre-Order (`Root -> Left -> Right`)**, **In-Order (`Left -> Root -> Right`)**, and **Post-Order (`Left -> Right -> Root`)**—form the backbone of tree manipulation, tree cloning, expression tree parsing, and Binary Search Tree (BST) sorted sequence extraction. While recursive traversals consume $O(H)$ stack space, **Morris Traversal** uses temporary threaded pointers to achieve **$O(N)$ Linear Time and $O(1)$ Constant Auxiliary Space**.

> **Important:** Key operational properties of DFS traversals:
> * **In-Order Traversal of a BST**: ALWAYS produces elements in **Strictly Sorted Ascending Order**!
> * **Pre-Order Traversal**: Excellent for tree cloning, serialization, and prefix expression evaluation.
> * **Post-Order Traversal**: Essential for bottom-up operations (deleting a tree, computing subtree sizes/heights, and postfix expression evaluation).

```
DFS Traversal Order Spectrum:
+-----------------------------------------------------------------------------------+
| Pre-Order  : [ ROOT ] -> [ Left Subtree ] -> [ Right Subtree ]                     |
| In-Order   : [ Left Subtree ] -> [ ROOT ] -> [ Right Subtree ] (BST Sorted Order!) ⚡|
| Post-Order : [ Left Subtree ] -> [ Right Subtree ] -> [ ROOT ]                     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Iterative DFS Mechanics

### 2.1 Iterative Pre-Order Traversal (Explicit Stack)
1. Initialize `Deque<TreeNode> stack = new ArrayDeque<>()`.
2. Push `root` onto stack.
3. While `!stack.isEmpty()`:
   - Pop `curr = stack.pop()`. Visit `curr.val`.
   - **Push Right Child FIRST** (`if (curr.right != null) stack.push(curr.right)`).
   - **Push Left Child SECOND** (`if (curr.left != null) stack.push(curr.left)`).
   - (Pushing right before left ensures the left child is popped and processed FIRST!).

```
Why Right Child is Pushed First in Iterative Pre-Order:
Stack is Last-In, First-Out (LIFO)!
By pushing curr.right BEFORE curr.left, curr.left sits at the top of the stack and is popped NEXT! ⚡
```

### 2.2 Iterative In-Order Traversal (Explicit Stack)
1. Initialize `Deque<TreeNode> stack = new ArrayDeque<>()`.
2. `curr = root`.
3. While `curr != null` OR `!stack.isEmpty()`:
   - Push all left nodes to stack: `while (curr != null) { stack.push(curr); curr = curr.left; }`
   - Pop `curr = stack.pop()`. Visit `curr.val`.
   - Move to right child: `curr = curr.right`.

> **Memory Trick:** **"Pre-Order Stack: Push Right child FIRST, Left child SECOND! In-Order Stack: Push all Left nodes down to null!"**

---

## 3. Characteristics & Morris $O(1)$ Space Threaded Traversal

### 3.1 Morris In-Order Traversal ($O(1)$ Auxiliary Space)
Standard DFS uses $O(H)$ recursion stack space. **Morris Traversal** modifies the tree temporarily by creating **Threaded Pointers** from a node's predecessor back to the node:

#### Morris In-Order Algorithm ($O(N)$ Time, $O(1)$ Space):
1. `curr = root`.
2. While `curr != null`:
   - If `curr.left == null`:
     - Visit `curr.val`.
     - Move to `curr = curr.right`.
   - Else (`curr.left != null`):
     - Find **In-Order Predecessor** `pred` (Rightmost node in `curr.left` subtree).
     - If `pred.right == null` (Thread does not exist):
       - Create thread: `pred.right = curr`!
       - Move to `curr = curr.left`.
     - Else (`pred.right == curr` - Thread already exists!):
       - Remove thread: `pred.right = null`!
       - Visit `curr.val`.
       - Move to `curr = curr.right`.

```
Morris Threading Topology:
Left Subtree Rightmost Node (Predecessor) ---> Temporary Thread Pointer ---> Current Node
Allows stepping back up the tree WITHOUT consuming recursion stack space! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Morris In-Order Traversal on Tree: `(1) <- [2] -> (3)`:

```
Init: curr = 2

Step 1: curr = 2. curr.left (1) != null.
  - Find predecessor of 2 in left subtree -> pred = 1.
  - pred.right is null -> Create thread: 1.right = 2.
  - Move curr = 1.

Step 2: curr = 1. curr.left is null.
  - Visit 1!
  - Move curr = curr.right -> Follows thread 1.right to 2!

Step 3: curr = 2. curr.left (1) != null.
  - Find predecessor -> pred = 1.
  - pred.right == 2 (Thread exists!).
  - Remove thread: 1.right = null.
  - Visit 2!
  - Move curr = curr.right -> 3.

Step 4: curr = 3. curr.left is null.
  - Visit 3!
  - Move curr = 3.right (null) -> Loop terminates!

Output = [1, 2, 3] in Sorted Order! Space Complexity = O(1) Strict Constant! ✅
```

---

## 5. Visual Diagram
Morris Threading Temporary Pointer Topography:

```
Before Threading:                     Temporary Thread Created:
        (2)                                   (2) <------+
       /   \                                 /   \       |
     (1)   (3)                             (1)   (3)     | (1.right = 2)
                                             +-----------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Recursive DFS, Iterative Stack DFS (Pre/In/Post Order), and Morris In-Order Traversal:

```java
import java.util.*;

public class BinaryTreeTraversalsMaster {

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

    // 1. Iterative Pre-Order Traversal (LeetCode 144) O(N) Time, O(H) Space
    public static List<Integer> preorderTraversalIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            TreeNode curr = stack.pop();
            result.add(curr.val);

            // Push right child FIRST so left is popped NEXT!
            if (curr.right != null) stack.push(curr.right);
            if (curr.left != null) stack.push(curr.left);
        }

        return result;
    }

    // 2. Iterative In-Order Traversal (LeetCode 94) O(N) Time, O(H) Space
    public static List<Integer> inorderTraversalIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;

        while (curr != null || !stack.isEmpty()) {
            // Push all left sub-nodes down to null
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            result.add(curr.val);
            curr = curr.right;
        }

        return result;
    }

    // 3. Iterative Post-Order Traversal (LeetCode 145) O(N) Time, O(H) Space
    public static List<Integer> postorderTraversalIterative(TreeNode root) {
        LinkedList<Integer> result = new LinkedList<>(); // Prepend to head
        if (root == null) return result;

        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);

        while (!stack.isEmpty()) {
            TreeNode curr = stack.pop();
            result.addFirst(curr.val); // Prepend value (Root -> Right -> Left reversed!)

            if (curr.left != null) stack.push(curr.left);
            if (curr.right != null) stack.push(curr.right);
        }

        return result;
    }

    // 4. Morris In-Order Traversal O(N) Time, O(1) AUXILIARY SPACE ⚡
    public static List<Integer> morrisInorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        TreeNode curr = root;

        while (curr != null) {
            if (curr.left == null) {
                result.add(curr.val);
                curr = curr.right; // Move to right or follow thread
            } else {
                // Find in-order predecessor (rightmost node in left subtree)
                TreeNode pred = curr.left;
                while (pred.right != null && pred.right != curr) {
                    pred = pred.right;
                }

                if (pred.right == null) {
                    // Create thread pointer back to curr
                    pred.right = curr;
                    curr = curr.left;
                } else {
                    // Thread already exists! Remove thread and visit curr
                    pred.right = null;
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
// Morris In-Order Thread Logic Line
TreeNode pred = curr.left;
while (pred.right != null && pred.right != curr) pred = pred.right;
```

---

## 7. Concrete Problem Examples
* **LeetCode 94 - Binary Tree Inorder Traversal**: BST sorted sequence extraction.
* **LeetCode 144 - Binary Tree Preorder Traversal**: Tree serialization & cloning.
* **LeetCode 145 - Binary Tree Postorder Traversal**: Subtree deletion & calculation.
* **LeetCode 114 - Flatten Binary Tree to Linked List**: In-place Morris-style pre-order flattening.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Iterative In-Order, Post-Order, and Morris Traversal:

```java
public class BinaryTreeTraversalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Tree Traversal Testing ===");
        // Build Tree:
        //       1
        //     /   \
        //    2     3
        //   / \
        //  4   5
        BinaryTreeTraversalsMaster.TreeNode root = new BinaryTreeTraversalsMaster.TreeNode(1);
        root.left = new BinaryTreeTraversalsMaster.TreeNode(2, 
            new BinaryTreeTraversalsMaster.TreeNode(4), new BinaryTreeTraversalsMaster.TreeNode(5));
        root.right = new BinaryTreeTraversalsMaster.TreeNode(3);

        System.out.println("Iterative Pre-Order:  " + BinaryTreeTraversalsMaster.preorderTraversalIterative(root));
        // Output: [1, 2, 4, 5, 3]

        System.out.println("Iterative In-Order:   " + BinaryTreeTraversalsMaster.inorderTraversalIterative(root));
        // Output: [4, 2, 5, 1, 3]

        System.out.println("Iterative Post-Order: " + BinaryTreeTraversalsMaster.postorderTraversalIterative(root));
        // Output: [4, 5, 2, 3, 1]

        System.out.println("Morris In-Order O(1): " + BinaryTreeTraversalsMaster.morrisInorderTraversal(root));
        // Output: [4, 2, 5, 1, 3] ✅
    }
}
```

---

## 9. Complexity Analysis

| Traversal Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Recursive DFS** | **$O(N)$ Linear ⚡** | $O(H)$ Recursion Stack | Uses implicit call stack |
| **Iterative DFS Stack** | **$O(N)$ Linear ⚡** | $O(H)$ Explicit Stack | Uses `ArrayDeque` stack |
| **Morris Traversal** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict Constant ⚡**| Uses temporary threaded pointers |

---

## 10. Edge Cases & Boundary Handling
* **Skewed Binary Tree ($H = N$)**: Standard recursive DFS uses $O(N)$ call stack space; Morris Traversal still uses $O(1)$ constant space.
* **Modifying Tree Structure During Morris Traversal**: Tree modifications MUST be cleaned up before returning (`pred.right = null`), ensuring the input tree structure remains unmodified upon completion.

---

## 11. Common Mistakes & Anti-Patterns
* **Pushing Left Child First in Iterative Pre-Order**:
  - Pushing `left` before `right` causes the `right` child to pop first, turning Pre-Order into `Root -> Right -> Left`.
  - **Push `right` child FIRST so `left` child is popped and processed NEXT**.
* **Forgetting to Clean Up Thread Pointers in Morris Traversal**:
  - Leaving temporary `pred.right = curr` threads corrupts the original binary tree structure.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why In-Order Traversal of a BST is Crucial:
> Performing an In-Order traversal (`Left -> Root -> Right`) on a Binary Search Tree (BST) ALWAYS visits keys in **Strictly Ascending Sorted Order**!
> This property is used to validate BSTs (LeetCode 98), find the K-th smallest element in a BST (LeetCode 230), and convert BSTs to sorted doubly linked lists!

> **Memory Trick:** **"BST In-Order Traversal ALWAYS yields elements in strictly sorted ascending order!"**

---

## 13. System & Implementation Comparisons

| Feature | Iterative Explicit Stack DFS | Morris Threaded Traversal |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Memory** | $O(H)$ Stack Space | **$O(1)$ Strict In-Place ⚡** |
| **Tree Modification**| Zero Modification | Temporary Threading (Cleaned Up) |

---

## 14. How to Recognize This in Questions
* **"Traverse a binary tree in O(1) extra space"** $\rightarrow$ Morris Traversal.
* **"Extract sorted sequence from a Binary Search Tree"** $\rightarrow$ In-Order Traversal.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Morris Traversal achieve $O(N)$ time complexity despite searching for predecessors?**  
  *A:* Finding the predecessor traverses edges in the left subtree. Across the entire traversal, each edge in the tree is traversed at most 3 times (once to create the thread, once to traverse the thread, once to remove the thread) $\implies 3N = \mathbf{O(N)\text{ Linear Time}}$.
* **Q: How does the 1-stack trick work for Iterative Post-Order Traversal?**  
  *A:* By running a modified Pre-Order traversal (`Root -> Right -> Left`) and prepending values to a `LinkedList` using `addFirst()`, the output sequence is reversed into Post-Order (`Left -> Right -> Root`)!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY TREE DFS TRAVERSALS                            |
+-----------------------------------------------------------------------+
| • Pre-Order: Root -> Left -> Right (Push Right FIRST to stack!)       |
| • In-Order: Left -> Root -> Right (BST In-Order = Sorted Ascending!)  |
| • Post-Order: Left -> Right -> Root (Bottom-up subtree calculations)  |
| • Morris Traversal: Uses pred.right = curr threads for O(1) space     |
| • Post-Order Trick: Root->Right->Left prepended to LinkedList head    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Iterative Pre-Order, In-Order, and Post-Order using Stack.
- [ ] I can write Morris In-Order Traversal in $O(1)$ constant space.
- [ ] I know why BST In-Order traversal yields sorted order.
- [ ] I know why right child must be pushed first in iterative pre-order.
- [ ] I can explain why Morris Traversal runs in $O(N)$ total time.
