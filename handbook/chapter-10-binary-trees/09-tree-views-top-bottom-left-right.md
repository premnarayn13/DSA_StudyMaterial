# 09. Binary Tree Views: Left, Right, Top, Bottom & Boundary Traversals

## 1. Introduction
Constructing visual projections of a Binary Tree—specifically **Left View**, **Right View (LeetCode 199)**, **Top View**, **Bottom View**, and **Boundary Traversal (LeetCode 545)**—are high-frequency technical coding interview problems. These problems evaluate 2D coordinate projections, level-order BFS vs pre-order DFS level tracking, and boundary edge collection without duplicate leaf visits.

> **Important:** While Left and Right Views track nodes level by level (horizontal levels), Top and Bottom Views project nodes vertically onto column lines ($X$-coordinates) using BFS to preserve top-down or bottom-up visibility!

```
Tree View Projections Spectrum:
+-----------------------------------------------------------------------------------+
| Left / Right Views  : Horizontal Projection per Depth Level D -> Track Level First/Last|
| Top / Bottom Views  : Vertical Projection per Column Line X    -> Track Col First/Last|
| Boundary Traversal  : Anti-Clockwise Shell -> Root + Left Edge + Leaves + Right Edge|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Left and Right Views (Depth Level Projection)
* **Left View**: The set of nodes visible when looking at the tree from the LEFT side (first node at each level).
  - *BFS Strategy*: In the queue level snapshot loop `for (int i = 0; i < levelSize; i++)`, collect node when `i == 0`.
  - *DFS Strategy*: Pre-Order (Root $\to$ Left $\to$ Right) with depth tracking. Collect node when `depth == result.size()`.
* **Right View (LeetCode 199)**: The set of nodes visible when looking at the tree from the RIGHT side (last node at each level).
  - *BFS Strategy*: Collect node when `i == levelSize - 1`.
  - *DFS Strategy*: Modified Pre-Order (Root $\to$ Right $\to$ Left). Collect node when `depth == result.size()`.

### 2.2 Top and Bottom Views (Column $X$-Coordinate Projection)
Assign column coordinate $X = 0$ to root. Left child is $X - 1$, Right child is $X + 1$.
* **Top View**: First node encountered at each column $X$ during level-order BFS traversal.
  - Use BFS with `TreeMap<Integer, Integer> colMap` (Column $\to$ Node Value).
  - ONLY insert into `colMap` if column $X$ is NOT present (`colMap.putIfAbsent(col, val)`).
* **Bottom View**: Last node encountered at each column $X$ during level-order BFS traversal.
  - Use BFS with `TreeMap<Integer, Integer> colMap`.
  - OVERWRITE `colMap` at every visit (`colMap.put(col, val)`).

### 2.3 Boundary Traversal (LeetCode 545)
Traverse the anti-clockwise outer boundary in 4 distinct steps:
1. **Root Node**: Add `root.val` if not a leaf.
2. **Left Boundary (Excluding Leaves)**: Move down left branch (prefer `left`, else `right`).
3. **All Leaf Nodes**: Collect all leaves in left-to-right order using Pre-Order DFS.
4. **Right Boundary (Excluding Leaves)**: Move down right branch (prefer `right`, else `left`), collect nodes, and **REVERSE** before appending!

```
Tree Views Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| View Type             | Coordinate Focus  | Traversal Method  | Storage Key Rule  |
+-----------------------+-------------------+-------------------+-------------------+
| Left View             | Level Depth D     | BFS / DFS (N-L-R) | First at Level D  |
| Right View (199)      | Level Depth D     | BFS / DFS (N-R-L) | Last at Level D   |
| Top View              | Column Line X     | Level-Order BFS   | `putIfAbsent(X)`  |
| Bottom View           | Column Line X     | Level-Order BFS   | `put(X)` Overwrite|
| Boundary (545)        | Outer Perimeter   | 4-Stage DFS       | Anti-Clockwise Shell|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Top View = putIfAbsent(col)! Bottom View = put(col) Overwrite! Boundary = Left Edge + Leaves + Reversed Right Edge!"**

---

## 3. Characteristics & Boundary Traversal Protocols

### 3.1 Eliminating Duplicate Leaf Visits in Boundary Traversal
A common bug in Boundary Traversal is adding the left-most leaf twice (once during Left Boundary collection, and once during Leaf Collection).
* **Rule**: Left Boundary and Right Boundary collection functions MUST explicitly skip leaf nodes (`if (!isLeaf(node)) result.add(node.val)`).
* Leaf nodes are collected EXCLUSIVELY during Step 3 (Leaf Collection).

---

## 4. Internal Working Mechanics
Tracing Top View & Bottom View on `[1, 2, 3, 4, 5, 6, 7]`:

```
                 Col -1      Col 0      Col +1
                   |           |           |
                 ( 2 )       ( 1 )       ( 3 )
                /     \     /     \     /     \
             ( 4 )   ( 5 ) ( 6 )   ( 7 )
             Col -2  Col 0  Col 0  Col +2

BFS Queue Processing:
- Node 1 (col 0)  : TopMap = {0: 1}, BottomMap = {0: 1}
- Node 2 (col -1) : TopMap = {0: 1, -1: 2}, BottomMap = {0: 1, -1: 2}
- Node 3 (col +1) : TopMap = {0: 1, -1: 2, 1: 3}, BottomMap = {0: 1, -1: 2, 1: 3}
- Node 4 (col -2) : TopMap = {-2: 4, -1: 2, 0: 1, 1: 3}, BottomMap = {-2: 4, -1: 2, 0: 1, 1: 3}
- Node 5 (col 0)  : TopMap unchanged. BottomMap[0] overwritten with 5!
- Node 6 (col 0)  : TopMap unchanged. BottomMap[0] overwritten with 6!
- Node 7 (col +2) : TopMap = {-2:4, -1:2, 0:1, 1:3, 2:7}, BottomMap = {-2:4, -1:2, 0:6, 1:3, 2:7}

Top View Result   : [4, 2, 1, 3, 7] ✅
Bottom View Result: [4, 2, 6, 3, 7] ✅
```

---

## 5. Visual Diagram
Boundary Traversal Anti-Clockwise 4-Stage Shell Topology:

```
                  ( 1 )   <--- Step 1: Root Node
                 /     \
   Step 2:     ( 2 )   ( 3 )   <--- Step 4: Right Boundary
  Left Edge   /     \       \         (Collected & REVERSED!)
            ( 4 )   ( 5 )   ( 6 )
             ^        ^       ^
             |        |       |
             +--------+-------+  <--- Step 3: All Leaf Nodes (Left-to-Right)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Left View, Right View (LeetCode 199), Top View, Bottom View, and Boundary Traversal (LeetCode 545):

```java
import java.util.*;

public class TreeViewsMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Left View of Binary Tree O(N) Time, O(W) Space (BFS)
    public static List<Integer> leftSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                if (i == 0) { // First node in level loop
                    result.add(curr.val);
                }
                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }
        }
        return result;
    }

    // 2. Right View of Binary Tree (LeetCode 199) O(N) Time, O(W) Space (BFS)
    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                if (i == levelSize - 1) { // Last node in level loop
                    result.add(curr.val);
                }
                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }
        }
        return result;
    }

    // 3. Top View of Binary Tree O(N log N) Time, O(N) Space
    static class ColNode {
        TreeNode node;
        int col;
        ColNode(TreeNode node, int col) { this.node = node; this.col = col; }
    }

    public static List<Integer> topView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Map<Integer, Integer> topMap = new TreeMap<>(); // Sorted by column
        Queue<ColNode> queue = new ArrayDeque<>();
        queue.offer(new ColNode(root, 0));

        while (!queue.isEmpty()) {
            ColNode curr = queue.poll();
            // ONLY put if column is absent (First node seen at column X!)
            topMap.putIfAbsent(curr.col, curr.node.val);

            if (curr.node.left != null)  queue.offer(new ColNode(curr.node.left, curr.col - 1));
            if (curr.node.right != null) queue.offer(new ColNode(curr.node.right, curr.col + 1));
        }

        result.addAll(topMap.values());
        return result;
    }

    // 4. Bottom View of Binary Tree O(N log N) Time, O(N) Space
    public static List<Integer> bottomView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Map<Integer, Integer> bottomMap = new TreeMap<>();
        Queue<ColNode> queue = new ArrayDeque<>();
        queue.offer(new ColNode(root, 0));

        while (!queue.isEmpty()) {
            ColNode curr = queue.poll();
            // ALWAYS overwrite column entry (Last node seen at column X!)
            bottomMap.put(curr.col, curr.node.val);

            if (curr.node.left != null)  queue.offer(new ColNode(curr.node.left, curr.col - 1));
            if (curr.node.right != null) queue.offer(new ColNode(curr.node.right, curr.col + 1));
        }

        result.addAll(bottomMap.values());
        return result;
    }

    // 5. Boundary Traversal of Binary Tree (LeetCode 545) O(N) Time, O(H) Space
    public static List<Integer> boundaryTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        if (!isLeaf(root)) result.add(root.val); // Step 1: Root

        addLeftBoundary(root.left, result);       // Step 2: Left Boundary
        addLeaves(root, result);                  // Step 3: All Leaves
        addRightBoundary(root.right, result);     // Step 4: Right Boundary (Reversed)

        return result;
    }

    private static boolean isLeaf(TreeNode node) {
        return node != null && node.left == null && node.right == null;
    }

    private static void addLeftBoundary(TreeNode node, List<Integer> result) {
        TreeNode curr = node;
        while (curr != null) {
            if (!isLeaf(curr)) result.add(curr.val);
            curr = (curr.left != null) ? curr.left : curr.right;
        }
    }

    private static void addLeaves(TreeNode node, List<Integer> result) {
        if (node == null) return;
        if (isLeaf(node)) {
            result.add(node.val);
            return;
        }
        addLeaves(node.left, result);
        addLeaves(node.right, result);
    }

    private static void addRightBoundary(TreeNode node, List<Integer> result) {
        TreeNode curr = node;
        List<Integer> temp = new ArrayList<>();
        while (curr != null) {
            if (!isLeaf(curr)) temp.add(curr.val);
            curr = (curr.right != null) ? curr.right : curr.left;
        }
        // Reverse right boundary before adding to result
        for (int i = temp.size() - 1; i >= 0; i--) {
            result.add(temp.get(i));
        }
    }
}
```

> **Quick Syntax:**
```java
// Boundary Right Edge Reversal
List<Integer> temp = new ArrayList<>();
while (curr != null) {
    if (!isLeaf(curr)) temp.add(curr.val);
    curr = (curr.right != null) ? curr.right : curr.left;
}
for (int i = temp.size() - 1; i >= 0; i--) result.add(temp.get(i));
```

---

## 7. Concrete Problem Examples
* **LeetCode 199 - Binary Tree Right Side View**: Level snapshot last element.
* **LeetCode 545 - Boundary of Binary Tree**: 4-Stage anti-clockwise boundary traversal.
* **Top & Bottom View Algorithms**: Vertical column coordinate BFS projections.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Left View, Right View, Top View, Bottom View, and Boundary Traversals:

```java
public class TreeViewsDemo {

    public static void main(String[] args) {
        // Build Tree: [1, 2, 3, 4, 5, 6, 7]
        TreeViewsMaster.TreeNode root = new TreeViewsMaster.TreeNode(1);
        root.left = new TreeViewsMaster.TreeNode(2);
        root.right = new TreeViewsMaster.TreeNode(3);
        root.left.left = new TreeViewsMaster.TreeNode(4);
        root.left.right = new TreeViewsMaster.TreeNode(5);
        root.right.left = new TreeViewsMaster.TreeNode(6);
        root.right.right = new TreeViewsMaster.TreeNode(7);

        System.out.println("=== 1. Left Side View ===");
        System.out.println(TreeViewsMaster.leftSideView(root)); // Output: [1, 2, 4]

        System.out.println("\n=== 2. Right Side View ===");
        System.out.println(TreeViewsMaster.rightSideView(root)); // Output: [1, 3, 7]

        System.out.println("\n=== 3. Top View ===");
        System.out.println(TreeViewsMaster.topView(root)); // Output: [4, 2, 1, 3, 7]

        System.out.println("\n=== 4. Bottom View ===");
        System.out.println(TreeViewsMaster.bottomView(root)); // Output: [4, 2, 6, 3, 7] (5 & 6 at Col 0, 6 seen last)

        System.out.println("\n=== 5. Boundary Traversal (LeetCode 545) ===");
        System.out.println(TreeViewsMaster.boundaryTraversal(root)); // Output: [1, 2, 4, 5, 6, 7, 3]
    }
}
```

---

## 9. Complexity Analysis

| View Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Left / Right Views** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Level snapshot `i == 0` or `size - 1` |
| **Top View** | **$O(N \log N)$** | $O(N)$ Map Space | `topMap.putIfAbsent(col, val)` |
| **Bottom View** | **$O(N \log N)$** | $O(N)$ Map Space | `bottomMap.put(col, val)` overwrite |
| **Boundary (545)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | 4-Stage anti-clockwise traversal |

---

## 10. Edge Cases & Boundary Handling
* **Single Node Tree**: All views return `[val]`. Boundary traversal returns `[val]`.
* **Skewed Tree (LinkedList Style)**:
  - Left Skewed: Left View and Right View contain all nodes. Top View contains root and left-most node.
* **Nodes Sharing Column & Depth Coordinates**: For Bottom View, level-order BFS guarantees the deepest node at column $X$ overwrites earlier nodes cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Using DFS for Top/Bottom Views without Depth Information**:
  - DFS traverses deep into left subtrees before right subtrees. In Top View, a deeper left node can overwrite a higher right node at the same column!
  - **Always use Level-Order BFS** for Top and Bottom Views to ensure upper levels are processed before lower levels.
* **Duplicate Leaf Collection in Boundary Traversal**: Including leaf nodes in Left/Right boundary traversal functions duplicates leaves. **Skip leaves in boundary functions** (`if (!isLeaf(node))`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Top View vs Bottom View Logic:
> * **Top View**: Use `putIfAbsent(col, val)` (Keeps the HIGHEST level node seen at column `col`).
> * **Bottom View**: Use `put(col, val)` (Overwrites with the DEEPEST level node seen at column `col`).

> **Memory Trick:** **"Top View keeps FIRST node at column X (putIfAbsent); Bottom View keeps LAST node at column X (put)!"**

---

## 13. System & Implementation Comparisons

| Feature | Horizontal Level Views (Left/Right) | Vertical Column Views (Top/Bottom) |
| :--- | :--- | :--- |
| **Coordinate System** | Level Depth $D$ | Column Line $X$ |
| **Data Map Required** | None (Level List) | `TreeMap<Integer, Integer>` |
| **Primary Method** | Queue Snapshot BFS | Column Tuple Queue BFS |

---

## 14. How to Recognize This in Questions
* **"Find nodes visible from right side of tree"** $\rightarrow$ LeetCode 199 (Right Side View BFS `i == size - 1`).
* **"Traverse the outer boundary of a binary tree anti-clockwise"** $\rightarrow$ LeetCode 545 (Root + Left Edge + Leaves + Reversed Right Edge).

---

## 15. Frequently Asked Interview Questions
* **Q: Why MUST Left and Right Boundary functions skip leaf nodes in Boundary Traversal?**  
  *A:* Because all leaf nodes are collected separately in Step 3 (Leaf Collection). If Left Boundary collected leaf nodes, the left-most leaf would be added twice to the result list.
* **Q: Why is level-order BFS preferred over DFS for Top View?**  
  *A:* BFS guarantees nodes are visited in increasing order of their depth $Y$. The first time column $X$ is visited in BFS, it is guaranteed to be the highest (top-most) node for that column.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY TREE VIEWS & BOUNDARY TRAVERSALS               |
+-----------------------------------------------------------------------+
| • Left View: Collect node when (i == 0) in level loop                 |
| • Right View (199): Collect node when (i == levelSize - 1)            |
| • Top View: BFS + TreeMap; putIfAbsent(col, val)                      |
| • Bottom View: BFS + TreeMap; put(col, val) overwrite                 |
| • Boundary (545): Root -> Left Edge (no leaves) -> Leaves -> Right Edge|
|   (no leaves, REVERSED!)                                              |
| • Leaf Skip Rule: Boundary edge functions MUST skip leaf nodes!       |
| • Complexity: Views run in O(N) Time | Top/Bottom run in O(N log N)   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Left and Right Views using queue level snapshotting.
- [ ] I can write Top View using `putIfAbsent` and BFS.
- [ ] I can write Bottom View using `put` overwrite and BFS.
- [ ] I can implement Boundary Traversal (LeetCode 545) in 4 distinct steps.
- [ ] I know why boundary edge functions must skip leaf nodes.
