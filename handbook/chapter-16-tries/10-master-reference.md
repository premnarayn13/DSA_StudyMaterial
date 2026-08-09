# 10. Master Reference — Tries (Prefix Trees)

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 16: Tries (Prefix Trees)**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for string algorithms and technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Trie Invariants ($O(L)$ Search Time Independent of Dictionary Size $N$), `findNode(str)` Refactoring Pattern for LeetCode 208, Wildcard DFS Backtracking for LeetCode 211, Bottom-Up Post-Order Pruning for Deletion, Pre-computed Top-3 Caching for Auto-Complete (LeetCode 1268), Suffix Trie Substring Invariant, Bitwise 32-Bit XOR Trie (LeetCode 421), and Unified Grid DFS for Word Search II (LeetCode 212)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Trie Character Index Mapping Formula**:
  - `int index = char - 'a';` (For lowercase English alphabet $R = 26$).
* **Exact Search vs Prefix Search Rules**:
  - `startsWith(prefix)` $\implies$ Path exists (`findNode(prefix) != null`).
  - `search(word)` $\implies$ Path exists AND `isEndOfWord == true` (`findNode(word).isEndOfWord`).
* **Post-Order Deletion Pruning Safety Rule**:
  - Prune node `curr` IF AND ONLY IF `!curr.isEndOfWord && !hasChildren(curr)`.
* **Suffix Trie Substring Invariant**:
  - Every substring of text $S$ is a PREFIX of at least ONE suffix $S[i \dots N-1]$. Substring search executes in **$O(M)$ time** (where $M$ is pattern length).
* **Bitwise XOR Maximization Rule**:
  - For bit `b` of number $X$, greedily follow `oppositeBit = 1 - b` in 32-Bit Binary Trie to maximize XOR result!

```
Tries Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Exact Search Time Complexity      | O(L) Time (Independent of dictionary size N!) ⚡  |
| LeetCode 208 Refactoring          | findNode(str) helper reduces code by 50%          |
| LeetCode 211 Wildcard '.'         | DFS branch to ALL 26 non-null children            |
| Auto-Complete Top-3 Cache         | Sort products array first -> Pre-cache top-3 lists|
| LeetCode 421 Bitwise XOR          | Greedily follow opposite bit (1 - b) from bit 31-0|
| LeetCode 212 Word Search II       | Unified Trie Grid DFS; prune if child is null     |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Insert Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L \cdot R)$ Space | Reuses existing prefix path |
| **Search Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Checks `node.isEndOfWord` |
| **StartsWith ($P$)**  | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Checks `findNode(P) != null` |
| **Delete Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L)$ Stack Space | Bottom-up post-order pruning |
| **Wildcard Search (211)**| **$O(L)$ Linear ⚡** | $O(R \cdot L)$ Average | $O(R^L)$ (All Dots) | $O(L)$ Stack Space | DFS branching on `'.'` |
| **Auto-Complete (1268)**| **$O(1)$ Instant ⚡** | **$O(1)$ Instant ⚡** | **$O(1)$ Instant ⚡** | $O(N \cdot L \cdot K)$ Cache| Pre-computed top-3 cache |
| **Suffix Substring ($M$)**| **$O(M)$ Linear ⚡** | **$O(M)$ Linear ⚡** | **$O(M)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Prefix search on suffix trie |
| **Max XOR Pair (421)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(32 \cdot N)$ Space | Bitwise 32-bit binary trie |
| **Word Search II (212)**| **$O(M \cdot N \cdot 3^L)$ ⚡**| **$O(M \cdot N \cdot 3^L)$ ⚡**| **$O(M \cdot N \cdot 3^L)$ ⚡**| $O(K \cdot L)$ Trie Space | Unified Trie Grid DFS pruning |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Trie Nodes                                                   |
+-----------------------------------------------------------------------------------+
| Array-Based `TrieNode` (`[26]`)      : 224 Bytes per Node (Header + 26 Refs + Bool) |
| HashMap-Based `MapTrieNode`          : ~64 Bytes Base (Dynamic Map Entries)         |
| Radix Tree Edge Compression          : Reduces Node Count by up to 70%!             |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Trie Index Mapping Line
int idx = word.charAt(i) - 'a';

// 2. LeetCode 208 findNode Helper Method
private TrieNode findNode(String str) {
    TrieNode curr = root;
    for (char c : str.toCharArray()) {
        int idx = c - 'a'; if (curr.children[idx] == null) return null;
        curr = curr.children[idx];
    }
    return curr;
}

// 3. LeetCode 211 Wildcard Loop Line
if (c == '.') { for (int i=0; i<26; i++) if (curr.children[i] != null && dfsSearch(word, index+1, curr.children[i])) return true; }

// 4. LeetCode 421 Bitwise Opposites Maximization Line
int bit = (num >> i) & 1; int oppositeBit = 1 - bit;
if (curr.children[oppositeBit] != null) { maxXOR |= (1 << i); curr = curr.children[oppositeBit]; }

// 5. LeetCode 212 Word Match & Deduplication Line
if (curr.word != null) { result.add(curr.word); curr.word = null; }
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Confusing `startsWith` with `search`**: `startsWith` checks path existence (`curr != null`), while `search` requires `curr.isEndOfWord == true`.
* **Pitfall 2: Pruning Nodes Representing Other Words**: In Trie deletion, pruning a node with `isEndOfWord == true` destroys another valid word. Only prune when `!curr.isEndOfWord && !hasChildren(curr)`.
* **Pitfall 3: Duplicate Matches in Word Search II (LeetCode 212)**: A word formable via multiple grid paths gets added repeatedly. Fix: set `curr.word = null` after adding to `result`.
* **Pitfall 4: Running $N^2$ Brute Force for Maximum XOR (LeetCode 421)**: Brute force checking all pairs takes $O(N^2)$ time and TLEs. Always use a 32-Bit Bitwise Binary Trie ($O(N)$).
* **Pitfall 5: Hardcoding Array Size 26 for Mixed Unicode Strings**: `new TrieNode[26]` crashes on non-lowercase input. Use `HashMap<Character, TrieNode>` for general Unicode input!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 16 (TRIES)                       |
+-----------------------------------------------------------------------+
| 1. Search Time     : O(L) where L is word length (Independent of N!) ⚡|
| 2. LeetCode 208    : startsWith checks != null; search checks isEndOfWord|
| 3. LeetCode 211    : Wildcard '.' branches DFS to ALL 26 children     |
| 4. Deletion        : Bottom-up prune IF AND ONLY IF !isEnd && !hasChildren|
| 5. Auto-Complete   : Pre-sort products -> Cache top-3 list per node ⚡|
| 6. Suffix Trie     : Insert all suffixes S[i...N-1] -> Substring search O(M)|
| 7. LeetCode 421    : 32-bit Trie; follow opposite bit (1 - b) to max XOR|
| 8. LeetCode 212    : Insert words to Trie; run 1 grid DFS pass with pruning|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write LeetCode 208 (`Trie`) from memory in 3 minutes using `findNode`.
- [ ] I can write LeetCode 211 (`WordDictionary` with wildcard '.') in Java.
- [ ] I can write Trie Deletion with bottom-up post-order pruning.
- [ ] I can write LeetCode 1268 (`Search Suggestions System`) with top-3 caching.
- [ ] I can write a Suffix Trie supporting $O(M)$ substring search.
- [ ] I can write LeetCode 421 (`Maximum XOR of Two Numbers in an Array`) in $O(N)$ time.
- [ ] I can write LeetCode 212 (`Word Search II`) with Trie grid DFS pruning.
