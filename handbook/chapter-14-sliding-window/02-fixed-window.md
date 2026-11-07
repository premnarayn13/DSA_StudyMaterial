# 02. Fixed-Size Sliding Window Architecture, Frequency Matching & Anagram Sweeping

## 1. Introduction
The **Fixed-Size Sliding Window Pattern** is a specialized variant of the sliding window paradigm where the window length is constrained to an exact constant size $K$. Unlike variable-size windows that expand and contract dynamically, a fixed-size window maintains a constant width of $K$ elements throughout its iteration across an array or string. This pattern solves **Maximum Average Subarray I (LeetCode 643)**, **Find All Anagrams in a String (LeetCode 438)**, and **Permutation in String (LeetCode 567)** in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** For fixed-size window problems, both boundary pointers—`left` and `right`—move forward in lockstep (`left++`, `right++`). By maintaining a 26-element character frequency array (`int[26]`), verifying substring anagram permutations reduces to checking whether **`matches == 26`** in **$O(1)$ constant time per slide**!

```
Fixed-Size Sliding Window Motion Spectrum:
+-----------------------------------------------------------------------------------+
| Initial Window (Indices 0 ... K-1) : Compute initial state/sum for first K items |
| Slide Step (Right = K ... N-1)     : Add arr[right], Remove arr[right - K]        |
| Pointer Relinking Invariant       : Window Length is ALWAYS (right - left + 1) = K |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Fixed-Size Window Anagram Sweeping

### 2.1 Find All Anagrams in a String (LeetCode 438)
Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`:
* **Anagram Invariant**: An anagram of `p` is any permutation of `p`. Therefore, any valid anagram substring in `s` MUST have a **Fixed Length equal to `p.length()`** AND have an identical character frequency distribution!

#### Algorithm ($O(N)$ Time, $O(1)$ Space):
1. If `s.length() < p.length()`, return empty list.
2. Maintain two 26-element frequency arrays: `pMap[26]` and `sMap[26]`.
3. Compute frequency count for `p` and initial window in `s` (indices `0` to `K-1`, where `K = p.length()`):
   - `pMap[p.charAt(i) - 'a']++`
   - `sMap[s.charAt(i) - 'a']++`
4. Count initial character matches (`0` to `25`):
   - `int matches = 0; for (int i = 0; i < 26; i++) if (pMap[i] == sMap[i]) matches++;`
5. If `matches == 26`, add index `0` to `result`.
6. Slide window from `right = K` to `s.length() - 1`:
   - **Incoming Character**: `inChar = s.charAt(right) - 'a'`.
     - Update `sMap[inChar]++`.
     - Update `matches` balance.
   - **Outgoing Character**: `outChar = s.charAt(right - K) - 'a'`.
     - Update `sMap[outChar]--`.
     - Update `matches` balance.
   - If `matches == 26`, add start index `right - K + 1` to `result`!

```
Character Match Balance Logic:
When updating count for char c:
- If sMap[c] WAS equal to pMap[c] before modification -> matches-- (Lost a match!)
- Modify sMap[c] (increment or decrement).
- If sMap[c] IS NOW equal to pMap[c] after modification -> matches++ (Gained a match!)
This enables O(1) Instant Anagram Checks without scanning the 26-element array! ⚡
```

> **Memory Trick:** **"Fixed Window Anagram: Window size is ALWAYS p.length()! Track matches count (0..26) for O(1) slide checks!"**

---

## 3. Characteristics & Permutation in String Mechanics (LeetCode 567)

### 3.1 Permutation in String Verification (LeetCode 567)
Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`:
* Identical fixed-size sliding window mechanism as LeetCode 438!
* If `matches == 26` at any point during sliding, return `true` immediately.
* If loop completes without `matches == 26`, return `false`.

### 3.2 Maximum Average Subarray I (LeetCode 643)
Given an array `nums` consisting of $N$ elements and integer $K$:
* Find a contiguous subarray of fixed length $K$ that has the maximum average value:
1. Compute initial sum of first $K$ elements: `currentSum`.
2. `maxSum = currentSum`.
3. Slide window from `right = K` to $N - 1$:
   - `currentSum += nums[right] - nums[right - K]`
   - `maxSum = Math.max(maxSum, currentSum)`
4. Return `(double) maxSum / K`.

---

## 4. Internal Working Mechanics
Tracing Find All Anagrams (LeetCode 438) on `s = "cbaebabacd"`, `p = "abc"` ($K = 3$):

```
Target p = "abc" -> pMap: a:1, b:1, c:1. All other 23 chars count 0.

Initial Window (s[0..2] = "cba"): sMap: a:1, b:1, c:1.
matches = 26! -> Add index 0 to result. result = [0].

Slide 1 (right = 3, inChar = 'e', outChar = 'c'):
  - Remove 'c': sMap['c'] becomes 0. matches-- (c lost match).
  - Add 'e'   : sMap['e'] becomes 1. matches-- (e lost match).
  - matches = 24 != 26.

Slide 2 (right = 4, inChar = 'b', outChar = 'b'):
  - In & Out are same ('b'). sMap unchanged. matches = 24.

Slide 3 (right = 5, inChar = 'a', outChar = 'a'):
  - In & Out are same ('a'). sMap unchanged. matches = 24.

Slide 4 (right = 6, inChar = 'b', outChar = 'e'):
  - Remove 'e': sMap['e'] becomes 0. matches++ ('e' regained match 0==0!).
  - Add 'b'   : sMap['b'] becomes 2. matches-- ('b' lost match 2!=1).

Slide 5 (right = 7, inChar = 'a', outChar = 'b'):
  - Remove 'b': sMap['b'] becomes 1. matches++ ('b' regained match 1==1!).
  - Add 'a'   : sMap['a'] becomes 2. matches-- ('a' lost match 2!=1).

Slide 6 (right = 8, inChar = 'c', outChar = 'a'):
  - Remove 'a': sMap['a'] becomes 1. matches++ ('a' regained match 1==1!).
  - Add 'c'   : sMap['c'] becomes 1. matches++ ('c' regained match 1==1!).
  - matches = 26! -> Add index (8 - 3 + 1) = 6 to result. result = [0, 6].

Final Anagram Start Indices: [0, 6] ✅ (O(N) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Fixed-Size Sliding Window Character Frequency Sweep Topography:

```
s = " c  b  a  e  b  a  b  a  c  d "
    [=======]                             Window 0: s[0..2] = "cba" -> Matches p ("abc") -> Start Idx 0 ✅
       [=======]                          Window 1: s[1..3] = "bae" -> Mismatch
          ...
                   [=======]              Window 6: s[6..8] = "bac" -> Matches p ("abc") -> Start Idx 6 ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Maximum Average Subarray I (LeetCode 643), Find All Anagrams in a String (LeetCode 438), Permutation in String (LeetCode 567), and Sub-arrays of Size K with Avg $\ge$ Threshold (LeetCode 1343):

```java
import java.util.*;

public class FixedWindowMaster {

    // 1. Find All Anagrams in a String (LeetCode 438) O(N) Time, O(1) Space
    public static List<Integer> findAnagrams(String s, String p) {
        List<Integer> result = new ArrayList<>();
        if (s == null || p == null || s.length() < p.length()) {
            return result;
        }

        int k = p.length();
        int[] pMap = new int[26];
        int[] sMap = new int[26];

        // Populate frequency for p and initial window of s
        for (int i = 0; i < k; i++) {
            pMap[p.charAt(i) - 'a']++;
            sMap[s.charAt(i) - 'a']++;
        }

        // Count initial character matches
        int matches = 0;
        for (int i = 0; i < 26; i++) {
            if (pMap[i] == sMap[i]) matches++;
        }

        if (matches == 26) result.add(0);

        // Slide window of size K across s
        for (int right = k; right < s.length(); right++) {
            int inChar = s.charAt(right) - 'a';
            int outChar = s.charAt(right - k) - 'a';

            // Add incoming character
            if (sMap[inChar] == pMap[inChar]) matches--; // Match lost
            sMap[inChar]++;
            if (sMap[inChar] == pMap[inChar]) matches++; // Match gained

            // Remove outgoing character
            if (sMap[outChar] == pMap[outChar]) matches--; // Match lost
            sMap[outChar]--;
            if (sMap[outChar] == pMap[outChar]) matches++; // Match gained

            // If all 26 characters match frequency, record start index
            if (matches == 26) {
                result.add(right - k + 1);
            }
        }

        return result;
    }

    // 2. Permutation in String Verification (LeetCode 567) O(N) Time, O(1) Space
    public static boolean checkInclusion(String s1, String s2) {
        if (s1 == null || s2 == null || s2.length() < s1.length()) {
            return false;
        }

        int k = s1.length();
        int[] map1 = new int[26];
        int[] map2 = new int[26];

        for (int i = 0; i < k; i++) {
            map1[s1.charAt(i) - 'a']++;
            map2[s2.charAt(i) - 'a']++;
        }

        int matches = 0;
        for (int i = 0; i < 26; i++) {
            if (map1[i] == map2[i]) matches++;
        }

        if (matches == 26) return true;

        for (int right = k; right < s2.length(); right++) {
            int inChar = s2.charAt(right) - 'a';
            int outChar = s2.charAt(right - k) - 'a';

            if (map2[inChar] == map1[inChar]) matches--;
            map2[inChar]++;
            if (map2[inChar] == map1[inChar]) matches++;

            if (map2[outChar] == map1[outChar]) matches--;
            map2[outChar]--;
            if (map2[outChar] == map1[outChar]) matches++;

            if (matches == 26) return true;
        }

        return false;
    }

    // 3. Maximum Average Subarray I (LeetCode 643) O(N) Time, O(1) Space
    public static double findMaxAverage(int[] nums, int k) {
        long currentSum = 0;
        for (int i = 0; i < k; i++) {
            currentSum += nums[i];
        }

        long maxSum = currentSum;
        for (int right = k; right < nums.length; right++) {
            currentSum += nums[right] - nums[right - k];
            maxSum = Math.max(maxSum, currentSum);
        }

        return (double) maxSum / k;
    }

    // 4. Number of Sub-arrays of Size K and Avg >= Threshold (LeetCode 1343) O(N) Time
    public static int numOfSubarrays(int[] arr, int k, int threshold) {
        long targetSum = (long) k * threshold; // Threshold equation: sum >= k * threshold
        long currentSum = 0;
        int count = 0;

        for (int i = 0; i < k; i++) {
            currentSum += arr[i];
        }

        if (currentSum >= targetSum) count++;

        for (int right = k; right < arr.length; right++) {
            currentSum += arr[right] - arr[right - k];
            if (currentSum >= targetSum) count++;
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// Fixed Window Matches Counter Tracking Template
if (sMap[inChar] == pMap[inChar]) matches--;
sMap[inChar]++;
if (sMap[inChar] == pMap[inChar]) matches++;
```

---

## 7. Concrete Problem Examples
* **LeetCode 438 - Find All Anagrams in a String**: Fixed window character frequency match.
* **LeetCode 567 - Permutation in String**: Substring anagram existence.
* **LeetCode 643 - Maximum Average Subarray I**: Fixed window floating-point average max.
* **LeetCode 1343 - Number of Sub-arrays of Size K and Average >= Threshold**: Fixed window target sum count.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Find All Anagrams, Permutation in String, and Max Average Subarray:

```java
public class FixedWindowDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Find All Anagrams (LeetCode 438) ===");
        String s = "cbaebabacd", p = "abc";
        List<Integer> anagramIndices = FixedWindowMaster.findAnagrams(s, p);
        System.out.println("Anagram Start Indices: " + anagramIndices); // Output: [0, 6]

        System.out.println("\n=== 2. Permutation in String (LeetCode 567) ===");
        String s1 = "ab", s2 = "eidbaooo";
        System.out.println("Contains Permutation? " + FixedWindowMaster.checkInclusion(s1, s2)); // Output: true

        System.out.println("\n=== 3. Maximum Average Subarray I (LeetCode 643) ===");
        int[] nums = {1, 12, -5, -6, 50, 3};
        double maxAvg = FixedWindowMaster.findMaxAverage(nums, 4);
        System.out.println("Max Average (K=4): " + maxAvg); // Output: 12.75 ([12, -5, -6, 50] / 4)
    }
}
```

---

## 9. Complexity Analysis

| Operation / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Find Anagrams (438)** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `matches` variable tracking (0..26) |
| **Permutation String (567)**| **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| Early return on `matches == 26` |
| **Max Average (643)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Single-pass `sum += in - out` |

---

## 10. Edge Cases & Boundary Handling
* **Pattern String Larger Than Search String (`p.length() > s.length()`)**: Returns empty list immediately.
* **32-Bit Integer Overflow in Subarray Sum**: In LeetCode 1343, threshold equation `currentSum >= (long) k * threshold` prevents multiplication overflow.

---

## 11. Common Mistakes & Anti-Patterns
* **Scanning Full 26-Element Array at Every Slide ($O(26N)$ Time Penalty)**:
  - Executing `Arrays.equals(sMap, pMap)` inside the sliding loop iterates 26 array elements $N$ times.
  - **Use a `matches` variable tracking matching frequencies for true $O(1)$ slide verification**.
* **Floating-Point Division Inside Sliding Loop**:
  - Calculating `currentSum / (double) K` at every step introduces floating-point rounding errors and division overhead.
  - **Maintain `currentSum` as `long` and perform single division at return time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `matches` Tracking Gives Optimal $O(1)$ Verification:
> By tracking the number of characters whose frequencies in `sMap` equal `pMap` using a `matches` counter (0 to 26):
> Adding an incoming character updates `matches` in $O(1)$ time.
> Removing an outgoing character updates `matches` in $O(1)$ time.
> Checking `matches == 26` evaluates in **$O(1)$ Constant Time**!

> **Memory Trick:** **"Track matches counter! When sMap[c] == pMap[c], matches++! Check matches == 26 in O(1) time!"**

---

## 13. System & Implementation Comparisons

| Feature | `matches` Variable Verification | `Arrays.equals()` Sweep |
| :--- | :--- | :--- |
| **Verification Time** | **$O(1)$ Instant ⚡** | $O(26)$ Operations per step |
| **Total Operations** | $2N$ Operations | $26N$ Operations |
| **Code Footprint** | Concise | Requires array loops |

---

## 14. How to Recognize This in Questions
* **"Find all anagrams / permutations of pattern P in string S"** $\rightarrow$ LeetCode 438 / 567 (Fixed window size `P.length()`).
* **"Find max average / target sum contiguous subarray of size K"** $\rightarrow$ LeetCode 643 / 1343.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is an anagram search problem classified as a FIXED-SIZE sliding window?**  
  *A:* Because an anagram is a permutation of string $P$. Any valid anagram substring MUST have a length strictly equal to $P.length()$. Therefore, the sliding window width is fixed to $K = P.length()$.
* **Q: How does `matches` counter handle characters that do not appear in string $P$?**  
  *A:* Characters not in $P$ have `pMap[c] = 0`. Initially, `sMap[c] = 0`, so `matches` starts incremented for all 23 non-occurring characters. When a non-$P$ character enters `sMap`, `sMap[c]` becomes 1 ($1 \ne 0$), so `matches--`. When it leaves `sMap`, `sMap[c]` returns to 0 ($0 == 0$), so `matches++`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FIXED-SIZE SLIDING WINDOW & ANAGRAM SWEEPING          |
+-----------------------------------------------------------------------+
| • Fixed Window Formula: sum = sum + nums[right] - nums[right - K]     |
| • Anagram Window Size: K is ALWAYS equal to p.length()                |
| • Match Counter Logic: Maintain matches (0..26) for O(1) slide checks  |
| • In-Out Char Update: Check match loss before mod, match gain after   |
| • Anagram Condition: If matches == 26 -> Valid anagram at (right-K+1)  |
| • Avg Threshold Trick: Compare currentSum >= (long) K * threshold     |
| • Time Complexity: O(N) Linear Time | O(1) Auxiliary Space ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Find All Anagrams (LeetCode 438) using `matches` variable tracking.
- [ ] I can write Permutation in String (LeetCode 567) in under 4 minutes.
- [ ] I know why `matches` tracking is faster than `Arrays.equals(sMap, pMap)`.
- [ ] I can solve Maximum Average Subarray I (LeetCode 643).
- [ ] I know how non-occurring characters update `matches` correctly.
