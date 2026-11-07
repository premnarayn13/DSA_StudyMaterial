# 03. Binary Search Fundamentals: Interval Halving, Midpoint Mathematics & Invariant Proofs

## 1. Introduction
**Binary Search** is the quintessential divide-and-conquer searching algorithm for sorted or monotonically partitioned search domains. By comparing a target key against the median element of a search interval $[low, high]$, Binary Search eliminates half of the remaining candidate elements at each step. This logarithmic reduction reduces time complexity from $O(N)$ to **$O(\log N)$**, enabling instant lookup across billions of elements. Mastering Binary Search fundamentals requires establishing rigid **Loop Invariants**, choosing correct interval termination conditions (`low <= high` vs `low < high`), and performing **Overflow-Safe Midpoint Arithmetic**.

> **Important:** The 3 Mandatory Invariants of Binary Search:
> 1. **Search Space Invariant**: At the start of every iteration, if the target key exists in the array, it MUST lie within the inclusive index range $[low, high]$.
> 2. **Overflow-Safe Midpoint Calculation**:
>    $$\text{mid} = low + \frac{high - low}{2} \quad \text{or} \quad \text{mid} = (low + high) \gg 1$$
>    Prevents 32-bit signed integer overflow when $low + high > 2^{31} - 1$ ($2,147,483,647$).
> 3. **Strict Interval Shrinking (Monotonic Progress)**: Every branch MUST shrink the search space ($high = mid - 1$ or $low = mid + 1$), guaranteeing the loop terminates in at most $\lfloor \log_2 N \rfloor + 1$ iterations. ⚡

```
Binary Search Interval Halving Topology (Target = 23):
Initial:  [ 2,  5,  8, 12, 16, 23, 38, 56, 72, 91 ]  low=0, high=9, mid=4 (val=16 < 23)
Step 1:                     [ 23, 38, 56, 72, 91 ]  low=5, high=9, mid=7 (val=56 > 23)
Step 2:                     [ 23, 38 ]              low=5, high=6, mid=5 (val=23 == 23)

Target 23 Found at Index 5 in 3 Comparisons! ⚡
```

---

## 2. Core Concepts & Binary Search Design Patterns Strategy Matrix

### 2.1 Binary Search Loop Templates Comparison Matrix
```
Binary Search Design Templates Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Template Paradigm     | Loop Condition    | Mid Assignment    | Target Range      |
+-----------------------+-------------------+-------------------+-------------------+
| **Template 1 (Exact)**| `while (low <= high)`| `high = mid - 1`  | Exact Value Match |
| **Template 2 (Left)** | `while (low < high)` | `high = mid`      | Boundary / Bound  |
| **Template 3 (Neighbor)**| `while (low + 1 < high)`| Check neighbors| 2-Element Window |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Template 1 (low <= high): Use high = mid - 1 and low = mid + 1 for exact value matches!"**

---

## 3. Characteristics & $O(\log N)$ Logarithmic Proof

### 3.1 Mathematical Proof of $O(\log N)$ Time Complexity
* Let $N$ be the initial size of the sorted array.
* At step $k$, the search space shrinks to $N / 2^k$.
* The algorithm terminates when the search space shrinks to size $1$:
  $$\frac{N}{2^k} = 1 \implies 2^k = N \implies k = \log_2 N$$
* Maximum Comparisons: $K_{\max} = \lfloor \log_2 N \rfloor + 1$.
* Total Time Complexity: $\mathbf{O(\log_2 N) \text{ Logarithmic Time}}$. Auxiliary Space: $\mathbf{O(1) \text{ Iterative Space}}$. ⚡

---

## 4. Internal Working Mechanics: The 32-Bit Integer Overflow Bug

In 2006, Joshua Bloch revealed that standard binary search implementations in Java `java.util.Arrays` contained a latent 32-bit integer overflow bug for over 9 years:

```java
// BUGS: Signed 32-Bit Integer Overflow!
int mid = (low + high) / 2;
// When low + high > 2,147,483,647, the sum wraps around to a NEGATIVE number!
// Array access arr[mid] throws java.lang.ArrayIndexOutOfBoundsException!
```

### 4.1 Production Solutions for Midpoint Calculation
1. **Subtraction Offset (Standard Java Production)**:
   ```java
   int mid = low + (high - low) / 2;
   ```
2. **Unsigned Right Shift (Bitwise Speedup)**:
   ```java
   int mid = (low + high) >>> 1; // >>> Zero-fills MSB bit, ignoring sign! ⚡
   ```

---

## 5. Visual Diagram: Search Space Contraction & Invariant Boundaries

```
Template 1 Iteration Contraction (low <= high):

Initial State:    [ low ........................ mid ........................ high ]
                                                  │
Case 1: arr[mid] < target ──> Shift Right:       [ low = mid + 1 .......... high ]
Case 2: arr[mid] > target ──> Shift Left : [ low .......... high = mid - 1 ]
Case 3: arr[mid] == target ─> Return mid! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Template 1 Exact Match Binary Search, Template 2 Boundary Binary Search, and Bitwise Unsigned Right Shift Mid Calculations.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Binary Search Fundamentals,
 * Overflow-Safe Midpoint Mathematics, and Invariant Verification.
 */
public class BinarySearchFundamentalsMaster {

    // =========================================================================
    // 1. TEMPLATE 1: EXACT MATCH ITERATIVE BINARY SEARCH (O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds exact index of target in a sorted integer array.
     * Uses Template 1 (low <= high) with subtraction offset midpoint calculation.
     *
     * @param arr sorted integer array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int binarySearchExact(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            // Overflow-Safe Midpoint Math: low + (high - low) / 2
            int mid = low + (high - low) / 2;

            if (arr[mid] == target) {
                return mid; // Exact match found!
            } else if (arr[mid] < target) {
                low = mid + 1; // Target lies in right half
            } else {
                high = mid - 1; // Target lies in left half
            }
        }

        return -1; // Target absent
    }

    // =========================================================================
    // 2. BITWISE UNSIGNED SHIFT BINARY SEARCH (High-Performance O(log N))
    // =========================================================================
    /**
     * Performs binary search using bitwise unsigned right shift ((low + high) >>> 1).
     * High-speed CPU instruction optimization.
     *
     * @param arr sorted integer array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int binarySearchBitwise(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            // Bitwise Unsigned Right Shift prevents negative wrapping!
            int mid = (low + high) >>> 1;

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }

        return -1;
    }

    // =========================================================================
    // 3. TEMPLATE 2: BOUNDARY BINARY SEARCH (First Match in Left Window O(log N))
    // =========================================================================
    /**
     * Finds the FIRST occurrence index of target when duplicates exist.
     * Uses Template 2 (low < high).
     *
     * @param arr sorted array with duplicates
     * @param target search key
     * @return first occurrence index or -1
     */
    public int findFirstOccurrence(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int low = 0;
        int high = arr.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid; // Keep mid as potential boundary answer!
            }
        }

        return (arr[low] == target) ? low : -1;
    }
}
```

> **Quick Syntax:**
```java
// Overflow-Safe Midpoint Expressions
int mid1 = low + (high - low) / 2; // Subtraction offset
int mid2 = (low + high) >>> 1;      // Bitwise unsigned shift
```

---

## 7. Concrete Problem Examples & Real-World Applications

1. **Database Indexing**:
   - Primary Key Lookups in Sorted B+ Tree Leaf Nodes ($O(\log N)$).

2. **Operating System Memory Allocation**:
   - Searching Free Memory Block Lists in Kernel Heap Allocators.

3. **Competitive Programming Benchmarks**:
   - LeetCode 704 (Binary Search), LeetCode 35 (Search Insert Position).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BinarySearchFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BINARY SEARCH FUNDAMENTALS DEMONSTRATION      ");
        System.out.println("=================================================\n");

        BinarySearchFundamentalsMaster master = new BinarySearchFundamentalsMaster();

        // 1. Exact Match Test
        int[] sortedArr = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
        int target = 23;
        int exactIdx = master.binarySearchExact(sortedArr, target);
        System.out.println("1. Exact Binary Search for " + target + " in " + Arrays.toString(sortedArr) + ":");
        System.out.println("   Found Index: " + exactIdx + " (Value = " + sortedArr[exactIdx] + ")");
        System.out.println("-------------------------------------------------");

        // 2. Bitwise Unsigned Shift Test
        int bitwiseIdx = master.binarySearchBitwise(sortedArr, target);
        System.out.println("2. Bitwise Unsigned Shift Search for " + target + ": Index = " + bitwiseIdx);
        System.out.println("-------------------------------------------------");

        // 3. First Occurrence Test (With Duplicates)
        int[] dupArr = {1, 2, 2, 2, 3, 4, 5};
        int dupTarget = 2;
        int firstIdx = master.findFirstOccurrence(dupArr, dupTarget);
        System.out.println("3. First Occurrence Search for " + dupTarget + " in " + Arrays.toString(dupArr) + ":");
        System.out.println("   First Index: " + firstIdx);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Binary Search Template | Time Complexity | Auxiliary Space | Mid Assignment | Loop Condition | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Template 1 (Exact)** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | `high = mid - 1` | `while (low <= high)` | Exact Value Search |
| **Template 2 (Boundary)**| $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | `high = mid` | `while (low < high)` | First/Last Boundary |
| **Template 3 (Window)**  | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | Check `low, high` | `while (low+1 < high)`| 2-Element Window |

---

## 10. Edge Cases & Boundary Handling

1. **Searching Array of Size 1 ($N = 1$)**:
   - Handled by `low = 0, high = 0`. Loop `while (low <= high)` runs once and evaluates `mid = 0`.

2. **Target Smaller Than All Elements**:
   - `high` decreases to `-1`. Loop terminates with `low = 0, high = -1`. Returns `-1`.

3. **Target Larger Than All Elements**:
   - `low` increases to $N$. Loop terminates with `low = N, high = N - 1`. Returns `-1`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Integer Overflow in Mid Calculation**:
  ```java
  // BAD: Integer overflow when low + high > 2,147,483,647!
  int mid = (low + high) / 2;
  
  // GOOD: Subtraction offset or bitwise unsigned shift!
  int mid = low + (high - low) / 2; // OR (low + high) >>> 1 ⚡
  ```

* **Anti-Pattern 2: Infinite Loop via Mis-Matched Template Assignments**:
  - Combining `while (low < high)` with `low = mid` without upper mid rounding causes infinite loops when `high - low == 1`.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Matching Loop Condition with Interval Assignments:
> * If loop is `while (low <= high)` $\implies$ Use `low = mid + 1` AND `high = mid - 1`.
> * If loop is `while (low < high)`  $\implies$ Use `low = mid + 1` AND `high = mid`.
> Mixing these two conventions is the #1 cause of off-by-one infinite loops in interview coding! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Iterative Binary Search | Recursive Binary Search |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\log N)$ Logarithmic ⚡** | **$O(\log N)$ Logarithmic ⚡** |
| **Auxiliary Memory** | **$O(1)$ Zero Extra Memory ⚡**| $O(\log N)$ Stack Frames |
| **Production Preference**| **Standard (No Stack Risk) ⚡**| Academic Demonstration |

---

## 14. How to Recognize This in Questions

* **"Search element in sorted array in O(log N) time"** $\rightarrow$ Template 1 Binary Search.
* **"Find first occurrence of key in array with duplicates"** $\rightarrow$ Template 2 Binary Search.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does `(low + high) >>> 1` prevent integer overflow?**  
  *A:* The logical unsigned right shift operator `>>>` zero-fills the most significant sign bit (MSB), treating the sum as an unsigned 32-bit integer ($0 \dots 4,294,967,295$).

* **Q: What is the maximum number of comparisons for Binary Search on 1,000,000 elements?**  
  *A:* $\lfloor \log_2 (1,000,000) \rfloor + 1 = 19 + 1 = \mathbf{20 \text{ comparisons max}}$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY SEARCH FUNDAMENTALS                            |
+-----------------------------------------------------------------------+
| • Search Invariant : Target lies in inclusive interval [low, high]     |
| • Mid Formula     : mid = low + (high - low) / 2 OR (low + high) >>> 1|
| • Template 1      : while (low <= high) -> low = mid + 1, high = mid - 1|
| • Template 2      : while (low < high)  -> low = mid + 1, high = mid    |
| • Comparisons     : Max log2(N) + 1 comparisons | O(log N) Time ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Template 1 exact match Binary Search in Java.
- [ ] I can write overflow-safe midpoint expressions (`low + (high - low) / 2` and `(low + high) >>> 1`).
- [ ] I can explain the 32-bit integer overflow bug in binary search.
- [ ] I can write Template 2 boundary Binary Search to find the first occurrence of a key.
- [ ] I can prove that Binary Search performs at most $\lfloor \log_2 N \rfloor + 1$ comparisons.
