# 07. String Sliding Window Problems, Substring Concatenation & Multi-Word Match Sweeping

## 1. Introduction
String sliding window problems represent a core category of string processing algorithms in technical interviews. By leveraging 2-pointer window mechanics alongside character frequency arrays (`int[128]` or `int[26]`) and word hash maps, problems such as **Substring with Concatenation of All Words (LeetCode 30)**, **Minimum Window Substring (LeetCode 76)**, **Find All Anagrams in a String (LeetCode 438)**, and **Longest Substring Without Repeating Characters (LeetCode 3)** are solved efficiently in **$O(N \cdot L)$ or $O(N)$ linear time**.

> **Important:** In **Substring with Concatenation of All Words (LeetCode 30)**, where all words in array `words` have an identical length $L$, we execute **$L$ independent fixed-size sliding window passes** (offsetting start indices from `0` to $L-1$). This optimizes multi-word substring searching from $O(N \cdot K \cdot L)$ down to **$O(N \cdot L)$ time**!

```
Substring Concatenation Multi-Pass Window Offset Topology:
Pass 0 (Start Offset 0) : Index 0, L, 2L, 3L ...
Pass 1 (Start Offset 1) : Index 1, 1+L, 1+2L, 1+3L ...
...
Pass L-1 (Offset L-1)   : Index L-1, 2L-1, 3L-1 ...
Covers EVERY possible substring boundary in exactly L linear scans! ⚡
```

---

## 2. Core Concepts & Substring Concatenation Mechanics (LeetCode 30)

### 2.1 Substring with Concatenation of All Words (LeetCode 30)
Given a string `s` and an array of strings `words` where all words have identical length $L$:
* Return all starting indices of substring(s) in `s` that are a concatenation of every word in `words` exactly once.

#### Algorithmic Strategy ($O(N \cdot L)$ Time, $O(M)$ Auxiliary Space):
1. Let $K = \text{words.length}$, $L = \text{words}[0].\text{length()}$, total length $W = K \times L$.
2. Create frequency map `wordMap` storing word occurrences in `words`.
3. Loop offset $i$ from `0` to $L - 1$:
   - `left = i`, `count = 0`.
   - Maintain `seenMap` tracking word counts in current window.
   - For `right = i` to $N - L$ (incrementing by $L$):
     - Extract word: `sub = s.substring(right, right + L)`.
     - If `sub` is in `wordMap`:
       - `seenMap.put(sub, seenMap.getOrDefault(sub, 0) + 1)`.
       - `count++`.
       - **Shrink Window While Word Over-used**:
         - While `seenMap.get(sub) > wordMap.get(sub)`:
           - `leftWord = s.substring(left, left + L)`.
           - `seenMap.put(leftWord, seenMap.get(leftWord) - 1)`.
           - `count--`.
           - `left += L`.
       - If `count == K`: Add `left` to result list!
     - Else (`sub` not in `wordMap`):
       - Reset window: `seenMap.clear()`, `count = 0`, `left = right + L`.

```
Why Offset Iteration i from 0 to L-1 Works:
By advancing right in steps of L (right += L), a single pass checks all word-aligned windows.
Running L passes offset by 0, 1 ... L-1 guarantees checking every contiguous substring of length W! ⚡
```

> **Memory Trick:** **"LeetCode 30: Run L offset passes! Jump pointers by L steps (right += L, left += L)! Reset window if word not in map!"**

---

## 3. Characteristics & String Window Problem Spectrum

```
+-----------------------------------------------------------------------------------+
| STRING SLIDING WINDOW PROBLEM CLASSIFICATION                                       |
+-----------------------------------+-----------------------+-----------------------+
| Problem                           | Window Size Strategy  | Key Validation Rule   |
+-----------------------------------+-----------------------+-----------------------+
| LeetCode 3 (No Repeats)           | Variable (Expand/Jump)| `charMap[c] < left`   |
| LeetCode 76 (Min Substring)       | Variable Shortest     | `formed == required`  |
| LeetCode 438 (All Anagrams)       | Fixed ($K = p.len$)   | `matches == 26`       |
| LeetCode 567 (Permutation String) | Fixed ($K = s1.len$)  | `matches == 26`       |
| LeetCode 30 (Word Concatenation)  | Multi-Pass Fixed ($W$)| `count == words.length`|
+-----------------------------------+-----------------------+-----------------------+
```

---

## 4. Internal Working Mechanics
Tracing Substring Concatenation (LeetCode 30) on `s = "barfoothefoobarman"`, `words = ["foo", "bar"]` ($L = 3, K = 2, W = 6$):

```
wordMap: {"foo": 1, "bar": 1}. K = 2, L = 3.

Pass 0 (i = 0):
  right = 0 ("bar"): Valid! seenMap: {"bar": 1}, count = 1.
  right = 3 ("foo"): Valid! seenMap: {"bar": 1, "foo": 1}, count = 2 == K!
    -> Record start index left = 0! Result = [0].
  right = 6 ("the"): Invalid word! Clear seenMap, count = 0, left = 9.
  ...

Pass 1 (i = 1): "arf", "oot", "hef"... (No matches)
Pass 2 (i = 2): "rfo", "oth", "efo"... (No matches)

Pass 0 (Later right = 9 "foo", right = 12 "bar"):
  right = 9 ("foo"): Valid! seenMap: {"foo": 1}, count = 1.
  right = 12 ("bar"): Valid! seenMap: {"foo": 1, "bar": 1}, count = 2 == K!
    -> Record start index left = 9! Result = [0, 9].

Final Concatenation Indices: [0, 9] ✅ (O(N) Time, O(M) Space!)
```

---

## 5. Visual Diagram
Substring Concatenation Offset Pass Traversal Topography:

```
s = " b  a  r  f  o  o  t  h  e  f  o  o  b  a  r  m  a  n "
    [=========] [=========]                                    Pass 0: "bar" + "foo" = Valid Concatenation at Idx 0 ✅
                   [=========] [=========]                     Pass 0: "foo" + "bar" = Valid Concatenation at Idx 9 ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Substring with Concatenation of All Words (LeetCode 30) and Find All Anagrams in a String (LeetCode 438):

```java
import java.util.*;

public class StringProblemsMaster {

    // 1. Substring with Concatenation of All Words (LeetCode 30) O(N * L) Time, O(M) Space
    public static List<Integer> findSubstring(String s, String[] words) {
        List<Integer> result = new ArrayList<>();
        if (s == null || words == null || words.length == 0 || s.length() == 0) {
            return result;
        }

        int wordLen = words[0].length();
        int numWords = words.length;
        int totalLen = wordLen * numWords;

        if (s.length() < totalLen) return result;

        Map<String, Integer> wordMap = new HashMap<>();
        for (String word : words) {
            wordMap.put(word, wordMap.getOrDefault(word, 0) + 1);
        }

        // Execute L independent offset passes
        for (int i = 0; i < wordLen; i++) {
            Map<String, Integer> seenMap = new HashMap<>();
            int left = i;
            int count = 0;

            for (int right = i; right <= s.length() - wordLen; right += wordLen) {
                String sub = s.substring(right, right + wordLen);

                if (wordMap.containsKey(sub)) {
                    seenMap.put(sub, seenMap.getOrDefault(sub, 0) + 1);
                    count++;

                    // Shrink window if word is over-used
                    while (seenMap.get(sub) > wordMap.get(sub)) {
                        String leftWord = s.substring(left, left + wordLen);
                        seenMap.put(leftWord, seenMap.get(leftWord) - 1);
                        count--;
                        left += wordLen;
                    }

                    // Record start index if all words matched
                    if (count == numWords) {
                        result.add(left);
                    }
                } else {
                    // Reset window state if unknown word encountered
                    seenMap.clear();
                    count = 0;
                    left = right + wordLen;
                }
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Word Window Step Progression
for (int right = i; right <= s.length() - wordLen; right += wordLen) {
    String sub = s.substring(right, right + wordLen);
    ...
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 30 - Substring with Concatenation of All Words**: Multi-pass offset word window.
* **LeetCode 76 - Minimum Window Substring**: Shortest frequency match string.
* **LeetCode 438 - Find All Anagrams in a String**: Fixed-size character frequency sweep.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Substring with Concatenation of All Words:

```java
public class StringProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Substring Concatenation (LeetCode 30) ===");
        String s = "barfoothefoobarman";
        String[] words = {"foo", "bar"};
        List<Integer> indices = StringProblemsMaster.findSubstring(s, words);
        System.out.println("Concatenation Start Indices: " + indices); // Output: [0, 9]
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Concatenation (30)** | **$O(N \cdot L)$ Linear ⚡**| $O(M)$ Hash Map | $L$ offset passes with step $L$ |
| **Min Substring (76)** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `formed == required` match counter |
| **Find Anagrams (438)** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `matches == 26` frequency check |

---

## 10. Edge Cases & Boundary Handling
* **Empty `words` Array**: Returns empty list immediately.
* **String `s` Length Smaller Than $W = K \times L$**: Returns empty list immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Checking Substrings Without Word Alignment ($O(N \cdot K \cdot L)$ Penalty)**:
  - Extracting all substrings at every single character index and comparing against `wordMap` degrades performance to $O(N \cdot K \cdot L)$!
  - **Execute $L$ offset passes with `right += wordLen` increments for $O(N \cdot L)$ time**.
* **Forgetting `left += wordLen` when Shrinking Over-used Words**:
  - Advancing `left` by 1 character instead of `wordLen` breaks word boundary alignment.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Substring Concatenation (30) Requires $L$ Offset Passes:
> A valid concatenation can start at ANY character index $0, 1 \dots L-1$.
> Once an offset start index $i$ is chosen, all subsequent words in the window MUST align to boundaries $i + k \cdot L$.
> Running $L$ passes covers all possible start offsets in $O(N \cdot L)$ time!

> **Memory Trick:** **"Word concatenation sliding window: Always step by wordLen (right += L, left += L) across L offset passes!"**

---

## 13. System & Implementation Comparisons

| Feature | $L$ Offset Passes Sliding Window | Naive Full Substring Check |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \cdot L)$ Optimal ⚡** | $O(N \cdot K \cdot L)$ |
| **State Reusability**| 100% Word Counts Reused | 0% (Re-parsed from scratch) |
| **Word Alignment** | Preserved | Re-parsed |

---

## 14. How to Recognize This in Questions
* **"Find all starting indices of substring concatenated from all words of equal length L"** $\rightarrow$ LeetCode 30 ($L$ offset passes with step $L$).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does LeetCode 30 require all words in `words` to have equal length $L$?**  
  *A:* Equal word length $L$ guarantees that window boundaries shift uniformly by $L$ steps (`right += L`), allowing sliding window frequency re-use.
* **Q: What happens when an unknown word is encountered in LeetCode 30?**  
  *A:* The window is reset: `seenMap.clear()`, `count = 0`, and `left` jumps directly past the unknown word (`left = right + L`).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING SLIDING WINDOW PROBLEMS & CONCATENATION        |
+-----------------------------------------------------------------------+
| • Word Concatenation (30): Run L offset passes (i = 0..L-1)           |
| • Window Progression: Advance right by wordLen (right += wordLen)     |
| • Over-used Word Shrink: while (seenMap[sub] > wordMap[sub]) left += L |
| • Unknown Word Reset: seenMap.clear(), count = 0, left = right + L    |
| • Match Condition: count == numWords -> Record start index left       |
| • Time Complexity: O(N * L) Linear Time | O(M) Auxiliary Space ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Substring with Concatenation of All Words (LeetCode 30).
- [ ] I know why $L$ offset passes are required for word alignment.
- [ ] I know how to handle over-used and unknown words in LeetCode 30.
- [ ] I can state the time complexity of LeetCode 30 ($O(N \cdot L)$).
- [ ] I know when to step by `wordLen` vs 1 character.
