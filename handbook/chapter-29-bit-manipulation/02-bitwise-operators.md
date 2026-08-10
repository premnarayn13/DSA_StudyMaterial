# 02. Bitwise Operators: Truth Tables, Algebraic Laws & Precedence Rules

## 1. Introduction
**Bitwise Operators** perform direct bit-by-bit manipulation on integral types (`byte`, `short`, `char`, `int`, `long`) at the hardware CPU level. Operating on primitive bits in a single CPU clock cycle, bitwise operators power high-performance algorithms, system flag vectors, network packet serialization, and memory-efficient data structures. Java supports seven fundamental bitwise operators: **Bitwise AND (`&`)**, **Bitwise OR (`|`)**, **Bitwise XOR (`^`)**, **Bitwise NOT (`~`)**, **Left Shift (`<<`)**, **Arithmetic Right Shift (`>>`)**, and **Logical Right Shift (`>>>`)**. Mastering bitwise truth tables, algebraic laws (Commutative, Associative, Distributive, De Morgan's), and operator precedence prevents subtle bugs in production code.

> **Important:** Core Structural Properties of Bitwise Operators:
> 1. **Bitwise AND (`&`)**:
>    - $1 \;\&\; 1 = 1$; $1 \;\&\; 0 = 0$; $0 \;\&\; 0 = 0$.
>    - Primary Purpose: **Bit Extraction & Masking** (e.g. `(x & (1 << k))` checks if bit $k$ is set).
> 2. **Bitwise OR (`|`)**:
>    - $1 \mid 0 = 1$; $0 \mid 0 = 0$; $1 \mid 1 = 1$.
>    - Primary Purpose: **Setting Bit Flags** (e.g. `x | (1 << k)` sets bit $k$ to 1).
> 3. **Bitwise XOR (`^`)**:
>    - $1 \oplus 1 = 0$; $0 \oplus 0 = 0$; $1 \oplus 0 = 1$.
>    - Primary Purpose: **Toggling Bits & Cancellation Invariant** ($A \oplus A = 0$ and $A \oplus 0 = A$).
> 4. **Operator Precedence Warning**:
>    - Bitwise operators (`&`, `|`, `^`) have **LOWER PRECEDENCE** than comparison operators (`==`, `!=`, `<`, `>`).
>    - ALWAYS surround bitwise expressions with parentheses: `((x & mask) == 0)`! ⚡

```
Bitwise Operators Truth Table Topology:

Bit A   Bit B   A & B (AND)   A | B (OR)   A ^ B (XOR)   ~A (NOT)
───────────────────────────────────────────────────────────────────
  0       0          0            0            0            1
  0       1          0            1            1            1
  1       0          0            1            1            0
  1       1          1            1            0            0

XOR (^) outputs 1 if and only if bits A and B are DIFFERENT! ⚡
```

---

## 2. Core Concepts & Bitwise Operators Strategy Matrix

### 2.1 Bitwise Operators Characteristic Matrix
```
Bitwise Operators Characteristic Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Bitwise Operator      | Symbol / Syntax   | Algebraic Property| Primary Pattern   | Hardware Speed    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Bitwise AND**       | `x & y`           | $A \& 0 = 0$      | **Bit Masking ⚡** | **1 CPU Cycle ⚡** |
| **Bitwise OR**        | `x | y`           | $A | 1 = 1$      | **Flag Setting ⚡**| **1 CPU Cycle ⚡** |
| **Bitwise XOR**       | `x ^ y`           | $A \oplus A = 0$  | **Bit Toggling ⚡**| **1 CPU Cycle ⚡** |
| **Bitwise NOT**       | `~x`              | $\sim(\sim A) = A$| One's Complement  | **1 CPU Cycle ⚡** |
| **Left Shift**        | `x << k`          | $x \times 2^k$    | Fast Multiply     | **1 CPU Cycle ⚡** |
| **Arithmetic Right**  | `x >> k`          | $\lfloor x / 2^k \rfloor$| Signed Divide| **1 CPU Cycle ⚡** |
| **Logical Right**     | `x >>> k`         | Unsigned Shift    | Unsigned Scan     | **1 CPU Cycle ⚡** |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"AND masks bits; OR sets bits; XOR toggles bits and satisfies A ^ A = 0; Always use parentheses ((x & y) == 0)!"**

---

## 3. Characteristics & Bitwise Algebraic Laws Proof

### 3.1 Mathematical Formalism of Bitwise Laws
* Let $A, B, C$ be $N$-bit vectors. Bitwise operators satisfy classical Boolean algebra laws:
* **1. Identity Laws**:
  $$A \& \text{0xFFFFFFFF} = A \quad \text{and} \quad A \mid 0 = A \quad \text{and} \quad A \oplus 0 = A$$
* **2. Annihilator Laws**:
  $$A \& 0 = 0 \quad \text{and} \quad A \mid \text{0xFFFFFFFF} = \text{0xFFFFFFFF}$$
* **3. Cancellation Law of XOR**:
  $$A \oplus A = 0 \implies (A \oplus B) \oplus B = A$$
  (Powers in-place variable swapping and single-number finding!).
* **4. De Morgan's Bitwise Laws**:
  $$\sim(A \& B) = (\sim A) \mid (\sim B) \quad \text{and} \quad \sim(A \mid B) = (\sim A) \& (\sim B)$$
* **5. Distributive Laws**:
  $$A \& (B \mid C) = (A \& B) \mid (A \& C) \quad \text{and} \quad A \mid (B \& C) = (A \mid B) \& (A \mid C)$$ ⚡

---

## 4. Internal Working Mechanics: In-Place XOR Variable Swap

Tracing In-Place XOR Variable Swap for $A = 12$ (`1100_2`) and $B = 25$ (`11001_2`):

```
Initial: A = 12, B = 25.

Step 1: A = A ^ B
- A = 12 ^ 25 = 01100 ^ 11001 = 10101 (21).

Step 2: B = A ^ B
- B = 21 ^ 25 = (12 ^ 25) ^ 25 = 12 ^ (25 ^ 25) = 12 ^ 0 = 12! (B is now 12!) ⚡

Step 3: A = A ^ B
- A = 21 ^ 12 = (12 ^ 25) ^ 12 = 25 ^ (12 ^ 12) = 25 ^ 0 = 25! (A is now 25!) ⚡

Swaps A and B in-place with ZERO temporary variables! ✅ ⚡
```

---

## 5. Visual Diagram: Bitwise Precedence Trap

```
Bitwise Operator Precedence Danger Zone:

Writing: if (x & mask == 0)

Evaluation Order (Due to Precedence):
1. Evaluates (mask == 0) FIRST!
2. Then evaluates x & (result of comparison).
BUG TRIGGERED! ❌

Correct Parenthesized Code:
if ((x & mask) == 0) ──► Evaluates (x & mask) FIRST! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Bitwise Operations, In-Place XOR Swapping, De Morgan's Law Verification, and Precedence Safety Checkers.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bitwise Operators:
 * Truth Tables, Algebraic Bit Laws, In-Place XOR Swaps, and Precedence Guards.
 */
public class BitwiseOperatorsMaster {

    // =========================================================================
    // 1. BITWISE OPERATOR CORE FUNCTIONS
    // =========================================================================
    public int bitwiseAnd(int a, int b) { return a & b; }
    public int bitwiseOr(int a, int b)  { return a | b; }
    public int bitwiseXor(int a, int b) { return a ^ b; }
    public int bitwiseNot(int a)        { return ~a; }

    // =========================================================================
    // 2. IN-PLACE XOR VARIABLE SWAPPER (O(1) Memory, No Temp Variable)
    // =========================================================================
    /**
     * Swaps values of a 2-element array in-place using XOR cancellation invariant.
     */
    public void swapInPlaceXOR(int[] pair) {
        if (pair == null || pair.length < 2 || pair[0] == pair[1]) return;

        pair[0] = pair[0] ^ pair[1]; // Step 1: A = A ^ B ⚡
        pair[1] = pair[0] ^ pair[1]; // Step 2: B = (A ^ B) ^ B = A ⚡
        pair[0] = pair[0] ^ pair[1]; // Step 3: A = (A ^ B) ^ A = B ⚡
    }

    // =========================================================================
    // 3. DE MORGAN'S BITWISE LAWS VERIFIER
    // =========================================================================
    public boolean verifyDeMorgansLaws(int a, int b) {
        int left1 = ~(a & b);
        int right1 = (~a) | (~b);

        int left2 = ~(a | b);
        int right2 = (~a) & (~b);

        return (left1 == right1) && (left2 == right2); // Always true! ⚡
    }

    // =========================================================================
    // 4. PRECEDENCE SAFE BIT MASK CHECKER
    // =========================================================================
    /**
     * Checks if bit at position k is set (1), using correct parentheses.
     */
    public boolean isBitSet(int num, int k) {
        return ((num & (1 << k)) != 0); // Mandatory double parentheses! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Bitwise Operator Core Lines
int andVal = a & b; int orVal = a | b; int xorVal = a ^ b; boolean bitSet = ((num & (1 << k)) != 0);
```

---

## 7. Concrete Problem Examples & Applications

1. **In-Place XOR Variable Swap**:
   - Swapping primitive values without allocating extra stack variables ($O(1)$ time).

2. **LeetCode 136 - Single Number**:
   - Finding the single element in array where every other element appears twice ($O(N)$ time, $O(1)$ space using XOR cancellation $A \oplus A = 0$).

3. **Bitmask System Flag Vector**:
   - Managing read/write/execute permissions using bitwise OR and AND flags.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BitwiseOperatorsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BITWISE OPERATORS BENCHMARK DEMO             ");
        System.out.println("=================================================\n");

        BitwiseOperatorsMaster master = new BitwiseOperatorsMaster();

        // 1. In-Place XOR Swap Test
        int[] pair = {12, 25};
        System.out.println("1. In-Place XOR Swap Test:");
        System.out.println("   Before Swap: " + Arrays.toString(pair));
        master.swapInPlaceXOR(pair);
        System.out.println("   After Swap : " + Arrays.toString(pair) + " (Swapped In-Place!)");
        System.out.println("-------------------------------------------------");

        // 2. De Morgan's Laws Verification
        int a = 0b1100, b = 0b1010;
        boolean deMorganVerified = master.verifyDeMorgansLaws(a, b);
        System.out.println("2. De Morgan's Bitwise Laws Verification:");
        System.out.println("   ~(A & B) == (~A | ~B) Verified: " + deMorganVerified);
        System.out.println("-------------------------------------------------");

        // 3. Bit Mask Checker
        int flags = 0b10100; // Bit 2 and Bit 4 set
        System.out.println("3. Bit Mask Check for Number 0b10100:");
        System.out.println("   Is Bit 2 Set: " + master.isBitSet(flags, 2));
        System.out.println("   Is Bit 3 Set: " + master.isBitSet(flags, 3));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bitwise Operator | Algebraic Property | Hardware Speed | Key Application |
| :--- | :--- | :--- | :--- |
| **Bitwise AND (`&`)** | $A \& 0 = 0$ | $\mathbf{O(1)}$ Single CPU Cycle⚡| Bit extraction & masking |
| **Bitwise OR (`|`)**  | $A \mid 1 = 1$ | $\mathbf{O(1)}$ Single CPU Cycle⚡| Flag vector setting |
| **Bitwise XOR (`^`)** | $A \oplus A = 0$ | $\mathbf{O(1)}$ Single CPU Cycle⚡| Toggling & single number |

---

## 10. Edge Cases & Boundary Handling

1. **In-Place XOR Swap on Same Memory Location (`a[i]` and `a[i]`)**:
   - Calling `swap(a, i, i)` zeroes out `a[i]` because `a[i] ^ a[i] = 0`. Guard with `if (pair[0] == pair[1]) return;`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Omitting Parentheses Around Bitwise Operator Expressions**:
  - Writing `if (x & 1 == 0)` evaluates `1 == 0` first due to precedence, producing incorrect results. **ALWAYS write `if ((x & 1) == 0)`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Operator Precedence Rule:
> Bitwise operators (`&`, `|`, `^`) have **LOWER precedence** than relational operators (`==`, `!=`, `<`, `>`). ALWAYS wrap bitwise operations in parentheses: `((x & mask) != 0)`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Logical Operators (`&&`, `||`) | Bitwise Operators (`&`, `|`) |
| :--- | :--- | :--- |
| **Operand Type** | Boolean Expressions | Integral Bits (`int`, `long`) |
| **Short-Circuiting**| Short-circuits evaluation | **No Short-Circuiting ⚡** |
| **Execution** | Conditional Jumps | **Hardware Bit ALU ⚡** |

---

## 14. How to Recognize This in Questions

* **"Swap two variables without using a temporary variable"** $\rightarrow$ In-Place XOR Swap.
* **"Check if k-th bit is set or set k-th bit to 1"** $\rightarrow$ Bitwise AND / OR.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does $A \oplus A = 0$ hold for any integer $A$?**  
  *A:* Because XOR outputs 0 when input bits are identical. Matching every set bit of $A$ with itself produces all 0 bits.

* **Q: Why are parentheses mandatory around bitwise expressions like `((x & 1) == 0)`?**  
  *A:* Because `==` has higher precedence than `&`. Without parentheses, `x & 1 == 0` parses as `x & (1 == 0)`, evaluating `x & false` which produces a compilation error or logical bug.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BITWISE OPERATORS                                     |
+-----------------------------------------------------------------------+
| • AND  (&)  : Extracts / masks bits (1 & 1 = 1; 1 & 0 = 0)            |
| • OR   (|)  : Sets bit flags (1 | 0 = 1; 0 | 0 = 0)                   |
| • XOR  (^)  : Toggles bits & satisfies A ^ A = 0 and A ^ 0 = A        |
| • NOT  (~)  : Inverts all bits (One's Complement)                     |
| • Swap      : A=A^B; B=A^B; A=A^B (In-place swap without temp!)      |
| • Precedence: ALWAYS use parentheses: ((x & mask) == 0)! ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Bitwise AND, OR, XOR, and NOT operations in Java.
- [ ] I can write the In-Place XOR variable swap algorithm.
- [ ] I can state why parentheses are required around `((x & mask) == 0)`.
- [ ] I can state De Morgan's bitwise laws ($\sim(A \& B) = \sim A \mid \sim B$).
- [ ] I can explain why $A \oplus A = 0$ holds for all integers.
