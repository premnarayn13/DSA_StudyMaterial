# 03. Subsets, Power Set & Duplicate Pruning Backtracking Engines

## 1. Introduction
The **Power Set** of a set $S$ is the set of all possible subsets of $S$, including the empty set $\emptyset$ and $S$ itself. Generating all $2^N$ subsets (e.g. **Subsets - LeetCode 78**) and handling duplicate elements without generating duplicate subset combinations (e.g. **Subsets II - LeetCode 90**) is the classic foundation of **Backtracking**. Backtracking explores subset combinations via an **Include / Exclude Decision Tree** in **$O(2^N \cdot N)$ Time** and **$O(N)$ Auxiliary Memory**.

> **Important:** Core Invariants of Subset Backtracking & Duplicate Pruning:
> 1. **Include / Exclude Decision Tree**: At index $i$, the algorithm branches into two decisions:
>    - Branch 1: Include element `nums[i]` in `currentSubset`, recurse to `i + 1`, then **BACKTRACK (Remove `nums[i]`)**.
>    - Branch 2: Exclude element `nums[i]` and proceed.
> 2. **Duplicate Pruning Invariant (LeetCode 90)**:
>    - Sort array `Arrays.sort(nums)` so identical elements are contiguous.
>    - Inside the backtracking loop: **`if (i > start && nums[i] == nums[i - 1]) continue;`**
>    - Skips duplicate choices at the SAME recursion depth level while allowing valid duplicate selections across different depth levels! ⚡

```
Subset Generation Decision Tree Topology for nums = [1, 2]:
                                    []
                             /              \
                     [1]                          []
                  /       \                    /      \
             [1, 2]       [1]                [2]       []

Total Subsets Generated = 2^2 = 4: {[], [1], [2], [1, 2]}! ⚡
```

---

## 2. Core Concepts & Subsets I vs Subsets II Architecture

### 2.1 Subset Backtracking Strategy Matrix
```
Subset Backtracking Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Subset Problem        | Pre-Condition     | Duplicate Pruning | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Subsets I (78)**    | Unique Elements   | None Required     | **$O(2^N \cdot N)$ ⚡**|
| **Subsets II (90)**   | Duplicate Elements| **`Arrays.sort()` + Skip Check ⚡**| **$O(2^N \cdot N)$ ⚡**|
| **Bitmask Iterative** | Bit Shifting      | Bitmask Matching  | **$O(2^N \cdot N)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Subsets II Pruning: Sort nums first! If (i > start && nums[i] == nums[i-1]) continue!"**

---

## 3. Characteristics & $O(2^N \cdot N)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(2^N \cdot N)$ Complexity
* A set of size $N$ has $2^N$ total subsets.
* The backtracking decision tree contains $2^N$ leaf nodes.
* Copying each generated subset of average size $N / 2$ into the result list takes $O(N)$ time.
* Total Time Complexity: $\mathbf{O(2^N \cdot N) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 90 (Subsets II with Duplicates) on Sorted Array `[1, 2, 2]`:

```
Init: result = [], current = [].

Call backtrack(start = 0):
- Add [] to result.
- Loop i = 0 (val 1): Push 1 -> current = [1]. Recurse backtrack(start = 1):
  - Add [1] to result.
  - Loop i = 1 (val 2): Push 2 -> current = [1, 2]. Recurse backtrack(start = 2):
    - Add [1, 2] to result.
    - Loop i = 2 (val 2): Push 2 -> current = [1, 2, 2]. Recurse backtrack(3):
      - Add [1, 2, 2] to result.
      - Pop 2 -> current = [1, 2].
    - Pop 2 -> current = [1].
  - Loop i = 2 (val 2): i > start (2 > 1) AND nums[2] == nums[1] (2 == 2) ---> SKIP DUPLICATE!
  - Pop 1 -> current = [].
- Loop i = 1 (val 2): Push 2 -> current = [2]. Recurse backtrack(2):
  - Add [2] to result.
  - Loop i = 2 (val 2): Push 2 -> current = [2, 2]. Recurse backtrack(3):
    - Add [2, 2] to result.
    - Pop 2 -> current = [2].
  - Pop 2 -> current = [].
- Loop i = 2 (val 2): i > 0 AND nums[2] == nums[1] ---> SKIP DUPLICATE!

Total Unique Subsets: [], [1], [1, 2], [1, 2, 2], [2], [2, 2] (6 unique subsets)! ✅
```

---

## 5. Visual Diagram
Duplicate Pruning Decision Tree Topography (LeetCode 90):

```
Level 0:                             []
                         /           |           \
Level 1:              [1]           [2]          [2] (Pruned! i > start && nums[i] == nums[i-1])
                    /     \          |
Level 2:       [1, 2]   [1, 2]      [2, 2]
                         (Pruned!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 78 (Subsets) and LeetCode 90 (Subsets II):

```java
import java.util.*;

// LeetCode 78 & 90: Subsets & Subsets II (Backtracking Master)
public class SubsetsMaster {

    // 1. LeetCode 78: Subsets I (Unique Elements) O(2^N * N) Time
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null) return result;

        backtrackSubsets(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrackSubsets(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current)); // Add deep copy of current subset

        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);                         // Step 1: Choose (Include element)
            backtrackSubsets(nums, i + 1, current, result); // Step 2: Recurse
            current.remove(current.size() - 1);           // Step 3: BACKTRACK (Undo choice)
        }
    }

    // 2. LeetCode 90: Subsets II (Duplicate Elements) O(2^N * N) Time
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null) return result;

        Arrays.sort(nums); // Mandatory step to group duplicates together!
        backtrackSubsetsWithDup(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrackSubsetsWithDup(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current)); // Add deep copy

        for (int i = start; i < nums.length; i++) {
            // Duplicate Pruning Guard: Skip duplicate choices at the SAME recursion depth
            if (i > start && nums[i] == nums[i - 1]) {
                continue;
            }

            current.add(nums[i]);                               // Choose
            backtrackSubsetsWithDup(nums, i + 1, current, result); // Recurse
            current.remove(current.size() - 1);                 // Backtrack
        }
    }
}
```

> **Quick Syntax:**
```java
// Subsets II Duplicate Pruning Line
if (i > start && nums[i] == nums[i - 1]) continue;
```

---

## 7. Concrete Problem Examples
* **LeetCode 78 - Subsets**: Primary unique subsets problem.
* **LeetCode 90 - Subsets II**: Primary duplicate pruning subsets problem.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 90 `subsetsWithDup`:

```java
public class SubsetsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 90 Subsets II Test ===");
        SubsetsMaster solver = new SubsetsMaster();

        int[] nums = {1, 2, 2};
        List<List<Integer>> result = solver.subsetsWithDup(nums);

        System.out.println("Unique Subsets of [1, 2, 2]:");
        for (List<Integer> subset : result) {
            System.out.println(subset);
        }
        // Output: [], [1], [1, 2], [1, 2, 2], [2], [2, 2] ✅
    }
}
```

---

## 9. Complexity Analysis

| Subset Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Subsets I (78)** | **$O(2^N \cdot N)$ Optimal ⚡**| **$O(N)$ Call Stack Memory**| Include/Exclude Decision Tree |
| **Subsets II (90)**| **$O(2^N \cdot N)$ Optimal ⚡**| **$O(N)$ Call Stack Memory**| `Arrays.sort()` + `i > start` check |

---

## 10. Edge Cases & Boundary Handling
* **Empty Array (`nums = []`)**: Returns `[[]]` (the empty set).
* **Array of All Identical Elements (`[2, 2, 2]`)**: Returns $N + 1$ unique subsets (`[], [2], [2,2], [2,2,2]`).

---

## 11. Common Mistakes & Anti-Patterns
* **Writing `i > 0` Instead of `i > start` for Duplicate Pruning**:
  - `i > 0` prunes duplicates globally across different recursion depths, preventing valid combinations like `[2, 2]`.
  - **ALWAYS check `i > start` to prune duplicates strictly within the SAME loop depth level**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `i > start` Is Mandatory for Duplicate Pruning:
> * `start` represents the beginning index of the current recursion depth level.
> * `i == start` is the FIRST time we choose an element value at this level.
> * `i > start` represents subsequent loop iterations at the SAME level. If `nums[i] == nums[i - 1]`, it means we are picking a duplicate value for the SAME position, which generates duplicate subset branches! ⚡

> **Memory Trick:** **"i > start checks duplicate choices at the SAME recursion level! i > 0 is wrong!"**

---

## 13. System & Implementation Comparisons

| Feature | Backtracking Subsets | Bitmask Iterative Subsets |
| :--- | :--- | :--- |
| **Duplicate Pruning** | **Clean `i > start` Check ⚡** | Complex Bitmask Deduplication |
| **Code Simplicity** | **High (~15 Lines) ⚡** | Moderate (Bit Shifting Loops) |
| **Time Complexity** | **$O(2^N \cdot N)$ Optimal ⚡**| **$O(2^N \cdot N)$ Optimal ⚡**|

---

## 14. How to Recognize This in Questions
* **"Generate all possible subsets or combinations of power set from array with duplicates"** $\rightarrow$ Subsets II (LeetCode 90).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is `Arrays.sort(nums)` mandatory for LeetCode 90?**  
  *A:* Because `nums[i] == nums[i - 1]` only detects duplicate values if identical elements are placed in adjacent contiguous indices.
* **Q: Why do we add a deep copy `new ArrayList<>(current)` to the result list?**  
  *A:* Because `current` is a mutable reference that is continuously modified during backtracking. Adding `current` directly would store empty lists when backtracking unwinds!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUBSETS & POWER SET BACKTRACKING                      |
+-----------------------------------------------------------------------+
| • Step 1: Add deep copy to result: result.add(new ArrayList<>(current))|
| • Step 2: Loop i = start to N-1:                                      |
|           if (i > start && nums[i] == nums[i-1]) continue; // Prune!  |
|           current.add(nums[i]); backtrack(i + 1); current.remove(...);|
| • Subsets II Constraint: MANDATORY Arrays.sort(nums) first!           |
| • Performance: O(2^N * N) Time | O(N) Call Stack Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 78 (`Subsets`) in Java using backtracking.
- [ ] I can write LeetCode 90 (`Subsets II`) with duplicate pruning.
- [ ] I know why `i > start` is used instead of `i > 0`.
- [ ] I know why `new ArrayList<>(current)` deep copy is mandatory.
- [ ] I can trace the subset decision tree step by step.
