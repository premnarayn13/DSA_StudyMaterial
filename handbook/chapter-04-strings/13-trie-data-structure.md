# 13. Trie Data Structure & Prefix Trees

## 1. Introduction
A **Trie** (pronounced "Try", derived from "Re**trie**val"), also known as a **Prefix Tree**, is a tree-like data structure used to store and retrieve strings efficiently. In technical coding interviews (LeetCode 208 "Implement Trie"), Tries enable prefix searches (`startsWith`), auto-complete systems, spell-checkers, dictionary lookups, and Maximum XOR queries in **$O(L)$ time** (where $L$ is key word length), independent of total dictionary size $N$.

> **Important:** Unlike a HashMap where lookup takes $O(L)$ time but prefix search takes $O(N \cdot L)$ time, a Trie executes **BOTH exact word lookup AND prefix search in $O(L)$ time**!

## 2. Core Concepts
* **TrieNode Structure**: Each node contains:
  * An array (or HashMap) of child references `TrieNode[] children = new TrieNode[26]`.
  * A boolean flag `boolean isEndOfWord` indicating whether the node completes a valid word.
* **Root Node**: Represents an empty string `""`.
* **Insert Operation (`insert(word)`)**: Traverses/creates nodes for each character of `word` and sets `isEndOfWord = true` on the final character node ($O(L)$ time).
* **Search Operation (`search(word)`)**: Traverses nodes matching characters of `word`. Returns `true` ONLY if traversal completes AND `isEndOfWord == true` ($O(L)$ time).
* **Prefix Search (`startsWith(prefix)`)**: Traverses nodes matching characters of `prefix`. Returns `true` if traversal completes without null links ($O(L)$ time).

> **Memory Trick:** **"Search checks isEndOfWord == true; StartsWith checks node != null!"**

## 3. Characteristics / Properties
* **Shared Prefix Memory Efficiency**: Words sharing common prefixes (e.g., `"cat"`, `"car"`, `"catnip"`) share the same ancestor nodes `'c' -> 'a'`, reducing memory footprint for large dictionaries.
* **Child Allocation Options**:
  * `TrieNode[26]`: Fastest lookup (direct array offset `ch - 'a'`), but consumes 26 pointer slots per node.
  * `HashMap<Character, TrieNode>`: Flexible for full ASCII / Unicode sets, allocating pointers on demand.

```
Trie Performance Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation             | Time Complexity   | Auxiliary Space   | Key Comparison    |
+-----------------------+-------------------+-------------------+-------------------+
| `insert(word)`        | O(L)              | O(L * 26)         | Creates missing nodes|
| `search(word)`        | O(L)              | O(1)              | Requires isEndOfWord=true|
| `startsWith(prefix)`  | O(L)              | O(1)              | Node presence only|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Insertion of `"cat"`, `"car"`, and `"cap"` into a Trie:

```
Step 1: Insert "cat"
Root -> 'c' -> 'a' -> 't' (isEndOfWord = true)

Step 2: Insert "car"
Root -> 'c' -> 'a' (Shared!) -> 'r' (isEndOfWord = true)

Step 3: Insert "cap"
Root -> 'c' -> 'a' (Shared!) -> 'p' (isEndOfWord = true)
```

## 5. Visual Diagram
Trie Node Structure & Pointer Memory Diagram:

```
               (Root)
                 |
                'c'
                 |
                'a'
              /  |  \
            't' 'r' 'p'
            [T] [T] [T]   ([T] = isEndOfWord == true)

Prefix "ca" traverses Root -> 'c' -> 'a' (Valid prefix! startsWith("ca") == true).
Search "ca" returns false because node 'a' has isEndOfWord == false.
```

## 6. Operations / Algorithms
LeetCode 208 Master Implementation:

```java
public class Trie {

    private static class TrieNode {
        private TrieNode[] children;
        private boolean isEndOfWord;

        public TrieNode() {
            children = new TrieNode[26];
            isEndOfWord = false;
        }
    }

    private final TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    // Insert word in O(L) Time
    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int index = c - 'a';
            if (curr.children[index] == null) {
                curr.children[index] = new TrieNode();
            }
            curr = curr.children[index];
        }
        curr.isEndOfWord = true;
    }

    // Search exact word in O(L) Time
    public boolean search(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int index = c - 'a';
            if (curr.children[index] == null) return false;
            curr = curr.children[index];
        }
        return curr.isEndOfWord;
    }

    // Search prefix in O(L) Time
    public boolean startsWith(String prefix) {
        TrieNode curr = root;
        for (char c : prefix.toCharArray()) {
            int index = c - 'a';
            if (curr.children[index] == null) return false;
            curr = curr.children[index];
        }
        return true; // Node reached -> valid prefix
    }
}
```

> **Quick Syntax:**
```java
// Trie Node Index Formula
int index = ch - 'a';
```

## 7. Examples
* **LeetCode 208 - Implement Trie (Prefix Tree)**: Full Trie data structure.
* **LeetCode 211 - Design Add and Search Words Data Structure**: Trie search supporting `.` wildcard matching via DFS recursion.
* **LeetCode 212 - Word Search II**: Backtracking 2D grid matrix using a Trie for multi-word search pruning.
* **LeetCode 421 - Maximum XOR of Two Numbers in an Array**: Binary Bitwise Trie ($0$ and $1$ children).

## 8. Java Code
Complete interview-ready Java suite implementing Trie with Wildcard `.` Search (LeetCode 211) and Multi-Word Search:

```java
public class TrieMaster {

    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEndOfWord = false;
    }

    private final TrieNode root = new TrieNode();

    // 1. Insert Word O(L)
    public void addWord(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
        }
        curr.isEndOfWord = true;
    }

    // 2. Search Word with '.' Wildcard Support (LeetCode 211) O(L) or O(26^L) worst
    public boolean searchWithWildcard(String word) {
        return searchHelp(word, 0, root);
    }

    private boolean searchHelp(String word, int index, TrieNode node) {
        if (node == null) return false;
        if (index == word.length()) return node.isEndOfWord;

        char c = word.charAt(index);
        if (c == '.') {
            // Wildcard '.' -> Try all 26 possible children
            for (TrieNode child : node.children) {
                if (child != null && searchHelp(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        } else {
            int childIdx = c - 'a';
            return searchHelp(word, index + 1, node.children[childIdx]);
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        TrieMaster trie = new TrieMaster();
        trie.addWord("bad");
        trie.addWord("dad");
        trie.addWord("mad");

        System.out.println("Search 'pad': " + trie.searchWithWildcard("pad")); // false
        System.out.println("Search 'bad': " + trie.searchWithWildcard("bad")); // true
        System.out.println("Search '.ad': " + trie.searchWithWildcard(".ad")); // true
        System.out.println("Search 'b..': " + trie.searchWithWildcard("b..")); // true
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **`insert(word)`** | **$O(L)$** | $O(L \cdot 26)$ | Independent of dictionary size $N$ |
| **`search(word)`** | **$O(L)$** | $O(1)$ | Faster than $O(N \cdot L)$ list search |
| **`startsWith(prefix)`**| **$O(L)$** | $O(1)$ | Impossible in $O(L)$ with standard HashSets |

## 10. Edge Cases
* **Empty String ("")**: Handled cleanly by setting `root.isEndOfWord = true`.
* **Uppercase / Non-English Letters**: `children[c - 'a']` crashes if characters are outside `'a'...'z'`. Use `HashMap<Character, TrieNode>` for full ASCII.
* **Prefix Search for Non-Existent Prefix**: Traversal encounters `null` link and returns `false` in $O(L)$ time.

## 11. Common Mistakes
* Returning `true` in `search(word)` without checking `curr.isEndOfWord` (causes prefix `"ca"` to return `true` when only `"cat"` was inserted!).
* Confusing `search(word)` (requires `isEndOfWord == true`) with `startsWith(prefix)` (requires only non-null node).
* Allocating new `TrieNode` objects during `search()` or `startsWith()` operations.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Difference between `search(word)` and `startsWith(prefix)`:
> * `search(word)`: Must reach non-null node AND check **`curr.isEndOfWord == true`**.
> * `startsWith(prefix)`: Just check if non-null node is reached (**`curr != null`**).

> **Memory Trick:** **"Search = End Flag Check; StartsWith = Node Presence Check!"**

## 13. Comparisons
| Feature | Trie Data Structure | HashSet / HashMap |
| :--- | :--- | :--- |
| **Exact Word Search** | $O(L)$ time | $O(L)$ avg time |
| **Prefix Search (`startsWith`)**| **$O(L)$ time (Optimal)** | $O(N \cdot L)$ time (Slow linear scan!) |
| **Auto-Complete Capability**| **EXCELLENT (Traverses subtree)**| Impossible |
| **Memory Consumption** | High (26 pointers / node) | Lower per string |

## 14. How to Recognize This in Questions
* **"Find all words matching prefix P"** $\rightarrow$ Trie Data Structure ($O(L)$ time).
* **"Design auto-complete or spell-checker system"** $\rightarrow$ Trie Data Structure.
* **"Word Search II on 2D Matrix Grid"** $\rightarrow$ Matrix DFS + Trie Pruning.

## 15. Frequently Asked Interview Questions
* **Q: Why is a Trie better than a HashSet for prefix searching?**  
  *A:* A HashSet computes the hash of the full string and cannot search prefixes without scanning all $N$ keys in $O(N \cdot L)$ time. A Trie traverses character nodes step-by-step, finding any prefix match in $O(L)$ time independent of dictionary size.
* **Q: What is a Binary Bitwise Trie?**  
  *A:* A Trie where each node has only 2 children (0 and 1) representing binary bit representations of integers. Used in LeetCode 421 to find Maximum XOR of two numbers in $O(32 \cdot N) \approx O(N)$ time.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE DATA STRUCTURE & PREFIX TREES                    |
+-----------------------------------------------------------------------+
| • Node Structure: TrieNode[] children = new TrieNode[26]; isEndOfWord  |
| • Insert(word): Traverse/allocate chars -> set isEndOfWord = true     |
| • Search(word): Return curr != null && curr.isEndOfWord               |
| • StartsWith(prefix): Return curr != null                             |
| • Wildcard '.' Search: Recursively branch to all 26 children on '.'    |
| • Exact Search & Prefix Search run in O(L) time independent of N!     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the `TrieNode` inner class structure from memory.
- [ ] I can implement `insert`, `search`, and `startsWith` in under 5 minutes.
- [ ] I know the difference between `search` and `startsWith` completion checks.
- [ ] I can implement Trie search with `.` wildcard support using DFS.
- [ ] I know how to use Tries for Maximum XOR problems.
