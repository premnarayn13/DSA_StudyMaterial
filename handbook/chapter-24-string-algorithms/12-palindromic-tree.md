# 12. Palindromic Tree (EERTREE): Dual Root Architecture, Suffix Links & Linear Count

## 1. Introduction
The **Palindromic Tree** (also universally known as the **EERTREE**), invented by Mikhail Rubinchik and Arseny M. Shur in 2015, is a specialized linear-time data structure designed to represent all distinct palindromic substrings of a string $S$. Unlike Suffix Trees or Manacher's Algorithm, an EERTREE constructs a directed acyclic graph with a unique **Dual Root Architecture**: Root 0 (representing imaginary odd-length palindromes with length $-1$) and Root 1 (representing empty even-length palindromes with length $0$). By maintaining **Suffix Links** (pointing to the longest proper palindromic suffix), the EERTREE processes characters online in **$O(N)$ Strict Linear Time** and **$O(N \cdot |\Sigma|)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of the Palindromic Tree (EERTREE):
> 1. **Dual Root Architecture**:
>    - **Root 0 (Odd Root)**: Has length $-1$. Its suffix link points to itself. Used for single-character odd palindromes (length $= -1 + 2 = 1$).
>    - **Root 1 (Even Root)**: Has length $0$. Its suffix link points to Root 0. Used for two-character even palindromes (length $= 0 + 2 = 2$).
> 2. **Node Attributes**:
>    - `len`: Length of the palindrome represented by this node.
>    - `link`: Suffix link to the node representing the longest proper palindromic suffix.
>    - `next[26]`: Transition edge for character $c$. If node has length $L$, adding char $c$ to both ends creates palindrome of length $L + 2$.
>    - `num`: Number of palindromic suffixes ending at the current character.
> 3. **Distinct Palindromic Substrings Theorem**:
>    - A string $S$ of length $N$ contains at most $N$ distinct palindromic substrings.
>    - In an EERTREE, the number of distinct palindromes equals:
>      $$\text{Distinct Palindromes} = \text{Total Nodes Created} - 2 \quad \text{(Excluding Roots 0 and 1)}$$
> 4. **$O(N)$ Online Construction**: Incremental character processing advances the last added palindrome suffix in $O(N)$ total amortized time! ⚡

```
EERTREE Dual Root Architecture & Transition Topology:

   (Odd Root 0: len = -1) <──────────┐ (Self Suffix Link)
          │                          │
          │ Transition 'a'           │
          ▼                          │
   (Node 2: "a", len = 1) ───────────┘ (Suffix Link to Odd Root)
          │
          │ Transition 'b'
          ▼
   (Node 3: "aba", len = 3) ─────────► (Suffix Link to Node 4: "b", len = 1)

   (Even Root 1: len = 0) ──────────► (Suffix Link to Odd Root 0)
          │
          │ Transition 'b'
          ▼
   (Node 4: "b", len = 1)
```

---

## 2. Core Concepts & EERTREE Strategy Matrix

### 2.1 Palindromic Data Structures Comparison Matrix
```
Palindromic Data Structures Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Structure / Engine    | Space Footprint   | Online Processing | Distinct Count    | Suffix Link Tree  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Manacher's Engine** | $O(N)$ Radius     | Offline           | Indirect          | None              |
| **EERTREE (PalTree)** | **$O(N \cdot |\Sigma|)$ Nodes⚡**| **Online $O(N)$ ⚡**| **Direct (Nodes-2)⚡**| **Suffix Links ⚡**|
| **Suffix Automaton**  | $O(N \cdot |\Sigma|)$| Online $O(N)$     | Indirect          | Suffix Link DAG   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"EERTREE uses Dual Roots (-1 and 0)! Total distinct palindromes = Total Nodes - 2 in O(N) online time!"**

---

## 3. Characteristics & $O(N)$ Linear Construction Proof

### 3.1 Mathematical Proof of $O(N)$ Linear Time Construction
* Let $S$ be a string of length $N$.
* When inserting character $S[i]$:
  - We start from the node of the longest palindromic suffix of $S[0 \dots i-1]$ (node `last`).
  - We traverse fallback suffix links `curr = curr.link` until $S[i - 1 - \text{curr.len}] == S[i]$.
* **Amortized Analysis**:
  - Each fallback transition along a suffix link strictly decreases `curr.len`.
  - Creating a new node increases `curr.len` by 2 (or 1).
  - Across all $N$ character insertions, the total increase in `curr.len` is at most $2N$.
  - Therefore, the total number of suffix link fallbacks across the entire construction is bounded by $2N$.
* Total Time Complexity: $\mathbf{O(N) \text{ Strict Amortized Linear Time}}$.
* Auxiliary Space: At most $N + 2$ nodes $\implies \mathbf{O(N \cdot |\Sigma|) \text{ Space}}$. ⚡

---

## 4. Internal Working Mechanics: Character Insertion Routine

Tracing Insertion of $S = \text{"aba"}$:

```
Init Dual Roots:
- Node 1 (Odd Root): len = -1, link = 1
- Node 2 (Even Root): len = 0, link = 1
- last = 2 (Even Root)

Insert i = 0 (S[0] = 'a'):
- Fallback from last=2: S[0 - 1 - 0] doesn't exist -> Fallback to link=1 (Odd Root).
- Odd Root len = -1: S[0 - 1 - (-1)] = S[0] == S[0] ('a' == 'a') -> MATCH!
- Create Node 3: "a", len = 1, link = 2 (Even Root), next['a'] from Node 1 = 3.
- Set last = 3. Distinct Palindromes = 1 ("a").

Insert i = 1 (S[1] = 'b'):
- Fallback from last=3 ("a"): S[1 - 1 - 1] doesn't exist -> Fallback to link=2 (Even Root).
- Even Root len = 0: S[1 - 1 - 0] = S[0] != S[1] ('a' != 'b') -> Fallback to link=1 (Odd Root).
- Odd Root MATCH ('b' == 'b') -> Create Node 4: "b", len = 1, link = 2 (Even Root).
- Set last = 4. Distinct Palindromes = 2 ("a", "b").

Insert i = 2 (S[2] = 'a'):
- Fallback from last=4 ("b"): S[2 - 1 - 1] = S[0] == S[2] ('a' == 'a') -> MATCH!
- Create Node 5: "aba", len = 3, link = 3 ("a").
- Set last = 5. Distinct Palindromes = 3 ("a", "b", "aba").

Final EERTREE Nodes Created = 5. Distinct Palindromes = 5 - 2 = 3! ✅
```

---

## 5. Visual Diagram: Suffix Link Fallback Tree Structure

```
Fallback Suffix Link Chain for Node "aba":

[ Node "aba" (len=3) ] ─── Suffix Link ───► [ Node "a" (len=1) ] ─── Suffix Link ───► [ Even Root (len=0) ]
                                                                                              │
                                                                                        Suffix Link
                                                                                              │
                                                                                              ▼
                                                                                    [ Odd Root (len=-1) ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing the complete Palindromic Tree (EERTREE) Data Structure, Online Character Insertions, Distinct Palindrome Counting, and Frequency Analytics.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Palindromic Tree (EERTREE),
 * Dual Root Architecture (-1 and 0), Online Incremental Construction, and Suffix Links.
 */
public class PalindromicTreeMaster {

    public static class EERTREENode {
        public final int[] next = new int[26]; // Transition edges for 'a'..'z'
        public int len;                        // Length of palindrome
        public int link;                       // Suffix link to longest proper palindromic suffix
        public int num;                        // Number of palindromic suffixes ending at this char
        public long occ;                       // Total occurrences in string

        public EERTREENode(int len) {
            this.len = len;
            this.link = 0;
            this.num = 0;
            this.occ = 0;
        }
    }

    public static class EERTREE {
        private final List<EERTREENode> tree = new ArrayList<>();
        private final StringBuilder s = new StringBuilder();
        private int last; // Index of node for longest palindromic suffix of current prefix

        public EERTREE() {
            // Node 1: Odd Root (length = -1)
            EERTREENode oddRoot = new EERTREENode(-1);
            oddRoot.link = 1; // Suffix link points to itself
            tree.add(oddRoot); // Index 0 (dummy unused)
            tree.add(oddRoot); // Index 1: Odd Root

            // Node 2: Even Root (length = 0)
            EERTREENode evenRoot = new EERTREENode(0);
            evenRoot.link = 1; // Suffix link points to Odd Root
            tree.add(evenRoot); // Index 2: Even Root

            this.last = 2; // Start at Even Root
        }

        /**
         * Inserts character ch online in O(1) amortized time.
         *
         * @param ch character to insert
         */
        public void addChar(char ch) {
            s.append(ch);
            int pos = s.length() - 1;
            int c = ch - 'a';

            // Step 1: Fallback along suffix links to find matching palindrome parent
            int curr = last;
            while (true) {
                int curLen = tree.get(curr).len;
                if (pos - 1 - curLen >= 0 && s.charAt(pos - 1 - curLen) == ch) {
                    break; // Match found!
                }
                curr = tree.get(curr).link;
            }

            // Step 2: Check if transition edge already exists
            if (tree.get(curr).next[c] != 0) {
                last = tree.get(curr).next[c];
                tree.get(last).occ++;
                return;
            }

            // Step 3: Create new Palindromic Node
            int nodeIdx = tree.size();
            EERTREENode newNode = new EERTREENode(tree.get(curr).len + 2);
            newNode.occ = 1;
            tree.add(newNode);

            tree.get(curr).next[c] = nodeIdx;

            // Step 4: Find Suffix Link for the new node
            if (newNode.len == 1) {
                newNode.link = 2; // Single char palindrome link points to Even Root
            } else {
                int temp = tree.get(curr).link;
                while (true) {
                    int curLen = tree.get(temp).len;
                    if (pos - 1 - curLen >= 0 && s.charAt(pos - 1 - curLen) == ch) {
                        break;
                    }
                    temp = tree.get(temp).link;
                }
                newNode.link = tree.get(temp).next[c];
            }

            newNode.num = tree.get(newNode.link).num + 1;
            last = nodeIdx;
        }

        /**
         * Returns total number of DISTINCT palindromic substrings in string.
         * Theorem: Distinct Count = Total Nodes - 2 (Roots)
         */
        public int countDistinctPalindromes() {
            return tree.size() - 3; // Subtract 3 (0-dummy, 1-odd root, 2-even root)
        }

        /**
         * Propagates occurrences from leaf nodes to root via suffix links.
         */
        public void propagateOccurrences() {
            for (int i = tree.size() - 1; i > 2; i--) {
                tree.get(tree.get(i).link).occ += tree.get(i).occ;
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// EERTREE Fallback Suffix Link Condition Line
while (pos - 1 - tree.get(curr).len < 0 || s.charAt(pos - 1 - tree.get(curr).len) != ch) curr = tree.get(curr).link;
```

---

## 7. Concrete Problem Examples & Applications

1. **Count Distinct Palindromic Substrings (LeetCode 1698 Variation)**:
   - Solved in $O(N)$ time via `tree.size() - 3`.

2. **Total Palindromic Substrings Count (LeetCode 647)**:
   - Solved by summing `node.num` during online insertions.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class PalindromicTreeDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     PALINDROMIC TREE (EERTREE) DEMO             ");
        System.out.println("=================================================\n");

        PalindromicTreeMaster.EERTREE eertree = new PalindromicTreeMaster.EERTREE();
        String str = "abacaba";

        System.out.println("1. Inserting String Online: \"" + str + "\"");
        for (char ch : str.toCharArray()) {
            eertree.addChar(ch);
        }

        int distinctCount = eertree.countDistinctPalindromes();
        System.out.println("   Total Distinct Palindromic Substrings: " + distinctCount + " Palindromes");
        System.out.println("   (Distinct Palindromes for \"abacaba\": \"a\", \"b\", \"c\", \"aba\", \"aca\", \"abacaba\")");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| EERTREE Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Character Add (`addChar`)**| $\mathbf{O(1)}$ Amortized ⚡| $O(|\Sigma|)$ Edges per Node | Fallback suffix links |
| **Full String Build**        | $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(N \cdot |\Sigma|)}$ Space | At most $N+2$ nodes |
| **Distinct Count Query**     | $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| `tree.size() - 3` |

---

## 10. Edge Cases & Boundary Handling

1. **String with No Palindromes > Length 1 (`"abcdef"`)**:
   - Creates exactly $N$ nodes (1 per character). Returns distinct count $= N$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Dual Root Initialization (Odd Root = -1, Even Root = 0)**:
  - Attempting to use a single root causes odd and even palindromes to collide, breaking suffix link transitions.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** EERTREE vs Manacher's Algorithm:
> * **Manacher's Algorithm**: Offline array-based algorithm. Finds longest palindrome and counts total palindromes in $O(N)$ space.
> * **EERTREE**: Online tree-based automaton. Builds an explicit structural graph of all distinct palindromes in $O(N)$ time with suffix links! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | EERTREE (Palindromic Tree) | Manacher's Algorithm | Suffix Automaton |
| :--- | :--- | :--- | :--- |
| **Distinct Palindromes**| **Direct $O(1)$ (`Nodes - 3`)⚡**| Indirect LCP calculation | Complex |
| **Online Processing**   | **Yes (Character Stream) ⚡**| No (Offline String) | Yes |
| **Graph Structure**     | Dual Root Tree | Array Radii | Single Root Automaton |

---

## 14. How to Recognize This in Questions

* **"Maintain distinct palindromic substrings online from a dynamic character stream"** $\rightarrow$ EERTREE.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does the EERTREE have two root nodes?**  
  *A:* Root 0 has length $-1$ for odd-length palindromes (so $-1 + 2 = 1$), and Root 1 has length $0$ for even-length palindromes (so $0 + 2 = 2$).

* **Q: What is the maximum number of distinct palindromic substrings in any string of length $N$?**  
  *A:* Exactly $N$ distinct palindromic substrings.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PALINDROMIC TREE (EERTREE)                            |
+-----------------------------------------------------------------------+
| • Dual Roots   : Root 0 (len = -1, odd), Root 1 (len = 0, even)       |
| • Node Fields  : len, link (suffix link), next[26], num, occ          |
| • Distinct Theorem: Total Distinct Palindromes = Total Nodes - 3      |
| • Fallback Rule: while (pos - 1 - len < 0 || S[pos-1-len] != S[pos])  |
| • Performance  : O(N) Online Construction | At most N+2 nodes ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can explain EERTREE Dual Root Architecture (Root -1 and Root 0).
- [ ] I can write online `addChar(ch)` character insertion in Java.
- [ ] I can calculate the number of distinct palindromic substrings in $O(1)$ time (`tree.size() - 3`).
- [ ] I can explain why a string of length $N$ has at most $N$ distinct palindromes.
- [ ] I can trace suffix link fallback chains for palindromic nodes.
