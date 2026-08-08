# 16. Master Reference — Strings

## 1. Introduction
This Master Reference consolidates all core principles, memory architecture details, character encoding arithmetic, pattern matching algorithms, and Java syntax templates for **Chapter 5: Strings**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh ASCII math offsets, String Constant Pool rules, KMP/Z-Algorithm formulas, and sliding window patterns.

## 2. Core Concepts & Formulas Cheat Sheet
* **ASCII Offsets**: `'0'`=48, `'A'`=65, `'a'`=97 $\implies$ `ch - '0'` (digit val), `ch - 'a'` (lowercase index 0..25).
* **Bitwise Case Conversion**: `ch | 32` (lowercase), `ch & ~32` (uppercase), `ch ^ 32` (toggle case).
* **Polynomial Rolling Hash**: $\text{Hash}(S) = (S[0] \cdot B^{M-1} + \dots + S[M-1]) \pmod{MOD}$
* **Rabin-Karp Roll Update**: $\text{newHash} = ((\text{oldHash} - T[i] \cdot B^{M-1}) \cdot B + T[i+M]) \pmod{MOD}$
* **KMP Jump Rule**: On mismatch at $P[j]$, if $j > 0$ set **`j = lps[j - 1]`** else `i++`.
* **Z-Algorithm Concatenation**: **`S = P + "$" + T`** (Match when `Z[i] == P.length()`).
* **Expand Around Center Valid Length**: **`validLen = right - left - 1`**; Start index: **`start = i - (len - 1) / 2`**.
* **Manacher's Transformed String**: `"aba"` $\to$ `"^#a#b#a#$"` | Mirror Index: **`i_mirror = 2 * C - i`**.
* **Sliding Window Jump**: `if (lastSeen[ch] >= left) left = lastSeen[ch] + 1`.

> **Memory Trick:** **"KMP: j = lps[j - 1]; Z-Algorithm: Z[i] == M; Manacher: i_mirror = 2*C - i"**.

## 3. Master String Algorithm Complexity Table
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Triggers / Use Case |
| :--- | :--- | :--- | :--- |
| **`s.charAt(i)` / `s.length()`**| $O(1)$ | $O(1)$ | Direct character lookup |
| **`s.substring(l, r)`** | $O(r - l)$ | $O(r - l)$ | Substring range copy (JDK 7+) |
| **`StringBuilder.append()`** | **Amortized $O(1)$**| $O(1)$ | Dynamic string construction |
| **`s.hashCode()`** | $O(N)$ 1st call | **$O(1)$ Cached** | Cached `hash` field optimization |
| **Naive Substring Search** | $O(N \cdot M)$ worst | $O(1)$ | Dual-pointer search `i <= N - M` |
| **KMP Algorithm** | **$O(N + M)$** | $O(M)$ | Guaranteed linear pattern search |
| **Rabin-Karp Algorithm** | **$O(N + M)$ avg** | $O(1)$ | Multi-pattern search & rolling hash |
| **Z-Algorithm** | **$O(N + M)$** | $O(N + M)$ | Exact prefix match via `P + "$" + T` |
| **Expand Around Center** | $O(N^2)$ | **$O(1)$ Constant** | Longest Palindromic Substring |
| **Manacher's Algorithm** | **$O(N)$ Linear** | $O(N)$ | $O(N)$ Longest Palindromic Substring |
| **Canonical Anagram Key** | **$O(N \cdot K)$** | $O(N \cdot K)$ Map | Group Anagrams (`#cnt0#cnt1...`) |
| **Edit Distance (2D DP)** | $O(M \cdot N)$ | $O(\min(M,N))$ | Min insertions, deletions, replaces |
| **One Edit Distance** | **$O(N)$ Linear** | **$O(1)$ Constant** | Two pointers (LeetCode 161) |
| **Trie Search / StartsWith** | **$O(L)$** | $O(L \cdot 26)$ | Prefix tree lookups & auto-complete |
| **Basic Calculator II** | **$O(N)$ Linear** | $O(N)$ Stack | Expression parsing via `ArrayDeque` |
| **Sliding Window No Repeats**| **$O(N)$ Linear** | **$O(1)$ Space** | `lastSeen[256]` pointer jumps |

## 4. Hardware & Memory Footprint Summary
```
+-----------------------------------------------------------------------------------+
| String Architecture Element | Memory Footprint & Details                          |
+-----------------------------------------------------------------------------------+
| JDK 9+ Compact Strings      | Stores LATIN1 as byte[] (1B/char), UTF-16 as 2B/char|
| Object Header (64-bit JVM)  | 24 Bytes Base Header (Mark Word + Klass Word + len) |
| HashCode Field              | 4 Bytes (Calculated on 1st call O(N), cached for O(1))|
| StringBuilder Buffer        | Dynamic byte[] array (Doubles capacity when full)   |
+-----------------------------------------------------------------------------------+
```

## 5. Java Code Templates & Snippets

> **Quick Syntax:**
```java
// 1. Clean Word Split
String[] words = s.trim().split("\\s+");

// 2. Anagram Group Key
StringBuilder sb = new StringBuilder();
for (int count : freq) sb.append('#').append(count);
String key = sb.toString();

// 3. Trie Search vs StartsWith
boolean isExactWord = (curr != null && curr.isEndOfWord);
boolean isPrefix    = (curr != null);

// 4. Expression Parsing Stack
Deque<Integer> stack = new ArrayDeque<>();

// 5. Sliding Window Jump
if (lastSeen[ch] >= left) left = lastSeen[ch] + 1;
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: String Immutability in Loops**: `s += "a"` inside a loop takes $O(N^2)$ time! Use `StringBuilder`.
* **Trap 2: `s == t` vs `s.equals(t)`**: `==` checks RAM reference address; `.equals()` checks character values.
* **Trap 3: Outer Loop Limit in Substring Search**: Outer loop MUST iterate up to `i <= N - M`.
* **Trap 4: Missing Delimiters in Anagram Keys**: `[1,0,11]` $\to$ `"1011"` collides with `[10,1,1]` $\to$ `"1011"`. Use `#1#0#11`.
* **Trap 5: One Edit Distance DP Trap**: Do NOT use 2D DP for One Edit Distance! Use Two Pointers in $O(N)$ time and $O(1)$ space.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 5 (STRINGS)                      |
+-----------------------------------------------------------------------+
| 1. Compact Strings (JDK 9+): byte[] array (1B/char LATIN1 vs 2B UTF16)|
| 2. HashCode: Computed 1st call O(N), cached field for O(1) lookups   |
| 3. KMP: Text pointer i never moves back! Mismatch -> j = lps[j - 1]   |
| 4. Rabin-Karp: Rolling hash ((oldHash - outChar*power)%MOD + MOD)%MOD|
| 5. Z-Algorithm: P + "$" + T -> Match when Z[i] == pattern.length()     |
| 6. Palindrome Expand: len = right - left - 1; start = i - (len-1)/2   |
| 7. Manacher: ^#a#b#a#$, i_mirror = 2*C - i, P[i] = min(R - i, P[mirror])|
| 8. Trie: Search checks isEndOfWord; StartsWith checks node != null    |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write `StringBuilder` loops and explain why `str += "a"` is $O(N^2)$.
- [ ] I can write KMP `buildLPS` and `kmpSearch` in under 5 minutes.
- [ ] I can write Z-Algorithm search using `P + "$" + T`.
- [ ] I can implement Expand Around Center and Manacher's Algorithm.
- [ ] I can implement Trie (`insert`, `search`, `startsWith`) and Basic Calculator II.
