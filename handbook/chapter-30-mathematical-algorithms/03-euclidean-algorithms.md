# 03. Euclidean Algorithms: Standard GCD, Extended Euclidean & Linear Diophantine Solvers

## 1. Introduction
The **Euclidean Algorithm** is one of the oldest known mathematical algorithms in recorded human history, dating back to Euclid's *Elements* (c. 300 BC). It computes the **Greatest Common Divisor ($\gcd(a, b)$)** of two positive integers in **$O(\log(\min(a, b)))$ Logarithmic Time** by repeatedly applying the modulo reduction identity $\gcd(a, b) = \gcd(b, a \bmod b)$. Building upon this foundation, the **Extended Euclidean Algorithm** calculates integer Bezout coefficients $x$ and $y$ that satisfy **Bezout's Identity ($a \cdot x + b \cdot y = \gcd(a, b)$)**. The Extended Euclidean algorithm is the essential engine for computing modular multiplicative inverses and solving **Linear Diophantine Equations ($a \cdot x + b \cdot y = c$)**.

> **Important:** Core Structural Formulas of Euclidean Algorithms:
> 1. **Standard Euclidean GCD Formula**:
>    $$\gcd(a, b) = \begin{cases} a & \text{if } b = 0 \\ \gcd(b, a \pmod b) & \text{if } b > 0 \end{cases}$$
> 2. **Least Common Multiple (LCM) Formula**:
>    $$\text{lcm}(a, b) = \frac{a}{\gcd(a, b)} \times b \quad (\text{Divide FIRST to prevent integer overflow!})$$
> 3. **Bezout's Identity & Extended Euclidean Recurrence**:
>    $$a \cdot x + b \cdot y = \gcd(a, b)$$
>    - Given recursive child solution $(x_1, y_1)$ for $(b, a \bmod b)$:
>      $$x = y_1 \quad \text{and} \quad y = x_1 - \left\lfloor \frac{a}{b} \right\rfloor \times y_1$$
> 4. **Linear Diophantine Solvability Condition**:
>    - The equation $a \cdot x + b \cdot y = c$ has integer solutions $(x, y)$ if and ONLY if $\gcd(a, b)$ divides $c$ ($\gcd(a, b) \mid c$). ⚡

```
Extended Euclidean State Recurrence Topology:

Goal: Solve a * x + b * y = gcd(a, b) for a = 35, b = 15.

Step 1: gcd(35, 15) -> 35 = 2 * 15 + 5
Step 2: gcd(15, 5)  -> 15 = 3 * 5 + 0
Step 3: Base Case b = 0 -> gcd = 5, x = 1, y = 0.

Unwinding State Transitions (x = y1, y = x1 - (a/b)*y1):
- Child (5, 0):  x = 1, y = 0
- Step 2 (15, 5): x = 0, y = 1 - (15/5)*0 = 1 ──► 15*(0) + 5*(1) = 5!
- Step 1 (35, 15): x = 1, y = 0 - (35/15)*1 = -2 ──► 35*(1) + 15*(-2) = 35 - 30 = 5! ✅

Bezout Coefficients: x = 1, y = -2! ⚡
```

---

## 2. Core Concepts & Euclidean Algorithms Strategy Matrix

### 2.1 Euclidean Algorithms Family Strategy Matrix
```
Euclidean Algorithms Family Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm Name        | Target Problem    | Time Complexity   | Auxiliary Space   | Key Identity      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Standard GCD**      | $\gcd(a, b)$      | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Iterative ⚡**| $\gcd(a,b)=\gcd(b, a\%b)$|
| **Safe LCM**          | $\text{lcm}(a, b)$| **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**| $(a / \gcd(a,b)) \times b$|
| **Extended Euclidean**| $ax + by = \gcd$  | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Iterative ⚡**| $x = y_1, y = x_1 - \lfloor a/b \rfloor y_1$|
| **Diophantine Solver**| $ax + by = c$     | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**| $\gcd(a,b) \mid c$ check |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Standard GCD: gcd(a, b) = b == 0 ? a : gcd(b, a % b); Extended Euclidean solves ax + by = gcd(a, b); Divide FIRST in LCM to avoid overflow!"**

---

## 3. Characteristics & Gabriel Lamé's Complexity Proof

### 3.1 Mathematical Proof of Euclidean Algorithm Logarithmic Bound ($O(\log(\min(a, b)))$)
* **Lamé's Theorem (1844)**:
  - The number of division steps required by the Euclidean algorithm to compute $\gcd(a, b)$ (for $a > b > 0$) is at most 5 times the number of decimal digits of $b$:
    $$\text{Steps} \le 5 \times \log_{10}(b) = O(\log b)$$
* **Worst-Case Input Pair (Consecutive Fibonacci Numbers)**:
  - Let $F_k$ be the $k$-th Fibonacci number ($F_0=0, F_1=1, F_2=1, F_3=2, F_4=3, F_5=5 \dots$).
  - Modulo property of Fibonacci numbers:
    $$F_{k} \pmod{F_{k-1}} = F_{k-2}$$
  - Computing $\gcd(F_k, F_{k-1})$ requires $k - 1$ steps, which is the absolute maximum number of steps for any inputs $\le F_k$.
  - Since $F_k \approx \frac{\phi^k}{\sqrt{5}}$ (where $\phi = \frac{1 + \sqrt{5}}{2} \approx 1.618$), $k = O(\log_\phi N)$.
* Therefore, Euclidean GCD runs in **Strict Logarithmic Time $O(\log(\min(a, b)))$**! ⚡

---

## 4. Internal Working Mechanics: Linear Diophantine Equation Solver

Tracing Linear Diophantine Equation $6x + 15y = 9$:

```
Goal: Find integer solution (x, y) for 6x + 15y = 9.

Step 1: Compute g = gcd(6, 15) = 3.
Step 2: Check Solvability Condition:
        Does 3 divide 9 (c % g == 0)?
        9 % 3 == 0 (YES! Solution Exists!) ✅

Step 3: Solve base Extended Euclidean for 6x_0 + 15y_0 = 3:
        Extended Euclidean yields x_0 = -2, y_0 = 1. (6*(-2) + 15*(1) = -12 + 15 = 3).

Step 4: Scale coefficients by (c / g) = (9 / 3) = 3:
        x_particular = x_0 * (c / g) = -2 * 3 = -6.
        y_particular = y_0 * (c / g) = 1 * 3 = 3.

Verification: 6*(-6) + 15*(3) = -36 + 45 = 9! ✅ ⚡
```

---

## 5. Visual Diagram: Extended Euclidean Back-Substitution

```
Extended Euclidean State Flowchart:

Forward Pass (Modulo Divisions):
gcd(35, 15) ──► 35 = 2 * 15 + 5
               gcd(15, 5) ──► 15 = 3 * 5 + 0
                              gcd(5, 0) ──► Base Case: g = 5, x = 1, y = 0

Backward Pass (Coefficient Updates):
                              x = 1, y = 0
               x = 0, y = 1 - (15/5)*0 = 1
x = 1, y = 0 - (35/15)*1 = -2 ──► Final Bezout Coefficients: x = 1, y = -2! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Standard Euclidean GCD, Safe LCM, Extended Euclidean Algorithm, and Linear Diophantine Equation Solver.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Euclidean Algorithms:
 * Standard Iterative & Recursive GCD, Safe LCM, Extended Euclidean, and Linear Diophantine Solvers.
 */
public class EuclideanAlgorithmsMaster {

    // =========================================================================
    // 1. STANDARD EUCLIDEAN GCD (O(log(min(a, b))) Time, O(1) Space)
    // =========================================================================
    /**
     * Computes Greatest Common Divisor recursively.
     */
    public long gcd(long a, long b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b); // Modulo identity ⚡
    }

    /**
     * Computes Greatest Common Divisor iteratively (Zero Call Stack Overhead).
     */
    public long gcdIterative(long a, long b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // =========================================================================
    // 2. SAFE LEAST COMMON MULTIPLE (LCM) (O(log(min(a, b))) Time)
    // =========================================================================
    /**
     * Computes LCM safely by dividing FIRST to prevent long overflow.
     */
    public long lcm(long a, long b) {
        if (a == 0 || b == 0) return 0;
        long g = gcd(a, b);
        return Math.abs(a / g) * Math.abs(b); // Divide FIRST! ⚡
    }

    // =========================================================================
    // 3. EXTENDED EUCLIDEAN ALGORITHM (ax + by = gcd(a, b))
    // =========================================================================
    public static class ExtendedGCDResult {
        public final long gcd;
        public final long x;
        public final long y;

        public ExtendedGCDResult(long gcd, long x, long y) {
            this.gcd = gcd;
            this.x = x;
            this.y = y;
        }
    }

    /**
     * Solves ax + by = gcd(a, b) returning Bezout coefficients x and y.
     */
    public ExtendedGCDResult extendedGCD(long a, long b) {
        if (b == 0) {
            return new ExtendedGCDResult(a, 1, 0); // Base Case: x = 1, y = 0 ⚡
        }

        ExtendedGCDResult child = extendedGCD(b, a % b);
        long x = child.y;
        long y = child.x - (a / b) * child.y; // Recurrence transition ⚡

        return new ExtendedGCDResult(child.gcd, x, y);
    }

    // =========================================================================
    // 4. LINEAR DIOPHANTINE EQUATION SOLVER (ax + by = c)
    // =========================================================================
    public static class DiophantineResult {
        public final boolean isSolvable;
        public final long x;
        public final long y;
        public final long gcd;

        public DiophantineResult(boolean isSolvable, long x, long y, long gcd) {
            this.isSolvable = isSolvable;
            this.x = x;
            this.y = y;
            this.gcd = gcd;
        }
    }

    /**
     * Solves ax + by = c. Returns particular solution (x, y) if solvable.
     */
    public DiophantineResult solveDiophantine(long a, long b, long c) {
        ExtendedGCDResult ext = extendedGCD(a, b);
        long g = ext.gcd;

        // Solvability Condition: gcd(a, b) MUST divide c! ⚡
        if (c % g != 0) {
            return new DiophantineResult(false, 0, 0, g); // No integer solution!
        }

        long scale = c / g;
        long x = ext.x * scale;
        long y = ext.y * scale;

        return new DiophantineResult(true, x, y, g);
    }
}
```

> **Quick Syntax:**
```java
// Euclidean Core Lines
long g = gcd(a, b); long l = (a / g) * b; // Divide FIRST in LCM!
long x = child.y, y = child.x - (a / b) * child.y; // Extended GCD Recurrence
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1979 - Find Greatest Common Divisor of Array**:
   - Array GCD computation benchmark ($O(\log(\min(a, b)))$ time).

2. **Modular Multiplicative Inverse Computation**:
   - Solving $a \cdot x \equiv 1 \pmod M$ via Extended GCD $a \cdot x + M \cdot y = 1$.

3. **Water Jug Problem / Die Hard Jug Riddle**:
   - Measuring $C$ gallons using jugs of capacity $A$ and $B$ (Solvable iff $\gcd(A, B) \mid C$).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class EuclideanAlgorithmsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   EUCLIDEAN ALGORITHMS BENCHMARK DEMO           ");
        System.out.println("=================================================\n");

        EuclideanAlgorithmsMaster master = new EuclideanAlgorithmsMaster();

        // 1. Standard GCD & Safe LCM Test
        long a = 35, b = 15;
        System.out.println("1. Standard GCD & Safe LCM for a = 35, b = 15:");
        System.out.println("   gcd(35, 15) : " + master.gcd(a, b) + " (Optimal = 5)");
        System.out.println("   lcm(35, 15) : " + master.lcm(a, b) + " (Optimal = 105)");
        System.out.println("-------------------------------------------------");

        // 2. Extended Euclidean Test (35x + 15y = 5)
        EuclideanAlgorithmsMaster.ExtendedGCDResult ext = master.extendedGCD(a, b);
        System.out.println("2. Extended Euclidean Result for 35x + 15y = gcd(35,15):");
        System.out.println("   gcd = " + ext.gcd + ", Bezout x = " + ext.x + ", Bezout y = " + ext.y);
        System.out.println("   Verification (35*x + 15*y): " + (a * ext.x + b * ext.y));
        System.out.println("-------------------------------------------------");

        // 3. Linear Diophantine Solver Test (6x + 15y = 9)
        EuclideanAlgorithmsMaster.DiophantineResult dio = master.solveDiophantine(6, 15, 9);
        System.out.println("3. Linear Diophantine Solver for 6x + 15y = 9:");
        System.out.println("   Is Solvable : " + dio.isSolvable);
        System.out.println("   Particular x: " + dio.x + ", Particular y: " + dio.y);
        System.out.println("   Verification (6*x + 15*y): " + (6 * dio.x + 15 * dio.y));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Euclidean Task | Algorithm Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Standard GCD** | Euclidean Modulo | $\mathbf{O(\log(\min(a, b)))}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Worst case Fibonacci |
| **Safe LCM** | GCD Division First | $\mathbf{O(\log(\min(a, b)))}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| $(a / \gcd) \times b$ |
| **Extended GCD** | Recurrence Backtrack| $\mathbf{O(\log(\min(a, b)))}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Bezout $ax + by = \gcd$ |
| **Diophantine Solver**| Extended GCD Scale| $\mathbf{O(\log(\min(a, b)))}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Solvability $\gcd \mid c$ |

---

## 10. Edge Cases & Boundary Handling

1. **Input $a = 0$ or $b = 0$**:
   - $\gcd(a, 0) = |a|$, $\text{lcm}(a, 0) = 0$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Multiplying Before Dividing in LCM (`(a * b) / gcd`)**:
  - For $a, b \approx 10^10$, $a \times b = 10^{20}$, which overflows 64-bit `long` limits ($2^{63}-1 \approx 9.22 \times 10^{18}$). **ALWAYS divide first: `(a / gcd) * b`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Safe LCM & Solvability Rules:
> * **Safe LCM**: $\text{lcm}(a, b) = (a / \gcd(a, b)) \times b$ (Divide FIRST!).
> * **Diophantine Solvability**: $a \cdot x + b \cdot y = c$ is solvable iff $\gcd(a, b) \mid c$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Subtraction-Based GCD | Euclidean Modulo GCD |
| :--- | :--- | :--- |
| **Time Complexity** | $O(\max(a, b))$ Linear (Slow!) | **$O(\log(\min(a, b)))$ Logarithmic ⚡** |
| **Worst-Case Input**| $a = 10^9, b = 1$ (1 Billion Steps) | **Fibonacci Numbers (~30 Steps) ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find greatest common divisor or least common multiple"** $\rightarrow$ Euclidean GCD & Safe LCM.
* **"Solve ax + by = c for integer values x and y"** $\rightarrow$ Extended Euclidean & Diophantine Solver.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Euclidean GCD time complexity $O(\log(\min(a, b)))$?**  
  *A:* Because at each step, $a \bmod b < \frac{a}{2}$. Thus, the numbers decrease by at least half every 2 steps, yielding logarithmic time bounds.

* **Q: What is the worst-case input pair for the Euclidean algorithm?**  
  *A:* Two consecutive Fibonacci numbers ($F_k, F_{k-1}$), because $F_k \bmod F_{k-1} = F_{k-2}$, requiring the maximum possible number of modulo steps for their magnitude.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: EUCLIDEAN ALGORITHMS                                  |
+-----------------------------------------------------------------------+
| • Standard GCD: gcd(a, b) = b == 0 ? a : gcd(b, a % b) -> O(log min)  |
| • Safe LCM    : lcm(a, b) = (a / gcd(a, b)) * b (Divide FIRST!)       |
| • Extended GCD: x = child.y, y = child.x - (a / b) * child.y          |
| • Diophantine : ax + by = c is solvable IF AND ONLY IF gcd(a,b) | c   |
| • Worst Case  : Consecutive Fibonacci numbers F_k, F_{k-1}! ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write recursive and iterative Euclidean GCD in Java.
- [ ] I can write Safe LCM in Java with divide-first protection.
- [ ] I can write the Extended Euclidean algorithm in Java.
- [ ] I can write a Linear Diophantine Equation solver in Java.
- [ ] I can explain why Euclidean GCD runs in $O(\log(\min(a, b)))$ time.
