# 13. Skip List Data Structure & Probabilistic Indexing

## 1. Introduction
A **Skip List** is a probabilistic data structure that enhances a sorted linked list by building a hierarchy of express forward pointer layers. Invented by William Pugh, a Skip List achieves **$O(\log N)$ average-case search, insertion, and deletion times** without requiring complex tree rotations (like AVL or Red-Black Trees). In technical coding interviews (LeetCode 1206 - Design Skiplist) and system design (Redis Sorted Sets / LevelDB SS Table indexing), Skip Lists represent an optimal alternative to balanced binary search trees.

> **Important:** A standard sorted linked list takes $O(N)$ to search. By adding logarithmic express lanes (levels), a Skip List enables **Binary Search behavior on Linked Lists** in $O(\log N)$ average time!

## 2. Core Concepts
* **Level Hierarchy**: Level 0 contains ALL sorted elements. Higher levels contain a fraction (typically $1/2$ or $1/4$) of elements, serving as express indexing lanes.
* **Probabilistic Level Generation (Coin Flip)**: When inserting a new element, its node height (number of levels) is assigned probabilistically using a geometric distribution:
  ```java
  int level = 1;
  while (random.nextDouble() < 0.5 && level < MAX_LEVEL) {
      level++;
  }
  ```
* **Express Lane Traversal**: Search begins at the highest level of `head`. Move RIGHT as long as `curr.next.val < target`. When `curr.next.val >= target`, move DOWN 1 level and repeat!

> **Memory Trick:** **"Search starts at top express level: Right as far as possible, then Down 1 level!"**

## 3. Characteristics / Properties
* **Probabilistic Balancing**: Replaces deterministic BST tree rotations with coin-flip random level assignments, guaranteeing $O(\log N)$ operations with high probability.
* **Concurrent Lock-Free Efficiency**: Far easier to implement concurrent lock-free updates compared to Red-Black Trees (used in Java's `ConcurrentSkipListMap`).

```
Skip List vs Balanced BST Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | Balanced BST (RBT)| Skip List         | System Impact     |
+-----------------------+-------------------+-------------------+-------------------+
| Average Search Time   | O(log N)          | O(log N)          | Identical speed   |
| Balancing Mechanism   | Tree Rotations    | Probabilistic Coin| Skip List simpler |
| Range Queries         | Complex in-order  | O(1) next scan ⚡ | Skip List wins    |
| Concurrent Locking    | Coarse / Complex  | Lock-free atomic  | Redis & Java Map  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Search for Target `19` in a 4-Level Skip List:

```
Level 3: Head -----------------------------------------> [ 17 ] ------------------------> null
Level 2: Head ---------------------> [ 9 ] -------------> [ 17 ] ------------------------> null
Level 1: Head --------> [ 3 ] -----> [ 9 ] -------------> [ 17 ] --------> [ 25 ] -------> null
Level 0: Head -> [1] -> [ 3 ] -> [6]-> [ 9 ] -> [12] -> [ 17 ] -> [19] -> [ 25 ] -> [31]-> null

Step 1: Start at Level 3 Head. Next is 17 < 19 -> Move Right to 17.
Step 2: From 17 on Level 3, next is null. Move Down to Level 2 (at node 17).
Step 3: From 17 on Level 2, next is null. Move Down to Level 1 (at node 17).
Step 4: From 17 on Level 1, next is 25 > 19. Move Down to Level 0 (at node 17).
Step 5: On Level 0, next is 19 == 19. Target FOUND at Level 0 in 5 steps! ✅
```

## 5. Visual Diagram
Skip List Node Express Pointer Connections:

```
Level 2: [Head] ------------------------> [Node 15 (next[2])] ----------------> null
Level 1: [Head] --------> [Node 7] -----> [Node 15 (next[1])] --------> [Node 22] -> null
Level 0: [Head] -> [3] -> [Node 7] ->[11]->[Node 15 (next[0])] ->[18]-> [Node 22] -> null

Multi-level Node Architecture: Node contains array `Node[] next` of size equal to its level!
```

## 6. Operations / Algorithms
LeetCode 1206 Design Skiplist Implementation:

```java
public class Skiplist {

    private static final double P = 0.5;
    private static final int MAX_LEVEL = 16;

    private static class Node {
        int val;
        Node[] forward; // Express links array

        Node(int val, int level) {
            this.val = val;
            this.forward = new Node[level];
        }
    }

    private final Node head;
    private int levelCount;
    private final Random random;

    public Skiplist() {
        head = new Node(-1, MAX_LEVEL);
        levelCount = 1;
        random = new Random();
    }

    // O(log N) Search
    public boolean search(int target) {
        Node curr = head;
        for (int i = levelCount - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < target) {
                curr = curr.forward[i]; // Move Right
            }
        }
        curr = curr.forward[0]; // Move to Level 0
        return curr != null && curr.val == target;
    }

    // Random Level Generator (Geometric Distribution)
    private int randomLevel() {
        int lvl = 1;
        while (random.nextDouble() < P && lvl < MAX_LEVEL) {
            lvl++;
        }
        return lvl;
    }
}
```

> **Quick Syntax:**
```java
// Express Right Traversal Line
while (curr.forward[i] != null && curr.forward[i].val < target) {
    curr = curr.forward[i];
}
```

## 7. Examples
* **LeetCode 1206 - Design Skiplist**: Full implementation of `search`, `add`, and `erase`.
* **Redis Sorted Sets (ZSET)**: Uses Skip Lists internally for $O(\log N)$ score lookups and fast range scanning.
* **Java `ConcurrentSkipListMap`**: High-concurrency lock-free ordered map implementation.

## 8. Java Code
Complete interview-ready Java suite implementing full Skip List with `search`, `add`, and `erase` (LeetCode 1206):

```java
import java.util.Arrays;
import java.util.Random;

public class SkipListMaster {

    private static final double P = 0.5;
    private static final int MAX_LEVEL = 16;

    private static class Node {
        int val;
        Node[] forward;

        Node(int val, int level) {
            this.val = val;
            this.forward = new Node[level];
        }
    }

    private final Node head;
    private int levelCount;
    private final Random random;

    public SkipListMaster() {
        head = new Node(-1, MAX_LEVEL);
        levelCount = 1;
        random = new Random();
    }

    // 1. Search Target O(log N) Avg Time
    public boolean search(int target) {
        Node curr = head;
        for (int i = levelCount - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < target) {
                curr = curr.forward[i];
            }
        }
        curr = curr.forward[0];
        return curr != null && curr.val == target;
    }

    // 2. Add Target O(log N) Avg Time
    public void add(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Node curr = head;

        // Find insertion predecessor at each level
        for (int i = levelCount - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }

        int lvl = randomLevel();
        if (lvl > levelCount) {
            for (int i = levelCount; i < lvl; i++) {
                update[i] = head;
            }
            levelCount = lvl;
        }

        Node newNode = new Node(num, lvl);
        for (int i = 0; i < lvl; i++) {
            newNode.forward[i] = update[i].forward[i];
            update[i].forward[i] = newNode;
        }
    }

    // 3. Erase Target O(log N) Avg Time
    public boolean erase(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Node curr = head;

        for (int i = levelCount - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }

        curr = curr.forward[0];
        if (curr == null || curr.val != num) return false;

        // Unlink node across all its levels
        for (int i = 0; i < levelCount; i++) {
            if (update[i].forward[i] != curr) break;
            update[i].forward[i] = curr.forward[i];
        }

        while (levelCount > 1 && head.forward[levelCount - 1] == null) {
            levelCount--;
        }

        return true;
    }

    private int randomLevel() {
        int lvl = 1;
        while (random.nextDouble() < P && lvl < MAX_LEVEL) {
            lvl++;
        }
        return lvl;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        SkipListMaster skiplist = new SkipListMaster();

        skiplist.add(1);
        skiplist.add(2);
        skiplist.add(3);

        System.out.println("Search 0: " + skiplist.search(0)); // false
        System.out.println("Search 1: " + skiplist.search(1)); // true

        skiplist.add(4);
        System.out.println("Search 1: " + skiplist.search(1)); // true
        System.out.println("Erase 0: "  + skiplist.erase(0));  // false
        System.out.println("Erase 1: "  + skiplist.erase(1));  // true
        System.out.println("Search 1 after erase: " + skiplist.search(1)); // false
    }
}
```

## 9. Complexity Analysis
| Operation | Average Time Complexity | Worst Case Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **`search(val)`** | **$O(\log N)$** | $O(N)$ (Unlucky coin flips) | $O(1)$ Constant |
| **`add(val)`** | **$O(\log N)$** | $O(N)$ | $O(\text{Level})$ array |
| **`erase(val)`** | **$O(\log N)$** | $O(N)$ | $O(\text{Level})$ array |
| **Total Space** | **$O(N)$ Average** | $O(N \log N)$ | Stores express links |

## 10. Edge Cases
* **Inserting Duplicates**: Multi-level Skip Lists handle duplicates by inserting duplicate nodes at their generated random level.
* **Erasing Non-Existent Target**: Returns `false` cleanly without modifying pointers.
* **`MAX_LEVEL` Bound**: Caps level generation to `MAX_LEVEL` (typically 16 or 32) to prevent unbounded memory allocation.

## 11. Common Mistakes
* Moving right when `curr.forward[i].val == target` during predecessor discovery (predecessor MUST be strictly `< target`!).
* Forgetting to update `update[i]` pointers when inserting or deleting nodes across multiple levels.
* Using deterministic level logic instead of geometric coin flip distribution.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why does Redis use Skip Lists instead of Red-Black Trees for Sorted Sets?
> 1. **Range Queries**: Scanning a range $[A, B]$ in a Skip List requires moving down to Level 0 and walking `next` pointers ($O(\log N + K)$ time). In BSTs, in-order range traversal is complex.
> 2. **Implementation Simplicity**: Skip Lists avoid complex tree rotation code.
> 3. **Lock-Free Concurrency**: Skip Lists allow fine-grained atomic pointer updates.

> **Memory Trick:** **"Predecessor condition is strictly LESS THAN: val < target"**.

## 13. Comparisons
| Feature | Red-Black Tree (`TreeMap`) | Skip List (`ConcurrentSkipListMap`) |
| :--- | :--- | :--- |
| **Balancing Strategy** | Strict Tree Rotations | **Probabilistic Coin Flips** |
| **Range Queries** | $O(\log N + K)$ in-order | **$O(\log N + K)$ linear `next` scan ⚡** |
| **Concurrency** | Heavy locking required | **Lock-free atomic updates** |
| **Real-World Use** | C++ `std::map`, Java `TreeMap` | Redis Sorted Sets, LevelDB, Java ConcurrentMap |

## 14. How to Recognize This in Questions
* **"Design an ordered set data structure with logarithmic search, add, and erase"** $\rightarrow$ Skip List (LeetCode 1206).
* **"Explain the data structure behind Redis Sorted Sets"** $\rightarrow$ Skip List + Hash Table.

## 15. Frequently Asked Interview Questions
* **Q: What is the probability distribution used for Skip List level assignment?**  
  *A:* Geometric distribution with probability $p = 0.5$ (or $0.25$). $50\%$ of nodes are at Level 1, $25\%$ at Level 2, $12.5\%$ at Level 3, etc. This bounds total extra pointers to $N / (1 - p) = 2N \implies O(N)$ space.
* **Q: Why does Skip List search achieve $O(\log N)$ average time complexity?**  
  *A:* Because each level cuts the search space by factor $1 / p = 2$ on average, identical to binary search tree traversal depth $\log_2 N$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SKIP LIST DATA STRUCTURE                             |
+-----------------------------------------------------------------------+
| • Node Structure: int val; Node[] forward (array of level pointers)   |
| • Search Rule: Move Right while forward[i].val < target, else Move Down|
| • Level Assignment: Random coin flip (p=0.5) geometric distribution   |
| • Predecessor Search: Array update[MAX_LEVEL] stores left nodes       |
| • Key Systems Use: Powering Redis Sorted Sets & Lock-Free Concurrent Maps|
| • Complexity: O(log N) Avg Time | O(N) Average Auxiliary Space        |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain probabilistic level assignment using coin flips.
- [ ] I can write the Skip List search loop moving right then down.
- [ ] I can implement `predecessor` array tracking during insertions.
- [ ] I know why Redis uses Skip Lists instead of Red-Black Trees.
- [ ] I can solve LeetCode 1206 (Design Skiplist).
