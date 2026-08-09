# 05. Binary Search Variations: Peak Element Search, Parity Indexing & Ternary Search

## 1. Introduction
While standard binary search operates on strictly sorted arrays, advanced **Binary Search Variations** apply divide-and-conquer logic to unsorted or non-strictly monotonic domains by identifying structural **Slope Predicates** and **Index Parity Invariants**. Core benchmark variations include **Find Peak Element (LeetCode 162)** (finding a local maximum element $arr[i-1] < arr[i] > arr[i+1]$ in $O(\log N)$ time), **Single Element in a Sorted Array (LeetCode 540)** (exploiting even-odd index pairing parity), and **Ternary Search** (finding extrema of unimodal continuous functions).

> **Important:** The 3 Advanced Binary Search Variation Invariants:
> 1. **Peak Element Slope Invariant (LeetCode 162)**:
>    - Compare `arr[mid]` with right neighbor `arr[mid + 1]`:
>      - If `arr[mid] < arr[mid + 1]`: Slope is strictly INCREASING $\implies$ A peak MUST exist in the right half `[mid + 1 ... high]`!
>      - If `arr[mid] > arr[mid + 1]`: Slope is DECREASING $\implies$ A peak MUST exist in the left half `[low ... mid]`!
> 2. **Single Element Parity Invariant (LeetCode 540)**:
>    - In a sorted array where every element appears twice except one single element:
>      - Before single element: First copy is at EVEN index, second copy is at ODD index (`mid ^ 1`).
>      - After single element: First copy is at ODD index, second copy is at EVEN index.
> 3. **Ternary Search Trisection**: Divides search domain into 3 parts using two midpoints $m_1$ and $m_2$, achieving $O(\log_3 N)$ time for unimodal functions. ⚡

```
Peak Element Slope Predicate Partitioning Topography:
Slope Analysis:       [ 1,  2,  1,  3,  5,  6,  4 ]
Neighbors at mid=3:   arr[3]=3, arr[4]=5 -> Slope Increasing (3 < 5)!
Decision:             Peak MUST exist in Right Half [4 ... 6]!

Peak Element 6 Found at Index 5 in O(log N) Steps! ⚡
```

---

## 2. Core Concepts & Variation Paradigms Matrix

### 2.1 Binary Search Variation Paradigms
```
Binary Search Variations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variation Pattern     | Key Predicate     | Decision Direction| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Peak Element (162)**| `arr[mid] < arr[mid+1]`| Shift toward higher neighbor| **$O(\log N)$ Log ⚡**|
| **Single Element(540)**| `arr[mid] == arr[mid ^ 1]`| Check even-odd pair parity| **$O(\log N)$ Log ⚡**|
| **Ternary Search**    | $f(m_1) < f(m_2)$ | Eliminate $1/3$ domain| **$O(\log_3 N)$ Log ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Peak Search: Follow higher neighbor slope! Single Element: Check mid ^ 1 parity pair!"**

---

## 3. Characteristics & $O(\log N)$ Peak Search Proof

### 3.1 Mathematical Proof of Peak Search $O(\log N)$ Time
* Consider an array of size $N$ with boundary conditions $arr[-1] = arr[N] = -\infty$.
* If $arr[mid] < arr[mid+1]$, moving right guarantees encountering a peak because the right boundary $arr[N] = -\infty$ must force the slope to decrease eventually.
* The search interval halves at each step: $N \to N/2 \to N/4 \dots 1$.
* Total Comparisons: $\mathbf{O(\log_2 N) \text{ Time Complexity}}$. Auxiliary Space: $\mathbf{O(1) \text{ Iterative Space}}$. ⚡

---

## 4. Internal Working Mechanics: Parity Bitwise XOR Trick (`mid ^ 1`)

In LeetCode 540 (Single Element in a Sorted Array), adjacent paired elements normally start on even indices:

```
Parity Index Pairing Mechanics:
Index:   0  1  2  3  4  5  6
Array:  [1, 1, 2, 3, 3, 4, 4]
                 ^ Single Element 2 at Index 2!

- If mid is EVEN (e.g. 2): mid ^ 1 = 3 (Right neighbor).
- If mid is ODD  (e.g. 3): mid ^ 1 = 2 (Left neighbor).

Checking arr[mid] == arr[mid ^ 1] tests whether the current mid belongs to a valid left-side pair!
If true  -> Single element lies to the RIGHT (low = mid + 1).
If false -> Single element lies to the LEFT (high = mid).

Single Element 2 isolated in O(log N) Time! ✅
```

---

## 5. Visual Diagram: Unimodal Ternary Search Trisection

```
Ternary Search Domain Trisection (Unimodal Maximum):

Search Domain:    [ low ........... m1 ........... m2 ........... high ]
                    m1 = low + (high - low) / 3
                    m2 = high - (high - low) / 3

Case 1: f(m1) < f(m2) ──> Maximum CANNOT lie in [low ... m1]. Set low = m1 + 1.
Case 2: f(m1) > f(m2) ──> Maximum CANNOT lie in [m2 ... high]. Set high = m2 - 1. ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 162 (Find Peak Element), LeetCode 540 (Single Element in Sorted Array), and Continuous Ternary Search.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced Binary Search Variations:
 * Peak Element Search, Parity Index Isolation, and Ternary Search.
 */
public class BinarySearchVariationsMaster {

    // =========================================================================
    // 1. FIND PEAK ELEMENT (LeetCode 162 O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds a local peak element (arr[i] > arr[i-1] and arr[i] > arr[i+1]).
     * Array boundary ends are treated as -infinity.
     *
     * @param nums input integer array
     * @return index of any local peak
     */
    public int findPeakElement(int[] nums) {
        if (nums == null || nums.length == 0) return -1;

        int low = 0;
        int high = nums.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            // Compare mid with right neighbor
            if (nums[mid] < nums[mid + 1]) {
                low = mid + 1; // Slope increasing -> Peak lies to the right
            } else {
                high = mid; // Slope decreasing -> Peak lies at mid or left
            }
        }

        return low; // low == high is a local peak index!
    }

    // =========================================================================
    // 2. SINGLE ELEMENT IN A SORTED ARRAY (LeetCode 540 Parity XOR O(log N))
    // =========================================================================
    /**
     * Finds the single element that appears exactly once in a sorted array.
     * Uses bitwise XOR (mid ^ 1) parity pairing.
     *
     * @param nums sorted array where all elements except one appear twice
     * @return the single element value
     */
    public int singleNonDuplicate(int[] nums) {
        if (nums == null || nums.length == 0) return -1;

        int low = 0;
        int high = nums.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            // mid ^ 1 flips even index to odd neighbor (mid+1), and odd index to even neighbor (mid-1)
            if (nums[mid] == nums[mid ^ 1]) {
                low = mid + 1; // Valid pair order -> Single element lies to the right
            } else {
                high = mid; // Broken pair order -> Single element lies at mid or left
            }
        }

        return nums[low];
    }

    // =========================================================================
    // 3. TERNARY SEARCH FOR UNIMODAL MAXIMUM (O(log3 N) Time)
    // =========================================================================
    /**
     * Finds local maximum of a unimodal continuous function f(x) over [low, high].
     *
     * @param low lower domain bound
     * @param high upper domain bound
     * @param eps precision threshold
     * @return x coordinate of unimodal maximum
     */
    public double ternarySearchMax(double low, double high, double eps) {
        while (high - low > eps) {
            double m1 = low + (high - low) / 3.0;
            double m2 = high - (high - low) / 3.0;

            double f_m1 = unimodalFunction(m1);
            double f_m2 = unimodalFunction(m2);

            if (f_m1 < f_m2) {
                low = m1; // Maximum lies in [m1 ... high]
            } else {
                high = m2; // Maximum lies in [low ... m2]
            }
        }

        return low + (high - low) / 2.0;
    }

    // Sample unimodal parabola f(x) = -(x - 3)^2 + 10 (Peak at x = 3.0)
    private double unimodalFunction(double x) {
        return -Math.pow(x - 3.0, 2) + 10.0;
    }
}
```

> **Quick Syntax:**
```java
// Peak Search Slope Comparison Line
if (nums[mid] < nums[mid + 1]) low = mid + 1; else high = mid;

// Parity Bitwise XOR Pairing Line
if (nums[mid] == nums[mid ^ 1]) low = mid + 1; else high = mid;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 162 - Find Peak Element**:
   - Signal Processing Local Extrema Filtering ($O(\log N)$).

2. **LeetCode 540 - Single Element in a Sorted Array**:
   - Parity Index Bitmask Isolation ($O(\log N)$).

3. **Optimization Solvers**:
   - Ternary Search for Convex/Unimodal Function Maximization.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BinarySearchVariationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BINARY SEARCH VARIATIONS DEMONSTRATION        ");
        System.out.println("=================================================\n");

        BinarySearchVariationsMaster master = new BinarySearchVariationsMaster();

        // 1. Peak Element Search Test
        int[] peakArr = {1, 2, 1, 3, 5, 6, 4};
        int peakIdx = master.findPeakElement(peakArr);
        System.out.println("1. Find Peak Element in " + Arrays.toString(peakArr) + ":");
        System.out.println("   Peak Index: " + peakIdx + " (Value = " + peakArr[peakIdx] + ")");
        System.out.println("-------------------------------------------------");

        // 2. Single Element Parity Search Test
        int[] singleArr = {1, 1, 2, 3, 3, 4, 4, 8, 8};
        int singleVal = master.singleNonDuplicate(singleArr);
        System.out.println("2. Single Non-Duplicate Element in " + Arrays.toString(singleArr) + ":");
        System.out.println("   Single Value: " + singleVal);
        System.out.println("-------------------------------------------------");

        // 3. Ternary Search Test (Unimodal Maximum for -(x-3)^2 + 10)
        double peakX = master.ternarySearchMax(0.0, 10.0, 1e-6);
        System.out.println("3. Ternary Search Peak X Coordinate: " + String.format("%.4f", peakX));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Variation Pattern | Time Complexity | Auxiliary Space | Key Predicate | Domain Requirement |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Search (162)** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | `nums[mid] < nums[mid+1]` | Boundary $-\infty$ |
| **Single Element (540)**| $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | `nums[mid] == nums[mid^1]` | Sorted pairs |
| **Ternary Search**    | $\mathbf{O(\log_3 N)}$ Log ⚡| $\mathbf{O(1)}$ Constant ⚡ | $f(m_1) < f(m_2)$ | Unimodal function |

---

## 10. Edge Cases & Boundary Handling

1. **Peak Element at Index 0 or $N - 1$**:
   - `findPeakElement` handles boundary peaks cleanly because array boundaries are implicitly $-\infty$. If `nums[0] > nums[1]`, the slope decreases immediately, terminating with `low = 0`.

2. **Single Element at Array Ends**:
   - Bitwise XOR `mid ^ 1` pairing handles boundary single elements at index $0$ or $N - 1$ without array out-of-bounds errors.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Accessing `nums[mid - 1]` Without Lower Bounds Check in Peak Search**:
  - Writing `nums[mid - 1] < nums[mid]` when `mid == 0` throws `ArrayIndexOutOfBoundsException`.
  - **Fix**: ALWAYS compare `nums[mid]` with right neighbor `nums[mid + 1]` (since `mid` is guaranteed $< N - 1$ when `low < high`).

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why `mid ^ 1` Bitwise XOR Replaces Manual Even/Odd Checking:
> * If `mid` is even (e.g. 4), `4 ^ 1 = 5` (checks right neighbor).
> * If `mid` is odd  (e.g. 5), `5 ^ 1 = 4` (checks left neighbor).
> Using `mid ^ 1` eliminates 10 lines of duplicated `if (mid % 2 == 0)` code into a single 1-line bitwise XOR test! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Binary Search Variations | Linear Scan Variations |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\log N)$ Logarithmic ⚡** | $O(N)$ Linear |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| **$O(1)$ Constant Space ⚡** |
| **Code Length** | ~10 Lines | ~15 Lines |

---

## 14. How to Recognize This in Questions

* **"Find local maximum in unsorted array where neighbors are distinct"** $\rightarrow$ LeetCode 162 Peak Search.
* **"Find single non-duplicate element in sorted array of pairs"** $\rightarrow$ LeetCode 540 Parity Search.
* **"Find max/min of continuous unimodal curve"** $\rightarrow$ Ternary Search.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does binary search work on unsorted arrays for Peak Element search?**  
  *A:* Because comparing `nums[mid]` with `nums[mid + 1]` establishes a slope predicate that guarantees a local peak MUST exist in the direction of the higher neighbor.

* **Q: How does `mid ^ 1` work for parity index checks?**  
  *A:* Flipping the 0-th bit converts even numbers to `even + 1` and odd numbers to `odd - 1`, matching paired twin indices automatically.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY SEARCH VARIATIONS                              |
+-----------------------------------------------------------------------+
| • Peak Search     : if (nums[mid] < nums[mid + 1]) low = mid + 1      |
| • Single Element  : if (nums[mid] == nums[mid ^ 1]) low = mid + 1     |
| • Ternary Search : Divides domain into 3 parts (m1, m2) for unimodal |
| • Parity XOR Rule : mid ^ 1 pairs even -> odd and odd -> even         |
| • Performance     : All variants achieve logarithmic O(log N) time! ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 162 (`Find Peak Element`) in $O(\log N)$ time.
- [ ] I can explain why Peak Search works on unsorted arrays.
- [ ] I can write LeetCode 540 (`Single Element in Sorted Array`) using `mid ^ 1`.
- [ ] I can explain the `mid ^ 1` bitwise XOR parity pairing trick.
- [ ] I can write continuous domain Ternary Search for unimodal functions.
