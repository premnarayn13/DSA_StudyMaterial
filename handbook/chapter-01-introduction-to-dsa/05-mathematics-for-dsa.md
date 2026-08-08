# 05. Mathematics for DSA

## 1. Introduction
Mathematical foundations underpin algorithmic efficiency, indexing, hashing, bitwise operations, and combinatorial bounds. In technical interviews, strong mathematical intuition allows you to derive $O(1)$ closed-form solutions instead of relying on brute-force $O(n)$ loops.

> **Important:** Key mathematical topics in DSA interviews include modular arithmetic, GCD/LCM, prime operations, logarithms, power formulas, and basic combinatorics.

## 2. Core Concepts
* **Modular Arithmetic**: Computation on remainder values where $(a + b) \pmod M = ((a \pmod M) + (b \pmod M)) \pmod M$.
* **Greatest Common Divisor (GCD)**: The largest integer that divides two numbers without remainder, computed using Euclid's algorithm in $O(\log(\min(a, b)))$.
* **Logarithm Property**: $\log_b(N) = k \iff b^k = N$. In computer science, default base is $2$ ($\log_2 N$).
* **Sum Formulas**: Arithmetic Progression sum $S_n = \frac{n(n+1)}{2}$. Geometric Progression sum $S_n = \frac{a(r^n - 1)}{r - 1}$.

> **Memory Trick:** **"Prevent Overflow with Modulo early"**. When returning answers modulo $10^9 + 7$, perform `% MOD` after EVERY addition or multiplication step.

## 3. Characteristics / Properties
* **Properties of Logarithms**:
  * $\log(a \cdot b) = \log(a) + \log(b)$
  * $\log(a / b) = \log(a) - \log(b)$
  * $\log(a^k) = k \cdot \log(a)$
  * Number of digits in base 10 of integer $N = \lfloor\log_{10}(N)\rfloor + 1$.
  * Number of bits in binary representation of $N = \lfloor\log_2(N)\rfloor + 1$.
* **Euclidean Algorithm Invariant**: $\gcd(a, b) = \gcd(b, a \pmod b)$ with base case $\gcd(a, 0) = a$.
* **LCM & GCD Relation**: $a \cdot b = \gcd(a, b) \cdot \text{lcm}(a, b) \implies \text{lcm}(a, b) = \frac{a \cdot b}{\gcd(a, b)}$.

## 4. Internal Working
Euclid's GCD Execution Trace for `gcd(48, 18)`:

```
Step 1: gcd(48, 18) -> 48 % 18 = 12 -> Next call: gcd(18, 12)
Step 2: gcd(18, 12) -> 18 % 12 = 6  -> Next call: gcd(12, 6)
Step 3: gcd(12, 6)  -> 12 % 6  = 0  -> Next call: gcd(6, 0)
Step 4: gcd(6, 0)   -> Base case b=0 -> Returns 6
```

## 5. Visual Diagram
Modular Arithmetic Cycle ($\pmod 5$):

```
                       0
                    /     \
                   4       1
                    \     /
                     3 - 2

Every addition (x + 1) moves clockwise. 
Subtractions (x - 1) move counter-clockwise.
```

## 6. Operations / Algorithms
Standard Mathematical Formulas for Coding Problems:
1. **Fast Exponentiation (Binary Exponentiation)**: Calculates $a^b \pmod M$ in $O(\log b)$ time using bit manipulation / recursive halving.
2. **Modular Subtraction**: To handle negative mod results in Java: `(a % M + M) % M`.
3. **Digit Extraction**:
   * Last digit of $N$: `N % 10`
   * Remove last digit: `N / 10`

> **Quick Syntax:**
```java
// Modular Arithmetic Constants
public static final int MOD = 1_000_000_007;

// Euclidean GCD
public static long gcd(long a, long b) {
    return b == 0 ? a : gcd(b, a % b);
}

// LCM using GCD (avoiding overflow)
public static long lcm(long a, long b) {
    return (a / gcd(a, b)) * b;
}
```

## 7. Examples
* **Sum of First $N$ Natural Numbers**: $O(1)$ formula `n * (n + 1) / 2` vs $O(n)$ loop.
* **Fast Power $A^B \pmod M$**: $O(\log B)$ using recursive halving vs $O(B)$ sequential multiplication.
* **Count Digits**: $O(1)$ formula `(int) Math.log10(N) + 1` vs $O(\log_{10} N)$ loop.
* **Check Prime**: $O(\sqrt{N})$ trial division up to $\sqrt{N}$ vs $O(N)$ trial division.

## 8. Java Code
Interview-ready Java implementation of mathematical utility algorithms.

```java
public class MathForDSA {

    // Fast Power O(log b)
    public static long power(long a, long b, long mod) {
        long res = 1;
        a %= mod;
        while (b > 0) {
            if ((b & 1) == 1) { // If b is odd
                res = (res * a) % mod;
            }
            a = (a * a) % mod; // Square the base
            b >>= 1;          // Divide exponent by 2
        }
        return res;
    }

    // Check Prime O(sqrt(N))
    public static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;

        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    // Safe Modular Arithmetic Addition & Subtraction
    public static long safeModAdd(long a, long b, long mod) {
        return ((a % mod) + (b % mod)) % mod;
    }

    public static long safeModSub(long a, long b, long mod) {
        return ((a % mod) - (b % mod) + mod) % mod;
    }

    public static void main(String[] args) {
        long MOD = 1_000_000_007;
        System.out.println("2^10 % 1000000007 = " + power(2, 10, MOD));
        System.out.println("Is 29 Prime? " + isPrime(29));
        System.out.println("GCD(48, 18) = " + gcd(48, 18));
        System.out.println("LCM(48, 18) = " + lcm(48, 18));
    }

    private static long gcd(long a, long b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    private static long lcm(long a, long b) {
        return (a / gcd(a, b)) * b;
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Sum $1 \dots N$ Formula** | $O(1)$ | $O(1)$ | Use `long` to prevent overflow |
| **Euclidean GCD** | $O(\log(\min(a, b)))$ | $O(\log(\min(a, b)))$ recursive | Worst case occurs on consecutive Fibonacci numbers |
| **Binary Exponentiation** | $O(\log B)$ | $O(1)$ iterative | Halves exponent each iteration |
| **Trial Division Prime Check**| $O(\sqrt{N})$ | $O(1)$ | Check up to $i \cdot i \le N$ |
| **Sieve of Eratosthenes** | $O(N \log(\log N))$ | $O(N)$ boolean array | Precomputes primes up to $N$ |

## 10. Edge Cases
* **Integer Overflow in Multiplication**: `a * b` overflows `32-bit int` before `% MOD`. Cast operands to `long` first: `(long) a * b % MOD`.
* **Negative Remainder in Java**: In Java, `-7 % 5 = -2`. For modular indexing, use `(x % M + M) % M` to get positive result `3`.
* **Division by Zero in Modulo**: Modulo $M = 0$ triggers `ArithmeticException`.

## 11. Common Mistakes
* Computing LCM via `(a * b) / gcd(a, b)` directly (causes `a * b` integer overflow before division). Always compute `(a / gcd(a, b)) * b`.
* Running prime checking loops up to $N/2$ instead of $\sqrt{N}$.
* Forgetting that modulo does NOT distribute over division: $(a / b) \pmod M \neq ((a \pmod M) / (b \pmod M)) \pmod M$. (Requires Modular Multiplicative Inverse).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `10^9 + 7` ($1000000007$) is commonly used as a modulo constant in competitive programming and interviews because it is a large prime number that fits inside standard 32-bit signed integers, preventing integer overflow during addition.

> **Memory Trick:** **"Divide before Multiply for LCM"**:
> `lcm = (a / gcd(a, b)) * b` (Prevents `a * b` integer overflow).

## 13. Comparisons
| Operation | Formula / Method | Time Complexity | Java Code Note |
| :--- | :--- | :--- | :--- |
| **Digit Count** | $\lfloor\log_{10} N\rfloor + 1$ | $O(1)$ | `(int) Math.log10(N) + 1` |
| **Bit Count** | $\lfloor\log_{2} N\rfloor + 1$ | $O(1)$ | `Integer.toBinaryString(N).length()` |
| **Odd / Even Check** | Bitwise AND `(N & 1)` | $O(1)$ | `(N & 1) == 0` is even |
| **Power of 2 Check** | `(N > 0) && ((N & (N - 1)) == 0)` | $O(1)$ | Fast bit trick |

## 14. How to Recognize This in Questions
* **"Return answer modulo 10^9 + 7"**: Indicates problem involves dynamic programming or combinatorial math where values grow exponentially.
* **"Find maximum shared factor / cyclic occurrence"**: Signals **GCD / LCM**.
* **"Rotate array by K steps"**: Signals Modular indexing `(i + K) % N`.

## 15. Frequently Asked Interview Questions
* **Q: Why does checking for primes only require searching up to $\sqrt{N}$?**  
  *A:* If $N = a \cdot b$, both factors cannot be greater than $\sqrt{N}$. If one factor is greater than $\sqrt{N}$, the other must be less than or equal to $\sqrt{N}$.
* **Q: How do you perform modular division $(A / B) \pmod M$?**  
  *A:* Using Fermat's Little Theorem (when $M$ is prime), $B^{-1} \equiv B^{M-2} \pmod M$. Thus, $(A / B) \pmod M = (A \cdot B^{M-2}) \pmod M$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATHEMATICS FOR DSA                                  |
+-----------------------------------------------------------------------+
| • LCM Formula: (a / gcd(a, b)) * b  [Prevents Overflow]               |
| • Java Negative Modulo Fix: (x % M + M) % M                           |
| • Fast Exponentiation: O(log B) via bit halving                      |
| • Prime Check Loop Bound: i * i <= N (O(sqrt(N)))                     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement Euclidean GCD recursively and iteratively.
- [ ] I know how to calculate LCM safely without integer overflow.
- [ ] I understand how to handle negative modulo results in Java.
- [ ] I can explain why prime check loops only need to iterate up to $\sqrt{N}$.
- [ ] I can implement binary exponentiation $O(\log B)$ using bitwise operators.
