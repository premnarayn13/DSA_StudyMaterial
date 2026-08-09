# 01. Trie Foundations, TrieNode Anatomy & Character Branching Invariants

## 1. Introduction
A **Trie** (derived from re**TRIE**val, pronounced "try" or "tree") is an $R$-way tree-based data structure optimized for fast string key retrieval, prefix matching, and dictionary operations. Unlike binary search trees that compare full key values at every node, a Trie structures keys character-by-character along edge branches. Searching for a string of length $L$ in a Trie executes in **$O(L)$ Time**—completely independent of the total number of keys $N$ stored in the structure!

> **Important:** The Core Invariants & Structural Mechanics of a Trie:
> 1. **Character Path Invariant**: Nodes do NOT store full key strings; a node's position in the Trie defines the prefix string it represents!
> 2. **Root Node**: Represents the empty prefix string `""`.
> 3. **`isEndOfWord` Boolean Flag**: Marks whether a path terminating at a specific node forms a complete valid word in the dictionary! ⚡

```
Trie Structural Topology (Storing "cat", "car", "cart", "dog"):
                      [ Root (isEnd=false) ]
                     /                      \
               'c'  /                        \ 'd'
              [ Node (isEnd=false) ]     [ Node (isEnd=false) ]
                 /                          /
           'a'  /                     'o'  /
       [ Node (isEnd=false) ]      [ Node (isEnd=false) ]
          /           \               /
    't'  /             \ 'r'    'g'  /
  [ Node (isEnd=true) ] [ Node (isEnd=true) ] [ Node (isEnd=true) ]
     ("cat")               ("car")               ("dog")
        |
   't'  |
  [ Node (isEnd=true) ] ("cart") ⚡
```

---

## 2. Core Concepts & `TrieNode` Structural Definition

### 2.1 The `TrieNode` Reference Array Definition
For a standard English lowercase alphabet ($R = 26$):

```java
public class TrieNode {
    public static final int ALPHABET_SIZE = 26;
    public TrieNode[] children; // Array of 26 references for 'a' through 'z'
    public boolean isEndOfWord; // True if this node represents the end of a valid word

    public TrieNode() {
        this.children = new TrieNode[ALPHABET_SIZE];
        this.isEndOfWord = false;
    }
}
```

```
Trie Structural Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Trie Implementation   | Branch Factor $R$ | Node Memory       | Search Time       |
+-----------------------+-------------------+-------------------+-------------------+
| **Array-Based Trie**  | $R = 26$ Array    | 26 Pointer Links  | **$O(L)$ Fast ⚡**|
| HashMap-Based Trie    | Dynamic `Map`     | Dynamic Objects   | $O(L)$ (Hash Cost)|
| Compressed (Radix)    | String Labels     | Compact Nodes     | **$O(L)$ Compact ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Trie search takes O(L) time where L is word length, regardless of dictionary size N!"**

---

## 3. Characteristics & $O(L)$ Search Time Guarantee

### 3.1 Why Trie Search Time $O(L)$ Is Independent of $N$
* In a Binary Search Tree, searching a key takes $O(H) = O(\log N)$ time. For large dictionaries ($N = 10,000,000$), $\log_2 N \approx 24$ comparisons.
* In a Trie, searching a 4-letter word like `"cart"` takes **EXACTLY 4 character array lookups** ($O(L)$ time), completely unaffected by whether the dictionary contains 10 words or 10,000,000 words! ⚡

---

## 4. Internal Working Mechanics
Tracing Trie Node Character Mapping for Key `"cat"`:

```
Alphabet Offset Formula: index = char - 'a' ('c' - 'a' = 2, 'a' - 'a' = 0, 't' - 'a' = 19).

Root Node:
1. Char 'c' (index 2): root.children[2] is null -> Instantiate new TrieNode. Move curr = root.children[2].
2. Char 'a' (index 0): curr.children[0] is null -> Instantiate new TrieNode. Move curr = curr.children[0].
3. Char 't' (index 19): curr.children[19] is null -> Instantiate new TrieNode. Move curr = curr.children[19].
4. Set curr.isEndOfWord = true!

Word "cat" inserted in 3 steps! ✅
```

---

## 5. Visual Diagram
Character Array Index Offset Mapping Topography:

```
Root children array (Size 26):
+---+---+---+---+---+ ... +----+
| 0 | 1 | 2 | 3 | 4 |     | 25 |
+---+---+---+---+---+ ... +----+
  a   b   |   d   e         z
          v ('c' - 'a' = 2)
     [ Next TrieNode ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing `TrieNode` construction, key insertion, and prefix search verification:

```java
import java.util.*;

public class TrieFoundationsMaster {

    public static class TrieNode {
        public static final int R = 26;
        public TrieNode[] children;
        public boolean isEndOfWord;

        public TrieNode() {
            this.children = new TrieNode[R];
            this.isEndOfWord = false;
        }
    }

    private final TrieNode root;

    public TrieFoundationsMaster() {
        this.root = new TrieNode();
    }

    // Insert word into Trie O(L) Time, O(L * R) Space
    public void insert(String word) {
        if (word == null || word.isEmpty()) return;

        TrieNode curr = root;
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            if (curr.children[index] == null) {
                curr.children[index] = new TrieNode();
            }
            curr = curr.children[index];
        }
        curr.isEndOfWord = true;
    }

    // Check if word exists in Trie O(L) Time
    public boolean search(String word) {
        if (word == null || word.isEmpty()) return false;

        TrieNode curr = root;
        for (int i = 0; i < word.length(); i++) {
            int index = word.charAt(i) - 'a';
            if (curr.children[index] == null) {
                return false; // Character path missing
            }
            curr = curr.children[index];
        }
        return curr.isEndOfWord; // Must be valid end of word
    }

    // Check if any word starts with prefix O(L) Time
    public boolean startsWith(String prefix) {
        if (prefix == null || prefix.isEmpty()) return false;

        TrieNode curr = root;
        for (int i = 0; i < prefix.length(); i++) {
            int index = prefix.charAt(i) - 'a';
            if (curr.children[index] == null) {
                return false;
            }
            curr = curr.children[index];
        }
        return true; // Valid prefix path exists
    }

    public TrieNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// Trie Index Formula Line
int index = word.charAt(i) - 'a';
```

---

## 7. Concrete Problem Examples
* **LeetCode 208 - Implement Trie (Prefix Tree)**: Core Trie implementation.
* **Auto-complete Search Engines**: Instant prefix suggestion lookups.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Trie insertion, word search, and prefix matching:

```java
public class TrieFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Trie Foundations Test ===");
        TrieFoundationsMaster trie = new TrieFoundationsMaster();

        trie.insert("cat");
        trie.insert("car");
        trie.insert("cart");

        System.out.println("Search 'cat':   " + trie.search("cat"));   // Output: true
        System.out.println("Search 'car':   " + trie.search("car"));   // Output: true
        System.out.println("Search 'can':   " + trie.search("can"));   // Output: false

        System.out.println("StartsWith 'ca': " + trie.startsWith("ca")); // Output: true
        System.out.println("StartsWith 'do': " + trie.startsWith("do")); // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Insert Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L \cdot R)$ Node Space |
| **Search Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|
| **StartsWith Prefix** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Empty String `""`**: Handled safely by early validation guard `if (word == null || word.isEmpty()) return;`.
* **Prefix Search vs Full Word Search**: `"ca"` returns `true` for `startsWith("ca")`, but `false` for `search("ca")` if `isEndOfWord` is `false`.

---

## 11. Common Mistakes & Anti-Patterns
* **Confusing `startsWith(prefix)` with `search(word)`**:
  - `startsWith` requires ONLY that the character path exists (`curr != null`).
  - `search` requires BOTH that the path exists AND `curr.isEndOfWord == true`.
* **Allocating 26-element arrays for Unicode / ASCII-256 strings**:
  - Using `new TrieNode[26]` fails on uppercase letters or special characters. Use `HashMap<Character, TrieNode>` for general Unicode input!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Tries Outperform Hash Tables for Prefix Operations:
> A Hash Table can perform $O(L)$ point lookups, BUT cannot answer prefix queries like `"find all words starting with 'app'"` without scanning all $N$ keys ($O(N \cdot L)$ penalty!).
> A Trie answers prefix queries in **$O(L)$ time**, making it the optimal structure for **Auto-complete Engines**!

> **Memory Trick:** **"Trie search takes O(L) time where L is word length! StartsWith checks path existence; Search checks isEndOfWord!"**

---

## 13. System & Implementation Comparisons

| Feature | Array-Based Trie (`[26]`) | HashMap-Based Trie |
| :--- | :--- | :--- |
| **Lookup Speed** | **Fastest (Direct Array Index) ⚡**| Slightly Slower (Hash overhead) |
| **Alphabet Support** | Fixed Lowercase ('a'-'z') | **Universal Unicode / Special Chars ⚡**|
| **Memory Efficiency**| Wasteful if sparse | **Compact for Sparse Alpha ⚡** |

---

## 14. How to Recognize This in Questions
* **"Search for words or prefixes in a dictionary of strings"** $\rightarrow$ LeetCode 208 (Trie).
* **"Build auto-complete prefix suggestions"** $\rightarrow$ Trie structure.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the time complexity of searching a word of length $L$ in a Trie containing $N$ words?**  
  *A:* $O(L)$ time, completely independent of $N$.
* **Q: Why does a Trie node NOT store its own character value explicitly?**  
  *A:* Because a node's character value is implicit from its index position in its parent's `children` array!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE FOUNDATIONS & PREFIX SEARCH                      |
+-----------------------------------------------------------------------+
| • Key Invariant : Node defines prefix path; stores isEndOfWord flag   |
| • Index Mapping : index = char - 'a' (For 26 lowercase English letters)|
| • Search Time   : O(L) where L is word length (Independent of N!) ⚡   |
| • StartsWith    : Checks path existence (curr != null)                |
| • Search        : Checks path existence AND curr.isEndOfWord == true  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a `TrieNode` definition in Java.
- [ ] I can write `insert`, `search`, and `startsWith` in $O(L)$ time.
- [ ] I know why Trie search time is independent of $N$.
- [ ] I know why Hash Tables fail on prefix queries.
- [ ] I can state the differences between array-based and HashMap-based Tries.
