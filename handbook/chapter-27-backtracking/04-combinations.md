# 04. Combinations: Unordered Subsets, Combination Sums & Loop Upper Bound Pruning

## 1. Introduction
**Combination Backtracking** generates unordered selections of $K$ elements from a set of $N$ candidate items where element order does NOT matter (i.e. $\{1, 2\}$ is mathematically identical to $\{2, 1\}$). To prevent generating identical candidate sets in different permutations, combination backtracking algorithms enforce the **Forward Indexing Invariant**: candidate loop iterations start strictly from **`startIndex`** (`for (int i = startIndex; i < n; i++)`), advancing forward to ensure that elements at smaller indices can never be chosen after elements at larger indices. Major variation benchmarks include **Combinations (LeetCode 77)**, **Combination Sum I (LeetCode 39)** (infinite item re-use), **Combination Sum II (LeetCode 40)** (single item use + duplicate pruning), and **Combination Sum III (LeetCode 216)**. Applying **Loop Upper Bound Pruning** (`i <= n - (k - path.size()) + 1`) prunes unviable search branches in advance, optimizing execution bounds.

> **Important:** Core Structural Invariants of Combination Backtracking:
> 1. **Forward Indexing Invariant (`startIndex`)**:
>    - Iterates `for (int i = startIndex; i < n; i++)`, ensuring candidate choices move monotonically forward, eliminating duplicate unordered combinations.
> 2. **Item Re-usability Rule**:
>    - **Single-Use Items (LC 77, LC 40)**: Next recursive call passes `startIndex = i + 1`.
>    - **Infinite-Use Items (LC 39)**: Next recursive call passes `startIndex = i` (allowing current element to be picked again!).
> 3. **Combination Sum II Duplicate Pruning Invariant (LC 40)**:
>    - Sort candidate array first ($nums[0] \le nums[1] \le \dots$).
>    - Skip candidate element $i$ if it equals its predecessor AND is NOT the first choice at the current decision level:
>      $$\text{if } (i > startIndex \text{ \&\& } nums[i] == nums[i-1]) \quad \text{continue;}$$
> 4. **Loop Upper Bound Pruning Formula (LC 77)**:
>    - Prune loop when remaining items in range $[i \dots n]$ are insufficient to fill remaining needed slots $(k - \text{path.size()})$:
>      $$\text{Upper Limit } i \le n - (k - \text{path.size()}) + 1$$ ⚡

```
Combination Loop Upper Bound Pruning Topology (N = 4, K = 3):

Goal: Pick K = 3 numbers from [1, 2, 3, 4].
Current path size = 0 -> Need (3 - 0) = 3 elements!

Candidate Loop i at depth 0:
- i = 1: Remaining elements [1, 2, 3, 4] (4 elements >= 3) -> VALID! ✅
- i = 2: Remaining elements [2, 3, 4] (3 elements >= 3) -> VALID! ✅
- i = 3: Remaining elements [3, 4] (2 elements < 3) -> PRUNED! ❌
- i = 4: Remaining elements [4] (1 element < 3) -> PRUNED! ❌

Upper Bound Formula (i <= 4 - 3 + 1 = 2) eliminates useless iterations! ⚡
```

---

## 2. Core Concepts & Combination Strategy Matrix

### 2.1 Combination Variations Strategy Matrix
```
Combination Variations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Combination Variant   | Target Goal       | Next `startIndex` | Duplicate Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Combinations (77)** | $K$ Elements      | `i + 1`           | Upper Bound Prune | **$O(\binom{N}{K})$ ⚡**|
| **Comb Sum I (39)**   | Target Sum $T$    | **`i` (Re-use)⚡** | Target Check      | $O(2^T)$          |
| **Comb Sum II (40)**  | Target Sum $T$    | `i + 1`           | **`i > startIndex` ⚡**| $O(2^N)$          |
| **Comb Sum III (216)**| Size $K$, Sum $T$ | `i + 1`           | Numbers $1 \dots 9$| **$O(\binom{9}{K})$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Combinations use startIndex; Re-use item = pass i; Single item = pass i+1; Skip duplicates = if (i > startIndex && nums[i] == nums[i-1]) continue!"**

---

## 3. Characteristics & Combination Sum II Duplicate Pruning Derivation

### 3.1 Mathematical Proof of `i > startIndex` Duplicate Pruning (LeetCode 40)
* Consider sorted candidate array $nums = [1_a, 1_b, 2, 5]$ and Target $T = 8$.
* **The Goal**: Prevent generating duplicate combination subsets (e.g. $[1_a, 2, 5]$ and $[1_b, 2, 5]$).
* **Case Analysis of `if (i > startIndex && nums[i] == nums[i-1]) continue;`**:
  - At decision depth $D$, `startIndex` is the FIRST candidate position evaluated at this level.
  - When $i = startIndex$: Element $nums[i] = 1_a$ is chosen. This is the FIRST occurrence of value $1$ at level $D$. It explores all valid combinations containing $1$.
  - When $i = startIndex + 1$: Candidate element is $nums[i] = 1_b$. Since $1_b == 1_a$ AND $i > startIndex$, this branch would attempt to start a search at level $D$ with value $1$ a SECOND time, creating duplicate combination subtrees!
  - Skipping $1_b$ at level $D$ guarantees that each unique value is used at most ONCE as a branching choice at any decision level.
  - Note that $[1_a, 1_b, 6]$ is STILL ALLOWED because $1_b$ is chosen at level $D+1$ where `startIndex == 1`, making $i == startIndex$! ⚡

---

## 4. Internal Working Mechanics: Loop Upper Bound Pruning Mechanics

Tracing LeetCode 77 (Combinations of size $K=3$ from $N=5$):

```
Unpruned Loop: for (int i = startIndex; i <= 5; i++)
Pruned Loop  : for (int i = startIndex; i <= 5 - (3 - path.size()) + 1; i++)

Depth 0 (path.size() = 0):
- Needed elements = 3 - 0 = 3.
- Upper Limit i <= 5 - 3 + 1 = 3.
- Loop runs for i = 1, 2, 3 ONLY! (i = 4, 5 skipped immediately!).

Depth 1 (path.size() = 1, chosen 1):
- Needed elements = 3 - 1 = 2.
- Upper Limit i <= 5 - 2 + 1 = 4.
- Loop runs for i = 2, 3, 4 ONLY! (i = 5 skipped!).

Pruning eliminates ~50% of state tree nodes! ✅ ⚡
```

---

## 5. Visual Diagram: Combination Sum II Duplicate Pruning Tree

```
Combination Sum II Duplicate Pruning Tree (candidates = [1_a, 1_b, 2], Target = 3):

                                  [ Root (Sum=0) ]
                      /                  |                  \
           [ Choice 1_a ]          [ Choice 1_b ]          [ Choice 2 ]
         (i = startIndex)       (i > startIndex!)
                │                        │
          Valid Branch               PRUNED! ❌
         /            \        (nums[i]==nums[i-1] Guard)
  [1_a, 1_b]        [1_a, 2]
  (Sum=2)          (Sum=3 ✅)

Guarantees unique combination sum outputs! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Combinations with Pruning (LeetCode 77), Combination Sum I (LeetCode 39), Combination Sum II (LeetCode 40), and Combination Sum III (LeetCode 216).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Combination Backtracking:
 * Unordered Selections, Re-usable Items, Combination Sums, and Upper Bound Pruning.
 */
public class CombinationsMaster {

    // =========================================================================
    // 1. LEETCODE 77: COMBINATIONS WITH LOOP UPPER BOUND PRUNING
    // =========================================================================
    /**
     * Generates all combinations of K numbers chosen from range 1 ... N.
     *
     * @param n range upper bound (1 ... N)
     * @param k target combination size
     * @return list of all combinations
     */
    public List<List<Integer>> combine(int n, int k) {
        List<List<Integer>> results = new ArrayList<>();
        if (n <= 0 || k <= 0 || k > n) return results;

        List<Integer> path = new ArrayList<>();
        combineDFS(n, k, 1, path, results);
        return results;
    }

    private void combineDFS(int n, int k, int startIndex, List<Integer> path, List<List<Integer>> results) {
        if (path.size() == k) {
            results.add(new ArrayList<>(path)); // Deep copy! ⚡
            return;
        }

        // LOOP UPPER BOUND PRUNING FORMULA LINE ⚡
        int upperLimit = n - (k - path.size()) + 1;

        for (int i = startIndex; i <= upperLimit; i++) {
            // Choose
            path.add(i);

            // Explore
            combineDFS(n, k, i + 1, path, results);

            // Unchoose (Backtrack!) ⚡
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 2. LEETCODE 39: COMBINATION SUM I (INFINITE RE-USE O(2^T) Time)
    // =========================================================================
    /**
     * Finds combinations summing to target where candidate items can be REUSED infinitely.
     */
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> results = new ArrayList<>();
        if (candidates == null || target <= 0) return results;

        Arrays.sort(candidates); // Sort for early sum pruning!
        List<Integer> path = new ArrayList<>();
        combinationSumDFS(candidates, target, 0, path, results);
        return results;
    }

    private void combinationSumDFS(int[] candidates, int remainingTarget, int startIndex, List<Integer> path, List<List<Integer>> results) {
        if (remainingTarget == 0) {
            results.add(new ArrayList<>(path));
            return;
        }

        for (int i = startIndex; i < candidates.length; i++) {
            // Early Sum Pruning: candidates array is sorted!
            if (remainingTarget - candidates[i] < 0) break; // Prune all larger candidates! ⚡

            // Choose
            path.add(candidates[i]);

            // Explore: Pass startIndex = i to allow INFINITE RE-USE of candidates[i]! ⚡
            combinationSumDFS(candidates, remainingTarget - candidates[i], i, path, results);

            // Unchoose
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 3. LEETCODE 40: COMBINATION SUM II (SINGLE-USE + DUPLICATE PRUNING)
    // =========================================================================
    /**
     * Finds unique combinations summing to target where each candidate item is used ONCE.
     */
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        List<List<Integer>> results = new ArrayList<>();
        if (candidates == null || target <= 0) return results;

        // Step 1: Sort candidates to group duplicates together! ⚡
        Arrays.sort(candidates);
        List<Integer> path = new ArrayList<>();
        combinationSum2DFS(candidates, target, 0, path, results);
        return results;
    }

    private void combinationSum2DFS(int[] candidates, int remainingTarget, int startIndex, List<Integer> path, List<List<Integer>> results) {
        if (remainingTarget == 0) {
            results.add(new ArrayList<>(path));
            return;
        }

        for (int i = startIndex; i < candidates.length; i++) {
            if (remainingTarget - candidates[i] < 0) break; // Early sum prune

            // COMBINATION DUPLICATE PRUNING INVARIANT LINE ⚡
            if (i > startIndex && candidates[i] == candidates[i - 1]) continue;

            // Choose
            path.add(candidates[i]);

            // Explore: Pass startIndex = i + 1 for SINGLE-USE items! ⚡
            combinationSum2DFS(candidates, remainingTarget - candidates[i], i + 1, path, results);

            // Unchoose
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 4. LEETCODE 216: COMBINATION SUM III (SIZE K USING DIGITS 1..9)
    // =========================================================================
    public List<List<Integer>> combinationSum3(int k, int n) {
        List<List<Integer>> results = new ArrayList<>();
        if (k <= 0 || n <= 0) return results;

        List<Integer> path = new ArrayList<>();
        combinationSum3DFS(k, n, 1, path, results);
        return results;
    }

    private void combinationSum3DFS(int k, int remainingSum, int startIndex, List<Integer> path, List<List<Integer>> results) {
        if (path.size() == k) {
            if (remainingSum == 0) results.add(new ArrayList<>(path));
            return;
        }

        int upperLimit = 9 - (k - path.size()) + 1; // Pruned upper limit ⚡

        for (int i = startIndex; i <= upperLimit; i++) {
            if (remainingSum - i < 0) break; // Sum prune

            path.add(i);
            combinationSum3DFS(k, remainingSum - i, i + 1, path, results);
            path.remove(path.size() - 1);
        }
    }
}
```

> **Quick Syntax:**
```java
// Combination Sum II Duplicate Pruning & Single-Use Lines
if (i > startIndex && candidates[i] == candidates[i - 1]) continue; combinationSum2DFS(..., i + 1, ...);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 77 - Combinations**:
   - Combination generation with loop upper bound pruning ($O(\binom{N}{K})$ time).

2. **LeetCode 39 - Combination Sum**:
   - Re-usable items combination sum ($O(2^T)$ time, pass `startIndex = i`).

3. **LeetCode 40 - Combination Sum II**:
   - Single-use items with duplicate pruning ($O(2^N)$ time, `i > startIndex`).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class CombinationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   COMBINATION BACKTRACKING BENCHMARK DEMO      ");
        System.out.println("=================================================\n");

        CombinationsMaster master = new CombinationsMaster();

        // 1. Combinations Test (LeetCode 77)
        int n1 = 4, k1 = 2;
        List<List<Integer>> comb1 = master.combine(n1, k1);
        System.out.println("1. LeetCode 77 Combinations for N = " + n1 + ", K = " + k1 + ":");
        System.out.println("   Total Combinations: " + comb1.size() + " (C(4,2) = 6)");
        System.out.println("   Combinations = " + comb1);
        System.out.println("-------------------------------------------------");

        // 2. Combination Sum I Test (LeetCode 39)
        int[] cand1 = {2, 3, 6, 7};
        int target1 = 7;
        List<List<Integer>> sum1 = master.combinationSum(cand1, target1);
        System.out.println("2. LeetCode 39 Combination Sum I (Re-usable Items) for Target " + target1 + ":");
        System.out.println("   Combinations = " + sum1 + " (Optimal = [[2,2,3], [7]])");
        System.out.println("-------------------------------------------------");

        // 3. Combination Sum II Test (LeetCode 40)
        int[] cand2 = {10, 1, 2, 7, 6, 1, 5};
        int target2 = 8;
        List<List<Integer>> sum2 = master.combinationSum2(cand2, target2);
        System.out.println("3. LeetCode 40 Combination Sum II (Single-use + Duplicate Pruning) for Target " + target2 + ":");
        System.out.println("   Combinations = " + sum2);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Combination Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Combinations (77)** | $\mathbf{O(\binom{N}{K})}$ Combinatorial⚡| $\mathbf{O(K)}$ Stack ⚡| Pruned `i <= n - (k - len) + 1` |
| **Comb Sum I (39)**   | $O(2^T)$ Exponential | $O(T)$ Stack Depth | Re-use item: pass `i` |
| **Comb Sum II (40)**  | $O(2^N)$ Exponential | $O(N)$ Stack Depth | Single-use: pass `i + 1` + Prune |

---

## 10. Edge Cases & Boundary Handling

1. **Target Sum Cannot Be Formed**:
   - Returns empty list `[]`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Confusing Duplicate Pruning Guard in Combinations (`i > startIndex`) with Permutations (`!visited[i-1]`)**:
  - In Combinations, there is no `visited[]` array! The duplicate guard MUST check `if (i > startIndex && nums[i] == nums[i-1]) continue;`. Do NOT use `!visited[i-1]` in Combinations!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Combination Sum Item Re-use Rules:
> * **Combination Sum I (Infinite Re-use)**: Pass `startIndex = i` to allow the current candidate to be chosen again.
> * **Combination Sum II (Single-use)**: Pass `startIndex = i + 1` to advance to the next candidate. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Combination Sum I (LC 39) | Combination Sum II (LC 40) |
| :--- | :--- | :--- |
| **Item Re-use** | Infinite Re-use ($x_i \in \mathbb{Z}_{\ge 0}$) | Single Use ($x_i \in \{0, 1\}$) |
| **Next `startIndex`** | **Pass `i` ⚡** | **Pass `i + 1` ⚡** |
| **Duplicate Pruning** | Not Needed | **`i > startIndex && nums[i] == nums[i-1]` ⚡**|

---

## 14. How to Recognize This in Questions

* **"Find all unique combinations of numbers summing to target (re-use allowed)"** $\rightarrow$ LeetCode 39.
* **"Find all unique combinations of numbers summing to target (each item used once)"** $\rightarrow$ LeetCode 40.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Combination Sum I pass `i` as the next `startIndex` instead of `i + 1`?**  
  *A:* Passing `i` allows the recursive call to consider the exact same element again, enabling infinite re-use of candidate numbers.

* **Q: How does `i > startIndex` prune duplicate combinations in Combination Sum II?**  
  *A:* It ensures that identical values are only used once as a decision branch at any given recursion depth, preventing duplicate combination branches.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COMBINATIONS BACKTRACKING                             |
+-----------------------------------------------------------------------+
| • Combinations 77 : Loop i = startIndex .. n - (k - path.size()) + 1  |
| • Comb Sum I 39   : Infinite re-use -> Pass startIndex = i            |
| • Comb Sum II 40  : Single use -> Pass i + 1 + Skip if i > startIndex && nums[i] == nums[i-1]|
| • Comb Sum III 216: Size K, Sum N using digits 1..9                   |
| • Pruning Rule    : Break loop early if remainingTarget - nums[i] < 0 ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 77 (`Combinations`) with loop upper bound pruning.
- [ ] I can write LeetCode 39 (`Combination Sum I`) passing `startIndex = i`.
- [ ] I can write LeetCode 40 (`Combination Sum II`) with duplicate pruning `i > startIndex`.
- [ ] I can write LeetCode 216 (`Combination Sum III`).
- [ ] I can explain the difference between `i` and `i + 1` in recursive calls.
