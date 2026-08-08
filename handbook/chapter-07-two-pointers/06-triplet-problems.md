# 06. Triplet Problems: 3Sum, 3Sum Closest & Triplet Duplicate Avoidance Mechanics

## 1. Introduction
Triplet problems represent a major leap in complexity within the Two Pointers taxonomy. By fixing one anchor element via an outer loop (`for i = 0 ... N-3`) and applying converging two pointers (`left` and `right`) on the remaining sub-array, problems like **3Sum (LeetCode 15)**, **3Sum Closest (LeetCode 16)**, and **3Sum Smaller (LeetCode 259)** reduce cubic $O(N^3)$ brute-force searches to **$O(N^2)$ quadratic time with $O(1)$ constant auxiliary space**.

> **Important:** In 3Sum (LeetCode 15), returning ONLY unique triplets requires rigorous **Duplicate Avoidance Pruning**! Both the outer anchor index `i` AND the inner converging pointers `left` and `right` MUST skip duplicate values (`while (left < right && nums[left] == nums[left+1]) left++`) to prevent duplicate triplet entries without relying on an expensive `Set<List<Integer>>`!

```
3Sum Algorithm Reduction Spectrum:
+-----------------------------------------------------------------------------------+
| Brute-Force 3 Loops  : O(N^3) Cubic Time -> Checks all N*(N-1)*(N-2)/6 triplets ❌|
| Fixed Anchor + 2Sum  : O(N^2) Quadratic Time -> Fix i, Converging 2-Pointer on rest ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & 3Sum Duplicate Avoidance Mechanics (LeetCode 15)

### 2.1 3Sum Algorithm (LeetCode 15 - Target Sum = 0)
Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that $i \ne j \ne k$ and `nums[i] + nums[j] + nums[k] == 0`:

1. **Sort Input Array**: `Arrays.sort(nums)` in ascending order ($O(N \log N)$ time).
2. **Outer Anchor Loop**: Iterate `i` from `0` to $N - 3$:
   - **Early Optimization**: If `nums[i] > 0`, break loop! (Since array is sorted, sum of 3 positive numbers can never equal 0!).
   - **Anchor Duplicate Skipping**: If `i > 0 && nums[i] == nums[i - 1]`, `continue` to next index!
3. **Inner Converging Two-Pointers**:
   - `left = i + 1`, `right = N - 1`.
   - While `left < right`:
     - `sum = nums[i] + nums[left] + nums[right]`.
     - If `sum == 0`:
       - Add `Arrays.asList(nums[i], nums[left], nums[right])` to `result`.
       - **Inner Left Duplicate Skipping**: `while (left < right && nums[left] == nums[left + 1]) left++;`
       - **Inner Right Duplicate Skipping**: `while (left < right && nums[right] == nums[right - 1]) right--;`
       - `left++; right--;`
     - Else if `sum < 0`: `left++;`
     - Else (`sum > 0`): `right--;`
4. Return `result`.

```
3Sum Anchor & Inner Pointer Duplicate Skipping:
Anchor Skip : if (i > 0 && nums[i] == nums[i - 1]) continue;
Inner Skip  : while (left < right && nums[left] == nums[left + 1]) left++;
              while (left < right && nums[right] == nums[right - 1]) right--;
              left++; right--;
```

> **Memory Trick:** **"3Sum: Fix anchor i, run 2-pointer on rest! Skip duplicate anchor AND skip duplicate inner left/right!"**

---

## 3. Characteristics & 3Sum Variants

### 3.1 3Sum Closest (LeetCode 16)
Given an integer array `nums` and target `target`, find 3 integers such that sum is closest to `target`:
1. Sort `nums`.
2. `closestSum = nums[0] + nums[1] + nums[2]`.
3. Loop `i` from `0` to $N - 3$:
   - `left = i + 1`, `right = N - 1`.
   - While `left < right`:
     - `sum = nums[i] + nums[left] + nums[right]`.
     - If `Math.abs(sum - target) < Math.abs(closestSum - target)`: `closestSum = sum;`
     - If `sum == target`: Return `target` immediately!
     - Else if `sum < target`: `left++;`
     - Else: `right--;`
4. Return `closestSum`.

### 3.2 3Sum Smaller (LeetCode 259)
Count number of triplets with sum strictly less than `target`:
* Loop `i` from `0` to $N - 3$:
  - `left = i + 1`, `right = N - 1`.
  - While `left < right`:
    - If `nums[i] + nums[left] + nums[right] < target`:
      - **Instant Range Count**: `count += (right - left);`
      - `left++;`
    - Else: `right--;`

---

## 4. Internal Working Mechanics
Tracing 3Sum (LeetCode 15) on `nums = [-1, 0, 1, 2, -1, -4]`:

```
Step 1: Sort array -> [-4, -1, -1, 0, 1, 2]

i = 0 (val -4): left = 1 (-1), right = 5 (2)
  - sum = -4 + -1 + 2 = -3 < 0 -> left++ (1)
  - sum = -4 + -1 + 2 = -3 < 0 -> left++ (0)
  - sum = -4 + 0 + 2 = -2 < 0  -> left++ (1)
  - sum = -4 + 1 + 2 = -1 < 0  -> left++ (loop ends).

i = 1 (val -1): left = 2 (-1), right = 5 (2)
  - sum = -1 + -1 + 2 = 0 == 0! -> Found [-1, -1, 2]!
    Skip duplicates: left=2 (-1), right=5 (2). left++, right-- -> left=3 (0), right=4 (1).
  - sum = -1 + 0 + 1 = 0 == 0!  -> Found [-1, 0, 1]!
    left++, right-- -> loop ends.

i = 2 (val -1): nums[2] == nums[1] -> SKIP duplicate anchor!

i = 3 (val 0): left = 4 (1), right = 5 (2)
  - sum = 0 + 1 + 2 = 3 > 0 -> right-- -> loop ends.

Result: [[-1, -1, 2], [-1, 0, 1]] ✅ (O(N^2) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
3Sum Fixed Anchor & Converging Two-Pointer Topology:

```
Sorted Array:   [ -4,   -1,   -1,    0,    1,    2 ]
                  ^      ^                       ^
               anchor   left                   right
               i = 0   (Fixed)                (Move inner pointers)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing 3Sum (LeetCode 15), 3Sum Closest (LeetCode 16), and 3Sum Smaller (LeetCode 259):

```java
import java.util.*;

public class TripletProblemsMaster {

    // 1. 3Sum (LeetCode 15) O(N^2) Time, O(1) Auxiliary Space
    public static List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null || nums.length < 3) return result;

        Arrays.sort(nums); // Sort in ascending order
        int n = nums.length;

        for (int i = 0; i < n - 2; i++) {
            // Early Optimization: If smallest element > 0, sum can never be 0
            if (nums[i] > 0) break;

            // Anchor Duplicate Skipping
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));

                    // Inner Left Duplicate Skipping
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    // Inner Right Duplicate Skipping
                    while (left < right && nums[right] == nums[right - 1]) right--;

                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }

        return result;
    }

    // 2. 3Sum Closest (LeetCode 16) O(N^2) Time, O(1) Auxiliary Space
    public static int threeSumClosest(int[] nums, int target) {
        Arrays.sort(nums);
        int n = nums.length;
        int closestSum = nums[0] + nums[1] + nums[2];

        for (int i = 0; i < n - 2; i++) {
            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (Math.abs(sum - target) < Math.abs(closestSum - target)) {
                    closestSum = sum;
                }

                if (sum == target) {
                    return target; // Exact match found
                } else if (sum < target) {
                    left++;
                } else {
                    right--;
                }
            }
        }

        return closestSum;
    }

    // 3. 3Sum Smaller (LeetCode 259) O(N^2) Time, O(1) Auxiliary Space
    public static int threeSumSmaller(int[] nums, int target) {
        Arrays.sort(nums);
        int n = nums.length;
        int count = 0;

        for (int i = 0; i < n - 2; i++) {
            int left = i + 1;
            int right = n - 1;

            while (left < right) {
                if (nums[i] + nums[left] + nums[right] < target) {
                    // All elements between left+1 and right form valid triplets
                    count += (right - left);
                    left++;
                } else {
                    right--;
                }
            }
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// 3Sum Duplicate Skipping Lines
if (i > 0 && nums[i] == nums[i - 1]) continue;
while (left < right && nums[left] == nums[left + 1]) left++;
while (left < right && nums[right] == nums[right - 1]) right--;
```

---

## 7. Concrete Problem Examples
* **LeetCode 15 - 3Sum**: Finding all unique triplets with zero sum.
* **LeetCode 16 - 3Sum Closest**: Finding 3-element sum closest to target.
* **LeetCode 259 - 3Sum Smaller**: Counting triplets with sum $< \text{target}$.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing 3Sum, 3Sum Closest, and 3Sum Smaller:

```java
public class TripletProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. 3Sum Unique Triplets (LeetCode 15) ===");
        int[] nums1 = {-1, 0, 1, 2, -1, -4};
        List<List<Integer>> triplets = TripletProblemsMaster.threeSum(nums1);
        System.out.println("Unique Triplets: " + triplets); // Output: [[-1, -1, 2], [-1, 0, 1]]

        System.out.println("\n=== 2. 3Sum Closest (LeetCode 16, target=1) ===");
        int[] nums2 = {-1, 2, 1, -4};
        int closest = TripletProblemsMaster.threeSumClosest(nums2, 1);
        System.out.println("Closest Sum: " + closest); // Output: 2 (-1 + 2 + 1)

        System.out.println("\n=== 3. 3Sum Smaller (LeetCode 259, target=2) ===");
        int[] nums3 = {-2, 0, 1, 3};
        int count = TripletProblemsMaster.threeSumSmaller(nums3, 2);
        System.out.println("Smaller Triplets Count: " + count); // Output: 2
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **3Sum (15)** | **$O(N^2)$ Quadratic ⚡**| **$O(1)$ Strict In-Place ⚡**| Outer $O(N)$ loop + Inner $O(N)$ 2-pointer |
| **3Sum Closest (16)** | **$O(N^2)$ Quadratic ⚡**| **$O(1)$ Strict In-Place ⚡**| Distance tracking `abs(sum - target)` |
| **3Sum Smaller (259)** | **$O(N^2)$ Quadratic ⚡**| **$O(1)$ Strict In-Place ⚡**| Instant range addition `count += right - left` |

---

## 10. Edge Cases & Boundary Handling
* **Array Length $< 3$**: Returns empty result list or 0 count immediately.
* **All Positive Elements (`nums[0] > 0`)**: Early break in 3Sum returns empty result instantly.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Set<List<Integer>>` for Duplicate Elimination**:
  - Pushing triplets into a `HashSet` to avoid duplicates consumes $O(N^2)$ extra memory and adds hash code computation overhead.
  - **Use explicit pointer skipping (`i > 0 && nums[i] == nums[i-1]`) for $O(1)$ space**.
* **Forgetting `left++` and `right--` After Finding Match**:
  - If `left++` and `right--` are omitted after `sum == 0`, the algorithm enters an **INFINITE LOOP**!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Dual-Tier Duplicate Skipping in 3Sum:
> To eliminate duplicate triplets without external memory:
> 1. **Anchor Tier**: `if (i > 0 && nums[i] == nums[i - 1]) continue;`
> 2. **Inner Left Tier**: `while (left < right && nums[left] == nums[left + 1]) left++;`
> 3. **Inner Right Tier**: `while (left < right && nums[right] == nums[right - 1]) right--;`
> Executing all 3 rules guarantees 100% unique triplets in $O(1)$ auxiliary space!

> **Memory Trick:** **"3Sum needs 3 skip checks: anchor (i==i-1), inner left (l==l+1), inner right (r==r-1)!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Pointer-Skipping 3Sum | Hash Set Deduplication 3Sum |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N^2)$ Set Storage |
| **Time Complexity** | **$O(N^2)$ Quadratic ⚡** | $O(N^2)$ Quadratic |
| **Code Elegance** | High (In-Place Pointer Control)| Medium (Set overhead) |

---

## 14. How to Recognize This in Questions
* **"Find all unique triplets that sum to zero"** $\rightarrow$ LeetCode 15 (3Sum with 3-tier duplicate skipping).
* **"Find three integers such that sum is closest to target"** $\rightarrow$ LeetCode 16.
* **"Count triplets with sum strictly less than target"** $\rightarrow$ LeetCode 259 (`count += right - left`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does 3Sum run in $O(N^2)$ time instead of $O(N^3)$ brute-force?**  
  *A:* By sorting the array and fixing the first element `nums[i]`, the problem reduces to finding two numbers in the remaining sorted sub-array that sum to `-nums[i]`. Two pointers solve this reduced subproblem in $O(N)$ time per anchor, yielding $N \times O(N) = \mathbf{O(N^2)\text{ Time}}$.
* **Q: Why is early break `if (nums[i] > 0) break;` valid in 3Sum?**  
  *A:* Since the array is sorted in ascending order, if `nums[i] > 0`, all subsequent elements `nums[left]` and `nums[right]` are also $> 0$. The sum of 3 positive numbers is strictly $> 0$, so no further zero-sum triplets can exist.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: 3SUM & TRIPLET PROBLEM PATTERNS                       |
+-----------------------------------------------------------------------+
| • Sort Array First: Arrays.sort(nums) is mandatory!                   |
| • Fix Anchor i: for (i = 0; i < N-2; i++)                              |
| • Early Break: if (nums[i] > 0) break;                                |
| • Anchor Skip: if (i > 0 && nums[i] == nums[i - 1]) continue;          |
| • Inner Left Skip: while (l < r && nums[l] == nums[l + 1]) l++;       |
| • Inner Right Skip: while (l < r && nums[r] == nums[r - 1]) r--;      |
| • 3Sum Smaller (259): count += (right - left) when sum < target       |
| • Complexity: O(N^2) Time | O(1) Auxiliary Space ⚡                    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 3Sum (LeetCode 15) in under 5 minutes without syntax bugs.
- [ ] I can state all 3 duplicate skipping rules in 3Sum.
- [ ] I can solve 3Sum Closest (LeetCode 16).
- [ ] I can solve 3Sum Smaller (LeetCode 259) using `count += right - left`.
- [ ] I know why early break `if (nums[i] > 0) break;` is mathematically sound.
