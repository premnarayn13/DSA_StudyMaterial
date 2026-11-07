# 07. Coin Change Pattern: Unbounded Knapsack, Combinations vs Permutations & Forward 1D DP

## 1. Introduction
The **Coin Change Pattern** is the central design archetype derived from **Unbounded Knapsack**, where items (coins) can be reused an **infinite number of times** ($x_i \in \mathbb{Z}_{\ge 0}$). Given $N$ coin denominations $C = \{c_1, c_2 \dots c_N\}$ and a target amount $A$, the Coin Change pattern addresses three fundamental operational questions:
1. **Minimum Coins Optimization (LeetCode 322)**: Find the minimum number of coins needed to make change for amount $A$ ($DP[amt] = \min(DP[amt], 1 + DP[amt - c])$).
2. **Combination Counts (LeetCode 518 - Coin Change II)**: Find total distinct combinations of coins that sum to amount $A$ (order does NOT matter, e.g. $\{1, 2\}$ is identical to $\{2, 1\}$).
3. **Permutation Counts (LeetCode 377 - Combination Sum IV)**: Find total distinct ordered sequences of coins that sum to amount $A$ (order DOES matter, e.g. $(1, 2)$ is distinct from $(2, 1)$).

By utilizing **Forward 1D Space Compression** ($w = c_i \dots A$), Coin Change algorithms execute in **$O(N \cdot A)$ Time Complexity** and **$O(A)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of the Coin Change Pattern:
> 1. **Forward 1D Space Compression Invariant**:
>    - Because coins can be reused infinitely, capacity/amount MUST be iterated **FORWARD (Left-to-Right from $c_i$ up to $A$)**:
>      $$DP[amt] = \text{op}\left( DP[amt], \, DP[amt - c_i] \right)$$
>    - Forward iteration allows updated state $DP[amt - c_i]$ to be reused immediately in the same pass!
> 2. **Combinations Loop Order Invariant (LeetCode 518)**:
>    - **Outer Loop = Coins, Inner Loop = Amounts**:
>      Processing coin-by-coin guarantees that coins are considered in strict fixed order, counting ONLY **Unordered Combinations**!
> 3. **Permutations Loop Order Invariant (LeetCode 377)**:
>    - **Outer Loop = Amounts, Inner Loop = Coins**:
>      Processing amount-by-amount allows any coin to be placed at any position, counting ALL **Ordered Permutations**! ⚡

```
Combinations vs Permutations Loop Topology:

Combination Loop Order (LeetCode 518 - Order Does Not Matter):
for (int coin : coins) {
    for (int amt = coin; amt <= target; amt++) {
        dp[amt] += dp[amt - coin];  ──► Outer Coin Loop = UNORDERED COMBINATIONS! ⚡
    }
}

Permutation Loop Order (LeetCode 377 - Order Matters):
for (int amt = 1; amt <= target; amt++) {
    for (int coin : coins) {
        if (amt >= coin) dp[amt] += dp[amt - coin];  ──► Outer Amount Loop = ORDERED PERMUTATIONS! ⚡
    }
}
```

---

## 2. Core Concepts & Coin Change Strategy Matrix

### 2.1 Coin Change Variants Comparison Matrix
```
Coin Change Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Target Metric     | Outer Loop        | Recurrence Equation| Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Min Coins (LC 322)**| Minimum Count     | Either            | $\min(dp[a], 1 + dp[a-c])$| **$O(A)$ 1D Array ⚡**|
| **Combinations (518)**| Unique Combinations| **Coins $c$ ⚡**   | $dp[a] += dp[a - c]$| **$O(A)$ 1D Array ⚡**|
| **Permutations (377)**| Ordered Sequences | **Amounts $a$ ⚡** | $dp[a] += dp[a - c]$| **$O(A)$ 1D Array ⚡**|
| **Unbounded Knap**    | Max Value         | Items             | $\max(v_i + dp[w-w_i], dp[w])$| **$O(W)$ 1D Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Outer loop COINS = Unordered Combinations (518); Outer loop AMOUNTS = Ordered Permutations (377)!"**

---

## 3. Characteristics & Loop Order Mathematical Proof

### 3.1 Mathematical Proof of Combinations vs Permutations Loop Order
* Let $C = \{1, 2\}$ and Target $A = 3$. Total combinations $= 1$ ($\{1, 1, 1\}$ and $\{1, 2\}$). Total permutations $= 3$ ($(1, 1, 1), (1, 2), (2, 1)$).
* **Case 1: Outer Loop = Coins (Combinations)**:
  - Iteration 1 (Coin 1): Computes all ways using ONLY coin 1. $DP[3]$ gets ways using $\{1, 1, 1\}$.
  - Iteration 2 (Coin 2): Adds coin 2 to existing states. $\{1, 2\}$ is added once.
  - Since coin 2 is never evaluated BEFORE coin 1, sequence $(2, 1)$ CANNOT be formed. Yields **Unordered Combinations**!
* **Case 2: Outer Loop = Amounts (Permutations)**:
  - At Amount $a=3$, the inner loop considers coin 1 (appending to $a=2$) AND coin 2 (appending to $a=1$).
  - Sequence $(1, 2)$ (coin 2 after 1) AND $(2, 1)$ (coin 1 after 2) are BOTH generated independently. Yields **Ordered Permutations**! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Execution Dry Run

Tracing Coin Change II (LeetCode 518) for $Coins = [1, 2, 5]$, Target $A = 5$:

```
Init: dp[0] = 1, dp[1..5] = 0.

Outer Loop 1 (Coin = 1):
amt=1: dp[1] += dp[0] -> dp[1] = 1
amt=2: dp[2] += dp[1] -> dp[2] = 1
amt=3: dp[3] += dp[2] -> dp[3] = 1
amt=4: dp[4] += dp[3] -> dp[4] = 1
amt=5: dp[5] += dp[4] -> dp[5] = 1  (Array after coin 1: [1, 1, 1, 1, 1, 1])

Outer Loop 2 (Coin = 2):
amt=2: dp[2] += dp[0] -> dp[2] = 1 + 1 = 2 ({1,1}, {2})
amt=3: dp[3] += dp[1] -> dp[3] = 1 + 1 = 2 ({1,1,1}, {1,2})
amt=4: dp[4] += dp[2] -> dp[4] = 1 + 2 = 3 ({1,1,1,1}, {1,1,2}, {2,2})
amt=5: dp[5] += dp[3] -> dp[5] = 1 + 2 = 3 ({1,1,1,1,1}, {1,1,1,2}, {1,2,2})

Outer Loop 3 (Coin = 5):
amt=5: dp[5] += dp[0] -> dp[5] = 3 + 1 = 4! ({5})

Final Total Combinations = 4! ({1,1,1,1,1}, {1,1,1,2}, {1,2,2}, {5}) ✅ ⚡
```

---

## 5. Visual Diagram: Forward 1D Space Compression Shift

```
Forward 1D DP Capacity Array Updating (Unbounded Re-use):

Array dp[amt]:  [ dp[0] | dp[1] | ... | dp[amt - c] | ... | dp[A] ]
                                            │               │
                                            └─ Forward Update ──► Reads newly updated state!
                                               Allows coin c to be reused infinitely! ⚡

Reverse Loop (W down to w_i) ──► 0/1 Knapsack (Single-use item)
Forward Loop (w_i up to W)   ──► Unbounded Knapsack (Infinite-use coin!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Minimum Coins (LeetCode 322), Coin Change II Combinations (LeetCode 518), Combination Sum IV Permutations (LeetCode 377), and Unbounded Knapsack.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Coin Change Pattern,
 * Unbounded Knapsack, Combinations vs Permutations, and Forward 1D Space Compression.
 */
public class CoinChangePatternMaster {

    // =========================================================================
    // 1. LEETCODE 322: MINIMUM COINS (O(N * A) Time, O(A) Space)
    // =========================================================================
    /**
     * Calculates minimum coins needed to make change for amount A.
     *
     * @param coins coin denominations
     * @param amount target amount A
     * @return minimum coin count, or -1 if impossible
     */
    public int coinChangeMin(int[] coins, int amount) {
        if (coins == null || amount < 0) return -1;
        if (amount == 0) return 0;

        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1); // Sentinel for infinity
        dp[0] = 0; // Base case: 0 coins for amount 0

        for (int coin : coins) {
            // FORWARD LOOP for Unbounded Re-use
            for (int amt = coin; amt <= amount; amt++) {
                dp[amt] = Math.min(dp[amt], 1 + dp[amt - coin]);
            }
        }

        return (dp[amount] > amount) ? -1 : dp[amount];
    }

    // =========================================================================
    // 2. LEETCODE 518: COIN CHANGE II - COMBINATIONS (O(N * A) Time, O(A) Space)
    // =========================================================================
    /**
     * Calculates total UNORDERED COMBINATIONS of coins summing to amount A.
     * Rule: Outer Loop = COINS!
     */
    public int changeCombinations(int amount, int[] coins) {
        if (coins == null || amount < 0) return 0;

        int[] dp = new int[amount + 1];
        dp[0] = 1; // Base case: 1 way to form 0 amount (empty set)

        // OUTER LOOP = COINS (Guarantees Unordered Combinations!) ⚡
        for (int coin : coins) {
            for (int amt = coin; amt <= amount; amt++) {
                dp[amt] += dp[amt - coin];
            }
        }

        return dp[amount];
    }

    // =========================================================================
    // 3. LEETCODE 377: COMBINATION SUM IV - PERMUTATIONS (O(N * A) Time)
    // =========================================================================
    /**
     * Calculates total ORDERED PERMUTATIONS of numbers summing to target.
     * Rule: Outer Loop = AMOUNTS!
     */
    public int combinationSum4Permutations(int[] nums, int target) {
        if (nums == null || target <= 0) return 0;

        int[] dp = new int[target + 1];
        dp[0] = 1; // Base case: 1 way to form 0 target

        // OUTER LOOP = AMOUNTS (Generates All Ordered Permutations!) ⚡
        for (int amt = 1; amt <= target; amt++) {
            for (int num : nums) {
                if (amt >= num) {
                    dp[amt] += dp[amt - num];
                }
            }
        }

        return dp[target];
    }

    // =========================================================================
    // 4. UNBOUNDED KNAPSACK STANDARD PATTERN (O(N * W) Time, O(W) Space)
    // =========================================================================
    /**
     * Solves Unbounded Knapsack where items can be reused infinitely.
     */
    public int solveUnboundedKnapsack(int[] weights, int[] values, int capacity) {
        if (weights == null || values == null || capacity <= 0) return 0;

        int n = weights.length;
        int[] dp = new int[capacity + 1];

        for (int i = 0; i < n; i++) {
            int w_i = weights[i];
            int v_i = values[i];

            // FORWARD LOOP for Unbounded Item Re-use! ⚡
            for (int w = w_i; w <= capacity; w++) {
                dp[w] = Math.max(dp[w], v_i + dp[w - w_i]);
            }
        }

        return dp[capacity];
    }
}
```

> **Quick Syntax:**
```java
// Combinations vs Permutations Loop Order Lines
// Combinations (518): for (int c : coins) for (int a = c; a <= A; a++) dp[a] += dp[a - c];
// Permutations (377): for (int a = 1; a <= A; a++) for (int c : coins) if (a >= c) dp[a] += dp[a - c];
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 322 - Coin Change**:
   - Minimum coins required to form target amount ($O(N \cdot A)$ time, $O(A)$ space).

2. **LeetCode 518 - Coin Change II**:
   - Total unordered coin combinations ($O(N \cdot A)$ time, outer coin loop).

3. **LeetCode 377 - Combination Sum IV**:
   - Total ordered coin permutations ($O(N \cdot A)$ time, outer amount loop).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class CoinChangePatternDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   COIN CHANGE & UNBOUNDED KNAPSACK DEMO         ");
        System.out.println("=================================================\n");

        CoinChangePatternMaster master = new CoinChangePatternMaster();

        int[] coins = {1, 2, 5};
        int target = 5;

        // 1. Min Coins Test (LeetCode 322)
        int minCoins = master.coinChangeMin(coins, target);
        System.out.println("1. LeetCode 322 Minimum Coins for Target " + target + ": " + minCoins + " Coins (Coin 5)");
        System.out.println("-------------------------------------------------");

        // 2. Combinations Test (LeetCode 518)
        int combinations = master.changeCombinations(target, coins);
        System.out.println("2. LeetCode 518 Coin Combinations (Outer Loop = Coins):");
        System.out.println("   Total Unordered Combinations: " + combinations + " ({1,1,1,1,1}, {1,1,1,2}, {1,2,2}, {5})");
        System.out.println("-------------------------------------------------");

        // 3. Permutations Test (LeetCode 377)
        int permutations = master.combinationSum4Permutations(coins, target);
        System.out.println("3. LeetCode 377 Combination Sum IV (Outer Loop = Amounts):");
        System.out.println("   Total Ordered Permutations  : " + permutations + " Permutations");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Coin Change Archetype | Time Complexity | Auxiliary Space | Outer Loop Field | Output Type |
| :--- | :--- | :--- | :--- | :--- |
| **Min Coins (LC 322)** | $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| Coins or Amounts | Minimum Count |
| **Combinations (518)**| $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| **Coins $c$ ⚡** | Unordered Combinations |
| **Permutations (377)**| $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| **Amounts $a$ ⚡** | Ordered Permutations |
| **Unbounded Knapsack**| $\mathbf{O(N \cdot W)}$ ⚡| $\mathbf{O(W)}$ 1D Array ⚡| Items $i$ | Maximum Value |

---

## 10. Edge Cases & Boundary Handling

1. **Target Amount 0**:
   - `dp[0] = 1` for combination counting, `dp[0] = 0` for min coins.

2. **No Solution Possible**:
   - `coinChangeMin` returns `-1`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Reversing Loop Order in Coin Change II (LeetCode 518)**:
  - Putting the amounts loop on the outside in LeetCode 518 generates ordered permutations instead of unordered combinations, causing overcounting errors! **ALWAYS put Coins on the outside for Combinations!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 1D Loop Direction & Outer Loop Order Rules:
> * **0/1 Knapsack**: Capacity loop $w$ goes **BACKWARDS ($W \to w_i$)**.
> * **Unbounded Knapsack / Coin Change**: Capacity loop $w$ goes **FORWARD ($w_i \to W$)**.
> * **Unordered Combinations**: Outer loop = **COINS**.
> * **Ordered Permutations**: Outer loop = **AMOUNTS**. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Combinations (LC 518) | Permutations (LC 377) |
| :--- | :--- | :--- |
| **Sequence $(1, 2)$ vs $(2, 1)$** | Counted ONCE (Identical) | Counted TWICE (Distinct) |
| **Outer Loop** | **Coins `c` ⚡** | **Amounts `a` ⚡** |
| **1D Array Traversal** | Forward ($c \to A$) | Forward ($c \to A$) |

---

## 14. How to Recognize This in Questions

* **"Find total unique ways to make amount A using coin denominations (order does not matter)"** $\rightarrow$ LeetCode 518 (Outer loop Coins).
* **"Find total ordered sequences that sum to target"** $\rightarrow$ LeetCode 377 (Outer loop Amounts).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does iterating coins in the outer loop produce unordered combinations?**  
  *A:* Because each coin denomination is processed to completion before the next coin is considered, guaranteeing that coins appear in non-decreasing index order, which excludes different ordering permutations.

* **Q: Why does Unbounded Knapsack use a forward 1D loop instead of reverse?**  
  *A:* Forward iteration updates $DP[w - w_i]$ in the current step, allowing the same item to be reused multiple times.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COIN CHANGE PATTERN                                   |
+-----------------------------------------------------------------------+
| • Unbounded 1D Loop: MUST iterate FORWARD from c_i up to A            |
| • Combinations 518 : Outer Loop = COINS   -> Unordered Combinations ⚡|
| • Permutations 377 : Outer Loop = AMOUNTS -> Ordered Permutations   ⚡|
| • Min Coins 322    : dp[amt] = min(dp[amt], 1 + dp[amt - c])          |
| • Performance      : O(N * A) Time | O(A) Auxiliary 1D Space ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 322 (`Coin Change`) in $O(N \cdot A)$ time and $O(A)$ space.
- [ ] I can write LeetCode 518 (`Coin Change II Combinations`) with outer coin loop.
- [ ] I can write LeetCode 377 (`Combination Sum IV Permutations`) with outer amount loop.
- [ ] I can explain why forward 1D iteration enables infinite item re-use.
- [ ] I can prove why outer coin loop prevents duplicate permutation counting.
