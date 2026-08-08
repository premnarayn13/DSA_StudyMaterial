# 12. Tree Symmetry, Subtree Matching & Isomorphism Architecture

## 1. Introduction
Validating structural symmetry and equivalence between binary trees—specifically **Symmetric Tree (LeetCode 101)**, **Same Tree (LeetCode 100)**, **Subtree of Another Tree (LeetCode 572)**, and **Flip Equivalent Binary Trees (LeetCode 951)**—are core structural matching problems in technical coding interviews. These problems evaluate multi-pointer recursive structural verification, mirror-image checking, and string hashing / serialization for fast subtree matching in **$O(N)$ linear time**.

> **Important:** Checking if a tree is **Symmetric** requires verifying if its left subtree and right subtree are **Mirror Images of Each Other**! Node $A$ and Node $B$ are mirror images if $A.\text{val} == B.\text{val}$, $A.\text{left}$ mirrors $B.\text{right}$, and $A.\text{right}$ mirrors $B.\text{left}$.

```
Tree Symmetry & Matching Spectrum:
+-----------------------------------------------------------------------------------+
| Same Tree (100)       : Structural Equality -> t1.val==t2.val && L==L && R==R    |
| Symmetric Tree (101)  : Mirror Equality     -> t1.val==t2.val && L==R && R==L ⚡  |
| Subtree Match (572)   : Tree Inclusion      -> sameTree(root, subRoot) || recurse |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Structural Equivalence Rules

### 2.1 Same Tree Verification (LeetCode 100)
Two binary trees `p` and `q` are identical if and only if:
1. Both `p` and `q` are `null` $\implies$ `true`.
2. One is `null` and the other is non-null $\implies$ `false`.
3. `p.val != q.val` $\implies$ `false`.
4. Recurse left and right: `isSameTree(p.left, q.left) && isSameTree(p.right, q.right)`.

### 2.2 Symmetric (Mirror) Tree Verification (LeetCode 101)
A tree is symmetric if its left and right subtrees are mirror images:
* `isSymmetric(root)` calls `isMirror(root.left, root.right)`.
* `isMirror(t1, t2)`:
  - Both `t1` and `t2` are `null` $\implies$ `true`.
  - One is `null`, other is non-null $\implies$ `false`.
  - `t1.val != t2.val` $\implies$ `false`.
  - Recurse mirror paths: **`isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left)`**!

### 2.3 Subtree of Another Tree Verification (LeetCode 572)
Given two binary trees `root` and `subRoot`:
* **Naive Recursive DFS ($O(N \cdot M)$ Time)**:
  - If `isSameTree(root, subRoot)` is true $\implies$ return `true`.
  - Else recurse: `isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot)`.
* **Optimal Tree Serialization + KMP ($O(N + M)$ Time)**:
  - Serialize `root` and `subRoot` into preorder strings with `null` markers (e.g. `",1,2,null,null..."`).
  - Search if `subRootString` is a substring of `rootString` using KMP or Rabin-Karp in **$O(N + M)$ linear time**!

```
Symmetry & Matching Verification Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Mirror Alignment  | Structural Match  | Optimal Time      |
+-----------------------+-------------------+-------------------+-------------------+
| Same Tree (100)       | Left-Left, Right-Right | Identical Nodes| O(N) Linear ⚡   |
| Symmetric Tree (101)  | Left-Right, Right-Left | Mirror Reflection| O(N) Linear ⚡   |
| Subtree Match (572)   | Subtree Search    | Inclusion Match   | O(N + M) KMP ⚡   |
| Flip Equivalent (951) | Swapped Children  | Isomorphic Flip   | O(N) Linear ⚡   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Same Tree checks (L1, L2) && (R1, R2)! Symmetric Tree checks (L1, R2) && (R1, L2)!"**

---

## 3. Characteristics & Iterative BFS Queue Mirror Checking

### 3.1 Iterative BFS Mirror Check Algorithm
To check symmetry iteratively without recursion call stack overhead:
* Enqueue `root.left` and `root.right` into an `ArrayDeque<TreeNode> queue`.
* While `!queue.isEmpty()`:
  - Poll two nodes: `t1 = queue.poll()` and `t2 = queue.poll()`.
  - If both `null` $\implies$ continue.
  - If one `null` or `t1.val != t2.val` $\implies$ return `false`!
  - Enqueue mirror pairs:
    - `queue.offer(t1.left); queue.offer(t2.right);`
    - `queue.offer(t1.right); queue.offer(t2.left);`

---

## 4. Internal Working Mechanics
Tracing Symmetric Tree (LeetCode 101) on `[1, 2, 2, 3, 4, 4, 3]`:

```
          ( 1 )
        /       \
      ( 2 )     ( 2 )
     /     \   /     \
   ( 3 )  ( 4 )( 4 ) ( 3 )

Call: isMirror(Node 2-Left, Node 2-Right)

Step 1: Check values: 2 == 2 (OK).
Step 2: Recurse Mirror Outer: isMirror(Node 3-Left, Node 3-Right) -> 3 == 3 (OK).
Step 3: Recurse Mirror Inner: isMirror(Node 4-Left, Node 4-Right) -> 4 == 4 (OK).

Result: IS SYMMETRIC! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Same Tree vs Symmetric Tree Mirror Alignment Topography:

```
[ SAME TREE (100) ALIGNMENT ]              [ SYMMETRIC TREE (101) MIRROR ALIGNMENT ]
     Tree 1        Tree 2                          Tree 1 Left        Tree 1 Right
      (1)           (1)                                (2)                 (2)
     /   \         /   \                              /   \               /   \
   (2)   (3)     (2)   (3)                          (3)   (4)           (4)   (3)
    |     |       |     |                            |     |             |     |
    +-----+       +-----+                            +-----+-------------+-----+
   (L1 == L2)    (R1 == R2)                         (L1 == R2)        (R1 == L2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Same Tree (LeetCode 100), Symmetric Tree (LeetCode 101 - Recursive & Iterative), Subtree of Another Tree (LeetCode 572 - DFS & KMP Serialization), and Flip Equivalent Binary Trees (LeetCode 951):

```java
import java.util.*;

public class TreeSymmetryMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Same Tree (LeetCode 100) O(N) Time, O(H) Space
    public static boolean isSameTree(TreeNode p, TreeNode q) {
        if (p == null && q == null) return true;
        if (p == null || q == null) return false;
        if (p.val != q.val) return false;

        return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
    }

    // 2. Symmetric Tree (LeetCode 101) O(N) Time, O(H) Space Recursive
    public static boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        return isMirror(root.left, root.right);
    }

    private static boolean isMirror(TreeNode t1, TreeNode t2) {
        if (t1 == null && t2 == null) return true;
        if (t1 == null || t2 == null) return false;
        if (t1.val != t2.val) return false;

        // Outer pair (t1.left, t2.right) AND Inner pair (t1.right, t2.left)
        return isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left);
    }

    // 3. Symmetric Tree Iterative BFS Queue (LeetCode 101) O(N) Time, O(W) Space
    public static boolean isSymmetricIterative(TreeNode root) {
        if (root == null) return true;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root.left);
        queue.offer(root.right);

        while (!queue.isEmpty()) {
            TreeNode t1 = queue.poll();
            TreeNode t2 = queue.poll();

            if (t1 == null && t2 == null) continue;
            if (t1 == null || t2 == null) return false;
            if (t1.val != t2.val) return false;

            // Enqueue mirror pairs
            queue.offer(t1.left);  queue.offer(t2.right);
            queue.offer(t1.right); queue.offer(t2.left);
        }

        return true;
    }

    // 4. Subtree of Another Tree (LeetCode 572) O(N * M) DFS / O(N + M) KMP
    public static boolean isSubtree(TreeNode root, TreeNode subRoot) {
        if (root == null) return false;
        if (isSameTree(root, subRoot)) return true;

        return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }

    // 5. Flip Equivalent Binary Trees (LeetCode 951) O(N) Time, O(H) Space
    public static boolean flipEquiv(TreeNode root1, TreeNode root2) {
        if (root1 == null && root2 == null) return true;
        if (root1 == null || root2 == null) return false;
        if (root1.val != root2.val) return false;

        // Option 1: Children not flipped (L1 == L2 && R1 == R2)
        boolean noFlip = flipEquiv(root1.left, root2.left) && flipEquiv(root1.right, root2.right);
        // Option 2: Children flipped (L1 == R2 && R1 == L2)
        boolean flip = flipEquiv(root1.left, root2.right) && flipEquiv(root1.right, root2.left);

        return noFlip || flip;
    }
}
```

> **Quick Syntax:**
```java
// Symmetric Mirror Pairs Enqueue
queue.offer(t1.left);  queue.offer(t2.right);
queue.offer(t1.right); queue.offer(t2.left);
```

---

## 7. Concrete Problem Examples
* **LeetCode 100 - Same Tree**: Direct structural equivalence DFS.
* **LeetCode 101 - Symmetric Tree**: Mirror reflection DFS/BFS.
* **LeetCode 572 - Subtree of Another Tree**: Subtree inclusion DFS / KMP serialization.
* **LeetCode 951 - Flip Equivalent Binary Trees**: Isomorphic flip matching.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Same Tree, Symmetric Tree (DFS & BFS), and Subtree Matching:

```java
public class TreeSymmetryDemo {

    public static void main(String[] args) {
        // Build Symmetric Tree: [1, 2, 2, 3, 4, 4, 3]
        TreeSymmetryMaster.TreeNode root = new TreeSymmetryMaster.TreeNode(1);
        root.left = new TreeSymmetryMaster.TreeNode(2);
        root.right = new TreeSymmetryMaster.TreeNode(2);
        root.left.left = new TreeSymmetryMaster.TreeNode(3);
        root.left.right = new TreeSymmetryMaster.TreeNode(4);
        root.right.left = new TreeSymmetryMaster.TreeNode(4);
        root.right.right = new TreeSymmetryMaster.TreeNode(3);

        System.out.println("=== 1. Symmetric Tree Check (LeetCode 101) ===");
        System.out.println("Recursive Is Symmetric? " + TreeSymmetryMaster.isSymmetric(root)); // true
        System.out.println("Iterative Is Symmetric? " + TreeSymmetryMaster.isSymmetricIterative(root)); // true

        System.out.println("\n=== 2. Subtree Matching (LeetCode 572) ===");
        TreeSymmetryMaster.TreeNode subRoot = new TreeSymmetryMaster.TreeNode(2);
        subRoot.left = new TreeSymmetryMaster.TreeNode(3);
        subRoot.right = new TreeSymmetryMaster.TreeNode(4);

        System.out.println("Is Subtree Present? " + TreeSymmetryMaster.isSubtree(root, subRoot)); // true
    }
}
```

---

## 9. Complexity Analysis

| Problem Pattern | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Same Tree (100)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Left-Left & Right-Right DFS |
| **Symmetric Tree (101)**| **$O(N)$ Linear ⚡** | $O(H)$ / $O(W)$ | Left-Right & Right-Left Mirror DFS/BFS |
| **Subtree Match DFS (572)**| $O(N \cdot M)$ Quadratic | $O(H)$ Call Stack | `isSameTree` call at every node |
| **Subtree Match KMP (572)**| **$O(N + M)$ Linear ⚡**| $O(N + M)$ String | Preorder String Serialization + KMP |

---

## 10. Edge Cases & Boundary Handling
* **Both Null Trees**: `p == null && q == null` returns `true`.
* **One Null, One Non-Null**: `p == null || q == null` returns `false`.
* **Single Node Tree**: Always symmetric.

---

## 11. Common Mistakes & Anti-Patterns
* **Writing `isMirror(t1.left, t2.left)` for Symmetry**:
  - Checking left with left checks SAMENESS, not MIRROR SYMMETRY!
  - **Fix**: Check `isMirror(t1.left, t2.right)` and `isMirror(t1.right, t2.left)`.
* **Omitting Null Marker Delimiters in Subtree Serialization**: Serializing without `null` markers leads to false substring matches between different tree structures!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Same Tree vs Symmetric Tree Alignment Rules:
> * **Same Tree (100)**: Pair `(p.left, q.left)` and `(p.right, q.right)`.
> * **Symmetric Tree (101)**: Pair `(t1.left, t2.right)` and `(t1.right, t2.left)`.
> * **Flip Equivalent (951)**: Check BOTH `(noFlip)` OR `(flip)`.

> **Memory Trick:** **"Same Tree aligns same sides (L1-L2, R1-R2)! Symmetric Tree aligns opposite sides (L1-R2, R1-L2)!"**

---

## 13. System & Implementation Comparisons

| Feature | Same Tree (100) | Symmetric Tree (101) | Flip Equivalent (951) |
| :--- | :--- | :--- | :--- |
| **Input Trees** | Two Trees ($P$ and $Q$) | One Tree (Left vs Right) | Two Trees ($R_1$ and $R_2$) |
| **Path Alignment** | Single Path | Mirror Path | Normal OR Flipped Path |
| **Time Complexity** | $O(N)$ | $O(N)$ | $O(N)$ |

---

## 14. How to Recognize This in Questions
* **"Check if a binary tree is a mirror image of itself"** $\rightarrow$ LeetCode 101 (`isMirror(t1.left, t2.right)`).
* **"Check if subRoot is a subtree of root"** $\rightarrow$ LeetCode 572 (`isSameTree` DFS or KMP Serialization).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Subtree of Another Tree (LeetCode 572) take $O(N \cdot M)$ time with naive DFS?**  
  *A:* Because for each of the $N$ nodes in `root`, we call `isSameTree`, which compares up to $M$ nodes in `subRoot`. Worst-case time is $O(N \cdot M)$.
* **Q: How to achieve $O(N + M)$ linear time for LeetCode 572?**  
  *A:* Serialize `root` and `subRoot` into preorder traversal strings with unique `null` markers (e.g. `",#1,#2,#null,#null"`). Then use the KMP string matching algorithm to check if `subRoot`'s string is a substring of `root`'s string in $O(N + M)$ time.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE SYMMETRY & SUBTREE MATCHING                      |
+-----------------------------------------------------------------------+
| • Same Tree (100): isSameTree(p.left, q.left) && isSameTree(p.right, q.right)|
| • Symmetric Tree (101): isMirror(t1.left, t2.right) && isMirror(t1.right, t2.left)|
| • Subtree Match (572): isSameTree(root, sub) || isSubtree(r.left, sub) || isSubtree(r.right, sub)|
| • Flip Equivalent (951): (noFlip) || (flip)                           |
| • Iterative Symmetry BFS: Enqueue mirror pairs (t1.left, t2.right) & (t1.right, t2.left)|
| • Complexity: Same/Symmetric run in O(N) Linear Time                  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `isSameTree` (LeetCode 100) in under 2 minutes.
- [ ] I can write recursive and iterative `isSymmetric` (LeetCode 101).
- [ ] I know why `isMirror` pairs `t1.left` with `t2.right`.
- [ ] I can write `isSubtree` (LeetCode 572).
- [ ] I can write Flip Equivalent Binary Trees (LeetCode 951).
- [ ] I know how to optimize LeetCode 572 to $O(N + M)$ using KMP serialization.
