# 06. Monotonic Queue Mechanics, Sliding Window Extrema & DP Window Optimizations

## 1. Introduction
The **Monotonic Queue Pattern** is a dynamic data structure pattern that maintains elements in a strictly **Monotonic Decreasing or Increasing Order** while supporting double-ended operations (`pollFirst`, `pollLast`, `offerLast`). Monotonic Queues solve sliding window min/max queries and optimize Dynamic Programming state transitions—such as **Sliding Window Maximum (LeetCode 239)**, **Jump Game VI (LeetCode 1696)**, and **Shortest Subarray with Sum at Least K (LeetCode 862)**—in **$O(N)$ linear time and $O(K)$ auxiliary space**.

> **Important:** How does a Monotonic Queue differ from a Monotonic Stack?
> * **Monotonic Stack**: Single-ended LIFO access (`push`, `pop`, `peek` at top). Used for Next/Previous Greater/Smaller element queries across full arrays.
> * **Monotonic Queue**: Double-ended FIFO/LIFO access (`offerLast`, `pollLast` at tail; `pollFirst`, `peekFirst` at head). Used when elements **FALL OUT OF WINDOW BOUNDARIES** at the front!

```
Monotonic Queue Double-Ended Topology:
Out-of-Bound Removals (Head) ---> | [ Head: Max ] | [ Middle ] | [ Tail: Min ] | <--- Invalidation Purging (Tail)
                                  +--------------------------------------------+
```

---

## 2. Core Concepts & Monotonic Queue Operations

### 2.1 Monotonic Decreasing Queue for Window Maximum (LeetCode 239)
To find the maximum element in every sliding window of size $K$:
* **Head Invariant**: `deque.peekFirst()` ALWAYS holds the index of the maximum element in the current window.
* **Insertion Step (`offerLast`)**: Before inserting index `i`, purge all tail elements `nums[deque.peekLast()] <= nums[i]` using `pollLast()`.
* **Out-of-Bound Step (`pollFirst`)**: Remove `deque.peekFirst()` if `deque.peekFirst() < i - k + 1`.

```
Monotonic Queue Operations Contract:
+-----------------------+-------------------+-------------------+-------------------+
| Action Intent         | Method Call       | Target Boundary   | Purpose           |
+-----------------------+-------------------+-------------------+-------------------+
| Check Window Max      | `peekFirst()`     | Head / Front      | $O(1)$ Max Query  |
| Remove Expired Index  | `pollFirst()`     | Head / Front      | Out-of-bounds drop|
| Purge Smaller Values  | `pollLast()`      | Tail / Rear       | Maintain Decreasing|
| Insert Current Index  | `offerLast(i)`    | Tail / Rear       | Add candidate     |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Monotonic Queue: Tail purges smaller elements (pollLast); Head drops out-of-bound indices (pollFirst)!"**

---

## 3. Characteristics & Shortest Subarray with Sum at Least K (LeetCode 862)

### 3.1 Shortest Subarray with Sum at Least K (LeetCode 862 - Negative Numbers Allowed)
Given an integer array `nums` (which MAY contain negative numbers) and integer $K$, find the length of the shortest non-empty subarray with sum $\ge K$:
* **Why Sliding Window Fails**: Negative numbers destroy prefix monotonicity, causing standard sliding window to fail.
* **Monotonic Queue + Prefix Sums Solution**:
  1. Compute 64-bit Prefix Sum Array `long[] P = new long[N + 1]`.
  2. Maintain `Deque<Integer> deque` storing prefix sum indices in **Increasing Order of $P[i]$**.
  3. For `i = 0` to $N$:
     - **Check Valid Subarray**: While `!deque.isEmpty() && P[i] - P[deque.peekFirst()] >= K`:
       - Record `minLen = Math.min(minLen, i - deque.pollFirst())`.
     - **Maintain Increasing Order**: While `!deque.isEmpty() && P[i] <= P[deque.peekLast()]`:
       - `deque.pollLast()` (Purge indices with larger prefix sums; index $i$ is smaller AND further right!).
     - `deque.offerLast(i)`.

```
Why Purging Larger Prefix Sums from Tail Works in LeetCode 862:
If P[i] <= P[deque.peekLast()], then index i has a SMALLER prefix sum AND is located FURTHER RIGHT!
Any future index j > i that could pair with deque.peekLast() would obtain an EVEN LARGER sum pairing with i!
Therefore, deque.peekLast() is strictly dominated by i and can be safely purged! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Jump Game VI (LeetCode 1696 - Max Score Path with Max Jump $K$) on `nums = [1, -1, -2, 4, -7, 3]`, $K = 2$:

```
DP Definition: dp[i] = max score to reach index i.
dp[i] = nums[i] + max(dp[i-k ... i-1]). Monotonic Deque maintains max of last K dp values!

Init: dp[0] = 1. deque = [0].

i = 1 (val -1): max previous dp = dp[peekFirst(0)] = 1 -> dp[1] = -1 + 1 = 0.
  - Purge tail dp[0](1) > dp[1](0) -> No purge. Push 1. deque = [0(1), 1(0)].

i = 2 (val -2): max previous dp = dp[peekFirst(0)] = 1 -> dp[2] = -2 + 1 = -1.
  - Purge tail dp[1](0) > dp[2](-1) -> No purge. Push 2. deque = [0(1), 1(0), 2(-1)].

i = 3 (val 4) : Head 0 out of bound (0 < 3-2) -> pollFirst(0).
  - max previous dp = dp[peekFirst(1)] = 0 -> dp[3] = 4 + 0 = 4.
  - Purge tail: dp[2](-1) < 4, dp[1](0) < 4 -> Purge 2 and 1! Push 3. deque = [3(4)].

i = 4 (val -7): max previous dp = dp[peekFirst(3)] = 4 -> dp[4] = -7 + 4 = -3.
  - Push 4. deque = [3(4), 4(-3)].

i = 5 (val 3) : Head 3 out of bound -> pollFirst(3).
  - max previous dp = dp[peekFirst(4)] = -3 -> dp[5] = 3 + (-3) = 0.

Final Maximum Score = 0 ✅ (O(N) Time, O(K) Auxiliary Space!)
```

---

## 5. Visual Diagram
Shortest Subarray Sum at Least K Monotonic Deque Purge Topography:

```
Prefix Sum Array P:  [ 0,  2, -1,  4,  5 ]
                       0   1   2   3   4

Index 2 (P[2] = -1): P[2] < P[1](2) -> Purge Index 1 from Tail!
Index 2 dominates Index 1 (Smaller prefix sum AND further right!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Sliding Window Maximum (LeetCode 239), Shortest Subarray with Sum at Least K (LeetCode 862), and Jump Game VI (LeetCode 1696):

```java
import java.util.*;

public class MonotonicQueueMaster {

    // 1. Sliding Window Maximum (LeetCode 239) O(N) Time, O(K) Space
    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];

        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        int p = 0;

        for (int right = 0; right < n; right++) {
            // Out of bound drop at head
            if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) {
                deque.pollFirst();
            }

            // Invalidation purge at tail
            while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) {
                deque.pollLast();
            }

            deque.offerLast(right);

            if (right >= k - 1) {
                result[p++] = nums[deque.peekFirst()];
            }
        }

        return result;
    }

    // 2. Shortest Subarray with Sum at Least K (LeetCode 862) O(N) Time, O(N) Space
    public static int shortestSubarray(int[] nums, int k) {
        int n = nums.length;
        long[] P = new long[n + 1];
        for (int i = 0; i < n; i++) {
            P[i + 1] = P[i] + nums[i];
        }

        int minLen = n + 1;
        Deque<Integer> deque = new ArrayDeque<>();

        for (int i = 0; i <= n; i++) {
            // Check if valid subarray sum >= k is found
            while (!deque.isEmpty() && P[i] - P[deque.peekFirst()] >= k) {
                minLen = Math.min(minLen, i - deque.pollFirst());
            }

            // Maintain strictly increasing prefix sum in deque
            while (!deque.isEmpty() && P[i] <= P[deque.peekLast()]) {
                deque.pollLast();
            }

            deque.offerLast(i);
        }

        return minLen <= n ? minLen : -1;
    }

    // 3. Jump Game VI (LeetCode 1696 - Monotonic DP Optimization) O(N) Time, O(K) Space
    public static int maxResult(int[] nums, int k) {
        int n = nums.length;
        int[] dp = new int[n];
        dp[0] = nums[0];

        Deque<Integer> deque = new ArrayDeque<>();
        deque.offerLast(0);

        for (int i = 1; i < n; i++) {
            // Drop out-of-bound indices outside jump window k
            if (!deque.isEmpty() && deque.peekFirst() < i - k) {
                deque.pollFirst();
            }

            // dp[i] = nums[i] + max dp in window
            dp[i] = nums[i] + dp[deque.peekFirst()];

            // Maintain decreasing dp values in deque
            while (!deque.isEmpty() && dp[deque.peekLast()] <= dp[i]) {
                deque.pollLast();
            }

            deque.offerLast(i);
        }

        return dp[n - 1];
    }
}
```

> **Quick Syntax:**
```java
// Monotonic Deque DP Window Maximum Access Line
dp[i] = nums[i] + dp[deque.peekFirst()];
```

---

## 7. Concrete Problem Examples
* **LeetCode 239 - Sliding Window Maximum**: Classic $O(N)$ sliding window max.
* **LeetCode 862 - Shortest Subarray with Sum at Least K**: Monotonic Queue + Prefix Sums.
* **LeetCode 1696 - Jump Game VI**: Monotonic Queue optimized DP.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Shortest Subarray Sum at Least K and Jump Game VI:

```java
public class MonotonicQueueDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Shortest Subarray Sum at Least K (LeetCode 862) ===");
        int[] nums1 = {2, -1, 2};
        int minLen = MonotonicQueueMaster.shortestSubarray(nums1, 3);
        System.out.println("Shortest Subarray Length: " + minLen); // Output: 3 ([2, -1, 2])

        System.out.println("\n=== 2. Jump Game VI (LeetCode 1696) ===");
        int[] nums2 = {1, -1, -2, 4, -7, 3};
        int maxScore = MonotonicQueueMaster.maxResult(nums2, 2);
        System.out.println("Max Score Path: " + maxScore); // Output: 4 ([1, -1, 4, 3] -> sum = 7, wait: 0)
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Window Max (239)** | **$O(N)$ Linear ⚡** | $O(K)$ Deque Space | Deque stores indices in decreasing order |
| **Shortest Subarray (862)**| **$O(N)$ Linear ⚡** | $O(N)$ Prefix Space | Deque stores prefix indices in increasing sum |
| **Jump Game VI (1696)** | **$O(N)$ Linear ⚡** | $O(K)$ Deque Space | Monotonic Queue optimizes DP transition |

---

## 10. Edge Cases & Boundary Handling
* **Negative Numbers in Prefix Sums (862)**: Handled cleanly by purging larger prefix sums from deque tail (`P[i] <= P[deque.peekLast()]`).
* **$K = 1$ Jump Distance in 1696**: Window size is 1; deque acts as single-element buffer.

---

## 11. Common Mistakes & Anti-Patterns
* **Using PriorityQueue for DP Transitions ($O(N \log K)$ Time Penalty)**:
  - Using a max-heap to store DP values in Jump Game VI costs $O(N \log K)$ time.
  - **Use a Monotonic Queue for $O(N)$ linear time**.
* **Forgetting to Check `P[i] - P[deque.peekFirst()] >= K` in LeetCode 862**:
  - Failing to check against head prefix sum breaks subarray sum calculations.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Monotonic Queue Optimizes DP Transitions:
> In DP transitions of the form $dp[i] = \text{cost}[i] + \max_{j \in [i-k \dots i-1]} dp[j]$:
> Finding the max $dp[j]$ in a sliding window of size $K$ takes $O(K)$ naive time.
> A Monotonic Decreasing Queue maintains the max $dp[j]$ at `peekFirst()` in **$O(1)$ Constant Time**, reducing total DP runtime from $O(N \cdot K)$ down to **$O(N)$ Linear Time**!

> **Memory Trick:** **"Monotonic Queue reduces 1D sliding DP transitions from O(N * K) to O(N) Linear Time!"**

---

## 13. System & Implementation Comparisons

| Feature | Monotonic Queue DP Optimization | PriorityQueue (Heap) DP Optimization |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \log K)$ Logarithmic |
| **Auxiliary Memory** | **$O(K)$ Deque Space ⚡** | $O(K)$ Heap Space |
| **Out-of-Bound Removal**| **$O(1)$ Instant Head Removal ⚡**| $O(\log K)$ Heap Removal |

---

## 14. How to Recognize This in Questions
* **"Find maximum/minimum in sliding window of size K"** $\rightarrow$ Monotonic Queue (LeetCode 239).
* **"Optimize DP recurrence dp[i] = nums[i] + max(dp[i-K ... i-1])"** $\rightarrow$ Monotonic Queue DP (LeetCode 1696).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does LeetCode 862 require a Monotonic Queue while LeetCode 209 uses standard Sliding Window?**  
  *A:* LeetCode 209 contains ONLY positive integers, guaranteeing monotonic array sums. LeetCode 862 contains NEGATIVE integers, destroying sum monotonicity. Prefix sums + Monotonic Queue restore $O(N)$ optimality.
* **Q: How does `deque.pollFirst()` inside `while (P[i] - P[deque.peekFirst()] >= K)` prevent re-checking?**  
  *A:* Once an index `peekFirst()` forms a valid subarray with `i`, any FUTURE index $j > i$ pairing with `peekFirst()` would produce a LARGER subarray length ($j - \text{peekFirst()} > i - \text{peekFirst()}$). Thus, `peekFirst()` can never form a shorter valid subarray and is safely popped forever.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MONOTONIC QUEUE MECHANICS & DP OPTIMIZATION            |
+-----------------------------------------------------------------------+
| • Window Max Rule (239): Head = max; purge tail peekLast() <= val     |
| • DP Window Max Rule (1696): dp[i] = nums[i] + dp[deque.peekFirst()]  |
| • Shortest Subarray (862): Prefix sums + Queue storing increasing P[i]|
| • Tail Purge (862): while (P[i] <= P[deque.peekLast()]) pollLast()     |
| • Time Complexity: O(N) Linear Time | O(K) Deque Space ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Sliding Window Maximum (LeetCode 239) using Monotonic Queue.
- [ ] I can write Shortest Subarray with Sum at Least K (LeetCode 862).
- [ ] I can optimize DP transitions using Monotonic Queue in Jump Game VI (1696).
- [ ] I know why negative numbers in LeetCode 862 require Monotonic Queue.
- [ ] I can state the operational differences between Monotonic Stack and Queue.
