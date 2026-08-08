# 10. Binary Tree Metrics: Diameter, Maximum Width & Distance Mechanics

## 1. Introduction
Computing tree-wide geometric metrics—such as **Diameter of a Binary Tree (LeetCode 543)** and **Maximum Width of a Binary Tree (LeetCode 662)**—are essential non-linear structural measurement problems in technical coding interviews. These problems evaluate post-order height synthesis vs global diameter tracking, and 64-bit heap index encoding (`2 * index + 1` and `2 * index + 2`) to calculate maximum level widths including null gaps in **$O(N)$ linear time**.

> **Important:** In Diameter of Binary Tree (LeetCode 543), the diameter is the length of the **longest path between ANY two nodes** in a tree (measured in number of EDGES). The diameter passing through node $X$ is equal to:
> $$\text{Diameter}(X) = \text{Height}(\text{LeftSubtree}) + \text{Height}(\text{RightSubtree})$$

```
Tree Metric Measurements Spectrum:
+-----------------------------------------------------------------------------------+
| Tree Diameter (543) : Longest edge path between ANY two nodes -> O(N) Post-Order  |
| Max Width (662)     : Max level width including NULL gaps     -> O(N) BFS Heap Pos|
| Node Distance (863) : Distance K from Target Node            -> Graph / Parent DFS|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Encoding

### 2.1 Diameter of a Binary Tree (LeetCode 543)
* **Definition**: Length of the longest path between any two nodes in a tree (measured in number of edges). The path may or may not pass through the root!
* **Post-Order Synthesis**:
  - At node `curr`:
    - `leftHeight = heightDFS(curr.left)` (Height of empty tree is 0).
    - `rightHeight = heightDFS(curr.right)`.
    - **Local Diameter through `curr`**: `localDiameter = leftHeight + rightHeight`.
    - Update global diameter: `maxDiameter = Math.max(maxDiameter, localDiameter)`.
    - **Return to Parent**: Return node height `1 + Math.max(leftHeight, rightHeight)`.

### 2.2 Maximum Width of a Binary Tree (LeetCode 662)
* **Definition**: The maximum width among all levels. Width of a level is the number of slots between the end nodes (the leftmost and rightmost non-null nodes in the level), **including NULL gaps in between**!
* **Binary Heap Index Position Encoding**:
  - Assign a 1D position index `idx` to nodes as if the tree were a Complete Binary Tree:
    - Root position index = `1` (or `0`).
    - Left child position index = `2 * idx`.
    - Right child position index = `2 * idx + 1`.
  - At each level in BFS:
    - `firstIdx = levelQueue.peek().idx`.
    - `lastIdx = levelQueue.peekLast().idx`.
    - Level width = **`lastIdx - firstIdx + 1`**.
    - Update global maximum width: `maxWidth = Math.max(maxWidth, lastIdx - firstIdx + 1)`.

```
Tree Metrics Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric Problem        | Core Property     | Traversal Pattern | Key Calculation   |
+-----------------------+-------------------+-------------------+-------------------+
| Diameter (543)        | Longest Edge Path | Post-Order DFS    | `leftH + rightH`  |
| Maximum Width (662)   | Level Width w/Null| BFS Heap Indexing | `lastIdx - firstIdx + 1`|
| All Nodes Distance K  | Distance Steps K  | Graph BFS / Parent| BFS Level Steps   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Diameter = leftHeight + rightHeight! Max Width = lastIdx - firstIdx + 1 using 2*idx & 2*idx+1 position encoding!"**

---

## 3. Characteristics & 64-Bit Integer Overflow Safeguards

### 3.1 Overcoming Heap Index Overflow in Maximum Width
In a deep skewed binary tree of height $H = 60$, $2^{60}$ position index encoding overflows 32-bit `int` (`Integer.MAX_VALUE \approx 2 \times 10^9`)!
* **Fix 1**: Use 64-bit `long` for position indices (`2L * idx`).
* **Fix 2 (Index Normalization)**: At the start of each level loop in BFS, normalize the first node's index to `0` by subtracting `firstIdx` from all node indices in that level!

```
Index Normalization Example:
Level Start: Queue contains nodes with indices [1000, 1002, 1005]
Subtract firstIdx (1000):
Normalized Indices: [0, 2, 5] -> Level Width = 5 - 0 + 1 = 6 (Zero Overflow Risk!) ✅
```

---

## 4. Internal Working Mechanics
Tracing Maximum Width of Binary Tree (LeetCode 662) on `[1, 3, 2, 5, 3, null, 9]`:

```
                  ( 1, idx=1 )
                 /            \
        ( 3, idx=2 )        ( 2, idx=3 )
       /            \                   \
( 5, idx=4 )    ( 3, idx=5 )        ( 9, idx=7 )

Level 0: Queue = [(1, idx=1)]
         Width = 1 - 1 + 1 = 1. maxWidth = 1.

Level 1: Queue = [(3, idx=2), (2, idx=3)]
         Width = 3 - 2 + 1 = 2. maxWidth = 2.

Level 2: Queue = [(5, idx=4), (3, idx=5), (9, idx=7)]
         firstIdx = 4, lastIdx = 7.
         Width = 7 - 4 + 1 = 4 (Null gap at idx=6 included!).
         maxWidth = max(2, 4) = 4.

Result: Maximum Width = 4 ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Tree Diameter vs Maximum Level Width Topology:

```
[ TREE DIAMETER (543) ]                    [ MAXIMUM WIDTH (662) ]
        ( 1 )                                       ( 1, idx=1 )
       /     \                                     /            \
     ( 2 )   ( 3 )                        ( 3, idx=2 )        ( 2, idx=3 )
    /     \                               /            \                   \
  ( 4 )   ( 5 )                     ( 5, idx=4 )    ( 3, idx=5 )        ( 9, idx=7 )
                                    |<----------------------------------------->|
Path 4 -> 2 -> 1 -> 3 (3 Edges)     Width = 7 - 4 + 1 = 4 (Includes NULL at idx 6!)
Diameter = leftH(2) + rightH(1) = 3
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Diameter of Binary Tree (LeetCode 543), Maximum Width of Binary Tree (LeetCode 662), and All Nodes Distance K in Binary Tree (LeetCode 863):

```java
import java.util.*;

public class TreeMetricsMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Diameter of Binary Tree (LeetCode 543) O(N) Time, O(H) Space
    private static int maxDiameterGlobal = 0;

    public static int diameterOfBinaryTree(TreeNode root) {
        maxDiameterGlobal = 0;
        heightDFS(root);
        return maxDiameterGlobal;
    }

    private static int heightDFS(TreeNode node) {
        if (node == null) return 0;

        int leftH = heightDFS(node.left);
        int rightH = heightDFS(node.right);

        // Local diameter is the sum of left and right subtree heights
        maxDiameterGlobal = Math.max(maxDiameterGlobal, leftH + rightH);

        // Return height of current node to parent
        return 1 + Math.max(leftH, rightH);
    }

    // 2. Maximum Width of Binary Tree (LeetCode 662) O(N) Time, O(W) Space
    static class PairNode {
        TreeNode node;
        long idx; // 64-bit index to prevent integer overflow

        PairNode(TreeNode node, long idx) {
            this.node = node;
            this.idx = idx;
        }
    }

    public static int widthOfBinaryTree(TreeNode root) {
        if (root == null) return 0;

        Deque<PairNode> queue = new ArrayDeque<>();
        queue.offer(new PairNode(root, 0L));
        int maxWidth = 0;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            long firstIdx = queue.peek().idx; // First node index in level
            long lastIdx = queue.peekLast().idx;  // Last node index in level

            maxWidth = Math.max(maxWidth, (int) (lastIdx - firstIdx + 1));

            for (int i = 0; i < levelSize; i++) {
                PairNode curr = queue.poll();
                long normalizedIdx = curr.idx - firstIdx; // Normalize index to 0

                if (curr.node.left != null) {
                    queue.offer(new PairNode(curr.node.left, 2 * normalizedIdx + 1));
                }
                if (curr.node.right != null) {
                    queue.offer(new PairNode(curr.node.right, 2 * normalizedIdx + 2));
                }
            }
        }

        return maxWidth;
    }

    // 3. All Nodes Distance K in Binary Tree (LeetCode 863) O(N) Time, O(N) Space
    public static List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
        List<Integer> result = new ArrayList<>();
        if (root == null || target == null) return result;

        // Step 1: Build Parent Map using DFS
        Map<TreeNode, TreeNode> parentMap = new HashMap<>();
        buildParentMap(root, null, parentMap);

        // Step 2: Graph BFS from target node
        Queue<TreeNode> queue = new ArrayDeque<>();
        Set<TreeNode> visited = new HashSet<>();

        queue.offer(target);
        visited.add(target);
        int currentDistance = 0;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            if (currentDistance == k) {
                for (int i = 0; i < levelSize; i++) {
                    result.add(queue.poll().val);
                }
                return result;
            }

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();

                // Explore 3 directions: Left, Right, Parent!
                if (curr.left != null && !visited.contains(curr.left)) {
                    visited.add(curr.left);
                    queue.offer(curr.left);
                }
                if (curr.right != null && !visited.contains(curr.right)) {
                    visited.add(curr.right);
                    queue.offer(curr.right);
                }
                TreeNode parent = parentMap.get(curr);
                if (parent != null && !visited.contains(parent)) {
                    visited.add(parent);
                    queue.offer(parent);
                }
            }

            currentDistance++;
        }

        return result;
    }

    private static void buildParentMap(TreeNode node, TreeNode parent, Map<TreeNode, TreeNode> parentMap) {
        if (node == null) return;
        parentMap.put(node, parent);
        buildParentMap(node.left, node, parentMap);
        buildParentMap(node.right, node, parentMap);
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 662 Index Normalization Formula
long normalizedIdx = curr.idx - firstIdx;
if (curr.node.left != null) queue.offer(new PairNode(curr.node.left, 2 * normalizedIdx + 1));
if (curr.node.right != null) queue.offer(new PairNode(curr.node.right, 2 * normalizedIdx + 2));
```

---

## 7. Concrete Problem Examples
* **LeetCode 543 - Diameter of Binary Tree**: Post-order DFS height sum.
* **LeetCode 662 - Maximum Width of Binary Tree**: Binary heap position indexing BFS.
* **LeetCode 863 - All Nodes Distance K in Binary Tree**: Parent mapping + Graph BFS.

---

## 8. Java Code Demonstration & Dry Run
Demonstration computing Diameter, Maximum Width, and Distance K nodes:

```java
public class TreeMetricsDemo {

    public static void main(String[] args) {
        // Build Tree: [1, 2, 3, 4, 5]
        TreeMetricsMaster.TreeNode root = new TreeMetricsMaster.TreeNode(1);
        root.left = new TreeMetricsMaster.TreeNode(2);
        root.right = new TreeMetricsMaster.TreeNode(3);
        root.left.left = new TreeMetricsMaster.TreeNode(4);
        root.left.right = new TreeMetricsMaster.TreeNode(5);

        System.out.println("=== 1. Diameter of Binary Tree (LeetCode 543) ===");
        System.out.println("Diameter: " + TreeMetricsMaster.diameterOfBinaryTree(root)); // Output: 3 (Path: 4 -> 2 -> 1 -> 3)

        System.out.println("\n=== 2. Maximum Width of Binary Tree (LeetCode 662) ===");
        System.out.println("Max Width: " + TreeMetricsMaster.widthOfBinaryTree(root)); // Output: 2

        System.out.println("\n=== 3. Distance K Nodes from Target (Target = 2, K = 1) ===");
        List<Integer> distK = TreeMetricsMaster.distanceK(root, root.left, 1);
        System.out.println("Nodes at Distance 1 from Node 2: " + distK); // Output: [4, 5, 1]
    }
}
```

---

## 9. Complexity Analysis

| Metric Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Diameter (543)** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack | Post-Order DFS Height Sum |
| **Max Width (662)** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Normalized Heap Index Position |
| **Distance K (863)** | **$O(N)$ Linear ⚡** | $O(N)$ Graph Space | Parent Map + Graph BFS |

---

## 10. Edge Cases & Boundary Handling
* **Single Node Tree**: Diameter is `0` (0 edges). Max width is `1`.
* **Deep Skewed Tree ($H = N$)**: Position index without normalization overflows 64-bit `long`! Index normalization (`curr.idx - firstIdx`) guarantees zero overflow.

---

## 11. Common Mistakes & Anti-Patterns
* **Measuring Diameter in Nodes instead of Edges**:
  - Some platforms define diameter as node count (`leftH + rightH + 1`). LeetCode 543 specifies **edge count** (`leftH + rightH`). Always check problem definitions!
* **Counting Width without NULL Gaps**: Counting only non-null nodes at a level violates LeetCode 662 rules! Null gaps between the leftmost and rightmost non-null nodes MUST be included using Heap Position Indexing (`lastIdx - firstIdx + 1`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Diameter Formula vs Height Return:
> In `diameterOfBinaryTree`:
> * **Local Diameter Update**: `maxDiameter = Math.max(maxDiameter, leftH + rightH)` (Sum of subtree heights).
> * **Height Return to Parent**: `return 1 + Math.max(leftH, rightH)` (Height of current node).

> **Memory Trick:** **"Local diameter = leftH + rightH; Returned height = 1 + max(leftH, rightH)!"**

---

## 13. System & Implementation Comparisons

| Feature | Binary Tree Diameter (543) | Binary Tree Max Width (662) |
| :--- | :--- | :--- |
| **Traversal Type** | Post-Order DFS | Level-Order Queue BFS |
| **State Encoding** | Height Integer | Heap Position Index (`2*idx+1`, `2*idx+2`) |
| **Null Gap Inclusion**| Irrelevant | **Mandatory Included ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find length of longest path between any two nodes in a tree"** $\rightarrow$ LeetCode 543 (Post-order DFS `leftH + rightH`).
* **"Find maximum width of binary tree including null gaps between end nodes"** $\rightarrow$ LeetCode 662 (BFS Heap Position Indexing `lastIdx - firstIdx + 1`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `leftH + rightH` give the diameter passing through a node?**  
  *A:* Because `leftH` is the number of edges on the longest downward path in the left subtree, and `rightH` is the number of edges on the longest downward path in the right subtree. Combining them forms the longest path passing through the current node.
* **Q: How does distance $K$ search (LeetCode 863) explore parent nodes?**  
  *A:* By pre-building a `parentMap<TreeNode, TreeNode>` using DFS. During BFS from the target node, we explore 3 directions at each step: `curr.left`, `curr.right`, and `parentMap.get(curr)`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY TREE DIAMETER, MAX WIDTH & DISTANCE METRICS    |
+-----------------------------------------------------------------------+
| • Diameter (543): Longest edge path between ANY two nodes             |
| • Local Diameter Update: maxDiameter = max(maxDiameter, leftH + rightH)|
| • Subtree Height Return: return 1 + max(leftH, rightH);               |
| • Max Width (662): BFS with Heap Position Indexing (2*idx+1, 2*idx+2) |
| • Normalized Index Formula: normIdx = curr.idx - firstIdx              |
| • Level Width: width = lastIdx - firstIdx + 1                         |
| • Distance K (863): Parent Map DFS -> 3-Direction Graph BFS           |
| • Complexity: All metric algorithms run in O(N) Linear Time           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `diameterOfBinaryTree` (LeetCode 543) in under 3 minutes.
- [ ] I can write `widthOfBinaryTree` (LeetCode 662) using position index normalization.
- [ ] I know why position indices must be normalized to prevent 64-bit overflow.
- [ ] I can write Distance K in Binary Tree (LeetCode 863) using parent map + BFS.
- [ ] I know why diameter measures edge count (`leftH + rightH`).
