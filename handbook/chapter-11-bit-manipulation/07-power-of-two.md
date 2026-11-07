# 07. Power of Two, Three & Four: Bitwise Verification & Constant Modulo Invariants

## 1. Introduction
Verifying whether an integer $N$ is a **Power of Two ($2^k$)**, **Power of Three ($3^k$)**, or **Power of Four ($4^k$)** is a fundamental mathematical benchmark in algorithmic problem solving. While naive implementations use logarithmic loops (`while (n % K == 0) n /= K;`), bitwise and number-theoretic properties allow all three power verification problems to be solved in **$O(1)$ Strict Constant Time** without any loops, floating-point functions, or recursion. Specifically:
1. **Power of Two (LeetCode 231)**: Exploits single-bit binary structure using `(n > 0) && ((n & (n - 1)) == 0)`.
2. **Power of Three (LeetCode 326)**: Exploits prime divisibility against the maximum 32-bit signed integer power of three ($3^{19} = 1,162,261,467$) using `(n > 0) && (1162261467 % n == 0)`.
3. **Power of Four (LeetCode 342)**: Combines Power of Two check with odd-position bitmask `0x55555555` using `(n > 0) && ((n & (n - 1)) == 0) && ((n & 0x55555555) != 0)`.

> **Important:** The 3 Constant Time Power Verification Formulas:
> 1. **Power of Two (LeetCode 231)**:
>    $$\text{isPowerOfTwo}(n) = (n > 0) \;\&\&\; ((n \;\&\; (n - 1)) == 0)$$
> 2. **Power of Three (LeetCode 326)**:
>    $$\text{isPowerOfThree}(n) = (n > 0) \;\&\&\; (1162261467 \pmod{n} == 0)$$
> 3. **Power of Four (LeetCode 342)**:
>    $$\text{isPowerOfFour}(n) = (n > 0) \;\&\&\; ((n \;\&\; (n - 1)) == 0) \;\&\&\; ((n \;\&\; \text{0x55555555}) \neq 0)$$
> 4. **Power of Four Modulo Alternative**:
>    - Any power of 4 minus 1 is divisible by 3: $(4^k - 1) \equiv 0 \pmod 3$.
>    - Formula: `(n > 0) && ((n & (n - 1)) == 0) && (n % 3 == 1)`! ⚡

```
Power of Two, Three & Four Classification Topology:

Input Number N (Positive N > 0):
├── Power of 2 (231) ──► Single Set Bit: (N & (N - 1)) == 0 ⚡
├── Power of 3 (326) ──► Prime Divisor of 3^19: (1162261467 % N) == 0 ⚡
└── Power of Four (342)
    ├── Must be Power of 2: (N & (N - 1)) == 0
    └── Single Set Bit must be at ODD position (Bit 0, 2, 4, 6...):
        Mask 0x55555555 = 01010101 01010101 01010101 01010101 ⚡
```

---

## 2. Core Concepts & Power Verification Strategy Matrix

### 2.1 Power Verification Strategy Matrix
```
Power Verification Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Target Power          | Bitwise / Math    | Time Complexity   | Auxiliary Space   | Key Mathematical Fact|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Power of Two (231)**| `(n & (n-1)) == 0`| **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**| Exactly 1 set bit |
| **Power of Three (326)**| `1162261467 % n == 0`| **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**| $3^{19} = 1,162,261,467$|
| **Power of Four (342)**| `n & 0x55555555`  | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**| Set bit at odd pos|
| **Power of Four Alt** | `n % 3 == 1`      | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**| $(4^k - 1) \equiv 0 \pmod 3$|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Power of 2 = n & (n-1)==0; Power of 3 = 1162261467 % n == 0; Power of 4 = Power of 2 + (n & 0x55555555) != 0!"**

---

## 3. Characteristics & Power of Four Mathematical Proof

### 3.1 Mathematical Proof of Power of Four `(n & 0x55555555) != 0`
* **Part A: Power of Four Binary Pattern**:
  - Powers of 4 in binary:
    - $4^0 = 1 = 00000001_2$ (Bit 0 set)
    - $4^1 = 4 = 00000100_2$ (Bit 2 set)
    - $4^2 = 16 = 00010000_2$ (Bit 4 set)
    - $4^3 = 64 = 01000000_2$ (Bit 6 set)
  - Every power of 4 is a power of 2 (has exactly 1 set bit), and its single set bit occurs ONLY at an **even 0-indexed position (bit 0, 2, 4, 6, 8, 10, 12 ... 30)**.
* **Part B: Odd Position Mask `0x55555555`**:
  - In hex, `0x5 = 0101_2`.
  - The 32-bit mask `0x55555555` has 1s placed at all even 0-indexed bit positions:
    $$\text{0x55555555} = 01010101 \; 01010101 \; 01010101 \; 01010101_2$$
* **Proof**:
  - Powers of 2 that are NOT powers of 4 (e.g. $2, 8, 32$) have their single set bit at an odd position (bit 1, 3, 5).
  - Bitwise ANDing $N \& \text{0x55555555}$ yields non-zero if and only if the single set bit of $N$ is located at an even position.
  - Thus, $(N > 0) \;\&\&\; ((N \& (N - 1)) == 0) \;\&\&\; ((N \& \text{0x55555555}) \neq 0)$ uniquely identifies Powers of Four in $O(1)$ time! ⚡

---

## 4. Internal Working Mechanics: Power of Three Max Integer Proof

Tracing Power of Three (LeetCode 326):

```
Max 32-bit Signed Integer = Integer.MAX_VALUE = 2,147,483,647.

Powers of 3 Sequence:
3^0  = 1
3^1  = 3
3^2  = 9
...
3^19 = 1,162,261,467 (Largest power of 3 <= 2,147,483,647!)
3^20 = 3,486,784,401 (Exceeds Integer.MAX_VALUE!).

Since 3 is a prime number, the ONLY positive divisors of 3^19 are powers of 3!
Therefore: N is a power of 3 <==> N > 0 AND (1162261467 % N == 0)! ✅ ⚡
```

---

## 5. Visual Diagram: Power of Four Bitmask Masking

```
Power of Four Bitmask Masking Topology:

N = 16 (4^2):       00000000 00000000 00000000 00010000 (Bit 4 set!)
Mask 0x55555555:   01010101 01010101 01010101 01010101

N & 0x55555555  ──► 00000000 00000000 00000000 00010000 != 0 (POWER OF 4!) ✅

N = 8 (2^3):        00000000 00000000 00000000 00001000 (Bit 3 set!)
N & 0x55555555  ──► 00000000 00000000 00000000 00000000 == 0 (NOT POWER OF 4!) ❌ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Power of Two (LeetCode 231), Power of Three (LeetCode 326), Power of Four Bitmask & Modulo 3 (LeetCode 342).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Constant-Time Power Verifiers:
 * LeetCode 231 (Power of 2), LeetCode 326 (Power of 3), and LeetCode 342 (Power of 4).
 */
public class PowerOfTwoMaster {

    // =========================================================================
    // 1. LEETCODE 231: POWER OF TWO (O(1) Time, O(1) Space)
    // =========================================================================
    /**
     * Checks if integer N is a power of two.
     */
    public boolean isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0; // Single set bit ⚡
    }

    // =========================================================================
    // 2. LEETCODE 326: POWER OF THREE (O(1) Time, O(1) Space)
    // =========================================================================
    /**
     * Checks if integer N is a power of three without loops or recursion.
     */
    public boolean isPowerOfThree(int n) {
        // 3^19 = 1,162,261,467 (Max 32-bit signed int power of 3)
        return n > 0 && (1162261467 % n == 0); // Divisibility test ⚡
    }

    // =========================================================================
    // 3. LEETCODE 342: POWER OF FOUR (BITMASK METHOD O(1) Time)
    // =========================================================================
    /**
     * Checks if integer N is a power of four using Bitmask 0x55555555.
     */
    public boolean isPowerOfFourBitmask(int n) {
        return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0; // Odd bit ⚡
    }

    // =========================================================================
    // 4. LEETCODE 342: POWER OF FOUR (MODULO 3 ALTERNATIVE O(1) Time)
    // =========================================================================
    /**
     * Checks if integer N is a power of four using Modulo 3 property.
     */
    public boolean isPowerOfFourModulo(int n) {
        return n > 0 && (n & (n - 1)) == 0 && (n % 3 == 1); // (4^k - 1) % 3 == 0 ⚡
    }
}
```

> **Quick Syntax:**
```java
// Power Verifiers O(1) Lines
boolean isPow2 = (n > 0 && (n & (n - 1)) == 0);
boolean isPow3 = (n > 0 && 1162261467 % n == 0);
boolean isPow4 = (n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 231 - Power of Two**:
   - Single set bit test ($O(1)$ time).

2. **LeetCode 326 - Power of Three**:
   - Prime divisor test against $3^{19} = 1,162,261,467$ ($O(1)$ time).

3. **LeetCode 342 - Power of Four**:
   - Bitmask odd-position test using `0x55555555` ($O(1)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class PowerOfTwoDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   POWER OF 2, 3, 4 VERIFICATION DEMO            ");
        System.out.println("=================================================\n");

        PowerOfTwoMaster master = new PowerOfTwoMaster();

        // 1. Power of Two Test
        int p2_a = 16, p2_b = 18;
        System.out.println("1. Power of Two Test (LeetCode 231):");
        System.out.println("   Is 16 Power of Two: " + master.isPowerOfTwo(p2_a) + " (Optimal = true)");
        System.out.println("   Is 18 Power of Two: " + master.isPowerOfTwo(p2_b) + " (Optimal = false)");
        System.out.println("-------------------------------------------------");

        // 2. Power of Three Test
        int p3_a = 27, p3_b = 45;
        System.out.println("2. Power of Three Test (LeetCode 326):");
        System.out.println("   Is 27 Power of Three: " + master.isPowerOfThree(p3_a) + " (Optimal = true)");
        System.out.println("   Is 45 Power of Three: " + master.isPowerOfThree(p3_b) + " (Optimal = false)");
        System.out.println("-------------------------------------------------");

        // 3. Power of Four Test
        int p4_a = 16, p4_b = 8;
        System.out.println("3. Power of Four Test (LeetCode 342):");
        System.out.println("   Is 16 Power of Four: " + master.isPowerOfFourBitmask(p4_a) + " (Optimal = true)");
        System.out.println("   Is 8 Power of Four : " + master.isPowerOfFourBitmask(p4_b) + " (Optimal = false)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Power Problem | Formula | Time Complexity | Auxiliary Space | Key Constant / Mask |
| :--- | :--- | :--- | :--- | :--- |
| **Power of Two (231)**| `(n > 0) && ((n & (n-1)) == 0)`| $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| `(n - 1)` |
| **Power of Three (326)**| `(n > 0) && (1162261467 % n == 0)`| $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| $3^{19} = 1,162,261,467$ |
| **Power of Four (342)**| `(n > 0) && isPow2 && (n & 0x55555555) != 0`| $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| Mask `0x55555555` |

---

## 10. Edge Cases & Boundary Handling

1. **Negative Numbers or Zero ($N \le 0$)**:
   - All verifiers enforce `n > 0` as the first short-circuit check.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using Logarithmic Loops (`while (n % 3 == 0) n /= 3;`)**:
  - Running a while loop executes multiple division CPU instructions. **ALWAYS use constant time $O(1)$ formulas `1162261467 % n == 0` for LeetCode 326!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 3 Power Formulas:
> * **Power of 2**: `(n > 0) && ((n & (n - 1)) == 0)`
> * **Power of 3**: `(n > 0) && (1162261467 % n == 0)`
> * **Power of 4**: `(n > 0) && ((n & (n - 1)) == 0) && ((n & 0x55555555) != 0)` ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Loop Method (`while`) | Constant-Time Bitwise / Math |
| :--- | :--- | :--- |
| **Execution Speed** | Variable $O(\log_K N)$ Loops | **$O(1)$ Single CPU Instruction ⚡** |
| **Branching** | Loop Condition Branches | **No Loops ⚡** |
| **Memory Footprint**| $O(1)$ | **$O(1)$ ⚡** |

---

## 14. How to Recognize This in Questions

* **"Check if number is power of 2, 3, or 4 without loops or recursion"** $\rightarrow$ LeetCode 231 / 326 / 342.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does `1162261467 % n == 0` check if $n$ is a power of 3?**  
  *A:* Because $1,162,261,467 = 3^{19}$ is the largest power of 3 fitting in a 32-bit signed integer. Since 3 is prime, the only positive integer divisors of $3^{19}$ are powers of 3 ($3^0, 3^1 \dots 3^{19}$).

* **Q: Why is `0x55555555` used for Power of Four?**  
  *A:* Because `0x55555555` has 1-bits placed at all even bit positions (bit 0, 2, 4, 6 ... 30), which are the exact bit positions occupied by powers of 4.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: POWER OF 2, 3, 4                                      |
+-----------------------------------------------------------------------+
| • Power of 2 (231): (n > 0) && ((n & (n - 1)) == 0)                   |
| • Power of 3 (326): (n > 0) && (1162261467 % n == 0)                  |
| • Power of 4 (342): (n > 0) && isPow2 && ((n & 0x55555555) != 0)      |
| • Power of 4 Alt  : (n > 0) && isPow2 && (n % 3 == 1)                 |
| • Performance     : All 3 problems solved in O(1) Constant Time! ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 231 (`Power of Two`) in Java.
- [ ] I can write LeetCode 326 (`Power of Three`) in Java without loops.
- [ ] I can write LeetCode 342 (`Power of Four`) using Bitmask `0x55555555`.
- [ ] I can explain why $3^{19} = 1,162,261,467$ works for Power of Three.
- [ ] I can explain why powers of 4 have single set bits at even positions.
