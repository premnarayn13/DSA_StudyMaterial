# 06. Bit Counting: Hamming Weight, SWAR Parallel Adders & Dynamic Programming Range Counts

## 1. Introduction
**Bit Counting** (also known as computing the **Hamming Weight** or **Population Count (`popcount`)**) is the process of calculating the total number of set 1-bits in a binary representation. Population count is a core primitive in information theory, error-correcting codes, Hamming distance computations, and database bitmap indexes. While naive bit-by-bit inspection takes 32 iterations, advanced counting algorithms operate at extreme speeds: **Brian Kernighan's Algorithm** runs in **$O(\text{Set Bits})$ time** by clearing the lowest set bit at each step (`n &= (n - 1)`), **SWAR (SIMD Within A Register) Parallel Bit Adders** compute popcount in **5 $O(1)$ CPU operations**, and **Counting Bits (LeetCode 338)** generates set bit counts for all numbers from $0$ to $N$ in **$O(N)$ Linear Time** using Dynamic Programming state recurrence ($DP[i] = DP[i \gg 1] + (i \;\&\; 1)$).

> **Important:** The 4 Master Bit Counting Algorithms:
> 1. **Brian Kernighan's Algorithm**:
>    - `while (n != 0) { n = n & (n - 1); count++; }`
>    - Runs in $O(K)$ time where $K$ is the exact number of set 1-bits!
> 2. **SWAR Parallel Bitwise Adder (`Integer.bitCount`)**:
>    - Divides 32-bit integer into 2-bit, 4-bit, 8-bit, 16-bit parallel fields, summing bit counts in 5 bitwise instructions ($O(1)$ hardware speed).
> 3. **Hamming Distance (LeetCode 461)**:
>    - Calculates total bit positions where two integers $X$ and $Y$ differ:
>      $$\text{HammingDistance}(X, Y) = \text{popcount}(X \oplus Y)$$
> 4. **Counting Bits $0 \dots N$ DP Recurrence (LeetCode 338)**:
>    - Generates array of set bit counts for range $0 \dots N$ in $O(N)$ linear time:
>      $$DP[i] = DP[i \gg 1] + (i \;\&\; 1)$$ ⚡

```
Bit Counting SWAR Parallel Adder Topology (32-bit Integer):

Initial 32 Bits: [b31 b30 b29 b28 ... b3 b2 b1 b0]
                       │
Step 1: Parallel 2-bit field sum (Mask 0x55555555)
Step 2: Parallel 4-bit field sum (Mask 0x33333333)
Step 3: Parallel 8-bit field sum (Mask 0x0F0F0F0F)
Step 4: Multiply by 0x01010101 & Shift right 24

Computes total 1-bits across 32 bits in 5 O(1) CPU instructions! ⚡
```

---

## 2. Core Concepts & Bit Counting Strategy Matrix

### 2.1 Bit Counting Algorithms Strategy Matrix
```
Bit Counting Algorithms Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Counting Algorithm    | Target Input      | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Brian Kernighan**   | Single 32-bit Int | `n & (n - 1)`     | **$O(\text{Set Bits})$ ⚡**| **$O(1)$ Memory ⚡**|
| **SWAR / bitCount**   | Single 32-bit Int | Parallel Bit Adder| **$O(1)$ 5 Ops ⚡**| **$O(1)$ Memory ⚡**|
| **Hamming Distance**  | Two Ints X, Y     | `popcount(X ^ Y)` | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Counting Bits (338)**| Range $0 \dots N$| $DP[i >> 1] + (i \& 1)$| **$O(N)$ Linear ⚡**| **$O(N)$ Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Brian Kernighan counts set bits in O(Set Bits) using n & (n - 1); Counting Bits range 0..N uses DP[i >> 1] + (i & 1)!"**

---

## 3. Characteristics & Counting Bits DP Recurrence Proof

### 3.1 Mathematical Proof of Range Bit Count DP ($DP[i] = DP[i \gg 1] + (i \;\&\; 1)$)
* Let $P(i)$ be the total number of set 1-bits in the binary representation of integer $i$.
* Consider right-shifting $i$ by 1 position ($i \gg 1$):
  - $i \gg 1 = \lfloor \frac{i}{2} \rfloor$.
  - The binary representation of $i \gg 1$ contains all bits of $i$ EXCEPT the Least Significant Bit (LSB at bit 0).
* **LSB Contribution**:
  - The LSB of $i$ is given by $i \;\&\; 1$ (equals $1$ if $i$ is odd, $0$ if $i$ is even).
* **Total Set Bits Equation**:
  $$P(i) = P(i \gg 1) + (i \;\&\; 1)$$
* **Base Case**: $P(0) = 0$.
* By computing $DP[i]$ sequentially for $i = 1 \dots N$, every entry depends on a previously computed index $i \gg 1 < i$, filling the entire array in **$O(N)$ Strict Linear Time** and zero re-computations! ⚡

---

## 4. Internal Working Mechanics: SWAR 32-bit Parallel Bit Adder

Tracing SWAR Parallel Bit Adder (`Integer.bitCount(i)`):

```
SWAR 32-bit Parallel Mask Reductions:

Mask 1 (0x55555555): 01010101 01010101 01010101 01010101 (Pairs adjacent bits)
Mask 2 (0x33333333): 00110011 00110011 00110011 00110011 (Groups 4-bit nibbles)
Mask 3 (0x0F0F0F0F): 00001111 00001111 00001111 00001111 (Groups 8-bit bytes)

Execution Steps:
i = i - ((i >>> 1) & 0x55555555);
i = (i & 0x33333333) + ((i >>> 2) & 0x33333333);
i = (i + (i >>> 4)) & 0x0F0F0F0F;
i = i + (i >>> 8);
i = i + (i >>> 16);
Result = i & 0x3F (Extracts total 1-bits up to 32)!

Executes in pure bitwise instructions without loops or branches! ✅ ⚡
```

---

## 5. Visual Diagram: LeetCode 338 Counting Bits Range DP

```
LeetCode 338 Range Bit Count DP Array (N = 7):

Index i:    0    1    2    3    4    5    6    7
Binary :   000  001  010  011  100  101  110  111
DP[i]  :    0    1    1    2    1    2    2    3

Recurrence Calculation:
- DP[4] (100_2) = DP[4 >> 1] + (4 & 1) = DP[2] (010_2) + 0 = 1 + 0 = 1!
- DP[5] (101_2) = DP[5 >> 1] + (5 & 1) = DP[2] (010_2) + 1 = 1 + 1 = 2!
- DP[7] (111_2) = DP[7 >> 1] + (7 & 1) = DP[3] (011_2) + 1 = 2 + 1 = 3!

Generates all set bit counts in O(N) Linear Time! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Brian Kernighan's Algorithm, SWAR Parallel Bit Counting, Hamming Distance (LeetCode 461), and Counting Bits DP Range (LeetCode 338).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bit Counting Algorithms:
 * Brian Kernighan's Algorithm, SWAR Parallel Adders, Hamming Distance, and Counting Bits Range DP.
 */
public class BitCountingMaster {

    // =========================================================================
    // 1. BRIAN KERNIGHAN'S SET BIT COUNT (O(Set Bits) Time, O(1) Space)
    // =========================================================================
    /**
     * Counts set bits in single 32-bit integer in O(Set Bits) time.
     */
    public int countSetBitsBrianKernighan(int n) {
        int count = 0;
        while (n != 0) {
            n = n & (n - 1); // Clears lowest set bit! ⚡
            count++;
        }
        return count;
    }

    // =========================================================================
    // 2. SWAR PARALLEL BIT ADDER (O(1) 5 Bitwise Operations)
    // =========================================================================
    /**
     * Parallel bitwise population count (Equivalent to Integer.bitCount(n)).
     */
    public int countSetBitsSWAR(int i) {
        i = i - ((i >>> 1) & 0x55555555);
        i = (i & 0x33333333) + ((i >>> 2) & 0x33333333);
        i = (i + (i >>> 4)) & 0x0F0F0F0F;
        i = i + (i >>> 8);
        i = i + (i >>> 16);
        return i & 0x3F; // O(1) Hardware Speed! ⚡
    }

    // =========================================================================
    // 3. LEETCODE 461: HAMMING DISTANCE (O(1) Time, O(1) Space)
    // =========================================================================
    /**
     * Calculates number of positions where corresponding bits differ between x and y.
     */
    public int hammingDistance(int x, int y) {
        int xor = x ^ y; // Bits where x and y differ are set to 1! ⚡
        return Integer.bitCount(xor);
    }

    // =========================================================================
    // 4. LEETCODE 338: COUNTING BITS RANGE 0 ... N (O(N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates array of set bit counts for numbers from 0 to N.
     *
     * @param n range upper bound
     * @return array DP of size N+1
     */
    public int[] countBits(int n) {
        if (n < 0) return new int[0];
        int[] dp = new int[n + 1];

        // Base case DP[0] = 0
        for (int i = 1; i <= n; i++) {
            // DP Recurrence: DP[i] = DP[i >> 1] + (i & 1) ⚡
            dp[i] = dp[i >> 1] + (i & 1);
        }

        return dp;
    }
}
```

> **Quick Syntax:**
```java
// Counting Bits Range DP Recurrence Line
dp[i] = dp[i >> 1] + (i & 1); // Solves LeetCode 338 in O(N) linear time
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 191 - Number of 1 Bits**:
   - Hamming Weight benchmark solved using Brian Kernighan or `Integer.bitCount`.

2. **LeetCode 461 - Hamming Distance**:
   - Bitwise XOR popcount between two integers (`Integer.bitCount(x ^ y)`).

3. **LeetCode 338 - Counting Bits**:
   - Range bit count array generated in $O(N)$ linear time via DP recurrence.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BitCountingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BIT COUNTING ALGORITHMS BENCHMARK DEMO        ");
        System.out.println("=================================================\n");

        BitCountingMaster master = new BitCountingMaster();

        // 1. Brian Kernighan & SWAR Test
        int num = 44; // 00101100 (3 bits)
        System.out.println("1. Set Bit Count Benchmark for x = 44 (00101100_2):");
        System.out.println("   Brian Kernighan Count: " + master.countSetBitsBrianKernighan(num) + " Bits");
        System.out.println("   SWAR Parallel Count  : " + master.countSetBitsSWAR(num) + " Bits (Optimal = 3)");
        System.out.println("-------------------------------------------------");

        // 2. Hamming Distance Test (LeetCode 461)
        int x = 1, y = 4; // 0001 vs 0100 -> Differ at 2 positions
        System.out.println("2. LeetCode 461 Hamming Distance Between 1 and 4:");
        System.out.println("   Hamming Distance: " + master.hammingDistance(x, y) + " (Optimal = 2)");
        System.out.println("-------------------------------------------------");

        // 3. Counting Bits Range Test (LeetCode 338 N = 7)
        int n = 7;
        int[] rangeDP = master.countBits(n);
        System.out.println("3. LeetCode 338 Counting Bits DP for Range 0 ... " + n + ":");
        System.out.println("   DP Array (O(N) Time): " + Arrays.toString(rangeDP));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bit Counting Task | Algorithm Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Hamming Weight (191)**| Brian Kernighan | $\mathbf{O(\text{Set Bits})}$ ⚡| $\mathbf{O(1)}$ Memory ⚡| `n & (n - 1)` |
| **Popcount Single Int** | SWAR / `bitCount` | $\mathbf{O(1)}$ 5 CPU Ops ⚡| $\mathbf{O(1)}$ Memory ⚡| Parallel bit adder |
| **Hamming Distance (461)**| Bitwise XOR + Count| $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| `Integer.bitCount(x ^ y)` |
| **Counting Bits (338)** | Range DP Recurrence| $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(N)}$ Array ⚡| `DP[i >> 1] + (i & 1)` |

---

## 10. Edge Cases & Boundary Handling

1. **Negative Integers in `countBits` Range**:
   - Returns empty array `[]` for negative $N$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running $O(N \log N)$ Loop for LeetCode 338 Counting Bits**:
  - Running a 32-bit inspection loop for every number $0 \dots N$ takes $O(N \log N)$ time. **ALWAYS use the DP recurrence `DP[i] = DP[i >> 1] + (i & 1)` to achieve $O(N)$ linear time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** LeetCode 338 Counting Bits DP Formula:
> To generate the set bit count for range $0 \dots N$ in $O(N)$ time, use the 1-line DP recurrence:
> $$DP[i] = DP[i \gg 1] + (i \;\&\; 1)$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive Loop Count | Brian Kernighan | SWAR (`Integer.bitCount`) |
| :--- | :--- | :--- | :--- |
| **Iterations / Ops** | Always 32 Iterations | **Set Bits Count ⚡** | **5 CPU Bitwise Ops ⚡** |
| **Time Complexity** | $O(32)$ Constant | $O(K)$ Dynamic | **$O(1)$ Hardware Constant ⚡**|

---

## 14. How to Recognize This in Questions

* **"Count total number of set bits for all numbers from 0 to N in O(N) time"** $\rightarrow$ LeetCode 338 (`DP[i >> 1] + (i & 1)`).
* **"Find total bit positions where two numbers differ"** $\rightarrow$ LeetCode 461 (`Integer.bitCount(x ^ y)`).

---

## 15. Frequently Asked Interview Questions

* **Q: How does `DP[i] = DP[i >> 1] + (i & 1)` generate set bit counts in $O(N)$ time?**  
  *A:* Shifting $i$ right by 1 ($i \gg 1$) removes its LSB, so the set bit count of $i$ equals the previously computed set bit count of $i \gg 1$ plus the LSB bit value ($i \;\&\; 1$).

* **Q: What is Hamming Distance?**  
  *A:* The number of bit positions at which two integers $X$ and $Y$ have different bit values, computed via `Integer.bitCount(x ^ y)`.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BIT COUNTING                                          |
+-----------------------------------------------------------------------+
| • Brian Kernighan: while(n!=0) { n &= (n-1); count++; } -> O(SetBits) |
| • SWAR / bitCount: Built-in Integer.bitCount(n) -> 5 O(1) CPU Ops ⚡   |
| • Hamming Distance: Integer.bitCount(x ^ y) -> Bit difference count   |
| • Range DP 338   : DP[i] = DP[i >> 1] + (i & 1) -> O(N) Linear Time⚡  |
| • Performance    : Computes set bit counts up to 32x faster! ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Brian Kernighan's bit counter in Java.
- [ ] I can write LeetCode 338 (`Counting Bits`) DP array generator in $O(N)$ time.
- [ ] I can write LeetCode 461 (`Hamming Distance`) in 1 line of Java.
- [ ] I can explain why `DP[i >> 1] + (i & 1)` is mathematically valid.
- [ ] I can state why `Integer.bitCount` operates in $O(1)$ hardware time.
