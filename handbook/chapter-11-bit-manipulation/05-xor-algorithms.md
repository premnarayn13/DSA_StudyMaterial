# 05. XOR Algorithms: Single Number I, II, III & Bit Group Partitioning

## 1. Introduction
The **Bitwise XOR Operator (`^`)** possesses unique mathematical invariants that make it the premier tool for solving element cancellation, missing number identification, and frequency partition problems in linear time ($O(N)$) and zero auxiliary space ($O(1)$). XOR operations operate under three foundational properties: (1) **Commutative & Associative Invariant** ($A \oplus B = B \oplus A$), (2) **Identity Invariant** ($A \oplus 0 = A$), and (3) **Self-Inverse Cancellation Invariant** ($A \oplus A = 0$). Famous algorithmic applications include **Single Number I (LeetCode 136)**, **Single Number II (LeetCode 137)** (elements appear 3 times), **Single Number III (LeetCode 260)** (2 unique numbers isolated via `diff & (-diff)`), and **Missing Number (LeetCode 268)**.

> **Important:** Core Structural Invariants of XOR Algorithms:
> 1. **Single Number I Invariant (LeetCode 136)**:
>    - Cumulative XORing all elements yields the single unique element:
>      $$\text{totalXOR} = a_1 \oplus a_1 \oplus a_2 \oplus a_2 \dots \oplus X = 0 \oplus 0 \dots \oplus X = X$$
> 2. **Single Number II Digital Logic Gates (LeetCode 137)**:
>    - Tracks bit counts modulo 3 using two 32-bit variables `ones` and `twos`:
>      $$\text{ones} = (\text{ones} \oplus \text{num}) \;\&\; \sim\text{twos} \quad \text{and} \quad \text{twos} = (\text{twos} \oplus \text{num}) \;\&\; \sim\text{ones}$$
> 3. **Single Number III Partitioning Invariant (LeetCode 260)**:
>    - Total XOR of all elements yields $\text{diff} = X \oplus Y$.
>    - Isolate the rightmost set 1-bit in `diff`: `isolatedBit = diff & (-diff)`.
>    - Partition all numbers into two groups based on whether `(num & isolatedBit) != 0`.
>    - XORing each group independently isolates $X$ and $Y$ in $O(N)$ time and $O(1)$ space! ⚡

```
Single Number III Bit Partitioning Topology (Find X=3, Y=5 in [1, 2, 1, 3, 2, 5]):

Total XOR diff = 3 ^ 5 = (011_2) ^ (101_2) = 110_2 (Decimal 6).

Isolate Lowest Bit: isolatedBit = diff & (-diff) = 6 & -6 = 010_2 (Decimal 2 - Bit 1!).

Group 1 (Bit 1 IS SET):   [ 3 (011), 2 (010), 2 (010) ] ──► Cumulative XOR = 3! ✅
Group 2 (Bit 1 IS CLEAR): [ 1 (001), 1 (001), 5 (101) ] ──► Cumulative XOR = 5! ✅

Partitions array into 2 disjoint groups, isolating both unique numbers X and Y! ⚡
```

---

## 2. Core Concepts & XOR Algorithms Strategy Matrix

### 2.1 XOR Algorithms Family Strategy Matrix
```
XOR Algorithms Family Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Element Frequency | Primary Mechanism | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Single Number I (136)**| Pairs (2x) + 1 | Cumulative XOR    | **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Single Number II (137)**| Triplets (3x) + 1| Digital Logic Mod 3| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Single Number III (260)**| Pairs + 2 Unique| Bit Partition `diff & (-diff)`| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Missing Number (268)**| Range $0 \dots N$| Index-Value XOR   | **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Single Number I = cumulative XOR; Single Number III = total XOR -> isolate bit = diff & (-diff) -> partition 2 groups!"**

---

## 3. Characteristics & Single Number III Mathematical Proof

### 3.1 Mathematical Proof of Single Number III Bit Partitioning
* Let array contain pairs of numbers plus two distinct unique numbers $X$ and $Y$ ($X \neq Y$).
* Cumulative XOR of all array elements yields:
  $$\text{diff} = X \oplus Y$$
* Since $X \neq Y$, $\text{diff} \neq 0$. Therefore, $\text{diff}$ contains at least one set 1-bit.
* Let $p$ be the position of the lowest set bit in $\text{diff}$, extracted via $\text{bit} = \text{diff} \& (-\text{diff})$.
* **Meaning of Bit $p$ in $X \oplus Y$**:
  - Bit $p$ is 1 in $X \oplus Y$ if and ONLY if $X$ and $Y$ differ at bit position $p$!
  - One number (say $X$) has bit $p = 1$, while the other number ($Y$) has bit $p = 0$.
* **Partitioning Guarantee**:
  - For all paired numbers $A, A$: both copies of $A$ have the exact same bit $p$. They will BOTH end up in Group 1 OR BOTH end up in Group 2.
  - In Group 1 (numbers with bit $p = 1$), all paired numbers cancel out ($A \oplus A = 0$), leaving ONLY $X$.
  - In Group 2 (numbers with bit $p = 0$), all paired numbers cancel out, leaving ONLY $Y$.
  - Isolates both unique values in $O(N)$ time and $O(1)$ space! ⚡

---

## 4. Internal Working Mechanics: Single Number II Digital Logic

Tracing Single Number II for elements appearing 3 times (LeetCode 137):

```
Digital Logic Gate Equations (Bit Counts Modulo 3):

ones = (ones ^ num) & ~twos;
twos = (twos ^ num) & ~ones;

State Transitions per Bit Count:
- Initial State : ones = 0, twos = 0 (Count = 0 mod 3)
- First Arrival : ones = 1, twos = 0 (Count = 1 mod 3)
- Second Arrival: ones = 0, twos = 1 (Count = 2 mod 3)
- Third Arrival : ones = 0, twos = 0 (Count = 0 mod 3 - Resets!)

Final Result = `ones` holds bits of the single number appearing ONCE! ✅ ⚡
```

---

## 5. Visual Diagram: Single Number III Execution Flow

```
Single Number III Bit Partition Flow:

Input Array: [ 1, 2, 1, 3, 2, 5 ]
                     │
         Calculate Total XOR diff
                     │
          diff = 3 ^ 5 = 110_2
                     │
       Isolate Lowest Bit diff & (-diff)
                     │
          isolatedBit = 010_2
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
Group 1 (Bit 1 IS SET)    Group 2 (Bit 1 IS CLEAR)
[ 3, 2, 2 ]               [ 1, 1, 5 ]
      │                             │
XOR Result = 3! ✅          XOR Result = 5! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Single Number I (LeetCode 136), Single Number II (LeetCode 137), Single Number III (LeetCode 260), and Missing Number (LeetCode 268).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing XOR Algorithms:
 * Single Number I, Single Number II (Digital Logic Mod 3), Single Number III (Bit Partitioning), and Missing Number.
 */
public class XORAlgorithmsMaster {

    // =========================================================================
    // 1. LEETCODE 136: SINGLE NUMBER I (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds single unique element where all other elements appear TWICE.
     */
    public int singleNumber1(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int xorSum = 0;
        for (int num : nums) {
            xorSum ^= num; // A ^ A = 0 cancellation! ⚡
        }
        return xorSum;
    }

    // =========================================================================
    // 2. LEETCODE 137: SINGLE NUMBER II (ELEMENTS APPEAR 3 TIMES)
    // =========================================================================
    /**
     * Finds single unique element where all other elements appear THREE TIMES.
     */
    public int singleNumber2(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int ones = 0, twos = 0;

        for (int num : nums) {
            ones = (ones ^ num) & ~twos; // Track bits appearing 1 time ⚡
            twos = (twos ^ num) & ~ones; // Track bits appearing 2 times ⚡
        }

        return ones;
    }

    // =========================================================================
    // 3. LEETCODE 260: SINGLE NUMBER III (2 UNIQUE NUMBERS O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds two unique elements where all other elements appear TWICE.
     */
    public int[] singleNumber3(int[] nums) {
        if (nums == null || nums.length < 2) return new int[0];

        // Step 1: Cumulative XOR of all elements -> diff = X ^ Y ⚡
        int diff = 0;
        for (int num : nums) {
            diff ^= num;
        }

        // Step 2: Isolate the lowest set bit in diff ⚡
        // Note: Using (diff & -diff) isolates rightmost 1-bit
        int isolatedBit = diff & (-diff);

        // Step 3: Partition elements into 2 groups based on isolatedBit
        int x = 0, y = 0;
        for (int num : nums) {
            if ((num & isolatedBit) != 0) {
                x ^= num; // Group 1 (Bit is set)
            } else {
                y ^= num; // Group 2 (Bit is clear)
            }
        }

        return new int[]{x, y};
    }

    // =========================================================================
    // 4. LEETCODE 268: MISSING NUMBER (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds missing number in array containing N distinct numbers in range 0 ... N.
     */
    public int missingNumber(int[] nums) {
        if (nums == null) return 0;
        int n = nums.length;
        int xorSum = n;

        for (int i = 0; i < n; i++) {
            xorSum ^= i ^ nums[i]; // XOR index i with nums[i] ⚡
        }

        return xorSum;
    }
}
```

> **Quick Syntax:**
```java
// Single Number III Partitioning Lines
int diff = 0; for (int num : nums) diff ^= num;
int isolatedBit = diff & (-diff);
if ((num & isolatedBit) != 0) x ^= num; else y ^= num;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 136 - Single Number I**:
   - Element cancellation benchmark ($O(N)$ time, $O(1)$ space).

2. **LeetCode 260 - Single Number III**:
   - Two unique numbers isolation benchmark using `diff & (-diff)`.

3. **LeetCode 268 - Missing Number**:
   - Finding missing range index using cumulative XORing.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class XORAlgorithmsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   XOR ALGORITHMS BENCHMARK DEMO                 ");
        System.out.println("=================================================\n");

        XORAlgorithmsMaster master = new XORAlgorithmsMaster();

        // 1. Single Number I Test (LeetCode 136)
        int[] nums1 = {4, 1, 2, 1, 2};
        int single1 = master.singleNumber1(nums1);
        System.out.println("1. LeetCode 136 Single Number I for [4, 1, 2, 1, 2]:");
        System.out.println("   Single Unique Number: " + single1 + " (Optimal = 4)");
        System.out.println("-------------------------------------------------");

        // 2. Single Number II Test (LeetCode 137)
        int[] nums2 = {2, 2, 3, 2};
        int single2 = master.singleNumber2(nums2);
        System.out.println("2. LeetCode 137 Single Number II (3x Trips) for [2, 2, 3, 2]:");
        System.out.println("   Single Unique Number: " + single2 + " (Optimal = 3)");
        System.out.println("-------------------------------------------------");

        // 3. Single Number III Test (LeetCode 260)
        int[] nums3 = {1, 2, 1, 3, 2, 5};
        int[] pair = master.singleNumber3(nums3);
        System.out.println("3. LeetCode 260 Single Number III for [1, 2, 1, 3, 2, 5]:");
        System.out.println("   Two Unique Numbers: " + Arrays.toString(pair) + " (Optimal = [3, 5])");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| XOR Algorithm | Target Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Single Number I (136)**| Pairs (2x) + 1 | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Cumulative XOR `a ^ a = 0` |
| **Single Number II (137)**| Triplets (3x) + 1| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Logic gates `ones`, `twos` |
| **Single Number III (260)**| Pairs + 2 Unique| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| **Bit partition `diff & (-diff)`⚡**|
| **Missing Number (268)**| Range $0 \dots N$ | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Index-value XOR |

---

## 10. Edge Cases & Boundary Handling

1. **Negative Integers in Array**:
   - Bitwise XOR algorithms work identically on negative Two's Complement integers without modification.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using HashSets or Sorting for Single Number Problems**:
  - Using a HashSet takes $O(N)$ auxiliary space; sorting takes $O(N \log N)$ time. **ALWAYS use Bitwise XOR to achieve $O(N)$ time and $O(1)$ space!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Single Number III Partitioning Rule:
> To isolate 2 unique numbers $X$ and $Y$ from an array of pairs, compute total XOR $\text{diff} = X \oplus Y$, extract `isolatedBit = diff & (-diff)`, and partition elements into two groups based on whether `(num & isolatedBit) != 0`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | HashSet Approach | Bitwise XOR Approach |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ Linear | **$O(N)$ Linear ⚡** |
| **Space Complexity** | $O(N)$ Memory Hash Table | **$O(1)$ Strict Zero Auxiliary Memory ⚡** |
| **Cache Locality** | Poor Pointer Chasing | **Optimal Sequential Array Access ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find element appearing once where all other elements appear twice"** $\rightarrow$ LeetCode 136.
* **"Find TWO elements appearing once where all other elements appear twice"** $\rightarrow$ LeetCode 260.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does cumulative XORing all elements find the single unique number in LeetCode 136?**  
  *A:* Because XOR is commutative and associative ($A \oplus B = B \oplus A$), and $A \oplus A = 0$. All duplicate pairs cancel out to 0, leaving $0 \oplus X = X$.

* **Q: How does `diff & (-diff)` help separate two unique numbers in LeetCode 260?**  
  *A:* `diff & (-diff)` isolates a bit position where $X$ and $Y$ differ (one number has bit 1, the other has bit 0). Partitioning array elements by this bit separates $X$ and $Y$ into disjoint groups, allowing each to be isolated via XORing.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: XOR ALGORITHMS                                        |
+-----------------------------------------------------------------------+
| • Single Num I 136 : Cumulative XOR all nums -> A ^ A = 0 cancels pairs|
| • Single Num II 137: Digital logic ones = (ones^num)&~twos; twos = ...|
| • Single Num III 260: diff = X^Y -> isolatedBit = diff & (-diff) ->   |
|                      Partition array by (num & isolatedBit) != 0      |
| • Missing Num 268  : Cumulative XOR indices and values -> xorSum ^= i^nums[i]|
| • Performance      : O(N) Time | O(1) Auxiliary Memory Footprint! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 136 (`Single Number I`) in $O(N)$ time and $O(1)$ space.
- [ ] I can write LeetCode 137 (`Single Number II`) using `ones` and `twos` logic gates.
- [ ] I can write LeetCode 260 (`Single Number III`) using bit partitioning `diff & (-diff)`.
- [ ] I can write LeetCode 268 (`Missing Number`) using index XORing.
- [ ] I can explain why `diff & (-diff)` separates $X$ and $Y$ into disjoint groups.
