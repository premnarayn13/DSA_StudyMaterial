# 10. Advanced Sliding Window Tricks, Dual Monotonic Deques & At Most K Reductions

## 1. Introduction
Advanced Sliding Window techniques tackle complex non-monotonic, multi-deque, and exact-count structural constraints. By pairing two monotonic deques—a **Max Deque** and a **Min Deque**—or applying the **At Most K Mathematical Reduction**, algorithms like **Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit (LeetCode 1438)** and **Subarrays with K Different Integers (LeetCode 992)** achieve **$O(N)$ linear time and $O(N)$ auxiliary space**.

> **Important:** In **Longest Subarray With Absolute Diff $\le$ Limit (LeetCode 1438)**, maintaining TWO deques simultaneously (a monotonic decreasing `maxDeque` and a monotonic increasing `minDeque`) provides the max element (`maxDeque.peekFirst()`) and min element (`minDeque.peekFirst()`) of the current window in **$O(1)$ constant time**. The window condition is valid iff:
> $$\text{maxDeque.peekFirst()} - \text{minDeque.peekFirst()} \le \text{Limit}$$

```
Dual Monotonic Deque Window Limit Topology:
+-----------------------------------------------------------------------------------+
| Max Deque (Decreasing) : Head holds MAX element in current window                 |
| Min Deque (Increasing) : Head holds MIN element in current window                 |
| Validity Condition     : maxDeque.peekFirst() - minDeque.peekFirst() <= Limit ⚡  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Dual Monotonic Deque Mechanics (LeetCode 1438)

### 2.1 Longest Continuous Subarray With Absolute Diff $\le$ Limit (LeetCode 1438)
Given an integer array `nums` and integer `limit`, return the size of the longest non-empty subarray such that the absolute difference between any two elements is $\le \text{limit}$:

#### Algorithm ($O(N)$ Time, $O(N)$ Auxiliary Space):
1. Maintain two deques: `Deque<Integer> maxDeque` (decreasing) and `Deque<Integer> minDeque` (increasing).
2. `left = 0`, `maxLen = 0`.
3. For `right = 0` to $N - 1$:
   - **Update Max Deque**: While `!maxDeque.isEmpty() && maxDeque.peekLast() < nums[right]`, `maxDeque.pollLast()`. `maxDeque.offerLast(nums[right])`.
   - **Update Min Deque**: While `!minDeque.isEmpty() && minDeque.peekLast() > nums[right]`, `minDeque.pollLast()`. `minDeque.offerLast(nums[right])`.
   - **Shrink Window While Invalid**: While `maxDeque.peekFirst() - minDeque.peekFirst() > limit`:
     - If `maxDeque.peekFirst() == nums[left]`, `maxDeque.pollFirst()`.
     - If `minDeque.peekFirst() == nums[left]`, `minDeque.pollFirst()`.
     - `left++`.
   - **Record Answer**: `maxLen = Math.max(maxLen, right - left + 1)`.
4. Return `maxLen`.

```
Why Dual Deques Solve Min/Max Window Query in O(1) Time:
Maintaining a single max or min using a Heap requires O(log N) operations.
Maintaining two monotonic deques allows instant O(1) queries for both max AND min elements! ⚡
```

> **Memory Trick:** **"Dual Deques (1438): maxDeque peekFirst() - minDeque peekFirst() <= limit! Purge tail on insert, poll head on left shrink!"**

---

## 3. Characteristics & Subarrays with K Different Integers (LeetCode 992)

### 3.1 Subarrays with K Different Integers (LeetCode 992)
Given an integer array `nums` and integer $K$, return the number of good subarrays that contain **exactly $K$ different integers**:

#### The At Most K Mathematical Transformation:
* Standard sliding window cannot easily count "Exactly $K$" distinct elements because shrinking `left` might reduce distinct count below $K$ while valid prefix sub-segments remain.
* **Reduction Formula**:

$$\text{Subarrays(Exactly } K) = \text{atMostK}(nums, K) - \text{atMostK}(nums, K - 1)$$

```java
public static int subarraysWithKDistinct(int[] nums, int k) {
    return atMostKDistinct(nums, k) - atMostKDistinct(nums, k - 1);
}

private static int atMostKDistinct(int[] nums, int k) {
    int[] count = new int[nums.length + 1];
    int left = 0, total = 0, distinctCount = 0;

    for (int right = 0; right < nums.length; right++) {
        if (count[nums[right]]++ == 0) distinctCount++;

        while (distinctCount > k) {
            if (--count[nums[left++]] == 0) distinctCount--;
        }

        total += (right - left + 1); // Subarray range accumulation formula!
    }

    return total;
}
```

---

## 4. Internal Working Mechanics
Tracing Dual Deque Absolute Diff $\le$ Limit (LeetCode 1438) on `nums = [8, 2, 4, 7]`, `limit = 4`:

```
Init: left = 0, maxLen = 0

right = 0 (val 8): maxDeque = [8], minDeque = [8]. diff = 0 <= 4. maxLen = 1.
right = 1 (val 2):
  - maxDeque = [8, 2] (8 > 2)
  - minDeque = [2] (8 > 2 -> purge 8)
  - diff = 8 - 2 = 6 > 4 -> INVALID!
  - Shrink left=0 (val 8): maxDeque.peekFirst() == 8 -> pollFirst(8). left = 1.
  - Window [2] (left=1, right=1). diff = 2 - 2 = 0 <= 4. maxLen = 1.

right = 2 (val 4):
  - maxDeque = [4] (2 < 4 -> purge 2)
  - minDeque = [2, 4] (2 < 4)
  - diff = 4 - 2 = 2 <= 4 -> VALID!
  - maxLen = max(1, 2 - 1 + 1) = 2 ([2, 4]).

right = 3 (val 7):
  - maxDeque = [7] (4 < 7 -> purge 4)
  - minDeque = [2, 4, 7]
  - diff = 7 - 2 = 5 > 4 -> INVALID!
  - Shrink left=1 (val 2): minDeque.peekFirst() == 2 -> pollFirst(2). left = 2.
  - Window [4, 7] (left=2, right=3). diff = 7 - 4 = 3 <= 4 -> VALID!
  - maxLen = max(2, 3 - 2 + 1) = 2 ([4, 7]).

Max Subarray Length = 2 ([2, 4] or [4, 7]) ✅ (O(N) Time, O(N) Space!)
```

---

## 5. Visual Diagram
Dual Monotonic Deque Max/Min Window Boundary Tracking Topography:

```
Window [ 2, 4, 7 ] (limit = 4):
  Max Deque Head -> [ 7 ] <- Max Deque Tail
  Min Deque Head -> [ 2, 4, 7 ] <- Min Deque Tail
  Diff = 7 - 2 = 5 > 4 (INVALID -> Poll minDeque head 2, left++)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Dual Monotonic Deque Absolute Limit (LeetCode 1438) and Subarrays with K Different Integers (LeetCode 992):

```java
import java.util.*;

public class AdvancedTricksMaster {

    // 1. Longest Continuous Subarray With Absolute Diff <= Limit (LeetCode 1438) O(N) Time, O(N) Space
    public static int longestSubarray(int[] nums, int limit) {
        if (nums == null || nums.length == 0) return 0;

        Deque<Integer> maxDeque = new ArrayDeque<>();
        Deque<Integer> minDeque = new ArrayDeque<>();

        int left = 0;
        int maxLen = 0;

        for (int right = 0; right < nums.length; right++) {
            int val = nums[right];

            // Maintain decreasing maxDeque
            while (!maxDeque.isEmpty() && maxDeque.peekLast() < val) {
                maxDeque.pollLast();
            }
            maxDeque.offerLast(val);

            // Maintain increasing minDeque
            while (!minDeque.isEmpty() && minDeque.peekLast() > val) {
                minDeque.pollLast();
            }
            minDeque.offerLast(val);

            // Shrink window while (max - min) > limit
            while (maxDeque.peekFirst() - minDeque.peekFirst() > limit) {
                if (maxDeque.peekFirst() == nums[left]) {
                    maxDeque.pollFirst();
                }
                if (minDeque.peekFirst() == nums[left]) {
                    minDeque.pollFirst();
                }
                left++;
            }

            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }

    // 2. Subarrays with K Different Integers (LeetCode 992) O(N) Time, O(N) Space
    public static int subarraysWithKDistinct(int[] nums, int k) {
        return atMostKDistinct(nums, k) - atMostKDistinct(nums, k - 1);
    }

    private static int atMostKDistinct(int[] nums, int k) {
        if (k <= 0) return 0;

        int[] count = new int[nums.length + 1];
        int left = 0;
        int totalSubarrays = 0;
        int distinctCount = 0;

        for (int right = 0; right < nums.length; right++) {
            if (count[nums[right]] == 0) {
                distinctCount++;
            }
            count[nums[right]]++;

            // Shrink window while distinct elements > k
            while (distinctCount > k) {
                count[nums[left]]--;
                if (count[nums[left]] == 0) {
                    distinctCount--;
                }
                left++;
            }

            // Count valid subarrays ending at right
            totalSubarrays += (right - left + 1);
        }

        return totalSubarrays;
    }
}
```

> **Quick Syntax:**
```java
// Dual Deque Max/Min Diff Check Line
while (maxDeque.peekFirst() - minDeque.peekFirst() > limit) {
    if (maxDeque.peekFirst() == nums[left]) maxDeque.pollFirst();
    if (minDeque.peekFirst() == nums[left]) minDeque.pollFirst();
    left++;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 1438 - Longest Continuous Subarray With Absolute Diff $\le$ Limit**: Dual Monotonic Deques.
* **LeetCode 992 - Subarrays with K Different Integers**: `atMost(K) - atMost(K - 1)` transformation.
* **LeetCode 862 - Shortest Subarray with Sum at Least K**: Monotonic Queue + Prefix Sums.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Dual Monotonic Deques and Subarrays with K Distinct Integers:

```java
public class AdvancedTricksDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Absolute Diff <= Limit (LeetCode 1438, Limit=4) ===");
        int[] nums1 = {8, 2, 4, 7};
        int maxLen = AdvancedTricksMaster.longestSubarray(nums1, 4);
        System.out.println("Longest Subarray Length: " + maxLen); // Output: 2 ([2, 4] or [4, 7])

        System.out.println("\n=== 2. Subarrays with K Distinct (LeetCode 992, K=2) ===");
        int[] nums2 = {1, 2, 1, 2, 3};
        int exactKCount = AdvancedTricksMaster.subarraysWithKDistinct(nums2, 2);
        System.out.println("Subarrays with Exactly 2 Distinct: " + exactKCount); // Output: 7
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Abs Diff Limit (1438)** | **$O(N)$ Linear ⚡** | $O(N)$ Deque Space | Dual Deque $O(1)$ max/min queries |
| **K Distinct Subarrays (992)**| **$O(N)$ Linear ⚡** | $O(N)$ Frequency Array| `atMost(K) - atMost(K - 1)` reduction |

---

## 10. Edge Cases & Boundary Handling
* **$K = 0$ in Subarrays with $K$ Distinct**: `atMostKDistinct(nums, 0)` returns `0` immediately.
* **Single Element Array**: Deques handle $N=1$ inputs cleanly, returning `1`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `TreeMap` for Min/Max Window Queries ($O(N \log N)$ Time Penalty)**:
  - Storing window elements in a `TreeMap` allows $O(1)$ min/max queries but costs $O(\log N)$ on every insert/delete.
  - **Use Dual Monotonic Deques for true $O(N)$ amortized linear execution**.
* **Comparing Values Instead of Head Elements in Dual Deques**:
  - Forgetting to check `maxDeque.peekFirst() == nums[left]` before polling head elements causes incorrect de-synchronization.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Dual Deque Monotonic Property Rules:
> * **`maxDeque`**: Monotonic DECREASING (Head is MAX). Purge tail while `peekLast() < val`.
> * **`minDeque`**: Monotonic INCREASING (Head is MIN). Purge tail while `peekLast() > val`.
> This guarantees $O(1)$ constant time access to both extreme values of the current window!

> **Memory Trick:** **"maxDeque is DECREASING (Head = Max)! minDeque is INCREASING (Head = Min)!"**

---

## 13. System & Implementation Comparisons

| Feature | Dual Monotonic Deques | TreeMap Window Balancing |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \log N)$ Logarithmic |
| **Auxiliary Memory** | **$O(N)$ Deque Space ⚡** | $O(N)$ Tree Node Space |
| **Min/Max Query** | **$O(1)$ Constant ⚡** | $O(\log N)$ Tree Search |

---

## 14. How to Recognize This in Questions
* **"Find longest subarray where max - min <= limit"** $\rightarrow$ LeetCode 1438 (Dual Monotonic Deques).
* **"Find number of subarrays with EXACTLY K distinct elements"** $\rightarrow$ LeetCode 992 (`atMost(K) - atMost(K - 1)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why are Dual Monotonic Deques strictly faster than `TreeMap` for LeetCode 1438?**  
  *A:* `TreeMap` insertion and removal take $O(\log N)$ time per element, yielding $O(N \log N)$ overall time. Dual monotonic deques push and pop each index at most once, executing in **$O(N)$ Amortized Linear Time**.
* **Q: Why does `atMost(K) - atMost(K - 1)` solve exact count queries?**  
  *A:* `atMost(K)` counts subarrays with $\le K$ items. `atMost(K - 1)` counts subarrays with $\le K - 1$ items. Subtracting them isolates subarrays with EXACTLY $K$ items.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED SLIDING WINDOW TRICKS & DUAL DEQUES          |
+-----------------------------------------------------------------------+
| • Abs Diff Limit (1438): maxDeque (decreasing) & minDeque (increasing)|
| • Validity Check: while (maxDeque.peekFirst() - minDeque.peekFirst() > limit)|
| • Poll Head Rule: if (maxDeque.peekFirst() == nums[l]) maxDeque.pollFirst()|
| • Exact K Reduction: Count(Exactly K) = atMost(K) - atMost(K - 1)     |
| • Subarray Count Addition: count += (right - left + 1)                 |
| • Time Complexity: O(N) Linear Time | O(N) Deque Space ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Longest Subarray With Absolute Diff $\le$ Limit (LeetCode 1438).
- [ ] I know how Dual Monotonic Deques maintain $O(1)$ max/min window queries.
- [ ] I can solve Subarrays with K Different Integers (LeetCode 992).
- [ ] I know why `atMost(K) - atMost(K - 1)` works for exact counts.
- [ ] I can explain why Dual Deques outperform `TreeMap`.
