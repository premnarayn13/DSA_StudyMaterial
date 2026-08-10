# 03. Bit Masks: Setting, Clearing, Toggling & Bit Extraction Formulas

## 1. Introduction
A **Bit Mask** is a specialized integer value whose binary bit pattern is used as a filter to selectively inspect, set, clear, toggle, or isolate specific bit positions within a target bit vector. Bit Masking is the core operational language of system kernels, hardware driver registers, network protocol flags, and optimal graph/DP algorithms. By creating single-bit masks (`1 << k`) or multi-bit range masks, developers can execute precise bitwise modifications in $O(1)$ single CPU clock cycles. Master formulas like **Brian Kernighan's Lowest Bit Clearer (`x & (x - 1)`)** and **The Lowest Set Bit Extractor (`x & (-x)`)** form the foundational building blocks of advanced structures like Fenwick Trees (Binary Indexed Trees).

> **Important:** The 6 Master Bit Masking Formulas:
> 1. **Check Bit $k$ Is Set**:
>    $$\text{isSet}(x, k) = ((x \;\&\; (1 \ll k)) \neq 0)$$
> 2. **Set Bit $k$ (Turn Bit ON)**:
>    $$\text{setBit}(x, k) = x \mid (1 \ll k)$$
> 3. **Clear Bit $k$ (Turn Bit OFF)**:
>    $$\text{clearBit}(x, k) = x \;\&\; \sim(1 \ll k)$$
> 4. **Toggle Bit $k$ (Flip Bit)**:
>    $$\text{toggleBit}(x, k) = x \oplus (1 \ll k)$$
> 5. **Clear Lowest Set Bit (Brian Kernighan's Formula)**:
>    $$\text{clearLowestBit}(x) = x \;\&\; (x - 1)$$
> 6. **Isolate Lowest Set Bit (Fenwick Tree Formula)**:
>    $$\text{isolateLowestBit}(x) = x \;\&\; (-x)$$ ⚡

```
Bit Masking Operations Topology:

Target x:           00000000 00000000 00000000 00101100 (Decimal 44)
Mask (1 << 3):      00000000 00000000 00000000 00001000

Check Bit 3:        x & (1 << 3)  ──► 00001000 != 0 (Bit 3 IS SET!) ✅
Set Bit 0:          x | (1 << 0)  ──► 00101101 (Decimal 45)
Clear Bit 3:        x & ~(1 << 3) ──► 00100100 (Decimal 36)
Clear Lowest Bit:   x & (x - 1)   ──► 44 & 43 = 00101000 (Decimal 40)
Isolate Lowest Bit: x & (-x)      ──► 44 & -44 = 00000100 (Decimal 4) ⚡
```

---

## 2. Core Concepts & Bit Masking Strategy Matrix

### 2.1 Bit Masking Operations Strategy Matrix
```
Bit Masking Operations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Operation Goal        | Bitwise Formula   | Primary Mask Used | Hardware Speed    | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Check Bit $k$**     | `((x & (1<<k))!=0)`| `1 << k`          | **1 CPU Cycle ⚡** | Condition Testing |
| **Set Bit $k$**       | `x | (1 << k)`    | `1 << k`          | **1 CPU Cycle ⚡** | Flag Enable       |
| **Clear Bit $k$**     | `x & ~(1 << k)`   | `~(1 << k)`       | **1 CPU Cycle ⚡** | Flag Disable      |
| **Toggle Bit $k$**    | `x ^ (1 << k)`    | `1 << k`          | **1 CPU Cycle ⚡** | State Flipping    |
| **Clear Lowest Bit**  | `x & (x - 1)`     | `x - 1`           | **1 CPU Cycle ⚡** | **Bit Count / Power of 2⚡**|
| **Isolate Lowest Bit**| `x & (-x)`        | `-x`              | **1 CPU Cycle ⚡** | **Fenwick Tree ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Check = x & (1<<k); Set = x | (1<<k); Clear = x & ~(1<<k); Clear Lowest = x & (x-1); Isolate Lowest = x & (-x)!"**

---

## 3. Characteristics & Lowest Bit Formulas Mathematical Proof

### 3.1 Mathematical Derivation of $x \; \& \; (x - 1)$ and $x \; \& \; (-x)$
* **Part A: Brian Kernighan's Formula ($x \; \& \; (x - 1)$)**:
  - Let $x$ have its lowest set bit at position $p$:
    $$x = \dots 1 0 0 \dots 0_2$$
  - Subtracting $1$ from $x$ borrows from bit $p$, setting bit $p$ to $0$ and flipping all lower bits $0 \dots p-1$ to $1$:
    $$x - 1 = \dots 0 1 1 \dots 1_2$$
  - Bitwise ANDing $x \; \& \; (x - 1)$ zeroes out bit $p$ while leaving all higher bits unchanged:
    $$x \; \& \; (x - 1) = \dots 0 0 0 \dots 0_2$$
  - Exactly clears the rightmost 1-bit in a single instruction!

* **Part B: Lowest Set Bit Extractor ($x \; \& \; (-x)$)**:
  - In Two's Complement arithmetic, $-x = \sim x + 1$.
  - Inverting $\sim x$ flips bit $p$ to $0$ and lower bits $0 \dots p-1$ to $1$.
  - Adding $1$ carries up to bit $p$, restoring bit $p$ to $1$ and setting all lower bits to $0$:
    $$-x = \sim x + 1 = \dots 1 0 0 \dots 0_2$$
  - Bitwise ANDing $x \; \& \; (-x)$ keeps ONLY bit $p$, zeroing all higher and lower bits! ⚡

---

## 4. Internal Working Mechanics: Brian Kernighan's Bit Counting Engine

Tracing Brian Kernighan's $O(\text{Set Bits})$ Population Count for $x = 44$ (`00101100_2`):

```
Goal: Count total number of 1-bits in x = 44.

Initial: x = 44 (00101100_2), count = 0

Iteration 1:
- Clear lowest set bit: x = x & (x - 1) = 44 & 43 = 40 (00101000_2).
- count = 1.

Iteration 2:
- Clear lowest set bit: x = x & (x - 1) = 40 & 39 = 32 (00100000_2).
- count = 2.

Iteration 3:
- Clear lowest set bit: x = x & (x - 1) = 32 & 31 = 0 (00000000_2).
- count = 3. Loop terminates (x == 0)!

Total Set Bits = 3! Runs in O(Set Bits) instead of O(32) iterations! ✅ ⚡
```

---

## 5. Visual Diagram: Isolate Lowest Bit ($x \; \& \; (-x)$)

```
Bit Extractor Topology (x = 44):

x        : 00000000 00000000 00000000 00101100 (Decimal 44)
~x       : 11111111 11111111 11111111 11010011
-x (~x+1): 11111111 11111111 11111111 11010100 (Decimal -44)
──────────────────────────────────────────────────────────
x & (-x) : 00000000 00000000 00000000 00000100 (Decimal 4!)

Isolates single rightmost 1-bit in O(1) CPU Cycle! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing all 6 Bit Masking Formulas, Brian Kernighan's Population Count (LeetCode 191), and Fenwick Tree Lowest Bit Extractor.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bit Masking Formulas:
 * Checking, Setting, Clearing, Toggling, Brian Kernighan's Algorithm, and Fenwick Bit Extraction.
 */
public class BitMasksMaster {

    // =========================================================================
    // 1. THE 6 MASTER BIT MASKING FORMULAS
    // =========================================================================
    public boolean checkBit(int x, int k)  { return ((x & (1 << k)) != 0); }
    public int setBit(int x, int k)        { return x | (1 << k); }
    public int clearBit(int x, int k)      { return x & ~(1 << k); }
    public int toggleBit(int x, int k)     { return x ^ (1 << k); }

    public int clearLowestSetBit(int x)    { return x & (x - 1); } // Brian Kernighan ⚡
    public int isolateLowestSetBit(int x)  { return x & (-x); }   // Fenwick Extractor ⚡

    // =========================================================================
    // 2. BRIAN KERNIGHAN'S POPULATION COUNT (LEETCODE 191 O(SetBits) Time)
    // =========================================================================
    /**
     * Counts number of set bits (1s) in a 32-bit integer in O(Set Bits) time.
     */
    public int countSetBitsBrianKernighan(int n) {
        int count = 0;
        while (n != 0) {
            n = n & (n - 1); // Clears lowest set bit in 1 CPU cycle! ⚡
            count++;
        }
        return count;
    }

    // =========================================================================
    // 3. RANGE BIT MASK CREATOR
    // =========================================================================
    /**
     * Creates a bit mask with 1s in bit range [left ... right] inclusive.
     */
    public int createRangeMask(int left, int right) {
        if (left < 0 || right > 31 || left > right) return 0;
        int fullMask = -1; // 0xFFFFFFFF (All 1s)
        int highMask = fullMask << (right + 1);
        int lowMask = (1 << left) - 1;
        return ~(highMask | lowMask); // 1s ONLY in range [left..right] ⚡
    }
}
```

> **Quick Syntax:**
```java
// Master Bit Masking Lines
int clearLowest = x & (x - 1); int isolateLowest = x & (-x); boolean isSet = ((x & (1 << k)) != 0);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 191 - Number of 1 Bits**:
   - Population count solved in $O(\text{Set Bits})$ time using `x & (x - 1)`.

2. **Fenwick Tree (Binary Indexed Tree)**:
   - Index update step uses `idx += idx & (-idx)` to advance to parent node.

3. **Bitmask Dynamic Programming (Held-Karp TSP)**:
   - Tracking visited cities set using integer bitmask states.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class BitMasksDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BIT MASKS BENCHMARK DEMO                      ");
        System.out.println("=================================================\n");

        BitMasksMaster master = new BitMasksMaster();

        int x = 44; // Binary: 00101100
        int k = 3;

        System.out.println("1. Bit Mask Operations on Input x = 44 (00101100_2):");
        System.out.println("   Check Bit 3 Is Set      : " + master.checkBit(x, k));
        System.out.println("   Set Bit 0 (44 | 1)      : " + master.setBit(x, 0) + " (00101101_2)");
        System.out.println("   Clear Bit 3 (44 & ~8)   : " + master.clearBit(x, k) + " (00100100_2)");
        System.out.println("   Toggle Bit 3 (44 ^ 8)   : " + master.toggleBit(x, k) + " (00100100_2)");
        System.out.println("-------------------------------------------------");

        // 2. Lowest Bit Formulas
        System.out.println("2. Lowest Bit Formulas for x = 44:");
        System.out.println("   Clear Lowest Set Bit x & (x - 1): " + master.clearLowestSetBit(x) + " (00101000_2 = 40)");
        System.out.println("   Isolate Lowest Set Bit x & (-x)  : " + master.isolateLowestSetBit(x) + " (00000100_2 = 4)");
        System.out.println("-------------------------------------------------");

        // 3. Brian Kernighan Bit Count
        System.out.println("3. Brian Kernighan Set Bit Count for 44:");
        System.out.println("   Total Set Bits: " + master.countSetBitsBrianKernighan(x) + " Bits (Optimal = 3)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bit Masking Operation | Formula | Time Complexity | Key Application |
| :--- | :--- | :--- | :--- |
| **Check Bit $k$** | `((x & (1 << k)) != 0)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| Bit condition test |
| **Clear Lowest Bit** | `x & (x - 1)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| Brian Kernighan bit count |
| **Isolate Lowest Bit**| `x & (-x)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| **Fenwick Tree index update⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **Input $x = 0$**:
   - `x & (x - 1)` returns 0; `x & (-x)` returns 0.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Shifting by $\ge 32$ Bits on 32-bit `int` Types**:
  - In Java, `1 << 32` evaluates to `1 << 0 = 1` because shift amounts are masked modulo 32 (`shift & 31`). **ALWAYS use `1L << k` for 64-bit `long` masking!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Long Bit Mask Rule:
> When creating bit masks for positions $k \ge 32$, **ALWAYS use `1L << k` with `long` primitive type**, otherwise `1 << 32` wraps around to `1 << 0`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard Loop Bit Inspection | Brian Kernighan (`x & (x-1)`) |
| :--- | :--- | :--- |
| **Iterations** | Always 32 Iterations | **Only Set Bits Count ⚡** |
| **Performance** | Constant $O(32)$ | **Up to 32x Faster ⚡** |
| **Code Size** | 4 Lines | **2 Lines ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count total set bits in integer in fast time"** $\rightarrow$ Brian Kernighan `x & (x - 1)`.
* **"Isolate single lowest set 1-bit"** $\rightarrow$ `x & (-x)`.

---

## 15. Frequently Asked Interview Questions

* **Q: How does `x & (x - 1)` clear the lowest set bit?**  
  *A:* Subtracting 1 flips the rightmost 1-bit to 0 and all trailing 0s to 1s. Bitwise ANDing $x \& (x-1)$ zeroes out the rightmost 1-bit while leaving higher bits intact.

* **Q: How does `x & (-x)` isolate the lowest set bit?**  
  *A:* In Two's Complement, $-x = \sim x + 1$. Adding 1 carries up to the rightmost 1-bit, so $x \& (-x)$ zeroes all higher and lower bits, leaving only the rightmost 1-bit.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BIT MASKS                                             |
+-----------------------------------------------------------------------+
| • Check Bit k : ((x & (1 << k)) != 0)                                 |
| • Set Bit k   : x | (1 << k)                                          |
| • Clear Bit k : x & ~(1 << k)                                         |
| • Toggle Bit k: x ^ (1 << k)                                          |
| • Clear Lowest Bit  : x & (x - 1)  (Brian Kernighan O(SetBits))       |
| • Isolate Lowest Bit: x & (-x)     (Fenwick Tree Index Extractor)     |
| • Rule        : Use 1L << k for k >= 32 with long types! ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write all 6 master bit masking formulas in Java.
- [ ] I can write Brian Kernighan's set bit counter in Java.
- [ ] I can explain why `x & (-x)` isolates the lowest 1-bit.
- [ ] I can state why `1L << k` is required for $k \ge 32$.
- [ ] I can write a range bit mask creator in Java.
