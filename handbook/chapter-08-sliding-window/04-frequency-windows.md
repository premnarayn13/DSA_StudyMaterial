# 04. Frequency Windows, Character Replacement & Minimum Substring Search

## 1. Introduction
**Frequency Sliding Windows** represent the most powerful class of variable-size window algorithms. By pairing two boundary pointers (`left` and `right`) with a character frequency map (`int[128]` or `int[26]`), these algorithms solve complex substring constraint problems—such as **Longest Repeating Character Replacement (LeetCode 424)** and **Minimum Window Substring (LeetCode 76)**—in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** In **Longest Repeating Character Replacement (LeetCode 424)**, the number of characters inside the window `[left ... right]` that MUST be replaced to make all characters identical is:
> $$\text{Replacements Needed} = (\text{right} - \text{left} + 1) - \text{maxFreq}$$
> As long as $(\text{right} - \text{left} + 1) - \text{maxFreq} \le K$, the window is VALID! If replacements exceed $K$, shrink by advancing `left++`!

```
Frequency Window Replacement Formula Topology:
+-----------------------------------------------------------------------------------+
| Window Length      : (right - left + 1)                                            |
| Max Freq Char      : maxFreq (Frequency of most frequent character in window)       |
| Replacement Quota  : (right - left + 1) - maxFreq <= K  -> Valid Window ⚡         |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Character Replacement Mechanics (LeetCode 424)

### 2.1 Longest Repeating Character Replacement (LeetCode 424)
Given a string `s` consisting of uppercase English letters and integer $K$, choose any character of the string and change it to any other uppercase letter up to $K$ times. Return the length of the longest substring containing the same letter:

#### Algorithm ($O(N)$ Time, $O(1)$ Space):
1. `left = 0`, `maxFreq = 0`, `maxLen = 0`.
2. Maintain frequency map `int[] count = new int[26]`.
3. For `right = 0` to $N - 1$:
   - `c = s.charAt(right) - 'A'`.
   - `count[c]++`.
   - `maxFreq = Math.max(maxFreq, count[c])`.
   - **Validity Check**: If $(\text{right} - \text{left} + 1) - \text{maxFreq} > K$:
     - Shrink window: `count[s.charAt(left) - 'A']--`.
     - `left++`.
   - Update `maxLen = Math.max(maxLen, right - left + 1)`.
4. Return `maxLen`.

```
Why maxFreq Does NOT Need to Be Decremented When Left Pointer Shrinks:
Even though shrinking left might decrease the count of the character that formed maxFreq,
we are ONLY searching for a window length strictly GREATER than maxLen!
A new larger valid window can ONLY be formed if maxFreq increases beyond its historical max!
Therefore, lazily leaving maxFreq as the historical maximum does not affect correctness! ⚡
```

> **Memory Trick:** **"Character Replacement: Window valid iff (right - left + 1) - maxFreq <= K! Shrink left++ if replacements exceed K!"**

---

## 3. Characteristics & Minimum Window Substring (LeetCode 76)

### 3.1 Minimum Window Substring (LeetCode 76 - Shortest Window Search)
Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window:

1. Maintain `tCount[128]` for characters in `t` and `windowCount[128]`.
2. `required = number of unique characters in t`.
3. `formed = 0` (number of unique characters meeting target frequency in current window).
4. `left = 0`, `minLen = Integer.MAX_VALUE`, `startIdx = 0`.
5. For `right = 0` to $N - 1$:
   - `c = s.charAt(right)`.
   - `windowCount[c]++`.
   - If `tCount[c] > 0 && windowCount[c] == tCount[c]`, `formed++`.
   - **Shrink Window While Valid (`formed == required`)**:
     - Record answer: `if (right - left + 1 < minLen) { minLen = right - left + 1; startIdx = left; }`.
     - `outChar = s.charAt(left)`.
     - `windowCount[outChar]--`.
     - If `tCount[outChar] > 0 && windowCount[outChar] < tCount[outChar]`, `formed--`.
     - `left++`.
6. Return `minLen == Integer.MAX_VALUE ? "" : s.substring(startIdx, startIdx + minLen)`.

---

## 4. Internal Working Mechanics
Tracing Character Replacement (LeetCode 424) on `s = "AABABBA"`, $K = 1$:

```
Init: left = 0, maxFreq = 0, maxLen = 0, count[26] = 0

right = 0 ('A'): count['A']=1, maxFreq=1. len=1. len-maxFreq=0 <= 1 -> maxLen=1.
right = 1 ('A'): count['A']=2, maxFreq=2. len=2. len-maxFreq=0 <= 1 -> maxLen=2.
right = 2 ('B'): count['B']=1, maxFreq=2. len=3. len-maxFreq=1 <= 1 -> maxLen=3.
right = 3 ('A'): count['A']=3, maxFreq=3. len=4. len-maxFreq=1 <= 1 -> maxLen=4.
right = 4 ('B'): count['B']=2, maxFreq=3. len=5. len-maxFreq=2 > 1 -> INVALID!
  - Shrink: count[s[left]('A')]-- -> count['A']=2. left=1.
  - Window len = 4. len-maxFreq = 4-3 = 1 <= 1 -> maxLen=4.

right = 5 ('B'): count['B']=3, maxFreq=3. len=5. len-maxFreq=2 > 1 -> INVALID!
  - Shrink: count[s[left]('A')]-- -> count['A']=1. left=2.
  - Window len = 4. maxLen=4.

right = 6 ('A'): count['A']=2, maxFreq=3. len=5. len-maxFreq=2 > 1 -> INVALID!
  - Shrink: count[s[left]('B')]-- -> count['B']=2. left=3.

Max Length = 4 ("AABA" or "ABBA") ✅ (O(N) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Minimum Window Substring Match Counter Tracking Topography:

```
String S:   A  D  O  B  E  C  O  D  E  B  A  N  C  (Target T = "ABC")
           [=========================]             Formed = 3 (Valid Window "ADOBECODEBA")
                  [==================]             Shrink left to find shortest valid!
                              [==============]     Shortest Valid Substring: "BANC" (Len 4) ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Character Replacement (LeetCode 424) and Minimum Window Substring (LeetCode 76):

```java
import java.util.*;

public class FrequencyWindowsMaster {

    // 1. Longest Repeating Character Replacement (LeetCode 424) O(N) Time, O(1) Space
    public static int characterReplacement(String s, int k) {
        if (s == null || s.length() == 0) return 0;

        int[] count = new int[26];
        int left = 0;
        int maxFreq = 0;
        int maxLen = 0;

        for (int right = 0; right < s.length(); right++) {
            int inChar = s.charAt(right) - 'A';
            count[inChar]++;
            maxFreq = Math.max(maxFreq, count[inChar]);

            // Window is invalid if (windowLen - maxFreq) > k
            while ((right - left + 1) - maxFreq > k) {
                int outChar = s.charAt(left) - 'A';
                count[outChar]--;
                left++;
                // Note: maxFreq does NOT need to be decremented!
            }

            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }

    // 2. Minimum Window Substring (LeetCode 76) O(N) Time, O(1) Auxiliary Space
    public static String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) return "";

        int[] tCount = new int[128];
        int[] windowCount = new int[128];

        int required = 0;
        for (char c : t.toCharArray()) {
            if (tCount[c] == 0) required++;
            tCount[c]++;
        }

        int formed = 0;
        int left = 0;
        int minLen = Integer.MAX_VALUE;
        int startIdx = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            windowCount[c]++;

            if (tCount[c] > 0 && windowCount[c] == tCount[c]) {
                formed++;
            }

            // Shrink window while valid (formed == required)
            while (formed == required && left <= right) {
                // Record answer for shortest window
                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    startIdx = left;
                }

                char outChar = s.charAt(left);
                windowCount[outChar]--;

                if (tCount[outChar] > 0 && windowCount[outChar] < tCount[outChar]) {
                    formed--;
                }
                left++;
            }
        }

        return minLen == Integer.MAX_VALUE ? "" : s.substring(startIdx, startIdx + minLen);
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 424 Replacement Formula Check
if ((right - left + 1) - maxFreq > k) {
    count[s.charAt(left) - 'A']--;
    left++;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 424 - Longest Repeating Character Replacement**: Frequency replacement bound.
* **LeetCode 76 - Minimum Window Substring**: Shortest frequency match window.
* **LeetCode 1004 - Max Consecutive Ones III**: Zero count frequency window.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Character Replacement and Minimum Window Substring:

```java
public class FrequencyWindowsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Character Replacement (LeetCode 424, K=1) ===");
        String s1 = "AABABBA";
        int maxSub1 = FrequencyWindowsMaster.characterReplacement(s1, 1);
        System.out.println("Max Replacement Substring Length: " + maxSub1); // Output: 4 ("AABA")

        System.out.println("\n=== 2. Minimum Window Substring (LeetCode 76) ===");
        String s2 = "ADOBECODEBANC", t2 = "ABC";
        String minWin = FrequencyWindowsMaster.minWindow(s2, t2);
        System.out.println("Minimum Window Substring: \"" + minWin + "\""); // Output: "BANC"
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Character Replacement (424)**| **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `(right - left + 1) - maxFreq <= k` |
| **Minimum Window (76)** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `formed == required` match counter |

---

## 10. Edge Cases & Boundary Handling
* **String `s` Shorter Than Target `t`**: Returns `""` immediately.
* **Target `t` Containing Duplicate Characters (`t = "AAB"`)**: `tCount['A'] = 2`; `formed` increments ONLY when `windowCount['A'] == 2`.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting to Re-calculate `maxFreq` by Scanning Array on Every Left Shrink**:
  - Scanning the 26-element array inside the shrink loop takes $O(26)$ operations, degrading performance.
  - **Leaving `maxFreq` as historical maximum is mathematically correct and runs in $O(1)$ time**.
* **Comparing Character Frequencies by Iterating Entire Map ($O(128N)$ Time)**:
  - Iterating `windowCount` vs `tCount` for all 128 ASCII chars inside the loop takes $128 \times N$ operations.
  - **Use `formed` and `required` match counters for $O(1)$ verification**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `maxFreq` Does Not Need to Be Recomputed on `left++`:
> We are searching for the MAXIMUM window length.
> A larger valid window can ONLY be discovered if we encounter a character whose frequency is STRICTLY GREATER than the current `maxFreq`.
> Therefore, shrinking `left` without decrementing `maxFreq` can never produce a false positive `maxLen` result!

> **Memory Trick:** **"Never recompute maxFreq when shrinking left! Answer only improves when maxFreq increases!"**

---

## 13. System & Implementation Comparisons

| Feature | `formed` / `required` Counter Strategy | Full Array Sweep Strategy |
| :--- | :--- | :--- |
| **Validation Time** | **$O(1)$ Instant ⚡** | $O(128)$ Ops per step |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(128N)$ Operations |
| **Code Footprint** | Concise & Optimal | Verbose |

---

## 14. How to Recognize This in Questions
* **"Replace at most K characters to get longest substring of identical letters"** $\rightarrow$ LeetCode 424 (`len - maxFreq <= K`).
* **"Find shortest substring of S containing all characters of T"** $\rightarrow$ LeetCode 76 (`formed == required` match counter).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `formed` match counter handle duplicate target characters in Minimum Window Substring (LeetCode 76)?**  
  *A:* `formed` increments ONCE when `windowCount[c] == tCount[c]`. If `t` requires 2 'A's (`tCount['A'] = 2`), `formed` does NOT increment when the 1st 'A' enters, but increments when the 2nd 'A' enters.
* **Q: Why is Minimum Window Substring (LeetCode 76) classified as a SHORTEST window search?**  
  *A:* Because once a valid window is found (`formed == required`), we continuously shrink `left++` to find the SMALLEST valid substring before the window becomes invalid.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FREQUENCY WINDOWS & CHARACTER REPLACEMENT             |
+-----------------------------------------------------------------------+
| • Replacement Valid Condition: (right - left + 1) - maxFreq <= K      |
| • maxFreq Optimization: Never recompute maxFreq when shrinking left!  |
| • Min Window Substring (76): Track formed & required match counters   |
| • Match Counter Rule: Increment formed when windowCount[c] == tCount[c]|
| • Shortest Window Record: Save minLen INSIDE while (formed == required)|
| • Time Complexity: O(N) Linear Time | O(1) Auxiliary Space ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Character Replacement (LeetCode 424) in $O(N)$ time.
- [ ] I know why `maxFreq` does not need to be recomputed when shrinking `left`.
- [ ] I can write Minimum Window Substring (LeetCode 76) using `formed` and `required`.
- [ ] I know how `formed` handles duplicate target characters.
- [ ] I can state the replacement quota formula `(right - left + 1) - maxFreq <= K`.
