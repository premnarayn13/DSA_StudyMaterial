# 05. Subsets: Power Sets, Cascading Trees & Duplicate Pruning Invariants

## 1. Introduction
The **Subsets Pattern** (Power Set Generation) is a foundational backtracking paradigm where the objective is to generate all $2^N$ possible subset combinations of a given array $S$ containing $N$ elements. Unlike Permutations (where element position matters) or Combinations of fixed size $K$, Subsets captures **EVERY NODE in the State Space Tree** as a valid solution candidate. Subsets backtracking executes under two major variations: (1) **Subsets of Distinct Elements (LeetCode 78)**, solved via Cascading Tree Traversal or Bitmask Generation in **$O(N \cdot 2^N)$ Time Complexity** and **$O(N)$ Auxiliary Space**, and (2) **Subsets with Duplicates (LeetCode 90)**, which requires sorting elements and applying the **Duplicate Pruning Invariant** (`if (i > startIndex && nums[i] == nums[i-1]) continue;`) to prevent generating identical subset combinations.

> **Important:** Core Structural Invariants of Subsets Backtracking:
> 1. **Every Node Solution Capture**:
>    - Unlike fixed-depth search trees that capture solutions only at leaf nodes (`path.size() == K`), Subsets captures a deep copy of `path` at EVERY decision node (`results.add(new ArrayList<>(path))`).
> 2. **Forward Indexing Invariant (`startIndex`)**:
>    - Recursive calls pass `startIndex = i + 1` to ensure elements are processed in strict ascending index order, preventing duplicate permutation subsets.
> 3. **Subsets II Duplicate Pruning Invariant (LeetCode 90)**:
>    - Sort the array first ($nums[0] \le nums[1] \le \dots$).
>    - Skip candidate $i$ if it equals its predecessor AND is NOT the first choice at the current decision level:
>      $$\text{if } (i > startIndex \text{ \&\& } nums[i] == nums[i-1]) \quad \text{continue;}$$
> 4. **Bitmask Iteration Alternative ($0 \dots 2^N - 1$)**:
>    - Iterates integers `mask` from $0$ to $2^N - 1$. Bit $i$ set (`(mask & (1 << i)) != 0`) includes element $i$ in the subset. ⚡

```
Subsets State Space Tree Topology (N = 3 Elements [1, 2, 3]):

                               [ Node 0: Root [] ] (Captured! ✅)
                    /                   |                   \
         [ Node 1: [1] ] (✅)    [ Node 2: [2] ] (✅)    [ Node 3: [3] ] (✅)
          /           \                 |
   [1, 2] (✅)     [1, 3] (✅)      [2, 3] (✅)
      │
  [1, 2, 3] (✅)

Captures all 2^3 = 8 Nodes in State Space Tree as valid subsets! ⚡
```

---

## 2. Core Concepts & Subsets Strategy Matrix

### 2.1 Subsets Strategy Matrix
```
Subsets Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Subsets Variation     | Input Elements    | Primary Engine    | Duplicate Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Subsets I (LC 78)** | All Unique        | Cascading DFS Tree| None Needed       | **$O(N \cdot 2^N)$ ⚡**|
| **Bitmask Subsets (78)**| All Unique      | Integer $0..2^N-1$| Bitwise Bit Check | **$O(N \cdot 2^N)$ ⚡**|
| **Subsets II (LC 90)**| Contains Dupes    | Sort + Cascading  | **`i > startIndex` ⚡**| **$O(N \cdot 2^N)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Subsets captures results.add(path) at EVERY node; Subsets II sorts + skips if (i > startIndex && nums[i] == nums[i-1])!"**

---

## 3. Characteristics & Subsets II Duplicate Pruning Proof

### 3.1 Mathematical Derivation of Subsets II Duplicate Pruning (LeetCode 90)
* Consider sorted candidate array $nums = [1, 2_a, 2_b]$. Total unpruned subsets $= 2^3 = 8$.
* Unpruned subsets include duplicate pairs: $[1, 2_a]$ and $[1, 2_b]$.
* **Goal**: Guarantee that duplicate elements are selected in strict relative index order (i.e. $2_b$ is ONLY selected if $2_a$ was selected at the preceding decision level).
* **Proof of `if (i > startIndex && nums[i] == nums[i-1]) continue;`**:
  - At any decision depth $D$, `startIndex` is the first candidate element considered.
  - When $i = startIndex$: Element $nums[i] = 2_a$ is evaluated as a candidate branch at level $D$.
  - When $i = startIndex + 1$: Candidate element is $nums[i] = 2_b$. Since $2_b == 2_a$ AND $i > startIndex$, $2_b$ is attempting to start a brand new branch at level $D$ with value $2$ a SECOND time.
  - Skipping $2_b$ when $i > startIndex$ prunes duplicate branch creation at level $D$, producing exactly the unique power set! ⚡

---

## 4. Internal Working Mechanics: Bitmask vs Recursive Subsets

Tracing Power Set Generation for $nums = [10, 20, 30]$ ($N = 3$):

```
Bitmask Iteration Method (0 to 2^3 - 1 = 7):

mask = 0 (000_2): Subset = []
mask = 1 (001_2): Bit 0 set -> Subset = [10]
mask = 2 (010_2): Bit 1 set -> Subset = [20]
mask = 3 (011_2): Bits 0,1 set -> Subset = [10, 20]
mask = 4 (100_2): Bit 2 set -> Subset = [30]
mask = 5 (101_2): Bits 0,2 set -> Subset = [10, 30]
mask = 6 (110_2): Bits 1,2 set -> Subset = [20, 30]
mask = 7 (111_2): Bits 0,1,2 set -> Subset = [10, 20, 30]

Generates all 8 subsets in O(N * 2^N) Time and O(1) Auxiliary Space! ✅ ⚡
```

---

## 5. Visual Diagram: Subsets II Duplicate Tree Pruning

```
Subsets II Duplicate Pruning Tree (nums = [1, 2_a, 2_b]):

                                  [ Root [] ] (Captured!)
                     /                 |                 \
            [ Choice 1 ]          [ Choice 2_a ]        [ Choice 2_b ]
          (i = startIndex)      (i = startIndex)      (i > startIndex!)
                │                      │                      │
            [1] (✅)                [2_a] (✅)              PRUNED! ❌
           /       \                   │             (nums[i]==nums[i-1])
      [1, 2_a]   [1, 2_b]           [2_a, 2_b] (✅)
       (✅)       (PRUNED! ❌)

Eliminates duplicate subsets seamlessly! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Subsets I (LeetCode 78), Subsets II with Duplicates (LeetCode 90), and Bitmask Power Set Generation.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Subsets Backtracking:
 * Cascading State Trees, Bitmask Power Sets, and Duplicate Pruning.
 */
public class SubsetsMaster {

    // =========================================================================
    // 1. LEETCODE 78: SUBSETS OF DISTINCT ELEMENTS (O(N * 2^N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates all unique subsets of an array of distinct integers.
     *
     * @param nums array of unique integers
     * @return power set list
     */
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null) return results;

        List<Integer> path = new ArrayList<>();
        subsetsDFS(nums, 0, path, results);
        return results;
    }

    private void subsetsDFS(int[] nums, int startIndex, List<Integer> path, List<List<Integer>> results) {
        // EVERY NODE IS A VALID SUBSET SOLUTION! ⚡
        results.add(new ArrayList<>(path));

        for (int i = startIndex; i < nums.length; i++) {
            // Choose
            path.add(nums[i]);

            // Explore
            subsetsDFS(nums, i + 1, path, results);

            // Unchoose (Backtrack!) ⚡
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 2. LEETCODE 90: SUBSETS II WITH DUPLICATES (O(N * 2^N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates all unique subsets for an array containing duplicate numbers.
     */
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null) return results;

        // Step 1: Sort array to group duplicate numbers together! ⚡
        int[] sortedNums = nums.clone();
        Arrays.sort(sortedNums);

        List<Integer> path = new ArrayList<>();
        subsetsWithDupDFS(sortedNums, 0, path, results);
        return results;
    }

    private void subsetsWithDupDFS(int[] nums, int startIndex, List<Integer> path, List<List<Integer>> results) {
        results.add(new ArrayList<>(path)); // Capture node

        for (int i = startIndex; i < nums.length; i++) {
            // SUBSETS II DUPLICATE PRUNING INVARIANT LINE ⚡
            if (i > startIndex && nums[i] == nums[i - 1]) continue;

            // Choose
            path.add(nums[i]);

            // Explore
            subsetsWithDupDFS(nums, i + 1, path, results);

            // Unchoose
            path.remove(path.size() - 1);
        }
    }

    // =========================================================================
    // 3. BITMASK POWER SET GENERATOR (O(N * 2^N) Time, O(1) Auxiliary Space)
    // =========================================================================
    /**
     * Generates Power Set using Bitmask Iteration.
     */
    public List<List<Integer>> subsetsBitmask(int[] nums) {
        List<List<Integer>> results = new ArrayList<>();
        if (nums == null) return results;

        int n = nums.length;
        int totalSubsets = 1 << n; // 2^N subsets

        for (int mask = 0; mask < totalSubsets; mask++) {
            List<Integer> subset = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) {
                    subset.add(nums[i]);
                }
            }
            results.add(subset);
        }

        return results;
    }
}
```

> **Quick Syntax:**
```java
// Subsets II Duplicate Pruning Line
if (i > startIndex && nums[i] == nums[i - 1]) continue;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 78 - Subsets**:
   - Power set generation benchmark ($O(N \cdot 2^N)$ time).

2. **LeetCode 90 - Subsets II**:
   - Duplicate numbers unique subset benchmark using `i > startIndex` guard.

3. **Bitmask Power Set Generation**:
   - Iterative bitmask subset generator in $O(1)$ auxiliary space.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class SubsetsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SUBSETS BACKTRACKING BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        SubsetsMaster master = new SubsetsMaster();

        // 1. Subsets I Test (LeetCode 78)
        int[] nums1 = {1, 2, 3};
        List<List<Integer>> sub1 = master.subsets(nums1);
        System.out.println("1. LeetCode 78 Subsets I for [1, 2, 3]:");
        System.out.println("   Total Subsets: " + sub1.size() + " (2^3 = 8)");
        System.out.println("   Subsets = " + sub1);
        System.out.println("-------------------------------------------------");

        // 2. Subsets II Test (LeetCode 90)
        int[] nums2 = {1, 2, 2};
        List<List<Integer>> sub2 = master.subsetsWithDup(nums2);
        System.out.println("2. LeetCode 90 Subsets II (Duplicates) for [1, 2, 2]:");
        System.out.println("   Total Unique Subsets: " + sub2.size() + " Subsets");
        System.out.println("   Subsets = " + sub2);
        System.out.println("-------------------------------------------------");

        // 3. Bitmask Power Set Test
        List<List<Integer>> bitSub = master.subsetsBitmask(nums1);
        System.out.println("3. Bitmask Power Set Generator for [1, 2, 3]:");
        System.out.println("   Total Subsets (Bitmask): " + bitSub.size() + " Subsets");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Subsets Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Subsets I (LC 78)** | $\mathbf{O(N \cdot 2^N)}$ Exponential⚡| $\mathbf{O(N)}$ Stack ⚡| $2^N$ total subsets |
| **Subsets II (LC 90)**| $\mathbf{O(N \cdot 2^N)}$ Exponential⚡| $\mathbf{O(N)}$ Stack ⚡| Sort + `i > startIndex` |
| **Bitmask Subsets**   | $\mathbf{O(N \cdot 2^N)}$ Exponential⚡| $\mathbf{O(1)}$ Memory ⚡| Bitwise bit check |

---

## 10. Edge Cases & Boundary Handling

1. **Empty Array Input (`nums = []`)**:
   - Returns `[[]]` (single empty subset `[]`).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Checking Base Case Depth Criteria in Subsets I**:
  - Adding a condition like `if (path.size() == K) return;` restricts output to fixed-size combinations instead of generating all $2^N$ subsets. Subsets MUST capture `results.add(new ArrayList<>(path))` at EVERY node!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Subsets vs Combinations Solution Capture Rule:
> * **Subsets**: Capture result at **EVERY node** (`results.add(...)` placed OUTSIDE loop).
> * **Combinations**: Capture result ONLY when `path.size() == K`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Subsets I (LC 78) | Subsets II (LC 90) |
| :--- | :--- | :--- |
| **Input Constraint** | All Unique Elements | Contains Duplicate Elements |
| **Array Sorting** | Not Required | **MUST Sort First (`Arrays.sort`) ⚡** |
| **Duplicate Guard** | None | **`i > startIndex && nums[i] == nums[i-1]` ⚡**|

---

## 14. How to Recognize This in Questions

* **"Generate all subsets / power set of array"** $\rightarrow$ LeetCode 78 / 90.
* **"Find all unique subset combinations when duplicates are present"** $\rightarrow$ LeetCode 90.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Subsets capture solutions at every node instead of just leaf nodes?**  
  *A:* Because every prefix path in the state space tree represents a valid subset of the input array (from empty set `[]` to full array).

* **Q: How does `i > startIndex` prune duplicate subsets in Subsets II?**  
  *A:* It ensures that duplicate numbers are used at most ONCE as a branching candidate at any given recursion depth, preventing duplicate subset subtrees.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUBSETS BACKTRACKING                                  |
+-----------------------------------------------------------------------+
| • Subsets I 78 : results.add(new ArrayList<>(path)) at EVERY node     |
| • Subsets II 90: Sort first + skip if (i > startIndex && nums[i] == nums[i-1])|
| • Bitmask Set  : Iterate mask 0..2^N-1 -> (mask & (1<<i)) != 0        |
| • Loop Rule    : for (int i = startIndex; i < n; i++)                 |
| • Performance  : O(N * 2^N) Time | O(N) Stack Depth Memory ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 78 (`Subsets`) in Java.
- [ ] I can write LeetCode 90 (`Subsets II`) with duplicate pruning.
- [ ] I can write the Bitmask Power Set Generator in $O(1)$ auxiliary space.
- [ ] I can explain why Subsets captures solutions at every node.
- [ ] I can state why array sorting is required for Subsets II.
