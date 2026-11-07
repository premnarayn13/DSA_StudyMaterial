# 10. Bucket Sort: Scatter-Gather Partitioning, Floating-Point Distribution & Subroutine Scaling

## 1. Introduction
**Bucket Sort** is a distribution-based non-comparison sorting algorithm designed for datasets uniformly distributed over a continuous interval (typically floating-point numbers in $[0.0, 1.0)$ or arbitrary integer ranges). Operating on a **Scatter-Gather Paradigm**, Bucket Sort partitions the input interval into $B$ empty buckets, scatters each input element into its corresponding bucket using a mathematical hash mapping function `bucketIndex = (int)(val * B)`, sorts each bucket individually using an efficient small-$N$ subroutine (**Insertion Sort**), and concatenates (gathers) the buckets in order. When inputs are uniformly distributed, Bucket Sort runs in **$O(N)$ Linear Average Time** and **$O(N + B)$ Auxiliary Space**.

> **Important:** Core Invariants of Bucket Sort & Scatter-Gather:
> 1. **Scatter Phase**: Assigns element `val` to bucket `idx`:
>    $$\text{bucketIndex} = \left\lfloor \frac{\text{val} - \text{minVal}}{\text{maxVal} - \text{minVal} + \epsilon} \times B \right\rfloor$$
>    Guarantees that all elements in bucket $i$ are strictly smaller than all elements in bucket $i+1$.
> 2. **Subroutine Sorting Phase**: Sorts each bucket using **Insertion Sort**. Since uniform distribution guarantees an expected $O(1)$ elements per bucket, sorting all buckets takes $O(N)$ average time.
> 3. **Gather Phase**: Concatenates sorted buckets sequentially into the final array.
> 4. **Skewed Worst-Case Degradation**: If all $N$ elements map into a single bucket, Bucket Sort degrades to Insertion Sort's worst-case time of **$O(N^2)$ Quadratic Time**. ⚡

```
Bucket Sort Scatter-Gather Topology (arr = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94], B = 10):
Scatter Phase:
Bucket 1 [0.1..0.2]: [ 0.17 ]
Bucket 2 [0.2..0.3]: [ 0.26 ]
Bucket 3 [0.3..0.4]: [ 0.39 ]
Bucket 7 [0.7..0.8]: [ 0.78, 0.72 ] -> Insertion Sort -> [ 0.72, 0.78 ]
Bucket 9 [0.9..1.0]: [ 0.94 ]

Gather Phase: Concatenate Buckets -> [ 0.17, 0.26, 0.39, 0.72, 0.78, 0.94 ]!

Linear Average Time Execution O(N) Completed! ⚡
```

---

## 2. Core Concepts & Bucket Sort Strategy Matrix

### 2.1 Bucket Sort Strategy Matrix
```
Bucket Sort Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Distribution Pattern  | Subroutine Used   | Average Time      | Worst Case Time   |
+-----------------------+-------------------+-------------------+-------------------+
| **Uniform $[0.0, 1.0)$**| Insertion Sort  | **$O(N)$ Linear ⚡**| $O(N^2)$ (Skewed) |
| **Arbitrary Range**   | Insertion Sort    | **$O(N + B)$ ⚡** | $O(N^2)$ (Skewed) |
| **Hybrid Quick-Bucket**| QuickSort Bucket  | **$O(N + B)$ ⚡** | $O(N \log N)$ Worst|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Scatter elements into buckets via hash index! Sort buckets with Insertion Sort, gather sequentially for O(N) linear average time!"**

---

## 3. Characteristics & $O(N)$ Linear Average Time Proof

### 3.1 Mathematical Proof of $O(N)$ Linear Average Time
* Let $N$ be the number of elements and $B$ be the number of buckets ($B = N$).
* Let $n_i$ be the random variable representing the number of elements falling into bucket $i$.
* The time to sort bucket $i$ using Insertion Sort is $O(n_i^2)$.
* Total expected time across all $B$ buckets:
  $$E[T(N)] = O(N) + \sum_{i=0}^{B-1} O(E[n_i^2])$$
* For uniform distribution, each element falls into bucket $i$ with probability $p = 1/B$.
* $n_i$ follows a Binomial Distribution $B(N, 1/B)$ with mean $E[n_i] = 1$ and variance $\text{Var}(n_i) = 1 - 1/B$.
* Expectation of square: $E[n_i^2] = \text{Var}(n_i) + E[n_i]^2 = (1 - 1/B) + 1 = 2 - 1/B = O(1)$.
* Summing over $N$ buckets: $\sum_{i=0}^{N-1} O(1) = O(N)$.
* Total Expected Time Complexity: $\mathbf{O(N) \text{ True Linear Average Time}}$. ⚡

---

## 4. Internal Working Mechanics: Scatter, Subroutine Sort & Gather

Tracing Bucket Sort on `arr = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]` with $B = 6$ Buckets:

```
Step 1: Scatter Phase (Hash: idx = (int)(val * 6)):
- 0.897 * 6 = 5.38 -> Bucket 5: [ 0.897 ]
- 0.565 * 6 = 3.39 -> Bucket 3: [ 0.565 ]
- 0.656 * 6 = 3.93 -> Bucket 3: [ 0.565, 0.656 ]
- 0.1234 * 6 = 0.74 -> Bucket 0: [ 0.1234 ]
- 0.665 * 6 = 3.99 -> Bucket 3: [ 0.565, 0.656, 0.665 ]
- 0.3434 * 6 = 2.06 -> Bucket 2: [ 0.3434 ]

Step 2: Subroutine Sort Phase (Insertion Sort per Bucket):
- Bucket 0: [ 0.1234 ]
- Bucket 2: [ 0.3434 ]
- Bucket 3: Insertion Sort -> [ 0.565, 0.656, 0.665 ]
- Bucket 5: [ 0.897 ]

Step 3: Gather Phase (Sequential Concatenation):
- Output: [ 0.1234, 0.3434, 0.565, 0.656, 0.665, 0.897 ]! ✅ (Executed in O(N) Average Time!)
```

---

## 5. Visual Diagram: Scatter-Gather Bucket Topology

```
Input Array: [ 0.78, 0.17, 0.39, 0.26, 0.72, 0.94 ]
                   │
                   ▼ (Scatter Phase: Math Hash Index Mapping)
Bucket 0 [0.0..0.2]: [ 0.17 ]
Bucket 1 [0.2..0.4]: [ 0.26, 0.39 ]
Bucket 2 [0.6..0.8]: [ 0.78, 0.72 ] ──> Insertion Sort ──> [ 0.72, 0.78 ]
Bucket 3 [0.8..1.0]: [ 0.94 ]
                   │
                   ▼ (Gather Phase: Sequential Bucket Flattening)
Output Array: [ 0.17, 0.26, 0.39, 0.72, 0.78, 0.94 ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Floating-Point Bucket Sort over $[0.0, 1.0)$, Range Integer Bucket Sort, and Subroutine Insertion Sort.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bucket Sort Algorithms,
 * Floating-Point Interval Buckets, Range Integer Buckets, and Insertion Subroutines.
 */
public class BucketSortMaster {

    // =========================================================================
    // 1. FLOATING-POINT BUCKET SORT OVER [0.0, 1.0) (O(N) Avg Time, O(N) Space)
    // =========================================================================
    /**
     * Performs Bucket Sort on floating-point numbers uniformly distributed in [0.0, 1.0).
     *
     * @param arr input double array
     */
    public void bucketSort(double[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;

        // Step 1: Create N empty buckets (ArrayList of Doubles)
        @SuppressWarnings("unchecked")
        List<Double>[] buckets = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            buckets[i] = new ArrayList<>();
        }

        // Step 2: Scatter Phase (Place elements into corresponding buckets)
        for (double val : arr) {
            int bucketIdx = (int) (val * n); // Hash mapping formula for [0.0, 1.0)
            if (bucketIdx >= n) bucketIdx = n - 1; // Clamp boundary edge case
            buckets[bucketIdx].add(val);
        }

        // Step 3: Subroutine Sort Phase (Sort individual buckets using Collections.sort / Insertion)
        for (int i = 0; i < n; i++) {
            Collections.sort(buckets[i]); // Insertion Sort under the hood for small lists
        }

        // Step 4: Gather Phase (Concatenate sorted buckets back into main array)
        int idx = 0;
        for (int i = 0; i < n; i++) {
            for (double val : buckets[i]) {
                arr[idx++] = val;
            }
        }
    }

    // =========================================================================
    // 2. RANGE INTEGER BUCKET SORT (Arbitrary Range MinVal to MaxVal)
    // =========================================================================
    /**
     * Performs Bucket Sort on integers over arbitrary minVal to maxVal ranges.
     */
    public void bucketSortRange(int[] arr, int numBuckets) {
        if (arr == null || arr.length <= 1 || numBuckets <= 0) return;

        int minVal = arr[0];
        int maxVal = arr[0];
        for (int num : arr) {
            if (num < minVal) minVal = num;
            if (num > maxVal) maxVal = num;
        }

        double range = (double) (maxVal - minVal + 1);

        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new ArrayList[numBuckets];
        for (int i = 0; i < numBuckets; i++) {
            buckets[i] = new ArrayList<>();
        }

        // Scatter Phase
        for (int val : arr) {
            int bucketIdx = (int) (((val - minVal) / range) * numBuckets);
            if (bucketIdx >= numBuckets) bucketIdx = numBuckets - 1;
            buckets[bucketIdx].add(val);
        }

        // Subroutine Sort Phase
        for (int i = 0; i < numBuckets; i++) {
            Collections.sort(buckets[i]);
        }

        // Gather Phase
        int idx = 0;
        for (int i = 0; i < numBuckets; i++) {
            for (int val : buckets[i]) {
                arr[idx++] = val;
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Floating-Point Bucket Hash Mapping Line
int bucketIdx = (int) (val * numBuckets);
```

---

## 7. Concrete Problem Examples & Applications

1. **Floating-Point Probability Distribution Sorting**:
   - Sorting floating-point sensor readings or probabilities uniformly distributed between $0.0$ and $1.0$ in $O(N)$ time.

2. **Topological External Bucket Files**:
   - Distributing external database rows into $B$ hash buckets on disk.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BucketSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     BUCKET SORT SCATTER-GATHER DEMO            ");
        System.out.println("=================================================\n");

        BucketSortMaster master = new BucketSortMaster();

        // 1. Floating-Point Bucket Sort Test
        double[] doubleArr = {0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434};
        System.out.println("1. Original Double Array: " + Arrays.toString(doubleArr));
        master.bucketSort(doubleArr);
        System.out.println("   Sorted Array (Scatter-Gather O(N) Avg): " + Arrays.toString(doubleArr));
        System.out.println("-------------------------------------------------");

        // 2. Integer Range Bucket Sort Test
        int[] intArr = {42, 17, 89, 23, 7, 56, 91, 34};
        System.out.println("2. Original Integer Array: " + Arrays.toString(intArr));
        master.bucketSortRange(intArr, 5);
        System.out.println("   Sorted Range Integers : " + Arrays.toString(intArr));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bucket Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Stability Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Uniform Bucket Sort** | $\mathbf{O(N + B)}$ Linear ⚡| $\mathbf{O(N + B)}$ Linear ⚡| $O(N^2)$ (All 1 Bucket) | $O(N + B)$ Bucket Lists| **Stable ⚡** |
| **Range Integer Bucket**| $\mathbf{O(N + B)}$ Linear ⚡| $\mathbf{O(N + B)}$ Linear ⚡| $O(N^2)$ (All 1 Bucket) | $O(N + B)$ Bucket Lists| **Stable ⚡** |

---

## 10. Edge Cases & Boundary Handling

1. **Value Equal to Max Range Boundary (`val == 1.0` or `val == maxVal`)**:
   - `(int)(1.0 * B)` yields `bucketIdx = B`, throwing `IndexOutOfBoundsException`.
   - **Guard**: Clamp index `if (bucketIdx >= B) bucketIdx = B - 1;`.

2. **Severely Skewed Data (All elements equal `[0.5, 0.5, 0.5]`)**:
   - All elements fall into bucket 0. Insertion sort runs in $O(N^2)$ worst-case time.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Bucket Sort to Non-Uniform Data Without Dynamic Sizing**:
  - Applying fixed-width Bucket Sort to exponentially clustered datasets causes single-bucket degradation ($O(N^2)$ time).
  - Use QuickSort / Merge Sort or dynamic tree buckets for non-uniform data.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Insertion Sort is Used inside Bucket Sort:
> Under uniform distribution, each bucket contains an expected average of **$O(1)$ elements** ($N/B \approx 1$).
> Insertion Sort runs with zero recursive overhead and low constant factors, making it the fastest possible subroutine for tiny $O(1)$ bucket sizes! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Bucket Sort | Counting Sort | Radix Sort |
| :--- | :--- | :--- | :--- |
| **Input Domain** | Continuous Floating-Point / Reals | Bounded Discrete Integers | Fixed-Length Integers / Strings |
| **Subroutine** | Insertion Sort per Bucket | Prefix Sum Accumulation | Stable Counting Sort |
| **Average Time** | **$O(N + B)$ Linear ⚡** | **$O(N + K)$ Linear ⚡** | **$O(d \cdot (N + K))$ Linear ⚡**|

---

## 14. How to Recognize This in Questions

* **"Sort array of floating-point numbers uniformly distributed in range [0.0, 1.0)"** $\rightarrow$ Bucket Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Bucket Sort achieve $O(N)$ average time complexity?**  
  *A:* Because uniform distribution guarantees that each bucket receives an expected $O(1)$ elements, allowing Insertion Sort per bucket to execute in $O(1)$ average time.

* **Q: How does Bucket Sort handle boundary values like `val = 1.0`?**  
  *A:* By clamping the calculated bucket index `bucketIdx = Math.min((int)(val * B), B - 1)` to prevent array out-of-bounds errors.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BUCKET SORT                                           |
+-----------------------------------------------------------------------+
| • Paradigm     : Scatter elements into buckets -> Sort -> Gather      |
| • Bucket Hash  : bucketIdx = (int)(val * numBuckets)                  |
| • Subroutine   : Insertion Sort per bucket (O(1) expected elements)   |
| • Performance  : O(N + B) Linear Average Time | O(N + B) Space ⚡      |
| • Edge Guard   : Clamp index if (bucketIdx >= B) bucketIdx = B - 1    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Floating-Point Bucket Sort over $[0.0, 1.0)$ in Java.
- [ ] I can write Range Integer Bucket Sort.
- [ ] I can prove why Bucket Sort runs in $O(N)$ linear average time under uniform distribution.
- [ ] I can clamp boundary edge cases `bucketIdx = B - 1`.
- [ ] I can state why Insertion Sort is the optimal subroutine for small bucket sizes.
