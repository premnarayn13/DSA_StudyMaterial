# 12. Master Reference — Sliding Window

## 1. Introduction
This Master Reference consolidates all mathematical formulas, window invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 8: Sliding Window**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Fixed Window `sum += in - out`, Anagram `matches == 26` verification, Subarray Product $O(1)$ addition `count += right - left + 1`, Character Replacement formula `(len - maxFreq) <= K`, Minimum Window Substring `formed == required` match tracking, Monotonic Deque index storage, Exact $K$ reduction `atMost(K) - atMost(K-1)`, and Dual Monotonic Deque limit checks!

---

## 2. Master Mathematical & Window Formula Cheat Sheet
* **Subarray Count Addition Formula**: When window `[left ... right]` is valid, the number of contiguous valid subarrays ending at index `right` is:

$$\text{Subarrays Added} = \text{right} - \text{left} + 1$$

* **Exact $K$ Mathematical Reduction**:

$$\text{Count(Exactly } K) = \text{Count(At Most } K) - \text{Count(At Most } K - 1)$$

* **Longest Character Replacement Invariant (LeetCode 424)**:
  - $\text{Replacements Needed} = (\text{right} - \text{left} + 1) - \text{maxFreq} \le K$.
* **Dual Monotonic Deque Limit Check (LeetCode 1438)**:
  - $\text{maxDeque.peekFirst()} - \text{minDeque.peekFirst()} \le \text{Limit}$.
* **Complementary Middle Subarray Reduction (LeetCode 1658)**:
  - $\text{Min Operations on Ends} = N - \text{Max Length Middle Subarray Summing to (TotalSum - X)}$.
* **2D Matrix Submatrix Compression (LeetCode 1074)**:
  - Compress rows between $r1$ and $r2$ into 1D array `colSum[c]`; reduces 2D submatrix sum to 1D prefix map in $O(R^2 \cdot C)$ time!

```
Sliding Window Invariants & Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Sliding Window Variant            | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Fixed Window Slide                | sum = sum + arr[right] - arr[right - K]           |
| Anagram Matches Tracker           | matches == 26 for O(1) slide verification         |
| Subarray Product Count            | count += (right - left + 1)                       |
| Character Replacement             | (right - left + 1) - maxFreq <= K                 |
| Monotonic Deque Max               | Store INDICES! Purge tail while peekLast <= val   |
| Exact K Subarrays                 | atMost(K) - atMost(K - 1)                         |
| Dual Deque Limit                  | maxDeque.peekFirst() - minDeque.peekFirst() <= L  |
| 2D Submatrix Target Sum           | Col compression + 1D prefix sum map (map.put(0,1))|
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Max Sum Subarray (Fixed K)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Fixed window `sum += in - out` |
| **Find All Anagrams (438)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `matches == 26` variable tracking |
| **Permutation in String (567)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| Early return on `matches == 26` |
| **Longest Substring No Rep (3)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| Index jump `left = map[c] + 1` |
| **Product Less Than K (713)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `count += (right - left + 1)` addition |
| **Min Subarray Sum (209)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Record `minLen` inside shrink loop |
| **Char Replacement (424)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `(len - maxFreq) <= K` bound |
| **Minimum Window Substring (76)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Aux Array ⚡**| `formed == required` match counter |
| **At Most K Distinct (340)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `distinctCount > K` shrink loop |
| **Fruit Into Baskets (904)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Map (Size $\le 3$) ⚡**| Isomorphic to $K=2$ distinct items |
| **Reduce X to Zero (1658)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Invert to max middle subarray sum |
| **Concatenation Words (30)**| **$O(N \cdot L)$ Linear⚡**| **$O(N \cdot L)$ Linear⚡**| **$O(N \cdot L)$ Linear⚡**| $O(M)$ Hash Map | $L$ offset passes with step $L$ |
| **Sliding Window Max (239)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(K)$ Deque Space | Monotonic Deque storing indices |
| **Nice Subarrays (1248)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `atMost(K) - atMost(K - 1)` |
| **2D Submatrix Target Sum (1074)**| **$O(R^2 \cdot C)$ ⚡** | **$O(R^2 \cdot C)$ ⚡** | **$O(R^2 \cdot C)$ ⚡** | $O(C)$ Aux Map | 2D to 1D column compression |
| **Abs Diff Limit (1438)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Deque Space | Dual Monotonic Deques (max & min) |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Sliding Window Operations                                   |
+-----------------------------------------------------------------------------------+
| Primitive Frequency Array (int[128]) : 512 Bytes (Fast, Zero GC Overhead) ⚡      |
| Monotonic ArrayDeque (Indices)       : 24 Bytes Object Header + 4N Bytes Integers  |
| HashMap Window Storage               : 32 Bytes per Entry (Higher Memory Overhead)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Fixed Window Sliding Formula
currentSum += nums[right] - nums[right - k];

// 2. Variable Longest Window Structure
for (int right = 0; right < n; right++) {
    updateState(nums[right]);
    while (isInvalidState()) {
        removeState(nums[left++]);
    }
    maxLen = Math.max(maxLen, right - left + 1); // Record AFTER shrink loop
}

// 3. Variable Shortest Window Structure
for (int right = 0; right < n; right++) {
    currentSum += nums[right];
    while (currentSum >= target) {
        minLen = Math.min(minLen, right - left + 1); // Record INSIDE shrink loop
        currentSum -= nums[left++];
    }
}

// 4. Monotonic Deque Purge & Store
while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) deque.pollLast();
deque.offerLast(right);

// 5. Exact K Reduction Rule
int exactK = atMostK(nums, k) - atMostK(nums, k - 1);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Product $< K$ when $K \le 1$ in LeetCode 713**: Causes an infinite loop when `nums[left] == 1`. Return 0 immediately if $K \le 1$.
* **Pitfall 2: Storing Values Instead of Indices in Monotonic Deque**: Storing values prevents checking if the maximum element has fallen out of the sliding window (`deque.peekFirst() < right - k + 1`).
* **Pitfall 3: Recomputing `maxFreq` When Shrinking `left` in LeetCode 424**: Recomputing `maxFreq` takes $O(26)$ operations. Leaving `maxFreq` as historical max is mathematically sound and runs in $O(1)$ time.
* **Pitfall 4: Scanning 26-Element Array for Anagram Matches**: Executing `Arrays.equals(sMap, pMap)` takes $O(26N)$ time. Maintain a `matches` variable tracking matching frequencies for true $O(1)$ slide verification.
* **Pitfall 5: Recording Answer Outside Shrink Loop in Shortest Window Search**: Saves an un-shrunk larger window length. Record `minLen` INSIDE the `while (currentSum >= target)` shrink loop before `left++`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 8 (SLIDING WINDOW)              |
+-----------------------------------------------------------------------+
| 1. Fixed Window: sum += nums[right] - nums[right - K]                 |
| 2. Anagram Sweep (438): Track matches counter (0..26) for O(1) checks |
| 3. Subarray Product < K (713): count += (right - left + 1) in O(1)    |
| 4. Product K Guard: Return 0 immediately if K <= 1                    |
| 5. Shortest Window (209): Record minLen INSIDE while shrink loop      |
| 6. Longest Window (340): Record maxLen AFTER while shrink loop        |
| 7. Char Replacement (424): Window valid if (len - maxFreq) <= K       |
| 8. Min Window Substring (76): Track formed == required match counter  |
| 9. Sliding Window Max (239): Store INDICES in Monotonic Deque         |
| 10. Exact K Reduction (1248, 992): Count = atMost(K) - atMost(K - 1)  |
| 11. Dual Deques (1438): maxDeque - minDeque <= limit for max/min diff |
| 12. 2D Submatrix Sum (1074): Fix r1 & r2; 1D prefix sum map over cols |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Fixed Window Max Sum in under 2 minutes.
- [ ] I can write Find All Anagrams (LeetCode 438) using `matches` variable tracking.
- [ ] I can write Subarray Product Less Than K (LeetCode 713) with `right - left + 1`.
- [ ] I know why $K \le 1$ MUST return 0 immediately in LeetCode 713.
- [ ] I can write Minimum Size Subarray Sum (LeetCode 209) recording `minLen` inside shrink loop.
- [ ] I can write Character Replacement (LeetCode 424) in $O(N)$ time.
- [ ] I know why `maxFreq` does not need to be recomputed when shrinking `left`.
- [ ] I can write Minimum Window Substring (LeetCode 76) using `formed` and `required`.
- [ ] I can write Sliding Window Maximum (LeetCode 239) using Monotonic Deque.
- [ ] I can solve Count Nice Subarrays (LeetCode 1248) using `atMost(K) - atMost(K-1)`.
- [ ] I can solve Longest Subarray With Absolute Diff $\le$ Limit (LeetCode 1438) using Dual Deques.
- [ ] I can solve Submatrices Sum to Target (LeetCode 1074) using 2D column compression.
