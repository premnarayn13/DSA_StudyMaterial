# 16. Master Reference — Arrays

## 1. Introduction
This Master Reference consolidates all core principles, memory formulas, algorithmic patterns, shifting rules, and Java syntax templates for **Chapter 4: Arrays**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh array memory arithmetic, shifting loop directions, 2D matrix transformations, and pattern recognition triggers.

## 2. Core Concepts & Formulas Cheat Sheet
* **Hardware Pointer Arithmetic**: $\text{Address}(\text{arr}[i]) = B + (i \times S)$
* **Row-Major 2D Mapping**: $\text{Address}(\text{matrix}[r][c]) = B + (r \times C + c) \times S$
* **2D Matrix Flattening**: $\text{index1D} = r \times C + c \implies r = \text{index1D} / C, c = \text{index1D} \% C$
* **2D Matrix Binary Search Midpoint**: `matrix[mid / C][mid % C]`
* **1-Indexed Prefix Range Sum**: $\text{Sum}(L, R) = \text{prefix}[R + 1] - \text{prefix}[L]$
* **Difference Array Range Update**: `D[L] += V` and `if (R + 1 < N) D[R + 1] -= V`
* **Right Rotation (3-Step Reversal)**: `Reverse(0, n-k-1)` $\to$ `Reverse(n-k, n-1)` $\to$ `Reverse(0, n-1)`
* **Kadane's Recurrence**: `currentSum = Math.max(nums[i], currentSum + nums[i])`

> **Memory Trick:** **"Insertion = Shift Right (Right-to-Left Loop); Deletion = Shift Left (Left-to-Right Loop)"**.

## 3. Master Array Algorithm Complexity Table
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Triggers / Use Case |
| :--- | :--- | :--- | :--- |
| **Array Access by Index** | $O(1)$ | $O(1)$ | Direct hardware base pointer arithmetic |
| **Unsorted Linear Search** | $O(N)$ | $O(1)$ | Sequential element comparison |
| **Binary Search (Sorted)** | $O(\log N)$ | $O(1)$ | `mid = left + (right - left) / 2` |
| **3-Step Array Rotation** | $O(N)$ | $O(1)$ | In-place rotation by $K$ steps |
| **Prefix Sum Range Query** | $O(1)$ query | $O(N)$ precompute | Static array range sum queries |
| **Difference Array Updates** | $O(1)$ update | $O(N)$ build | $Q$ range additions $[L, R, V]$ |
| **Kadane's Algorithm** | $O(N)$ | $O(1)$ | Maximum contiguous subarray sum |
| **Frequency Array (`int[26]`)**| $O(N)$ | $O(1)$ | Bounded character counting |
| **Coordinate Compression** | $O(N \log N)$ | $O(N)$ | Large / Negative values mapped to ranks |
| **Staircase Matrix Search** | $O(R + C)$ | $O(1)$ | Search in row & col sorted matrix |
| **Spiral Matrix Traversal** | $O(R \cdot C)$ | $O(1)$ | 4 shrinking boundary pointers |
| **Cyclic Sort** | $O(N)$ | $O(1)$ | Values in range $1 \dots N$ |

## 4. Hardware & Memory Footprint Summary
```
+-----------------------------------------------------------------------------------+
| Data Structure              | Base Header | Pointer Overhead | Element Size (100) |
+-----------------------------------------------------------------------------------+
| int[100] (Primitive Array)  | 16 Bytes    | 0 Bytes          | 416 Bytes (Fast⚡)|
| Integer[100] (Object Array) | 16 Bytes    | 8 Bytes/ref      | 3,216 Bytes (Slow)|
| ArrayList<Integer> (100)    | 24 Bytes    | 8 Bytes/ref      | 3,240 Bytes       |
+-----------------------------------------------------------------------------------+
```

## 5. Java Code Templates & Snippets

> **Quick Syntax:**
```java
// 1. Safe Midpoint
int mid = left + (right - left) / 2;

// 2. Normalize Rotation
int k = rawK % n;

// 3. Subarray Sum Equals K (Prefix + HashMap)
long target = currentPrefixSum - k;
if (map.containsKey(target)) count += map.get(target);

// 4. Matrix Transpose & 90° Clockwise Rotation
// Transpose: Swap matrix[i][j] with matrix[j][i] for j > i
// Rotate 90° Clockwise: Transpose -> Reverse Each Row

// 5. Staircase Search (Top-Right Start)
int r = 0, c = C - 1;
while (r < R && c >= 0) {
    if (matrix[r][c] == target) return true;
    if (matrix[r][c] > target) c--;
    else r++;
}
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: Shifting Direction Error**: Right shifting for insertion MUST loop right-to-left (`i = size-1` down to `index`).
* **Trap 2: `Integer.MIN_VALUE` Subtraction**: Never use `a - b` in Comparators! Use `Integer.compare(a, b)`.
* **Trap 3: Negative Numbers in Sliding Window**: Sliding window fails when negative numbers exist; use Prefix Sum + HashMap!
* **Trap 4: All Negative Numbers in Kadane's**: Initialize `currentSum = nums[0]` and `maxSum = nums[0]` to handle negative arrays.
* **Trap 5: XOR Swap Same Index Bug**: XOR swap zeroes out the element if `i == j`. Use standard temp variable.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 4 (ARRAYS)                       |
+-----------------------------------------------------------------------+
| 1. Address(i) = Base + (i * S) -> O(1) Access                         |
| 2. Matrix 2D -> 1D: r * C + c | Binary Search 2D: matrix[mid/C][mid%C]|
| 3. Prefix Sum: Range sum = prefix[R + 1] - prefix[L]                  |
| 4. Difference Array: D[L] += V, D[R + 1] -= V                         |
| 5. Kadane: currentSum = Math.max(nums[i], currentSum + nums[i])        |
| 6. Rotation (Right K): Reverse(0, n-k-1) -> Reverse(n-k, n-1) -> Rev All|
| 7. Matrix 90° Clockwise: Transpose -> Reverse Rows                   |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write array range reversal, rotation, and insertion shifting from memory.
- [ ] I can implement 1-indexed Prefix Sum and Difference Array range updates.
- [ ] I can write Kadane's Algorithm handling all-negative arrays.
- [ ] I can implement 2D Matrix Staircase Search and Spiral Traversal.
- [ ] I can solve missing/duplicate number problems using Cyclic Sort.
