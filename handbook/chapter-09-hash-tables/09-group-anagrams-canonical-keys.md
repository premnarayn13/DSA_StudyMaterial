# 09. Group Anagrams & Canonical Frequency Key Architecture

## 1. Introduction
Grouping anagrams (LeetCode 49) and string equivalence clustering under transformations are fundamental string hashing problems in technical coding interviews. Given an array of strings `strs`, we must group all anagrams together into sublists. Anagrams are strings formed by rearranging the letters of another string. The core algorithmic challenge is converting each string into a **Canonical Key Identifier** such that all anagrammatic permutations produce the **EXACT SAME HASH MAP KEY**, enabling grouping in **$O(N \cdot L)$ linear time** (where $N$ is the number of strings and $L$ is the maximum string length).

> **Important:** While sorting characters (`Arrays.sort(charArray)`) constructs a valid canonical key in $O(N \cdot L \log L)$ time, constructing a **26-Character Frequency Tuple Key** (e.g. `#1#0#2...`) achieves optimal **$O(N \cdot L)$ linear time**!

```
Canonical Key Generation Performance:
+-----------------------------------------------------------------------------------+
| Sorted Character Key  : "eat" -> 'a','e','t' -> "aet"          -> O(N * L log L)  |
| Character Frequency   : "eat" -> 1 'a', 1 'e', 1 't'           -> O(N * L) Linear ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Canonical Key Strategies

### 2.1 What is a Canonical Form?
A **Canonical Form** is a standardized mathematical representation such that every element in an equivalence class maps to the exact same representative identifier.
* For anagrams: Two strings $S_1$ and $S_2$ are anagrams if and only if:
  $$\text{canonicalKey}(S_1) == \text{canonicalKey}(S_2)$$

### 2.2 Strategy 1: Sorted Character Array Key ($O(N \cdot L \log L)$ Time)
1. Convert string $S$ to a character array `char[] ca = S.toCharArray()`.
2. Sort the array `Arrays.sort(ca)`.
3. Convert back to string `String key = new String(ca)`.
4. All anagrams (e.g. `"eat"`, `"tea"`, `"ate"`) produce the identical sorted string key `"aet"`.

### 2.3 Strategy 2: Character Frequency Count Tuple Key ($O(N \cdot L)$ Linear Time - OPTIMAL)
Since strings consist of lowercase English letters (`'a'` to `'z'`), we can count character frequencies using a 26-element array `int[] count = new int[26]`.
1. Iterate over characters in $S$, incrementing `count[c - 'a']++`.
2. Format `count` into a string representation, using a delimiter (`#`) to prevent frequency ambiguity:
   $$\text{Key} = \text{"\#1\#0\#0\#0\#1\dots\#1"}$$
3. Because generating `count` takes $O(L)$ time for string length $L$, total processing across $N$ strings takes **$O(N \cdot L)$ linear time**!

```
Character Frequency Key Formats:
String "eat":
Count: a:1, b:0, c:0, d:0, e:1 ... t:1 ...
Key  : "#1#0#0#0#1#0#0#0#0#0#0#0#0#0#0#0#0#0#0#1#0#0#0#0#0#0"

String "tea":
Count: a:1, b:0, c:0, d:0, e:1 ... t:1 ...
Key  : "#1#0#0#0#1#0#0#0#0#0#0#0#0#0#0#0#0#0#0#1#0#0#0#0#0#0" (IDENTICAL KEY!) ✅
```

> **Memory Trick:** **"Sorted Key = O(N * L log L)! Frequency Count Key (#1#0#1...) = O(N * L) Linear Time!"**

---

## 3. Characteristics & Delimiter Ambiguity Audits

### 3.1 Why Delimiters are MANDATORY in Frequency Keys
Suppose string $S_1$ has 1 `'a'` and 11 `'b'`s, while string $S_2$ has 11 `'a'`s and 1 `'b'`.
* Without delimiters:
  - $S_1$ frequency counts `[1, 11]` concatenated $\to$ `"111"`.
  - $S_2$ frequency counts `[11, 1]` concatenated $\to$ `"111"`.
  - **FALSE COLLISION BUG!** $S_1$ and $S_2$ are NOT anagrams, but produce the exact same raw string `"111"`.
* With delimiters (`#`):
  - $S_1$ key: `"#1#11"`.
  - $S_2$ key: `"#11#1"`.
  - Keys are distinct! `#` delimiters eliminate string representation ambiguity.

---

## 4. Internal Working Mechanics
Tracing Group Anagrams (LeetCode 49) on `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`:

```
Init Map: HashMap<String, List<String>> map = new HashMap<>();

Process "eat":
Freq Count: [1, 0, 0, 0, 1 ... 1 ...] -> Key: "#1#0#0#0#1...#1"
map.put("#1#0...", ["eat"])

Process "tea":
Freq Count: [1, 0, 0, 0, 1 ... 1 ...] -> Key: "#1#0#0#0#1...#1"
Key exists! map.get("#1#0...").add("tea") -> ["eat", "tea"]

Process "tan":
Freq Count: [1, 0, 0, 0, 0 ... 1 ... 1] -> Key: "#1#0#0#0#0...#1#1"
map.put("#1#0...#1#1", ["tan"])

Process "ate":
Freq Key matches "#1#0...#1" -> ["eat", "tea", "ate"]

Process "nat":
Freq Key matches "#1#0...#1#1" -> ["tan", "nat"]

Process "bat":
Freq Key: "#1#1...#1" -> map.put("#1#1...", ["bat"])

Output: [ ["eat", "tea", "ate"], ["tan", "nat"], ["bat"] ] ✅ (O(N * L) Time!)
```

---

## 5. Visual Diagram
Group Anagrams Hash Map Canonical Key Mapping Topology:

```
Input Strings: ["eat", "tea", "tan", "ate", "nat", "bat"]

           [ CANONICAL FREQUENCY KEY GENERATOR ]
                         |
      +------------------+------------------+
      |                                     |
Key: "#1#0#0#0#1...#1"                Key: "#1#0...#1#1"        Key: "#1#1...#1"
      |                                     |                         |
      v                                     v                         v
+------------------+                  +------------------+      +------------------+
| ["eat", "tea",   |                  | ["tan", "nat"]   |      | ["bat"]          |
|  "ate"]          |                  +------------------+      +------------------+
+------------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Group Anagrams (LeetCode 49), Valid Anagram (LeetCode 242), and Group Shifted Strings (LeetCode 249):

```java
import java.util.*;

public class GroupAnagramsCanonicalMaster {

    // 1. Group Anagrams using Frequency Count Key O(N * L) Time, O(N * L) Space - OPTIMAL
    public static List<List<String>> groupAnagramsFrequency(String[] strs) {
        if (strs == null || strs.length == 0) return new ArrayList<>();

        Map<String, List<String>> map = new HashMap<>();

        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) {
                count[c - 'a']++;
            }

            // Build canonical string key with '#' delimiters
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 26; i++) {
                sb.append('#').append(count[i]);
            }
            String key = sb.toString();

            if (!map.containsKey(key)) {
                map.put(key, new ArrayList<>());
            }
            map.get(key).add(s);
        }

        return new ArrayList<>(map.values());
    }

    // 2. Group Anagrams using Sorted Char Array Key O(N * L log L) Time, O(N * L) Space
    public static List<List<String>> groupAnagramsSorted(String[] strs) {
        if (strs == null || strs.length == 0) return new ArrayList<>();

        Map<String, List<String>> map = new HashMap<>();

        for (String s : strs) {
            char[] ca = s.toCharArray();
            Arrays.sort(ca);
            String key = String.valueOf(ca);

            if (!map.containsKey(key)) {
                map.put(key, new ArrayList<>());
            }
            map.get(key).add(s);
        }

        return new ArrayList<>(map.values());
    }

    // 3. Group Shifted Strings (LeetCode 249) O(N * L) Time, O(N * L) Space
    public static List<List<String>> groupShiftedStrings(String[] strings) {
        Map<String, List<String>> map = new HashMap<>();

        for (String s : strings) {
            // Build shift-invariant diff key: e.g. "abc" diffs -> "1#1#", "xyz" -> "1#1#"
            StringBuilder sb = new StringBuilder();
            for (int i = 1; i < s.length(); i++) {
                int diff = s.charAt(i) - s.charAt(i - 1);
                if (diff < 0) diff += 26; // Cyclic shift handling
                sb.append(diff).append('#');
            }
            String key = sb.toString();

            if (!map.containsKey(key)) {
                map.put(key, new ArrayList<>());
            }
            map.get(key).add(s);
        }

        return new ArrayList<>(map.values());
    }
}
```

> **Quick Syntax:**
```java
// Frequency Count Key Formatting
StringBuilder sb = new StringBuilder();
for (int c : count) sb.append('#').append(c);
String key = sb.toString();
```

---

## 7. Concrete Problem Examples
* **LeetCode 49 - Group Anagrams**: Grouping strings using canonical keys.
* **LeetCode 242 - Valid Anagram**: Checking character frequency equality.
* **LeetCode 249 - Group Shifted Strings**: Grouping strings under cyclic shift transformations.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Group Anagrams (both Frequency and Sorted key strategies) and Group Shifted Strings:

```java
public class GroupAnagramsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Group Anagrams (Frequency Key O(N*L)) ===");
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        System.out.println("Input: " + Arrays.toString(strs));
        System.out.println("Grouped Output: " + GroupAnagramsCanonicalMaster.groupAnagramsFrequency(strs));

        System.out.println("\n=== 2. Group Shifted Strings (LeetCode 249) ===");
        String[] shifted = {"abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"};
        System.out.println("Input: " + Arrays.toString(shifted));
        System.out.println("Shift Grouped Output: " + GroupAnagramsCanonicalMaster.groupShiftedStrings(shifted));
    }
}
```

---

## 9. Complexity Analysis

| Canonical Key Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Frequency Count Key (`#1#0...`)**| **$O(N \cdot L)$ Linear ⚡** | **$O(N \cdot L)$** | 26-Element Array Formatting |
| **Sorted Char Key (`Arrays.sort`)**| $O(N \cdot L \log L)$ | $O(N \cdot L)$ | Char Array Sorting Cost |
| **Shift Diff Key (LeetCode 249)** | **$O(N \cdot L)$ Linear ⚡** | $O(N \cdot L)$ | Difference Array Formatting |

---

## 10. Edge Cases & Boundary Handling
* **Empty Strings (`strs = ["", ""]`)**: Frequency count key generates `"#0#0...#0"`, grouping empty strings into a single list `[["", ""]]` cleanly.
* **Single Character Strings (`strs = ["a", "b", "a"]`)**: Handled correctly as separate groups.
* **Cyclic Shift Wraparound (LeetCode 249)**: Computing character differences e.g. `'a' - 'z' = -25`. Adding `+ 26` converts `-25` to positive `1` (`'z' -> 'a'` shift diff).

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting Delimiters in Frequency Keys**: Concatenating counts without `#` causes false collisions between count `[1, 11]` and `[11, 1]`!
* **Using `Arrays.toString(count)` vs `StringBuilder`**: `Arrays.toString(int[])` creates unnecessary heap allocation noise. Using `StringBuilder` with `#` is faster.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Frequency Key vs Sorted Key Trade-Off:
> * **Frequency Count Key (`#1#0#1...`)**: Takes **$O(N \cdot L)$ linear time**. Optimal for short alphabet sizes (e.g. 26 lowercase English letters).
> * **Sorted Char Key (`Arrays.sort`)**: Takes **$O(N \cdot L \log L)$ time**. Preferred if character set is unlimited (Unicode / 128 ASCII).

> **Memory Trick:** **"Lowercase English? Use Frequency Key #1#0... for O(N*L)! Unlimited Unicode? Use Sorted Char Key!"**

---

## 13. System & Implementation Comparisons

| Feature | Sorted Character Key | Frequency Count Key |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \cdot L \log L)$ | **$O(N \cdot L)$ Linear ⚡** |
| **Alphabet Constraint**| Works for ALL Unicode chars | Requires bounded alphabet (e.g. 26) |
| **String Overhead** | Short key length $L$ | Fixed 26-element key length ~52 chars |

---

## 14. How to Recognize This in Questions
* **"Group strings that can be formed by rearranging characters"** $\rightarrow$ Group Anagrams with Canonical Key Map (`HashMap<String, List<String>>`).
* **"Group strings that belong to the same shift sequence"** $\rightarrow$ Group Shifted Strings with Shift Difference Key.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Frequency Count Key achieve $O(N \cdot L)$ time complexity?**  
  *A:* For each string of length $L$, counting character frequencies takes $O(L)$ time, and formatting the 26-element frequency array into a key string takes $O(26) = O(1)$ constant time. Across $N$ strings, total time is $N \cdot (O(L) + O(1)) = \mathbf{O(N \cdot L)}$.
* **Q: How to handle Group Shifted Strings (LeetCode 249) when difference between characters is negative?**  
  *A:* When `diff = s.charAt(i) - s.charAt(i - 1) < 0`, add 26 (`diff += 26`). For example, for `"ba"`, `'a' - 'b' = -1 \to -1 + 26 = 25`. This normalizes cyclic wraparound shifts across the alphabet.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GROUP ANAGRAMS & CANONICAL KEYS                       |
+-----------------------------------------------------------------------+
| • Anagram Condition: Strings are anagrams iff CanonicalKeys are equal |
| • Frequency Key: int[26] count -> format as "#1#0#1..." -> O(N * L) ⚡|
| • Sorted Key: Arrays.sort(charArray) -> O(N * L log L)                |
| • Delimiter Rule: ALWAYS use '#' delimiter to avoid 1,11 vs 11,1 bugs |
| • Shifted Strings (249): Key = (char[i] - char[i-1] + 26) % 26        |
| • Output Pattern: HashMap<String, List<String>> -> return map.values()|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Frequency Count Key generator with `#` delimiters.
- [ ] I know why `#` delimiters are mandatory to prevent false collisions.
- [ ] I can write the Sorted Char Key implementation.
- [ ] I know when to choose Frequency Key ($O(N \cdot L)$) vs Sorted Key ($O(N \cdot L \log L)$).
- [ ] I can solve Group Shifted Strings (LeetCode 249) using shift diff keys.
