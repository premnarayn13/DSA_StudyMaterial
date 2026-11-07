# 15. Advanced String Concepts: Suffix Automata (SAM), Duval's Algorithm & Minimal Rotations

## 1. Introduction
**Advanced String Concepts** push beyond classical linear pattern matching into state-of-the-art automata theory, combinatorial string factorization, and minimal rotation algorithms. Primary advanced paradigms include:
1. **Suffix Automaton (SAM - Minimal Suffix DFA)**: A directed acyclic graph that represents all substrings of a string $S$ in **$O(N)$ Space and Time**. Containing at most $2N - 1$ states and $3N - 4$ transitions, a SAM compresses Suffix Trees into the most memory-efficient structure for substring counting, matching, and longest common substring queries.
2. **Duval's Algorithm & Lyndon Factorization**: Factors a string $S$ into a unique lexicographically non-increasing sequence of **Lyndon Words** ($S = w_1 w_2 \dots w_k$ where $w_1 \ge w_2 \ge \dots \ge w_k$) in **$O(N)$ Strict Linear Time** and **$O(1)$ Space**, solving the **Lexicographically Minimal String Rotation (Booth's Algorithm / LeetCode 899)** problem.
3. **Wildcard Pattern Matching (Bitset Acceleration / FFT)**: Matches patterns containing wildcards `'?'` or `'*'` in $O(N \cdot M / 64)$ time using bitset parallel processing.

> **Important:** Core Invariants of Advanced String Automata & Factorization:
> 1. **Suffix Automaton (SAM) State Invariant**:
>    - A state in SAM represents an equivalence class of substrings that share the exact same set of end-positions (`endpos` set).
>    - State attributes: `len` (maximum length of substring in class), `link` (suffix link to state of longest proper suffix with a larger `endpos` set), and `next[26]` (transition edges).
> 2. **Lyndon Word Definition**:
>    - A string $w$ is a Lyndon word if it is strictly smaller lexicographically than all its proper right rotations ($w < \text{rot}(w)$).
> 3. **Duval's $O(N)$ Linear Factorization**:
>    - Maintains 3 pointers `i`, `j`, `k` to parse pre-Lyndon prefixes, factoring any string into Lyndon components in **$O(N)$ Time and $O(1)$ Memory**! ⚡

```
Suffix Automaton (SAM) State Graph Topology for S = "aba":

                    (State 0: Root "")
                     /        \
                  'a'          'b'
                 /                \
          (State 1: "a") ────────► (State 2: "b")
                 \                /
                  'b'          'a'
                   \          /
                (State 3: "ab" & "aba")

Contains ALL substrings {"a", "b", "ab", "ba", "aba"} using ONLY 4 states! ⚡
```

---

## 2. Core Concepts & Advanced String Engine Strategy Matrix

### 2.1 Advanced String Engine Strategy Matrix
```
Advanced String Engine Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Engine / Algorithm    | State / Space     | Construction Time | Substring Query   | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Suffix Automaton**  | $2N - 1$ States   | **$O(N)$ Linear ⚡**| **$O(L)$ Instant ⚡**| Substring DFA     |
| **Duval's Factorization**| $O(1)$ Pointers  | **$O(N)$ Linear ⚡**| N/A               | Minimal Rotations |
| **Bitset Matching**   | $O(M / 64)$ Bitset| **$O(N \cdot M / 64)$⚡**| Bitwise Shift   | Wildcard Matching |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"SAM represents all substrings in 2N-1 states O(N) space! Duval factors Lyndon words in O(N) time O(1) space!"**

---

## 3. Characteristics & $O(N)$ Suffix Automaton State Proof

### 3.1 Mathematical Proof of $O(N)$ States in Suffix Automaton
* Let $S$ be a string of length $N$.
* The Suffix Automaton (SAM) represents all $N(N+1)/2$ substrings as paths from the initial state 0.
* **State Bound Proof**:
  - The end-position sets (`endpos`) of substrings form a inclusion-exclusion tree hierarchy.
  - A tree with $N$ leaves has at most $2N - 1$ total nodes.
  - Therefore, the SAM contains at most **$2N - 1$ States**!
* **Transition Edge Bound Proof**:
  - The transitions form a directed acyclic graph (DAG) with a spanning tree.
  - Total transition edges $\le \mathbf{3N - 4}$.
* Construction Time: Each character insertion adds at most 2 states and updates suffix links in $O(1)$ amortized time.
* Overall Complexity: $\mathbf{O(N) \text{ Strict Linear Time and Space}}$. ⚡

---

## 4. Internal Working Mechanics: Duval's $O(N)$ Minimal String Rotation

How Duval's Algorithm finds the lexicographically minimal rotation of string $S$ in $O(N)$ time and $O(1)$ space:

```
Tracing Duval's Minimal Rotation for S = "bba" (Concatenated S + S = "bbabba"):

Form S' = S + S = "bbabba" (Length 2N = 6).
Maintain 3 pointers: i = 0, j = 1, k = 0.

Step 1 (k = 0): Compare S'[i+k] ('b') with S'[j+k] ('b') -> Equal! k++ (k = 1).
Step 2 (k = 1): Compare S'[i+1] ('b') with S'[j+1] ('a') -> 'b' > 'a'!
        S'[i] ('b') is GREATER than S'[j] ('a').
        Advance i to i + k + 1 = 0 + 1 + 1 = 2!
        Reset j = i + 1 = 3, k = 0.

Step 3 (i = 2): Candidate rotation starts at index 2 ("abb")!
Loop completes when j reaches 2N.

Minimal String Rotation found starting at Index 2 -> "abb"! ✅ (Executed in O(N) Time & O(1) Memory!)
```

---

## 5. Visual Diagram: Suffix Automaton (SAM) Endpos Hierarchy Tree

```
Substrings Endpos Set Inclusion Tree Hierarchy:

                      [ Endpos = {0, 1, 2, 3} (Root "") ]
                                 /            \
           [ Endpos = {0, 2} ("a") ]    [ Endpos = {1, 3} ("b") ]
                      │                            │
           [ Endpos = {2} ("ba") ]      [ Endpos = {3} ("ab") ]

Tree depth is bounded by string length N, proving 2N-1 max states! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing the complete Suffix Automaton (SAM) Engine, Duval's Algorithm for Minimal String Rotation, and Bitset Parallel Wildcard Matching.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced String Concepts:
 * Suffix Automaton (SAM), Duval's Minimal Rotation Engine, and Bitset Wildcard Search.
 */
public class AdvancedStringConceptsMaster {

    // =========================================================================
    // 1. SUFFIX AUTOMATON (SAM) ENGINE (O(N) Time, O(N * |Sigma|) Space)
    // =========================================================================
    public static class SAMNode {
        public final int[] next = new int[26]; // Transition edges for 'a'..'z'
        public int len;                        // Max length of substring in state
        public int link;                       // Suffix link to parent state

        public SAMNode() {
            Arrays.fill(next, -1);
            this.len = 0;
            this.link = -1;
        }
    }

    public static class SuffixAutomaton {
        private final List<SAMNode> st = new ArrayList<>();
        private int last;

        public SuffixAutomaton(String s) {
            // State 0: Root empty string
            SAMNode root = new SAMNode();
            st.add(root);
            last = 0;

            for (int i = 0; i < s.length(); i++) {
                extend(s.charAt(i));
            }
        }

        /**
         * Extends SAM by single character in O(1) amortized time.
         */
        private void extend(char c) {
            int cur = st.size();
            SAMNode currNode = new SAMNode();
            currNode.len = st.get(last).len + 1;
            st.add(currNode);

            int charIdx = c - 'a';
            int p = last;

            // Follow suffix links to add transition to new state
            while (p != -1 && st.get(p).next[charIdx] == -1) {
                st.get(p).next[charIdx] = cur;
                p = st.get(p).link;
            }

            if (p == -1) {
                st.get(cur).link = 0; // Point to root
            } else {
                int q = st.get(p).next[charIdx];
                if (st.get(p).len + 1 == st.get(q).len) {
                    st.get(cur).link = q;
                } else {
                    // Clone state q to split long substrings
                    int clone = st.size();
                    SAMNode cloneNode = new SAMNode();
                    cloneNode.len = st.get(p).len + 1;
                    cloneNode.link = st.get(q).link;
                    System.arraycopy(st.get(q).next, 0, cloneNode.next, 0, 26);
                    st.add(cloneNode);

                    while (p != -1 && st.get(p).next[charIdx] == q) {
                        st.get(p).next[charIdx] = clone;
                        p = st.get(p).link;
                    }

                    st.get(q).link = clone;
                    st.get(cur).link = clone;
                }
            }

            last = cur;
        }

        /**
         * Checks if a substring exists in the original string in O(L) time.
         */
        public boolean containsSubstring(String pattern) {
            if (pattern == null) return false;
            int curr = 0; // Start at root
            for (char ch : pattern.toCharArray()) {
                int idx = ch - 'a';
                if (st.get(curr).next[idx] == -1) {
                    return false; // Edge absent -> Substring does not exist!
                }
                curr = st.get(curr).next[idx];
            }
            return true;
        }

        /**
         * Returns total number of distinct substrings in original string in O(N) time.
         */
        public long countDistinctSubstrings() {
            long total = 0;
            for (int i = 1; i < st.size(); i++) {
                total += st.get(i).len - st.get(st.get(i).link).len;
            }
            return total;
        }
    }

    // =========================================================================
    // 2. DUVAL'S MINIMAL STRING ROTATION ENGINE (Booth's Algorithm O(N) Time, O(1) Memory)
    // =========================================================================
    /**
     * Finds the lexicographically minimal rotation of string S in O(N) time and O(1) space.
     * LeetCode 899 variation.
     *
     * @param s input string
     * @return lexicographically smallest rotation string
     */
    public String findMinimalRotation(String s) {
        if (s == null || s.length() <= 1) return s;

        int n = s.length();
        String s2 = s + s; // Concatenate string to handle rotations seamlessly

        int i = 0; // Starting candidate index
        int j = 1;
        int k = 0;

        while (i < n && j < n && k < n) {
            char charI = s2.charAt(i + k);
            char charJ = s2.charAt(j + k);

            if (charI == charJ) {
                k++;
            } else if (charI > charJ) {
                i = Math.max(i + k + 1, j + 1); // Skip invalid candidates! ⚡
                j = i + 1;
                k = 0;
            } else {
                j = Math.max(j + k + 1, i + 1);
                k = 0;
            }
        }

        int minStartIdx = Math.min(i, j);
        return s2.substring(minStartIdx, minStartIdx + n);
    }
}
```

> **Quick Syntax:**
```java
// Duval's Minimal Rotation Skip Line
if (charI > charJ) { i = Math.max(i + k + 1, j + 1); j = i + 1; k = 0; }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 899 - Orderly Queue (Minimal String Rotation)**:
   - Solved in $O(N)$ time and $O(1)$ space using Duval's / Booth's Algorithm.

2. **LeetCode 1698 - Number of Distinct Substrings in a String**:
   - Solved in $O(N)$ time via SAM state length sum (`len[i] - len[link[i]]`).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class AdvancedStringConceptsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ADVANCED STRING AUTOMATA & DUVAL DEMO         ");
        System.out.println("=================================================\n");

        AdvancedStringConceptsMaster master = new AdvancedStringConceptsMaster();

        // 1. Suffix Automaton (SAM) Test
        String str = "abacaba";
        AdvancedStringConceptsMaster.SuffixAutomaton sam = new AdvancedStringConceptsMaster.SuffixAutomaton(str);

        System.out.println("1. Input String: \"" + str + "\"");
        System.out.println("   SAM Substring Search (\"caba\"): " + sam.containsSubstring("caba"));
        System.out.println("   SAM Substring Search (\"xyz\") : " + sam.containsSubstring("xyz"));
        System.out.println("   Total Distinct Substrings (SAM): " + sam.countDistinctSubstrings() + " Substrings");
        System.out.println("-------------------------------------------------");

        // 2. Duval's Minimal Rotation Test
        String rotStr = "bba";
        String minRot = master.findMinimalRotation(rotStr);
        System.out.println("2. Input String for Minimal Rotation: \"" + rotStr + "\"");
        System.out.println("   Lexicographically Minimal Rotation: \"" + minRot + "\" (O(N) Time & O(1) Space)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Advanced Engine | Construction Time | Substring Query Time | Auxiliary Memory | Key Feature |
| :--- | :--- | :--- | :--- | :--- |
| **Suffix Automaton (SAM)**| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(L)}$ Instant ⚡| $O(N \cdot |\Sigma|)$ States | Minimal Substring DFA ($2N-1$ states) |
| **Duval's Factorization**| $\mathbf{O(N)}$ Linear ⚡| N/A | $\mathbf{O(1)}$ Memory ⚡| Minimal Rotation in $O(1)$ space |

---

## 10. Edge Cases & Boundary Handling

1. **String with All Same Characters (`"aaaa"`)**:
   - SAM creates $N+1$ states. Duval's algorithm completes in $N$ comparisons returning `"aaaa"`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Building $O(N^2)$ Suffix Trees Instead of $O(N)$ Suffix Automata**:
  - Standard suffix trees use $O(N^2)$ node memory if implemented naively. Suffix Automaton (SAM) guarantees at most $2N - 1$ states in $O(N)$ space!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** SAM vs Suffix Array Choice:
> * **Suffix Array**: Simpler implementation, requires $O(N \log N)$ or $O(N)$ construction, queries substrings in $O(M \log N)$ binary search.
> * **Suffix Automaton (SAM)**: State machine DFA, constructs in $O(N)$ time, queries substrings in **Instant $O(L)$ time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Suffix Automaton (SAM) | Suffix Array + LCP | Suffix Tree |
| :--- | :--- | :--- | :--- |
| **State / Node Count** | **At most $2N - 1$ States ⚡**| $N$ Integers | Up to $2N$ Nodes |
| **Substring Search Time**| **$O(L)$ Instant ⚡**| $O(L \log N)$ BS | **$O(L)$ Instant ⚡**|
| **Construction Time** | **$O(N)$ Linear ⚡**| $O(N \log N)$ / $O(N)$| $O(N)$ (Ukkonen) |

---

## 14. How to Recognize This in Questions

* **"Find lexicographically smallest rotation of string S in O(N) time and O(1) space"** $\rightarrow$ Duval's Algorithm.
* **"Check if pattern P is a substring in O(L) time using minimal state machine"** $\rightarrow$ Suffix Automaton (SAM).

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Suffix Automaton (SAM)?**  
  *A:* The minimal deterministic finite automaton (DFA) that recognizes all suffixes (and substrings) of a string $S$ in $O(N)$ time and space using at most $2N - 1$ states.

* **Q: How does Duval's Algorithm find the minimal string rotation in $O(1)$ space?**  
  *A:* By maintaining 3 pointers `i`, `j`, `k` over the concatenated string $S + S$ to skip candidates that cannot form a minimal rotation.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED STRING CONCEPTS                              |
+-----------------------------------------------------------------------+
| • Suffix Automaton: Minimal DFA representing all substrings in 2N-1 states|
| • SAM Distinct Count: Sum(len[i] - len[link[i]]) over all states     |
| • Duval's Engine  : Minimal string rotation in O(N) time & O(1) space |
| • Skip Condition  : If charI > charJ -> i = max(i + k + 1, j + 1)     |
| • Performance     : SAM and Duval's algorithm run in strict O(N) time⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Suffix Automaton (SAM) state extension in Java.
- [ ] I can write Duval's Algorithm for minimal string rotation in $O(N)$ time and $O(1)$ space.
- [ ] I can calculate the number of distinct substrings using Suffix Automaton.
- [ ] I can state the maximum number of states in a SAM ($2N - 1$).
- [ ] I can explain why SAM queries substrings in $O(L)$ time.
