# 03. Breadth-First Search (BFS) Level-Order, Zigzag & Vertical Traversals

## 1. Introduction
**Breadth-First Search (BFS)** tree traversal explores a binary tree level by level, visiting all nodes at depth $D$ before advancing to nodes at depth $D + 1$. In technical coding interviews, BFS forms the basis for Level-Order Traversal (LeetCode 102), Zigzag Level-Order Traversal (LeetCode 103), Binary Tree Right Side View (LeetCode 199), Vertical Order Traversal (LeetCode 987), and Populating Next Right Pointers (LeetCode 116).

> **Important:** The fundamental invariant of Level-Order BFS is **Queue Size Snapshotting (`int levelSize = queue.size()`)** at the start of each level loop. This ensures that nodes added during the current level's exploration are NOT processed until the next level iteration!

```
BFS Level Exploration Topology:
+-----------------------------------------------------------------------------------+
| Level 0 (Depth 0) : [ Root Node ]                                                |
| Level 1 (Depth 1) : [ Left Child, Right Child ]                                  |
| Level 2 (Depth 2) : [ Left-Left, Left-Right, Right-Left, Right-Right ]           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Patterns

### 2.1 The Queue Snapshot BFS Template
To process a binary tree level by level:
1. Initialize an `ArrayDeque<TreeNode> queue` and enqueue `root`.
2. While `!queue.isEmpty()`:
   - Capture current level width: **`int levelSize = queue.size()`**.
   - Create a level list `List<Integer> currentLevel = new ArrayList<>()`.
   - Loop `for (int i = 0; i < levelSize; i++)`:
     - Poll node: `TreeNode curr = queue.poll()`.
     - Process node `curr.val`.
     - Enqueue valid children: `if (curr.left != null) queue.offer(curr.left); if (curr.right != null) queue.offer(curr.right);`
   - Append `currentLevel` to `result`.

### 2.2 Zigzag (Snake) Level-Order Traversal (LeetCode 103)
Alternate traversal direction between levels:
* **Even Levels (0, 2, 4...)**: Left to Right. Append values normally to level list (`levelList.add(curr.val)`).
* **Odd Levels (1, 3, 5...)**: Right to Left. Prepend values to level list (`levelList.add(0, curr.val)`) OR use a Deque (`LinkedList.addFirst()`).

### 2.3 Binary Tree Right Side View (LeetCode 199)
* In the level-order snapshot loop `for (int i = 0; i < levelSize; i++)`, the node at index `i == levelSize - 1` (the LAST node in the level loop) is the rightmost visible node for that level!

### 2.4 Vertical Order Traversal (LeetCode 987)
Assign a 2D coordinate $(X, Y)$ to each node:
* Root is at $(X = 0, Y = 0)$.
* Left child of $(X, Y)$ is at $(X - 1, Y + 1)$.
* Right child of $(X, Y)$ is at $(X + 1, Y + 1)$.
* Group nodes by Column $X$ using a `TreeMap<Integer, List<NodeInfo>>` (sorted from left-to-right columns). Nodes sharing the same $(X, Y)$ are sorted by value!

```
BFS Traversal Variants Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| BFS Traversal Variant | Level Action      | Order Logic       | Key Identifier    |
+-----------------------+-------------------+-------------------+-------------------+
| Standard Level Order  | Collect All       | Left to Right     | `levelSize = q.size()`|
| Zigzag Level Order    | Alternate Insert  | Left-Right / Right-Left | `leftToRight` boolean|
| Right Side View       | Collect Last Node | `if (i == size-1)`| Last level element|
| Vertical Order (987)  | Group by Column X | Sorted X, Y, Val  | `TreeMap<Col, List>`|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Snapshot queue.size() BEFORE level loop! Last node in level loop (i == size - 1) gives Right Side View!"**

---

## 3. Characteristics & Memory Analysis

### 3.1 Maximum Queue Width Memory
Unlike DFS where memory is bounded by tree height $H$ ($O(H)$ stack space), BFS memory is bounded by the **Maximum Level Width $W$** of the tree.
* For a Perfect Binary Tree of height $H$, the last level contains $W = 2^H \approx \mathbf{N / 2\text{ Leaf Nodes}}$.
* Thus, BFS auxiliary space complexity is **$O(W) = O(N)$** in the worst case!

---

## 4. Internal Working Mechanics
Tracing Binary Tree Right Side View (LeetCode 199) on `[1, 2, 3, null, 5, null, 4]`:

```
          ( 1 )
         /     \
       ( 2 )   ( 3 )
        \        \
        ( 5 )    ( 4 )

Init: queue = [1], rightView = []

Level 0: levelSize = 1.
- i=0: poll 1. Children: enqueue 2, 3. i == 1-1 (LAST!) -> rightView.add(1).
  queue = [2, 3] | rightView = [1]

Level 1: levelSize = 2.
- i=0: poll 2. Children: enqueue 5.
- i=1: poll 3. Children: enqueue 4. i == 2-1 (LAST!) -> rightView.add(3).
  queue = [5, 4] | rightView = [1, 3]

Level 2: levelSize = 2.
- i=0: poll 5. Children: none.
- i=1: poll 4. Children: none. i == 2-1 (LAST!) -> rightView.add(4).
  queue = [] | rightView = [1, 3, 4]

Result: Right Side View = [1, 3, 4] ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Vertical Order Traversal Column Coordinate Grid Assignment:

```
                  Col -1      Col 0      Col +1
                    |           |           |
                    |         ( 1 )         |   (0, 0)
                    |        /     \        |
                    v      /         \      v
                  ( 2 )               ( 3 )     (-1, 1) & (+1, 1)
                 /     \             /     \
               /         \         /         \
             ( 4 )      ( 5 )   ( 6 )       ( 7 )
               ^          ^       ^           ^
               |          |       |           |
            Col -2     Col 0    Col 0      Col +2

Col -2: [4]
Col -1: [2]
Col  0: [1, 5, 6]  (Nodes 5 & 6 share Col 0!)
Col +1: [3]
Col +2: [7]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Level Order (LeetCode 102), Zigzag (LeetCode 103), Right Side View (LeetCode 199), and Vertical Order Traversal (LeetCode 987):

```java
import java.util.*;

public class TreeTraversalsBFSMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Binary Tree Level Order Traversal (LeetCode 102) O(N) Time, O(W) Space
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size(); // SNAPSHOT LEVEL SIZE!
            List<Integer> currentLevel = new ArrayList<>(levelSize);

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                currentLevel.add(curr.val);

                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }

            result.add(currentLevel);
        }

        return result;
    }

    // 2. Binary Tree Zigzag Level Order Traversal (LeetCode 103) O(N) Time, O(W) Space
    public static List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);
        boolean leftToRight = true;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            LinkedList<Integer> currentLevel = new LinkedList<>();

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();

                if (leftToRight) {
                    currentLevel.addLast(curr.val);
                } else {
                    currentLevel.addFirst(curr.val); // Prepend for right-to-left
                }

                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }

            result.add(currentLevel);
            leftToRight = !leftToRight; // Toggle direction
        }

        return result;
    }

    // 3. Binary Tree Right Side View (LeetCode 199) O(N) Time, O(W) Space
    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();

                // If last node in current level, append to right side view
                if (i == levelSize - 1) {
                    result.add(curr.val);
                }

                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }
        }

        return result;
    }

    // 4. Vertical Order Traversal of a Binary Tree (LeetCode 987) O(N log N) Time, O(N) Space
    static class NodeInfo {
        TreeNode node;
        int row;
        int col;

        NodeInfo(TreeNode node, int row, int col) {
            this.node = node;
            this.row = row;
            this.col = col;
        }
    }

    public static List<List<Integer>> verticalTraversal(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        // TreeMap automatically sorts columns from Left (-X) to Right (+X)
        Map<Integer, List<NodeInfo>> columnMap = new TreeMap<>();
        Queue<NodeInfo> queue = new ArrayDeque<>();
        queue.offer(new NodeInfo(root, 0, 0));

        while (!queue.isEmpty()) {
            NodeInfo curr = queue.poll();
            columnMap.computeIfAbsent(curr.col, k -> new ArrayList<>()).add(curr);

            if (curr.node.left != null) {
                queue.offer(new NodeInfo(curr.node.left, curr.row + 1, curr.col - 1));
            }
            if (curr.node.right != null) {
                queue.offer(new NodeInfo(curr.node.right, curr.row + 1, curr.col + 1));
            }
        }

        for (List<NodeInfo> list : columnMap.values()) {
            // Sort by row first, then by value
            list.sort((a, b) -> {
                if (a.row != b.row) return Integer.compare(a.row, b.row);
                return Integer.compare(a.node.val, b.node.val);
            });

            List<Integer> colValues = new ArrayList<>();
            for (NodeInfo info : list) {
                colValues.add(info.node.val);
            }
            result.add(colValues);
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Standard Level Size Snapshot Pattern
int levelSize = queue.size();
for (int i = 0; i < levelSize; i++) {
    TreeNode curr = queue.poll();
    if (i == levelSize - 1) rightView.add(curr.val);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 102 - Binary Tree Level Order Traversal**: Standard BFS queue snapshotting.
* **LeetCode 103 - Binary Tree Zigzag Level Order**: Toggling direction deque insertion.
* **LeetCode 199 - Binary Tree Right Side View**: Collecting last element in level loop.
* **LeetCode 987 - Vertical Order Traversal**: $(X, Y)$ coordinate grouping + TreeMap.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Level Order, Zigzag, Right Side View, and Vertical Order Traversals:

```java
public class TreeTraversalsBFSDemo {

    public static void main(String[] args) {
        // Build Tree: [1, 2, 3, 4, 5, 6, 7]
        TreeTraversalsBFSMaster.TreeNode root = new TreeTraversalsBFSMaster.TreeNode(1);
        root.left = new TreeTraversalsBFSMaster.TreeNode(2);
        root.right = new TreeTraversalsBFSMaster.TreeNode(3);
        root.left.left = new TreeTraversalsBFSMaster.TreeNode(4);
        root.left.right = new TreeTraversalsBFSMaster.TreeNode(5);
        root.right.left = new TreeTraversalsBFSMaster.TreeNode(6);
        root.right.right = new TreeTraversalsBFSMaster.TreeNode(7);

        System.out.println("=== 1. Level Order Traversal (LeetCode 102) ===");
        System.out.println(TreeTraversalsBFSMaster.levelOrder(root));

        System.out.println("\n=== 2. Zigzag Level Order (LeetCode 103) ===");
        System.out.println(TreeTraversalsBFSMaster.zigzagLevelOrder(root));

        System.out.println("\n=== 3. Right Side View (LeetCode 199) ===");
        System.out.println(TreeTraversalsBFSMaster.rightSideView(root));

        System.out.println("\n=== 4. Vertical Order Traversal (LeetCode 987) ===");
        System.out.println(TreeTraversalsBFSMaster.verticalTraversal(root));
    }
}
```

---

## 9. Complexity Analysis

| BFS Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Level Order (102)** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Snapshot level size `queue.size()` |
| **Zigzag Order (103)** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Toggle Deque insertion |
| **Right Side View (199)** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Last level element `i == size - 1` |
| **Vertical Order (987)** | **$O(N \log N)$** | $O(N)$ Map Space | TreeMap column sorting + row/val sort |

---

## 10. Edge Cases & Boundary Handling
* **Null Root**: Return empty list `[]` immediately.
* **Single Node**: Return `[[val]]` for level order, `[val]` for right side view.
* **Deep Skewed Tree (LinkedList Style)**: Queue width $W = 1$, space complexity is $O(1)$.

---

## 11. Common Mistakes & Anti-Patterns
* **Writing `i < queue.size()` Directly inside the For Loop**:
  - `for (int i = 0; i < queue.size(); i++)` causes `queue.size()` to change dynamically as children are enqueued! Levels get corrupted. **ALWAYS capture `int levelSize = queue.size()` BEFORE entering the loop**.
* **Using `LinkedList` for FIFO Queue in Java**: `ArrayDeque` is faster and consumes less RAM.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** BFS vs DFS Space Complexity Trade-Off:
> * **DFS Memory**: Bounded by **Tree Height $H$** ($O(H)$ stack space). Best for deep, narrow trees.
> * **BFS Memory**: Bounded by **Tree Max Width $W$** ($O(W)$ queue space). Best for shallow, wide trees or shortest path level queries.

> **Memory Trick:** **"Snapshot level size into a local variable BEFORE the level loop!"**

---

## 13. System & Implementation Comparisons

| Feature | DFS Traversals | BFS Level Order Traversals |
| :--- | :--- | :--- |
| **Primary Structure** | `Stack` / JVM Call Stack | `ArrayDeque` Queue |
| **Memory Bound** | Height $H$ ($O(\log N)$ to $O(N)$) | Width $W$ ($O(N)$ for perfect trees) |
| **Level Processing** | Vertical exploration | **Horizontal Level-by-Level ⚡** |
| **Shortest Unweighted Path**| Requires exploring all paths | **First reach is shortest path! ⚡** |

---

## 14. How to Recognize This in Questions
* **"Traverse a binary tree level by level"** $\rightarrow$ BFS Queue Snapshot (`int size = queue.size()`).
* **"Find rightmost node visible at each level"** $\rightarrow$ Right Side View (`i == levelSize - 1`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why must `int levelSize = queue.size()` be captured in a variable before the loop?**  
  *A:* Because inside the loop, we call `queue.offer(child)`, which increases `queue.size()`. Evaluating `i < queue.size()` directly would cause the loop to process newly added children in the current level instead of deferring them to the next level.
* **Q: How does Vertical Order Traversal handle nodes sharing the same (Row, Col) coordinates?**  
  *A:* LeetCode 987 specifies that nodes sharing identical $(X, Y)$ coordinates must be sorted in ascending order of their node values. We achieve this by sorting `NodeInfo` objects by `row` first, then by `val`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BFS LEVEL-ORDER & VERTICAL TRAVERSALS                 |
+-----------------------------------------------------------------------+
| • Snapshot Invariant: int levelSize = queue.size(); for (0..size-1)   |
| • Level Order: Collect all level elements in order                    |
| • Zigzag Order: Toggle boolean leftToRight; addFirst() for odd levels|
| • Right Side View: Collect node when (i == levelSize - 1)            |
| • Vertical Order: Group by Col X; left child (X-1, Y+1), right (X+1, Y+1)|
| • Queue Choice: Queue<TreeNode> queue = new ArrayDeque<>();           |
| • Complexity: O(N) Linear Time | O(W) Queue Width Memory              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the queue snapshot level-order template in 60 seconds.
- [ ] I know why `int levelSize = queue.size()` must be stored in a variable.
- [ ] I can solve Binary Tree Right Side View (LeetCode 199).
- [ ] I can solve Zigzag Level Order (LeetCode 103).
- [ ] I can implement Vertical Order Traversal (LeetCode 987) with $(X,Y)$ coordinates.
