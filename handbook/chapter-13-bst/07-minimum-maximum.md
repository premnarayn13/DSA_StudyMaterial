# 07. BST Minimum, Maximum, Floor & Ceiling Operations in $O(1)$ Space

## 1. Introduction
Finding the **Minimum**, **Maximum**, **Floor** (largest value $\le X$), and **Ceiling** (smallest value $\ge X$) in a **Binary Search Tree (BST)** leverages the BST ordering invariant ($L < Root < R$) to achieve **$O(H)$ logarithmic time** (where $H = \log N$ in a balanced BST) and **$O(1)$ Strict Constant Auxiliary Space**. Because minimum and maximum elements reside at extreme structural boundaries, finding min/max requires simple single-direction link traversals down the tree.

> **Important:** Fundamental Rules for Extreme Key Operations in a BST:
> 1. **Global Minimum Node**: Always the **LEFTMOST NODE** in the BST (`while (curr.left != null) curr = curr.left`).
> 2. **Global Maximum Node**: Always the **RIGHTMOST NODE** in the BST (`while (curr.right != null) curr = curr.right`).
> 3. **Floor of Key $X$**: Largest key in BST that is $\le X$. (Record candidate when `curr.val <= X` and move right!).
> 4. **Ceiling of Key $X$**: Smallest key in BST that is $\ge X$. (Record candidate when `curr.val >= X` and move left!). ⚡

```
BST Extreme Values & Floor / Ceiling Spectrum:
                       [ 50 ]  <--- Root
                      /      \
            [ 30 ]            [ 70 ]  <--- Maximum Node (Rightmost!)
           /      \
       [ 20 ]    [ 40 ]
         ^
  Minimum Node (Leftmost!)

Floor of 35 = 30 (Largest val <= 35) | Ceiling of 35 = 40 (Smallest val >= 35) ⚡
```

---

## 2. Core Concepts & Floor / Ceiling Search Architecture

### 2.1 Floor and Ceiling Algorithms ($O(1)$ Space)
* **Floor Search Algorithm (Key $X$)**:
  1. `floor = null`, `curr = root`.
  2. While `curr != null`:
     - If `curr.val == X`: Return `curr.val`! (Exact match).
     - If `curr.val < X`: `floor = curr.val` (Record candidate floor!); `curr = curr.right`.
     - Else (`curr.val > X`): `curr = curr.left`.
  3. Return `floor`.

* **Ceiling Search Algorithm (Key $X$)**:
  1. `ceiling = null`, `curr = root`.
  2. While `curr != null`:
     - If `curr.val == X`: Return `curr.val`!
     - If `curr.val > X`: `ceiling = curr.val` (Record candidate ceiling!); `curr = curr.left`.
     - Else (`curr.val < X`): `curr = curr.right`.
  3. Return `ceiling`.

```
Floor & Ceiling Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Intent      | Search Candidate  | Move Direction    | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Global Minimum**    | `curr.left`       | Unidirectional Left| **$O(1)$ Constant ⚡**|
| **Global Maximum**    | `curr.right`      | Unidirectional Right| **$O(1)$ Constant ⚡**|
| **Floor(X) ($\le X$)**| `curr.val < X`    | Candidate = curr, Move Right| **$O(1)$ Constant ⚡**|
| **Ceil(X) ($\ge X$)** | `curr.val > X`    | Candidate = curr, Move Left| **$O(1)$ Constant ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Min = Leftmost! Max = Rightmost! Floor(X): record candidate when val < X and move right!"**

---

## 3. Characteristics & Property Proofs

### 3.1 Unidirectional Extreme Traversal Guarantee
Because all keys in `curr.left` are strictly less than `curr.val`, no node in `curr.left` can ever contain the maximum element of a tree. Therefore, finding the maximum ONLY needs to navigate down `curr.right` links without backtracking!

---

## 4. Internal Working Mechanics
Tracing Floor(35) in BST `[50, 30, 70, 20, 40]`:

```
Init: X = 35. floor = null, curr = root (50).

Step 1: curr = 50. 35 < 50:
  - Move curr = curr.left (Node 30).

Step 2: curr = 30. 35 > 30:
  - Record candidate: floor = 30.
  - Move curr = curr.right (Node 40).

Step 3: curr = 40. 35 < 40:
  - Move curr = curr.left (null).

Loop terminates!

Returns Floor(35) = 30! ✅ (O(H) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Floor vs Ceiling Search Path Topography:

```
                      [ Root 50 ] (35 < 50, Move Left)
                     /         \
            [ Node 30 ]        (Node 70) (35 > 30 -> Record Floor = 30, Move Right)
           /          \
      (Node 20)     [ Node 40 ] (35 < 40 -> Record Ceiling = 40, Move Left -> Null!)
                       |
               Floor = 30 | Ceiling = 40! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Minimum, Maximum, Floor, and Ceiling in a BST:

```java
import java.util.*;

public class BSTMinMaxMaster {

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

    // 1. Find Minimum Key in BST O(H) Time, O(1) Auxiliary Space
    public static TreeNode findMin(TreeNode root) {
        if (root == null) return null;
        TreeNode curr = root;
        while (curr.left != null) {
            curr = curr.left; // Follow leftmost links
        }
        return curr;
    }

    // 2. Find Maximum Key in BST O(H) Time, O(1) Auxiliary Space
    public static TreeNode findMax(TreeNode root) {
        if (root == null) return null;
        TreeNode curr = root;
        while (curr.right != null) {
            curr = curr.right; // Follow rightmost links
        }
        return curr;
    }

    // 3. Find Floor of Key X in BST (Largest val <= X) O(H) Time, O(1) Space
    public static Integer findFloor(TreeNode root, int x) {
        Integer floor = null;
        TreeNode curr = root;

        while (curr != null) {
            if (curr.val == x) {
                return curr.val; // Exact match
            }
            if (curr.val < x) {
                floor = curr.val; // Candidate floor found
                curr = curr.right;
            } else {
                curr = curr.left;
            }
        }

        return floor;
    }

    // 4. Find Ceiling of Key X in BST (Smallest val >= X) O(H) Time, O(1) Space
    public static Integer findCeiling(TreeNode root, int x) {
        Integer ceiling = null;
        TreeNode curr = root;

        while (curr != null) {
            if (curr.val == x) {
                return curr.val; // Exact match
            }
            if (curr.val > x) {
                ceiling = curr.val; // Candidate ceiling found
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }

        return ceiling;
    }
}
```

> **Quick Syntax:**
```java
// Floor Search Candidate Line
if (curr.val < x) { floor = curr.val; curr = curr.right; }
```

---

## 7. Concrete Problem Examples
* **Floor & Ceiling in BST**: Boundary key searches.
* **BST Range Extremes**: Min/Max key extraction.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Minimum, Maximum, Floor, and Ceiling:

```java
public class BSTMinMaxDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. BST Min / Max / Floor / Ceiling Test ===");
        // Build Tree:
        //       50
        //     /    \
        //    30    70
        //   /  \
        //  20  40
        BSTMinMaxMaster.TreeNode root = new BSTMinMaxMaster.TreeNode(50);
        root.left = new BSTMinMaxMaster.TreeNode(30, 
            new BSTMinMaxMaster.TreeNode(20), new BSTMinMaxMaster.TreeNode(40));
        root.right = new BSTMinMaxMaster.TreeNode(70);

        System.out.println("Global Minimum: " + BSTMinMaxMaster.findMin(root).val); // Output: 20
        System.out.println("Global Maximum: " + BSTMinMaxMaster.findMax(root).val); // Output: 70

        System.out.println("Floor of 35:   " + BSTMinMaxMaster.findFloor(root, 35));   // Output: 30
        System.out.println("Ceiling of 35: " + BSTMinMaxMaster.findCeiling(root, 35)); // Output: 40 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Find Minimum** | **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|
| **Find Maximum** | **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|
| **Find Floor / Ceil**| **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Empty Tree (`root == null`)**: Returns `null` for all queries safely.
* **Key $X$ Smaller Than Global Minimum**: `findFloor` returns `null`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Full In-Order Traversal ($O(N)$ Penalty) to Find Minimum**:
  - Scanning the entire tree to find the minimum wastes $O(N)$ time.
  - **Follow leftmost links `while (curr.left != null)` for $O(H)$ time**.
* **Recording Floor Candidate When Moving Left**:
  - Moving left means `curr.val > X`. `curr.val` can NEVER be a floor because it is strictly greater than $X$!
  - **ONLY record floor candidates when `curr.val < X` and moving right**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Floor vs Ceiling Recording Directions:
> * **Floor($X$)**: We want the LARGEST key $\le X$. When `curr.val < X`, `curr.val` is smaller than $X$, so it is a candidate floor. We record `floor = curr.val` and move RIGHT to search for a larger candidate.
> * **Ceiling($X$)**: We want the SMALLEST key $\ge X$. When `curr.val > X`, `curr.val` is larger than $X$, so it is a candidate ceiling. We record `ceiling = curr.val` and move LEFT to search for a smaller candidate.

> **Memory Trick:** **"Floor: record when curr.val < X, move right! Ceiling: record when curr.val > X, move left!"**

---

## 13. System & Implementation Comparisons

| Feature | BST Min / Max Search | Unsorted Array Min / Max Search |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(H)$ Logarithmic ⚡** | $O(N)$ Full Array Scan |
| **Auxiliary Memory** | **$O(1)$ Strict Constant ⚡** | $O(1)$ Auxiliary Space |
| **Search Traversal**| Single Unidirectional Path | Linear Scan |

---

## 14. How to Recognize This in Questions
* **"Find maximum / minimum element in a Binary Search Tree"** $\rightarrow$ Follow rightmost / leftmost links.
* **"Find largest key in BST that is less than or equal to X"** $\rightarrow$ Floor in BST.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Floor of $X$ if $X$ exists in the BST?**  
  *A:* $X$ itself! (Since range definition is inclusive $\le X$).
* **Q: How does `findMin` execute in $O(1)$ space?**  
  *A:* By running a simple `while (curr.left != null) curr = curr.left;` loop without recursion call stacks.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST MIN, MAX, FLOOR & CEILING                         |
+-----------------------------------------------------------------------+
| • Minimum: Leftmost node (while curr.left != null curr = curr.left)   |
| • Maximum: Rightmost node (while curr.right != null curr = curr.right)|
| • Floor(X): If (curr.val < X) { floor = curr.val; curr = right; }     |
| • Ceil(X) : If (curr.val > X) { ceiling = curr.val; curr = left; }    |
| • Space Bounds: All 4 operations run in O(1) Auxiliary Space ⚡       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `findMin` and `findMax` in $O(1)$ space.
- [ ] I can write `findFloor` and `findCeiling` in $O(1)$ space.
- [ ] I know why Floor records candidate when moving right.
- [ ] I know why Ceiling records candidate when moving left.
- [ ] I can handle exact match cases `curr.val == X`.
