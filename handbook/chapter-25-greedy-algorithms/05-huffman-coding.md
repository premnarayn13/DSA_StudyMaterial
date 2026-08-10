# 05. Huffman Coding: Min-Heap Greedy Merges, Prefix-Free Trees & Bitstream Engines

## 1. Introduction
**Huffman Coding** is an optimal greedy data compression algorithm invented by David A. Huffman in 1952 while he was a Ph.D. student at MIT. Designed to assign **Variable-Length Prefix-Free Bit Codes** to characters based on their frequencies of occurrence, Huffman Coding assigns shorter bit codes to high-frequency characters (e.g. `'e'`, `'a'`) and longer bit codes to low-frequency characters (e.g. `'z'`, `'q'`). By iteratively popping and merging the two lowest-frequency nodes using a **Min-Heap (Priority Queue)**, Huffman Coding constructs a binary trie tree in **$O(N \log |\Sigma|)$ Time Complexity** and **$O(|\Sigma|)$ Auxiliary Space**, achieving the theoretical minimum expected codeword length bounded by **Shannon's Information Entropy**.

> **Important:** Core Structural Invariants of Huffman Coding:
> 1. **Greedy Min-Heap Choice Property**:
>    - At each step, pop the **two nodes with the SMALLEST frequencies** ($f_1$ and $f_2$), merge them into a single parent node of frequency $f_1 + f_2$, and push the parent node back into the Min-Heap.
>    - Why? Lowest frequency characters are placed at maximum depth in the tree, receiving the longest bit codes!
> 2. **Prefix-Free Property (Unambiguous Bitstreams)**:
>    - No character codeword is a prefix of any other character codeword.
>    - Ensures that a compressed bitstream can be decoded sequentially from left to right in **$O(1)$ time per bit** without requiring delimiters!
> 3. **Binary Tree Traversal Invariant**:
>    - Left branch edges represent bit `'0'`; Right branch edges represent bit `'1'`.
>    - All characters reside strictly at **Leaf Nodes**. Internal nodes contain only frequency sums. ⚡

```
Huffman Min-Heap Merge Topology (Text Frequencies: A:5, B:2, C:1, D:1):

Step 1: Pop C(1) and D(1) ──► Merge to Node1(2)
Step 2: Pop B(2) and Node1(2) ──► Merge to Node2(4)
Step 3: Pop Node2(4) and A(5) ──► Merge to Root(9)

Tree Topography:
                   (Root: 9)
                  /         \
             '0' /           \ '1'
             Node2(4)        Leaf A(5)  ──► Code for 'A' = "1"
            /        \
       '0' /          \ '1'
       Leaf B(2)      Node1(2)        ──► Code for 'B' = "00"
                     /        \
                '0' /          \ '1'
                Leaf C(1)      Leaf D(1) ──► Code for 'C' = "010", 'D' = "011" ⚡
```

---

## 2. Core Concepts & Huffman Strategy Matrix

### 2.1 Huffman Strategy Matrix
```
Huffman Compression Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Stage                 | Primary Mechanism | Time Complexity   | Auxiliary Space   | Key Invariant     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Frequency Counting**| Character Map     | **$O(N)$ Linear ⚡**| $O(|\Sigma|)$ Map | Single String Pass|
| **Tree Construction** | Min-Heap Merges   | **$O(|\Sigma| \log |\Sigma|)$⚡**| $O(|\Sigma|)$ Queue| Lowest 2 popped   |
| **Code Map Extract**  | Tree DFS Traverse | $O(|\Sigma|)$     | $O(|\Sigma|)$ Map | Left '0', Right '1'|
| **Bit Encoding**      | Map Lookup        | **$O(N)$ Linear ⚡**| $O(N_{\text{bits}})$ String| Direct replacement|
| **Bit Decoding**      | Tree Traversal    | **$O(N_{\text{bits}})$ Linear⚡**| $\mathbf{O(1)}$ Memory ⚡| Root reset at leaf|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Huffman pops 2 smallest nodes from Min-Heap to merge parent! High frequency = Short code!"**

---

## 3. Characteristics & Shannon Entropy Proof

### 3.1 Mathematical Proof of Huffman Optimality & Shannon Bound
* Let source alphabet $\Sigma = \{c_1, c_2 \dots c_k\}$ have probabilities $p_1, p_2 \dots p_k$ ($\sum p_i = 1$).
* Expected codeword length $L(C) = \sum_{i=1}^k p_i \cdot l_i$ where $l_i$ is the bit length of code $c_i$.
* **Shannon Entropy Limit**:
  $$H(X) = -\sum_{i=1}^k p_i \log_2 (p_i) \le L(C) < H(X) + 1$$
* **Greedy Optimality Proof**:
  1. **Sibling Lemma**: In an optimal prefix tree, the two lowest frequency characters $c_1, c_2$ MUST be sibling leaves at maximum depth in the tree.
  2. **Induction Step**: Merging $c_1$ and $c_2$ into a single node with frequency $p_1 + p_2$ reduces the problem size from $k$ to $k - 1$.
  3. By induction, the tree constructed by greedy min-heap merging yields the absolute minimum expected codeword length $L(C)$ among all prefix-free binary codes! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Execution Dry Run

Tracing Huffman Coding for Text $T = \text{"BEEP BOOP"}$:

```
Step 1: Count Character Frequencies:
'E': 2, 'P': 2, 'O': 2, 'B': 2, ' ': 1 (Total N = 9 chars, |Sigma| = 5).

Step 2: Build Min-Heap:
Queue = [ ' '(1), 'B'(2), 'E'(2), 'O'(2), 'P'(2) ]

Step 3: Iterative Merges:
- Merge ' '(1) and 'B'(2) ──► Node1(3). Queue = [ 'E'(2), 'O'(2), 'P'(2), Node1(3) ]
- Merge 'E'(2) and 'O'(2) ──► Node2(4). Queue = [ 'P'(2), Node1(3), Node2(4) ]
- Merge 'P'(2) and Node1(3) ──► Node3(5). Queue = [ Node2(4), Node3(5) ]
- Merge Node2(4) and Node3(5) ──► Root(9).

Step 4: Extract Bit Codes:
'E': "00", 'O': "01", 'P': "10", ' ': "110", 'B': "111"

Step 5: Encode "BEEP BOOP":
"111 00 00 10 110 111 01 01 10" ──► Total 21 Bits (vs 72 ASCII Bits -> 70.8% Savings!) ✅
```

---

## 5. Visual Diagram: Prefix-Free Bit Tree Navigation

```
Tree Traversal Decoding for Bitstream "11100":

                     (Root)
                    /      \
               '0' /        \ '1'
               (Node2)      (Node3)
               /     \       /     \
             "00"   "01"   "10"    (Node1)
            ('E')  ('O')  ('P')    /     \
                                 "110"   "111"
                                 (' ')   ('B')

Bit 1 ──► Right (Node3)
Bit 1 ──► Right (Node1)
Bit 1 ──► Right (Leaf 'B')! Output 'B', reset to Root.
Bit 0 ──► Left (Node2)
Bit 0 ──► Left (Leaf 'E')! Output 'E', reset to Root.

Decoded Text: "BE"! Unambiguous left-to-right parsing! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing the complete Huffman Coding Engine, Min-Heap Tree Construction, Bitstream Encoding, and Bitstream Decoding.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Huffman Coding,
 * Min-Heap Greedy Tree Construction, and Bitstream Processing.
 */
public class HuffmanCodingMaster {

    public static class HuffmanNode implements Comparable<HuffmanNode> {
        public final char ch;
        public final int frequency;
        public final HuffmanNode left;
        public final HuffmanNode right;

        // Leaf Node Constructor
        public HuffmanNode(char ch, int frequency) {
            this.ch = ch;
            this.frequency = frequency;
            this.left = null;
            this.right = null;
        }

        // Internal Parent Node Constructor
        public HuffmanNode(int frequency, HuffmanNode left, HuffmanNode right) {
            this.ch = '\0'; // Special marker for internal non-leaf node
            this.frequency = frequency;
            this.left = left;
            this.right = right;
        }

        public boolean isLeaf() {
            return left == null && right == null;
        }

        @Override
        public int compareTo(HuffmanNode o) {
            return Integer.compare(this.frequency, o.frequency);
        }
    }

    public static class HuffmanEngine {
        private final Map<Character, String> codeMap = new HashMap<>();
        private final Map<String, Character> reverseCodeMap = new HashMap<>();
        private HuffmanNode root;

        /**
         * Builds Huffman Tree from text input in O(N + |Sigma| log |Sigma|) time.
         *
         * @param text input string
         */
        public void buildTree(String text) {
            if (text == null || text.isEmpty()) return;

            // Step 1: Count character frequencies
            Map<Character, Integer> freqMap = new HashMap<>();
            for (char c : text.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }

            // Step 2: Push all leaf nodes into Min-Heap
            PriorityQueue<HuffmanNode> minHeap = new PriorityQueue<>();
            for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
                minHeap.add(new HuffmanNode(entry.getKey(), entry.getValue()));
            }

            // Handle Single Unique Character edge case
            if (minHeap.size() == 1) {
                HuffmanNode single = minHeap.poll();
                root = new HuffmanNode(single.frequency, single, null);
                codeMap.put(single.ch, "0");
                reverseCodeMap.put("0", single.ch);
                return;
            }

            // Step 3: Iteratively pop 2 smallest nodes and merge
            while (minHeap.size() > 1) {
                HuffmanNode left = minHeap.poll();
                HuffmanNode right = minHeap.poll();
                HuffmanNode parent = new HuffmanNode(left.frequency + right.frequency, left, right);
                minHeap.add(parent);
            }

            root = minHeap.poll();

            // Step 4: Traverse tree to generate prefix-free bit codes
            codeMap.clear();
            reverseCodeMap.clear();
            buildCodeMap(root, "");
        }

        private void buildCodeMap(HuffmanNode node, String code) {
            if (node == null) return;

            if (node.isLeaf()) {
                codeMap.put(node.ch, code);
                reverseCodeMap.put(code, node.ch);
                return;
            }

            buildCodeMap(node.left, code + "0");
            buildCodeMap(node.right, code + "1");
        }

        /**
         * Encodes text into a Huffman bit string.
         */
        public String encode(String text) {
            StringBuilder sb = new StringBuilder();
            for (char c : text.toCharArray()) {
                sb.append(codeMap.get(c));
            }
            return sb.toString();
        }

        /**
         * Decodes bitstream back into original text using tree traversal in O(Bits) time.
         */
        public String decode(String bitstream) {
            StringBuilder sb = new StringBuilder();
            HuffmanNode curr = root;

            for (int i = 0; i < bitstream.length(); i++) {
                char bit = bitstream.charAt(i);
                curr = (bit == '0') ? curr.left : curr.right;

                if (curr.isLeaf()) {
                    sb.append(curr.ch);
                    curr = root; // Reset to root for next character! ⚡
                }
            }

            return sb.toString();
        }

        public Map<Character, String> getCodeMap() {
            return Collections.unmodifiableMap(codeMap);
        }
    }
}
```

> **Quick Syntax:**
```java
// Huffman Min-Heap Merge Line
while (minHeap.size() > 1) { HuffmanNode left = minHeap.poll(), right = minHeap.poll(); minHeap.add(new HuffmanNode(left.frequency + right.frequency, left, right)); }
```

---

## 7. Concrete Problem Examples & Applications

1. **GZIP / ZIP / Deflate Compression Architecture**:
   - Uses Huffman Coding on LZ77 literal/distance match tokens.

2. **JPEG & PNG Image File Encoding**:
   - Encodes quantized DCT coefficients (JPEG) or filtered pixel differences (PNG) using Huffman Trees.

3. **MP3 Audio Compression**:
   - Employs Huffman Coding on quantized MDCT frequency domain audio coefficients.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class HuffmanCodingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   HUFFMAN CODING GREEDY COMPRESSION DEMO        ");
        System.out.println("=================================================\n");

        String text = "BEEP BOOP";
        System.out.println("1. Original Input Text: \"" + text + "\" (Length = " + text.length() + " chars)");

        HuffmanCodingMaster.HuffmanEngine engine = new HuffmanCodingMaster.HuffmanEngine();
        engine.buildTree(text);

        String encodedBitstream = engine.encode(text);
        String decodedText = engine.decode(encodedBitstream);

        System.out.println("\n2. Generated Prefix-Free Bit Codes Map:");
        engine.getCodeMap().forEach((ch, code) -> System.out.println("   '" + ch + "' ──► " + code));

        System.out.println("\n3. Bitstream Encoding & Decoding Verification:");
        System.out.println("   Encoded Bitstream    : " + encodedBitstream);
        System.out.println("   Bit Length           : " + encodedBitstream.length() + " Bits (vs " + (text.length() * 8) + " ASCII Bits)");
        System.out.println("   Compression Ratio    : " + String.format("%.2f%%", (1.0 - (double) encodedBitstream.length() / (text.length() * 8)) * 100));
        System.out.println("   Decoded Output Text  : \"" + decodedText + "\"");
        System.out.println("   Decoding Success     : " + text.equals(decodedText));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Huffman Phase | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Frequency Pass**   | $\mathbf{O(N)}$ Linear ⚡| $O(|\Sigma|)$ Map | Scan input text |
| **Min-Heap Merges**  | $\mathbf{O(|\Sigma| \log |\Sigma|)}$⚡| $O(|\Sigma|)$ PriorityQueue | Pop 2 smallest nodes |
| **Code Extraction**  | $O(|\Sigma|)$ Linear | $O(|\Sigma|)$ Recursion | DFS Tree Traversal |
| **Bit Encoding**     | $\mathbf{O(N)}$ Linear ⚡| $O(N_{\text{bits}})$ Output | Map replace |
| **Bit Decoding**     | $\mathbf{O(N_{\text{bits}})}$ Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Tree Pointer Traversal |

---

## 10. Edge Cases & Boundary Handling

1. **Single Unique Character Text (`"AAAAA"`)**:
   - Root is initialized with left child pointing to `'A'`, code maps `'A' \to \text{"0"}`. Handled cleanly without null pointer exceptions.

2. **Empty Text (`""`)**:
   - `buildTree` returns early safely.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Merging Non-Minimal Nodes in Heap**:
  - Failing to pop the **two absolute smallest frequency nodes** at each step breaks the prefix-free optimal code bound. ALWAYS use a Min-Heap (`PriorityQueue`).

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Huffman Coding Is Greedy:
> Huffman Coding makes the **local optimal choice** of merging the two smallest frequency nodes at every step without looking ahead or backtracking, constructing a **globally optimal prefix-free tree**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Huffman Coding | Fixed-Length ASCII | Run-Length Encoding (RLE) |
| :--- | :--- | :--- | :--- |
| **Bit Representation** | Variable-Length | Fixed 8 Bits | Character + Count |
| **Prefix-Free Property**| **Guaranteed ⚡** | N/A | N/A |
| **Optimal Lossless**   | **Achieves Shannon Limit ⚡**| Sub-optimal | Requires contiguous runs |

---

## 14. How to Recognize This in Questions

* **"Construct optimal variable-length prefix-free binary codes based on frequencies"** $\rightarrow$ Huffman Coding.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Prefix-Free Code?**  
  *A:* A code system where no character code is a prefix of another code, allowing unambiguous decoding without delimiters.

* **Q: Why does Huffman Coding place high frequency characters near the root?**  
  *A:* Because placing high-frequency characters near the root assigns them shorter bit paths, minimizing the overall expected codeword length.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: HUFFMAN CODING                                        |
+-----------------------------------------------------------------------+
| • Greedy Choice: Pop 2 smallest frequency nodes from Min-Heap to merge|
| • Structure    : Binary Tree (Left='0', Right='1'), Leaves = Chars    |
| • Property     : Prefix-Free (No code is a prefix of another code)   |
| • Performance  : O(N + |Sigma| log |Sigma|) Build | O(Bits) Decode ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can build a Huffman Min-Heap Tree in Java.
- [ ] I can generate prefix-free bit codes via DFS tree traversal.
- [ ] I can write a Huffman bitstream encoder and decoder.
- [ ] I can prove why Huffman Coding is optimal using Shannon's Entropy Theorem.
- [ ] I can handle the single unique character edge case cleanly.
