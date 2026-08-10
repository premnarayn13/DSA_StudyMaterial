# 16. Master Reference — String Algorithms & Foundations

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 24: String Algorithms**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering String Representations & Memory Layouts, Naive Substring Matching, KMP Algorithm (LPS Table), Rabin-Karp Rolling Hash, Boyer-Moore (Bad Character Rule & Horspool), Z-Algorithm, Tries & Prefix Trees, Suffix Arrays & Kasai's LCP, Aho-Corasick Multi-Pattern Automaton, Manacher's Algorithm, Double String Hashing, Palindromic Trees (EERTREE), String Compression (RLE & Huffman Coding), String Pattern Recognition, and Suffix Automata (SAM).

> **Important:** Review this master reference 15 minutes before an interview to refresh the 6 String Master Archetypes, Java Compact Strings (`byte[] coder`), Horner's Base-31 Hash (`(h << 5) - h + c`), KMP zero text backtracking `j = lps[j-1]`, Rabin-Karp $O(1)$ rolling hash update, Boyer-Moore $O(N / M)$ sub-linear jumps, Kasai's LCP monotonic reduction ($k - 1$), EERTREE Dual Root Architecture (-1 and 0), Double Hash Moduli ($10^9+7$ and $10^9+9$), and Suffix Automaton $2N-1$ states bound!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Java Hash Code Polynomial Equation**:
  - $H(S) = \sum_{i=0}^{N-1} s_i \cdot 31^{N - 1 - i} = (h \ll 5) - h + s_i$.
* **Non-Empty Substring & Prefix/Suffix Count Theorem**:
  - Substrings $= \frac{N(N+1)}{2}, \quad \text{Prefixes} = N+1, \quad \text{Suffixes} = N+1$.
* **Naive Search Worst-Case Bound**:
  - $C_{\max} = (N - M + 1) \times M = \mathbf{O(N \cdot M) \text{ Quadratic Time}}$.
* **KMP LPS Failure Transition**:
  - `if (text.charAt(i) != pattern.charAt(j) && j > 0) j = lps[j - 1];` (Text pointer $i$ NEVER moves backward!).
* **Rabin-Karp $O(1)$ Rolling Hash Equation**:
  - $H_{i+1} = \left( B \cdot (H_i - T[i] \cdot h) + T[i + M] \right) \pmod Q$ where $h = B^{M-1} \pmod Q$.
* **Boyer-Moore Bad Character Shift**:
  - $\text{shift} = \max(1, j - \text{badChar}[T[s + j]])$. Sub-linear best case $= \mathbf{O(N / M) \text{ Time}}$.
* **Z-Array Re-use Condition**:
  - `if (z[k] < r - i + 1) z[i] = z[k];` (Reuses Z-box $[L, R]$ prefix match length).
* **Trie Prefix Search Complexity**:
  - Time $= \mathbf{O(L)}$ for Insert, Search, StartsWith. Space $= O(N \cdot L \cdot |\Sigma|)$.
* **Distinct Substrings Theorem (Suffix Array + LCP)**:
  - $\text{Distinct Substrings} = \frac{N(N+1)}{2} - \sum_{i=1}^{N-1} LCP[i]$.
* **Kasai's LCP Monotonic Reduction Lemma**:
  - $\text{LCP}(i + 1) \ge \text{LCP}(i) - 1 \implies \mathbf{O(N) \text{ Strict Linear Time}}$.
* **Aho-Corasick Multi-Pattern Search**:
  - Time $= \mathbf{O(N + \sum M_i + Z)}$ where $Z$ is total match occurrences.
* **Manacher's Palindrome Radius Re-use Rule**:
  - $P[i] = \min(R - i, P[2C - i])$ over transformed string `"^#c1#c2#...#cn#$"`.
* **Double Modulo Hashing Range Query**:
  - $\text{Hash}(L, R) = (pref[R + 1] - pref[L] \cdot pow[R - L + 1]) \pmod Q$ (Collision probability $< 10^{-18}$).
* **EERTREE Dual Root Distinct Theorem**:
  - $\text{Distinct Palindromes} = \text{Total Nodes Created} - 3$ (Roots $-1$ and $0$).
* **Shannon Information Entropy Theorem**:
  - $H(X) = -\sum p_i \log_2 p_i \text{ bits per char}$ (Minimum lossless compression limit).
* **Suffix Automaton (SAM) State Bound**:
  - At most $2N - 1$ states and $3N - 4$ transition edges.

```
Master String Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm / Structure | Best Case Time    | Worst Case Time   | Auxiliary Space   | Text Backtracking |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Naive Search**      | $O(N)$            | $O(N \cdot M)$ ❌ | **$O(1)$ In-Place⚡**| Resets $i \to i+1$|
| **KMP Algorithm**     | **$O(N + M)$ ⚡** | **$O(N + M)$ ⚡** | $O(M)$ Table      | **Zero Backtrack ⚡**|
| **Rabin-Karp**        | **$O(N + M)$ ⚡** | $O(N \cdot M)$    | **$O(1)$ In-Place⚡**| **Zero Backtrack ⚡**|
| **Boyer-Moore**       | **$O(N / M)$ ⚡** | $O(N \cdot M)$    | $O(M + |\Sigma|)$ | Right-to-Left Scan|
| **Z-Algorithm**       | **$O(N + M)$ ⚡** | **$O(N + M)$ ⚡** | $O(N + M)$ Array  | Linear Scan       |
| **Trie Prefix Tree**  | **$O(L)$ Instant ⚡**| **$O(L)$ Instant ⚡**| $O(N \cdot L \cdot 26)$| $O(L)$ Hops     |
| **Suffix Array + LCP**| **$O(N \log N)$ ⚡**| **$O(N \log N)$ ⚡**| $O(N)$ Integers   | $O(M \log N)$ BS  |
| **Aho-Corasick**      | **$O(N + Z)$ ⚡** | **$O(N + Z)$ ⚡** | $O(\sum M_i \cdot |\Sigma|)$| **Zero Backtrack ⚡**|
| **Manacher's Engine** | **$O(N)$ Strict ⚡**| **$O(N)$ Strict ⚡**| $O(N)$ Transformed| $O(N)$ Radius Array|
| **Double String Hash**| **$O(1)$ Range ⚡**| **$O(1)$ Range ⚡**| $O(N)$ Prefixes   | $O(1)$ Math Query |
| **Palindromic Tree**  | **$O(N)$ Online ⚡**| **$O(N)$ Online ⚡**| $O(N \cdot |\Sigma|)$| Dual Roots (-1, 0)|
| **Suffix Automaton**  | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| $O(N \cdot |\Sigma|)$| $2N-1$ States     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| String Algorithm / Structure | Purpose | Precomputation Time | Query / Search Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **String foundations** | Base representation | N/A | $O(1)$ `charAt`, $O(N)$ Hash | Compact `byte[]` | Latin-1 / UTF-16 |
| **Naive Search** | Baseline match | $O(0)$ | $O(N \cdot M)$ Worst | $\mathbf{O(1)}$ Memory ⚡| All offsets $N-M+1$ |
| **KMP Algorithm** | Single pattern match | $O(M)$ LPS Table | $\mathbf{O(N + M)}$ Strict ⚡| $O(M)$ Table | Zero text backtrack |
| **Rabin-Karp** | Multi-pattern match | $O(M)$ Hash | $\mathbf{O(N + M)}$ Average ⚡| $\mathbf{O(1)}$ Memory ⚡| $O(1)$ Rolling Hash |
| **Boyer-Moore** | Sub-linear file search | $O(M + |\Sigma|)$ | $\mathbf{O(N / M)}$ Sub-Linear⚡| $O(M + |\Sigma|)$ | Bad Char + Good Suffix |
| **Z-Algorithm** | Prefix match array | $O(0)$ | $\mathbf{O(N + M)}$ Strict ⚡| $O(N + M)$ Array | Z-Box $[L, R]$ Reuse |
| **Trie (Prefix Tree)** | Autocomplete / Prefix | $O(\sum M_i)$ | $\mathbf{O(L)}$ Instant ⚡| $O(N \cdot L \cdot 26)$ | Prefix tree edges |
| **Suffix Array + Kasai**| Distinct Substrings | $O(N \log N)$ | $O(M \log N)$ BS | $O(N)$ Integers | $\frac{N(N+1)}{2} - \sum LCP$ |
| **Aho-Corasick** | NIDS / Content Filter | $O(\sum M_i \cdot |\Sigma|)$ | $\mathbf{O(N + Z)}$ Strict ⚡| $O(\sum M_i \cdot |\Sigma|)$| Trie + BFS Fail Links |
| **Manacher's Engine** | Longest Palindrome | $O(N)$ Transform | $\mathbf{O(N)}$ Strict ⚡| $O(N)$ Transformed | Mirror $P[i']$ Re-use |
| **Double String Hash**| Substring Equality | $O(N)$ Prefixes | $\mathbf{O(1)}$ Instant ⚡| $O(N)$ Arrays | $< 10^{-18}$ Collision |
| **Palindromic Tree** | Online Palindromes | $O(0)$ | $\mathbf{O(N)}$ Online ⚡| $O(N \cdot |\Sigma|)$ | Dual Roots (-1, 0) |
| **Run-Length Encoding**| Repetitive Signals | N/A | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ In-Place ⚡| Contiguous runs |
| **Huffman Coding** | Lossless Text / PNG | $O(N \log |\Sigma|)$ | $\mathbf{O(N_{\text{bits}})}$ Linear⚡| $O(|\Sigma|)$ Tree | Prefix-free Min-Heap |
| **Duval's Factorization**| Minimal Rotation | $O(0)$ | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Pointers $i, j, k$ |
| **Suffix Automaton** | Substring DFA | $O(N)$ SAM Build | $\mathbf{O(L)}$ Instant ⚡| $O(N \cdot |\Sigma|)$ | $2N - 1$ States |

---

## 4. Architectural System & Library Audit
```
+-----------------------------------------------------------------------------------+
| Production System String Architectures                                            |
+-----------------------------------------------------------------------------------+
| JDK 9+ String Internals                        : Compact Strings (byte[] coder: Latin-1/UTF-16)|
| Network Intrusion Detection (Snort NIDS)        : Aho-Corasick Automaton Engine     |
| Text Editor / IDE Search (ctrl+F / GNU grep)   : Boyer-Moore / Horspool Engine     |
| File Compression (GZIP / PNG / ZIP)            : LZ77 + Huffman Prefix-Free Coding |
| Genomic Database Search (BLAST / GenBank)      : Suffix Array + Kasai's LCP Array  |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Java Base-31 Polynomial Hash Formula
> h = 31 * h + s.charAt(i); // Equivalent to (h << 5) - h + s.charAt(i)
> 
> // 2. KMP LPS Table Mismatch Fallback
> if (pattern.charAt(i) != pattern.charAt(len) && len != 0) len = lps[len - 1];
> 
> // 3. KMP Search Text Transition (Zero Text Backtracking)
> if (text.charAt(i) == pattern.charAt(j)) { i++; j++; } if (j == m) { matches.add(i - j); j = lps[j - 1]; } else if (i < n && text.charAt(i) != pattern.charAt(j)) { if (j != 0) j = lps[j - 1]; else i++; }
> 
> // 4. Rabin-Karp O(1) Rolling Hash Modulo Update
> textHash = (BASE * (textHash - text.charAt(i) * h) + text.charAt(i + m)) % PRIME; if (textHash < 0) textHash += PRIME;
> 
> // 5. Boyer-Moore Bad Character Shift
> int shift = Math.max(1, j - badChar[text.charAt(s + j)]); s += shift;
> 
> // 6. Z-Algorithm Box Re-use Condition
> if (z[k] < r - i + 1) z[i] = z[k]; else { l = i; while (r < n && s.charAt(r-l) == s.charAt(r)) r++; z[i] = r - l; r--; }
> 
> // 7. Kasai's LCP Monotonic Reduction
> lcp[rank[i]] = k; if (k > 0) k--;
> 
> // 8. Manacher's Mirror Radius Initialization
> int iMirror = 2 * c - i; if (i < r) p[i] = Math.min(r - i, p[iMirror]);
> 
> // 9. Double String Hash O(1) Query
> long h1 = (pref1[right + 1] - (pref1[left] * pow1[len]) % MOD1) % MOD1; if (h1 < 0) h1 += MOD1;
> 
> // 10. Duval's Minimal Rotation Candidate Skip
> if (charI > charJ) { i = Math.max(i + k + 1, j + 1); j = i + 1; k = 0; }
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: String Concatenation with `+` Inside Loops**: `s += ch` creates $O(N^2)$ temporary garbage objects. Always use **`StringBuilder`** ($O(N)$ total time).
* **Pitfall 2: Incrementing Text Pointer `i++` During KMP Fallback**: Incrementing $i$ during `j = lps[j-1]` fallback skips character comparisons. Text pointer $i$ MUST remain unchanged during fallback!
* **Pitfall 3: Single Modulus Hash Collisions**: Single prime hashing ($10^9+7$) has a $\sim 99\%$ collision rate over $N^2$ substring queries. Always use **Double Modulo Hashing** ($10^9+7$ and $10^9+9$).
* **Pitfall 4: Resetting $k = 0$ in LCP Computation**: Resetting $k = 0$ at every step degrades LCP computation to $O(N^2)$ quadratic time. Always use Kasai's $k - 1$ monotonic reduction bound!
* **Pitfall 5: Advancing `mid` Pointer on 2-Swap in Dutch National Flag**: Swapping `nums[mid]` with `nums[high]` brings an uninspected element from `high`. Keep `mid` unchanged (`high--`).
* **Pitfall 6: Forgetting Aho-Corasick Dictionary Output Links**: Omitting `dictionaryLink` misses short nested pattern matches (e.g. `"he"`) when a longer pattern (e.g. `"she"`) matches.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 24 (STRING ALGORITHMS)          |
+-----------------------------------------------------------------------+
| 1. Compact Strings: JDK 9+ uses byte[] coder (Latin-1 1B / UTF-16 2B) |
| 2. KMP Algorithm  : LPS table precomputation -> Zero text backtracking|
| 3. Rabin-Karp     : Rolling hash update in O(1) time (Multi-pattern) |
| 4. Boyer-Moore    : Right-to-left scan -> Sub-linear O(N / M) best time|
| 5. Trie Tree      : Character edge tree -> O(L) time prefix search ⚡   |
| 6. Suffix Array   : Distinct Substrings = N*(N+1)/2 - sum(LCP)        |
| 7. Kasai's LCP    : Monotonic k - 1 reduction -> O(N) linear time     |
| 8. Aho-Corasick   : Trie + BFS Fail Links -> O(N + Z) single-pass     |
| 9. Manacher's     : Transformed "^#c1#...#cn#$" -> Mirror P[i'] -> O(N)|
| 10. Double Hash   : (Hash1, Hash2) with 10^9+7 & 10^9+9 (< 10^-18 risk)|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can explain Java Compact Strings memory layout (`byte[] coder`).
- [ ] I can write manual string hash code calculation using base 31 Horner's rule.
- [ ] I can write Naive Pattern Matching with $O(N)$ distinct pattern jump optimization.
- [ ] I can write $O(M)$ LPS Table Precomputation routine in Java.
- [ ] I can write KMP Search Engine with zero text pointer backtracking.
- [ ] I can write Rabin-Karp rolling hash update with negative modulo correction.
- [ ] I can write Boyer-Moore Bad Character right-to-left matching and Horspool search.
- [ ] I can write $O(N)$ Z-Array construction and pattern matching via $S = P + \text{'\$'} + T$.
- [ ] I can implement LeetCode 208 (`Implement Trie`) using `TrieNode[26]` in Java.
- [ ] I can write Prefix-Doubling Suffix Array and Kasai's $O(N)$ LCP Array algorithm.
- [ ] I can calculate distinct substrings using Suffix Array + LCP.
- [ ] I can build an Aho-Corasick Automaton with BFS failure links and dictionary output links.
- [ ] I can write Manacher's $O(N)$ linear-time longest palindromic substring algorithm.
- [ ] I can write Double Modulo Hashing ($10^9+7$ and $10^9+9$) for $O(1)$ range queries.
- [ ] I can write online Palindromic Tree (EERTREE) insertions with Dual Roots.
- [ ] I can write in-place Run-Length Encoding and Huffman Coding Tree compression.
- [ ] I can write Duval's Algorithm for minimal string rotation in $O(N)$ time and $O(1)$ space.
- [ ] I can write Suffix Automaton (SAM) state extension in $O(N)$ linear time.
