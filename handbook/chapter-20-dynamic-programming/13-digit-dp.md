# 13. Digit DP: Range $[A \dots B]$ Counting, Tight Bounds & Sub-State Traversals

## 1. Introduction
**Digit Dynamic Programming** is a specialized DP technique designed to count or sum valid integers in a given numerical range $[A \dots B]$ ($B \le 10^{18}$) that satisfy specific digit-level properties (such as having unique digits, containing no adjacent matching digits, possessing a specific digit sum, or containing digit sequences like "49"). Because the range bound $B$ can be up to $10^{18}$, iterating through numbers individually takes $O(B)$ time, which is impossibly slow. Digit DP processes the integer **Digit-by-Digit from Most Significant Digit (MSD) to Least Significant Digit (LSD)** using a Memoized State Vector. Digit DP reduces counting time from $O(B)$ down to **$O(\text{Length} \cdot \text{States})$ Linear Logarithmic Time** ($O(\log_{10} B)$).

> **Important:** Core Structural Invariants of Digit DP:
> 1. **Range Subtraction Invariant**:
>    - The number of valid integers in range $[A \dots B]$ is evaluated using range decomposition:
>      $$\text{Count}([A \dots B]) = \text{Count}(B) - \text{Count}(A - 1)$$
> 2. **`tight` Boundary Invariant**:
>    - Boolean parameter `tight` tracks whether current digit choices are constrained by the prefix of upper bound $B$:
>      - If `tight == true`: Current digit choice $d$ is restricted to $0 \le d \le \text{digit}[idx]$.
>      - If `tight == false`: Current digit choice $d$ is unconstrained: $0 \le d \le 9$.
> 3. **`isLeadingZero` Invariant**:
>    - Boolean parameter `isLeadingZero` distinguishes leading zero padding (e.g. `007` $\to$ single digit `7`) from structural internal zeros.
> 4. **State Vector Representation**:
>    - $DP[\text{idx}][\text{tight}][\text{leading\_zero}][\text{property\_mask}]$ uniquely identifies a subproblem state. ⚡

```
Digit DP State Traversal Tree (Upper Bound B = "352"):

Index 0 (MSD):
├── Choice d = 0, 1, 2 ──► tight = false (All future digits can be 0..9!) ⚡
└── Choice d = 3       ──► tight = true  (Next digit constrained by '5'!)

Index 1:
├── From tight = false ──► Choices 0..9 (All unconstrained)
└── From tight = true  ──► Choices 0..5 (Constrained by digit[1]=5)

Drastically prunes 10^18 search space down to O(Length * States)! ⚡
```

---

## 2. Core Concepts & Digit DP Strategy Matrix

### 2.1 Digit DP Strategy Matrix
```
Digit DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Target Metric     | Key State Mask    | Range Decomposition| Time Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Numbers At Most N (902)**| Count valid digits| Substring match   | $\text{Count}(N)$ | **$O(\log_{10} N \cdot D)$ ⚡**|
| **Unique Digits (357)**| Count unique digits| Bitmask of used $d$| $\text{Count}(N)$ | **$O(\log_{10} N \cdot 2^{10})$⚡**|
| **Digit Sum Range**   | Sum of digits     | Accumulated sum   | $\text{Count}(B) - \text{Count}(A-1)$| **$O(\log_{10} B \cdot \text{Sum})$⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Range Count([A..B]) = Count(B) - Count(A-1); tight == true constrains digit d <= limit; tight == false allows 0..9!"**

---

## 3. Characteristics & Tight Bound Mathematical Proof

### 3.1 Mathematical Proof of `tight` State Branching
* Let upper bound $B$ have digit representation $D_1 D_2 \dots D_L$ (length $L = \lfloor \log_{10} B \rfloor + 1$).
* When choosing digit $d_k$ at position $k$:
  - If all previously chosen digits matched the upper bound prefix ($d_1 = D_1, d_2 = D_2 \dots d_{k-1} = D_{k-1}$), setting $d_k > D_k$ would make the resulting number exceed $B$. Thus, $d_k$ MUST be $\le D_k$ (`tight == true`).
  - If any previously chosen digit was strictly smaller than its prefix counterpart ($d_m < D_m$ for some $m < k$), the resulting number is GUARANTEED to be smaller than $B$ regardless of future choices. Thus, $d_k$ can be ANY digit $0 \le d_k \le 9$ (`tight == false`).
* Once `tight` transitions to `false` at step $m$, ALL subsequent child branches retain `tight = false`.
* This reduces total evaluated states per length to $2 \times \text{Length} \times \text{Masks}$, proving **$O(\log_{10} B \cdot \text{Masks})$ Time Complexity**. ⚡

---

## 4. Internal Working Mechanics: Recursive Digit DP Template

Standard production structure of Digit DP DFS Function:

```
int countDigitDFS(String S, int idx, boolean tight, boolean isLeadingZero, int mask, int[][][] memo) {
    if (idx == S.length()) return isLeadingZero ? 0 : 1; // Base case: Formed valid number
    if (!tight && !isLeadingZero && memo[idx][mask] != -1) return memo[idx][mask]; // Memo return!

    int limit = tight ? (S.charAt(idx) - '0') : 9;
    int totalWays = 0;

    for (int d = 0; d <= limit; d++) {
        boolean nextTight = tight && (d == limit);
        boolean nextLeadingZero = isLeadingZero && (d == 0);
        int nextMask = nextLeadingZero ? mask : (mask | (1 << d));

        totalWays += countDigitDFS(S, idx + 1, nextTight, nextLeadingZero, nextMask, memo);
    }

    if (!tight && !isLeadingZero) memo[idx][mask] = totalWays;
    return totalWays;
}
```

---

## 5. Visual Diagram: Range Decomposition Breakdown

```
Range Decomposition Strategy:

Target Range [ A = 100, B = 500 ]:

Calculate Count(B = 500) ──► Counts valid numbers in range [ 0 ... 500 ]
Calculate Count(A - 1 = 99) ──► Counts valid numbers in range [ 0 ... 99 ]

Result = Count(500) - Count(99) = Valid Numbers in [ 100 ... 500 ]! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Digit DP across Range Decomposition, Numbers At Most N Given Digit Set (LeetCode 902), and Count Numbers with Unique Digits (LeetCode 357).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Digit DP Algorithms:
 * Range Decomposition, Tight Bounds, Leading Zeros, and Unique Digits Counting.
 */
public class DigitDPProblemsMaster {

    // =========================================================================
    // 1. LEETCODE 902: NUMBERS AT MOST N GIVEN DIGIT SET (O(log10 N) Time)
    // =========================================================================
    /**
     * Finds total positive integers <= N that can be written using digits array.
     *
     * @param digits array of valid digit strings (e.g. ["1","3","5","7"])
     * @param n upper bound integer N
     * @return total valid count
     */
    public int atMostNGivenDigitSet(String[] digits, int n) {
        if (digits == null || digits.length == 0 || n <= 0) return 0;

        String sN = String.valueOf(n);
        int len = sN.length();
        int[] digitSet = new int[digits.length];
        for (int i = 0; i < digits.length; i++) digitSet[i] = Integer.parseInt(digits[i]);

        int[][][] memo = new int[len][2][2];
        for (int[][] m1 : memo) for (int[] m2 : m1) Arrays.fill(m2, -1);

        return countAtMostDFS(sN, 0, true, true, digitSet, memo);
    }

    private int countAtMostDFS(String sN, int idx, boolean tight, boolean isLeadingZero, int[] digitSet, int[][][] memo) {
        if (idx == sN.length()) return isLeadingZero ? 0 : 1; // Valid non-zero number formed

        int tIdx = tight ? 1 : 0;
        int lIdx = isLeadingZero ? 1 : 0;
        if (memo[idx][tIdx][lIdx] != -1) return memo[idx][tIdx][lIdx];

        int limit = tight ? (sN.charAt(idx) - '0') : 9;
        int count = 0;

        // Option 1: Continue leading zero (if currently leading zero)
        if (isLeadingZero) {
            count += countAtMostDFS(sN, idx + 1, false, true, digitSet, memo);
        }

        // Option 2: Try picking digits from allowed digit set
        for (int d : digitSet) {
            if (d <= limit) {
                boolean nextTight = tight && (d == limit);
                count += countAtMostDFS(sN, idx + 1, nextTight, false, digitSet, memo);
            }
        }

        memo[idx][tIdx][lIdx] = count;
        return count;
    }

    // =========================================================================
    // 2. LEETCODE 357: COUNT NUMBERS WITH UNIQUE DIGITS (O(10) Time)
    // =========================================================================
    /**
     * Counts numbers x with unique digits where 0 <= x < 10^n.
     */
    public int countNumbersWithUniqueDigits(int n) {
        if (n == 0) return 1;
        if (n > 10) n = 10; // Max 10 unique digits possible (0..9)

        int totalCount = 10; // Base case for n = 1 (digits 0..9)
        int uniqueDigitsCount = 9;
        int availableDigits = 9;

        for (int i = 2; i <= n; i++) {
            uniqueDigitsCount *= availableDigits;
            totalCount += uniqueDigitsCount;
            availableDigits--;
        }

        return totalCount;
    }

    // =========================================================================
    // 3. DIGIT DP RANGE COUNTING SUITE (Count Numbers with Digit Constraint)
    // =========================================================================
    /**
     * Counts numbers in range [a .. b] having no adjacent duplicate digits.
     */
    public int countNoAdjacentDuplicatesInRange(int a, int b) {
        return countNoAdj(b) - countNoAdj(a - 1); // Range Decomposition! ⚡
    }

    private int countNoAdj(int n) {
        if (n < 0) return 0;
        if (n == 0) return 1;

        String sN = String.valueOf(n);
        int len = sN.length();
        int[][][] memo = new int[len][11][2];
        for (int[][] m1 : memo) for (int[] m2 : m1) Arrays.fill(m2, -1);

        return countNoAdjDFS(sN, 0, 10, true, true, memo);
    }

    private int countNoAdjDFS(String sN, int idx, int lastDigit, boolean tight, boolean isLeadingZero, int[][][] memo) {
        if (idx == sN.length()) return 1;

        int tIdx = tight ? 1 : 0;
        if (memo[idx][lastDigit][tIdx] != -1) return memo[idx][lastDigit][tIdx];

        int limit = tight ? (sN.charAt(idx) - '0') : 9;
        int count = 0;

        for (int d = 0; d <= limit; d++) {
            if (!isLeadingZero && d == lastDigit) continue; // No adjacent duplicate digits! ⚡

            boolean nextTight = tight && (d == limit);
            boolean nextLeadingZero = isLeadingZero && (d == 0);
            int nextLastDigit = nextLeadingZero ? 10 : d;

            count += countNoAdjDFS(sN, idx + 1, nextLastDigit, nextTight, nextLeadingZero, memo);
        }

        memo[idx][lastDigit][tIdx] = count;
        return count;
    }
}
```

> **Quick Syntax:**
```java
// Digit DP Range Decomposition & Tight Bound Lines
int limit = tight ? (sN.charAt(idx) - '0') : 9; boolean nextTight = tight && (d == limit);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 902 - Numbers At Most N Given Digit Set**:
   - Digit DP counting benchmark ($O(\log_{10} N \cdot D)$ time).

2. **LeetCode 357 - Count Numbers with Unique Digits**:
   - Unique digit permutations counting benchmark ($O(10)$ time).

3. **Range Digit Counting ($[A \dots B]$)**:
   - Evaluated via Range Decomposition $\text{Count}(B) - \text{Count}(A-1)$.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class DigitDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   DIGIT DYNAMIC PROGRAMMING BENCHMARK DEMO      ");
        System.out.println("=================================================\n");

        DigitDPProblemsMaster master = new DigitDPProblemsMaster();

        // 1. LeetCode 902 Test
        String[] digits = {"1", "3", "5", "7"};
        int n = 100;
        int count902 = master.atMostNGivenDigitSet(digits, n);

        System.out.println("1. LeetCode 902 Numbers At Most N = " + n + " with Digits [1, 3, 5, 7]:");
        System.out.println("   Total Valid Integers: " + count902 + " (1-digit: 4, 2-digit: 16 -> Total 20)");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 357 Test
        int numLen = 3;
        int countUnique = master.countNumbersWithUniqueDigits(numLen);
        System.out.println("2. LeetCode 357 Unique Digits for 0 <= x < 10^" + numLen + ":");
        System.out.println("   Total Numbers with Unique Digits: " + countUnique + " (Optimal = 739)");
        System.out.println("-------------------------------------------------");

        // 3. Digit Range Test [10 .. 50]
        int a = 10, b = 50;
        int noAdjCount = master.countNoAdjacentDuplicatesInRange(a, b);
        System.out.println("3. Range Digit Counting [ " + a + " .. " + b + " ] (No Adjacent Duplicate Digits):");
        System.out.println("   Total Valid Numbers: " + noAdjCount + " Numbers");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Digit DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Numbers At Most N (902)**| $\mathbf{O(\log_{10} N \cdot D)}$ ⚡| $O(\log_{10} N)$ Stack | `tight` & `isLeadingZero` |
| **Unique Digits (357)**| $\mathbf{O(10)}$ Constant ⚡| $\mathbf{O(1)}$ Memory ⚡| Permutation math |
| **Range Digit Counting**| $\mathbf{O(\log_{10} B \cdot S)}$⚡| $O(\log_{10} B \cdot S)$ Memo| Range decomposition $B - (A-1)$ |

---

## 10. Edge Cases & Boundary Handling

1. **Upper Bound $A = 0$ in Range Decomposition**:
   - `count(0)` handles single-digit zero explicitly.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Memoizing States When `tight == true`**:
  - When `tight == true`, future digit choices are restricted by upper bound $B$. Memoizing state when `tight == true` pollutes the cache for future unconstrained searches. **ONLY memoize when `tight == false` and `isLeadingZero == false`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Digit DP Memoization Rule:
> Never return cached results or store to the memoization array when **`tight == true`** or **`isLeadingZero == true`**! Only cache unconstrained state branches (`tight == false && !isLeadingZero`)! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Range Iteration | Digit DP Traversal |
| :--- | :--- | :--- |
| **Time Complexity** | $O(B)$ Exponential ($10^{18}$) ❌ | **$O(\log_{10} B)$ Linear Log ⚡** |
| **Range Limit** | $B \le 10^7$ | **$B \le 10^{18}$ ⚡** |
| **Control Flow** | Iterative Loop | Top-Down DFS + Memoization |

---

## 14. How to Recognize This in Questions

* **"Count numbers in range [A .. B] up to 10^18 having specific digit property"** $\rightarrow$ Digit DP.
* **"Count numbers at most N constructed from digit set"** $\rightarrow$ LeetCode 902.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Range Decomposition evaluate $\text{Count}(B) - \text{Count}(A-1)$?**  
  *A:* Because computing valid numbers in $[0 \dots N]$ is significantly easier with a single upper bound $N$. Subtracting $\text{Count}(A-1)$ isolates the exact range $[A \dots B]$.

* **Q: Why is `tight` necessary in Digit DP?**  
  *A:* To enforce that digits selected at the current position do not exceed the upper bound $B$'s digit at the same position when all previous digits matched $B$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: DIGIT DP                                              |
+-----------------------------------------------------------------------+
| • Range Rule  : Count([A..B]) = Count(B) - Count(A - 1)               |
| • Tight Bound : Limit = tight ? digit[idx] : 9                        |
| • Next Tight  : nextTight = tight && (d == limit)                     |
| • Memo Guard  : ONLY memoize when tight == false && !isLeadingZero ⚡ |
| • Performance : O(log10 B * States) Time | Handles B <= 10^18! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Digit DP Range Decomposition $\text{Count}(B) - \text{Count}(A-1)$ in Java.
- [ ] I can solve LeetCode 902 (`Numbers At Most N Given Digit Set`).
- [ ] I can solve LeetCode 357 (`Count Numbers with Unique Digits`).
- [ ] I can explain why `tight == true` states must NOT be memoized.
- [ ] I can state the purpose of `isLeadingZero`.
