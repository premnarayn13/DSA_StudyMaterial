# 09. Tree Construction, Dual-Traversal Range Partitioning & HashMap Index Maps

## 1. Introduction
**Tree Construction** algorithms reconstruct a unique Binary Tree from 1D traversal sequences. While a single traversal sequence (e.g. Pre-Order alone) is ambiguous and maps to multiple valid tree shapes, combining **Pre-Order + In-Order (LeetCode 105)** or **In-Order + Post-Order (LeetCode 106)** unambiguously identifies the root node and partitions left and right subtrees. Using a **HashMap Index Map** to locate root indices in $O(1)$ time enables building unique binary trees in **$O(N)$ linear time and $O(N)$ auxiliary space**.

> **Important:** Why is an **In-Order Traversal** REQUIRED to uniquely reconstruct a Binary Tree?
> * **Pre-Order (`Root -> Left -> Right`)**: Identifies the **ROOT NODE** (it is ALWAYS the first element `preorder[preStart]`).
> * **Post-Order (`Left -> Right -> Root`)**: Identifies the **ROOT NODE** (it is ALWAYS the last element `postorder[postEnd]`).
> * **In-Order (`Left -> Root -> Right`)**: Identifies the **BOUNDARY DIVIDER**! All elements to the left of `inIndex` belong to the Left Subtree; all elements to the right belong to the Right Subtree! ⚡

```
Dual-Traversal Partition Topology (LeetCode 105):
Pre-Order Sequence : [ ROOT (3) ] | [ Left Subtree: 9 ] | [ Right Subtree: 20, 15, 7 ]
In-Order Sequence  : [ Left Subtree: 9 ] | [ ROOT (3) ] | [ Right Subtree: 15, 20, 7 ]
                                            ^ (inIndex found in O(1) via HashMap!)
Left Subtree Size = inIndex - inStart = 1 - 0 = 1! ⚡
```

---

## 2. Core Concepts & Preorder + Inorder Construction (LeetCode 105)

### 2.1 Algorithmic Strategy ($O(N)$ Time, $O(N)$ Auxiliary Space)
1. Build `Map<Integer, Integer> inMap` mapping `inorder[i] -> i` index for $O(1)$ lookup.
2. Define recursive builder function:
   `build(preStart, inStart, inEnd)`:
   - Base Case: If `preStart > preorder.length - 1` OR `inStart > inEnd`, return `null`.
   - Create `root = new TreeNode(preorder[preStart])`.
   - Find `inIndex = inMap.get(root.val)`.
   - Compute `leftTreeSize = inIndex - inStart`.
   - **Left Subtree Call**:
     `root.left = build(preStart + 1, inStart, inIndex - 1)`
   - **Right Subtree Call**:
     `root.right = build(preStart + leftTreeSize + 1, inIndex + 1, inEnd)`
   - Return `root`.

```
Range Boundary Math Rules (LeetCode 105):
- Next Pre-order index for Left Subtree  : preStart + 1
- Next Pre-order index for Right Subtree : preStart + leftTreeSize + 1
- Left Subtree In-order bounds          : [inStart ... inIndex - 1]
- Right Subtree In-order bounds         : [inIndex + 1 ... inEnd]
```

> **Memory Trick:** **"Preorder gives the ROOT; Inorder gives the SUBTREE BOUNDARY! Pre-index for right subtree is preStart + leftSize + 1!"**

---

## 3. Characteristics & Inorder + Postorder Construction (LeetCode 106)

### 3.1 Construct Tree from Inorder and Postorder (LeetCode 106)
In Post-Order + In-Order construction:
* **Root Node**: Found at the **END** of the post-order range: `postorder[postEnd]`.
* **Right Subtree Call**: Processed FIRST because post-order elements immediately preceding `postEnd` belong to the Right Subtree!
* **Range Formula**:
  - `rightTreeSize = inEnd - inIndex`.
  - `root.right = build(postEnd - 1, inIndex + 1, inEnd)`
  - `root.left = build(postEnd - rightTreeSize - 1, inStart, inIndex - 1)`

---

## 4. Internal Working Mechanics
Tracing Construct Tree from Preorder `[3, 9, 20, 15, 7]` and Inorder `[9, 3, 15, 20, 7]`:

```
Init: inMap = {9:0, 3:1, 15:2, 20:3, 7:4}

Call build(preStart=0, inStart=0, inEnd=4):
- rootVal = preorder[0] = 3. root = Node(3).
- inIndex = inMap.get(3) = 1.
- leftTreeSize = 1 - 0 = 1.

Left Call: build(preStart=1, inStart=0, inEnd=0):
  - rootVal = preorder[1] = 9. root.left = Node(9).
  - inIndex = 0. leftTreeSize = 0.
  - Subtree bounds empty -> returns Node(9).

Right Call: build(preStart = 0+1+1 = 2, inStart=2, inEnd=4):
  - rootVal = preorder[2] = 20. root.right = Node(20).
  - inIndex = 3. leftTreeSize = 3 - 2 = 1.
  - Left Call (preStart=3, inStart=2, inEnd=2) -> Node(15).
  - Right Call (preStart=4, inStart=4, inEnd=4) -> Node(7).

Tree reconstructed flawlessly in O(N) Time! ✅
```

---

## 5. Visual Diagram
Tree Construction Subtree Boundary Partition Topography:

```
Preorder:  [ 3 | 9 | 20 , 15 , 7 ]
             ^   ^   ^^^^^^^^^^^
           Root Left    Right

Inorder :  [ 9 | 3 | 15 , 20 , 7 ]
             ^   ^   ^^^^^^^^^^^
           Left Root    Right
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Tree Construction from Preorder + Inorder (LeetCode 105) and Inorder + Postorder (LeetCode 106):

```java
import java.util.*;

public class TreeConstructionMaster {

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

    // 1. Construct Binary Tree from Preorder and Inorder (LeetCode 105) O(N) Time, O(N) Space
    public static TreeNode buildTreePreIn(int[] preorder, int[] inorder) {
        if (preorder == null || inorder == null || preorder.length != inorder.length) return null;

        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }

        return buildPreInHelper(preorder, 0, 0, inorder.length - 1, inMap);
    }

    private static TreeNode buildPreInHelper(int[] preorder, int preStart, int inStart, int inEnd, Map<Integer, Integer> inMap) {
        if (preStart > preorder.length - 1 || inStart > inEnd) {
            return null;
        }

        int rootVal = preorder[preStart];
        TreeNode root = new TreeNode(rootVal);
        int inIndex = inMap.get(rootVal);
        int leftTreeSize = inIndex - inStart;

        // Recursively construct left and right subtrees
        root.left = buildPreInHelper(preorder, preStart + 1, inStart, inIndex - 1, inMap);
        root.right = buildPreInHelper(preorder, preStart + leftTreeSize + 1, inIndex + 1, inEnd, inMap);

        return root;
    }

    // 2. Construct Binary Tree from Inorder and Postorder (LeetCode 106) O(N) Time, O(N) Space
    public static TreeNode buildTreeInPost(int[] inorder, int[] postorder) {
        if (inorder == null || postorder == null || inorder.length != postorder.length) return null;

        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }

        return buildInPostHelper(postorder, postorder.length - 1, 0, inorder.length - 1, inMap);
    }

    private static TreeNode buildInPostHelper(int[] postorder, int postEnd, int inStart, int inEnd, Map<Integer, Integer> inMap) {
        if (postEnd < 0 || inStart > inEnd) {
            return null;
        }

        int rootVal = postorder[postEnd];
        TreeNode root = new TreeNode(rootVal);
        int inIndex = inMap.get(rootVal);
        int rightTreeSize = inEnd - inIndex;

        // Recursively construct right subtree FIRST (post-order processes right before root)
        root.right = buildInPostHelper(postorder, postEnd - 1, inIndex + 1, inEnd, inMap);
        root.left = buildInPostHelper(postorder, postEnd - rightTreeSize - 1, inStart, inIndex - 1, inMap);

        return root;
    }
}
```

> **Quick Syntax:**
```java
// Right Preorder Index Offsetting Line
root.right = buildPreInHelper(preorder, preStart + leftTreeSize + 1, inIndex + 1, inEnd, inMap);
```

---

## 7. Concrete Problem Examples
* **LeetCode 105 - Construct Binary Tree from Preorder and Inorder Traversal**: Primary dual-traversal tree construction.
* **LeetCode 106 - Construct Binary Tree from Inorder and Postorder Traversal**: End-root postorder partition.
* **LeetCode 889 - Construct Binary Tree from Preorder and Postorder Traversal**: Full binary tree construction.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `buildTreePreIn` and `buildTreeInPost`:

```java
public class TreeConstructionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Construct Tree from Preorder & Inorder (LeetCode 105) ===");
        int[] preorder = {3, 9, 20, 15, 7};
        int[] inorder  = {9, 3, 15, 20, 7};

        TreeConstructionMaster.TreeNode root = TreeConstructionMaster.buildTreePreIn(preorder, inorder);
        System.out.println("Reconstructed Root Val: " + root.val); // Output: 3
        System.out.println("Root Left Val:  " + root.left.val);     // Output: 9
        System.out.println("Root Right Val: " + root.right.val);    // Output: 20 ✅

        System.out.println("\n=== 2. Construct Tree from Inorder & Postorder (LeetCode 106) ===");
        int[] postorder = {9, 15, 7, 20, 3};
        TreeConstructionMaster.TreeNode root2 = TreeConstructionMaster.buildTreeInPost(inorder, postorder);
        System.out.println("Reconstructed Root 2 Val: " + root2.val); // Output: 3 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Optimization |
| :--- | :--- | :--- | :--- |
| **Naive Search in Inorder** | $O(N^2)$ Quadratic | $O(N)$ Stack Space | Scans inorder array linearly for root |
| **HashMap `inMap` Optimization**| **$O(N)$ Linear ⚡** | **$O(N)$ Map Space** | $O(1)$ root index lookup via `inMap.get()` |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Values in Tree**: Standard dual-traversal tree reconstruction algorithms ASSUME ALL NODE VALUES ARE UNIQUE. If duplicates exist, multiple tree topologies produce identical traversal arrays.
* **Single Node Tree**: `inStart == inEnd` returns a single leaf node correctly.

---

## 11. Common Mistakes & Anti-Patterns
* **Scanning In-Order Array Linearly for Root Index ($O(N^2)$ Time Penalty)**:
  - Performing a linear search `for (int i = inStart; i <= inEnd; i++)` to find `rootVal` inside the loop degrades time complexity to $O(N^2)$!
  - **Pre-populate a `Map<Integer, Integer> inMap` for $O(1)$ index lookup**.
* **Miscalculating `preStart` for Right Subtree**:
  - Writing `preStart + 1` for right subtree call causes the right child to pick a left subtree element!
  - **Always offset by left subtree size: `preStart + leftTreeSize + 1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Preorder + Postorder Alone CANNOT Uniquely Reconstruct Arbitrary Binary Trees:
> Without an In-Order traversal, Preorder (`[1, 2]`) and Postorder (`[2, 1]`) can represent EITHER:
> * Tree A: Root 1 with LEFT child 2.
> * Tree B: Root 1 with RIGHT child 2.
> Inorder traversal is REQUIRED to distinguish left vs right child assignments! (Unless the tree is guaranteed to be FULL!).

> **Memory Trick:** **"Inorder traversal is required to distinguish left vs right child subtrees!"**

---

## 13. System & Implementation Comparisons

| Feature | Preorder + Inorder (105) | Inorder + Postorder (106) |
| :--- | :--- | :--- |
| **Root Location** | First Element (`preStart`) | **Last Element (`postEnd`) ⚡** |
| **Subtree Size Count**| `leftTreeSize = inIndex - inStart` | `rightTreeSize = inEnd - inIndex` |
| **Recursion Order** | Left Subtree First | **Right Subtree First ⚡** |

---

## 14. How to Recognize This in Questions
* **"Reconstruct binary tree given preorder and inorder traversal arrays"** $\rightarrow$ LeetCode 105 (HashMap `inMap` + `leftTreeSize` offset).
* **"Reconstruct binary tree given inorder and postorder traversal arrays"** $\rightarrow$ LeetCode 106 (End root + `rightTreeSize` offset).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `buildTreePreIn` offset `preStart` by `leftTreeSize + 1` for the right child?**  
  *A:* Because Pre-Order traversal processes ALL nodes in the left subtree before starting the right subtree. Skipping `leftTreeSize` elements past `preStart + 1` locates the exact starting index of the right subtree in the preorder array.
* **Q: What is the time complexity if a HashMap is NOT used?**  
  *A:* Without a HashMap, finding the root index in the in-order array takes $O(N)$ linear time per node, yielding a total time complexity of $O(N^2)$ for skewed trees.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE CONSTRUCTION & PARTITIONING                       |
+-----------------------------------------------------------------------+
| • Preorder Rule : Root is at preStart (First element)                 |
| • Postorder Rule: Root is at postEnd (Last element)                   |
| • Inorder Rule  : Root index inMap divides Left and Right subtrees    |
| • Left Size     : leftTreeSize = inIndex - inStart                    |
| • Right Pre-Index: preStart + leftTreeSize + 1                        |
| • Optimization  : Use HashMap for O(1) inIndex lookups -> O(N) Time ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Construct Binary Tree from Preorder & Inorder (LeetCode 105) in $O(N)$ time.
- [ ] I can write Construct Binary Tree from Inorder & Postorder (LeetCode 106).
- [ ] I know why `inMap` HashMap optimization is required for $O(N)$ time.
- [ ] I can derive the right subtree preorder index offset `preStart + leftTreeSize + 1`.
- [ ] I know why Preorder + Postorder alone cannot uniquely reconstruct arbitrary trees.
