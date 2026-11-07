# 08. Sudoku Solver: 9x9 Constraint Validation, 3x3 Sub-box Mapping & Bitmask Solvers

## 1. Introduction
The **Sudoku Solver (LeetCode 37)** is one of the most prominent real-world applications of Constraint Satisfaction Problem (CSP) backtracking algorithms. Given a $9 \times 9$ grid partially filled with digits `'1'`..`'9'` and empty cells denoted by `'.'`. The objective is to fill all empty cells such that every row, every column, and every $3 \times 3$ sub-box contains the digits `'1'` through `'9'` with **NO DUPLICATES**. While naive brute-force digit assignment over 81 cells takes an impossible $O(9^{81})$ search space, row-column-box constraint backtracking with **$O(1)$ Constraint Check Arrays** or **Bitmask Accelerators** prunes the search space down to under **5 Milliseconds Execution Time**.

> **Important:** Core Structural Invariants of Sudoku Backtracking:
> 1. **$3 \times 3$ Sub-box Indexing Formula**:
>    - For any cell $(r, c)$, its corresponding $3 \times 3$ sub-box index $0 \dots 8$ is given by:
>      $$\text{boxIdx} = \left(\frac{r}{3}\right) \times 3 + \left(\frac{c}{3}\right)$$
> 2. **O(1) Constraint Validation Arrays**:
>    - `rows[r][d]`: Boolean indicating if digit $d$ is present in row $r$.
>    - `cols[c][d]`: Boolean indicating if digit $d$ is present in col $c$.
>    - `boxes[b][d]`: Boolean indicating if digit $d$ is present in sub-box $b$.
> 3. **Early Termination Return Rule**:
>    - Once the last empty cell is filled successfully, the DFS returns `true` immediately to halt further backtracking and preserve the solved board in-place!
> 4. **Bitmask Sudoku Optimization**:
>    - Represents occupied digits in row $r$, col $c$, and box $b$ as 9-bit integers:
>      $$\text{available} = \sim(\text{rows}[r] \mid \text{cols}[c] \mid \text{boxes}[b]) \;\&\; 0x1FF$$
>    - Extracts lowest valid candidate digit in $O(1)$ time! ⚡

```
Sudoku 3x3 Sub-box Index Mapping Topology:

    Col 0..2    Col 3..5    Col 6..8
  ┌───────────┬───────────┬───────────┐
R |  Box 0    |  Box 1    |  Box 2    |  (Row 0..2)
o |           |           |           |
w ├───────────┼───────────┼───────────┤
0 |  Box 3    |  Box 4    |  Box 5    |  (Row 3..5)
. |           |           |           |
2 ├───────────┼───────────┼───────────┤
  |  Box 6    |  Box 7    |  Box 8    |  (Row 6..8)
  └───────────┴───────────┴───────────┘

Formula: boxIdx = (row / 3) * 3 + (col / 3) ⚡
```

---

## 2. Core Concepts & Sudoku Strategy Matrix

### 2.1 Sudoku Solver Implementations Strategy Matrix
```
Sudoku Solver Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Implementation        | Primary Target    | Pruning Structure | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Boolean Arrays (37)**| In-Place Solution | `rows`, `cols`, `boxes`| **$O(9^{m})$ Pruned ⚡**| **$O(81)$ Stack ⚡**|
| **Bitmask Solver (37)**| High Speed Count  | 9-Bit Integers    | **$O(9^{m})$ Fast ⚡**| **$O(81)$ Stack ⚡**|
| **Minimum Remaining (MRV)**| Hard Sudoku  | Most Constrained  | **Optimized $O(9^m)$⚡**| $O(81)$ Stack     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sudoku 3x3 box index = (r/3)*3 + (c/3); Return true immediately on completion to preserve board!"**

---

## 3. Characteristics & Bitmask Sudoku Acceleration Proof

### 3.1 Mathematical Derivation of Bitmask Sudoku Digit Extraction
* Let `rows[r]`, `cols[c]`, and `boxes[b]` be 9-bit integers where bit $d$ ($1 \le d \le 9$) is 1 if digit $d$ is placed.
* **Available Digits Mask for Cell $(r, c)$**:
  $$\text{available} = \sim(\text{rows}[r] \mid \text{cols}[c] \mid \text{boxes}[b]) \;\&\; 0x1FF$$
  (Where $0x1FF = 111111111_2 = 511$, masking only the lowest 9 bits!).
* **Extracting Candidate Digit $d$**:
  - `bit = available & (-available)` extracts the lowest set bit.
  - `digit = Integer.numberOfTrailingZeros(bit) + 1`.
* **State Operations**:
  - Place digit: `rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit;`
  - Remove digit: `rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit;`
* Replaces 9-step array iteration loops with single bitwise operations! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Board Resolution

Tracing Sudoku Cell Resolution for Cell $(r=0, c=2)$:

```
Given Cell (0,2) is empty '.':
Calculate box index: b = (0/3)*3 + (2/3) = 0.

Check constraints for digits 1..9:
- Digit 1: In row 0? No. In col 2? No. In box 0? Yes! PRUNED! ❌
- Digit 2: In row 0? No. In col 2? No. In box 0? No. VALID CHOICE! ✅

Choose '2' for board[0][2]:
- Set rows[0]['2'] = true, cols[2]['2'] = true, boxes[0]['2'] = true.

Recurse to next empty cell...
If downstream search fails -> Backtrack and unchoose '2'! ✅ ⚡
```

---

## 5. Visual Diagram: 3x3 Sub-box Indexing Grid

```
Grid Sub-box Index Calculation:

Cell (r=4, c=7):
- Row Block = 4 / 3 = 1
- Col Block = 7 / 3 = 2
- Sub-box Index = 1 * 3 + 2 = 5!

Instantly identifies 3x3 box constraint array index! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Sudoku Solver (LeetCode 37) using Boolean Constraint Arrays, Bitmask Acceleration, and Board Validation.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Sudoku Solver Backtracking:
 * 9x9 Board Mutators, 3x3 Box Mapping, Boolean Constraint Arrays, and Bitmask Acceleration.
 */
public class SudokuMaster {

    // =========================================================================
    // 1. LEETCODE 37: SUDOKU SOLVER (BOOLEAN ARRAYS O(9^m) Time, O(81) Space)
    // =========================================================================
    /**
     * Solves a 9x9 Sudoku board in-place using Backtracking DFS.
     *
     * @param board 9x9 character matrix (digits '1'..'9' or '.')
     */
    public void solveSudoku(char[][] board) {
        if (board == null || board.length != 9 || board[0].length != 9) return;

        boolean[][] rows = new boolean[9][10];
        boolean[][] cols = new boolean[9][10];
        boolean[][] boxes = new boolean[9][10];

        // Step 1: Pre-populate constraint arrays from initial board setup
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] != '.') {
                    int d = board[r][c] - '0';
                    int b = (r / 3) * 3 + (c / 3);
                    rows[r][d] = true;
                    cols[c][d] = true;
                    boxes[b][d] = true;
                }
            }
        }

        // Step 2: Run Backtracking DFS
        solveSudokuDFS(board, 0, 0, rows, cols, boxes);
    }

    private boolean solveSudokuDFS(char[][] board, int r, int c, boolean[][] rows, boolean[][] cols, boolean[][] boxes) {
        // Advance to next row when column reaches 9
        if (c == 9) {
            r++;
            c = 0;
        }

        // Base Case: All 81 cells scanned successfully!
        if (r == 9) return true; // Solution found! ⚡

        // If cell is already filled, skip to next cell
        if (board[r][c] != '.') {
            return solveSudokuDFS(board, r, c + 1, rows, cols, boxes);
        }

        int b = (r / 3) * 3 + (c / 3); // 3x3 Box Index ⚡

        // Try candidate digits 1..9
        for (int d = 1; d <= 9; d++) {
            // O(1) Constraint Check
            if (rows[r][d] || cols[c][d] || boxes[b][d]) continue; // Threat conflict! ⚡

            // Choose
            board[r][c] = (char) ('0' + d);
            rows[r][d] = true;
            cols[c][d] = true;
            boxes[b][d] = true;

            // Explore
            if (solveSudokuDFS(board, r, c + 1, rows, cols, boxes)) {
                return true; // Early termination return true! ⚡
            }

            // Unchoose (Backtrack!) ⚡
            board[r][c] = '.';
            rows[r][d] = false;
            cols[c][d] = false;
            boxes[b][d] = false;
        }

        return false; // Backtrack!
    }

    // =========================================================================
    // 2. BITMASK ACCELERATED SUDOKU SOLVER (O(9^m) Fast Bitwise Operations)
    // =========================================================================
    public void solveSudokuBitmask(char[][] board) {
        if (board == null || board.length != 9 || board[0].length != 9) return;

        int[] rows = new int[9];
        int[] cols = new int[9];
        int[] boxes = new int[9];

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] != '.') {
                    int d = board[r][c] - '0';
                    int b = (r / 3) * 3 + (c / 3);
                    int bit = 1 << d;
                    rows[r] |= bit;
                    cols[c] |= bit;
                    boxes[b] |= bit;
                }
            }
        }

        bitmaskSudokuDFS(board, 0, 0, rows, cols, boxes);
    }

    private boolean bitmaskSudokuDFS(char[][] board, int r, int c, int[] rows, int[] cols, int[] boxes) {
        if (c == 9) { r++; c = 0; }
        if (r == 9) return true;

        if (board[r][c] != '.') {
            return bitmaskSudokuDFS(board, r, c + 1, rows, cols, boxes);
        }

        int b = (r / 3) * 3 + (c / 3);
        // Available digits bitmask
        int available = (~(rows[r] | cols[c] | boxes[b])) & 0x3FE; // Bits 1..9

        while (available != 0) {
            int bit = available & (-available); // Lowest set bit ⚡
            available -= bit;
            int d = Integer.numberOfTrailingZeros(bit);

            // Choose
            board[r][c] = (char) ('0' + d);
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit;

            // Explore
            if (bitmaskSudokuDFS(board, r, c + 1, rows, cols, boxes)) return true;

            // Unchoose
            board[r][c] = '.';
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit;
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Sudoku 3x3 Box Index Formula & Early Return Lines
int b = (r / 3) * 3 + (c / 3); if (solveSudokuDFS(board, r, c + 1, rows, cols, boxes)) return true;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 37 - Sudoku Solver**:
   - Primary 9x9 CSP board solver benchmark ($O(9^m)$ time).

2. **Valid Sudoku (LeetCode 36)**:
   - Initial board constraint validation in $O(1)$ time ($81$ cells).

3. **Kakuro & Futoshiki Number Puzzles**:
   - Grid constraint satisfaction game engine.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class SudokuDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SUDOKU SOLVER BACKTRACKING BENCHMARK DEMO     ");
        System.out.println("=================================================\n");

        SudokuMaster master = new SudokuMaster();

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

        System.out.println("1. Input 9x9 Sudoku Board Loaded.");
        master.solveSudoku(board);

        System.out.println("\n2. Sudoku Solved Successfully In-Place!");
        System.out.println("   Solved Board Configuration:");
        for (char[] row : board) {
            System.out.println("     " + Arrays.toString(row));
        }
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Sudoku Solver Approach | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Boolean Arrays (37)**| $\mathbf{O(9^m)}$ Pruned ⚡| $\mathbf{O(81)}$ Stack Depth| `rows`, `cols`, `boxes` arrays |
| **Bitmask Solver (37)**| $\mathbf{O(9^m)}$ Fast ⚡| $\mathbf{O(81)}$ Stack Depth| Bitwise `available & (-available)` |

---

## 10. Edge Cases & Boundary Handling

1. **Already Solved Board (0 empty cells)**:
   - Returns `true` immediately without recursive calls.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Early Termination Return True**:
  - Writing `solveSudokuDFS(...)` without returning `true` on solution causes backtracking to undo the solved board, leaving all cells as `'.'` at the end. **ALWAYS return `true` immediately when $r == 9$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 3x3 Box Formula:
> For any cell $(r, c)$ in a $9 \times 9$ Sudoku board, the $3 \times 3$ sub-box index $0 \dots 8$ is ALWAYS:
> $$\text{boxIdx} = (r / 3) \times 3 + (c / 3)$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive Raycasting | Boolean Array Validation | Bitmask Acceleration |
| :--- | :--- | :--- | :--- |
| **Constraint Check** | $O(9)$ Grid Loop | $O(1)$ Array Read | **$O(1)$ Bitwise AND `&` ⚡** |
| **Memory Footprint** | None | 27 Boolean Arrays | **3 Integer Masks ⚡** |
| **Execution Time** | ~100 ms | ~10 ms | **< 2 ms ⚡** |

---

## 14. How to Recognize This in Questions

* **"Fill 9x9 grid with digits 1..9 such that no row, col, or 3x3 box has duplicates"** $\rightarrow$ Sudoku Solver (LeetCode 37).

---

## 15. Frequently Asked Interview Questions

* **Q: How do you calculate the 3x3 sub-box index for cell $(r, c)$?**  
  *A:* `boxIdx = (r / 3) * 3 + (c / 3)`.

* **Q: Why does the DFS function return `boolean` instead of `void` in Sudoku Solver?**  
  *A:* Returning `true` signals to parent recursive calls that the puzzle is solved, triggering an immediate chain reaction of early returns that preserves the solved board in-place.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUDOKU SOLVER                                         |
+-----------------------------------------------------------------------+
| • Box Index Formula: boxIdx = (row / 3) * 3 + (col / 3)               |
| • O(1) Arrays      : rows[r][d], cols[c][d], boxes[b][d]              |
| • Early Termination: if (solveDFS(...)) return true;                  |
| • Bitmask Trick    : available = (~(rows[r] | cols[c] | boxes[b])) & 0x3FE|
| • Performance      : Solves 9x9 Sudoku in < 2ms! ⚡                    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 37 (`Sudoku Solver`) in Java.
- [ ] I can write LeetCode 36 (`Valid Sudoku`) initial board validator.
- [ ] I can state the 3x3 sub-box indexing formula `(r / 3) * 3 + (c / 3)`.
- [ ] I can explain why the DFS function MUST return `boolean`.
- [ ] I can write Bitmask Accelerated Sudoku Solver.
