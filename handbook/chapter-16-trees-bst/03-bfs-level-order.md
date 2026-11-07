# 03. BFS Level-Order Traversal, Queue Layering & Vertical Column Topography

## 1. Introduction
**Breadth-First Search (BFS) Level-Order Traversal** processes nodes in a Binary Tree level by level, from top to bottom and left to right within each level. Powered by a **FIFO Queue (`Queue<TreeNode>`)**, BFS level-order traversal solves level-based tree analytics—such as **Binary Tree Level Order Traversal (LeetCode 102)**, **Binary Tree Zigzag Level Order Traversal (LeetCode 103)**, **Populating Next Right Pointers in Each Node (LeetCode 116 / 117)**, and **Vertical Order Traversal (LeetCode 987)**—in **$O(N)$ linear time and $O(W)$ auxiliary space** (where $W$ is the maximum width of the tree).

> **Important:** Why does BFS level-order traversal process a tree level by level in exact order?
> The **Queue Size Snapshot Pattern** (`int levelSize = queue.size()`) captures the exact number of nodes existing at the current level BEFORE the inner processing loop begins!
> As children of the current level are added to the queue, they wait behind the snapshot boundary, ensuring level separation! ⚡

```
Queue Level Snapshot Topology:
Queue State : [ Node A (L1) ] -> Size Snapshot = 1
Processing  : Poll Node A -> Add Children (B, C) to Queue rear
Next Queue  : [ Node B (L2) | Node C (L2) ] -> Size Snapshot = 2
Level separation is strictly preserved! ⚡
```

---

## 2. Core Concepts & BFS Level Snapshot Architecture

### 2.1 The Queue Level Snapshot Pattern
To group nodes by their depth levels into `List<List<Integer>>`:
1. Initialize `Queue<TreeNode> queue = new ArrayDeque<>()`.
2. `queue.offer(root)`.
3. While `!queue.isEmpty()`:
   - Capture current level count: **`int levelSize = queue.size()`**!
   - Create `List<Integer> currentLevel = new ArrayList<>()`.
   - Loop `i = 0` to `levelSize - 1`:
     - `TreeNode curr = queue.poll()`.
     - `currentLevel.add(curr.val)`.
     - `if (curr.left != null) queue.offer(curr.left);`
     - `if (curr.right != null) queue.offer(curr.right);`
   - `result.add(currentLevel)`.
4. Return `result`.

```
BFS Level Snapshot Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Processing Direction| Queue / Deque Usage| Special Mechanism |
+-----------------------+-------------------+-------------------+-------------------+
| Standard Level Order  | Left to Right     | `Queue<TreeNode>` | Level size snapshot|
| Zigzag Level Order    | Alternating L-R/R-L| `Deque<Integer>`  | Prepend on odd levels|
| Next Right Pointers   | Left to Right     | `Queue` or $O(1)$ Pointer| `curr.next = queue.peek()`|
| Vertical Order (987)  | Top to Bottom, Left to Right| PriorityQueue + HashMap| Column coordinate $X$|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"BFS Level Order: Always capture int levelSize = queue.size() before processing each level!"**

---

## 3. Characteristics & Vertical Order Traversal Coordinates (LeetCode 987)

### 3.1 Vertical Order Traversal Coordinate System (LeetCode 987)
Assign 2D spatial coordinates $(X, Y)$ to every node in the tree:
* **Root Node**: Assigned coordinates $(0, 0)$.
* **Left Child**: Assigned coordinates $(X - 1, Y + 1)$ (Moves 1 unit LEFT, 1 level DOWN).
* **Right Child**: Assigned coordinates $(X + 1, Y + 1)$ (Moves 1 unit RIGHT, 1 level DOWN).
* **Sorting Rule for Identical Coordinates $(X, Y)$**: If two nodes share the exact same column $X$ and row $Y$, sort them by their **Node Value in Ascending Order**!

```
Vertical Coordinate Map:
                  Root (0, 0)
                   /       \
        Left (-1, 1)       Right (+1, 1)
          /       \         /         \
     (-2, 2)     (0, 2)   (0, 2)      (+2, 2)
                 ^          ^
                 (Nodes at (0,2) are sorted by value!) ⚡
```

---

## 4. Internal Working Mechanics
Tracing Zigzag Level Order Traversal (LeetCode 103) on `root = [3, 9, 20, null, null, 15, 7]`:

```
Init: queue = [3], level = 0 (Even: Left to Right)

Level 0 (size 1):
  - Poll 3. Add 3 to level list -> [3].
  - Offer left child 9, right child 20. queue = [9, 20].
  - result = [[3]].

Level 1 (size 2, Odd: Right to Left):
  - Poll 9. Prepend/append to level list -> [9]. Offer children (none).
  - Poll 20. Add to front of level list -> [20, 9]. Offer left 15, right 7. queue = [15, 7].
  - result = [[3], [20, 9]].

Level 2 (size 2, Even: Left to Right):
  - Poll 15, Poll 7. level list = [15, 7].
  - result = [[3], [20, 9], [15, 7]].

Zigzag order constructed in O(N) Time! ✅
```

---

## 5. Visual Diagram
Populating Next Right Pointers (LeetCode 116) Topology:

```
Level 2 Queue State: [ Node 4 | Node 5 | Node 6 | Node 7 ]
                       |        |        |        |
                   4.next -> 5.next -> 6.next -> 7.next = null
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Level-Order Traversal (LeetCode 102), Zigzag Level-Order (LeetCode 103), Populating Next Right Pointers (LeetCode 116), and Vertical Order Traversal (LeetCode 987):

```java
import java.util.*;

public class BFSLevelOrderMaster {

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

    // Node wrapper with Next pointer for LeetCode 116/117
    public static class Node {
        public int val;
        public Node left;
        public Node right;
        public Node next;

        public Node(int val) {
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
            int levelSize = queue.size(); // Level Snapshot
            List<Integer> currentLevel = new ArrayList<>(levelSize);

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                currentLevel.add(curr.val);

                if (curr.left != null) queue.offer(curr.left);
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
                    currentLevel.addLast(curr.val); // Append to tail
                } else {
                    currentLevel.addFirst(curr.val); // Prepend to head
                }

                if (curr.left != null) queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }

            result.add(currentLevel);
            leftToRight = !leftToRight; // Alternate direction
        }

        return result;
    }

    // 3. Populating Next Right Pointers in Each Node (LeetCode 116 - O(1) Space)
    public static Node connect(Node root) {
        if (root == null) return null;

        Node leftmost = root;

        // Traverse level by level using existing next pointers!
        while (leftmost.left != null) {
            Node head = leftmost;

            while (head != null) {
                // Connection 1: Left child points to Right child
                head.left.next = head.right;

                // Connection 2: Right child points to next subtree's Left child
                if (head.next != null) {
                    head.right.next = head.next.left;
                }

                head = head.next; // Move right across level
            }

            leftmost = leftmost.left; // Move down to next level
        }

        return root;
    }

    // 4. Vertical Order Traversal of a Binary Tree (LeetCode 987) O(N log N) Time
    private static class Point implements Comparable<Point> {
        int x, y, val;
        Point(int x, int y, int val) { this.x = x; this.y = y; this.val = val; }

        @Override
        public int compareTo(Point other) {
            if (this.x != other.x) return Integer.compare(this.x, other.x);
            if (this.y != other.y) return Integer.compare(this.y, other.y);
            return Integer.compare(this.val, other.val);
        }
    }

    public static List<List<Integer>> verticalTraversal(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        List<Point> points = new ArrayList<>();
        dfsCoordinates(root, 0, 0, points);

        Collections.sort(points); // Sort by X, then Y, then Val

        Map<Integer, List<Integer>> colMap = new LinkedHashMap<>();
        for (Point p : points) {
            colMap.putIfAbsent(p.x, new ArrayList<>());
            colMap.get(p.x).add(p.val);
        }

        result.addAll(colMap.values());
        return result;
    }

    private static void dfsCoordinates(TreeNode node, int x, int y, List<Point> points) {
        if (node == null) return;
        points.add(new Point(x, y, node.val));
        dfsCoordinates(node.left, x - 1, y + 1, points);
        dfsCoordinates(node.right, x + 1, y + 1, points);
    }
}
```

> **Quick Syntax:**
```java
// Level Order Queue Snapshot Pattern
int levelSize = queue.size();
for (int i = 0; i < levelSize; i++) {
    TreeNode curr = queue.poll();
    ...
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 102 - Binary Tree Level Order Traversal**: Standard BFS queue snapshot.
* **LeetCode 103 - Binary Tree Zigzag Level Order Traversal**: Alternating level deque.
* **LeetCode 116 - Populating Next Right Pointers**: $O(1)$ space next pointer linkage.
* **LeetCode 987 - Vertical Order Traversal**: 2D coordinate sorting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Level-Order, Zigzag, and Next Right Pointers:

```java
public class BFSLevelOrderDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Level Order & Zigzag Traversal ===");
        BFSLevelOrderMaster.TreeNode root = new BFSLevelOrderMaster.TreeNode(3);
        root.left = new BFSLevelOrderMaster.TreeNode(9);
        root.right = new BFSLevelOrderMaster.TreeNode(20, 
            new BFSLevelOrderMaster.TreeNode(15), new BFSLevelOrderMaster.TreeNode(7));

        System.out.println("Level Order:  " + BFSLevelOrderMaster.levelOrder(root));
        // Output: [[3], [9, 20], [15, 7]]

        System.out.println("Zigzag Order: " + BFSLevelOrderMaster.zigzagLevelOrder(root));
        // Output: [[3], [20, 9], [15, 7]]

        System.out.println("\n=== 2. Vertical Order Traversal (LeetCode 987) ===");
        System.out.println("Vertical Order: " + BFSLevelOrderMaster.verticalTraversal(root));
        // Output: [[9], [3, 15], [20], [7]]
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Level Order (102)** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | $W$ is max level width |
| **Zigzag (103)** | **$O(N)$ Linear ⚡** | $O(W)$ Deque Space | Alternating `addFirst`/`addLast` |
| **Next Right Pointers (116)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict Constant ⚡**| Leverages existing next pointers |
| **Vertical Order (987)**| **$O(N \log N)$ ⚡** | $O(N)$ Point Space | Coordinate sorting by $X, Y, Val$ |

---

## 10. Edge Cases & Boundary Handling
* **Empty Tree (`root == null`)**: Returns empty list `[]` immediately.
* **Nodes With Identical $(X, Y)$ Coordinates in 987**: Sorted by node value ascending via `Comparable<Point>`.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting `int levelSize = queue.size()` Inside the Level Loop**:
  - Writing `for (int i = 0; i < queue.size(); i++)` re-evaluates `queue.size()` dynamically as child nodes are offered, mixing adjacent levels together!
  - **Always freeze `int levelSize = queue.size()` before beginning the level loop**.
* **Using Queue BFS for Next Right Pointers (LeetCode 116) When $O(1)$ Space is Demanded**:
  - Queue BFS uses $O(W)$ space.
  - **Use existing level `next` pointers to achieve $O(1)$ auxiliary space**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** $O(1)$ Auxiliary Space Trick for Populating Next Right Pointers (LeetCode 116):
> Instead of allocating a BFS Queue:
> Treat the current level as a Linked List connected by `.next` pointers!
> 1. `head.left.next = head.right` (Connect left child to right child).
> 2. `head.right.next = head.next.left` (Connect right child to adjacent subtree's left child).
> 3. Step `head = head.next` to process the entire level in **$O(1)$ Space**!

> **Memory Trick:** **"Populating Next Right Pointers in Perfect Trees can be done in O(1) space using existing level next pointers!"**

---

## 13. System & Implementation Comparisons

| Feature | Queue BFS Level Order | $O(1)$ Next-Pointer Level Order |
| :--- | :--- | :--- |
| **Auxiliary Memory** | $O(W)$ Queue Space | **$O(1)$ Strict Constant Space ⚡** |
| **Applicability** | Any Arbitrary Binary Tree | Requires Next Pointer Structure |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Traverse tree level by level from top to bottom"** $\rightarrow$ Level-Order Traversal (`queue.size()` snapshot).
* **"Traverse tree in vertical columns from left to right"** $\rightarrow$ LeetCode 987 (2D coordinates $X, Y$).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `queue.size()` need to be captured into a local variable before the inner level loop?**  
  *A:* Because offering left and right child nodes into the queue during the loop increases `queue.size()`. Capturing `levelSize = queue.size()` snapshot guarantees processing only the nodes belonging to the current depth level.
* **Q: How does Vertical Order Traversal (LeetCode 987) assign coordinates?**  
  *A:* Root is $(0, 0)$. Going left moves to $(X-1, Y+1)$; going right moves to $(X+1, Y+1)$. Sorting all nodes by $X$ ascending, $Y$ ascending, and $Val$ ascending produces correct vertical column groupings.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BFS LEVEL-ORDER & VERTICAL TRAVERSALS                 |
+-----------------------------------------------------------------------+
| • Snapshot Rule: Always set int levelSize = queue.size() before loop  |
| • Zigzag Rule: Alternate addLast() and addFirst() on a LinkedList     |
| • Next Pointers (116): head.left.next = head.right; right.next = next.left|
| • Vertical Coordinates (987): Left = (X-1, Y+1); Right = (X+1, Y+1)   |
| • Time Complexity: O(N) Linear Time | O(W) Queue Space ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Level Order Traversal (LeetCode 102) using the queue size snapshot.
- [ ] I can write Zigzag Level Order (LeetCode 103).
- [ ] I can write Populating Next Right Pointers (LeetCode 116) in $O(1)$ space.
- [ ] I can write Vertical Order Traversal (LeetCode 987) with 2D coordinates.
- [ ] I know why dynamic `queue.size()` inside the loop condition breaks level separation.
