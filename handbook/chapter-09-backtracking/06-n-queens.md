# 06. N-Queens: Column/Diagonal Pruning, Bitmask Accelerators & Solution Counts

## 1. Introduction
The **N-Queens Problem** is the classic benchmark problem of Constraint Satisfaction Problems (CSP) and backtracking algorithms. Given an $N \times N$ chessboard, the objective is to place $N$ non-attacking chess queens such that no two queens share the same **row**, **column**, **main diagonal**, or **anti-diagonal**. While naive brute-force testing of all $N^2$ board positions takes an astronomical $O((N^2)^N)$ time, row-by-row backtracking with **Column and Diagonal Pruning Arrays** reduces execution time to **$O(N!)$ Factorial Time Complexity** and **$O(N)$ Auxiliary Space**. Applying **Bitmask Acceleration** (`(~(cols | diag1 | diag2)) & limit`) speeds up N-Queens state checks by over $10\times$ using $O(1)$ bitwise CPU instructions.

> **Important:** Core Structural Invariants of N-Queens Backtracking:
> 1. **Row-by-Row Search Invariant**:
>    - Place EXACTLY one queen per row ($row = 0 \dots N-1$). This automatically guarantees that no two queens ever share the same row!
> 2. **O(1) Threat Check Arrays**:
>    - Column Check Array: `cols[col]` (size $N$).
>    - Main Diagonal Array (`/` direction): `diag1[row + col]` (size $2N$).
>    - Anti-Diagonal Array (`\` direction): `diag2[row - col + N]` (size $2N$).
> 3. **Bitmask Speedup Invariant (LeetCode 52)**:
>    - Represents occupied columns, main diagonals, and anti-diagonals as bitmasks.
>    - Available placement positions bitmask:
>      $$\text{available} = \sim(\text{cols} \mid \text{diag1} \mid \text{diag2}) \;\&\; ((1 \ll N) - 1)$$
>    - Extracts lowest available bit instantly using `bit = available & (-available)`! ⚡

```
N-Queens Diagonal Constraint Mapping Topology:

Main Diagonal (r + c):             Anti-Diagonal (r - c + N):
(0,0)=0  (0,1)=1  (0,2)=2          (0,0)=N  (0,1)=N-1  (0,2)=N-2
(1,0)=1  (1,1)=2  (1,2)=3          (1,0)=N+1 (1,1)=N   (1,2)=N-1
(2,0)=2  (2,1)=3  (2,2)=4          (2,0)=N+2 (2,1)=N+1 (2,2)=N

Constant O(1) array lookups replace N-step directional raycasts! ⚡
```

---

## 2. Core Concepts & N-Queens Strategy Matrix

### 2.1 N-Queens Implementations Strategy Matrix
```
N-Queens Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Implementation        | Primary Target    | Pruning Structure | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Board Strings (51)**| Full Board Views  | Boolean Arrays    | **$O(N!)$ Factorial⚡**| **$O(N^2)$ Board ⚡**|
| **Solution Count (52)**| Integer Count     | Boolean Arrays    | **$O(N!)$ Factorial⚡**| **$O(N)$ Stack ⚡** |
| **Bitmask Solver (52)**| Max Speed Count   | Bitmask Operators | **$O(N!)$ Fast ⚡**| **$O(N)$ Stack ⚡** |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"N-Queens places 1 queen per row; Main diag = r+c; Anti diag = r-c+N; Bitmask uses bit = available & (-available)!"**

---

## 3. Characteristics & Bitmask N-Queens Mathematical Derivation

### 3.1 Mathematical Derivation of Bitmask N-Queens State Acceleration
* Let `cols`, `diag1`, and `diag2` be integers where bit $k$ is 1 if column/diagonal $k$ is under attack.
* When moving from row $r$ to row $r+1$:
  - Columns under attack remain unchanged: `cols`.
  - Main diagonals (`/`) shift left by 1 bit position: `(diag1 | bit) << 1`.
  - Anti-diagonals (`\`) shift right by 1 bit position: `(diag2 | bit) >> 1`.
* **Extracting Available Column Positions**:
  $$\text{available} = \sim(\text{cols} \mid \text{diag1} \mid \text{diag2}) \;\&\; \text{limit}$$
* **Iterating Bits Using Lowest Set Bit Trick**:
  - `bit = available & (-available)` extracts the rightmost 1-bit in $O(1)$ time.
  - `available -= bit` removes the processed bit.
* Eliminates all loop iterations over invalid columns, executing in pure bitwise instructions! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step N-Queens Board Placement

Tracing N-Queens for $N = 4$:

```
Row 0: Place Q at (0, 1) [Col 1]
- cols[1] = true, diag1[1] = true, diag2[0-1+4=3] = true.

Row 1: Candidate cols = 0, 1, 2, 3.
- Col 0: diag1[1+0=1] is true! PRUNED! ❌
- Col 1: cols[1] is true! PRUNED! ❌
- Col 2: Valid! Place Q at (1, 3) [Col 3].

Row 2: Candidate cols = 0, 1, 2, 3.
- Col 0: Valid! Place Q at (2, 0) [Col 0].

Row 3: Candidate cols = 0, 1, 2, 3.
- Col 0, 1, 2, 3 all under attack! PRUNED! ❌

Backtrack to Row 2 -> Try next valid placement!
Generates all 2 valid 4-Queens configurations! ✅ ⚡
```

---

## 5. Visual Diagram: 4-Queens Valid Board Configuration

```
Valid 4-Queens Placement 1:
. Q . .  (Row 0, Col 1)
. . . Q  (Row 1, Col 3)
Q . . .  (Row 2, Col 0)
. . Q .  (Row 3, Col 2)

No two queens share same row, column, main diagonal, or anti-diagonal! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing N-Queens All Board Solutions (LeetCode 51), N-Queens II Solution Count (LeetCode 52), and Bitmask Accelerated N-Queens Solver.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing N-Queens Backtracking:
 * Column/Diagonal Arrays, Board Reconstruction, and Bitmask Acceleration.
 */
public class NQueensMaster {

    // =========================================================================
    // 1. LEETCODE 51: N-QUEENS ALL BOARD CONFIGURATIONS (O(N!) Time)
    // =========================================================================
    /**
     * Finds all distinct N-Queens board configurations.
     *
     * @param n chessboard size N x N
     * @return list of board configurations
     */
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> results = new ArrayList<>();
        if (n <= 0) return results;

        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');

        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n]; // Main diagonal r + c
        boolean[] diag2 = new boolean[2 * n]; // Anti diagonal r - c + n

        solveNQueensDFS(board, 0, n, cols, diag1, diag2, results);
        return results;
    }

    private void solveNQueensDFS(char[][] board, int row, int n, boolean[] cols, boolean[] diag1, boolean[] diag2, List<List<String>> results) {
        if (row == n) {
            results.add(constructBoard(board)); // Capture solution! ⚡
            return;
        }

        for (int col = 0; col < n; col++) {
            int d1 = row + col;
            int d2 = row - col + n;

            // O(1) Threat Check Arrays
            if (cols[col] || diag1[d1] || diag2[d2]) continue; // Prune threat! ⚡

            // Choose
            board[row][col] = 'Q';
            cols[col] = true;
            diag1[d1] = true;
            diag2[d2] = true;

            // Explore
            solveNQueensDFS(board, row + 1, n, cols, diag1, diag2, results);

            // Unchoose (Backtrack!) ⚡
            board[row][col] = '.';
            cols[col] = false;
            diag1[d1] = false;
            diag2[d2] = false;
        }
    }

    private List<String> constructBoard(char[][] board) {
        List<String> res = new ArrayList<>();
        for (char[] row : board) res.add(new String(row));
        return res;
    }

    // =========================================================================
    // 2. LEETCODE 52: N-QUEENS II BITMASK ACCELERATOR (O(N!) Fast)
    // =========================================================================
    private int bitmaskSolutionCount = 0;

    /**
     * Counts total distinct N-Queens solutions using Bitmask Acceleration.
     */
    public int totalNQueensBitmask(int n) {
        if (n <= 0) return 0;
        bitmaskSolutionCount = 0;
        int limit = (1 << n) - 1; // Full N-bit mask sentinel ⚡

        bitmaskDFS(0, 0, 0, limit);
        return bitmaskSolutionCount;
    }

    private void bitmaskDFS(int cols, int diag1, int diag2, int limit) {
        if (cols == limit) {
            bitmaskSolutionCount++; // Solution found! ⚡
            return;
        }

        // Available column positions bitmask
        int available = (~(cols | diag1 | diag2)) & limit;

        while (available != 0) {
            // Extract lowest set bit in O(1) time
            int bit = available & (-available);
            available -= bit;

            // Explore next row with shifted diagonal threat masks! ⚡
            bitmaskDFS(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, limit);
        }
    }
}
```

> **Quick Syntax:**
```java
// Bitmask N-Queens Lowest Bit Extraction Line
int bit = available & (-available); available -= bit; bitmaskDFS(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, limit);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 51 - N-Queens**:
   - Board view reconstruction benchmark ($O(N!)$ time).

2. **LeetCode 52 - N-Queens II**:
   - Solution counting benchmark using bitmask acceleration.

3. **Constraint Satisfaction Problems (CSP)**:
   - Resource allocation and non-interfering frequency channel assignment.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class NQueensDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   N-QUEENS BACKTRACKING BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        NQueensMaster master = new NQueensMaster();

        // 1. N-Queens Board Views Test (LeetCode 51)
        int n = 4;
        List<List<String>> boards = master.solveNQueens(n);
        System.out.println("1. LeetCode 51 N-Queens Board Solutions for N = " + n + ":");
        System.out.println("   Total Board Configurations: " + boards.size() + " Solutions");
        for (int i = 0; i < boards.size(); i++) {
            System.out.println("   Solution " + (i + 1) + ":");
            boards.get(i).forEach(row -> System.out.println("     " + row));
        }
        System.out.println("-------------------------------------------------");

        // 2. Bitmask N-Queens Solution Count Test (LeetCode 52)
        int n8 = 8;
        int count8 = master.totalNQueensBitmask(n8);
        System.out.println("2. LeetCode 52 Bitmask N-Queens II Count for N = " + n8 + ":");
        System.out.println("   Total Solutions (Bitmask O(1) Bit operations): " + count8 + " Solutions (Optimal = 92)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| N-Queens Implementation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Board Views (LC 51)** | $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(N^2)}$ Board Space| Board string building |
| **Boolean Arrays (52)** | $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack Depth | `cols`, `diag1`, `diag2` |
| **Bitmask Solver (52)** | $\mathbf{O(N!)}$ Fast ⚡| $\mathbf{O(N)}$ Stack Depth | `bit = available & (-available)` |

---

## 10. Edge Cases & Boundary Handling

1. **N = 1**:
   - Returns 1 solution `[["Q"]]`.

2. **N = 2 or N = 3**:
   - Returns 0 solutions (impossible to place non-attacking queens).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Raycasting 8 Directions at Each Step to Check Queen Threat**:
  - Scanning the board in 8 directions using loops takes $O(N)$ time per cell, degrading N-Queens runtime to $O(N \cdot N!)$. **ALWAYS use $O(1)$ boolean arrays or bitmasks!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 3 N-Queens Constraint Array Formulas:
> * **Column Array**: `cols[col]`
> * **Main Diagonal (`/`)**: `diag1[row + col]`
> * **Anti-Diagonal (`\`)**: `diag2[row - col + N]` ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Boolean Array Pruning | Bitmask Acceleration |
| :--- | :--- | :--- |
| **Check Speed** | 3 Array Reads ($O(1)$) | **Bitwise Operator `&` ($O(1)$) ⚡** |
| **Memory Cost** | $O(N)$ Boolean Arrays | **Primitive Integers ⚡** |
| **Code Speedup** | Standard Baseline | **10x Faster Execution ⚡** |

---

## 14. How to Recognize This in Questions

* **"Place N non-attacking items on N x N grid"** $\rightarrow$ N-Queens Backtracking.
* **"Count total distinct non-attacking board arrangements"** $\rightarrow$ LeetCode 52 (Bitmask N-Queens).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does main diagonal check use `row + col` and anti-diagonal check use `row - col + N`?**  
  *A:* Because cells along the same `/` diagonal have constant $row + col$ sums, and cells along the same `\` diagonal have constant $row - col$ differences. Adding $N$ prevents negative array indexing.

* **Q: How does the bitwise operation `available & (-available)` work?**  
  *A:* In 2's complement arithmetic, `-available` inverts all bits and adds 1. Bitwise ANDing `available & (-available)` isolates the single rightmost 1-bit.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: N-QUEENS BACKTRACKING                                 |
+-----------------------------------------------------------------------+
| • Search Rule  : Place 1 queen per row (row 0..N-1)                   |
| • Threat Arrays: cols[col], diag1[row + col], diag2[row - col + N]    |
| • Bitmask Trick: bit = available & (-available) -> lowest 1-bit       |
| • Bitmask DFS  : bitmaskDFS(cols | bit, (d1|bit)<<1, (d2|bit)>>1, limit)|
| • Performance  : O(N!) Time | N=8 -> 92 Solutions | N=4 -> 2 Solutions ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 51 (`N-Queens`) in Java.
- [ ] I can write LeetCode 52 (`N-Queens II`) using Bitmask Acceleration.
- [ ] I can state the 3 diagonal and column array indexing formulas.
- [ ] I can explain how `available & (-available)` extracts the lowest 1-bit.
- [ ] I can state the solution counts for $N=4$ (2) and $N=8$ (92).
