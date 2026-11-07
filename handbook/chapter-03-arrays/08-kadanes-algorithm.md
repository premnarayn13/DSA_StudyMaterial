# 08. Kadane's Algorithm (Maximum Subarray)

## 1. Introduction
**Kadane's Algorithm** is a classic dynamic programming technique that solves the Maximum Subarray Sum problem in **$O(n)$ linear time and $O(1)$ auxiliary space**. Given an array of integers (which may include negative values), Kadane's Algorithm finds a contiguous subarray with the largest possible sum. In technical coding interviews (LeetCode 53), Kadane's Algorithm is one of the most frequently tested array paradigms.

> **Important:** Brute force checking all $O(n^2)$ contiguous subarrays takes $O(n^2)$ or $O(n^3)$ time. Kadane's Algorithm reduces this to **$O(n)$ time and $O(1)$ space** in a single linear pass!

## 2. Core Concepts
* **Dynamic Programming State**: At each index `i`, we make a local decision: Should we extend the existing subarray sum by adding `nums[i]`, OR start a brand-new subarray starting at `nums[i]`?
* **Local Optimum Recurrence (`currentSum`)**:
  $$\text{currentSum}[i] = \max(\text{nums}[i], \text{currentSum}[i-1] + \text{nums}[i])$$
* **Global Optimum (`maxSum`)**: The maximum `currentSum` encountered across all index positions $0 \dots n-1$:
  $$\text{maxSum} = \max(\text{maxSum}, \text{currentSum}[i])$$
* **Discard Negative Prefix Rule**: If `currentSum` becomes negative, it can NEVER contribute positively to any future subarray! Reset `currentSum = 0` (or start fresh with `nums[i]`).

> **Memory Trick:** **"Extend or Restart"**. At index `i`, `currentSum = Math.max(nums[i], currentSum + nums[i])`. If `currentSum` drops below 0, drop it!

## 3. Characteristics / Properties
* **Contiguous Subarray Constraint**: Elements in the chosen window must be physically adjacent in the input array.
* **All-Negative Numbers Guard**: When the array contains ONLY negative numbers (e.g., `[-5, -2, -8]`), the maximum subarray sum is the **least negative single element** (`-2`), NOT 0!
* **Subarray Boundaries Tracking**: Keeping track of `start` and `end` indices allows returning the actual subarray elements, not just the numerical sum value.

```
Maximum Subarray Search Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Search Strategy       | Time Complexity   | Space Complexity  | Notes / Verdict   |
+-----------------------+-------------------+-------------------+-------------------+
| Brute Force 3 Loops   | O(n³)             | O(1)              | Total TLE!        |
| Prefix Sum 2 Loops    | O(n²)             | O(n)              | Slow              |
| Divide and Conquer    | O(n log n)        | O(log n) stack    | Overcomplicated   |
| Kadane's Algorithm    | O(n)              | O(1)              | OPTIMAL & GOLDEN⚡|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Kadane's Algorithm on `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]` ($N = 9$):

```
Initialization: currentSum = 0, maxSum = Integer.MIN_VALUE

i = 0 (val -2): currentSum = max(-2, 0 + -2) = -2 | maxSum = max(-INF, -2) = -2
i = 1 (val  1): currentSum = max( 1, -2 +  1) =  1 | maxSum = max(-2, 1)    =  1
i = 2 (val -3): currentSum = max(-3,  1 + -3) = -2 | maxSum = max(1, -2)    =  1
i = 3 (val  4): currentSum = max( 4, -2 +  4) =  4 | maxSum = max(1, 4)     =  4
i = 4 (val -1): currentSum = max(-1,  4 + -1) =  3 | maxSum = max(4, 3)     =  4
i = 5 (val  2): currentSum = max( 2,  3 +  2) =  5 | maxSum = max(4, 5)     =  5
i = 6 (val  1): currentSum = max( 1,  5 +  1) =  6 | maxSum = max(5, 6)     =  6  <-- MAX!
i = 7 (val -5): currentSum = max(-5,  6 + -5) =  1 | maxSum = max(6, 1)     =  6
i = 8 (val  4): currentSum = max( 4,  1 +  4) =  5 | maxSum = max(6, 5)     =  6

Maximum Subarray Sum Found: 6  (Subarray: [4, -1, 2, 1]) ✅
```

## 5. Visual Diagram
Kadane's Decision Rule Visualized:

```
  Index:       0      1      2      3      4      5      6      7      8
  nums:      [ -2 ][  1 ][ -3 ][  4 ][ -1 ][  2 ][  1 ][ -5 ][  4 ]
                          ^      <----------------------->
                    Drop Prefix       MAX SUBARRAY WINDOW
                    (Reset sum)          Sum = 4-1+2+1 = 6
```

## 6. Operations / Algorithms
Standard Kadane's Algorithm Implementation:

```java
public int maxSubArray(int[] nums) {
    int maxSum = nums[0];
    int currentSum = nums[0];

    for (int i = 1; i < nums.length; i++) {
        // Core Kadane Decision: Extend previous window OR start fresh at nums[i]
        currentSum = Math.max(nums[i], currentSum + nums[i]);
        // Update global maximum
        maxSum = Math.max(maxSum, currentSum);
    }
    return maxSum;
}
```

> **Quick Syntax:**
```java
// Kadane's Inner Loop State Update
currentSum = Math.max(nums[i], currentSum + nums[i]);
maxSum = Math.max(maxSum, currentSum);
```

## 7. Examples
* **LeetCode 53 - Maximum Subarray**: Standard Kadane's algorithm.
* **LeetCode 918 - Maximum Sum Circular Subarray**: Kadane's max sum combined with Kadane's min sum to handle circular wrap-around.
* **Maximum Product Subarray (LeetCode 152)**: Modified Kadane maintaining both `maxProduct` and `minProduct` (due to negative multiplication sign flips).

## 8. Java Code
Complete interview-ready Java suite implementing standard Kadane's algorithm AND Subarray Boundary tracking:

```java
import java.util.Arrays;

public class KadanesAlgorithmMaster {

    // 1. Standard Kadane's Algorithm: Returns Maximum Subarray Sum O(n) Time, O(1) Space
    public static int maxSubArray(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int currentSum = nums[0];
        int maxSum = nums[0];

        for (int i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }

        return maxSum;
    }

    // 2. Advanced Kadane: Returns Subarray Boundaries [start, end, maxSum]
    public static int[] maxSubArrayWithIndices(int[] nums) {
        if (nums == null || nums.length == 0) return new int[]{0, 0, 0};

        int currentSum = nums[0];
        int maxSum = nums[0];

        int bestStart = 0;
        int bestEnd = 0;
        int tempStart = 0;

        for (int i = 1; i < nums.length; i++) {
            if (nums[i] > currentSum + nums[i]) {
                currentSum = nums[i]; // Start new subarray
                tempStart = i;
            } else {
                currentSum += nums[i]; // Extend current subarray
            }

            if (currentSum > maxSum) {
                maxSum = currentSum;
                bestStart = tempStart;
                bestEnd = i;
            }
        }

        System.out.println("Subarray range: [" + bestStart + " ... " + bestEnd + "]");
        return new int[]{bestStart, bestEnd, maxSum};
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Max Subarray Sum: " + maxSubArray(nums1)); // Output: 6

        System.out.print("Boundary Tracking: ");
        int[] result = maxSubArrayWithIndices(nums1);
        System.out.println("Max Sum = " + result[2]); // Subarray range: [3 ... 6], Max Sum = 6

        // Test All-Negative Array
        int[] allNegative = {-5, -2, -8, -1, -4};
        System.out.println("All Negative Max Sum: " + maxSubArray(allNegative)); // Output: -1
    }
}
```

## 9. Complexity Analysis
| Algorithm Variant | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Standard Kadane's Algorithm** | **$O(n)$** | **$O(1)$** | Single linear pass over array |
| **Kadane's with Index Tracking**| **$O(n)$** | **$O(1)$** | Tracks `bestStart` and `bestEnd` pointers |
| **Circular Subarray Kadane** | **$O(n)$** | **$O(1)$** | Runs Max Kadane + Min Kadane |
| **Divide and Conquer Subarray** | $O(n \log n)$ | $O(\log n)$ call stack | Merges left/right cross sums |

## 10. Edge Cases
* **All Negative Numbers**: Initializing `maxSum = 0` or `currentSum = 0` fails on `[-5, -2, -8]`, returning 0 instead of `-2`. **Fix**: Initialize `maxSum = nums[0]` and `currentSum = nums[0]`.
* **Single Element Array (`nums.length == 1`)**: Returns `nums[0]` immediately.
* **Large Integer Overflow**: If subarray values approach $10^9$, accumulating sums in 32-bit `int` overflows. Use `long currentSum`.

## 11. Common Mistakes
* Initializing `maxSum = 0` instead of `nums[0]` (fails on all-negative arrays!).
* Resetting `currentSum = 0` BEFORE updating `maxSum` when all elements are negative.
* Confusing Subarray (must be contiguous) with Subsequence (can skip elements).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Always initialize Kadane variables to `nums[0]`, NOT `0`!
> * `int currentSum = nums[0];`
> * `int maxSum = nums[0];`
> This single fix handles arrays with all-negative numbers correctly!

> **Memory Trick:** **"CurrentSum = Math.max(nums[i], currentSum + nums[i])"**.

## 13. Comparisons
| Problem | Standard Subarray Sum (Kadane) | Maximum Product Subarray |
| :--- | :--- | :--- |
| **Operation** | Addition (`+`) | Multiplication (`*`) |
| **State Tracked** | `currentSum` | `maxProduct` AND `minProduct` |
| **Negative Sign Effect** | Reduces sum | Flips negative to positive (Min becomes Max!) |
| **Time Complexity** | $O(n)$ | $O(n)$ |

## 14. How to Recognize This in Questions
* **"Find contiguous subarray with largest sum"** $\rightarrow$ Kadane's Algorithm ($O(n)$ time, $O(1)$ space).
* **"Find maximum sum in circular array"** $\rightarrow$ Kadane's Max vs TotalSum - Kadane's Min.

## 15. Frequently Asked Interview Questions
* **Q: How does Kadane's Algorithm handle arrays with all negative numbers?**  
  *A:* By initializing `currentSum = nums[0]` and `maxSum = nums[0]`, the algorithm compares `nums[i]` against `currentSum + nums[i]`. For all negative numbers, `nums[i]` is always larger than `currentSum + nums[i]`, effectively picking the single least-negative element.
* **Q: How do you find the Maximum Sum Circular Subarray (LeetCode 918)?**  
  *A:* The maximum circular subarray sum is either the standard maximum subarray sum (found via Kadane's), OR a wrapped subarray whose sum equals `TotalArraySum - MinKadaneSubarraySum`. Take the maximum of both (with edge case guard when all numbers are negative).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: KADANE'S ALGORITHM                                   |
+-----------------------------------------------------------------------+
| • State Recurrence: currentSum = Math.max(nums[i], currentSum + nums[i])|
| • Global Maximum: maxSum = Math.max(maxSum, currentSum)               |
| • All-Negative Fix: Init currentSum = nums[0] and maxSum = nums[0]   |
| • Time Complexity: O(n) Linear Pass | Auxiliary Space: O(1) Constant  |
| • Subarray = Contiguous Block! (Subsequence can skip items)           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write standard Kadane's Algorithm in under 2 minutes.
- [ ] I know why initializing `currentSum = nums[0]` handles all-negative arrays.
- [ ] I can track and return the start/end indices of the maximum subarray.
- [ ] I know how to extend Kadane's to solve Maximum Product Subarray.
- [ ] I can explain why Kadane's Algorithm is $O(n)$ time and $O(1)$ space.
