# 04. Sliding Window Maximum & Monotonic Deque Pattern

## 1. Introduction
The **Sliding Window Maximum** problem (LeetCode 239) is a flagship hard technical coding interview problem that tests real-time range query optimization. Given an array of integers `nums` and a sliding window of size $K$ moving from left to right, we must find the maximum value inside the window at each step. While a naive solution takes $O(N \cdot K)$ time, the **Monotonic Deque** pattern solves this problem in **$O(N)$ linear time and $O(K)$ space**.

> **Important:** In Sliding Window Maximum, the Monotonic Deque stores **ARRAY INDICES**, maintaining array values in strictly **decreasing order**. The front of the deque (`peekFirst()`) ALWAYS holds the index of the maximum element in the active window!

## 2. Core Concepts
* **Monotonic Decreasing Deque Invariant**:
  $$\text{nums}[\text{deque.peekFirst()}] \ge \text{nums}[\text{deque.second()}] \ge \dots \ge \text{nums}[\text{deque.peekLast()}]$$
* **3-Phase Window Step Pipeline**:
  1. **Evict Out-of-Bound Indices (Front)**: If `deque.peekFirst() <= i - K`, poll from front (`deque.pollFirst()`).
  2. **Evict Smaller Elements (Rear)**: While `!deque.isEmpty()` and `nums[i] >= nums[deque.peekLast()]`, poll from rear (`deque.pollLast()`).
  3. **Offer Current Index (Rear)**: `deque.offerLast(i)`.
  4. **Record Window Maximum**: When $i \ge K - 1$, `result[i - K + 1] = nums[deque.peekFirst()]`.

> **Memory Trick:** **"Front evicts out-of-bounds (peekFirst <= i - K); Rear evicts smaller values (nums[i] >= nums[peekLast])!"**

## 3. Characteristics / Properties
* **Amortized Linear $O(N)$ Time Proof**: Every array index is pushed to `deque` once via `offerLast()` and popped at most once (either via `pollFirst()` or `pollLast()`). Total operations across all $N$ steps are bounded by $2N \implies \mathbf{O(N)\text{ Time Complexity}}$.

```
Sliding Window Maximum Approaches Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Approach              | Time Complexity   | Auxiliary Space   | Performance       |
+-----------------------+-------------------+-------------------+-------------------+
| Brute Force Window    | O(N * K)          | O(1) Constant     | TLE (Too Slow)    |
| Max-Heap (PriorityQueue)| O(N log K)      | O(K) Heap Memory  | Moderate          |
| Monotonic Deque       | O(N) Linear ⚡   | O(K) Deque Memory | OPTIMAL EXPECTED  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Sliding Window Maximum on `nums = [1, 3, -1, -3, 5, 3, 6, 7], K = 3`:

```
i=0 (1):  deque: [0]
i=1 (3):  3 > nums[0](1) -> pollLast(0). offerLast(1) | deque: [1]
i=2 (-1): -1 < nums[1](3) -> offerLast(2)              | deque: [1, 2]
          Window 0 [1, 3, -1]: Max = nums[1] = 3      | res[0] = 3

i=3 (-3): Out-of-bounds check: 1 > 3-3 (OK). -3 < -1 -> offerLast(3) | deque: [1, 2, 3]
          Window 1 [3, -1, -3]: Max = nums[1] = 3     | res[1] = 3

i=4 (5):  Out-of-bounds check: 1 <= 4-3 -> pollFirst(1)!
          5 > nums[3](-3) & 5 > nums[2](-1) -> pollLast(3), pollLast(2). offerLast(4) | deque: [4]
          Window 2 [-1, -3, 5]: Max = nums[4] = 5     | res[2] = 5

... Continue to end ...
Final Result Array: [3, 3, 5, 5, 6, 7] ✅ (Linear O(N) Time!)
```

## 5. Visual Diagram
Sliding Window Monotonic Deque Mechanics:

```
Active Window: [ -1, -3, 5 ]  (Indices 2, 3, 4)

Step 1: Evict out-of-bound indices from FRONT (peekFirst() <= i - K)
Step 2: Evict smaller elements from REAR (nums[i] >= nums[peekLast()])
Step 3: Insert index i at REAR (offerLast(i))
Step 4: Window Maximum is ALWAYS at FRONT (nums[peekFirst()])
```

## 6. Operations / Algorithms
LeetCode 239 Master Implementation:

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    if (nums == null || nums.length == 0 || k <= 0) return new int[0];

    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // Stores INDICES

    for (int i = 0; i < n; i++) {
        // Step 1: Evict out-of-bound indices from FRONT
        if (!deque.isEmpty() && deque.peekFirst() <= i - k) {
            deque.pollFirst();
        }

        // Step 2: Evict smaller element indices from REAR
        while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) {
            deque.pollLast();
        }

        // Step 3: Offer current index to REAR
        deque.offerLast(i);

        // Step 4: Record maximum when window reaches size K
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }

    return result;
}
```

> **Quick Syntax:**
```java
// 4-Step Monotonic Deque Loop Sequence
if (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) deque.pollLast();
deque.offerLast(i);
if (i >= k - 1) result[i - k + 1] = nums[deque.peekFirst()];
```

## 7. Examples
* **LeetCode 239 - Sliding Window Maximum**: Standard Monotonic Deque sliding window maximum.
* **LeetCode 1696 - Jump Game VI**: Dynamic Programming + Monotonic Deque window optimization.
* **LeetCode 862 - Shortest Subarray with Sum at Least K**: Prefix Sums + Monotonic Deque.

## 8. Java Code
Complete interview-ready Java suite implementing Sliding Window Maximum (LeetCode 239) and Constrained Subsequence Sum (LeetCode 1425):

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class SlidingWindowMaximumMaster {

    // 1. Sliding Window Maximum (LeetCode 239) O(N) Time, O(K) Space
    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];

        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            // 1. Evict out-of-bounds from Front
            if (!deque.isEmpty() && deque.peekFirst() <= i - k) {
                deque.pollFirst();
            }

            // 2. Evict smaller values from Rear
            while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) {
                deque.pollLast();
            }

            // 3. Offer current index to Rear
            deque.offerLast(i);

            // 4. Record result once window size K is reached
            if (i >= k - 1) {
                result[i - k + 1] = nums[deque.peekFirst()];
            }
        }

        return result;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums = {1, 3, -1, -3, 5, 3, 6, 7};
        int k = 3;

        int[] maxWindow = maxSlidingWindow(nums, k);
        System.out.println("Sliding Window Max (K=3): " + Arrays.toString(maxWindow));
        // Output: [3, 3, 5, 5, 6, 7]
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Monotonic Deque Window** | **$O(N)$ Linear** | **$O(K)$ Deque Space** | Each index pushed/popped at most once |
| **Max-Heap Window** | $O(N \log K)$ | $O(K)$ Heap Memory | Heap poll/offer cost |
| **Brute Force Window** | $O(N \cdot K)$ | $O(1)$ Constant | Inner max loop per window |

## 10. Edge Cases
* **$K = 1$**: Output array is identical to input `nums` array.
* **$K = N$**: Output array contains single element: the maximum of the entire array.
* **Duplicates in Window (e.g. `[2, 2, 2], K=2`)**: Eviction loop condition `nums[i] >= nums[deque.peekLast()]` (with `>=`) evicts older duplicates cleanly.

## 11. Common Mistakes
* Storing raw values (`nums[i]`) instead of **INDICES `i`** on deque (prevents out-of-bounds check `deque.peekFirst() <= i - k`!).
* Using `>` instead of `>=` in `nums[i] >= nums[deque.peekLast()]` (retains unnecessary duplicate elements on deque).
* Off-by-one errors in window result index `i - k + 1`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Store INDICES, Not Values!
> The Monotonic Deque MUST store **array indices `i`**: `deque.offerLast(i)`.
> Storing indices enables TWO critical operations:
> 1. Checking out-of-bound expiry at FRONT: **`deque.peekFirst() <= i - k`**
> 2. Comparing values at REAR: **`nums[i] >= nums[deque.peekLast()]`**

> **Memory Trick:** **"Front evicts expired indices (peekFirst <= i - K); Rear evicts smaller values!"**

## 13. Comparisons
| Feature | Max-Heap PriorityQueue | Monotonic Deque |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log K)$ | **$O(N)$ Amortized Linear ⚡** |
| **Out-of-Bound Eviction**| Lazy / Complex $O(K)$ | **Instant $O(1)$ Front Poll** |
| **Interview Recommendation** | Sub-optimal | **OPTIMAL EXPECTED ANSWER** |

## 14. How to Recognize This in Questions
* **"Find maximum/minimum in every contiguous subarray of size K"** $\rightarrow$ Monotonic Deque (LeetCode 239).
* **"Optimize DP recurrence over sliding range [i-K, i-1]"** $\rightarrow$ DP + Monotonic Deque (LeetCode 1425).

## 15. Frequently Asked Interview Questions
* **Q: Why does Monotonic Deque run in $O(N)$ time despite having a `while` loop inside a `for` loop?**  
  *A:* Across all $N$ loop iterations, each index enters the deque exactly once via `offerLast()` and is popped at most once (via `pollFirst()` or `pollLast()`). The total number of pops across the entire algorithm execution cannot exceed $N$, yielding an amortized time complexity of $O(N)$.
* **Q: Why must we store indices instead of values in the deque?**  
  *A:* Indices allow us to check if the element at the front of the deque has fallen out of the active sliding window (`deque.peekFirst() <= i - k`) in $O(1)$ time, while still allowing value lookup via `nums[deque.peekFirst()]`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SLIDING WINDOW MAXIMUM & MONOTONIC DEQUE              |
+-----------------------------------------------------------------------+
| • Deque Content: Store INDICES i (deque.offerLast(i))                 |
| • Step 1 (Front Expiry): if (peekFirst() <= i - k) pollFirst();       |
| • Step 2 (Rear Eviction): while (nums[i] >= nums[peekLast()]) pollLast();|
| • Step 3 (Offer Rear): offerLast(i);                                  |
| • Step 4 (Record Max): if (i >= k - 1) res[i - k + 1] = nums[peekFirst()];|
| • Complexity: O(N) Linear Time | O(K) Auxiliary Deque Space           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why Monotonic Deque stores array indices `i` rather than values.
- [ ] I can write the 4-step window pipeline in under 3 minutes.
- [ ] I can write the Front out-of-bound check `deque.peekFirst() <= i - k`.
- [ ] I can write the Rear smaller value eviction `nums[i] >= nums[deque.peekLast()]`.
- [ ] I can solve LeetCode 239 in $O(N)$ time from memory.
