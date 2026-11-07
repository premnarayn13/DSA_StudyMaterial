# 09. Bitmask Enumeration: Sub-mask Iteration & Gosper's Hack

## 1. Introduction
**Bitmask Enumeration** is a advanced bit-manipulation discipline focused on efficiently iterating through candidate subset combinations represented as integer bit vectors. Two major mathematical bit tricks govern bitmask enumeration:
1. **Sub-mask Enumeration (`sub = (sub - 1) & mask`)**: Iterates through **ALL SUB-MASKS** of a given `mask` integer. Iterating sub-masks over ALL $2^N$ masks takes **$O(3^N)$ Time Complexity** instead of the naive $O(4^N)$ grid search time!
2. **Gosper's Hack**: Generates all bitmasks containing **EXACTLY $K$ SET BITS** in strict lexicographical order in **$O(1)$ Time per State**, bypassing the need to generate and test all $2^N$ masks.

> **Important:** The 2 Master Bitmask Enumeration Formulas:
> 1. **Sub-mask Iteration Loop**:
>    ```java
>    for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
>        // Process valid sub-mask of mask! ⚡
>    }
>    ```
> 2. **Gosper's Hack (Fixed Size $K$ Bitmask Generator)**:
>    ```java
>    int c = mask & -mask; // Isolate lowest set bit
>    int r = mask + c;     // Add lowest bit to mask
>    mask = (((r ^ mask) >> 2) / c) | r; // Next lexicographical K-bit mask! ⚡
>    ```
> 3. **Total Sub-mask Iteration Complexity Proof**:
>    $$\sum_{k=0}^N \binom{N}{k} 2^k = (1 + 2)^N = 3^N$$
>    Iterating all sub-masks across all masks takes $3^N$ operations instead of naive $4^N$! ⚡

```
Sub-mask Enumeration Traversal Topology (mask = 1011_2 = Decimal 11):

Initial mask: 1011_2 (Bits 0, 1, 3 set)

Sub-mask Iterations (sub = (sub - 1) & mask):
1. sub = 1011_2 (11)  ──► Base mask
2. sub = 1010_2 (10)  ──► Bits 1, 3 set
3. sub = 1001_2 (9)   ──► Bits 0, 3 set
4. sub = 1000_2 (8)   ──► Bit 3 set
5. sub = 0011_2 (3)   ──► Bits 0, 1 set
6. sub = 0010_2 (2)   ──► Bit 1 set
7. sub = 0001_2 (1)   ──► Bit 0 set
Loop terminates when sub == 0!

Iterates all 2^3 = 8 sub-masks without visiting non-matching masks! ⚡
```

---

## 2. Core Concepts & Enumeration Strategy Matrix

### 2.1 Bitmask Enumeration Strategy Matrix
```
Bitmask Enumeration Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Enumeration Goal      | Bitwise Formula   | Primary Mechanism | Total Operations  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Sub-masks of Mask** | `sub = (sub-1)&mask`| Bit Borrow & AND | $2^k$ Sub-masks   | **$O(2^k)$ Fast ⚡**|
| **Sub-masks All Masks**| Double Loop      | Binomial Expansion| $3^N$ Total       | **$O(3^N)$ vs $O(4^N)$⚡**|
| **Fixed K-Bit Masks** | **Gosper's Hack ⚡**| Bit Shift-XOR     | $\binom{N}{K}$ States| **$O(1)$ per state⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sub-mask loop: sub = (sub - 1) & mask; Gosper's Hack generates next K-bit mask in O(1) time!"**

---

## 3. Characteristics & $O(3^N)$ Sub-mask Sum Proof

### 3.1 Mathematical Proof of $O(3^N)$ All Sub-mask Iterations
* Consider $N$ items. We wish to iterate over all possible masks, and for each mask, iterate over all of its sub-masks.
* A mask with $k$ set bits has exactly $2^k$ sub-masks.
* The total number of masks with $k$ set bits is given by the binomial coefficient $\binom{N}{k}$.
* **Total Operations Count**:
  $$T(N) = \sum_{k=0}^N \binom{N}{k} 2^k$$
* By the **Binomial Theorem** ($(a + b)^N = \sum_{k=0}^N \binom{N}{k} a^{N-k} b^k$), setting $a = 1$ and $b = 2$:
  $$T(N) = (1 + 2)^N = 3^N$$
* **Comparison**:
  - Naive double loop over all mask pairs: $2^N \times 2^N = 4^N$.
  - Sub-mask loop `sub = (sub - 1) & mask`: $3^N$.
  - For $N = 15$: $4^{15} \approx 1.07 \times 10^9$ ops (Slow!) vs $3^{15} = 1.43 \times 10^7$ ops (**Over 75x FASTER!**). ⚡

---

## 4. Internal Working Mechanics: Gosper's Hack Step-by-Step

Tracing Gosper's Hack for $K = 2$ set bits on 4-bit integers ($N=4, K=2$):

```
Goal: Generate all 4-bit masks with K = 2 set bits (0011, 0101, 0110, 1001, 1010, 1100).

Initial mask: mask = 0011_2 (Decimal 3).

Iteration 1:
1. c = mask & -mask = 0011 & 1101 = 0001_2 (Lowest set bit).
2. r = mask + c = 0011 + 0001 = 0100_2.
3. mask = (((r ^ mask) >> 2) / c) | r
        = (((0100 ^ 0011) >> 2) / 1) | 0100
        = ((0111 >> 2) / 1) | 0100 = 0001 | 0100 = 0101_2 (Decimal 5!).

Iteration 2: Next mask = 0110_2 (Decimal 6!).
Iteration 3: Next mask = 1001_2 (Decimal 9!).
Iteration 4: Next mask = 1010_2 (Decimal 10!).
Iteration 5: Next mask = 1100_2 (Decimal 12!).

Generates all C(4,2) = 6 combinations in O(1) time per state! ✅ ⚡
```

---

## 5. Visual Diagram: Gosper's Hack State Transition

```
Gosper's Hack Bit Shift Mechanics:

Current Mask:  0 1 0 1 1 0 0 0  (Bits 3, 4, 6 set)
                     ▲
            Lowest Set Bit c = 00001000

r = mask + c:  0 1 1 0 0 0 0 0  (Bit carry propagates up!)

New Mask:      0 1 1 0 0 0 1 1  (Next lexicographical K-bit mask!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Sub-mask Iteration Loop, $O(3^N)$ Sub-mask Aggregator, and Gosper's Hack Fixed $K$-Bitmask Generator.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bitmask Enumeration:
 * Sub-mask Iteration Loops, O(3^N) Binomial Aggregators, and Gosper's Hack.
 */
public class BitmaskEnumerationMaster {

    // =========================================================================
    // 1. SUB-MASK ITERATION LOOP (sub = (sub - 1) & mask)
    // =========================================================================
    /**
     * Finds all sub-masks of a given mask integer.
     *
     * @param mask target mask
     * @return list of all sub-masks
     */
    public List<Integer> getAllSubmasks(int mask) {
        List<Integer> submasks = new ArrayList<>();
        if (mask <= 0) return submasks;

        // SUB-MASK ITERATION LOOP ⚡
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
            submasks.add(sub);
        }
        submasks.add(0); // Add empty set 0

        return submasks;
    }

    // =========================================================================
    // 2. GOSPER'S HACK (FIXED K-BITMASK GENERATOR O(1) PER STATE)
    // =========================================================================
    /**
     * Generates all N-bit integers with exactly K set bits using Gosper's Hack.
     *
     * @param n total bit length
     * @param k target number of set bits
     * @return list of generated K-bit masks
     */
    public List<Integer> gospersHack(int n, int k) {
        List<Integer> result = new ArrayList<>();
        if (k <= 0 || n <= 0 || k > n) return result;

        int mask = (1 << k) - 1; // Initial smallest K-bit mask (e.g. 0011 for K=2) ⚡
        int limit = 1 << n;

        while (mask < limit) {
            result.add(mask);

            // GOSPER'S HACK FORMULA LINES ⚡
            int c = mask & -mask;                // Isolate lowest set bit
            int r = mask + c;                    // Add c to mask
            if (r == 0) break; // Avoid overflow
            mask = (((r ^ mask) >> 2) / c) | r; // Calculate next K-bit mask! ⚡
        }

        return result;
    }

    // =========================================================================
    // 3. ALL MASK SUB-MASK TOTAL COUNTER (O(3^N) Complexity Proof)
    // =========================================================================
    public long countAllSubmaskPairs(int n) {
        long totalPairs = 0;
        int maxMask = 1 << n;

        for (int mask = 0; mask < maxMask; mask++) {
            for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
                totalPairs++;
            }
            totalPairs++; // Include sub = 0
        }

        return totalPairs; // Exactly 3^N! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Sub-mask & Gosper's Hack Lines
for (int sub = mask; sub > 0; sub = (sub - 1) & mask) ...
int c = mask & -mask, r = mask + c; mask = (((r ^ mask) >> 2) / c) | r;
```

---

## 7. Concrete Problem Examples & Applications

1. **Sub-mask Iteration (`sub = (sub - 1) & mask`)**:
   - Sub-mask dynamic programming (e.g. Partition to K Subsets LeetCode 698).

2. **Gosper's Hack**:
   - Generating $K$-combinations of $N$ items in $O(1)$ time per state ($O(\binom{N}{K})$ total time).

3. **Bitmask Set Covering Problems**:
   - Aggregating costs over all subset combinations.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class BitmaskEnumerationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BITMASK ENUMERATION BENCHMARK DEMO            ");
        System.out.println("=================================================\n");

        BitmaskEnumerationMaster master = new BitmaskEnumerationMaster();

        // 1. Sub-mask Iteration Test (mask = 11 = 1011_2)
        int mask = 11;
        List<Integer> submasks = master.getAllSubmasks(mask);
        System.out.println("1. Sub-mask Iteration for mask = 11 (1011_2):");
        System.out.println("   Total Sub-masks Generated: " + submasks.size() + " (2^3 = 8)");
        System.out.println("   Sub-masks = " + submasks);
        System.out.println("-------------------------------------------------");

        // 2. Gosper's Hack Test (N = 4, K = 2)
        int n = 4, k = 2;
        List<Integer> kBitmasks = master.gospersHack(n, k);
        System.out.println("2. Gosper's Hack K-Bitmask Generator (N = 4, K = 2):");
        System.out.println("   Total Masks Generated: " + kBitmasks.size() + " (C(4,2) = 6)");
        System.out.println("   K-Bit Masks = " + kBitmasks);
        System.out.println("-------------------------------------------------");

        // 3. O(3^N) Verification (N = 4)
        long pairs = master.countAllSubmaskPairs(4);
        System.out.println("3. All Sub-mask Pairs Verification for N = 4:");
        System.out.println("   Total Pairs Counted: " + pairs + " (3^4 = 81)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bitmask Enumeration Task | Formula | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Sub-mask Iteration** | `sub = (sub - 1) & mask` | $\mathbf{O(2^k)}$ Sub-masks ⚡| $\mathbf{O(1)}$ Memory ⚡| Bit borrow & AND |
| **All Sub-masks Iteration**| Double Loop | $\mathbf{O(3^N)}$ Binomial ⚡| $\mathbf{O(1)}$ Memory ⚡| $(1 + 2)^N = 3^N$ |
| **Gosper's Hack** | Bit Shift-XOR | $\mathbf{O(1)}$ per State ⚡| $\mathbf{O(1)}$ Memory ⚡| Fixed $K$ set bits |

---

## 10. Edge Cases & Boundary Handling

1. **Sub-mask Loop `sub = 0`**:
   - The condition `sub > 0` terminates the loop before `sub = -1`, avoiding infinite loops. `sub = 0` must be handled explicitly after the loop.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Naive Sub-mask Checking (`for sub = 0 ... mask`)**:
  - Checking every integer from 0 to `mask` takes $O(\text{mask}) = O(2^N)$ time per mask, resulting in $O(4^N)$ total operations. **ALWAYS use `sub = (sub - 1) & mask` to achieve $O(3^N)$ time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Bitmask Enumeration Rules:
> 1. To iterate all sub-masks of a mask: `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)`.
> 2. To generate $K$-set-bit masks: Use **Gosper's Hack**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive Double Loop ($4^N$) | Sub-mask Loop (`sub = (sub-1)&mask`) |
| :--- | :--- | :--- |
| **Total Operations** | $2^N \times 2^N = 4^N$ | **Binomial Expansion $3^N$ ⚡** |
| **Speedup (N=15)** | ~1.07 Billion Ops | **~14.3 Million Ops (75x Faster!) ⚡** |
| **Validity** | Evaluates non-sub-masks | **Evaluates ONLY valid sub-masks ⚡** |

---

## 14. How to Recognize This in Questions

* **"Iterate all sub-masks for subset dynamic programming"** $\rightarrow$ `sub = (sub - 1) & mask`.
* **"Generate all combinations of size K using bitmasks"** $\rightarrow$ Gosper's Hack.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does `sub = (sub - 1) & mask` iterate through all valid sub-masks?**  
  *A:* Subtracting 1 borrows from the lowest set bit of `sub` and sets all lower bits to 1. Bitwise ANDing with `mask` strips away all 1-bits that are not present in `mask`, leaving the next smaller valid sub-mask.

* **Q: Why is iterating all sub-masks across all masks $O(3^N)$ instead of $O(4^N)$?**  
  *A:* Because a mask with $k$ set bits has $2^k$ sub-masks. Summing $\binom{N}{k} 2^k$ over $k = 0 \dots N$ equals $(1 + 2)^N = 3^N$ by the Binomial Theorem.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BITMASK ENUMERATION                                   |
+-----------------------------------------------------------------------+
| • Sub-mask Loop : for (int sub = mask; sub > 0; sub = (sub - 1) & mask)⚡|
| • All Sub-masks : O(3^N) Total Time vs O(4^N) Naive Search            |
| • Gosper's Hack : c = mask & -mask; r = mask + c;                     |
|                   mask = (((r ^ mask) >> 2) / c) | r                  |
| • Gosper Speed  : Generates fixed K-bit masks in O(1) time per state ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the sub-mask iteration loop `sub = (sub - 1) & mask` in Java.
- [ ] I can write Gosper's Hack for fixed $K$-bitmask generation in Java.
- [ ] I can prove why iterating all sub-masks takes $O(3^N)$ time.
- [ ] I can explain how `(sub - 1) & mask` borrows bits correctly.
- [ ] I can state why Gosper's Hack operates in $O(1)$ time per state.
