# 09. Radix Sort: Digit-by-Digit Processing, LSD vs MSD & Linear Bounds

## 1. Introduction
**Radix Sort** is an optimal non-comparison integer and string sorting algorithm that processes data digit-by-digit (or byte-by-byte) from either the **Least Significant Digit (LSD)** to the Most Significant Digit, or vice versa using **Most Significant Digit (MSD)** recursion. Rather than comparing elements directly ($x \le y$), Radix Sort distributes keys into $K$ radix buckets (e.g., base-10 digits $0 \dots 9$ or base-256 byte values) using a **Stable Subroutine (Counting Sort)** across $d$ passes, where $d$ is the maximum number of digits in the input. Radix Sort achieves **$O(d \cdot (N + K))$ Linear-Time Complexity** in **$O(N + K)$ Auxiliary Space**.

> **Important:** Core Invariants of Radix Sort & Digit Paradigms:
> 1. **LSD Radix Sort (Least Significant Digit)**: Processes digits right-to-left from least significant (units $10^0$) to most significant ($10^{d-1}$). REQUIRES a **Strictly Stable Subroutine (Counting Sort)** at every digit pass to preserve lower-digit relative ordering.
> 2. **MSD Radix Sort (Most Significant Digit)**: Processes digits left-to-right from most significant ($10^{d-1}$) down to units ($10^0$). Uses bucket-based recursion, ideal for variable-length strings and lexicographical sorting.
> 3. **Digit Extraction Formula (Base-10)**:
>    $$\text{digit} = \left\lfloor \frac{\text{val}}{\text{exp}} \right\rfloor \pmod{10}$$
>    where $\text{exp} = 1, 10, 100, 1000 \dots$
> 4. **Bitwise Radix Optimization (Base-256 / Byte Radix)**:
>    $$\text{byteVal} = (\text{val} \gg \text{shift}) \,\&\, 0xFF$$
>    Replaces integer division `/ exp` with 1-cycle bitwise shifts (`>>`) and bitmasks (`& 0xFF`), accelerating execution speed by **4x** on CPU hardware! ⚡

```
LSD Radix Sort (Base-10) Topology (arr = [170, 45, 75, 90, 802, 24, 2, 66]):
Pass 1 (1s Digit exp=1)   -> [ 170, 90, 802, 2, 24, 45, 75, 66 ]
Pass 2 (10s Digit exp=10) -> [ 802, 2, 24, 45, 66, 170, 75, 90 ]
Pass 3 (100s Digit exp=100)->[ 2, 24, 45, 66, 75, 90, 170, 802 ]

Array Fully Sorted in d=3 Linear Passes! ⚡
```

---

## 2. Core Concepts & Radix Sort Strategy Matrix

### 2.1 Radix Sort Strategy Matrix
```
Radix Sort Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Paradigm              | Processing Direction| Subroutine Needed | Ideal Domain      |
+-----------------------+-------------------+-------------------+-------------------+
| **LSD Radix Sort**    | Right-to-Left (1s)| **Counting Sort ⚡**| Fixed-Length Ints |
| **MSD Radix Sort**    | Left-to-Right (MSD)| Recursive Buckets | Variable Strings  |
| **Bitwise Base-256**  | Bit Shift (8 bits)| Stable Counting   | 32-bit Integers   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LSD processes right-to-left using Counting Sort; Bitwise Base-256 uses shift >> and mask & 0xFF!"**

---

## 3. Characteristics & $O(d \cdot (N + K))$ Complexity Proof

### 3.1 Mathematical Proof of $O(d \cdot (N + K))$ Linear Bounds
* Let $N$ be the number of keys, $d$ be the maximum number of digits/bytes per key, and $K$ be the radix base size (e.g. $K = 10$ for decimal digits, $K = 256$ for 8-bit bytes).
* The algorithm performs $d$ sequential passes.
* Each pass invokes Counting Sort over $N$ elements with radix base $K$, taking $O(N + K)$ time.
* Total Time Complexity:
  $$T(N) = \sum_{p=1}^{d} O(N + K) = \mathbf{O(d \cdot (N + K)) \text{ Time Complexity}}$$
* For 32-bit integers using Base-256 ($K = 256$), $d = 4$ passes constant.
* Thus $T(N) = 4 \cdot O(N + 256) = \mathbf{O(N) \text{ True Linear Time}}$! ⚡

---

## 4. Internal Working Mechanics: LSD Digit Passing

Tracing LSD Radix Sort on `arr = [170, 45, 75, 90, 802, 24, 2, 66]`:

```
Max Value = 802 (3 Digits -> Pass exp = 1, 10, 100).

Pass 1 (exp = 1, Units Digit):
Extract digits: 170(0), 45(5), 75(5), 90(0), 802(2), 24(4), 2(2), 66(6).
Counting Sort places elements stably:
Output: [ 170, 90, 802, 2, 24, 45, 75, 66 ]

Pass 2 (exp = 10, Tens Digit):
Extract digits: 170(7), 90(9), 802(0), 2(0), 24(2), 45(4), 75(7), 66(6).
Counting Sort places elements stably:
Output: [ 802, 2, 24, 45, 66, 170, 75, 90 ]

Pass 3 (exp = 100, Hundreds Digit):
Extract digits: 802(8), 2(0), 24(0), 45(0), 66(0), 170(1), 75(0), 90(0).
Counting Sort places elements stably:
Output: [ 2, 24, 45, 66, 75, 90, 170, 802 ]

Array sorted in d=3 linear passes! ✅
```

---

## 5. Visual Diagram: Bitwise Base-256 Radix Shifting

```
32-Bit Integer Split into 4 Bytes (Base-256):

32-Bit Int: [ Byte 3 (MSB) | Byte 2 | Byte 1 | Byte 0 (LSB) ]
Bit Shifts:   (val >> 24)    (val >> 16) (val >> 8)  (val >> 0)

Mask Expression: (val >> shift) & 0xFF  ---> Yields byte integer in range [0 ... 255]! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LSD Radix Sort (Base-10), High-Speed Bitwise Base-256 Radix Sort, and MSD String Radix Sort.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Radix Sort Algorithms,
 * Base-10 LSD Radix, Bitwise Base-256 Radix, and MSD String Radix.
 */
public class RadixSortMaster {

    // =========================================================================
    // 1. BASE-10 LSD RADIX SORT (O(d * (N + K)) Time, O(N + K) Space)
    // =========================================================================
    /**
     * Performs LSD Radix Sort on non-negative integer arrays.
     *
     * @param arr input integer array
     */
    public void lsdRadixSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        // Find maximum number to determine digit count d
        int maxVal = arr[0];
        for (int num : arr) {
            if (num > maxVal) maxVal = num;
        }

        // Process digit positions exp = 1, 10, 100, 1000...
        for (int exp = 1; maxVal / exp > 0; exp *= 10) {
            countingSortByDigit(arr, exp);
        }
    }

    private void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10]; // Radix Base K = 10 (digits 0..9)

        // Step 1: Frequency count of current digit (val / exp) % 10
        for (int i = 0; i < n; i++) {
            int digit = (arr[i] / exp) % 10;
            count[digit]++;
        }

        // Step 2: Prefix Sum Cumulative Frequency
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        // Step 3: Stable Right-to-Left Output Placement (N-1 down to 0)
        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[count[digit] - 1] = arr[i];
            count[digit]--;
        }

        // Copy sorted output back into original array
        System.arraycopy(output, 0, arr, 0, n);
    }

    // =========================================================================
    // 2. BITWISE BASE-256 RADIX SORT (4-Pass 32-Bit Fast Integer Sort)
    // =========================================================================
    /**
     * High-speed 4-pass Bitwise Base-256 Radix Sort for 32-bit integers.
     * Uses bit shifting (>> shift) and bit masking (& 0xFF) for 4x speedup!
     */
    public void bitwiseRadixSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        int[] output = new int[n];

        // 4 Passes for 32-bit integers (8 bits per pass: shift = 0, 8, 16, 24)
        for (int shift = 0; shift < 32; shift += 8) {
            int[] count = new int[256]; // Radix Base K = 256

            // Count frequencies
            for (int i = 0; i < n; i++) {
                int byteVal = (arr[i] >> shift) & 0xFF;
                count[byteVal]++;
            }

            // Prefix Sum
            for (int i = 1; i < 256; i++) {
                count[i] += count[i - 1];
            }

            // Stable Right-to-Left Output Placement
            for (int i = n - 1; i >= 0; i--) {
                int byteVal = (arr[i] >> shift) & 0xFF;
                output[count[byteVal] - 1] = arr[i];
                count[byteVal]--;
            }

            System.arraycopy(output, 0, arr, 0, n);
        }
    }

    // =========================================================================
    // 3. MSD STRING RADIX SORT (Variable-Length String Sorting)
    // =========================================================================
    /**
     * Sorts variable-length strings lexicographically using MSD Radix Sort.
     */
    public void msdStringSort(String[] arr) {
        if (arr == null || arr.length <= 1) return;
        String[] aux = new String[arr.length];
        msdStringSortHelper(arr, 0, arr.length - 1, 0, aux);
    }

    private void msdStringSortHelper(String[] arr, int lo, int hi, int d, String[] aux) {
        if (hi <= lo) return;

        int R = 256; // Extended ASCII radix
        int[] count = new int[R + 2];

        // Step 1: Count frequencies of d-th character
        for (int i = lo; i <= hi; i++) {
            int c = charAt(arr[i], d);
            count[c + 2]++;
        }

        // Step 2: Cumulative counts
        for (int r = 0; r < R + 1; r++) {
            count[r + 1] += count[r];
        }

        // Step 3: Distribute to auxiliary array
        for (int i = lo; i <= hi; i++) {
            int c = charAt(arr[i], d);
            aux[lo + count[c + 1]++] = arr[i];
        }

        // Step 4: Copy back
        for (int i = lo; i <= hi; i++) {
            arr[i] = aux[i];
        }

        // Step 5: Recurse on each character bucket
        for (int r = 0; r < R; r++) {
            msdStringSortHelper(arr, lo + count[r], lo + count[r + 1] - 1, d + 1, aux);
        }
    }

    private int charAt(String s, int d) {
        if (d < s.length()) return s.charAt(d);
        else return -1;
    }
}
```

> **Quick Syntax:**
```java
// Bitwise Base-256 Digit Extraction Line
int byteVal = (val >> shift) & 0xFF;
```

---

## 7. Concrete Problem Examples & Applications

1. **32-bit Integer GPU Sorting Engines**:
   - Bitwise Base-256 Radix Sort executes in exact 4 passes ($O(N)$ time) on graphics cards.

2. **Suffix Array & String Lexicographical Sorting**:
   - MSD String Radix Sort sorts million-string databases without full character comparison scans.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class RadixSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     RADIX SORT DIGIT PROCESSING DEMO            ");
        System.out.println("=================================================\n");

        RadixSortMaster master = new RadixSortMaster();

        // 1. Base-10 LSD Radix Sort Test
        int[] arr1 = {170, 45, 75, 90, 802, 24, 2, 66};
        System.out.println("1. Original Array for LSD Base-10 Radix: " + Arrays.toString(arr1));
        master.lsdRadixSort(arr1);
        System.out.println("   Sorted Array (d=3 Passes)           : " + Arrays.toString(arr1));
        System.out.println("-------------------------------------------------");

        // 2. Bitwise Base-256 Fast Radix Sort Test
        int[] arr2 = {170, 45, 75, 90, 802, 24, 2, 66};
        System.out.println("2. Bitwise Base-256 Fast 4-Pass Sort: " + Arrays.toString(arr2));
        master.bitwiseRadixSort(arr2);
        System.out.println("   Sorted Array (Bitwise Shift)     : " + Arrays.toString(arr2));
        System.out.println("-------------------------------------------------");

        // 3. MSD String Radix Sort Test
        String[] strArr = {"she", "sells", "sea", "shells", "by", "the", "sea", "shore"};
        System.out.println("3. Original String Array: " + Arrays.toString(strArr));
        master.msdStringSort(strArr);
        System.out.println("   Sorted Strings (MSD Radix): " + Arrays.toString(strArr));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Radix Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Stability Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LSD Radix Sort** | $\mathbf{O(d \cdot (N + K))}$ ⚡| $\mathbf{O(d \cdot (N + K))}$ ⚡| $\mathbf{O(d \cdot (N + K))}$ ⚡| $O(N + K)$ Extra Memory| **Stable ⚡** |
| **Bitwise Base-256**| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $O(N + 256)$ Space | **Stable ⚡** |
| **MSD String Radix**| $\mathbf{O(N \cdot L)}$ Linear| $\mathbf{O(N \cdot L)}$ Linear| $\mathbf{O(N \cdot L)}$ Linear| $O(N + R)$ Space | **Stable ⚡** |

---

## 10. Edge Cases & Boundary Handling

1. **Negative Integers in Bitwise Base-256 Radix Sort**:
   - 32-bit signed two's complement integers require flipping the MSB (sign bit) `arr[i] ^ 0x80000000` before sorting to preserve negative-to-positive ordering.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using Unstable Subroutine in LSD Radix Sort**:
  - If the digit subroutine is unstable (e.g. QuickSort), higher-digit passes destroy lower-digit relative ordering, ruining the final sort. LSD Radix Sort MUST use **Stable Counting Sort**!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Base-256 Bitwise Radix Outperforms Base-10:
> Integer division `/ 10` and modulo `% 10` require 10–12 ALU clock cycles.
> Bitwise shift `>> 8` and masking `& 0xFF` execute in **1 single clock cycle**, running **4x faster** on modern CPU hardware! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | LSD Radix Sort | Quick Sort | Counting Sort |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | **$O(d \cdot (N + K))$ Linear ⚡**| $O(N \log N)$ Average | $O(N + K)$ Linear |
| **Digit Pass Count $d$**| Fixed Passes ($d = 4$ for Base-256) | N/A | Single Pass ($d = 1$) |
| **Stability** | **Stable ⚡** | Unstable | **Stable ⚡** |

---

## 14. How to Recognize This in Questions

* **"Sort 1,000,000 32-bit integers in strict O(N) linear time"** $\rightarrow$ Bitwise Base-256 Radix Sort ($d = 4$).
* **"Sort large collection of fixed-length strings or IP addresses"** $\rightarrow$ Radix Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does LSD Radix Sort require a stable digit sorting subroutine?**  
  *A:* Because when higher-order digits are equal (e.g. `170` and `190` at hundreds place `1`), stability ensures their previously sorted lower-digit relative order is preserved.

* **Q: What is the optimal radix base $K$ for 32-bit integers?**  
  *A:* Base $K = 256$ ($2^8 = 256$, 8 bits per pass). It requires exactly $d = 32 / 8 = 4$ passes and uses a tiny 256-element count array.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RADIX SORT                                            |
+-----------------------------------------------------------------------+
| • LSD Radix     : Digit-by-digit right-to-left using Stable Counting  |
| • MSD Radix     : Digit-by-digit left-to-right via bucket recursion   |
| • Bitwise 256   : byteVal = (val >> shift) & 0xFF (4 Passes for 32-bit)|
| • Performance   : O(d * (N + K)) Time | Linear O(N) for 32-bit ints ⚡  |
| • Requirement   : Subroutine MUST be strictly STABLE! ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Base-10 LSD Radix Sort in Java.
- [ ] I can write Bitwise Base-256 4-pass Fast Radix Sort using `>>` and `& 0xFF`.
- [ ] I can write MSD String Radix Sort for variable-length strings.
- [ ] I can explain why LSD Radix Sort requires a stable digit subroutine.
- [ ] I can state the time complexity of Bitwise Radix Sort for 32-bit integers ($O(4N) = O(N)$).
