# 04. Combinations, Permutations & Combination Sum Backtracking Engines

## 1. Introduction
**Combinations** (order does NOT matter: $[1, 2] \equiv [2, 1]$) and **Permutations** (order MATTERS: $[1, 2] \ne [2, 1]$) represent the two core combinatorial paradigms in computer science. Master problems like **Combinations (LeetCode 77)**, **Combination Sum (LeetCode 39)**, **Combination Sum II (LeetCode 40)**, **Permutations (LeetCode 46)**, and **Permutations II (LeetCode 47)** form the core framework of backtracking. Permutations explore $N!$ ordered arrangements in **$O(N! \cdot N)$ Time**, while Combinations explore $C(N, K)$ subsets in **$O(C(N, K) \cdot K)$ Time**.

> **Important:** The Core Invariants of Combinations vs Permutations:
> 1. **Combinations (`start` Index Invariant)**:
>    - Uses a `start` index parameter in the loop (`for (int i = start; i < N; i++)`).
>    - Passing `i + 1` (or `i` for unlimited re-use in LeetCode 39) prevents backwards choices, guaranteeing ordered combination sets without duplicates!
> 2. **Permutations (`boolean[] visited` Array Invariant)**:
>    - Loops from $0$ to $N-1$ at EVERY recursion level (`for (int i = 0; i < N; i++)`).
>    - Uses a `boolean[] visited` array to track used elements in the current permutation path!
> 3. **Permutations II Duplicate Pruning Invariant (LeetCode 47)**:
>    - **`if (visited[i] || (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1])) continue;`**
>    - Prunes duplicate permutations when the identical predecessor `nums[i - 1]` has NOT been visited in the current tree level! ⚡

```
Combinations vs Permutations Branching Topography:
Combinations (start index = 0):                 Permutations (visited array):
        []                                              []
     /   |   \                                      /   |   \
   [1]  [2]  [3]                                  [1]  [2]  [3]
   / \    |                                      / \   / \  / \
 [1,2][1,3][2,3]                               [1,2][1,3]... (All N! Orders!) ⚡
```

---

## 2. Core Concepts & Problem Pattern Strategy Matrix

### 2.1 Combinatorial Backtracking Strategy Matrix
```
Combinatorial Backtracking Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Loop Index        | Visited Array?    | Subproblem Parameter|
+-----------------------+-------------------+-------------------+-------------------+
| **Combinations (77)** | `i = start`       | NO                | `i + 1`           |
| **Comb Sum I (39)**   | `i = start`       | NO                | `i` (Reuse element)|
| **Comb Sum II (40)**  | `i = start`       | NO                | `i + 1` + Pruning |
| **Permutations (46)** | `i = 0`           | **YES (`visited`)⚡**| `visited[i] = true`|
| **Perm II (47)**      | `i = 0`           | **YES (`visited`)⚡**| Duplicate Check   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Combinations use start index (i+1)! Permutations loop i=0 with boolean[] visited!"**

---

## 3. Characteristics & $O(N! \cdot N)$ Time Complexity Proof

### 3.1 Mathematical Proof of Permutation Complexity $O(N! \cdot N)$
* For an array of size $N$, there are $N! = N \times (N-1) \times \dots \times 1$ total unique permutations.
* The permutation backtracking tree has $N!$ leaf nodes.
* Copying each generated permutation of size $N$ into the result list takes $O(N)$ time.
* Total Time Complexity: $\mathbf{O(N! \cdot N) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 47 (Permutations II with Duplicates) on Sorted Array `[1, 1, 2]`:

```
Init: visited = [F, F, F], current = [].

Level 0 DFS:
- Loop i = 0 (val 1): visited[0] = T, current = [1]. Recurse Level 1:
  - Loop i = 0: visited[0] is T -> Skip.
  - Loop i = 1 (val 1): i > 0 && nums[1] == nums[0] (1==1) && !visited[0] is FALSE (visited[0] is T!).
    - Push 1: visited[1] = T, current = [1, 1]. Recurse Level 2:
      - Loop i = 2 (val 2): Push 2 -> current = [1, 1, 2]. Add to result! Pop 2.
    - Pop 1: visited[1] = F, current = [1].
  - Loop i = 2 (val 2): Push 2 -> current = [1, 2]. Recurse Level 2:
    - Loop i = 1 (val 1): Push 1 -> current = [1, 2, 1]. Add to result! Pop 1.
  - Pop 2: visited[2] = F, current = [1].
- Pop 1: visited[0] = F, current = [].

- Loop i = 1 (val 1): i > 0 && nums[1] == nums[0] (1==1) && !visited[0] is TRUE (visited[0] is F!) ---> PRUNED! (Prevents duplicate permutations!)

Unique Permutations Generated: [1, 1, 2], [1, 2, 1], [2, 1, 1]! ✅ (O(N! * N) Time!)
```

---

## 5. Visual Diagram
Permutations II Duplicate Pruning Topography (LeetCode 47):

```
Level 0:                                  []
                     /                    |                    \
Level 1:          [1] (i=0)          [1] (i=1: PRUNED!)        [2] (i=2)
                /     \             (!visited[0] is True!)      /     \
Level 2:    [1, 1]   [1, 2]                                  [2, 1]  [2, 1]
                                                                      (Pruned!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 39 (Combination Sum), LeetCode 46 (Permutations), and LeetCode 47 (Permutations II):

```java
import java.util.*;

// LeetCode 39, 46, 47: Combinations & Permutations Master
public class CombPermMaster {

    // 1. LeetCode 39: Combination Sum O(2^T * T) Time
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        if (candidates == null) return result;

        Arrays.sort(candidates);
        backtrackCombSum(candidates, target, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrackCombSum(int[] candidates, int target, int start, List<Integer> current, List<List<Integer>> result) {
        if (target == 0) {
            result.add(new ArrayList<>(current)); // Target reached!
            return;
        }

        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > target) break; // Prune search branch (Sorted array optimization!)

            current.add(candidates[i]);
            backtrackCombSum(candidates, target - candidates[i], i, current, result); // Pass 'i' (Allow reuse of same element!)
            current.remove(current.size() - 1); // Backtrack
        }
    }

    // 2. LeetCode 46: Permutations I (Unique Elements) O(N! * N) Time
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null) return result;

        boolean[] visited = new boolean[nums.length];
        backtrackPermute(nums, visited, new ArrayList<>(), result);
        return result;
    }

    private void backtrackPermute(int[] nums, boolean[] visited, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (visited[i]) continue; // Skip already used elements in current path

            visited[i] = true;
            current.add(nums[i]);
            backtrackPermute(nums, visited, current, result);
            current.remove(current.size() - 1);
            visited[i] = false; // Backtrack
        }
    }

    // 3. LeetCode 47: Permutations II (Duplicate Elements) O(N! * N) Time
    public List<List<Integer>> permuteUnique(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null) return result;

        Arrays.sort(nums); // Mandatory sorting to group duplicate values!
        boolean[] visited = new boolean[nums.length];
        backtrackPermuteUnique(nums, visited, new ArrayList<>(), result);
        return result;
    }

    private void backtrackPermuteUnique(int[] nums, boolean[] visited, List<Integer> current, List<List<Integer>> result) {
        if (current.size() == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (visited[i]) continue;

            // Permutations II Pruning Condition:
            // Skip duplicate choice if identical predecessor nums[i-1] was NOT visited in current level!
            if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) {
                continue;
            }

            visited[i] = true;
            current.add(nums[i]);
            backtrackPermuteUnique(nums, visited, current, result);
            current.remove(current.size() - 1);
            visited[i] = false;
        }
    }
}
```

> **Quick Syntax:**
```java
// Permutations II Pruning Line
if (visited[i] || (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1])) continue;
```

---

## 7. Concrete Problem Examples
* **LeetCode 39 - Combination Sum**: Element reuse allowed.
* **LeetCode 40 - Combination Sum II**: Unique elements with duplicates.
* **LeetCode 46 / 47 - Permutations I & II**: Ordered permutations.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 47 `permuteUnique`:

```java
public class CombPermDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 47 Permutations II Test ===");
        CombPermMaster solver = new CombPermMaster();

        int[] nums = {1, 1, 2};
        List<List<Integer>> result = solver.permuteUnique(nums);

        System.out.println("Unique Permutations of [1, 1, 2]:");
        for (List<Integer> perm : result) {
            System.out.println(perm);
        }
        // Output: [1, 1, 2], [1, 2, 1], [2, 1, 1] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Combination Sum (39)**| **$O(2^T \cdot T)$ Exponential**| **$O(T)$ Stack Memory**| Subproblem parameter `i` reuse |
| **Permutations I (46)** | **$O(N! \cdot N)$ Factorial ⚡**| **$O(N)$ Visited & Stack**| Loop $i=0$ with `boolean[] visited`|
| **Permutations II (47)**| **$O(N! \cdot N)$ Factorial ⚡**| **$O(N)$ Visited & Stack**| `i > 0 && !visited[i-1]` check |

---

## 10. Edge Cases & Boundary Handling
* **$N = 1$ Single Element**: Returns single list `[[nums[0]]]`.
* **Combination Target Cannot Be Formed**: Returns empty result `[]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `visited[i - 1]` Instead of `!visited[i - 1]` for Permutations II Pruning**:
  - Writing `visited[i - 1]` prunes valid vertical depth paths instead of pruning duplicate horizontal breadth choices.
  - **ALWAYS check `!visited[i - 1]` to prune duplicate choices at the SAME tree level**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `!visited[i - 1]` Prunes Duplicate Permutations Horizontally:
> When `nums[i] == nums[i - 1]`, if `visited[i - 1] == false`, it means `nums[i - 1]` was ALREADY processed and backtracked at the current recursion level.
> Choosing `nums[i]` now would duplicate the exact subtree already generated by `nums[i - 1]`!
> Skips this duplicate choice immediately! ⚡

> **Memory Trick:** **"Permutations II: Check (!visited[i-1]) to prune horizontal duplicates!"**

---

## 13. System & Implementation Comparisons

| Feature | Combinations Backtracking | Permutations Backtracking |
| :--- | :--- | :--- |
| **Loop Start Index** | **`for (int i = start; ...)` ⚡** | `for (int i = 0; ...)` |
| **Visited Guard** | Not Needed (Forward Index) | **`boolean[] visited` Required ⚡** |
| **Total Outputs** | $C(N, K)$ Subsets | $N!$ Ordered Arrangements |

---

## 14. How to Recognize This in Questions
* **"Generate all unique ordered arrangements of array with duplicates"** $\rightarrow$ Permutations II (LeetCode 47).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the main difference in implementation between combinations and permutations?**  
  *A:* Combinations use a `start` index parameter in the loop (`i = start`) to prevent backward choices. Permutations loop from `0` to `N-1` at every level and use a `boolean[] visited` array.
* **Q: Why does LeetCode 39 (Combination Sum) pass `i` to the recursive call instead of `i + 1`?**  
  *A:* Passing `i` allows the algorithm to reuse the current element `candidates[i]` an unlimited number of times.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: COMBINATIONS & PERMUTATIONS                           |
+-----------------------------------------------------------------------+
| • Combinations (39): for (i = start...N-1) -> Recurse with i or i+1   |
| • Permutations (46): for (i = 0...N-1) -> if (visited[i]) continue;   |
| • Permutations (47): Arrays.sort(nums);                               |
|   if (visited[i] || (i > 0 && nums[i] == nums[i-1] && !visited[i-1])) continue;|
| • Performance       : Permutations O(N! * N) | Combinations O(C(N,K)*K)⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 39 (`Combination Sum`) in Java.
- [ ] I can write LeetCode 46 (`Permutations I`).
- [ ] I can write LeetCode 47 (`Permutations II`) with duplicate pruning.
- [ ] I know why `!visited[i - 1]` is used for horizontal pruning.
- [ ] I can trace permutation decision trees step by step.
