# 09. Rat in a Maze, Direction Vectors & Grid Backtracking Traversal

## 1. Introduction
**Rat in a Maze** is a classic 2D grid backtracking problem where a rat starts at the top-left corner `(0, 0)` of an $N \times N$ binary matrix and must navigate to the bottom-right destination corner `(N-1, N-1)`. The rat can move in 4 directions: **Down ('D')**, **Left ('L')**, **Right ('R')**, and **Up ('U')**, provided the cell contains `1` (open path) and is not blocked by `0` (wall). Backtracking using **Direction Vectors** and **In-Place Cell Masking (`maze[r][c] = 0`)** extracts all valid directional path strings in **$O(3^{N^2})$ Time** and **$O(N^2)$ Space**.

> **Important:** Core Invariants of Rat in a Maze:
> 1. **Lexicographical Direction Vectors**:
>    - Sort direction choices alphabetically: **Down ('D')**, **Left ('L')**, **Right ('R')**, **Up ('U')** to generate lexicographically sorted path output strings!
>    - Direction Arrays: `dRow = {1, 0, 0, -1}`, `dCol = {0, -1, 1, 0}`, `dChar = {'D', 'L', 'R', 'U'}`.
> 2. **In-Place Visited Cell Masking**:
>    - Mask visited path cell: `maze[r][c] = 0`.
>    - Recurse 4 directions.
>    - **BACKTRACK**: Restore `maze[r][c] = 1`!
> 3. **Base Case Destination Guard**:
>    - If `r == N - 1` AND `c == N - 1`: Add `path.toString()` to result list and return! ⚡

```
Rat in a Maze Grid Topology (N = 4):
Start Node (0, 0) ---> [D] ---> [R] ---> [D] ---> [D] ---> [R] ---> Target (3, 3)

Directional Path Generated: "DDRDRR"! ⚡
```

---

## 2. Core Concepts & Direction Vector Architecture

### 2.1 Lexicographical Direction Array Matrix
```
Direction Vector Table (Alphabetical Order: D, L, R, U):
+-----------------------+-------------------+-------------------+-------------------+
| Direction Char        | Row Change (`dRow`)| Col Change (`dCol`)| Lexicographical Id|
+-----------------------+-------------------+-------------------+-------------------+
| **'D' (Down)**        | **$+1$**          | $0$               | Index 0           |
| **'L' (Left)**        | $0$               | **$-1$**          | Index 1           |
| **'R' (Right)**       | $0$               | **$+1$**          | Index 2           |
| **'U' (Up)**          | **$-1$**          | $0$               | Index 3           |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Direction Loop Order: D (+1,0), L (0,-1), R (0,+1), U (-1,0) for automatic lexicographical path sorting!"**

---

## 3. Characteristics & $O(3^{N^2})$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(3^{N^2})$ Complexity
* An $N \times N$ matrix contains $N^2$ total cells.
* From each cell, the search branches into at most 3 valid unvisited directions (excluding the incoming parent cell).
* Maximum path depth in a simple non-self-intersecting grid path $\le N^2$.
* Total Time Complexity: $\mathbf{O(3^{N^2}) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Rat in a Maze on $4 \times 4$ Matrix:

```
Maze:
[1, 0, 0, 0]
[1, 1, 0, 1]
[1, 1, 0, 0]
[0, 1, 1, 1]

1. Start (0, 0): Mask maze[0][0] = 0.
   - Try 'D' -> Move to (1, 0): Valid! Mask maze[1][0] = 0, path = "D".
     - Try 'D' -> Move to (2, 0): Valid! Mask maze[2][0] = 0, path = "DD".
       - Try 'D' -> (3, 0) is 0 (Blocked!).
       - Try 'L' -> (2, -1) Out of Bounds.
       - Try 'R' -> Move to (2, 1): Valid! Mask maze[2][1] = 0, path = "DDR".
         - Try 'D' -> Move to (3, 1): Valid! Mask maze[3][1] = 0, path = "DDRD".
           - Try 'R' -> Move to (3, 2): Valid! Mask maze[3][2] = 0, path = "DDRDR".
             - Try 'R' -> Move to (3, 3): DESTINATION REACHED! Add "DDRDRR" to result!

Returns path "DDRDRR"! ✅ (O(3^{N^2}) Time!)
```

---

## 5. Visual Diagram
Maze Grid Traversal Topography:

```
(0,0) [R] -> (0,1) Blocked!
  |
  v [D]
(1,0) [R] -> (1,1) [D] -> (2,1) [D] -> (3,1) [R] -> (3,2) [R] -> (3,3) [TARGET!]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Rat in a Maze Problem using Direction Vectors:

```java
import java.util.*;

// Rat in a Maze Master Class
public class RatInMazeMaster {

    // Direction Vectors in Lexicographical Order: D, L, R, U
    private final int[] dRow = {1, 0, 0, -1};
    private final int[] dCol = {0, -1, 1, 0};
    private final char[] dChar = {'D', 'L', 'R', 'U'};

    // Find All Lexicographically Sorted Paths O(3^(N^2)) Time, O(N^2) Space
    public List<String> findPath(int[][] maze, int n) {
        List<String> result = new ArrayList<>();

        // Start cell or Destination cell blocked check
        if (maze == null || n == 0 || maze[0][0] == 0 || maze[n - 1][n - 1] == 0) {
            return result;
        }

        StringBuilder path = new StringBuilder();
        backtrackMaze(maze, n, 0, 0, path, result);

        return result;
    }

    private void backtrackMaze(int[][] maze, int n, int r, int c, 
                              StringBuilder path, List<String> result) {
        // Base Case: Reached Destination (N-1, N-1)!
        if (r == n - 1 && c == n - 1) {
            result.add(path.toString()); // Add valid directional path
            return;
        }

        // Step 1: CHOOSE (Mask cell in-place to prevent self-intersection)
        maze[r][c] = 0;

        // Step 2: RECURSE in 4 Lexicographical Directions (D, L, R, U)
        for (int i = 0; i < 4; i++) {
            int nextR = r + dRow[i];
            int nextC = c + dCol[i];

            // Boundary Check & Open Path Check
            if (nextR >= 0 && nextR < n && nextC >= 0 && nextC < n && maze[nextR][nextC] == 1) {
                path.append(dChar[i]);                                   // Push direction char
                backtrackMaze(maze, n, nextR, nextC, path, result);       // Recurse
                path.deleteCharAt(path.length() - 1);                     // Backtrack path string
            }
        }

        // Step 3: BACKTRACK (Restore cell in-place)
        maze[r][c] = 1;
    }
}
```

> **Quick Syntax:**
```java
// Direction Vector Loop Line
for (int i = 0; i < 4; i++) {
    int nr = r + dRow[i], nc = c + dCol[i];
    if (nr >= 0 && nr < n && nc >= 0 && nc < n && maze[nr][nc] == 1) { ... }
}
```

---

## 7. Concrete Problem Examples
* **Rat in a Maze Problem**: Primary grid maze navigation.
* **Robot Grid Traversal**: Autonomous pathfinding in grid obstacle maps.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `findPath`:

```java
public class RatInMazeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Rat in a Maze Test ===");
        RatInMazeMaster solver = new RatInMazeMaster();

        int n = 4;
        int[][] maze = {
            {1, 0, 0, 0},
            {1, 1, 0, 1},
            {1, 1, 0, 0},
            {0, 1, 1, 1}
        };

        List<String> paths = solver.findPath(maze, n);
        System.out.println("All Lexicographical Paths: " + paths);
        // Output: ["DDRDRR", "DRDDRR"] ✅
    }
}
```

---

## 9. Complexity Analysis

| Algorithm Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Rat in a Maze DFS** | **$O(3^{N^2})$ Exponential ⚡**| **$O(N^2)$ Call Stack Memory**| In-place cell masking `maze[r][c] = 0` |
| **BFS Shortest Path**| **$O(N^2)$ Linear ⚡** | **$O(N^2)$ Queue Memory** | FIFO Queue shortest path |

---

## 10. Edge Cases & Boundary Handling
* **Start Cell Blocked (`maze[0][0] == 0`)**: Returns empty list `[]` immediately.
* **Destination Cell Blocked (`maze[N-1][N-1] == 0`)**: Returns empty list `[]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Non-Alphabetical Direction Orders (e.g. U, D, L, R)**:
  - Non-alphabetical direction orders generate paths out of lexicographical order, failing strict online judge comparison tests.
  - **ALWAYS use alphabetical direction order: D, L, R, U**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Direction Vectors (`dRow`, `dCol`, `dChar`) Clean Up Code:
> Writing 4 separate `if-else` blocks for Down, Left, Right, Up duplicates 30 lines of code.
> Iterating through a single 4-element loop `for (int i = 0; i < 4; i++)` using `dRow[i]` and `dCol[i]` reduces method size to **10 lines of clean code**! ⚡

> **Memory Trick:** **"Use dRow = {1,0,0,-1} and dCol = {0,-1,1,0} to clean up grid navigation loops!"**

---

## 13. System & Implementation Comparisons

| Feature | Direction Vector Loop | Manual 4 `if` Blocks |
| :--- | :--- | :--- |
| **Code Length** | **~10 Lines Clean Code ⚡** | ~40 Lines Duplicated Code |
| **Lexicographical Order**| **Automatic via `dChar` array ⚡**| Manual ordering |
| **Maintainability** | High | Low |

---

## 14. How to Recognize This in Questions
* **"Find all valid directional paths (D, L, R, U) from top-left to bottom-right in grid"** $\rightarrow$ Rat in a Maze.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is the time complexity $O(3^{N^2})$ instead of $O(4^{N^2})$?**  
  *A:* Because from the second step onward, the rat cannot backtrack to the cell it just came from, limiting choices to at most 3 directions per cell.
* **Q: How does in-place masking `maze[r][c] = 0` prevent infinite loops?**  
  *A:* Setting `maze[r][c] = 0` makes the cell look like a wall, preventing subsequent recursive calls from revisiting the same cell on the current path.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RAT IN A MAZE                                         |
+-----------------------------------------------------------------------+
| • Directions     : dRow = {1, 0, 0, -1}, dCol = {0, -1, 1, 0}, dChar = {'D','L','R','U'}|
| • In-Place Mask  : maze[r][c] = 0; backtrack: maze[r][c] = 1;         |
| • Path String    : path.append(dChar[i]); deleteCharAt(path.length()-1);|
| • Base Case      : if (r == n - 1 && c == n - 1) result.add(path.toString());|
| • Performance    : O(3^(N^2)) Time | O(N^2) Stack Space ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Rat in a Maze in Java using direction vectors.
- [ ] I know why alphabetical direction order D, L, R, U is used.
- [ ] I can write in-place cell masking (`maze[r][c] = 0`).
- [ ] I can state the time complexity bounds ($O(3^{N^2})$).
- [ ] I can trace maze backtracking step by step.
