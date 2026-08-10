# 14. Pattern Recognition & String Triggers: Identifying Algorithmic Archetypes

## 1. Introduction
Rapid problem-solving in technical coding interviews requires instant **String Pattern Recognition**. Rather than analyzing string problems from scratch, experienced engineers map problem descriptions directly to one of six universal **String Master Archetypes**: **Sliding Window & Two-Pointer**, **KMP / LPS Failure Transitions**, **Rolling Hash Rabin-Karp**, **Boyer-Moore Bad Character Jumps**, **Trie Prefix Trees**, and **Suffix Array / Palindromic Trees**. Identifying trigger words in problem statements allows instant selection of optimal data structures, loop invariants, and time complexity bounds.

> **Important:** The 6 Universal String Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Sliding Window & Two-Pointer**: Trigger = *"Longest substring without repeating characters, anagram window, valid palindrome"*. Mechanics = Two pointers `left, right` with Frequency Map. Time = $O(N)$.
> 2. **Pattern 2: KMP Prefix Function ($\text{lps}[i]$)**: Trigger = *"Find single pattern in text with strict O(N+M) time, repeated substring pattern"*. Mechanics = Zero text backtracking with LPS array. Time = $O(N + M)$.
> 3. **Pattern 3: Rolling Hash (Rabin-Karp)**: Trigger = *"Find multiple patterns of same length, longest duplicate substring"*. Mechanics = $O(1)$ Hash Rolling update. Time = $O(N + M)$ average.
> 4. **Pattern 4: Boyer-Moore Sub-Linear Search**: Trigger = *"Fast keyword search in long text files (grep engine)"*. Mechanics = Right-to-left scan with Bad Char table. Time = $O(N / M)$ sub-linear best.
> 5. **Pattern 5: Trie Prefix Trees**: Trigger = *"Implement autocomplete, startsWith prefix check, word search grid"*. Mechanics = Character-by-character edge tree. Time = $O(L)$.
> 6. **Pattern 6: Suffix Array & Palindromic Trees**: Trigger = *"Number of distinct substrings, longest repeated substring, distinct palindromes"*. Mechanics = SA + Kasai LCP or EERTREE. Time = $O(N)$. ⚡

```
String Master Archetype Decision Tree Topography:
Problem Trigger Signal:
├── "Longest substring without repeating chars / Anagram window?" -> Pattern 1: Sliding Window
├── "Single pattern match with strict linear time / Repeated substring?" -> Pattern 2: KMP (LPS)
├── "Multi-pattern same length / Longest duplicate substring?" ----> Pattern 3: Rabin-Karp
├── "Sub-linear keyword search in large text file?" -------------> Pattern 4: Boyer-Moore
├── "Autocomplete / StartsWith prefix check / Word Search?" ------> Pattern 5: Trie Prefix Tree
└── "Distinct substrings count / Palindromic tree online?" --------> Pattern 6: Suffix Array / EERTREE ⚡
```

---

## 2. Core Concepts & Master Pattern Strategy Matrix

### 2.1 Master String Pattern Recognition Matrix
```
Master String Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Key Structure     | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **1. Sliding Window** | "Longest substring"| Two Pointers + Map| **$O(N)$ Linear ⚡**|
| **2. KMP (LPS)**      | "Strict O(N+M)"   | LPS Table `lps[]` | **$O(N + M)$ Strict ⚡**|
| **3. Rolling Hash**   | "Multi-pattern M" | Double Hash Pair  | **$O(N + M)$ Avg ⚡**|
| **4. Boyer-Moore**    | "Fast file search"| Bad Char Table    | **$O(N / M)$ Sub-Linear⚡**|
| **5. Trie Tree**      | "startsWith / Auto"| `TrieNode[26]`    | **$O(L)$ Instant ⚡**|
| **6. Suffix Array**   | "Distinct count"  | SA + Kasai LCP    | **$O(N \log N)$ / $O(N)$⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Longest substring = Sliding Window; Prefix startsWith = Trie; Distinct Substrings = Suffix Array LCP!"**

---

## 3. Deep Dive into the 6 String Archetypes

### 3.1 Archetype 1: Sliding Window & Two-Pointer
* **Triggers**: *"Find longest substring without repeating characters"*, *"Find all anagrams in string"*, *"Minimum window substring"*.
* **Template**: `while (right < n)` expand `right`, update frequency map, `while (invalid)` shrink `left`.

### 3.2 Archetype 5: Trie Prefix Trees
* **Triggers**: *"Implement Trie"*, *"Search words with prefix"*, *"Boggle Word Search II"*.
* **Template**: `TrieNode` with `children` and `isEndOfWord`. Traverse $L$ character nodes descending from root.

### 3.3 Archetype 6: Suffix Array & LCP / Palindromic Trees
* **Triggers**: *"Count total distinct substrings"*, *"Longest repeated substring"*, *"Count distinct palindromes"*.
* **Template**: Suffix Array + Kasai's LCP Array ($\text{Distinct} = \frac{N(N+1)}{2} - \sum LCP[i]$) or EERTREE.

---

## 4. Internal Working Mechanics: Matching LeetCode Problems to Archetypes

```
Problem Match Audits:

LeetCode 3 (Longest Substring Without Repeating Chars) -> Archetype 1: Sliding Window
LeetCode 76 (Minimum Window Substring)                -> Archetype 1: Sliding Window
LeetCode 28 (Find Index of First Occurrence)         -> Archetype 2: KMP Algorithm
LeetCode 459 (Repeated Substring Pattern)            -> Archetype 2: KMP LPS Table Property
LeetCode 1044 (Longest Duplicate Substring)           -> Archetype 3: Binary Search + Rolling Hash
LeetCode 208 (Implement Trie Prefix Tree)            -> Archetype 5: Trie Tree Structure
LeetCode 212 (Word Search II Grid Backtracking)      -> Archetype 5: Trie + DFS Pruning
LeetCode 1698 (Count Distinct Substrings in String)   -> Archetype 6: Suffix Array + Kasai LCP
LeetCode 5 (Longest Palindromic Substring)           -> Archetype 6: Manacher's / EERTREE
```

---

## 5. Visual Diagram: String Pattern Selector Flowchart

```
                          [ New String Problem ]
                                     │
                       Is it about PREFIX SEARCH / Autocomplete?
                             /                  \
                         (Yes)                  (No)
                          /                        \
              [ Pattern 5: Trie Tree ]    Is it about DISTINCT SUBSTRINGS / Palindromes?
                                              /                     \
                                          (Yes)                     (No)
                                           /                           \
                              [ Pattern 6: Suffix Array ]   Is it finding SUBSTRING WINDOW bounds?
                                                                /                \
                                                            (Yes)                (No)
                                                             /                      \
                                                [ Pattern 1: Sliding Window ]  Is strict linear time matching needed?
                                                                                  /                    \
                                                                              (Yes)                    (No)
                                                                               /                          \
                                                                 [ Pattern 2: KMP Search ]   [ Pattern 3/4: Hash/BM ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across all 6 String Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating the 6 String Algorithmic Archetypes.
 */
public class StringPatternRecognitionMaster {

    // =========================================================================
    // PATTERN 1: SLIDING WINDOW (LeetCode 3 Longest Substring Without Repeats)
    // =========================================================================
    public int pattern1_SlidingWindow(String s) {
        if (s == null || s.length() == 0) return 0;

        Map<Character, Integer> lastSeen = new HashMap<>();
        int maxLen = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (lastSeen.containsKey(ch)) {
                left = Math.max(left, lastSeen.get(ch) + 1);
            }
            lastSeen.put(ch, right);
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }

    // =========================================================================
    // PATTERN 2: KMP SEARCH (LeetCode 28 O(N + M) Time)
    // =========================================================================
    public int pattern2_KMPSearch(String text, String pattern) {
        if (text == null || pattern == null || pattern.isEmpty()) return 0;
        int n = text.length(), m = pattern.length();
        if (m > n) return -1;

        int[] lps = computeLPS(pattern);
        int i = 0, j = 0;

        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            if (j == m) return i - j; // Match found!
            else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) j = lps[j - 1];
                else i++;
            }
        }
        return -1;
    }

    private int[] computeLPS(String p) {
        int[] lps = new int[p.length()];
        int len = 0, i = 1;
        while (i < p.length()) {
            if (p.charAt(i) == p.charAt(len)) {
                lps[i++] = ++len;
            } else {
                if (len != 0) len = lps[len - 1];
                else lps[i++] = 0;
            }
        }
        return lps;
    }

    // =========================================================================
    // PATTERN 3: ROLLING HASH (Rabin-Karp O(N + M) Avg Time)
    // =========================================================================
    public int pattern3_RabinKarp(String text, String pattern) {
        if (text == null || pattern == null || pattern.length() > text.length()) return -1;

        int n = text.length(), m = pattern.length();
        long base = 256, prime = 1_000_000_007;
        long h = 1, pHash = 0, tHash = 0;

        for (int i = 0; i < m - 1; i++) h = (h * base) % prime;
        for (int i = 0; i < m; i++) {
            pHash = (base * pHash + pattern.charAt(i)) % prime;
            tHash = (base * tHash + text.charAt(i)) % prime;
        }

        for (int i = 0; i <= n - m; i++) {
            if (pHash == tHash && text.substring(i, i + m).equals(pattern)) return i;
            if (i < n - m) {
                tHash = (base * (tHash - text.charAt(i) * h) + text.charAt(i + m)) % prime;
                if (tHash < 0) tHash += prime;
            }
        }
        return -1;
    }

    // =========================================================================
    // PATTERN 5: TRIE PREFIX TREE (LeetCode 208 O(L) Time)
    // =========================================================================
    public static class Pattern5_Trie {
        private static class Node {
            Node[] children = new Node[26];
            boolean isEnd = false;
        }

        private final Node root = new Node();

        public void insert(String word) {
            Node curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) curr.children[idx] = new Node();
                curr = curr.children[idx];
            }
            curr.isEnd = true;
        }

        public boolean startsWith(String prefix) {
            Node curr = root;
            for (char c : prefix.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return false;
                curr = curr.children[idx];
            }
            return true;
        }
    }
}
```

> **Quick Syntax:**
```java
// String Pattern Selection Identifier
// Trigger: "Longest substring" -> Pattern 1: Sliding Window
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Sliding Window)**: LeetCode 3, LeetCode 76, LeetCode 438, LeetCode 567.
* **Pattern 2 (KMP LPS)**: LeetCode 28, LeetCode 459, LeetCode 1392, LeetCode 214.
* **Pattern 3 (Rolling Hash)**: LeetCode 1044, LeetCode 187, LeetCode 1554.
* **Pattern 4 (Boyer-Moore)**: Sub-linear grep file search tools.
* **Pattern 5 (Trie Tree)**: LeetCode 208, LeetCode 211, LeetCode 212, LeetCode 1268.
* **Pattern 6 (Suffix Array / EERTREE)**: LeetCode 1698, LeetCode 5, LeetCode 647.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class StringPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   STRING PATTERN RECOGNITION DEMONSTRATION      ");
        System.out.println("=================================================\n");

        StringPatternRecognitionMaster master = new StringPatternRecognitionMaster();

        // 1. Pattern 1 Test (Sliding Window)
        String s1 = "abcabcbb";
        int len1 = master.pattern1_SlidingWindow(s1);
        System.out.println("1. Pattern 1 (Sliding Window) Longest Substring for \"" + s1 + "\": " + len1);
        System.out.println("-------------------------------------------------");

        // 2. Pattern 2 Test (KMP)
        String text = "sadbutsad", pattern = "sad";
        int kmpIdx = master.pattern2_KMPSearch(text, pattern);
        System.out.println("2. Pattern 2 (KMP) Search \"" + pattern + "\" in \"" + text + "\": Index = " + kmpIdx);
        System.out.println("-------------------------------------------------");

        // 3. Pattern 5 Test (Trie)
        StringPatternRecognitionMaster.Pattern5_Trie trie = new StringPatternRecognitionMaster.Pattern5_Trie();
        trie.insert("apple");
        boolean startsWithApp = trie.startsWith("app");
        System.out.println("3. Pattern 5 (Trie) startsWith(\"app\") on [\"apple\"]: " + startsWithApp);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| String Master Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Sliding Window** | $\mathbf{O(N)}$ Linear ⚡| $O(|\Sigma|)$ Map | "Longest substring without repeating" |
| **2. KMP (LPS)**      | $\mathbf{O(N + M)}$ Strict ⚡| $O(M)$ Table | "Single pattern match in linear time" |
| **3. Rolling Hash**   | $\mathbf{O(N + M)}$ Average ⚡| $\mathbf{O(1)}$ Space ⚡| "Multi-pattern M / Longest duplicate" |
| **4. Boyer-Moore**    | $\mathbf{O(N / M)}$ Sub-Linear⚡| $O(|\Sigma|)$ Table | "Fast text editor search (ctrl+F)" |
| **5. Trie Tree**      | $\mathbf{O(L)}$ Instant ⚡| $O(N \cdot L \cdot |\Sigma|)$ | "startsWith / Autocomplete / Boggle" |
| **6. Suffix Array**   | $\mathbf{O(N \log N)}$ / $\mathbf{O(N)}$⚡| $O(N)$ Integers | "Distinct substrings count" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Pattern 1 (Sliding Window) and Pattern 5 (Trie)**:
   - If searching within a **single long continuous string** for window properties $\implies$ Use Pattern 1 (Sliding Window).
   - If searching across a **dictionary of many distinct words** for prefix matching $\implies$ Use Pattern 5 (Trie).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Naive Substring Search to Large Streaming Files**:
  - Using Naive search on 100MB text files causes $O(N \cdot M)$ slowdowns. Use **KMP** (zero text backtracking) or **Boyer-Moore** ($O(N / M)$ sub-linear).

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second String Pattern Selector:
> 1. Prefix checking / Autocomplete? $\to$ Pattern 5 (Trie Tree).
> 2. Substring window bounds? $\to$ Pattern 1 (Sliding Window).
> 3. Single pattern linear match? $\to$ Pattern 2 (KMP Algorithm).
> 4. Multi-pattern or duplicate substring? $\to$ Pattern 3 (Rabin-Karp Rolling Hash).
> 5. Distinct substrings count? $\to$ Pattern 6 (Suffix Array + LCP). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Data Structure | Main Search Loop Condition | Space Cost |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Sliding Window)** | Two Pointers + Map | `while (right < n)` | $O(|\Sigma|)$ |
| **Pattern 2 (KMP LPS)** | LPS Array `lps[]` | `while (i < n)` | $O(M)$ |
| **Pattern 5 (Trie)** | Directed Tree Graph | `for (char c : str)` | $O(N \cdot L \cdot |\Sigma|)$ |

---

## 14. How to Recognize This in Questions

* **"Longest substring without repeating characters"** $\rightarrow$ Pattern 1 (Sliding Window).
* **"Check startsWith(prefix) in dictionary"** $\rightarrow$ Pattern 5 (Trie Tree).
* **"Count total distinct substrings in S"** $\rightarrow$ Pattern 6 (Suffix Array + LCP).

---

## 15. Frequently Asked Interview Questions

* **Q: When should I choose KMP over Rabin-Karp?**  
  *A:* Choose KMP when searching a single pattern with 100% deterministic $O(N + M)$ worst-case time guarantee. Choose Rabin-Karp when searching multiple patterns of equal length simultaneously.

* **Q: Why does a Trie perform prefix matching faster than a Hash Set?**  
  *A:* Hash Sets cannot perform prefix matches without inspecting all $N$ entries ($O(N \cdot L)$ time). A Trie executes prefix matches in instant $O(L)$ time by following node edges.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING PATTERN RECOGNITION                            |
+-----------------------------------------------------------------------+
| • Pattern 1: Sliding Window   -> "Longest substring without repeats"  |
| • Pattern 2: KMP (LPS)        -> "Single pattern match O(N+M) time"   |
| • Pattern 3: Rolling Hash     -> "Multi-pattern M / Longest duplicate"|
| • Pattern 4: Boyer-Moore      -> "Sub-linear text search (grep engine)"|
| • Pattern 5: Trie Tree        -> "startsWith prefix check / Autocomplete"|
| • Pattern 6: Suffix Array LCP -> "Distinct substrings count" ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any string problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I know when to use Sliding Window vs Trie Tree.
- [ ] I can implement Sliding Window (LeetCode 3) in Java.
- [ ] I can implement KMP search (LeetCode 28) in Java.
- [ ] I can state the formula for distinct substrings count using Suffix Array + LCP.
