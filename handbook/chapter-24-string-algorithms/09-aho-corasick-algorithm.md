# 09. Aho-Corasick Algorithm: Multi-Pattern Automaton, Failure Links & Linear Streaming

## 1. Introduction
The **Aho-Corasick Algorithm** is a landmark multi-pattern string-matching algorithm invented by Alfred V. Aho and Margaret J. Corasick in 1975. Designed to search for an arbitrary dictionary of $K$ patterns $P = \{P_1, P_2 \dots P_K\}$ simultaneously within a single Text string $T$ of length $N$, Aho-Corasick constructs a Finite State Automaton by augmenting a **Trie Prefix Tree** with **BFS Failure Links** (analogous to KMP's LPS table) and **Dictionary Output Links**. Aho-Corasick processes text in a single forward pass with **Zero Text Pointer Backtracking**, matching all $K$ patterns across text $T$ in **$O(N + \sum M_i + Z)$ Linear Time** where $\sum M_i$ is the total pattern lengths and $Z$ is total pattern match occurrences. Aho-Corasick powers **Network Intrusion Detection Systems (Snort)**, **Antivirus Signature Scanners**, and **Multi-Keyword Content Filters**.

> **Important:** Core Invariants of the Aho-Corasick Automaton:
> 1. **GOTO Trie TrieNode Tree**: Standard Trie structure storing all $K$ patterns. Root represents state 0 (`""`).
> 2. **BFS Failure Link (`fail[u]`)**:
>    - Points from state $u$ to state $v$ representing the longest proper suffix of the string path at state $u$ that is also a valid prefix in the Trie.
>    - Built layer-by-layer using Breadth-First Search (BFS) level-order traversal.
> 3. **Dictionary Output Link (`output[u]`)**:
>    - Links state $u$ to the nearest ancestor state reachable via failure links that marks a completed pattern end, allowing matching nested patterns (e.g. matching both `"he"` and `"hers"`) in $O(1)$ time per occurrence!
> 4. **Zero Text Pointer Backtracking**: Text pointer $i \in [0 \dots N-1]$ moves strictly rightward, advancing from state to state in $O(1)$ amortized time. ⚡

```
Aho-Corasick Automaton Topology for Dictionary P = {"he", "she", "his", "hers"}:

                         (Root 0)
                        /   |   \
                     'h'   's'   ...
                     /       \
                 (State 1)   (State 3)
                 /   \           \
             'e'     'i'         'h'
             /         \           \
       (State 2)*     (State 6)   (State 4)
           /              \           \
         'r'              's'         'e'
         /                  \           \
     (State 8)            (State 7)*   (State 5)*
       /
     's'
     /
 (State 9)*

* Failure Link from State 4 ('sh') points to State 1 ('h')!
* Failure Link from State 5 ('she') points to State 2 ('he')! ⚡
```

---

## 2. Core Concepts & Multi-Pattern Strategy Matrix

### 2.1 Multi-Pattern Matching Comparison Matrix
```
Multi-Pattern Matching Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm             | Pattern Count $K$ | Pre-processing    | Text Search Time  | Text Backtracking |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Naive Search**      | $K$ Passes        | $O(0)$            | $O(K \cdot N \cdot M)$| Resets $i$       |
| **KMP Algorithm**     | $K$ Passes        | $O(\sum M_i)$     | $O(K \cdot N)$    | **Zero Backtrack ⚡**|
| **Rabin-Karp**        | Single Pass (M)   | $O(\sum M_i)$     | $O(N + Z \cdot M)$| Zero Backtrack    |
| **Aho-Corasick Engine**| **Single Pass ⚡** | **$O(\sum M_i)$ ⚡**| **$O(N + Z)$ Strict ⚡**| **Zero Backtrack ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Aho-Corasick builds BFS failure links on a Trie! Searches K patterns in 1 single text pass O(N + Z)!"**

---

## 3. Characteristics & $O(N + \sum M_i + Z)$ Complexity Proof

### 3.1 Mathematical Proof of $O(N + \sum M_i + Z)$ Linear Time
* Let $N$ be Text length, $\sum M_i$ be sum of all $K$ pattern lengths, and $Z$ be total pattern matches found.
* **Phase 1: GOTO Trie Construction**:
  - Inserting $K$ patterns into Trie takes $O(\sum M_i)$ time.
* **Phase 2: BFS Failure & Output Link Construction**:
  - BFS queue visits each node in Trie exactly once.
  - For each node, finding failure link takes amortized $O(1)$ steps.
  - Phase 2 takes $O(\sum M_i \cdot |\Sigma|)$ time.
* **Phase 3: Text Search Engine**:
  - Text pointer $i$ advances $N$ times.
  - Fallback transitions along failure links decrease depth in Trie. Since total depth increases at most $N$ times, total failure steps $\le N$.
  - Collecting matched patterns follows output links in $O(Z)$ total time.
* Total Search Time: $O(N + Z)$.
* Overall Algorithm Time Complexity: $\mathbf{O(N + \sum M_i + Z) \text{ Strict Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: BFS Failure Link Construction

How are Failure Links constructed using BFS level-order traversal?

```
Tracing BFS Failure Link Construction for Dictionary P = {"he", "she", "his", "hers"}:

Step 1: Root (State 0) children:
- State 1 ('h'): Set fail[1] = 0. Push to BFS Queue.
- State 3 ('s'): Set fail[3] = 0. Push to BFS Queue.

Step 2: Pop State 1 ('h'):
- Child 'e' (State 2): Look at fail[1] (State 0). State 0 has no 'e' child. Set fail[2] = 0.
- Child 'i' (State 6): Look at fail[1] (State 0). State 0 has no 'i' child. Set fail[6] = 0.

Step 3: Pop State 3 ('s'):
- Child 'h' (State 4): Look at fail[3] (State 0). State 0 HAS child 'h' (State 1)!
  Set fail[4] = State 1 ('h')! ⚡

Step 4: Pop State 4 ('sh'):
- Child 'e' (State 5): Look at fail[4] (State 1). State 1 HAS child 'e' (State 2)!
  Set fail[5] = State 2 ('he')! ⚡
  Output Link: State 5 matches "she" AND links to State 2 ("he")!

Failure links connect longest proper suffix to matching prefix! ✅
```

---

## 5. Visual Diagram: Aho-Corasick Automaton Transitions & Output Links

```
Automaton State Transitions for Text T = "ushers":

State 0 ──'u'──► State 0 (Fail)
State 0 ──'s'──► State 3 ('s')
State 3 ──'h'──► State 4 ('sh')
State 4 ──'e'──► State 5 ('she')  ──► Output Matches: ["she", "he"]! ⚡
                                      (Follows dict link to State 2)
State 5 ──'r'──► State 8 ('sher')
State 8 ──'s'──► State 9 ('shers') ──► Output Matches: ["hers"]! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing the complete Aho-Corasick Automaton Engine, Trie Node GOTO Construction, BFS Failure & Output Link Construction, and Text Search Engine.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Aho-Corasick Automaton Engine,
 * BFS Failure Link Construction, Output Links, and Multi-Pattern Searching.
 */
public class AhoCorasickMaster {

    public static class MatchResult {
        public final int textIndex;    // 0-based ending index in text
        public final String pattern;   // Matched pattern string

        public MatchResult(int textIndex, String pattern) {
            this.textIndex = textIndex;
            this.pattern = pattern;
        }

        @Override
        public String toString() {
            return "Match{" + pattern + " @ endIdx=" + textIndex + "}";
        }
    }

    public static class AhoCorasickNode {
        public final Map<Character, AhoCorasickNode> children = new HashMap<>();
        public AhoCorasickNode failureLink = null;
        public AhoCorasickNode dictionaryLink = null; // Next output node in fail chain
        public final List<String> outputPatterns = new ArrayList<>();
        public final int id;

        public AhoCorasickNode(int id) {
            this.id = id;
        }
    }

    public static class AutomatonEngine {
        private final AhoCorasickNode root;
        private int nodeCounter = 0;

        public AutomatonEngine(List<String> patterns) {
            this.root = new AhoCorasickNode(nodeCounter++);
            buildGotoTrie(patterns);
            buildFailureAndOutputLinks();
        }

        // Step 1: Build GOTO Trie Graph
        private void buildGotoTrie(List<String> patterns) {
            for (String p : patterns) {
                if (p == null || p.isEmpty()) continue;
                AhoCorasickNode curr = root;
                for (char ch : p.toCharArray()) {
                    curr = curr.children.computeIfAbsent(ch, k -> new AhoCorasickNode(nodeCounter++));
                }
                curr.outputPatterns.add(p);
            }
        }

        // Step 2: Build BFS Failure & Dictionary Output Links
        private void buildFailureAndOutputLinks() {
            Queue<AhoCorasickNode> queue = new LinkedList<>();

            // Depth 1 nodes: failure links point to root
            for (AhoCorasickNode child : root.children.values()) {
                child.failureLink = root;
                queue.add(child);
            }

            // BFS level-order traversal
            while (!queue.isEmpty()) {
                AhoCorasickNode curr = queue.poll();

                for (Map.Entry<Character, AhoCorasickNode> entry : curr.children.entrySet()) {
                    char ch = entry.getKey();
                    AhoCorasickNode child = entry.getValue();

                    // Find failure link for child by traversing curr's fail chain
                    AhoCorasickNode tempFail = curr.failureLink;
                    while (tempFail != null && !tempFail.children.containsKey(ch)) {
                        tempFail = tempFail.failureLink;
                    }

                    if (tempFail != null) {
                        child.failureLink = tempFail.children.get(ch);
                    } else {
                        child.failureLink = root;
                    }

                    // Set Dictionary Output Link to nearest ancestor with non-empty output
                    if (!child.failureLink.outputPatterns.isEmpty()) {
                        child.dictionaryLink = child.failureLink;
                    } else {
                        child.dictionaryLink = child.failureLink.dictionaryLink;
                    }

                    queue.add(child);
                }
            }
        }

        // Step 3: Single-Pass Multi-Pattern Text Search Engine (O(N + Z) Time)
        public List<MatchResult> search(String text) {
            List<MatchResult> results = new ArrayList<>();
            if (text == null || text.isEmpty()) return results;

            AhoCorasickNode curr = root;

            for (int i = 0; i < text.length(); i++) {
                char ch = text.charAt(i);

                // Fallback along failure links if transition char is absent
                while (curr != root && !curr.children.containsKey(ch)) {
                    curr = curr.failureLink;
                }

                if (curr.children.containsKey(ch)) {
                    curr = curr.children.get(ch);
                } else {
                    curr = root;
                }

                // Collect direct output patterns matching at current state
                for (String p : curr.outputPatterns) {
                    results.add(new MatchResult(i, p));
                }

                // Collect indirect output patterns via dictionary links!
                AhoCorasickNode dictNode = curr.dictionaryLink;
                while (dictNode != null) {
                    for (String p : dictNode.outputPatterns) {
                        results.add(new MatchResult(i, p));
                    }
                    dictNode = dictNode.dictionaryLink;
                }
            }

            return results;
        }
    }
}
```

> **Quick Syntax:**
```java
// Aho-Corasick Text Search Transition Line
while (curr != root && !curr.children.containsKey(ch)) curr = curr.failureLink;
```

---

## 7. Concrete Problem Examples & Applications

1. **Network Intrusion Detection Systems (Snort NIDS)**:
   - Snort inspects incoming TCP/IP packet payloads against 10,000+ malicious virus signature strings simultaneously using Aho-Corasick in $O(N)$ linear time!

2. **Antivirus & Malware Signature Scanners**:
   - Scanning binary executable files for millions of virus byte sequences in a single pass.

3. **Multi-Keyword Content Filtering & Censorship Systems**:
   - Filtering prohibited keywords in chat messages or social media posts instantly.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class AhoCorasickDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   AHO-CORASICK MULTI-PATTERN AUTOMATON DEMO     ");
        System.out.println("=================================================\n");

        List<String> dictionary = List.of("he", "she", "his", "hers");
        System.out.println("1. Dictionary Patterns: " + dictionary);

        AhoCorasickMaster.AutomatonEngine engine = new AhoCorasickMaster.AutomatonEngine(dictionary);

        String text = "ushers";
        System.out.println("2. Searching Text   : \"" + text + "\"");

        List<AhoCorasickMaster.MatchResult> matches = engine.search(text);

        System.out.println("\n3. Single-Pass Match Results:");
        for (AhoCorasickMaster.MatchResult match : matches) {
            System.out.println("   - " + match);
        }

        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Aho-Corasick Phase | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **GOTO Trie Build** | $\mathbf{O(\sum M_i)}$ ⚡| $O(\sum M_i \cdot |\Sigma|)$ | Single pattern insertions |
| **BFS Failure Links**| $\mathbf{O(\sum M_i \cdot |\Sigma|)}$| $O(\sum M_i)$ Queue | Level-order BFS traversal |
| **Text Search Engine**| $\mathbf{O(N + Z)}$ Strict ⚡| $\mathbf{O(1)}$ Memory ⚡| Zero text pointer backtrack |
| **Overall Engine**  | $\mathbf{O(N + \sum M_i + Z)}$| $O(\sum M_i \cdot |\Sigma|)$ | Single pass multi-pattern |

---

## 10. Edge Cases & Boundary Handling

1. **Nested Substring Patterns (e.g. `"he"` inside `"she"`)**:
   - Handled via Dictionary Output Links (`dictionaryLink`), capturing both `"she"` and `"he"` matches at the exact same ending index!

2. **No Patterns Match Text**:
   - Fallback loop returns to root node safely. Returns empty result list in $O(N)$ time.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Omitting Dictionary Output Links**:
  - Forgetting dictionary links causes short nested pattern matches (e.g. `"he"`) to be missed when a longer pattern (e.g. `"she"`) matches.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Aho-Corasick Beats Running KMP $K$ Times:
> * **KMP $K$ Passes**: Runs $K$ separate text scans taking $K \times O(N) = O(K \cdot N)$ time.
> * **Aho-Corasick**: Combines all $K$ patterns into a single finite state machine, processing text in **1 Single Pass $O(N + Z)$ Time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Aho-Corasick Automaton | Rabin-Karp Multi-Pattern | KMP (K Passes) |
| :--- | :--- | :--- | :--- |
| **Pass Count** | **Single Pass ⚡** | Single Pass (Fixed M) | $K$ Separate Passes |
| **Variable Pattern Lengths**| **Supported Seamlessly ⚡**| Requires Multiple Hashes| Supported |
| **Search Time** | **$O(N + Z)$ Strict ⚡** | $O(N + Z \cdot M)$ | $O(K \cdot N)$ |

---

## 14. How to Recognize This in Questions

* **"Search a dictionary of K patterns of varying lengths in text T in a single pass"** $\rightarrow$ Aho-Corasick Algorithm.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Failure Link in Aho-Corasick?**  
  *A:* A link from state $u$ to state $v$ representing the longest proper suffix of the path at state $u$ that is also a valid prefix in the Trie.

* **Q: How does Aho-Corasick handle nested pattern matches?**  
  *A:* Via Dictionary Output Links, which chain ancestor states that contain completed pattern matches, allowing all nested patterns to be collected at current text index in $O(1)$ time per match.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: AHO-CORASICK ALGORITHM                                |
+-----------------------------------------------------------------------+
| • Automaton    : Trie + BFS Failure Links + Dictionary Output Links   |
| • Failure Link : Points to longest proper suffix that is a Trie prefix|
| • Dict Link    : Links state to nearest ancestor with pattern output  |
| • Text Search  : Single pass O(N + Z) time with ZERO text backtracking|
| • Use Case     : Snort NIDS, Antivirus Signatures, Content Filters ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can build GOTO Trie for dictionary patterns in Java.
- [ ] I can build BFS Failure Links and Dictionary Output Links.
- [ ] I can write single-pass multi-pattern text search engine.
- [ ] I can prove why Aho-Corasick search time is $O(N + Z)$.
- [ ] I can explain how Dictionary Output Links capture nested matches.
