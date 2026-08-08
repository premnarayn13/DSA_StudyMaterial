# 11. Isomorphic Strings & Bijective Hash Mapping

## 1. Introduction
Determining if two strings are **Isomorphic** (LeetCode 205 - Isomorphic Strings), checking **Word Pattern matching** (LeetCode 290 - Word Pattern), and enforcing **Bijective Character Mappings** are essential string equivalence problems in technical coding interviews. Two strings $S$ and $T$ are isomorphic if the characters in $S$ can be replaced to get $T$, preserving character order and establishing a **strict One-to-One and Onto (Bijective) relationship** between characters in $S$ and characters in $T$.

> **Important:** A simple one-way mapping ($S \to T$) is INSUFFICIENT! Two distinct characters in $S$ CANNOT map to the same character in $T$. To enforce bijectivity in $O(N)$ time, we must either use **Dual Hash Maps** ($S \to T$ and $T \to S$) or a **Last-Seen Index Array** (`int[256]`)!

```
Bijective Mapping Principle:
+-----------------------------------------------------------------------------------+
| One-Way Map (S -> T) Bug : "ab" -> "aa" ('a'->'a', 'b'->'a') -> WRONG! Overlaps!  |
| Bijective Map (S <-> T)  : Requires 1-to-1 Mapping in BOTH directions -> CORRECT! |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Algebra

### 2.1 The Mathematical Definition of a Bijective Function
Let $\Sigma_S$ be the alphabet of string $S$ and $\Sigma_T$ be the alphabet of string $T$.
A mapping $f: \Sigma_S \to \Sigma_T$ is **Isomorphic** if and only if $f$ is a **Bijection** (both Injective and Surjective):
1. **Injective (One-to-One)**: If $x_1 \neq x_2$, then $f(x_1) \neq f(x_2)$. No two characters in $S$ map to the same character in $T$.
2. **Surjective (Onto)**: Every character in $T$ has a corresponding character in $S$.
3. **Order Preserving**: For all indices $i$, $T[i] = f(S[i])$.

### 2.2 Technique 1: Dual Hash Maps ($O(N)$ Time, $O(N)$ Space)
Maintain two separate Hash Maps:
* `mapST<Character, Character>`: Tracks mapping $S[i] \to T[i]$.
* `mapTS<Character, Character>`: Tracks mapping $T[i] \to S[i]$.
* At each index $i$:
  - If `mapST.get(S[i]) != T[i]`, return `false`.
  - If `mapTS.get(T[i]) != S[i]`, return `false`.
  - Put both mappings: `mapST.put(S[i], T[i])` and `mapTS.put(T[i], S[i])`.

### 2.3 Technique 2: Last-Seen Index Arrays ($O(N)$ Time, $O(1)$ Auxiliary Space - OPTIMAL)
Instead of storing character-to-character maps, store the **Last Seen Position Index** of characters in $S$ and $T$:
* Maintain two arrays: `int[] lastSeenS = new int[256]` and `int[] lastSeenT = new int[256]`.
* At index $i$ (1-indexed position $i + 1$ to avoid 0 default initialization conflicts):
  - If `lastSeenS[S[i]] != lastSeenT[T[i]]`, return `false`!
  - Update `lastSeenS[S[i]] = i + 1` and `lastSeenT[T[i]] = i + 1`.

```
Last-Seen Index Comparison Trace for "egg" vs "add":
i=0: S['e']=0, T['a']=0 (Equal!). Set lastSeenS['e']=1, lastSeenT['a']=1.
i=1: S['g']=0, T['d']=0 (Equal!). Set lastSeenS['g']=2, lastSeenT['d']=2.
i=2: S['g']=2, T['d']=2 (Equal!). Set lastSeenS['g']=3, lastSeenT['d']=3.
Result: ISOMORPHIC! ✅

Trace for "foo" vs "bar":
i=0: S['f']=0, T['b']=0 (Equal!). Set lastSeenS['f']=1, lastSeenT['b']=1.
i=1: S['o']=0, T['a']=0 (Equal!). Set lastSeenS['o']=2, lastSeenT['a']=2.
i=2: S['o']=2, T['r']=0 (MISMATCH! 2 != 0).
Result: NOT ISOMORPHIC! ❌
```

> **Memory Trick:** **"Isomorphic = Bijective (Both Ways)! Use lastSeenS[s[i]] == lastSeenT[t[i]] for O(N) O(1)-Space verification!"**

---

## 3. Characteristics & Problem Variants

### 3.1 Word Pattern Matching (LeetCode 290)
Given a pattern string `pattern` (e.g. `"abba"`) and a space-delimited string `s` (e.g. `"dog cat cat dog"`):
* Split `s` into words array `String[] words = s.split(" ")`.
* If `pattern.length() != words.length`, return `false`.
* Apply bijective mapping between characters in `pattern` and strings in `words`:
  - `mapCharToWord<Character, String>`
  - `mapWordToChar<String, Character>`

```
Isomorphic Mapping Variants Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Source Domain     | Target Domain     | Best Technique    |
+-----------------------+-------------------+-------------------+-------------------+
| Isomorphic Strings(205)| Character        | Character         | `int[256]` Arrays |
| Word Pattern (290)    | Character        | String Word       | Dual Hash Maps    |
| Pattern Matching      | String Key       | String Value      | Dual Hash Maps    |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Word Pattern (LeetCode 290) on `pattern = "abba", s = "dog cat cat dog"`:

```
Words Array: ["dog", "cat", "cat", "dog"]
Length check: 4 == 4 (OK)

i=0: char='a', word="dog"
     mapCharToWord: {'a' -> "dog"}
     mapWordToChar: {"dog" -> 'a'}

i=1: char='b', word="cat"
     mapCharToWord: {'a'->"dog", 'b'->"cat"}
     mapWordToChar: {"dog"->'a', "cat"->'b'}

i=2: char='b', word="cat"
     mapCharToWord.get('b') == "cat" (Matches!)
     mapWordToChar.get("cat") == 'b' (Matches!)

i=3: char='a', word="dog"
     mapCharToWord.get('a') == "dog" (Matches!)
     mapWordToChar.get("dog") == 'a' (Matches!)

Result: MATCHES PATTERN! ✅
```

---

## 5. Visual Diagram
Bijective Mapping Validation Topology:

```
   Pattern String:    "a"      "b"      "b"      "a"
                       |        |        |        |
    Mapping Map:       v        v        v        v
   Words List:       "dog"    "cat"    "cat"    "dog"
                       ^        ^        ^        ^
                       |        |        |        |
    Reverse Map:      "a"      "b"      "b"      "a"

Both Forward (Char -> Word) and Reverse (Word -> Char) must match at all positions!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Isomorphic Strings (LeetCode 205) and Word Pattern (LeetCode 290):

```java
import java.util.*;

public class IsomorphicMappingMaster {

    // 1. Isomorphic Strings using Last-Seen Arrays O(N) Time, O(1) Space - OPTIMAL
    public static boolean isIsomorphicArray(String s, String t) {
        if (s == null || t == null || s.length() != t.length()) return false;

        int[] lastSeenS = new int[256];
        int[] lastSeenT = new int[256];

        for (int i = 0; i < s.length(); i++) {
            char charS = s.charAt(i);
            char charT = t.charAt(i);

            // Store 1-based index (i + 1) to distinguish from default 0 initialization
            if (lastSeenS[charS] != lastSeenT[charT]) {
                return false;
            }

            lastSeenS[charS] = i + 1;
            lastSeenT[charT] = i + 1;
        }

        return true;
    }

    // 2. Isomorphic Strings using Dual Hash Maps O(N) Time, O(N) Space
    public static boolean isIsomorphicMaps(String s, String t) {
        if (s.length() != t.length()) return false;

        Map<Character, Character> mapST = new HashMap<>();
        Map<Character, Character> mapTS = new HashMap<>();

        for (int i = 0; i < s.length(); i++) {
            char cS = s.charAt(i);
            char cT = t.charAt(i);

            if (mapST.containsKey(cS) && mapST.get(cS) != cT) {
                return false;
            }
            if (mapTS.containsKey(cT) && mapTS.get(cT) != cS) {
                return false;
            }

            mapST.put(cS, cT);
            mapTS.put(cT, cS);
        }

        return true;
    }

    // 3. Word Pattern (LeetCode 290) O(N) Time, O(N) Space
    public static boolean wordPattern(String pattern, String s) {
        String[] words = s.split(" ");
        if (pattern.length() != words.length) return false;

        Map<Character, String> charToWord = new HashMap<>();
        Map<String, Character> wordToChar = new HashMap<>();

        for (int i = 0; i < pattern.length(); i++) {
            char c = pattern.charAt(i);
            String word = words[i];

            if (charToWord.containsKey(c) && !charToWord.get(c).equals(word)) {
                return false;
            }
            if (wordToChar.containsKey(word) && wordToChar.get(word) != c) {
                return false;
            }

            charToWord.put(c, word);
            wordToChar.put(word, c);
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// 1-Based Last-Seen Index Match Check
if (lastSeenS[s.charAt(i)] != lastSeenT[t.charAt(i)]) return false;
lastSeenS[s.charAt(i)] = i + 1;
lastSeenT[t.charAt(i)] = i + 1;
```

---

## 7. Concrete Problem Examples
* **LeetCode 205 - Isomorphic Strings**: Checking character bijectivity.
* **LeetCode 290 - Word Pattern**: Checking character-to-word bijectivity.
* **LeetCode 890 - Find and Replace Pattern**: Matching string lists against pattern.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Isomorphic String and Word Pattern matching algorithms:

```java
public class IsomorphicMappingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Isomorphic Strings ===");
        System.out.println("'egg' & 'add': " + IsomorphicMappingMaster.isIsomorphicArray("egg", "add")); // true
        System.out.println("'foo' & 'bar': " + IsomorphicMappingMaster.isIsomorphicArray("foo", "bar")); // false
        System.out.println("'paper' & 'title': " + IsomorphicMappingMaster.isIsomorphicArray("paper", "title")); // true
        System.out.println("'badc' & 'baba': " + IsomorphicMappingMaster.isIsomorphicArray("badc", "baba")); // false

        System.out.println("\n=== 2. Testing Word Pattern ===");
        System.out.println("'abba' & 'dog cat cat dog': " + IsomorphicMappingMaster.wordPattern("abba", "dog cat cat dog")); // true
        System.out.println("'abba' & 'dog cat cat fish': " + IsomorphicMappingMaster.wordPattern("abba", "dog cat cat fish")); // false
        System.out.println("'aaaa' & 'dog cat cat dog': " + IsomorphicMappingMaster.wordPattern("aaaa", "dog cat cat dog")); // false
    }
}
```

---

## 9. Complexity Analysis

| Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Last-Seen Array (`int[256]`)**| **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Direct 256 ASCII indexing |
| **Dual Hash Maps** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Maps both directions $S \leftrightarrow T$ |
| **Single Map + Set (`containsValue`)**| $O(N \cdot |\Sigma|)$ | $O(N)$ Space | `containsValue()` is $O(N)$ scan! |

---

## 10. Edge Cases & Boundary Handling
* **String Length Mismatch**: If `s.length() != t.length()`, return `false` immediately.
* **1-Based Indexing for Last-Seen Arrays**: `int[]` defaults to 0. If we stored 0-based index `i`, index 0 (`i = 0`) would be indistinguishable from unvisited character default `0`! Storing `i + 1` resolves this cleanly.
* **Extended ASCII / Unicode Characters**: For full ASCII, use `int[256]`. For Unicode, fallback to Dual Hash Maps.

---

## 11. Common Mistakes & Anti-Patterns
* **Using a Single Map ($S \to T$) without Reverse Validation**:
  For `s = "badc", t = "baba"`:
  - `'b' \to 'b'`, `'a' \to 'a'`, `'d' \to 'b'` (Single map allows `'d' \to 'b'` because `'d'` was unmapped!).
  - Result: Incorrectly reports `true`! Dual mapping catches `'b'` already mapped to `'b'` when `'d'` tries to claim it.
* **Using `map.containsValue()` in Single Map**: `containsValue()` takes $O(N)$ linear scan time, degrading total algorithm complexity to $O(N^2)$! Use Dual Hash Maps for $O(1)$ lookups.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Dual Maps are Mandatory for Bijective Checks:
> A single map checks only **Injectivity ($S \to T$)**.
> To prevent two distinct source keys mapping to the same target value, you must check **Surjectivity ($T \to S$)**.
> Dual Hash Maps or Dual Last-Seen Arrays provide **Strict Bijective Validation** in $O(1)$ time per character!

> **Memory Trick:** **"Single map causes overlap bugs! Dual maps or dual lastSeen arrays enforce bijectivity!"**

---

## 13. System & Implementation Comparisons

| Feature | Single Map + `containsValue()` | Dual Hash Maps | Dual `int[256]` Arrays |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(N^2)$ (Slow scan!) | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Space** | $O(N)$ | $O(N)$ | **$O(1)$ Constant ⚡** |
| **Character Set** | Any Object | Any Object | Bounded ASCII (256) |

---

## 14. How to Recognize This in Questions
* **"Determine if characters in S can be replaced to form T preserving order"** $\rightarrow$ Isomorphic Strings (`lastSeenS[s[i]] == lastSeenT[t[i]]`).
* **"Check if string follows pattern 'abba'"** $\rightarrow$ Word Pattern Dual Map.

---

## 15. Frequently Asked Interview Questions
* **Q: Why do we store `i + 1` instead of `i` in the `lastSeen` array?**  
  *A:* In Java, `int[]` arrays are initialized with `0`. If we stored 0-based index `i = 0`, `lastSeen['a'] = 0` would be identical to an unvisited character's default value `0`, causing false index mismatch errors on the first character.
* **Q: Why does `isIsomorphic("badc", "baba")` fail with a single map?**  
  *A:* Because `'b' \to 'b'` and `'a' \to 'a'`. When processing `'d'`, a single forward map sees `'d'` is unmapped and maps `'d' \to 'b'`, causing both `'b'` and `'d'` to map to `'b'`. Dual mapping checks reverse map `mapTS.containsKey('b')`, catching the conflict.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ISOMORPHIC STRINGS & BIJECTIVE MAPPING                |
+-----------------------------------------------------------------------+
| • Bijective Rule: 1-to-1 mapping in BOTH directions (S <-> T)         |
| • Optimal Array Method: int[] sSeen = new int[256], tSeen = new int[256]|
| • Match Check: if (sSeen[s.charAt(i)] != tSeen[t.charAt(i)]) return false;|
| • Update Step: sSeen[s.charAt(i)] = i + 1; tSeen[t.charAt(i)] = i + 1;|
| • Word Pattern (290): Dual HashMaps (charToWord & wordToChar)         |
| • Avoid Anti-Pattern: Never use map.containsValue() -> O(N²) Slow!    |
| • Complexity: O(N) Linear Time | O(1) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the 1-based `lastSeenS[s[i]] == lastSeenT[t[i]]` check.
- [ ] I know why `i + 1` is stored instead of `i` in primitive arrays.
- [ ] I can explain why single-map approaches fail on `"badc"` vs `"baba"`.
- [ ] I can solve Word Pattern (LeetCode 290) using dual maps.
- [ ] I know why `containsValue()` degrades time complexity to $O(N^2)$.
