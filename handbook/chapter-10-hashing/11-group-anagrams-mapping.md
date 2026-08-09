# 11. Group Anagrams, Frequency Key Formatting & Bijective Mapping Mechanics

## 1. Introduction
Grouping items by structural equivalence or verifying structural isomorphisms requires transforming objects into a **Canonical Hash Key**. Algorithms like **Group Anagrams (LeetCode 49)**, **Isomorphic Strings (LeetCode 205)**, and **Word Pattern (LeetCode 290)** rely on **Frequency Encoding Strings** or **Bijective Mapping Hash Maps** to group or validate string relationships in **$O(N \cdot K)$ linear time** (where $N$ is word count and $K$ is maximum word length).

> **Important:** Why is Frequency Array Key Generation (`#1#0#2...`) superior to Sorting Characters (`Arrays.sort()`) for Group Anagrams?
> * **Sorting Key**: `Arrays.sort(charArray)` takes $O(K \log K)$ time per word $\implies \mathbf{O(N \cdot K \log K)\text{ Total Time}}$.
> * **Frequency Encoding Key**: Counting 26 character frequencies into a string key (e.g. `#1#0#2...`) takes $O(K)$ time per word $\implies \mathbf{O(N \cdot K)\text{ Total Time}}$! ⚡

```
Canonical Hash Key Transformation Topology:
Words ("eat", "tea", "ate")  --->  [ Frequency Encoder int[26] ]
                                            |
                                            v
Canonical Key String          --->  "#1#0#0#0#1#0...#1" (Identical Key for all 3!)
HashMap Grouping              --->  Map.get("#1#0...") -> ["eat", "tea", "ate"] ⚡
```

---

## 2. Core Concepts & Group Anagrams Canonical Keys (LeetCode 49)

### 2.1 Group Anagrams Canonical Key Strategies
Given an array of strings `strs`, group the anagrams together in any order:

#### Strategy 1: Frequency Array String Key ($O(N \cdot K)$ Time - Optimal)
1. Initialize `Map<String, List<String>> map = new HashMap<>()`.
2. For each string `s` in `strs`:
   - Compute character frequency array `int[] count = new int[26]`.
   - Build canonical key string using delimiter: `#1#0#2#0...`
   - `map.putIfAbsent(key, new ArrayList<>())`.
   - `map.get(key).add(s)`.
3. Return `new ArrayList<>(map.values())`.

#### Strategy 2: Sorted Character Key ($O(N \cdot K \log K)$ Time)
* Convert string to `char[]`, execute `Arrays.sort(charArray)`, and use `String.valueOf(charArray)` as map key.

```
Canonical Key Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Strategy Variant      | Key Format        | Time Per Word     | Total Time (N Words)|
+-----------------------+-------------------+-------------------+-------------------+
| Sorted Character Key  | `"aet"`           | $O(K \log K)$     | $O(N \cdot K \log K)$|
| **Frequency Array Key**| **`"#1#0#0...#1"`**| **$O(K)$ ⚡**     | **$O(N \cdot K)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Group Anagrams: Frequency string key '#1#0#2' achieves strict O(N * K) time!"**

---

## 3. Characteristics & Bijective Mapping Mechanics (LeetCode 205 / 290)

### 3.1 Isomorphic Strings & Word Pattern Bijective Mapping (LeetCode 205 / 290)
Determine if string `s` and string `t` are isomorphic (characters in `s` can be replaced to get `t`):
* **Bijective Mapping Requirement**:
  - Every character $s[i]$ MUST map to EXACTLY one character $t[i]$.
  - No two distinct characters in $s$ can map to the SAME character in $t$!

#### 2-Map Strategy / Single Last-Seen Index Map Strategy ($O(N)$ Time):
```java
// Elegant Single Last-Seen Index Map Solution
public static boolean isIsomorphic(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] mapS = new int[256];
    int[] mapT = new int[256];

    for (int i = 0; i < s.length(); i++) {
        char c1 = s.charAt(i);
        char c2 = t.charAt(i);
        // Compare last seen 1-based index positions
        if (mapS[c1] != mapT[c2]) return false;
        mapS[c1] = i + 1; // Store 1-based index to distinguish from 0 default
        mapT[c2] = i + 1;
    }
    return true;
}
```

---

## 4. Internal Working Mechanics
Tracing Group Anagrams Frequency Key Generation on `["eat", "tea", "tan"]`:

```
String "eat":
  - Count Array: 'a'=1, 'e'=1, 't'=1, all others 0.
  - Key String : "#1#0#0#0#1#0#0#0#0#0#0#0#0#0#0#0#0#0#0#1#0#0#0#0#0#0"
  - Map: {"#1#0...": ["eat"]}

String "tea":
  - Count Array: 'a'=1, 'e'=1, 't'=1.
  - Key String : "#1#0...#1" (Matches Key!)
  - Map: {"#1#0...": ["eat", "tea"]}

String "tan":
  - Count Array: 'a'=1, 'n'=1, 't'=1.
  - Key String : "#1#0...#1#0" (Different Key!)
  - Map: {"#1#0...": ["eat", "tea"], "#1#0...n": ["tan"]}

Output = [["eat", "tea"], ["tan"]] ✅ (O(N * K) Time!)
```

---

## 5. Visual Diagram
Bijective Character Mapping Invariant Topography:

```
String S:   e   g   g
            |   |   |  (Bijective 1-to-1 Mapping)
String T:   a   d   d

Map S -> T: 'e' -> 'a', 'g' -> 'd'  (Valid Isomorphic Mapping! ✅)

String S:   f   o   o
            |   |   |
String T:   b   a   r  ('o' maps to 'a' AND 'r' -> Violation! ❌)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Group Anagrams (LeetCode 49), Isomorphic Strings (LeetCode 205), and Word Pattern (LeetCode 290):

```java
import java.util.*;

public class GroupAnagramsMappingMaster {

    // 1. Group Anagrams Frequency Array Key (LeetCode 49) O(N * K) Time, O(N * K) Space
    public static List<List<String>> groupAnagrams(String[] strs) {
        if (strs == null || strs.length == 0) return new ArrayList<>();

        Map<String, List<String>> map = new HashMap<>();

        for (String s : strs) {
            int[] count = new int[26];
            for (char c : s.toCharArray()) {
                count[c - 'a']++;
            }

            // Build canonical key string using StringBuilder
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 26; i++) {
                sb.append('#').append(count[i]);
            }
            String key = sb.toString();

            map.putIfAbsent(key, new ArrayList<>());
            map.get(key).add(s);
        }

        return new ArrayList<>(map.values());
    }

    // 2. Isomorphic Strings Bijective Index Map (LeetCode 205) O(N) Time, O(1) Space
    public static boolean isIsomorphic(String s, String t) {
        if (s == null || t == null || s.length() != t.length()) return false;

        int[] mapS = new int[256];
        int[] mapT = new int[256];

        for (int i = 0; i < s.length(); i++) {
            char c1 = s.charAt(i);
            char c2 = t.charAt(i);

            // Compare last seen 1-based indices
            if (mapS[c1] != mapT[c2]) {
                return false;
            }

            mapS[c1] = i + 1; // 1-based index marker
            mapT[c2] = i + 1;
        }

        return true;
    }

    // 3. Word Pattern Bijective Mapping (LeetCode 290) O(N) Time, O(N) Space
    public static boolean wordPattern(String pattern, String s) {
        if (pattern == null || s == null) return false;

        String[] words = s.split(" ");
        if (pattern.length() != words.length) return false;

        Map<Character, String> charToWord = new HashMap<>();
        Map<String, Character> wordToChar = new HashMap<>();

        for (int i = 0; i < pattern.length(); i++) {
            char c = pattern.charAt(i);
            String w = words[i];

            if (charToWord.containsKey(c)) {
                if (!charToWord.get(c).equals(w)) return false;
            } else {
                charToWord.put(c, w);
            }

            if (wordToChar.containsKey(w)) {
                if (wordToChar.get(w) != c) return false;
            } else {
                wordToChar.put(w, c);
            }
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// Frequency Key Builder Line
StringBuilder sb = new StringBuilder();
for (int c : count) sb.append('#').append(c);
String key = sb.toString();
```

---

## 7. Concrete Problem Examples
* **LeetCode 49 - Group Anagrams**: Canonical frequency array key string.
* **LeetCode 205 - Isomorphic Strings**: Bijective 1-to-1 index mapping.
* **LeetCode 290 - Word Pattern**: 2-way character-to-word mapping.
* **LeetCode 242 - Valid Anagram**: Character frequency validation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Group Anagrams, Isomorphic Strings, and Word Pattern:

```java
public class GroupAnagramsMappingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Group Anagrams (LeetCode 49) ===");
        String[] strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        List<List<String>> groups = GroupAnagramsMappingMaster.groupAnagrams(strs);
        System.out.println("Grouped Anagrams: " + groups);
        // Output: [[eat, tea, ate], [tan, nat], [bat]]

        System.out.println("\n=== 2. Isomorphic Strings (LeetCode 205) ===");
        System.out.println("Is \"egg\" and \"add\" Isomorphic? " + 
            GroupAnagramsMappingMaster.isIsomorphic("egg", "add")); // true
        System.out.println("Is \"foo\" and \"bar\" Isomorphic? " + 
            GroupAnagramsMappingMaster.isIsomorphic("foo", "bar")); // false

        System.out.println("\n=== 3. Word Pattern (LeetCode 290) ===");
        System.out.println("Pattern \"abba\" matches \"dog cat cat dog\"? " + 
            GroupAnagramsMappingMaster.wordPattern("abba", "dog cat cat dog")); // true
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Group Anagrams (49)** | **$O(N \cdot K)$ Linear ⚡** | $O(N \cdot K)$ Map Space | Frequency array key `#1#0#2...` |
| **Isomorphic Strings (205)**| **$O(N)$ Linear ⚡** | **$O(1)$ Array Space ⚡**| Dual last-seen 1-based index arrays |
| **Word Pattern (290)** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Dual map bijective verification |

---

## 10. Edge Cases & Boundary Handling
* **Empty / Single String Inputs**: Handled cleanly by base null checks.
* **1-Based Indexing in `isIsomorphic`**: Initializing `mapS[c] = i + 1` distinguishes index 0 from array default value `0`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Arrays.sort()` for Group Anagram Key ($O(N \cdot K \log K)$ Overhead)**:
  - Sorting characters for $N$ words takes $O(N \cdot K \log K)$ time.
  - **Use Frequency Encoding Key (`#1#0#2...`) for $O(N \cdot K)$ linear time**.
* **Using Single Directional Map for Isomorphic Verification**:
  - A single map `charToWord` permits two distinct keys to point to the same target value (violating bijection).
  - **Use 2 Maps or Dual Last-Seen Index Arrays for 1-to-1 bijection**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Delimiters (`#`) Are Required in Frequency Keys:
> Without delimiters, frequency counts `count[0]=1, count[1]=11` and `count[0]=11, count[1]=1` produce the SAME string key `"111"`!
> Adding `#` delimiters (`"#1#11"` vs `"#11#1"`) guarantees key uniqueness!

> **Memory Trick:** **"Always add '#' delimiters between frequency counts when building canonical string keys!"**

---

## 13. System & Implementation Comparisons

| Feature | Frequency Array Key (`#1#0#2`) | Sorted String Key (`"aet"`) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \cdot K)$ Linear ⚡** | $O(N \cdot K \log K)$ Logarithmic |
| **Key Generation Overhead**| StringBuilder Append | Character Array Sort |
| **Execution Speed** | **Fastest ⚡** | Slower |

---

## 14. How to Recognize This in Questions
* **"Group strings that contain identical character counts"** $\rightarrow$ LeetCode 49 (Frequency Array Key).
* **"Check if pattern matches string word sequence 1-to-1"** $\rightarrow$ LeetCode 290 (Bijective dual mapping).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `isIsomorphic` use 1-based index storage (`i + 1`)?**  
  *A:* Array slots in Java default to `0`. If we stored 0-based indices `i`, index 0 would be indistinguishable from unvisited default array slots. Storing `i + 1` ensures visited slots contain non-zero indices.
* **Q: What is a Bijective Function in computer science?**  
  *A:* A bijection is a 1-to-1 and onto mapping. For every element in set $A$, there is exactly one corresponding element in set $B$, and vice versa.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GROUP ANAGRAMS & BIJECTIVE MAPPING                   |
+-----------------------------------------------------------------------+
| • Group Anagrams Key: Use frequency string "#1#0#2" for O(N*K) time   |
| • Delimiter Rule: ALWAYS use '#' delimiter between counts             |
| • Isomorphic Check: Compare last seen indices: mapS[c1] == mapT[c2]   |
| • 1-Based Indexing: Store i + 1 to distinguish index 0 from default 0 |
| • Word Pattern (290): Dual maps required for 1-to-1 bijective match   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Group Anagrams (LeetCode 49) in $O(N \cdot K)$ time using frequency keys.
- [ ] I know why `#` delimiters are required in frequency keys.
- [ ] I can write Isomorphic Strings (LeetCode 205) using dual index arrays.
- [ ] I can write Word Pattern (LeetCode 290) using dual HashMap bijection.
- [ ] I know why 1-based indexing is used in last-seen arrays.
