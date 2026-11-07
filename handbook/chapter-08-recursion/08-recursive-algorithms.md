# 08. Core Recursive Algorithms: Binary Search, Merge Sort, Quick Sort & DFS

## 1. Introduction
**Core Recursive Algorithms** form the primary computational engine of fundamental computer science workflows. Rather than treating recursion as a standalone syntax trick, standard algorithms leverage recursive Divide and Conquer and Depth-First Search (DFS) frameworks to achieve optimal time bounds across searching, sorting, tree parsing, and graph exploration. Benchmark algorithms including **Recursive Binary Search ($O(\log N)$)**, **Recursive Merge Sort ($O(N \log N)$)**, **Recursive Quick Sort ($O(N \log N)$ average)**, and **Recursive Tree/Graph DFS ($O(V + E)$)** demonstrate how precise base case guards and subproblem partitioning operate in high-throughput Java production code.

> **Important:** Core Recursive Algorithm Framework Invariants:
> 1. **Recursive Binary Search**: State = `(arr, target, low, high)`. Halves search interval by comparing `target` with `mid = low + (high - low) / 2`.
> 2. **Recursive Merge Sort**: State = `(arr, left, right)`. Divides array into halves, recursively sorts both halves, and merges sorted halves using an auxiliary array in $O(N \log N)$ time.
> 3. **Recursive Quick Sort**: State = `(arr, low, high)`. Partitions array around a pivot element $P$ such that elements $\le P$ are on the left and $> P$ are on the right, then recurses on both partitions.
> 4. **Recursive DFS (Trees/Graphs)**: State = `(node, visited/result)`. Recurses deep down child branches before backtracking. ⚡

```
Divide and Conquer Array Partitioning Topology (Merge Sort):
Level 0:                    [ 38, 27, 43, 3, 9, 82, 10 ]
                                 /                  \
Level 1:              [ 38, 27, 43, 3 ]         [ 9, 82, 10 ]
                         /         \               /       \
Level 2:           [ 38, 27 ]    [ 43, 3 ]     [ 9, 82 ]   [ 10 ]
                      /    \      /    \        /    \       |
Level 3:           [38]   [27]  [43]   [3]    [9]   [82]   [10] (Base Cases!)

Bottom-Up Unwinding: Merges sorted sub-arrays back up the call stack! ⚡
```

---

## 2. Core Concepts & Core Recursive Algorithms Strategy Matrix

### 2.1 Core Algorithm Strategy Matrix
```
Core Recursive Algorithms Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Recursive Algorithm   | Primary Paradigm  | Base Case Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Binary Search**     | Interval Halving  | `low > high`      | **$O(\log N)$ Log ⚡**|
| **Merge Sort**        | Divide & Conquer  | `left >= right`   | **$O(N \log N)$ Strict ⚡**|
| **Quick Sort**        | Partition & Conquer| `low >= high`     | **$O(N \log N)$ Avg / $O(N^2)$ Worst**|
| **Tree/Graph DFS**    | Deep Exploration  | `node == null`    | **$O(V + E)$ Linear ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Binary Search halves interval O(log N); Merge Sort merges sorted halves O(N log N); Quick Sort partitions around pivot!"**

---

## 3. Characteristics & $O(N \log N)$ Merge Sort Time Complexity Proof

### 3.1 Mathematical Proof of Merge Sort $O(N \log N)$ Time
* Recurrence Relation: $T(N) = 2 T(N/2) + O(N)$, with base case $T(1) = 0$.
* Tree Height $H = \log_2 N$.
* Work per level: $2^l \times \left(\frac{N}{2^l}\right) = N$ for every level $l \in [0 \dots \log_2 N]$.
* Total Work: $T(N) = N \times (\log_2 N + 1) = \mathbf{O(N \log N) \text{ Strict Time Complexity}}$ across Best, Average, and Worst cases! ⚡

---

## 4. Internal Working Mechanics: Quick Sort Lomuto Partitioning

Tracing Quick Sort Lomuto Partitioning on Array `[3, 8, 2, 5, 1, 4]` (`low = 0, high = 5`, Pivot = `arr[high] = 4`):

```
Init: pivot = 4, partitionIndex i = low - 1 = -1.

Loop j = 0 to 4 (high - 1):
- j = 0 (val 3): 3 <= 4 -> i++ (0). Swap arr[0] and arr[0] (3 <-> 3). Array: [3, 8, 2, 5, 1, 4].
- j = 1 (val 8): 8 > 4  -> Skip.
- j = 2 (val 2): 2 <= 4 -> i++ (1). Swap arr[1] and arr[2] (8 <-> 2). Array: [3, 2, 8, 5, 1, 4].
- j = 3 (val 5): 5 > 4  -> Skip.
- j = 4 (val 1): 1 <= 4 -> i++ (2). Swap arr[2] and arr[4] (8 <-> 1). Array: [3, 2, 1, 5, 8, 4].

End Loop: Swap pivot arr[high] (4) with arr[i + 1] (arr[3] = 5).
Final Partitioned Array: [3, 2, 1, 4, 8, 5]!

Pivot 4 is at correct index 3! Left part [3, 2, 1] <= 4, Right part [8, 5] > 4! ✅
```

---

## 5. Visual Diagram: Quick Sort vs. Merge Sort Subproblem Partitioning

```
1. Merge Sort (Divide Top-Down, Sort Bottom-Up):
Divide Phase:    [ 4, 2, 1, 3 ]
                 /            \
            [ 4, 2 ]        [ 1, 3 ]
             /    \          /    \
           [4]    [2]      [1]    [3]  <-- Base Cases Met!
Merge Phase: [ 2, 4 ]        [ 1, 3 ]
                 \            /
                [ 1, 2, 3, 4 ]  <-- Sorted Array! ⚡

2. Quick Sort (Partition Top-Down, In-Place):
Partition 1:    [ 3, 2, 1, 4, 8, 5 ] (Pivot 4 placed at index 3)
                    /             \
Recurse:   [ 3, 2, 1 ]           [ 8, 5 ]
           (Pivot 1)             (Pivot 5)
               /                     \
          [ 3, 2 ]                 [ 8 ]
           (Pivot 2) -> Sorted! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Recursive Binary Search, Recursive Merge Sort, Recursive Quick Sort, and Binary Tree DFS traversals.

```java
import java.util.*;

/**
 * Production-Grade Suite Implementing Core Recursive Algorithms:
 * Binary Search, Merge Sort, Quick Sort, and Binary Tree DFS Traversals.
 */
public class RecursiveAlgorithmsMaster {

    // =========================================================================
    // 1. RECURSIVE BINARY SEARCH (O(log N) Time, O(log N) Stack Space)
    // =========================================================================
    /**
     * Solves binary search recursively over a sorted array.
     *
     * @param arr sorted integer array
     * @param target search target
     * @return index of target or -1 if absent
     */
    public int binarySearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;
        return binarySearchHelper(arr, target, 0, arr.length - 1);
    }

    private int binarySearchHelper(int[] arr, int target, int low, int high) {
        // Base Case Guard: Target absent in search range
        if (low > high) {
            return -1;
        }

        int mid = low + (high - low) / 2; // Prevent 32-bit integer overflow!

        if (arr[mid] == target) {
            return mid; // Target found!
        } else if (arr[mid] > target) {
            return binarySearchHelper(arr, target, low, mid - 1); // Search left half
        } else {
            return binarySearchHelper(arr, target, mid + 1, high); // Search right half
        }
    }

    // =========================================================================
    // 2. RECURSIVE MERGE SORT (O(N log N) Time, O(N) Auxiliary Memory)
    // =========================================================================
    /**
     * Sorts an array using recursive Merge Sort.
     *
     * @param arr input array
     */
    public void mergeSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        mergeSortHelper(arr, 0, arr.length - 1);
    }

    private void mergeSortHelper(int[] arr, int left, int right) {
        // Base Case Guard
        if (left >= right) return;

        int mid = left + (right - left) / 2;

        // Step 1: Divide & Recurse on both halves
        mergeSortHelper(arr, left, mid);
        mergeSortHelper(arr, mid + 1, right);

        // Step 2: Merge sorted halves
        merge(arr, left, mid, right);
    }

    private void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }

        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        System.arraycopy(temp, 0, arr, left, temp.length);
    }

    // =========================================================================
    // 3. RECURSIVE QUICK SORT (O(N log N) Avg Time, O(log N) Stack Space)
    // =========================================================================
    /**
     * Sorts an array using recursive Quick Sort with Lomuto partitioning.
     *
     * @param arr input array
     */
    public void quickSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        quickSortHelper(arr, 0, arr.length - 1);
    }

    private void quickSortHelper(int[] arr, int low, int high) {
        // Base Case Guard
        if (low >= high) return;

        // Step 1: Partition array around pivot
        int pivotIndex = partition(arr, low, high);

        // Step 2: Recurse on sub-partitions
        quickSortHelper(arr, low, pivotIndex - 1);
        quickSortHelper(arr, pivotIndex + 1, high);
    }

    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high]; // Select last element as pivot
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1; // Return correct final index of pivot
    }

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // =========================================================================
    // 4. RECURSIVE BINARY TREE DFS TRAVERSAL
    // =========================================================================
    public static class TreeNode {
        public int val;
        public TreeNode left, right;
        public TreeNode(int val) { this.val = val; }
    }

    /**
     * In-order DFS traversal (Left, Root, Right).
     */
    public List<Integer> inorderDFS(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }

    private void inorderHelper(TreeNode node, List<Integer> result) {
        if (node == null) return; // Base Case Guard
        inorderHelper(node.left, result);  // Recurse Left
        result.add(node.val);             // Process Root
        inorderHelper(node.right, result); // Recurse Right
    }
}
```

> **Quick Syntax:**
```java
// Mid Calculation Line (Overflow Safe)
int mid = low + (high - low) / 2;
```

---

## 7. Concrete Problem Examples & Applications

1. **Searching Systems**:
   - Binary Search over Sorted Arrays ($O(\log N)$).
   - Peak Element Search in Monotonic Sequences.

2. **Sorting Engines**:
   - Merge Sort: Stable sorting for External Storage / Linked Lists.
   - Quick Sort: High-speed in-place array sorting (standard `Arrays.sort()`).

3. **Hierarchical Parsing**:
   - Binary Tree In-Order / Pre-Order / Post-Order DFS.
   - Expression Tree Parsing and Evaluation.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class RecursiveAlgorithmsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    CORE RECURSIVE ALGORITHMS DEMONSTRATION      ");
        System.out.println("=================================================\n");

        RecursiveAlgorithmsMaster master = new RecursiveAlgorithmsMaster();

        // 1. Recursive Binary Search Test
        int[] sortedArr = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
        int target = 23;
        int searchIdx = master.binarySearch(sortedArr, target);
        System.out.println("1. Binary Search Target " + target + " in " + Arrays.toString(sortedArr) + ":");
        System.out.println("   Target Index: " + searchIdx + " (Value = " + sortedArr[searchIdx] + ")");
        System.out.println("-------------------------------------------------");

        // 2. Recursive Merge Sort Test
        int[] arr1 = {38, 27, 43, 3, 9, 82, 10};
        System.out.println("2. Original Array for Merge Sort: " + Arrays.toString(arr1));
        master.mergeSort(arr1);
        System.out.println("   Sorted Array (Merge Sort)   : " + Arrays.toString(arr1));
        System.out.println("-------------------------------------------------");

        // 3. Recursive Quick Sort Test
        int[] arr2 = {3, 8, 2, 5, 1, 4};
        System.out.println("3. Original Array for Quick Sort: " + Arrays.toString(arr2));
        master.quickSort(arr2);
        System.out.println("   Sorted Array (Quick Sort)   : " + Arrays.toString(arr2));
        System.out.println("-------------------------------------------------");

        // 4. Binary Tree DFS In-Order Test
        RecursiveAlgorithmsMaster.TreeNode root = new RecursiveAlgorithmsMaster.TreeNode(4);
        root.left = new RecursiveAlgorithmsMaster.TreeNode(2);
        root.right = new RecursiveAlgorithmsMaster.TreeNode(5);
        root.left.left = new RecursiveAlgorithmsMaster.TreeNode(1);
        root.left.right = new RecursiveAlgorithmsMaster.TreeNode(3);

        List<Integer> inorder = master.inorderDFS(root);
        System.out.println("4. Binary Tree In-Order DFS Traversal: " + inorder);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Recursive Algorithm | Time Complexity (Best) | Time Complexity (Worst) | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Binary Search** | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Logarithmic | $\mathbf{O(\log N)}$ Stack | Interval Halving |
| **Merge Sort** | $\mathbf{O(N \log N)}$ | $\mathbf{O(N \log N)}$ Strict ⚡ | $\mathbf{O(N)}$ Aux Array | Stable Divide & Conquer |
| **Quick Sort** | $\mathbf{O(N \log N)}$ | $\mathbf{O(N^2)}$ (Sorted input)| $\mathbf{O(\log N)}$ Stack ⚡| In-Place Partitioning |
| **Tree DFS Traversal** | $\mathbf{O(V + E)}$ Linear | $\mathbf{O(V + E)}$ Linear | $\mathbf{O(H)}$ Tree Height | Deep Branch Visiting |

---

## 10. Edge Cases & Boundary Handling

1. **32-Bit Integer Overflow in `mid` Calculation**:
   - Writing `int mid = (low + high) / 2` causes integer overflow when `low + high > 2,147,483,647`.
   - **Fix**: ALWAYS use `int mid = low + (high - low) / 2`.

2. **Single Element or Empty Array**:
   - `left >= right` or `low >= high` base cases return immediately without array out-of-bounds errors.

3. **Quick Sort Worst Case on Already Sorted Array**:
   - Selecting last element as pivot on an already sorted array yields $O(N^2)$ time.
   - **Guard**: Randomize pivot selection (`swap(arr, low + rand % (high - low + 1), high)`).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Off-by-One Errors in Subproblem Boundaries**:
  - In Binary Search, calling `binarySearchHelper(arr, target, low, mid)` instead of `mid - 1` causes infinite recursive loops when `low == mid`.

* **Anti-Pattern 2: Allocating Temporary Merge Arrays Inside Recursive Helper**:
  - Allocating `new int[right - left + 1]` inside `merge()` creates thousands of short-lived heap objects. For maximum performance, allocate a single auxiliary array of size $N$ upfront and pass it down.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Merge Sort is Preferred for Linked Lists while Quick Sort is Preferred for Arrays:
> * **Arrays**: Random memory access $O(1)$ makes Quick Sort's in-place partitioning extremely fast with zero auxiliary array allocations.
> * **Linked Lists**: Sequential access makes partitioning slow, but pointer manipulation allows Merge Sort to merge two sorted lists in $O(1)$ extra space with zero array allocations! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Merge Sort (Recursive) | Quick Sort (Recursive) | Heap Sort (Iterative) |
| :--- | :--- | :--- | :--- |
| **Time (Worst Case)** | **$O(N \log N)$ Strict ⚡**| $O(N^2)$ Quadratic | **$O(N \log N)$ Strict ⚡**|
| **Auxiliary Memory** | $O(N)$ Extra Memory | **$O(\log N)$ Stack Space ⚡**| **$O(1)$ Zero Extra Space ⚡**|
| **Stability** | **Stable Sort ⚡** | Unstable Sort | Unstable Sort |

---

## 14. How to Recognize This in Questions

* **"Search element in sorted array in logarithmic time"** $\rightarrow$ Recursive Binary Search.
* **"Sort container with guaranteed O(N log N) stability"** $\rightarrow$ Recursive Merge Sort.
* **"In-place fast array sorting with low space overhead"** $\rightarrow$ Recursive Quick Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Merge Sort require $O(N)$ extra space while Quick Sort requires $O(\log N)$ stack space?**  
  *A:* Merge Sort requires an auxiliary array of size $N$ to merge two sorted halves without overwriting un-merged elements. Quick Sort partitions array elements in-place, requiring memory ONLY for recursive call stack frames ($O(\log N)$ depth).

* **Q: How can Quick Sort's $O(N^2)$ worst-case time complexity be avoided?**  
  *A:* By using Randomized Pivot Selection or Median-of-Three pivot selection to guarantee balanced sub-partitions.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: CORE RECURSIVE ALGORITHMS                             |
+-----------------------------------------------------------------------+
| • Binary Search : mid = low + (high - low) / 2 | Time O(log N)        |
| • Merge Sort    : T(N) = 2T(N/2) + O(N) | Stable | Time O(N log N) ⚡|
| • Quick Sort    : Partition around pivot | In-place | Time O(N log N) avg|
| • Tree DFS      : Inorder (Left, Root, Right) | Time O(V + E) ⚡       |
| • Mid Overflow  : ALWAYS use low + (high - low) / 2                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write overflow-safe Recursive Binary Search in Java.
- [ ] I can write Recursive Merge Sort with temporary array merging.
- [ ] I can write Recursive Quick Sort with Lomuto partitioning.
- [ ] I can explain why Merge Sort is $O(N \log N)$ across all cases.
- [ ] I can write Recursive Binary Tree In-Order DFS traversal.
