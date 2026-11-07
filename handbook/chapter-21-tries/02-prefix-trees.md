# 02. Prefix Tree Architecture, Subtree Sharing & Compressed Radix Trees

## 1. Introduction
A **Prefix Tree** (the standard formulation of a Trie, LeetCode 208) achieves extreme space efficiency by **SHARING COMMON PREFIX SUBTREES** across thousands of words. For example, the words `"apple"`, `"app"`, `"application"`, and `"apply"` share the common prefix path `"app"`, requiring only 3 character nodes to represent the prefix for all 4 words! Understanding Prefix Tree architecture, array vs HashMap implementations, and Compressed Radix Trees (Patricia Tries) enables building production **IP Router Longest Prefix Matchers** and **Spell-Check Engines** in **$O(L)$ time**.

> **Important:** Subtree Prefix Sharing & Compressed Radix Trees:
> 1. **Prefix Sharing Invariant**: If $K$ words share a common prefix of length $L$, the Trie stores that prefix ONCE using $L$ nodes instead of $K \times L$ characters!
> 2. **Compressed Radix Tree (Patricia Trie)**: Merges long chains of single-child nodes into a single edge containing a string label (e.g. merging `'a' \to 'p' \to 'p'` into a single edge `"app"`), reducing node count by up to 70%! ⚡

```
Standard Prefix Tree (Subtree Sharing Topology):
                      [ Root ]
                         | 'a'
                      [ Node ]
                         | 'p'
                      [ Node ]
                         | 'p'
              [ Node (isEnd="app") ]
             /           | 'l'        \ 'l'
       'e'  /            |             \
 [ Node ("apple") ]   [ Node ]    [ Node ("apply") ]
                         | 'i'
                     [ ... "application" ] ⚡
```

---

## 2. Core Concepts & Array vs HashMap vs Radix Trie Architectures

### 2.1 Architectural Comparison Matrix
```
Prefix Tree Architectural Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Implementation Variant| Branch Overhead   | Alphabet Range    | Memory Efficiency |
+-----------------------+-------------------+-------------------+-------------------+
| **Array-Based Trie**  | `TrieNode[26]`    | Fixed ('a'-'z')   | Sparse Wasted ❌  |
| **HashMap-Based Trie**| `Map<Char, Node>` | **Universal ⚡**   | **Compact ⚡**    |
| **Compressed Radix**  | Edge String Labels| Universal         | **Ultra-Compact ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Standard Tries share prefix subtrees! Radix Tries compress single-child chains into multi-character edges!"**

---

## 3. Characteristics & HashMap-Based Trie (LeetCode 208 Universal)

### 3.1 HashMap-Based Trie Implementation
To support any Unicode character, special symbols, or mixed case input without wasting fixed 26-element array memory:

```java
public class MapTrieNode {
    public Map<Character, MapTrieNode> children;
    public boolean isEndOfWord;

    public MapTrieNode() {
        this.children = new HashMap<>();
        this.isEndOfWord = false;
    }
}
```

---

## 4. Internal Working Mechanics
Tracing Subtree Sharing for Inserting `"app"` and `"apple"`:

```
Step 1: Insert "app":
- Create path 'a' -> 'p' -> 'p' (isEnd = true).

Step 2: Insert "apple":
- Traverse existing shared path 'a' -> 'p' -> 'p'. ZERO new nodes allocated for "app"!
- From 'p', allocate 'l' -> 'e' (isEnd = true).

"app" and "apple" share 3 nodes completely! ✅ (Saves memory & time!)
```

---

## 5. Visual Diagram
Standard Trie vs Compressed Radix Tree Topography:

```
Standard Trie (Chain Nodes):                   Compressed Radix Tree (Edge Compression):
           [ Root ]                                            [ Root ]
              | 'a'                                               | "app"
           [ Node ]                                    [ Node (isEnd="app") ]
              | 'p'                                       /              \
           [ Node ]                                 "le" /                \ "lication"
              | 'p'                                 [ "apple" ]       [ "application" ]
      [ Node (isEnd="app") ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 208 (Implement Trie - Array and HashMap Variants):

```java
import java.util.*;

// LeetCode 208: Implement Trie (Prefix Tree)
public class PrefixTreeMaster {

    // 1. Array-Based Prefix Tree (LeetCode 208 Optimal for 'a'-'z')
    public static class Trie {
        private final TrieNode root;

        private static class TrieNode {
            private final TrieNode[] children = new TrieNode[26];
            private boolean isEnd = false;
        }

        public Trie() {
            root = new TrieNode();
        }

        // Insert word O(L) Time, O(L) Space
        public void insert(String word) {
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

        // Search word O(L) Time
        public boolean search(String word) {
            TrieNode node = findNode(word);
            return node != null && node.isEnd;
        }

        // StartsWith prefix O(L) Time
        public boolean startsWith(String prefix) {
            return findNode(prefix) != null;
        }

        private TrieNode findNode(String str) {
            TrieNode curr = root;
            for (char c : str.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) return null;
                curr = curr.children[idx];
            }
            return curr;
        }
    }

    // 2. HashMap-Based Prefix Tree (Supports Unicode & Mixed Cases)
    public static class MapTrie {
        private final MapNode root = new MapNode();

        private static class MapNode {
            private final Map<Character, MapNode> children = new HashMap<>();
            private boolean isEnd = false;
        }

        public void insert(String word) {
            MapNode curr = root;
            for (char c : word.toCharArray()) {
                curr.children.putIfAbsent(c, new MapNode());
                curr = curr.children.get(c);
            }
            curr.isEnd = true;
        }

        public boolean search(String word) {
            MapNode node = find(word);
            return node != null && node.isEnd;
        }

        public boolean startsWith(String prefix) {
            return find(prefix) != null;
        }

        private MapNode find(String str) {
            MapNode curr = root;
            for (char c : str.toCharArray()) {
                if (!curr.children.containsKey(c)) return null;
                curr = curr.children.get(c);
            }
            return curr;
        }
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 208 Helper Navigation Method
private TrieNode findNode(String str) {
    TrieNode curr = root;
    for (char c : str.toCharArray()) {
        int idx = c - 'a'; if (curr.children[idx] == null) return null;
        curr = curr.children[idx];
    }
    return curr;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 208 - Implement Trie (Prefix Tree)**: Core problem.
* **IP Router Routing Tables**: Longest Prefix Match (LPM) subnet routing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `Trie` and `MapTrie`:

```java
public class PrefixTreeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 208 Implement Trie Test ===");
        PrefixTreeMaster.Trie trie = new PrefixTreeMaster.Trie();

        trie.insert("apple");
        System.out.println("Search 'apple':   " + trie.search("apple"));   // Output: true
        System.out.println("Search 'app':     " + trie.search("app"));     // Output: false
        System.out.println("StartsWith 'app': " + trie.startsWith("app")); // Output: true

        trie.insert("app");
        System.out.println("Search 'app' after insert: " + trie.search("app")); // Output: true ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Method | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`insert(word)`** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L)$ New Nodes Space |
| **`search(word)`** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|
| **`startsWith(pref)`**| **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Single Letter Words (`"a"`)**: Instantiates root's child at index 0 and sets `isEnd = true`.
* **Prefix Search Beyond Word Length**: Returns `null` cleanly when child path terminates early.

---

## 11. Common Mistakes & Anti-Patterns
* **Duplicating Code Between `search` and `startsWith`**:
  - Writing redundant loops for `search` and `startsWith` creates code duplication.
  - **Refactor common path traversal into a private `findNode(str)` helper method**!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Cleanest Refactoring Pattern for LeetCode 208:
> Create a helper method `private TrieNode findNode(String str)` that navigates the Trie path character by character.
> * `startsWith(prefix)` $\implies$ **`return findNode(prefix) != null;`**
> * `search(word)` $\implies$ **`TrieNode n = findNode(word); return n != null && n.isEnd;`**
> This refactoring reduces LeetCode 208 code size by 50%! ⚡

> **Memory Trick:** **"Refactor findNode(str): startsWith checks != null; search checks != null && isEnd!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard Trie | Compressed Radix Tree (Patricia) |
| :--- | :--- | :--- |
| **Edge Storage** | 1 Character per Edge | Multi-Character String Label |
| **Node Count** | High (1 Node per Char) | **Minimal (Merged Chains) ⚡** |
| **Lookup Speed** | $O(L)$ Array Hops | **$O(L)$ Fewer Hop Dereferences ⚡**|

---

## 14. How to Recognize This in Questions
* **"Implement Trie with insert, search, and startsWith operations"** $\rightarrow$ LeetCode 208.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `findNode` simplify Trie implementation?**  
  *A:* Because `findNode` encapsulates the character path traversal loop, allowing `startsWith` and `search` to be written as 1-liners.
* **Q: How does a Radix Tree compress nodes?**  
  *A:* By merging any node with only 1 child into a single combined edge label string, eliminating redundant single-child nodes.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PREFIX TREE ARCHITECTURE (LEETCODE 208)               |
+-----------------------------------------------------------------------+
| • Subtree Sharing: Common prefixes share identical node paths         |
| • findNode Helper: Traverses path for any string; returns node or null|
| • startsWith(p)  : return findNode(p) != null;                        |
| • search(w)      : TrieNode n = findNode(w); return n != null && n.isEnd;|
| • Array vs Map   : Use array TrieNode[26] for 'a'-'z'; Map for Unicode|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 208 (`Trie`) from memory in 3 minutes using `findNode`.
- [ ] I can write a `MapTrie` supporting Unicode input.
- [ ] I know how subtree sharing optimizes memory for common prefixes.
- [ ] I know how Radix Trees compress single-child chains.
- [ ] I can trace path traversals for `search` vs `startsWith`.
