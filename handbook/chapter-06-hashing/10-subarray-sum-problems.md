# 10. Subarray Sum Problems, Prefix Hash Maps & Modulo Remainder Invariants

## 1. Introduction
**Subarray Sum Problems** represent one of the most essential sub-families of Hash Map applications. By pairing a cumulative **Prefix Sum** sequence with a **Hash Map** (`prefixMap`), algorithms solve complex sub-array sum, divisibility, and zero-one balance queries—such as **Subarray Sum Equals K (LeetCode 560)**, **Continuous Subarray Sum (LeetCode 523)**, **Subarray Sums Divisible by K (LeetCode 974)**, and **Contiguous Array (LeetCode 525)**—in **$O(N)$ linear time and $O(N)$ auxiliary space**.

> **Important:** Why does Subarray Sum Equals K require Prefix Hash Maps instead of two pointers / sliding window?
> Sliding window requires array elements to be NON-NEGATIVE (ensuring monotone window expansion).
> When an array contains **NEGATIVE NUMBERS**, window sums fluctuate non-monotonically!
> Prefix Sum Hashing relies on the equation:
> $$\text{SubarraySum}(i \dots j) = P[j] - P[i-1] = K \implies \mathbf{P[i-1] = P[j] - K}$$
> Checking if $P[j] - K$ exists in the Hash Map solves the problem in $O(N)$ time regardless of negative numbers! ⚡

```
Prefix Sum Hashing Mathematical Topology:
Array     : [  3,   4,   7,  -2,   2,   1,  42 ]
Prefix P  : [  3,   7,  14,  12,  14,  15,  57 ]
                       ^^         ^^
           Subarray(3..4) = P[4] - P[2-1] = 14 - 14 = 0! (Sum between indices 3 and 4 is ZERO!) ⚡
```

---

## 2. Core Concepts & Subarray Sum Equals K (LeetCode 560)

### 2.1 Subarray Sum Equals K Algorithm (LeetCode 560)
Given an integer array `nums` and integer $K$, return the total number of subarrays whose sum equals $K$:

#### Prefix Hash Map Rules ($O(N)$ Time, $O(N)$ Auxiliary Space):
1. Maintain `Map<Integer, Integer> prefixMap` storing `(prefixSum, frequency)`.
2. **Base Sentinel Initialization**: `prefixMap.put(0, 1)`! (Pre-populates a prefix sum of 0 occurring once, allowing subarrays starting at index 0 to be counted!).
3. `currSum = 0`, `count = 0`.
4. For each `num` in `nums`:
   - `currSum += num`.
   - **Check Match**: If `prefixMap.containsKey(currSum - K)`:
     - `count += prefixMap.get(currSum - K)`.
   - **Record Prefix**: `prefixMap.put(currSum, prefixMap.getOrDefault(currSum, 0) + 1)`.
5. Return `count`.

```
Prefix Hash Map Sentinel Rule:
Initializing prefixMap.put(0, 1) ensures that if currSum == K at index j,
currSum - K = 0 is immediately matched against the sentinel, counting the prefix subarray nums[0...j]! ⚡
```

> **Memory Trick:** **"Subarray Sum Equals K: Check prefixMap.containsKey(currSum - K)! Initialize prefixMap.put(0, 1)!"**

---

## 3. Characteristics & Continuous Subarray Sum Modulo Hashing (LeetCode 523 / 974)

### 3.1 Subarray Sums Divisible by K (LeetCode 974)
Given an integer array `nums` and integer $K$, return the number of non-empty subarrays that have a sum divisible by $K$:
* **Modulo Math Invariant**: If two prefix sums $P[j]$ and $P[i]$ produce the SAME remainder when divided by $K$:
  $$P[j] \bmod K == P[i] \bmod K \implies (P[j] - P[i]) \bmod K == 0$$
* **Negative Modulo Correction**: In Java, `-2 % 5` evaluates to `-2`. Always normalize remainders to positive values:
  $$\text{remainder} = ((\text{currSum} \bmod K) + K) \bmod K$$
* **Algorithm**: Maintain `Map<Integer, Integer> remainderMap`, initialize `remainderMap.put(0, 1)`, and accumulate matches for `remainderMap.get(remainder)`.

---

## 4. Internal Working Mechanics
Tracing Subarray Sum Equals K (LeetCode 560) on `nums = [1, 1, 1]`, $K = 2$:

```
Init: prefixMap = {0: 1}, currSum = 0, count = 0

i = 0 (val 1): currSum = 1. Target = 1 - 2 = -1. Map does not contain -1.
  - Record currSum 1: prefixMap = {0: 1, 1: 1}

i = 1 (val 1): currSum = 2. Target = 2 - 2 = 0. Map CONTAINS 0 (freq 1)!
  - count += 1 -> count = 1.
  - Record currSum 2: prefixMap = {0: 1, 1: 1, 2: 1}

i = 2 (val 1): currSum = 3. Target = 3 - 2 = 1. Map CONTAINS 1 (freq 1)!
  - count += 1 -> count = 2.
  - Record currSum 3: prefixMap = {0: 1, 1: 1, 2: 1, 3: 1}

Total Subarrays with Sum = 2 is 2 ([1,1] at indices 0..1 and [1,1] at indices 1..2) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Contiguous Array (LeetCode 525 - Max Length Equal 0s and 1s) Prefix Transformation:

```
Original Array (0s and 1s) : [ 0,  1,  0,  0,  1,  1,  0 ]
Transform 0 to -1          : [-1, +1, -1, -1, +1, +1, -1 ]
Cumulative Prefix Sum P    : [-1,  0, -1, -2, -1,  0, -1 ]
                               ^       ^               ^
                    Index 0, Index 2, Index 6 produce SAME prefix sum -1!
                    Max Length = Index 6 - Index 0 = 6! ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Subarray Sum Equals K (LeetCode 560), Subarray Sums Divisible by K (LeetCode 974), Continuous Subarray Sum (LeetCode 523), and Contiguous Array (LeetCode 525):

```java
import java.util.*;

public class SubarraySumProblemsMaster {

    // 1. Subarray Sum Equals K (LeetCode 560) O(N) Time, O(N) Space
    public static int subarraySum(int[] nums, int k) {
        if (nums == null || nums.length == 0) return 0;

        Map<Integer, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0, 1); // Base sentinel initialization

        int currSum = 0;
        int count = 0;

        for (int num : nums) {
            currSum += num;

            // Check if (currSum - k) exists in prefix map
            if (prefixMap.containsKey(currSum - k)) {
                count += prefixMap.get(currSum - k);
            }

            prefixMap.put(currSum, prefixMap.getOrDefault(currSum, 0) + 1);
        }

        return count;
    }

    // 2. Subarray Sums Divisible by K (LeetCode 974) O(N) Time, O(K) Space
    public static int subarraysDivByK(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return 0;

        Map<Integer, Integer> remainderMap = new HashMap<>();
        remainderMap.put(0, 1); // Base sentinel initialization

        int currSum = 0;
        int count = 0;

        for (int num : nums) {
            currSum += num;
            // Normalize remainder to positive range [0 ... K-1]
            int remainder = ((currSum % k) + k) % k;

            if (remainderMap.containsKey(remainder)) {
                count += remainderMap.get(remainder);
            }

            remainderMap.put(remainder, remainderMap.getOrDefault(remainder, 0) + 1);
        }

        return count;
    }

    // 3. Contiguous Array - Equal 0s and 1s Max Length (LeetCode 525) O(N) Time, O(N) Space
    public static int findMaxLength(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        Map<Integer, Integer> prefixIndexMap = new HashMap<>();
        prefixIndexMap.put(0, -1); // Sentinel index -1 for sum 0

        int currSum = 0;
        int maxLen = 0;

        for (int i = 0; i < nums.length; i++) {
            // Transform 0 to -1, 1 remains +1
            currSum += (nums[i] == 0) ? -1 : 1;

            if (prefixIndexMap.containsKey(currSum)) {
                maxLen = Math.max(maxLen, i - prefixIndexMap.get(currSum));
            } else {
                prefixIndexMap.put(currSum, i); // Store FIRST occurrence index only!
            }
        }

        return maxLen;
    }
}
```

> **Quick Syntax:**
```java
// Subarray Sum Prefix Search Line
if (prefixMap.containsKey(currSum - k)) {
    count += prefixMap.get(currSum - k);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 560 - Subarray Sum Equals K**: Basic prefix sum + HashMap.
* **LeetCode 974 - Subarray Sums Divisible by K**: Modulo remainder prefix map.
* **LeetCode 525 - Contiguous Array**: Convert 0 to -1 + prefix index map.
* **LeetCode 523 - Continuous Subarray Sum**: Modulo index difference $\ge 2$.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Subarray Sum Equals K, Subarray Sums Divisible by K, and Contiguous Array:

```java
public class SubarraySumProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Subarray Sum Equals K (LeetCode 560) ===");
        int[] nums1 = {1, 1, 1};
        int count1 = SubarraySumProblemsMaster.subarraySum(nums1, 2);
        System.out.println("Subarrays with Sum=2: " + count1); // Output: 2

        System.out.println("\n=== 2. Subarray Sums Divisible by K (LeetCode 974) ===");
        int[] nums2 = {4, 5, 0, -2, -3, 1};
        int count2 = SubarraySumProblemsMaster.subarraysDivByK(nums2, 5);
        System.out.println("Subarrays Divisible by 5: " + count2); // Output: 7

        System.out.println("\n=== 3. Contiguous Array Equal 0s and 1s (LeetCode 525) ===");
        int[] nums3 = {0, 1, 0, 0, 1, 1, 0};
        int maxLen = SubarraySumProblemsMaster.findMaxLength(nums3);
        System.out.println("Max Length Equal 0s and 1s: " + maxLen); // Output: 6
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- |
| **Subarray Sum K (560)** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | `prefixMap.containsKey(currSum - K)` |
| **Divisible by K (974)** | **$O(N)$ Linear ⚡** | $O(K)$ Map Space | Positive remainder `((currSum % K) + K) % K` |
| **Equal 0s & 1s (525)** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Convert `0` to `-1`; store first index |

---

## 10. Edge Cases & Boundary Handling
* **Negative Remainder Invariant in Java**: `-2 % 5 = -2`. Formula `((currSum % K) + K) % K` maps `-2` to `3` correctly.
* **Subarray Starting at Index 0**: Handled by sentinel `prefixMap.put(0, 1)` or `prefixIndexMap.put(0, -1)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Sentinel Initialization `prefixMap.put(0, 1)`**:
  - Omitting the base sentinel ignores subarrays starting at index 0 whose sum equals $K$!
  - **Always initialize `prefixMap.put(0, 1)` for counts or `prefixIndexMap.put(0, -1)` for lengths**.
* **Overwriting First Occurrence Index in LeetCode 525**:
  - Updating `prefixIndexMap.put(currSum, i)` on every occurrence shortens calculated subarray lengths.
  - **Store ONLY the FIRST index occurrence of each prefix sum to maximize length!**

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Slanted 2-Pointer Fails on LeetCode 560:
> Two-pointer sliding window assumes array values are non-negative, meaning moving `right` ALWAYS increases window sum.
> When array values contain negative numbers, moving `right` can DECREASE window sum, breaking monotonicity.
> **Use Prefix Hash Maps for any subarray sum problem containing negative numbers!**

> **Memory Trick:** **"Negative numbers in array -> Two pointers fail -> Use Prefix Hash Maps!"**

---

## 13. System & Implementation Comparisons

| Feature | Prefix Hash Map Approach | Brute-Force Nested Loops |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | $O(N)$ Map Space | **$O(1)$ Constant** |
| **Negative Number Support**| **Fully Supported ⚡** | Fully Supported |

---

## 14. How to Recognize This in Questions
* **"Find number of continuous subarrays with sum equal to K"** $\rightarrow$ LeetCode 560 (Prefix HashMap).
* **"Find max length of subarray with equal number of 0s and 1s"** $\rightarrow$ LeetCode 525 (Convert 0 to -1 + Prefix Index Map).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `findMaxLength` (LeetCode 525) convert 0s to -1s?**  
  *A:* By mapping 0 to -1 and 1 to +1, a subarray containing equal numbers of 0s and 1s sums to EXACTLY 0. The problem reduces to finding the maximum distance between two identical prefix sum occurrences ($P[j] == P[i]$).
* **Q: Why does `subarraysDivByK` (LeetCode 974) require positive modulo normalization?**  
  *A:* In Java, the `%` operator returns negative remainders for negative numbers. Normalizing remainders via `((currSum % K) + K) % K` maps negative remainders into valid positive bucket indices $[0 \dots K-1]$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUBARRAY SUM & PREFIX HASH MAPS                       |
+-----------------------------------------------------------------------+
| • Base Sentinel Rule: Always initialize prefixMap.put(0, 1)           |
| • Subarray Match Target: check if prefixMap.containsKey(currSum - K)   |
| • Positive Remainder: remainder = ((currSum % K) + K) % K             |
| • Equal 0s & 1s (525): Transform 0 -> -1; store FIRST index occurrence|
| • Time Complexity: O(N) Linear Time | O(N) Auxiliary Space ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Subarray Sum Equals K (LeetCode 560) in $O(N)$ time.
- [ ] I know why `prefixMap.put(0, 1)` base sentinel is required.
- [ ] I can write Subarray Sums Divisible by K (LeetCode 974) with positive modulo.
- [ ] I can write Contiguous Array (LeetCode 525) by converting 0 to -1.
- [ ] I know why two-pointer sliding window fails when negative numbers exist.
