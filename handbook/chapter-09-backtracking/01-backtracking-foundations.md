# 01. Backtracking Foundations: Choose, Explore, Unchoose Invariants & State Pruning

## 1. Introduction
**Backtracking** is a systematic algorithmic technique for solving combinatorial search, decision, and optimization problems by building candidate solutions incrementally along a **State Space Tree** and discarding ("pruning") candidates as soon as it is determined that they cannot lead to a valid global solution. Unlike brute-force exhaustive search which evaluates all $O(N!)$ or $O(2^N)$ possibilities to completion, Backtracking enforces the **Choose-Explore-Unchoose Invariant**: at each decision step, the algorithm (1) **Chooses** a valid candidate choice, (2) **Explores** deeper down the recursive call tree, and (3) **Unchooses** (undoes the local state mutation) upon returning to backtrack and explore alternative candidate branches. Backtracking powers foundational algorithms such as **N-Queens**, **Sudoku Solver**, **Permutations**, **Subsets**, and **Graph Coloring**.

> **Important:** The 3 Core Pillars of Backtracking:
> 1. **Choose-Explore-Unchoose Triad**:
>    - **Choose**: Mutate state (e.g. `path.add(choice)` or `visited[u] = true`).
>    - **Explore**: Make recursive call (`backtrack(nextState)`).
>    - **Unchoose**: Revert state mutation (`path.remove(path.size() - 1)` or `visited[u] = false`).
> 2. **State Space Tree Pruning**:
>    - Evaluating bounding functions (`isValid(choice)`) BEFORE making a recursive call eliminates entire dead-end subtrees, drastically reducing runtime from $O(N!)$ down to practical bounds.
> 3. **Base Case Solution Capture**:
>    - When the recursive depth reaches target solution criteria (e.g. `path.size() == N` or `col == N`), capture a deep copy of candidate path (`result.add(new ArrayList<>(path))`). ⚡

```
Choose-Explore-Unchoose Trajectory Topology:

                      [ Decision Node (State S) ]
                                   │
                      1. Choose Candidate Choice C
                                   │
                                   ▼
                      [ Child Node (State S + C) ]
                                   │
                      2. Explore Recursively (DFS)
                                   │
                                   ▼
                      [ Backtrack Return from Child ]
                                   │
                      3. Unchoose Choice C (Undo State Mutation!) ⚡
```

---

## 2. Core Concepts & Search Paradigm Strategy Matrix

### 2.1 Combinatorial Search Strategy Matrix
```
Combinatorial Search Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Paradigm              | Search Space      | Pruning Mechanism | State Reversion   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Brute Force Search**| Full Exhaustive   | None              | Not Needed        | Worst $O(N!)$     |
| **Backtracking**      | **State Tree ⚡** | **Bounding Check⚡**| **Unchoose Step ⚡**| **Pruned $O(B^N)$ ⚡**|
| **Branch & Bound**    | Best-First Queue  | Cost Lower Bound  | Priority Queue    | Pruned $O(B^N)$   |
| **Dynamic Programming**| Subproblem DAG    | No Backtracking   | Memoization Table | Polynomial $O(N^k)$|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Backtracking = Choose (Mutate) -> Explore (Recurse) -> Unchoose (Revert)! Prunes invalid branches early!"**

---

## 3. Characteristics & State Space Tree Mathematical Bounds

### 3.1 Mathematical Complexity of Backtracking
* Let $B$ be the maximum branching factor (number of valid choices per decision step) and $H$ be the maximum depth of the state space tree.
* **Unpruned State Space Size**:
  $$T(N) = \sum_{k=0}^H B^k = \frac{B^{H+1} - 1}{B - 1} \implies O(B^H)$$
* For Permutations of $N$ items: $T(N) = N \cdot (N-1) \cdot (N-2) \dots 1 = O(N!)$.
* For Subsets of $N$ items: $T(N) = 2^N$.
* **Pruning Impact**:
  - Effective pruning constraints reduce the branching factor from $B$ to an effective factor $B_{\text{eff}} \ll B$, reducing total evaluated nodes by orders of magnitude (e.g., N-Queens for $N=8$ reduces $8^8 = 16,777,216$ nodes down to only $2,057$ evaluated nodes!). ⚡

---

## 4. Internal Working Mechanics: The Universal Backtracking Blueprint

Every backtracking algorithm adheres to the **Universal Backtracking Template**:

```java
void backtrack(State state, List<Choice> choices, List<Solution> results) {
    // Step 1: Base Case Check (Solution Criteria Satisfied)
    if (isSolution(state)) {
        results.add(copySolution(state)); // Deep copy!
        return;
    }

    // Step 2: Iterate over Candidate Choices
    for (Choice choice : choices) {
        // Step 3: Pruning / Bounding Check
        if (!isValid(state, choice)) continue; // Prune invalid branch! ⚡

        // Step 4: Choose (Apply State Mutation)
        makeChoice(state, choice);

        // Step 5: Explore (Recursive Call)
        backtrack(state, choices, results);

        // Step 6: Unchoose (Revert State Mutation)
        undoChoice(state, choice); // Backtrack step! ⚡
    }
}
```

---

## 5. Visual Diagram: State Space Tree Pruning

```
State Space Tree Pruning Topology (N-Queens Placement):

                             [ Queen 0 at (0,0) ]
                            /         |         \
                           /          |          \
                 [ Q1 at (1,0) ] [ Q1 at (1,1) ] [ Q1 at (1,2) ]
                        │             │                │
                (Invalid Column) (Invalid Diag)    (Valid Placement!) ✅
                        │             │                │
                    PRUNED ❌     PRUNED ❌       Explore Deeper... ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Backtracking Foundations across Subsets (LeetCode 78) and N-Queens (LeetCode 51).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Backtracking Foundations:
 * Choose-Explore-Unchoose Invariants, State Pruning, Subsets, and N-Queens.
 */
public class BacktrackingFoundationsMaster {

    // =========================================================================
    // 1. LEETCODE 78: SUBSETS / POWER SET (O(N * 2^N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates all unique subsets (power set) of an integer array.
     *
     * @param nums array of unique integers
     * @return list of all subsets
     */
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null) return results;

        List<Integer> currentPath = new ArrayList<>();
        subsetsDFS(nums, 0, currentPath, results);
        return results;
    }

    private void subsetsDFS(int[] nums, int startIndex, List<Integer> path, List<List<Integer>> results) {
        // Step 1: Capture current subset (Every node in state tree is a valid subset!)
        results.add(new ArrayList<>(path)); // Deep copy ⚡

        // Step 2: Iterate over candidate choices
        for (int i = startIndex; i < nums.length; i++) {
            // Choose
            path.add(nums[i]);

            // Explore
            subsetsDFS(nums, i + 1, path, results);

            // Unchoose (Backtrack step!) ⚡
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 2. LEETCODE 51: N-QUEENS SOLVER (O(N!) Time, O(N) Space)
    // =========================================================================
    /**
     * Solves N-Queens placement problem returning list of valid board configurations.
     */
    public List<List<String>> solveNQueens(int n) {
        List<List<String>> results = new ArrayList<>();
        if (n <= 0) return results;

        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');

        boolean[] cols = new boolean[n];
        boolean[] diag1 = new boolean[2 * n]; // r + c
        boolean[] diag2 = new boolean[2 * n]; // r - c + n

        nQueensDFS(board, 0, n, cols, diag1, diag2, results);
        return results;
    }

    private void nQueensDFS(char[][] board, int row, int n, boolean[] cols, boolean[] diag1, boolean[] diag2, List<List<String>> results) {
        if (row == n) {
            results.add(constructBoard(board));
            return;
        }

        for (int col = 0; col < n; col++) {
            int d1 = row + col;
            int d2 = row - col + n;

            // Pruning / Bounding Check: Is placement valid?
            if (cols[col] || diag1[d1] || diag2[d2]) continue; // Prune branch! ⚡

            // Choose
            board[row][col] = 'Q';
            cols[col] = true;
            diag1[d1] = true;
            diag2[d2] = true;

            // Explore
            nQueensDFS(board, row + 1, n, cols, diag1, diag2, results);

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
}
```

> **Quick Syntax:**
> ```java
> // Backtracking Choose-Explore-Unchoose Pattern Lines
> path.add(nums[i]); subsetsDFS(nums, i + 1, path, results); path.remove(path.size() - 1);
> ```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 78 - Subsets**:
   - Power set state space tree traversal benchmark ($O(N \cdot 2^N)$ time).

2. **LeetCode 51 - N-Queens**:
   - Diagonal and column pruning benchmark ($O(N!)$ time).

3. **Sudoku Solver & Game Tree AI**:
   - Constraint propagation and backtracking board solver.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class BacktrackingFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BACKTRACKING FOUNDATIONS BENCHMARK DEMO       ");
        System.out.println("=================================================\n");

        BacktrackingFoundationsMaster master = new BacktrackingFoundationsMaster();

        // 1. Subsets Test (LeetCode 78)
        int[] nums = {1, 2, 3};
        List<List<Integer>> subsets = master.subsets(nums);

        System.out.println("1. Subsets for Array [1, 2, 3]:");
        System.out.println("   Total Subsets Generated: " + subsets.size() + " Subsets (2^3 = 8)");
        System.out.println("   Subsets = " + subsets);
        System.out.println("-------------------------------------------------");

        // 2. N-Queens Test (LeetCode 51)
        int n = 4;
        List<List<String>> queenBoards = master.solveNQueens(n);
        System.out.println("2. N-Queens Solution Configurations for N = " + n + ":");
        System.out.println("   Total Valid Board Placements: " + queenBoards.size() + " Configurations");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Backtracking Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Subsets (LeetCode 78)** | $\mathbf{O(N \cdot 2^N)}$ ⚡| $\mathbf{O(N)}$ Stack ⚡| $2^N$ total subsets |
| **N-Queens (LeetCode 51)**| $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(N)}$ Board Space| Column & diagonal pruning |
| **Sudoku Solver**         | $O(9^{9 \times 9})$ | $O(81)$ Grid Space | 3x3 box & row pruning |

---

## 10. Edge Cases & Boundary Handling

1. **Empty Array Input (`nums = []`)**:
   - `subsets` returns `[[]]` (single empty subset `[]`).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Make a Deep Copy When Storing Results**:
  - Writing `results.add(path)` stores a reference to the mutable list `path`. When backtracking mutates `path`, all stored results get corrupted to empty lists! **ALWAYS write `results.add(new ArrayList<>(path))`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Backtracking Deep Copy Invariant:
> Whenever adding a candidate solution `path` to the final results list, **ALWAYS capture a deep copy**: `results.add(new ArrayList<>(path))`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Brute Force Search | Backtracking Search | Dynamic Programming |
| :--- | :--- | :--- | :--- |
| **Pruning** | None | **Early Branch Pruning ⚡**| Overlapping Subproblems |
| **Memory** | $O(N!)$ Arrays | **$O(N)$ Recursion Stack ⚡**| $O(N)$ / $O(N^2)$ Table |
| **State Mutation** | Immutable copies | **In-Place Mutate / Revert ⚡**| No State Mutation |

---

## 14. How to Recognize This in Questions

* **"Generate all valid combinations / permutations / subsets of array"** $\rightarrow$ Backtracking.
* **"Find all valid placements of queens or digits satisfying constraints"** $\rightarrow$ N-Queens / Sudoku Backtracking.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the Choose-Explore-Unchoose pattern?**  
  *A:* The 3-step backtracking cycle where an algorithm mutates local state to make a choice, recursively explores child states, and reverts local state upon return to backtrack.

* **Q: Why must candidate solutions be deep-copied before adding to results?**  
  *A:* Because `path` is a single mutable list reference. Storing `path` directly causes subsequent backtracking `remove` calls to mutate previously stored results.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BACKTRACKING FOUNDATIONS                              |
+-----------------------------------------------------------------------+
| • 3 Invariants: Choose (Mutate) -> Explore (DFS) -> Unchoose (Revert) |
| • Deep Copy   : MUST write results.add(new ArrayList<>(path))!        |
| • Pruning     : Check isValid(state, choice) BEFORE recursive call    |
| • Subsets 78  : O(N * 2^N) Time | N-Queens 51 : O(N!) Time            |
| • Performance : Prunes exponential search space drastically! ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the Choose-Explore-Unchoose backtracking pattern.
- [ ] I can write Subsets (LeetCode 78) in Java.
- [ ] I can write N-Queens (LeetCode 51) with column and diagonal pruning.
- [ ] I can explain why candidate solutions MUST be deep-copied.
- [ ] I can state the difference between Backtracking and Dynamic Programming.
