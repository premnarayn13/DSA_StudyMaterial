# 14. Master Reference — Backtracking Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 27: Backtracking**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Backtracking Foundations, State Space Trees, Permutations (Distinct & Duplicates), Combinations & Loop Upper Bound Pruning, Subsets & Bitmask Power Sets, N-Queens & Bitmask Accelerators, Rat in a Maze 4-Directional Pathfinding, Sudoku Solver & 3x3 Sub-box Indexing, Knight's Tour & Warnsdorff's Minimum Degree Heuristic, Graph $K$-Coloring & Bipartite Checks, Hamiltonian Cycle & Dirac's Theorem, Pruning Techniques (Feasibility, Optimality Bounding, Symmetry Breaking, MRV), and the 6 Master Backtracking Archetypes.

> **Important:** Review this master reference 15 minutes before an interview to refresh the Choose-Explore-Unchoose Triad, Deep Copy Result Capture (`results.add(new ArrayList<>(path))`), Permutations loop at index 0 + `visited[]`, Permutations II duplicate guard `!visited[i-1]`, Combinations loop at `startIndex`, Combination Sum II duplicate guard `i > startIndex`, Combinations loop upper bound pruning (`i <= n - (k - len) + 1`), N-Queens diagonal formulas (`r+c` and `r-c+N`), Bitmask N-Queens lowest set bit (`bit = available & (-available)`), Sudoku 3x3 box formula (`(r/3)*3 + (c/3)`), Rat in a Maze visited cell reversion (`visited[r][c] = false`), Warnsdorff's minimum degree sort, Hamiltonian origin re-connection check (`graph[path[V-1]][path[0]] == 1`), and Optimality Bounding ($C \ge C^*$ cut)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **The Choose-Explore-Unchoose Triad**:
  - `path.add(choice);` $\to$ `backtrack(nextState);` $\to$ `path.remove(path.size() - 1);`
* **Deep Copy Result Capture Invariant**:
  - `results.add(new ArrayList<>(path));` (ALWAYS deep-copy mutable path list!).
* **Permutations II Duplicate Pruning Invariant (LC 47)**:
  - `if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) continue;` (Requires sorted array!).
* **Combination Sum II Duplicate Pruning Invariant (LC 40)**:
  - `if (i > startIndex && nums[i] == nums[i - 1]) continue;` (Requires sorted array!).
* **Combinations Loop Upper Bound Pruning Formula (LC 77)**:
  - `int upperLimit = n - (k - path.size()) + 1;` $\to$ `for (int i = startIndex; i <= upperLimit; i++)`
* **Subsets vs Combinations Solution Capture Rule**:
  - **Subsets**: Capture result at EVERY node (`results.add(...)` placed OUTSIDE candidate loop).
  - **Combinations**: Capture result ONLY when `path.size() == K`.
* **N-Queens Diagonal Constraint Indexing Formulas**:
  - Column: `cols[col]` (size $N$).
  - Main Diagonal (`/` direction): `diag1[row + col]` (size $2N$).
  - Anti-Diagonal (`\` direction): `diag2[row - col + N]` (size $2N$).
* **Bitmask N-Queens Lowest Bit Extraction Trick (LC 52)**:
  - `int available = (~(cols | diag1 | diag2)) & limit;`
  - `int bit = available & (-available); available -= bit;`
* **Sudoku 3x3 Sub-box Indexing Formula (LC 37)**:
  - `int boxIdx = (row / 3) * 3 + (col / 3);`
* **Sudoku Early Termination Return Rule**:
  - `if (solveDFS(...)) return true;` (Preserves solved board in-place!).
* **Rat in a Maze Visited Cell Reversion Invariant**:
  - `visited[r][c] = true; DFS(...); visited[r][c] = false;`
* **Warnsdorff's Minimum Degree Rule (Knight's Tour)**:
  - Move to candidate neighbor node $v$ with **MINIMUM ONWARD UNVISITED DEGREE** $d(v) = |V(v)|$.
* **Dirac's Theorem (Hamiltonian Cycle Guarantee)**:
  - If every vertex $v \in V$ has degree $\text{deg}(v) \ge \frac{V}{2}$ (for $V \ge 3$), $G$ is GUARANTEED Hamiltonian.
* **Optimality Bounding Cutoff Invariant**:
  - If `currentCost >= bestCost`, prune branch immediately (`return`).
* **Minimum Remaining Values (MRV / Most Constrained Variable)**:
  - Select decision variable with FEWEST remaining valid candidates first.

```
Master Backtracking Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Backtracking Archetype| Primary Loop Start| Tracking Mechanism| Solution Capture  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Permutations (46)** | **Index 0 ⚡**     | `boolean[] visited`| Leaf Nodes Only   | **$O(N \cdot N!)$ ⚡**|
| **Permutations II (47)**| **Index 0 ⚡**   | `!visited[i-1]`   | Leaf Nodes Only   | **$O(N \cdot N!)$ ⚡**|
| **Subsets I (78)**    | **`startIndex` ⚡**| Index Pointer     | **EVERY Node ⚡**  | **$O(N \cdot 2^N)$ ⚡**|
| **Subsets II (90)**   | **`startIndex` ⚡**| `i > startIndex`  | **EVERY Node ⚡**  | **$O(N \cdot 2^N)$ ⚡**|
| **Combinations (77)** | **`startIndex` ⚡**| Upper Limit Prune | Leaf Nodes ($K$)  | **$O(\binom{N}{K})$ ⚡**|
| **Comb Sum I (39)**   | Pass `i` (Re-use) | Index Pointer     | Target Sum        | $O(2^T)$          |
| **Comb Sum II (40)**  | Pass `i + 1`      | `i > startIndex`  | Target Sum        | $O(2^N)$          |
| **N-Queens (51)**     | Row-by-Row        | `cols`/`d1`/`d2`  | Row == N          | **$O(N!)$ Factorial⚡**|
| **Sudoku Solver (37)**| Cell-by-Cell      | `(r/3)*3 + (c/3)` | Row == 9 (`true`) | $O(9^m)$          |
| **Rat in a Maze**     | D, L, R, U        | `visited[r][c]` rev| Cell (N-1, N-1)   | $O(4^{N^2})$      |
| **Knight's Tour**     | 8 L-Moves         | Warnsdorff Degree | Step == N * N      | **$O(N^2)$ Linear ⚡**|
| **Graph K-Coloring**  | Vertex $0 \dots V-1$| `isSafe(u, c)`    | Vertex == V       | $O(K^V)$          |
| **Hamiltonian Cycle** | Path Array        | Origin Re-connect | Pos == V (`graph`)| $O(N!)$          |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Backtracking Topic | Purpose | Primary Decision Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Permutations (46)** | Ordered arrangements | Loop index 0 + `visited[]` | $\mathbf{O(N \cdot N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack Depth| $N!$ leaf solutions |
| **Permutations II (47)**| Unique permutations | Sort + `!visited[i-1]` guard | $\mathbf{O(N \cdot N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack Depth| Eliminate twin duplicates |
| **Subsets I (78)** | Power set generation | Capture result at EVERY node | $\mathbf{O(N \cdot 2^N)}$ Exponential⚡| $\mathbf{O(N)}$ Stack Depth| $2^N$ total nodes |
| **Subsets II (90)** | Unique power set | Sort + `i > startIndex` guard | $\mathbf{O(N \cdot 2^N)}$ Exponential⚡| $\mathbf{O(N)}$ Stack Depth| Eliminate duplicate subsets |
| **Combinations (77)** | Unordered size K | Pruned upper limit formula | $\mathbf{O(\binom{N}{K})}$ Combinatorial⚡| $\mathbf{O(K)}$ Stack Depth| `i <= n - (k - len) + 1` |
| **Comb Sum I (39)** | Re-usable item sum | Pass `startIndex = i` | $O(2^T)$ Exponential | $O(T)$ Stack Depth | Infinite item re-use |
| **Comb Sum II (40)** | Single-use item sum | Pass `startIndex = i + 1` + Prune| $O(2^N)$ Exponential | $O(N)$ Stack Depth | Single item use + Sort |
| **N-Queens (51)** | Board placements | `cols`, `diag1`, `diag2` arrays | $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(N^2)}$ Board Space| Row-by-row placement |
| **N-Queens II (52)** | Solutions count | `bit = available & (-available)`| $\mathbf{O(N!)}$ Fast Bitwise⚡| $\mathbf{O(N)}$ Stack Depth| Bitwise 10x speedup |
| **Sudoku Solver (37)** | Fill 9x9 board | `(r/3)*3 + (c/3)` box index | $O(9^m)$ Pruned | $O(81)$ Stack Depth | Early return `true` |
| **Rat in a Maze** | 2D matrix paths | `visited[r][c]` reversion | $O(4^{N^2})$ Worst | $O(N^2)$ Matrix Space| Lexicographical D,L,R,U |
| **Knight's Tour** | Visit all N^2 cells | Warnsdorff min degree sort | $\mathbf{O(N^2)}$ Strict Linear⚡| $\mathbf{O(N^2)}$ Board Space| Minimum onward degree |
| **Bipartite Graph (785)**| 2-Colorability check | BFS/DFS alternating color | $\mathbf{O(V + E)}$ Linear ⚡| $\mathbf{O(V)}$ Queue Space| Odd cycle detection |
| **Graph K-Coloring** | Color V vertices | `isSafe(u, c)` neighbor check | $O(K^V)$ Exponential | $O(V)$ Stack Depth | Chromatic number $\chi(G)$ |
| **Hamiltonian Cycle** | Visit V vertices once | Origin re-connection check | $O(N!)$ Factorial | $O(V)$ Stack Depth | Dirac's Theorem $\text{deg} \ge V/2$ |
| **TSP Optimality Cut**| Min cost tour | Prune `currentCost >= bestCost` | $O(N!)$ Pruned | $O(V)$ Stack Depth | Optimality bounding |

---

## 4. Architectural System & Production Use Cases
```
+-----------------------------------------------------------------------------------+
| Production System Backtracking Architectures                                      |
+-----------------------------------------------------------------------------------+
| Sudoku, Crossword & Kakuro Board Game Engines  : 9x9 CSP Backtracking Solvers     |
| Compiler Register Allocation & Interference    : Graph K-Coloring Backtracking    |
| Printed Circuit Board (PCB) Drill Navigation   : Knight's Tour / TSP Backtracking   |
| Automated Timetable & Exam Scheduling          : Constraint Propagation (MRV)     |
| Robotics Pathfinding & Grid Navigation         : Rat in a Maze 4-Directional DFS   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Deep Copy Result Capture Invariant
> results.add(new ArrayList<>(path));
> 
> // 2. Permutations Distinct (Loop at 0 + visited[])
> for (int i = 0; i < nums.length; i++) { if (visited[i]) continue; visited[i] = true; path.add(nums[i]); permuteDFS(...); path.remove(path.size() - 1); visited[i] = false; }
> 
> // 3. Permutations II Duplicate Pruning (LC 47)
> if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) continue;
> 
> // 4. Combinations & Subsets II Duplicate Pruning (LC 40 / LC 90)
> if (i > startIndex && nums[i] == nums[i - 1]) continue;
> 
> // 5. Combinations Loop Upper Bound Pruning (LC 77)
> int upperLimit = n - (k - path.size()) + 1; for (int i = startIndex; i <= upperLimit; i++) ...
> 
> // 6. Combination Sum Item Re-use Rule
> combinationSumDFS(..., i, ...);    // Infinite re-use (LC 39)
> combinationSum2DFS(..., i + 1, ..); // Single use (LC 40)
> 
> // 7. N-Queens O(1) Threat Checks
> int d1 = row + col, d2 = row - col + n; if (cols[col] || diag1[d1] || diag2[d2]) continue;
> 
> // 8. Bitmask N-Queens Lowest Bit Extraction
> int bit = available & (-available); available -= bit; bitmaskDFS(cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, limit);
> 
> // 9. Sudoku 3x3 Box Formula & Early Termination
> int b = (r / 3) * 3 + (c / 3); if (solveSudokuDFS(...)) return true;
> 
> // 10. Rat in a Maze Visited Cell Reversion
> visited[nextR][nextC] = true; ratInAMazeDFS(...); visited[nextR][nextC] = false;
> 
> // 11. Warnsdorff's Minimum Degree Sorting
> Collections.sort(options); // Sort candidates by onward degree ASC
> 
> // 12. Optimality Bounding Cutoff
> if (currentCost >= bestCost) return;
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Forgetting to Make a Deep Copy When Adding Path to Results**: Writing `results.add(path)` stores a reference to mutable list `path`, corrupting all results when backtracking mutates `path`. **ALWAYS write `results.add(new ArrayList<>(path))`**!
* **Pitfall 2: Confusing Permutations II Duplicate Guard with Combinations II Duplicate Guard**:
  - Permutations II uses `if (i > 0 && nums[i] == nums[i-1] && !visited[i-1]) continue;` (Loop starts at 0).
  - Combinations II / Subsets II uses `if (i > startIndex && nums[i] == nums[i-1]) continue;` (Loop starts at `startIndex`). **Do not interchange them**!
* **Pitfall 3: Forgetting Early Termination Return True in Sudoku**: Writing `solveSudokuDFS(...)` without returning `true` on solution causes backtracking to undo the solved board. **ALWAYS return `true` immediately when $r == 9$**!
* **Pitfall 4: Forgetting Visited Cell Reversion in Grid Paths**: Leaving `visited[r][c] = true` permanently destroys remaining path candidates. **ALWAYS reset `visited[r][c] = false` during backtracking**!
* **Pitfall 5: Forgetting Origin Re-connection Check in Hamiltonian Cycle**: Checking that $V$ vertices are visited without verifying `graph[path[V-1]][path[0]] == 1` produces a Hamiltonian Path, NOT a Hamiltonian Cycle. **ALWAYS check origin connection**!
* **Pitfall 6: Running Naive 8-Way Knight's Tour Without Warnsdorff's Heuristic**: Plain DFS freezes for $8 \times 8$ board ($8^{64}$ nodes). **ALWAYS sort candidate knight moves by minimum onward degree**!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 27 (BACKTRACKING)                |
+-----------------------------------------------------------------------+
| 1. Choose-Explore-Unchoose: path.add(c) -> recurse -> path.remove(end)|
| 2. Deep Copy Invariant    : results.add(new ArrayList<>(path))        |
| 3. Permutations (LC 46)   : Loop i = 0..N-1 + boolean[] visited       |
| 4. Permutations II (LC 47): Sort + skip if nums[i]==prev && !visited  |
| 5. Subsets I (LC 78)      : Capture results.add(path) at EVERY node   |
| 6. Subsets II (LC 90)     : Sort + skip if i > startIndex && nums[i]==prev|
| 7. Combinations (LC 77)   : Loop i = startIndex..n - (k - len) + 1    |
| 8. Comb Sum I (LC 39)     : Infinite re-use -> Pass startIndex = i    |
| 9. Comb Sum II (LC 40)    : Single use -> Pass i + 1 + Skip if i > start|
| 10. N-Queens (LC 51)      : cols[col], diag1[r+c], diag2[r-c+n]       |
| 11. Sudoku Solver (LC 37) : boxIdx = (r/3)*3 + (c/3) + return true    |
| 12. Rat in a Maze         : 4 Directions D,L,R,U + visited[r][c]=false|
| 13. Knight's Tour         : Sort by Warnsdorff MINIMUM ONWARD DEGREE ⚡|
| 14. Hamiltonian Cycle     : Check origin edge graph[path[V-1]][0] == 1|
| 15. Optimality Cut        : If currentCost >= bestCost -> Prune! ⚡     |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can state the 3 steps of the Choose-Explore-Unchoose triad.
- [ ] I can explain why candidate path solutions MUST be deep-copied before adding to results.
- [ ] I can write Permutations (LeetCode 46) and Permutations II (LeetCode 47) in Java.
- [ ] I can write Subsets (LeetCode 78) and Subsets II (LeetCode 90) in Java.
- [ ] I can write Combinations (LeetCode 77) with loop upper bound pruning.
- [ ] I can write Combination Sum I (LeetCode 39) and Combination Sum II (LeetCode 40) in Java.
- [ ] I can state the difference between `startIndex = i` and `startIndex = i + 1`.
- [ ] I can write N-Queens (LeetCode 51) and N-Queens II (LeetCode 52 Bitmask) in Java.
- [ ] I can state the 3 N-Queens threat array formulas (`cols`, `r+c`, `r-c+n`).
- [ ] I can write Sudoku Solver (LeetCode 37) in Java and explain early return `true`.
- [ ] I can state the 3x3 Sudoku sub-box index formula `(r / 3) * 3 + (c / 3)`.
- [ ] I can write Rat in a Maze All Paths in Java with visited cell reversion.
- [ ] I can write Warnsdorff's Minimum Degree Knight's Tour Solver in Java.
- [ ] I can write Hamiltonian Cycle Backtracking with origin re-connection check.
- [ ] I can state Dirac's Theorem degree condition ($\text{deg}(v) \ge \frac{V}{2}$).
- [ ] I can write TSP Backtracking with Optimality Bounding ($C \ge C^*$) pruning.
- [ ] I can state the 5 major pruning strategies.
- [ ] I can match any backtracking interview question to one of the 6 Master Archetypes in under 10 seconds.
