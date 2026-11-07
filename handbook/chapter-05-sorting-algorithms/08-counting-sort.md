# 08. Counting Sort: Non-Comparison Linear Bounds, Frequency Offsets & Prefix Sum Stability

## 1. Introduction
**Counting Sort** is an optimal non-comparison sorting algorithm that bypasses the theoretical $\Omega(N \log N)$ lower bound of comparison-based sorting by exploiting integer key range distributions. By assuming keys lie within a bounded integer range $[minVal \dots maxVal]$ of size $K = maxVal - minVal + 1$, Counting Sort counts element frequencies, builds a **Prefix Sum Cumulative Frequency Array**, and places elements directly into their final destination indices in **$O(N + K)$ Linear Time**. Right-to-left placement during output generation guarantees **Strict Sorting Stability** in **$O(N + K)$ Auxiliary Space**.

> **Important:** The 4 Structural Invariants of Counting Sort:
> 1. **Non-Comparison Invariant**: Operates WITHOUT key comparisons ($x \le y$), avoiding the $\Omega(N \log N)$ lower bound limit.
> 2. **Frequency Array Construction**: Creates count array `count[K]` tracking the exact occurrence frequency of each key value.
> 3. **Prefix Sum Accumulation**: Transforms `count[i]` into cumulative frequency counts:
>    $$\text{count}[i] = \text{count}[i] + \text{count}[i-1]$$
>    `count[val]` specifies the exact 1-based count of elements $\le val$.
> 4. **Right-to-Left Placement Stability Invariant**: Iterates the input array **BACKWARDS from $N-1$ down to $0$**, placing `arr[i]` into `output[count[val] - 1]` and decrementing `count[val]--`. Iterating backwards guarantees equal keys retain their relative input order! ⚡

```
Counting Sort Pipeline Topology (arr = [4, 2, 2, 8, 3, 3], Range K = 9):
Step 1: Frequency Array   -> count = [0, 0, 2, 2, 1, 0, 0, 0, 1] (Keys 0..8)
Step 2: Prefix Sum Array  -> count = [0, 0, 2, 4, 5, 5, 5, 5, 6] (Cumulative Count)
Step 3: Right-to-Left Placement -> Output = [ 2, 2, 3, 3, 4, 8 ]!

Linear Time Execution O(N + K) Completed! ⚡
```

---

## 2. Core Concepts & Counting Sort Strategy Matrix

### 2.1 Counting Sort Strategy Matrix
```
Counting Sort Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Step        | Primary Action    | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **1. Range Scanning** | Find Min & Max    | $O(N)$            | $O(1)$            |
| **2. Frequency Count**| Populate `count`  | $O(N)$            | $O(K)$ Count Array|
| **3. Prefix Sum**     | Accumulate sums   | $O(K)$            | $O(K)$ Count Array|
| **4. Stable Output**  | Right-to-Left Push| $O(N)$            | $O(N)$ Output Array|
| **Overall Algorithm** | Counting Sort     | **$O(N + K)$ Linear ⚡**| **$O(N + K)$ Space**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Counting Sort: Frequency count -> Prefix sum -> Right-to-left placement for stability O(N + K)!"**

---

## 3. Characteristics & $O(N + K)$ Linear Time Proof

### 3.1 Mathematical Proof of $O(N + K)$ Linear Time
* Let $N$ be the number of elements and $K$ be the integer range size ($K = maxVal - minVal + 1$).
* Step 1 (Find min/max): $N$ comparisons $\implies O(N)$.
* Step 2 (Frequency count): $N$ array increments $\implies O(N)$.
* Step 3 (Prefix sum accumulation): $K$ loop additions $\implies O(K)$.
* Step 4 (Stable output placement): $N$ assignments $\implies O(N)$.
* Total Time Complexity: $O(N) + O(N) + O(K) + O(N) = \mathbf{O(N + K) \text{ Linear Time}}$.
* When $K = O(N)$, total time is strictly **$O(N)$**. (If $K = O(N^2)$, Counting Sort degrades to $O(N^2)$ time!). ⚡

---

## 4. Internal Working Mechanics: Why Right-to-Left Placement Preserves Stability

Tracing Right-to-Left Output Placement on `arr = [ 3[A], 2, 3[B] ]`:

```
Input: [ 3[A], 2, 3[B] ] (3[A] is at index 0, 3[B] is at index 2)

Frequency Array (Range 2..3):
count[2] = 1, count[3] = 2

Prefix Sum Array:
count[2] = 1, count[3] = 3

Right-to-Left Placement Loop (i = 2 down to 0):

Step 1 (i = 2, val = 3[B]):
- count[3] is 3. Target index = count[3] - 1 = 2.
- Place 3[B] at output[2]. Decrement count[3] to 2.
- Output: [ _, _, 3[B] ]

Step 2 (i = 1, val = 2):
- count[2] is 1. Target index = 0.
- Place 2 at output[0]. Decrement count[2] to 0.
- Output: [ 2, _, 3[B] ]

Step 3 (i = 0, val = 3[A]):
- count[3] is 2. Target index = count[3] - 1 = 1.
- Place 3[A] at output[1]. Decrement count[3] to 1.
- Output: [ 2, 3[A], 3[B] ]

Result: 3[A] appears BEFORE 3[B] in output! Relative order PRESERVED! ✅
```

---

## 5. Visual Diagram: Prefix Sum Array Index Destination Mapping

```
Cumulative Count Array Transformation:

Raw Frequencies:    [  Count(2)=1  |  Count(3)=2  ]
Prefix Sum Array:   [  Count(2)=1  |  Count(3)=3  ]
                         │                 │
                         v                 v
Destination Range:  [ Index 0 ]   [ Indices 1 .. 2 ]

Prefix sum defines the EXACT upper boundary index for each key! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Stable Counting Sort (handling negative range offsets) and an Object Key Counting Sort.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Counting Sort Algorithms,
 * Range Offsets, Prefix Sum Arrays, and Stable Output Placements.
 */
public class CountingSortMaster {

    // =========================================================================
    // 1. STABLE COUNTING SORT WITH NEGATIVE RANGE OFFSETS (O(N + K) Time & Space)
    // =========================================================================
    /**
     * Performs Stable Counting Sort over an integer array containing negative/positive keys.
     *
     * @param arr input integer array
     */
    public void countingSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        // Step 1: Scan Min and Max Values in O(N) Time
        int minVal = arr[0];
        int maxVal = arr[0];
        for (int num : arr) {
            if (num < minVal) minVal = num;
            if (num > maxVal) maxVal = num;
        }

        int range = maxVal - minVal + 1; // Range K
        int[] count = new int[range];
        int[] output = new int[arr.length];

        // Step 2: Frequency Count in O(N) Time (With minVal offset shift)
        for (int num : arr) {
            count[num - minVal]++;
        }

        // Step 3: Prefix Sum Accumulation in O(K) Time
        for (int i = 1; i < range; i++) {
            count[i] += count[i - 1];
        }

        // Step 4: Stable Output Placement (RIGHT-TO-LEFT LOOP from N-1 down to 0)
        for (int i = arr.length - 1; i >= 0; i--) {
            int val = arr[i];
            int countIdx = val - minVal;

            output[count[countIdx] - 1] = val; // Place in output
            count[countIdx]--;                 // Decrement cumulative count
        }

        // Copy sorted output back into original array
        System.arraycopy(output, 0, arr, 0, arr.length);
    }
}
```

> **Quick Syntax:**
```java
// Stable Right-to-Left Placement Loop Line
for (int i = n - 1; i >= 0; i--) output[--count[arr[i] - minVal]] = arr[i];
```

---

## 7. Concrete Problem Examples & Applications

1. **Radix Sort Subroutines**:
   - Counting Sort serves as the stable digit-by-digit sorting subroutine inside Radix Sort.

2. **Bounded Integer Key Sorting**:
   - Sorting student exam grades $[0 \dots 100]$ for 1,000,000 students in $O(N)$ time!

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class CountingSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     COUNTING SORT LINEAR BOUNDS DEMO            ");
        System.out.println("=================================================\n");

        CountingSortMaster master = new CountingSortMaster();

        // 1. Stable Counting Sort Test (With Negative Values)
        int[] arr = {4, -2, 2, 8, 3, 3, -2};
        System.out.println("1. Original Array (With Negative Keys): " + Arrays.toString(arr));
        master.countingSort(arr);
        System.out.println("   Sorted Array (O(N + K) Linear Time): " + Arrays.toString(arr));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Sorting Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Counting Sort** | $\mathbf{O(N + K)}$ Linear ⚡| $\mathbf{O(N + K)}$ Linear ⚡| $\mathbf{O(N + K)}$ Linear ⚡| $O(N + K)$ Extra Array| Bounded integer range $K$ |

---

## 10. Edge Cases & Boundary Handling

1. **Range Size $K$ Much Larger Than $N$ ($K \gg N$)**:
   - If sorting `[1, 1000000000]`, range $K = 10^9$ causes $O(10^9)$ space allocation and memory explosion.
   - **Guard**: Fall back to QuickSort / Merge Sort when $K > N \log N$.

2. **Negative Range Keys**:
   - Subtracting `minVal` (`num - minVal`) maps negative keys to valid non-negative array indices $[0 \dots K-1]$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forward Iteration (`0 ... N-1`) During Output Placement**:
  - Iterating forward from $0$ to $N-1$ during output placement reverses the relative order of equal keys, rendering Counting Sort **UNSTABLE**.
  - **ALWAYS iterate BACKWARDS from $N-1$ down to $0$ to preserve stability**.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Counting Sort Beats Comparison-Based Sorting:
> Counting Sort does NOT compare elements!
> It direct-indexes frequency values into an array, bypassing the mathematical $\Omega(N \log N)$ lower bound and achieving true **$O(N + K)$ Linear Time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Counting Sort | Quick Sort | Merge Sort |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | **$O(N + K)$ Linear ⚡** | $O(N \log N)$ Average | $O(N \log N)$ Strict |
| **Auxiliary Memory** | $O(N + K)$ Extra Space | **$O(\log N)$ Stack Space ⚡**| $O(N)$ Extra Memory |
| **Stability** | **Stable ⚡** | Unstable | **Stable ⚡** |

---

## 14. How to Recognize This in Questions

* **"Sort N integers in bounded range [0 ... K] in linear time"** $\rightarrow$ Counting Sort ($O(N + K)$).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does backward iteration (`N-1` down to `0`) preserve stability in Counting Sort?**  
  *A:* Because prefix sum `count[val]` specifies the rightmost output index for `val`. Processing the last occurrence of `val` first places it into the highest available index. Earlier occurrences are placed into lower indices, preserving original relative order.

* **Q: When should Counting Sort NOT be used?**  
  *A:* When range $K$ is significantly larger than $N$ ($K \gg N$), or when keys are non-discrete real numbers/floating-point values.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COUNTING SORT                                         |
+-----------------------------------------------------------------------+
| • Non-Comparison: Bypasses Omega(N log N) limit | O(N + K) Time ⚡     |
| • Offset Shift  : Range index = num - minVal                          |
| • Prefix Sum    : count[i] += count[i - 1]                            |
| • Backward Loop : for (i = n - 1 down to 0) output[--count[idx]] = val|
| • Stability     : Preserved by backward placement loop! ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Stable Counting Sort with negative range offsets in Java.
- [ ] I can explain why backward output placement preserves sorting stability.
- [ ] I can prove why Counting Sort runs in $O(N + K)$ linear time.
- [ ] I can state when Counting Sort degrades (when range $K \gg N$).
- [ ] I can build cumulative prefix sum arrays manually.
