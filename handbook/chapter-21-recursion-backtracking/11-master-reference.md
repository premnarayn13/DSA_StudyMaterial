# 11. Master Reference — Recursion & Backtracking Algorithms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 21: Recursion & Backtracking**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for call stack mechanics, tail recursion accumulator patterns, power sets ($2^N$), permutations ($N!$), combinations ($C(N, K)$), N-Queens ($O(1)$ diagonal checks), Sudoku Solver ($3 \times 3$ box math), Word Search (in-place masking), Palindrome Partitioning (2D DP acceleration), and Expression Evaluation ($*$-precedence undo).

> **Important:** Review this master reference 15 minutes before an interview to refresh the 3 Pillars of Recursion (Base Case, Reduction, Combination), Unwinding vs Descent execution phases, Accumulator Pattern (`factTail(n - 1, n * acc)`), Subsets II Pruning (`i > start && nums[i] == nums[i-1]`), Permutations II Pruning (`!visited[i-1]`), N-Queens Main Diagonal (`r - c + N - 1`), Sudoku $3 \times 3$ Box Math (`3 * (r / 3) + i / 3`), Word Search In-Place Masking (`board[r][c] = '#'`), Palindrome DP Table (`dp[i][j]`), and Expression Multiplication Undo `(eval - prev) + (prev * val)`!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **The 3 Pillars of Recursive Design**:
  - Base Case Guard + Recursive Subproblem Reduction + Result Combination Step.
* **Accumulator Pattern Equation**:
  - `factTail(n, acc) = factTail(n - 1, n * acc)` (Base case $n \le 1$ returns `acc`).
* **Subsets II Duplicate Pruning Invariant**:
  - `Arrays.sort(nums); if (i > start && nums[i] == nums[i - 1]) continue;`
* **Permutations II Duplicate Pruning Invariant**:
  - `Arrays.sort(nums); if (visited[i] || (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1])) continue;`
* **N-Queens Diagonal ID Invariants**:
  - Main Diagonal (Top-Left to Bottom-Right): `diagIdx = row - col + (N - 1)`.
  - Anti-Diagonal (Top-Right to Bottom-Left): `antiDiagIdx = row + col`.
* **Sudoku $3 \times 3$ Sub-Box Indexing Equation**:
  - `boxRow = 3 * (row / 3) + i / 3; boxCol = 3 * (col / 3) + i % 3;` (for $i \in [0 \dots 8]$).
* **Word Search In-Place Cell Masking**:
  - `char temp = board[r][c]; board[r][c] = '#'; dfs(); board[r][c] = temp;`
* **Palindrome Partitioning 2D DP Table Equation**:
  - `dp[i][j] = (s.charAt(i) == s.charAt(j)) && (j - i <= 2 || dp[i + 1][j - 1]);`
* **Expression Add Operators Multiplication Undo Formula**:
  - `newEval = (eval - prevOperand) + (prevOperand * val); newPrev = prevOperand * val;`

```
Recursion & Backtracking Master Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Category      | Search Paradigm   | Key Data Structure| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Subsets / Power Set**| Include / Exclude | `i = start` Loop  | **$O(2^N \cdot N)$ ⚡**|
| **Combinations (77)** | Combination Tree  | `i = start` Loop  | **$O(C(N, K) \cdot K)$ ⚡**|
| **Permutations (46)** | Permutation Tree  | `boolean[] visited`| **$O(N! \cdot N)$ ⚡**|
| **N-Queens (51)**     | Constraint Check  | 3 Boolean Arrays  | **$O(N!)$ ⚡**     |
| **Sudoku Solver (37)**| Grid Constraint   | $3 \times 3$ Box Math| **$O(1)$ Constant ⚡**|
| **Word Search (79)**  | Grid Backtrack    | In-Place Masking  | **$O(M \cdot N \cdot 3^L)$ ⚡**|
| **Add Operators (282)**| Precedence Math   | `(eval, prev)`    | **$O(4^N)$ ⚡**    |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Pattern / Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Recursion**   | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Memory | 1 self-call per frame |
| **Tail Recursion (TCO)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Accumulator parameter |
| **Subsets I (78)**     | **$O(2^N \cdot N)$ ⚡**| **$O(2^N \cdot N)$ ⚡**| **$O(2^N \cdot N)$ ⚡**| $O(N)$ Call Stack | `i = start` index loop |
| **Subsets II (90)**    | **$O(2^N \cdot N)$ ⚡**| **$O(2^N \cdot N)$ ⚡**| **$O(2^N \cdot N)$ ⚡**| $O(N)$ Call Stack | `i > start && nums[i]==nums[i-1]` |
| **Combinations (77)**  | **$O(C(N,K)\cdot K)$**| **$O(C(N,K)\cdot K)$**| **$O(C(N,K)\cdot K)$**| $O(K)$ Call Stack | `i = start` index loop |
| **Permutations I (46)**| **$O(N! \cdot N)$ ⚡** | **$O(N! \cdot N)$ ⚡** | **$O(N! \cdot N)$ ⚡** | $O(N)$ Visited Stack| `boolean[] visited` array |
| **Permutations II (47)**| **$O(N! \cdot N)$ ⚡** | **$O(N! \cdot N)$ ⚡** | **$O(N! \cdot N)$ ⚡** | $O(N)$ Visited Stack| `!visited[i-1]` check |
| **N-Queens I (51)**    | **$O(N!)$ Factorial**| **$O(N!)$ Factorial**| **$O(N!)$ Factorial**| $O(N^2)$ Board Stack | $O(1)$ diagonal boolean arrays |
| **Sudoku Solver (37)** | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ Board Stack | $3 \times 3$ sub-box math |
| **Word Search I (79)** | **$O(M \cdot N \cdot 3^L)$**| **$O(M \cdot N \cdot 3^L)$**| **$O(M \cdot N \cdot 3^L)$**| $O(L)$ Stack Memory | In-place masking `board[r][c]='#'` |
| **Word Search II (212)**| **$O(M \cdot N \cdot 3^L)$**| **$O(M \cdot N \cdot 3^L)$**| **$O(M \cdot N \cdot 3^L)$**| $O(K \cdot L)$ Trie | Trie prefix pruning |
| **Palindrome Part (131)**| **$O(N \cdot 2^N)$ ⚡** | **$O(N \cdot 2^N)$ ⚡** | **$O(N \cdot 2^N)$ ⚡** | $O(N^2)$ DP Matrix | Precomputed $O(1)$ DP table |
| **Add Operators (282)**| **$O(4^N)$ Exp ⚡** | **$O(4^N)$ Exp ⚡** | **$O(4^N)$ Exp ⚡** | $O(N)$ Call Stack | `(eval - prev) + (prev * val)` |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Call Stack Memory Breakdown for Recursion & Backtracking                          |
+-----------------------------------------------------------------------------------+
| Stack Frame Memory Overhead                    : ~48 to 128 Bytes per Frame       |
| Default JVM Thread Stack Limit                 : ~10,000 Frames max depth           |
| Backtracking Stack Memory Optimization          : In-Place Mutation + Unwinding Pop|
| Primary Rule                                   : Deep-copy List only at LEAF nodes!|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Subsets II Duplicate Pruning Line
if (i > start && nums[i] == nums[i - 1]) continue;

// 2. Permutations II Horizontal Pruning Line
if (visited[i] || (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1])) continue;

// 3. N-Queens O(1) Collision Check Line
int diagIdx = row - col + (n - 1), antiDiagIdx = row + col;
if (cols[col] || diagonals[diagIdx] || antiDiagonals[antiDiagIdx]) continue;

// 4. Sudoku 3x3 Sub-Box Constraint Line
int boxRow = 3 * (row / 3) + i / 3, boxCol = 3 * (col / 3) + i % 3;
if (board[boxRow][boxCol] == ch) return false;

// 5. Word Search In-Place Cell Masking & Restore Line
char temp = board[r][c]; board[r][c] = '#';
boolean found = dfs(r+1, c) || dfs(r-1, c) || dfs(r, c+1) || dfs(r, c-1);
board[r][c] = temp; // Restored!

// 6. Palindrome 2D DP Table Precomputation Line
dp[i][j] = (s.charAt(i) == s.charAt(j)) && (j - i <= 2 || dp[i + 1][j - 1]);

// 7. Expression Add Operators Multiplication Undo Line
long newEval = (eval - prevOperand) + (prevOperand * val);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using `i > 0` Instead of `i > start` for Subsets II Pruning**: Writing `i > 0` prunes duplicates globally across different recursion depths, breaking valid combinations like `[2, 2]`. Always use `i > start`.
* **Pitfall 2: Adding Mutable `current` List Directly to Result**: Writing `result.add(current)` stores references to a single mutable list that gets cleared when unwinding. Always store deep copies `result.add(new ArrayList<>(current))`.
* **Pitfall 3: Assuming Java HotSpot JVM Performs Tail Call Optimization (TCO)**: Writing tail-recursive methods in Java still incurs $O(N)$ stack memory. Manually convert tail recursion to `while` loops in Java!
* **Pitfall 4: Using $O(N)$ Scan Loops in N-Queens `isSafe()` Method**: Scanning diagonals with $O(N)$ loops degrades speed by $N\times$. Always use $O(1)$ boolean arrays for `diagonals[r - c + N - 1]`.
* **Pitfall 5: Forgetting `!visited[i - 1]` Check in Permutations II**: Checking `visited[i - 1]` instead of `!visited[i - 1]` prunes vertical depth paths instead of horizontal breadth choices.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 21 (RECURSION & BACKTRACKING)   |
+-----------------------------------------------------------------------+
| 1. Subsets (78/90)    : `i = start` loop; Prune if `i > start && nums[i] == nums[i-1]`|
| 2. Permutations (46/47): `i = 0` loop + `visited[]`; Prune if `!visited[i-1]`|
| 3. N-Queens (51/52)   : Recurse row-by-row; Diag `r - c + N - 1`, Anti `r + c`|
| 4. Sudoku Solver (37) : Cell-by-cell; Sub-box `3 * (r / 3) + i / 3`   |
| 5. Word Search (79)   : Mask cell `board[r][c] = '#'`; Restore on return|
| 6. Palindrome (131)   : Precompute `dp[i][j]` table for O(1) checks   |
| 7. Add Operators (282): Undo multiplication `(eval - prev) + (prev * val)`|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write LeetCode 78 (`Subsets`) and LeetCode 90 (`Subsets II`) in Java.
- [ ] I can write LeetCode 39 (`Combination Sum`) and LeetCode 40 (`Combination Sum II`).
- [ ] I can write LeetCode 46 (`Permutations I`) and LeetCode 47 (`Permutations II`).
- [ ] I can write LeetCode 51 (`N-Queens`) using $O(1)$ diagonal boolean tracking.
- [ ] I can write LeetCode 37 (`Sudoku Solver`) using $3 \times 3$ sub-box math.
- [ ] I can write LeetCode 79 (`Word Search I`) using in-place masking.
- [ ] I can write LeetCode 212 (`Word Search II`) using Trie prefix pruning.
- [ ] I can write LeetCode 131 (`Palindrome Partitioning I`) with 2D DP acceleration.
- [ ] I can write Rat in a Maze using direction vectors `{'D','L','R','U'}`.
- [ ] I can write LeetCode 282 (`Expression Add Operators`) with multiplication undo.
