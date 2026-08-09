# 08. Array Sliding Window Problems, Monotonic Deque & Exact Subarray Count Transformations

## 1. Introduction
Array sliding window problems feature advanced data structure pairings—such as **Monotonic Deques** and **Prefix Sum Hash Maps**—to evaluate complex subarray constraints over numerical sequences. Problems like **Sliding Window Maximum (LeetCode 239)**, **Count Number of Nice Subarrays (LeetCode 1248)**, and **Subarray Sum Equals K (LeetCode 560)** are solved in **$O(N)$ linear time**.

> **Important:** How to solve **"Exact K Subarrays"** (e.g. Exactly K odd numbers or Exactly K distinct elements) using Sliding Window:
> Standard sliding window cannot easily count "Exactly K" directly. Instead, transform the query using the **At Most K Mathematical Reduction**:
> $$\text{Count(Exactly } K) = \text{Count(At Most } K) - \text{Count(At Most } K - 1)$$
> Finding "At Most K" is trivial using standard variable sliding window! ⚡

```
Exact K Mathematical Reduction Spectrum:
+-----------------------------------------------------------------------------------+
| Query: Exactly K Subarrays -> Standard sliding window breaks on exact match ❌     |
| Transformation Formula     : AtMost(K) - AtMost(K - 1)                           |
| Execution Mechanics        : Run standard O(N) sliding window TWICE!              |
| Complexity                 : 2 * O(N) = O(N) Linear Time! ⚡                        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Monotonic Deque Window Maximum (LeetCode 239)

### 2.1 Sliding Window Maximum (LeetCode 239)
Given an integer array `nums` and a sliding window of size $K$ moving from left to right, return the max element in each window:

#### Monotonic Deque Mechanics ($O(N)$ Time, $O(K)$ Auxiliary Space):
1. Maintain a double-ended queue `ArrayDeque<Integer> deque` storing **ARRAY INDICES** (not values!).
2. Maintain monotonic property: Elements in `deque` have strictly **DECREASING VALUES** from head to tail.
3. For `right = 0` to $N - 1$:
   - **Remove Out-of-Bound Indices**: If `!deque.isEmpty() && deque.peekFirst() < right - k + 1`, remove head: `deque.pollFirst()`.
   - **Maintain Monotonic Decreasing Order**: While `!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]`, remove tail: `deque.pollLast()`.
   - **Push Current Index**: `deque.offerLast(right)`.
   - **Record Answer**: Once `right >= k - 1`, the maximum element of the current window is AT THE HEAD of the deque: `result[p++] = nums[deque.peekFirst()]`!

```
Why Monotonic Deque Eliminates Smaller Outdated Elements:
If an incoming element nums[right] is GREATER than an older element nums[i] (where i < right),
nums[i] can NEVER be the maximum for the current window OR ANY FUTURE WINDOW!
We can safely purge nums[i] from the tail of the deque in O(1) amortized time! ⚡
```

> **Memory Trick:** **"Sliding Window Max: Store indices in Deque! Purge smaller tail elements (peekLast <= val)! Max is ALWAYS at peekFirst!"**

---

## 3. Characteristics & The "At Most K" Mathematical Reduction (LeetCode 1248)

### 3.1 Count Number of Nice Subarrays (LeetCode 1248)
An array `nums` is called "nice" if it contains exactly $K$ odd numbers. Return the number of nice subarrays:
1. Define helper `atMostK(nums, K)`: Count subarrays containing **at most $K$ odd numbers**.
2. **Formula**: `return atMostK(nums, k) - atMostK(nums, k - 1)`.

```java
private static int atMostK(int[] nums, int k) {
    if (k < 0) return 0;
    int left = 0, count = 0, oddCount = 0;

    for (int right = 0; right < nums.length; right++) {
        if (nums[right] % 2 != 0) oddCount++;

        while (oddCount > k) {
            if (nums[left] % 2 != 0) oddCount--;
            left++;
        }

        count += (right - left + 1); // Subarray count formula!
    }

    return count;
}
```

---

## 4. Internal Working Mechanics
Tracing Sliding Window Maximum (LeetCode 239) on `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, $K = 3$:

```
right = 0 (val 1) : deque = [0 (val 1)]
right = 1 (val 3) : val 3 > nums[peekLast(0)] (1) -> pollLast(0). Push 1. deque = [1 (val 3)]
right = 2 (val -1): val -1 < 3 -> Push 2. deque = [1 (val 3), 2 (val -1)].
  - Window 0 [0..2]: max = nums[peekFirst(1)] = 3. result = [3].

right = 3 (val -3): Push 3. deque = [1(3), 2(-1), 3(-3)].
  - Window 1 [1..3]: max = nums[peekFirst(1)] = 3. result = [3, 3].

right = 4 (val 5) : Purge 3(-3), 2(-1), 1(3) because 5 is larger! Push 4. deque = [4 (val 5)].
  - Window 2 [2..4]: max = nums[peekFirst(4)] = 5. result = [3, 3, 5].

right = 5 (val 3) : Push 5. deque = [4(5), 5(3)].
  - Window 3 [3..5]: max = nums[peekFirst(4)] = 5. result = [3, 3, 5, 5].

right = 6 (val 6) : Purge 5(3), 4(5). Push 6. deque = [6 (val 6)].
  - Window 4 [4..6]: max = nums[peekFirst(6)] = 6. result = [3, 3, 5, 5, 6].

right = 7 (val 7) : Purge 6(6). Push 7. deque = [7 (val 7)].
  - Window 5 [5..7]: max = nums[peekFirst(7)] = 7. result = [3, 3, 5, 5, 6, 7].

Final Sliding Window Max Array: [3, 3, 5, 5, 6, 7] ✅ (O(N) Time, O(K) Space!)
```

---

## 5. Visual Diagram
Monotonic Decreasing Deque Insertion & Purging Topography:

```
Incoming val 5 at right=4:
Deque Head -> [ Index 1 (Val 3), Index 2 (Val -1), Index 3 (Val -3) ] <- Deque Tail
                |                 |                 |
                v                 v                 v
             PURGE (3 < 5)     PURGE (-1 < 5)    PURGE (-3 < 5)

New Deque Head -> [ Index 4 (Val 5) ] <- Deque Tail  (New Maximum at Head!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Sliding Window Maximum (LeetCode 239) and Count Number of Nice Subarrays (LeetCode 1248):

```java
import java.util.*;

public class ArrayProblemsMaster {

    // 1. Sliding Window Maximum (LeetCode 239) O(N) Time, O(K) Space
    public static int[] maxSlidingWindow(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0) return new int[0];

        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        int p = 0;

        for (int right = 0; right < n; right++) {
            // Remove out-of-bound indices from head
            if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) {
                deque.pollFirst();
            }

            // Remove smaller elements from tail to maintain monotonic decreasing order
            while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) {
                deque.pollLast();
            }

            // Push current index
            deque.offerLast(right);

            // Record maximum element at head once initial window of size K is reached
            if (right >= k - 1) {
                result[p++] = nums[deque.peekFirst()];
            }
        }

        return result;
    }

    // 2. Count Number of Nice Subarrays (LeetCode 1248) O(N) Time, O(1) Space
    public static int numberOfSubarrays(int[] nums, int k) {
        return atMostK(nums, k) - atMostK(nums, k - 1);
    }

    private static int atMostK(int[] nums, int k) {
        if (k < 0) return 0;

        int left = 0;
        int count = 0;
        int oddCount = 0;

        for (int right = 0; right < nums.length; right++) {
            if (nums[right] % 2 != 0) {
                oddCount++;
            }

            while (oddCount > k) {
                if (nums[left] % 2 != 0) {
                    oddCount--;
                }
                left++;
            }

            count += (right - left + 1);
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// Monotonic Deque Purge & Store Syntax
while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) {
    deque.pollLast();
}
deque.offerLast(right);
```

---

## 7. Concrete Problem Examples
* **LeetCode 239 - Sliding Window Maximum**: Monotonic Deque $O(N)$ maximum.
* **LeetCode 1248 - Count Number of Nice Subarrays**: Exact $K$ reduction (`atMost(K) - atMost(K-1)`).
* **LeetCode 992 - Subarrays with K Different Integers**: Exact $K$ distinct elements transformation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Sliding Window Maximum and Count Nice Subarrays:

```java
public class ArrayProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Sliding Window Maximum (LeetCode 239, K=3) ===");
        int[] nums1 = {1, 3, -1, -3, 5, 3, 6, 7};
        int[] maxes = ArrayProblemsMaster.maxSlidingWindow(nums1, 3);
        System.out.println("Window Maximums: " + Arrays.toString(maxes));
        // Output: [3, 3, 5, 5, 6, 7]

        System.out.println("\n=== 2. Count Nice Subarrays (LeetCode 1248, K=3) ===");
        int[] nums2 = {1, 1, 2, 1, 1};
        int niceCount = ArrayProblemsMaster.numberOfSubarrays(nums2, 3);
        System.out.println("Nice Subarrays Count: " + niceCount); // Output: 2
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Window Max (239)** | **$O(N)$ Linear ⚡** | $O(K)$ Deque Space | Each index pushed/popped at most once |
| **Nice Subarrays (1248)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| 2 passes of `atMostK` ($2N = O(N)$) |

---

## 10. Edge Cases & Boundary Handling
* **$K = 1$ in Sliding Window Maximum**: Handled cleanly; deque returns array elements directly.
* **No Odd Numbers in LeetCode 1248**: Returns `0` cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Storing Values Instead of Indices in Monotonic Deque**:
  - Storing values prevents checking if the head element has fallen out of the sliding window boundary (`deque.peekFirst() < right - k + 1`).
  - **Always store ARRAY INDICES in the deque**.
* **Attempting Direct Sliding Window for "Exactly K" Subarray Counts**:
  - Direct sliding window breaks because shrinking `left` might reduce odd counts below $K$ while valid prefix combinations exist.
  - **Use `atMost(K) - atMost(K - 1)` for exact count queries**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Monotonic Deque Runs in $O(N)$ Amortized Linear Time:
> Even though there is a `while` loop purging elements from the tail of the deque (`pollLast()`), **EVERY ARRAY INDEX IS PUSHED EXACTLY ONCE AND POPPED AT MOST ONCE** across the entire iteration!
> Total deque operations $\le 2N \implies \mathbf{O(N)\text{ Amortized Linear Time}}$!

> **Memory Trick:** **"Store INDICES in Deque! Every index is pushed once and popped at most once -> O(N) Time!"**

---

## 13. System & Implementation Comparisons

| Feature | Monotonic Deque Window Max | PriorityQueue (Max-Heap) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \log K)$ |
| **Auxiliary Memory** | **$O(K)$ Deque Space ⚡** | $O(K)$ Heap Space |
| **Out-of-Bounds Removal**| $O(1)$ Amortized | $O(\log K)$ Heap Removal |

---

## 14. How to Recognize This in Questions
* **"Find max/min element in every sliding window of size K"** $\rightarrow$ LeetCode 239 (Monotonic Deque storing indices).
* **"Find number of subarrays with EXACTLY K odd/distinct items"** $\rightarrow$ LeetCode 1248 / 992 (`atMost(K) - atMost(K-1)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Monotonic Deque store array indices instead of element values?**  
  *A:* Indices allow checking whether the maximum element at the head of the deque is still inside the current sliding window boundary (`deque.peekFirst() >= right - k + 1`). Values do not provide positional boundary information.
* **Q: How does `atMost(K) - atMost(K - 1)` compute the exact count of subarrays with $K$ items?**  
  *A:* The set of subarrays with at most $K$ items consists of those with $0, 1, 2 \dots K$ items. Subtracting subarrays with at most $K - 1$ items leaves ONLY those with EXACTLY $K$ items.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ARRAY SLIDING WINDOW & MONOTONIC DEQUE                |
+-----------------------------------------------------------------------+
| • Sliding Window Max (239): Store INDICES in ArrayDeque               |
| • Out-of-bound Check: if (deque.peekFirst() < right - k + 1) pollFirst()|
| • Tail Purge: while (nums[deque.peekLast()] <= nums[right]) pollLast() |
| • Window Max Location: Always at nums[deque.peekFirst()]!              |
| • Exact K Reduction: Count(Exactly K) = atMost(K) - atMost(K - 1)     |
| • Time Complexity: O(N) Amortized Linear Time | O(K) Deque Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Sliding Window Maximum (LeetCode 239) using Monotonic Deque in $O(N)$ time.
- [ ] I know why Monotonic Deque MUST store indices instead of values.
- [ ] I can solve Count Number of Nice Subarrays (LeetCode 1248) using `atMost(K) - atMost(K-1)`.
- [ ] I can prove why Monotonic Deque runs in $O(N)$ amortized time.
- [ ] I know how to handle out-of-bound window removals in a Deque.
