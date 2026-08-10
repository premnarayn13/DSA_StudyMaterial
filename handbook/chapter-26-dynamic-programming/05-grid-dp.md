# 05. Grid DP: 2D Matrix Traversals, Path Optimization & Space Compression

## 1. Introduction
**Grid Dynamic Programming** is a central 2D DP pattern where subproblem states correspond to cells $(i, j)$ in an $M \times N$ matrix. In a typical grid DP scenario, an agent moves from top-left cell $(0, 0)$ to bottom-right cell $(M-1, N-1)$ using restricted movement directions (e.g. Right and Down). Grid DP addresses three primary problem archetypes: (1) **Path Counting** (e.g., Unique Paths $DP[i][j] = DP[i-1][j] + DP[i][j-1]$), (2) **Cost Minimization / Maximization** (e.g., Minimum Path Sum $DP[i][j] = \text{grid}[i][j] + \min(DP[i-1][j], DP[i][j-1])$), and (3) **Reverse / Multi-Agent Grid DP** (e.g., Dungeon Game & Cherry Pickup). By reducing 2D DP matrices to 1D DP rolling arrays, Grid DP algorithms execute in **$O(M \cdot N)$ Time Complexity** and **$O(N)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Grid DP:
> 1. **2D State Representation ($DP[i][j]$)**:
>    - $DP[i][j]$ represents the optimal cost, total paths, or remaining health to reach cell $(i, j)$ from origin $(0, 0)$ (or from cell $(i, j)$ to target).
> 2. **Standard Directional Transitions (Right & Down)**:
>    - Incoming transitions to cell $(i, j)$ come strictly from the Top cell $(i-1, j)$ and Left cell $(i, j-1)$:
>      $$DP[i][j] = \text{cost}[i][j] + \min(DP[i-1][j], DP[i][j-1])$$
> 3. **1D Space Compression Invariant**:
>    - Since state $DP[i][j]$ depends ONLY on the previous row $DP[i-1][j]$ and current row left cell $DP[i][j-1]$, the 2D grid $DP[M][N]$ can be compressed into a **1D Array $DP[N]$**:
>      $$DP[j] = \text{cost}[i][j] + \min(DP[j], DP[j-1])$$
> 4. **Obstacle Sentinel Rule**:
>    - If cell $(i, j)$ contains an obstacle, set $DP[i][j] = 0$ (for path counts) or $\infty$ (for min path sum). ⚡

```
Grid DP Transition Topology (Cell (i, j) Dependencies):

            [ Cell (i-1, j): TOP ]
                      │  (Down Step)
                      ▼
[ Cell (i, j-1): LEFT ] ──► [ Target Cell (i, j) ]
     (Right Step)

Transitions:
- Unique Paths     : DP[i][j] = DP[i-1][j] + DP[i][j-1]
- Minimum Path Sum : DP[i][j] = Grid[i][j] + min(DP[i-1][j], DP[i][j-1]) ⚡
```

---

## 2. Core Concepts & Grid DP Strategy Matrix

### 2.1 Grid DP Problem Variants Strategy Matrix
```
Grid DP Problem Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Grid Problem Variant  | Flow Direction    | State Transition  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Unique Paths (LC 62)**| Top-Left $\to$ Bottom| $DP[j] += DP[j-1]$| **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
| **Obstacles (LC 63)** | Top-Left $\to$ Bottom| $Obs ? 0 : DP[j]+DP[j-1]$| **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
| **Min Path Sum (LC 64)**| Top-Left $\to$ Bottom| $G[i][j] + \min(dp[j], dp[j-1])$| **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
| **Dungeon Game (LC 174)**| Bottom-Right $\to$ Top| Reverse Health DP | **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
| **Cherry Pickup (741)**| 2 Simultaneous Paths| $DP[r1][c1][r2]$   | $O(N^3)$          | $O(N^2)$ Table    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Grid DP cell (i,j) depends on Top cell (i-1, j) and Left cell (i, j-1)! Compress 2D table to 1D array dp[j] += dp[j-1]!"**

---

## 3. Characteristics & Reverse Grid DP Mathematical Proof

### 3.1 Mathematical Derivation of LeetCode 174 (Dungeon Game - Reverse Grid DP)
* A knight starts at $(0, 0)$ with initial health $H > 0$ and must reach $(M-1, N-1)$. Grid cells contain demons (negative values) or magic orbs (positive values). Health must NEVER drop $\le 0$ at any point.
* **Why Forward DP Fails**:
  - Forward DP from $(0, 0)$ needs to track TWO parameters at each cell: current health AND accumulated min health required. This violates the single-value subproblem invariant.
* **Reverse DP Formulation**:
  - Let $DP[i][j]$ be the **Minimum Health Required BEFORE entering cell $(i, j)$** to reach the destination and survive.
  - From cell $(i, j)$, knight can move Right $(i, j+1)$ or Down $(i+1, j)$.
  - Min health needed after leaving cell $(i, j)$:
    $$\text{minHealthOnExit} = \min(DP[i+1][j], DP[i][j+1])$$
  - Health needed before entering cell $(i, j)$:
    $$DP[i][j] = \max(1, \text{minHealthOnExit} - \text{grid}[i][j])$$
* Base Case at Destination $(M-1, N-1)$:
  $$DP[M-1][N-1] = \max(1, 1 - \text{grid}[M-1][N-1])$$
* Reverse DP evaluates from Bottom-Right to Top-Left in **$O(M \cdot N)$ Time and $O(N)$ Space**! ⚡

---

## 4. Internal Working Mechanics: 2D-to-1D Space Compression

How 2D Grid DP matrix $DP[M][N]$ is compressed to 1D Array $DP[N]$:

```
2D Matrix Representation:
Row i-1: [ ... | dp[i-1][j-1] | dp[i-1][j]   | ... ]
Row i  : [ ... | dp[i][j-1]   | dp[i][j] (X) | ... ]

1D Array In-Place Update:
Before evaluating index j: Array dp[] contains Row i-1 values!
- dp[j] holds top cell value dp[i-1][j]!
- dp[j-1] holds left cell value dp[i][j-1] (already updated for current row i)!

In-Place Formula: dp[j] = grid[i][j] + min(dp[j], dp[j-1])!
Space compressed from O(M * N) to O(N) seamlessly! ✅ ⚡
```

---

## 5. Visual Diagram: Dungeon Game Reverse Health Transition

```
Reverse Grid DP Traversal (Dungeon Game LC 174):

Target Destination (M-1, N-1): Grid = -5 ──► Health Required = max(1, 1 - (-5)) = 6!

[ Cell (i, j): Grid = -2 ] ◄── Replaced by min(Exit Right, Exit Down) ─── [ Target Health = 6 ]
                               Exit Required = 6 - (-2) = 8 Health!

Evaluates from Bottom-Right to Top-Left Origin (0, 0)! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Minimum Path Sum (LeetCode 64), Unique Paths II with Obstacles (LeetCode 63), Dungeon Game (LeetCode 174), and 1D Space Compression.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Grid DP Algorithms:
 * Minimum Path Sum, Unique Paths with Obstacles, Dungeon Game, and 1D Space Compression.
 */
public class GridDPProblemsMaster {

    // =========================================================================
    // 1. LEETCODE 64: MINIMUM PATH SUM (O(M * N) Time, O(N) 1D Space)
    // =========================================================================
    /**
     * Finds minimum path sum from top-left to bottom-right cell in grid.
     *
     * @param grid 2D matrix of non-negative numbers
     * @return minimum path sum
     */
    public int minPathSum(int[][] grid) {
        if (grid == null || grid.length == 0 || grid[0].length == 0) return 0;

        int m = grid.length;
        int n = grid[0].length;

        int[] dp = new int[n];
        dp[0] = grid[0][0];

        // Base Case Initialization: First Row
        for (int j = 1; j < n; j++) {
            dp[j] = dp[j - 1] + grid[0][j];
        }

        // Iterate remaining rows
        for (int i = 1; i < m; i++) {
            dp[0] += grid[i][0]; // First column transition (Down only)

            for (int j = 1; j < n; j++) {
                dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]); // Top vs Left! ⚡
            }
        }

        return dp[n - 1];
    }

    // =========================================================================
    // 2. LEETCODE 63: UNIQUE PATHS II WITH OBSTACLES (O(M * N) Time, O(N) Space)
    // =========================================================================
    /**
     * Calculates unique paths in grid containing obstacles (1 = obstacle, 0 = empty).
     */
    public int uniquePathsWithObstacles(int[][] obstacleGrid) {
        if (obstacleGrid == null || obstacleGrid.length == 0 || obstacleGrid[0][0] == 1) return 0;

        int m = obstacleGrid.length;
        int n = obstacleGrid[0].length;

        int[] dp = new int[n];
        dp[0] = 1; // Base case: starting origin

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (obstacleGrid[i][j] == 1) {
                    dp[j] = 0; // Obstacle blocks all paths! ⚡
                } else if (j > 0) {
                    dp[j] += dp[j - 1]; // Top + Left
                }
            }
        }

        return dp[n - 1];
    }

    // =========================================================================
    // 3. LEETCODE 174: DUNGEON GAME (REVERSE GRID DP O(M * N) Time, O(N) Space)
    // =========================================================================
    /**
     * Finds minimum initial health to survive dungeon from top-left to bottom-right.
     */
    public int calculateMinimumHP(int[][] dungeon) {
        if (dungeon == null || dungeon.length == 0) return 1;

        int m = dungeon.length;
        int n = dungeon[0].length;

        int[] dp = new int[n + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[n - 1] = 1; // Base sentinel boundary

        for (int i = m - 1; i >= 0; i--) {
            for (int j = n - 1; j >= 0; j--) {
                if (i == m - 1 && j == n - 1) {
                    dp[j] = Math.max(1, 1 - dungeon[i][j]);
                } else {
                    int minExitHealth = Math.min(dp[j], dp[j + 1]); // Down vs Right!
                    dp[j] = Math.max(1, minExitHealth - dungeon[i][j]);
                }
            }
        }

        return dp[0];
    }
}
```

> **Quick Syntax:**
```java
// Reverse Grid DP Dungeon Game Formula Line
int minExit = Math.min(dp[j], dp[j + 1]); dp[j] = Math.max(1, minExit - dungeon[i][j]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 64 - Minimum Path Sum**:
   - Standard 2D grid cost minimization benchmark ($O(M \cdot N)$ time, $O(N)$ space).

2. **LeetCode 63 - Unique Paths II**:
   - Grid path counting with obstacle sentinels ($O(N)$ 1D space).

3. **LeetCode 174 - Dungeon Game**:
   - Reverse Grid DP calculating minimum initial health ($O(M \cdot N)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class GridDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GRID DYNAMIC PROGRAMMING BENCHMARK DEMO      ");
        System.out.println("=================================================\n");

        GridDPProblemsMaster master = new GridDPProblemsMaster();

        // 1. Min Path Sum Test (LeetCode 64)
        int[][] grid = {
            {1, 3, 1},
            {1, 5, 1},
            {4, 2, 1}
        };

        int minSum = master.minPathSum(grid);
        System.out.println("1. LeetCode 64 Minimum Path Sum for Grid:");
        System.out.println("   Min Path Sum (1D Space): " + minSum + " (Path: 1->3->1->1->1)");
        System.out.println("-------------------------------------------------");

        // 2. Unique Paths II Test (LeetCode 63)
        int[][] obsGrid = {
            {0, 0, 0},
            {0, 1, 0},
            {0, 0, 0}
        };

        int paths = master.uniquePathsWithObstacles(obsGrid);
        System.out.println("2. LeetCode 63 Unique Paths II with Obstacle at (1,1):");
        System.out.println("   Total Valid Paths: " + paths + " Paths");
        System.out.println("-------------------------------------------------");

        // 3. Dungeon Game Test (LeetCode 174)
        int[][] dungeon = {
            {-2, -3, 3},
            {-5, -10, 1},
            {10, 30, -5}
        };

        int minHP = master.calculateMinimumHP(dungeon);
        System.out.println("3. LeetCode 174 Dungeon Game Minimum Initial HP:");
        System.out.println("   Minimum Required Initial Health: " + minHP + " HP");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Grid DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Minimum Path Sum (LC 64)** | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| `grid[i][j] + min(top, left)` |
| **Unique Paths II (LC 63)**  | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| Obstacle sets `dp[j] = 0` |
| **Dungeon Game (LC 174)**    | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| Reverse DP from $(M-1, N-1)$ |
| **Cherry Pickup (LC 741)**   | $O(N^3)$ | $O(N^2)$ Table | 2 simultaneous runners |

---

## 10. Edge Cases & Boundary Handling

1. **Obstacle at Origin $(0, 0)$ or Target $(M-1, N-1)$**:
   - `uniquePathsWithObstacles` returns 0 immediately.

2. **Single Row Grid ($M = 1$) or Single Column Grid ($N = 1$)**:
   - Handled cleanly in 1D array transitions.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running Forward DP on Dungeon Game**:
  - Forward DP requires tracking two parameters (current health and min health required), violating single-value subproblem state definitions. **ALWAYS use REVERSE GRID DP for Dungeon Game!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Grid DP Space Optimization Rule:
> Any 2D Grid DP where cell $(i, j)$ depends only on row $i-1$ and row $i$ can ALWAYS be compressed to a **1D Array $DP[N]$** by processing columns $j$ left-to-right! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Forward Grid DP | Reverse Grid DP |
| :--- | :--- | :--- |
| **Traversal Direction** | Top-Left $(0,0) \to$ Bottom-Right | Bottom-Right $(M-1,N-1) \to$ Top-Left |
| **Use Case** | Path Counting, Min/Max Cost | Survival Health Constraints (Dungeon) |
| **Space Complexity** | **$O(N)$ 1D Array ⚡** | **$O(N)$ 1D Array ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find minimum path sum from top-left to bottom-right cell in grid"** $\rightarrow$ LeetCode 64.
* **"Find minimum initial health required to reach destination in grid"** $\rightarrow$ LeetCode 174 (Reverse Grid DP).

---

## 15. Frequently Asked Interview Questions

* **Q: How does 1D space compression work in 2D Grid DP?**  
  *A:* By maintaining a 1D array `dp[N]` representing the current row. `dp[j]` stores the value from the top cell (previous row), and `dp[j-1]` stores the value from the left cell (already updated for the current row).

* **Q: Why does Dungeon Game require Reverse Grid DP?**  
  *A:* Because future health gains or losses dictate the minimum health needed before entering a cell. Reverse DP evaluates from destination back to origin seamlessly.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRID DP PROBLEMS                                      |
+-----------------------------------------------------------------------+
| • Unique Paths : dp[j] += dp[j-1] (Compress 2D to 1D Array)           |
| • Min Path Sum : dp[j] = grid[i][j] + min(dp[j], dp[j-1])             |
| • Obstacles    : If grid[i][j] == 1 -> dp[j] = 0 (Block path)         |
| • Dungeon Game : Reverse DP -> dp[j] = max(1, min(dp[j], dp[j+1]) - g)|
| • Performance  : O(M * N) Time | O(N) Auxiliary 1D Space ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Minimum Path Sum (LeetCode 64) with 1D space compression in Java.
- [ ] I can write Unique Paths II (LeetCode 63) with obstacle sentinels.
- [ ] I can write Reverse Grid DP for Dungeon Game (LeetCode 174).
- [ ] I can explain why 2D Grid DP can be compressed to 1D array $DP[N]$.
- [ ] I can explain why Dungeon Game requires Reverse DP.
