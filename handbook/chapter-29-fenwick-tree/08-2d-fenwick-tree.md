# 08. 2D Fenwick Trees, Nested LSB Traversal & 2D Matrix Submatrix Queries

## 1. Introduction
A **2D Fenwick Tree (2D BIT)**—specifically **Range Sum Query 2D - Mutable (LeetCode 308)**—extends the 1D Fenwick Tree to a 2D matrix grid of size $M \times N$. By nesting 1D LSB bitwise loops over both row and column indices (`row += row & (-row)` and `col += col & (-col)`), a 2D Fenwick Tree performs dynamic point updates and submatrix sum queries over any 2D region $[r_1, c_1] \dots [r_2, c_2]$ in **$O(\log M \cdot \log N)$ Time** using **$O(M \cdot N)$ Space**.

> **Important:** The 2D Fenwick Tree Invariants & Submatrix Query Equation:
> 1. **2D Array Allocation**: Allocate `tree[M + 1][N + 1]` using 1-based indexing for both rows and columns.
> 2. **Nested Bitwise Traversal**:
>    - Point Update: Outer loop `r += r & (-r)`, inner loop `c += c & (-c)`.
>    - 2D Prefix Query: Outer loop `r -= r & (-r)`, inner loop `c -= c & (-c)`.
> 3. **2D Inclusion-Exclusion Submatrix Sum Formula**:
>    $$\text{SubmatrixSum}(r_1, c_1, r_2, c_2) = Q(r_2, c_2) - Q(r_1 - 1, c_2) - Q(r_2, c_1 - 1) + Q(r_1 - 1, c_1 - 1)$$
>    where $Q(r, c)$ computes the prefix sum of submatrix $[0, 0] \dots [r, c]$! ⚡

```
2D Inclusion-Exclusion Submatrix Query Topology (Submatrix [r1, c1] to [r2, c2]):
+-----------------------+
|  Q(r1-1, c1-1)  | A   |
+-----------------+-----+
|  B              | TARGET MATRIX [r1, c1] ... [r2, c2] |
+-----------------+-------------------------------------+

Target Submatrix = Q(r2, c2) - Q(r1-1, c2) - Q(r2, c1-1) + Q(r1-1, c1-1)! ⚡
```

---

## 2. Core Concepts & LeetCode 308 2D Fenwick Tree Architecture

### 2.1 LeetCode 308 Operational Strategy Matrix
```
2D Fenwick Tree Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| 2D Operation          | Nested Loops      | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **`update(r, c, val)`**| Outer R / Inner C | **$O(\log M \cdot \log N)$ ⚡**| $O(M \cdot N)$ Array|
| **`query(r, c)`**     | Outer R / Inner C | **$O(\log M \cdot \log N)$ ⚡**| $O(M \cdot N)$ Array|
| **`sumRegion()`**     | 4 Prefix Queries  | **$O(\log M \cdot \log N)$ ⚡**| $O(1)$ Auxiliary  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"2D BIT: Nest 1D loops over rows and cols! Submatrix sum = Q(r2,c2) - Q(r1-1,c2) - Q(r2,c1-1) + Q(r1-1,c1-1)!"**

---

## 3. Characteristics & 2D Binary Bit Bounds

### 3.1 Time Complexity Bounds
* A 2D point update visits at most $\lceil \log_2 M \rceil \times \lceil \log_2 N \rceil$ cells.
* A 2D submatrix query calls 4 prefix queries, visiting at most $4 \times \lceil \log_2 M \rceil \times \lceil \log_2 N \rceil$ cells.
* Total Time Complexity: $\mathbf{O(\log M \cdot \log N) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing 2D Submatrix Sum Query for $[r_1=1, c_1=1] \dots [r_2=2, c_2=2]$ on a $3 \times 3$ Matrix:

```
Full Matrix 3x3. Target region is submatrix (1,1) to (2,2).

Call sumRegion(1, 1, 2, 2):
1. Compute Q(2, 2)   -> Total sum of submatrix (0,0) to (2,2).
2. Subtract Q(0, 2)  -> Remove top rows (0,0) to (0,2).
3. Subtract Q(2, 0)  -> Remove left cols (0,0) to (2,0).
4. Add back Q(0, 0)  -> Re-add top-left corner double-subtracted region.

Result = Q(2,2) - Q(0,2) - Q(2,0) + Q(0,0)! Executed in O(log M * log N) time! ✅
```

---

## 5. Visual Diagram
2D Inclusion-Exclusion Matrix Subtraction Topography:

```
Total Region Q(r2, c2):          Subtract Top Q(r1-1, c2):     Subtract Left Q(r2, c1-1):
+-------------------+            +-------------------+         +---+---------------+
| x  x  x  x  x  x  |            | -  -  -  -  -  -  |         | - | x  x  x  x  x |
| x  x  x  x  x  x  |            | x  x  x  x  x  x  |         | - | x  x  x  x  x |
| x  x  x  x  x  x  |            | x  x  x  x  x  x  |         | - | x  x  x  x  x |
+-------------------+            +-------------------+         +---+---------------+

Add Back Top-Left Q(r1-1, c1-1) to restore double-subtracted intersection! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 308 (Range Sum Query 2D - Mutable using 2D Fenwick Tree):

```java
import java.util.*;

// LeetCode 308: Range Sum Query 2D - Mutable
public class NumMatrix2DFenwick {

    private final int[][] tree;
    private final int[][] matrix;
    private final int m;
    private final int n;

    public NumMatrix2DFenwick(int[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            this.m = 0; this.n = 0;
            this.tree = new int[0][0];
            this.matrix = new int[0][0];
            return;
        }

        this.m = matrix.length;
        this.n = matrix[0].length;
        this.tree = new int[m + 1][n + 1];
        this.matrix = new int[m][n];

        // Populate 2D Fenwick Tree using point additions
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                update(r, c, matrix[r][c]);
            }
        }
    }

    // 2D Additive Point Update O(log M * log N) Time
    private void add(int row, int col, int delta) {
        for (int r = row; r <= m; r += (r & -r)) {
            for (int c = col; c <= n; c += (c & -c)) {
                tree[r][c] += delta; // Nested bitwise LSB addition
            }
        }
    }

    // LeetCode 308 Value Replacement Update O(log M * log N) Time
    public void update(int row, int col, int val) {
        if (m == 0 || n == 0) return;
        int delta = val - matrix[row][col];
        matrix[row][col] = val;

        add(row + 1, col + 1, delta); // Convert to 1-based indexing
    }

    // 2D Prefix Sum Query Q(row, col) O(log M * log N) Time
    private int query(int row, int col) {
        int sum = 0;
        for (int r = row; r > 0; r -= (r & -r)) {
            for (int c = col; c > 0; c -= (c & -c)) {
                sum += tree[r][c]; // Nested bitwise LSB subtraction
            }
        }
        return sum;
    }

    // LeetCode 308 Submatrix Region Sum Query O(log M * log N) Time
    public int sumRegion(int row1, int col1, int row2, int col2) {
        if (m == 0 || n == 0) return 0;

        // 2D Inclusion-Exclusion Formula using 1-based indexing
        int r2 = row2 + 1, c2 = col2 + 1;
        int r1 = row1,     c1 = col1;

        return query(r2, c2) - query(r1, c2) - query(r2, c1) + query(r1, c1);
    }
}
```

> **Quick Syntax:**
```java
// 2D Submatrix Inclusion-Exclusion Line
return query(row2 + 1, col2 + 1) - query(row1, col2 + 1) - query(row2 + 1, col1) + query(row1, col1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 308 - Range Sum Query 2D - Mutable**: Primary 2D BIT problem.
* **Dynamic Image Submatrix Processing**: Dynamic pixel region updates.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 308 `NumMatrix2DFenwick`:

```java
public class NumMatrix2DFenwickDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 308 2D Fenwick Tree Test ===");
        int[][] matrix = {
            {3, 0, 1, 4, 2},
            {5, 6, 3, 2, 1},
            {1, 2, 0, 1, 5},
            {4, 1, 0, 1, 7},
            {1, 0, 3, 0, 5}
        };

        NumMatrix2DFenwick numMatrix = new NumMatrix2DFenwick(matrix);

        System.out.println("Submatrix Sum (2,1) to (4,3): " + 
            numMatrix.sumRegion(2, 1, 4, 3)); // Output: 8

        System.out.println("\nUpdating Cell (3,2) from 0 to 2...");
        numMatrix.update(3, 2, 2);

        System.out.println("Submatrix Sum (2,1) to (4,3) AFTER Update: " + 
            numMatrix.sumRegion(2, 1, 4, 3)); // Output: 10 ✅
    }
}
```

---

## 9. Complexity Analysis

| 2D Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`update(r, c, v)`** | **$O(\log M \cdot \log N)$ ⚡**| **$O(M \cdot N)$ Matrix Space**| Nested row/col LSB loops |
| **`sumRegion()`**     | **$O(\log M \cdot \log N)$ ⚡**| **$O(1)$ Auxiliary Space**| 4 2D prefix queries |

---

## 10. Edge Cases & Boundary Handling
* **$1 \times 1$ Matrix**: Evaluates safely in $O(1)$ time.
* **Entire Matrix Query (`(0,0)` to `(M-1, N-1)`)**: Returns total sum via `query(M, N)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Top-Left Addition `+ Q(r1, c1)` in 2D Inclusion-Exclusion**:
  - Subtracting both top and left regions double-subtracts the top-left intersection region `(0,0) ... (r1-1, c1-1)`.
  - **ALWAYS re-add `+ query(row1, col1)` at the end of `sumRegion`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Cleanest 2D Inclusion-Exclusion Formula Indexing:
> For 0-based input parameters `(row1, col1, row2, col2)`:
> Define 1-based bounds: $r_2 = \text{row2} + 1$, $c_2 = \text{col2} + 1$, $r_1 = \text{row1}$, $c_1 = \text{col1}$.
> Formula: **`return query(r2, c2) - query(r1, c2) - query(r2, c1) + query(r1, c1);`**
> This clean notation avoids off-by-one errors! ⚡

> **Memory Trick:** **"2D Submatrix = Q(r2+1, c2+1) - Q(r1, c2+1) - Q(r2+1, c1) + Q(r1, c1)!"**

---

## 13. System & Implementation Comparisons

| Feature | 2D Fenwick Tree (LeetCode 308) | 2D Prefix Sum Matrix |
| :--- | :--- | :--- |
| **Update Time** | **$O(\log M \cdot \log N)$ Logarithmic ⚡**| $O(M \cdot N)$ Full Matrix Scan ❌ |
| **Query Time** | **$O(\log M \cdot \log N)$ Logarithmic ⚡**| **$O(1)$ Constant Time ⚡** |
| **Code Simplicity** | **15 Lines Nested Loops ⚡** | ~30 Lines |

---

## 14. How to Recognize This in Questions
* **"Dynamic 2D matrix submatrix sum queries and point updates"** $\rightarrow$ LeetCode 308 (2D Fenwick Tree).

---

## 15. Frequently Asked Interview Questions
* **Q: How does a 2D Fenwick Tree handle row and column updates?**  
  *A:* Using nested bitwise loops: outer loop `r += r & (-r)`, inner loop `c += c & (-c)`.
* **Q: What is the auxiliary space complexity of a 2D Fenwick Tree?**  
  *A:* $O(M \cdot N)$ memory for the 2D `tree[M + 1][N + 1]` array.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: 2D FENWICK TREES (LEETCODE 308)                       |
+-----------------------------------------------------------------------+
| • Nested Traversal: for (r; r>0; r-=r&-r) for (c; c>0; c-=c&-c) sum+=tree[r][c]|
| • Formula         : Q(r2+1, c2+1) - Q(r1, c2+1) - Q(r2+1, c1) + Q(r1, c1)|
| • Point Update    : Delta = new - old; add(r+1, c+1, delta)           |
| • Time Bounds     : O(log M * log N) for both updates and region queries|
| • Space Bounds    : O(M * N) Matrix Array Space ⚡                     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 308 (`NumMatrix2DFenwick`) in Java.
- [ ] I can write nested LSB loops for 2D update and 2D query.
- [ ] I can derive the 2D Inclusion-Exclusion submatrix formula.
- [ ] I know why top-left intersection `+ Q(r1, c1)` must be added back.
- [ ] I can trace 2D submatrix sum queries step by step.
