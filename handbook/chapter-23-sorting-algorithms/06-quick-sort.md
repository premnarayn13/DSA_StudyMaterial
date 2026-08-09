# 06. Quick Sort: Partitioning Dynamics, Dual-Pivot Schemes & Stack Optimizations

## 1. Introduction
**Quick Sort** is an ultra-fast, in-place comparison-based sorting algorithm designed by Tony Hoare. Operating on the **Partition and Conquer** paradigm, Quick Sort selects a **Pivot Element $P$** and partitions the array into two sub-arrays such that all elements in the left partition are $\le P$ and all elements in the right partition are $\ge P$. Quick Sort then recurses on both partitions. Due to its **Exceptional L1/L2 Cache Locality**, **In-Place Execution ($O(\log N)$ Stack Space)**, and **Low Constant Factors**, Quick Sort (specifically **Dual-Pivot QuickSort**) serves as the default primitive sorting engine in `java.util.Arrays.sort()`.

> **Important:** Core Invariants of Quick Sort & Partitioning Schemes:
> 1. **Lomuto Partitioning**: Uses single directional scan `j` and boundary pointer `i`. Pivot selected as last element (`arr[high]`). Simple to implement, but performs more swaps than Hoare partitioning.
> 2. **Hoare Partitioning**: Uses two pointers (`i` starting left, `j` starting right) moving inward until they find out-of-place elements. Performs **$3\times$ fewer swaps** than Lomuto partitioning!
> 3. **Randomized Pivot Selection**: Randomly selects pivot index `rand(low, high)` to eliminate $O(N^2)$ worst-case performance on pre-sorted arrays.
> 4. **Tail Call Stack Depth Optimization**: Always recurse on the **SMALLER PARTITION FIRST** and process the larger partition using an iterative `while` loop, guaranteeing maximum call stack depth of **$O(\log N)$**! ⚡

```
Quick Sort Hoare Partitioning Topology (Pivot P = 4):
Array:           [ 3,  8,  2,  5,  1,  4 ]
Pointers:         i ──>             <── j

Step 1: i finds 8 (> 4), j finds 1 (< 4) ──> Swap(8, 1) ──> [ 3, 1, 2, 5, 8, 4 ]
Step 2: i finds 5 (> 4), j finds 2 (< 4) ──> Pointers cross! (i >= j)

Partition Index = j! Left part [3, 1, 2] <= 4, Right part [5, 8, 4] >= 4! ⚡
```

---

## 2. Core Concepts & Partitioning Schemes Comparison Matrix

### 2.1 Partitioning Schemes Strategy Matrix
```
Quick Sort Partitioning Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Partitioning Scheme   | Pointer Strategy  | Swap Efficiency   | Equal Key Handling|
+-----------------------+-------------------+-------------------+-------------------+
| **Lomuto Partition**  | 1 Direction Scan  | Baseline Swaps    | Slow on duplicates|
| **Hoare Partition**   | 2 Inward Pointers | **3x Fewer Swaps⚡**| **Fast Hoare Cut ⚡**|
| **Dual-Pivot (Java)** | 3 Partitions      | **Cache Optimal ⚡**| Dual Pivot Ranges |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Hoare partitioning uses 2 inward pointers and executes 3x fewer swaps than Lomuto!"**

---

## 3. Characteristics & $O(N \log N)$ Average Time Proof

### 3.1 Mathematical Proof of $O(N \log N)$ Average Time
* Recurrence Relation: $T(N) = T(k) + T(N - 1 - k) + O(N)$, where $k$ is the pivot rank.
* Assuming all pivot ranks $k \in [0 \dots N-1]$ are equally likely (probability $1/N$):
  $$T(N) = O(N) + \frac{2}{N} \sum_{k=0}^{N-1} T(k)$$
* Solving via integration yields:
  $$T(N) = 2 N \ln N = 1.39 N \log_2 N = \mathbf{O(N \log N) \text{ Average Time Complexity}}$$
* Worst Case (Fixed pivot on pre-sorted array): $T(N) = T(N-1) + O(N) = \mathbf{O(N^2) \text{ Quadratic Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tail Call Elimination ($O(\log N)$ Stack Guard)

Naive Quick Sort can cause stack overflow if recursion always hits the larger partition first ($O(N)$ stack depth).

```
Tail Call Stack Depth Optimization Protocol:

// BAD: Recurses on left first unconditionally -> Worst-case O(N) Stack Depth!
quickSort(low, pivot - 1);
quickSort(pivot + 1, high);

// GOOD: Recurse on SMALLER partition first, iterate on LARGER partition! ⚡
while (low < high) {
    int pivot = partition(arr, low, high);
    if (pivot - low < high - pivot) {
        quickSort(low, pivot - 1); // Small left partition (Recurse)
        low = pivot + 1;           // Large right partition (Loop!)
    } else {
        quickSort(pivot + 1, high); // Small right partition (Recurse)
        high = pivot - 1;          // Large left partition (Loop!)
    }
}
Guarantees Call Stack Memory is strictly bounded by O(log N)! ✅
```

---

## 5. Visual Diagram: Dual-Pivot Partitioning Topology (Java Arrays.sort)

```
Dual-Pivot QuickSort 3-Way Partitioning (P1 < P2):

Array Domain: [  < P1  |  P1 <= val <= P2  |  Unexamined  |  > P2  ]
Indices:       0 ... L-1   L .......... K-1   K ........ G   G+1 .. N-1

L = Left pointer, K = Current scan pointer, G = Great pointer
Partitions array into 3 contiguous sub-regions in a single pass! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Lomuto Partitioning, Hoare Partitioning, Randomized Pivot Quick Sort, and Tail-Call Optimized Quick Sort.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Quick Sort Algorithms,
 * Hoare & Lomuto Partitioning, Randomized Pivots, and Tail-Call Stack Safety.
 */
public class QuickSortMaster {

    private final Random random = new Random();

    // =========================================================================
    // 1. RANDOMIZED QUICK SORT WITH HOARE PARTITIONING (O(N log N) Avg Time)
    // =========================================================================
    /**
     * Sorts array using Randomized Quick Sort with Hoare partitioning.
     *
     * @param arr input integer array
     */
    public void quickSortHoare(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        quickSortHoareHelper(arr, 0, arr.length - 1);
    }

    private void quickSortHoareHelper(int[] arr, int low, int high) {
        // Tail-Call Elimination Loop to enforce O(log N) Stack Memory!
        while (low < high) {
            // Step 1: Randomized Pivot Selection (Prevents O(N^2) worst case)
            int randPivotIdx = low + random.nextInt(high - low + 1);
            swap(arr, low, randPivotIdx);

            // Step 2: Hoare Partitioning
            int pivotIndex = hoarePartition(arr, low, high);

            // Step 3: Recurse on SMALLER partition first
            if (pivotIndex - low < high - pivotIndex) {
                quickSortHoareHelper(arr, low, pivotIndex);
                low = pivotIndex + 1; // Iterate on larger partition
            } else {
                quickSortHoareHelper(arr, pivotIndex + 1, high);
                high = pivotIndex;   // Iterate on larger partition
            }
        }
    }

    /**
     * Hoare Partitioning Scheme.
     * Uses inward moving pointers. Executes 3x fewer swaps than Lomuto.
     */
    private int hoarePartition(int[] arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1;
        int j = high + 1;

        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);

            if (i >= j) return j;

            swap(arr, i, j);
        }
    }

    // =========================================================================
    // 2. LOMUTO PARTITIONING QUICK SORT (Single Scan Pointer)
    // =========================================================================
    public void quickSortLomuto(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        quickSortLomutoHelper(arr, 0, arr.length - 1);
    }

    private void quickSortLomutoHelper(int[] arr, int low, int high) {
        if (low < high) {
            int p = lomutoPartition(arr, low, high);
            quickSortLomutoHelper(arr, low, p - 1);
            quickSortLomutoHelper(arr, p + 1, high);
        }
    }

    private int lomutoPartition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }

        swap(arr, i + 1, high);
        return i + 1;
    }

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Hoare Inward Pointer Loop Line
do { i++; } while (arr[i] < pivot); do { j--; } while (arr[j] > pivot); if (i >= j) return j; swap(arr, i, j);
```

---

## 7. Concrete Problem Examples & Systems Integration

1. **Java Primitive Arrays (`java.util.Arrays.sort(int[])`)**:
   - Uses **Dual-Pivot QuickSort** (Yaroslavskiy algorithm) for maximum CPU cache throughput.

2. **QuickSelect Algorithm (LeetCode 215 - Kth Largest Element)**:
   - Uses QuickSort partitioning to locate K-th largest element in **$O(N)$ Average Time** without sorting full array!

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class QuickSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     QUICK SORT PARTITIONING DEMONSTRATION       ");
        System.out.println("=================================================\n");

        QuickSortMaster master = new QuickSortMaster();

        // 1. Hoare Partitioning Quick Sort Test
        int[] arr1 = {3, 8, 2, 5, 1, 4};
        System.out.println("1. Original Array for Hoare Quick Sort: " + Arrays.toString(arr1));
        master.quickSortHoare(arr1);
        System.out.println("   Sorted Array (Hoare Inward Swaps)  : " + Arrays.toString(arr1));
        System.out.println("-------------------------------------------------");

        // 2. Lomuto Partitioning Quick Sort Test
        int[] arr2 = {10, 7, 8, 9, 1, 5};
        System.out.println("2. Original Array for Lomuto Quick Sort: " + Arrays.toString(arr2));
        master.quickSortLomuto(arr2);
        System.out.println("   Sorted Array (Lomuto Single Scan)   : " + Arrays.toString(arr2));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Quick Sort Variant | Average Time | Worst Case Time | Auxiliary Stack Space | Primary Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Lomuto Partition** | $\mathbf{O(N \log N)}$ ⚡| $O(N^2)$ (Fixed pivot) | $\mathbf{O(\log N)}$ Stack ⚡| Simple Implementation |
| **Hoare Partition**  | $\mathbf{O(N \log N)}$ ⚡| $O(N^2)$ (Fixed pivot) | $\mathbf{O(\log N)}$ Stack ⚡| **3x Fewer Swaps ⚡** |
| **Randomized + Tail Opt**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ (P=99.9%)| **Strict $O(\log N)$ Stack ⚡**| **No $O(N^2)$ Worst Case ⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **Already Sorted Array with Fixed Last Pivot (Lomuto)**:
   - Lomuto partitioning produces partitions of size $0$ and $N-1$, degrading to $O(N^2)$ time.
   - **Fix**: Use Randomized Pivot selection (`swap(arr, low + rand, high)`).

2. **All Identical Elements (`[5, 5, 5, 5]`)**:
   - Hoare partitioning stops pointers at equal keys and swaps them, producing perfectly balanced $N/2$ partitions.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Unconditional Recursion on Both Partitions (Stack Overflow Risk)**:
  - Recursing on left and right partitions without checking size can consume $O(N)$ stack frames on skewed inputs. Always recurse on the smaller partition first!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Hoare Partitioning Outperforms Lomuto Partitioning:
> Hoare partitioning uses two inward pointers (`i` and `j`). On average, Hoare partitioning performs **$3\times$ fewer element swaps** than Lomuto partitioning and handles duplicate elements gracefully without degrading partition balance! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Quick Sort (In-Place) | Merge Sort | Heap Sort |
| :--- | :--- | :--- | :--- |
| **Average Speed** | **Fastest In-Memory ⚡** | Fast | Moderate |
| **Auxiliary Memory** | **$O(\log N)$ Stack Space ⚡**| $O(N)$ Extra Memory | **$O(1)$ Zero Extra ⚡**|
| **Stability** | Unstable | **Stable ⚡** | Unstable |

---

## 14. How to Recognize This in Questions

* **"Sort primitive array in-place with maximum memory cache performance"** $\rightarrow$ Quick Sort.
* **"Find K-th largest / smallest element in O(N) average time"** $\rightarrow$ QuickSelect Partitioning.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Quick Sort faster than Merge Sort in practice?**  
  *A:* Quick Sort operates in-place with superior L1/L2 cache locality and low constant factors, whereas Merge Sort requires $O(N)$ auxiliary array allocations and element copy loops.

* **Q: How does Tail Call Elimination bound Quick Sort call stack memory to $O(\log N)$?**  
  *A:* By recursing on the smaller partition first ($\le N/2$ elements) and processing the larger partition via an iterative `while` loop, the call stack depth is guaranteed not to exceed $\log_2 N$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUICK SORT                                            |
+-----------------------------------------------------------------------+
| • Core Logic    : Partition array around pivot P so Left <= P <= Right |
| • Hoare Scheme  : 2 inward pointers -> 3x fewer swaps than Lomuto! ⚡  |
| • Randomized    : Swap pivot with random index to eliminate O(N^2)    |
| • Tail Stack Opt: Recurse on SMALLER partition first -> O(log N) Stack|
| • Performance   : Fastest primitive in-memory sort | O(N log N) Avg ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Quick Sort using Hoare inward pointer partitioning in Java.
- [ ] I can write Quick Sort using Lomuto partitioning.
- [ ] I can write Randomized Pivot Selection to prevent $O(N^2)$ worst-case time.
- [ ] I can implement Tail Call Stack Optimization to guarantee $O(\log N)$ stack space.
- [ ] I can explain why Hoare partitioning performs 3x fewer swaps than Lomuto.
