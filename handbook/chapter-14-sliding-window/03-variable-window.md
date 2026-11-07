# 03. Variable-Size Shrinkable Windows, Subarray Product Counting & Threshold Bounds

## 1. Introduction
The **Variable-Size Shrinkable Sliding Window Pattern** is a core algorithmic strategy used to find optimal contiguous subarrays or substrings—specifically **Longest Valid Substrings** or **Shortest Valid Subarrays**—where the window length expands and shrinks dynamically. Problems like **Subarray Product Less Than K (LeetCode 713)**, **Minimum Size Subarray Sum (LeetCode 209)**, and **Longest Substring Without Repeating Characters (LeetCode 3)** are solved in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** In **Subarray Product Less Than K (LeetCode 713)**, when a valid window `[left ... right]` has a product strictly less than $K$, the number of contiguous valid subarrays ENDING at index `right` is **EXACTLY `right - left + 1`**! Adding `right - left + 1` to the answer on every step counts all valid contiguous sub-segments in $O(1)$ constant time!

```
Variable Window Expansion-Shrink Mechanics:
+-----------------------------------------------------------------------------------+
| Expand Phase : Advance right pointer (`right++`), update window product/sum state  |
| Shrink Phase : While state is invalid (`product >= K` or `sum >= Target`):        |
|                Remove arr[left] state, advance left pointer (`left++`)            |
| Count Add Phase: Valid window [left..right] adds (right - left + 1) subarrays ⚡  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Subarray Product Counting (LeetCode 713)

### 2.1 Subarray Product Less Than K (LeetCode 713)
Given an array of positive integers `nums` and integer $K$, return the number of contiguous subarrays where the product of all elements is strictly less than $K$:

1. If $K \le 1$, return `0` (Since all `nums[i] >= 1`, product can never be strictly $< 1$).
2. Initialize `left = 0`, `currentProduct = 1`, `count = 0`.
3. Iterate `right` from `0` to $N - 1$:
   - **Expand Window**: Multiply `currentProduct *= nums[right]`.
   - **Shrink Window**: While `currentProduct >= K && left <= right`:
     - Divide `currentProduct /= nums[left]`.
     - `left++`.
   - **Instant Count Addition**: Add **`count += (right - left + 1)`**!
4. Return `count`.

```
Why (right - left + 1) Counts All Valid Subarrays Ending at Right:
For window [left ... right] = [10, 5, 2] (right = 2, left = 0):
The contiguous subarrays ending at index 2 are:
1. [ 2 ]            (Length 1)
2. [ 5, 2 ]         (Length 2)
3. [ 10, 5, 2 ]     (Length 3)
Total valid new subarrays ending at right = right - left + 1 = 2 - 0 + 1 = 3! ⚡
```

> **Memory Trick:** **"Subarray Product < K: While product >= K, divide by nums[left] and left++! Add (right - left + 1) to count!"**

---

## 3. Characteristics & Minimum Size Subarray Sum (LeetCode 209)

### 3.1 Minimum Size Subarray Sum (LeetCode 209 - Shortest Window Search)
Given an array of positive integers `nums` and target `target`, find the minimal length of a contiguous subarray whose sum is $\ge \text{target}$:
* **Shortest Window Dynamic**:
  1. `left = 0`, `currentSum = 0`, `minLen = Integer.MAX_VALUE`.
  2. For `right = 0` to $N - 1$:
     - `currentSum += nums[right]`.
     - While `currentSum >= target`:
       - `minLen = Math.min(minLen, right - left + 1);`
       - `currentSum -= nums[left];`
       - `left++;`
  3. Return `minLen == Integer.MAX_VALUE ? 0 : minLen`.

```
Longest vs Shortest Variable Window Update Rules:
Longest Window  : Record answer AFTER shrink loop (when window becomes VALID again).
Shortest Window : Record answer INSIDE shrink loop (while window remains VALID).
```

---

## 4. Internal Working Mechanics
Tracing Subarray Product Less Than K (LeetCode 713) on `nums = [10, 5, 2, 6]`, $K = 100$:

```
Init: left = 0, currentProduct = 1, count = 0

right = 0 (val 10): currentProduct = 10 < 100.
  - Add (right - left + 1) = 0 - 0 + 1 = 1 subarray ([10]).
  - count = 1.

right = 1 (val 5) : currentProduct = 10 * 5 = 50 < 100.
  - Add (right - left + 1) = 1 - 0 + 1 = 2 subarrays ([5], [10, 5]).
  - count = 1 + 2 = 3.

right = 2 (val 2) : currentProduct = 50 * 2 = 100 >= 100!
  - Shrink loop: currentProduct /= nums[left] (10) -> currentProduct = 10. left = 1.
  - Now currentProduct (10) < 100.
  - Add (right - left + 1) = 2 - 1 + 1 = 2 subarrays ([2], [5, 2]).
  - count = 3 + 2 = 5.

right = 3 (val 6) : currentProduct = 10 * 6 = 60 < 100.
  - Add (right - left + 1) = 3 - 1 + 1 = 3 subarrays ([6], [2, 6], [5, 2, 6]).
  - count = 5 + 3 = 8.

Total Valid Subarrays = 8 ✅ (O(N) Single Pass!)
```

---

## 5. Visual Diagram
Subarray Product Contiguous Subsegment Inclusion Topography:

```
Window [ 10,  5,  2 ] (left = 0, right = 2):
                          Subarrays ending at right (2):
                          - [ 2 ]
                          - [ 5, 2 ]
                          - [ 10, 5, 2 ]
Total Added: (2 - 0 + 1) = 3 Subarrays!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Subarray Product Less Than K (LeetCode 713), Minimum Size Subarray Sum (LeetCode 209), and Max Consecutive Ones III (LeetCode 1004):

```java
import java.util.*;

public class VariableWindowMaster {

    // 1. Subarray Product Less Than K (LeetCode 713) O(N) Time, O(1) Space
    public static int numSubarrayProductLessThanK(int[] nums, int k) {
        if (k <= 1 || nums == null || nums.length == 0) return 0;

        int left = 0;
        long currentProduct = 1;
        int count = 0;

        for (int right = 0; right < nums.length; right++) {
            currentProduct *= nums[right];

            // Shrink window while product >= k
            while (currentProduct >= k && left <= right) {
                currentProduct /= nums[left];
                left++;
            }

            // Count all valid contiguous subarrays ending at right index
            count += (right - left + 1);
        }

        return count;
    }

    // 2. Minimum Size Subarray Sum (LeetCode 209) O(N) Time, O(1) Space
    public static int minSubArrayLen(int target, int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int left = 0;
        long currentSum = 0;
        int minLen = Integer.MAX_VALUE;

        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];

            // Shrink window while sum >= target
            while (currentSum >= target) {
                minLen = Math.min(minLen, right - left + 1);
                currentSum -= nums[left];
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }

    // 3. Max Consecutive Ones III (LeetCode 1004) O(N) Time, O(1) Space
    public static int longestOnes(int[] nums, int k) {
        int left = 0;
        int zeroCount = 0;
        int maxLen = 0;

        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) {
                zeroCount++;
            }

            // Shrink window if zero count exceeds allowed flip quota k
            while (zeroCount > k) {
                if (nums[left] == 0) {
                    zeroCount--;
                }
                left++;
            }

            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}
```

> **Quick Syntax:**
```java
// Subarray Count Addition Formula
count += (right - left + 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 713 - Subarray Product Less Than K**: Product shrinkage + `right - left + 1` addition.
* **LeetCode 209 - Minimum Size Subarray Sum**: Shortest window shrink loop.
* **LeetCode 1004 - Max Consecutive Ones III**: Zero flip quota window expansion.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Subarray Product Less Than K, Min Subarray Sum, and Max Consecutive Ones III:

```java
public class VariableWindowDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Subarray Product Less Than K (LeetCode 713, K=100) ===");
        int[] nums1 = {10, 5, 2, 6};
        int count = VariableWindowMaster.numSubarrayProductLessThanK(nums1, 100);
        System.out.println("Valid Subarrays Count: " + count); // Output: 8

        System.out.println("\n=== 2. Minimum Size Subarray Sum (LeetCode 209, Target=7) ===");
        int[] nums2 = {2, 3, 1, 2, 4, 3};
        int minLen = VariableWindowMaster.minSubArrayLen(7, nums2);
        System.out.println("Minimum Subarray Length: " + minLen); // Output: 2 ([4, 3])

        System.out.println("\n=== 3. Max Consecutive Ones III (LeetCode 1004, K=2) ===");
        int[] nums3 = {1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0};
        int maxOnes = VariableWindowMaster.longestOnes(nums3, 2);
        System.out.println("Max Consecutive Ones (K=2 flips): " + maxOnes); // Output: 6
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Product < K (713)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `count += (right - left + 1)` addition |
| **Min Subarray Sum (209)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Record `minLen` inside shrink loop |
| **Max Ones III (1004)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `zeroCount > k` shrink condition |

---

## 10. Edge Cases & Boundary Handling
* **$K \le 1$ in Product Problem**: Returns `0` immediately (since positive integers cannot produce product $< 1$).
* **Target Sum Unreachable**: Returns `0` if total array sum is $< \text{target}$.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting $K \le 1$ Guard in LeetCode 713**:
  - If $K = 0$ or $K = 1$, executing the shrink `while (currentProduct >= K)` causes an **INFINITE LOOP** when `nums[left] == 1`!
  - **Always return 0 immediately if $K \le 1$**.
* **Recording Answer Outside Shrink Loop in Shortest Window Search**:
  - In Minimum Size Subarray Sum, recording `minLen` outside the shrink loop records an un-shrunk larger window length.
  - **Record shortest window length INSIDE the `while (currentSum >= target)` shrink loop**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Longest vs Shortest Window Recording Locations:
> * **Finding Longest Window (e.g. 3, 1004)**: Update `maxLen = Math.max(maxLen, right - left + 1)` AFTER the `while` shrink loop finishes.
> * **Finding Shortest Window (e.g. 209)**: Update `minLen = Math.min(minLen, right - left + 1)` INSIDE the `while` shrink loop before `left++`.

> **Memory Trick:** **"Longest window updates answer AFTER shrink loop! Shortest window updates answer INSIDE shrink loop!"**

---

## 13. System & Implementation Comparisons

| Feature | Sliding Window Subarray Counting | Brute-Force $O(N^2)$ Pair Check |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(1)$ |
| **Count Addition** | **$O(1)$ Range Addition `right - left + 1` ⚡**| Individual Subarray Iteration |

---

## 14. How to Recognize This in Questions
* **"Find number of contiguous subarrays where product is less than K"** $\rightarrow$ LeetCode 713 (`count += right - left + 1`).
* **"Find minimal length of contiguous subarray with sum >= target"** $\rightarrow$ LeetCode 209 (Shortest window shrink loop).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does adding `right - left + 1` count all valid subarrays ending at `right` in LeetCode 713?**  
  *A:* In a valid window `[left ... right]`, any contiguous sub-segment starting at index $x \in [\text{left} \dots \text{right}]$ and ending at `right` is a subset of the full window. Since all numbers are positive, a smaller sub-segment product is strictly $\le$ full window product $< K$. There are exactly `right - left + 1` such starting indices!
* **Q: Why MUST $K \le 1$ return 0 immediately in LeetCode 713?**  
  *A:* Since input array `nums` contains positive integers ($\ge 1$), the smallest possible product of 1 element is $\ge 1$. A product strictly $< 1$ or $< 0$ is mathematically impossible.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: VARIABLE-SIZE SHRINKABLE WINDOWS                      |
+-----------------------------------------------------------------------+
| • Product < K Rule (713): if (k <= 1) return 0; currentProduct *= nums[r]|
| • Product Shrink: while (currentProduct >= k && left <= right) div by nums[left]|
| • Instant Subarray Count: count += (right - left + 1)                 |
| • Shortest Window (209): Record minLen INSIDE while (sum >= target) loop|
| • Longest Window (1004): Record maxLen AFTER while (zeros > k) loop    |
| • Space Invariant: All variable window algorithms run in O(1) Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Subarray Product Less Than K (LeetCode 713) in under 3 minutes.
- [ ] I know why `right - left + 1` counts all valid subarrays ending at `right`.
- [ ] I know why $K \le 1$ MUST return 0 immediately in LeetCode 713.
- [ ] I can write Minimum Size Subarray Sum (LeetCode 209) in $O(N)$ time.
- [ ] I know where to record the answer for Longest vs Shortest window problems.
