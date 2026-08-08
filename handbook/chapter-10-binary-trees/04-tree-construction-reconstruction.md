# 04. Binary Tree Construction, Reconstruction & Serialization Architecture

## 1. Introduction
Reconstructing a Binary Tree from traversal sequences (LeetCode 105 - Preorder & Inorder, LeetCode 106 - Inorder & Postorder) and Serializing/Deserializing a Binary Tree (LeetCode 297) are high-frequency technical coding interview problems. These problems evaluate recursive divide-and-conquer problem decomposition, index boundary mapping, Hash Map lookup acceleration, and string encoding mechanics to reconstruct identical binary trees in **$O(N)$ linear time**.

> **Important:** Constructing a unique Binary Tree CANNOT be done with Preorder or Postorder traversal alone! A unique general Binary Tree REQUIRES the **Inorder Traversal** to partition elements into left and right subtrees! (Exception: Full Binary Trees can be reconstructed from Preorder & Postorder alone).

```
Reconstruction Requirements Spectrum:
+-----------------------------------------------------------------------------------+
| Preorder + Inorder    : Uniquely reconstructs ANY Binary Tree -> O(N) Time ⚡      |
| Postorder + Inorder   : Uniquely reconstructs ANY Binary Tree -> O(N) Time ⚡      |
| Preorder + Postorder  : Uniquely reconstructs ONLY FULL Binary Trees -> O(N) Time |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Partitioning

### 2.1 The Inorder Partition Invariant
* **Preorder Sequence (`[Root, Left Subtree, Right Subtree]`)**: First element `preorder[preStart]` is ALWAYS the root of the current subtree.
* **Inorder Sequence (`[Left Subtree, Root, Right Subtree]`)**: Locating `root.val` at index `inIndex` in the Inorder array partitions the tree into:
  - **Left Subtree**: `inorder[inStart ... inIndex - 1]`
  - **Right Subtree**: `inorder[inIndex + 1 ... inEnd]`

### 2.2 Hash Map Index Accelerator ($O(N)$ vs $O(N^2)$ Time)
If we scan the Inorder array linearly to find `root.val` on every recursive call, each search takes $O(N)$ time, causing overall tree reconstruction to take $O(N^2)$ time!
By building an **Inorder Value-to-Index Hash Map (`inMap.put(inorder[i], i)`)** in $O(N)$ time before starting recursion, looking up `inIndex` takes **$O(1)$ constant time**, optimizing total reconstruction to **$O(N)$ linear time**!

### 2.3 Index Boundaries Mapping (Preorder + Inorder)
For subtree with `preorder` range `[preStart, preEnd]` and `inorder` range `[inStart, inEnd]`:
* `rootVal = preorder[preStart]`
* `inIndex = inMap.get(rootVal)`
* `leftSubtreeSize = inIndex - inStart`
* **Left Subtree Bounds**:
  - `preorder`: `[preStart + 1, preStart + leftSubtreeSize]`
  - `inorder`: `[inStart, inIndex - 1]`
* **Right Subtree Bounds**:
  - `preorder`: `[preStart + leftSubtreeSize + 1, preEnd]`
  - `inorder`: `[inIndex + 1, inEnd]`

```
Subtree Index Calculation:
preorder: [ Root | <---- Left Subtree ----> | <---- Right Subtree ----> ]
          preStart  preStart+1   preStart+L  preStart+L+1         preEnd

inorder : [ <---- Left Subtree ----> | Root | <---- Right Subtree ----> ]
          inStart         inIndex-1  inIndex inIndex+1           inEnd
```

> **Memory Trick:** **"Inorder splits left and right subtrees! Hash Map inMap.put(inorder[i], i) makes root lookup O(1)!"**

---

## 3. Characteristics & Tree Serialization (LeetCode 297)

### 3.1 Binary Tree Serialization / Deserialization Protocol
* **Serialization**: Convert a binary tree structure into a flat string representation.
  - Standard Format: Preorder traversal encoding `null` pointers as `"null"` separated by commas `","` (e.g. `"1,2,null,null,3,4,null,null,5,null,null"`).
* **Deserialization**: Reconstruct the exact tree from the serialized string.
  - Split string by `","` into a `Queue<String>`.
  - Recursively poll from queue: If token is `"null"`, return `null`. Else create `new TreeNode(Integer.parseInt(token))` and recursively assign `.left` and `.right`!

```
Preorder Serialization Flow:
Tree:     (1)                  Serialized String:
         /   \                 "1,2,null,null,3,4,null,null,5,null,null"
       (2)   (3)
            /   \
          (4)   (5)
```

---

## 4. Internal Working Mechanics
Tracing Preorder `[3, 9, 20, 15, 7]` and Inorder `[9, 3, 15, 20, 7]` Tree Reconstruction:

```
Init: inMap = {9:0, 3:1, 15:2, 20:3, 7:4}

Root 1: preStart = 0 -> Root Val = 3.
        inIndex = inMap.get(3) = 1.
        leftSize = inIndex - inStart = 1 - 0 = 1.

Left Child Recursion (Root 3):
  preRange = [1, 1], inRange = [0, 0] -> Root Val = 9.
  inIndex = inMap.get(9) = 0. leftSize = 0 - 0 = 0.
  Left & Right bounds invalid -> Returns TreeNode(9).

Right Child Recursion (Root 3):
  preRange = [2, 4], inRange = [2, 4] -> Root Val = 20.
  inIndex = inMap.get(20) = 3. leftSize = 3 - 2 = 1.
  - Left Child: preRange [2, 2], inRange [2, 2] -> TreeNode(15).
  - Right Child: preRange [4, 4], inRange [4, 4] -> TreeNode(7).

Resulting Tree: [3, 9, 20, null, null, 15, 7] ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Subtree Range Partitioning Invariant:

```
Preorder Array:  [  3  |  9  |  20,  15,  7  ]
                   ^      ^       ^
                  Root   Left   Right Subtree

Inorder Array :  [  9  |  3  |  15,  20,  7  ]
                   ^      ^       ^
                 Left   Root    Right Subtree
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Preorder+Inorder (LeetCode 105), Inorder+Postorder (LeetCode 106), and Preorder Serialization/Deserialization (LeetCode 297):

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
    }

    // 1. Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105) O(N) Time, O(N) Space
    public static TreeNode buildTreePreIn(int[] preorder, int[] inorder) {
        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }

        return buildPreInHelper(preorder, 0, preorder.length - 1, 
                                inorder, 0, inorder.length - 1, inMap);
    }

    private static TreeNode buildPreInHelper(int[] preorder, int preStart, int preEnd,
                                             int[] inorder, int inStart, int inEnd,
                                             Map<Integer, Integer> inMap) {
        if (preStart > preEnd || inStart > inEnd) return null;

        int rootVal = preorder[preStart];
        TreeNode root = new TreeNode(rootVal);

        int inIndex = inMap.get(rootVal);
        int leftSubtreeSize = inIndex - inStart;

        root.left = buildPreInHelper(preorder, preStart + 1, preStart + leftSubtreeSize,
                                     inorder, inStart, inIndex - 1, inMap);

        root.right = buildPreInHelper(preorder, preStart + leftSubtreeSize + 1, preEnd,
                                      inorder, inIndex + 1, inEnd, inMap);

        return root;
    }

    // 2. Construct Binary Tree from Inorder and Postorder Traversal (LeetCode 106) O(N) Time, O(N) Space
    public static TreeNode buildTreeInPost(int[] inorder, int[] postorder) {
        Map<Integer, Integer> inMap = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) {
            inMap.put(inorder[i], i);
        }

        return buildInPostHelper(inorder, 0, inorder.length - 1,
                                 postorder, 0, postorder.length - 1, inMap);
    }

    private static TreeNode buildInPostHelper(int[] inorder, int inStart, int inEnd,
                                              int[] postorder, int postStart, int postEnd,
                                              Map<Integer, Integer> inMap) {
        if (inStart > inEnd || postStart > postEnd) return null;

        int rootVal = postorder[postEnd]; // Last element of postorder is Root!
        TreeNode root = new TreeNode(rootVal);

        int inIndex = inMap.get(rootVal);
        int leftSubtreeSize = inIndex - inStart;

        root.left = buildInPostHelper(inorder, inStart, inIndex - 1,
                                      postorder, postStart, postStart + leftSubtreeSize - 1, inMap);

        root.right = buildInPostHelper(inorder, inIndex + 1, inEnd,
                                       postorder, postStart + leftSubtreeSize, postEnd - 1, inMap);

        return root;
    }

    // 3. Serialize and Deserialize Binary Tree (LeetCode 297) O(N) Time, O(N) Space
    public static class Codec {

        // Encodes a tree to a single string.
        public String serialize(TreeNode root) {
            StringBuilder sb = new StringBuilder();
            serializeHelper(root, sb);
            return sb.toString();
        }

        private void serializeHelper(TreeNode node, StringBuilder sb) {
            if (node == null) {
                sb.append("null," );
                return;
            }

            sb.append(node.val).append("," );
            serializeHelper(node.left, sb);
            serializeHelper(node.right, sb);
        }

        // Decodes your encoded data to tree.
        public TreeNode deserialize(String data) {
            String[] tokens = data.split("," );
            Queue<String> queue = new ArrayDeque<>(Arrays.asList(tokens));
            return deserializeHelper(queue);
        }

        private TreeNode deserializeHelper(Queue<String> queue) {
            String valStr = queue.poll();
            if (valStr.equals("null" )) {
                return null;
            }

            TreeNode node = new TreeNode(Integer.parseInt(valStr));
            node.left = deserializeHelper(queue);
            node.right = deserializeHelper(queue);
            return node;
        }
    }
}
```

> **Quick Syntax:**
```java
// Preorder Serialization Recursive Helper
if (node == null) { sb.append("null,"); return; }
sb.append(node.val).append(",");
serialize(node.left, sb);
serialize(node.right, sb);
```

---

## 7. Concrete Problem Examples
* **LeetCode 105 - Construct Binary Tree from Preorder and Inorder**: $O(N)$ reconstruction with Hash Map.
* **LeetCode 106 - Construct Binary Tree from Inorder and Postorder**: $O(N)$ postorder root extraction.
* **LeetCode 297 - Serialize and Deserialize Binary Tree**: Preorder string codec.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing tree reconstruction and serialization codec:

```java
public class TreeConstructionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Reconstructing Tree from Preorder & Inorder ===");
        int[] preorder = {3, 9, 20, 15, 7};
        int[] inorder  = {9, 3, 15, 20, 7};

        TreeConstructionMaster.TreeNode root = 
            TreeConstructionMaster.buildTreePreIn(preorder, inorder);

        System.out.println("Reconstructed Root Val: " + root.val);
        System.out.println("Left Child:  " + root.left.val);
        System.out.println("Right Child: " + root.right.val);

        System.out.println("\n=== 2. Testing Serialization / Deserialization Codec ===");
        TreeConstructionMaster.Codec codec = new TreeConstructionMaster.Codec();
        String serialized = codec.serialize(root);
        System.out.println("Serialized String: " + serialized);

        TreeConstructionMaster.TreeNode deserializedRoot = codec.deserialize(serialized);
        System.out.println("Deserialized Root Val: " + deserializedRoot.val);
    }
}
```

---

## 9. Complexity Analysis

| Construction Problem | Time Complexity | Auxiliary Space | Key Optimization |
| :--- | :--- | :--- | :--- |
| **Pre + In (Linear Map)** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Inorder index lookup in $O(1)$ time |
| **Pre + In (Naive Scan)** | $O(N^2)$ Quadratic | $O(H)$ Stack Space | $O(N)$ linear scan per node |
| **Codec (297)** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Preorder string split queue |

---

## 10. Edge Cases & Boundary Handling
* **Empty Input Arrays**: Return `null` immediately.
* **Single Node Array**: Return `new TreeNode(preorder[0])`.
* **Duplicates in Traversal Arrays**: Standard tree reconstruction algorithms assume **unique node values**. If values are not unique, multiple valid binary trees exist!

---

## 11. Common Mistakes & Anti-Patterns
* **Performing Linear Searches for Inorder Index**: Scanning the `inorder` array linearly on every recursive step causes $O(N^2)$ time slowdown! Always pre-build `inMap = new HashMap<>()`.
* **Incorrect Subtree Index Offset Calculation**: Confusing `preStart + leftSubtreeSize` boundary offsets. Always calculate `leftSubtreeSize = inIndex - inStart`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `inMap` Pre-processing is Mandatory:
> Pre-building `inMap` maps `nodeValue -> inorderIndex` in $O(N)$ time initially.
> This turns the inorder split lookup into an **$O(1)$ constant time query**, ensuring the overall divide-and-conquer recursion takes **$O(N)$ linear time**!

> **Memory Trick:** **"Calculate leftSubtreeSize = inIndex - inStart to compute exact preorder boundary offsets!"**

---

## 13. System & Implementation Comparisons

| Feature | Preorder + Inorder | Postorder + Inorder | Preorder + Postorder |
| :--- | :--- | :--- | :--- |
| **Root Location** | First element `pre[0]` | Last element `post[N-1]` | First element `pre[0]` |
| **Tree Unique Guarantee**| **ANY Binary Tree ⚡** | **ANY Binary Tree ⚡** | **FULL Binary Trees ONLY** |
| **Map Helper Required** | `inorder` Index Map | `inorder` Index Map | `postorder` Index Map |

---

## 14. How to Recognize This in Questions
* **"Reconstruct a binary tree given preorder and inorder traversal arrays"** $\rightarrow$ LeetCode 105 ($O(N)$ divide and conquer with `inMap`).
* **"Serialize a binary tree into a string and deserialize it back"** $\rightarrow$ LeetCode 297 (Preorder string recursion with `null` markers).

---

## 15. Frequently Asked Interview Questions
* **Q: Why cannot a unique binary tree be reconstructed from Preorder and Postorder traversals alone?**  
  *A:* Because without Inorder traversal, we cannot determine whether a single child node belongs to the left subtree or the right subtree. For example, tree `1 -> left 2` and tree `1 -> right 2` produce the exact same Preorder `[1, 2]` and Postorder `[2, 1]` traversals!
* **Q: How does `leftSubtreeSize = inIndex - inStart` simplify boundary offset calculations?**  
  *A:* Since the number of nodes in the left subtree is identical in both Preorder and Inorder arrays, adding `leftSubtreeSize` to `preStart` gives the exact end index of the left subtree in the Preorder array (`preStart + leftSubtreeSize`).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE CONSTRUCTION & SERIALIZATION                     |
+-----------------------------------------------------------------------+
| • Inorder Invariant: Splitting inorder at inIndex yields left & right |
| • Hash Map Accelerator: Pre-build inMap in O(N) for O(1) root lookup  |
| • Subtree Size Formula: leftSubtreeSize = inIndex - inStart           |
| • Preorder Bounds: Left [preStart+1, preStart+L], Right [preStart+L+1, preEnd]|
| • Pre+Post Limitation: Reconstructs ONLY Full Binary Trees uniquely   |
| • Serialization: Preorder "1,2,null,null,3" string split into Queue   |
| • Complexity: O(N) Linear Time | O(N) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `inMap` pre-processing for $O(N)$ tree reconstruction.
- [ ] I can derive `leftSubtreeSize = inIndex - inStart`.
- [ ] I can write LeetCode 105 (Pre + In) in under 5 minutes.
- [ ] I can write LeetCode 106 (In + Post).
- [ ] I can write Preorder Tree Serialization/Deserialization Codec (LeetCode 297).
- [ ] I know why general trees cannot be reconstructed from Pre+Post alone.
