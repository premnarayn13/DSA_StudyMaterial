# 05. Pair Problems, Sum Target Optimization & Square Sorting Mechanics

## 1. Introduction
Pair problems represent the foundational class of Two-Pointer applications on linear data structures. Given a sorted or sortable sequence, finding element pairs that satisfy sum constraints—such as **Two Sum II (LeetCode 167)**, **Count Pairs Whose Sum is Less than Target (LeetCode 2824)**, **Squares of a Sorted Array (LeetCode 977)**, and **Two Sum Less Than K (LeetCode 1099)**—can be solved in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** On a sorted array, if `nums[left] + nums[right] < target`, then `nums[left]` CANNOT form a valid sum with ANY element from index `left + 1` to `right`! This single comparison allows counting **`right - left` valid pairs instantaneously** or advancing `left++` in $O(1)$ time, bypassing $O(N^2)$ brute-force iteration!

```
Sorted Pair Search Mechanics:
+-----------------------------------------------------------------------------------+
| sum == target : Pair Found! Return [left + 1, right + 1] (or count pairs)         |
| sum < target  : Sum too small -> Advance left++ (or count = count + (right - left))|
| sum > target  : Sum too large -> Decrement right--                                |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Squares of a Sorted Array (LeetCode 977 - $O(N)$ Time, $O(N)$ Output Space)
Given an array `nums` sorted in non-decreasing order containing negative and positive integers:
* Squaring negative numbers makes them positive, creating a V-shaped sequence where the largest squared values reside at the extreme boundaries (`left = 0` or `right = N - 1`).
* **Algorithm**:
  1. `left = 0`, `right = N - 1`, `p = N - 1`.
  2. Create output array `int[] result = new int[N]`.
  3. While `left <= right`:
     - Compare squared absolute values: `sqLeft = nums[left] * nums[left]`, `sqRight = nums[right] * nums[right]`.
     - If `sqLeft > sqRight`: `result[p--] = sqLeft; left++;`
     - Else: `result[p--] = sqRight; right--;`
  4. Return `result`.

```
Squares of Sorted Array Tracing [ -4, -1, 0, 3, 10 ]:
sqLeft = 16, sqRight = 100 -> Put 100 at end. right--.
sqLeft = 16, sqRight = 9   -> Put 16 at end-1. left++.
sqLeft = 1,  sqRight = 9   -> Put 9 at end-2.  right--.
sqLeft = 1,  sqRight = 0   -> Put 1 at end-3.  left++.
sqLeft = 0,  sqRight = 0   -> Put 0 at end-4.  left++.

Result: [ 0, 1, 9, 16, 100 ] ✅ (O(N) Single Pass!)
```

### 2.2 Count Pairs Whose Sum is Less Than Target (LeetCode 2824)
Given a sorted list `nums` and a target `target`:
1. `left = 0`, `right = N - 1`, `count = 0`.
2. While `left < right`:
   - If `nums[left] + nums[right] < target`:
     - Since `nums` is sorted, ALL elements between `left + 1` and `right` ALSO satisfy `nums[left] + nums[i] < target`!
     - Add **`count += (right - left)`** in $O(1)$ time!
     - `left++`.
   - Else (`nums[left] + nums[right] >= target`):
     - `right--`.
3. Return `count`.

> **Memory Trick:** **"Count Pairs < Target: If sum < target, add ALL (right - left) valid pairs at once and left++!"**

---

## 3. Characteristics & Two Sum Less Than K (LeetCode 1099)

### 3.1 Two Sum Less Than K (LeetCode 1099)
Given an array `nums` and integer $K$, find the maximum pair sum `nums[i] + nums[j] < K` (where $i \ne j$):
1. Sort `nums` in ascending order: `Arrays.sort(nums)` ($O(N \log N)$ time).
2. `left = 0`, `right = N - 1`, `maxSum = -1`.
3. While `left < right`:
   - `sum = nums[left] + nums[right]`.
   - If `sum < K`:
     - `maxSum = Math.max(maxSum, sum);`
     - `left++;`
   - Else (`sum >= K`):
     - `right--;`
4. Return `maxSum`.

---

## 4. Internal Working Mechanics
Tracing Count Pairs Less Than Target (LeetCode 2824) on `nums = [-1, 1, 2, 3, 1]`, `target = 2`:

```
Step 1: Sort nums -> [-1, 1, 1, 2, 3]
Init: left = 0 (val -1), right = 4 (val 3), count = 0

Pass 1: sum = -1 + 3 = 2 >= target (2).
        sum not < target -> right-- (right = 3, val 2).

Pass 2: sum = -1 + 2 = 1 < target (2).
        Pairs starting at left(-1): (-1, 1), (-1, 1), (-1, 2) -> (right - left = 3 - 0 = 3) pairs!
        count += 3 -> count = 3. left++ (left = 1, val 1).

Pass 3: sum = 1 + 2 = 3 >= target (2).
        right-- (right = 2, val 1).

Pass 4: sum = 1 + 1 = 2 >= target (2).
        right-- (right = 1). Loop terminates (left == right).

Total Valid Pairs Count = 3 ✅ (O(N log N) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Count Pairs Less Than Target Range Accumulation Topography:

```
Sorted Array:   [ -1,   1,   1,   2,   3 ]
                   ^              ^
                 left           right
                 sum = -1 + 2 = 1 < target (2)

Pairs added: (-1, 1@idx1), (-1, 1@idx2), (-1, 2@idx3)
Count Added: (right - left) = 3 - 0 = 3 pairs in O(1) step!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Squares of a Sorted Array (LeetCode 977), Count Pairs Less Than Target (LeetCode 2824), Two Sum Less Than K (LeetCode 1099), and Two Sum II (LeetCode 167):

```java
import java.util.*;

public class PairProblemsMaster {

    // 1. Squares of a Sorted Array (LeetCode 977) O(N) Time, O(N) Output Space
    public static int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        int left = 0;
        int right = n - 1;
        int p = n - 1;

        while (left <= right) {
            int sqLeft = nums[left] * nums[left];
            int sqRight = nums[right] * nums[right];

            if (sqLeft > sqRight) {
                result[p--] = sqLeft;
                left++;
            } else {
                result[p--] = sqRight;
                right--;
            }
        }

        return result;
    }

    // 2. Count Pairs Whose Sum is Less than Target (LeetCode 2824) O(N log N) Time, O(1) Space
    public static int countPairs(List<Integer> nums, int target) {
        Collections.sort(nums); // Sort in ascending order
        int left = 0;
        int right = nums.size() - 1;
        int count = 0;

        while (left < right) {
            if (nums.get(left) + nums.get(right) < target) {
                // All elements between left+1 and right form valid pairs with left!
                count += (right - left);
                left++;
            } else {
                right--;
            }
        }

        return count;
    }

    // 3. Two Sum Less Than K (LeetCode 1099) O(N log N) Time, O(1) Auxiliary Space
    public static int twoSumLessThanK(int[] nums, int k) {
        Arrays.sort(nums);
        int left = 0;
        int right = nums.length - 1;
        int maxSum = -1;

        while (left < right) {
            int sum = nums[left] + nums[right];
            if (sum < k) {
                maxSum = Math.max(maxSum, sum);
                left++;
            } else {
                right--;
            }
        }

        return maxSum;
    }

    // 4. Two Sum II - Input Array Is Sorted (LeetCode 167) O(N) Time, O(1) Space
    public static int[] twoSum(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) {
                return new int[]{left + 1, right + 1};
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }

        return new int[]{-1, -1};
    }
}
```

> **Quick Syntax:**
```java
// Range Pair Counting Syntax
if (nums[left] + nums[right] < target) {
    count += (right - left); // Instant range accumulation!
    left++;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 977 - Squares of a Sorted Array**: 2-pointer absolute value comparison.
* **LeetCode 2824 - Count Pairs Whose Sum is Less than Target**: $O(1)$ range accumulation.
* **LeetCode 1099 - Two Sum Less Than K**: Max bounded pair sum search.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Squares of Sorted Array, Count Pairs Less Than Target, and Two Sum Less Than K:

```java
public class PairProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Squares of Sorted Array (LeetCode 977) ===");
        int[] nums1 = {-4, -1, 0, 3, 10};
        int[] sq = PairProblemsMaster.sortedSquares(nums1);
        System.out.println("Sorted Squares: " + Arrays.toString(sq)); // Output: [0, 1, 9, 16, 100]

        System.out.println("\n=== 2. Count Pairs Less Than Target (LeetCode 2824) ===");
        List<Integer> nums2 = Arrays.asList(-1, 1, 2, 3, 1);
        int validPairs = PairProblemsMaster.countPairs(nums2, 2);
        System.out.println("Valid Pairs Count (target=2): " + validPairs); // Output: 3

        System.out.println("\n=== 3. Two Sum Less Than K (LeetCode 1099) ===");
        int[] nums3 = {34, 23, 1, 24, 75, 33, 54, 8};
        int maxKSum = PairProblemsMaster.twoSumLessThanK(nums3, 60);
        System.out.println("Max Pair Sum < 60: " + maxKSum); // Output: 58 (34 + 24)
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Sorted Squares (977)**| **$O(N)$ Linear ⚡** | $O(N)$ Output Array | Fill result array from right to left |
| **Count Pairs (2824)** | **$O(N \log N)$ Sort ⚡**| **$O(1)$ Strict In-Place ⚡**| $O(1)$ range addition `count += right - left` |
| **Two Sum < K (1099)** | **$O(N \log N)$ Sort ⚡**| **$O(1)$ Strict In-Place ⚡**| Converging two pointers |

---

## 10. Edge Cases & Boundary Handling
* **Array With Negative Numbers in Squares Problem**: Handled cleanly by comparing squared absolute values `sqLeft` vs `sqRight`.
* **No Valid Pair Sum Less Than K**: Returns `-1` initialized state cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Iterating Pairs One-by-One in Range Counting Problems ($O(N^2)$ Penalty)**:
  - When `nums[left] + nums[right] < target`, writing an inner loop to count each pair individually degrades performance to $O(N^2)$!
  - **Add `count += (right - left)` instantaneously in $O(1)$ time**.
* **Filling Squares Array Left-to-Right**:
  - Smallest squared values reside in the middle, while largest squared values reside at the extremes.
  - **Fill the output array from right to left (`p = N - 1` down to `0`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `count += (right - left)` Works Instantaneously:
> In a sorted array, if `nums[left] + nums[right] < target`, any element `nums[i]` where `left < i <= right` is $\le \text{nums}[right]$.
> Therefore `nums[left] + nums[i] < target` is GUARANTEED to hold for all $i \in [\text{left}+1 \dots \text{right}]$.
> There are exactly `right - left` such elements!

> **Memory Trick:** **"Range counting in sorted arrays: add (right - left) in O(1) time!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Range Accumulation | Brute-Force Pair Scan |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \log N)$ ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(1)$ |
| **Code Efficiency** | 10 Lines | 15 Lines |

---

## 14. How to Recognize This in Questions
* **"Find squares of sorted array in non-decreasing order in O(N) time"** $\rightarrow$ LeetCode 977 (2-pointer fill from right to left).
* **"Count pairs whose sum is strictly less than target"** $\rightarrow$ LeetCode 2824 (`count += right - left`).
* **"Find max sum of two numbers less than K"** $\rightarrow$ LeetCode 1099.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Squares of a Sorted Array fill the result array from index $N-1$ down to $0$?**  
  *A:* Because squaring negative numbers turns them positive, creating a V-shaped parabola where the largest squared values appear at the array boundaries (`left` and `right`). Placing the maximum of `sqLeft` and `sqRight` at index $p--$ populates the result in sorted order.
* **Q: Does sorting an unsorted array before applying two pointers preserve original indices?**  
  *A:* No! Sorting alters array indices. If original 0-indexed positions are required (as in standard Two Sum), a Hash Map MUST be used unless index-value pair tuples are sorted explicitly.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO POINTER PAIR PROBLEMS & SUM TARGETS               |
+-----------------------------------------------------------------------+
| • Sorted Squares (977): Compare sqLeft vs sqRight; fill result right-to-left|
| • Count Pairs < Target (2824): Sort first; if sum < target add (right-left)|
| • Two Sum < K (1099): Track maxSum = max(maxSum, sum) when sum < K     |
| • Two Sum II (167): Return [left+1, right+1] on exact sum match       |
| • Complexity: O(N) Time for sorted inputs; O(N log N) if sorting needed|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Squares of Sorted Array (LeetCode 977) in $O(N)$ time.
- [ ] I can derive why filling result array right-to-left is required in 977.
- [ ] I can solve Count Pairs Less Than Target (LeetCode 2824) using `count += right - left`.
- [ ] I can solve Two Sum Less Than K (LeetCode 1099).
- [ ] I know when sorting an array invalidates original element index queries.
