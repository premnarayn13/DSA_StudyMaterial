# 08. BST Validation, Long Range Bounds & Swapped Node Recovery Engines

## 1. Introduction
Validating whether an arbitrary binary tree is a valid Binary Search Tree—specifically **Validate Binary Search Tree (LeetCode 98)** and **Recover Binary Search Tree (LeetCode 99)**—requires verifying that every node obeys global subtree boundary constraints. While naive parent-child checks fail to detect grand-ancestor violations, **Range Boundary Recursion `(minBound, maxBound)`** and **In-Order Traversal Invariant Checking** validate BSTs in **$O(N)$ linear time and $O(H)$ auxiliary space**.

> **Important:** Why Local Parent-Child Check (`node.left < node && node.right > node`) FAILS:
> Checking only immediate parent-child links misses grand-ancestor constraint violations!
> For example: A node in a right subtree could be smaller than a higher ancestor node!
> * **Correct Strategy 1 (Range Bounds)**: Pass `(minBound, maxBound)` boundaries down recursively using `Long.MIN_VALUE` and `Long.MAX_VALUE`!
> * **Correct Strategy 2 (In-Order Prev Pointer)**: Verify that In-Order traversal yields a strictly increasing sequence (`prev < curr.val`)! ⚡

```
Invalid BST Example (Local check passes, BUT global check FAILS!):
         10
        /  \
       5   15
          /  \
        (6)   20   <--- Local check: 6 < 15 passes! BUT 6 is in RIGHT subtree of 10! INVALID! ❌
```

---

## 2. Core Concepts & Range Boundary Recursion (LeetCode 98)

### 2.1 Range Boundary Recursion Strategy
Pass valid value boundaries `(minBound, maxBound)` down the tree:
1. `validate(root, Long.MIN_VALUE, Long.MAX_VALUE)`:
   - Base Case: If `node == null`, return `true`.
   - Range Check: If `node.val <= minBound || node.val >= maxBound`, return `false`!
   - **Left Child Call**: Range becomes **`(minBound, node.val)`** (Upper bound restricted to `node.val`).
   - **Right Child Call**: Range becomes **`(node.val, maxBound)`** (Lower bound restricted to `node.val`).
   - Return `validate(node.left, minBound, node.val) && validate(node.right, node.val, maxBound)`.

```
BST Validation Strategy Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Validation Strategy   | Time Complexity   | Auxiliary Space   | Key Advantage     |
+-----------------------+-------------------+-------------------+-------------------+
| **Range Bounds (`Long`)**| **$O(N)$ Linear ⚡**| $O(H)$ Stack Space | Pure functional recursion|
| **In-Order Prev Pointer**| **$O(N)$ Linear ⚡**| $O(H)$ Stack Space | Direct sorted order check|
| **Morris Validation** | **$O(N)$ Linear ⚡**| **$O(1)$ Constant ⚡**| Zero stack allocation|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Validate BST: Use Long.MIN_VALUE and Long.MAX_VALUE to prevent Integer overflow!"**

---

## 3. Characteristics & Recover Binary Search Tree (LeetCode 99)

### 3.1 Recover Binary Search Tree (LeetCode 99)
Two elements in a BST are swapped by mistake. Recover the tree without changing its structure in $O(1)$ auxiliary space:
* Perform In-Order traversal while tracking `prev`, `first`, and `second`:
  - If `prev != null && prev.val > curr.val`:
    - First violation: `first = prev`, `second = curr`.
    - Second violation (if any): `second = curr`.
* Swap `first.val` and `second.val`!

---

## 4. Internal Working Mechanics
Tracing Validate Binary Search Tree (LeetCode 98) on Invalid Tree `[10, 5, 15, null, null, 6, 20]`:

```
Call validate(10, MIN_VAL, MAX_VAL):
- Left Call : validate(5, MIN_VAL, 10)  -> Valid (5 in range).
- Right Call: validate(15, 10, MAX_VAL) -> Valid so far.
    - Left Child 6 Call: validate(6, 10, 15):
        - Check: 6 <= 10 (minBound) -> FAILS RANGE CHECK!
        - Returns FALSE!

Validation terminates early with FALSE! Tree is INVALID! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Range Bounds Inheritance Topography:

```
                      Root 10  (Range: -inf ... +inf)
                     /       \
         (Range: -inf ... 10) (Range: 10 ... +inf)
                 /                 \
            Node 5               Node 15
                                 /      \
                    (Range: 10 ... 15)  (Range: 15 ... +inf)
                           /                  \
                       Node 6 (FAIL!)       Node 20
                       (6 is NOT > 10!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Validate BST (LeetCode 98 - Range Bounds and In-Order Prev) and Recover BST (LeetCode 99):

```java
import java.util.*;

public class BSTValidationMaster {

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

    // 1. Validate BST Range Bounds (LeetCode 98) O(N) Time, O(H) Space
    public static boolean isValidBST(TreeNode root) {
        return validateRange(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean validateRange(TreeNode node, long minBound, long maxBound) {
        if (node == null) return true;

        // Range Invariant Check
        if (node.val <= minBound || node.val >= maxBound) {
            return false;
        }

        // Left child max bound is node.val; Right child min bound is node.val
        return validateRange(node.left, minBound, node.val) &&
               validateRange(node.right, node.val, maxBound);
    }

    // 2. Validate BST In-Order Prev Pointer Strategy O(N) Time, O(H) Space
    private static TreeNode prevNode = null;

    public static boolean isValidBSTInorder(TreeNode root) {
        prevNode = null; // Reset static state
        return inorderCheck(root);
    }

    private static boolean inorderCheck(TreeNode node) {
        if (node == null) return true;

        if (!inorderCheck(node.left)) return false;

        if (prevNode != null && node.val <= prevNode.val) {
            return false; // Violation of strictly ascending order!
        }
        prevNode = node;

        return inorderCheck(node.right);
    }

    // 3. Recover Binary Search Tree (LeetCode 99) O(N) Time, O(H) Space
    private static TreeNode firstSwapped = null;
    private static TreeNode secondSwapped = null;
    private static TreeNode prevRecover = null;

    public static void recoverTree(TreeNode root) {
        firstSwapped = null;
        secondSwapped = null;
        prevRecover = null;

        findSwappedNodes(root);

        // Swap back the values of the two corrupted nodes
        if (firstSwapped != null && secondSwapped != null) {
            int temp = firstSwapped.val;
            firstSwapped.val = secondSwapped.val;
            secondSwapped.val = temp;
        }
    }

    private static void findSwappedNodes(TreeNode node) {
        if (node == null) return;

        findSwappedNodes(node.left);

        if (prevRecover != null && prevRecover.val > node.val) {
            if (firstSwapped == null) {
                firstSwapped = prevRecover; // First violation
            }
            secondSwapped = node; // Second violation (or adjacent violation)
        }
        prevRecover = node;

        findSwappedNodes(node.right);
    }
}
```

> **Quick Syntax:**
```java
// Validate BST Long Range Line
return validateRange(node.left, minBound, node.val) && validateRange(node.right, node.val, maxBound);
```

---

## 7. Concrete Problem Examples
* **LeetCode 98 - Validate Binary Search Tree**: Range bounds validation.
* **LeetCode 99 - Recover Binary Search Tree**: In-order swapped nodes recovery.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Validate BST and Recover BST:

```java
public class BSTValidationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Validate BST Test (LeetCode 98) ===");
        BSTValidationMaster.TreeNode validRoot = new BSTValidationMaster.TreeNode(5);
        validRoot.left = new BSTValidationMaster.TreeNode(1);
        validRoot.right = new BSTValidationMaster.TreeNode(6, 
            new BSTValidationMaster.TreeNode(3), new BSTValidationMaster.TreeNode(7));

        System.out.println("Is Valid BST? " + 
            BSTValidationMaster.isValidBST(validRoot)); // false (3 is in right subtree of 5!)

        System.out.println("\n=== 2. Recover BST Test (LeetCode 99) ===");
        // Build Swapped Tree: [1, 3, null, null, 2] (3 and 1 swapped)
        BSTValidationMaster.TreeNode corrupted = new BSTValidationMaster.TreeNode(3);
        corrupted.left = new BSTValidationMaster.TreeNode(1, null, new BSTValidationMaster.TreeNode(2));

        BSTValidationMaster.recoverTree(corrupted);
        System.out.println("Recovered Root Value: " + corrupted.val); // Output: 1
        System.out.println("Is Valid After Recovery? " + 
            BSTValidationMaster.isValidBST(corrupted)); // Output: true ✅
    }
}
```

---

## 9. Complexity Analysis

| Validation Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space |
| **Recover BST (99)**  | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Node Values Equal `Integer.MIN_VALUE` / `Integer.MAX_VALUE`**: Using `int` range bounds causes overflow errors. Always use **`Long.MIN_VALUE` and `Long.MAX_VALUE`**!
* **Adjacent Swapped Nodes in Recover BST**: Handled cleanly by updating `secondSwapped = node` on both violations.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Integer.MIN_VALUE` for Range Bounds**:
  - `node.val <= minBound` returns `false` incorrectly when `node.val == Integer.MIN_VALUE`.
  - **Use `Long.MIN_VALUE` and `Long.MAX_VALUE`**.
* **Checking Only Local Parent-Child Links**:
  - Local parent-child checks miss grand-ancestor violations.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `Long.MIN_VALUE` and `Long.MAX_VALUE` are Mandatory:
> LeetCode 98 includes test cases containing single nodes with value `-2147483648` (`Integer.MIN_VALUE`).
> If you write `validate(root, Integer.MIN_VALUE, Integer.MAX_VALUE)`:
> The boundary condition `node.val <= minBound` evaluates `-2147483648 <= -2147483648` to `true`, incorrectly failing valid trees!
> **Always use 64-bit `Long` bounds!**

> **Memory Trick:** **"Use 64-bit Long bounds to prevent Integer.MIN_VALUE validation overflow bugs!"**

---

## 13. System & Implementation Comparisons

| Feature | Range Bounds Strategy | In-Order Prev Pointer Strategy |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Memory** | $O(H)$ Call Stack | $O(H)$ Call Stack |
| **State Dependencies**| Pure Parameters | Requires Static `prev` Pointer |

---

## 14. How to Recognize This in Questions
* **"Validate whether a binary tree is a valid Binary Search Tree"** $\rightarrow$ LeetCode 98 (Range bounds using `Long`).
* **"Recover a BST where two nodes were swapped"** $\rightarrow$ LeetCode 99 (In-order violation tracking).

---

## 15. Frequently Asked Interview Questions
* **Q: How can Recover BST (LeetCode 99) be solved in $O(1)$ auxiliary space?**  
  *A:* By performing the In-Order traversal using **Morris Traversal** instead of recursion.
* **Q: Why does `prev.val > curr.val` identify swapped nodes in a BST?**  
  *A:* Because In-Order traversal of a valid BST must yield a strictly increasing sequence. Any decrease (`prev.val > curr.val`) indicates a swapped node violation.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST VALIDATION & RECOVERY                             |
+-----------------------------------------------------------------------+
| • Validation Bounds: Pass (Long.MIN_VALUE, Long.MAX_VALUE) range      |
| • Left Child Bounds: validate(node.left, minBound, node.val)          |
| • Right Child Bounds: validate(node.right, node.val, maxBound)        |
| • Overflow Trap   : NEVER use Integer bounds; use Long bounds!        |
| • Recover BST (99): Track prev.val > curr.val violations during Inorder|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Validate BST (LeetCode 98) using `Long` range bounds.
- [ ] I can write Recover BST (LeetCode 99) in $O(N)$ time.
- [ ] I know why `Integer.MIN_VALUE` causes overflow bugs in BST validation.
- [ ] I know why local parent-child checks fail.
- [ ] I can trace swapped node recovery for adjacent vs distant nodes.
