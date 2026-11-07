# 12. Matrix Fundamentals & 2D Arrays

## 1. Introduction
A **Matrix** (or 2D Array) is a two-dimensional grid of numbers arranged in $R$ rows and $C$ columns. In technical coding interviews, 2D matrix problems evaluate spatial indexing, boundary validation, matrix transformations (transposition, rotation), and grid traversals. Understanding how matrix row/column indices map to memory enables writing bug-free $O(R \cdot C)$ grid algorithms.

> **Important:** Matrix operations require validating bounds for EVERY cell $(r, c)$: **`0 <= r < R && 0 <= c < C`**. A single out-of-bounds access throws `ArrayIndexOutOfBoundsException`.

## 2. Core Concepts
* **Matrix Representation in Java**: `int[][] matrix = new int[R][C]` allocates an outer array of length $R$, where each element is a 1D array of length $C$.
* **Matrix Transposition**: Swapping elements across the main diagonal: `matrix[r][c] <-> matrix[c][r]` (converts an $R \times C$ matrix into a $C \times R$ matrix).
* **Matrix Rotation (90 Degrees Clockwise)**:
  1. Transpose the matrix in-place (`matrix[i][j] <-> matrix[j][i]`).
  2. Reverse each individual row in-place (`reverse(matrix[i])`).
* **Matrix Directions Array**: Using offset direction vectors to navigate 4-directional (Up, Down, Left, Right) or 8-directional neighbor cells.

> **Memory Trick:** **"90° Clockwise Rotation = Transpose -> Reverse Each Row"**.

## 3. Characteristics / Properties
* **Main Diagonal Property**: Cells on the main diagonal satisfy **`r == c`**.
* **Anti-Diagonal Property**: Cells on the anti-diagonal satisfy **`r + c == N - 1`** (for an $N \times N$ square matrix).
* **In-Place Transposition**: Transposition can be performed in-place ONLY on square $N \times N$ matrices by swapping `matrix[i][j]` with `matrix[j][i]` for $j > i$.

```
Matrix Navigation & Boundary Rules:
+-----------------------+-------------------------------------------------------+
| Concept               | Rule / Formula                                        |
+-----------------------+-------------------------------------------------------+
| Row Count             | R = matrix.length                                     |
| Column Count          | C = matrix[0].length                                  |
| Bound Check           | r >= 0 && r < R && c >= 0 && c < C                    |
| Main Diagonal         | r == c                                                |
| Anti-Diagonal         | r + c == N - 1                                        |
| Transpose Swap        | swap(matrix[i][j], matrix[j][i]) for j > i            |
+-----------------------+-------------------------------------------------------+
```

## 4. Internal Working
Tracing 90-Degree Clockwise Matrix Rotation on a $3 \times 3$ Matrix:

```
Original Matrix:
[ 1, 2, 3 ]
[ 4, 5, 6 ]
[ 7, 8, 9 ]

Step 1: Transpose Matrix (Swap matrix[i][j] with matrix[j][i] for j > i)
[ 1, 4, 7 ]
[ 2, 5, 8 ]
[ 3, 6, 9 ]

Step 2: Reverse Each Row In-Place
Row 0: [ 1, 4, 7 ] -> Reverse -> [ 7, 4, 1 ]
Row 1: [ 2, 5, 8 ] -> Reverse -> [ 8, 5, 2 ]
Row 2: [ 3, 6, 9 ] -> Reverse -> [ 9, 6, 3 ]

Final 90° Clockwise Rotated Matrix:
[ 7, 4, 1 ]
[ 8, 5, 2 ]
[ 9, 6, 3 ] ✅ (Correct!)
```

## 5. Visual Diagram
4-Directional Neighbor Offsets (`dr`, `dc` vectors):

```
                       Up (-1, 0)
                           ^
                           |
      Left (0, -1) <--- (r, c) ---> Right (0, +1)
                           |
                           v
                      Down (+1, 0)

Direction Vectors in Java:
int[] dr = {-1, 1, 0, 0}; // Row offsets: Up, Down, Left, Right
int[] dc = {0, 0, -1, 1}; // Col offsets: Up, Down, Left, Right
```

## 6. Operations / Algorithms
Essential Matrix Navigation Templates:

### 1. 4-Directional Neighbor Exploration Idiom
```java
int[] dr = {-1, 1, 0, 0};
int[] dc = {0, 0, -1, 1};

for (int d = 0; d < 4; d++) {
    int nr = r + dr[d];
    int nc = c + dc[d];
    if (nr >= 0 && nr < R && nc >= 0 && nc < C) {
        // Valid neighboring cell (nr, nc)
    }
}
```

### 2. In-Place Square Matrix Transposition ($N \times N$)
```java
public void transpose(int[][] matrix) {
    int n = matrix.length;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) { // Only upper triangle j > i!
            int temp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = temp;
        }
    }
}
```

> **Quick Syntax:**
```java
// Matrix Row & Column Dimensions in Java
int R = matrix.length;
int C = (R > 0) ? matrix[0].length : 0;
```

## 7. Examples
* **LeetCode 48 - Rotate Image**: Rotate $N \times N$ matrix by 90 degrees clockwise in-place.
* **LeetCode 867 - Transpose Matrix**: Transpose an $R \times C$ matrix into a $C \times R$ matrix.
* **LeetCode 73 - Set Matrix Zeroes**: Setting entire row and column to 0 if a cell contains 0.

## 8. Java Code
Complete interview-ready Java suite implementing Matrix Transposition, 90-degree Clockwise Rotation, 90-degree Counter-Clockwise Rotation, and Boundary Validations:

```java
import java.util.Arrays;

public class MatrixFundamentalsMaster {

    // 1. Transpose N x N Matrix In-Place O(N^2) Time, O(1) Space
    public static void transpose(int[][] matrix) {
        if (matrix == null || matrix.length == 0) return;
        int n = matrix.length;

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) { // Swap upper triangle with lower triangle
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = temp;
            }
        }
    }

    // 2. Rotate Image 90 Degrees Clockwise In-Place (LeetCode 48) O(N^2) Time, O(1) Space
    public static void rotateClockwise(int[][] matrix) {
        if (matrix == null || matrix.length == 0) return;

        // Step 1: Transpose matrix
        transpose(matrix);

        // Step 2: Reverse each row in-place
        for (int[] row : matrix) {
            reverseRow(row);
        }
    }

    // 3. Rotate Image 90 Degrees Counter-Clockwise In-Place O(N^2) Time, O(1) Space
    public static void rotateCounterClockwise(int[][] matrix) {
        if (matrix == null || matrix.length == 0) return;

        // Step 1: Reverse each row first
        for (int[] row : matrix) {
            reverseRow(row);
        }

        // Step 2: Transpose matrix
        transpose(matrix);
    }

    // Helper method to reverse 1D array row in-place
    private static void reverseRow(int[] row) {
        int left = 0, right = row.length - 1;
        while (left < right) {
            int temp = row[left];
            row[left] = row[right];
            row[right] = temp;
            left++;
            right--;
        }
    }

    // Helper method to print matrix
    public static void printMatrix(int[][] matrix) {
        for (int[] row : matrix) {
            System.out.println(Arrays.toString(row));
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        System.out.println("Original Matrix:");
        printMatrix(matrix);

        rotateClockwise(matrix);
        System.out.println("\nAfter 90° Clockwise Rotation:");
        printMatrix(matrix);
        /*
        [7, 4, 1]
        [8, 5, 2]
        [9, 6, 3]
        */
    }
}
```

## 9. Complexity Analysis
| Matrix Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **In-Place Transposition ($N \times N$)**| **$O(N^2)$** | **$O(1)$** | Swaps upper triangle elements |
| **90° Clockwise Rotation** | **$O(N^2)$** | **$O(1)$** | Transpose + Row Reversal |
| **90° Counter-Clockwise Rotation**| **$O(N^2)$** | **$O(1)$** | Row Reversal + Transpose |
| **Out-of-Place Transpose ($R \times C$)**| **$O(R \cdot C)$**| $O(R \cdot C)$ | Creates new $C \times R$ matrix |

## 10. Edge Cases
* **Empty Matrix**: `matrix == null || matrix.length == 0 || matrix[0].length == 0`. Always check `matrix[0].length` after confirming `matrix.length > 0`.
* **Non-Square Matrix Transposition ($R \neq C$)**: In-place transposition is impossible for non-square matrices because grid dimensions change ($R \times C \to C \times R$). Must allocate a new `new int[C][R]` matrix!
* **1x1 Matrix**: Returns immediately without modifications.

## 11. Common Mistakes
* Iterating `j` from `0` to `n` during transposition (swaps elements twice, returning matrix back to original state!). Inner loop MUST start at `j = i + 1`.
* Forgetting to check `matrix[0].length == 0` for empty matrices.
* Hardcoding matrix dimensions instead of dynamically querying `R = matrix.length` and `C = matrix[0].length`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Remember the rotation formulas:
> * **90° Clockwise Rotation**: Transpose $\to$ Reverse Rows.
> * **90° Counter-Clockwise Rotation**: Reverse Rows $\to$ Transpose (or Transpose $\to$ Reverse Columns).
> * **180° Rotation**: Reverse Rows $\to$ Reverse Columns.

> **Memory Trick:** **"Transposition Loop starts at j = i + 1"**. Swapping `j = 0` to `n` undoes all swaps!

## 13. Comparisons
| Feature | In-Place Transpose ($N \times N$) | New Matrix Transpose ($R \times C$) |
| :--- | :--- | :--- |
| **Matrix Type** | Square matrices only | Any matrix dimensions |
| **Time Complexity** | $O(N^2)$ | $O(R \cdot C)$ |
| **Space Complexity**| **$O(1)$ (In-Place)** | $O(R \cdot C)$ (Allocates new grid) |
| **Inner Loop** | `for (int j = i + 1; j < N; j++)` | `for (int c = 0; c < C; c++)` |

## 14. How to Recognize This in Questions
* **"Rotate image / grid by 90 degrees in-place"** $\rightarrow$ Transpose + Row Reversal.
* **"Check if matrix is symmetric"** $\rightarrow$ Check if `matrix[i][j] == matrix[j][i]`.

## 15. Frequently Asked Interview Questions
* **Q: Why must transposition inner loop start at `j = i + 1`?**  
  *A:* If `j` starts at `0`, element `(i, j)` is swapped to `(j, i)`, and when the outer loop reaches `j`, it is swapped BACK to `(i, j)`, undoing the transposition completely! Starting at `j = i + 1` processes only the upper right triangle elements.
* **Q: How do you check if a matrix cell is valid in 1 line of Java code?**  
  *A:* `boolean isValid = (r >= 0 && r < matrix.length && c >= 0 && c < matrix[0].length);`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATRIX FUNDAMENTALS & 2D ARRAYS                       |
+-----------------------------------------------------------------------+
| • Dimensions: R = matrix.length, C = matrix[0].length                 |
| • Boundary Check: r >= 0 && r < R && c >= 0 && c < C                  |
| • In-Place Transpose: Swap matrix[i][j] with matrix[j][i] for j > i   |
| • 90° Clockwise Rotation: Transpose -> Reverse Each Row               |
| • 90° Counter-Clockwise:  Reverse Each Row -> Transpose               |
| • 4-Direction Vectors: dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1}         |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the 4-directional neighbor offset logic (`dr`, `dc`).
- [ ] I can transpose an $N \times N$ matrix in-place without double-swapping.
- [ ] I can rotate a matrix 90 degrees clockwise in-place.
- [ ] I can rotate a matrix 90 degrees counter-clockwise in-place.
- [ ] I know how to check matrix boundary conditions safely.
