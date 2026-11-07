# 11. Tree Views, Boundary Traversals & Level-Order Projection Algorithms

## 1. Introduction
**Tree Views** extract specific 2D perimeter perspectives of a Binary Tree. By observing the tree from different geometric viewpoints—**Right Side View (LeetCode 199)**, **Left Side View**, **Top View**, **Bottom View**, and **Boundary Traversal (LeetCode 545)**—algorithms extract the visible nodes in **$O(N)$ linear time and $O(W)$ auxiliary space** using BFS level-order queues, vertical column maps, or reverse DFS depth tracking.

> **Important:** The key architectural mechanisms for Tree Views:
> * **Right Side View (LeetCode 199)**: The LAST node processed in each level during BFS level-order traversal (OR DFS `Right-to-Left` depth tracking where `depth == result.size()`)!
> * **Left Side View**: The FIRST node processed in each level during BFS level-order traversal.
> * **Top View**: The FIRST node encountered in each vertical column $X$ during BFS level-order traversal.
> * **Bottom View**: The LAST node encountered in each vertical column $X$ during BFS level-order traversal.

```
Tree Views Perspective Spectrum Topology:
                        [ Top View ]
                            |
   [ Left View ] --->  [ Root Node ]  <--- [ Right View ]
                         /        \
                    [ Left ]    [ Right ]
                            |
                      [ Bottom View ]
```

---

## 2. Core Concepts & Right Side View Mechanics (LeetCode 199)

### 2.1 Binary Tree Right Side View (LeetCode 199)
Given the root of a binary tree, imagine yourself standing on the right side of it; return the values of the nodes you can see ordered from top to bottom.

#### DFS `Right-to-Left` Strategy ($O(N)$ Time, $O(H)$ Auxiliary Space - Optimal):
1. Traverse tree using DFS in order: **`Root -> Right Child -> Left Child`**.
2. Pass current `depth` (starting at 0).
3. If **`depth == result.size()`**: Add `root.val` to `result`! (Since right child is visited FIRST at each depth level, the first node encountered at depth level $D$ is guaranteed to be the rightmost visible node!).
4. Recurse right: `dfs(root.right, depth + 1, result)`.
5. Recurse left: `dfs(root.left, depth + 1, result)`.

```
Why depth == result.size() Works:
At depth level 0, result.size() is 0 -> Add root (result size becomes 1).
At depth level 1, right child is visited first. depth (1) == result.size() (1) -> Add right child!
Subsequent left nodes at depth level 1 have depth (1) < result.size() (2) -> SKIPPED! ⚡
```

> **Memory Trick:** **"Right Side View: DFS Root -> Right -> Left! Add node when depth == result.size()!"**

---

## 3. Characteristics & Boundary Traversal Mechanics (LeetCode 545)

### 3.1 Boundary Traversal of Binary Tree (LeetCode 545)
Traverse the perimeter of a Binary Tree in **Counter-Clockwise Order**:
1. **Root Node**: Add `root.val` (if not a leaf).
2. **Left Boundary**: Traverse down `node.left` (or `node.right` if left is null), adding internal non-leaf nodes.
3. **Leaves**: Perform DFS to collect all leaf nodes from Left to Right.
4. **Right Boundary**: Traverse down `node.right` (or `node.left` if right is null), collect non-leaf nodes, and **REVERSE** them before adding to result!

```
Boundary Traversal Order:
Root -> Left Boundary (Top-Down) -> All Leaves (Left-to-Right) -> Right Boundary (Bottom-Up Reversed!) ⚡
```

---

## 4. Internal Working Mechanics
Tracing Top View vs Bottom View on Tree: `(1) <- [2] -> (3)`:

```
BFS Column Traversal (Queue stores Pairs: [node, col]):
Queue: [(2, col=0)], colMap = {}

1. Poll (2, col=0):
   - Top View   : col 0 not in map -> TopMap[0] = 2.
   - Bottom View: Overwrite BottomMap[0] = 2.
   - Offer (1, col=-1), Offer (3, col=+1).

2. Poll (1, col=-1):
   - Top Map[-1] = 1, Bottom Map[-1] = 1.

3. Poll (3, col=1):
   - Top Map[1] = 3, Bottom Map[1] = 3.

Top View Result    : [1, 2, 3] (First node per column)
Bottom View Result : [1, 2, 3] (Last node per column) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Tree Boundary Traversal Counter-Clockwise Topography:

```
                  (1) Root Node
                 /   \
  Left Boundary (2)   (3) Right Boundary (Reversed!)
               /   \     \
             (4)   (5)   (6)
            /   \
  Leaves: (7)   (8)
  Order: 1 -> 2 -> 4 -> 7 -> 8 -> 5 -> 6 -> 3! ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Right Side View (LeetCode 199), Left Side View, Top View, Bottom View, and Boundary Traversal (LeetCode 545):

```java
import java.util.*;

public class TreeViewsRotationsMaster {

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

    // 1. Right Side View DFS (LeetCode 199) O(N) Time, O(H) Space
    public static List<Integer> rightSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        dfsRightView(root, 0, result);
        return result;
    }

    private static void dfsRightView(TreeNode node, int depth, List<Integer> result) {
        if (node == null) return;

        // First node visited at this depth level is the rightmost visible node
        if (depth == result.size()) {
            result.add(node.val);
        }

        dfsRightView(node.right, depth + 1, result); // Visit RIGHT child first!
        dfsRightView(node.left, depth + 1, result);
    }

    // 2. Left Side View DFS O(N) Time, O(H) Space
    public static List<Integer> leftSideView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        dfsLeftView(root, 0, result);
        return result;
    }

    private static void dfsLeftView(TreeNode node, int depth, List<Integer> result) {
        if (node == null) return;

        if (depth == result.size()) {
            result.add(node.val);
        }

        dfsLeftView(node.left, depth + 1, result); // Visit LEFT child first!
        dfsLeftView(node.right, depth + 1, result);
    }

    // 3. Top View & Bottom View Queue BFS O(N) Time, O(N) Space
    private static class QueuePair {
        TreeNode node;
        int col;
        QueuePair(TreeNode node, int col) { this.node = node; this.col = col; }
    }

    public static List<Integer> topView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Map<Integer, Integer> topMap = new TreeMap<>(); // Sorted by column X
        Queue<QueuePair> queue = new ArrayDeque<>();
        queue.offer(new QueuePair(root, 0));

        while (!queue.isEmpty()) {
            QueuePair curr = queue.poll();
            // Record ONLY the FIRST node encountered in each column
            topMap.putIfAbsent(curr.col, curr.node.val);

            if (curr.node.left != null) queue.offer(new QueuePair(curr.node.left, curr.col - 1));
            if (curr.node.right != null) queue.offer(new QueuePair(curr.node.right, curr.col + 1));
        }

        result.addAll(topMap.values());
        return result;
    }

    public static List<Integer> bottomView(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        Map<Integer, Integer> bottomMap = new TreeMap<>(); // Sorted by column X
        Queue<QueuePair> queue = new ArrayDeque<>();
        queue.offer(new QueuePair(root, 0));

        while (!queue.isEmpty()) {
            QueuePair curr = queue.poll();
            // Overwrite to record the LAST node encountered in each column
            bottomMap.put(curr.col, curr.node.val);

            if (curr.node.left != null) queue.offer(new QueuePair(curr.node.left, curr.col - 1));
            if (curr.node.right != null) queue.offer(new QueuePair(curr.node.right, curr.col + 1));
        }

        result.addAll(bottomMap.values());
        return result;
    }

    // 4. Boundary Traversal (LeetCode 545) O(N) Time, O(H) Space
    public static List<Integer> boundaryTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;

        if (!isLeaf(root)) result.add(root.val);

        addLeftBoundary(root.left, result);
        addLeaves(root, result);
        addRightBoundary(root.right, result);

        return result;
    }

    private static boolean isLeaf(TreeNode node) {
        return node != null && node.left == null && node.right == null;
    }

    private static void addLeftBoundary(TreeNode node, List<Integer> result) {
        while (node != null) {
            if (!isLeaf(node)) result.add(node.val);
            node = (node.left != null) ? node.left : node.right;
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
        List<Integer> temp = new ArrayList<>();
        while (node != null) {
            if (!isLeaf(node)) temp.add(node.val);
            node = (node.right != null) ? node.right : node.left;
        }
        // Reverse right boundary for bottom-up order
        for (int i = temp.size() - 1; i >= 0; i--) {
            result.add(temp.get(i));
        }
    }
}
```

> **Quick Syntax:**
```java
// Right Side View DFS Line
if (depth == result.size()) result.add(node.val);
dfsRightView(node.right, depth + 1, result);
```

---

## 7. Concrete Problem Examples
* **LeetCode 199 - Binary Tree Right Side View**: DFS depth-level tracking.
* **LeetCode 545 - Boundary of Binary Tree**: Perimeter counter-clockwise traversal.
* **Top View & Bottom View**: BFS column coordinate mapping.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Right Side View, Top View, and Boundary Traversal:

```java
public class TreeViewsRotationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Right Side View (LeetCode 199) ===");
        TreeViewsRotationsMaster.TreeNode root = new TreeViewsRotationsMaster.TreeNode(1);
        root.left = new TreeViewsRotationsMaster.TreeNode(2, null, new TreeViewsRotationsMaster.TreeNode(5));
        root.right = new TreeViewsRotationsMaster.TreeNode(3, null, new TreeViewsRotationsMaster.TreeNode(4));

        List<Integer> rightView = TreeViewsRotationsMaster.rightSideView(root);
        System.out.println("Right Side View: " + rightView); // Output: [1, 3, 4]

        System.out.println("\n=== 2. Top View & Bottom View ===");
        System.out.println("Top View:    " + TreeViewsRotationsMaster.topView(root));    // Output: [2, 1, 3, 4]
        System.out.println("Bottom View: " + TreeViewsRotationsMaster.bottomView(root)); // Output: [2, 5, 3, 4]

        System.out.println("\n=== 3. Boundary Traversal (LeetCode 545) ===");
        System.out.println("Boundary:    " + TreeViewsRotationsMaster.boundaryTraversal(root)); // Output: [1, 2, 5, 4, 3] ✅
    }
}
```

---

## 9. Complexity Analysis

| View Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Right / Left View (199)**| **$O(N)$ Linear ⚡** | **$O(H)$ Stack Space ⚡**| `depth == result.size()` DFS check |
| **Top / Bottom View** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Column $X$ BFS `TreeMap` |
| **Boundary Traversal (545)**| **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | 3-pass perimeter traversal |

---

## 10. Edge Cases & Boundary Handling
* **Empty Tree (`root == null`)**: Returns empty list `[]`.
* **Single Node Tree**: `boundaryTraversal` returns single node value `[root.val]` without duplicating as leaf.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Level-Order Queue for Right Side View ($O(W)$ Space) When DFS Takes $O(H)$ Space**:
  - Queue BFS uses $O(W)$ space. DFS `Right-to-Left` uses $O(H)$ space (more memory-efficient for wide trees!).
* **Including Leaf Nodes in Left/Right Boundary Traversals**:
  - Left boundary and right boundary functions MUST skip leaf nodes (`if (!isLeaf(node))`) to prevent duplicate entries in final boundary result!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Difference Between Top View and Bottom View:
> Both use BFS level-order queue traversal with column $X$ tracking.
> * **Top View**: Uses `topMap.putIfAbsent(col, node.val)` (Records ONLY the FIRST node seen in each column).
> * **Bottom View**: Uses `bottomMap.put(col, node.val)` (Overwrites to record the LAST node seen in each column).

> **Memory Trick:** **"Top View = putIfAbsent(); Bottom View = put() overwrite!"**

---

## 13. System & Implementation Comparisons

| Feature | DFS Right-to-Left Right View | BFS Level-Order Right View |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(H)$ Stack Space ⚡** | $O(W)$ Queue Space |
| **Code Footprint** | **5 Lines ⚡** | 15 Lines |
| **Execution Speed** | **Fastest (Direct DFS) ⚡** | Slower (Queue allocations) |

---

## 14. How to Recognize This in Questions
* **"Return visible nodes when looking at binary tree from right side"** $\rightarrow$ LeetCode 199 (DFS `Right-to-Left` with `depth == result.size()`).
* **"Traverse binary tree boundary counter-clockwise"** $\rightarrow$ LeetCode 545 (Root + Left boundary + Leaves + Reversed right boundary).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does DFS `Right-to-Left` visit the rightmost visible node first at every depth level?**  
  *A:* Because `dfs(node.right)` is called BEFORE `dfs(node.left)`. For any depth $D$, the rightmost path branches down first, placing its node at index $D$ of the result list.
* **Q: Why does Right Boundary traversal need to be reversed in Boundary Traversal (LeetCode 545)?**  
  *A:* Because counter-clockwise perimeter traversal moves UP the right boundary from leaf to root. Iterating down the right boundary collects nodes top-down, requiring a reversal step to achieve bottom-up order.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TREE VIEWS & BOUNDARY TRAVERSALS                      |
+-----------------------------------------------------------------------+
| • Right View DFS: Root -> Right -> Left; if (depth == result.size())  |
| • Left View DFS : Root -> Left -> Right; if (depth == result.size())  |
| • Top View      : BFS column map using putIfAbsent(col, val)          |
| • Bottom View   : BFS column map using put(col, val) overwrite        |
| • Boundary (545): Root + Left boundary + Leaves + Reversed Right boundary|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Binary Tree Right Side View (LeetCode 199) in 5 lines using DFS.
- [ ] I can write Top View and Bottom View using BFS column maps.
- [ ] I can write Boundary Traversal (LeetCode 545).
- [ ] I know why `putIfAbsent` gives Top View while `put` gives Bottom View.
- [ ] I know how to avoid leaf duplicates in boundary traversals.
