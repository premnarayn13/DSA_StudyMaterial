# 13. Pattern Recognition & Bit Manipulation Triggers: 6 Master Archetypes

## 1. Introduction
High-speed problem solving in technical coding interviews requires instant **Bit Manipulation Pattern Recognition**. Rather than attempting to guess bitwise operators, masks, and loop bounds under pressure, experienced engineers map problem descriptions directly to one of **6 Universal Bit Manipulation Master Archetypes**: **Single Number & XOR Cancellation Archetype**, **Bit Masking & State Control Archetype**, **Bit Counting & Range Population Archetype**, **Power Verification Archetype**, **Gray Code Transition Archetype**, and **Sub-mask & Bitmask DP Archetype**. Identifying trigger words in problem statements allows immediate selection of optimal bitwise formulas, shift directions, and sub-mask loops.

> **Important:** The 6 Universal Bit Manipulation Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Single Number & XOR Cancellation**: Trigger = *"Find element appearing once where others appear pairs/triplets"*. Mechanics = Cumulative XOR or `diff & (-diff)` bit partitioning.
> 2. **Pattern 2: Bit Masking & State Control**: Trigger = *"Check, set, clear, toggle, or isolate lowest bit"*. Mechanics = `(1 << k)`, `x & (x - 1)`, `x & (-x)`.
> 3. **Pattern 3: Bit Counting & Range Population**: Trigger = *"Count set 1-bits in single integer or range 0..N"*. Mechanics = Brian Kernighan or `DP[i >> 1] + (i & 1)`.
> 4. **Pattern 4: Power Verification**: Trigger = *"Check if integer is power of 2, 3, or 4 in O(1) time"*. Mechanics = `(n & (n - 1)) == 0`, `1162261467 % n == 0`, `n & 0x55555555`.
> 5. **Pattern 5: Gray Code Transition**: Trigger = *"Sequence of 2^N integers differing by 1 bit"*. Mechanics = `i ^ (i >> 1)`.
> 6. **Pattern 6: Sub-mask & Bitmask DP**: Trigger = *"Iterate all sub-masks / Subset selection DP for N <= 20"*. Mechanics = `sub = (sub - 1) & mask`, `DP[mask][u]`. ⚡

```
Master Bit Manipulation Archetype Decision Flowchart:

Problem Trigger Signal:
├── "Find single unique element / pairs cancel?" ────► Pattern 1: Single Number & XOR (XOR Sum / diff & -diff)
├── "Check / set / clear / isolate lowest bit?" ─────► Pattern 2: Bit Masking (1<<k, x & (x-1), x & -x)
├── "Count set 1-bits in range 0..N in O(N) time?" ──► Pattern 3: Bit Counting (DP[i >> 1] + (i & 1))
├── "Check power of 2, 3, or 4 in O(1) time?" ──────► Pattern 4: Power Verification (n & (n-1)==0, 0x55555555)
├── "Sequence of 2^N integers differing by 1 bit?" ─► Pattern 5: Gray Code (i ^ (i >> 1))
└── "Iterate all sub-masks / Bitmask DP N <= 20?" ───► Pattern 6: Sub-mask & Bitmask DP (sub = (sub-1)&mask) ⚡
```

---

## 2. Core Concepts & Master Bit Manipulation Strategy Matrix

### 2.1 Master Bit Manipulation Pattern Recognition Matrix
```
Master Bit Manipulation Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Primary Formula   | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. Single Number**  | "Find unique element"| `diff & (-diff)`  | **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **2. Bit Masking**    | "State bit control"| `x & (x - 1)` / `x & (-x)`| **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **3. Bit Counting**   | "Count set bits"  | `DP[i>>1] + (i&1)`| **$O(N)$ Linear ⚡**| **$O(N)$ Array ⚡**|
| **4. Power Check**    | "Power of 2, 3, 4"| `(n & (n-1))==0`  | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **5. Gray Code**      | "1-bit difference"| `i ^ (i >> 1)`    | **$O(2^N)$ Linear ⚡**| **$O(2^N)$ Array ⚡**|
| **6. Bitmask DP**     | "Sub-masks / TSP" | `sub = (sub-1)&mask`| **$O(3^N)$ / $O(N^2 \cdot 2^N)$⚡**| **$O(2^N)$ Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Pattern 1 = XOR sum; Pattern 2 = x & (x-1) and x & (-x); Pattern 3 = DP[i >> 1] + (i & 1); Pattern 4 = n & (n-1)==0; Pattern 5 = i ^ (i >> 1); Pattern 6 = sub = (sub-1)&mask!"**

---

## 3. Deep Dive into the 6 Bit Manipulation Archetypes & LeetCode Audits

### 3.1 Auditing Top LeetCode Benchmark Problems
```
LeetCode Benchmark Problem Audits:

LeetCode 136 (Single Number I)           ──► Pattern 1: Single Number (Cumulative XOR Sum)
LeetCode 137 (Single Number II)          ──► Pattern 1: Single Number (Digital Logic ones & twos)
LeetCode 260 (Single Number III)         ──► Pattern 1: Single Number (Partition diff & (-diff))
LeetCode 268 (Missing Number)            ──► Pattern 1: Single Number (Index-Value XOR Sum)
LeetCode 191 (Number of 1 Bits)          ──► Pattern 2 & 3: Bit Masking & Counting (x & (x - 1))
LeetCode 231 (Power of Two)              ──► Pattern 4: Power Verification ((n > 0) && (n & (n - 1)) == 0)
LeetCode 326 (Power of Three)            ──► Pattern 4: Power Verification (1162261467 % n == 0)
LeetCode 342 (Power of Four)             ──► Pattern 4: Power Verification (n & 0x55555555 != 0)
LeetCode 461 (Hamming Distance)          ──► Pattern 3: Bit Counting (Integer.bitCount(x ^ y))
LeetCode 338 (Counting Bits Range 0..N)  ──► Pattern 3: Bit Counting (DP[i >> 1] + (i & 1))
LeetCode 89  (Gray Code Sequence)        ──► Pattern 5: Gray Code (res.add(i ^ (i >> 1)))
LeetCode 698 (Partition K Subsets)       ──► Pattern 6: Sub-mask DP (sub = (sub - 1) & mask)
LeetCode 1125 (Smallest Sufficient Team) ──► Pattern 6: Bitmask DP (DP[mask | skill])
```

---

## 4. Internal Working Mechanics: The 6 Master Pattern Code Templates

```java
// PATTERN 1: SINGLE NUMBER III (LeetCode 260)
int diff = 0; for (int num : nums) diff ^= num;
int isolatedBit = diff & (-diff); int x = 0, y = 0;
for (int num : nums) { if ((num & isolatedBit) != 0) x ^= num; else y ^= num; }

// PATTERN 2: BIT MASKING FORMULAS
int clearLowest = x & (x - 1); int isolateLowest = x & (-x); boolean isSet = ((x & (1 << k)) != 0);

// PATTERN 3: COUNTING BITS RANGE DP (LeetCode 338)
for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);

// PATTERN 4: POWER VERIFICATIONS (LeetCode 231, 326, 342)
boolean isPow2 = (n > 0 && (n & (n - 1)) == 0);
boolean isPow3 = (n > 0 && 1162261467 % n == 0);
boolean isPow4 = (n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0);

// PATTERN 5: GRAY CODE (LeetCode 89)
for (int i = 0; i < (1 << n); i++) res.add(i ^ (i >>> 1));

// PATTERN 6: SUB-MASK ITERATION LOOP
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) { ... }
```

---

## 5. Visual Diagram: The 6 Bit Manipulation Archetypes Map

```
                          [ Bit Manipulation Decision Engine ]
                                          │
                 ┌────────────────────────┴────────────────────────┐
                 ▼                                                 ▼
      [ Single Int Operations ]                           [ Array / Subset Operations ]
      /          │          \                             /          │          \
     ▼           ▼           ▼                           ▼           ▼           ▼
Pattern 2    Pattern 3   Pattern 4                   Pattern 1   Pattern 5   Pattern 6
(Bit Masking)(Bit Count)(Power Check)               (Single Num) (Gray Code) (Sub-mask DP)
x & (x-1)    DP[i>>1]+(i&1) (n&(n-1))==0            Cumulative XOR i^(i>>1) sub=(sub-1)&mask
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across the 6 Bit Manipulation Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating Reference Implementations
 * Across the 6 Universal Bit Manipulation Master Archetypes.
 */
public class BitManipulationPatternRecognitionMaster {

    // PATTERN 1: SINGLE NUMBER III (LeetCode 260)
    public int[] pattern1_SingleNumber3(int[] nums) {
        int diff = 0; for (int num : nums) diff ^= num;
        int isolatedBit = diff & (-diff);
        int x = 0, y = 0;
        for (int num : nums) {
            if ((num & isolatedBit) != 0) x ^= num; else y ^= num;
        }
        return new int[]{x, y};
    }

    // PATTERN 2: BIT MASKING FORMULAS
    public int pattern2_IsolateLowestBit(int x) { return x & (-x); }
    public int pattern2_ClearLowestBit(int x)   { return x & (x - 1); }

    // PATTERN 3: COUNTING BITS RANGE DP (LeetCode 338)
    public int[] pattern3_CountBits(int n) {
        int[] dp = new int[n + 1];
        for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1); // DP Recurrence ⚡
        return dp;
    }

    // PATTERN 4: POWER VERIFICATION (LeetCode 231, 326, 342)
    public boolean pattern4_IsPowerOfTwo(int n)  { return n > 0 && (n & (n - 1)) == 0; }
    public boolean pattern4_IsPowerOfThree(int n){ return n > 0 && 1162261467 % n == 0; }
    public boolean pattern4_IsPowerOfFour(int n) { return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0; }

    // PATTERN 5: GRAY CODE (LeetCode 89)
    public List<Integer> pattern5_GrayCode(int n) {
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < (1 << n); i++) res.add(i ^ (i >>> 1));
        return res;
    }

    // PATTERN 6: SUB-MASK ITERATION LOOP
    public List<Integer> pattern6_GetAllSubmasks(int mask) {
        List<Integer> subs = new ArrayList<>();
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) subs.add(sub);
        subs.add(0);
        return subs;
    }
}
```

> **Quick Syntax:**
```java
// Master Bit Manipulation Lines
int isolatedBit = diff & (-diff); dp[i] = dp[i >> 1] + (i & 1); res.add(i ^ (i >>> 1)); for (int sub = mask; sub > 0; sub = (sub - 1) & mask) ...
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Single Number)**: LeetCode 136, LeetCode 137, LeetCode 260, LeetCode 268.
* **Pattern 2 (Bit Masking)**: LeetCode 191, Fenwick Tree index updates.
* **Pattern 3 (Bit Counting)**: LeetCode 338, LeetCode 461.
* **Pattern 4 (Power Verification)**: LeetCode 231, LeetCode 326, LeetCode 342.
* **Pattern 5 (Gray Code)**: LeetCode 89.
* **Pattern 6 (Sub-mask & Bitmask DP)**: Held-Karp TSP, LeetCode 698, LeetCode 1125.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BitManipulationPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   6 MASTER BIT MANIPULATION ARCHETYPES DEMO     ");
        System.out.println("=================================================\n");

        BitManipulationPatternRecognitionMaster master = new BitManipulationPatternRecognitionMaster();

        // 1. Pattern 1 (Single Number III)
        int[] nums = {1, 2, 1, 3, 2, 5};
        System.out.println("1. Pattern 1 (Single Number III): " + Arrays.toString(master.pattern1_SingleNumber3(nums)));

        // 2. Pattern 3 (Counting Bits Range N=5)
        System.out.println("2. Pattern 3 (Counting Bits N=5): " + Arrays.toString(master.pattern3_CountBits(5)));

        // 3. Pattern 4 (Power Check 16)
        System.out.println("3. Pattern 4 (Is 16 Power of 4): " + master.pattern4_IsPowerOfFour(16));

        // 4. Pattern 5 (Gray Code N=2)
        System.out.println("4. Pattern 5 (Gray Code N=2): " + master.pattern5_GrayCode(2));

        // 5. Pattern 6 (Sub-masks of 11)
        System.out.println("5. Pattern 6 (Sub-masks of 11): " + master.pattern6_GetAllSubmasks(11));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Master Bit Manipulation Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Single Number**  | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| "Find single unique element" |
| **2. Bit Masking**    | $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| "Check/set/clear/isolate bit" |
| **3. Bit Counting**   | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Array ⚡| "Count set bits range 0..N" |
| **4. Power Check**    | $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| "Check power of 2, 3, or 4" |
| **5. Gray Code**      | $\mathbf{O(2^N)}$ Linear ⚡| $\mathbf{O(2^N)}$ Array ⚡| "Sequence differing by 1 bit" |
| **6. Bitmask DP**     | $\mathbf{O(3^N)}$ / $\mathbf{O(N^2 \cdot 2^N)}$⚡| $\mathbf{O(2^N)}$ Array ⚡| "Iterate all sub-masks / TSP" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Single Number I and Single Number III**:
   - 1 unique element $\to$ **Cumulative XOR sum**.
   - 2 unique elements $\to$ **Bit partitioning via `diff & (-diff)`**.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Omitting Positivity Guard in Power Checks**:
  - Writing `(n & (n - 1)) == 0` without checking `n > 0` returns `true` for `n = 0`, causing logical bugs. **ALWAYS check `n > 0 && ((n & (n - 1)) == 0)`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Bit Manipulation Selector Rule:
> 1. Single unique element? $\to$ Pattern 1 (Cumulative XOR / `diff & -diff`).
> 2. Isolate lowest 1-bit? $\to$ Pattern 2 (`x & (-x)`).
> 3. Count set bits range $0..N$? $\to$ Pattern 3 (`DP[i >> 1] + (i & 1)`).
> 4. Check Power of 2/3/4? $\to$ Pattern 4 (`(n & (n - 1)) == 0`, `1162261467 % n == 0`, `0x55555555`).
> 5. Gray Code sequence? $\to$ Pattern 5 (`i ^ (i >> 1)`).
> 6. Sub-mask iteration? $\to$ Pattern 6 (`sub = (sub - 1) & mask`). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Operation | Memory Footprint | Primary Optimization |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Single Num)** | Bitwise XOR (`^`) | **$O(1)$ Memory ⚡** | Eliminates HashSets |
| **Pattern 3 (Bit Counting)**| DP Recurrence | $O(N)$ Array | Eliminates $O(32)$ loop |
| **Pattern 6 (Sub-mask DP)**| Sub-mask AND | $O(2^N)$ DP Table | Eliminates $O(4^N)$ grid search |

---

## 14. How to Recognize This in Questions

* **"Count total set 1-bits for all numbers from 0 to N in O(N) time"** $\rightarrow$ Pattern 3 (LeetCode 338).
* **"Find 2 unique numbers appearing once"** $\rightarrow$ Pattern 1 (LeetCode 260).

---

## 15. Frequently Asked Interview Questions

* **Q: How do you choose between `x & (x - 1)` and `x & (-x)`?**  
  *A:* Use `x & (x - 1)` to CLEAR the lowest set bit (e.g. counting set bits, checking power of 2). Use `x & (-x)` to ISOLATE the lowest set bit (e.g. Fenwick Tree, Single Number III bit partitioning).

* **Q: What is the DP recurrence for LeetCode 338 Counting Bits?**  
  *A:* `DP[i] = DP[i >> 1] + (i & 1)`.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 6 MASTER BIT MANIPULATION ARCHETYPES                  |
+-----------------------------------------------------------------------+
| • Pattern 1: Single Number -> XOR sum / diff & (-diff) partitioning   |
| • Pattern 2: Bit Masking   -> x & (x - 1) clear / x & (-x) isolate    |
| • Pattern 3: Bit Counting  -> DP[i] = DP[i >> 1] + (i & 1)            |
| • Pattern 4: Power Check   -> (n > 0) && (n & (n - 1)) == 0           |
| • Pattern 5: Gray Code     -> res.add(i ^ (i >>> 1))                  |
| • Pattern 6: Sub-mask DP   -> for (int sub = mask; sub > 0; sub = (sub - 1) & mask)|
| • Performance : Executes in O(1) hardware CPU clock cycles! ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any bit manipulation problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I can write Single Number III (`diff & (-diff)`) in Java.
- [ ] I can write Counting Bits (`DP[i >> 1] + (i & 1)`) in Java.
- [ ] I can write all 3 Power Verification formulas (2, 3, 4).
- [ ] I can write the sub-mask iteration loop `sub = (sub - 1) & mask`.
