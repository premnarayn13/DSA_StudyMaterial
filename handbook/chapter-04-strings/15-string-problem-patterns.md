# 15. String Problem Recognition Patterns

## 1. Introduction
String algorithmic problems in technical coding interviews follow distinct pattern signals. Recognizing key problem phrasing—such as longest substring with $K$ unique characters, substring pattern matching, anagram grouping, or expression evaluation—enables instant selection of the optimal algorithmic paradigm: Two Pointers, Sliding Window, KMP, Rabin-Karp, Z-Algorithm, Expand Around Center, Trie, or Stack Parsing.

> **Important:** Rapidly identifying whether a string problem requires **Contiguous Substrings** (Sliding Window / KMP / Z-Algorithm) vs **Non-Contiguous Subsequences** (Dynamic Programming) dictates your solution architecture!

## 2. Core Concepts
* **Pattern 1: Two Pointers (Opposite Direction)**: Used for Palindrome validation (`isPalindrome`) and reverse word operations.
* **Pattern 2: Sliding Window (Dynamic / Variable Size)**: Used for "Longest Substring Without Repeating Characters" (LeetCode 3) or "Minimum Window Substring" (LeetCode 76).
* **Pattern 3: Sliding Window (Fixed Size $K$)**: Used for "Find All Anagrams in a String" (LeetCode 438) or fixed character frequency match windows.
* **Pattern 4: String Matching (Linear $O(N + M)$)**:
  * Use **KMP** when pattern has self-repeating prefixes/suffixes.
  * Use **Rabin-Karp** when performing **Multi-Pattern** search or rolling hash checks.
  * Use **Z-Algorithm** when checking exact prefix alignments via `P + "$" + T`.
* **Pattern 5: Expand Around Center ($O(N^2)$ Time, $O(1)$ Space)**: Used for Longest Palindromic Substring (LeetCode 5) and Palindromic Substrings Count (LeetCode 647).
* **Pattern 6: Trie Data Structure**: Used for prefix searches (`startsWith`), auto-complete, and multi-word 2D matrix searches (LeetCode 212).
* **Pattern 7: Stack-Based Expression Evaluation**: Used for Basic Calculator, string decoding (`3[a2[c]]`), and bracket validation.

> **Memory Trick:** **"Subarray/Substring Window -> Sliding Window; Multi-Pattern -> Rabin-Karp; Palindrome Center -> Expand Around Center; Prefix Lookups -> Trie"**.

## 3. Characteristics / Properties
* **Pattern Recognition Decision Matrix**:

```
Problem Phrasing / Signal                      Optimal String Pattern       Target Complexity
---------------------------------------------------------------------------------------------
Check if string reads same forward/backward     Two Pointers (Opposite)      O(N) Time, O(1) Space
Longest substring without repeating chars      Sliding Window (HashSet/Map)  O(N) Time, O(1) Space
Minimum window substring containing all chars  Sliding Window + Freq Array  O(N) Time, O(1) Space
Find pattern P in text T in linear time        KMP or Z-Algorithm           O(N + M) Time, O(M) Space
Find any of K patterns of length M in text     Rabin-Karp + HashSet         O(N + K*M) Time, O(K) Space
Longest palindromic substring                  Expand Around Center          O(N²) Time, O(1) Space
Auto-complete / Word prefix lookup             Trie Data Structure           O(L) Time per query
Evaluate expression "3+2*2" or decode "3[a]"   Stack Parsing (ArrayDeque)    O(N) Time, O(N) Space
```

## 4. Internal Working
Decision Tree for Selecting String Patterns:

```
                       [ String Problem ]
                               |
            +------------------+------------------+
            |                                     |
    [ Substring / Window ]                [ Global String Match ]
            |                                     |
    +-------+-------+                     +-------+-------+
    |               |                     |               |
[Contiguous]  [Palindromes]          [Pattern Search]  [Prefix Lookups]
    |               |                     |               |
(Sliding Window)(Expand Center)       (KMP/Rabin-Karp)  (Trie Structure)
```

## 5. Visual Diagram
Sliding Window Core Mechanics (Minimum Window Substring - LeetCode 76):

```
Text: ADOBECODEBANC, Target: ABC

Expand Right Pointer until window contains all target characters:
Window: [A D O B E C] -> Contains 'A','B','C'! (Valid window, len=6)

Shrink Left Pointer while window remains valid:
Shrink: A [D O B E C] -> Missing 'A'! (Stop shrinking)

Expand Right Pointer again:
Window: A D O [B E C O D E B A] -> Shrink Left -> ... -> [B A N C] (Valid window, len=4 🎉 MINIMUM!)
```

## 6. Operations / Algorithms
LeetCode 3 "Longest Substring Without Repeating Characters" Implementation:

```java
public int lengthOfLongestSubstring(String s) {
    if (s == null || s.length() == 0) return 0;

    int[] lastSeen = new int[256];
    Arrays.fill(lastSeen, -1);

    int maxLen = 0;
    int left = 0;

    for (int right = 0; right < s.length(); right++) {
        char ch = s.charAt(right);

        // If char was seen within current window, advance left pointer
        if (lastSeen[ch] >= left) {
            left = lastSeen[ch] + 1;
        }

        lastSeen[ch] = right; // Update last seen index
        maxLen = Math.max(maxLen, right - left + 1);
    }

    return maxLen;
}
```

> **Quick Syntax:**
```java
// Sliding Window Window Length Formula
int currentWindowLen = right - left + 1;
```

## 7. Examples
* **LeetCode 3 - Longest Substring Without Repeating Characters**: Sliding Window + `lastSeen[256]` array in $O(N)$ time.
* **LeetCode 76 - Minimum Window Substring**: Sliding Window + character frequency counting in $O(N)$ time.
* **LeetCode 438 - Find All Anagrams in a String**: Fixed Sliding Window of size $P$.

## 8. Java Code
Complete interview-ready Java suite implementing Longest Substring Without Repeating Characters and Minimum Window Substring:

```java
import java.util.Arrays;

public class StringPatternRecognitionMaster {

    // 1. Longest Substring Without Repeating Characters (LeetCode 3) O(N) Time, O(1) Space
    public static int lengthOfLongestSubstring(String s) {
        if (s == null || s.length() == 0) return 0;

        int[] lastSeen = new int[256]; // ASCII last seen index table
        Arrays.fill(lastSeen, -1);

        int maxLen = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);

            // If char was already seen inside current window, jump left pointer
            if (lastSeen[c] >= left) {
                left = lastSeen[c] + 1;
            }

            lastSeen[c] = right;
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }

    // 2. Minimum Window Substring (LeetCode 76) O(N + M) Time, O(1) Space
    public static String minWindow(String s, String t) {
        if (s == null || t == null || s.length() < t.length()) return "";

        int[] targetFreq = new int[256];
        for (char c : t.toCharArray()) {
            targetFreq[c]++;
        }

        int[] windowFreq = new int[256];
        int requiredMatches = 0;
        for (int count : targetFreq) {
            if (count > 0) requiredMatches++;
        }

        int formedMatches = 0;
        int left = 0, right = 0;
        int minLen = Integer.MAX_VALUE;
        int minStart = 0;

        while (right < s.length()) {
            char rightChar = s.charAt(right);
            windowFreq[rightChar]++;

            if (targetFreq[rightChar] > 0 && windowFreq[rightChar] == targetFreq[rightChar]) {
                formedMatches++;
            }

            // Shrink window from left as long as all matches are satisfied
            while (left <= right && formedMatches == requiredMatches) {
                char leftChar = s.charAt(left);

                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    minStart = left;
                }

                windowFreq[leftChar]--;
                if (targetFreq[leftChar] > 0 && windowFreq[leftChar] < targetFreq[leftChar]) {
                    formedMatches--;
                }
                left++;
            }

            right++;
        }

        return (minLen == Integer.MAX_VALUE) ? "" : s.substring(minStart, minStart + minLen);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Longest Substring Without Repeating Characters
        String s1 = "abcabcbb";
        System.out.println("Longest Substring without repeats in '" + s1 + "': " + lengthOfLongestSubstring(s1)); // Output: 3 ("abc")

        // Test Minimum Window Substring
        String text = "ADOBECODEBANC", target = "ABC";
        System.out.println("Min Window Substring of '" + target + "' in '" + text + "': \"" + minWindow(text, target) + "\""); // Output: "BANC"
    }
}
```

## 9. Complexity Analysis
| String Pattern | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Sliding Window (Last Seen Array)**| **$O(N)$ Linear** | **$O(1)$ Space (256 ints)**| Single pass, left pointer jumps |
| **Minimum Window Substring** | **$O(N + M)$ Linear** | **$O(1)$ Space (256 ints)**| Formed matches counter optimization |
| **KMP Pattern Search** | **$O(N + M)$ Linear** | $O(M)$ Space | Guaranteed linear pattern search |
| **Expand Around Center** | $O(N^2)$ | **$O(1)$ Space** | Zero memory allocation |

## 10. Edge Cases
* **Empty Input String**: Returns `0` or `""` immediately.
* **String with Single Unique Character** (e.g., `"bbbbb"`): Sliding window jumps left pointer smoothly; result is 1.
* **Target Not Present in Minimum Window**: Returns `""` cleanly without index errors.

## 11. Common Mistakes
* Using `HashSet<Character>` and shrinking `left` pointer step-by-step when `lastSeen[256]` index array allows `left` to jump to `lastSeen[ch] + 1` in $O(1)$ time!
* Recalculating character frequencies by iterating over the entire window on every step (causes $O(N^2)$ slowdown!).
* Forgetting to update `lastSeen[ch]` on every iteration in Sliding Window.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `lastSeen[256]` Array Jump Trick:
> Instead of shrinking `left` pointer one position at a time in a `while` loop, store character last seen indices in `int[] lastSeen = new int[256]`. When a duplicate character is encountered, jump `left` directly:
> **`if (lastSeen[ch] >= left) left = lastSeen[ch] + 1;`**

> **Memory Trick:** **"LastSeen Array allows left pointer to jump directly to lastSeen[ch] + 1!"**

## 13. Comparisons
| Metric | Sliding Window + HashSet | Sliding Window + `lastSeen[256]` Array |
| :--- | :--- | :--- |
| **Left Pointer Advance**| Step-by-step `while` loop | **Instantaneous Jump (`left = lastSeen[c] + 1`)** |
| **Time Complexity** | $O(N)$ | **$O(N)$ (Faster constant factor)** |
| **Auxiliary Space** | $O(N)$ Heap Objects | **$O(1)$ Fixed 256 ints** |
| **Interview Recommendation** | Good | **OPTIMAL & PREFERRED ⚡** |

## 14. How to Recognize This in Questions
* **"Find longest substring without repeating characters"** $\rightarrow$ Sliding Window + `lastSeen[256]` array ($O(N)$ time, $O(1)$ space).
* **"Find smallest substring containing all characters of pattern"** $\rightarrow$ Sliding Window + Formed Matches counter.
* **"Check if pattern P exists in text T"** $\rightarrow$ KMP ($O(N + M)$).

## 15. Frequently Asked Interview Questions
* **Q: Why is `int[256]` preferred over `HashMap<Character, Integer>` for character sliding windows?**  
  *A:* `int[256]` provides instant $O(1)$ array offset indexing without object allocation, autoboxing, or hash computation overhead, resulting in 10x faster execution and zero garbage collection pressure.
* **Q: How does the `formedMatches` counter optimize Minimum Window Substring?**  
  *A:* Instead of comparing all 256 array entries on every window slide (which takes $O(26 \cdot N)$ or $O(256 \cdot N)$ operations), `formedMatches` tracks how many unique characters meet their target frequency. When `formedMatches == requiredMatches`, we know the window is valid in $O(1)$ time!

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING PROBLEM RECOGNITION PATTERNS                   |
+-----------------------------------------------------------------------+
| • Longest Substring No Repeats: Sliding Window + lastSeen[256] array  |
| • Jump Rule: if (lastSeen[ch] >= left) left = lastSeen[ch] + 1        |
| • Minimum Window Substring: Expand right, shrink left when valid      |
| • Formed Matches Counter: Tracks satisfied unique char counts in O(1) |
| • Window Length: len = right - left + 1                               |
| • Optimal Complexity: O(N) Linear Time | O(1) Auxiliary Space         |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement Longest Substring Without Repeats using `lastSeen[256]`.
- [ ] I can write the `left = lastSeen[ch] + 1` pointer jump logic.
- [ ] I can implement Minimum Window Substring (LeetCode 76).
- [ ] I know how `formedMatches` avoids array comparisons on every window step.
- [ ] I can select between Sliding Window, KMP, Rabin-Karp, and Trie based on problem signals.
