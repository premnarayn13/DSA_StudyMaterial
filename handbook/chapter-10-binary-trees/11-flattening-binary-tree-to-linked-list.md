# 11. Flattening Binary Trees & BST Conversion to Doubly Linked Lists

## 1. Introduction
Flattening a Binary Tree into a Singly Linked List in pre-order traversal sequence (LeetCode 114) and converting a Binary Search Tree (BST) into a Sorted Circular Doubly Linked List (LeetCode 426) are premier tree-pointer manipulation problems in technical coding interviews. These problems evaluate modifying binary tree child pointers (`left` and `right`) **in-place** without allocating new tree nodes, maintaining structural invariants in **$O(N)$ linear time**.

> **Important:** In Flatten Binary Tree to Linked List (LeetCode 114), the flattened list must follow **Pre-Order Traversal (Root $\to$ Left $\to$ Right)** where every node's `left` pointer is set to `null` and `right` pointer points to the next node. Using **Reversed Post-Order DFS (Right $\to$ Left $\to$ Root)** with a `prev` reference achieves in-place flattening in $O(N)$ time and $O(H)$ space!

```
Tree Flattening & List Conversion Spectrum:
+-----------------------------------------------------------------------------------+
| Flatten Tree (114) : Pre-Order Sequence (Right-only list)    -> O(N) In-Place ⚡   |
| BST to Sorted DLL (426) : In-Order Sequence (Doubly Linked)   -> O(N) In-Place ⚡   |
| Morris In-Place Flatten: Zero Stack Memory                   -> O(N) Time, O(1) Space|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Techniques

### 2.1 Technique 1: Reversed Post-Order DFS (Right $\to$ Left $\to$ Root)
Standard Pre-Order Traversal processes Root $\to$ Left $\to$ Right. However, modifying `curr.right` during standard pre-order traversal overwrites the original right subtree pointer before it is explored!
* **Reversed Post-Order Sequence**: Explore **Right Subtree $\to$ Left Subtree $\to$ Root**.
* Maintain a pointer `prev` (initially `null`).
* At node `curr`:
  - Recurse right: `flatten(curr.right)`.
  - Recurse left: `flatten(curr.left)`.
  - Wire node pointers: `curr.right = prev; curr.left = null;`.
  - Update `prev = curr`.

### 2.2 Technique 2: Morris In-Place Pointer Manipulation ($O(1)$ Space)
To achieve true **$O(1)$ auxiliary space**:
* At node `curr`:
  - If `curr.left != null`:
    - Find the **right-most node** in `curr`'s left subtree: `pred = curr.left; while (pred.right != null) pred = pred.right;`.
    - Connect `pred.right` to `curr.right`: `pred.right = curr.right`.
    - Move left subtree to right: `curr.right = curr.left; curr.left = null;`.
  - Move `curr = curr.right`.

### 2.3 Technique 3: BST to Sorted Circular Doubly Linked List (LeetCode 426)
* Perform an **In-Order Traversal (Left $\to$ Root $\to$ Right)**.
* Maintain `first` (head of list) and `last` (tail of list) pointers.
* At node `curr`:
  - If `last == null`: Set `first = curr` (first visited node is head).
  - Else: Link `last.right = curr` and `curr.left = last`.
  - Update `last = curr`.
* After full traversal, make list **circular**: `first.left = last; last.right = first;`.

```
BST to Circular Doubly Linked List Mapping:
BST In-Order: [1, 2, 3, 4, 5]
Doubly List : (head: 1) <===> (2) <===> (3) <===> (4) <===> (5: tail)
Circular    : head.left = tail, tail.right = head!
```

> **Memory Trick:** **"Flatten Tree = Reversed Post-Order (Right -> Left -> Root) with prev pointer! BST to DLL = In-Order traversal wiring last.right = curr and curr.left = last!"**

---

## 3. Characteristics & Transformation Rules

```
Tree Flattening & Conversion Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Traversal Order   | Pointer Mapping   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| Flatten Tree (114)    | Reversed Post-Order| `left=null, right=prev` | O(H) Call Stack   |
| Morris Flatten (114)  | Morris Iterative  | `pred.right=curr.right` | O(1) Auxiliary ⚡ |
| BST to Sorted DLL(426)| In-Order Traversal| `last.right=curr, curr.left=last` | O(H) Call Stack|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Morris In-Place Flattening (LeetCode 114) on `[1, 2, 5, 3, 4, null, 6]`:

```
          ( 1 )
         /     \
       ( 2 )   ( 5 )
      /     \       \
    ( 3 )   ( 4 )   ( 6 )

Step 1: curr = 1. curr.left != null (2).
        Find pred = right-most of left subtree (Node 4).
        Set pred.right = curr.right -> 4.right = 5.
        Move left to right: 1.right = 2, 1.left = null.

Intermediate Tree State:
          ( 1 )
             \
             ( 2 )
            /     \
          ( 3 )   ( 4 )
                     \
                     ( 5 )
                        \
                        ( 6 )

Step 2: Advance curr = 1.right (2). curr.left != null (3).
        Find pred = Node 3.
        Set 3.right = 4.
        Move left to right: 2.right = 3, 2.left = null.

Step 3: Continue down right pointers until curr == null.

Flattened Right-Only List: 1 -> 2 -> 3 -> 4 -> 5 -> 6 ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
BST to Sorted Circular Doubly Linked List Topology:

```
                  ( 4 )
                 /     \
               ( 2 )   ( 5 )
              /     \
            ( 1 )   ( 3 )

In-Order Traversal Steps:
Visit 1: first = 1, last = 1
Visit 2: last(1).right = 2, 2.left = 1, last = 2
Visit 3: last(2).right = 3, 3.left = 2, last = 3
Visit 4: last(3).right = 4, 4.left = 3, last = 4
Visit 5: last(4).right = 5, 5.left = 4, last = 5

Circular Boundary Wiring:
first(1).left = last(5)
last(5).right = first(1)

Circular Doubly Linked List: [ 1 <===> 2 <===> 3 <===> 4 <===> 5 ] ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Flatten Binary Tree to Linked List (LeetCode 114 - Reversed DFS and Morris $O(1)$) and Convert BST to Sorted Doubly Linked List (LeetCode 426):

```java
import java.util.*;

public class TreeFlatteningMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // Node for Doubly Linked List Conversion (LeetCode 426)
    public static class Node {
        public int val;
        public Node left;
        public Node right;

        public Node(int val) {
            this.val = val;
        }

        public Node(int val, Node left, Node right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // 1. Flatten Binary Tree to Linked List (LeetCode 114) O(N) Time, O(H) Space (Reversed DFS)
    private static TreeNode flattenPrev = null;

    public static void flatten(TreeNode root) {
        flattenPrev = null;
        flattenHelper(root);
    }

    private static void flattenHelper(TreeNode node) {
        if (node == null) return;

        // Reversed Post-Order DFS: Right -> Left -> Root
        flattenHelper(node.right);
        flattenHelper(node.left);

        // Pointer Wiring
        node.right = flattenPrev;
        node.left = null;
        flattenPrev = node;
    }

    // 2. Flatten Binary Tree to Linked List (LeetCode 114) O(N) Time, O(1) Auxiliary Space (Morris)
    public static void flattenMorris(TreeNode root) {
        TreeNode curr = root;

        while (curr != null) {
            if (curr.left != null) {
                // Find right-most node in left subtree
                TreeNode pred = curr.left;
                while (pred.right != null) {
                    pred = pred.right;
                }

                // Connect predecessor's right to current node's right
                pred.right = curr.right;

                // Move left subtree to right and nullify left
                curr.right = curr.left;
                curr.left = null;
            }

            // Move to next right node
            curr = curr.right;
        }
    }

    // 3. Convert BST to Sorted Doubly Linked List (LeetCode 426) O(N) Time, O(H) Space
    private static Node dllFirst = null;
    private static Node dllLast = null;

    public static Node treeToDoublyList(Node root) {
        if (root == null) return null;

        dllFirst = null;
        dllLast = null;

        inorderDLLDFS(root);

        // Make list circular
        dllFirst.left = dllLast;
        dllLast.right = dllFirst;

        return dllFirst;
    }

    private static void inorderDLLDFS(Node node) {
        if (node == null) return;

        inorderDLLDFS(node.left);

        // Wiring node into doubly linked list
        if (dllLast == null) {
            dllFirst = node; // First node visited in-order is head!
        } else {
            dllLast.right = node;
            node.left = dllLast;
        }
        dllLast = node;

        inorderDLLDFS(node.right);
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 426 Circular Doubly List Wiring Helper
if (last == null) first = node;
else { last.right = node; node.left = last; }
last = node;
```

---

## 7. Concrete Problem Examples
* **LeetCode 114 - Flatten Binary Tree to Linked List**: In-place pre-order right-only list creation.
* **LeetCode 426 - Convert Binary Search Tree to Sorted Doubly Linked List**: In-order circular DLL.
* **LeetCode 897 - Increasing Order Search Tree**: Creating right-leaning BST list.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Flattening algorithms (DFS and Morris) and BST to Circular DLL conversion:

```java
public class TreeFlatteningDemo {

    public static void main(String[] args) {
        // Build Tree: [1, 2, 5, 3, 4, null, 6]
        TreeFlatteningMaster.TreeNode root = new TreeFlatteningMaster.TreeNode(1);
        root.left = new TreeFlatteningMaster.TreeNode(2);
        root.right = new TreeFlatteningMaster.TreeNode(5);
        root.left.left = new TreeFlatteningMaster.TreeNode(3);
        root.left.right = new TreeFlatteningMaster.TreeNode(4);
        root.right.right = new TreeFlatteningMaster.TreeNode(6);

        System.out.println("=== 1. Flattening Tree In-Place (Morris O(1) Space) ===");
        TreeFlatteningMaster.flattenMorris(root);

        System.out.print("Flattened Right Nodes Sequence: ");
        TreeFlatteningMaster.TreeNode curr = root;
        while (curr != null) {
            System.out.print(curr.val + " -> ");
            curr = curr.right;
        }
        System.out.println("null");

        System.out.println("\n=== 2. BST to Circular Doubly Linked List (LeetCode 426) ===");
        TreeFlatteningMaster.Node bstRoot = new TreeFlatteningMaster.Node(4);
        bstRoot.left = new TreeFlatteningMaster.Node(2);
        bstRoot.right = new TreeFlatteningMaster.Node(5);
        bstRoot.left.left = new TreeFlatteningMaster.Node(1);
        bstRoot.left.right = new TreeFlatteningMaster.Node(3);

        TreeFlatteningMaster.Node head = TreeFlatteningMaster.treeToDoublyList(bstRoot);
        System.out.print("Circular DLL (Head -> Tail): ");
        TreeFlatteningMaster.Node p = head;
        for (int i = 0; i < 5; i++) {
            System.out.print(p.val + " <===> ");
            p = p.right;
        }
        System.out.println("Head(" + p.val + ")");
    }
}
```

---

## 9. Complexity Analysis

| Flattening Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Reversed DFS (114)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Right $\to$ Left $\to$ Root DFS + `prev` |
| **Morris Flatten (114)** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| In-Place `pred.right = curr.right` |
| **BST to DLL (426)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | In-Order `last.right=curr, curr.left=last` |

---

## 10. Edge Cases & Boundary Handling
* **Null Root**: Return `null` immediately.
* **Single Node Tree**: Tree remains unchanged.
* **Already Flattened Right-Leaning Tree**: Morris pointer loop executes in $O(N)$ time without modifying pointers.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting Standard Pre-Order DFS for Flattening (LeetCode 114)**:
  - Processing Root $\to$ Left $\to$ Right and modifying `curr.right` in-place overwrites `curr.right` before the right subtree is visited!
  - **Fix**: Use **Reversed Post-Order DFS (Right $\to$ Left $\to$ Root)** or Morris In-Place Flattening.
* **Forgetting to Set `curr.left = null` in Flattening**:
  - Leaving `curr.left` populated creates cycles and invalid binary tree objects.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Reversed DFS vs Morris In-Place Trade-Off:
> * **Reversed DFS**: ~8 lines of code. Time $O(N)$, Stack Space $O(H)$.
> * **Morris In-Place**: ~12 lines of code. Time $O(N)$, Auxiliary Space **$O(1)$ Constant**.
> Always offer the Morris $O(1)$ space solution as an advanced optimization!

> **Memory Trick:** **"Reversed DFS avoids right-pointer overwrite bugs! Morris links pred.right to curr.right!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard Pre-Order DFS | Reversed Post-Order DFS | Morris In-Place |
| :--- | :--- | :--- | :--- |
| **Traversal Direction** | Root $\to$ Left $\to$ Right | Right $\to$ Left $\to$ Root | Top-Down Pointer Shift |
| **Overwrites Right Child?**| YES (Requires copy) | NO (Processes right first!)| NO (Links to predecessor) |
| **Auxiliary Space** | $O(H)$ | $O(H)$ | **$O(1)$ Constant ⚡** |

---

## 14. How to Recognize This in Questions
* **"Flatten binary tree into a single right-leaning linked list in-place"** $\rightarrow$ LeetCode 114 (Reversed Post-Order DFS or Morris).
* **"Convert BST to sorted circular doubly linked list in-place"** $\rightarrow$ LeetCode 426 (In-order DFS linking `first` and `last`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Reversed Post-Order DFS avoid losing right subtree child pointers?**  
  *A:* By visiting `curr.right` first, the right subtree is completely processed and stored in `prev` before `curr`'s left child or `curr` itself is modified.
* **Q: How does LeetCode 426 make the doubly linked list circular?**  
  *A:* After in-order traversal completes, `first` points to the head and `last` points to the tail. Setting `first.left = last` and `last.right = first` connects head and tail into a circular loop.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLATTENING TREES & BST TO DOUBLY LINKED LIST          |
+-----------------------------------------------------------------------+
| • Flatten Tree (114): Reversed DFS (Right -> Left -> Root)            |
| • Pointer Rule: node.right = prev; node.left = null; prev = node;     |
| • Morris Flatten: pred = right-most of left subtree; pred.right = curr.right|
|   curr.right = curr.left; curr.left = null;                           |
| • BST to DLL (426): In-Order DFS (Left -> Root -> Right)              |
| • DLL Wiring: last.right = curr; curr.left = last; last = curr;       |
| • Circular Wiring: first.left = last; last.right = first;             |
| • Complexity: O(N) Linear Time | Morris O(1) Constant Auxiliary Space |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Reversed DFS Flatten (LeetCode 114) in under 3 minutes.
- [ ] I can write Morris $O(1)$ space Flattening.
- [ ] I know why standard Pre-Order DFS overwrites right child pointers.
- [ ] I can write BST to Circular Doubly Linked List (LeetCode 426).
- [ ] I can explain why Morris In-Place Flattening runs in $O(1)$ auxiliary space.
