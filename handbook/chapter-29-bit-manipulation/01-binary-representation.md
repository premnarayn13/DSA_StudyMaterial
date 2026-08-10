# 01. Binary Representation: Two's Complement, Sign Bits & Bitwise Storage Mechanics

## 1. Introduction
At the most fundamental level of computer architecture, all numerical data, memory addresses, and data structures are stored and manipulated as sequences of binary digits (**bits**: `0` and `1`). Understanding **Binary Representation** and hardware bitwise layout is essential for low-level system design, high-frequency trading engines, cryptographic protocols, and algorithmic optimizations. Signed integers in modern 32-bit and 64-bit systems are universally encoded using the **Two's Complement System**, which enables subtraction to be computed via standard addition circuitry without separate subtraction hardware. Two's Complement governs arithmetic bit shifts, sign bit extensions, overflow behavior, and key bit manipulation tricks like `-x = ~x + 1`.

> **Important:** The 4 Core Pillars of Binary Representation:
> 1. **Two's Complement Representation**:
>    - For a 32-bit signed integer `x`, the Most Significant Bit (MSB at bit 31) acts as the **Sign Bit**: `0` for non-negative integers, `1` for negative integers.
>    - To negate an integer $x$: Invert all bits (`~x`) and add 1 (`~x + 1`).
>      $$-x = \sim x + 1$$
> 2. **32-bit Integer Range Limits**:
>    - Minimum Value: `Integer.MIN_VALUE` = $-2^{31} = -2,147,483,648$ (`0x80000000` = `10000000 00000000 00000000 00000000`).
>    - Maximum Value: `Integer.MAX_VALUE` = $2^{31}-1 = 2,147,483,647$ (`0x7FFFFFFF` = `01111111 11111111 11111111 11111111`).
> 3. **Arithmetic vs Logical Right Shifts**:
>    - **Arithmetic Right Shift (`>>`)**: Preserves the sign bit by shifting in `1`s for negative numbers (sign-extension).
>    - **Logical Right Shift (`>>>`)**: Fills vacant left bits with `0`s regardless of sign (unsigned shift).
> 4. **IEEE 754 Floating-Point Encoding (32-bit Float)**:
>    - 1 Sign Bit + 8 Exponent Bits (Biased by 127) + 23 Mantissa/Fraction Bits. ⚡

```
Two's Complement 32-bit Integer Bit Topology:

MSB (Sign Bit)                                              LSB (Bit 0)
 │                                                               │
 ▼                                                               ▼
[S|B30|B29|B28| ...                                     ... |B2|B1|B0]

Positive Integer (+5):  00000000 00000000 00000000 00000101
Invert Bits (~5):       11111111 11111111 11111111 11111010
Add 1 (~5 + 1 = -5):    11111111 11111111 11111111 11111011 (-5 in Two's Complement!) ⚡
```

---

## 2. Core Concepts & Binary System Strategy Matrix

### 2.1 Integer & Bitwise Systems Comparison Matrix
```
Integer & Bitwise Systems Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Representation System | MSB Interpretation| Zero Representation| Range for N Bits  | Addition Hardware |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Unsigned Binary**   | Magnitude Bit     | Single `0`        | $[0 \dots 2^N-1]$ | Standard Adder    |
| **Sign-Magnitude**    | Separate Sign Bit | Double (`+0`, `-0`)| $[-(2^{N-1}-1) \dots 2^{N-1}-1]$| Extra Sign Logic  |
| **Two's Complement**  | **Weighted $-2^{N-1}$⚡**| **Single `0` ⚡** | **$[-2^{N-1} \dots 2^{N-1}-1]$⚡**| **Unified Adder ⚡**|
| **IEEE 754 Float**    | Sign / Exp / Mant | Denormalized / Inf| IEEE 754 Format   | Floating ALU      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Two's Complement negation: -x = ~x + 1! Arithmetic shift >> preserves sign; Logical shift >>> fills zeroes!"**

---

## 3. Characteristics & Two's Complement Mathematical Proof

### 3.1 Mathematical Proof of Two's Complement Negation
* In an $N$-bit integer system, the numerical value of a bit vector $B = (b_{N-1}, b_{N-2} \dots b_0)$ in Two's Complement is:
  $$V(B) = -b_{N-1} \cdot 2^{N-1} + \sum_{i=0}^{N-2} b_i \cdot 2^i$$
* **Proof that $-X = \sim X + 1$**:
  1. Let $X$ be an $N$-bit integer. The bitwise NOT operation $\sim X$ flips every bit of $X$.
  2. The sum of $X$ and $\sim X$ produces a bit vector with all bits set to 1 ($111\dots1_2$):
     $$X + \sim X = 2^N - 1$$
  3. Rearranging algebraically:
     $$\sim X + 1 = 2^N - X$$
  4. In $N$-bit modular arithmetic (modulo $2^N$), $2^N \equiv 0 \pmod{2^N}$:
     $$\sim X + 1 \equiv -X \pmod{2^N}$$
  5. Therefore, $\sim X + 1$ is the exact bit representation of $-X$ in Two's Complement! ⚡

---

## 4. Internal Working Mechanics: Arithmetic vs Logical Shifts

Tracing Bit Shift Operations on Negative Number `-8` (`0xFFFFFFF8` = `11111111 ... 11111000`):

```
Arithmetic Right Shift (-8 >> 2):
- Shifts bits right by 2 positions.
- Fills left 2 vacant bits with SIGN BIT '1' (Sign Extension).
- Result: 11111111 ... 11111110 = -2 in Two's Complement! ✅ ⚡

Logical Right Shift (-8 >>> 2):
- Shifts bits right by 2 positions.
- Fills left 2 vacant bits with '0' regardless of sign.
- Result: 00111111 ... 11111110 = 1,073,741,822 (Positive Integer)! ✅ ⚡
```

---

## 5. Visual Diagram: IEEE 754 Single-Precision Float Layout

```
IEEE 754 32-bit Single-Precision Float Layout:

Bit 31       Bit 30 ........ Bit 23    Bit 22 ........................ Bit 0
┌───────────┬─────────────────────────┬─────────────────────────────────────┐
│ Sign (S)  │ Exponent (E - 8 Bits)   │ Mantissa / Fraction (M - 23 Bits)   │
└───────────┴─────────────────────────┴─────────────────────────────────────┘
  1 Bit        Biased by 127            Implicit Leading 1.M

Value = (-1)^S * 2^(E - 127) * (1.M) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Binary Representation Converters, Two's Complement Visualizer, Bit Shift Analyzers, and IEEE 754 Inspection Engines.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Binary Representation:
 * Two's Complement Mechanics, Bit Shift Analyzers, and IEEE 754 Converters.
 */
public class BinaryRepresentationMaster {

    // =========================================================================
    // 1. TWO'S COMPLEMENT & BINARY STRING FORMATTER
    // =========================================================================
    /**
     * Converts a 32-bit integer into a formatted 32-character binary string with 4-bit groupings.
     *
     * @param num input 32-bit integer
     * @return formatted 32-bit binary string
     */
    public String toBinaryString32(int num) {
        StringBuilder sb = new StringBuilder();
        for (int i = 31; i >= 0; i--) {
            int bit = (num >>> i) & 1; // Logical right shift ⚡
            sb.append(bit);
            if (i > 0 && i % 4 == 0) sb.append(" ");
        }
        return sb.toString();
    }

    /**
     * Demonstrates Two's Complement Negation formula: -x = ~x + 1.
     */
    public boolean verifyTwosComplementNegation(int x) {
        int bitwiseNegation = ~x + 1;
        return bitwiseNegation == -x; // Always true in Two's Complement! ⚡
    }

    // =========================================================================
    // 2. ARITHMETIC VS LOGICAL RIGHT SHIFT DEMONSTRATOR
    // =========================================================================
    public String analyzeShifts(int num, int shiftCount) {
        int arithmeticShift = num >> shiftCount;  // Preserves sign bit
        int logicalShift = num >>> shiftCount;   // Fills zeroes

        return String.format(
            "Input: %d\n" +
            "Binary Original     : %s\n" +
            "Arithmetic (>> %d)  : %s (Value = %d)\n" +
            "Logical    (>>> %d) : %s (Value = %d)",
            num,
            toBinaryString32(num),
            shiftCount, toBinaryString32(arithmeticShift), arithmeticShift,
            shiftCount, toBinaryString32(logicalShift), logicalShift
        );
    }

    // =========================================================================
    // 3. IEEE 754 FLOAT BINARY INSPECTOR
    // =========================================================================
    public String inspectFloatIEEE754(float value) {
        int bits = Float.floatToIntBits(value);
        int sign = (bits >>> 31) & 1;
        int exponent = (bits >>> 23) & 0xFF;
        int mantissa = bits & 0x7FFFFF;

        return String.format(
            "Float Value: %f\n" +
            "Raw 32-bit Hex : 0x%08X\n" +
            "Sign Bit (S)   : %d (%s)\n" +
            "Exponent (E)   : %d (Unbiased E-127 = %d)\n" +
            "Mantissa (M)   : 0x%06X (Binary = %s)",
            value, bits, sign, (sign == 0 ? "+" : "-"),
            exponent, (exponent - 127),
            mantissa, Integer.toBinaryString(mantissa)
        );
    }
}
```

> **Quick Syntax:**
```java
// Two's Complement Negation & Shift Lines
int negX = ~x + 1; int arithmetic = num >> shift; int logical = num >>> shift;
```

---

## 7. Concrete Problem Examples & Applications

1. **Two's Complement Inspection**:
   - Fundamental bitwise arithmetic representation ($O(1)$ time).

2. **LeetCode 191 - Number of 1 Bits**:
   - Counting set bits in binary representation of 32-bit unsigned integer.

3. **Cryptographic Hash Bit Layouts**:
   - SHA-256 and MD5 bitwise message padding algorithms.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class BinaryRepresentationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BINARY REPRESENTATION & SHIFTS BENCHMARK DEMO ");
        System.out.println("=================================================\n");

        BinaryRepresentationMaster master = new BinaryRepresentationMaster();

        // 1. Two's Complement Negation Test
        int num = 5;
        System.out.println("1. Two's Complement Negation for x = " + num + ":");
        System.out.println("   Positive 5  : " + master.toBinaryString32(num));
        System.out.println("   Bitwise ~5  : " + master.toBinaryString32(~num));
        System.out.println("   -5 (~5 + 1) : " + master.toBinaryString32(-num));
        System.out.println("   Verification (-x == ~x + 1): " + master.verifyTwosComplementNegation(num));
        System.out.println("-------------------------------------------------");

        // 2. Shift Analysis for Negative Number (-8)
        System.out.println("2. Shift Analysis for Negative Integer -8:");
        System.out.println(master.analyzeShifts(-8, 2));
        System.out.println("-------------------------------------------------");

        // 3. IEEE 754 Float Inspection
        System.out.println("3. IEEE 754 Floating-Point Inspection for 3.14159f:");
        System.out.println(master.inspectFloatIEEE754(3.14159f));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Binary Representation Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Two's Complement Negation** | $\mathbf{O(1)}$ Single Instruction⚡| $\mathbf{O(1)}$ Memory ⚡| `-x = ~x + 1` |
| **Arithmetic Right Shift (`>>`)**| $\mathbf{O(1)}$ Single Instruction⚡| $\mathbf{O(1)}$ Memory ⚡| Preserves sign bit |
| **Logical Right Shift (`>>>`)**| $\mathbf{O(1)}$ Single Instruction⚡| $\mathbf{O(1)}$ Memory ⚡| Fills zeroes |

---

## 10. Edge Cases & Boundary Handling

1. **Integer Overflow Beyond `Integer.MAX_VALUE`**:
   - `Integer.MAX_VALUE + 1` wraps around to `Integer.MIN_VALUE` (`-2,147,483,648`) in Two's Complement.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using `>>` Instead of `>>>` for Unsigned Bit Manipulation**:
  - Using arithmetic right shift `>>` on negative integers shifts in `1`s at the MSB, causing infinite loops when iterating until `num == 0`. **ALWAYS use logical shift `>>>` for unsigned bit manipulation!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Two's Complement Negation Rule:
> In Two's Complement arithmetic, negating any integer $x$ is ALWAYS equivalent to bitwise inverting all bits and adding 1:
> $$-x = \sim x + 1$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Arithmetic Shift (`>>`) | Logical Shift (`>>>`) |
| :--- | :--- | :--- |
| **Vacant Bit Filling** | **Copies Sign Bit (Sign Extension) ⚡**| **Fills Zeroes (`0`) ⚡** |
| **Negative Behavior** | Keeps Number Negative | Converts to Positive Value |
| **Ideal Application** | Signed Division by $2^k$ | **Bitmask Unsigned Scanning ⚡** |

---

## 14. How to Recognize This in Questions

* **"Explain how negative numbers are stored in 32-bit Java integers"** $\rightarrow$ Two's Complement System.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Two's Complement use `~x + 1` to negate a number?**  
  *A:* Because $X + \sim X = 2^N - 1$, which implies $\sim X + 1 = 2^N - X \equiv -X \pmod{2^N}$.

* **Q: What is the difference between `>>` and `>>>` in Java?**  
  *A:* `>>` is an arithmetic right shift that preserves the sign bit by filling vacant MSB bits with `1`s for negative numbers, whereas `>>>` is a logical right shift that fills MSB bits with `0`s regardless of sign.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY REPRESENTATION                                 |
+-----------------------------------------------------------------------+
| • Negation Rule : -x = ~x + 1 in Two's Complement arithmetic          |
| • Sign Bit MSB  : Bit 31 is 0 for non-negative, 1 for negative        |
| • Arithmetic >> : Sign-extending shift (fills 1s for negative numbers)|
| • Logical >>>   : Unsigned shift (fills 0s regardless of sign) ⚡       |
| • Min Value     : Integer.MIN_VALUE = 0x80000000 = -2,147,483,648      |
| • Max Value     : Integer.MAX_VALUE = 0x7FFFFFFF =  2,147,483,647      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Two's Complement negation `-x = ~x + 1` in Java.
- [ ] I can explain the difference between arithmetic `>>` and logical `>>>` shifts.
- [ ] I can state the 32-bit Integer min (`0x80000000`) and max (`0x7FFFFFFF`) hex values.
- [ ] I can explain why Two's Complement has only a single zero representation.
- [ ] I can inspect IEEE 754 float sign, exponent, and mantissa bits in Java.
