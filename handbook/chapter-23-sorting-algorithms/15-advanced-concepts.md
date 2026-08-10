# 15. Advanced Concepts: Sorting Networks, Dutch National Flag & Bitonic Sort

## 1. Introduction
**Advanced Sorting Concepts** push beyond standard comparison models into parallel hardware architectures, linear-time multi-way partitioning, and specialized array re-arrangements. Primary advanced paradigms include:
1. **Dutch National Flag 3-Way Partitioning (LeetCode 75 - Sort Colors)**: Arranges elements with duplicate keys (e.g. 0s, 1s, 2s) into 3 contiguous sub-regions in **$O(N)$ Single-Pass Linear Time** and **$O(1)$ Space**.
2. **Wiggle / Wave Array Sorting (LeetCode 280 / 324)**: Re-arranges an array into a wave pattern $nums[0] \le nums[1] \ge nums[2] \le nums[3] \dots$ in **$O(N)$ Linear Time**.
3. **Bitonic Sort & Sorting Networks**: Parallel sorting algorithms built from fixed hardware comparator networks (compare-and-swap nodes) executing in **$O(\log^2 N)$ Parallel Time Depth** on GPUs and FPGAs.
4. **Partial Sorting (QuickSelect LeetCode 215)**: Locates the top-K smallest or largest elements in **$O(N)$ Average Time** without sorting the full array.

> **Important:** Core Invariants of Advanced Sorting:
> 1. **Dutch National Flag 3-Pointer Invariant**: Maintains 3 pointers: `low` (boundary of 0s), `mid` (current scanner), and `high` (boundary of 2s):
>    - `nums[mid] == 0` $\implies$ `swap(low++, mid++)`
>    - `nums[mid] == 1` $\implies$ `mid++`
>    - `nums[mid] == 2` $\implies$ `swap(mid, high--)` (Do NOT advance `mid`!).
> 2. **Bitonic Sequence Property**: A sequence is Bitonic if it monotonically increases and then monotonically decreases, or can be circularly shifted to do so. Bitonic Sort merges two bitonic sequences in parallel.
> 3. **QuickSelect Partial Partitioning**: Recursively partitions ONLY the half containing the target index $K$, running in $O(N + N/2 + N/4 \dots) = \mathbf{O(N) \text{ Linear Average Time}}$. ⚡

```
Dutch National Flag 3-Pointer Topology (arr = [2, 0, 2, 1, 1, 0]):
Low = 0, Mid = 0, High = 5

Mid at 0 (val 2): Swap(0, 5) -> [ 0, 0, 2, 1, 1, 2 ], High becomes 4 (Mid stays 0).
Mid at 0 (val 0): Swap(0, 0) -> [ 0, 0, 2, 1, 1, 2 ], Low becomes 1, Mid becomes 1.
Mid at 1 (val 0): Swap(1, 1) -> [ 0, 0, 2, 1, 1, 2 ], Low becomes 2, Mid becomes 2.
Mid at 2 (val 2): Swap(2, 4) -> [ 0, 0, 1, 1, 2, 2 ], High becomes 3 (Mid stays 2).
Mid at 2 (val 1): Mid becomes 3. Loop terminates (Mid > High)!

Array Sorted in 1 Pass O(N) Time & O(1) Space! ⚡
```

---

## 2. Core Concepts & Advanced Sorting Strategy Matrix

### 2.1 Advanced Sorting Strategy Matrix
```
Advanced Sorting Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm / Pattern   | Goal              | Primary Mechanism | Complexity        |
+-----------------------+-------------------+-------------------+-------------------+
| **Dutch Flag (75)**   | 3-Way Partition   | 3 Pointers (low,mid,high)| **$O(N)$ Time / $O(1)$ Space ⚡**|
| **Wiggle Sort (280)** | Wave Re-ordering  | Single Pass Swaps | **$O(N)$ Time / $O(1)$ Space ⚡**|
| **QuickSelect (215)** | K-th Extrema      | Partial QuickSort | **$O(N)$ Avg Time / $O(1)$ Space ⚡**|
| **Bitonic Sort**      | Parallel GPU Sort | Hardware Networks | **$O(\log^2 N)$ Parallel Depth ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sort Colors 0,1,2 = Dutch Flag 3 pointers O(N); K-th Extrema = QuickSelect O(N) avg!"**

---

## 3. Characteristics & $O(N)$ QuickSelect Proof

### 3.1 Mathematical Proof of $O(N)$ Average QuickSelect Time
* QuickSelect partitions an array of size $N$ using a pivot.
* Unlike QuickSort (which recurses on BOTH halves), QuickSelect recurses on ONLY ONE half containing target rank $K$.
* Expected work across partition steps:
  $$T(N) = N + \frac{N}{2} + \frac{N}{4} + \frac{N}{8} \dots = N \sum_{i=0}^{\infty} \frac{1}{2^i}$$
* The infinite geometric series sum $\sum_{i=0}^{\infty} \frac{1}{2^i} = 2$.
* Total Expected Time: $T(N) = 2 N = \mathbf{O(N) \text{ True Linear Average Time}}$. ⚡

---

## 4. Internal Working Mechanics: Wiggle Sort Single Pass

Tracing Wiggle Sort I (LeetCode 280) `nums[0] <= nums[1] >= nums[2] <= nums[3] ...`:

```
Array: [ 3, 5, 2, 1, 6, 4 ]

Condition Rules:
- If index i is ODD: nums[i] MUST be >= nums[i - 1].
- If index i is EVEN: nums[i] MUST be <= nums[i - 1].

Step 1 (i = 1, ODD): Check 5 >= 3 (True) -> Keep: [ 3, 5, 2, 1, 6, 4 ]
Step 2 (i = 2, EVEN): Check 2 <= 5 (True) -> Keep: [ 3, 5, 2, 1, 6, 4 ]
Step 3 (i = 3, ODD): Check 1 >= 2 (False!) -> Swap(1, 2): [ 3, 5, 1, 2, 6, 4 ]
Step 4 (i = 4, EVEN): Check 6 <= 2 (False!) -> Swap(6, 2): [ 3, 5, 1, 6, 2, 4 ]
Step 5 (i = 5, ODD): Check 4 >= 2 (True) -> Keep: [ 3, 5, 1, 6, 2, 4 ]

Array Wiggle Formed: [ 3 <= 5 >= 1 <= 6 >= 2 <= 4 ] in O(N) Time! ✅
```

---

## 5. Visual Diagram: Bitonic Sorting Network Hardware Topology

```
Bitonic Sorting Network Node (Comparator Swap Unit):

Input A ──┐    ┌── Min(A, B)
          ├───►│  (Comparator Box)
Input B ──┘    └── Max(A, B)

Network connects N comparators in log^2(N) parallel stages! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Dutch National Flag (LeetCode 75), Wiggle Sort (LeetCode 280), and QuickSelect K-th Element (LeetCode 215).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced Sorting Paradigms:
 * Dutch National Flag, Wiggle Sort, and QuickSelect K-th Element Location.
 */
public class AdvancedConceptsMaster {

    private final Random random = new Random();

    // =========================================================================
    // 1. DUTCH NATIONAL FLAG 3-WAY PARTITION (LeetCode 75 O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Sorts array containing only 0s, 1s, and 2s in 1 pass.
     * LeetCode 75 Solution.
     *
     * @param nums input array of 0s, 1s, and 2s
     */
    public void sortColors(int[] nums) {
        if (nums == null || nums.length <= 1) return;

        int low = 0;
        int mid = 0;
        int high = nums.length - 1;

        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums, low, mid);
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else { // nums[mid] == 2
                swap(nums, mid, high);
                high--; // Do NOT increment mid here because swapped element from high must be inspected! ⚡
            }
        }
    }

    // =========================================================================
    // 2. WIGGLE SORT I (LeetCode 280 Single Pass O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Re-arranges array in-place into wiggle order: nums[0] <= nums[1] >= nums[2] <= nums[3]...
     */
    public void wiggleSort(int[] nums) {
        if (nums == null || nums.length <= 1) return;

        for (int i = 1; i < nums.length; i++) {
            if ((i % 2 == 1 && nums[i] < nums[i - 1]) || (i % 2 == 0 && nums[i] > nums[i - 1])) {
                swap(nums, i, i - 1);
            }
        }
    }

    // =========================================================================
    // 3. QUICKSELECT K-TH LARGEST ELEMENT (LeetCode 215 O(N) Avg Time)
    // =========================================================================
    /**
     * Finds K-th largest element in unsorted array in O(N) average time.
     * LeetCode 215 Solution.
     */
    public int findKthLargest(int[] nums, int k) {
        if (nums == null || nums.length < k) return -1;
        int targetIdx = nums.length - k; // Index in sorted order
        return quickSelect(nums, 0, nums.length - 1, targetIdx);
    }

    private int quickSelect(int[] nums, int low, int high, int k) {
        if (low == high) return nums[low];

        int randIdx = low + random.nextInt(high - low + 1);
        swap(nums, low, randIdx);

        int pivotIdx = partition(nums, low, high);

        if (pivotIdx == k) {
            return nums[pivotIdx];
        } else if (pivotIdx < k) {
            return quickSelect(nums, pivotIdx + 1, high, k);
        } else {
            return quickSelect(nums, low, pivotIdx - 1, k);
        }
    }

    private int partition(int[] nums, int low, int high) {
        int pivot = nums[low];
        int i = low - 1;
        int j = high + 1;

        while (true) {
            do { i++; } while (nums[i] < pivot);
            do { j--; } while (nums[j] > pivot);
            if (i >= j) return j;
            swap(nums, i, j);
        }
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Dutch Flag Swap Condition for 2
if (nums[mid] == 2) { swap(nums, mid, high); high--; } // Keep mid unchanged!
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 75 - Sort Colors**:
   - Primary Dutch National Flag 3-pointer benchmark ($O(N)$ time, $O(1)$ space).

2. **LeetCode 215 - Kth Largest Element in an Array**:
   - Partial sorting via QuickSelect ($O(N)$ average time).

3. **GPU Hardware Sort Acceleration**:
   - Bitonic Sorting Networks on Parallel CUDA Cores ($O(\log^2 N)$ parallel depth).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class AdvancedConceptsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ADVANCED SORTING CONCEPTS DEMO               ");
        System.out.println("=================================================\n");

        AdvancedConceptsMaster master = new AdvancedConceptsMaster();

        // 1. Dutch National Flag Test (LeetCode 75)
        int[] colors = {2, 0, 2, 1, 1, 0};
        System.out.println("1. Original Colors Array: " + Arrays.toString(colors));
        master.sortColors(colors);
        System.out.println("   Sorted Colors (Dutch Flag 1-Pass): " + Arrays.toString(colors));
        System.out.println("-------------------------------------------------");

        // 2. Wiggle Sort Test (LeetCode 280)
        int[] wiggle = {3, 5, 2, 1, 6, 4};
        System.out.println("2. Original Array for Wiggle Sort: " + Arrays.toString(wiggle));
        master.wiggleSort(wiggle);
        System.out.println("   Wiggle Sorted Array            : " + Arrays.toString(wiggle));
        System.out.println("-------------------------------------------------");

        // 3. QuickSelect Test (LeetCode 215)
        int[] arr = {3, 2, 1, 5, 6, 4};
        int k = 2;
        int kthMax = master.findKthLargest(arr, k);
        System.out.println("3. " + k + "-nd Largest Element in " + Arrays.toString(arr) + ": " + kthMax);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Advanced Paradigm | Time Complexity | Auxiliary Space | Key Architectural Rule |
| :--- | :--- | :--- | :--- |
| **Dutch Flag (75)** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ In-Place ⚡| Do not advance `mid` on 2-swap |
| **Wiggle Sort (280)**| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ In-Place ⚡| Single pass parity swaps |
| **QuickSelect (215)**| $\mathbf{O(N)}$ Average ⚡| $\mathbf{O(1)}$ Space ⚡| Recurse on ONLY ONE partition |
| **Bitonic Sort**     | $O(N \log^2 N)$ Sequential| **$O(\log^2 N)$ Parallel Depth ⚡**| Fixed hardware comparators |

---

## 10. Edge Cases & Boundary Handling

1. **Dutch Flag All Equal Array (`[1, 1, 1, 1]`)**:
   - `mid` pointer advances smoothly from $0$ to $N-1$ in $N$ iterations.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Advancing `mid` Pointer After Swapping 2 in Dutch Flag**:
  - Writing `mid++` when swapping `nums[mid]` with `nums[high]` is broken because the element brought from `high` has not been inspected yet! Keep `mid` unchanged.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why QuickSelect Beats Min-Heap for K-th Element:
> * Min-Heap approach takes $O(N + K \log N)$ time and requires $O(N)$ extra memory.
> * QuickSelect takes **$O(N)$ Linear Average Time** and operates **In-Place ($O(1)$ Space)**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | QuickSelect (Partial Sort) | Full QuickSort | Priority Queue Heap |
| :--- | :--- | :--- | :--- |
| **Goal** | Find K-th Element | Sort Full Array | Track Streaming Extrema |
| **Average Time** | **$O(N)$ Linear ⚡** | $O(N \log N)$ | $O(N + K \log N)$ |
| **Auxiliary Memory** | **$O(1)$ Space ⚡** | $O(\log N)$ Stack | $O(N)$ Heap |

---

## 14. How to Recognize This in Questions

* **"Sort array of 0s, 1s, and 2s in 1 pass with O(1) space"** $\rightarrow$ Dutch National Flag (LeetCode 75).
* **"Find K-th largest element in unsorted array in O(N) average time"** $\rightarrow$ QuickSelect (LeetCode 215).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Dutch National Flag operate in $O(N)$ time and 1 pass?**  
  *A:* Because every iteration either increments `low` or `mid`, or decrements `high`, processing 1 element per step until `mid > high`.

* **Q: Why does Bitonic Sort run fast on GPUs?**  
  *A:* Bitonic Sort uses a fixed, data-independent sequence of comparisons (Sorting Network), allowing graphics cards to execute all comparators in parallel without branch predictor stalls.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED SORTING CONCEPTS                             |
+-----------------------------------------------------------------------+
| • Dutch Flag    : 3 Pointers (low, mid, high) | Swap 2 -> high-- (mid same)|
| • Wiggle Sort   : Single pass odd/even parity swaps -> O(N) Time      |
| • QuickSelect   : Partition single half -> O(N) Linear Average Time ⚡  |
| • Bitonic Sort  : Hardware network comparator -> O(log^2 N) Parallel  |
| • Performance   : Dutch Flag and QuickSelect run in O(N) time & O(1) space|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 75 (`Sort Colors / Dutch National Flag`) in 1 pass and $O(1)$ space.
- [ ] I can write LeetCode 280 (`Wiggle Sort`) in $O(N)$ time.
- [ ] I can write LeetCode 215 (`K-th Largest Element`) using QuickSelect in $O(N)$ average time.
- [ ] I know why `mid` is not incremented when swapping with `high` in Dutch Flag.
- [ ] I can state the parallel time depth of Bitonic Sort ($O(\log^2 N)$).
