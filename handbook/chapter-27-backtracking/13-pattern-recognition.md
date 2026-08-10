# 13. Pattern Recognition & Backtracking Triggers: 6 Master Archetypes

## 1. Introduction
High-speed problem solving in technical coding interviews requires instant **Backtracking Pattern Recognition**. Rather than attempting to reinvent candidate loops, visited structures, and pruning guards under pressure, experienced engineers map problem descriptions directly to one of **6 Universal Backtracking Master Archetypes**: **Permutations Archetype**, **Combinations & Subsets Archetype**, **Constraint Placement Archetype**, **Grid Pathfinding Archetype**, **Partitioning Archetype**, and **Graph Cycle / Coloring Archetype**. Identifying trigger words in problem statements allows immediate selection of optimal loop starting indices, visited array management, and duplicate pruning guards.

> **Important:** The 6 Universal Backtracking Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Permutations Archetype**: Trigger = *"Generate all ordered arrangements / sequences"*. Mechanics = Loop starts at **index 0** with `boolean[] visited`. Time = $O(N \cdot N!)$.
> 2. **Pattern 2: Combinations & Subsets Archetype**: Trigger = *"Generate all unordered subsets / combinations of size K"*. Mechanics = Loop starts at **`startIndex`**. Time = $O(2^N)$ / $O(\binom{N}{K})$.
> 3. **Pattern 3: Constraint Placement Archetype**: Trigger = *"Place N non-attacking items / fill Sudoku board"*. Mechanics = $O(1)$ Constraint Arrays (`cols`, `diag`, `boxes`). Time = $O(N!)$ / $O(9^m)$.
> 4. **Pattern 4: Grid Pathfinding Archetype**: Trigger = *"Find paths / word in 2D matrix"*. Mechanics = 4 Directions (D, L, R, U) with `visited[r][c]` reversion. Time = $O(4^{N^2})$.
> 5. **Pattern 5: String Partitioning Archetype**: Trigger = *"Partition string into palindromic or dictionary substrings"*. Mechanics = Loop `end = startIndex ... N` with substring validation. Time = $O(N \cdot 2^N)$.
> 6. **Pattern 6: Graph Cycle & Coloring Archetype**: Trigger = *"Visit every vertex once / Color graph with K colors"*. Mechanics = Adjacency check `isSafe()` + origin re-connection. Time = $O(N!)$ / $O(K^V)$. ⚡

```
Master Backtracking Archetype Decision Flowchart:

Problem Trigger Signal:
├── "Ordered arrangements of N elements?" ─────────► Pattern 1: Permutations (Loop at 0 + visited[])
├── "Unordered subsets / combinations?" ──────────► Pattern 2: Combinations / Subsets (Loop at startIndex)
├── "Place N items / fill Sudoku board?" ──────────► Pattern 3: Constraint Placement (O(1) Constraint Arrays)
├── "Paths / Word search in 2D grid?" ────────────► Pattern 4: Grid Pathfinding (4 Directions + Reversion)
├── "Partition string into valid substrings?" ─────► Pattern 5: String Partitioning (Substring Validation)
└── "Visit every vertex once / K-Coloring?" ───────► Pattern 6: Graph Cycle / Coloring (Adjacency check) ⚡
```

---

## 2. Core Concepts & Master Backtracking Strategy Matrix

### 2.1 Master Backtracking Pattern Recognition Matrix
```
Master Backtracking Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Loop Start Index  | Duplicate Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. Permutations**   | "Ordered sequence"| **Index 0 ⚡**     | `!visited[i-1]` ⚡ | **$O(N \cdot N!)$ ⚡**|
| **2. Combinations**   | "Unordered subset"| **`startIndex` ⚡**| `i > startIndex` ⚡| **$O(2^N)$ / $O(\binom{N}{K})$⚡**|
| **3. Constraint Place**| "Queens / Sudoku"| Row-by-Row        | `cols`/`diag`/`box`| **$O(N!)$ / $O(9^m)$ ⚡**|
| **4. Grid Pathfinding**| "Maze / Word search"| 4 Directions D,L,R,U| `visited[r][c]` rev| **$O(4^{N^2})$ ⚡**|
| **5. Partitioning**   | "Palindrome split"| Substring End     | Substring Check   | **$O(N \cdot 2^N)$ ⚡**|
| **6. Graph Cycle**    | "Hamiltonian/Color"| Vertex Adjacency  | `!visited[v]`     | **$O(N!)$ / $O(K^V)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Permutations loop at 0; Combinations loop at startIndex; Duplicate guard uses i > startIndex (Comb) or !visited[i-1] (Perm)!"**

---

## 3. Deep Dive into the 6 Backtracking Archetypes & LeetCode Audits

### 3.1 Auditing Top LeetCode Benchmark Problems
```
LeetCode Benchmark Problem Audits:

LeetCode 46 (Permutations)                ──► Pattern 1: Permutations (Loop at 0 + boolean[] visited)
LeetCode 47 (Permutations II)             ──► Pattern 1: Permutations (Sort + !visited[i-1] Guard)
LeetCode 78 (Subsets I)                   ──► Pattern 2: Subsets (Capture at EVERY node + startIndex)
LeetCode 90 (Subsets II)                  ──► Pattern 2: Subsets (Sort + i > startIndex Guard)
LeetCode 77 (Combinations)                ──► Pattern 2: Combinations (Loop upper limit pruning)
LeetCode 39 (Combination Sum I)           ──► Pattern 2: Combinations (Re-use: pass startIndex = i)
LeetCode 40 (Combination Sum II)          ──► Pattern 2: Combinations (Single use: pass startIndex = i+1)
LeetCode 51 (N-Queens)                    ──► Pattern 3: Constraint Placement (cols/diag1/diag2)
LeetCode 37 (Sudoku Solver)               ──► Pattern 3: Constraint Placement (3x3 Box + return true)
LeetCode 79 (Word Search)                 ──► Pattern 4: Grid Pathfinding (4 Directions + visited reversion)
LeetCode 131 (Palindrome Partitioning)    ──► Pattern 5: String Partitioning (Substring IsPalindrome Check)
LeetCode 785 (Bipartite 2-Coloring)       ──► Pattern 6: Graph Coloring (BFS/DFS Linear Check)
```

---

## 4. Internal Working Mechanics: String Partitioning Pattern (LeetCode 131)

Tracing LeetCode 131 (Palindrome Partitioning) for $S = \text{"aab"}$:

```
Goal: Partition string S into all possible palindromic substring combinations.

State: backtrack(s, startIndex, path, results)

Depth 0 (startIndex = 0):
- end = 1: Substring "a" is Palindrome? YES!
  Choose "a" -> Recurse startIndex = 1.
  Depth 1 (startIndex = 1):
  - end = 2: Substring "a" is Palindrome? YES!
    Choose "a" -> Recurse startIndex = 2.
    Depth 2 (startIndex = 2):
    - end = 3: Substring "b" is Palindrome? YES!
      Choose "b" -> Recurse startIndex = 3.
      Depth 3 (startIndex = 3 == S.length()):
      CAPTURE SOLUTION: ["a", "a", "b"]! ✅ ⚡

  - end = 3: Substring "ab" is Palindrome? NO! Skip.

- end = 2: Substring "aa" is Palindrome? YES!
  Choose "aa" -> Recurse startIndex = 2.
  - end = 3: Substring "b" is Palindrome? YES!
    CAPTURE SOLUTION: ["aa", "b"]! ✅ ⚡

Total Valid Palindromic Partitions = [["a", "a", "b"], ["aa", "b"]]! ✅ ⚡
```

---

## 5. Visual Diagram: The 6 Backtracking Archetypes Map

```
                            [ Backtracking Decision Engine ]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
          [ Sequence / Subsets ]                        [ Grid / Board / Graph ]
          /          │          \                       /          │          \
         ▼           ▼           ▼                     ▼           ▼           ▼
    Pattern 1    Pattern 2   Pattern 5             Pattern 3   Pattern 4   Pattern 6
  (Permute 0)  (Comb start)  (Partition)          (Constraint) (Grid Path) (Graph Cycle)
  visited[]   startIndex    Substring Pal        cols/diag/box  D,L,R,U    isSafe()
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across the 6 Backtracking Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating Reference Implementations
 * Across the 6 Universal Backtracking Master Archetypes.
 */
public class BacktrackingPatternRecognitionMaster {

    // PATTERN 1: PERMUTATIONS (LeetCode 46)
    public List<List<Integer>> pattern1_Permutations(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        boolean[] visited = new boolean[nums.length];
        permuteDFS(nums, visited, new ArrayList<>(), res);
        return res;
    }
    private void permuteDFS(int[] nums, boolean[] visited, List<Integer> path, List<List<Integer>> res) {
        if (path.size() == nums.length) { res.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < nums.length; i++) { // LOOP AT INDEX 0 ⚡
            if (visited[i]) continue;
            visited[i] = true; path.add(nums[i]);
            permuteDFS(nums, visited, path, res);
            path.remove(path.size() - 1); visited[i] = false;
        }
    }

    // PATTERN 2: COMBINATIONS / SUBSETS (LeetCode 78)
    public List<List<Integer>> pattern2_Subsets(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        subsetsDFS(nums, 0, new ArrayList<>(), res);
        return res;
    }
    private void subsetsDFS(int[] nums, int startIndex, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path)); // CAPTURE AT EVERY NODE ⚡
        for (int i = startIndex; i < nums.length; i++) { // LOOP AT STARTINDEX ⚡
            path.add(nums[i]);
            subsetsDFS(nums, i + 1, path, res);
            path.remove(path.size() - 1);
        }
    }

    // PATTERN 3: CONSTRAINT PLACEMENT (LeetCode 51 N-Queens)
    public List<List<String>> pattern3_NQueens(int n) {
        List<List<String>> res = new ArrayList<>();
        char[][] board = new char[n][n];
        for (char[] row : board) Arrays.fill(row, '.');
        nQueensDFS(board, 0, n, new boolean[n], new boolean[2*n], new boolean[2*n], res);
        return res;
    }
    private void nQueensDFS(char[][] board, int r, int n, boolean[] cols, boolean[] d1, boolean[] d2, List<List<String>> res) {
        if (r == n) {
            List<String> b = new ArrayList<>(); for (char[] row : board) b.add(new String(row));
            res.add(b); return;
        }
        for (int c = 0; c < n; c++) {
            if (cols[c] || d1[r + c] || d2[r - c + n]) continue; // CONSTRAINT CHECK ⚡
            board[r][c] = 'Q'; cols[c] = d1[r + c] = d2[r - c + n] = true;
            nQueensDFS(board, r + 1, n, cols, d1, d2, res);
            board[r][c] = '.'; cols[c] = d1[r + c] = d2[r - c + n] = false;
        }
    }

    // PATTERN 5: STRING PARTITIONING (LeetCode 131 Palindrome Partitioning)
    public List<List<String>> pattern5_Partition(String s) {
        List<List<String>> res = new ArrayList<>();
        partitionDFS(s, 0, new ArrayList<>(), res);
        return res;
    }
    private void partitionDFS(String s, int startIndex, List<String> path, List<List<String>> res) {
        if (startIndex == s.length()) { res.add(new ArrayList<>(path)); return; }
        for (int end = startIndex + 1; end <= s.length(); end++) {
            String sub = s.substring(startIndex, end);
            if (isPalindrome(sub)) {
                path.add(sub);
                partitionDFS(s, end, path, res);
                path.remove(path.size() - 1);
            }
        }
    }
    private boolean isPalindrome(String s) {
        int l = 0, r = s.length() - 1;
        while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
        return true;
    }
}
```

> **Quick Syntax:**
```java
// Master Backtracking Loop Rules
// Permutations (Pattern 1) : for (int i = 0; i < n; i++) if (!visited[i]) ...
// Combinations (Pattern 2)  : for (int i = startIndex; i < n; i++) ...
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Permutations)**: LeetCode 46, LeetCode 47, LeetCode 31.
* **Pattern 2 (Combinations & Subsets)**: LeetCode 78, LeetCode 90, LeetCode 77, LeetCode 39, LeetCode 40, LeetCode 216.
* **Pattern 3 (Constraint Placement)**: LeetCode 51, LeetCode 52, LeetCode 37.
* **Pattern 4 (Grid Pathfinding)**: Rat in a Maze, LeetCode 79.
* **Pattern 5 (String Partitioning)**: LeetCode 131, LeetCode 93 (Restore IP Addresses).
* **Pattern 6 (Graph Cycle & Coloring)**: Hamiltonian Cycle, Graph $K$-Coloring, LeetCode 785.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class BacktrackingPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   6 MASTER BACKTRACKING ARCHETYPES DEMO         ");
        System.out.println("=================================================\n");

        BacktrackingPatternRecognitionMaster master = new BacktrackingPatternRecognitionMaster();

        // 1. Pattern 1 (Permutations)
        int[] permNums = {1, 2, 3};
        System.out.println("1. Pattern 1 (Permutations [1,2,3]): Total = " + master.pattern1_Permutations(permNums).size());

        // 2. Pattern 2 (Subsets)
        int[] subNums = {1, 2, 3};
        System.out.println("2. Pattern 2 (Subsets [1,2,3]): Total = " + master.pattern2_Subsets(subNums).size());

        // 3. Pattern 3 (N-Queens N=4)
        System.out.println("3. Pattern 3 (Constraint Placement N=4): Total Solutions = " + master.pattern3_NQueens(4).size());

        // 4. Pattern 5 (Palindrome Partitioning "aab")
        List<List<String>> partitions = master.pattern5_Partition("aab");
        System.out.println("4. Pattern 5 (String Partitioning \"aab\"): Partitions = " + partitions);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Backtracking Master Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Permutations**   | $\mathbf{O(N \cdot N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack ⚡| "Generate all ordered arrangements" |
| **2. Combinations**   | $\mathbf{O(2^N)}$ / $\mathbf{O(\binom{N}{K})}$⚡| $\mathbf{O(N)}$ Stack ⚡| "Generate all unordered subsets / size K" |
| **3. Constraint Place**| $\mathbf{O(N!)}$ / $\mathbf{O(9^m)}$ ⚡| $\mathbf{O(N)}$ Stack ⚡| "Place N non-attacking items / fill Sudoku" |
| **4. Grid Pathfinding**| $\mathbf{O(4^{N^2})}$ Exponential⚡| $\mathbf{O(N^2)}$ Matrix ⚡| "Find paths / word in 2D grid" |
| **5. Partitioning**   | $\mathbf{O(N \cdot 2^N)}$ ⚡| $\mathbf{O(N)}$ Stack ⚡| "Partition string into valid substrings" |
| **6. Graph Cycle**    | $\mathbf{O(N!)}$ / $\mathbf{O(K^V)}$ ⚡| $\mathbf{O(V)}$ Stack ⚡| "Visit every vertex once / K-Coloring" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Permutations and Combinations**:
   - Element order matters $\to$ **Loop at index 0 + `visited[]`**.
   - Element order does NOT matter $\to$ **Loop at `startIndex`**.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using `visited[]` Array in Combination / Subsets Search**:
  - `visited[]` is ONLY used when iterating from index 0 in Permutations. In Combinations, the `startIndex` pointer handles forward progress naturally. **Do not use `visited[]` for Combinations!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Backtracking Selector Rule:
> 1. Ordered arrangement? $\to$ Pattern 1 (Loop at 0 + `visited[]`).
> 2. Unordered subset? $\to$ Pattern 2 (Loop at `startIndex`).
> 3. Queens / Sudoku? $\to$ Pattern 3 (Constraint arrays).
> 4. Grid path? $\to$ Pattern 4 (4 Directions + visited reversion).
> 5. String split? $\to$ Pattern 5 (Substring check).
> 6. Vertex cycle / coloring? $\to$ Pattern 6 (Adjacency check). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Loop Starting Index | Tracking Method | Solution Capture Depth |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Permutations)** | **Index 0 ⚡** | `boolean[] visited` | Leaf Nodes Only (`path.size() == N`) |
| **Pattern 2 (Subsets)** | **`startIndex` ⚡** | Index Pointer | **EVERY Node (`results.add(...)`) ⚡** |
| **Pattern 2 (Combinations)**| **`startIndex` ⚡** | Index Pointer | Leaf Nodes Only (`path.size() == K`) |

---

## 14. How to Recognize This in Questions

* **"Generate all valid palindromic partitions of string S"** $\rightarrow$ Pattern 5 (LeetCode 131).
* **"Find all words on 2D board of characters"** $\rightarrow$ Pattern 4 (LeetCode 79).

---

## 15. Frequently Asked Interview Questions

* **Q: How do you differentiate Permutations from Combinations in backtracking code?**  
  *A:* By the loop starting index: Permutations start from index 0 with a `visited[]` array, while Combinations start from `startIndex` without `visited[]`.

* **Q: Why does Subsets capture solutions at every node while Combinations captures only at leaf nodes?**  
  *A:* Because every node in a subsets state tree represents a valid subset of any size ($0 \dots N$), whereas combinations require a fixed target size $K$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 6 MASTER BACKTRACKING ARCHETYPES                      |
+-----------------------------------------------------------------------+
| • Pattern 1: Permutations -> Loop i = 0..N-1 + boolean[] visited       |
| • Pattern 2: Combinations -> Loop i = startIndex..N-1                 |
| • Pattern 3: Constraint   -> O(1) Arrays (cols, diag, boxes)          |
| • Pattern 4: Grid Paths   -> 4 Directions + visited[r][c] = false     |
| • Pattern 5: Partitioning -> Substring end = startIndex..N            |
| • Pattern 6: Graph Cycle  -> Adjacency isSafe() + origin re-connect   |
| • Rule     : Always deep copy results.add(new ArrayList<>(path))! ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any backtracking problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I know when to loop from index 0 vs `startIndex`.
- [ ] I can write Permutations (LeetCode 46) and Subsets (LeetCode 78) in Java.
- [ ] I can write N-Queens (LeetCode 51) and Sudoku Solver (LeetCode 37) in Java.
- [ ] I can write Palindrome Partitioning (LeetCode 131) in Java.
