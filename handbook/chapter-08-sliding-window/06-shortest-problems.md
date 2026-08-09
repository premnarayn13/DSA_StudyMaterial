# 06. Shortest Window Problems, Target Sum Shrinking & Boundary Reduction

## 1. Introduction
The **Shortest Window Sub-category** of Sliding Window algorithms aims to find the minimal length contiguous subarray or substring that satisfies a given target constraint. Unlike Longest Window problems that record answers outside the shrink loop, Shortest Window problems—such as **Minimum Size Subarray Sum (LeetCode 209)**, **Minimum Window Substring (LeetCode 76)**, and **Minimum Operations to Reduce X to Zero (LeetCode 1658)**—aggressively shrink the window using a `while` loop, recording answer candidates **INSIDE the shrink loop while the window remains valid**.

> **Important:** The key architectural difference between Longest and Shortest window problems lies in **When to Record the Window Size**:
> * **Longest Window**: Record `maxLen` AFTER the `while` shrink loop (when window becomes valid).
> * **Shortest Window**: Record `minLen` INSIDE the `while` shrink loop (while window remains valid).

```
Shortest Window Shrink-Record Protocol:
+-----------------------------------------------------------------------------------+
| 1. Expand Window : Advance right, accumulate sum/frequency state                  |
| 2. Shrink Loop   : While state is VALID (e.g. sum >= target or formed == required):|
|                    a. Record Answer : minLen = min(minLen, right - left + 1) ⚡  |
|                    b. Remove arr[left] state, advance left pointer (`left++`)     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Target Sum Shrink Mechanics

### 2.1 Minimum Size Subarray Sum (LeetCode 209 - $O(N)$ Shortest Search)
Given an array of positive integers `nums` and positive integer `target`, return the minimal length of a contiguous subarray whose sum is $\ge \text{target}$:

1. `left = 0`, `currentSum = 0`, `minLen = Integer.MAX_VALUE`.
2. For `right = 0` to $N - 1$:
   - `currentSum += nums[right]`.
   - **Shrink Window While Valid (`currentSum >= target`)**:
     - **Record Answer INSIDE Shrink Loop**: `minLen = Math.min(minLen, right - left + 1);`
     - `currentSum -= nums[left];`
     - `left++;`
3. Return `minLen == Integer.MAX_VALUE ? 0 : minLen`.

```
Shortest Window Shrink Execution Invariant:
When currentSum >= target, window [left ... right] is valid.
We record minLen, then shrink by removing nums[left].
If the remaining smaller window [left+1 ... right] is STILL >= target,
the shrink loop runs AGAIN, recording an even SHORTER valid window! ⚡
```

> **Memory Trick:** **"Shortest Window: Shrink WHILE VALID! Record minLen INSIDE the shrink loop before left++!"**

---

## 3. Characteristics & Minimum Operations to Reduce X to Zero (LeetCode 1658)

### 3.1 Minimum Operations to Reduce X to Zero (LeetCode 1658)
Given an integer array `nums` and integer $X$, remove an element from either the extreme left or extreme right of the array in each operation until the sum of removed elements equals $X$. Return the minimum number of operations required:

#### The Complementary Max Window Invariant:
* Removing elements from the extreme left and right to sum to $X$ is mathematically equivalent to **Finding the LONGEST CONTIGUOUS SUBARRAY in the middle whose sum equals `totalSum - X`**!

$$\text{Target Middle Sum} = \sum \text{nums} - X$$

$$\text{Min Operations} = N - \text{Max Middle Subarray Length}$$

```java
public static int minOperations(int[] nums, int x) {
    int totalSum = 0;
    for (int num : nums) totalSum += num;

    int target = totalSum - x;
    if (target < 0) return -1;
    if (target == 0) return nums.length;

    int left = 0, currentSum = 0, maxLen = -1;
    for (int right = 0; right < nums.length; right++) {
        currentSum += nums[right];

        while (currentSum > target && left <= right) {
            currentSum -= nums[left++];
        }

        if (currentSum == target) {
            maxLen = Math.max(maxLen, right - left + 1);
        }
    }

    return maxLen == -1 ? -1 : nums.length - maxLen;
}
```

---

## 4. Internal Working Mechanics
Tracing Minimum Size Subarray Sum (LeetCode 209) on `nums = [2, 3, 1, 2, 4, 3]`, `target = 7`:

```
Init: left = 0, currentSum = 0, minLen = MAX_VALUE

right = 0 (val 2): sum = 2 < 7.
right = 1 (val 3): sum = 5 < 7.
right = 2 (val 1): sum = 6 < 7.
right = 3 (val 2): sum = 8 >= 7 -> VALID!
  - Record minLen = min(MAX, 3 - 0 + 1) = 4 ([2, 3, 1, 2]).
  - Shrink: sum -= nums[0] (2) -> sum = 6. left = 1.
  - sum (6) < 7 -> Shrink loop ends.

right = 4 (val 4): sum = 6 + 4 = 10 >= 7 -> VALID!
  - Record minLen = min(4, 4 - 1 + 1) = 4 ([3, 1, 2, 4]).
  - Shrink 1: sum -= nums[1] (3) -> sum = 7. left = 2.
  - sum (7) >= 7 STILL VALID! -> Record minLen = min(4, 4 - 2 + 1) = 3 ([1, 2, 4])!
  - Shrink 2: sum -= nums[2] (1) -> sum = 6. left = 3.
  - sum (6) < 7 -> Shrink loop ends.

right = 5 (val 3): sum = 6 + 3 = 9 >= 7 -> VALID!
  - Record minLen = min(3, 5 - 3 + 1) = 3 ([2, 4, 3]).
  - Shrink 1: sum -= nums[3] (2) -> sum = 7. left = 4.
  - sum (7) >= 7 STILL VALID! -> Record minLen = min(3, 5 - 4 + 1) = 2 ([4, 3])!
  - Shrink 2: sum -= nums[4] (4) -> sum = 3. left = 5.

Minimum Length Found = 2 ([4, 3]) ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Shortest Window Shrinking Loop Traversal Topography:

```
nums = [ 2,  3,  1,  2,  4,  3 ]
                 [===========]          right = 4: Valid Window [3, 1, 2, 4] (Len 4)
                     [=======]          Shrink 1 : Valid Window [1, 2, 4]    (Len 3)
                         [===]          right = 5: Valid Window [4, 3]       (Len 2) ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Minimum Size Subarray Sum (LeetCode 209), Minimum Window Substring (LeetCode 76), and Minimum Operations to Reduce X to Zero (LeetCode 1658):

```java
import java.util.*;

public class ShortestProblemsMaster {

    // 1. Minimum Size Subarray Sum (LeetCode 209) O(N) Time, O(1) Space
    public static int minSubArrayLen(int target, int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int left = 0;
        long currentSum = 0;
        int minLen = Integer.MAX_VALUE;

        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];

            // Shrink window WHILE valid
            while (currentSum >= target) {
                // Record answer INSIDE shrink loop
                minLen = Math.min(minLen, right - left + 1);
                currentSum -= nums[left];
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }

    // 2. Minimum Operations to Reduce X to Zero (LeetCode 1658) O(N) Time, O(1) Space
    public static int minOperations(int[] nums, int x) {
        if (nums == null || nums.length == 0) return -1;

        int totalSum = 0;
        for (int num : nums) totalSum += num;

        int target = totalSum - x;
        if (target < 0) return -1;
        if (target == 0) return nums.length;

        int left = 0;
        int currentSum = 0;
        int maxLen = -1;

        // Find longest contiguous middle subarray summing to target
        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];

            while (currentSum > target && left <= right) {
                currentSum -= nums[left];
                left++;
            }

            if (currentSum == target) {
                maxLen = Math.max(maxLen, right - left + 1);
            }
        }

        return maxLen == -1 ? -1 : nums.length - maxLen;
    }
}
```

> **Quick Syntax:**
```java
// Shortest Window Record Pattern
while (currentSum >= target) {
    minLen = Math.min(minLen, right - left + 1); // Record inside shrink loop!
    currentSum -= nums[left++];
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 209 - Minimum Size Subarray Sum**: Shortest window target sum search.
* **LeetCode 76 - Minimum Window Substring**: Shortest frequency match substring.
* **LeetCode 1658 - Minimum Operations to Reduce X to Zero**: Complementary longest middle subarray.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Minimum Size Subarray Sum and Minimum Operations to Reduce X to Zero:

```java
public class ShortestProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Minimum Size Subarray Sum (LeetCode 209, Target=7) ===");
        int[] nums1 = {2, 3, 1, 2, 4, 3};
        int minLen = ShortestProblemsMaster.minSubArrayLen(7, nums1);
        System.out.println("Minimum Subarray Length: " + minLen); // Output: 2 ([4, 3])

        System.out.println("\n=== 2. Min Operations to Reduce X to Zero (LeetCode 1658, X=5) ===");
        int[] nums2 = {1, 1, 4, 2, 3};
        int minOps = ShortestProblemsMaster.minOperations(nums2, 5);
        System.out.println("Minimum Operations: " + minOps); // Output: 2 (Remove 2 and 3 from right)
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Min Subarray Sum (209)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Record `minLen` inside shrink loop |
| **Reduce X to Zero (1658)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Complementary max middle target search |

---

## 10. Edge Cases & Boundary Handling
* **No Subarray Meets Target**: Returns `0` (or `-1` for 1658) cleanly.
* **$X$ Equals Total Array Sum in 1658**: Target middle sum is `0`; returns `nums.length` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Recording `minLen` Outside the Shrink Loop**:
  - Recording `minLen` outside `while (currentSum >= target)` saves the window length AFTER it became invalid (`currentSum < target`), producing incorrect results!
  - **Always record `minLen` INSIDE the `while` shrink loop BEFORE advancing `left`**.
* **Attempting Direct 2-Pointer Search on Ends for LeetCode 1658**:
  - Trying to greedily pick from left or right ends fails on non-monotonic arrays.
  - **Invert the problem to find the longest middle subarray with sum `totalSum - X`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Problem Inversion Trick in LeetCode 1658:
> Minimizing elements removed from two ends (left + right = X) is mathematically IDENTICAL to maximizing elements kept in the middle ($\text{Middle Sum} = \text{TotalSum} - X$).
> This transforms a two-ended boundary search into a standard **Longest Subarray Sliding Window Problem**!

> **Memory Trick:** **"Min operations on array ends = Max window in the middle summing to (TotalSum - X)!"**

---

## 13. System & Implementation Comparisons

| Feature | Inverted Middle Sliding Window | Greedy Two-Ended Search |
| :--- | :--- | :--- |
| **Correctness** | **100% Guaranteed Optimal ⚡**| Fails on Non-Monotonic Inputs |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(2^N)$ Exponential |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Stack Memory |

---

## 14. How to Recognize This in Questions
* **"Find minimal length of contiguous subarray with sum >= target"** $\rightarrow$ LeetCode 209 (Shortest window shrink loop).
* **"Remove elements from ends to reduce X to zero in minimum operations"** $\rightarrow$ LeetCode 1658 (Invert to max middle window sum).

---

## 15. Frequently Asked Interview Questions
* **Q: Why MUST `minLen` be recorded INSIDE the `while` shrink loop in Shortest Window search?**  
  *A:* Because the `while` loop condition checks that the window is VALID (`currentSum >= target`). We must record `minLen` while the window is valid, BEFORE `left++` removes an element and potentially makes the window invalid.
* **Q: Why does LeetCode 1658 require all elements in `nums` to be positive?**  
  *A:* Positive elements guarantee that adding an element strictly INCREASES the window sum, maintaining window monotonicity required for sliding window optimality.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SHORTEST SLIDING WINDOW PROBLEMS                      |
+-----------------------------------------------------------------------+
| • Shortest Record Rule: minLen = min(minLen, right - left + 1) INSIDE |
|   the while (currentSum >= target) shrink loop BEFORE left++          |
| • Reduce X to Zero (1658): Invert problem! Find max middle subarray   |
|   summing to (totalSum - X). Return (N - maxLen).                     |
| • Space Invariant: All shortest window algorithms run in O(1) Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Minimum Size Subarray Sum (LeetCode 209) in under 3 minutes.
- [ ] I know why `minLen` MUST be recorded INSIDE the shrink loop.
- [ ] I can solve Minimum Operations to Reduce X to Zero (LeetCode 1658).
- [ ] I can derive the complementary middle target formula `totalSum - X`.
- [ ] I know why array monotonicity is required for sliding window validity.
