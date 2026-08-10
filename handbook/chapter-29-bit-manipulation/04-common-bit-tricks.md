# 04. Common Bit Tricks: Power of 2, ASCII Case Conversions & Fast Arithmetic

## 1. Introduction
**Bit Manipulation Hacks** are ultra-fast $O(1)$ hardware idioms that replace expensive arithmetic operations (division, modulo, string casing, conditional branches) with single CPU clock cycle bitwise instructions. Because CPU ALUs process bit shifts, AND masks, and XOR operators in 1 clock cycle, using bit tricks optimizes execution speed in high-performance competitive programming, game engines, and production systems. Key classic bit tricks include **Fast Parity Check (`(x & 1) == 0`)**, **Power of Two Verification (`(x & (x - 1)) == 0`)**, **ASCII Case Switching via Bit 5 Tricks (`ch | ' '` and `ch & '_'`)**, and **Fast Modulo by Power of Two (`x & (2^k - 1)`)**.

> **Important:** The 6 Master Bit Manipulation Hacks:
> 1. **Fast Parity (Even / Odd Check)**:
>    $$\text{isEven}(x) = ((x \;\&\; 1) == 0) \quad \text{and} \quad \text{isOdd}(x) = ((x \;\&\; 1) \neq 0)$$
> 2. **Power of Two Verification (LeetCode 231)**:
>    $$\text{isPowerOfTwo}(x) = (x > 0) \;\&\&\; ((x \;\&\; (x - 1)) == 0)$$
> 3. **Fast Modulo by Power of Two ($2^k$)**:
>    $$x \pmod{2^k} = x \;\&\; (2^k - 1)$$
> 4. **ASCII Case Conversion Hacks (Bit 5 Control)**:
>    - Convert to Lowercase: `ch | ' '` (Bit 5 = 1, `'A'` $\to$ `'a'`).
>    - Convert to Uppercase: `ch & '_'` (Bit 5 = 0, `'a'` $\to$ `'A'`).
>    - Toggle Letter Case : `ch ^ ' '` (Flips Bit 5).
> 5. **Fast Multiplication & Division by $2^k$**:
>    - Multiply by $2^k$: `x << k`. Divide by $2^k$: `x >> k`.
> 6. **In-Place Swap Without Temp Variable**:
>    - `a ^= b; b ^= a; a ^= b;` ⚡

```
ASCII Bit 5 Case Conversion Topology:

ASCII 'A' (65): 01000001_2
ASCII 'a' (97): 01100001_2  <-- Bit 5 (value 32) controls case!

- 'A' | ' ' (32) ──► 01000001 | 00100000 = 01100001 ('a' Lowercase!) ✅
- 'a' & '_' (95) ──► 01100001 & 11011111 = 01000001 ('A' Uppercase!) ✅
- 'A' ^ ' ' (32) ──► 01000001 ^ 00100000 = 01100001 ('a' Toggled!) ✅ ⚡
```

---

## 2. Core Concepts & Bit Tricks Strategy Matrix

### 2.1 Common Bit Hacks Strategy Matrix
```
Common Bit Hacks Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Goal / Problem        | Bitwise Hack      | Classical Operator| Speedup Factor    | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Even / Odd Check**  | `(x & 1) == 0`    | `x % 2 == 0`      | **2x Faster ⚡**   | Parity Test       |
| **Power of Two**      | `(x & (x-1)) == 0`| `while(x%2==0)`   | **$O(1)$ Instant ⚡**| LeetCode 231      |
| **Modulo by $2^k$**   | `x & (2^k - 1)`   | `x % (2^k)`       | **3x Faster ⚡**   | Ring Buffer Index |
| **Convert Lowercase** | `ch | ' '`        | `Character.to...` | **1 CPU Cycle ⚡** | Fast Parsing      |
| **Convert Uppercase** | `ch & '_'`        | `Character.to...` | **1 CPU Cycle ⚡** | Fast Parsing      |
| **Toggle Letter Case**| `ch ^ ' '`        | `Character.is...` | **1 CPU Cycle ⚡** | Case Inversion    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Power of 2 = (x > 0) && ((x & (x - 1)) == 0); Lowercase = ch | ' '; Uppercase = ch & '_'; Toggle = ch ^ ' '!"**

---

## 3. Characteristics & Power of Two Mathematical Proof

### 3.1 Mathematical Proof of Power of Two Check `(x & (x - 1)) == 0`
* A positive integer $x > 0$ is a **Power of Two** if and only if $x = 2^k$ for some non-negative integer $k$.
* **Binary Representation of $2^k$**:
  - $x = 2^k$ has EXACTLY ONE set bit at position $k$:
    $$x = 100\dots0_2$$
* **Binary Representation of $x - 1$**:
  - Subtracting 1 flips bit $k$ to 0 and all lower bits $0 \dots k-1$ to 1:
    $$x - 1 = 011\dots1_2$$
* **Bitwise AND Product**:
  - Bitwise ANDing $x \; \& \; (x - 1)$ yields:
    $$x \; \& \; (x - 1) = 100\dots0_2 \;\&\; 011\dots1_2 = 000\dots0_2 = 0$$
* If $x$ is NOT a power of two, $x$ has $\ge 2$ set bits. Clearing the lowest set bit leaves at least one other 1-bit, so $x \; \& \; (x - 1) \neq 0$.
* Therefore, $(x > 0) \;\&\&\; ((x \; \& \; (x - 1)) == 0)$ is a necessary and sufficient test for Power of Two! ⚡

---

## 4. Internal Working Mechanics: Fast Modulo by Power of Two ($2^k$)

Tracing Fast Modulo $x \pmod{8}$ for $x = 29$ ($29 = 11101_2$, $8 = 2^3$, Mask $8 - 1 = 7 = 111_2$):

```
Goal: Calculate 29 % 8 without expensive integer division hardware.

Number 29 in Binary: 11101_2 (29 = 16 + 8 + 4 + 1)
Mask (8 - 1 = 7)   : 00111_2 (Lowest 3 bits)

Bitwise AND:
  11101 (29)
& 00111 (7)
───────────
  00101 (5!)

29 % 8 = 5 in 1 CPU Clock Cycle! ✅ ⚡
```

---

## 5. Visual Diagram: ASCII Case Switching Tricks

```
ASCII Bit 5 Case Switching Operations:

Space Character ' '     : 00100000_2 (Decimal 32)
Underscore Character '_' : 11011111_2 (Bitwise NOT of 32!)

'A' | ' '  ──► Sets Bit 5 to 1  ──► 'a' (Lowercase!) ✅
'a' & '_'  ──► Clears Bit 5 to 0 ──► 'A' (Uppercase!) ✅
'A' ^ ' '  ──► Flips Bit 5      ──► 'a' (Toggled!) ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing all 6 Common Bit Manipulation Hacks, Power of Two Verifiers (LeetCode 231), and Fast ASCII Case Switchers.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Common Bit Manipulation Hacks:
 * Power of Two Checks, ASCII Case Switches, Fast Modulo, and Parity Tests.
 */
public class CommonBitTricksMaster {

    // =========================================================================
    // 1. FAST ARITHMETIC & PARITY TRICKS
    // =========================================================================
    public boolean isEven(int x) { return (x & 1) == 0; } // Fast parity ⚡
    public boolean isOdd(int x)  { return (x & 1) != 0; }

    public int multiplyByPowerOfTwo(int x, int k) { return x << k; } // x * 2^k
    public int divideByPowerOfTwo(int x, int k)   { return x >> k; } // x / 2^k

    /**
     * Fast Modulo by Power of Two (x % 2^k = x & (2^k - 1)).
     */
    public int moduloPowerOfTwo(int x, int powerOfTwo) {
        return x & (powerOfTwo - 1); // e.g. x % 8 = x & 7 ⚡
    }

    // =========================================================================
    // 2. LEETCODE 231: POWER OF TWO CHECKER (O(1) Time, O(1) Space)
    // =========================================================================
    /**
     * Checks if an integer is a power of two.
     */
    public boolean isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0; // O(1) Instant! ⚡
    }

    // =========================================================================
    // 3. ASCII CASE CONVERSION TRICKS (BIT 5 CONTROL)
    // =========================================================================
    public char toLowerCaseBitwise(char ch) {
        return (char) (ch | ' '); // Sets bit 5 to 1 ('A' -> 'a') ⚡
    }

    public char toUpperCaseBitwise(char ch) {
        return (char) (ch & '_'); // Clears bit 5 to 0 ('a' -> 'A') ⚡
    }

    public char toggleCaseBitwise(char ch) {
        return (char) (ch ^ ' '); // Flips bit 5 ⚡
    }
}
```

> **Quick Syntax:**
```java
// Common Bit Hacks Lines
boolean isPowerOf2 = (n > 0 && (n & (n - 1)) == 0); char lower = (char)(ch | ' '); char upper = (char)(ch & '_');
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 231 - Power of Two**:
   - Primary power of two verification benchmark solved in $O(1)$ time.

2. **Circular Ring Buffer Indexing**:
   - Fast index wrap-around `idx = (idx + 1) & (CAPACITY - 1)` where capacity is a power of 2.

3. **High-Speed String & Token Parsers**:
   - In-place ASCII case conversion using bitwise OR/AND.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class CommonBitTricksDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   COMMON BIT TRICKS BENCHMARK DEMO             ");
        System.out.println("=================================================\n");

        CommonBitTricksMaster master = new CommonBitTricksMaster();

        // 1. Fast Parity & Modulo Test
        int num = 29;
        System.out.println("1. Fast Parity & Modulo Test for x = " + num + ":");
        System.out.println("   Is Even (29 & 1 == 0): " + master.isEven(num));
        System.out.println("   Fast Modulo 29 % 8 (29 & 7): " + master.moduloPowerOfTwo(num, 8) + " (Optimal = 5)");
        System.out.println("-------------------------------------------------");

        // 2. Power of Two Test (LeetCode 231)
        int n1 = 16, n2 = 18;
        System.out.println("2. Power of Two Verification (LeetCode 231):");
        System.out.println("   Is 16 Power of Two: " + master.isPowerOfTwo(n1) + " (Optimal = true)");
        System.out.println("   Is 18 Power of Two: " + master.isPowerOfTwo(n2) + " (Optimal = false)");
        System.out.println("-------------------------------------------------");

        // 3. ASCII Case Conversion Hacks
        char upper = 'G', lower = 'g';
        System.out.println("3. ASCII Case Conversion Hacks:");
        System.out.println("   'G' | ' ' -> Lowercase : '" + master.toLowerCaseBitwise(upper) + "'");
        System.out.println("   'g' & '_' -> Uppercase : '" + master.toUpperCaseBitwise(lower) + "'");
        System.out.println("   'G' ^ ' ' -> Toggle Case: '" + master.toggleCaseBitwise(upper) + "'");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Common Bit Hack | Bitwise Formula | Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Even / Odd Check** | `(x & 1) == 0` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡|
| **Power of Two (231)**| `(n > 0) && ((n & (n - 1)) == 0)`| $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡|
| **Modulo by $2^k$** | `x & (2^k - 1)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡|
| **To Lowercase** | `ch | ' '` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡|
| **To Uppercase** | `ch & '_'` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡|

---

## 10. Edge Cases & Boundary Handling

1. **Power of Two for Negative Numbers or Zero (`n <= 0`)**:
   - Must check `n > 0` before `(n & (n - 1)) == 0` to prevent false positive for `n = 0`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Omitting `n > 0` in Power of Two Check**:
  - For `n = 0`, `0 & -1 = 0`, which satisfies `(n & (n - 1)) == 0` even though 0 is NOT a power of two. **ALWAYS check `n > 0 && ((n & (n - 1)) == 0)`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Power of Two Formula:
> To check if integer $n$ is a Power of Two, ALWAYS include the positivity check:
> $$\text{isPowerOfTwo}(n) = (n > 0) \;\&\&\; ((n \;\&\; (n - 1)) == 0)$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Classical Modulo (`x % 8`) | Bitwise Modulo (`x & 7`) |
| :--- | :--- | :--- |
| **Execution Hardware** | Integer Division Unit | **Bitwise AND ALU ⚡** |
| **Clock Cycles** | ~10 to 20 Cycles | **1 Cycle ⚡** |
| **Requirement** | Any divisor | Divisor MUST be Power of $2^k$ |

---

## 14. How to Recognize This in Questions

* **"Check if a number is a power of two in O(1) time"** $\rightarrow$ LeetCode 231 (`n > 0 && (n & (n - 1)) == 0`).
* **"Convert letter case without branching"** $\rightarrow$ `ch | ' '` and `ch & '_'`.

---

## 15. Frequently Asked Interview Questions

* **Q: How does `ch | ' '` convert uppercase letters to lowercase?**  
  *A:* In ASCII encoding, uppercase and lowercase letters differ by bit 5 (value 32). Space `' '` has ASCII value 32 (`00100000_2`). Bitwise ORing `ch | ' '` sets bit 5 to 1, converting uppercase `'A'` (65) to lowercase `'a'` (97).

* **Q: How does `ch & '_'` convert lowercase letters to uppercase?**  
  *A:* Underscore `'_'` has ASCII value 95 (`11011111_2`), which has bit 5 set to 0 and all other bits set to 1. Bitwise ANDing `ch & '_'` clears bit 5 to 0, converting lowercase `'a'` (97) to uppercase `'A'` (65).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COMMON BIT TRICKS                                     |
+-----------------------------------------------------------------------+
| • Power of 2 : (n > 0) && ((n & (n - 1)) == 0)  (LeetCode 231) ⚡     |
| • Even / Odd : (x & 1) == 0 (Even) | (x & 1) != 0 (Odd)               |
| • Modulo 2^k : x & (2^k - 1)  (e.g. x % 8 = x & 7)                    |
| • Lowercase  : ch | ' '  (Sets bit 5 to 1)                           |
| • Uppercase  : ch & '_'  (Clears bit 5 to 0)                          |
| • Toggle Case: ch ^ ' '  (Flips bit 5)                                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 231 (`Power of Two`) in Java in $O(1)$ time.
- [ ] I can write fast parity checks `(x & 1) == 0`.
- [ ] I can write fast modulo by $2^k$ (`x & (2^k - 1)`).
- [ ] I can state the ASCII case conversion tricks (`ch | ' '`, `ch & '_'`, `ch ^ ' '`).
- [ ] I can explain why `n > 0` is required for Power of Two verification.
