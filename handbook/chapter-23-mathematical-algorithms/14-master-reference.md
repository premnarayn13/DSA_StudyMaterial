# 14. Master Reference — Mathematical Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 30: Mathematical Algorithms**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Number Theory, Prime Factorization ($\sigma_0, \sigma_1$, SPF Sieve), Prime Algorithms (Sieve of Eratosthenes, Segmented Sieve, Miller-Rabin), Euclidean Algorithms (Standard GCD, Safe LCM, Extended GCD, Linear Diophantine), Modular Arithmetic ($10^9+7$, Negative Mod Guard, 64-bit Multiplication), Fast Exponentiation ($O(\log N)$), Modular Inverse (Fermat $A^{M-2}$, Extended GCD, Linear Range DP), Euler Totient ($\phi(N)$, Euler's Theorem), Chinese Remainder Theorem (CRT, Non-Coprime Merger), Combinatorics (Pascal DP, Catalan $C_N$, Inclusion-Exclusion), Matrix Exponentiation (Fibonacci $O(\log N)$), Probability (Reservoir Sampling $1/N$, Linearity of Expectation, Las Vegas vs Monte Carlo), Mathematical Optimization (Newton-Raphson Sqrt, Golden Section, Continuous BS), and the 6 Master Mathematical Archetypes.

> **Important:** Review this master reference 15 minutes before an interview to refresh Prime Factorization ($\sigma_0(N) = \prod (e_i + 1)$), Divisor Sum ($\sigma_1(N) = \prod \frac{p_i^{e_i+1}-1}{p_i-1}$), Safe LCM (`(a / gcd) * b`), Extended GCD recurrence ($x = y_1, y = x_1 - \lfloor a/b \rfloor y_1$), Negative Modulo Guard `(a - b % M + M) % M`, 64-Bit Multiplication Guard `((long) a * b) % M`, Fast Power $O(\log N)$, Fermat's Inverse $A^{M-2} \bmod M$, Linear Range Inverses DP (`inv[i] = M - (M/i) * inv[M%i] % M`), Euler Product Formula $\phi(N) = N \prod \frac{p-1}{p}$, CRT Formula $X = \sum a_i M_i Y_i \pmod M$, Catalan Number $C_N = \frac{1}{N+1} \binom{2N}{N}$, Fibonacci Matrix Power $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^N$, Reservoir Sampling $P = 1/i$, and Newton-Raphson Sqrt $x = 0.5(x + N/x)$!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Fundamental Theorem of Arithmetic**:
  - $N = p_1^{e_1} \times p_2^{e_2} \dots \times p_k^{e_k}$.
* **Divisor Functions Formulas**:
  - Total Divisors Count: $\sigma_0(N) = \prod_{i=1}^k (e_i + 1)$.
  - Sum of Divisors: $\sigma_1(N) = \prod_{i=1}^k \frac{p_i^{e_i + 1} - 1}{p_i - 1}$.
* **Trial Division Search Bound**:
  - Search prime factors up to $\sqrt{N}$ (`p * p <= N`).
* **Euclidean GCD & Safe LCM**:
  - $\gcd(a, b) = \text{b == 0 ? a : gcd(b, a \% b)}$.
  - Safe LCM: $\text{lcm}(a, b) = (a / \gcd(a, b)) \times b$ (Divide FIRST!).
* **Extended Euclidean Bezout Recurrence**:
  - $a \cdot x + b \cdot y = \gcd(a, b) \implies x = y_1, y = x_1 - \lfloor a/b \rfloor \times y_1$.
* **Modular Arithmetic Guards**:
  - Subtraction Guard: `(a - b % M + M) % M`.
  - 64-bit Multiplication Guard: `((long) a * b) % M`.
  - Division via Inverse: `(a * modInverse(b)) % M`.
* **Fast Exponentiation Recurrence**:
  - $A^N = (A^2)^{N/2}$ if $N$ is even; $A \times (A^2)^{(N-1)/2}$ if $N$ is odd.
* **Modular Inverse Formulas**:
  - Fermat's Inverse (Prime $M$): $A^{-1} \equiv A^{M-2} \pmod M$.
  - Linear Range DP ($1 \dots N \pmod M$): $inv[i] = M - \lfloor M/i \rfloor \times inv[M \bmod i] \pmod M$.
* **Euler Totient Function ($\phi(N)$)**:
  - Product Formula: $\phi(N) = N \times \prod_{p \mid N} \frac{p - 1}{p}$.
  - Euler's Theorem: If $\gcd(A, M) = 1$, $A^{\phi(M)} \equiv 1 \pmod M \implies A^B \pmod M = A^{B \pmod{\phi(M)}} \pmod M$.
* **Chinese Remainder Theorem (CRT)**:
  - $M = \prod m_i, M_i = M / m_i, Y_i = M_i^{-1} \pmod{m_i} \implies X = \sum a_i M_i Y_i \pmod M$.
* **Combinatorics & Catalan Numbers**:
  - Pascal DP: $C(N, K) = C(N-1, K-1) + C(N-1, K)$.
  - Catalan Number (LC 96): $C_N = \frac{1}{N+1} \binom{2N}{N}$. Recurrence $C_N = \sum_{j=0}^{N-1} C_j \times C_{N-1-j}$.
* **Fibonacci Matrix Exponentiation**:
  - $\begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n$ in $O(\log N)$ time.
* **Reservoir Sampling Invariant**:
  - For stream item $i$ (1-indexed): Select item $i$ with probability $P = \frac{1}{i}$ (`random.nextInt(i) == 0`). Yields exact uniform $P = \frac{1}{N}$.
* **Newton-Raphson Square Root (LC 69)**:
  - $x_{k+1} = \frac{1}{2} \left( x_k + \frac{N}{x_k} \right)$ (Quadratic convergence!).

```
Master Mathematical Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Mathematical Topic    | Core Formula      | Primary Engine    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Prime Factorization**| $\sigma_0(N) = \prod(e_i+1)$| Trial Division | **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Sieve of Eratosthenes**| Mark $p^2$ multiples| Sieve Array     | **$O(N \log \log N)$⚡**| $O(N)$ Array Space|
| **Segmented Sieve**   | Range $[L, R]$    | Small Primes Sieve| **$O((R-L+1)\log \log R)$⚡**| **$O(\sqrt{R})$ Space ⚡**|
| **Miller-Rabin Test** | 12 Fixed Bases    | Fermat Modular    | **$O(K \log^3 N)$ ⚡**| **$O(1)$ Memory ⚡**|
| **Euclidean GCD**     | $\gcd(a,b)=\gcd(b,a\%b)$| Modulo Division | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**|
| **Safe LCM**          | $(a / \gcd) \times b$| Divide FIRST     | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**|
| **Extended GCD**      | $ax + by = \gcd$  | Recurrence        | **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**|
| **Modular Arithmetic**| Negative/Mul Guard| Modulo Rules      | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Fast Exponentiation**| $A^N \pmod M$    | Binary Bit Shift  | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Fermat Inverse**    | $A^{M-2} \bmod M$ | Fast Power        | **$O(\log M)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Linear Range Inv**  | $inv[i] = M - (M/i)\dots$| DP Recurrence | **$O(N)$ Strict Linear⚡**| $O(N)$ Array Space|
| **Euler Totient**     | $\phi(N) = N \prod \frac{p-1}{p}$| Prime Product  | **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **CRT Solver**        | $X = \sum a_i M_i Y_i$| Explicit Sum   | **$O(K \log M)$ Fast ⚡**| $O(K)$ Array Space |
| **Catalan (LC 96)**   | $C_N = \frac{1}{N+1} \binom{2N}{N}$| Convolution DP| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Matrix Fibonacci**  | $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^N$| Matrix Power| **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Reservoir Sampling**| $P = 1 / i$        | Random Choice     | **$O(N)$ Single Pass⚡**| **$O(1)$ Memory ⚡**|
| **Newton-Raphson Sqrt**| $x = 0.5(x + N/x)$ | Tangent Recurrence| **$O(\log(\text{prec}))$⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Mathematical Topic | Primary Formula | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Prime Factorization** | Trial Division | $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Loop up to $\sqrt{N}$ |
| **Sieve of Eratosthenes**| Mark $p^2$ | $\mathbf{O(N \log \log N)}$ ⚡| $O(N)$ Array Space| Classical prime sieve |
| **Segmented Sieve** | Range $[L, R]$ | $\mathbf{O((R-L+1)\log \log R)}$⚡| $\mathbf{O(\sqrt{R})}$ Space ⚡| Fits in 32 KB CPU L1 Cache |
| **Miller-Rabin Test** | 64-Bit Deterministic| $\mathbf{O(K \log^3 N)}$ Fast⚡| $\mathbf{O(1)}$ Memory ⚡| 12 Fixed bases |
| **Euclidean GCD** | Modulo Reduction | $\mathbf{O(\log(\min(a,b)))}$⚡| $\mathbf{O(1)}$ Memory ⚡| Worst case Fibonacci |
| **Safe LCM** | Divide First | $\mathbf{O(\log(\min(a,b)))}$⚡| $\mathbf{O(1)}$ Memory ⚡| $(a / \gcd) \times b$ |
| **Extended GCD** | Bezout Coefficients| $\mathbf{O(\log(\min(a,b)))}$⚡| $\mathbf{O(1)}$ Memory ⚡| $ax + by = \gcd$ |
| **Fast Exponentiation** | Binary Bit Shifts | $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| `exp >>= 1` & base squaring |
| **Fermat Inverse** | $A^{M-2} \bmod M$ | $\mathbf{O(\log M)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Prime modulus $M$ |
| **Linear Range Inv** | DP Recurrence | $\mathbf{O(N)}$ Strict Linear⚡| $O(N)$ Array Space| Range $1 \dots N$ inverses |
| **Euler Totient** | Product Formula | $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| $\phi(N) = N \prod \frac{p-1}{p}$ |
| **CRT Solver** | $X = \sum a_i M_i Y_i$ | $\mathbf{O(K \log M)}$ Fast ⚡| $O(K)$ Array Space| Pairwise coprime moduli |
| **Catalan BSTs (96)** | $C_N = \frac{1}{N+1} \binom{2N}{N}$| $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Unique BSTs count |
| **Matrix Fibonacci** | 2x2 Matrix Power | $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Cell `[0][1]` holds $F_N$ |
| **Reservoir Sampling** | $P = 1 / i$ | $\mathbf{O(N)}$ Single Pass⚡| $\mathbf{O(1)}$ Memory ⚡| Streaming uniform $1/N$ |
| **Newton Sqrt (69)** | $x = 0.5(x + N/x)$ | $\mathbf{O(\log(\text{prec}))}$ ⚡| $\mathbf{O(1)}$ Memory ⚡| Quadratic convergence |

---

## 4. Architectural System & Production Use Cases
```
+-----------------------------------------------------------------------------------+
| Production System Mathematical Architectures                                       |
+-----------------------------------------------------------------------------------+
| RSA & Elliptic Curve Cryptographic Key Engines   : Miller-Rabin, Fermat Inverse, CRT|
| Distributed Database Stream Sampling (Redis)     : Reservoir Sampling (O(1) Space) |
| Network Router Subnetting & Packet Scheduling   : Extended GCD & Diophantine Solvers|
| Parallel Big-Integer Multiplication (RSA CRT)    : CRT 4x Decryption Speedup      |
| Financial Options & High-Frequency Risk Engine   : Newton-Raphson & Golden Search |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Trial Division Prime Factorization & Divisors
> for (long p = 2; p * p <= n; p++) {
>     if (n % p == 0) { int e = 0; while (n % p == 0) { e++; n /= p; } totalDivisors *= (e + 1); }
> }
> 
> // 2. Segmented Sieve Range Start Offset
> long start = Math.max((long) p * p, ((L + p - 1) / p) * (long) p);
> 
> // 3. Euclidean GCD & Safe LCM
> long g = gcd(a, b); long lcm = (a / g) * b; // Divide FIRST!
> 
> // 4. Modular Arithmetic Guards
> long sub = (a - b % M + M) % M; long mul = ((long) a * b) % M;
> 
> // 5. Fast Exponentiation & Fermat Inverse
> while (exp > 0) { if ((exp & 1) == 1) res = (res * base) % mod; base = (base * base) % mod; exp >>= 1; }
> long inv = powerModular(a, primeMod - 2, primeMod);
> 
> // 6. Linear Range Inverses DP
> inv[i] = primeMod - (primeMod / i) * inv[(int)(primeMod % i)] % primeMod;
> 
> // 7. Euler Totient Product Formula
> if (temp % p == 0) { while (temp % p == 0) temp /= p; result -= result / p; }
> 
> // 8. CRT Explicit Construction
> long Mi = M / m[i]; long Yi = modInverse(Mi, m[i]); X = (X + a[i] * Mi * Yi) % M;
> 
> // 9. LeetCode 96 Catalan BST & Fibonacci Matrix Power
> dp[i] += dp[j] * dp[i - 1 - j]; long[][] T = {{1, 1}, {1, 0}}; return powerMatrix(T, n)[0][1];
> 
> // 10. Reservoir Sampling & Newton-Raphson Sqrt
> if (random.nextInt(count) == 0) reservoir = currentVal; root = 0.5 * (x + n / x);
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Multiplying Before Dividing in LCM (`(a * b) / gcd`)**: Multiplying $a \times b$ first overflows 64-bit `long` limits ($9.22 \times 10^{18}$). **ALWAYS divide first: `(a / gcd) * b`**!
* **Pitfall 2: Omitting Negative Modulo Guard in Subtraction**: Writing `(a - b) % M` yields negative remainders in Java (`-5 % 7 = -5`). **ALWAYS write `(a - b % M + M) % M`**!
* **Pitfall 3: Omitting `(long)` Cast in Modular Multiplication**: Writing `(intA * intB) % M` overflows 32-bit `int` limits before modulo execution. **ALWAYS write `((long) intA * intB) % M`**!
* **Pitfall 4: Applying Fermat's Inverse to Composite Modulus $M$**: Fermat's formula $A^{M-2} \bmod M$ is ONLY valid when $M$ is prime. **ALWAYS use Extended Euclidean Inverse for composite $M$**!
* **Pitfall 5: Applying Standard CRT to Non-Coprime Moduli**: Applying $M_i = M / m_i$ when $\gcd(m_i, m_j) \neq 1$ breaks the modular inverse. **ALWAYS check coprimality or use Non-Coprime Merger**!
* **Pitfall 6: Using While Condition `right - left > eps` for Continuous Binary Search**: Floating-point subtraction can cause infinite loops. **ALWAYS use fixed 60-80 iterations for continuous real binary search**!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 30 (MATHEMATICAL ALGORITHMS)     |
+-----------------------------------------------------------------------+
| 1. Divisor Count   : sigma_0(N) = (e1 + 1)(e2 + 1)...(ek + 1)         |
| 2. Safe LCM        : lcm(a, b) = (a / gcd(a, b)) * b (Divide FIRST!) ⚡|
| 3. Extended GCD    : x = child.y, y = child.x - (a / b) * child.y     |
| 4. Subtraction Guard: (a - b % M + M) % M (Prevents negative mod!)    |
| 5. Multiplication  : ((long) a * b) % M (Prevents 32-bit overflow!)   |
| 6. Fast Power      : A^N % M in O(log N) time via bit shifts          |
| 7. Fermat Inverse  : A^(M-2) % M for prime modulus M                  |
| 8. Linear Range Inv: inv[i] = M - (M/i) * inv[M%i] % M (O(N) DP!) ⚡   |
| 9. Euler Product   : phi(N) = N * ∏ (p - 1) / p                     |
| 10. CRT Formula    : X = sum(a_i * M_i * Y_i) % M for coprime m_i    |
| 11. Catalan BSTs   : C_N = (1 / (N+1)) * C(2N, N) (LeetCode 96) ⚡     |
| 12. Matrix Fibonacci: T = {{1, 1}, {1, 0}} -> T^N[0][1] = F_N O(log N) ⚡|
| 13. Reservoir Sample: select item i with P = 1 / i -> Uniform 1/N ⚡   |
| 14. Newton Sqrt    : x = 0.5 * (x + N / x) (LeetCode 69)              |
| 15. Continuous BS  : Use fixed 60 iterations to avoid infinite loops! ⚡|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Trial Division Prime Factorization and Divisor Count in Java.
- [ ] I can write Safe LCM in Java with divide-first protection.
- [ ] I can write Extended Euclidean algorithm in Java.
- [ ] I can write safe modular addition, subtraction, and multiplication guards in Java.
- [ ] I can write Modular Fast Exponentiation $A^N \bmod M$ in Java in $O(log N)$ time.
- [ ] I can write Fermat's modular inverse $A^{M-2} \bmod M$ in Java.
- [ ] I can write the $O(N)$ Linear Range Inverse DP array generator in Java.
- [ ] I can write single-value Euler Totient $\phi(N)$ in $O(\sqrt{N})$ time in Java.
- [ ] I can write the Standard CRT solver in Java.
- [ ] I can write LeetCode 96 (`Unique Binary Search Trees`) Catalan solver in Java.
- [ ] I can write Fibonacci 2x2 Matrix Exponentiation in $O(\log N)$ time in Java.
- [ ] I can write Reservoir Sampling for 1 item and $K$ items in Java.
- [ ] I can write Newton-Raphson integer square root (LeetCode 69) in Java.
- [ ] I can write continuous real domain binary search using fixed 60 iterations.
- [ ] I can match any mathematical question to one of the 6 Master Archetypes in under 10 seconds.
