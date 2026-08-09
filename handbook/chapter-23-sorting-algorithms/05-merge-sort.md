# 05. Merge Sort: Divide & Conquer, Stability Invariants & Inversion Counting

## 1. Introduction
**Merge Sort** is an optimal comparison-based Divide and Conquer sorting algorithm designed by John von Neumann. It operates by recursively halving an input array of size $N$ into two equal sub-arrays, recursively sorting both halves, and merging the sorted sub-arrays using a **Two-Pointer Merge Routine**. Merge Sort guarantees strict **$O(N \log N)$ Time Complexity** across Best, Average, and Worst cases, while preserving **Strict Sorting Stability**. Beyond sorting, the merge routine's structural invariants serve as the engine for solving counting problems like **Inversion Count** and **Count of Smaller Numbers After Self (LeetCode 315)**.

> **Important:** Core Invariants of Merge Sort:
> 1. **Divide Phase**: Bisect search range $[left \dots right]$ at $mid = left + (right - left) / 2$, spawning 2 subproblems of size $N/2$.
> 2. **Stability Invariant in Merge Routine**:
>    - During the merge phase, when comparing elements from left and right halves:
>      $$\text{if } (arr[i] \le arr[j]) \implies \text{take left element } arr[i]$$
>    - Using non-strict inequality ($\le$) guarantees that equal keys from the left half are placed BEFORE equal keys from the right half, preserving strict **Stability**!
> 3. **Inversion Counting Connection**: An inversion is a pair $(i, j)$ where $i < j$ and $arr[i] > arr[j]$. During merging, if $arr[j] < arr[i]$, exactly $(mid - i + 1)$ inversions are detected in $O(1)$ time! ⚡

```
Merge Sort Top-Down Divide and Bottom-Up Merge Topology:
Divide:              [ 38, 27, 43, 3, 9, 82, 10 ]
                          /                 \
                   [ 38, 27, 43, 3 ]     [ 9, 82, 10 ]
                      /         \           /       \
                [ 38, 27 ]    [ 43, 3 ] [ 9, 82 ]   [ 10 ]
                   /    \      /    \    /    \       |
                [38]   [27]  [43]   [3] [9]   [82]   [10] (Base Cases!)

Merge:          [ 27, 38 ]    [ 3, 43 ] [ 9, 82 ]   [ 10 ]
                     \           /          \        /
                   [ 3, 27, 38, 43 ]     [ 9, 10, 82 ]
                          \                 /
                     [ 3, 9, 10, 27, 38, 43, 82 ] (Strictly Sorted Output!) ⚡
```

---

## 2. Core Concepts & Merge Sort Variants Strategy Matrix

### 2.1 Merge Sort Strategy Matrix
```
Merge Sort Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variant               | Paradigm          | Auxiliary Space   | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+
| **Top-Down Recursive**| Recursion Stack   | $O(N)$ Temp + Stack| High Readability  |
| **Bottom-Up Iterative**| Iterative Widths | $O(N)$ Temp Array | **Zero Call Stack ⚡**|
| **Linked List Merge** | Pointer Re-linking| **$O(1)$ Space ⚡**| Zero Memory Alloc |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Merge Sort: Divide at mid, sort halves, merge with arr[i] <= arr[j] for stability!"**

---

## 3. Characteristics & Strict $O(N \log N)$ Time Complexity Proof

### 3.1 Mathematical Proof of Strict $O(N \log N)$ Bounds
* Recurrence Relation: $T(N) = 2 T(N/2) + O(N)$, with base case $T(1) = 0$.
* Expanding the recurrence tree:
  - Tree Height: $H = \log_2 N$.
  - Work per level: $2^l \times \left(\frac{N}{2^l}\right) = N$ operations per level.
* Total Work across all $\log_2 N + 1$ levels:
  $$T(N) = N \cdot (\log_2 N + 1) = \mathbf{O(N \log N) \text{ Strict Time Complexity}}$$
* Unlike QuickSort, Merge Sort NEVER degrades to $O(N^2)$ time! ⚡

---

## 4. Internal Working Mechanics: Inversion Counting During Merging

How does the merge phase count array inversions in $O(N \log N)$ time?

```
Tracing Inversion Count during Merge of Left [ 3, 8 ] and Right [ 2, 5 ]:

Left Half: [ 3, 8 ] (Indices i = 0..1, mid = 1)
Right Half: [ 2, 5 ] (Indices j = 2..3)

Step 1: Compare arr[i=0] (3) with arr[j=2] (2).
        2 < 3! Right element 2 is smaller than left element 3.
        Because Left Half is sorted, 2 is smaller than ALL remaining left elements [3, 8]!
        Inversions Count += (mid - i + 1) = (1 - 0 + 1) = 2 Inversions ((3, 2) and (8, 2)).
        Take 2 -> Temp: [ 2 ]. Advance j to 3.

Step 2: Compare arr[i=0] (3) with arr[j=3] (5).
        3 <= 5 -> Take 3 -> Temp: [ 2, 3 ]. Advance i to 1.

Step 3: Compare arr[i=1] (8) with arr[j=3] (5).
        5 < 8 -> Inversions Count += (mid - i + 1) = (1 - 1 + 1) = 1 Inversion ((8, 5)).
        Take 5 -> Temp: [ 2, 3, 5 ]. Advance j to 4.

Total Inversions Counted = 2 + 1 = 3 Inversions! ✅ (Calculated in O(N log N) Time!)
```

---

## 5. Visual Diagram: Two-Pointer Merge Phase Topography

```
Merging Left Sub-Array [ 2, 7, 9 ] and Right Sub-Array [ 3, 5, 8 ]:

Pointer i ─> [ 2, 7, 9 ]
Pointer j ─> [ 3, 5, 8 ]

Step 1: arr[i] (2) <= arr[j] (3) ──> Take 2 (Left) ──> Temp: [ 2 ]
Step 2: arr[i] (7)  > arr[j] (3) ──> Take 3 (Right) ──> Temp: [ 2, 3 ]
Step 3: arr[i] (7)  > arr[j] (5) ──> Take 5 (Right) ──> Temp: [ 2, 3, 5 ]
Step 4: arr[i] (7) <= arr[j] (8) ──> Take 7 (Left) ──> Temp: [ 2, 3, 5, 7 ]
Step 5: arr[i] (9)  > arr[j] (8) ──> Take 8 (Right) ──> Temp: [ 2, 3, 5, 7, 8 ]
Step 6: Flush remaining Left     ──> Take 9 (Left) ──> Temp: [ 2, 3, 5, 7, 8, 9 ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Top-Down Merge Sort, Bottom-Up Iterative Merge Sort, and $O(N \log N)$ Inversion Counting.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Merge Sort Algorithms,
 * Bottom-Up Iterative Merging, and Inversion Counting Engines.
 */
public class MergeSortMaster {

    // =========================================================================
    // 1. TOP-DOWN RECURSIVE MERGE SORT (O(N log N) Strict Time, O(N) Space)
    // =========================================================================
    /**
     * Sorts array using Top-Down Merge Sort.
     * Allocates a single temporary auxiliary array upfront to maximize performance.
     *
     * @param arr input integer array
     */
    public void topDownMergeSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int[] temp = new int[arr.length]; // Single allocation upfront!
        mergeSortHelper(arr, 0, arr.length - 1, temp);
    }

    private void mergeSortHelper(int[] arr, int left, int right, int[] temp) {
        if (left >= right) return; // Base Case Guard

        int mid = left + (right - left) / 2;

        // Step 1: Divide & Recurse on left and right halves
        mergeSortHelper(arr, left, mid, temp);
        mergeSortHelper(arr, mid + 1, right, temp);

        // Optimization Guard: If already sorted across boundary, skip merge!
        if (arr[mid] <= arr[mid + 1]) {
            return;
        }

        // Step 2: Merge sorted halves
        merge(arr, left, mid, right, temp);
    }

    private void merge(int[] arr, int left, int mid, int right, int[] temp) {
        int i = left;
        int j = mid + 1;
        int k = left;

        // Stable Two-Pointer Merge Phase: arr[i] <= arr[j]
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) { // Non-strict <= preserves STABILITY! ⚡
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }

        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        // Copy merged elements back into main array
        System.arraycopy(temp, left, arr, left, right - left + 1);
    }

    // =========================================================================
    // 2. BOTTOM-UP ITERATIVE MERGE SORT (Zero Call Stack Overhead)
    // =========================================================================
    /**
     * Sorts array iteratively using Bottom-Up Merge Sort.
     * Merges sub-array width pairs (1, 2, 4, 8 ...) without call stack recursion.
     */
    public void bottomUpMergeSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        int[] temp = new int[n];

        for (int width = 1; width < n; width *= 2) {
            for (int left = 0; left < n - width; left += 2 * width) {
                int mid = left + width - 1;
                int right = Math.min(left + 2 * width - 1, n - 1);

                merge(arr, left, mid, right, temp);
            }
        }
    }

    // =========================================================================
    // 3. INVERSION COUNTING ENGINE (O(N log N) Time, O(N) Space)
    // =========================================================================
    /**
     * Calculates total inversion count in an array.
     *
     * @param arr input array
     * @return total number of inversions
     */
    public long countInversions(int[] arr) {
        if (arr == null || arr.length <= 1) return 0;

        int[] copy = arr.clone();
        int[] temp = new int[arr.length];
        return countInversionsHelper(copy, 0, copy.length - 1, temp);
    }

    private long countInversionsHelper(int[] arr, int left, int right, int[] temp) {
        if (left >= right) return 0;

        int mid = left + (right - left) / 2;
        long inversions = 0;

        inversions += countInversionsHelper(arr, left, mid, temp);
        inversions += countInversionsHelper(arr, mid + 1, right, temp);

        inversions += mergeAndCount(arr, left, mid, right, temp);

        return inversions;
    }

    private long mergeAndCount(int[] arr, int left, int mid, int right, int[] temp) {
        int i = left;
        int j = mid + 1;
        int k = left;
        long inversions = 0;

        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
                inversions += (mid - i + 1); // Count remaining elements in left half! ⚡
            }
        }

        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        System.arraycopy(temp, left, arr, left, right - left + 1);
        return inversions;
    }
}
```

> **Quick Syntax:**
```java
// Inversion Count Line in Merge Phase
if (arr[i] <= arr[j]) temp[k++] = arr[i++]; else { temp[k++] = arr[j++]; inversions += (mid - i + 1); }
```

---

## 7. Concrete Problem Examples & Applications

1. **Linked List Sorting**:
   - Merge Sort is the standard sorting algorithm for Linked Lists because it requires **$O(1)$ Extra Space** by re-linking node pointers without array allocations!

2. **Inversion Counting & Ranking**:
   - Measuring dataset disorder or recommendation preference correlation (Kendall Tau Distance).

3. **External Sort Systems**:
   - Sorting massive multi-terabyte files on disk using Multi-Way External Merge Sort.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class MergeSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     MERGE SORT VARIANTS & INVERSIONS DEMO       ");
        System.out.println("=================================================\n");

        MergeSortMaster master = new MergeSortMaster();

        // 1. Top-Down Merge Sort Test
        int[] arr1 = {38, 27, 43, 3, 9, 82, 10};
        System.out.println("1. Original Array for Top-Down Merge Sort: " + Arrays.toString(arr1));
        master.topDownMergeSort(arr1);
        System.out.println("   Sorted Array                          : " + Arrays.toString(arr1));
        System.out.println("-------------------------------------------------");

        // 2. Bottom-Up Iterative Merge Sort Test
        int[] arr2 = {9, 82, 10, 38, 27, 43, 3};
        System.out.println("2. Original Array for Bottom-Up Merge Sort: " + Arrays.toString(arr2));
        master.bottomUpMergeSort(arr2);
        System.out.println("   Sorted Array (Zero Call Stack)        : " + Arrays.toString(arr2));
        System.out.println("-------------------------------------------------");

        // 3. Inversion Count Test
        int[] arr3 = {8, 4, 2, 1};
        long invCount = master.countInversions(arr3);
        System.out.println("3. Inversion Count for " + Arrays.toString(arr3) + ": " + invCount + " Inversions");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Merge Sort Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Stability Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Top-Down Recursive** | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Temp + Stack | **Stable ⚡** |
| **Bottom-Up Iterative**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Temp Array | **Stable ⚡** |
| **Linked List Merge**  | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| **$O(1)$ Pointer Space ⚡**| **Stable ⚡** |

---

## 10. Edge Cases & Boundary Handling

1. **Already Sorted Array (`arr[mid] <= arr[mid + 1]`)**:
   - Adding optimization check `if (arr[mid] <= arr[mid + 1]) return;` skips the merge routine completely, running in $O(N)$ time for sorted inputs!

2. **Array of Size 1**:
   - Handled by base case `left >= right` returning immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Allocating `new int[right - left + 1]` Inside Merge Routine**:
  - Allocating temporary arrays inside the recursive `merge()` method creates thousands of short-lived heap objects.
  - **Fix**: Allocate a single auxiliary array `int[] temp = new int[N]` upfront in the caller method and pass it down.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Merge Sort Uses `arr[i] <= arr[j]` for Stability:
> During merging, if `arr[i]` from the left half equals `arr[j]` from the right half, non-strict inequality (`<=`) chooses `arr[i]` from the left half first.
> This guarantees equal elements from the left side remain ahead of equal elements from the right side, preserving **Strict Stability**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Merge Sort | Quick Sort | Heap Sort |
| :--- | :--- | :--- | :--- |
| **Time (Worst Case)** | **$O(N \log N)$ Strict ⚡** | $O(N^2)$ Quadratic | **$O(N \log N)$ Strict ⚡** |
| **Auxiliary Space** | $O(N)$ Memory | **$O(\log N)$ Stack Space ⚡**| **$O(1)$ In-Place Memory ⚡**|
| **Stability** | **Stable ⚡** | Unstable | Unstable |

---

## 14. How to Recognize This in Questions

* **"Sort linked list in O(N log N) time and O(1) space"** $\rightarrow$ Merge Sort on Linked List.
* **"Count total inverted pairs (i < j and arr[i] > arr[j]) in array"** $\rightarrow$ Merge Sort Inversion Counting.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Merge Sort preferred for Linked Lists over Quick Sort?**  
  *A:* Linked Lists allow node pointer re-linking in $O(1)$ space during the merge step, eliminating Merge Sort's $O(N)$ array memory overhead. Quick Sort relies on random access indexing ($O(1)$) which Linked Lists do not support.

* **Q: How does `inversions += (mid - i + 1)` count inversions in $O(1)$ time per merge step?**  
  *A:* Because the left sub-array $[left \dots mid]$ is sorted, if $arr[j] < arr[i]$, then $arr[j]$ is strictly smaller than $arr[i]$ AND all remaining elements from $i$ to $mid$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MERGE SORT                                            |
+-----------------------------------------------------------------------+
| • Divide & Conquer : Divide at mid, sort halves, merge with 2 pointers|
| • Stability Guard  : Use arr[i] <= arr[j] to pick left element first  |
| • Inversion Count  : inversions += (mid - i + 1) when arr[j] < arr[i] |
| • Optimization     : If arr[mid] <= arr[mid + 1], skip merge step! ⚡   |
| • Performance      : Strict O(N log N) Time | O(N) Auxiliary Space    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Top-Down Merge Sort in Java with a single upfront auxiliary array.
- [ ] I can write Bottom-Up Iterative Merge Sort (zero call stack overhead).
- [ ] I can write Inversion Counting using Merge Sort in $O(N \log N)$ time.
- [ ] I can explain why `arr[i] <= arr[j]` preserves sorting stability.
- [ ] I can explain why Merge Sort is $O(1)$ space for Linked Lists.
