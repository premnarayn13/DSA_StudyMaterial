# 05. N-Queens Problem, Constraint Propagation & Diagonal Indexing Rules

## 1. Introduction
The **N-Queens Problem** (LeetCode 51 & 52) is the quintessential constraint satisfaction problem in backtracking. The objective is to place $N$ chess queens on an $N \times N$ chessboard such that **NO TWO QUEENS ATTACK EACH OTHER** (no two queens share the same row, column, main diagonal, or anti-diagonal). Using **Row-by-Row Backtracking** combined with $O(1)$ HashSets or Bitmasks for diagonal collision checks, the N-Queens solver executes in **$O(N!)$ Time** and **$O(N)$ Auxiliary Space**.

> **Important:** Mathematical Indexing Rules for $O(1)$ Attack Checking:
> 1. **Row Constraint**: Place exactly ONE queen per row $r \in [0 \dots N-1]$. This automatically guarantees no two queens share a row!
> 2. **Column Constraint (`cols` Set)**: Track occupied columns using a `boolean[] cols` or `Set<Integer> cols` array of size $N$.
> 3. **Main Diagonal Constraint (`diagonals` Set)**:
>    - All cells on the same main diagonal (top-left to bottom-right) share the CONSTANT DIFFERENCE: **$(r - c)$**!
>    - Indexed via `cols + (r - c) + (N - 1)` or `Set<Integer> diagonals`.
> 4. **Anti-Diagonal Constraint (`antiDiagonals` Set)**:
>    - All cells on the same anti-diagonal (top-right to bottom-left) share the CONSTANT SUM: **$(r + c)$**!
>    - Indexed via `(r + c)` or `Set<Integer> antiDiagonals`. ⚡

```
N-Queens Board Indexing Topology (N = 4):
Main Diagonal (r - c = Constant):               Anti-Diagonal (r + c = Constant):
 (0,0)-> 0   (0,1)-> -1  (0,2)-> -2             (0,0)-> 0   (0,1)-> 1   (0,2)-> 2
 (1,0)-> 1   (1,1)-> 0   (1,2)-> -1             (1,0)-> 1   (1,1)-> 2   (1,2)-> 3
 (2,0)-> 2   (2,1)-> 1   (2,2)-> 0              (2,0)-> 2   (2,1)-> 3   (2,2)-> 4

Main Diagonal ID: (r - c + N - 1) | Anti-Diagonal ID: (r + c) ⚡
```

---

## 2. Core Concepts & LeetCode 51 vs 52 Strategy Matrix

### 2.1 N-Queens Problem Variant Matrix
```
N-Queens Problem Variant Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Output Format     | Goal              | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **N-Queens I (51)**   | `List<List<String>>`| Return all boards | **$O(N!)$ Factorial ⚡**|
| **N-Queens II (52)**  | `int totalCount`  | Count total solutions| **$O(N!)$ Factorial ⚡**|
| **Bitmask N-Queens**  | Bitwise Bitmask   | Fast counting     | **$O(N!)$ Factorial ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Main Diagonal = r - c + (N-1)! Anti-Diagonal = r + c! O(1) collision checks!"**

---

## 3. Characteristics & $O(N!)$ Time Complexity Bounds

### 3.1 Mathematical Proof of $O(N!)$ Complexity
* Row 0 has $N$ valid column choices.
* Row 1 has at most $N - 1$ un-attacked column choices.
* Row 2 has at most $N - 2$ choices.
* Upper bound on total state search space = $N \times (N-1) \times \dots \times 1 = \mathbf{O(N!) \text{ Factorial Time}}$. ⚡

---

## 4. Internal Working Mechanics
Tracing N-Queens Placement on $4 \times 4$ Board:

```
Row 0: Place Queen at (0, 1). Occupied: cols={1}, diag={0-1+3=2}, anti={0+1=1}.
Row 1: Try col 0 -> Attack! Try col 1 -> Attack! Try col 3 -> Valid!
       Place Queen at (1, 3). Occupied: cols={1,3}, diag={2, 1-3+3=1}, anti={1, 1+3=4}.
Row 2: Try col 0 -> Valid!
       Place Queen at (2, 0). Occupied: cols={1,3,0}, diag={2,1, 2-0+3=5}, anti={1,4, 2+0=2}.
Row 3: Try all cols 0..3 -> ALL ATTACKED! Backtrack to Row 2!

Unwind & Backtrack: Moves Queen to (0, 2) -> Finds valid board:
. Q . .
. . . Q
Q . . .
. . Q .

Valid Solution Found! ✅ (O(N!) Time!)
```

---

## 5. Visual Diagram
$4 \times 4$ N-Queens Valid Solution Topography:

```
    Col 0   Col 1   Col 2   Col 3
Row 0 [. ]    [Q]     [. ]    [. ]
Row 1 [. ]    [. ]    [. ]    [Q]
Row 2 [Q]     [. ]    [. ]    [. ]
Row 3 [. ]    [. ]    [Q]     [. ]   <--- Valid N-Queens Board Configuration! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 51 (N-Queens Board Construction) and LeetCode 52 (N-Queens Total Count):

```java
import java.util.*;

// LeetCode 51 & 52: N-Queens Master Class
public class NQueensMaster {

    // 1. LeetCode 51: Return All Valid N-Queens Board Configurations O(N!) Time
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> result = new ArrayList<>();
        if (n <= 0) return result;

        boolean[] cols = new boolean[n];
        boolean[] diagonals = new boolean[2 * n];     // r - c + (n - 1)
        boolean[] antiDiagonals = new boolean[2 * n]; // r + c

        char[][] board = new char[n][n];
        for (int r = 0; r < n; r++) {
            Arrays.fill(board[r], '.');
        }

        backtrackNQueens(n, 0, board, cols, diagonals, antiDiagonals, result);
        return result;
    }

    private void backtrackNQueens(int n, int row, char[][] board, 
                                 boolean[] cols, boolean[] diagonals, boolean[] antiDiagonals, 
                                 List<List<String>> result) {
        // Base Case: All N Queens placed successfully in N rows!
        if (row == n) {
            result.add(constructBoard(board));
            return;
        }

        for (int col = 0; col < n; col++) {
            int diagIdx = row - col + (n - 1);
            int antiDiagIdx = row + col;

            // Collision Guard Check in O(1) Time
            if (cols[col] || diagonals[diagIdx] || antiDiagonals[antiDiagIdx]) {
                continue; // Under attack! Skip column.
            }

            // Step 1: CHOOSE (Place Queen & Mark Constraints)
            board[row][col] = 'Q';
            cols[col] = true;
            diagonals[diagIdx] = true;
            antiDiagonals[antiDiagIdx] = true;

            // Step 2: RECURSE to next row
            backtrackNQueens(n, row + 1, board, cols, diagonals, antiDiagonals, result);

            // Step 3: BACKTRACK (Remove Queen & Unmark Constraints)
            board[row][col] = '.';
            cols[col] = false;
            diagonals[diagIdx] = false;
            antiDiagonals[antiDiagIdx] = false;
        }
    }

    private List<String> constructBoard(char[][] board) {
        List<String> list = new ArrayList<>();
        for (char[] row : board) {
            list.add(new String(row));
        }
        return list;
    }

    // 2. LeetCode 52: Return Count of Total N-Queens Solutions O(N!) Time
    public int totalNQueens(int n) {
        boolean[] cols = new boolean[n];
        boolean[] diagonals = new boolean[2 * n];
        boolean[] antiDiagonals = new boolean[2 * n];

        return countNQueens(n, 0, cols, diagonals, antiDiagonals);
    }

    private int countNQueens(int n, int row, boolean[] cols, boolean[] diagonals, boolean[] antiDiagonals) {
        if (row == n) return 1; // Found 1 valid solution

        int count = 0;
        for (int col = 0; col < n; col++) {
            int diagIdx = row - col + (n - 1);
            int antiDiagIdx = row + col;

            if (cols[col] || diagonals[diagIdx] || antiDiagonals[antiDiagIdx]) continue;

            cols[col] = diagonals[diagIdx] = antiDiagonals[antiDiagIdx] = true;
            count += countNQueens(n, row + 1, cols, diagonals, antiDiagonals);
            cols[col] = diagonals[diagIdx] = antiDiagonals[antiDiagIdx] = false; // Backtrack
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// N-Queens Collision Check Line
int diagIdx = row - col + (n - 1), antiDiagIdx = row + col;
if (cols[col] || diagonals[diagIdx] || antiDiagonals[antiDiagIdx]) continue;
```

---

## 7. Concrete Problem Examples
* **LeetCode 51 - N-Queens**: Full board representation output.
* **LeetCode 52 - N-Queens II**: Total solution count calculation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 51 and 52 for $N = 4$:

```java
public class NQueensDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 51 N-Queens Board Test ===");
        NQueensMaster solver = new NQueensMaster();

        int n = 4;
        List<List<String>> boards = solver.solveNQueens(n);
        int totalSolutions = solver.totalNQueens(n);

        System.out.println("Total Solutions for N = 4: " + totalSolutions); // Output: 2

        System.out.println("Generated Board 1:");
        for (String row : boards.get(0)) {
            System.out.println(row);
        }
        // Output shows valid N-Queens chessboard! ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **N-Queens I (51)** | **$O(N!)$ Factorial ⚡**| **$O(N^2)$ Board + Stack**| $O(1)$ diagonal collision array check |
| **N-Queens II (52)**| **$O(N!)$ Factorial ⚡**| **$O(N)$ Call Stack Memory**| Direct solution counting |

---

## 10. Edge Cases & Boundary Handling
* **$N = 1$**: Single cell board `[["Q"]]`, returning 1 solution.
* **$N = 2$ and $N = 3$**: No valid solutions exist, returning empty list `[]` and count `0`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using $O(N)$ Diagonal Scanning Loops in `isSafe()` Method**:
  - Scanning up-left and up-right diagonals using $O(N)$ `while` loops per cell degrades search speed by $N \times$.
  - **ALWAYS use $O(1)$ boolean tracking arrays for `diagonals[r - c + N - 1]` and `antiDiagonals[r + c]`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Mathematical Proof of Diagonal Indexing Formulas:
> 1. **Main Diagonal (Top-Left to Bottom-Right)**:
>    - Cells $(0,0), (1,1), (2,2)$ share $r - c = 0$.
>    - Range of $r - c$ is $[-(N-1) \dots (N-1)]$. Adding offset $+(N - 1)$ shifts indices into positive array range $[0 \dots 2N - 2]$!
> 2. **Anti-Diagonal (Top-Right to Bottom-Left)**:
>    - Cells $(0,2), (1,1), (2,0)$ share $r + c = 2$. Range is $[0 \dots 2N - 2]$ directly! ⚡

> **Memory Trick:** **"Main Diag Index = r - c + N - 1! Anti-Diag Index = r + c!"**

---

## 13. System & Implementation Comparisons

| Feature | $O(1)$ Array Collision Check | $O(N)$ Scanning `isSafe()` Check |
| :--- | :--- | :--- |
| **Collision Check Time**| **$O(1)$ Instant Lookup ⚡** | $O(N)$ Loop Scanning |
| **Space Overhead** | $O(N)$ Boolean Arrays | Zero Memory |
| **Performance** | **10x Faster Execution ⚡** | Slow Execution |

---

## 14. How to Recognize This in Questions
* **"Place N items on grid such that no two attack diagonally or orthogonally"** $\rightarrow$ N-Queens (LeetCode 51).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does N-Queens recurse row-by-row instead of cell-by-cell?**  
  *A:* Because placing 1 queen per row reduces search depth to $N$ and automatically eliminates row collisions.
* **Q: How does `row - col + (n - 1)` index main diagonals?**  
  *A:* $r - c$ is constant along main diagonals; adding $+(n - 1)$ maps negative values to valid 0-based array indices.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: N-QUEENS PROBLEM (LEETCODE 51 & 52)                   |
+-----------------------------------------------------------------------+
| • Row Invariant  : Recurse row-by-row (row == n is base case!)        |
| • Column Guard   : cols[col]                                          |
| • Main Diag Guard: diagonals[row - col + (n - 1)]                     |
| • Anti Diag Guard: antiDiagonals[row + col]                           |
| • Backtracking   : Unmark cols, diagonals, antiDiagonals on return    |
| • Performance    : O(N!) Time | O(N) Call Stack Space ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 51 (`N-Queens`) in Java.
- [ ] I can write LeetCode 52 (`N-Queens II`).
- [ ] I know why `row - col + (n - 1)` indexes main diagonals.
- [ ] I know why `row + col` indexes anti-diagonals.
- [ ] I can trace N-Queens placement step by step.
