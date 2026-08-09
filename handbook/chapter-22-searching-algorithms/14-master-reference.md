# 14. Master Reference — Searching Algorithms & Foundations

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, search space bounds, operational complexities, design patterns, and interview pitfalls for **Chapter 22: Searching Algorithms**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Search Problem Taxonomy, Sentinel Linear Search, Template 1 Exact Binary Search, Template 2 Lower/Upper Bounds, Search Insert Position (LeetCode 35), Range Boundaries (LeetCode 34), Peak Element Search (LeetCode 162), Rotated Sorted Array Search (LeetCode 33/81), Binary Search on Answer (LeetCode 875/1011/1552), 2D Matrix Search (LeetCode 74/240), Exponential Search, Interpolation Search, Dual Heap Stream Medians (LeetCode 295), and Branchless Low-Level Optimizations.

> **Important:** Review this master reference 15 minutes before an interview to refresh the 3 Binary Search Invariants, Midpoint Formulas (`low + (high - low) / 2` and `(low + high) >>> 1`), Lower Bound (`arr[mid] >= target`), Upper Bound (`arr[mid] > target`), Range Frequency (`upperBound - lowerBound`), Rotated Half Check (`nums[low] <= nums[mid]`), Binary Search on Answer Feasibility (`isPossible(mid)`), 2D Virtual Mapping (`mid / cols, mid % cols`), Top-Right Corner Staircase (`(0, cols - 1)`), and Interpolation Prediction Formula!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Search Predicate Invariant**:
  - $P(x)$ partitions domain into two contiguous regions: `[false, false, ..., true, true]`.
* **Overflow-Safe Midpoint Calculation**:
  - `mid = low + (high - low) / 2` OR `mid = (low + high) >>> 1`.
* **Sentinel Linear Loop Comparison Cut**:
  - `arr[n - 1] = target; while (arr[i] != target) i++; arr[n - 1] = last;` (Cuts loop bounds checks by 50%).
* **Lower Bound Equation (First Index $\ge$ Target)**:
  - `if (arr[mid] >= target) high = mid; else low = mid + 1;` (Returns index in $[0 \dots N]$).
* **Upper Bound Equation (First Index $>$ Target)**:
  - `if (arr[mid] > target) high = mid; else low = mid + 1;` (Returns index in $[0 \dots N]$).
* **Range Frequency Counting Formula**:
  - $\text{frequency}(\text{target}) = \text{upperBound}(\text{target}) - \text{lowerBound}(\text{target})$.
* **Rotated Sorted Half Identification**:
  - `if (nums[low] <= nums[mid])` $\implies$ Left half $[low \dots mid]$ is strictly sorted.
* **Integer Ceiling Division Formula**:
  - $\text{hours} = \frac{\text{pile} + \text{speed} - 1}{\text{speed}}$ (Avoids double floating-point conversion).
* **2D Matrix Virtual Index Mapping**:
  - $\text{row} = \text{mid} / \text{cols}, \quad \text{col} = \text{mid} \% \text{cols}$.
* **Interpolation Search Position Prediction**:
  - $\text{pos} = low + \left\lfloor \frac{\text{target} - \text{arr}[low]}{\text{arr}[high] - \text{arr}[low]} \times (high - low) \right\rfloor$.
* **Branchless Binary Search Shift**:
  - `low = (arr[mid] <= target) ? mid : low; size -= half;`.

```
Searching Master Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Search Paradigm   | Key Data Structure| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Exact Match BS**    | 1D Sorted Array   | `(low, high)`     | **$O(\log N)$ Log ⚡**|
| **Boundary Search**   | Lower/Upper Bound | `(low, high=N)`   | **$O(\log N)$ Log ⚡**|
| **Slope Predicate**   | Peak Search       | `nums[mid] < right`| **$O(\log N)$ Log ⚡**|
| **Rotated Array**     | Pivot Shift Check | `nums[low]<=mid`  | **$O(\log N)$ Log ⚡**|
| **Search on Answer**  | Candidate Range   | `isPossible(mid)` | **$O(N \log (\text{Range}))$ ⚡**|
| **2D Matrix Search**  | Virtual / Stairs  | `mid / cols`      | **$O(\log(MN))$ / $O(M+N)$⚡**|
| **Interpolation**     | Uniform Data      | Linear Predict    | **$O(\log(\log N))$ Ultra-Fast⚡**|
| **Stream Median**     | Dual Priority Q   | MaxHeap + MinHeap | **$O(1)$ Median Lookup ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Searching Algorithm / Pattern | Data Precondition | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Primary Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Linear Search** | Unordered | $\mathbf{O(1)}$ Constant | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | 2 comparisons / step |
| **Sentinel Linear Search** | Unordered | $\mathbf{O(1)}$ Constant | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | 1 comparison / step (50% cut) |
| **Move-to-Front Search**   | Temporal Locality | $\mathbf{O(1)}$ Amortized ⚡| $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | Shift found item to index 0 |
| **Exact Binary Search (704)**| Sorted Array | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `while (low <= high)` |
| **Lower Bound (Search Insert 35)**| Sorted Array | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `if (arr[mid] >= target) high = mid` |
| **Upper Bound Algorithm** | Sorted Array | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `if (arr[mid] > target) high = mid` |
| **Peak Element Search (162)**| Unsorted Slope | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `nums[mid] < nums[mid + 1]` |
| **Single Element Search (540)**| Sorted Pairs | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | Bitwise XOR `mid ^ 1` pairing |
| **Rotated Search I (33)**  | Rotated Unique | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `nums[low] <= nums[mid]` check |
| **Rotated Search II (81)** | Rotated Dups | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Avg | $O(N)$ (All Dups) | $\mathbf{O(1)}$ Iterative ⚡ | Shrink `low++ / high--` |
| **Find Minimum Rotated (153)**| Rotated Unique | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | `nums[mid] > nums[high]` |
| **Search on Answer (875)** | Candidate Range | $\mathbf{O(N)}$ Feasibility | $\mathbf{O(N \log R)}$ ⚡ | $\mathbf{O(N \log R)}$ ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | Helper `isPossible(mid)` |
| **Search 2D Matrix I (74)** | Fully Monotonic | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log(MN))}$ ⚡ | $\mathbf{O(\log(MN))}$ ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | Virtual 1D `mid / cols` |
| **Search 2D Matrix II (240)**| Row/Col Sorted | $\mathbf{O(1)}$ Constant | $\mathbf{O(M + N)}$ Linear ⚡| $\mathbf{O(M + N)}$ Linear ⚡| $\mathbf{O(1)}$ Iterative ⚡ | Top-Right Corner `(0, cols-1)` |
| **Exponential Search**    | Unbounded Stream | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log \text{Pos})}$ ⚡| $\mathbf{O(\log \text{Pos})}$ ⚡| $\mathbf{O(1)}$ Iterative ⚡ | Double index `i *= 2` |
| **Interpolation Search**  | Uniform Data | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log(\log N))}$⚡| $O(N)$ (Skewed data) | $\mathbf{O(1)}$ Iterative ⚡ | Linear proportion `pos` |
| **Dual Heap Stream Median**| Data Stream | $\mathbf{O(1)}$ Median ⚡ | $\mathbf{O(1)}$ Median ⚡ | $\mathbf{O(1)}$ Median ⚡ | $O(N)$ Heap Memory | MaxHeap (lower), MinHeap (upper) |
| **Branchless Binary Search**| Sorted Array | $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Iterative ⚡ | Zero branch mispredictions |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| L1 Cache Line & Memory Footprint Breakdown for Search Engines                     |
+-----------------------------------------------------------------------------------+
| CPU Cache Line Size                            : 64 Bytes (Stores 8 64-bit Longs / 16 Ints)|
| Small Array Threshold Optimization ($N \le 32$) : Linear Search beats Binary Search!|
| Branch Misprediction Penalty                   : 15 to 20 Clock Cycles per Flush  |
| Integer Division Cost (`/ 2`)                   : 10 to 12 Clock Cycles             |
| Bitwise Unsigned Right Shift (`>>> 1`)          : 1 Single Clock Cycle ⚡             |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Overflow-Safe Midpoint Expressions
> int mid1 = low + (high - low) / 2; // Subtraction offset
> int mid2 = (low + high) >>> 1;      // Bitwise unsigned shift
> 
> // 2. Lower Bound (First >= Target)
> if (arr[mid] >= target) high = mid; else low = mid + 1;
> 
> // 3. Upper Bound (First > Target)
> if (arr[mid] > target) high = mid; else low = mid + 1;
> 
> // 4. Peak Search Slope Predicate
> if (nums[mid] < nums[mid + 1]) low = mid + 1; else high = mid;
> 
> // 5. Rotated Array Sorted Half Check
> if (nums[low] <= nums[mid]) { /* Left Sorted */ } else { /* Right Sorted */ }
> 
> // 6. Find Minimum in Rotated Array
> if (nums[mid] > nums[high]) low = mid + 1; else high = mid;
> 
> // 7. Integer Ceiling Division Formula
> long hours = (pile + speed - 1) / speed;
> 
> // 8. 2D Matrix Virtual 1D Coordinate Mapping
> int val = matrix[mid / cols][mid % cols];
> 
> // 9. Interpolation Position Prediction Formula
> int pos = low + (int) (((double) (target - arr[low]) / (arr[high] - arr[low])) * (high - low));
> 
> // 10. Branchless Binary Search Conditional Assignment
> low = (arr[mid] <= target) ? mid : low; size -= half;
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Signed 32-Bit Integer Overflow in Mid Calculation**: Writing `(low + high) / 2` overflows when `low + high > 2,147,483,647`. Always use `low + (high - low) / 2` or `(low + high) >>> 1`.
* **Pitfall 2: Initializing `high = arr.length - 1` for Lower/Upper Bound**: Lower/Upper bound MUST initialize `high = arr.length` to allow returning index $N$ when all elements are smaller than target.
* **Pitfall 3: Comparing `nums[mid]` with `nums[low]` in Find Minimum**: In Find Minimum (LeetCode 153), comparing `nums[mid]` with `nums[low]` fails on un-rotated arrays like `[1, 2, 3]`. Always compare `nums[mid]` with `nums[high]`.
* **Pitfall 4: Initializing `low = 0` for Ship Package Capacity**: Ship capacity `low` MUST be initialized to $\max(weights)$ (heaviest single package). Setting `low = 0` causes capacity to fail fitting a single heavy package.
* **Pitfall 5: Starting Staircase Search at Top-Left Corner `(0, 0)`**: Starting at `(0, 0)` makes both right and down choices increase values, destroying directional elimination. Always start at Top-Right Corner `(0, cols - 1)`.
* **Pitfall 6: Floating-Point Division Truncation in Interpolation Formula**: Integer division `(target - arr[low]) / (arr[high] - arr[low])` truncates to 0. Always cast numerator to `(double)`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 22 (SEARCHING ALGORITHMS)        |
+-----------------------------------------------------------------------+
| 1. Mid Formula   : mid = low + (high - low) / 2 OR (low + high) >>> 1 |
| 2. Lower Bound   : First >= Target | Range [0 ... N] | high = arr.length|
| 3. Upper Bound   : First > Target  | Range [0 ... N] | high = arr.length|
| 4. Frequency     : Count = upperBound(target) - lowerBound(target)    |
| 5. Rotated Check : if (nums[low] <= nums[mid]) -> Left Half is Sorted!|
| 6. Find Minimum  : if (nums[mid] > nums[high]) low = mid + 1          |
| 7. BS on Answer  : Min Max -> First TRUE; Max Min -> Last TRUE        |
| 8. Matrix BS     : 74 -> Virtual mid / cols; 240 -> Top-Right (0, cols-1)|
| 9. Interpolation : pos = low + ((target-arr[low])/(arr[high]-arr[low]))*(high-low)|
| 10. Dual Heap    : MaxHeap (lower 50%), MinHeap (upper 50%) -> O(1) Median|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write overflow-safe Template 1 exact match Binary Search in Java.
- [ ] I can write `lowerBound` (First $\ge$) and `upperBound` (First $>$) with `high = arr.length`.
- [ ] I can calculate $O(\log N)$ frequency counting using `upperBound - lowerBound`.
- [ ] I can solve LeetCode 35 (`Search Insert Position`) and LeetCode 34 (`First and Last Position`).
- [ ] I can write LeetCode 162 (`Find Peak Element`) using slope comparisons `nums[mid] < nums[mid+1]`.
- [ ] I can write LeetCode 540 (`Single Element in Sorted Array`) using `mid ^ 1` bitwise XOR pairing.
- [ ] I can write LeetCode 33 (`Search in Rotated Sorted Array`) using sorted half checks `nums[low] <= nums[mid]`.
- [ ] I can write LeetCode 153 (`Find Minimum in Rotated Sorted Array`) by comparing `nums[mid]` with `nums[high]`.
- [ ] I can solve LeetCode 875 (`Koko Eating Bananas`) and LeetCode 1011 (`Capacity To Ship Packages`).
- [ ] I can solve LeetCode 1552 (`Magnetic Force Between Two Balls / Aggressive Cows`).
- [ ] I can write LeetCode 74 (`Search 2D Matrix I`) using virtual 1D `mid / cols` mapping.
- [ ] I can write LeetCode 240 (`Search 2D Matrix II`) using top-right corner staircase scanning.
- [ ] I can write Exponential Search for unbounded streams ($O(\log \text{Pos})$).
- [ ] I can write Interpolation Search ($O(\log(\log N))$) with double precision casting.
- [ ] I can write LeetCode 295 (`Find Median from Data Stream`) using Dual Heaps.
- [ ] I can write Branchless Binary Search and $N \le 32$ small-array hybrid linear fallback.
