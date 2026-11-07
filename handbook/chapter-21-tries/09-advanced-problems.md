# 09. Advanced Trie Problems: Word Search II (LeetCode 212) & Stream Matchers

## 1. Introduction
**Advanced Trie Problems** represent the pinnacle of string algorithmic design, combining Trie data structures with **2D Grid Backtracking DFS**, **Reverse Stream Matchers**, and **Prefix Pruning Engines**. Problems like **Word Search II (LeetCode 212)**, **Replace Words (LeetCode 648)**, and **Stream of Characters (LeetCode 1032 - Reverse Trie Stream Matcher)** execute in **$O(M \cdot N \cdot 3^L)$ or $O(L)$ time** by leveraging Tries to prune millions of dead search paths on 2D grids and stream buffers.

> **Important:** Why Tries Optimize Grid Search (LeetCode 212 - Word Search II):
> Standard DFS grid search for $K$ words runs $K$ separate grid searches ($O(K \cdot M \cdot N \cdot 4^L)$ TLE penalty!).
> **Trie Optimization Strategy**: Insert all $K$ words into a SINGLE Trie. Run ONE unified 2D grid DFS pass, checking grid paths against Trie nodes!
> If a grid path is NOT a valid prefix in the Trie (`curr.children[c - 'a'] == null`), **PRUNE THE DFS BRANCH IMMEDIATELY**! ⚡

```
Word Search II (LeetCode 212) Unified Trie Grid Search Topology:
Grid:                             Trie (Words: "oath", "pea", "eat", "rain"):
[ 'o', 'a', 'a', 'n' ]                      [ Root ]
[ 'e', 't', 'a', 'e' ]                     /   |    \
[ 'i', 'h', 'k', 'r' ]               'o'  /    | 'p'\ 'e'
[ 'i', 'f', 'l', 'v' ]             [Node]   [Node]  [Node]

Grid DFS starting at 'o' matches Trie path 'o' -> 'a' -> 't' -> 'h' ("oath") in ONE PASS! ⚡
```

---

## 2. Core Concepts & LeetCode 212 Word Search II Engine

### 2.1 LeetCode 212 Trie Grid DFS Algorithm
1. Insert all `words` into a Trie.
2. For memory optimization, store `node.word = word` directly at terminal nodes (`isEndOfWord`), eliminating string concatenation during DFS!
3. Iterate over every cell `(r, c)` in the $M \times N$ grid:
   - Call `dfs(grid, r, c, root, result)`.
4. Inside `dfs(grid, r, c, currNode, result)`:
   - Boundary Check: If out of bounds or `grid[r][c] == '#'` (visited cell): Return.
   - Character Check: `char ch = grid[r][c]`. `int idx = ch - 'a'`.
   - **Trie Prefix Pruning**: If `currNode.children[idx] == null`: **PRUNE BRANCH IMMEDIATELY**!
   - Move `currNode = currNode.children[idx]`.
   - **Match Check**: If `currNode.word != null`:
     - Add `currNode.word` to `result`.
     - Set `currNode.word = null` (Prevents duplicate word additions!).
   - Mark visited: `grid[r][c] = '#'`.
   - Recurse in 4 directions: `(r+1, c), (r-1, c), (r, c+1), (r, c-1)`.
   - Backtrack: `grid[r][c] = ch`.

```
Advanced Trie Pattern Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Word Search II (212)**| Unified Trie Grid | **$O(M \cdot N \cdot 3^L)$ ⚡**| $O(K \cdot L)$ Trie|
| **Replace Words (648)**| Shortest Root Fix | **$O(\sum L_i)$ Linear ⚡**| $O(N \cdot L)$ Trie|
| **Stream Characters (1032)**| Reverse Trie Stream| **$O(L_{\max})$ per query ⚡**| $O(\sum L_i)$ Trie|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 212: Insert words into Trie; store word string at leaf nodes; prune grid DFS if children[c - 'a'] == null!"**

---

## 3. Characteristics & Reverse Trie Stream Matching (LeetCode 1032)

### 3.1 Reverse Trie Stream Matching (LeetCode 1032)
Given a stream of characters queried one by one: check if any suffix of the stream matches a word in the dictionary:
* **Key Insight**: Build a Trie with words inserted **IN REVERSE ORDER**!
* Maintain a character stream buffer `StringBuilder`.
* For query `query(char c)`:
  - Append `c` to buffer.
  - Search buffer backwards from newest to oldest character in the Reverse Trie.
  - Return `true` if any `isEndOfWord == true` node is reached in $O(L_{\max})$ time! ⚡

---

## 4. Internal Working Mechanics
Tracing Word Search II (LeetCode 212) on Grid `['o','a'], ['t','h']` with Words `["oath", "cat"]`:

```
Trie contains "oath" and "cat".

Start DFS at cell (0, 0) = 'o':
- 'o' exists in Trie root.children['o'-'a']. Move to Node('o').
- Neighbor (0, 1) = 'a': Node('o').children['a'-'a'] exists. Move to Node('oa').
- Neighbor (1, 1) = 'h': Node('oa').children['h'-'a'] is NULL! -> PRUNE 'h'!
- Neighbor (1, 0) = 't': Node('oa').children['t'-'a'] exists. Move to Node('oat').
- Neighbor (1, 1) = 'h': Node('oat').children['h'-'a'] exists. Move to Node('oath').
  - Node('oath').word == "oath" -> MATCH FOUND! Add "oath" to result!

Total DFS operations = 5 cell steps! (Skipped thousands of invalid paths!) ✅
```

---

## 5. Visual Diagram
Word Search II Trie Grid DFS & Subtree Node Pruning Topography:

```
Grid Cell (r, c) = 'o' ----> Trie Root.children['o'-'a'] (Valid Prefix Node)
      |
Grid Cell (r+1, c) = 't' --> Trie Node.children['t'-'a'] (Valid Prefix Node)
      |
Grid Cell (r+2, c) = 'x' --> Trie Node.children['x'-'a'] is NULL! 
                             PRUNE DFS BRANCH IMMEDIATELY! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 212 (Word Search II) using Trie-optimized grid backtracking DFS:

```java
import java.util.*;

// LeetCode 212: Word Search II
public class AdvancedTrieProblemsMaster {

    private static class TrieNode {
        private final TrieNode[] children = new TrieNode[26];
        private String word = null; // Store complete word string at terminal node
    }

    // LeetCode 212 Solution O(M * N * 3^L) Time, O(K * L) Space
    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        if (board == null || board.length == 0 || words == null || words.length == 0) {
            return result;
        }

        // Step 1: Build Trie with terminal word storing
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode curr = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (curr.children[idx] == null) {
                    curr.children[idx] = new TrieNode();
                }
                curr = curr.children[idx];
            }
            curr.word = word; // Store word at terminal node
        }

        // Step 2: Unified 2D Grid Backtracking DFS
        int rows = board.length;
        int cols = board[0].length;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dfs(board, r, c, root, result);
            }
        }

        return result;
    }

    private void dfs(char[][] board, int r, int c, TrieNode curr, List<String> result) {
        // Boundary Check & Visited Check ('#')
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] == '#') {
            return;
        }

        char ch = board[r][c];
        int idx = ch - 'a';

        // Step 3: Trie Prefix Pruning (If path not in Trie, return immediately!)
        if (curr.children[idx] == null) {
            return;
        }

        curr = curr.children[idx];

        // Step 4: Word Match Check
        if (curr.word != null) {
            result.add(curr.word);
            curr.word = null; // Set null to prevent adding duplicate words!
        }

        // Step 5: Mark visited & Explore 4 Directions
        board[r][c] = '#';

        dfs(board, r + 1, c, curr, result);
        dfs(board, r - 1, c, curr, result);
        dfs(board, r, c + 1, curr, result);
        dfs(board, r, c - 1, curr, result);

        // Step 6: Backtrack
        board[r][c] = ch;
    }
}
```

> **Quick Syntax:**
```java
// Word Search II Match & Deduplication Line
if (curr.word != null) { result.add(curr.word); curr.word = null; }
```

---

## 7. Concrete Problem Examples
* **LeetCode 212 - Word Search II**: Core Trie + Grid DFS problem.
* **LeetCode 648 - Replace Words**: Shortest root prefix replacement.
* **LeetCode 1032 - Stream of Characters**: Reverse Trie stream matching.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 212 `findWords`:

```java
public class AdvancedTrieProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 212 Word Search II Test ===");
        AdvancedTrieProblemsMaster solver = new AdvancedTrieProblemsMaster();

        char[][] board = {
            {'o','a','a','n'},
            {'e','t','a','e'},
            {'i','h','k','r'},
            {'i','f','l','v'}
        };
        String[] words = {"oath","pea","eat","rain"};

        List<String> matchedWords = solver.findWords(board, words);
        System.out.println("Matched Words in Grid: " + matchedWords);
        // Output: ["oath", "eat"] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Word Search II (212)**| **$O(M \cdot N \cdot 3^L)$ ⚡** | $O(K \cdot L)$ Trie Space | Trie prefix pruning on grid DFS |
| **Replace Words (648)** | **$O(\sum L_i)$ Linear ⚡** | $O(N \cdot L)$ Trie Space | Shortest root match in Trie |
| **Stream Characters (1032)**| **$O(L_{\max})$ per query ⚡**| $O(\sum L_i)$ Trie Space | Reverse Trie stream search |

---

## 10. Edge Cases & Boundary Handling
* **Grid Contains Duplicate Paths to Same Word**: Handled by setting `curr.word = null` after adding to `result`.
* **Single Cell Board**: Evaluated safely by boundary checks.

---

## 11. Common Mistakes & Anti-Patterns
* **Running Separate Grid Searches for Each Word (TLE)**:
  - Running standard LeetCode 79 `exist(word)` $K$ times takes $O(K \cdot M \cdot N \cdot 4^L)$ time and TLEs.
  - **Insert all words into a single Trie and run ONE unified grid DFS**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `curr.word = null` Deduplicates Results:
> In LeetCode 212, a word like `"oath"` might be formable via multiple distinct paths on the grid.
> After matching `"oath"` the first time, setting `curr.word = null` ensures subsequent paths that reach the same terminal node skip adding duplicate copies to `result`!

> **Memory Trick:** **"Set curr.word = null after matching to prevent duplicate words in result!"**

---

## 13. System & Implementation Comparisons

| Feature | Trie-Optimized Grid DFS (LeetCode 212) | Independent Word Searches |
| :--- | :--- | :--- |
| **Search Traversal** | **1 Unified Grid DFS Pass ⚡** | $K$ Independent Grid Searches |
| **Time Complexity** | **$O(M \cdot N \cdot 3^L)$ Optimal ⚡** | $O(K \cdot M \cdot N \cdot 4^L)$ (TLE) |
| **Pruning Power** | Prunes non-prefix paths instantly | No prefix pruning |

---

## 14. How to Recognize This in Questions
* **"Find all dictionary words present in a 2D character grid"** $\rightarrow$ LeetCode 212 (Trie + Grid DFS).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Word Search II store string `word` at terminal Trie nodes?**  
  *A:* Storing `word` directly at terminal nodes eliminates string building/concatenation overhead during grid DFS recursion.
* **Q: How does LeetCode 1032 (Stream of Characters) work?**  
  *A:* Words are inserted into the Trie IN REVERSE. Stream queries search backwards from the latest buffer character into the Reverse Trie.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED TRIE PROBLEMS (LEETCODE 212)                 |
+-----------------------------------------------------------------------+
| • Step 1: Insert all words into Trie; store word string at leaves     |
| • Step 2: Unified Grid DFS starting at every cell (r, c)              |
| • Step 3: Trie Pruning: If curr.children[ch - 'a'] == null -> RETURN! |
| • Step 4: Deduplicate: If curr.word != null -> add & set word = null  |
| • Step 5: Mark board[r][c] = '#' -> Recurse 4 directions -> Backtrack  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 212 (`WordSearch II`) in Java.
- [ ] I can explain why Trie prefix pruning optimizes grid DFS.
- [ ] I know why `curr.word = null` prevents duplicate matches.
- [ ] I can write LeetCode 1032 (`Stream of Characters`) using a Reverse Trie.
- [ ] I can trace Trie grid DFS step by step.
