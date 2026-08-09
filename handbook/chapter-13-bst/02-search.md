# 02. BST Search Mechanics, Iterative $O(1)$ Space & Range Search Pruning

## 1. Introduction
Searching in a **Binary Search Tree (BST)**—specifically **Search in a Binary Search Tree (LeetCode 700)** and **Range Sum of BST (LeetCode 938)**—leverages the BST ordering invariant ($L < Root < R$) to eliminate an entire candidate subtree at every comparison step. By navigating left when `target < curr.val` and right when `target > curr.val`, BST search executes in **$O(H)$ logarithmic time** (where $H = \log N$ in a balanced BST) and **$O(1)$ Strict Constant Auxiliary Space** when implemented iteratively.

> **Important:** Why does Iterative BST Search achieve **$O(1)$ Auxiliary Space**?
> Unlike general binary trees that require call stacks or explicit queues, a BST search follows a single unidirectional path from root to target!
> Maintaining a single pointer `curr = root` and updating `curr = curr.left` or `curr = curr.right` in a simple `while` loop uses ZERO recursion call stack allocations! ⚡

```
BST Unidirectional Search Path Topology:
Target Key = 25. Tree Root = 50:
                     [ 50 ]  ---> 25 < 50 (Branch LEFT!)
                    /      \
            [ 30 ]          [ 70 ]  ---> 25 < 30 (Branch LEFT!)
           /      \
       [ 25 ]    [ 40 ]             ---> 25 == 25 (TARGET FOUND IN 3 STEPS!) ⚡
```

---

## 2. Core Concepts & Iterative vs Recursive BST Search

### 2.1 Iterative BST Search Algorithm ($O(1)$ Space - Optimal)
1. Set `curr = root`.
2. While `curr != null` AND `curr.val != target`:
   - If `target < curr.val`: `curr = curr.left`.
   - Else (`target > curr.val`): `curr = curr.right`.
3. Return `curr` (Returns found node or `null` if not present).

```
BST Search Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Implementation Variant| Average Time      | Worst Case Time   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Iterative Search**  | **$O(\log N)$ ⚡**| $O(N)$ (Skewed)   | **$O(1)$ Constant ⚡**|
| Recursive Search      | **$O(\log N)$ ⚡**| $O(N)$ (Skewed)   | $O(H)$ Stack Space|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Iterative BST Search: Use a single while loop `curr = (target < curr.val) ? curr.left : curr.right` for O(1) space!"**

---

## 3. Characteristics & Range Search Pruning (LeetCode 938)

### 3.1 Range Sum of BST (LeetCode 938 - Range Pruning)
Given the root of a BST and range `[low, high]`, return the sum of values of all nodes with a value in the inclusive range `[low, high]`:

#### Range Search Pruning Rules:
* If `curr.val > low`: Recurse into `curr.left` (There may be valid keys $\ge low$ in left subtree!).
* If `low <= curr.val && curr.val <= high`: Add `curr.val` to total sum!
* If `curr.val < high`: Recurse into `curr.right` (There may be valid keys $\le high$ in right subtree!).

```
Range Search Branch Pruning Decision:
- If curr.val < low  : PRUNE LEFT SUBTREE completely! (All left keys are < low!).
- If curr.val > high : PRUNE RIGHT SUBTREE completely! (All right keys are > high!).
Pruning reduces search work from O(N) down to O(K + H) where K is matching keys count! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Range Sum of BST (LeetCode 938) on `root = 10`, `low = 7`, `high = 15`:

```
Tree: [10, 5, 15, 3, 7, null, 18]

Call rangeSumBST(10, 7, 15):
- Node 10: 10 in [7, 15] -> Add 10 to sum.
  - 10 > 7 -> Recurse Left (Node 5).
  - 10 < 15 -> Recurse Right (Node 15).

- Node 5: 5 < 7 -> PRUNE LEFT CHILD 3! Only Recurse Right (Node 7).
  - Node 7: 7 in [7, 15] -> Add 7 to sum.

- Node 15: 15 in [7, 15] -> Add 15 to sum.
  - 15 < 15 is false -> PRUNE RIGHT CHILD 18!

Total Range Sum = 10 + 7 + 15 = 32! Executed in 4 node visits! ✅ (O(K + H) Time!)
```

---

## 5. Visual Diagram
Range Search Branch Pruning Topography:

```
                      [ Node 10 ] (In Range 7..15 -> Count 10)
                     /           \
         (10 > 7 -> Search)     (10 < 15 -> Search)
               /                       \
        [ Node 5 ]                   [ Node 15 ] (Count 15)
       /          \                 /           \
  (Pruned 3!)   [ Node 7 ]     (No left)    (Pruned 18!)
  (3 < 7!)     (Count 7)                    (18 > 15!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Search in a BST (LeetCode 700 - Iterative and Recursive) and Range Sum of BST (LeetCode 938):

```java
import java.util.*;

public class BSTSearchMaster {

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

    // 1. Search in a BST Iterative (LeetCode 700) O(H) Time, O(1) Auxiliary Space (Optimal!)
    public static TreeNode searchBSTIterative(TreeNode root, int val) {
        TreeNode curr = root;
        while (curr != null && curr.val != val) {
            if (val < curr.val) {
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }
        return curr;
    }

    // 2. Search in a BST Recursive O(H) Time, O(H) Call Stack Space
    public static TreeNode searchBSTRecursive(TreeNode root, int val) {
        if (root == null || root.val == val) {
            return root;
        }
        if (val < root.val) {
            return searchBSTRecursive(root.left, val);
        } else {
            return searchBSTRecursive(root.right, val);
        }
    }

    // 3. Range Sum of BST with Pruning (LeetCode 938) O(K + H) Time, O(H) Space
    public static int rangeSumBST(TreeNode root, int low, int high) {
        if (root == null) return 0;

        int sum = 0;
        if (low <= root.val && root.val <= high) {
            sum += root.val; // Value inside range
        }

        // Branch Pruning Condition 1: Go Left if root.val > low
        if (root.val > low) {
            sum += rangeSumBST(root.left, low, high);
        }

        // Branch Pruning Condition 2: Go Right if root.val < high
        if (root.val < high) {
            sum += rangeSumBST(root.right, low, high);
        }

        return sum;
    }
}
```

> **Quick Syntax:**
```java
// Iterative BST Search Loop
while (curr != null && curr.val != target) curr = (target < curr.val) ? curr.left : curr.right;
```

---

## 7. Concrete Problem Examples
* **LeetCode 700 - Search in a Binary Search Tree**: Fundamental BST search.
* **LeetCode 938 - Range Sum of BST**: Range search with branch pruning.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Iterative BST Search and Range Sum of BST:

```java
public class BSTSearchDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Iterative BST Search Test ===");
        BSTSearchMaster.TreeNode root = new BSTSearchMaster.TreeNode(4);
        root.left = new BSTSearchMaster.TreeNode(2, 
            new BSTSearchMaster.TreeNode(1), new BSTSearchMaster.TreeNode(3));
        root.right = new BSTSearchMaster.TreeNode(7);

        BSTSearchMaster.TreeNode found = BSTSearchMaster.searchBSTIterative(root, 2);
        System.out.println("Search Val 2: Found Subtree Root Val = " + 
            (found != null ? found.val : "null")); // Output: 2

        System.out.println("\n=== 2. Range Sum of BST Test (LeetCode 938) ===");
        int rangeSum = BSTSearchMaster.rangeSumBST(root, 2, 7);
        System.out.println("Range Sum [2, 7]: " + rangeSum); // Output: 16 (2 + 3 + 4 + 7) ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Iterative Search (700)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|
| **Recursive Search (700)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Call Stack Space |
| **Range Sum BST (938)** | **$O(\log N)$ ⚡** | **$O(K + H)$ ⚡** | $O(N)$ Linear | $O(H)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Target Key Not Found**: `searchBSTIterative` returns `null` safely.
* **Single Node Tree**: Search finishes in 1 comparison step.

---

## 11. Common Mistakes & Anti-Patterns
* **Using General Binary Tree Search ($O(N)$ Time Penalty) for a BST**:
  - Searching both left and right subtrees unconditionally ignores the BST invariant and wastes $O(N)$ time.
  - **Always compare `target` with `curr.val` to branch into left OR right subtree**.
* **Unnecessary Recursion Stack Allocation**:
  - Prefer iterative `while` loops over recursion for simple BST search to achieve $O(1)$ auxiliary space.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Range Search Pruning Saves Time:
> In Range Sum of BST (LeetCode 938):
> If `curr.val < low`, EVERY key in `curr.left` is strictly smaller than `curr.val` ($< low$). Searching `curr.left` is guaranteed to find ZERO valid elements!
> Pruning `curr.left` skips entire subtrees, executing range queries in **$O(K + H)$ time**!

> **Memory Trick:** **"If curr.val < low, prune left! If curr.val > high, prune right!"**

---

## 13. System & Implementation Comparisons

| Feature | Iterative BST Search | Recursive BST Search |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Strict Constant ⚡** | $O(H)$ Call Stack Space |
| **Stack Overflow Risk** | **Zero Stack Overflow Risk ⚡**| Risk on Deep Skewed Trees |
| **Execution Speed** | **Fastest (Single Loop) ⚡** | Slightly Slower |

---

## 14. How to Recognize This in Questions
* **"Search for a target value in a Binary Search Tree"** $\rightarrow$ LeetCode 700 (Iterative BST search).
* **"Sum all values in BST falling within [low, high] range"** $\rightarrow$ LeetCode 938 (Pruned range search).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is iterative search preferred over recursive search in production BST implementations?**  
  *A:* Because iterative BST search consumes $O(1)$ auxiliary space and eliminates stack overflow risks on deep or skewed trees.
* **Q: What is the time complexity of Range Sum of BST if the entire tree falls within `[low, high]`?**  
  *A:* $O(N)$ linear time, because every node in the tree is visited.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST SEARCH & RANGE PRUNING                            |
+-----------------------------------------------------------------------+
| • Search Decision : If target < curr.val go left; else go right       |
| • Iterative Loop  : while (curr != null && curr.val != target)        |
| • Space Bounds    : Iterative search uses O(1) Auxiliary Space ⚡     |
| • Pruning Rule 1  : If curr.val > low -> Search Left Subtree          |
| • Pruning Rule 2  : If curr.val < high -> Search Right Subtree         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Iterative BST Search (LeetCode 700) in $O(1)$ space.
- [ ] I can write Range Sum of BST (LeetCode 938) with branch pruning.
- [ ] I know why iterative search eliminates stack overflow risks.
- [ ] I know how range search pruning prunes irrelevant subtrees.
- [ ] I can trace search paths on balanced vs skewed trees.
