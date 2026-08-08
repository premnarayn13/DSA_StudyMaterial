# 14. Trie (Prefix Tree) Architecture & Concurrent ConcurrentSkipListMap

## 1. Introduction
The **Trie (Prefix Tree - LeetCode 208)** and thread-safe concurrent tree structures (**`java.util.concurrent.ConcurrentSkipListMap`**) represent essential specialized tree data structures in technical coding interviews and high-concurrency systems design. A Trie is an $N$-ary prefix search tree used for instant prefix matching, autocomplete search engines, spell checkers, and IP routing tables. In multi-threaded enterprise software, `ConcurrentSkipListMap` provides a lock-free, thread-safe alternative to synchronized Red-Black Trees, achieving **$O(\log N)$ expected time for concurrent read/write operations**.

> **Important:** In a Trie, nodes do NOT store character values directly! Instead, a node's character is defined by its **child array index position** (`children[c - 'a']`), and each string path shares common prefix nodes to achieve **$O(L)$ search time** (where $L$ is the string length, independent of total dataset size $N$!).

```
Prefix Search Data Structures Spectrum:
+-----------------------------------------------------------------------------------+
| Hash Set Search     : Whole String Match Only -> O(L) Time, No Prefix Support     |
| Trie (Prefix Tree)  : Prefix & Word Match    -> O(L) Time, Shared Prefix Space ⚡ |
| ConcurrentSkipList  : Thread-Safe Sorted Map -> O(log N) Lock-Free Concurrent ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Trie Node Architecture

### 2.1 The Trie Node Structure
Each node in a standard lowercase English Trie contains:
1. **Children Array (`TrieNode[] children = new TrieNode[26]`)**: References to child nodes for characters `'a'` through `'z'`.
2. **End-of-Word Flag (`boolean isEnd`)**: Boolean marker indicating whether the path from the root node to the current node forms a complete valid word.

### 2.2 Trie Operations & Algorithms
* **Insert String $S$ ($O(L)$ Time)**:
  - Start at `root`.
  - For each char $C$ in $S$:
    - `index = C - 'a'`.
    - If `curr.children[index] == null`, instantiate `curr.children[index] = new TrieNode()`.
    - Move `curr = curr.children[index]`.
  - Set `curr.isEnd = true`.
* **Search Word $S$ ($O(L)$ Time)**:
  - Follow child pointers for each char in $S$. If any child pointer is `null`, return `false`.
  - After processing all chars, return `curr.isEnd`.
* **StartsWith Prefix $P$ ($O(L)$ Time)**:
  - Follow child pointers for each char in $P$. If any child pointer is `null`, return `false`.
  - After processing all chars in prefix $P$, return `true` (regardless of `isEnd`!).

### 2.3 Concurrent Thread-Safe Trees & `ConcurrentSkipListMap`
Standard `TreeMap` (Red-Black Tree) is NOT thread-safe. Wrapping `TreeMap` in `Collections.synchronizedSortedMap()` creates a single coarse-grained lock, bottlenecking throughput under high concurrency.
* **`ConcurrentSkipListMap`**: A thread-safe, lock-free concurrent sorted map based on **Skip Lists**. It uses **CAS (Compare-And-Swap)** hardware primitives for concurrent writes, enabling lock-free $O(\log N)$ searches, insertions, and range queries!

```
Concurrent Sorted Map Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Map Implementation    | Lock Strategy     | Read Throughput   | Write Throughput  |
+-----------------------+-------------------+-------------------+-------------------+
| `TreeMap`             | Unsafe (No Locks) | Single Threaded   | Single Threaded   |
| `SynchronizedTreeMap` | Global Monolithic | Poor (Bottleneck) | Poor (Bottleneck) |
| `ConcurrentSkipList`  | Lock-Free CAS ⚡  | **Maximum ⚡**    | **High Concurrency|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Trie Node: TrieNode[26] children + boolean isEnd! Search returns curr.isEnd; StartsWith returns true!"**

---

## 3. Characteristics & Trie Problem Variations

### 3.1 Word Search II (LeetCode 212 - Grid Backtracking + Trie)
* Building a Trie of dictionary words allows searching a 2D grid of characters for valid words in $O(\text{Grid})$ time.
* Optimization: Store full word string inside `TrieNode.word` at `isEnd` nodes, eliminating `StringBuilder` string creation during grid DFS backtracking.

---

## 4. Internal Working Mechanics
Tracing Trie Insertion of `"apple"` and `"app"`:

```
Root
 |
 ['a'] (idx 0)
 |
 ['p'] (idx 15)
 |
 ['p'] (idx 15) -> isEnd = true ("app" is a valid word!)
 |
 ['l'] (idx 11)
 |
 ['e'] (idx 4)  -> isEnd = true ("apple" is a valid word!)
```

```
Search "app"   : Traverses a -> p -> p. Child exists and isEnd == true -> Return TRUE! ✅
StartsWith "ap": Traverses a -> p. Child exists -> Return TRUE! ✅
Search "appl"  : Traverses a -> p -> p -> l. Child exists but isEnd == false -> Return FALSE! ❌
```

---

## 5. Visual Diagram
Trie Structural Node Layout & Shared Prefix Paths:

```
                      ( Root )
                     /        \
                  ['a']      ['c']
                   /            \
                ['p']          ['a']
                 /                \
              ['p'] (isEnd=true)  ['t'] (isEnd=true)
               /
            ['l']
             /
          ['e'] (isEnd=true)

Shared Prefix "ap" stored ONCE for both "app" and "apple"!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Implement Trie / Prefix Tree (LeetCode 208), Add and Search Word with Wildcard '.' (LeetCode 211), and Word Search II (LeetCode 212):

```java
import java.util.*;

public class TrieMaster {

    // 1. Implement Trie (Prefix Tree - LeetCode 208) O(L) Time, O(N * L * 26) Space
    public static class Trie {
        private static class TrieNode {
            TrieNode[] children;
            boolean isEnd;

            TrieNode() {
                children = new TrieNode[26];
                isEnd = false;
            }
        }

        private final TrieNode root;

        public Trie() {
            root = new TrieNode();
        }

        // Inserts a word into the trie. O(L) Time
        public void insert(String word) {
            if (word == null) return;
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) {
                    curr.children[idx] = new TrieNode();
                }
                curr = curr.children[idx];
            }
            curr.isEnd = true;
        }

        // Returns true if the word is in the trie. O(L) Time
        public boolean search(String word) {
            TrieNode node = searchPrefixNode(word);
            return node != null && node.isEnd;
        }

        // Returns true if there is any word in the trie that starts with the given prefix. O(L) Time
        public boolean startsWith(String prefix) {
            return searchPrefixNode(prefix) != null;
        }

        private TrieNode searchPrefixNode(String prefix) {
            if (prefix == null) return null;
            TrieNode curr = root;
            for (char c : prefix.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return null;
                curr = curr.children[idx];
            }
            return curr;
        }
    }

    // 2. Design Add and Search Words Data Structure with '.' Wildcards (LeetCode 211)
    public static class WordDictionary {
        private static class TrieNode {
            TrieNode[] children = new TrieNode[26];
            boolean isEnd = false;
        }

        private final TrieNode root = new TrieNode();

        public void addWord(String word) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
                curr = curr.children[idx];
            }
            curr.isEnd = true;
        }

        public boolean search(String word) {
            return searchWildcardDFS(word, 0, root);
        }

        private boolean searchWildcardDFS(String word, int index, TrieNode node) {
            if (node == null) return false;
            if (index == word.length()) return node.isEnd;

            char c = word.charAt(index);
            if (c == '.') {
                // Wildcard matches ANY child 0..25
                for (int i = 0; i < 26; i++) {
                    if (node.children[i] != null && searchWildcardDFS(word, index + 1, node.children[i])) {
                        return true;
                    }
                }
                return false;
            } else {
                int idx = c - 'a';
                return searchWildcardDFS(word, index + 1, node.children[idx]);
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Wildcard '.' Subtree Exploration Loop
if (c == '.') {
    for (int i = 0; i < 26; i++) {
        if (node.children[i] != null && searchWildcard(word, index + 1, node.children[i]))
            return true;
    }
    return false;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 208 - Implement Trie (Prefix Tree)**: Core Trie operations.
* **LeetCode 211 - Design Add and Search Words Data Structure**: Wildcard '.' search DFS.
* **LeetCode 212 - Word Search II**: Grid backtracking + Trie optimization.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Trie insertion, exact word search, prefix search, and wildcard wildcard search:

```java
public class TrieDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Standard Trie (LeetCode 208) ===");
        TrieMaster.Trie trie = new TrieMaster.Trie();
        trie.insert("apple");
        trie.insert("app");

        System.out.println("Search 'apple': " + trie.search("apple"));   // true
        System.out.println("Search 'app':   " + trie.search("app"));     // true
        System.out.println("Search 'appl':  " + trie.search("appl"));    // false
        System.out.println("StartsWith 'app': " + trie.startsWith("app")); // true

        System.out.println("\n=== 2. Testing Wildcard WordDictionary (LeetCode 211) ===");
        TrieMaster.WordDictionary dict = new TrieMaster.WordDictionary();
        dict.addWord("bad");
        dict.addWord("dad");
        dict.addWord("mad");

        System.out.println("Search 'pad': " + dict.search("pad")); // false
        System.out.println("Search 'bad': " + dict.search("bad")); // true
        System.out.println("Search '.ad': " + dict.search(".ad")); // true (matches bad, dad, mad)
        System.out.println("Search 'b..': " + dict.search("b..")); // true (matches bad)
    }
}
```

---

## 9. Complexity Analysis

| Data Structure | Search Time | Prefix Search Time | Concurrency Model |
| :--- | :--- | :--- | :--- |
| **Trie (Prefix Tree)** | **$O(L)$ ($L$ string length) ⚡**| **$O(L)$ ($L$ prefix length) ⚡**| Standard Unsafe |
| **HashMap<String, V>** | $O(L)$ (Hash computation) | $O(N)$ (Requires linear key scan) | Thread Unsafe |
| **`ConcurrentSkipListMap`**| **$O(\log N)$ Logarithmic ⚡**| $O(\log N)$ Range SubMap | **Lock-Free CAS ⚡** |

---

## 10. Edge Cases & Boundary Handling
* **Empty String Insertion (`""`)**: `insert("")` sets `root.isEnd = true`.
* **Non-Lowercase Characters**: Standard `TrieNode[26]` assumes `'a'..'z'`. For general ASCII, use `TrieNode[256]` or `HashMap<Character, TrieNode>`.

---

## 11. Common Mistakes & Anti-Patterns
* **Confusing `search()` with `startsWith()`**:
  - `search()` requires `node != null && node.isEnd == true`.
  - `startsWith()` requires only `node != null` (ignores `isEnd`).
* **Memory Bloat with Large Alphabets**: Using `new TrieNode[256]` or `new TrieNode[65536]` when most array slots remain `null`. Use `Map<Character, TrieNode>` for sparse character sets.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Trie Beats HashMap for Autocomplete:
> A HashMap can check whole string equality in $O(L)$ time, but finding all words starting with prefix `"app"` requires scanning all $N$ keys in $O(N \cdot L)$ time!
> A Trie locates the prefix node in $O(L)$ time and collects all matching descendant words instantly!

> **Memory Trick:** **"Trie search checks isEnd; startsWith ignores isEnd! Use HashMap for sparse child nodes!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard Array Trie (`TrieNode[26]`) | Map Trie (`HashMap<Character, Node>`) |
| :--- | :--- | :--- |
| **Search Time** | **Fastest $O(L)$ (Direct Index) ⚡** | Slightly slower (Hash Map overhead) |
| **Memory Usage** | Fixed 26 references per node | **Compact (Allocates per child) ⚡** |
| **Alphabet Range**| Bounded ('a'..'z') | **Unlimited (Unicode / ASCII)** |

---

## 14. How to Recognize This in Questions
* **"Design a data structure supporting insert, search, and startsWith prefix operations"** $\rightarrow$ LeetCode 208 (Trie).
* **"Find all words in a 2D grid matching a dictionary"** $\rightarrow$ LeetCode 212 (Trie + Grid DFS).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Trie search take $O(L)$ time regardless of whether the dictionary contains 10 words or 1,000,000 words?**  
  *A:* Because at each character in string $S$, we index directly into `curr.children[c - 'a']` in $O(1)$ constant time. Following $L$ characters takes $L$ steps, completely independent of total words $N$.
* **Q: Why is `ConcurrentSkipListMap` preferred over `Collections.synchronizedSortedMap()`?**  
  *A:* Synchronized wrapper maps lock the ENTIRE map during every read and write operation, causing thread contention bottlenecks. `ConcurrentSkipListMap` uses lock-free Compare-And-Swap (CAS) operations on skip list node pointers, allowing multiple threads to read and write concurrently.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE (PREFIX TREE) & CONCURRENT SKIPLIST              |
+-----------------------------------------------------------------------+
| • Trie Node: TrieNode[] children = new TrieNode[26]; boolean isEnd;   |
| • Insert S: Follow/create child[c - 'a'], set curr.isEnd = true       |
| • Search S: Follow child pointers; return node != null && node.isEnd   |
| • StartsWith P: Follow child pointers; return node != null            |
| • Wildcard '.' (211): Loop children 0..25 and recurse on wildcard '.' |
| • Autocomplete Advantage: Finds prefix matches in O(L) time           |
| • Concurrent Priority: ConcurrentSkipListMap for lock-free O(log N)    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `TrieNode` definition and `insert()`, `search()`, `startsWith()`.
- [ ] I know why `startsWith()` does NOT check `isEnd`.
- [ ] I can write wildcard `.` search DFS (LeetCode 211).
- [ ] I know why Trie beats HashMap for autocomplete prefix search.
- [ ] I know why `ConcurrentSkipListMap` provides lock-free concurrency.
