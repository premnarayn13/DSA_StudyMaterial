# 03. Trie Insertion Mechanics, Character Mapping & Vocabulary Indexing Engines

## 1. Introduction
Inserting a string key into a **Trie** is the fundamental build operation for prefix trees and dictionaries. Unlike binary search tree insertion (which compares keys and rebalances node heights), Trie insertion traverses or instantiates nodes character-by-character along a single top-down path. Inserting a word of length $L$ into a Trie executes in **$O(L)$ Strict Linear Time** (where $L$ is the length of the string) and **$O(L \cdot R)$ Auxiliary Space** for new node allocations.

> **Important:** The Universal Invariants of Trie Insertion:
> 1. **Reuse Existing Prefix Path**: If a prefix path already exists in the Trie (e.g. inserting `"application"` when `"app"` is present), the insertion algorithm REUSES existing nodes without allocating new memory!
> 2. **Instantiate Missing Suffix Path**: For any character link that is `null`, instantiate a `new TrieNode()`.
> 3. **Mark End of Word**: Upon processing the last character `word.charAt(L - 1)`, set `curr.isEndOfWord = true`! ⚡

```
Trie Insertion Top-Down Path Traversal Topology:
Inserting Key = "cat" into empty Trie:
Step 1: Process 'c' (idx = 2)  ---> root.children[2] is null -> Instantiate Node(1)
Step 2: Process 'a' (idx = 0)  ---> Node(1).children[0] is null -> Instantiate Node(2)
Step 3: Process 't' (idx = 19) ---> Node(2).children[19] is null -> Instantiate Node(3)
Step 4: Mark Terminal ---------> Node(3).isEndOfWord = true! ⚡
```

---

## 2. Core Concepts & Iterative vs Recursive Insertion Architecture

### 2.1 Iterative Trie Insertion Algorithm ($O(L)$ Time, Optimal)
1. Initialize `curr = root`.
2. For each character `c` in `word`:
   - Compute character index: `int idx = c - 'a'`.
   - If `curr.children[idx] == null`:
     - `curr.children[idx] = new TrieNode()`.
   - Move pointer: `curr = curr.children[idx]`.
3. Set terminal flag: `curr.isEndOfWord = true`.

```
Trie Insertion Strategy Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Implementation Variant| Time Complexity   | Auxiliary Space   | Stack Safety      |
+-----------------------+-------------------+-------------------+-------------------+
| **Iterative Insertion**| **$O(L)$ Linear ⚡**| **$O(L)$ Space**  | **Zero Stack Risk ⚡**|
| Recursive Insertion   | **$O(L)$ Linear ⚡**| $O(L)$ Stack Space| Risk on Long Keys |
| Bulk Dictionary Load  | **$O(\sum L_i)$ ⚡**| $O(\sum L_i \cdot R)$| Sequential Batch |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Iterative Trie Insert: Loop chars, create node if null, move curr, set isEndOfWord = true at end!"**

---

## 3. Characteristics & Bulk Vocabulary Loading

### 3.1 Bulk Vocabulary Insertion Benchmark
To insert $N$ words of average length $L$ into a Trie:
* Total Time Complexity: $\mathbf{O(N \cdot L)}$ (Strictly proportional to total character volume).
* Total Space Complexity: $\mathbf{O(U \cdot R)}$ where $U$ is the total number of unique prefix nodes created across the vocabulary.

---

## 4. Internal Working Mechanics
Tracing Insertion of `"car"` when `"cat"` is already present in Trie:

```
Trie contains: root -> 'c' -> 'a' -> 't' (isEnd=true).

Insert "car":
1. Char 'c' (idx 2): root.children[2] is non-null (Node 1). Move curr = Node 1. (Reused!)
2. Char 'a' (idx 0): Node 1.children[0] is non-null (Node 2). Move curr = Node 2. (Reused!)
3. Char 'r' (idx 17): Node 2.children[17] IS NULL!
   - Instantiate Node 4 at Node 2.children[17].
   - Move curr = Node 4.
4. Set Node 4.isEndOfWord = true!

Inserted "car" by reusing 2 nodes and creating ONLY 1 new node! ✅ (O(L) Time!)
```

---

## 5. Visual Diagram
Subtree Node Reuse During Insertion Topography:

```
Before Inserting "car":                     After Inserting "car":
       [ Root ]                                    [ Root ]
          | 'c'                                       | 'c'
       [ Node 1 ]                                  [ Node 1 ]
          | 'a'                                       | 'a'
       [ Node 2 ]                                  [ Node 2 ]
          | 't'                                    /          \ 'r'
  [ Node 3 ("cat") ]                         't'  /            \
                                       [ Node 3 ("cat") ]  [ Node 4 ("car") ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Iterative, Recursive, and Bulk Vocabulary Trie Insertion:

```java
import java.util.*;

public class TrieInsertMaster {

    public static class TrieNode {
        public static final int R = 26;
        public TrieNode[] children;
        public boolean isEndOfWord;
        public int prefixCount; // Optional: Counts how many words share this prefix

        public TrieNode() {
            this.children = new TrieNode[R];
            this.isEndOfWord = false;
            this.prefixCount = 0;
        }
    }

    private final TrieNode root;

    public TrieInsertMaster() {
        this.root = new TrieNode();
    }

    // 1. Iterative Trie Insertion O(L) Time, O(L * R) Space (Optimal!)
    public void insert(String word) {
        if (word == null || word.isEmpty()) return;

        TrieNode curr = root;
        for (int i = 0; i < word.length(); i++) {
            int idx = word.charAt(i) - 'a';
            if (curr.children[idx] == null) {
                curr.children[idx] = new TrieNode();
            }
            curr = curr.children[idx];
            curr.prefixCount++; // Increment shared prefix counter
        }
        curr.isEndOfWord = true;
    }

    // 2. Bulk Dictionary Load O(N * L) Time
    public void insertAll(List<String> words) {
        if (words == null) return;
        for (String word : words) {
            insert(word);
        }
    }

    // 3. Count how many words start with given prefix O(L) Time
    public int countWordsWithPrefix(String prefix) {
        if (prefix == null || prefix.isEmpty()) return 0;

        TrieNode curr = root;
        for (int i = 0; i < prefix.length(); i++) {
            int idx = prefix.charAt(i) - 'a';
            if (curr.children[idx] == null) return 0;
            curr = curr.children[idx];
        }
        return curr.prefixCount;
    }

    public TrieNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// Trie Insertion Loop
TrieNode curr = root;
for (char c : word.toCharArray()) {
    int idx = c - 'a'; if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
    curr = curr.children[idx];
}
curr.isEndOfWord = true;
```

---

## 7. Concrete Problem Examples
* **LeetCode 208 - Insert Method**: Fundamental Trie insertion.
* **LeetCode 211 - Design Add and Search Words Data Structure**: Word dictionary insertion.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `insert` and `countWordsWithPrefix`:

```java
public class TrieInsertDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Trie Insertion & Prefix Count Test ===");
        TrieInsertMaster trie = new TrieInsertMaster();

        trie.insertAll(Arrays.asList("app", "apple", "application", "apt", "bat"));

        System.out.println("Words starting with 'app': " + 
            trie.countWordsWithPrefix("app")); // Output: 3 ("app", "apple", "application")

        System.out.println("Words starting with 'ap':  " + 
            trie.countWordsWithPrefix("ap"));  // Output: 4 ("app", "apple", "application", "apt")

        System.out.println("Words starting with 'ba':  " + 
            trie.countWordsWithPrefix("ba"));  // Output: 1 ("bat") ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Method | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Insert Single Word ($L$)**| **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L \cdot R)$ Space |
| **Bulk Insert ($N$ Words)**| **$O(N \cdot L)$ ⚡** | **$O(N \cdot L)$ ⚡** | **$O(N \cdot L)$ ⚡** | $O(U \cdot R)$ Unique Nodes |
| **Prefix Count Query**| **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Inserting Existing Word Twice**: Re-traverses path, sets `isEndOfWord = true`, prefix counts increment.
* **Inserting Prefix of Existing Word**: E.g. inserting `"app"` when `"apple"` exists sets `node.isEndOfWord = true` at the existing `"app"` node without allocating new nodes.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `curr.isEndOfWord = true` at End of Loop**:
  - Forgetting to mark terminal node leaves inserted words unrecognizable by `search()`.
  - **ALWAYS set `curr.isEndOfWord = true` after character loop finishes**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Adding `prefixCount` to `TrieNode`:
> Augmenting `TrieNode` with `public int prefixCount = 0;` and incrementing `curr.prefixCount++` during insertion allows answering **"Count how many words start with prefix P"** in **$O(L)$ time**!
> Without `prefixCount`, counting matching prefix words requires a full DFS subtree traversal ($O(K)$ time).

> **Memory Trick:** **"Augment TrieNode with prefixCount to get O(L) prefix word counts!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard Trie Insertion | Compressed Radix Insertion |
| :--- | :--- | :--- |
| **Node Allocation** | 1 Node per new character | 1 Node per edge split |
| **Code Simplicity** | **High (Simple loop) ⚡** | Low (Complex string splitting) |
| **Insertion Time** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Insert words into a dictionary for instant prefix search"** $\rightarrow$ Trie Insertion.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the auxiliary space complexity of inserting a word of length $L$?**  
  *A:* At most $O(L \cdot R)$ space (if all $L$ characters require allocating new nodes).
* **Q: How does inserting `"app"` differ when `"apple"` already exists vs when tree is empty?**  
  *A:* When `"apple"` exists, zero new nodes are allocated; the existing `'p'` node simply has `isEndOfWord` set to `true`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE INSERTION MECHANICS                              |
+-----------------------------------------------------------------------+
| • Path Traversal : Reuses existing prefix nodes; creates new if null  |
| • Terminal Flag  : MUST set curr.isEndOfWord = true at end of loop    |
| • Time Bounds    : O(L) where L is string length (Optimal!) ⚡         |
| • Prefix Count   : Increment curr.prefixCount++ to track prefix counts|
| • Bulk Insert    : O(N * L) total time for N words of length L        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write iterative Trie Insertion in Java in under 2 minutes.
- [ ] I can augment `TrieNode` with `prefixCount` for $O(L)$ prefix counting.
- [ ] I know why node allocations are minimized when inserting common prefixes.
- [ ] I know how to handle bulk vocabulary loading.
- [ ] I can trace node allocations during word insertion step by step.
