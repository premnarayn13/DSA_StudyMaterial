# 14. BST Conversions, Reverse In-Order Traversals & Divide-and-Conquer Transformations

## 1. Introduction
**BST Conversions and Structural Transformations** convert Binary Search Trees into other data structures (such as Doubly Linked Lists or Greater Sum Trees) or construct height-balanced BSTs from linear inputs (such as Sorted Arrays or Sorted Linked Lists). Algorithms like **Convert Sorted Array to BST (LeetCode 108)**, **Convert Sorted List to BST (LeetCode 109)**, **Convert BST to Greater Tree (LeetCode 538 / 1038)**, and **Convert BST to Sorted Doubly Linked List (LeetCode 426)** execute in **$O(N)$ linear time and $O(H)$ auxiliary space** using **Reverse In-Order Traversals** and **Divide-and-Conquer Midpoint Partitioning**.

> **Important:** Why does **Reverse In-Order Traversal (`Right -> Root -> Left`)** solve Convert BST to Greater Tree (LeetCode 538)?
> Standard In-Order (`Left -> Root -> Right`) visits keys in ascending order (`1 -> 2 -> 3`).
> Reverse In-Order (`Right -> Root -> Left`) visits keys in **STRICTLY DESCENDING ORDER (`3 -> 2 -> 1`)**!
> Maintaining a running sum of visited values continuously replaces each key with the sum of all keys greater than or equal to it in a single pass! ⚡

```
Reverse In-Order Cumulative Sum Topology:
Standard BST Keys  : 2  <--- 5  <--- 13  (Right-to-Left Traversal Order)
Running Cumulative : 20 <--- 18 <--- 13  (Each node updated to sum of all larger keys!) ⚡
```

---

## 2. Core Concepts & Divide-and-Conquer Array Conversion (LeetCode 108)

### 2.1 Convert Sorted Array to Height-Balanced BST (LeetCode 108)
Given an integer array `nums` where elements are sorted in ascending order, convert it to a **Height-Balanced Binary Search Tree**:

#### Divide-and-Conquer Midpoint Strategy ($O(N)$ Time, $O(\log N)$ Stack Space):
1. To ensure equal node balance across left and right subtrees, ALWAYS pick the **MIDPOINT ELEMENT** as the root node!
   $$\text{mid} = \text{left} + \frac{\text{right} - \text{left}}{2}$$
2. Create `root = new TreeNode(nums[mid])`.
3. Recursively build left subtree from left half: `root.left = build(left, mid - 1)`.
4. Recursively build right subtree from right half: `root.right = build(mid + 1, right)`.
5. Return `root`.

```
Divide-and-Conquer Array Partitioning Topology:
Array: [ -10,  -3,   0,   5,   9 ]
               |     ^    |
          Left Sub  Mid  Right Sub
Root = 0. Left Subtree built from [-10, -3]. Right Subtree built from [5, 9].
Guarantees Height-Balanced BST with Height H <= log2(N)! ⚡
```

> **Memory Trick:** **"Convert Sorted Array to BST: Pick mid = (left + right)/2 as root! Build left from (left, mid-1), right from (mid+1, right)!"**

---

## 3. Characteristics & Convert BST to Doubly Linked List (LeetCode 426)

### 3.1 Convert Binary Search Tree to Sorted Doubly Linked List (LeetCode 426)
Convert a BST into a Circular Doubly Linked List in-place (where `left` acts as `prev` pointer and `right` acts as `next` pointer):
* **In-Order Traversal Linkage ($O(N)$ Time, $O(H)$ Auxiliary Space)**:
  1. Maintain `first = null` and `last = null`.
  2. Perform standard In-Order traversal (`Left -> Root -> Right`):
     - For current node `curr`:
       - If `last != null`: Link `last.right = curr` and `curr.left = last`.
       - Else: Set `first = curr` (Head of Doubly Linked List!).
       - Update `last = curr`.
  3. After traversal completes, close circular loop:
     - `first.left = last; last.right = first;`
  4. Return `first`.

---

## 4. Internal Working Mechanics
Tracing Convert BST to Greater Tree (LeetCode 538) on BST `[4, 1, 6, 0, 2, 5, 7]`:

```
Init: runningSum = 0. Traversal Order: Right -> Root -> Left

1. Visit 7: runningSum += 7 = 7. Node 7 -> 7.
2. Visit 6: runningSum += 6 = 13. Node 6 -> 13.
3. Visit 5: runningSum += 5 = 18. Node 5 -> 18.
4. Visit 4: runningSum += 4 = 22. Node 4 -> 22.
5. Visit 2: runningSum += 2 = 24. Node 2 -> 24.
6. Visit 1: runningSum += 1 = 25. Node 1 -> 25.
7. Visit 0: runningSum += 0 = 25. Node 0 -> 25.

Tree converted to Greater Tree in 1 single pass! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Convert BST to Sorted Doubly Linked List (LeetCode 426) Linkage Topography:

```
BST Nodes in In-Order: Node(1) <---> Node(2) <---> Node(3)
                         ^                           ^
                       first                       last
Circular Loop Close  : first.left = last; last.right = first; ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Convert Sorted Array to BST (LeetCode 108), Convert Sorted List to BST (LeetCode 109), Convert BST to Greater Tree (LeetCode 538), and Convert BST to Doubly Linked List (LeetCode 426):

```java
import java.util.*;

public class BSTConversionsMaster {

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

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Convert Sorted Array to BST (LeetCode 108) O(N) Time, O(log N) Space
    public static TreeNode sortedArrayToBST(int[] nums) {
        if (nums == null || nums.length == 0) return null;
        return buildArrayBST(nums, 0, nums.length - 1);
    }

    private static TreeNode buildArrayBST(int[] nums, int left, int right) {
        if (left > right) return null;

        // Choose midpoint to guarantee height balance
        int mid = left + (right - left) / 2;
        TreeNode root = new TreeNode(nums[mid]);

        root.left = buildArrayBST(nums, left, mid - 1);
        root.right = buildArrayBST(nums, mid + 1, right);

        return root;
    }

    // 2. Convert Sorted List to BST (LeetCode 109 - Slow/Fast Pointer) O(N log N) Time
    public static TreeNode sortedListToBST(ListNode head) {
        if (head == null) return null;
        if (head.next == null) return new TreeNode(head.val);

        // Find midpoint using Slow and Fast pointers (with prev pointer)
        ListNode prev = null;
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            prev = slow;
            slow = slow.next;
            fast = fast.next.next;
        }

        // Disconnect left half from slow midpoint
        if (prev != null) {
            prev.next = null;
        }

        TreeNode root = new TreeNode(slow.val);
        root.left = sortedListToBST(head);
        root.right = sortedListToBST(slow.next);

        return root;
    }

    // 3. Convert BST to Greater Tree (LeetCode 538 / 1038) O(N) Time, O(H) Space
    private static int runningSum = 0;

    public static TreeNode convertBST(TreeNode root) {
        runningSum = 0;
        reverseInorder(root);
        return root;
    }

    // Reverse In-Order Traversal: Right -> Root -> Left
    private static void reverseInorder(TreeNode node) {
        if (node == null) return;

        reverseInorder(node.right); // 1. Traverse Right Subtree

        runningSum += node.val;     // 2. Update Running Sum & Overwrite Node Val
        node.val = runningSum;

        reverseInorder(node.left);  // 3. Traverse Left Subtree
    }

    // 4. Convert BST to Doubly Linked List (LeetCode 426) O(N) Time, O(H) Space
    private static TreeNode firstDLL = null;
    private static TreeNode lastDLL = null;

    public static TreeNode treeToDoublyList(TreeNode root) {
        if (root == null) return null;
        firstDLL = null;
        lastDLL = null;

        inorderDLL(root);

        // Close circular doubly linked list loop
        firstDLL.left = lastDLL;
        lastDLL.right = firstDLL;

        return firstDLL;
    }

    private static void inorderDLL(TreeNode node) {
        if (node == null) return;

        inorderDLL(node.left);

        if (lastDLL != null) {
            lastDLL.right = node; // Right is Next pointer
            node.left = lastDLL;  // Left is Prev pointer
        } else {
            firstDLL = node;      // First node visited is head
        }
        lastDLL = node;

        inorderDLL(node.right);
    }
}
```

> **Quick Syntax:**
```java
// Reverse In-Order Line for Greater Tree
reverseInorder(node.right);
runningSum += node.val;
node.val = runningSum;
reverseInorder(node.left);
```

---

## 7. Concrete Problem Examples
* **LeetCode 108 - Convert Sorted Array to Binary Search Tree**: Midpoint array divide & conquer.
* **LeetCode 109 - Convert Sorted List to Binary Search Tree**: Slow/fast pointer linked list conversion.
* **LeetCode 538 - Convert BST to Greater Tree**: Reverse in-order cumulative sum.
* **LeetCode 426 - Convert BST to Sorted Doubly Linked List**: In-order pointer linkage.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Convert Sorted Array to BST and Convert BST to Greater Tree:

```java
public class BSTConversionsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Convert Sorted Array to BST (LeetCode 108) ===");
        int[] nums = {-10, -3, 0, 5, 9};
        BSTConversionsMaster.TreeNode root = BSTConversionsMaster.sortedArrayToBST(nums);
        System.out.println("Reconstructed Root: " + root.val); // Output: 0 (Midpoint!)
        System.out.println("Root Left:  " + root.left.val);     // Output: -3
        System.out.println("Root Right: " + root.right.val);    // Output: 9

        System.out.println("\n=== 2. Convert BST to Greater Tree (LeetCode 538) ===");
        // Build BST: (4) with left 1, right 6
        BSTConversionsMaster.TreeNode bst = new BSTConversionsMaster.TreeNode(4, 
            new BSTConversionsMaster.TreeNode(1), new BSTConversionsMaster.TreeNode(6));

        BSTConversionsMaster.convertBST(bst);
        System.out.println("New Root Value (4 -> 4+6=10): " + bst.val);       // Output: 10
        System.out.println("New Right Value (6 -> 6):     " + bst.right.val); // Output: 6
        System.out.println("New Left Value (1 -> 1+10=11): " + bst.left.val);  // Output: 11 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Array to BST (108)** | **$O(N)$ Linear ⚡** | $O(\log N)$ Stack Space | Midpoint index splitting `(left+right)/2` |
| **List to BST (109)** | **$O(N \log N)$ ⚡** | $O(\log N)$ Stack Space | Slow/fast pointer midpoint find |
| **Greater Tree (538)** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Reverse In-Order `Right -> Root -> Left` |
| **BST to DLL (426)** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | In-Order `last.right = curr; curr.left = last` |

---

## 10. Edge Cases & Boundary Handling
* **Empty Input Array / List**: Returns `null` immediately.
* **Single Element Array (`[5]`)**: Creates root node 5 with `left = null` and `right = null`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Standard In-Order (`Left -> Root -> Right`) for Greater Tree**:
  - Standard In-Order visits keys in ascending order (`1 -> 2 -> 3`), requiring extra passes to calculate suffix sums.
  - **Use Reverse In-Order (`Right -> Root -> Left`) for $O(N)$ single-pass execution**.
* **Integer Overflow in Midpoint Calculation**:
  - Writing `mid = (left + right) / 2` causes integer overflow for large arrays.
  - **Use `mid = left + (right - left) / 2`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Reverse In-Order (`Right -> Root -> Left`) Replaces Values with Greater Sums:
> A node's value in a Greater Sum Tree must equal: $\text{Node.val} + \sum \text{All larger keys in BST}$.
> Because all larger keys reside in the RIGHT subtree and ancestor nodes, traversing `Right Subtree -> Node -> Left Subtree` visits nodes in strictly descending order.
> Accumulating `runningSum += node.val` and assigning `node.val = runningSum` updates every node in **$O(N)$ time**!

> **Memory Trick:** **"Reverse In-Order = Right -> Root -> Left! Visits keys in descending order for Greater Sum Trees!"**

---

## 13. System & Implementation Comparisons

| Feature | Sorted Array to BST (108) | Sorted List to BST (109) |
| :--- | :--- | :--- |
| **Midpoint Access Time** | **$O(1)$ Direct Index ⚡** | $O(N)$ Slow/Fast Pointer |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \log N)$ Logarithmic |
| **Auxiliary Memory** | $O(\log N)$ Stack Space | $O(\log N)$ Stack Space |

---

## 14. How to Recognize This in Questions
* **"Convert sorted array to height-balanced BST"** $\rightarrow$ LeetCode 108 (Midpoint divide & conquer).
* **"Convert BST so every key is replaced by sum of all larger keys"** $\rightarrow$ LeetCode 538 (Reverse In-Order `Right -> Root -> Left`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `sortedArrayToBST` pick the midpoint element as the root node?**  
  *A:* Picking the midpoint element `mid = left + (right - left) / 2` guarantees that the left half and right half contain equal (or off-by-one) number of elements, ensuring that left and right subtrees have equal height ($H = \lfloor \log_2 N \rfloor$).
* **Q: How can `sortedListToBST` be optimized to run in $O(N)$ time instead of $O(N \log N)$?**  
  *A:* By simulating In-Order tree construction! Pass list length $N$, recursively build the left subtree, consume the head list node for the root, and build the right subtree.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST CONVERSIONS & TRANSFORMATIONS                     |
+-----------------------------------------------------------------------+
| • Array to BST (108): Pick mid = left + (right - left) / 2 as root    |
| • Greater Tree (538): Reverse In-Order traversal (Right -> Root -> Left)|
| • Running Sum Rule  : runningSum += node.val; node.val = runningSum;  |
| • BST to DLL (426)  : In-Order traversal linking last.right = curr    |
| • DLL Loop Close    : first.left = last; last.right = first;          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Convert Sorted Array to BST (LeetCode 108).
- [ ] I can write Convert BST to Greater Tree (LeetCode 538) using Reverse In-Order.
- [ ] I can write Convert BST to Doubly Linked List (LeetCode 426).
- [ ] I know why midpoint selection guarantees height balance.
- [ ] I know why Reverse In-Order visits keys in descending order.
