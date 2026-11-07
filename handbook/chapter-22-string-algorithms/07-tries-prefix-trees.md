# 07. Tries & Prefix Trees: Node Architecture, Prefix Search & Memory Optimizations

## 1. Introduction
A **Trie** (derived from "re**TRIE**val" and pronounced "try"), also known as a **Prefix Tree**, is a tree-like retrieval data structure used to store and search collections of strings over a fixed alphabet $\Sigma$. Unlike binary search trees or hash tables that compare full strings of length $L$, a Trie stores strings character-by-character along directed edge paths descending from a root node. Each node represents a single character prefix, allowing lookup, insertion, prefix searching (`startsWith`), and deletion operations to execute in **$O(L)$ Time Complexity**—completely independent of the total number of stored strings $N$! Tries form the architectural foundation for **Search Engine Autocomplete**, **IP Routing Table Lookups**, **Spell Checkers**, and **Dictionary Systems**.

> **Important:** Core Structural Invariants of Tries:
> 1. **Root Node Invariant**: The root node corresponds to an empty string `""` and holds no character value.
> 2. **Edge Character Representation**: Edges descending from parent to child represent individual characters $c \in \Sigma$.
> 3. **`isEndOfWord` Flag**: Each node contains a boolean flag (`isEndOfWord`) marking whether the path from the root to that node forms a valid complete word in the dictionary.
> 4. **$O(L)$ Lookup Speed**: Searching a string of length $L$ requires at most $L$ pointer traversals down the tree:
>    $$\text{Time Complexity} = O(L) \quad \text{vs} \quad \text{Hash Table } O(L) \text{ Hash Compute + } O(L) \text{ Collision Verification}$$
> 5. **Memory Trade-off**: Standard array-backed Tries (`TrieNode[26]`) use $O(N \cdot L \cdot |\Sigma|)$ space. Memory can be optimized via **HashMap-backed children**, **Compressed Tries (Radix Trees)**, or **Ternary Search Trees (TST)**. ⚡

```
Trie Tree Topology Storing Words ["cat", "car", "cart", "dog", "dot"]:

                        Root ("")
                       /        \
                    'c'          'd'
                   /                \
                 'a'                'o'
                /   \               /  \
              'r' *  't' *        'g' * 't' *
               |
             't' *

Note: '*' indicates isEndOfWord = true!
Shared Prefixes ("ca" and "do") are stored EXACTLY ONCE in memory! ⚡
```

---

## 2. Core Concepts & Trie Variants Strategy Matrix

### 2.1 Complete Trie Variants Comparison Matrix
```
Trie Architecture Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Trie Variant          | Node Storage      | Insertion Time    | Search Time       | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Array-Based Trie**  | `TrieNode[26]`    | **$O(L)$ Instant ⚡**| **$O(L)$ Instant ⚡**| $O(N \cdot L \cdot 26)$ (Sparse)|
| **Map-Based Trie**    | `HashMap<Char,N>` | **$O(L)$ Linear ⚡**| **$O(L)$ Linear ⚡**| **$O(N \cdot L)$ Compact ⚡**|
| **Ternary Search Tree**| Left, Equal, Right| $O(L \log |\Sigma|)$| $O(L \log |\Sigma|)$| **$O(N \cdot L)$ Minimal ⚡**|
| **Radix Tree (Compressed)**| Multi-Char Edges| **$O(L)$ Linear ⚡**| **$O(L)$ Linear ⚡**| **$O(N)$ Nodes Only ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Trie lookup is O(L) time where L is word length! Shared prefixes are merged into single tree paths!"**

---

## 3. Characteristics & Mathematical Complexity Proofs

### 3.1 Mathematical Proof of $O(L)$ Time & $O(N \cdot L \cdot |\Sigma|)$ Space
* **Insertion & Search Time Complexity Proof**:
  - Let $L$ be the length of the string to insert or search.
  - At each character $s[i]$ ($0 \le i < L$), the algorithm performs 1 array index lookup `children[s[i] - 'a']` or hash map lookup.
  - Total pointer hops across $L$ characters: $L$ steps.
  - Total Time Complexity: $\mathbf{O(L) \text{ Operations}}$ (Independent of dictionary size $N$!).
* **Space Complexity Proof**:
  - In the worst case, $N$ words of length $L$ share no common prefix.
  - Total tree nodes created $= N \cdot L + 1$.
  - Each node contains an array of size $|\Sigma|$ pointers.
  - Total Space Complexity: $\mathbf{O(N \cdot L \cdot |\Sigma|) \text{ Space}}$.
  - For lowercase English alphabet ($|\Sigma| = 26$), space is $26 \times N \times L$ pointers. ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Operations

### 4.1 Insertion Mechanic
1. Start at `root`.
2. For each character `c` in word $W$:
   - Check if `current.children[c - 'a']` exists.
   - If `null`, instantiate a new `TrieNode`.
   - Advance `current = current.children[c - 'a']`.
3. Set `current.isEndOfWord = true`.

### 4.2 Search Mechanic (`search(word)`)
1. Start at `root`.
2. For each character `c` in word $W$:
   - If `current.children[c - 'a'] == null`, return `false` (Word absent!).
   - Advance `current = current.children[c - 'a']`.
3. Return `current != null && current.isEndOfWord`.

### 4.3 Prefix Search Mechanic (`startsWith(prefix)`)
1. Start at `root`.
2. For each character `c` in prefix $P$:
   - If `current.children[c - 'a'] == null`, return `false`.
   - Advance `current = current.children[c - 'a']`.
3. Return `true` (Prefix path exists in Trie!).

### 4.4 Recursive Deletion Mechanic (`delete(word)`)
1. Traverse down to the target word node recursively.
2. Unset `isEndOfWord = false`.
3. If node has no other children and is not the end of another word, remove the node reference from parent to reclaim memory!

```
Tracing Insertion of "cat" and "car":

Initial State: Root ("")

Insert "cat":
- 'c': Root.children['c'] == null -> Create Node('c'). Advance.
- 'a': Node('c').children['a'] == null -> Create Node('a'). Advance.
- 't': Node('a').children['t'] == null -> Create Node('t'). Advance.
- Mark Node('t').isEndOfWord = true.

Insert "car":
- 'c': Node('c') EXISTS -> Advance.
- 'a': Node('a') EXISTS -> Advance (Reused shared prefix "ca"!).
- 'r': Node('a').children['r'] == null -> Create Node('r'). Advance.
- Mark Node('r').isEndOfWord = true.

"ca" branch shared cleanly between "cat" and "car"! ✅
```

---

## 5. Visual Diagram: Trie Memory Layout & Traversal Node Paths

```
Detailed Memory View of Array-Based TrieNode:

+-------------------------------------------------------------+
| Class TrieNode                                              |
+-------------------------------------------------------------+
| boolean isEndOfWord: true / false                           |
| TrieNode[] children: [ 0: null | 1: null | ... | 25: ptr ] |  (26 Pointers)
+-------------------------------------------------------------+

Pointer Path Traversal for "car":

[ Root ] ──── 'c' ───► [ Node 'c' ] ──── 'a' ───► [ Node 'a' ] ──── 'r' ───► [ Node 'r' (isEnd=true) ]
                                                        │
                                                        └─── 't' ───► [ Node 't' (isEnd=true) ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing an Array-Backed Trie (LeetCode 208), a HashMap-Backed Trie (supporting arbitrary Unicode characters), and Autocomplete Prefix Search.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Tries & Prefix Trees,
 * Array-Backed Storage, HashMap Unicode Extensions, and Autocomplete Engines.
 */
public class TrieMaster {

    // =========================================================================
    // 1. STANDARD ARRAY-BACKED TRIE (LeetCode 208 O(L) Time, O(N*L*26) Space)
    // =========================================================================
    public static class ArrayTrie {

        public static class TrieNode {
            public final TrieNode[] children;
            public boolean isEndOfWord;
            public int prefixCount; // Tracks how many words share this prefix!

            public TrieNode() {
                this.children = new TrieNode[26]; // 26 lowercase English letters
                this.isEndOfWord = false;
                this.prefixCount = 0;
            }
        }

        private final TrieNode root;

        public ArrayTrie() {
            this.root = new TrieNode();
        }

        /**
         * Inserts a word into the Trie in O(L) time.
         *
         * @param word string to insert
         */
        public void insert(String word) {
            if (word == null || word.length() == 0) return;

            TrieNode curr = root;
            for (int i = 0; i < word.length(); i++) {
                char ch = word.charAt(i);
                int idx = ch - 'a';

                if (curr.children[idx] == null) {
                    curr.children[idx] = new TrieNode();
                }

                curr = curr.children[idx];
                curr.prefixCount++;
            }

            curr.isEndOfWord = true;
        }

        /**
         * Searches if a exact complete word exists in Trie in O(L) time.
         *
         * @param word target search word
         * @return true if word exists and is marked as end of word
         */
        public boolean search(String word) {
            if (word == null || word.length() == 0) return false;

            TrieNode node = searchNode(word);
            return node != null && node.isEndOfWord;
        }

        /**
         * Checks if there is any word in the Trie that starts with given prefix in O(L) time.
         *
         * @param prefix search prefix
         * @return true if prefix path exists
         */
        public boolean startsWith(String prefix) {
            if (prefix == null || prefix.length() == 0) return false;

            return searchNode(prefix) != null;
        }

        /**
         * Returns how many words in the Trie share the given prefix in O(L) time.
         */
        public int countWordsWithPrefix(String prefix) {
            if (prefix == null || prefix.length() == 0) return 0;

            TrieNode node = searchNode(prefix);
            return (node != null) ? node.prefixCount : 0;
        }

        /**
         * Deletes a word from the Trie in O(L) time and reclaims unused nodes.
         */
        public boolean delete(String word) {
            if (word == null || !search(word)) return false;
            return deleteHelper(root, word, 0);
        }

        private boolean deleteHelper(TrieNode curr, String word, int depth) {
            if (depth == word.length()) {
                curr.isEndOfWord = false;
                return isNodeEmpty(curr);
            }

            int idx = word.charAt(depth) - 'a';
            TrieNode child = curr.children[idx];
            curr.prefixCount--;

            boolean shouldDeleteChild = deleteHelper(child, word, depth + 1);

            if (shouldDeleteChild) {
                curr.children[idx] = null; // Reclaim node reference! ⚡
                return !curr.isEndOfWord && isNodeEmpty(curr);
            }

            return false;
        }

        private boolean isNodeEmpty(TrieNode node) {
            for (TrieNode child : node.children) {
                if (child != null) return false;
            }
            return true;
        }

        private TrieNode searchNode(String str) {
            TrieNode curr = root;
            for (int i = 0; i < str.length(); i++) {
                int idx = str.charAt(i) - 'a';
                if (curr.children[idx] == null) {
                    return null;
                }
                curr = curr.children[idx];
            }
            return curr;
        }
    }

    // =========================================================================
    // 2. UNICODE MAP-BACKED TRIE & AUTOCOMPLETE ENGINE
    // =========================================================================
    public static class MapTrie {

        public static class MapTrieNode {
            public final Map<Character, MapTrieNode> children = new HashMap<>();
            public boolean isEndOfWord = false;
        }

        private final MapTrieNode root = new MapTrieNode();

        public void insert(String word) {
            if (word == null) return;
            MapTrieNode curr = root;
            for (char ch : word.toCharArray()) {
                curr = curr.children.computeIfAbsent(ch, k -> new MapTrieNode());
            }
            curr.isEndOfWord = true;
        }

        /**
         * Returns all words in the Trie starting with given prefix (Autocomplete Engine).
         */
        public List<String> autocomplete(String prefix) {
            List<String> results = new ArrayList<>();
            if (prefix == null) return results;

            MapTrieNode curr = root;
            for (char ch : prefix.toCharArray()) {
                if (!curr.children.containsKey(ch)) {
                    return results; // Prefix absent
                }
                curr = curr.children.get(ch);
            }

            // DFS to collect all words starting from prefix node
            dfsCollectWords(curr, new StringBuilder(prefix), results);
            return results;
        }

        private void dfsCollectWords(MapTrieNode curr, StringBuilder path, List<String> results) {
            if (curr.isEndOfWord) {
                results.add(path.toString());
            }

            for (Map.Entry<Character, MapTrieNode> entry : curr.children.entrySet()) {
                path.append(entry.getKey());
                dfsCollectWords(entry.getValue(), path, results);
                path.deleteCharAt(path.length() - 1); // Backtrack! ⚡
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Map-Backed Trie Node Insertion Line
curr = curr.children.computeIfAbsent(ch, k -> new MapTrieNode());
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 208 - Implement Trie (Prefix Tree)**:
   - Primary Trie implementation benchmark problem.

2. **LeetCode 211 - Design Add and Search Words Data Structure**:
   - Trie traversal supporting '.' wildcard characters via DFS.

3. **LeetCode 212 - Word Search II**:
   - Backtracking grid traversal combined with Trie prefix pruning ($O(M \cdot 4^L)$ optimized to milliseconds!).

4. **Search Engine Autocomplete & Spell Checking**:
   - Suggesting top-K search queries based on prefix DFS traversal.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class TrieDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     TRIE & PREFIX TREE DEMONSTRATION            ");
        System.out.println("=================================================\n");

        // 1. Array-Backed Trie Test (LeetCode 208)
        TrieMaster.ArrayTrie trie = new TrieMaster.ArrayTrie();
        trie.insert("apple");
        trie.insert("app");
        trie.insert("apricot");
        trie.insert("banana");

        System.out.println("1. Array-Backed Trie Test:");
        System.out.println("   search(\"apple\")     : " + trie.search("apple"));
        System.out.println("   search(\"app\")       : " + trie.search("app"));
        System.out.println("   search(\"appl\")      : " + trie.search("appl") + " (Prefix only)");
        System.out.println("   startsWith(\"app\")   : " + trie.startsWith("app"));
        System.out.println("   countWordsWithPrefix(\"ap\"): " + trie.countWordsWithPrefix("ap") + " Words");
        System.out.println("-------------------------------------------------");

        // Delete test
        trie.delete("app");
        System.out.println("   After delete(\"app\"):");
        System.out.println("   search(\"app\")       : " + trie.search("app") + " (Deleted!)");
        System.out.println("   search(\"apple\")     : " + trie.search("apple") + " (Preserved!)");
        System.out.println("-------------------------------------------------");

        // 2. Autocomplete Engine Test (MapTrie)
        TrieMaster.MapTrie mapTrie = new TrieMaster.MapTrie();
        mapTrie.insert("car");
        mapTrie.insert("cat");
        mapTrie.insert("cart");
        mapTrie.insert("carbon");
        mapTrie.insert("dog");

        String prefix = "car";
        List<String> suggestions = mapTrie.autocomplete(prefix);
        System.out.println("2. Autocomplete Suggestions for Prefix \"" + prefix + "\":");
        System.out.println("   Results: " + suggestions);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Trie Operation | Array Trie Time | Map Trie Time | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Insert Word** | $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(L)}$ Linear ⚡| $O(L \cdot |\Sigma|)$ Nodes | Fast $O(1)$ Array Index |
| **Search Word** | $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Independent of Dictionary Size $N$ |
| **StartsWith Prefix**| $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Instant Prefix Checking |
| **Delete Word** | $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(L)}$ Linear ⚡| $\mathbf{O(L)}$ Stack | Recursive Node Cleanup |
| **Autocomplete DFS** | $O(L + K)$ | $O(L + K)$ | $O(L)$ Path Buffer | Collects all prefix matches |

---

## 10. Edge Cases & Boundary Handling

1. **Empty String `""`**:
   - Root node marks `isEndOfWord = true`. Handled cleanly without child pointer allocations.

2. **Single Character Words (`"a"`)**:
   - Direct child lookup at index `0`, setting `isEndOfWord = true`.

3. **Deleting Word That Is Prefix of Another Word (e.g. Delete `"app"` when `"apple"` exists)**:
   - Sets `isEndOfWord = false` on `"app"` node, but preserves child pointer to `'l'` so `"apple"` remains intact!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Deleting Shared Prefix Nodes During Word Removal**:
  - Deleting node `'p'` when removing `"app"` corrupts the path for `"apple"`.
  - **Fix**: Check `isNodeEmpty(curr)` and `!curr.isEndOfWord` before removing child references!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Trie vs Hash Table Comparison:
> * **Hash Table**: $O(L)$ time to compute hash + $O(L)$ to compare keys. CANNOT perform prefix searches (`startsWith`) efficiently ($O(N \cdot L)$ scan required).
> * **Trie**: $O(L)$ time lookup AND $O(L)$ instant prefix checking (`startsWith`). Ideal for Autocomplete! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Array-Backed Trie | Map-Backed Trie | Ternary Search Tree (TST) |
| :--- | :--- | :--- | :--- |
| **Alphabet Flexibility** | Fixed (e.g., lowercase 26) | **Any Unicode Symbol ⚡** | Any Character |
| **Child Lookup Speed**   | **Instant 1-Cycle Index ⚡**| Hash Map Overhead | $O(\log |\Sigma|)$ Binary Compare |
| **Memory Efficiency**    | Sparse Array Overhead | **Compact Memory ⚡** | **Maximum Memory Saving ⚡**|

---

## 14. How to Recognize This in Questions

* **"Implement a structure to store strings with fast prefix search startsWith(prefix)"** $\rightarrow$ Trie.
* **"Find all words from dictionary present in a 2D Boggle matrix grid"** $\rightarrow$ Trie + Backtracking.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Trie lookup time $O(L)$ independent of dictionary size $N$?**  
  *A:* Because searching depends only on traversing $L$ character nodes descending from the root, regardless of how many millions of words $N$ are stored in the tree.

* **Q: What is the difference between an Array-Backed Trie and a Map-Backed Trie?**  
  *A:* Array-Backed Trie uses `TrieNode[26]` for $O(1)$ fast indexing but wastes memory on null pointers. Map-Backed Trie uses `HashMap<Character, TrieNode>` which saves memory and supports arbitrary Unicode characters.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIES & PREFIX TREES                                  |
+-----------------------------------------------------------------------+
| • Core Logic    : Character-by-character edge traversal from root     |
| • Node Fields   : TrieNode[] children (or Map), boolean isEndOfWord   |
| • Lookup Speed  : O(L) Time for Insert, Search, StartsWith (L = len)  |
| • Prefix Advantage: startsWith(prefix) takes O(L) time (Unmatched by Hash Tables)|
| • Deletion Rule : Delete node ONLY if isNodeEmpty() && !isEndOfWord   |
| • Autocomplete  : Traverse to prefix node -> DFS collect all words ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can implement LeetCode 208 (`Implement Trie`) using `TrieNode[26]` in Java.
- [ ] I can write Map-Backed Trie supporting Unicode characters.
- [ ] I can write recursive `delete(word)` with memory node cleanup.
- [ ] I can write an Autocomplete engine using Trie + DFS.
- [ ] I can state why Trie performs prefix searches faster than a Hash Table.
