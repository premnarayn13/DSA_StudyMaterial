# 11. Pattern Recognition & Problem Triggers: Identifying Recursive Archetypes

## 1. Introduction
In competitive programming and technical coding interviews, speed and accuracy depend on rapid **Pattern Recognition**. Rather than attempting to solve every recursive problem from scratch, expert engineers map problem statements directly to one of six universal **Recursive Algorithmic Archetypes**: **State Space Expansion (Combinatorial)**, **Two-Pointer Range Shrinking**, **Divide & Conquer Halving**, **In-Place Grid Masking**, **Top-Down Memoization**, and **Accumulator Tail Optimization**. Recognizing key structural trigger phrases in problem descriptions enables instant selection of optimal state representations, base case guards, and time complexity bounds.

> **Important:** The 6 Universal Recursive Master Patterns & Triggers:
> 1. **Pattern 1: State Space Expansion (Backtracking)**: Trigger = *"Find all permutations, subsets, or combinations of length N"*. State = `(index, path)`. Time = $O(2^N)$ or $O(N!)$.
> 2. **Pattern 2: Two-Pointer Window Shrinking**: Trigger = *"Check palindrome or match symmetric boundaries inward"*. State = `(left, right)`. Time = $O(N)$.
> 3. **Pattern 3: Divide & Conquer Halving**: Trigger = *"Logarithmic interval search or balanced tree sorting"*. State = `(low, high)`. Time = $O(\log N)$ or $O(N \log N)$.
> 4. **Pattern 4: In-Place Grid Masking (2D DFS)**: Trigger = *"Find connected components, island counts, or maze paths"*. State = `(r, c)`. Time = $O(M \cdot N)$.
> 5. **Pattern 5: Top-Down Memoization (DP)**: Trigger = *"Find min/max value or total ways with repeating sub-choices"*. State = `(index, target)`. Time = $O(N \cdot K)$.
> 6. **Pattern 6: Accumulator Tail Transformation**: Trigger = *"Eliminate stack memory overhead for deep linear calls"*. State = `(n, accumulator)`. Space = $O(1)$. ⚡

```
Master Pattern Decision Tree Topography:
Problem Description Trigger Signal:
├── "Find ALL combinations / permutations?" ─────────> Pattern 1: State Space Expansion (Backtracking)
├── "Check string symmetry or outer boundaries?" ────> Pattern 2: Two-Pointer Window Shrinking
├── "Halve search space or divide sub-arrays?" ──────> Pattern 3: Divide & Conquer Halving
├── "2D Matrix connected component traversal?" ──────> Pattern 4: In-Place Grid Masking
└── "Max/Min optimal choice with overlapping sub-states?" ──> Pattern 5: Top-Down Memoization ⚡
```

---

## 2. Core Concepts & Master Pattern Strategy Matrix

### 2.1 Pattern Recognition Matrix
```
Master Recursive Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | State Parameters  | Primary Mechanism |
+-----------------------+-------------------+-------------------+-------------------+
| **1. State Expansion**| "Find all subsets"| `(index, path)`   | Choose-Unchoose   |
| **2. Window Shrink**  | "Check palindrome"| `(left, right)`   | Dual Inward Moves |
| **3. Halving Divide** | "Search in log N" | `(low, high)`     | Mid Pivot Division|
| **4. Grid Masking**   | "Count islands"   | `(r, c)`          | In-Place Mutation |
| **5. Memoized DP**    | "Max profit / ways"| `(index, target)` | Lookup Table Cache|
| **6. Accumulator**    | "O(1) stack memory"| `(n, acc)`       | Tail Position Call|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Subsets = Expansion! Symmetry = Window Shrink! Islands = Grid Masking! Max Ways = Memoized DP!"**

---

## 3. Deep Dive into the 6 Recursive Archetypes

### 3.1 Archetype 1: State Space Expansion (Combinatorial Backtracking)
* **Trigger Words**: *"Generate all..."*, *"Find all unique permutations..."*, *"Power Set..."*
* **State Template**: `solve(int index, List<Integer> path)`
* **Invariants**: Loop `i` from `start` to `N - 1`. Perform Choose-Recurse-Unchoose Triad. Add `new ArrayList<>(path)` at base case.

### 3.2 Archetype 2: Two-Pointer Window Shrinking
* **Trigger Words**: *"Validate palindrome..."*, *"Reverse array recursively..."*, *"Match outer ends..."*
* **State Template**: `solve(int left, int right)`
* **Invariants**: Base case `left >= right`. Check boundary match `arr[left] == arr[right]`. Recurse `(left + 1, right - 1)`.

### 3.3 Archetype 3: Divide & Conquer Halving
* **Trigger Words**: *"Sorted array search..."*, *"Sort in O(N log N)..."*, *"Fast power X^N..."*
* **State Template**: `solve(int low, int high)`
* **Invariants**: Base case `low > high` or `low == high`. Compute `mid = low + (high - low) / 2`. Recurse on left/right partitions.

---

## 4. Internal Working Mechanics: Matching LeetCode Problems to Archetypes

```
Problem Match Audits:

LeetCode 78 (Subsets)             ---> Match Archetype 1: State Space Expansion (Index + Path)
LeetCode 125 (Valid Palindrome)   ---> Match Archetype 2: Two-Pointer Window Shrinking (Left + Right)
LeetCode 33 (Rotated Array Search)---> Match Archetype 3: Divide & Conquer Halving (Low + High)
LeetCode 200 (Number of Islands)  ---> Match Archetype 4: Grid Masking DFS (Row + Col)
LeetCode 322 (Coin Change)        ---> Match Archetype 5: Top-Down Memoization (Index + Remaining)
LeetCode 50 (Pow(x, n))           ---> Match Archetype 3: Divide & Conquer Halving (Half Exponent)
```

---

## 5. Visual Diagram: Pattern Selector Flowchart

```
                          [ New Problem Statement ]
                                      │
                         Is it a 2D Matrix / Grid?
                             /                \
                         (Yes)                (No)
                          /                      \
             [ Pattern 4: Grid Masking ]      Is it generating ALL combinations?
                                                 /                  \
                                             (Yes)                  (No)
                                              /                        \
                             [ Pattern 1: State Expansion ]     Does it have overlapping sub-choices?
                                                                   /                   \
                                                               (Yes)                   (No)
                                                                /                         \
                                                   [ Pattern 5: Memoized DP ]     [ Pattern 3: Divide & Conquer ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across all 6 Recursive Master Patterns.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating the 6 Recursive Algorithmic Archetypes.
 */
public class PatternRecognitionMaster {

    // =========================================================================
    // PATTERN 1: STATE SPACE EXPANSION (Combinatorial Subsets O(2^N))
    // =========================================================================
    public List<List<Integer>> pattern1_StateSpaceExpansion(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null) return result;
        backtrackExpansion(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrackExpansion(int[] nums, int start, List<Integer> path, List<List<Integer>> result) {
        result.add(new ArrayList<>(path)); // Store deep copy snapshot

        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);                                   // 1. CHOOSE
            backtrackExpansion(nums, i + 1, path, result);       // 2. RECURSE
            path.remove(path.size() - 1);                        // 3. UNCHOOSE
        }
    }

    // =========================================================================
    // PATTERN 2: TWO-POINTER WINDOW SHRINKING (Palindrome Verification O(N))
    // =========================================================================
    public boolean pattern2_TwoPointerWindowShrink(String s) {
        if (s == null) return false;
        return windowShrinkHelper(s, 0, s.length() - 1);
    }

    private boolean windowShrinkHelper(String s, int left, int right) {
        if (left >= right) return true; // Base Case Guard
        if (s.charAt(left) != s.charAt(right)) return false;
        return windowShrinkHelper(s, left + 1, right - 1); // Shrink window
    }

    // =========================================================================
    // PATTERN 3: DIVIDE & CONQUER HALVING (Fast Power O(log N))
    // =========================================================================
    public double pattern3_DivideAndConquerHalving(double x, int n) {
        long N = n;
        if (N < 0) {
            x = 1.0 / x;
            N = -N;
        }
        return halvingHelper(x, N);
    }

    private double halvingHelper(double x, long n) {
        if (n == 0) return 1.0;
        if (n == 1) return x;

        double half = halvingHelper(x, n / 2); // Halve subproblem size
        return (n % 2 == 0) ? (half * half) : (half * half * x);
    }

    // =========================================================================
    // PATTERN 4: IN-PLACE GRID MASKING (Island Count 2D DFS O(M * N))
    // =========================================================================
    public int pattern4_InPlaceGridMasking(char[][] grid) {
        if (grid == null || grid.length == 0) return 0;
        int islands = 0;
        int rows = grid.length, cols = grid[0].length;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '1') {
                    islands++;
                    gridMaskingDFS(grid, r, c, rows, cols); // Sink connected land
                }
            }
        }
        return islands;
    }

    private void gridMaskingDFS(char[][] grid, int r, int c, int rows, int cols) {
        if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') return;

        grid[r][c] = '0'; // In-place cell masking!

        gridMaskingDFS(grid, r + 1, c, rows, cols);
        gridMaskingDFS(grid, r - 1, c, rows, cols);
        gridMaskingDFS(grid, r, c + 1, rows, cols);
        gridMaskingDFS(grid, r, c - 1, rows, cols);
    }

    // =========================================================================
    // PATTERN 5: TOP-DOWN MEMOIZATION (Coin Change Min Coins O(N * Amount))
    // =========================================================================
    public int pattern5_TopDownMemoization(int[] coins, int amount) {
        if (coins == null || amount < 0) return -1;
        int[] memo = new int[amount + 1];
        Arrays.fill(memo, -2); // -2 represents unvisited
        return memoCoinHelper(coins, amount, memo);
    }

    private int memoCoinHelper(int[] coins, int rem, int[] memo) {
        if (rem == 0) return 0;
        if (rem < 0) return -1;
        if (memo[rem] != -2) return memo[rem];

        int minCoins = Integer.MAX_VALUE;
        for (int coin : coins) {
            int subRes = memoCoinHelper(coins, rem - coin, memo);
            if (subRes >= 0) {
                minCoins = Math.min(minCoins, subRes + 1);
            }
        }

        memo[rem] = (minCoins == Integer.MAX_VALUE) ? -1 : minCoins;
        return memo[rem];
    }
}
```

> **Quick Syntax:**
```java
// Pattern Recognition Quick Identifier Template
// Trigger: "Generate all..." -> Pattern 1: State Space Expansion
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (State Expansion)**: LeetCode 78 (Subsets), LeetCode 46 (Permutations), LeetCode 39 (Combination Sum).
* **Pattern 2 (Window Shrinking)**: LeetCode 125 (Valid Palindrome), LeetCode 344 (Reverse String).
* **Pattern 3 (Divide Halving)**: LeetCode 50 (Pow(x, n)), LeetCode 23 (Merge k Sorted Lists).
* **Pattern 4 (Grid Masking)**: LeetCode 200 (Number of Islands), LeetCode 733 (Flood Fill).
* **Pattern 5 (Memoized DP)**: LeetCode 322 (Coin Change), LeetCode 198 (House Robber).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class PatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   RECURSIVE PATTERN RECOGNITION DEMONSTRATION   ");
        System.out.println("=================================================\n");

        PatternRecognitionMaster master = new PatternRecognitionMaster();

        // 1. Pattern 1 Test (Subsets)
        int[] set = {1, 2};
        List<List<Integer>> subsets = master.pattern1_StateSpaceExpansion(set);
        System.out.println("1. Pattern 1 (State Expansion) Subsets for " + Arrays.toString(set) + ": " + subsets);
        System.out.println("-------------------------------------------------");

        // 2. Pattern 2 Test (Window Shrinking)
        String pal = "racecar";
        boolean isPal = master.pattern2_TwoPointerWindowShrink(pal);
        System.out.println("2. Pattern 2 (Window Shrinking) Is '" + pal + "' Palindrome? " + isPal);
        System.out.println("-------------------------------------------------");

        // 3. Pattern 3 Test (Divide Halving)
        double pow = master.pattern3_DivideAndConquerHalving(2.0, 10);
        System.out.println("3. Pattern 3 (Divide Halving) Pow(2, 10): " + pow);
        System.out.println("-------------------------------------------------");

        // 4. Pattern 4 Test (Grid Masking)
        char[][] grid = {
            {'1', '1', '0', '0'},
            {'1', '1', '0', '0'},
            {'0', '0', '1', '0'},
            {'0', '0', '0', '1'}
        };
        int islands = master.pattern4_InPlaceGridMasking(grid);
        System.out.println("4. Pattern 4 (Grid Masking) Total Islands Found: " + islands);
        System.out.println("-------------------------------------------------");

        // 5. Pattern 5 Test (Memoized DP Coin Change)
        int[] coins = {1, 2, 5};
        int amount = 11;
        int minCoins = master.pattern5_TopDownMemoization(coins, amount);
        System.out.println("5. Pattern 5 (Memoized DP) Min Coins for Amount " + amount + ": " + minCoins);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Master Pattern | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. State Expansion** | $\mathbf{O(2^N)}$ or $\mathbf{O(N!)}$ | $\mathbf{O(N)}$ Stack Depth | "Generate all combinations / subsets" |
| **2. Window Shrinking**| $\mathbf{O(N)}$ Linear ⚡ | $\mathbf{O(N)}$ Stack Depth | "Check palindrome / symmetric ends" |
| **3. Divide Halving**  | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Stack Depth | "Halve search space / fast power" |
| **4. Grid Masking**    | $\mathbf{O(M \cdot N)}$ Linear ⚡| $\mathbf{O(M \cdot N)}$ Call Stack| "Connected grid components / islands" |
| **5. Memoized DP**     | $\mathbf{O(N \cdot K)}$ Poly ⚡ | $\mathbf{O(N \cdot K)}$ Cache Table| "Find min/max value with overlapping states" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Pattern 1 (Backtracking) and Pattern 5 (Memoized DP)**:
   - If problem asks for **ALL valid configurations** $\implies$ Use Pattern 1 (Backtracking cannot be memoized because every full path is unique!).
   - If problem asks for **MIN/MAX/COUNT value** $\implies$ Use Pattern 5 (Top-Down Memoization).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Attempting to Memoize All-Path Backtracking (Pattern 1)**:
  - Memoization caches optimal *values*, NOT lists of millions of distinct path configurations. Applying memoization to "Generate All Subsets" breaks path collection.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Pattern Matching Protocol:
> When presented with a problem:
> 1. Look for output type: List of configurations $\to$ Pattern 1 (Backtracking); Min/Max numeric value $\to$ Pattern 5 (DP).
> 2. Look for input structure: 2D Matrix $\to$ Pattern 4 (Grid Masking); Single String/Array $\to$ Pattern 2 or 3.
> Matching these 2 structural signals identifies the exact archetype before writing a single line of code! ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Focus | State Mutation Method | Memory Footprint |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Backtracking)** | Exhaustive Tree Search | Shared List `add/remove` | $O(N)$ Path Memory |
| **Pattern 4 (Grid Masking)** | Topology Traversal | In-Place Cell Overwrite `0` | $O(M \cdot N)$ Stack Memory |
| **Pattern 5 (Memoized DP)** | Subproblem Optimization | Array / Matrix Cache Lookups | $O(N \cdot K)$ Table Memory |

---

## 14. How to Recognize This in Questions

* **"Generate all..."** $\rightarrow$ Pattern 1 (State Expansion).
* **"Find minimum cost to reach..."** $\rightarrow$ Pattern 5 (Memoized DP).
* **"Count connected regions in 2D array"** $\rightarrow$ Pattern 4 (Grid Masking).

---

## 15. Frequently Asked Interview Questions

* **Q: Why can't we memoize "Generate All Permutations"?**  
  *A:* Because every permutation path is unique and must be emitted. Subproblem states do not share a single scalar optimal answer, so caching does not reduce output complexity.

* **Q: How does Grid Masking (Pattern 4) eliminate the need for a visited matrix?**  
  *A:* By mutating target cells in-place (e.g. overwriting land `'1'` with `'0'`). Subsequent recursive calls see `'0'` and treat it as water, skipping the cell automatically.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RECURSIVE PATTERN RECOGNITION                         |
+-----------------------------------------------------------------------+
| • Pattern 1: State Expansion (Backtracking) -> "Generate all subsets" |
| • Pattern 2: Window Shrink                  -> "Check palindrome"    |
| • Pattern 3: Divide Halving                 -> "Search in log N"     |
| • Pattern 4: Grid Masking                   -> "Count islands"       |
| • Pattern 5: Memoized DP                    -> "Min/Max optimal ways"|
| • Key Rule : Configurations = Backtrack; Optimal Value = Memoized DP! ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any recursive problem statement to one of the 6 Master Patterns.
- [ ] I know when to use Backtracking (Pattern 1) versus Memoized DP (Pattern 5).
- [ ] I can write Two-Pointer Window Shrinking in Java.
- [ ] I can write In-Place Grid Masking for 2D connected component problems.
- [ ] I can write Divide & Conquer Halving for logarithmic calculations.
