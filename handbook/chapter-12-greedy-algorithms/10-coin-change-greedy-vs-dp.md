# 10. Coin Change: Greedy vs Dynamic Programming & Canonical Coin Proofs

## 1. Introduction
The **Coin Change Problem** is a foundational decision-making benchmark that highlights the precise boundary between **Greedy Algorithmic Success** and **Greedy Algorithmic Failure**. Given a set of coin denominations $D = \{d_1, d_2 \dots d_N\}$ and a target amount $A$, the goal is to make change for $A$ using the **Minimum Number of Coins**. For **Canonical Currency Systems** (such as US or Euro denominations $\{1, 5, 10, 25, 50, 100\}$), a Greedy algorithm that repeatedly picks the largest coin $d_i \le A$ executes in **$O(N)$ Time Complexity** and **$O(1)$ Auxiliary Space**. However, for **Non-Canonical Systems** (such as $\{1, 3, 4\}$ for Target Amount $6$), the Greedy algorithm fails completely, requiring **Dynamic Programming (Unbounded Knapsack)** in **$O(N \cdot A)$ Time Complexity**.

> **Important:** Core Invariants of Coin Change Systems:
> 1. **Canonical Coin System Invariant**:
>    - A coin system is **Canonical** if for every target amount $A$, the Greedy choice (picking the largest coin $d_i \le A$) yields the optimal minimum number of coins.
>    - US/Euro coins are specifically engineered by central banks to be Canonical!
> 2. **Non-Canonical Failure Invariant**:
>    - A coin system is **Non-Canonical** if counter-examples exist where picking the largest coin forces sub-optimal extra coins.
>    - Example: Denominations $\{1, 3, 4\}$, Target Amount $= 6$:
>      - **Greedy Pick**: Takes $4$, remaining $2 \to$ Takes $1 + 1 \implies 3\text{ Coins } (4 + 1 + 1)$.
>      - **Optimal Choice (DP)**: Takes $3 + 3 \implies \mathbf{2\text{ Coins } (3 + 3)}$!
> 3. **Pearson's $O(N^3)$ Canonical System Verification Algorithm**:
>    - Checks whether a given set of coin denominations is canonical in polynomial time! ⚡

```
Coin Change Greedy Success vs Failure Topology:

Canonical System {1, 5, 10, 25}, Amount = 30:
Greedy: Pick 25 -> Rem 5 -> Pick 5 -> Total 2 Coins (25 + 5) ✅ (OPTIMAL!)

Non-Canonical System {1, 3, 4}, Amount = 6:
Greedy: Pick 4 -> Rem 2 -> Pick 1 -> Rem 1 -> Pick 1 -> Total 3 Coins (4 + 1 + 1) ❌ (SUB-OPTIMAL!)
DP Opt : Pick 3 -> Rem 3 -> Pick 3 --------------------> Total 2 Coins (3 + 3) ✅ (OPTIMAL!) ⚡
```

---

## 2. Core Concepts & Coin Change Strategy Matrix

### 2.1 Coin Change Strategy Matrix
```
Coin Change Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Coin System Type      | Target Amount $A$ | Optimal Algorithm | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Canonical System**  | Any Amount        | **Greedy Choice ⚡**| **$O(N)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Non-Canonical**     | Any Amount        | **Dynamic Prog ⚡**| $O(N \cdot A)$    | $O(A)$ DP Array   |
| **Arbitrary System**  | Unknown           | **Dynamic Prog ⚡**| $O(N \cdot A)$    | $O(A)$ DP Array   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Canonical coins (US/Euro) = Greedy O(N); Non-canonical or arbitrary coins = DP Unbounded Knapsack O(N * A)!"**

---

## 3. Characteristics & Pearson's Canonical Verification Mathematical Foundations

### 3.1 Mathematical Proof of Canonical Coin Conditions
* **Tight Counter-Example Theorem (Kozen & Zaks)**:
  - If a coin system $\{1, c_2, c_3 \dots c_N\}$ is NOT canonical, the smallest counter-example $A$ lies in the range:
    $$c_3 + 1 < A < c_N + c_{N-1}$$
* **Pearson's Verification Theorem**:
  - Pearson (1995) proved that verifying whether a coin system is canonical requires testing at most $O(N^3)$ candidate amounts $A$. If Greedy matches DP for all candidate test values in Pearson's set, the system is GUARANTEED to be Canonical! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step DP State Transitions

How DP solves Non-Canonical Coin Change ($D = \{1, 3, 4\}$, Target $A = 6$):

```
DP Table Definition: dp[amt] = Min coins required to make amount amt.
Base Case: dp[0] = 0, dp[1..6] = infinity.

State Transition: dp[amt] = min( dp[amt], 1 + dp[amt - coin] )

- amt = 1: dp[1] = 1 + dp[0] = 1 (Coin 1)
- amt = 2: dp[2] = 1 + dp[1] = 2 (Coin 1+1)
- amt = 3: dp[3] = min( 1+dp[2]=3, 1+dp[0]=1 ) = 1 (Coin 3)
- amt = 4: dp[4] = min( 1+dp[3]=2, 1+dp[1]=2, 1+dp[0]=1 ) = 1 (Coin 4)
- amt = 5: dp[5] = min( 1+dp[4]=2, 1+dp[2]=3, 1+dp[1]=2 ) = 2 (Coin 4+1 or 3+2)
- amt = 6: dp[6] = min( 1+dp[5]=3, 1+dp[3]=2, 1+dp[2]=3 ) = 2! (Coin 3+3)

DP finds optimal 2 coins (3 + 3) where Greedy failed! ✅
```

---

## 5. Visual Diagram: Greedy Path vs DP State Graph

```
Amount A = 6 over Denominations {1, 3, 4}:

Greedy Path (Sub-optimal):
(6) ─── Pick 4 ───► (2) ─── Pick 1 ───► (1) ─── Pick 1 ───► (0) [3 Coins] ❌

DP Optimal State Path:
(6) ─── Pick 3 ───► (3) ─── Pick 3 ───► (0)                     [2 Coins] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Greedy Coin Change for Canonical Systems, LeetCode 322 (Coin Change DP), and Pearson's Canonical System Verification.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Coin Change Algorithms:
 * Greedy Choice for Canonical Systems, DP Unbounded Knapsack for Arbitrary Systems,
 * and System Verification.
 */
public class CoinChangeMaster {

    // =========================================================================
    // 1. GREEDY COIN CHANGE (CANONICAL SYSTEMS O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves Coin Change using Greedy Choice (FOR CANONICAL COIN SYSTEMS ONLY).
     *
     * @param coins coin denominations (e.g. {1, 5, 10, 25})
     * @param amount target amount A
     * @return list of selected coins, or empty list if impossible
     */
    public List<Integer> solveGreedyCanonical(int[] coins, int amount) {
        List<Integer> selected = new ArrayList<>();
        if (coins == null || coins.length == 0 || amount <= 0) return selected;

        // Sort coins descending
        int[] sortedCoins = coins.clone();
        Arrays.sort(sortedCoins);

        int currentAmount = amount;

        for (int i = sortedCoins.length - 1; i >= 0; i--) {
            int coin = sortedCoins[i];
            while (currentAmount >= coin) {
                selected.add(coin);
                currentAmount -= coin; // Greedy choice! ⚡
            }
        }

        if (currentAmount != 0) return new ArrayList<>(); // Impossible
        return selected;
    }

    // =========================================================================
    // 2. LEETCODE 322: COIN CHANGE DYNAMIC PROGRAMMING (O(N * A) Time)
    // =========================================================================
    /**
     * Solves Coin Change for ANY arbitrary coin system using Dynamic Programming.
     * LeetCode 322 Solution.
     */
    public int coinChangeDP(int[] coins, int amount) {
        if (coins == null || amount < 0) return -1;
        if (amount == 0) return 0;

        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1); // Sentinel for infinity
        dp[0] = 0;

        for (int amt = 1; amt <= amount; amt++) {
            for (int coin : coins) {
                if (amt - coin >= 0) {
                    dp[amt] = Math.min(dp[amt], 1 + dp[amt - coin]);
                }
            }
        }

        return (dp[amount] > amount) ? -1 : dp[amount];
    }

    // =========================================================================
    // 3. CANONICAL SYSTEM VERIFICATION ENGINE (O(N^3) Time)
    // =========================================================================
    /**
     * Verifies if a given coin system is Canonical (Greedy ALWAYS equals DP).
     */
    public boolean isCanonicalSystem(int[] coins, int testMaxAmount) {
        for (int amt = 1; amt <= testMaxAmount; amt++) {
            List<Integer> greedyResult = solveGreedyCanonical(coins, amt);
            int greedyCount = greedyResult.isEmpty() ? Integer.MAX_VALUE : greedyResult.size();
            int dpCount = coinChangeDP(coins, amt);

            if (greedyCount != dpCount) {
                System.out.println("Counter-Example Found! Amount = " + amt + 
                                   ": Greedy = " + greedyCount + " Coins, DP = " + dpCount + " Coins");
                return false; // System is NOT Canonical! ⚡
            }
        }
        return true;
    }
}
```

> **Quick Syntax:**
```java
// Coin Change DP State Line
if (amt - coin >= 0) dp[amt] = Math.min(dp[amt], 1 + dp[amt - coin]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 322 - Coin Change**:
   - Primary DP Unbounded Knapsack benchmark problem ($O(N \cdot A)$ time).

2. **Automated Vending Machine & ATM Cash Dispensers**:
   - ATMs dispense currency notes using Greedy choice over Canonical currency sets ($100, 50, 20, 10$).

3. **Cryptocurrency & Token Micro-Payments**:
   - Calculating minimal token transactions for custom non-canonical tokens via DP.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class CoinChangeDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   COIN CHANGE: GREEDY VS DP DEMONSTRATION      ");
        System.out.println("=================================================\n");

        CoinChangeMaster master = new CoinChangeMaster();

        // 1. Canonical US Coins Test (Greedy Succeeds)
        int[] usCoins = {1, 5, 10, 25};
        int target1 = 30;
        List<Integer> greedyUs = master.solveGreedyCanonical(usCoins, target1);
        int dpUs = master.coinChangeDP(usCoins, target1);

        System.out.println("1. Canonical System {1, 5, 10, 25}, Target Amount = " + target1 + ":");
        System.out.println("   Greedy Selected Coins: " + greedyUs + " (" + greedyUs.size() + " Coins)");
        System.out.println("   DP Minimum Coins     : " + dpUs + " Coins");
        System.out.println("   Greedy Matches DP    : " + (greedyUs.size() == dpUs) + " (OPTIMAL ✅)");
        System.out.println("-------------------------------------------------");

        // 2. Non-Canonical System Test (Greedy Fails)
        int[] nonCanonical = {1, 3, 4};
        int target2 = 6;
        List<Integer> greedyNon = master.solveGreedyCanonical(nonCanonical, target2);
        int dpNon = master.coinChangeDP(nonCanonical, target2);

        System.out.println("2. Non-Canonical System {1, 3, 4}, Target Amount = " + target2 + ":");
        System.out.println("   Greedy Selected Coins: " + greedyNon + " (" + greedyNon.size() + " Coins)");
        System.out.println("   DP Minimum Coins     : " + dpNon + " Coins");
        System.out.println("   Greedy Fails!        : " + (greedyNon.size() != dpNon) + " (DP = 3+3 = 2 Coins! ✅)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Coin Change Approach | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | System Suitability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Greedy Choice**   | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| **Canonical Coins ONLY ✅**|
| **Dynamic Prog (DP)**| $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(N \cdot A)}$ ⚡| $O(A)$ DP Array | **Arbitrary Coins ✅**|

---

## 10. Edge Cases & Boundary Handling

1. **Target Amount 0**:
   - `coinChangeDP` returns 0 immediately.

2. **Amount Cannot Be Formed (`dp[amount] == infinity`)**:
   - `coinChangeDP` returns `-1`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Greedy Coin Change to Arbitrary Interview Problems**:
  - Assuming Greedy works for any coin array given in LeetCode 322 causes wrong answers on non-canonical test cases. **ALWAYS use Dynamic Programming for arbitrary coin arrays!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Use Greedy vs DP for Coin Change:
> * **Use Greedy**: ONLY if explicitly stated that coins form a **Canonical System** (e.g. US/Euro currency).
> * **Use Dynamic Programming**: For ALL general LeetCode / interview coin change problems! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Greedy Coin Change | Dynamic Programming (DP) |
| :--- | :--- | :--- |
| **Correctness Guarantee** | Conditional (Canonical Only) | **100% Universal Guarantee ⚡** |
| **Time Complexity** | **Fast $O(N)$ ⚡** | $O(N \cdot A)$ |
| **Auxiliary Memory** | **$O(1)$ In-Place ⚡** | $O(A)$ Array |

---

## 14. How to Recognize This in Questions

* **"Find minimum coins to make amount A for arbitrary coin array"** $\rightarrow$ LeetCode 322 (DP).
* **"Dispense change for US dollar notes"** $\rightarrow$ Greedy Choice.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Canonical Coin System?**  
  *A:* A coin denomination system for which the Greedy choice (picking the largest coin $\le A$) is guaranteed to yield the minimum number of coins for every target amount $A$.

* **Q: Give a counter-example where Greedy coin change fails.**  
  *A:* Denominations $\{1, 3, 4\}$, Target Amount $= 6$. Greedy picks $4 + 1 + 1$ (3 coins), whereas optimal is $3 + 3$ (2 coins).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COIN CHANGE (GREEDY VS DP)                            |
+-----------------------------------------------------------------------+
| • Canonical Coins: US/Euro {1,5,10,25} -> Greedy works in O(N) time ⚡ |
| • Counter-Example: {1, 3, 4} for Amt 6 -> Greedy 4+1+1 (3), DP 3+3 (2)|
| • LeetCode 322   : ALWAYS use DP! dp[amt] = min(dp[amt], 1+dp[amt-c]) |
| • Performance    : Greedy O(N) Time | DP O(N * A) Time ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Greedy Coin Change for Canonical Systems in Java.
- [ ] I can solve LeetCode 322 (`Coin Change`) using Dynamic Programming in $O(N \cdot A)$ time.
- [ ] I can state a non-canonical counter-example ($\{1, 3, 4\}$ for Amount $6$).
- [ ] I can explain Pearson's Canonical System Verification concept.
- [ ] I can state when to choose Greedy vs DP for Coin Change.
