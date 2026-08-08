# 08. Subarray Sum Equals K & Prefix Sum Hash Mapping

## 1. Introduction
The **Prefix Sum + Hash Map Pattern** is a powerful algorithmic technique used to find contiguous subarrays satisfying sum constraints in **$O(N)$ linear time**. In technical coding interviews, problems such as Subarray Sum Equals K (LeetCode 560), Continuous Subarray Sum (LeetCode 523), Subarray Sums Divisible by K (LeetCode 974), and Contiguous Array of Equal 0s and 1s (LeetCode 525) evaluate transforming range sum queries over contiguous array intervals into $O(1)$ Hash Map complement lookups.

> **Important:** The fundamental identity of Prefix Sum Hashing is that the sum of a contiguous subarray between indices $i$ and $j$ ($i \le j$) is equal to:
> $$\text{sum}(i \dots j) = \text{prefixSum}[j] - \text{prefixSum}[i - 1] = K \implies \text{prefixSum}[i - 1] = \text{prefixSum}[j] - K$$
> Storing running prefix sums in a Hash Map allows us to count or locate valid subarrays instantly!

```
Subarray Sum Paradigms Spectrum:
+-----------------------------------------------------------------------------------+
| Brute Force Subarrays        : Evaluate all N*(N+1)/2 subarrays -> O(N³) / O(N²)  |
| Sliding Window (Positive Only): Works ONLY if all array elements > 0 -> O(N) Time |
| Prefix Sum + Hash Map        : Works for POSITIVE, ZERO & NEGATIVE! -> O(N) Time ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Algebra

### 2.1 Mathematical Identity of Subarray Range Sums
Let $P[i]$ be the running cumulative prefix sum up to index $i$:

$$P[i] = \sum_{m=0}^{i} \text{nums}[m] \quad \text{with } P[-1] = 0$$

The sum of any contiguous subarray $\text{nums}[i \dots j]$ is:

$$\text{Sum}(i \dots j) = P[j] - P[i - 1]$$

Setting $\text{Sum}(i \dots j) = K$:

$$P[j] - P[i - 1] = K \implies \mathbf{P[i - 1] = P[j] - K}$$

### 2.2 Why Sliding Window FAILS for Negative Numbers
When array elements are strictly positive ($\text{nums}[m] > 0$), expanding a sliding window increases the window sum monotonically, and shrinking it decreases the sum.
However, when an array contains **negative numbers or zeros**, the window sum is non-monotonic! Sliding window pointers cannot determine whether to expand or shrink. **Prefix Sum + Hash Map is MANDATORY when an array contains negative integers!**

### 2.3 The Mandatory Base Initialization Rule (`map.put(0, 1)`)
Before iterating through the array, the prefix sum Hash Map MUST be initialized with:

$$\text{map.put}(0, 1)$$

* **Why?** A subarray starting from the very first element (index $0 \dots j$) having sum $K$ has $P[j] = K$.
* Searching for complement $P[j] - K = K - K = 0$ requires the map to contain prefix sum $0$ with frequency count $1$ (representing the empty prefix $P[-1] = 0$). Failing to initialize `map.put(0, 1)` misses all valid subarrays starting at index 0!

```
Base Map Initialization Necessity:
Array: [3, 4], K = 7
i=0 (3): P[0]=3. Complement 3-7 = -4 (Not in map). Map: {0:1, 3:1}
i=1 (4): P[1]=7. Complement 7-7 = 0.
         - WITHOUT map.put(0,1): Complement 0 NOT FOUND! Count = 0 (WRONG!)
         - WITH map.put(0,1)   : Complement 0 FOUND! Count = 1 (CORRECT!) ✅
```

> **Memory Trick:** **"Subarray Sum Target Identity: prefixSum[i-1] = prefixSum[j] - K! ALWAYS initialize map.put(0, 1)!"**

---

## 3. Characteristics & Problem Variations Matrix

### 3.1 Subarray Sums Divisible by K (LeetCode 974)
To find subarrays where $\text{Sum}(i \dots j) \pmod K = 0$:

$$(P[j] - P[i - 1]) \pmod K = 0 \implies P[j] \pmod K = P[i - 1] \pmod K$$

* Store frequency of prefix sum remainders `remainder = (P[j] % K + K) % K`.
* Adding `+ K` before `% K` handles negative modulo in Java (e.g. `-2 % 5 = -2` $\to$ `(-2 + 5) % 5 = 3`).

### 3.2 Contiguous Array of Equal 0s and 1s (LeetCode 525)
* Replace all `0`s with `-1`s.
* The problem transforms into finding the **Longest Subarray with Sum = 0**!
* Store FIRST occurrence index of each prefix sum in map to maximize subarray length $j - \text{map.get}(P[j])$.

```
Prefix Sum Hash Map Problem Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variation     | Map Key Stored    | Map Value Stored  | Goal Condition    |
+-----------------------+-------------------+-------------------+-------------------+
| Subarray Sum = K (560)| Prefix Sum `P[j]` | Frequency Count   | `count += map.get(P[j]-K)`|
| Equal 0s & 1s (525)   | Prefix Sum `P[j]` | First Index `i`   | `maxLen = max(maxLen, j - idx)`|
| Sum Divisible by K(974)| Remainder `P%K`   | Frequency Count   | `count += map.get(rem)`|
| Continuous Subarray(523)| Remainder `P%K`  | First Index `i`   | `j - idx >= 2`    |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Subarray Sum Equals K (LeetCode 560) on `nums = [1, -1, 1, 1, 1], K = 2`:

```
Init: map = {0: 1}, runningSum = 0, count = 0

i=0 (1) : runningSum = 1. Complement = 1 - 2 = -1. Map contains -1? No.
          map.put(1, 1) | Map: {0:1, 1:1}

i=1 (-1): runningSum = 0. Complement = 0 - 2 = -2. Map contains -2? No.
          map.put(0, 2) | Map: {0:2, 1:1}

i=2 (1) : runningSum = 1. Complement = 1 - 2 = -1. Map contains -1? No.
          map.put(1, 2) | Map: {0:2, 1:2}

i=3 (1) : runningSum = 2. Complement = 2 - 2 = 0. Map contains 0? YES! (freq = 2)
          count += 2 (subarrays [1,-1,1,1] and [1,1]).
          map.put(2, 1) | Map: {0:2, 1:2, 2:1}

i=4 (1) : runningSum = 3. Complement = 3 - 2 = 1. Map contains 1? YES! (freq = 2)
          count += 2 (subarrays [1,1] and [-1,1,1,1]).
          map.put(3, 1) | Map: {0:2, 1:2, 2:1, 3:1}

Total Valid Subarrays Count: 4 ✅ (Linear O(N) Time!)
```

---

## 5. Visual Diagram
Prefix Sum Target Complement Mapping Topology:

```
Array Indices:      0     1     2     3     4
Array Values:    [  1,   -1,    1,    1,    1  ]   K = 2

Prefix Sums P:      1     0     1     2     3   (With P[-1] = 0)

At Index 3 (P[3] = 2):
Target Complement = P[3] - K = 2 - 2 = 0

Search Map for Prefix Sum 0:
Map finds P[-1] = 0 (Start at index 0) -> Subarray [1, -1, 1, 1] Sum = 2
Map finds P[1]  = 0 (Start at index 2) -> Subarray [1, 1]       Sum = 2
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Subarray Sum Equals K (LeetCode 560), Contiguous Array Equal 0s/1s (LeetCode 525), Subarray Sums Divisible by K (LeetCode 974), and Continuous Subarray Sum (LeetCode 523):

```java
import java.util.*;

public class PrefixSumHashMaster {

    // 1. Subarray Sum Equals K (LeetCode 560) O(N) Time, O(N) Space
    public static int subarraySum(int[] nums, int k) {
        if (nums == null || nums.length == 0) return 0;

        Map<Integer, Integer> prefixMap = new HashMap<>();
        prefixMap.put(0, 1); // Base Rule: Empty prefix has sum 0 with count 1

        int runningSum = 0;
        int totalSubarrays = 0;

        for (int num : nums) {
            runningSum += num;
            int complement = runningSum - k;

            // If complement prefix sum exists, add its frequency
            if (prefixMap.containsKey(complement)) {
                totalSubarrays += prefixMap.get(complement);
            }

            // Update frequency of current running sum
            prefixMap.put(runningSum, prefixMap.getOrDefault(runningSum, 0) + 1);
        }

        return totalSubarrays;
    }

    // 2. Contiguous Array Equal 0s and 1s (LeetCode 525) O(N) Time, O(N) Space
    public static int findMaxLength(int[] nums) {
        Map<Integer, Integer> firstSeenMap = new HashMap<>();
        firstSeenMap.put(0, -1); // Prefix sum 0 first seen at virtual index -1

        int runningSum = 0;
        int maxLength = 0;

        for (int i = 0; i < nums.length; i++) {
            // Treat 0 as -1, 1 as +1
            runningSum += (nums[i] == 1) ? 1 : -1;

            if (firstSeenMap.containsKey(runningSum)) {
                int previousIndex = firstSeenMap.get(runningSum);
                maxLength = Math.max(maxLength, i - previousIndex);
            } else {
                firstSeenMap.put(runningSum, i); // Store ONLY FIRST occurrence to maximize length!
            }
        }

        return maxLength;
    }

    // 3. Subarray Sums Divisible by K (LeetCode 974) O(N) Time, O(K) Space
    public static int subarraysDivByK(int[] nums, int k) {
        Map<Integer, Integer> remainderMap = new HashMap<>();
        remainderMap.put(0, 1); // Remainder 0 first seen count 1

        int runningSum = 0;
        int count = 0;

        for (int num : nums) {
            runningSum += num;
            // Handle negative modulo in Java safely: ((r % k) + k) % k
            int remainder = ((runningSum % k) + k) % k;

            if (remainderMap.containsKey(remainder)) {
                count += remainderMap.get(remainder);
            }

            remainderMap.put(remainder, remainderMap.getOrDefault(remainder, 0) + 1);
        }

        return count;
    }

    // 4. Continuous Subarray Sum (LeetCode 523) O(N) Time, O(min(N, K)) Space
    public static boolean checkSubarraySum(int[] nums, int k) {
        Map<Integer, Integer> remainderIndexMap = new HashMap<>();
        remainderIndexMap.put(0, -1); // Base index -1 for remainder 0

        int runningSum = 0;

        for (int i = 0; i < nums.length; i++) {
            runningSum += nums[i];
            int remainder = (k != 0) ? ((runningSum % k) + k) % k : runningSum;

            if (remainderIndexMap.containsKey(remainder)) {
                // Constraint: Subarray length must be at least 2
                if (i - remainderIndexMap.get(remainder) >= 2) {
                    return true;
                }
            } else {
                remainderIndexMap.put(remainder, i);
            }
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Safe Positive Modulo Formula for Negative Running Sums
int remainder = ((runningSum % k) + k) % k;
```

---

## 7. Concrete Problem Examples
* **LeetCode 560 - Subarray Sum Equals K**: Frequency tracking of running prefix sums.
* **LeetCode 525 - Contiguous Array**: Mapping 0 $\to$ -1 to find longest 0-sum subarray.
* **LeetCode 974 - Subarray Sums Divisible by K**: Modulo remainder frequency mapping.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing all prefix sum hash patterns:

```java
public class PrefixSumHashDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Subarray Sum Equals K ===");
        int[] nums1 = {1, 1, 1};
        int k1 = 2;
        System.out.println("Input: [1, 1, 1], K = 2 -> Count: " + PrefixSumHashMaster.subarraySum(nums1, k1)); // Output: 2

        System.out.println("\n=== 2. Contiguous Array (Equal 0s and 1s) ===");
        int[] nums2 = {0, 1, 0, 1, 1, 1, 0};
        System.out.println("Input: [0, 1, 0, 1, 1, 1, 0] -> Max Length: " + PrefixSumHashMaster.findMaxLength(nums2)); // Output: 6

        System.out.println("\n=== 3. Subarray Sums Divisible by K ===");
        int[] nums3 = {4, 5, 0, -2, -3, 1};
        int k3 = 5;
        System.out.println("Input: [4, 5, 0, -2, -3, 1], K = 5 -> Count: " + PrefixSumHashMaster.subarraysDivByK(nums3, k3)); // Output: 7
    }
}
```

---

## 9. Complexity Analysis

| Problem Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Subarray Sum Equals K (560)** | **$O(N)$ Linear ⚡** | **$O(N)$ Space** | Prefix Sum Frequency Map |
| **Equal 0s and 1s (525)** | **$O(N)$ Linear ⚡** | **$O(N)$ Space** | Replace 0 with -1, First Index Map |
| **Sum Divisible by K (974)** | **$O(N)$ Linear ⚡** | **$O(K)$ Space** | Modulo Remainder Frequency Map |
| **Continuous Subarray Sum (523)**| **$O(N)$ Linear ⚡** | **$O(\min(N, K))$** | Remainder First Index Map ($len \ge 2$) |

---

## 10. Edge Cases & Boundary Handling
* **Forgetting `map.put(0, 1)`**: Misses all valid subarrays that start at index 0!
* **Negative Modulo in Java**: In Java, `-7 % 3 = -1`. Modulo remainders used as map keys MUST be positive! Always use: `((sum % k) + k) % k`.
* **Array Contains All Zeros (`nums = [0, 0, 0], K = 0`)**: Map frequency increments cleanly to count all zero-sum subarrays.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting Sliding Window when Array Has Negative Numbers**: Sliding window fails because sums decrease on expansion when encountering negative numbers. Use Prefix Sum + Hash Map!
* **Updating First Occurrence Map Index in Maximum Length Problems**: In LeetCode 525, updating `firstSeenMap.put(sum, i)` when `sum` already exists REDUCES the subarray length! Store ONLY the FIRST index seen.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Frequency Map vs First Index Map Rules:
> 1. **Counting Subarrays (e.g. 560, 974)**: Map stores **Frequencies** (`map.put(sum, map.getOrDefault(sum, 0) + 1)`). Update map on EVERY iteration!
> 2. **Max Length Subarrays (e.g. 525, 523)**: Map stores **First Index Seen** (`firstSeenMap.putIfAbsent(sum, i)`). DO NOT update map if key exists!

> **Memory Trick:** **"Counting Problem = Map Frequency (Update Always)! Max Length Problem = Map First Index (Update Only If Absent)!"**

---

## 13. System & Implementation Comparisons

| Feature | Sliding Window | Prefix Sum + Hash Map |
| :--- | :--- | :--- |
| **Negative Number Support** | NO (Crashes / Incorrect) | **YES (Fully Supported) ⚡** |
| **Time Complexity** | $O(N)$ Linear | **$O(N)$ Linear ⚡** |
| **Space Complexity** | **$O(1)$ Constant ⚡** | $O(N)$ Auxiliary Map Space |
| **Zero Element Support** | Fragile | **Fully Supported** |

---

## 14. How to Recognize This in Questions
* **"Find number of contiguous subarrays with sum equal to K"** $\rightarrow$ Prefix Sum Frequency Map (`P[j] - K`).
* **"Find longest contiguous subarray of 0s and 1s"** $\rightarrow$ Convert 0 to -1, Prefix Sum First Index Map.

---

## 15. Frequently Asked Interview Questions
* **Q: Why do we initialize `prefixMap.put(0, 1)` for counting problems and `firstSeenMap.put(0, -1)` for length problems?**  
  *A:* `prefixMap.put(0, 1)` represents $P[-1] = 0$ occurring 1 time before processing array elements. For length problems, `firstSeenMap.put(0, -1)` records that prefix sum 0 occurred at virtual index $-1$, so if $P[j] = 0$, length is $j - (-1) = j + 1$.
* **Q: How does `((sum % k) + k) % k` fix Java negative remainder bugs?**  
  *A:* In Java, `%` is a remainder operator, preserving negative signs (e.g. `-5 % 3 = -2`). Adding `k` produces `1`, and taking `% k` again handles positive numbers cleanly without changing their value.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PREFIX SUM & HASH MAPPING                             |
+-----------------------------------------------------------------------+
| • Subarray Sum Identity: Sum(i..j) = P[j] - P[i-1] = K                |
| • Target Complement: Search map for P[i-1] = P[j] - K                 |
| • Base Rule 1 (Counting): ALWAYS initialize map.put(0, 1)             |
| • Base Rule 2 (Max Length): ALWAYS initialize map.put(0, -1)          |
| • Java Positive Modulo: remainder = ((runningSum % k) + k) % k        |
| • Counting vs Length: Counting updates map always; Length updates     |
|   ONLY if key is absent (to preserve earliest index)!                 |
| • Negative Numbers: Forces Prefix Sum Hash Map over Sliding Window!  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can derive the prefix sum complement identity $P[i-1] = P[j] - K$.
- [ ] I know why `map.put(0, 1)` is mandatory for counting subarrays.
- [ ] I know why `map.put(0, -1)` is mandatory for max length subarrays.
- [ ] I can write the negative modulo fix `((sum % k) + k) % k`.
- [ ] I can solve LeetCode 560, 525, 974, and 523 in $O(N)$ linear time.
- [ ] I know why Sliding Window fails when negative numbers exist.
