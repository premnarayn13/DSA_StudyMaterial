# 14. Advanced Matrix Algorithms

## 1. Introduction
Advanced matrix algorithms tackle complex structural modifications, searching, and optimization problems on 2D grids. In technical interviews, problems such as Search in a 2D Matrix (LeetCode 74 / 240), Set Matrix Zeroes (LeetCode 73), Game of Life (LeetCode 289), and 2D Prefix Sum Range Queries (LeetCode 304) test a candidate's ability to achieve optimal time complexities ($O(R + C)$ or $O(\log(R \cdot C))$) and $O(1)$ auxiliary space by leveraging mathematical search properties and in-place state encoding tricks.

> **Important:** In-place matrix modification problems (like Set Matrix Zeroes or Game of Life) forbid allocating an extra $R \times C$ grid. Use **Row 0 and Column 0 as in-place storage flags** or **bitwise state transition encoding** to achieve $O(1)$ space!

## 2. Core Concepts
* **Search in Row-and-Column Sorted Matrix (Staircase Search)**: Starting search at the **top-right corner** `(0, C-1)` or **bottom-left corner** `(R-1, 0)`. At each step, eliminate an entire row or column, achieving $O(R + C)$ search time.
* **In-Place State Encoding**: Using auxiliary bit states or special character markers (e.g., `-1`, `2`, `3`) to store current AND previous cell states simultaneously in $O(1)$ space.
* **2D Prefix Sum (Region Sum Query)**: Precomputing a 2D prefix sum grid $P$ to answer any sub-matrix sum query $(r_1, c_1)$ to $(r_2, c_2)$ in constant $O(1)$ time.
  $$P[r][c] = \text{val} + P[r-1][c] + P[r][c-1] - P[r-1][c-1]$$

> **Memory Trick for Staircase Search:** **"Start at Top-Right (0, C-1). If target < cell, go LEFT (c--); if target > cell, go DOWN (r++)"**.

## 3. Characteristics / Properties
* **Staircase Search Property**: Top-Right cell `(0, C-1)` acts as a Decision Node—elements to its left are smaller; elements below it are larger.
* **2D Sub-matrix Sum Formula**:
  $$\text{Sum}((r_1, c_1) \dots (r_2, c_2)) = P[r_2][c_2] - P[r_1-1][c_2] - P[r_2][c_1-1] + P[r_1-1][c_1-1]$$

```
Matrix Algorithm Strategy Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Matrix Problem        | Naive / Extra Space| Optimal Strategy  | Time / Space      |
+-----------------------+-------------------+-------------------+-------------------+
| Search 2D Matrix II   | O(R * C)          | Staircase Search  | O(R + C) | O(1)   |
| Set Matrix Zeroes     | O(R * C) space    | Row 0 / Col 0 Flag| O(R * C) | O(1)⚡ |
| Game of Life          | O(R * C) copy grid| 2-Bit State Mask  | O(R * C) | O(1)⚡ |
| 2D Range Sum Query    | O(R * C) query    | 2D Prefix Sum     | O(1) query | O(RC)|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Staircase Search for `target = 5` on a Sorted Matrix ($4 \times 4$):

```
Matrix:
[ 1,  4,  7, 11 ]
[ 2,  5,  8, 12 ]
[ 3,  6,  9, 16 ]
[ 10, 13, 14, 17 ]

Start at Top-Right: r = 0, c = 3 (Cell val = 11)
Target 5 < 11 -> Move LEFT (c = 2)

Cell (0, 2) val = 7
Target 5 < 7  -> Move LEFT (c = 1)

Cell (0, 1) val = 4
Target 5 > 4  -> Move DOWN (r = 1)

Cell (1, 1) val = 5
Target 5 == 5 -> FOUND AT (1, 1)! ✅ (Total steps = 4 comparisons!)
```

## 5. Visual Diagram
Staircase Search Decision Flow (Top-Right Start):

```
                 (0, C-1) Top-Right Node
                     /          \
              <-- Smaller      Larger -->
             (Move LEFT)       (Move DOWN)
                c--               r++

Eliminates an entire column or row in a single step!
```

## 6. Operations / Algorithms
In-Place Set Matrix Zeroes Algorithm (LeetCode 73):

```java
public void setZeroes(int[][] matrix) {
    int R = matrix.length, C = matrix[0].length;
    boolean firstRowZero = false, firstColZero = false;

    // Check if first row or first col need to be zeroed
    for (int c = 0; c < C; c++) if (matrix[0][c] == 0) firstRowZero = true;
    for (int r = 0; r < R; r++) if (matrix[r][0] == 0) firstColZero = true;

    // Use Row 0 and Col 0 as in-place storage flags
    for (int r = 1; r < R; r++) {
        for (int c = 1; c < C; c++) {
            if (matrix[r][c] == 0) {
                matrix[r][0] = 0;
                matrix[0][c] = 0;
            }
        }
    }

    // Zero out cells based on flags
    for (int r = 1; r < R; r++) {
        for (int c = 1; c < C; c++) {
            if (matrix[r][0] == 0 || matrix[0][c] == 0) {
                matrix[r][c] = 0;
            }
        }
    }

    // Zero out first row and first col if flagged
    if (firstRowZero) for (int c = 0; c < C; c++) matrix[0][c] = 0;
    if (firstColZero) for (int r = 0; r < R; r++) matrix[r][0] = 0;
}
```

> **Quick Syntax:**
```java
// 2D Prefix Sum Formula (1-indexed dp array)
dp[r][c] = matrix[r-1][c-1] + dp[r-1][c] + dp[r][c-1] - dp[r-1][c-1];

// 2D Sub-matrix Range Sum Formula (r1, c1) to (r2, c2)
int sum = dp[r2+1][c2+1] - dp[r1][c2+1] - dp[r2+1][c1] + dp[r1][c1];
```

## 7. Examples
* **LeetCode 240 - Search a 2D Matrix II**: Search in matrix where rows and columns are independently sorted in $O(R + C)$ time.
* **LeetCode 73 - Set Matrix Zeroes**: Set entire row and column to 0 using $O(1)$ space.
* **LeetCode 304 - Range Sum Query 2D (Immutable)**: 2D Prefix sum array answering sub-matrix sum queries in $O(1)$ time.

## 8. Java Code
Complete interview-ready Java suite implementing Staircase Matrix Search, In-Place Set Matrix Zeroes, and 2D Prefix Sum Range Queries:

```java
import java.util.Arrays;

public class AdvancedMatrixAlgorithmsMaster {

    // 1. Staircase Search in 2D Matrix II (LeetCode 240) O(R + C) Time, O(1) Space
    public static boolean searchMatrix(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return false;

        int R = matrix.length;
        int C = matrix[0].length;

        // Start at Top-Right Corner
        int r = 0, c = C - 1;

        while (r < R && c >= 0) {
            if (matrix[r][c] == target) {
                return true; // Target found
            }
            if (matrix[r][c] > target) {
                c--; // Target is smaller -> move LEFT
            } else {
                r++; // Target is larger -> move DOWN
            }
        }

        return false; // Target not present
    }

    // 2. 2D Prefix Sum (LeetCode 304) O(R * C) Precompute, O(1) Query Time
    static class NumMatrix {
        private long[][] dp;

        public NumMatrix(int[][] matrix) {
            if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return;
            int R = matrix.length, C = matrix[0].length;
            dp = new long[R + 1][C + 1];

            for (int r = 1; r <= R; r++) {
                for (int c = 1; c <= C; c++) {
                    dp[r][c] = matrix[r - 1][c - 1] 
                             + dp[r - 1][c] 
                             + dp[r][c - 1] 
                             - dp[r - 1][c - 1];
                }
            }
        }

        public long sumRegion(int r1, int c1, int r2, int c2) {
            return dp[r2 + 1][c2 + 1] 
                 - dp[r1][c2 + 1] 
                 - dp[r2 + 1][c1] 
                 + dp[r1][c1];
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[][] sortedMatrix = {
            {1,  4,  7, 11},
            {2,  5,  8, 12},
            {3,  6,  9, 16},
            {10, 13, 14, 17}
        };

        System.out.println("Search 5: " + searchMatrix(sortedMatrix, 5));   // true
        System.out.println("Search 15: " + searchMatrix(sortedMatrix, 15)); // false

        // Test 2D Prefix Sum
        int[][] grid = {
            {3, 0, 1, 4, 2},
            {5, 6, 3, 2, 1},
            {1, 2, 0, 1, 5},
            {4, 1, 0, 1, 7},
            {1, 0, 3, 0, 5}
        };
        NumMatrix numMatrix = new NumMatrix(grid);
        System.out.println("Submatrix Sum (2,1) to (4,3): " + numMatrix.sumRegion(2, 1, 4, 3)); // Output: 8
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Technique |
| :--- | :--- | :--- | :--- |
| **Staircase Search (Search 2D II)**| **$O(R + C)$** | **$O(1)$** | Top-Right decision node traversal |
| **Set Matrix Zeroes In-Place** | **$O(R \cdot C)$**| **$O(1)$** | Uses Row 0 and Col 0 as flag storage |
| **2D Prefix Sum Precomputation**| $O(R \cdot C)$ | $O(R \cdot C)$ | Inclusion-Exclusion DP formula |
| **2D Sub-matrix Region Query** | **$O(1)$** | **$O(1)$** | 4-term 2D prefix arithmetic |

## 10. Edge Cases
* **Target Smaller than Minimum (matrix[0][0]) / Larger than Maximum (matrix[R-1][C-1])**: Staircase search exits bounds immediately in $O(1)$ time.
* **Single Cell Matrix ($1 \times 1$)**: Works cleanly without index errors.
* **All Zeros Matrix**: Set Matrix Zeroes handles correctly without double-flagging issues.

## 11. Common Mistakes
* Starting Staircase Search at Top-Left `(0,0)` or Bottom-Right `(R-1, C-1)` (Top-Left has both right and down as larger values, so you cannot make a deterministic decision!). You MUST start at **Top-Right `(0, C-1)`** or **Bottom-Left `(R-1, 0)`**.
* Overwriting Row 0 or Col 0 flags prematurely in Set Matrix Zeroes before checking the rest of the matrix.
* Forgetting to add back `P[r1-1][c1-1]` in the 2D Sub-matrix Sum formula (subtracts overlapping region twice!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why can't you start Staircase Search at `(0,0)` (Top-Left)?
> Because moving right INCREASES values, and moving down ALSO INCREASES values. At `(0,0)`, if `target > matrix[0][0]`, you don't know whether to move right or down! Top-Right `(0, C-1)` works because moving left DECREASES values while moving down INCREASES values, enabling a clear 2-way decision!

> **Memory Trick:** **"Top-Right is the Decision Node: Left = Smaller, Down = Larger"**.

## 13. Comparisons
| Feature | Search 2D Matrix I (LeetCode 74) | Search 2D Matrix II (LeetCode 240) |
| :--- | :--- | :--- |
| **Sorting Property** | First int of row > last int of prev row | Rows AND Cols sorted independently |
| **Optimal Algorithm**| Flattened 1D Binary Search | **Staircase Search** |
| **Time Complexity** | **$O(\log(R \cdot C))$** | **$O(R + C)$** |
| **Indexing Access** | `matrix[mid / C][mid % C]` | `r = 0, c = C - 1; c-- / r++` |

## 14. How to Recognize This in Questions
* **"Search in matrix where rows are sorted left-to-right and cols are sorted top-to-bottom"** $\rightarrow$ Staircase Search ($O(R + C)$).
* **"Modify matrix in-place with O(1) space"** $\rightarrow$ Use Row 0 / Col 0 or State Bit Masking.
* **"Answer multiple sub-matrix range sum queries"** $\rightarrow$ 2D Prefix Sum Array ($O(1)$ query).

## 15. Frequently Asked Interview Questions
* **Q: Why does 2D Prefix Sum subtract `P[r1-1][c2]` and `P[r2][c1-1]` but add back `P[r1-1][c1-1]`?**  
  *A:* Subtracting the top region `P[r1-1][c2]` and left region `P[r2][c1-1]` subtracts the top-left overlapping sub-matrix twice. Adding back `P[r1-1][c1-1]` restores the correct inclusion-exclusion balance.
* **Q: How does Game of Life achieve $O(1)$ space complexity?**  
  *A:* By encoding state transitions into the 2nd bit of each cell's integer (`00` = dead, `01` = live, `10` = dead to live, `11` = live to live). A final bit-shift `cell >> 1` updates the grid in-place.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED MATRIX ALGORITHMS                            |
+-----------------------------------------------------------------------+
| • Staircase Search: Start at (0, C-1). If target < cell c--, else r++ |
| • Staircase Complexity: O(R + C) Time | O(1) Auxiliary Space          |
| • In-Place Set Zeroes: Use Row 0 & Col 0 as flag storage              |
| • 2D Prefix Sum: P[r][c] = val + P[r-1][c] + P[r][c-1] - P[r-1][c-1]  |
| • 2D Region Sum: P[r2][c2] - P[r1-1][c2] - P[r2][c1-1] + P[r1-1][c1-1]|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement Staircase Search starting from Top-Right `(0, C-1)`.
- [ ] I know why Top-Left `(0, 0)` cannot be used for Staircase Search.
- [ ] I can set matrix zeroes in-place using Row 0 and Col 0 flags in $O(1)$ space.
- [ ] I can write the 2D Prefix Sum inclusion-exclusion precomputation formula.
- [ ] I can write the 2D Sub-matrix Region Sum query formula.
