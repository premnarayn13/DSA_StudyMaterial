# 08. Gray Code: Single-Bit Transitions, Binary-to-Gray Encoders & Sequence Generation

## 1. Introduction
**Gray Code** (also known as **Reflected Binary Code**) is a binary numeral system where two successive values differ by **EXACTLY ONE BIT POSITION** (a Hamming distance of 1). Named after Bell Labs physicist Frank Gray, Gray Code eliminates physical switching glitches in mechanical rotary encoders, digital communications, analog-to-digital converters (ADCs), and Karnaugh Maps. Converting a standard binary integer $B$ into its corresponding Gray Code representation $G$ executes in **$O(1)$ Single CPU Instruction** via the **Binary-to-Gray Conversion Formula ($G = B \oplus (B \gg 1)$)**. Generating the complete $N$-bit Gray Code sequence (LeetCode 89) of size $2^N$ executes in **$O(2^N)$ Strict Linear Time** without complex recursion or memory allocation.

> **Important:** Core Structural Properties of Gray Code:
> 1. **Single-Bit Transition Invariant**:
>    - For any two consecutive elements in a Gray Code sequence $G_i$ and $G_{i+1}$:
>      $$\text{HammingDistance}(G_i, G_{i+1}) = \text{popcount}(G_i \oplus G_{i+1}) = 1$$
> 2. **Binary-to-Gray Conversion Formula**:
>    - For a binary integer $B$:
>      $$G = B \oplus (B \gg 1)$$
> 3. **Gray-to-Binary Conversion Algorithm**:
>    - Restores standard binary integer $B$ from Gray Code $G$ by iteratively XORing right-shifted bits:
>      $$B = G \oplus (G \gg 1) \oplus (G \gg 2) \oplus (G \gg 4) \oplus (G \gg 8) \oplus (G \gg 16)$$
> 4. **LeetCode 89 Gray Code Sequence Generation**:
>    - For $N$ bits, iterate integer $i$ from $0$ to $2^N - 1$:
>      $$\text{sequence}[i] = i \oplus (i \gg 1)$$ ⚡

```
Standard Binary vs Gray Code Comparison Topology (3 Bits):

Decimal Value   Standard Binary   Gray Code (G = B ^ (B >> 1))   Bit Changes Count
──────────────────────────────────────────────────────────────────────────────────
      0               000                     000                       -
      1               001                     001                    1 Bit  ✅
      2               010                     011                    1 Bit  ✅
      3               011                     010                    1 Bit  ✅
      4               100                     110                    1 Bit  ✅
      5               101                     111                    1 Bit  ✅
      6               110                     101                    1 Bit  ✅
      7               111                     100                    1 Bit  ✅

Every single transition changes EXACTLY ONE BIT! ⚡
```

---

## 2. Core Concepts & Gray Code Strategy Matrix

### 2.1 Gray Code Conversions Strategy Matrix
```
Gray Code Conversions Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Conversion Direction  | Bitwise Formula   | Time Complexity   | Auxiliary Space   | Hardware Speed    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Binary to Gray**    | `g = b ^ (b >> 1)`| **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**| **1 CPU Cycle ⚡** |
| **Gray to Binary**    | Shift-XOR Chain   | **$O(1)$ 5 Ops ⚡**| **$O(1)$ Memory ⚡**| **5 CPU Ops ⚡**   |
| **Sequence Gen (89)** | `i ^ (i >> 1)`    | **$O(2^N)$ Linear ⚡**| **$O(2^N)$ Array ⚡**| **Fast Linear ⚡** |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Binary to Gray: g = b ^ (b >> 1); LeetCode 89 Sequence: res.add(i ^ (i >> 1)) for i = 0..2^N-1!"**

---

## 3. Characteristics & Binary-to-Gray Mathematical Proof

### 3.1 Mathematical Proof of Binary-to-Gray Conversion $G = B \oplus (B \gg 1)$
* Let $B = (b_{n-1}, b_{n-2} \dots b_0)$ be an $n$-bit binary integer.
* The Gray Code bit vector $G = (g_{n-1}, g_{n-2} \dots g_0)$ is defined such that the MSB bit remains identical ($g_{n-1} = b_{n-1}$), and each subsequent bit $g_i$ is the XOR sum of adjacent binary bits:
  $$g_i = b_i \oplus b_{i+1} \quad \text{for } 0 \le i < n-1$$
* **Proof that $G = B \oplus (B \gg 1)$**:
  - The right-shifted binary vector $B \gg 1$ has bit $i$ given by $b_{i+1}$ (with 0 shifted into MSB).
  - Bitwise XORing $B \oplus (B \gg 1)$ at position $i$ evaluates:
    $$(B \oplus (B \gg 1))_i = b_i \oplus b_{i+1} = g_i$$
  - At the MSB position $n-1$: $b_{n-1} \oplus 0 = b_{n-1} = g_{n-1}$.
  - Thus, the single instruction $G = B \oplus (B \gg 1)$ computes the exact Gray Code vector $G$ in 1 CPU cycle! ⚡

---

## 4. Internal Working Mechanics: Gray-to-Binary Conversion Algorithm

Tracing Gray-to-Binary Conversion for $G = 6$ (`110_2`):

```
Goal: Convert Gray Code G = 110_2 (Decimal 6) back to Standard Binary B.

Formula:
int num = g;
num ^= (num >>> 1);
num ^= (num >>> 2);
num ^= (num >>> 4);
num ^= (num >>> 8);
num ^= (num >>> 16);

Execution Steps:
g = 110_2 (6)
num = 110_2
num ^= (110_2 >>> 1 = 011_2) ──► 110 ^ 011 = 101_2
num ^= (101_2 >>> 2 = 001_2) ──► 101 ^ 001 = 100_2 (Decimal 4!)

Resulting Standard Binary B = 100_2 (Decimal 4).
Verification: Binary 4 -> Gray = 4 ^ (4 >> 1) = 100 ^ 010 = 110_2 (6)! ✅ ⚡
```

---

## 5. Visual Diagram: Single-Bit Rotary Encoder Application

```
Mechanical Rotary Encoder (Glitch-Free State Transitions):

Standard Binary Transition (1 -> 2):
001_2 ──► 010_2  (Bits 0 and 1 BOTH change simultaneously!)
If Bit 0 changes before Bit 1: Mechanical state momentarily reads 000_2 (FALSE STATE GLITCH!) ❌

Gray Code Transition (1 -> 2):
001_2 ──► 011_2  (ONLY Bit 1 changes!)
Glitch-Free Mechanical State Transition! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Binary-to-Gray Conversion, Gray-to-Binary Decoding, and LeetCode 89 Gray Code Sequence Generation.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Gray Code Algorithms:
 * Binary-to-Gray Encoders, Gray-to-Binary Decoders, and LeetCode 89 Sequence Generators.
 */
public class GrayCodeMaster {

    // =========================================================================
    // 1. BINARY TO GRAY & GRAY TO BINARY CONVERTERS (O(1) Time)
    // =========================================================================
    /**
     * Converts a standard binary integer B into its Gray Code representation.
     */
    public int binaryToGray(int b) {
        return b ^ (b >>> 1); // Single CPU Instruction! ⚡
    }

    /**
     * Converts a Gray Code integer G back into standard binary integer B.
     */
    public int grayToBinary(int g) {
        int b = g;
        b ^= (b >>> 1);
        b ^= (b >>> 2);
        b ^= (b >>> 4);
        b ^= (b >>> 8);
        b ^= (b >>> 16);
        return b; // Restores standard binary ⚡
    }

    // =========================================================================
    // 2. LEETCODE 89: GRAY CODE SEQUENCE GENERATOR (O(2^N) Time, O(2^N) Space)
    // =========================================================================
    /**
     * Generates an N-bit Gray Code sequence starting with 0.
     *
     * @param n number of bits
     * @return list of integer values forming valid Gray Code sequence
     */
    public List<Integer> grayCode(int n) {
        List<Integer> result = new ArrayList<>();
        if (n < 0 || n > 31) return result;

        int totalCount = 1 << n; // 2^N elements

        // Formula: sequence[i] = i ^ (i >> 1) ⚡
        for (int i = 0; i < totalCount; i++) {
            result.add(i ^ (i >>> 1));
        }

        return result;
    }

    // =========================================================================
    // 3. GRAY CODE SEQUENCE VALIDATOR
    // =========================================================================
    /**
     * Verifies that consecutive elements in sequence differ by EXACTLY 1 BIT.
     */
    public boolean isValidGrayCodeSequence(List<Integer> seq) {
        if (seq == null || seq.size() <= 1) return true;

        for (int i = 0; i < seq.size() - 1; i++) {
            int diff = seq.get(i) ^ seq.get(i + 1);
            // Verify diff has EXACTLY ONE set 1-bit! ⚡
            if ((diff & (diff - 1)) != 0 || diff == 0) {
                return false; // Invalid sequence!
            }
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// Gray Code Core Lines
int gray = b ^ (b >>> 1); list.add(i ^ (i >>> 1)); // Solves LeetCode 89 in O(2^N) linear time
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 89 - Gray Code**:
   - Sequence generation benchmark ($O(2^N)$ time, `i ^ (i >> 1)`).

2. **Rotary Encoders & Position Sensors**:
   - Glitch-free mechanical angle measurement.

3. **Karnaugh Maps (K-Maps)**:
   - Boolean expression simplification using adjacent Gray Code headers.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class GrayCodeDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GRAY CODE ALGORITHMS BENCHMARK DEMO           ");
        System.out.println("=================================================\n");

        GrayCodeMaster master = new GrayCodeMaster();

        // 1. Binary-to-Gray & Gray-to-Binary Test
        int binaryNum = 4; // 100_2
        int grayNum = master.binaryToGray(binaryNum);
        int restoredNum = master.grayToBinary(grayNum);

        System.out.println("1. Binary / Gray Code Conversions for 4 (100_2):");
        System.out.println("   Binary Integer     : " + binaryNum + " (100_2)");
        System.out.println("   Gray Code (b^(b>>1)): " + grayNum + " (110_2)");
        System.out.println("   Restored Binary    : " + restoredNum + " (100_2)");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 89 Sequence Test (N = 3 Bits)
        int n = 3;
        List<Integer> seq = master.grayCode(n);
        boolean valid = master.isValidGrayCodeSequence(seq);

        System.out.println("2. LeetCode 89 Gray Code Sequence Generation (N = 3 Bits):");
        System.out.println("   Generated Sequence: " + seq);
        System.out.println("   Is Sequence Valid (Hamming Distance = 1): " + valid);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Gray Code Task | Algorithm Formula | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Binary to Gray** | `g = b ^ (b >>> 1)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Single XOR shift |
| **Gray to Binary** | Shift-XOR Chain | $\mathbf{O(1)}$ 5 CPU Ops ⚡| $\mathbf{O(1)}$ Memory ⚡| Cumulative XOR |
| **Sequence Gen (89)**| `res.add(i ^ (i >>> 1))`| $\mathbf{O(2^N)}$ Linear ⚡| $\mathbf{O(2^N)}$ Array ⚡| $2^N$ total elements |

---

## 10. Edge Cases & Boundary Handling

1. **N = 0**:
   - Returns `[0]`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Generating Gray Code Using Backtracking Search**:
  - Writing DFS backtracking to generate Gray Code sequences takes $O(N \cdot 2^N)$ time. **ALWAYS use the 1-line formula `i ^ (i >> 1)` to generate LeetCode 89 in $O(2^N)$ time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** LeetCode 89 Gray Code Formula:
> To generate an $N$-bit Gray Code sequence in $O(2^N)$ time, iterate integer $i$ from $0$ to $2^N - 1$:
> $$\text{element} = i \oplus (i \gg 1)$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard Binary Sequence | Gray Code Sequence |
| :--- | :--- | :--- |
| **Bit Transitions** | Multi-bit changes (e.g. 3 $\to$ 4 changes 3 bits) | **EXACTLY 1 BIT CHANGE ⚡** |
| **Hardware Glitches**| High Risk of False Intermediate States | **Glitch-Free State Transitions ⚡**|
| **Formula** | Sequential Increment `i++` | **Reflected `i ^ (i >> 1)` ⚡** |

---

## 14. How to Recognize This in Questions

* **"Generate a sequence of 2^N integers where consecutive elements differ by 1 bit"** $\rightarrow$ LeetCode 89 (Gray Code).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does $G = B \oplus (B \gg 1)$ convert binary to Gray Code?**  
  *A:* Because bitwise XORing adjacent binary bits ($b_i \oplus b_{i+1}$) ensures that when binary increments from $B$ to $B+1$, exactly one bit position flips in the resulting Gray Code $G$.

* **Q: Where is Gray Code used in real-world hardware systems?**  
  *A:* In optical rotary encoders, analog-to-digital converters (ADCs), and asynchronous FIFO queue pointers (to prevent multi-bit CDC meta-stability glitches across clock domains).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRAY CODE                                             |
+-----------------------------------------------------------------------+
| • Single Bit Property: Consecutive elements differ by EXACTLY 1 BIT   |
| • Binary to Gray      : g = b ^ (b >>> 1)                             |
| • Gray to Binary      : b ^= (b >>> 1); b ^= (b >>> 2); ...           |
| • LeetCode 89         : list.add(i ^ (i >>> 1)) for i = 0..2^N-1 ⚡    |
| • Hardware Advantage  : Glitch-free state transitions in encoders ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Binary-to-Gray conversion `g = b ^ (b >>> 1)` in Java.
- [ ] I can write LeetCode 89 (`Gray Code Sequence`) in $O(2^N)$ time.
- [ ] I can write the Gray-to-Binary decoding algorithm.
- [ ] I can write a sequence validator checking Hamming Distance = 1.
- [ ] I can explain why Gray Code prevents mechanical rotary encoder glitches.
