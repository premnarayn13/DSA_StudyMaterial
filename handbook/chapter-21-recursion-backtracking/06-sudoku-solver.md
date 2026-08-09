# 06. Sudoku Solver, $3 \times 3$ Box Constraint Engines & Grid Invariants

## 1. Introduction
The **Sudoku Solver** (LeetCode 37) and **Valid Sudoku** (LeetCode 36) represent classic 2D grid constraint propagation problems. A standard $9 \times 9$ Sudoku grid must be populated with digits `'1'` through `'9'` such that **EVERY ROW**, **EVERY COLUMN**, and **EVERY OF THE NINE $3 \times 3$ SUB-BOXES** contains all digits `'1'` through `'9'` without duplication. Solved via **Cell-by-Cell Backtracking**, Sudoku solvers modify the $9 \times 9$ board array in-place, returning `true` as soon as a complete valid assignment is achieved.

> **Important:** The $3 \times 3$ Sub-Box Indexing & Validity Invariant:
> 1. **Cell-by-Cell Grid Scan**: Loop rows $r \in [0 \dots 8]$, cols $c \in [0 \dots 8]$. Find first empty cell `board[r][c] == '.'`.
> 2. **Digit Trial Loop**: Try placing digits $ch \in ['1' \dots '9']$.
> 3. **$O(1)$ Validity Invariant (`isValid(board, r, c, ch)`)**:
>    - Row Check: `board[r][i] == ch` for $i \in [0 \dots 8]$.
>    - Column Check: `board[i][c] == ch` for $i \in [0 \dots 8]$.
>    - **$3 \times 3$ Box Formula Check**:
>      $$\text{BoxRow} = 3 \cdot \left(\frac{r}{3}\right) + \frac{i}{3} \quad \text{and} \quad \text{BoxCol} = 3 \cdot \left(\frac{c}{3}\right) + (i \pmod 3) \quad (\text{for } i \in [0 \dots 8])$$
> 4. **Early Termination Signal**: When all empty cells are filled, return `true` to immediately short-circuit all remaining recursion stack frames! ⚡

```
$3 \times 3$ Sub-Box Indexing Math Topology:
Target Cell (r = 4, c = 7):
Sub-Box Origin: startRow = 3 * (4 / 3) = 3 * 1 = 3, startCol = 3 * (7 / 3) = 3 * 2 = 6

Iterating i from 0 to 8 scans all 9 cells inside sub-box [3..5][6..8]! ⚡
```

---

## 2. Core Concepts & LeetCode 36 vs 37 Strategy Matrix

### 2.1 Sudoku Problem Variant Matrix
```
Sudoku Problem Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Goal              | Traversal Method  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Valid Sudoku (36)** | Validate initial  | Single $9\times9$ Scan| **$O(1)$ Constant ⚡**|
| **Sudoku Solver (37)**| Complete solver   | Cell Backtracking | **$O(9^E) \approx O(1)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sudoku 3x3 Box Origin: startRow = 3 * (r / 3), startCol = 3 * (c / 3)! Return true on first complete board!"**

---

## 3. Characteristics & Practical Time Complexity Bounds

### 3.1 Mathematical Complexity Bounds
* Upper bound on total search states: $9^{81}$ (assuming 81 empty cells).
* In practice, constraint propagation reduces empty cells $E \ll 81$, executing in under $1 \text{ ms}$ on $9 \times 9$ boards!
* Fixed $9 \times 9$ grid size dictates **$O(1)$ Constant Time** and **$O(1)$ Constant Stack Memory Space**! ⚡

---

## 4. Internal Working Mechanics
Tracing Sudoku Backtracking on Empty Cell $(r = 0, c = 2)$:

```
Cell (0, 2) is '.':
- Try ch = '1': isValid(0, 2, '1') returns false (1 exists in row 0!).
- Try ch = '2': isValid(0, 2, '2') returns false (2 exists in 3x3 box!).
- Try ch = '5': isValid(0, 2, '5') returns true!
  - Place board[0][2] = '5'.
  - Recurse solve(board):
    - Subtree returns false (Lead to dead end).
  - BACKTRACK: Reset board[0][2] = '.'.
- Try ch = '6': isValid(0, 2, '6') returns true!
  - Place board[0][2] = '6'.
  - Recurse solve(board) -> Returns true!

Complete Board Solved! Short-circuit returns true! ✅
```

---

## 5. Visual Diagram
$3 \times 3$ Box Partition Topography:

```
    Cols 0 1 2   Cols 3 4 5   Cols 6 7 8
Rows 0..2  [ Box 0 ]    [ Box 1 ]    [ Box 2 ]
Rows 3..5  [ Box 3 ]    [ Box 4 ]    [ Box 5 ]  <--- Cell (4, 7) belongs to Box 5!
Rows 6..8  [ Box 6 ]    [ Box 7 ]    [ Box 8 ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 37 (Sudoku Solver) and LeetCode 36 (Valid Sudoku):

```java
import java.util.*;

// LeetCode 36 & 37: Sudoku Solver Master Class
public class SudokuSolverMaster {

    // 1. LeetCode 37: Solve Sudoku Grid In-Place O(1) Time & Space
    public void solveSudoku(char[][] board) {
        if (board == null || board.length != 9 || board[0].length != 9) return;
        solve(board);
    }

    private boolean solve(char[][] board) {
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') { // Empty cell found
                    for (char ch = '1'; ch <= '9'; ch++) {
                        if (isValid(board, r, c, ch)) {
                            board[r][c] = ch; // Choose digit

                            if (solve(board)) {
                                return true; // Short-circuit: Complete board solved!
                            }

                            board[r][c] = '.'; // BACKTRACK (Reset cell)
                        }
                    }
                    return false; // All 9 digits failed! Trigger backtracking up stack.
                }
            }
        }
        return true; // All empty cells successfully populated!
    }

    // O(1) Validity Checker
    public boolean isValid(char[][] board, int row, int col, char ch) {
        for (int i = 0; i < 9; i++) {
            // Check Row Constraint
            if (board[row][i] == ch) return false;

            // Check Column Constraint
            if (board[i][col] == ch) return false;

            // Check 3x3 Sub-Box Constraint
            int boxRow = 3 * (row / 3) + i / 3;
            int boxCol = 3 * (col / 3) + i % 3;
            if (board[boxRow][boxCol] == ch) return false;
        }
        return true;
    }

    // 2. LeetCode 36: Valid Sudoku Checker O(1) Time & Space
    public boolean isValidSudoku(char[][] board) {
        Set<String> seen = new HashSet<>();

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char val = board[r][c];
                if (val != '.') {
                    // Encode unique row, col, and box string keys
                    if (!seen.add(val + " in row " + r) ||
                        !seen.add(val + " in col " + c) ||
                        !seen.add(val + " in box " + (r / 3) + "-" + (c / 3))) {
                        return false; // Duplicate digit detected!
                    }
                }
            }
        }
        return true;
    }
}
```

> **Quick Syntax:**
```java
// Sudoku 3x3 Box Constraint Line
int boxRow = 3 * (row / 3) + i / 3, boxCol = 3 * (col / 3) + i % 3;
if (board[boxRow][boxCol] == ch) return false;
```

---

## 7. Concrete Problem Examples
* **LeetCode 37 - Sudoku Solver**: Full 2D grid solver.
* **LeetCode 36 - Valid Sudoku**: Validation engine.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 37 `solveSudoku`:

```java
public class SudokuSolverDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 37 Sudoku Solver Test ===");
        SudokuSolverMaster solver = new SudokuSolverMaster();

        char[][] board = {
            {'5','3','.','.','7','.','.','.','.'},
            {'6','.','.','1','9','5','.','.','.'},
            {'.','9','8','.','.','.','.','6','.'},
            {'8','.','.','.','6','.','.','.','3'},
            {'4','.','.','8','.','3','.','.','1'},
            {'7','.','.','.','2','.','.','.','6'},
            {'.','6','.','.','.','.','2','8','.'},
            {'.','.','.','4','1','9','.','.','5'},
            {'.','.','.','.','8','.','.','7','9'}
        };

        solver.solveSudoku(board);

        System.out.println("Solved Sudoku Grid (Row 0): " + new String(board[0]));
        // Output shows fully populated valid Sudoku board! ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Valid Sudoku (36)**| **$O(1)$ Constant ⚡** | **$O(1)$ HashSet Memory**| Single 81-cell scan |
| **Sudoku Solver (37)**| **$O(1)$ Constant ⚡** | **$O(1)$ Call Stack Memory**| Cell-by-cell grid backtracking |

---

## 10. Edge Cases & Boundary Handling
* **Invalid Board Input**: `solve()` returns `false`, leaving board unmodified.
* **Fully Solved Board Input**: `solve()` returns `true` immediately without modifying any cell.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `return true` When `solve(board)` Returns True**:
  - Failing to propagate `return true` up the recursion stack causes the solver to backtrack past the solved configuration, resetting cells back to `'.'`.
  - **ALWAYS return `true` immediately when `if (solve(board))` succeeds**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `isValid()` Can Scan Row, Col, and Box in 1 Single Loop (`i = 0..8`):
> Instead of writing 3 separate loops, loop $i = 0 \dots 8$ evaluates:
> 1. Row element: `board[row][i]`
> 2. Column element: `board[i][col]`
> 3. Sub-box element: `board[3 * (row / 3) + i / 3][3 * (col / 3) + i % 3]`
> This combines all 3 constraint checks into a single 9-step loop! ⚡

> **Memory Trick:** **"Check row, col, and 3x3 box in 1 single 9-step loop using i / 3 and i % 3!"**

---

## 13. System & Implementation Comparisons

| Feature | Cell-by-Cell Backtracking | Constraint Satisfaction Engine |
| :--- | :--- | :--- |
| **Grid Size** | Fixed $9 \times 9$ Board | Arbitrary $N \times N$ Grid |
| **Space Overhead** | **$O(1)$ In-Place Board Mod ⚡**| Additional Constraint Sets |
| **Code Length** | **~20 Lines Clean Code ⚡** | ~60 Lines |

---

## 14. How to Recognize This in Questions
* **"Fill 2D grid satisfying row, column, and sub-grid constraints"** $\rightarrow$ Sudoku Solver (LeetCode 37).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `solveSudoku` return a boolean value?**  
  *A:* To allow short-circuit evaluation: returning `true` immediately stops further recursive calls once a valid board assignment is found.
* **Q: How does `3 * (row / 3) + i / 3` calculate the sub-box row?**  
  *A:* `3 * (row / 3)` finds the top row of the $3 \times 3$ box; `i / 3` steps down rows 0, 1, and 2 as $i$ goes from 0 to 8.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUDOKU SOLVER (LEETCODE 37)                           |
+-----------------------------------------------------------------------+
| • Search Strategy : Find empty '.', try digits '1'..'9', recurse      |
| • Sub-Box Formula : boxRow = 3 * (r / 3) + i / 3; boxCol = 3 * (c / 3) + i % 3;|
| • Validity Check  : Check row, col, and 3x3 box in 1 loop (i = 0..8)  |
| • Short-Circuit   : if (solve(board)) return true;                    |
| • Backtrack Reset : board[r][c] = '.' on failure                      |
| • Performance     : O(1) Constant Time | O(1) In-Place Memory ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 37 (`Sudoku Solver`) in Java.
- [ ] I can write LeetCode 36 (`Valid Sudoku`).
- [ ] I know how `3 * (row / 3) + i / 3` computes sub-box indices.
- [ ] I know why boolean return short-circuiting is mandatory.
- [ ] I can trace Sudoku backtracking step by step.
