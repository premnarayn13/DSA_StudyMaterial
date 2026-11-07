# 04. Trie Search Mechanics, Wildcard Matching & DFS Pattern Engines

## 1. Introduction
Searching in a **Trie** encompasses three distinct operational query patterns: **Exact Word Search (`search(word)`)**, **Prefix Path Search (`startsWith(prefix)`)**, and **Wildcard Pattern Search (`searchWithWildcard(pattern)`)**—specifically **Design Add and Search Words Data Structure (LeetCode 211)**. While exact word and prefix search execute in **$O(L)$ Strict Linear Time** (where $L$ is length of word), searching with wildcard characters (like `'.'` matching any single letter) uses **Backtracking Depth-First Search (DFS)** to branch across non-null child links in **$O(R^L)$ Worst-Case Time**.

> **Important:** The 3 Query Patterns in Trie Searching:
> 1. **Exact Word Search (`search(word)`)**: Traverses path for `word`; returns `curr != null && curr.isEndOfWord`.
> 2. **Prefix Path Search (`startsWith(prefix)`)**: Traverses path for `prefix`; returns `curr != null`.
> 3. **Wildcard Search (`search(pattern)` LeetCode 211)**: When character is `'.'`, recursively explores ALL 26 non-null child branches (`curr.children[0...25]`)! ⚡

```
Trie Wildcard Search Topology (Searching pattern "b.t" in Trie containing "bat", "bet", "bit", "cat"):
                      [ Root ]
                     /        \
               'b'  /          \ 'c' (Pruned! 'c' != 'b')
       [ Node ("b") ]
       /     |     \
  'a' /  'e' |  'i' \  ('.' matches 'a', 'e', AND 'i'! Branch DFS to all 3 children!)
     v       v       v
   [Node]  [Node]  [Node]
     | 't'   | 't'   | 't'
    ("bat") ("bet") ("bit") -> Returns TRUE (Matches 3 words!) ⚡
```

---

## 2. Core Concepts & LeetCode 211 Wildcard Backtracking Engine

### 2.1 LeetCode 211 Backtracking DFS Algorithm
To search for pattern `word` starting at `index` from node `curr`:
1. Base Case: If `index == word.length()`: Return `curr.isEndOfWord`.
2. Get character `char c = word.charAt(index)`.
3. If `c != '.'` (Exact Character Match):
   - `int idx = c - 'a'`.
   - If `curr.children[idx] == null`: Return `false`.
   - Return `dfsSearch(word, index + 1, curr.children[idx])`.
4. Else (`c == '.'` - Wildcard Match):
   - Iterate through all 26 children: `for (int i = 0; i < 26; i++)`.
   - If `curr.children[i] != null`:
     - If `dfsSearch(word, index + 1, curr.children[i]) == true`: Return `true`!
   - Return `false` (No child branch matched wildcard).

```
Trie Search Pattern Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Query Pattern         | Time Complexity   | Auxiliary Space   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| **Exact Word Search** | **$O(L)$ Linear ⚡**| **$O(1)$ Constant ⚡**| `curr = curr.children[idx]`|
| **Prefix Search**     | **$O(L)$ Linear ⚡**| **$O(1)$ Constant ⚡**| `curr != null` check|
| **Wildcard Search (211)**| $O(R^L)$ (Worst) | $O(L)$ Stack Space| DFS branch on `'.'`|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Wildcard '.': If char is '.', branch DFS to ALL 26 non-null children!"**

---

## 3. Characteristics & Search Complexity Bounds

### 3.1 Time Complexity Bounds
* **Exact Search**: $O(L)$ time, zero backtracking.
* **Wildcard Search**: Best case $O(L)$ (no wildcards). Worst case $O(R^L)$ when pattern consists of all dots (`"...."`).

---

## 4. Internal Working Mechanics
Tracing Wildcard Search for `"b.t"` on Trie `["bat", "cat"]`:

```
Call dfsSearch("b.t", index=0, root):

Step 1: index = 0, char = 'b'.
- Exact match 'b' (idx 1). root.children[1] is Node("b").
- Recurse dfsSearch("b.t", index=1, Node("b")).

Step 2: index = 1, char = '.'.
- Wildcard '.' matched! Loop i = 0 to 25.
- i = 0 ('a'): Node("b").children[0] is Node("ba").
  - Recurse dfsSearch("b.t", index=2, Node("ba")).
    - index = 2, char = 't'.
    - Exact match 't' (idx 19). Node("ba").children[19] is Node("bat") (isEnd=true).
    - index = 3 == length -> Returns TRUE!

Wildcard match found in 3 steps! ✅
```

---

## 5. Visual Diagram
Wildcard Search DFS Branching Topography:

```
Pattern "b.t":
             [ Root ]
                | 'b' (Exact match)
          [ Node "b" ]
                |
           +----+----+ (Char = '.' -> Branch to all non-null children!)
          /     |     \
     'a' /  'e' |      \ 'i'
    [ "ba" ] [ "be" ] [ "bi" ]
       |        |        |
      't'      't'      't'
   [ "bat" ] [ "bet" ] [ "bit" ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 211 (Design Add and Search Words Data Structure):

```java
import java.util.*;

// LeetCode 211: Design Add and Search Words Data Structure
public class WordDictionaryMaster {

    private static class TrieNode {
        private final TrieNode[] children = new TrieNode[26];
        private boolean isEndOfWord = false;
    }

    private final TrieNode root;

    public WordDictionaryMaster() {
        this.root = new TrieNode();
    }

    // Add word O(L) Time, O(L * R) Space
    public void addWord(String word) {
        if (word == null || word.isEmpty()) return;

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

    // Search word (supports wildcard '.') O(L) Best, O(R^L) Worst Time
    public boolean search(String word) {
        if (word == null) return false;
        return dfsSearch(word, 0, root);
    }

    private boolean dfsSearch(String word, int index, TrieNode curr) {
        if (curr == null) return false;

        // Base Case: All characters processed
        if (index == word.length()) {
            return curr.isEndOfWord;
        }

        char c = word.charAt(index);

        if (c != '.') {
            // Case 1: Exact Character Match
            int idx = c - 'a';
            return dfsSearch(word, index + 1, curr.children[idx]);
        } else {
            // Case 2: Wildcard '.' -> Branch to ALL non-null children
            for (int i = 0; i < 26; i++) {
                if (curr.children[i] != null) {
                    if (dfsSearch(word, index + 1, curr.children[i])) {
                        return true; // Match found along this branch!
                    }
                }
            }
            return false; // No branch matched
        }
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 211 Wildcard DFS Loop Line
if (c == '.') { for (int i=0; i<26; i++) if (curr.children[i] != null && dfsSearch(word, index+1, curr.children[i])) return true; }
```

---

## 7. Concrete Problem Examples
* **LeetCode 211 - Design Add and Search Words Data Structure**: Primary wildcard search problem.
* **Regex Pattern Matching**: Simple wildcard string matching engines.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `WordDictionaryMaster` (LeetCode 211):

```java
public class WordDictionaryDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 211 Wildcard Search Test ===");
        WordDictionaryMaster dict = new WordDictionaryMaster();

        dict.addWord("bad");
        dict.addWord("dad");
        dict.addWord("mad");

        System.out.println("Search 'pad': " + dict.search("pad")); // Output: false
        System.out.println("Search 'bad': " + dict.search("bad")); // Output: true
        System.out.println("Search '.ad': " + dict.search(".ad")); // Output: true (Matches "bad", "dad", "mad")
        System.out.println("Search 'b..': " + dict.search("b..")); // Output: true (Matches "bad") ✅
    }
}
```

---

## 9. Complexity Analysis

| Search Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Exact Word Search** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|
| **Prefix Search** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(1)$ Constant ⚡**|
| **Wildcard Search (211)**| **$O(L)$ Linear ⚡** | $O(R \cdot L)$ Average | $O(R^L)$ (All Dots) | $O(L)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Pattern All Dots (`"..."`)**: Searches all words of length 3 via full DFS recursion.
* **Index Exceeds Word Length**: Guarded by `index == word.length()` base case.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Null Check in Wildcard Loop**:
  - Calling `dfsSearch` on `curr.children[i]` without checking `curr.children[i] != null` causes `NullPointerException`.
  - **Always check `if (curr.children[i] != null)` before recursing**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Backtracking DFS is Mandatory for LeetCode 211:
> A single wildcard `'.'` can match 26 different possible characters.
> Because multiple branches could potentially match remaining characters of the pattern, we MUST use **Backtracking Depth-First Search (DFS)** to explore candidate branches until a valid word match is found or all branches return `false`.

> **Memory Trick:** **"LeetCode 211: Use DFS for wildcard '.'! Return true immediately when any branch succeeds!"**

---

## 13. System & Implementation Comparisons

| Feature | Exact Trie Search | Wildcard DFS Trie Search |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(L)$ Strict Linear ⚡** | $O(R^L)$ Exponential Worst Case |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(L)$ Call Stack Space |
| **Branching Factor**| Single Pointer Follow | Multiple DFS Branches |

---

## 14. How to Recognize This in Questions
* **"Design word dictionary supporting wildcard search with '.'"** $\rightarrow$ LeetCode 211 (Trie DFS).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the time complexity of searching pattern `".a."` in a Trie of lowercase English words?**  
  *A:* Worst case $O(26^2 \cdot L) = O(R^2 \cdot L)$ because each `'.'` branches into 26 possible children.
* **Q: Can wildcard search be written iteratively?**  
  *A:* It can be written using an explicit stack or queue (BFS), but recursive DFS is significantly cleaner and consumes less auxiliary memory.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE SEARCH & WILDCARD MATCHING (LEETCODE 211)        |
+-----------------------------------------------------------------------+
| • Exact Search   : O(L) time (Follow idx = c - 'a' until isEnd)       |
| • Wildcard Search: DFS recursion with index parameter                 |
| • If char != '.' : Recurse into children[c - 'a']                     |
| • If char == '.' : Loop i=0..25; if children[i]!=null recurse;        |
|                    return true if any child succeeds!                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 211 (`WordDictionary`) in Java.
- [ ] I can write the DFS recursive helper for wildcard matching.
- [ ] I know why wildcard search requires backtracking.
- [ ] I can state the time complexity of exact vs wildcard search.
- [ ] I can trace wildcard matching on `"a.c"` step by step.
