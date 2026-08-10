# 07. Rat in a Maze: Grid Pathfinding, Lexicographical Directions & Visited Reversions

## 1. Introduction
**Rat in a Maze** is a classic 2D matrix pathfinding problem solved via backtracking depth-first search. Given an $N \times N$ binary grid where cell `1` represents an open passable path and cell `0` represents a blocked wall, a rat starts at the top-left cell $(0, 0)$ and aims to reach the bottom-right destination cell $(N-1, N-1)$. The rat can move in 4 cardinal directions: **Down ('D')**, **Left ('L')**, **Right ('R')**, and **Up ('U')**. To prevent infinite cycles (looping endlessly between adjacent open cells), the algorithm maintains a 2D `visited[N][N]` boolean matrix operating under the **Visited Cell Backtracking Invariant**: mark `visited[r][c] = true` before exploring child steps, and unmark `visited[r][c] = false` when returning to backtrack. Rat in a Maze pathfinding executes in **$O(4^{N^2})$ Worst-Case Time Complexity** and **$O(N^2)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Rat in a Maze Backtracking:
> 1. **Lexicographical Direction Order ('D', 'L', 'R', 'U')**:
>    - Processing direction choices in strict alphabetical order (`'D'` $\to$ `'L'` $\to$ `'R'` $\to$ `'U'`) guarantees that all generated path strings are sorted in lexicographical order automatically!
> 2. **Visited Reversion Invariant**:
>    - Mark `visited[r][c] = true` upon entering cell $(r, c)$.
>    - Unmark `visited[r][c] = false` upon exiting cell $(r, c)$ to allow other path candidates to traverse through cell $(r, c)$!
> 3. **Boundary & Wall Pruning**:
>    - A move to cell $(nextR, nextC)$ is valid if and only if:
>      $$0 \le nextR < N \;\&\&\; 0 \le nextC < N \;\&\&\; \text{maze}[nextR][nextC] == 1 \;\&\&\; !\text{visited}[nextR][nextC]$$
> 4. **Early Termination vs All-Paths Search**:
>    - **Single Path Search**: Returns `boolean` immediately when destination is reached.
>    - **All Paths Search**: Appends current path to results and backtracks to find remaining paths! ⚡

```
Rat in a Maze 4-Directional Movement Vectors:

                [ Up 'U': (r-1, c) ]
                         ▲
                         │
[ Left 'L': (r, c-1) ] ──┼── [ Right 'R': (r, c+1) ]
                         │
                         ▼
               [ Down 'D': (r+1, c) ]

Lexicographical Order: Down 'D' -> Left 'L' -> Right 'R' -> Up 'U'! ⚡
```

---

## 2. Core Concepts & Grid Pathfinding Strategy Matrix

### 2.1 Grid Pathfinding Strategy Matrix
```
Grid Pathfinding Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pathfinding Strategy  | Search Objective  | Direction Order   | Visited Reversion?| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **All Paths (Backtrack)**| Lexicographical Paths| D, L, R, U      | **YES (Unmark) ⚡**| **$O(4^{N^2})$ Worst⚡**|
| **Single Path (DFS)** | First Valid Path  | Any Order         | **YES (Unmark) ⚡**| $O(N^2)$ Fast     |
| **Shortest Path (BFS)**| Shortest Steps    | Queue Level-order | NO (Permanent)    | $O(N^2)$ Linear   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Backtracking All Paths requires unmarking visited[r][c] = false; BFS Shortest Path uses permanent visited!"**

---

## 3. Characteristics & Visited Reversion Mathematical Proof

### 3.1 Mathematical Proof of Visited Reversion Requirement
* Consider maze where cell $(1, 1)$ lies at the intersection of two distinct valid paths to destination $(N-1, N-1)$:
  - Path 1: $(0,0) \to (1,0) \to (1,1) \to (2,1) \to (2,2)$
  - Path 2: $(0,0) \to (0,1) \to (1,1) \to (2,1) \to (2,2)$
* **Case 1: Without Visited Reversion (Permanent Marking)**:
  - Path 1 is explored first. Cell $(1, 1)$ is marked `visited[1][1] = true`.
  - When Path 1 completes, cell $(1, 1)$ remains marked `true`.
  - Path 2 starts from $(0, 0) \to (0, 1)$, but fails at $(1, 1)$ because `visited[1][1] == true`. Path 2 is falsely destroyed!
* **Case 2: With Visited Reversion (`visited[r][c] = false`)**:
  - Path 1 finishes and unmarks `visited[1][1] = false` during backtracking.
  - Path 2 reaches $(1, 1)$, finds `visited[1][1] == false`, and successfully completes!
* Visited Reversion is MANDATORY for generating ALL valid path configurations! ⚡

---

## 4. Internal Working Mechanics: 4-Directional DFS Execution

Tracing Rat in a Maze for $4 \times 4$ Matrix:

```
Maze Matrix:
[1, 0, 0, 0]
[1, 1, 0, 1]
[1, 1, 0, 0]
[0, 1, 1, 1]

Start (0,0): Move Down 'D' -> (1,0)
From (1,0): Try 'D' -> (2,0). From (2,0): Try 'D' -> (3,0) Wall '0'!
            Try 'L' -> Out! Try 'R' -> (2,1).
From (2,1): Try 'D' -> (3,1). From (3,1): Try 'R' -> (3,2) -> Try 'R' -> (3,3) DESTINATION REACHED! ✅

Path 1 Formed: "DDRDRR"

Backtrack to explore alternative branches...
Path 2 Formed: "DRDDRR" ✅ ⚡
```

---

## 5. Visual Diagram: Visited Reversion Backtracking Cycle

```
Visited State Cycle for Cell (r, c):

[ Enter Cell (r, c) ] ──► Mark visited[r][c] = true ──► [ Explore Children (D, L, R, U) ]
                                                                   │
[ Revert visited[r][c] = false ] ◄── Unchoose (Backtrack!) ────────┘

Restores grid state for remaining path traversals! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Rat in a Maze All Paths Generator (GeeksForGeeks Benchmark), Single Path Solver, and Path Validation Engines.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Rat in a Maze Backtracking:
 * 4-Directional Traversals, Lexicographical Ordering, and Visited Reversions.
 */
public class RatInAMazeMaster {

    private static final int[] DIR_ROW = {1, 0, 0, -1}; // Down, Left, Right, Up
    private static final int[] DIR_COL = {0, -1, 1, 0};
    private static final char[] DIR_CHAR = {'D', 'L', 'R', 'U'}; // Lexicographical! ⚡

    // =========================================================================
    // 1. ALL PATHS RAT IN A MAZE SOLVER (O(4^(N^2)) Time, O(N^2) Space)
    // =========================================================================
    /**
     * Finds all valid paths from (0,0) to (N-1, N-1) in lexicographical order.
     *
     * @param maze N x N binary matrix (1 = open, 0 = wall)
     * @return list of path strings (e.g. ["DDRDRR", "DRDDRR"])
     */
    public List<String> findPath(int[][] maze) {
        List<String> results = new ArrayList<>();
        if (maze == null || maze.length == 0 || maze[0][0] == 0) return results;

        int n = maze.length;
        if (maze[n - 1][n - 1] == 0) return results; // Destination blocked!

        boolean[][] visited = new boolean[n][n];
        StringBuilder currentPath = new StringBuilder();

        visited[0][0] = true; // Mark origin
        ratInAMazeDFS(maze, 0, 0, n, visited, currentPath, results);
        return results;
    }

    private void ratInAMazeDFS(int[][] maze, int r, int c, int n, boolean[][] visited, StringBuilder path, List<String> results) {
        // Base Case: Destination cell (N-1, N-1) reached!
        if (r == n - 1 && c == n - 1) {
            results.add(path.toString()); // Capture path string ⚡
            return;
        }

        // Iterate in Lexicographical Order: 'D', 'L', 'R', 'U'
        for (int i = 0; i < 4; i++) {
            int nextR = r + DIR_ROW[i];
            int nextC = c + DIR_COL[i];

            // Boundary & Wall Pruning Check
            if (isValidMove(maze, nextR, nextC, n, visited)) {
                // Choose
                visited[nextR][nextC] = true;
                path.append(DIR_CHAR[i]);

                // Explore
                ratInAMazeDFS(maze, nextR, nextC, n, visited, path, results);

                // Unchoose (Visited Reversion Backtrack!) ⚡
                path.deleteCharAt(path.length() - 1);
                visited[nextR][nextC] = false;
            }
        }
    }

    private boolean isValidMove(int[][] maze, int r, int c, int n, boolean[][] visited) {
        return r >= 0 && r < n && c >= 0 && c < n && maze[r][c] == 1 && !visited[r][c];
    }

    // =========================================================================
    // 2. SINGLE PATH FAST SEARCH (Early Termination O(N^2) Time)
    // =========================================================================
    /**
     * Finds the first valid path and terminates search immediately.
     */
    public String findSinglePath(int[][] maze) {
        if (maze == null || maze.length == 0 || maze[0][0] == 0) return "";
        int n = maze.length;
        boolean[][] visited = new boolean[n][n];
        StringBuilder path = new StringBuilder();

        visited[0][0] = true;
        if (singlePathDFS(maze, 0, 0, n, visited, path)) {
            return path.toString();
        }
        return "";
    }

    private boolean singlePathDFS(int[][] maze, int r, int c, int n, boolean[][] visited, StringBuilder path) {
        if (r == n - 1 && c == n - 1) return true; // Destination reached! ⚡

        for (int i = 0; i < 4; i++) {
            int nextR = r + DIR_ROW[i];
            int nextC = c + DIR_COL[i];

            if (isValidMove(maze, nextR, nextC, n, visited)) {
                visited[nextR][nextC] = true;
                path.append(DIR_CHAR[i]);

                if (singlePathDFS(maze, nextR, nextC, n, visited, path)) {
                    return true; // Early Termination! ⚡
                }

                path.deleteCharAt(path.length() - 1);
                visited[nextR][nextC] = false;
            }
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Visited Reversion Lines
visited[nextR][nextC] = true; ratInAMazeDFS(...); visited[nextR][nextC] = false;
```

---

## 7. Concrete Problem Examples & Applications

1. **Rat in a Maze (GeeksForGeeks Benchmark)**:
   - Primary 4-directional matrix pathfinding benchmark ($O(4^{N^2})$ time).

2. **Word Search (LeetCode 79)**:
   - 2D grid character backtracking using visited cell reversion.

3. **Robot Vacuum & Autonomous Maze Navigation**:
   - Physical maze exploration using backtracking path reversal.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class RatInAMazeDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   RAT IN A MAZE BACKTRACKING BENCHMARK DEMO     ");
        System.out.println("=================================================\n");

        RatInAMazeMaster master = new RatInAMazeMaster();

        int[][] maze = {
            {1, 0, 0, 0},
            {1, 1, 0, 1},
            {1, 1, 0, 0},
            {0, 1, 1, 1}
        };

        // 1. All Paths Test
        List<String> paths = master.findPath(maze);
        System.out.println("1. All Valid Lexicographical Paths in 4x4 Maze:");
        System.out.println("   Total Paths Found: " + paths.size() + " Paths");
        System.out.println("   Paths List = " + paths);
        System.out.println("-------------------------------------------------");

        // 2. Single Path Fast Search Test
        String singlePath = master.findSinglePath(maze);
        System.out.println("2. Single Path Search (Early Termination):");
        System.out.println("   First Path Found = \"" + singlePath + "\"");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Rat in a Maze Search | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **All Paths Search** | $\mathbf{O(4^{N^2})}$ Exponential⚡| $\mathbf{O(N^2)}$ Matrix Space| Visited reversion `false` |
| **Single Path Search**| $O(N^2)$ Pruned | $\mathbf{O(N^2)}$ Matrix Space| Early return `true` |
| **Shortest Path BFS** | $\mathbf{O(N^2)}$ Linear ⚡| $\mathbf{O(N^2)}$ Queue Space| Permanent visited |

---

## 10. Edge Cases & Boundary Handling

1. **Origin (0,0) or Target (N-1, N-1) Blocked (`maze[0][0] == 0`)**:
   - Returns empty list `[]` immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Visited Cell Reversion (`visited[r][c] = false`)**:
  - Leaving `visited[r][c] = true` permanently prevents alternative valid path candidates from traversing shared open cells. **ALWAYS reset `visited[r][c] = false` during backtracking!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Lexicographical Direction Rule:
> To generate path strings in strict alphabetical order, process movement vectors in the exact order: **Down ('D') $\to$ Left ('L') $\to$ Right ('R') $\to$ Up ('U')**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | All Paths Backtracking | Shortest Path BFS |
| :--- | :--- | :--- |
| **Objective** | All Lexicographical Paths | Single Minimum Length Path |
| **Visited Reversion** | **YES (`visited = false`) ⚡** | NO (Permanent `visited = true`) |
| **Time Complexity** | $O(4^{N^2})$ Exponential | **$O(N^2)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find all valid paths for rat moving in grid from top-left to bottom-right"** $\rightarrow$ Rat in a Maze.
* **"Find word in 2D board of letters"** $\rightarrow$ LeetCode 79 (Word Search).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Rat in a Maze process directions in the order D, L, R, U?**  
  *A:* Because 'D' < 'L' < 'R' < 'U' alphabetically, which guarantees that all output path strings are sorted in lexicographical order without requiring additional sorting.

* **Q: Why must visited cells be un-marked during backtracking?**  
  *A:* Because a cell can be part of multiple different valid paths. Unmarking `visited[r][c] = false` allows other path searches to use the cell.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RAT IN A MAZE                                         |
+-----------------------------------------------------------------------+
| • Direction Vector : 'D' (1,0), 'L' (0,-1), 'R' (0,1), 'U' (-1,0)     |
| • Visited Invariant: visited[r][c] = true -> DFS -> visited[r][c] = false|
| • Pruning Check    : 0 <= r < N && 0 <= c < N && maze[r][c]==1 && !vis|
| • Lexicographical  : Process directions D -> L -> R -> U              |
| • Performance      : O(4^(N^2)) Worst Time | O(N^2) Space ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Rat in a Maze All Paths in Java.
- [ ] I can write Single Path Search with early termination.
- [ ] I can state the 4 direction vectors in lexicographical order.
- [ ] I can explain why visited cell reversion is required.
- [ ] I can state the boundary and wall pruning condition.
