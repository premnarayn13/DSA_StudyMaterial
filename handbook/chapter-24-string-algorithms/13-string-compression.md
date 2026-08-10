# 13. String Compression: RLE, Huffman Coding Trees & Shannon Entropy Bounds

## 1. Introduction
**String Compression** encompasses algorithmic techniques designed to reduce the bit-length footprint required to represent textual or binary data. Governed by **Shannon's Information Entropy Theorem**, compression algorithms split into two primary paradigms: (1) **Lossless Compression** (where original data can be perfectly reconstructed, e.g., text, code, medical images), and (2) **Lossy Compression** (where imperceptible data is discarded for higher compression ratios, e.g., JPEG, MP3). Classical lossless compression algorithms include **Run-Length Encoding (RLE)** ($O(N)$ simple character counting), **Huffman Coding** ($O(N \log |\Sigma|)$ optimal prefix-free variable-length bit codes via Min-Heap Trees), and **Lempel-Ziv-Welch (LZW)** (dictionary-based token replacement used in GIF and ZIP formats).

> **Important:** Core Structural Invariants of String Compression:
> 1. **Shannon Entropy Bound ($H(X)$)**:
>    - The theoretical minimum average bits required per character for a source with character probabilities $p_i$:
>      $$H(X) = -\sum_{i=1}^{|\Sigma|} p_i \log_2 (p_i) \quad \text{bits per character}$$
>    - No lossless compression algorithm can represent data using fewer average bits than $H(X)$!
> 2. **Run-Length Encoding (RLE) Invariant**:
>    - Replaces contiguous repeated character runs $c c c \dots c$ of length $K$ with $(c, K)$ pairs (e.g. `"a3b2c4"`). Highly effective for repetitive data!
> 3. **Huffman Prefix-Free Tree Property**:
>    - Assigns shorter bit codes to high-frequency characters and longer bit codes to low-frequency characters.
>    - **Prefix-Free Invariant**: No character's bit code is a prefix of another character's bit code, allowing unambiguous bitstream decoding without delimiters! ⚡

```
Huffman Coding Tree Construction Topology (Text = "ABRACADABRA"):
Frequencies: 'A':5, 'B':2, 'R':2, 'C':1, 'D':1

Min-Heap Merge Steps:
Merge ('C':1, 'D':1) ──► Node_1 (Count 2)
Merge ('B':2, 'R':2) ──► Node_2 (Count 4)
Merge (Node_1:2, Node_2:4) ──► Node_3 (Count 6)
Merge ('A':5, Node_3:6)   ──► Root Node (Count 11)

Bit Code Assignments:
'A': '0' (1 bit!) | 'B': '110' | 'R': '111' | 'C': '100' | 'D': '101'
Total Bits = 5(1) + 2(3) + 2(3) + 1(3) + 1(3) = 23 Bits (vs 88 ASCII Bits -> 74% Savings!) ⚡
```

---

## 2. Core Concepts & Compression Strategy Matrix

### 2.1 String Compression Strategy Matrix
```
String Compression Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Compression Algorithm | Compression Basis | Encoding Speed    | Decoding Speed    | Ideal Domain      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Run-Length (RLE)**  | Consecutive Runs  | **$O(N)$ Instant ⚡**| **$O(N)$ Instant ⚡**| Repetitive Signals|
| **Huffman Coding**    | Char Frequencies  | **$O(N \log |\Sigma|)$⚡**| **$O(N)$ Bitstream⚡**| Text / GZIP / PNG |
| **LZW Dictionary**    | Substring Patterns| $O(N)$ Table      | $O(N)$ Table      | GIF / PDF / ZIP   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Huffman assigns shorter bit codes to frequent chars! RLE encodes consecutive runs cK!"**

---

## 3. Characteristics & Shannon's Information Entropy Proof

### 3.1 Mathematical Proof of Huffman Optimality & Shannon Limit
* Let source alphabet $\Sigma = \{c_1, c_2 \dots c_k\}$ have probabilities $p_1, p_2 \dots p_k$.
* Shannon's Source Coding Theorem proves that any prefix-free code has expected codeword length $L(C) = \sum p_i \cdot \text{len}(code_i)$ bounded by:
  $$H(X) \le L(C) < H(X) + 1$$
* Huffman's Greedy Min-Heap Construction guarantees that $L(C)$ achieves the absolute minimum possible expected codeword length among all character-by-character prefix-free codes! ⚡

---

## 4. Internal Working Mechanics: Huffman Min-Heap Construction

How Huffman Coding constructs optimal prefix-free trees using a Priority Queue:

```
Tracing Huffman Tree Building for Frequencies: 'A':5, 'B':2, 'C':1, 'D':1:

Step 1: Create leaf nodes and push to Min-Heap:
Min-Heap: [ C(1), D(1), B(2), A(5) ]

Step 2: Pop 2 smallest nodes (C:1 and D:1). Create parent Node1 (weight 2).
Push Node1(2) to Min-Heap: [ B(2), Node1(2), A(5) ]

Step 3: Pop 2 smallest nodes (B:2 and Node1:2). Create parent Node2 (weight 4).
Push Node2(4) to Min-Heap: [ Node2(4), A(5) ]

Step 4: Pop 2 smallest nodes (Node2:4 and A:5). Create Root Node (weight 9).
Heap contains 1 single Root node -> TREE COMPLETE!

Step 5: Traverse Left = '0', Right = '1' to extract bit codes! ✅
```

---

## 5. Visual Diagram: Prefix-Free Bitstream Decoding

```
Huffman Bitstream Decoding Topology:

Compressed Bitstream: "0 1 1 0 0 1 1 1"
                       │ │ │ │ │ │ │ │
                       ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼

Traverse Huffman Tree from Root:
- Bit '0'   ──► Left ──► Leaf 'A'! Output 'A', reset to Root.
- Bit '1'   ──► Right
- Bit '1'   ──► Right
- Bit '0'   ──► Left ──► Leaf 'B'! Output 'B', reset to Root.
- Bit '0'   ──► Left ──► Leaf 'A'! Output 'A', reset to Root.

Decoded Text: "ABA" (Decoded in O(1) time per bit without ambiguity!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Run-Length Encoding/Decoding (LeetCode 443) and a complete Huffman Coding Compression Engine.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing String Compression Engines:
 * Run-Length Encoding (RLE) and Huffman Coding Prefix-Free Trees.
 */
public class StringCompressionMaster {

    // =========================================================================
    // 1. RUN-LENGTH ENCODING & DECODING (LeetCode 443 O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Compresses character array in-place using Run-Length Encoding.
     * LeetCode 443 Solution.
     *
     * @param chars input character array
     * @return new length of compressed array
     */
    public int compressRLE(char[] chars) {
        if (chars == null || chars.length == 0) return 0;

        int writeIdx = 0;
        int i = 0;

        while (i < chars.length) {
            char currentChar = chars[i];
            int count = 0;

            // Count contiguous run length
            while (i < chars.length && chars[i] == currentChar) {
                i++;
                count++;
            }

            // Write character
            chars[writeIdx++] = currentChar;

            // Write count digits if count > 1
            if (count > 1) {
                for (char c : String.valueOf(count).toCharArray()) {
                    chars[writeIdx++] = c;
                }
            }
        }

        return writeIdx;
    }

    /**
     * Decompresses an RLE encoded string.
     */
    public String decompressRLE(String compressed) {
        if (compressed == null || compressed.isEmpty()) return "";

        StringBuilder sb = new StringBuilder();
        int i = 0;

        while (i < compressed.length()) {
            char ch = compressed.charAt(i++);
            StringBuilder countSb = new StringBuilder();

            while (i < compressed.length() && Character.isDigit(compressed.charAt(i))) {
                countSb.append(compressed.charAt(i++));
            }

            int count = (countSb.length() == 0) ? 1 : Integer.parseInt(countSb.toString());
            for (int k = 0; k < count; k++) {
                sb.append(ch);
            }
        }

        return sb.toString();
    }

    // =========================================================================
    // 2. HUFFMAN CODING COMPRESSION ENGINE (O(N log |Sigma|) Time)
    // =========================================================================
    public static class HuffmanNode implements Comparable<HuffmanNode> {
        public final char ch;
        public final int frequency;
        public final HuffmanNode left;
        public final HuffmanNode right;

        public HuffmanNode(char ch, int frequency) {
            this.ch = ch;
            this.frequency = frequency;
            this.left = null;
            this.right = null;
        }

        public HuffmanNode(int frequency, HuffmanNode left, HuffmanNode right) {
            this.ch = '\0'; // Internal node
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
        private HuffmanNode root;

        /**
         * Builds Huffman Tree from text frequency distribution.
         */
        public void buildTree(String text) {
            if (text == null || text.isEmpty()) return;

            Map<Character, Integer> freqMap = new HashMap<>();
            for (char c : text.toCharArray()) {
                freqMap.put(c, freqMap.getOrDefault(c, 0) + 1);
            }

            PriorityQueue<HuffmanNode> minHeap = new PriorityQueue<>();
            for (Map.Entry<Character, Integer> entry : freqMap.entrySet()) {
                minHeap.add(new HuffmanNode(entry.getKey(), entry.getValue()));
            }

            // Edge Case: Single unique character
            if (minHeap.size() == 1) {
                HuffmanNode single = minHeap.poll();
                root = new HuffmanNode(single.frequency, single, null);
                codeMap.put(single.ch, "0");
                return;
            }

            while (minHeap.size() > 1) {
                HuffmanNode left = minHeap.poll();
                HuffmanNode right = minHeap.poll();
                HuffmanNode parent = new HuffmanNode(left.frequency + right.frequency, left, right);
                minHeap.add(parent);
            }

            root = minHeap.poll();
            buildCodeMap(root, "");
        }

        private void buildCodeMap(HuffmanNode node, String code) {
            if (node == null) return;
            if (node.isLeaf()) {
                codeMap.put(node.ch, code);
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
         * Decodes a Huffman bit string back into original text in O(BitLength) time.
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
// Huffman Bitstream Decode Reset Line
if (curr.isLeaf()) { sb.append(curr.ch); curr = root; }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 443 - String Compression**:
   - Primary RLE in-place compression benchmark ($O(N)$ time, $O(1)$ space).

2. **ZIP / GZIP Archiving Systems**:
   - Deflate algorithm combines DEFLATE (LZ77) and Huffman Coding for maximum file compression.

3. **PNG Image File Format**:
   - Uses Huffman Coding on image byte streams for lossless graphics storage.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class StringCompressionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   STRING COMPRESSION ENGINES DEMO               ");
        System.out.println("=================================================\n");

        StringCompressionMaster master = new StringCompressionMaster();

        // 1. RLE Compression Test (LeetCode 443)
        char[] chars = {'a', 'a', 'b', 'b', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'};
        System.out.println("1. Original Array for RLE: " + Arrays.toString(chars));
        int newLen = master.compressRLE(chars);
        System.out.print("   Compressed Result     : [ ");
        for (int i = 0; i < newLen; i++) System.out.print("'" + chars[i] + "' ");
        System.out.println("] (New Length = " + newLen + ")");
        System.out.println("-------------------------------------------------");

        // 2. Huffman Coding Engine Test
        String text = "ABRACADABRA";
        StringCompressionMaster.HuffmanEngine huffman = new StringCompressionMaster.HuffmanEngine();
        huffman.buildTree(text);

        String bitstream = huffman.encode(text);
        String decoded = huffman.decode(bitstream);

        System.out.println("2. Huffman Coding Test for Text: \"" + text + "\"");
        System.out.println("   Huffman Bit Codes Map       : " + huffman.getCodeMap());
        System.out.println("   Encoded Bitstream           : " + bitstream);
        System.out.println("   Bit Length (vs 88 ASCII bits): " + bitstream.length() + " Bits");
        System.out.println("   Decoded Text                : \"" + decoded + "\"");
        System.out.println("   Decoding Verified           : " + text.equals(decoded));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Compression Algorithm | Encoding Time | Decoding Time | Auxiliary Space | Compression Principle |
| :--- | :--- | :--- | :--- | :--- |
| **Run-Length (RLE)**  | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ In-Place ⚡| Contiguous run counts |
| **Huffman Coding**    | $\mathbf{O(N \log |\Sigma|)}$⚡| $\mathbf{O(N_{\text{bits}})}$ Linear⚡| $O(|\Sigma|)$ Tree | Variable-length prefix codes |
| **LZW Compression**   | $O(N)$ Table | $O(N)$ Table | $O(\text{DictSize})$ | Dictionary token replacement |

---

## 10. Edge Cases & Boundary Handling

1. **High Entropy Random Noise Data (Non-Compressible)**:
   - Compressing truly random data using RLE expands file size (e.g. `"abcdef"` $\to$ `"a1b1c1d1e1f1"`).
   - **Guard**: Check if compressed size > original size; if true, output uncompressed raw stream.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Non-Prefix Free Bit Code Assignment**:
  - Assigning bit codes where one character's code is a prefix of another (e.g. 'A'='0', 'B'='01') creates ambiguous bitstreams that cannot be decoded. Huffman trees guarantee **Prefix-Free Codes**!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Huffman Coding Uses Priority Queues (Min-Heap):
> Popping the two smallest frequency nodes iteratively guarantees that the least frequent characters end up deepest in the tree (longest bit codes), while the most frequent characters end up nearest the root (shortest bit codes)! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Huffman Coding | Run-Length Encoding (RLE) | LZW Compression |
| :--- | :--- | :--- | :--- |
| **Data Requirement** | Frequency Skewness | Contiguous Repeats | Substring Repeated Patterns |
| **Prefix-Free Property**| **Guaranteed ⚡** | N/A | Token Table |
| **Decoding Speed** | **Fast $O(1)$ / Bit ⚡** | **Fast $O(N)$ ⚡** | Fast Table Lookup |

---

## 14. How to Recognize This in Questions

* **"Compress character array in-place replacing repeated characters with counts"** $\rightarrow$ RLE (LeetCode 443).
* **"Construct optimal variable-length prefix-free binary codes for characters"** $\rightarrow$ Huffman Coding.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Prefix-Free Code?**  
  *A:* A code system where no codeword is a prefix of any other codeword, ensuring unambiguous bitstream parsing without delimiters.

* **Q: What is Shannon's Entropy Bound?**  
  *A:* The theoretical minimum average number of bits per character required to represent a source, defined as $H(X) = -\sum p_i \log_2 p_i$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING COMPRESSION                                    |
+-----------------------------------------------------------------------+
| • RLE Principle  : Replace repeated runs ccc with (c, count)          |
| • Huffman Engine : Build Min-Heap -> Merge 2 smallest -> Extract codes|
| • Prefix-Free    : No code is a prefix of another code -> Easy decode |
| • Shannon Bound  : Minimum average bits = -sum(p_i * log2(p_i))       |
| • Performance    : Huffman encodes in O(N log |Sigma|), decodes in O(N)⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write in-place Run-Length Encoding (LeetCode 443) in Java.
- [ ] I can build a Huffman Coding Min-Heap Tree.
- [ ] I can generate prefix-free bit codes from a Huffman Tree.
- [ ] I can write a Huffman bitstream decoder.
- [ ] I can state Shannon's Information Entropy formula.
