# 03. Depth-First Search (DFS), Backtracking Traversal & Grid Flood-Fill Engines

## 1. Introduction
**Depth-First Search (DFS)** is a fundamental graph exploration strategy that traverses as deep as possible along each branch before backtracking. Powered by **Call Stack Recursion** or an explicit LIFO Stack (`Stack<Integer>`), DFS is the primary engine for **Grid Flood-Fill**, **Number of Islands (LeetCode 200)**, **Max Area of Island (LeetCode 695)**, **Clone Graph (LeetCode 133)**, and **Cycle Detection**. DFS executes in **$O(V + E)$ Linear Time** and **$O(V)$ Call Stack Memory Space**.

> **Important:** Core Invariants of Graph DFS:
> 1. **Deep Path Traversal**: Explores child branch $u \to v$ to its terminal end before returning to backtrack through alternative branches.
> 2. **Visited Guard Invariant**: Mark `visited[u] = true` IMMEDIATELY upon entering `dfs(u)` to prevent infinite recursion in cyclic graphs!
> 3. **Grid Flood-Fill Pattern**: In 2D grid problems (LeetCode 200), mutate `grid[r][c] = '0'` (sink visited land) to achieve $O(1)$ auxiliary space without an explicit visited array! ⚡

```
Graph DFS Deep Branch Exploration Topology (Source = Node 0):
                              [ Node 0 ]
                             /          \
                     [ Node 1 ]        [ Node 2 ]
                        /                  \
                [ Node 3 ]                [ Node 4 ]

Traversal Path: 0 -> 1 -> 3 (Terminal! Backtrack to 1 -> 0) -> 2 -> 4 (Terminal!) ⚡
```

---

## 2. Core Concepts & Grid Flood-Fill Architecture

### 2.1 DFS Operational Patterns Matrix
```
DFS Operational Patterns Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| DFS Pattern           | Visited Guard     | Return Value      | Primary Problem   |
+-----------------------+-------------------+-------------------+-------------------+
| **Grid Flood-Fill**   | `grid[r][c] = '0'`| Area / Count      | Islands (200/695) |
| **Clone Graph (133)** | `Map<Node, Node>` | Cloned Node       | Deep Copy Graph   |
| **Backtracking DFS**  | Visited Array / Set| Path Sequence     | Path Searching    |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Graph DFS: Recurse deep along each branch! Sink grid cells (grid[r][c] = '0') for O(1) space flood-fill!"**

---

## 3. Characteristics & $O(V + E)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(V + E)$ DFS Complexity
* Every vertex $v \in V$ is visited and marked `visited[v] = true` exactly ONCE $\implies \mathbf{O(V)}$ function calls.
* For each vertex $u$, DFS iterates over all outgoing edges $(u, v)$ in its adjacency list.
* Across all recursive frames, every edge $e \in E$ is traversed at most once (directed) or twice (undirected) $\implies \mathbf{O(E)}$ edge lookups.
* Total Time Complexity: $\mathbf{O(V + E) \text{ Strict Linear Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 200 Number of Islands DFS on Grid:

```
Grid:
[ '1', '1', '0' ]
[ '1', '0', '0' ]
[ '0', '0', '1' ]

Outer Loop finds '1' at (0, 0): Increment islandCount = 1. Call dfs(0, 0):
- (0, 0): Sink grid[0][0] = '0'. Recurse (1, 0) and (0, 1).
- (1, 0): Sink grid[1][0] = '0'. Neighbors are water. Return.
- (0, 1): Sink grid[0][1] = '0'. Neighbors are water. Return.
First island completely sunk!

Outer Loop finds '1' at (2, 2): Increment islandCount = 2. Call dfs(2, 2):
- (2, 2): Sink grid[2][2] = '0'. Return.

Total Islands = 2! Executed in O(M * N) time! ✅
```

---

## 5. Visual Diagram
Grid Flood-Fill Sink Topography:

```
Before DFS at (0, 0):                   After DFS at (0, 0) (Island Sunk!):
[ '1', '1', '0' ]                       [ '0', '0', '0' ]
[ '1', '0', '0' ]  ==================>  [ '0', '0', '0' ]
[ '0', '0', '1' ]                       [ '0', '0', '1' ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 200 (Number of Islands) and LeetCode 133 (Clone Graph):

```java
import java.util.*;

public class GraphDFSMaster {

    // Node definition for LeetCode 133 Clone Graph
    public static class Node {
        public int val;
        public List<Node> neighbors;
        public Node(int val) {
            this.val = val;
            this.neighbors = new ArrayList<>();
        }
    }

    // 1. LeetCode 200: Number of Islands (Grid DFS Flood-Fill) O(M * N) Time
    public int numIslands(char[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) return 0;

        int rows = grid.length;
        int cols = grid[0].length;
        int islandCount = 0;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    islandCount++;
                    dfsSinkIsland(grid, r, c); // Sink entire island via DFS
                }
            }
        }

        return islandCount;
    }

    private void dfsSinkIsland(char[][] grid, int r, int c) {
        // Boundary Check & Water Check
        if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length || grid[r][c] == '0') {
            return;
        }

        grid[r][c] = '0'; // Sink land cell (Mark visited in-place!)

        // Recurse in 4 orthogonal directions
        dfsSinkIsland(grid, r + 1, c);
        dfsSinkIsland(grid, r - 1, c);
        dfsSinkIsland(grid, r, c + 1);
        dfsSinkIsland(grid, r, c - 1);
    }

    // 2. LeetCode 133: Clone Graph (DFS with Hash Map) O(V + E) Time
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Node, Node> visitedMap = new HashMap<>();
        return dfsClone(node, visitedMap);
    }

    private Node dfsClone(Node node, Map<Node, Node> visitedMap) {
        if (visitedMap.containsKey(node)) {
            return visitedMap.get(node); // Return existing cloned node
        }

        // Create deep copy of node
        Node clone = new Node(node.val);
        visitedMap.put(node, clone);

        // Recursively clone all neighbors
        for (Node neighbor : node.neighbors) {
            clone.neighbors.add(dfsClone(neighbor, visitedMap));
        }

        return clone;
    }
}
```

> **Quick Syntax:**
```java
// Grid DFS Flood-Fill Sinking Line
if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == '0') return;
grid[r][c] = '0'; // Sink land cell
```

---

## 7. Concrete Problem Examples
* **LeetCode 200 - Number of Islands**: Primary grid DFS.
* **LeetCode 695 - Max Area of Island**: Subtree size calculation via DFS.
* **LeetCode 133 - Clone Graph**: Deep copy graph traversal.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 200 `numIslands`:

```java
public class GraphDFSDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 200 Number of Islands DFS Test ===");
        GraphDFSMaster solver = new GraphDFSMaster();

        char[][] grid = {
            {'1','1','0','0','0'},
            {'1','1','0','0','0'},
            {'0','0','1','0','0'},
            {'0','0','0','1','1'}
        };

        int islandCount = solver.numIslands(grid);
        System.out.println("Total Number of Islands: " + islandCount); // Output: 3 ✅
    }
}
```

---

## 9. Complexity Analysis

| DFS Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Grid Flood-Fill (200)** | **$O(M \cdot N)$ Linear ⚡**| **$O(M \cdot N)$ Stack Space**| In-place cell sinking `grid[r][c] = '0'` |
| **Clone Graph (133)** | **$O(V + E)$ Linear ⚡**| **$O(V)$ Map & Stack** | `Map<Node, Node>` visited tracking |

---

## 10. Edge Cases & Boundary Handling
* **Grid Full of Water (`'0'`)**: Returns `0` islands immediately.
* **Entire Grid is 1 Single Island**: Sinks all cells in 1 recursive DFS pass, returning `1`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Boundary Checks in Grid DFS**:
  - Accessing `grid[r][c]` without checking `r >= 0 && r < rows && c >= 0 && c < cols` causes `ArrayIndexOutOfBoundsException`.
  - **ALWAYS perform boundary guards BEFORE dereferencing `grid[r][c]`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why In-Place Sinking (`grid[r][c] = '0'`) Saves Memory:
> Allocating a `boolean[][] visited` array for a $1000 \times 1000$ grid requires 1 MB of extra memory.
> Mutating `grid[r][c] = '0'` directly marks visited land cells in-place, reducing auxiliary space to $O(1)$ extra space (excluding call stack)! ⚡

> **Memory Trick:** **"Sink grid cells (grid[r][c] = '0') in-place to eliminate boolean[][] visited array space!"**

---

## 13. System & Implementation Comparisons

| Feature | Depth-First Search (DFS) | Breadth-First Search (BFS) |
| :--- | :--- | :--- |
| **Implementation** | **Clean Recursion / Stack ⚡** | Iterative Queue Loop |
| **Unweighted Shortest Path**| No Shortest Path Guarantee | **Guaranteed Shortest Path ⚡**|
| **Memory Footprint** | $O(\text{Depth})$ Recursion Stack | $O(\text{Width})$ Queue Buffer |

---

## 14. How to Recognize This in Questions
* **"Count connected island components or compute maximum area in 2D grid"** $\rightarrow$ DFS Flood-Fill.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is DFS preferred over BFS for island flood-fill problems?**  
  *A:* Because recursive DFS requires significantly less code (~10 lines) than iterative BFS queue management.
* **Q: How does LeetCode 133 (Clone Graph) prevent infinite loops in cyclic graphs?**  
  *A:* By storing original nodes mapped to cloned nodes in a `Map<Node, Node> visitedMap`. If a node is already in the map, its existing clone is returned immediately.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DEPTH-FIRST SEARCH (DFS)                              |
+-----------------------------------------------------------------------+
| • Recurse Deep    : Explores branch to terminal leaf before backtracking|
| • Grid Flood-Fill : Sink visited land cells in-place: grid[r][c] = '0'|
| • Boundary Guard  : Check (r < 0 || r >= rows || c < 0 || c >= cols)  |
| • Clone Graph (133): Map<Node, Node> prevents cyclic infinite loops   |
| • Time Bounds     : O(V + E) Linear Time | O(V) Call Stack Memory ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 200 (`Number of Islands`) using DFS flood-fill.
- [ ] I can write LeetCode 695 (`Max Area of Island`) in Java.
- [ ] I can write LeetCode 133 (`Clone Graph`) using DFS.
- [ ] I know why in-place sinking (`grid[r][c] = '0'`) saves memory.
- [ ] I can trace DFS call stack execution step by step.
