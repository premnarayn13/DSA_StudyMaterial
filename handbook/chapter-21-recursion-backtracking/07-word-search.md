# 07. Word Search, Grid Backtracking & Trie Prefix Pruning Engines

## 1. Introduction
**Word Search I** (LeetCode 79) and **Word Search II** (LeetCode 212) combine 2D grid navigation with **Backtracking** and **Trie (Prefix Tree) Pruning**. Word Search I checks if a target word exists in a 2D character grid by exploring 4 orthogonal directions using **In-Place Character Masking (`board[r][c] = '#'`)** to prevent cell re-use. Word Search II searches for multiple words simultaneously by integrating a **Trie Prefix Tree** into the grid backtracking search, executing in **$O(M \cdot N \cdot 3^L)$ Time** and **$O(L)$ Stack Memory Space**.

> **Important:** Core Invariants of Word Search & Trie Integration:
> 1. **In-Place Visited Character Masking**:
>    - Store original character: `char temp = board[r][c]`.
>    - Mask visited cell in-place: `board[r][c] = '#'`.
>    - Recurse 4 directions: $(r+1, c), (r-1, c), (r, c+1), (r, c-1)$.
>    - **BACKTRACK**: Restore `board[r][c] = temp`!
> 2. **Word Search II Trie Pruning Invariant (LeetCode 212)**:
>    - If current grid cell character does NOT match any child node in the Trie (`node.children[ch - 'a'] == null`), **PRUNE THE ENTIRE SEARCH BRANCH IMMEDIATELY**!
>    - When a word is found, set `node.word = null` to avoid duplicate results! ⚡

```
Word Search I 4-Directional Backtracking Topography:
Target Word: "ABCCED"
Grid at (0, 0) 'A' ---> Recurse Right (0, 1) 'B' ---> Recurse Down (1, 1) 'C' ---> Recurse Down (2, 1) 'C'...
Cell Masking: board[0][0] = '#' -> board[0][1] = '#' -> board[1][1] = '#' (Restored on return!). ⚡
```

---

## 2. Core Concepts & Word Search I vs Word Search II Strategy Matrix

### 2.1 Word Search Strategy Matrix
```
Word Search Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Search Scope      | Primary Structure | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Word Search I (79)**| Single Word       | In-Place Masking  | **$O(M \cdot N \cdot 3^L)$ ⚡**|
| **Word Search II (212)**| Multiple Words   | **Trie + Grid DFS ⚡**| **$O(M \cdot N \cdot 3^L)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Word Search: Mask cell with '#' -> Recurse 4 dirs -> Restore board[r][c] = temp! Trie prunes bad prefixes!"**

---

## 3. Characteristics & $O(M \cdot N \cdot 3^L)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(M \cdot N \cdot 3^L)$ Complexity
* There are $M \times N$ starting cell origins on the grid.
* From the second character onward, each step branches into at most 3 directions (since we cannot backtrack to the immediate parent cell).
* For a word of length $L$, the maximum search depth is $L$.
* Total Time Complexity: $\mathbf{O(M \cdot N \cdot 3^L) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Word Search I on Grid for Word "SEE":

```
Grid:
['A','B','C','E']
['S','F','C','S']
['A','D','E','E']

1. Outer loop finds 'S' at (1, 0). Launch dfs(1, 0, index = 0):
- Character matches 'S'! Save temp = 'S', mask board[1][0] = '#'.
- Recurse 4 directions for 'E' (index = 1):
  - (2, 0) 'A' != 'E' -> Fail.
  - (0, 0) 'A' != 'E' -> Fail.
  - (1, 1) 'F' != 'E' -> Fail.
  - All fail! Restore board[1][0] = 'S'. Return false.

2. Outer loop finds 'S' at (1, 3). Launch dfs(1, 3, index = 0):
- Character matches 'S'! Save temp = 'S', mask board[1][3] = '#'.
- Recurse Down to (2, 3) 'E': Matches 'E'! Save temp = 'E', mask board[2][3] = '#'.
  - Recurse Left to (2, 2) 'E': Matches 'E'! Index == word.length - 1 -> FOUND WORD!
  - Restore board[2][3] = 'E', restore board[1][3] = 'S'.

Returns true! ✅ (O(M * N * 3^L) Time!)
```

---

## 5. Visual Diagram
Grid In-Place Character Masking Topography:

```
Before Step:                    During Step (Masked!):            After Return (Restored!):
['S', 'F', 'C', 'S']            ['#', 'F', 'C', 'S']              ['S', 'F', 'C', 'S']
['A', 'D', 'E', 'E']    ====>   ['A', 'D', 'E', 'E']     ====>    ['A', 'D', 'E', 'E']
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 79 (Word Search I) and LeetCode 212 (Word Search II using Trie):

```java
import java.util.*;

// LeetCode 79 & 212: Word Search & Trie Integration Master
public class WordSearchMaster {

    // 1. LeetCode 79: Word Search I (Single Word Search) O(M * N * 3^L) Time
    public boolean exist(char[][] board, String word) {
        if (board == null || board.length == 0 || word == null) return false;

        int rows = board.length;
        int cols = board[0].length;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (board[r][c] == word.charAt(0)) {
                    if (dfsSearch(board, word, r, c, 0)) {
                        return true; // Word found!
                    }
                }
            }
        }

        return false;
    }

    private boolean dfsSearch(char[][] board, String word, int r, int c, int index) {
        if (index == word.length()) {
            return true; // Complete word matched!
        }

        // Boundary Check & Character Match Guard
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] != word.charAt(index)) {
            return false;
        }

        // Step 1: Save character & Mask cell in-place
        char temp = board[r][c];
        board[r][c] = '#';

        // Step 2: Recurse in 4 orthogonal directions
        boolean found = dfsSearch(board, word, r + 1, c, index + 1) ||
                        dfsSearch(board, word, r - 1, c, index + 1) ||
                        dfsSearch(board, word, r, c + 1, index + 1) ||
                        dfsSearch(board, word, r, c - 1, index + 1);

        // Step 3: BACKTRACK (Restore original character)
        board[r][c] = temp;

        return found;
    }

    // 2. LeetCode 212: Word Search II (Trie + Grid DFS) O(M * N * 3^L) Time
    private static class TrieNode {
        private final TrieNode[] children = new TrieNode[26];
        private String word = null;
    }

    public List<String> findWords(char[][] board, String[] words) {
        List<String> result = new ArrayList<>();
        if (board == null || words == null) return result;

        // Step 1: Build Trie from list of words
        TrieNode root = new TrieNode();
        for (String w : words) {
            TrieNode node = root;
            for (char ch : w.toCharArray()) {
                int idx = ch - 'a';
                if (node.children[idx] == null) {
                    node.children[idx] = new TrieNode();
                }
                node = node.children[idx];
            }
            node.word = w; // Store complete word at leaf node
        }

        // Step 2: Grid DFS with Trie Pruning
        int rows = board.length;
        int cols = board[0].length;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dfsTrie(board, r, c, root, result);
            }
        }

        return result;
    }

    private void dfsTrie(char[][] board, int r, int c, TrieNode node, List<String> result) {
        if (r < 0 || r >= board.length || c < 0 || c >= board[0].length || board[r][c] == '#') {
            return;
        }

        char ch = board[r][c];
        int idx = ch - 'a';
        if (node.children[idx] == null) {
            return; // Trie Pruning: Character does not exist in any word prefix!
        }

        node = node.children[idx];

        if (node.word != null) {
            result.add(node.word); // Found word!
            node.word = null;      // Deduplicate: Prevent adding same word multiple times
        }

        board[r][c] = '#'; // Mask cell

        dfsTrie(board, r + 1, c, node, result);
        dfsTrie(board, r - 1, c, node, result);
        dfsTrie(board, r, c + 1, node, result);
        dfsTrie(board, r, c - 1, node, result);

        board[r][c] = ch; // Backtrack (Restore character)
    }
}
```

> **Quick Syntax:**
```java
// In-Place Masking & Restoring Lines
char temp = board[r][c]; board[r][c] = '#';
boolean found = dfs(r+1, c) || dfs(r-1, c) || dfs(r, c+1) || dfs(r, c-1);
board[r][c] = temp; // Restored!
```

---

## 7. Concrete Problem Examples
* **LeetCode 79 - Word Search**: Single word grid backtracking.
* **LeetCode 212 - Word Search II**: Trie prefix tree grid search.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 79 `exist`:

```java
public class WordSearchDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 79 Word Search Test ===");
        WordSearchMaster solver = new WordSearchMaster();

        char[][] board = {
            {'A','B','C','E'},
            {'S','F','C','S'},
            {'A','D','E','E'}
        };

        System.out.println("Does 'ABCCED' exist? " + solver.exist(board, "ABCCED")); // Output: true
        System.out.println("Does 'SEE' exist?    " + solver.exist(board, "SEE"));    // Output: true
        System.out.println("Does 'ABCB' exist?   " + solver.exist(board, "ABCB"));   // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Word Search I (79)**| **$O(M \cdot N \cdot 3^L)$ Time ⚡**| **$O(L)$ Stack Memory**| In-place cell masking `board[r][c] = '#'` |
| **Word Search II (212)**| **$O(M \cdot N \cdot 3^L)$ Time ⚡**| **$O(K \cdot L)$ Trie Space**| Trie prefix pruning `node.children[idx] == null` |

---

## 10. Edge Cases & Boundary Handling
* **Word Length Exceeds Total Cells ($L > M \times N$)**: Returns `false` immediately.
* **Single Cell Board (`1 x 1`)**: Evaluates safely in $O(1)$ time.

---

## 11. Common Mistakes & Anti-Patterns
* **Allocating an Explicit `boolean[][] visited` Array for Word Search**:
  - Allocating a `visited` array creates unnecessary heap objects per starting cell.
  - **ALWAYS use in-place masking `board[r][c] = '#'` for $O(1)$ auxiliary space**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `node.word = null` Is Essential in LeetCode 212:
> In Word Search II, the same word can be reached via different grid paths.
> Setting `node.word = null` immediately after adding it to the result list prevents adding duplicate copies of the word to the output! ⚡

> **Memory Trick:** **"Word Search II: Set node.word = null after finding word to eliminate duplicate results!"**

---

## 13. System & Implementation Comparisons

| Feature | Word Search I (LeetCode 79) | Word Search II (LeetCode 212) |
| :--- | :--- | :--- |
| **Search Mechanism** | Backtracking DFS per word | **Trie Prefix Tree + Grid DFS ⚡** |
| **Multi-Word Search** | $W \times O(M \cdot N \cdot 3^L)$ (Slow) | **Single Pass $O(M \cdot N \cdot 3^L)$ ⚡** |
| **Pruning Technique**| Character Match Guard | Trie Node Null Guard |

---

## 14. How to Recognize This in Questions
* **"Search for word or list of words in 2D character matrix"** $\rightarrow$ LeetCode 79 / 212.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Word Search use 3 branch directions instead of 4 after the start cell?**  
  *A:* Because the immediate parent cell is masked (`'#'`), preventing the search from stepping backward.
* **Q: How does Trie integration speed up LeetCode 212?**  
  *A:* If a grid path forms a prefix not present in the Trie (`node.children[idx] == null`), the search prunes that branch immediately without testing further cells.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: WORD SEARCH & TRIE INTEGRATION                        |
+-----------------------------------------------------------------------+
| • In-Place Mask : Save char temp = board[r][c]; board[r][c] = '#';    |
| • Backtrack Reset: board[r][c] = temp;                                |
| • 4 Directions  : Recurse (r+1,c), (r-1,c), (r,c+1), (r,c-1)          |
| • Trie Pruning  : if (node.children[ch - 'a'] == null) return; (212)  |
| • Performance   : O(M * N * 3^L) Time | O(L) Stack Memory Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 79 (`Word Search I`) in Java.
- [ ] I can write LeetCode 212 (`Word Search II`) using a Trie.
- [ ] I know why in-place masking `board[r][c] = '#'` saves memory.
- [ ] I know why `node.word = null` prevents duplicate output.
- [ ] I can trace grid backtracking step by step.
