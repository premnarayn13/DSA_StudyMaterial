# 05. Trie Deletion Mechanics, Bottom-Up Post-Order Pruning & Memory Recovery

## 1. Introduction
Deleting a word from a **Trie** requires removing the target key while preserving all other words that share common prefixes or suffixes with it. Unlike insertion (which operates top-down), Trie deletion requires a **Bottom-Up Post-Order Traversal** to prune orphan nodes that are no longer part of any valid word. Trie deletion operates in **$O(L)$ Strict Linear Time** (where $L$ is word length) and **$O(L)$ Auxiliary Call Stack Space**.

> **Important:** The 3 Structural Conditions of Trie Word Deletion:
> 1. **Condition 1: Deleted Word is a Prefix of Other Words (e.g. deleting `"app"` when `"apple"` exists)**:
>    - Simply set `curr.isEndOfWord = false`! ZERO nodes are deleted!
> 2. **Condition 2: Deleted Word Shares Prefixes with Other Words (e.g. deleting `"apple"` when `"app"` exists)**:
>    - Prune nodes bottom-up from `'e'` back to `'l'`, stopping at `'p'` because `curr.isEndOfWord == true`!
> 3. **Condition 3: Deleted Word Has No Common Path (Unique Word)**:
>    - Prune all nodes from leaf back up to `root`! ⚡

```
Trie Bottom-Up Post-Order Pruning Topology:
Deleting "apple" when "app" exists:
Step 1: Traverse down to 'e' (isEnd=true). Set isEnd = false.
Step 2: Post-Order Check 'e' ----> Has 0 children & isEnd=false -> Prune 'e'! (Return null)
Step 3: Post-Order Check 'l' ----> Has 0 children & isEnd=false -> Prune 'l'! (Return null)
Step 4: Post-Order Check 'p' ----> isEnd is TRUE ("app") -> STOP PRUNING! Return 'p'! ⚡
```

---

## 2. Core Concepts & Post-Order Recursion Architecture

### 2.1 Post-Order Pruning Algorithm
To delete `word` starting at `index` from node `curr`:
1. Base Case: If `curr == null`, return `null` (Word not in Trie).
2. If `index == word.length()`:
   - If `!curr.isEndOfWord`: Return `curr` (Word not present in Trie).
   - Set `curr.isEndOfWord = false` (Unmark word termination!).
3. Else (`index < word.length()`):
   - `int idx = word.charAt(index) - 'a'`.
   - `curr.children[idx] = deleteHelper(word, index + 1, curr.children[idx])`.
4. **Post-Order Node Removal Invariant**:
   - Check if `curr` has any non-null children: `boolean hasChildren = checkChildren(curr)`.
   - If `!curr.isEndOfWord && !hasChildren`: Return `null` (Prune this node from memory!).
   - Else: Return `curr` (Retain this node!).

```
Trie Deletion Condition Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Structural Case       | Node Status       | Pruning Action    | Node Allocation   |
+-----------------------+-------------------+-------------------+-------------------+
| **Prefix of Other**   | Has children      | `isEnd = false`   | **0 Nodes Deleted ⚡**|
| **Shares Prefix**     | End node reached  | Prune suffix links| Prune suffix nodes|
| **Unique Key**        | 0 Children, !isEnd| Full Path Prune   | Prune all nodes   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Trie Delete: Traverse down to end; set isEnd = false; prune node bottom-up IF !isEnd && hasNoChildren!"**

---

## 3. Characteristics & Post-Order Memory Recovery

### 3.1 Memory Recovery Property
Post-order recursion evaluates child pointers after returning from deeper call frames. This guarantees that a parent node is pruned IF AND ONLY IF all of its children have already been pruned and it is not a valid word end point!

---

## 4. Internal Working Mechanics
Tracing Deletion of `"car"` from Trie containing `"cat"` and `"car"`:

```
Trie: root -> 'c' -> 'a' -> split ('t' isEnd, 'r' isEnd).

Delete "car":
1. Traverse down path 'c' -> 'a' -> 'r'.
2. Node 'r': set isEnd = false. Node 'r' has 0 children -> Prune 'r'! (Node 'a'.children['r'] becomes null).
3. Return to Node 'a': Node 'a' STILL HAS CHILD 't'! (hasChildren = true).
   - Node 'a' CANNOT BE PRUNED! Return Node 'a'.
4. Return to Node 'c': Has child 'a' -> Return Node 'c'.

Result: "car" deleted, "cat" preserved perfectly! ✅ (O(L) Time, O(L) Space!)
```

---

## 5. Visual Diagram
Trie Deletion Bottom-Up Pruning Topography:

```
Before Deleting "apple":                      After Deleting "apple" ("app" preserved):
       [ Root ]                                      [ Root ]
          | 'a'                                         | 'a'
       [ Node ]                                      [ Node ]
          | 'p'                                         | 'p'
       [ Node ]                                      [ Node ]
          | 'p'                                         | 'p'
 [ Node ("app") ]                              [ Node ("app") ]  <--- Pruning Stops Here!
       \ 'l'                                      (Node 'l' and 'e' pruned!)
     [ Node ]
        \ 'e'
  [ Node ("apple") ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Trie Deletion with bottom-up post-order pruning:

```java
import java.util.*;

public class TrieDeleteMaster {

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

    public TrieDeleteMaster() {
        this.root = new TrieNode();
    }

    public void insert(String word) {
        if (word == null || word.isEmpty()) return;
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
            curr = curr.children[idx];
        }
        curr.isEndOfWord = true;
    }

    public boolean search(String word) {
        TrieNode node = find(word);
        return node != null && node.isEndOfWord;
    }

    private TrieNode find(String str) {
        TrieNode curr = root;
        for (char c : str.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }

    // Full Trie Deletion Algorithm O(L) Time, O(L) Auxiliary Stack Space
    public boolean delete(String word) {
        if (word == null || word.isEmpty()) return false;
        return deleteHelper(root, word, 0);
    }

    private boolean deleteHelper(TrieNode curr, String word, int index) {
        if (curr == null) return false; // Key not in Trie

        // Base Case: All characters processed
        if (index == word.length()) {
            if (!curr.isEndOfWord) return false; // Word does not exist
            curr.isEndOfWord = false; // Condition 1: Unmark word end
            return true;
        }

        int idx = word.charAt(index) - 'a';
        boolean deleted = deleteHelper(curr.children[idx], word, index + 1);

        if (deleted) {
            // Post-Order Pruning Check: If child became empty, prune pointer!
            TrieNode child = curr.children[idx];
            if (child != null && !child.isEndOfWord && !hasChildren(child)) {
                curr.children[idx] = null; // Prune child node from memory
            }
            return true;
        }

        return false;
    }

    // Helper: Check if node has any non-null children
    private boolean hasChildren(TrieNode node) {
        for (int i = 0; i < 26; i++) {
            if (node.children[i] != null) return true;
        }
        return false;
    }

    public TrieNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// Post-Order Pruning Check Line
if (child != null && !child.isEndOfWord && !hasChildren(child)) curr.children[idx] = null;
```

---

## 7. Concrete Problem Examples
* **Dynamic Vocabulary Management**: Removing terms from a Trie dictionary.
* **Auto-complete Index Eviction**: Pruning expired search suggestions.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Trie Deletion across all 3 deletion cases:

```java
public class TrieDeleteDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Trie Word Deletion Test ===");
        TrieDeleteMaster trie = new TrieDeleteMaster();

        trie.insert("app");
        trie.insert("apple");
        trie.insert("car");

        System.out.println("Deleting 'apple' (Condition 2: 'app' preserved)...");
        trie.delete("apple");

        System.out.println("Search 'apple': " + trie.search("apple")); // Output: false
        System.out.println("Search 'app':   " + trie.search("app"));   // Output: true

        System.out.println("\nDeleting 'app' (Condition 1: isEnd set false)...");
        trie.delete("app");
        System.out.println("Search 'app':   " + trie.search("app"));   // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Deletion Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Delete Word ($L$)** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** | $O(L)$ Call Stack Space |
| **`hasChildren(node)`**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(1)$ Auxiliary Space |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Non-Existent Word**: Returns `false` safely without modifying Trie topology.
* **Deleting Single Word in Trie**: Prunes all nodes back up to `root`.

---

## 11. Common Mistakes & Anti-Patterns
* **Pruning Nodes Top-Down Instead of Bottom-Up**:
  - Top-down deletion cannot know whether a node is shared by deeper words until the end of the word is reached.
  - **ALWAYS use bottom-up post-order recursion to evaluate `hasChildren`**.
* **Pruning Nodes with `isEndOfWord == true`**:
  - Pruning a node that represents another valid word (e.g. pruning `'p'` when deleting `"apple"`) destroys the word `"app"`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The Pruning Safety Rule:
> A Trie node `curr` can be pruned (`curr = null`) IF AND ONLY IF it satisfies TWO conditions simultaneously:
> 1. `!curr.isEndOfWord` (It is not the end of another valid word!).
> 2. `!hasChildren(curr)` (It has zero active child branches!).
> If either condition fails, `curr` MUST be preserved in memory!

> **Memory Trick:** **"Prune node IF AND ONLY IF !isEndOfWord AND !hasChildren!"**

---

## 13. System & Implementation Comparisons

| Feature | Post-Order Recursive Deletion | Iterative Deletion with Parent Stack |
| :--- | :--- | :--- |
| **Implementation** | **Clean Post-Order Logic ⚡** | Requires Explicit Stack Array |
| **Memory Recovery**| Automatic via recursion return | Manual stack pop & nulling |
| **Time Complexity** | **$O(L)$ Linear ⚡** | **$O(L)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Remove a word from a Trie dictionary while preserving prefix sharing"** $\rightarrow$ Trie Deletion.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Trie deletion use post-order recursion?**  
  *A:* Because post-order recursion evaluates child pointers *after* returning from deeper call frames, allowing nodes with 0 remaining children to be pruned bottom-up.
* **Q: What happens when you delete `"app"` when `"apple"` is present?**  
  *A:* `isEndOfWord` of node `'p'` is set to `false`, but node `'p'` is NOT deleted because it has child `'l'`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TRIE DELETION MECHANICS                               |
+-----------------------------------------------------------------------+
| • Search Down  : Recursively traverse down to index == word.length()  |
| • Mark False   : Set target node curr.isEndOfWord = false             |
| • Post-Order Pruning Rule: Prune node IF !curr.isEndOfWord && !hasChildren|
| • Time Bounds  : O(L) Linear Time where L is word length ⚡            |
| • Safety Rule  : NEVER prune nodes representing other valid words!     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Trie Deletion with post-order pruning in Java.
- [ ] I can state the 3 structural conditions of Trie deletion.
- [ ] I know why post-order recursion is required for pruning.
- [ ] I know the 2 simultaneous conditions required to safely prune a node.
- [ ] I can trace deletion of `"apple"` vs `"app"` step by step.
