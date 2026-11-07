# 04. Lower & Upper Bound Algorithms: Range Searching & Frequency Counting

## 1. Introduction
**Lower Bound** and **Upper Bound** algorithms are the fundamental building blocks of range searching, frequency counting, and boundary partitioning in sorted datasets. Inspired by C++ STL functions (`std::lower_bound` and `std::upper_bound`), these algorithms extend basic binary search to locate critical structural transition boundaries in $O(\log N)$ time:
* **Lower Bound**: The first index $i$ in $[0 \dots N]$ where $\text{arr}[i] \ge \text{target}$ (smallest index where value is NOT less than target).
* **Upper Bound**: The first index $i$ in $[0 \dots N]$ where $\text{arr}[i] > \text{target}$ (smallest index where value is GREATER than target).

Combining Lower and Upper Bounds solves range problems like **Search Insert Position (LeetCode 35)** and **Find First and Last Position of Element in Sorted Array (LeetCode 34)** in **$O(\log N)$ Time** and **$O(1)$ Space**.

> **Important:** Core Invariants of Lower Bound, Upper Bound & Range Frequency:
> 1. **Lower Bound Invariant**: First index $i$ satisfying $\text{arr}[i] \ge \text{target}$. If target is absent, returns the insertion index maintaining sorted order.
> 2. **Upper Bound Invariant**: First index $i$ satisfying $\text{arr}[i] > \text{target}$.
> 3. **Range Frequency Counting Formula**:
>    $$\text{frequency}(\text{target}) = \text{upper\_bound}(\text{target}) - \text{lower\_bound}(\text{target})$$
>    Calculates exact occurrence count of target in $O(\log N)$ time without linear scanning! ⚡

```
Lower Bound vs Upper Bound Boundary Topology:
Array:          [ 1,  2,  4,  4,  4,  5,  7 ]   Target = 4
Indices:          0   1   2   3   4   5   6   7 (Insertion Index N)
                          ^           ^
                     Lower Bound   Upper Bound
                     (index = 2)   (index = 5)

Frequency of 4 = Upper Bound (5) - Lower Bound (2) = 3 Occurrences! ⚡
```

---

## 2. Core Concepts & Boundary Operations Matrix

### 2.1 Lower Bound vs Upper Bound Strategy Matrix
```
Boundary Operations Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation             | Predicate Test $P(i)$| Return Boundary Condition| Search Condition|
+-----------------------+-------------------+-------------------+-------------------+
| **Lower Bound**       | $\text{arr}[i] \ge \text{target}$| First index where val $\ge$ target| `arr[mid] >= target`|
| **Upper Bound**       | $\text{arr}[i] > \text{target}$ | First index where val $>$ target| `arr[mid] > target`|
| **Search Insert (35)**| $\text{arr}[i] \ge \text{target}$| Identical to Lower Bound! | `arr[mid] >= target`|
| **First/Last (34)**   | Dual Bound Scan   | `[lower_bound, upper_bound - 1]`| Range Bounds |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Lower Bound: arr[mid] >= target (First >=); Upper Bound: arr[mid] > target (First >)!"**

---

## 3. Characteristics & $O(\log N)$ Range Frequency Proof

### 3.1 Mathematical Proof of $O(\log N)$ Range Frequency Counting
* Naive frequency counting locates target and scans linearly left/right, taking $O(N)$ worst-case time for array of identical values `[4, 4, 4, 4, 4]`.
* Lower Bound binary search takes $O(\log_2 N)$ steps.
* Upper Bound binary search takes $O(\log_2 N)$ steps.
* Total Frequency Calculation: $O(\log N) + O(\log N) = \mathbf{O(\log N) \text{ Time Complexity}}$. Auxiliary Space: $\mathbf{O(1) \text{ Constant Space}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Lower & Upper Bound

Tracing Lower and Upper Bound on `arr = [1, 2, 4, 4, 4, 5, 7]`, Target = `4`:

```
1. Trace Lower Bound (First index where val >= 4):
Init: low = 0, high = 7 (Size N).
- Step 1: mid = 3 (val = 4 >= 4) -> high = 3. Search range: [0 ... 3].
- Step 2: mid = 1 (val = 2 < 4)  -> low = 2.  Search range: [2 ... 3].
- Step 3: mid = 2 (val = 4 >= 4) -> high = 2. Search range: [2 ... 2].
Loop terminates (low == high == 2).
Lower Bound = Index 2! (Value = 4)

2. Trace Upper Bound (First index where val > 4):
Init: low = 0, high = 7.
- Step 1: mid = 3 (val = 4 <= 4) -> low = 4.  Search range: [4 ... 7].
- Step 2: mid = 5 (val = 5 > 4)  -> high = 5. Search range: [4 ... 5].
- Step 3: mid = 4 (val = 4 <= 4) -> low = 5.  Search range: [5 ... 5].
Loop terminates (low == high == 5).
Upper Bound = Index 5! (Value = 5)

Range Frequency = Upper Bound (5) - Lower Bound (2) = 3 Occurrences! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram: Search Range First and Last Index Mapping

```
Array:                 [ 1,  2,  4,  4,  4,  5,  7 ]
Indices:                 0   1   2   3   4   5   6   7

Lower Bound (val >= 4) --------> [2]  (First Occurrence Index!)
Upper Bound (val > 4)  --------------> [5]  (Exclusive Right Boundary!)

First Occurrence Index = Lower Bound = 2
Last Occurrence Index  = Upper Bound - 1 = 4 ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Lower Bound, Upper Bound, Search Insert Position (LeetCode 35), and Range Range Search (LeetCode 34).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Lower Bound, Upper Bound,
 * Range Frequency Counting, and Range Range Boundaries.
 */
public class LowerUpperBoundMaster {

    // =========================================================================
    // 1. LOWER BOUND ALGORITHM (First index where arr[i] >= target O(log N))
    // =========================================================================
    /**
     * Finds lower bound index (first element >= target).
     * Range: [0 ... N]. Returns N if all elements < target.
     *
     * @param arr sorted array
     * @param target search target
     * @return lower bound index
     */
    public int lowerBound(int[] arr, int target) {
        if (arr == null || arr.length == 0) return 0;

        int low = 0;
        int high = arr.length; // Exclusive upper range N!

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] >= target) {
                high = mid; // Candidate found, try finding earlier match
            } else {
                low = mid + 1; // Must search right half
            }
        }

        return low; // low == high
    }

    // =========================================================================
    // 2. UPPER BOUND ALGORITHM (First index where arr[i] > target O(log N))
    // =========================================================================
    /**
     * Finds upper bound index (first element > target).
     * Range: [0 ... N]. Returns N if all elements <= target.
     *
     * @param arr sorted array
     * @param target search target
     * @return upper bound index
     */
    public int upperBound(int[] arr, int target) {
        if (arr == null || arr.length == 0) return 0;

        int low = 0;
        int high = arr.length; // Exclusive upper range N!

        while (low < high) {
            int mid = low + (high - low) / 2;

            if (arr[mid] > target) {
                high = mid; // Candidate found, try finding earlier match
            } else {
                low = mid + 1; // Must search right half
            }
        }

        return low; // low == high
    }

    // =========================================================================
    // 3. SEARCH INSERT POSITION (LeetCode 35 O(log N))
    // =========================================================================
    /**
     * Returns index if target is found; otherwise returns insertion index.
     * Identical to lower bound!
     */
    public int searchInsert(int[] arr, int target) {
        return lowerBound(arr, target);
    }

    // =========================================================================
    // 4. FIND FIRST AND LAST POSITION (LeetCode 34 O(log N))
    // =========================================================================
    /**
     * Finds starting and ending position of target in sorted array.
     * Returns [-1, -1] if target absent.
     */
    public int[] searchRange(int[] arr, int target) {
        if (arr == null || arr.length == 0) return new int[]{-1, -1};

        int lb = lowerBound(arr, target);

        // Check if lower bound index is valid and equals target
        if (lb == arr.length || arr[lb] != target) {
            return new int[]{-1, -1}; // Target absent
        }

        int ub = upperBound(arr, target);

        return new int[]{lb, ub - 1}; // Last index is ub - 1
    }

    // =========================================================================
    // 5. O(log N) RANGE FREQUENCY COUNTING
    // =========================================================================
    /**
     * Calculates total occurrences of target in sorted array in O(log N) time.
     */
    public int countFrequency(int[] arr, int target) {
        if (arr == null || arr.length == 0) return 0;
        return upperBound(arr, target) - lowerBound(arr, target);
    }
}
```

> **Quick Syntax:**
```java
// Lower Bound vs Upper Bound Loop Lines
// Lower Bound (First >=): if (arr[mid] >= target) high = mid; else low = mid + 1;
// Upper Bound (First > ): if (arr[mid] > target)  high = mid; else low = mid + 1;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 35 - Search Insert Position**:
   - Direct Lower Bound calculation.

2. **LeetCode 34 - Find First and Last Position of Element**:
   - `first = lowerBound(target)`, `last = upperBound(target) - 1`.

3. **Database Range Queries**:
   - SQL `WHERE age BETWEEN 20 AND 30`: Returns `[lowerBound(20) ... upperBound(30) - 1]`.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class LowerUpperBoundDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   LOWER & UPPER BOUND ALGORITHMS DEMONSTRATION  ");
        System.out.println("=================================================\n");

        LowerUpperBoundMaster master = new LowerUpperBoundMaster();
        int[] arr = {1, 2, 4, 4, 4, 5, 7};
        int target = 4;

        // 1. Lower Bound & Upper Bound Tests
        int lb = master.lowerBound(arr, target);
        int ub = master.upperBound(arr, target);
        System.out.println("1. Array: " + Arrays.toString(arr) + ", Target = " + target);
        System.out.println("   Lower Bound Index (First >= 4): " + lb + " (Val = " + arr[lb] + ")");
        System.out.println("   Upper Bound Index (First > 4) : " + ub + " (Val = " + arr[ub] + ")");
        System.out.println("-------------------------------------------------");

        // 2. Frequency Count Test
        int freq = master.countFrequency(arr, target);
        System.out.println("2. Frequency Count of " + target + " (upper - lower): " + freq + " Occurrences");
        System.out.println("-------------------------------------------------");

        // 3. Search Range Test (LeetCode 34)
        int[] range = master.searchRange(arr, target);
        System.out.println("3. First and Last Position of " + target + ": " + Arrays.toString(range));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Boundary Algorithm | Time Complexity | Auxiliary Space | Search Range | Primary Function |
| :--- | :--- | :--- | :--- | :--- |
| **Lower Bound** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $[0 \dots N]$ | First index $\ge$ target |
| **Upper Bound** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $[0 \dots N]$ | First index $>$ target |
| **Search Insert (35)** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $[0 \dots N]$ | Insertion position |
| **Frequency Count** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $[0 \dots N]$ | `ub - lb` |

---

## 10. Edge Cases & Boundary Handling

1. **Target Less Than All Elements**:
   - `lowerBound` and `upperBound` return index `0`.

2. **Target Greater Than All Elements**:
   - `lowerBound` and `upperBound` return index `N` (length of array).
   - **Guard**: Initialize `high = arr.length` (NOT `arr.length - 1`) to allow returning index $N$ for insertion at end!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Initializing `high = arr.length - 1` in Lower/Upper Bound**:
  - Setting `high = arr.length - 1` prevents lower/upper bound from returning index $N$ when the target is larger than all array elements, breaking Search Insert Position for trailing insertions.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Range Bounds Search Invariant:
> To locate the exact occurrence range $[first, last]$ of a target in a sorted array:
> * `first = lowerBound(arr, target)`
> * `last  = upperBound(arr, target) - 1`
> * If `first == arr.length || arr[first] != target` $\implies$ Target does NOT exist in array! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Scan Range Search | Lower / Upper Bound Range Search |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ Worst Case | **$O(\log N)$ Logarithmic ⚡** |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| **$O(1)$ Constant Space ⚡** |
| **Duplicate Scale** | Heavy slowdown for duplicates | **Immune to duplicate frequency ⚡**|

---

## 14. How to Recognize This in Questions

* **"Find insertion index for target in sorted array"** $\rightarrow$ Lower Bound (LeetCode 35).
* **"Find starting and ending position of value in sorted array"** $\rightarrow$ Lower Bound + Upper Bound (LeetCode 34).
* **"Count total occurrences of target in sorted array in O(log N)"** $\rightarrow$ `upperBound - lowerBound`.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the relationship between Search Insert Position (LeetCode 35) and Lower Bound?**  
  *A:* They are identical! Both return the first index where $\text{arr}[i] \ge \text{target}$, which is the exact insertion index maintaining sorted order.

* **Q: Why does Upper Bound initialize `high = arr.length` instead of `arr.length - 1`?**  
  *A:* Because if all elements in the array are $\le \text{target}$, the upper bound boundary lies beyond the last index at position $N$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: LOWER & UPPER BOUND                                   |
+-----------------------------------------------------------------------+
| • Lower Bound : First index where arr[i] >= target (First >=)         |
| • Upper Bound : First index where arr[i] > target  (First > )         |
| • Range Search: First = lowerBound, Last = upperBound - 1             |
| • Frequency   : Count = upperBound(target) - lowerBound(target)       |
| • Range Init  : ALWAYS set high = arr.length to allow returning N! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write `lowerBound` in Java with `high = arr.length`.
- [ ] I can write `upperBound` in Java with `high = arr.length`.
- [ ] I can compute $O(\log N)$ frequency counting using `upperBound - lowerBound`.
- [ ] I can solve LeetCode 35 (`Search Insert Position`).
- [ ] I can solve LeetCode 34 (`Find First and Last Position of Element`).
