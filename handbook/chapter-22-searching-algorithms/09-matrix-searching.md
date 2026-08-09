# 09. Matrix Searching: 2D Matrix Flattening, Top-Right Corner Scanning & Binary Search

## 1. Introduction
**Matrix Searching** encompasses algorithmic strategies for locating target keys within 2D matrix grids exhibiting structural sorting properties. Matrix searching splits into two primary architectural benchmarks:
1. **Fully Monotonic Matrix (LeetCode 74)**: The first integer of each row is greater than the last integer of the previous row. Virtual flattening maps 2D coordinates `(r, c)` to 1D index $i$ via `r = i / cols` and `c = i % cols`, executing binary search in **$O(\log (M \cdot N))$ Time**.
2. **Row-Wise and Column-Wise Sorted Matrix (LeetCode 240)**: Each row and column is independently sorted in ascending order. Starting at the **Top-Right Corner `(0, cols - 1)`** enables a **Staircase Elimination Scan** in **$O(M + N)$ Linear-Space Time**.

> **Important:** Core Invariants of Matrix Searching:
> 1. **Virtual 1D Flattening Invariant (LeetCode 74)**:
>    - For a 1D virtual index $mid \in [0 \dots M \cdot N - 1]$:
>      $$\text{row} = \text{mid} / \text{cols}, \quad \text{col} = \text{mid} \% \text{cols}$$
>    - Allows standard Template 1 Binary Search directly on 2D matrices!
> 2. **Top-Right Corner Staircase Invariant (LeetCode 240)**:
>    - Position at top-right corner `(r = 0, c = cols - 1)`:
>      - If `matrix[r][c] == target`: Found match!
>      - If `matrix[r][c] > target`: Current column `c` is TOO LARGE $\implies$ Eliminate column `c--`!
>      - If `matrix[r][c] < target`: Current row `r` is TOO SMALL $\implies$ Eliminate row `r++`! ⚡

```
Top-Right Corner Staircase Scan Topology (Target = 5):
Matrix:   [  1,   4,   7,  11,  15 ]
          [  2,   5,   8,  12,  19 ]
          [  3,   6,   9,  16,  22 ]

Start Top-Right (0, 4) val 15 > 5  ---> Eliminate Col 4 (c = 3)
At (0, 3) val 11 > 5                ---> Eliminate Col 3 (c = 2)
At (0, 2) val 7 > 5                 ---> Eliminate Col 2 (c = 1)
At (0, 1) val 4 < 5                 ---> Eliminate Row 0 (r = 1)
At (1, 1) val 5 == 5                ---> FOUND TARGET 5! ⚡
```

---

## 2. Core Concepts & Matrix Searching Strategy Matrix

### 2.1 Matrix Searching Strategy Matrix
```
Matrix Searching Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Matrix Structure      | Primary Algorithm | Starting State    | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Fully Monotonic(74)**| Virtual 1D Binary | `low=0, high=M*N-1`| **$O(\log(M \cdot N))$ ⚡**|
| **Row/Col Sorted(240)**| Top-Right Staircase| `r=0, c=cols-1`   | **$O(M + N)$ Linear ⚡**|
| **K-th Smallest (378)**| Binary Search Ans | `low=mat[0][0]`   | **$O(M \log(\text{Range}))$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 74: Flatten (mid / cols, mid % cols) O(log(MN)); LeetCode 240: Top-Right Staircase O(M + N)!"**

---

## 3. Characteristics & $O(M + N)$ Staircase Proof

### 3.1 Mathematical Proof of $O(M + N)$ Staircase Scanning
* Start at top-right corner `(0, N-1)`.
* Every comparison either decrements column `c--` or increments row `r++`.
* The algorithm can decrement column at most $N$ times and increment row at most $M$ times.
* Maximum Steps: $S_{\max} = M + N$.
* Total Time Complexity: $\mathbf{O(M + N) \text{ Linear Time Complexity}}$. Auxiliary Space: $\mathbf{O(1) \text{ Constant Space}}$. ⚡

---

## 4. Internal Working Mechanics: Virtual 1D Coordinate Mapping

Tracing Virtual 1D Mapping on a $3 \times 4$ Matrix ($M = 3, N = 4$):

```
Matrix (3 x 4):
[  1,  3,  5,  7 ]   Row 0  (Indices 0..3)
[ 10, 11, 16, 20 ]   Row 1  (Indices 4..7)
[ 23, 30, 34, 60 ]   Row 2  (Indices 8..11)

Total Elements = 3 * 4 = 12 (Virtual Range 0 ... 11).

Convert Virtual Index mid = 6 to 2D Coordinates:
- row = 6 / 4 = 1
- col = 6 % 4 = 2
- Element matrix[1][2] = 16!

Convert Virtual Index mid = 9 to 2D Coordinates:
- row = 9 / 4 = 2
- col = 9 % 4 = 1
- Element matrix[2][1] = 30!

Virtual Mapping maps any 1D binary search index to 2D matrix in O(1) time! ✅
```

---

## 5. Visual Diagram: Staircase Elimination vs Virtual Binary Search

```
1. LeetCode 74 Virtual Binary Search (Fully Monotonic):
1D Range: [ 0 ........................ mid ........................ M*N-1 ]
            row = mid / cols, col = mid % cols  ---> Standard Binary Search ⚡

2. LeetCode 240 Top-Right Staircase (Row & Col Sorted):
           [ 1,   4,   7,  11, (15) ] <--- Start Top-Right Corner!
           [ 2,   5,   8,  12,  19  ]        val > target -> Move LEFT (c--)
           [ 3,   6,   9,  16,  22  ]        val < target -> Move DOWN (r++) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 74 (Search a 2D Matrix I), LeetCode 240 (Search a 2D Matrix II), and LeetCode 378 (K-th Smallest Element in a Sorted Matrix).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing 2D Matrix Searching Algorithms:
 * Virtual 1D Binary Search, Top-Right Corner Staircase Scanning, and K-th Element Search.
 */
public class MatrixSearchingMaster {

    // =========================================================================
    // 1. SEARCH A 2D MATRIX I (LeetCode 74 Virtual 1D BS O(log(M * N)))
    // =========================================================================
    /**
     * Searches target in a fully monotonic 2D matrix.
     * LeetCode 74 Solution.
     *
     * @param matrix 2D matrix where first int of row > last int of prev row
     * @param target search key
     * @return true if target exists
     */
    public boolean searchMatrix(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0] == null || matrix[0].length == 0) {
            return false;
        }

        int rows = matrix.length;
        int cols = matrix[0].length;

        int low = 0;
        int high = rows * cols - 1; // Virtual 1D range!

        while (low <= high) {
            int mid = low + (high - low) / 2;

            // Virtual 2D Coordinate Mapping: row = mid / cols, col = mid % cols
            int val = matrix[mid / cols][mid % cols];

            if (val == target) {
                return true;
            } else if (val < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return false;
    }

    // =========================================================================
    // 2. SEARCH A 2D MATRIX II (LeetCode 240 Top-Right Staircase O(M + N))
    // =========================================================================
    /**
     * Searches target in row-wise and column-wise sorted matrix.
     * LeetCode 240 Solution.
     */
    public boolean searchMatrixII(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0] == null || matrix[0].length == 0) {
            return false;
        }

        int rows = matrix.length;
        int cols = matrix[0].length;

        // Start at Top-Right Corner (r = 0, c = cols - 1)
        int r = 0;
        int c = cols - 1;

        while (r < rows && c >= 0) {
            int val = matrix[r][c];

            if (val == target) {
                return true; // Match found!
            } else if (val > target) {
                c--; // Current column is too large -> Move LEFT
            } else {
                r++; // Current row is too small -> Move DOWN
            }
        }

        return false;
    }

    // =========================================================================
    // 3. K-TH SMALLEST ELEMENT IN SORTED MATRIX (LeetCode 378 O(M log(Range)))
    // =========================================================================
    /**
     * Finds K-th smallest element in row/column-wise sorted matrix.
     * LeetCode 378 Solution using Binary Search on Answer.
     */
    public int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        int low = matrix[0][0];
        int high = matrix[n - 1][n - 1];

        while (low < high) {
            int mid = low + (high - low) / 2;

            int count = countLessEqual(matrix, mid, n);

            if (count < k) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        return low;
    }

    private int countLessEqual(int[][] matrix, int target, int n) {
        int count = 0;
        int r = n - 1; // Start bottom-left corner
        int c = 0;

        while (r >= 0 && c < n) {
            if (matrix[r][c] <= target) {
                count += (r + 1); // Add entire column elements above r
                c++;
            } else {
                r--;
            }
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// 2D Virtual Index Mapping Line
int val = matrix[mid / cols][mid % cols];
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 74 - Search a 2D Matrix**:
   - Virtual 1D Binary Search ($O(\log(M \cdot N))$).

2. **LeetCode 240 - Search a 2D Matrix II**:
   - Top-Right Staircase Scanning ($O(M + N)$).

3. **LeetCode 378 - K-th Smallest Element in a Sorted Matrix**:
   - Binary Search on Answer Matrix Range ($O(M \log(\text{Range}))$).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class MatrixSearchingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     2D MATRIX SEARCHING DEMONSTRATION           ");
        System.out.println("=================================================\n");

        MatrixSearchingMaster master = new MatrixSearchingMaster();

        // 1. Fully Monotonic Matrix Test (LeetCode 74)
        int[][] mat1 = {
            {1, 3, 5, 7},
            {10, 11, 16, 20},
            {23, 30, 34, 60}
        };
        int target1 = 3;
        boolean found1 = master.searchMatrix(mat1, target1);
        System.out.println("1. LeetCode 74 Search Target " + target1 + " (Monotonic Matrix): Exists = " + found1);
        System.out.println("-------------------------------------------------");

        // 2. Row/Col Sorted Matrix Test (LeetCode 240)
        int[][] mat2 = {
            {1, 4, 7, 11, 15},
            {2, 5, 8, 12, 19},
            {3, 6, 9, 16, 22}
        };
        int target2 = 5;
        boolean found2 = master.searchMatrixII(mat2, target2);
        System.out.println("2. LeetCode 240 Search Target " + target2 + " (Row/Col Sorted Matrix): Exists = " + found2);
        System.out.println("-------------------------------------------------");

        // 3. K-th Smallest Element Test (LeetCode 378)
        int[][] mat3 = {
            {1, 5, 9},
            {10, 11, 13},
            {12, 13, 15}
        };
        int k = 8;
        int kthVal = master.kthSmallest(mat3, k);
        System.out.println("3. LeetCode 378 8-th Smallest Element in Matrix: " + kthVal);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Matrix Searching Problem | Matrix Condition | Time Complexity | Auxiliary Space | Key Starting Corner |
| :--- | :--- | :--- | :--- | :--- |
| **Search 2D Matrix I (74)**| Fully Monotonic | $\mathbf{O(\log(M \cdot N))}$ Log ⚡| $\mathbf{O(1)}$ Constant ⚡ | Virtual 1D index `0` |
| **Search 2D Matrix II (240)**| Row & Col Sorted| $\mathbf{O(M + N)}$ Linear ⚡ | $\mathbf{O(1)}$ Constant ⚡ | Top-Right `(0, cols-1)` |
| **K-th Smallest (378)**| Row & Col Sorted| $\mathbf{O(M \log(\text{Range}))}$| $\mathbf{O(1)}$ Constant ⚡ | Bottom-Left Count |

---

## 10. Edge Cases & Boundary Handling

1. **Empty 2D Matrix (`matrix.length == 0` or `matrix[0].length == 0`)**:
   - Handled cleanly by top-level defensive guards returning `false` immediately.

2. **$1 \times 1$ Single Cell Matrix**:
   - Virtual binary search `low = 0, high = 0` evaluates single cell correctly.

3. **Target Smaller Than Top-Left Corner `matrix[0][0]`**:
   - Staircase search terminates when `c < 0` or `r >= rows` and returns `false`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Starting Staircase Search at Top-Left Corner `(0, 0)`**:
  - Starting at `(0, 0)` makes both right and down choices increase values, destroying the ability to eliminate directions.
  - **ALWAYS start at Top-Right Corner `(0, cols - 1)` or Bottom-Left Corner `(rows - 1, 0)`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Top-Right Corner Works for LeetCode 240:
> At top-right corner `(0, cols - 1)`:
> * Moving **LEFT (c--)** strictly DECREASES value.
> * Moving **DOWN (r++)** strictly INCREASES value.
> This opposite directional behavior creates a deterministic decision tree at every step! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Virtual 1D Binary Search (LeetCode 74) | Top-Right Staircase (LeetCode 240) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\log(M \cdot N))$ Logarithmic ⚡** | **$O(M + N)$ Linear ⚡** |
| **Matrix Requirement**| Fully Monotonic (Row end < Next start) | Row-Wise & Column-Wise Sorted |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡** | **$O(1)$ Constant Space ⚡** |

---

## 14. How to Recognize This in Questions

* **"Search element in fully continuous sorted 2D grid"** $\rightarrow$ LeetCode 74 Virtual Binary Search.
* **"Search element in matrix where each row and column are individually sorted"** $\rightarrow$ LeetCode 240 Top-Right Staircase.

---

## 15. Frequently Asked Interview Questions

* **Q: How does `mid / cols` and `mid % cols` convert 1D indices to 2D matrix coordinates?**  
  *A:* Integer division `mid / cols` computes row offset (how many full rows preceded `mid`). Modulo `mid % cols` computes column offset within that row.

* **Q: Why can't Top-Right Staircase be used for fully monotonic matrices?**  
  *A:* It CAN be used, but top-right staircase takes $O(M + N)$ time, whereas Virtual 1D Binary Search takes faster $O(\log(M \cdot N))$ time for fully monotonic grids.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATRIX SEARCHING                                      |
+-----------------------------------------------------------------------+
| • LeetCode 74 (Monotonic Grid): row = mid / cols, col = mid % cols    |
| • LeetCode 74 Time            : O(log(M * N)) Virtual 1D BS ⚡         |
| • LeetCode 240 (Row/Col Sorted): Start at Top-Right Corner (0, cols-1) |
| • Staircase Direction         : val > target -> c--; val < target -> r++|
| • LeetCode 240 Time           : O(M + N) Linear Time | O(1) Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 74 (`Search a 2D Matrix I`) using virtual 1D coordinate mapping.
- [ ] I can write LeetCode 240 (`Search a 2D Matrix II`) using top-right corner staircase scanning.
- [ ] I can write LeetCode 378 (`K-th Smallest Element in a Sorted Matrix`).
- [ ] I know why top-right corner `(0, cols - 1)` allows directional elimination.
- [ ] I can trace staircase matrix elimination step by step.
