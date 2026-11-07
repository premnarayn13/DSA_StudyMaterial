# 13. Matrix Traversal Patterns

## 1. Introduction
Matrix traversal patterns dictate the order in which cells of a 2D grid are visited. In technical coding interviews, specialized matrix traversals—including Spiral Traversal, Diagonal Traversal, Snake/Zigzag Traversal, and Boundary Traversal—test a candidate's ability to maintain strict pointer boundaries without getting lost in off-by-one errors.

> **Important:** Spiral Matrix Traversal relies on **4 dynamic boundary pointers**: `top`, `bottom`, `left`, and `right`. Shrinking boundaries after completing each boundary directional sweep prevents duplicate processing.

## 2. Core Concepts
* **Spiral Traversal**: Visiting grid cells in a clockwise spiral from the outer perimeter shrinking inward to the center.
* **Diagonal Traversal**: Traversing matrix elements along main diagonals ($r + c = k$ or $r - c = k$).
* **Zigzag / Snake Traversal**: Moving right across even rows and left across odd rows to process elements sequentially.
* **Boundary Traversal**: Traversing only the outermost perimeter cells of a matrix ($O(R + C)$ time).

> **Memory Trick:** **"Top Row -> Right Col -> Bottom Row -> Left Col -> Shrink Boundaries!"**

## 3. Characteristics / Properties
* **Total Visits**: Every cell is visited exactly ONCE, yielding $O(R \cdot C)$ linear time complexity.
* **Dynamic Boundary Shrinking**:
  * Top Row processed $\to$ `top++`
  * Right Column processed $\to$ `right--`
  * Bottom Row processed $\to$ `bottom--`
  * Left Column processed $\to$ `left++`

```
Matrix Traversal Pattern Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Traversal Pattern     | Boundary Control  | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| Spiral Traversal      | 4 Shrinking Bounds| O(R * C)          | O(1)              |
| Anti-Diagonal (r+c=k) | Sum Invariant k   | O(R * C)          | O(1)              |
| Zigzag / Snake        | Row Parity check  | O(R * C)          | O(1)              |
| Boundary Only         | Outer 4 Edges     | O(R + C)          | O(1)              |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Spiral Traversal on a $3 \times 4$ Matrix:

```
Matrix:
[  1,  2,  3,  4 ]   (Top = 0, Bottom = 2)
[  5,  6,  7,  8 ]
[  9, 10, 11, 12 ]   (Left = 0, Right = 3)

Step 1: Traverse Top Row (left=0 to right=3 at top=0) -> [1, 2, 3, 4] | top++ (top=1)
Step 2: Traverse Right Col (top=1 to bottom=2 at right=3) -> [8, 12]  | right-- (right=2)
Step 3: Traverse Bottom Row (right=2 down to left=0 at bottom=2) -> [11, 10, 9] | bottom-- (bottom=1)
Step 4: Traverse Left Col (bottom=1 down to top=1 at left=0) -> [5] | left++ (left=1)

Step 5: Inner Spiral Top Row (left=1 to right=2 at top=1) -> [6, 7] | top++ (top=2 > bottom=1 STOP!)

Result: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7] ✅ (Correct!)
```

## 5. Visual Diagram
Spiral Boundary Traversal Flow & Shrinking Arrows:

```
(top, left) --------------> (top, right)
     ^                           |
     |   [ Inner Spiral Room ]   |
     |                           v
(bottom, left) <----------- (bottom, right)

Boundary Pointers:
top++    (after left -> right sweep)
right--  (after top -> bottom sweep)
bottom-- (after right -> left sweep)
left++   (after bottom -> top sweep)
```

## 6. Operations / Algorithms
Spiral Matrix Master Implementation:

```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> result = new ArrayList<>();
    if (matrix == null || matrix.length == 0) return result;

    int top = 0, bottom = matrix.length - 1;
    int left = 0, right = matrix[0].length - 1;

    while (top <= bottom && left <= right) {
        // 1. Traverse Right across Top row
        for (int c = left; c <= right; c++) result.add(matrix[top][c]);
        top++;

        // 2. Traverse Down along Right column
        for (int r = top; r <= bottom; r++) result.add(matrix[r][right]);
        right--;

        // 3. Traverse Left across Bottom row (Guard against single row duplicate!)
        if (top <= bottom) {
            for (int c = right; c >= left; c--) result.add(matrix[bottom][c]);
            bottom--;
        }

        // 4. Traverse Up along Left column (Guard against single col duplicate!)
        if (left <= right) {
            for (int r = bottom; r >= top; r--) result.add(matrix[r][left]);
            left++;
        }
    }
    return result;
}
```

> **Quick Syntax:**
```java
// Boundary Guards for Bottom and Left Sweeps
if (top <= bottom) { /* Bottom row sweep */ }
if (left <= right) { /* Left col sweep */ }
```

## 7. Examples
* **LeetCode 54 - Spiral Matrix**: Return elements of $R \times C$ matrix in spiral order.
* **LeetCode 59 - Spiral Matrix II**: Generate an $N \times N$ matrix filled with elements $1 \dots N^2$ in spiral order.
* **LeetCode 498 - Diagonal Traverse**: Traverse matrix elements diagonally in alternating up/down directions.

## 8. Java Code
Complete interview-ready Java suite implementing Spiral Traversal, Diagonal Traversal, and Spiral Matrix Generation:

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MatrixTraversalMaster {

    // 1. Spiral Matrix Traversal (LeetCode 54) O(R * C) Time, O(1) Auxiliary Space
    public static List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return result;

        int top = 0, bottom = matrix.length - 1;
        int left = 0, right = matrix[0].length - 1;

        while (top <= bottom && left <= right) {
            // Traverse Top Row
            for (int j = left; j <= right; j++) result.add(matrix[top][j]);
            top++;

            // Traverse Right Column
            for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
            right--;

            // Traverse Bottom Row (Guard against single remaining row)
            if (top <= bottom) {
                for (int j = right; j >= left; j--) result.add(matrix[bottom][j]);
                bottom--;
            }

            // Traverse Left Column (Guard against single remaining column)
            if (left <= right) {
                for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
                left++;
            }
        }

        return result;
    }

    // 2. Generate Spiral Matrix II (LeetCode 59) O(N^2) Time, O(1) Auxiliary Space
    public static int[][] generateMatrix(int n) {
        int[][] matrix = new int[n][n];
        int top = 0, bottom = n - 1;
        int left = 0, right = n - 1;
        int num = 1;

        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) matrix[top][j] = num++;
            top++;

            for (int i = top; i <= bottom; i++) matrix[i][right] = num++;
            right--;

            if (top <= bottom) {
                for (int j = right; j >= left; j--) matrix[bottom][j] = num++;
                bottom--;
            }

            if (left <= right) {
                for (int i = bottom; i >= top; i--) matrix[i][left] = num++;
                left++;
            }
        }

        return matrix;
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
            {1, 2, 3, 4},
            {5, 6, 7, 8},
            {9, 10, 11, 12}
        };

        System.out.println("Spiral Order: " + spiralOrder(matrix));
        // Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

        System.out.println("\nGenerated 3x3 Spiral Matrix II:");
        printMatrix(generateMatrix(3));
        /*
        [1, 2, 3]
        [8, 9, 4]
        [7, 6, 5]
        */
    }
}
```

## 9. Complexity Analysis
| Traversal Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Spiral Order (LeetCode 54)** | **$O(R \cdot C)$** | **$O(1)$** | Visits each cell exactly once |
| **Spiral Generation (LeetCode 59)**| **$O(N^2)$** | **$O(1)$** | Fills grid cells in spiral order |
| **Diagonal Traverse** | **$O(R \cdot C)$** | **$O(1)$** | Flips direction on boundary hits |
| **Snake Traversal** | **$O(R \cdot C)$** | **$O(1)$** | Reverses direction on odd rows |

## 10. Edge Cases
* **Single Row Matrix ($1 \times C$)**: Without the `if (top <= bottom)` guard, the bottom row sweep duplicates top row entries!
* **Single Column Matrix ($R \times 1$)**: Without the `if (left <= right)` guard, the left column sweep duplicates right column entries!
* **$1 \times 1$ Matrix**: Processes single element and terminates cleanly.

## 11. Common Mistakes
* Forgetting the `if (top <= bottom)` and `if (left <= right)` check before bottom and left sweeps (causes duplicate elements in non-square matrices!).
* Forgetting to update boundary pointers after finishing a directional sweep (`top++`, `right--`, `bottom--`, `left++`).
* Using 4 nested loops without checking global termination `while (top <= bottom && left <= right)`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why are the `if (top <= bottom)` and `if (left <= right)` checks mandatory in Spiral Matrix?
> After `top++` or `right--` executes, the remaining space might be reduced to 0 rows or 0 columns. Without these checks, the subsequent bottom and left loops will re-traverse already processed cells in 1D matrix strips!

> **Memory Trick:** **"4 Direction Steps: R, D, L, U with boundary checks on L and U"**.

## 13. Comparisons
| Feature | Spiral Order | Diagonal Order | Snake / Zigzag Order |
| :--- | :--- | :--- | :--- |
| **Direction Changes** | 4 (Clockwise Shrinking) | 2 (Up-Right / Down-Left) | 2 (Left-Right / Right-Left) |
| **Boundary Pointers** | 4 (`top`, `bottom`, `left`, `right`) | Index Sum Invariants ($r + c$) | Row parity (`r % 2`) |
| **Time Complexity** | $O(R \cdot C)$ | $O(R \cdot C)$ | $O(R \cdot C)$ |

## 14. How to Recognize This in Questions
* **"Traverse matrix in spiral order / perimeter inward"** $\rightarrow$ Spiral Traversal with 4 boundary pointers.
* **"Traverse matrix diagonally in alternating directions"** $\rightarrow$ Diagonal Traversal.

## 15. Frequently Asked Interview Questions
* **Q: How does Spiral Traversal guarantee $O(1)$ auxiliary space?**  
  *A:* By using only 4 integer boundary pointers (`top`, `bottom`, `left`, `right`) and writing directly to the output array/list without creating temporary data structures.
* **Q: What is the sum invariant of an anti-diagonal in a 2D matrix?**  
  *A:* For any cell $(r, c)$ on an anti-diagonal, the sum of row and column indices is constant: $r + c = k$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATRIX TRAVERSAL PATTERNS                             |
+-----------------------------------------------------------------------+
| • Spiral Pointers: top=0, bottom=R-1, left=0, right=C-1               |
| • 4 Steps: Right (top++), Down (right--), Left (bottom--), Up (left++)|
| • Mandatory Guards: `if (top <= bottom)` & `if (left <= right)`       |
| • Eliminates Duplicates on 1D strips (1xC or Rx1 matrices)            |
| • Time Complexity: O(R * C) | Auxiliary Space: O(1)                   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write Spiral Matrix Traversal from memory in 3 minutes.
- [ ] I know why `if (top <= bottom)` and `if (left <= right)` guards are mandatory.
- [ ] I can generate a 2D Spiral Matrix II of size $N \times N$.
- [ ] I know how to navigate 4-directional neighbor grids using `dr` and `dc`.
- [ ] I understand diagonal index sum invariants ($r + c = k$).
