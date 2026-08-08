# 11. Anagrams & Character Frequency Hashing

## 1. Introduction
Two strings are **Anagrams** if they contain the exact same characters with the exact same frequencies, differing only in character order (e.g., `"listen"` and `"silent"`). In technical coding interviews, anagram problems evaluate a candidate's mastery of frequency counting, canonical hashing keys, sliding window character match counts, and prime multiplication hashing for grouping anagrams.

> **Important:** Grouping Anagrams (LeetCode 49) can be solved by sorting each string in $O(N \cdot K \log K)$ time, OR by constructing a canonical **Frequency Tuple Key** (e.g., `#1#0#2...`) in **$O(N \cdot K)$ linear time**!

## 2. Core Concepts
* **Anagram Invariant**: Sorting two anagram strings produces identical character sequences (`sort(S1) == sort(S2)`).
* **Single Frequency Array Matching (`int[26]`)**: Incrementing counts for string 1 and decrementing for string 2. If all 26 elements in the array evaluate to `0`, the strings are anagrams.
* **Canonical Frequency Key (`buildKey`)**: Converting an `int[26]` array into a unique string key like `"1#0#2#0...#0"` to group anagrams in a `Map<String, List<String>>` in linear time.
* **Sliding Window Anagram Search (LeetCode 438)**: Maintaining a fixed window of size $P$ over text $T$ using frequency difference arrays or a `matches` counter.

> **Memory Trick:** **"Sort chars for O(N * K log K); Frequency key for O(N * K) linear performance!"**

## 3. Characteristics / Properties
* **Frequency Array Space Optimality**: `int[26]` frequency arrays consume **$O(1)$ constant auxiliary space** and zero garbage collection heap overhead.
* **Matches Counter Optimization**: In Sliding Window anagram search, keeping a `matches` count (number of characters whose frequency in window equals target frequency) avoids scanning all 26 array positions on every window step!

```
Anagram Grouping Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Grouping Strategy     | Time Complexity   | Space Complexity  | Key Advantage     |
+-----------------------+-------------------+-------------------+-------------------+
| Sorted Character Key  | O(N * K log K)    | O(N * K) Map      | Simple to code    |
| Frequency Tuple Key   | O(N * K)          | O(N * K) Map      | LINEAR TIME ⚡    |
| Prime Product Hash    | O(N * K)          | O(N * K) Map      | Numeric Hash Key  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Group Anagrams (LeetCode 49) via Frequency Tuple Keys:

```
Input: ["eat", "tea", "tan", "ate", "nat", "bat"]

Word "eat": freq array -> [a:1, b:0, c:0, d:0, e:1, ..., t:1, ...]
            Key generated: "1#0#0#0#1...#1..." -> HashMap["1#0#0#0#1..."] = ["eat"]

Word "tea": freq array -> Same [a:1, e:1, t:1]
            Key generated: "1#0#0#0#1...#1..." -> HashMap["1#0#0#0#1..."].add("tea")

Word "tan": Key generated: "1#0#0#0#0...#1...#1..." -> HashMap["..."] = ["tan"]

Final Grouped Result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]] ✅
```

## 5. Visual Diagram
Sliding Window Anagram Search (`Find All Anagrams in String`):

```
Text T:     c b a e b a b a c d    (Pattern P = "abc", Len = 3)
Window 0:  [c b a]                 Freq matches P! -> Index 0 added to results! 🎉
Shift 1:     [b a e]               'c' out, 'e' in -> Mismatch!
Shift 2:       [a e b]             Mismatch!
Shift 3:         [e b a]           Mismatch!
Shift 4:           [b a b]         Mismatch!
Shift 5:             [a b a]       Mismatch!
Shift 6:               [b a c]     Freq matches P! -> Index 6 added to results! 🎉
```

## 6. Operations / Algorithms
Canonical Frequency Key Builder & Group Anagrams Implementation:

```java
public List<List<String>> groupAnagrams(String[] strs) {
    if (strs == null || strs.length == 0) return new ArrayList<>();

    Map<String, List<String>> map = new HashMap<>();

    for (String s : strs) {
        // Build int[26] frequency array
        int[] freq = new int[26];
        for (char c : s.toCharArray()) {
            freq[c - 'a']++;
        }

        // Build canonical frequency key string: "#1#0#2#0..."
        StringBuilder sb = new StringBuilder();
        for (int count : freq) {
            sb.append('#').append(count);
        }
        String key = sb.toString();

        map.putIfAbsent(key, new ArrayList<>());
        map.get(key).add(s);
    }

    return new ArrayList<>(map.values());
}
```

> **Quick Syntax:**
```java
// Fast Key Generator using char array string constructor
char[] charArr = s.toCharArray();
Arrays.sort(charArr);
String sortedKey = new String(charArr);
```

## 7. Examples
* **LeetCode 242 - Valid Anagram**: Checking if two strings are anagrams in $O(N)$ time.
* **LeetCode 49 - Group Anagrams**: Grouping anagrams into lists using frequency keys in $O(N \cdot K)$ time.
* **LeetCode 438 - Find All Anagrams in a String**: Sliding window pattern matching in $O(N)$ time.
* **LeetCode 567 - Permutation in String**: Checking if $S_1$'s permutation is a substring of $S_2$.

## 8. Java Code
Complete interview-ready Java suite implementing Valid Anagram, Group Anagrams, and Sliding Window Anagram Finder:

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class AnagramsMaster {

    // 1. Valid Anagram Check O(N) Time, O(1) Space
    public static boolean isAnagram(String s, String t) {
        if (s == null || t == null || s.length() != t.length()) return false;

        int[] freq = new int[26];
        for (int i = 0; i < s.length(); i++) {
            freq[s.charAt(i) - 'a']++;
            freq[t.charAt(i) - 'a']--;
        }

        for (int count : freq) {
            if (count != 0) return false;
        }

        return true;
    }

    // 2. Group Anagrams (LeetCode 49) O(N * K) Time, O(N * K) Space
    public static List<List<String>> groupAnagrams(String[] strs) {
        if (strs == null || strs.length == 0) return new ArrayList<>();

        Map<String, List<String>> map = new HashMap<>();

        for (String s : strs) {
            int[] freq = new int[26];
            for (char c : s.toCharArray()) {
                freq[c - 'a']++;
            }

            // Build unique key
            StringBuilder sb = new StringBuilder();
            for (int count : freq) {
                sb.append('#').append(count);
            }
            String key = sb.toString();

            map.putIfAbsent(key, new ArrayList<>());
            map.get(key).add(s);
        }

        return new ArrayList<>(map.values());
    }

    // 3. Find All Anagrams in a String (LeetCode 438) O(N) Time, O(1) Space
    public static List<Integer> findAnagrams(String s, String p) {
        List<Integer> result = new ArrayList<>();
        if (s == null || p == null || s.length() < p.length()) return result;

        int[] pFreq = new int[26];
        int[] sFreq = new int[26];

        for (char c : p.toCharArray()) {
            pFreq[c - 'a']++;
        }

        int pLen = p.length();
        for (int i = 0; i < s.length(); i++) {
            // Add right character to window
            sFreq[s.charAt(i) - 'a']++;

            // Remove left character from window when window size > pLen
            if (i >= pLen) {
                sFreq[s.charAt(i - pLen) - 'a']--;
            }

            // Check if window frequency matches pattern frequency
            if (Arrays.equals(sFreq, pFreq)) {
                result.add(i - pLen + 1);
            }
        }

        return result;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Valid Anagram
        System.out.println("Is 'anagram' & 'nagaram' Anagram? " + isAnagram("anagram", "nagaram")); // true

        // Test Group Anagrams
        String[] words = {"eat", "tea", "tan", "ate", "nat", "bat"};
        System.out.println("Grouped Anagrams: " + groupAnagrams(words));
        // Output: [[eat, tea, ate], [tan, nat], [bat]]

        // Test Find All Anagrams
        String s = "cbaebabacd", p = "abc";
        System.out.println("Anagram Indices of 'abc' in 'cbaebabacd': " + findAnagrams(s, p));
        // Output: [0, 6]
    }
}
```

## 9. Complexity Analysis
| Problem Pattern | Sorting Approach Time | Frequency Key Approach Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Valid Anagram Check** | $O(N \log N)$ | **$O(N)$ Linear** | $O(1)$ constant space |
| **Group Anagrams ($N$ words)** | $O(N \cdot K \log K)$ | **$O(N \cdot K)$ Linear** | $O(N \cdot K)$ Map space |
| **Find All Anagrams ($N$ text)**| $O(N \cdot 26)$ | **$O(N)$ Linear** | $O(1)$ fixed 26 ints |

## 10. Edge Cases
* **Empty Strings / Null Inputs**: Return empty lists immediately.
* **Strings with Different Lengths**: `s.length() != t.length()` cannot be anagrams; return `false` in $O(1)$ time.
* **Non-Lowercase Characters**: If input includes uppercase or Unicode, `int[26]` causes index errors! Use `int[256]` or `HashMap<Character, Integer>`.

## 11. Common Mistakes
* Omitting delimiters `#` in frequency keys (e.g., building key `"1011"` for `freq[0]=1, freq[1]=0, freq[2]=11` matches `freq[0]=10, freq[1]=1, freq[2]=1`!). **Always separate counts with `#`**.
* Sorting every word in Group Anagrams when a linear $O(N \cdot K)$ frequency key approach was requested.
* Allocating a new frequency array inside the sliding window loop instead of modifying `sFreq` in-place.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why are delimiters (like `#`) mandatory in frequency key construction?
> Without delimiters, count array `[1, 0, 11]` generates `"1011"`, which collides with count array `[10, 1, 1]`! With delimiters, `"#1#0#11"` and `"#10#1#1"` are distinct keys.

> **Memory Trick:** **"Always format frequency keys as `#cnt0#cnt1#cnt2...`!"**

## 13. Comparisons
| Metric | Sorted String Key (`sort(s)`) | Frequency Tuple Key (`#1#0...`) |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \cdot K \log K)$ | **$O(N \cdot K)$ (Optimal)** |
| **Code Simplicity** | Very Simple | Simple |
| **Key Length** | $K$ characters | $\approx 50$ characters |
| **Interview Recommendation** | Good start | **OPTIMAL FINAL ANSWER** |

## 14. How to Recognize This in Questions
* **"Group words that are anagrams of each other"** $\rightarrow$ Group Anagrams using Frequency Tuple Key.
* **"Find all occurrence indices of pattern permutation in text"** $\rightarrow$ Sliding Window Frequency Matching ($O(N)$).

## 15. Frequently Asked Interview Questions
* **Q: How does `Arrays.equals(sFreq, pFreq)` run in $O(1)$ time?**  
  *A:* Because both arrays are fixed at length 26! The array comparison performs exactly 26 primitive integer equality checks, taking constant $O(1)$ time independent of text length $N$.
* **Q: Can Prime Multiplication Hashing be used for Anagram Grouping?**  
  *A:* Yes! Map each character `'a'...'z'` to a distinct prime number (2, 3, 5, 7, 11...). The product of prime values for any anagram is identical (Fundamental Theorem of Arithmetic). However, product hashing risks `long` overflow for long words ($K > 15$).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ANAGRAMS & CHARACTER FREQUENCY HASHING                |
+-----------------------------------------------------------------------+
| • Anagram Check: int[26] freq; ++ for s1, -- for s2; check all == 0   |
| • Group Anagram Key: #cnt0#cnt1#...#cnt25 -> HashMap<String, List>    |
| • Delimiters Mandatory: Prevents "1"+"011" == "10"+"11" key collisions |
| • Sliding Window Anagrams: Maintain sFreq[26], compare via            |
|   Arrays.equals(sFreq, pFreq) in O(1) time per step                   |
| • Group Anagrams Complexity: O(N * K) Time | O(N * K) Space            |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write single-array Valid Anagram check in $O(N)$ time.
- [ ] I can build a delimiter-separated frequency tuple key string.
- [ ] I can implement Group Anagrams in $O(N \cdot K)$ linear time.
- [ ] I can implement Sliding Window Anagram Search (LeetCode 438).
- [ ] I know why `Arrays.equals(sFreq, pFreq)` is $O(1)$ time for 26-element arrays.
