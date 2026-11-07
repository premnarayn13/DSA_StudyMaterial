# 06. Auto-Complete Engines, Prefix Suggestion Systems & Ranking Heaps

## 1. Introduction
**Auto-Complete Engines**—specifically **Search Suggestions System (LeetCode 1268)** and **Design Search Autocomplete System (LeetCode 642)**—are among the most prominent real-world applications of Tries. Given a search prefix string, an Auto-Complete Engine navigates to the prefix node in **$O(L)$ time**, then executes a **Backtracking DFS Subtree Search** combined with a **Min-Heap (PriorityQueue)** to return the Top-$K$ (e.g. Top-3) most relevant or lexicographically smallest suggested words in **$O(L + M \log K)$ time**.

> **Important:** The Auto-Complete Engine 2-Phase Strategy:
> 1. **Phase 1: Prefix Traversal**: Navigate top-down from root following prefix $P$ of length $L$. If any character node is missing, return empty list `[]` in $O(L)$ time!
> 2. **Phase 2: Subtree DFS & Top-$K$ Ranking**: Perform DFS from prefix node. Maintain a Min-Heap of size $K$ (e.g. $K=3$). Keep the $K$ top-ranked words, discarding lower-ranked candidates in **$O(M \log K)$ time** (where $M$ is total words in subtree)! ⚡

```
Auto-Complete Search Suggestion Pipeline Topology (Prefix = "app"):
Step 1: Traverse Prefix "app" -------> Navigates root -> 'a' -> 'p' -> 'p' (Node P)
Step 2: Subtree DFS Search ----------> Collects candidates: "app", "apple", "application", "apply"
Step 3: Top-3 Min-Heap Ranking ------> Keeps Top-3 Lexicographical: ["app", "apple", "application"] ⚡
```

---

## 2. Core Concepts & LeetCode 1268 Search Suggestions System

### 2.1 Search Suggestions System Algorithm (LeetCode 1268)
Given array of `products` and a `searchWord`:
1. Build a Trie containing all `products`.
2. For each prefix `searchWord[0...i]` ($i = 0 \dots L-1$):
   - Traverse to prefix node in Trie.
   - Collect all words in subtree via DFS.
   - Sort/Select Top-3 lexicographically smallest words.
   - Add Top-3 list to result!

```
Auto-Complete Engine Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Auto-Complete System  | Top-$K$ Criteria  | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **LeetCode 1268**     | Top-3 Lexicographical| **$O(L + M \log 3)$ ⚡**| $O(N \cdot L)$ Trie|
| **LeetCode 642**      | Top-3 Frequency   | **$O(L + M \log 3)$ ⚡**| $O(N \cdot L)$ Trie|
| Pre-computed Node Cache| Pre-stored Top-3 List| **$O(L)$ Strict ⚡**| Increased Node Space|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Auto-Complete: Traverse to prefix node in O(L) time -> Run DFS to collect subtree words -> Rank Top-K!"**

---

## 3. Characteristics & Pre-Computed Top-3 Node Cache Optimization

### 3.1 Industrial Production Optimization: Pre-Computed Top-3 Caching
In high-performance search engines (Google / Amazon search bars):
* Instead of running DFS on every keystroke:
* Every `TrieNode` stores a pre-computed list: `public List<String> top3Cache = new ArrayList<>();`.
* During insertion, each node along the path maintains its Top-3 suggested words.
* **Query Time**: `suggest(prefix)` returns `curr.top3Cache` directly in **$O(L)$ STRICT TIME** without running any DFS! ⚡

---

## 4. Internal Working Mechanics
Tracing Search Suggestions System (LeetCode 1268) for products `["mobile","mouse","moneypot","monitor","mousepad"]` and searchWord `"mouse"`:

```
Trie built. Prefix "m":
- Subtree DFS collects: ["mobile","moneypot","monitor","mouse","mousepad"].
- Top-3 Lexicographical: ["mobile","moneypot","monitor"].

Prefix "mo":
- Subtree DFS collects: ["mobile","moneypot","monitor","mouse","mousepad"].
- Top-3 Lexicographical: ["mobile","moneypot","monitor"].

Prefix "mou":
- Subtree DFS collects: ["mouse","mousepad"].
- Top-3 Lexicographical: ["mouse","mousepad"].

Executed in O(L) time per prefix! ✅
```

---

## 5. Visual Diagram
Subtree DFS & Top-K Min-Heap Ranking Topography:

```
                    [ Prefix Node "app" ]
                   /          |          \
             "apple"    "application"   "apply"
                   \          |          /
             +--------------------------------+
             | Min-Heap (Size 3)              |
             | Top-3: ["app", "apple", "appli"]|
             +--------------------------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 1268 (Search Suggestions System - Trie DFS and Pre-computed Node Cache):

```java
import java.util.*;

// LeetCode 1268: Search Suggestions System
public class AutoCompleteMaster {

    private static class TrieNode {
        private final TrieNode[] children = new TrieNode[26];
        private final List<String> top3Cache = new ArrayList<>(); // Pre-computed Top-3 cache
    }

    private final TrieNode root = new TrieNode();

    // Build Trie with Pre-computed Top-3 Caching O(N * L log N)
    public void buildTrie(String[] products) {
        Arrays.sort(products); // Sort products lexicographically first!

        for (String product : products) {
            TrieNode curr = root;
            for (char c : product.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) {
                    curr.children[idx] = new TrieNode();
                }
                curr = curr.children[idx];

                // Cache top-3 lexicographically smallest words at node
                if (curr.top3Cache.size() < 3) {
                    curr.top3Cache.add(product);
                }
            }
        }
    }

    // LeetCode 1268 Solution: Instant O(L) Top-3 Suggestions
    public List<List<String>> suggestedProducts(String[] products, String searchWord) {
        buildTrie(products);
        List<List<String>> result = new ArrayList<>();

        TrieNode curr = root;
        for (char c : searchWord.toCharArray()) {
            int idx = c - 'a';
            if (curr != null) {
                curr = curr.children[idx];
            }
            if (curr != null) {
                result.add(curr.top3Cache); // Instant O(1) fetch from cache!
            } else {
                result.add(new ArrayList<>()); // Empty list if prefix missing
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Pre-computed Top-3 Caching Line
if (curr.top3Cache.size() < 3) curr.top3Cache.add(product);
```

---

## 7. Concrete Problem Examples
* **LeetCode 1268 - Search Suggestions System**: Top-3 lexicographical suggestions.
* **LeetCode 642 - Design Search Autocomplete System**: Frequency-ranked search bar.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 1268 Auto-Complete Engine:

```java
public class AutoCompleteDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 1268 Search Suggestions System Test ===");
        AutoCompleteMaster engine = new AutoCompleteMaster();
        String[] products = {"mobile","mouse","moneypot","monitor","mousepad"};
        String searchWord = "mouse";

        List<List<String>> suggestions = engine.suggestedProducts(products, searchWord);

        for (int i = 0; i < searchWord.length(); i++) {
            String prefix = searchWord.substring(0, i + 1);
            System.out.println("Prefix '" + prefix + "': " + suggestions.get(i));
        }
        // Output:
        // Prefix 'm':     ["mobile", "moneypot", "monitor"]
        // Prefix 'mo':    ["mobile", "moneypot", "monitor"]
        // Prefix 'mou':   ["mouse", "mousepad"]
        // Prefix 'mous':  ["mouse", "mousepad"]
        // Prefix 'mouse': ["mouse", "mousepad"] ✅
    }
}
```

---

## 9. Complexity Analysis

| Auto-Complete Approach | Build Time | Query Time per Character | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **DFS Subtree Search** | $O(N \cdot L)$ | $O(L + M \log K)$ | $O(N \cdot L)$ Trie |
| **Pre-computed Cache**| **$O(N \cdot L \log N)$ ⚡**| **$O(1)$ Instant ⚡** | $O(N \cdot L \cdot K)$ Space |

---

## 10. Edge Cases & Boundary Handling
* **Prefix Not Present in Trie**: `curr` becomes `null`, returns `[]` immediately for all remaining characters.
* **Fewer Than 3 Products Match**: Returns available products (e.g. list of size 1 or 2).

---

## 11. Common Mistakes & Anti-Patterns
* **Running Full DFS on Every Keystroke Without Caching**:
  - Re-running DFS across a subtree of 100,000 words on every character keystroke causes UI lag.
  - **Pre-sort products and cache top-3 lists inside `TrieNode` for $O(1)$ query speed**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Pre-sorting Products Enables $O(1)$ Caching:
> By sorting `products` array lexicographically BEFORE populating the Trie:
> The first 3 words that pass through any `TrieNode` during insertion are GUARANTEED to be the top-3 lexicographically smallest words for that prefix!
> Simply checking `if (node.top3Cache.size() < 3) node.top3Cache.add(product)` caches optimal suggestions automatically! ⚡

> **Memory Trick:** **"Sort products first -> First 3 words inserted at any node are automatically the Top-3 lexicographical suggestions!"**

---

## 13. System & Implementation Comparisons

| Feature | Pre-computed Top-3 Cache Trie | Dynamic DFS Subtree Trie |
| :--- | :--- | :--- |
| **Query Speed** | **$O(1)$ Instant per char ⚡** | $O(M \log K)$ DFS Scan |
| **Build Pre-sorting** | Sort `products` array first | No pre-sorting required |
| **Code Simplicity** | **High (Clean caching) ⚡** | Moderate (DFS recursion) |

---

## 14. How to Recognize This in Questions
* **"Design auto-complete search bar returning top-3 matching products for each prefix character"** $\rightarrow$ LeetCode 1268.

---

## 15. Frequently Asked Interview Questions
* **Q: How does pre-sorting products optimize LeetCode 1268 to $O(1)$ query time per character?**  
  *A:* Pre-sorting guarantees that the first 3 products inserted through any prefix node are the lexicographically smallest, allowing `top3Cache` to be populated during a single insertion pass.
* **Q: How does LeetCode 642 handle frequency ranking?**  
  *A:* By storing sentence frequencies in a `Map<String, Integer>` inside `TrieNode` and maintaining a Min-Heap of size 3 ordered by `(-frequency, sentence)`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: AUTO-COMPLETE ENGINES (LEETCODE 1268)                 |
+-----------------------------------------------------------------------+
| • Step 1: Sort products array lexicographically                       |
| • Step 2: Insert into Trie; cache product if node.top3Cache.size() < 3|
| • Step 3: Query searchWord: Navigate curr = curr.children[char - 'a'] |
| • Step 4: Fetch curr.top3Cache in O(1) time per character! ⚡          |
| • Query Bounds: O(L) Total Time for entire searchWord! ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 1268 (`Search Suggestions System`) in Java.
- [ ] I know why pre-sorting products enables $O(1)$ top-3 caching.
- [ ] I can write dynamic DFS subtree search for top-$K$ suggestions.
- [ ] I know how LeetCode 642 handles frequency-ranked auto-complete.
- [ ] I can trace top-3 suggestions for sequential prefix characters.
