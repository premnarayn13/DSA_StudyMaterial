# 07. Generalized K-Sum Framework, 4Sum & 64-Bit Integer Overflow Safeguards

## 1. Introduction
The **Generalized $K$-Sum Problem Family** extends 2Sum and 3Sum to arbitrary $K$-element target sum combinations (such as **4Sum - LeetCode 18**). While a naive brute-force approach consumes $O(N^K)$ polynomial time, the generalized recursive $K$-Sum algorithm reduces complexity to **$O(N^{K-1})$ time with $O(1)$ constant auxiliary space** by recursively fixing $K-2$ anchor elements and executing a base-case Two-Pointer search on the remaining two elements.

> **Important:** In 4Sum (LeetCode 18), summing 4 integers near $\pm 10^9$ causes **32-bit Integer Overflow** (`2,000,000,000 + 2,000,000,000` exceeds `Integer.MAX_VALUE = 2,147,483,647`). The $K$-Sum algorithm MUST cast target sum calculations to **64-bit `long`** (`(long) target - nums[i]`) to prevent arithmetic wrapping bugs!

```
K-Sum Complexity Reduction Hierarchy:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Brute Force Time  | Generalized K-Sum | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| 2Sum (Sorted)         | $O(N^2)$          | **$O(N)$ ⚡**     | Converging 2-Pointer|
| 3Sum (15)             | $O(N^3)$          | **$O(N^2)$ ⚡**   | 1 Anchor + 2Sum   |
| 4Sum (18)             | $O(N^4)$          | **$O(N^3)$ ⚡**   | 2 Anchors + 2Sum  |
| Generalized K-Sum     | $O(N^K)$          | **$O(N^{K-1})$ ⚡**| (K-2) Anchors + 2Sum|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 2. Core Concepts & Generalized $K$-Sum Recursive Architecture

### 2.1 The Generalized Recursive $K$-Sum Paradigm
Any $K$-Sum problem (where $K \ge 2$) on a sorted array `nums` can be decomposed recursively:
1. **Base Case ($K = 2$)**: Run standard converging Two-Pointer search (`twoSum`) on the sub-array `nums[start ... N-1]`.
2. **Recursive Step ($K > 2$)**: Loop `i` from `start` to $N - K$:
   - Skip duplicates: `if (i > start && nums[i] == nums[i - 1]) continue;`
   - **Pruning Check 1 (Sum Too Small)**: If $K \cdot \text{nums}[i] > \text{target}$, break loop! (Since array is sorted, remaining elements are too large).
   - **Pruning Check 2 (Sum Too Large)**: If $\text{nums}[i] + (K-1) \cdot \text{nums}[N-1] < \text{target}$, continue! (Max possible sum from `i` is too small).
   - Recursively solve **`kSum(K - 1, i + 1, target - nums[i])`**.
   - Prepend `nums[i]` to all returned $(K-1)$-tuples.

```
4Sum Recursive Reduction Tree (K = 4):
kSum(4, start=0, target)
  |---> Fix Anchor i: kSum(3, start=i+1, target - nums[i])
           |---> Fix Anchor j: kSum(2, start=j+1, target - nums[i] - nums[j])
                    |---> Converging 2-Pointer Base Case (Returns Pairs!)
```

> **Memory Trick:** **"K-Sum reduces to (K-2) anchor loops + 2-pointer base case! Always use 64-bit long for sum targets!"**

---

## 3. Characteristics & 64-Bit Overflow Protection

### 3.1 32-Bit Integer Overflow Safeguard in 4Sum (LeetCode 18)
Consider `nums = [1000000000, 1000000000, 1000000000, 1000000000]` and `target = 0`.
* Evaluating `int sum = nums[i] + nums[j] + nums[left] + nums[right]` yields `4,000,000,000`, which wraps around in 32-bit signed integer arithmetic to **`-294,967,296`**!
* **Safeguard**: Cast sub-target subtractions and sum additions to **64-bit `long`**:

```java
long sum = (long) nums[i] + nums[j] + nums[left] + nums[right];
long remainingTarget = (long) target - nums[i];
```

---

## 4. Internal Working Mechanics
Tracing 4Sum (LeetCode 18) on `nums = [1, 0, -1, 0, -2, 2]`, `target = 0`:

```
Step 1: Sort nums -> [-2, -1, 0, 0, 1, 2] (N = 6)

kSum(k=4, start=0, target=0):
  i = 0 (val -2): Recurse kSum(k=3, start=1, target=2)
    j = 1 (val -1): Recurse kSum(k=2, start=2, target=3)
      2-Pointer on [0, 0, 1, 2]: left=2(0), right=5(2) -> sum=2 < 3 -> left++
      left=4(1), right=5(2) -> sum = 1 + 2 = 3 == 3! -> Found [-2, -1, 1, 2]!

  i = 1 (val -1): Recurse kSum(k=3, start=2, target=1)
    j = 2 (val 0): Recurse kSum(k=2, start=3, target=1)
      2-Pointer on [0, 1, 2]: left=3(0), right=5(2) -> sum=2 > 1 -> right--
      left=3(0), right=4(1) -> sum = 0 + 1 = 1 == 1! -> Found [-1, 0, 0, 1]!

Result: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]] ✅ (O(N^3) Time!)
```

---

## 5. Visual Diagram
Generalized K-Sum Recursive Reduction Topology:

```
Level 0: 4Sum (K = 4) --------> Fix Anchor 1 (nums[i])
                                     |
Level 1: 3Sum (K = 3) -------------> Fix Anchor 2 (nums[j])
                                          |
Level 2: 2Sum Base Case (K = 2) --------> Converging Two Pointers (left, right)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing 4Sum (LeetCode 18) and the Generalized $K$-Sum Recursive Framework:

```java
import java.util.*;

public class KSumProblemsMaster {

    // 1. 4Sum (LeetCode 18) O(N^3) Time, O(1) Auxiliary Space
    public static List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        return kSum(nums, (long) target, 4, 0);
    }

    // 2. Generalized Recursive K-Sum Engine O(N^(K-1)) Time
    public static List<List<Integer>> kSum(int[] nums, long target, int k, int start) {
        List<List<Integer>> result = new ArrayList<>();
        int n = nums.length;

        if (start >= n) return result;

        // Base Case: 2Sum Converging Two Pointers
        if (k == 2) {
            int left = start;
            int right = n - 1;

            while (left < right) {
                long sum = (long) nums[left] + nums[right];

                if (sum == target) {
                    List<Integer> pair = new ArrayList<>();
                    pair.add(nums[left]);
                    pair.add(nums[right]);
                    result.add(pair);

                    // Skip left duplicates
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    // Skip right duplicates
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < target) {
                    left++;
                } else {
                    right--;
                }
            }

            return result;
        }

        // Recursive Step: K > 2 (Fix Anchor and Recurse K - 1)
        for (int i = start; i < n - k + 1; i++) {
            // Anchor Duplicate Skipping
            if (i > start && nums[i] == nums[i - 1]) continue;

            // Pruning Check 1: Smallest possible K-sum > target -> Impossible!
            if ((long) nums[i] * k > target) break;

            // Pruning Check 2: Largest possible K-sum < target -> Try next anchor!
            if ((long) nums[i] + (long) (k - 1) * nums[n - 1] < target) continue;

            // Recurse for (k - 1) sum
            List<List<Integer>> subResults = kSum(nums, target - nums[i], k - 1, i + 1);

            for (List<Integer> sub : subResults) {
                List<Integer> list = new ArrayList<>();
                list.add(nums[i]);
                list.addAll(sub);
                result.add(list);
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// 64-Bit Overflow Protection Casts in K-Sum
long sum = (long) nums[left] + nums[right];
List<List<Integer>> subResults = kSum(nums, target - nums[i], k - 1, i + 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 18 - 4Sum**: 4-element target sum combinations.
* **LeetCode 454 - 4Sum II**: HashMap $O(N^2)$ algorithm across 4 independent arrays.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing 4Sum and Generalized 5-Sum:

```java
public class KSumProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. 4Sum (LeetCode 18, Target = 0) ===");
        int[] nums1 = {1, 0, -1, 0, -2, 2};
        List<List<Integer>> res4Sum = KSumProblemsMaster.fourSum(nums1, 0);
        System.out.println("4Sum Unique Quadruplets: " + res4Sum);
        // Output: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]

        System.out.println("\n=== 2. 64-Bit Integer Overflow Safeguard Test ===");
        int[] numsOverflow = {1000000000, 1000000000, 1000000000, 1000000000};
        List<List<Integer>> resOverflow = KSumProblemsMaster.fourSum(numsOverflow, 0);
        System.out.println("Overflow Test Result (Expected empty): " + resOverflow); // Output: []
    }
}
```

---

## 9. Complexity Analysis

| Problem Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **4Sum (18)** | **$O(N^3)$ Cubic ⚡** | **$O(1)$ Auxiliary ⚡**| 2 Anchor loops + 2-pointer base case |
| **Generalized K-Sum** | **$O(N^{K-1})$ Polynomial⚡**| $O(K)$ Call Stack | Recursion depth $K - 2$ |

---

## 10. Edge Cases & Boundary Handling
* **32-Bit Integer Overflow**: Prevents `target - nums[i]` or `nums[left] + nums[right]` wrapping around negative values using `long` casts.
* **Array Length $< K$**: Returns empty list immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `int sum = nums[i] + nums[j] + nums[left] + nums[right]` Without Long Casting**:
  - Accumulating four large 32-bit integers causes integer overflow and incorrect comparisons!
  - **Cast to `long` (`(long) nums[i] + ...`) BEFORE addition**.
* **Hardcoding Separate Methods for 3Sum, 4Sum, 5Sum**:
  - Writing redundant nested loops for each $K$ creates unmaintainable code.
  - **Use the Generalized Recursive `kSum` framework**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Pruning Optimizations in K-Sum:
> 1. **Smallest K-Sum Pruning**: If `nums[i] * k > target`, break immediately! (No remaining elements can sum to target).
> 2. **Largest K-Sum Pruning**: If `nums[i] + (k - 1) * nums[n - 1] < target`, continue! (Current anchor is too small even with largest possible elements).

> **Memory Trick:** **"K-Sum pruning: If nums[i]*K > target break! If nums[i] + (K-1)*max < target continue!"**

---

## 13. System & Implementation Comparisons

| Feature | Generalized Recursive K-Sum | Flat Nested Loops |
| :--- | :--- | :--- |
| **Generality** | **Handles any K (3, 4, 5...) ⚡**| Rigid (Hardcoded for single K) |
| **Pruning Support** | Built-in (2 Early Pruning Checks) | Complex |
| **Time Complexity** | $O(N^{K-1})$ | $O(N^{K-1})$ |

---

## 14. How to Recognize This in Questions
* **"Find all unique quadruplets that sum to target"** $\rightarrow$ LeetCode 18 (4Sum with `long` casting).
* **"Find K elements in sorted array that sum to target"** $\rightarrow$ Generalized $K$-Sum framework.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the Generalized $K$-Sum framework run in $O(N^{K-1})$ time?**  
  *A:* The recursive calls fix $K-2$ anchor elements using nested loops, which takes $O(N^{K-2})$ time. The base case executes a Two-Pointer search in $O(N)$ time. Total complexity is $O(N^{K-2}) \times O(N) = \mathbf{O(N^{K-1})\text{ Time}}$.
* **Q: Why are 64-bit `long` casts necessary in LeetCode 18?**  
  *A:* Input values in 4Sum can be up to $10^9$. Adding four such values produces $4 \times 10^9$, which exceeds 32-bit `Integer.MAX_VALUE` ($2.14 \times 10^9$), causing integer overflow and incorrect search logic.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GENERALIZED K-SUM FRAMEWORK                           |
+-----------------------------------------------------------------------+
| • Recursive Reduction: Reduces K-Sum to (K-2) anchors + 2Sum base case|
| • Time Complexity: O(N^(K-1)) Time across all K >= 2                  |
| • 64-Bit Overflow Protection: Cast target & sum to long!              |
| • Pruning Check 1: if ((long) nums[i] * k > target) break;            |
| • Pruning Check 2: if ((long) nums[i] + (k-1)*nums[n-1] < target) continue;|
| • Duplicate Skipping: if (i > start && nums[i] == nums[i-1]) continue;|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 4Sum (LeetCode 18) with 64-bit `long` casting.
- [ ] I can implement the Generalized Recursive `kSum` framework.
- [ ] I can state both K-Sum pruning optimizations.
- [ ] I know why 32-bit integer overflow occurs in 4Sum.
- [ ] I know why $K$-Sum runs in $O(N^{K-1})$ time.
