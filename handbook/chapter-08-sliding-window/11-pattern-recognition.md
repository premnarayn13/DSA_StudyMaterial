# 11. Sliding Window Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly identifying the appropriate Sliding Window variant during a coding interview is key to solving array and string sub-segment problems in **$O(N)$ linear time and $O(1)$ constant space**. Sliding window problems fall into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal sliding window strategies, along with copy-paste production Java templates.

> **Important:** Master the primary sliding window selection rules:
> 1. **Fixed-Size Window ($K$ is Fixed)**: Use when window size is a constant $K$ (e.g. Anagrams, Max Subarray Size $K$).
> 2. **Variable-Size Shrinkable Window**: Use for Longest/Shortest valid subarray/substring search.
> 3. **Monotonic Deque Window**: Use when finding sliding window Max/Min in $O(N)$ time.
> 4. **At Most K Mathematical Reduction**: Use for "Exact $K$" counting queries (`atMost(K) - atMost(K-1)`).

---

## 2. Master Sliding Window Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER SLIDING WINDOW PROBLEM DECISION MATRIX                                                     |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Find max/min sum of contiguous subarray size K"  | Fixed-Size Window     | `sum += in - out`     |
| "Find all anagrams / permutations of pattern P"   | Fixed Frequency Sweep | `matches == 26`       |
| "Find longest substring with at most K distinct"  | Variable Longest      | `distinctCount > k`   |
| "Find minimal length subarray with sum >= target" | Variable Shortest     | Record inside `while` |
| "Find max element in every window of size K"      | Monotonic Deque       | `deque.peekFirst()`   |
| "Find number of subarrays with EXACTLY K items"   | At Most K Reduction   | `atMost(K) - atMost(K-1)`|
| "Find longest subarray where max - min <= limit"  | Dual Monotonic Deques | `maxDeque - minDeque` |
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Fixed-Size Window Anagram Sweep Template
* **Signal**: Finding all anagrams or permutations of pattern $P$ in string $S$ (438, 567).

```java
public static List<Integer> findAnagramsTemplate(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s == null || p == null || s.length() < p.length()) return result;

    int k = p.length();
    int[] pMap = new int[26], sMap = new int[26];
    for (int i = 0; i < k; i++) {
        pMap[p.charAt(i) - 'a']++;
        sMap[s.charAt(i) - 'a']++;
    }

    int matches = 0;
    for (int i = 0; i < 26; i++) if (pMap[i] == sMap[i]) matches++;
    if (matches == 26) result.add(0);

    for (int right = k; right < s.length(); right++) {
        int in = s.charAt(right) - 'a', out = s.charAt(right - k) - 'a';

        if (sMap[in] == pMap[in]) matches--; sMap[in]++; if (sMap[in] == pMap[in]) matches++;
        if (sMap[out] == pMap[out]) matches--; sMap[out]--; if (sMap[out] == pMap[out]) matches++;

        if (matches == 26) result.add(right - k + 1);
    }

    return result;
}
```

---

## 4. Pattern 2: Variable-Size Longest Window Template
* **Signal**: Finding longest subarray/substring satisfying condition (3, 340, 1004).

```java
public static int longestWindowTemplate(String s, int k) {
    int[] count = new int[128];
    int left = 0, distinctCount = 0, maxLen = 0;

    for (int right = 0; right < s.length(); right++) {
        if (count[s.charAt(right)]++ == 0) distinctCount++;

        while (distinctCount > k) {
            if (--count[s.charAt(left++)] == 0) distinctCount--;
        }

        maxLen = Math.max(maxLen, right - left + 1); // Record AFTER shrink loop!
    }

    return maxLen;
}
```

---

## 5. Pattern 3: Variable-Size Shortest Window Template
* **Signal**: Finding shortest subarray/substring satisfying target sum/frequency (209, 76).

```java
public static int shortestWindowTemplate(int target, int[] nums) {
    int left = 0, minLen = Integer.MAX_VALUE;
    long currentSum = 0;

    for (int right = 0; right < nums.length; right++) {
        currentSum += nums[right];

        while (currentSum >= target) {
            minLen = Math.min(minLen, right - left + 1); // Record INSIDE shrink loop!
            currentSum -= nums[left++];
        }
    }

    return minLen == Integer.MAX_VALUE ? 0 : minLen;
}
```

---

## 6. Pattern 4: Monotonic Deque Sliding Window Max Template
* **Signal**: Finding maximum/minimum in every sliding window of size $K$ (239).

```java
public static int[] maxSlidingWindowTemplate(int[] nums, int k) {
    int n = nums.length, p = 0;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>();

    for (int right = 0; right < n; right++) {
        if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) deque.pollFirst();
        while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) deque.pollLast();
        deque.offerLast(right);

        if (right >= k - 1) result[p++] = nums[deque.peekFirst()];
    }

    return result;
}
```

---

## 7. Pattern 5: Exact K Subarray Count Reduction Template
* **Signal**: Finding number of subarrays with EXACTLY $K$ odd/distinct items (1248, 992).

```java
public static int exactKSubarraysTemplate(int[] nums, int k) {
    return atMostK(nums, k) - atMostK(nums, k - 1);
}

private static int atMostK(int[] nums, int k) {
    if (k < 0) return 0;
    int left = 0, count = 0, distinctCount = 0;
    int[] freq = new int[nums.length + 1];

    for (int right = 0; right < nums.length; right++) {
        if (freq[nums[right]]++ == 0) distinctCount++;
        while (distinctCount > k) {
            if (--freq[nums[left++]] == 0) distinctCount--;
        }
        count += (right - left + 1); // Subarray count formula!
    }

    return count;
}
```

---

## 8. Pattern 6: Dual Monotonic Deque Limit Template
* **Signal**: Finding longest subarray where absolute difference between max and min $\le$ limit (1438).

```java
public static int dualDequeLimitTemplate(int[] nums, int limit) {
    Deque<Integer> maxDeque = new ArrayDeque<>(), minDeque = new ArrayDeque<>();
    int left = 0, maxLen = 0;

    for (int right = 0; right < nums.length; right++) {
        int val = nums[right];
        while (!maxDeque.isEmpty() && maxDeque.peekLast() < val) maxDeque.pollLast();
        maxDeque.offerLast(val);
        while (!minDeque.isEmpty() && minDeque.peekLast() > val) minDeque.pollLast();
        minDeque.offerLast(val);

        while (maxDeque.peekFirst() - minDeque.peekFirst() > limit) {
            if (maxDeque.peekFirst() == nums[left]) maxDeque.pollFirst();
            if (minDeque.peekFirst() == nums[left]) minDeque.pollFirst();
            left++;
        }

        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

---

## 9. Edge Case & Trap Checklist
* **Product $< K$ when $K \le 1$**: Return 0 immediately to prevent infinite loops.
* **Storing Values vs Indices in Deque**: Always store indices to verify window boundaries.
* **Longest vs Shortest Record Location**: Longest updates AFTER shrink loop; Shortest updates INSIDE shrink loop.
* **Exact K Queries**: Always use `atMost(K) - atMost(K - 1)`.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: SLIDING WINDOW PATTERN RECOGNITION                   |
+-----------------------------------------------------------------------+
| 1. Fixed Window (438): K = p.len; track matches counter (0..26)      |
| 2. Longest Window (340): Record maxLen AFTER while (distinct > K) loop|
| 3. Shortest Window (209): Record minLen INSIDE while (sum >= target)  |
| 4. Subarray Product < K (713): count += (right - left + 1) in O(1)    |
| 5. Sliding Max (239): Monotonic Deque storing INDICES; max at head    |
| 6. Exact K Subarrays (1248): Count(Exact K) = atMost(K) - atMost(K-1) |
| 7. Dual Deques (1438): maxDeque - minDeque <= limit for max/min diff  |
| 8. 2D Submatrix Sum (1074): Fix r1 & r2; 1D prefix sum map over cols |
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know where to record the answer for Longest vs Shortest window problems.
- [ ] I know why `atMost(K) - atMost(K - 1)` solves exact count queries.
- [ ] I can write Monotonic Deque Sliding Window Max (LeetCode 239).
