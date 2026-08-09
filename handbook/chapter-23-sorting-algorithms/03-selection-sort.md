# 03. Selection Sort: Minimum Element Selection, Instability & Minimal Swap Bounds

## 1. Introduction
**Selection Sort** is an in-place comparison sorting algorithm that divides the input array into two contiguous sub-arrays: a sorted prefix at the left and an unsorted suffix at the right. In each pass, Selection Sort scans the unsorted suffix to locate the **Minimum Element** and swaps it directly with the leftmost unsorted element, expanding the sorted prefix by 1 position. Selection Sort's primary architectural advantage is its strict **$O(N)$ Minimal Swaps Bound** (executing at most $N-1$ swaps total). However, its standard implementation is **Non-Adaptive** (executing $O(N^2)$ comparisons regardless of input order) and inherently **Unstable**.

> **Important:** Core Invariants of Selection Sort:
> 1. **Prefix Sorted Invariant**: After pass $i$ ($0 \le i < N-1$), the sub-array $[0 \dots i]$ contains the $i+1$ smallest elements in strictly sorted order.
> 2. **$O(N)$ Minimal Swaps Bound**: Performs EXACTLY $N-1$ swaps in worst case (and 0 swaps if self-swap skipped). Ideal for systems where flash memory writes are expensive!
> 3. **Instability Invariant**: Standard Selection Sort breaks stability by making non-adjacent long-distance swaps across equal keys (e.g. swapping `5[A]` at index 0 with `2` moves `5[A]` behind `5[B]`).
> 4. **Stable Selection Sort Variant**: Replaces long-distance swapping with right-shifting elements to insert the minimum element at position $i$ stably. ⚡

```
Selection Sort Pass 1 Topology (arr = [64, 25, 12, 22, 11]):
Scan Unsorted Suffix [64, 25, 12, 22, 11] -> Minimum is 11 at index 4.
Swap arr[0] (64) with arr[4] (11) -> Array becomes: [ (11), | 25, 12, 22, 64 ]

Pass 1 Complete: 11 is locked in final sorted position at index 0! ⚡
```

---

## 2. Core Concepts & Selection Sort Variants Strategy Matrix

### 2.1 Selection Sort Strategy Matrix
```
Selection Sort Variants Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variant               | Swap Mechanism    | Total Comparisons | Stability Invariant|
+-----------------------+-------------------+-------------------+-------------------+
| **Standard Selection**| Long-Distance Swap| $N(N-1)/2 = O(N^2)$| **Unstable ❌**   |
| **Stable Selection**  | Shift Right Insert| $N(N-1)/2 = O(N^2)$| **Stable ⚡**      |
| **Dual Selection**    | Min & Max Pair    | $O(N^2)$ (50% cut)| Unstable          |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Selection Sort: Scans minimum element per pass! Executes at most N-1 swaps total (O(N) swaps)!"**

---

## 3. Characteristics & $O(N)$ Minimal Swaps Proof

### 3.1 Mathematical Proof of $O(N)$ Minimal Swaps Bound
* Consider an array of size $N$.
* At each pass $i \in [0 \dots N-2]$, Selection Sort executes at most 1 swap: `swap(arr, i, minIndex)`.
* Total Swaps across all $N-1$ passes:
  $$S_{\max} = N - 1 = \mathbf{O(N) \text{ Linear Swaps}}$$
* Total Comparisons: $\sum_{i=0}^{N-2} (N - 1 - i) = \frac{N(N-1)}{2} = \mathbf{O(N^2) \text{ Non-Adaptive Comparisons}}$.
* Auxiliary Space: $\mathbf{O(1) \text{ In-Place Memory}}$. ⚡

---

## 4. Internal Working Mechanics: Why Standard Selection Sort Is Unstable

Tracing instability on array `[ 5[A], 5[B], 2 ]`:

```
Initial State: [ 5[A], 5[B], 2 ]  (5[A] is at index 0, 5[B] is at index 1)

Pass 1 (i = 0):
- Scan unsorted suffix [5[A], 5[B], 2] for minimum.
- Minimum element is 2 at index 2.
- Swap arr[0] (5[A]) with arr[2] (2).
- Array state becomes: [ 2, 5[B], 5[A] ]

Notice: 5[A] jumped behind 5[B]!
Relative input order of equal keys 5[A] and 5[B] is BROKEN!
Standard Selection Sort is inherently UNSTABLE! ❌
```

---

## 5. Visual Diagram: Selection Sort Sub-Array Partitioning

```
Pass 1:  [ (11), | 25, 12, 22, 64 ]   (Sorted Prefix: [11], Min 12 found at index 2)
Pass 2:  [ 11, (12), | 25, 22, 64 ]   (Sorted Prefix: [11, 12], Min 22 found at index 3)
Pass 3:  [ 11, 12, (22), | 25, 64 ]   (Sorted Prefix: [11, 12, 22], Min 25 found at index 3)
Pass 4:  [ 11, 12, 22, (25), | 64 ]   (Fully Sorted Array!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Standard Selection Sort, Stable Selection Sort (using element shifting), and Dual Selection Sort (simultaneously finding Min and Max).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Selection Sort Algorithms,
 * Minimal Swap Guarantees, and Stable Shifting Variants.
 */
public class SelectionSortMaster {

    // =========================================================================
    // 1. STANDARD SELECTION SORT (O(N^2) Time, O(1) Memory, O(N) Swaps)
    // =========================================================================
    /**
     * Performs standard Selection Sort.
     * Guarantees at most N-1 swaps total. Unstable.
     *
     * @param arr input integer array
     */
    public void standardSelectionSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;

            // Find minimum element in unsorted suffix [i ... n-1]
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }

            // Swap minimum element with leftmost unsorted position i
            if (minIndex != i) {
                swap(arr, i, minIndex); // At most N-1 swaps! ⚡
            }
        }
    }

    // =========================================================================
    // 2. STABLE SELECTION SORT (Shifting Insertion O(N^2) Time, Stable)
    // =========================================================================
    /**
     * Performs Stable Selection Sort by shifting elements right instead of long swapping.
     */
    public void stableSelectionSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;

            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }

            // Stable Insertion Shift: Move min element to position i without long swaps
            int key = arr[minIndex];
            while (minIndex > i) {
                arr[minIndex] = arr[minIndex - 1]; // Shift right
                minIndex--;
            }
            arr[i] = key; // Place minimum element at index i stably! ⚡
        }
    }

    // =========================================================================
    // 3. DUAL SELECTION SORT (Min & Max Simultaneous Selection)
    // =========================================================================
    /**
     * Simultaneously selects minimum and maximum in each pass.
     * Cuts comparison count by ~50%.
     */
    public void dualSelectionSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int start = 0;
        int end = arr.length - 1;

        while (start < end) {
            int minIndex = start;
            int maxIndex = start;

            for (int i = start + 1; i <= end; i++) {
                if (arr[i] < arr[minIndex]) minIndex = i;
                if (arr[i] > arr[maxIndex]) maxIndex = i;
            }

            // Swap minimum with start
            swap(arr, start, minIndex);

            // Handle edge case if max element was located at start position
            if (maxIndex == start) {
                maxIndex = minIndex;
            }

            // Swap maximum with end
            swap(arr, end, maxIndex);

            start++;
            end--;
        }
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
// Selection Minimum Index Finding Line
int minIndex = i; for (int j = i + 1; j < n; j++) if (arr[j] < arr[minIndex]) minIndex = j;
```

---

## 7. Concrete Problem Examples & Applications

1. **Flash Memory EEPROM Systems**:
   - Write operations on Solid State Drives (SSDs) and Microcontrollers degrade hardware cell life. Selection Sort's $O(N)$ minimal swaps bound minimizes write cycles!

2. **Small Array Sorting**:
   - Sorting arrays where swap operations are extremely expensive compared to key comparisons.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class SelectionSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    SELECTION SORT VARIANTS DEMONSTRATION        ");
        System.out.println("=================================================\n");

        SelectionSortMaster master = new SelectionSortMaster();

        // 1. Standard Selection Sort Test
        int[] arr1 = {64, 25, 12, 22, 11};
        System.out.println("1. Original Array for Selection Sort: " + Arrays.toString(arr1));
        master.standardSelectionSort(arr1);
        System.out.println("   Sorted Array (Minimal Swaps)      : " + Arrays.toString(arr1));
        System.out.println("-------------------------------------------------");

        // 2. Stable Selection Sort Test
        int[] arr2 = {5, 2, 8, 2, 1};
        System.out.println("2. Original Array for Stable Selection: " + Arrays.toString(arr2));
        master.stableSelectionSort(arr2);
        System.out.println("   Sorted Array (Stable Shift)        : " + Arrays.toString(arr2));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Selection Variant | Best Case Time | Average Case Time | Worst Case Time | Total Swaps (Worst) | Stability Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Selection**| $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | **$N - 1 = O(N)$ Swaps ⚡**| **Unstable ❌** |
| **Stable Selection**  | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ Shifts | **Stable ⚡** |
| **Dual Selection**    | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(N)$ Swaps | **Unstable ❌** |

---

## 10. Edge Cases & Boundary Handling

1. **Pre-Sorted Array (`[1, 2, 3, 4, 5]`)**:
   - Standard Selection Sort STILL performs $N(N-1)/2$ comparisons! It is **Non-Adaptive**.
   - `if (minIndex != i)` skips self-swaps, performing 0 memory writes.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Believing Selection Sort is Adaptive**:
  - Selection Sort ALWAYS scans the full unsorted suffix $[i+1 \dots N-1]$ to find the minimum. It cannot terminate early on pre-sorted arrays.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Choose Selection Sort Over Bubble/Insertion Sort:
> Choose Selection Sort when **MEMORY WRITE OPERATIONS ARE EXPENSIVE**!
> Insertion/Bubble Sort perform $O(N^2)$ memory writes. Selection Sort performs at most $O(N)$ memory writes (EXACTLY $N-1$ swaps), protecting EEPROM / Flash storage hardware! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Selection Sort | Insertion Sort | Bubble Sort |
| :--- | :--- | :--- | :--- |
| **Worst Comparisons**| $N(N-1)/2$ | $N(N-1)/2$ | $N(N-1)/2$ |
| **Worst Swaps / Writes**| **$N - 1 = O(N)$ Minimal ⚡**| $O(N^2)$ Writes | $O(N^2)$ Swaps |
| **Adaptivity** | Non-Adaptive ($O(N^2)$) | **Adaptive ($O(N)$) ⚡**| **Adaptive ($O(N)$) ⚡**|

---

## 14. How to Recognize This in Questions

* **"Sort array minimizing the total number of memory write / swap operations to O(N)"** $\rightarrow$ Selection Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Selection Sort execute at most $N-1$ swaps?**  
  *A:* Because each pass $i$ places the true minimum element directly into its final destination index $i$ using at most 1 swap.

* **Q: Why is standard Selection Sort non-adaptive?**  
  *A:* Because the outer loop runs $N-1$ times and the inner loop ALWAYS scans all remaining elements $i+1 \dots N-1$ to confirm the minimum, regardless of initial array order.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SELECTION SORT                                        |
+-----------------------------------------------------------------------+
| • Core Logic    : Finds min element in unsorted suffix and swaps to index i|
| • Swaps Bound   : EXACTLY N - 1 swaps total (O(N) Memory Writes) ⚡    |
| • Comparisons   : N(N-1)/2 = O(N^2) Non-Adaptive Comparisons          |
| • Stability     : Standard is UNSTABLE due to long-distance swaps ❌    |
| • Use Case      : Ideal for Flash / EEPROM memory with expensive writes!|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write standard Selection Sort in Java with `minIndex != i` swap guards.
- [ ] I can prove why Selection Sort executes at most $N-1$ total swaps.
- [ ] I can explain why standard Selection Sort is unstable.
- [ ] I can write Stable Selection Sort using element right-shifting.
- [ ] I can explain why Selection Sort is non-adaptive.
