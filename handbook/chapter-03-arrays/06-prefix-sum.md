# 06. Prefix Sum Technique

## 1. Introduction
The **Prefix Sum** technique is a fundamental algorithmic pattern used to answer contiguous range sum queries on an array in constant $O(1)$ time after an $O(n)$ precomputation phase. In technical interviews, prefix sums serve as the core building block for solving subarray sum problems, 2D matrix range queries, product array problems, and subarray frequency hashing.

> **Important:** Without Prefix Sum, answering $Q$ range sum queries on an array of size $N$ takes $O(Q \cdot N)$ time. With Prefix Sum, the total execution time drops to **$O(N + Q)$**—reducing execution speed from minutes to milliseconds!

## 2. Core Concepts
* **Prefix Sum Definition**: An array `prefix[i]` where each entry stores the cumulative sum of all elements from index `0` up to index `i`:
  $$\text{prefix}[i] = \sum_{j=0}^{i} \text{arr}[j] = \text{prefix}[i-1] + \text{arr}[i]$$
* **Range Sum Formula**: The sum of elements in subarray range `[L, R]` (inclusive) is computed in $O(1)$ time via:
  $$\text{Sum}(L, R) = \text{prefix}[R] - \text{prefix}[L - 1]$$
  *(For $L = 0$, $\text{Sum}(0, R) = \text{prefix}[R]$).*
* **1-Indexed Dummy Prefix Array (Best Practice)**: Allocating `prefix` array of size $N + 1$ where `prefix[0] = 0` and `prefix[i] = prefix[i-1] + arr[i-1]`. Range sum simplifies to:
  $$\text{Sum}(L, R) = \text{prefix}[R + 1] - \text{prefix}[L]$$

> **Memory Trick:** **"Range Sum(L, R) = Prefix[R] - Prefix[L-1]"**. With a 1-indexed 0-padded prefix array, it becomes **"Prefix[R + 1] - Prefix[L]"**.

## 3. Characteristics / Properties
* **Precomputation Trade-off**: Incurs $O(N)$ time and $O(N)$ space upfront to reduce subsequent query time from $O(N)$ to $O(1)$.
* **Static Array Constraint**: Ideal for static arrays where elements do NOT change between range queries. (If elements update dynamically between queries, Segment Trees or Fenwick Trees are required for $O(\log N)$ updates).

```
Range Query Performance Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Query Strategy        | Precompute Time   | Query Time        | Total for Q Queries|
+-----------------------+-------------------+-------------------+-------------------+
| Naive Loop Range Sum  | O(1)              | O(N) per query    | O(Q * N) (SLOW!)  |
| Prefix Sum Array      | O(N)              | O(1) per query    | O(N + Q) (FAST!⚡)|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing 1-Indexed Prefix Sum Construction & Range Query:

```
Original Array: arr = [ 3, 1, 4, 1, 5, 9 ]  (N = 6)

Prefix Array Construction (Size N + 1 = 7, prefix[0] = 0):
prefix[0] = 0
prefix[1] = prefix[0] + arr[0] = 0 + 3 = 3
prefix[2] = prefix[1] + arr[1] = 3 + 1 = 4
prefix[3] = prefix[2] + arr[2] = 4 + 4 = 8
prefix[4] = prefix[3] + arr[3] = 8 + 1 = 9
prefix[5] = prefix[4] + arr[4] = 9 + 5 = 14
prefix[6] = prefix[5] + arr[5] = 14 + 9 = 23

Prefix Array: [ 0, 3, 4, 8, 9, 14, 23 ]

Query: Calculate Sum of Subarray from L = 2 to R = 4 (arr[2..4] = 4 + 1 + 5 = 10)
Formula: prefix[R + 1] - prefix[L] = prefix[5] - prefix[2] = 14 - 4 = 10 ✅ (O(1) time!)
```

## 5. Visual Diagram
Prefix Range Subtraction Visualized:

```
Index:       0     1     2     3     4     5
arr:       [ 3 ][ 1 ][ 4 ][ 1 ][ 5 ][ 9 ]
           <------- Prefix[4] ------> (Cumulative Sum 0..4 = 14)
           <-- Prefix[1] -->           (Cumulative Sum 0..1 = 4)

                     [ TARGET RANGE L=2..R=4 ]
                     [ 4 ][ 1 ][ 5 ]   (Sum = 14 - 4 = 10)
```

## 6. Operations / Algorithms
Code Building Blocks for Prefix Sum Techniques:

### 1. Standard 1-Indexed Prefix Array Construction & Query
```java
// Precomputation O(N)
int n = arr.length;
long[] prefix = new long[n + 1];
for (int i = 0; i < n; i++) {
    prefix[i + 1] = prefix[i] + arr[i];
}

// Range Sum Query L..R O(1)
public long queryRange(int L, int R) {
    return prefix[R + 1] - prefix[L];
}
```

### 2. Prefix Sum + HashMap for Subarray Sum Equals K (LeetCode 560)
```java
public int subarraySum(int[] nums, int k) {
    Map<Long, Integer> map = new HashMap<>();
    map.put(0L, 1); // Base case: prefix sum 0 occurs once
    
    long currentSum = 0;
    int count = 0;
    
    for (int num : nums) {
        currentSum += num;
        // If (currentSum - k) exists in map, we found valid subarrays!
        if (map.containsKey(currentSum - k)) {
            count += map.get(currentSum - k);
        }
        map.put(currentSum, map.getOrDefault(currentSum, 0) + 1);
    }
    return count;
}
```

> **Quick Syntax:**
```java
// Subarray Sum Equals K Key Lookup
long targetPrefix = currentPrefixSum - K;
if (prefixMap.containsKey(targetPrefix)) {
    validSubarraysCount += prefixMap.get(targetPrefix);
}
```

## 7. Examples
* **LeetCode 303 - Range Sum Query (Immutable)**: $O(1)$ query range sums.
* **LeetCode 560 - Subarray Sum Equals K**: Finding count of subarrays summing to $K$ using Prefix Sum + HashMap in $O(N)$ time.
* **LeetCode 238 - Product of Array Except Self**: Computing prefix products and suffix products without division.

## 8. Java Code
Complete interview-ready Java suite demonstrating Prefix Sum Range Queries and Subarray Sum Equals K:

```java
import java.util.HashMap;
import java.util.Map;

public class PrefixSumMaster {

    private long[] prefix;

    // Constructor: Precomputes 1-indexed Prefix Sum Array in O(n)
    public PrefixSumMaster(int[] arr) {
        if (arr == null) return;
        int n = arr.length;
        this.prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            this.prefix[i + 1] = this.prefix[i] + arr[i];
        }
    }

    // O(1) Range Sum Query [L, R] inclusive
    public long queryRange(int L, int R) {
        if (prefix == null || L < 0 || R >= prefix.length - 1 || L > R) {
            throw new IllegalArgumentException("Invalid range indices!");
        }
        return prefix[R + 1] - prefix[L];
    }

    // LeetCode 560: Count Subarrays with Sum Equal to K in O(n) Time, O(n) Space
    public static int countSubarraysWithSumK(int[] nums, int k) {
        if (nums == null || nums.length == 0) return 0;

        Map<Long, Integer> prefixFreq = new HashMap<>();
        prefixFreq.put(0L, 1); // Base condition for subarrays starting at index 0

        long currentPrefixSum = 0;
        int count = 0;

        for (int num : nums) {
            currentPrefixSum += num;

            // If (currentPrefixSum - k) exists, add its frequency
            if (prefixFreq.containsKey(currentPrefixSum - k)) {
                count += prefixFreq.get(currentPrefixSum - k);
            }

            // Record current prefix sum frequency
            prefixFreq.put(currentPrefixSum, prefixFreq.getOrDefault(currentPrefixSum, 0) + 1);
        }

        return count;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] data = {3, 1, 4, 1, 5, 9};
        PrefixSumMaster ps = new PrefixSumMaster(data);

        // Range Sum of index 2 to 4 (values: 4 + 1 + 5 = 10)
        System.out.println("Range Sum [2..4]: " + ps.queryRange(2, 4)); // Output: 10

        // Subarray Sum Equals K Test
        int[] nums = {1, 1, 1};
        int k = 2;
        System.out.println("Subarrays in {1,1,1} with sum 2: " + countSubarraysWithSumK(nums, k)); // Output: 2
    }
}
```

## 9. Complexity Analysis
| Problem Pattern | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Range Sum Query Precomputation**| $O(n)$ | $O(n)$ | Precomputes `prefix[N+1]` array |
| **Range Sum Query Answer** | $O(1)$ | $O(1)$ | Simple subtraction `prefix[R+1] - prefix[L]` |
| **Subarray Sum Equals K** | $O(n)$ | $O(n)$ | Prefix Sum + HashMap frequency lookup |
| **Product Except Self** | $O(n)$ | $O(1)$ auxiliary | Prefix Product + Suffix Product sweep |

## 10. Edge Cases
* **Integer Overflow in Prefix Sum**: Summing large arrays ($10^5$ elements with values $10^9$) causes 32-bit `int` overflow! Always use **`long[]`** for prefix sums.
* **Negative Numbers in Subarray Sum**: Sliding Window fails when negative numbers exist in the array; Prefix Sum + HashMap MUST be used instead!
* **Range $L = 0$**: Using 0-indexed prefix array requires `if (L == 0) return prefix[R]; else return prefix[R] - prefix[L-1];`. 1-indexed prefix array avoids this `if` check.

## 11. Common Mistakes
* Using 32-bit `int[]` for prefix sum arrays when values can accumulate to exceed $2 \times 10^9$.
* Trying to use Sliding Window for "Subarray Sum Equals K" when the array contains **negative numbers** (Sliding window requires monotonic non-decreasing sums!).
* Forgetting to initialize HashMap with `map.put(0L, 1)` in Subarray Sum problems (misses valid subarrays starting at index 0).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** When can you use Sliding Window vs Prefix Sum + HashMap for Subarray Sum problems?
> * **Positive Numbers Only**: Use **Sliding Window** ($O(N)$ time, $O(1)$ space).
> * **Negative & Positive Numbers**: You MUST use **Prefix Sum + HashMap** ($O(N)$ time, $O(N)$ space) because prefix sums are non-monotonic!

> **Memory Trick:** **"Always put map.put(0L, 1) first in Prefix HashMap problems!"**

## 13. Comparisons
| Technique | Sliding Window | Prefix Sum + HashMap |
| :--- | :--- | :--- |
| **Array Constraint** | Positive elements only (Monotonic) | **Handles negative elements** |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Space Complexity**| **$O(1)$ (Optimal)** | $O(N)$ (HashMap storage) |
| **Query Speed** | Single pass | Single pass with Hash lookups |

## 14. How to Recognize This in Questions
* **"Multiple range sum queries on static array"** $\rightarrow$ Prefix Sum Array ($O(1)$ query).
* **"Find number of subarrays summing to K (with negative numbers)"** $\rightarrow$ Prefix Sum + HashMap.
* **"Find equilibrium index where left sum equals right sum"** $\rightarrow$ Total Sum vs Prefix Sum.

## 15. Frequently Asked Interview Questions
* **Q: Why does 1-indexed prefix array `prefix[N + 1]` simplify code?**  
  *A:* By setting `prefix[0] = 0`, the range sum formula `prefix[R + 1] - prefix[L]` works universally for all ranges $L \le R$, eliminating special conditional branches for $L = 0$.
* **Q: How do you find the equilibrium index of an array in $O(n)$ time and $O(1)$ space?**  
  *A:* Compute total array sum $S$. Iterate through array maintaining `leftSum`. At index $i$, `rightSum = S - leftSum - arr[i]`. If `leftSum == rightSum`, $i$ is an equilibrium index.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PREFIX SUM TECHNIQUE                                  |
+-----------------------------------------------------------------------+
| • Range Sum(L, R) = prefix[R + 1] - prefix[L] (1-indexed prefix array)|
| • Always use long[] for prefix array to prevent Integer Overflow     |
| • Negative numbers present? Use Prefix Sum + HashMap, NOT Sliding Window|
| • Subarray Sum K Trick: Target = currentPrefix - K; Map init: (0L, 1) |
| • Equilibrium Index: leftSum == totalSum - leftSum - arr[i]          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can build a 1-indexed Prefix Sum array in $O(n)$ time.
- [ ] I know why `long[]` must be used for prefix sum accumulation.
- [ ] I can solve LeetCode 560 (Subarray Sum Equals K) using Prefix Sum + HashMap.
- [ ] I know why Sliding Window fails when negative numbers are present.
- [ ] I can find array equilibrium index in $O(n)$ time and $O(1)$ space.
