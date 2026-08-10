# 03. Permutations: Ordered Sequences, Visited Arrays & Duplicate Pruning

## 1. Introduction
**Permutation Generation** is a fundamental backtracking paradigm that explores all ordered arrangements of $N$ distinct or non-distinct elements. Because element order matters in permutations (e.g. sequence $(1, 2, 3)$ is distinct from $(3, 2, 1)$), the state space tree for $N$ elements branches into $N!$ leaf solution nodes. Backtracking permutation algorithms operate under two structural variations: (1) **Permutations of Distinct Elements (LeetCode 46)**, solved via a `visited[]` boolean tracking array or in-place swapping in **$O(N \cdot N!)$ Time Complexity**, and (2) **Permutations with Duplicates (LeetCode 47)**, which requires sorting elements and applying the **Duplicate Pruning Invariant** (`if (i > 0 && nums[i] == nums[i-1] && !visited[i-1]) continue;`) to prevent duplicate permutation sequences from being generated.

> **Important:** Core Structural Invariants of Permutations Backtracking:
> 1. **Ordered Sequence Invariant**:
>    - Every candidate choice iteration starts from index $0$ (not `startIndex`), using a `visited[]` array to track elements already included in the current recursive path.
> 2. **Duplicate Pruning Invariant (LeetCode 47)**:
>    - For arrays containing duplicate values, sort the array first ($nums[0] \le nums[1] \le \dots$).
>    - Skip candidate element $i$ if it equals its predecessor AND its predecessor has NOT been visited in the current path:
>      $$\text{if } (i > 0 \text{ \&\& } nums[i] == nums[i-1] \text{ \&\& } !visited[i-1]) \quad \text{continue;}$$
>    - Why `!visited[i-1]`? This forces duplicate numbers to be processed in strict index order, eliminating duplicate permutation branches!
> 3. **In-Place Swap Permutation Strategy**:
>    - Swapping element `i` with `first` eliminates the need for an auxiliary `visited[]` array or `List<Integer>` allocations during traversal. ⚡

```
Permutations State Space Tree Topology (N = 3 Distinct Elements [1, 2, 3]):

                                [ Root [] ]
                    /                |                \
         [ Choice 1 ]           [ Choice 2 ]           [ Choice 3 ]
        /           \          /           \          /           \
  [1, 2]         [1, 3]      [2, 1]         [2, 3]      [3, 1]         [3, 2]
    │              │           │              │           │              │
 [1, 2, 3]      [1, 3, 2]   [2, 1, 3]      [2, 3, 1]   [3, 1, 2]      [3, 2, 1]

Generates N! = 3! = 6 Permutations in O(N * N!) Time! ⚡
```

---

## 2. Core Concepts & Permutation Strategy Matrix

### 2.1 Permutation Variants Comparison Matrix
```
Permutation Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Permutation Variant   | Input Elements    | Primary Mechanism | Duplicate Guard   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Distinct Elements (46)**| All Unique      | `visited[]` Array | None Needed       | **$O(N)$ Stack ⚡**|
| **In-Place Swap (46)**| All Unique        | `swap(i, first)`  | None Needed       | **$O(N)$ Stack ⚡**|
| **Duplicates (47)**   | Contains Dupes    | Sort + `visited[]`| `!visited[i-1]` ⚡ | **$O(N)$ Stack ⚡**|
| **Next Permutation (31)**| Any Array       | Lexicographical   | Narayana Pandita  | **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Permutations iterate from index 0 using visited[]; Duplicates require sorting + skipping if nums[i]==nums[i-1] && !visited[i-1]!"**

---

## 3. Characteristics & Duplicate Pruning Mathematical Proof

### 3.1 Mathematical Derivation of Duplicate Pruning (`!visited[i-1]`)
* Consider array $nums = [1_a, 1_b, 2]$ containing duplicate ones.
* Without duplicate pruning, naive backtracking generates $3! = 6$ permutations, including identical pairs: $(1_a, 1_b, 2)$ and $(1_b, 1_a, 2)$.
* **Goal**: Enforce that identical numbers are picked in strict relative index order (i.e. $1_a$ MUST be picked before $1_b$).
* **Case Analysis of `if (nums[i] == nums[i-1] && !visited[i-1]) continue;`**:
  - When evaluating $1_b$ at index $i=1$:
    If $1_a$ at index $i-1=0$ has NOT been visited (`!visited[0]`), it means we are attempting to start a new permutation position with $1_b$ BEFORE using $1_a$.
    Pruning this branch ensures $1_b$ is ONLY used when $1_a$ is already active in the current prefix path (`visited[0] == true`).
  - This eliminates all $1_b \dots 1_a$ permutations, leaving exactly $\frac{N!}{\prod (k_i!)}$ unique permutations! ⚡

---

## 4. Internal Working Mechanics: Next Permutation (LeetCode 31)

Tracing Narayana Pandita's $O(N)$ Lexicographical Next Permutation Algorithm for $nums = [1, 2, 4, 3, 1]$:

```
Step 1: Find largest index i such that nums[i] < nums[i+1] (First decreasing element from right):
        - Index i = 1 (nums[1] = 2 < nums[2] = 4).

Step 2: Find largest index j > i such that nums[j] > nums[i] (Smallest element > 2 to the right):
        - Index j = 3 (nums[3] = 3 > 2).

Step 3: Swap nums[i] and nums[j]:
        - Swap nums[1] (2) and nums[3] (3) ──► Array becomes [1, 3, 4, 2, 1].

Step 4: Reverse suffix from index i+1 to end:
        - Reverse subarray [4, 2, 1] at index 2..4 ──► Array becomes [1, 3, 1, 2, 4].

Next Lexicographical Permutation = [1, 3, 1, 2, 4] in O(N) Time and O(1) Space! ✅ ⚡
```

---

## 5. Visual Diagram: Duplicate Pruning Tree Pruning

```
Duplicate Pruning Tree Topology for [1_a, 1_b, 2]:

                               [ Root [] ]
                   /                |                \
        [ Choice 1_a ]      [ Choice 1_b ]           [ Choice 2 ]
       (visited[0]=true)   (visited[0]=false!)
             │                      │
       Valid Branch             PRUNED! ❌
             │             (!visited[i-1] Guard Triggered)
      [1_a, 1_b, 2] ⚡

Guarantees 1_a is always picked before 1_b, eliminating duplicate trees! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Permutations of Distinct Elements (LeetCode 46), Permutations with Duplicates (LeetCode 47), In-Place Swap Permutations, and Next Permutation (LeetCode 31).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Permutation Backtracking:
 * Visited Arrays, In-Place Swapping, Duplicate Pruning, and Next Permutation.
 */
public class PermutationsMaster {

    // =========================================================================
    // 1. LEETCODE 46: PERMUTATIONS OF DISTINCT ELEMENTS (O(N * N!) Time)
    // =========================================================================
    /**
     * Generates all permutations of an array of distinct integers.
     *
     * @param nums array of unique integers
     * @return list of all permutations
     */
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null || nums.length == 0) return results;

        boolean[] visited = new boolean[nums.length];
        List<Integer> currentPath = new ArrayList<>();
        permuteDFS(nums, visited, currentPath, results);
        return results;
    }

    private void permuteDFS(int[] nums, boolean[] visited, List<Integer> path, List<List<Integer>> results) {
        if (path.size() == nums.length) {
            results.add(new ArrayList<>(path)); // Deep copy! ⚡
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (visited[i]) continue; // Skip already used elements in current path!

            // Choose
            visited[i] = true;
            path.add(nums[i]);

            // Explore
            permuteDFS(nums, visited, path, results);

            // Unchoose (Backtrack!) ⚡
            path.remove(path.size() - 1);
            visited[i] = false;
        }
    }

    // =========================================================================
    // 2. LEETCODE 47: PERMUTATIONS WITH DUPLICATES (O(N * N!) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates all unique permutations for an array containing duplicate numbers.
     */
    public List<List<Integer>> permuteUnique(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null || nums.length == 0) return results;

        // Step 1: Sort array to group duplicates together! ⚡
        int[] sortedNums = nums.clone();
        Arrays.sort(sortedNums);

        boolean[] visited = new boolean[sortedNums.length];
        List<Integer> currentPath = new ArrayList<>();
        permuteUniqueDFS(sortedNums, visited, currentPath, results);
        return results;
    }

    private void permuteUniqueDFS(int[] nums, boolean[] visited, List<Integer> path, List<List<Integer>> results) {
        if (path.size() == nums.length) {
            results.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (visited[i]) continue;

            // DUPLICATE PRUNING INVARIANT LINE ⚡
            if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) continue;

            // Choose
            visited[i] = true;
            path.add(nums[i]);

            // Explore
            permuteUniqueDFS(nums, visited, path, results);

            // Unchoose
            path.remove(path.size() - 1);
            visited[i] = false;
        }
    }

    // =========================================================================
    // 3. LEETCODE 31: NEXT PERMUTATION (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Rearranges numbers into the lexicographically next greater permutation in-place.
     */
    public void nextPermutation(int[] nums) {
        if (nums == null || nums.length <= 1) return;

        int n = nums.length;
        int i = n - 2;

        // Step 1: Find first decreasing element from right
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            i--;
        }

        if (i >= 0) {
            // Step 2: Find element just larger than nums[i] from right
            int j = n - 1;
            while (nums[j] <= nums[i]) {
                j--;
            }
            // Step 3: Swap nums[i] and nums[j]
            swap(nums, i, j);
        }

        // Step 4: Reverse suffix from i + 1 to end
        reverse(nums, i + 1, n - 1);
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i]; nums[i] = nums[j]; nums[j] = temp;
    }

    private void reverse(int[] nums, int start, int end) {
        while (start < end) {
            swap(nums, start++, end--);
        }
    }
}
```

> **Quick Syntax:**
```java
// Duplicate Permutation Pruning Line
if (i > 0 && nums[i] == nums[i - 1] && !visited[i - 1]) continue;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 46 - Permutations**:
   - Distinct elements permutation benchmark ($O(N \cdot N!)$ time).

2. **LeetCode 47 - Permutations II**:
   - Duplicate numbers unique permutation benchmark using `!visited[i-1]`.

3. **LeetCode 31 - Next Permutation**:
   - In-place lexicographical permutation algorithm ($O(N)$ time, $O(1)$ space).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class PermutationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   PERMUTATION BACKTRACKING BENCHMARK DEMO       ");
        System.out.println("=================================================\n");

        PermutationsMaster master = new PermutationsMaster();

        // 1. Distinct Permutations Test (LeetCode 46)
        int[] nums1 = {1, 2, 3};
        List<List<Integer>> perm1 = master.permute(nums1);
        System.out.println("1. LeetCode 46 Permutations for [1, 2, 3]:");
        System.out.println("   Total Permutations: " + perm1.size() + " (3! = 6)");
        System.out.println("   Permutations = " + perm1);
        System.out.println("-------------------------------------------------");

        // 2. Duplicate Permutations Test (LeetCode 47)
        int[] nums2 = {1, 1, 2};
        List<List<Integer>> perm2 = master.permuteUnique(nums2);
        System.out.println("2. LeetCode 47 Unique Permutations for [1, 1, 2]:");
        System.out.println("   Total Unique Permutations: " + perm2.size() + " (3!/2! = 3)");
        System.out.println("   Permutations = " + perm2);
        System.out.println("-------------------------------------------------");

        // 3. Next Permutation Test (LeetCode 31)
        int[] nums3 = {1, 2, 4, 3, 1};
        System.out.println("3. LeetCode 31 Next Permutation for " + Arrays.toString(nums3) + ":");
        master.nextPermutation(nums3);
        System.out.println("   Next Permutation (In-Place O(N)): " + Arrays.toString(nums3));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Permutation Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Distinct Elements (46)**| $\mathbf{O(N \cdot N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack ⚡| `visited[]` array check |
| **Duplicates (47)**   | $\mathbf{O(N \cdot N!)}$ Factorial⚡| $\mathbf{O(N)}$ Stack ⚡| Sort + `!visited[i-1]` |
| **Next Permutation (31)**| $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Narayana Pandita algorithm |

---

## 10. Edge Cases & Boundary Handling

1. **Single Element Array (`nums = [1]`)**:
   - Returns `[[1]]` immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Sort Array Before Applying Duplicate Pruning in Permutations II**:
  - The duplicate pruning guard `nums[i] == nums[i-1]` relies strictly on duplicate elements being adjacent. Failing to call `Arrays.sort(nums)` allows duplicate permutations to leak through! **ALWAYS sort before duplicate pruning!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Permutations vs Combinations Iteration Rule:
> * **Permutations**: Loop starts from **index 0** (`for (int i = 0; i < n; i++)`) because element order matters, using `visited[]`.
> * **Combinations / Subsets**: Loop starts from **`startIndex`** (`for (int i = startIndex; i < n; i++)`) to prevent duplicate combinations! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Permutations (LC 46) | Combinations (LC 77) |
| :--- | :--- | :--- |
| **Order Sensitivity** | Order Matters ($(1,2) \neq (2,1)$) | Order Does Not Matter |
| **Loop Start Index** | **Starts at Index 0 ⚡** | Starts at `startIndex` |
| **Tracking Structure**| `boolean[] visited` Array | Index Pointer |

---

## 14. How to Recognize This in Questions

* **"Generate all permutations / arrangements of array"** $\rightarrow$ LeetCode 46 / 47.
* **"Find next lexicographical permutation in-place"** $\rightarrow$ LeetCode 31.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Permutation backtracking iterate from index 0 instead of `startIndex`?**  
  *A:* Because element position matters in permutations. Any unvisited element from anywhere in the array can fill the next position in the current sequence.

* **Q: How does `!visited[i-1]` eliminate duplicate permutations?**  
  *A:* By requiring that identical numbers are selected in strict left-to-right index order. It prunes attempts to start a new position with a duplicate number if its earlier duplicate twin is not currently active in the prefix path.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PERMUTATIONS BACKTRACKING                             |
+-----------------------------------------------------------------------+
| • Distinct 46  : Loop i = 0..N-1 with boolean[] visited tracking      |
| • Duplicates 47: Sort first + skip if nums[i]==nums[i-1] && !visited[i-1]|
| • Next Perm 31 : Find decreasing i -> swap with j > i -> reverse suffix|
| • Loop Rule    : Permutations start at 0; Combinations start at startIndex⚡|
| • Performance  : O(N * N!) Time | O(N) Stack Depth Memory ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 46 (`Permutations`) using `visited[]` array in Java.
- [ ] I can write LeetCode 47 (`Permutations II`) with duplicate pruning.
- [ ] I can write LeetCode 31 (`Next Permutation`) in $O(N)$ time and $O(1)$ space.
- [ ] I can explain why duplicate pruning requires `!visited[i-1]`.
- [ ] I can state why permutations iterate from index 0 while combinations iterate from `startIndex`.
