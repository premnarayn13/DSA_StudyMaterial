# 11. Interval DP & Game Theory: Minimax Games, Stone Merging & 3-Parameter States

## 1. Introduction
**Interval Dynamic Programming & Game Theory DP** generalizes sequence partition problems to handle adversarial zero-sum games, multi-pile merging, and complex 3-parameter interval states. In Game Theory Interval DP (such as **Predict the Winner / Stone Game - LeetCode 486**), two optimal players take turns selecting items from either end of an interval $[i \dots j]$. Subproblems model the relative score difference achievable by the current player:
$$DP[i][j] = \max\left( \text{nums}[i] - DP[i+1][j], \; \text{nums}[j] - DP[i][j-1] \right)$$
In **Minimum Cost to Merge Stones (LeetCode 1000)**, $N$ piles of stones are merged in contiguous groups of size $K$. When interval states depend on external contiguous counts (such as **Remove Boxes - LeetCode 546**), standard 2D interval DP is extended to a 3-parameter state $DP[i][j][k]$ (where $k$ represents identical color elements preceding index $i$). Interval DP algorithms execute in **$O(N^3)$ to $O(N^4)$ Time Complexity** and **$O(N^2)$ to $O(N^3)$ Space**.

> **Important:** Core Structural Invariants of Interval DP & Game Theory:
> 1. **Minimax Score Difference Invariant (LeetCode 486)**:
>    - $DP[i][j]$ represents the **Maximum Relative Score Lead** the CURRENT player can obtain over the opponent from interval $[i \dots j]$.
>    - Subtracting $DP[i+1][j]$ handles the opponent's optimal play in the subsequent turn!
> 2. **K-Pile Merge Feasibility Condition (LeetCode 1000)**:
>    - $N$ piles can be merged into 1 pile in steps of size $K$ if and only if:
>      $$(N - 1) \pmod{K - 1} == 0$$
> 3. **3-Parameter State Invariant (Remove Boxes - LeetCode 546)**:
>    - $DP[i][j][k]$ = Maximum score clearing subarray $[i \dots j]$ given $k$ extra boxes matching `boxes[i]` attached to its left! ⚡

```
Predict the Winner Minimax Decision Topology (Interval [i ... j]):

                     [ State DP[i][j] ] (Current Player Turn)
                            /         \
                           /           \
  (Pick Left Element nums[i])         (Pick Right Element nums[j])
                         /               \
                        ▼                 ▼
          nums[i] - DP[i+1][j]       nums[j] - DP[i][j-1]

DP[i][j] = max( nums[i] - DP[i+1][j], nums[j] - DP[i][j-1] ) ⚡
```

---

## 2. Core Concepts & Interval DP Strategy Matrix

### 2.1 Interval DP Strategy Matrix
```
Interval DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | State Representation| Transition Recurrence| Time Complexity| Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Predict Winner (486)**| Relative score $[i..j]$| $\max(A[i] - dp[i+1][j], A[j] - dp[i][j-1])$| **$O(N^2)$ Quadratic⚡**| **$O(N)$ 1D Array ⚡**|
| **Merge Stones (1000)**| Min cost $[i..j][m]$| Split $m$ piles at $k$| **$O(N^3 \cdot K)$ ⚡**| $O(N^2 \cdot K)$ Table|
| **Remove Boxes (546)**| Max points $[i..j][k]$| Attach left count $k$| **$O(N^4)$ ⚡**     | $O(N^3)$ 3D Array |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Minimax Game DP = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1]); Merge Stones feasibility = (N-1) % (K-1) == 0!"**

---

## 3. Characteristics & Minimax Relative Score Mathematical Proof

### 3.1 Mathematical Derivation of Minimax Game State Invariant (Stone Game)
* Two players $A$ and $B$ play zero-sum game on array $A[0 \dots N-1]$. Player $A$ goes first.
* Let $S_A$ be total points picked by Player $A$, and $S_B$ be total points picked by Player $B$. Player $A$ wins if $S_A \ge S_B \iff S_A - S_B \ge 0$.
* Let $DP[i][j]$ be the maximum relative point advantage $(S_{\text{current}} - S_{\text{opponent}})$ for the player whose turn it is on subarray $[i \dots j]$.
* **Choices for Current Player**:
  1. **Pick Left $A[i]$**: Player gains $A[i]$ points. Subarray becomes $[i+1 \dots j]$. The opponent now faces subarray $[i+1 \dots j]$ with relative advantage $DP[i+1][j] = (S_{\text{opponent}} - S_{\text{current}})$.
     Relative advantage gained by picking $A[i]$:
     $$A[i] - DP[i+1][j]$$
  2. **Pick Right $A[j]$**: Relative advantage gained by picking $A[j]$:
     $$A[j] - DP[i][j-1]$$
* Recurrence Equation:
  $$DP[i][j] = \max\left( A[i] - DP[i+1][j], \; A[j] - DP[i][j-1] \right)$$
* Base Cases: $DP[i][i] = A[i]$ (single element interval).
* Player $A$ wins if $DP[0][N-1] \ge 0$! Solved in **$O(N^2)$ Time and $O(N)$ Space**! ⚡

---

## 4. Internal Working Mechanics: Remove Boxes 3-Parameter State Reduction

Tracing LeetCode 546 (Remove Boxes - $DP[i][j][k]$):

```
State Definition: dp[i][j][k] = Max points clearing boxes[i..j] with k extra boxes matching boxes[i] to its left.

Option 1: Clear boxes[i] together with the k matching boxes immediately:
Points = (k + 1)^2 + dp[i + 1][j][0]

Option 2: Don't clear boxes[i] now! Look for matching box boxes[m] == boxes[i] in range (i+1 .. j):
Combine the (k + 1) matching boxes with boxes[m]!
Points = dp[i + 1][m - 1][0] + dp[m][j][k + 1]

Take maximum over Option 1 and all valid splits m in Option 2!
Solved in O(N^4) Time via Top-Down Memoization! ✅ ⚡
```

---

## 5. Visual Diagram: Minimax Relative Advantage Shift

```
Turn-by-Turn Minimax Advantage Reduction:

Player A Turn on [i ... j]:
- Chooses Left A[i] ──► Leaves Opponent B facing [i+1 ... j]
- Net Relative Lead = A[i] - (B's Optimal Lead on [i+1 ... j])

Player B Turn on [i+1 ... j]:
- Chooses Right A[j] ──► Leaves Player A facing [i+1 ... j-1]
- Net Relative Lead = A[j] - (A's Optimal Lead on [i+1 ... j-1])

Evaluates diagonally over window length L = 1..N! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Predict the Winner / Stone Game (LeetCode 486), Minimum Cost to Merge Stones (LeetCode 1000), and Remove Boxes 3-Parameter DP (LeetCode 546).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Interval DP & Game Theory Algorithms:
 * Minimax Predict the Winner, K-Pile Stone Merging, and 3-Parameter Remove Boxes.
 */
public class IntervalDPProblemsMaster {

    // =========================================================================
    // 1. LEETCODE 486: PREDICT THE WINNER / STONE GAME (O(N^2) Time, O(N) Space)
    // =========================================================================
    /**
     * Determines if Player 1 can win the game picking from ends of array.
     *
     * @param nums array of game scores
     * @return true if Player 1 score >= Player 2 score
     */
    public boolean predictTheWinner(int[] nums) {
        if (nums == null || nums.length == 0) return true;
        int n = nums.length;

        int[] dp = new int[n];

        // Base case: window length L = 1
        for (int i = 0; i < n; i++) dp[i] = nums[i];

        // Window length L from 2 up to n
        for (int L = 2; L <= n; L++) {
            for (int i = 0; i <= n - L; i++) {
                int j = i + L - 1;

                // Minimax choice: max(Pick Left - opp, Pick Right - opp) ⚡
                dp[i] = Math.max(nums[i] - dp[i + 1], nums[j] - dp[i]);
            }
        }

        return dp[0] >= 0;
    }

    // =========================================================================
    // 2. LEETCODE 1000: MINIMUM COST TO MERGE STONES (O(N^3 * K) Time)
    // =========================================================================
    /**
     * Calculates min cost to merge N stone piles into 1 pile in groups of K.
     */
    public int mergeStones(int[] stones, int k) {
        if (stones == null || stones.length == 0) return 0;
        int n = stones.length;

        // K-pile feasibility check invariant
        if ((n - 1) % (k - 1) != 0) return -1;

        // Prefix sum array for range sum O(1) queries
        int[] prefix = new int[n + 1];
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + stones[i];

        int[][][] dp = new int[n][n][k + 1];
        for (int[][] row : dp) for (int[] col : row) Arrays.fill(col, Integer.MAX_VALUE / 2);

        for (int i = 0; i < n; i++) dp[i][i][1] = 0; // 1 pile requires 0 cost

        for (int L = 2; L <= n; L++) {
            for (int i = 0; i <= n - L; i++) {
                int j = i + L - 1;

                for (int m = 2; m <= k; m++) {
                    for (int p = i; p < j; p += k - 1) {
                        dp[i][j][m] = Math.min(dp[i][j][m], dp[i][p][1] + dp[p + 1][j][m - 1]);
                    }
                }

                // If m piles can be merged into 1 pile
                dp[i][j][1] = dp[i][j][k] + (prefix[j + 1] - prefix[i]);
            }
        }

        return dp[0][n - 1][1];
    }

    // =========================================================================
    // 3. LEETCODE 546: REMOVE BOXES (3-PARAMETER DP O(N^4) Time, O(N^3) Space)
    // =========================================================================
    /**
     * Calculates maximum points removing box groups with 3-parameter memoization.
     */
    public int removeBoxes(int[] boxes) {
        if (boxes == null || boxes.length == 0) return 0;
        int n = boxes.length;
        int[][][] memo = new int[n][n][n];

        return removeBoxesMemo(boxes, 0, n - 1, 0, memo);
    }

    private int removeBoxesMemo(int[] boxes, int i, int j, int k, int[][][] memo) {
        if (i > j) return 0;
        if (memo[i][j][k] != 0) return memo[i][j][k];

        // Compress consecutive identical boxes to the left of i
        int originalI = i, originalK = k;
        while (i + 1 <= j && boxes[i] == boxes[i + 1]) {
            i++;
            k++;
        }

        // Option 1: Remove boxes[i] and all k matching boxes directly
        int res = (k + 1) * (k + 1) + removeBoxesMemo(boxes, i + 1, j, 0, memo);

        // Option 2: Combine with matching box m in range (i+1 .. j)
        for (int m = i + 1; m <= j; m++) {
            if (boxes[m] == boxes[i]) {
                int points = removeBoxesMemo(boxes, i + 1, m - 1, 0, memo) +
                             removeBoxesMemo(boxes, m, j, k + 1, memo);
                res = Math.max(res, points);
            }
        }

        memo[originalI][j][originalK] = res;
        return res;
    }
}
```

> **Quick Syntax:**
```java
// Predict Winner Minimax Transition Line
dp[i] = Math.max(nums[i] - dp[i + 1], nums[j] - dp[i]); // Left vs Right choice
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 486 - Predict the Winner**:
   - Minimax game theory benchmark solved in $O(N^2)$ time and $O(N)$ space.

2. **LeetCode 1000 - Minimum Cost to Merge Stones**:
   - Multi-pile stone merging benchmark ($O(N^3 \cdot K)$ time).

3. **LeetCode 546 - Remove Boxes**:
   - Advanced 3-parameter interval DP ($O(N^4)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class IntervalDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   INTERVAL DP & GAME THEORY BENCHMARK DEMO      ");
        System.out.println("=================================================\n");

        IntervalDPProblemsMaster master = new IntervalDPProblemsMaster();

        // 1. Predict the Winner Test (LeetCode 486)
        int[] gameScores = {1, 5, 233, 7};
        boolean p1Wins = master.predictTheWinner(gameScores);
        System.out.println("1. LeetCode 486 Predict the Winner for Scores [1, 5, 233, 7]:");
        System.out.println("   Player 1 Can Win (Minimax DP): " + p1Wins + " (Optimal)");
        System.out.println("-------------------------------------------------");

        // 2. Merge Stones Test (LeetCode 1000)
        int[] stones = {3, 2, 4, 1};
        int k = 2;
        int minCost = master.mergeStones(stones, k);
        System.out.println("2. LeetCode 1000 Merge Stones for [3, 2, 4, 1], K = " + k + ":");
        System.out.println("   Minimum Merge Cost: " + minCost + " Cost (Optimal = 20)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Interval DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Predict Winner (486)**| $\mathbf{O(N^2)}$ Quadratic⚡| $\mathbf{O(N)}$ 1D Array ⚡| Minimax $\max(A[i]-dp, A[j]-dp)$ |
| **Merge Stones (1000)** | $\mathbf{O(N^3 \cdot K)}$ ⚡| $O(N^2 \cdot K)$ Table | Feasibility $(N-1) \% (K-1) == 0$ |
| **Remove Boxes (546)**  | $\mathbf{O(N^4)}$ ⚡| $O(N^3)$ 3D Array | 3-Parameter state $DP[i][j][k]$ |

---

## 10. Edge Cases & Boundary Handling

1. **Feasibility Check in Merge Stones**:
   - `(N - 1) % (K - 1) != 0` returns `-1` immediately (impossible to reduce to 1 pile).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Opponent Subtraction in Game DP**:
  - Writing `dp[i][j] = max(nums[i] + dp[i+1][j], nums[j] + dp[i][j-1])` ignores that the opponent gets to play next, leading to wrong answers. ALWAYS subtract the opponent's relative lead!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Minimax Game Theory Rule:
> In zero-sum sequential 2-player games, state $DP[i][j]$ represents the **relative score difference** $(S_{\text{current}} - S_{\text{opponent}})$. Subtracting the next state reflects the opponent's optimal counter-play! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | 2D Interval DP | 3D Interval DP (Remove Boxes) |
| :--- | :--- | :--- |
| **State Parameters** | $[i \dots j]$ (2 Parameters) | $[i \dots j][k]$ (3 Parameters) |
| **Time Complexity** | **$O(N^2)$ / $O(N^3)$ ⚡** | $O(N^4)$ |
| **Space Complexity** | **$O(N)$ / $O(N^2)$ ⚡** | $O(N^3)$ 3D Table |

---

## 14. How to Recognize This in Questions

* **"Two players take turns picking numbers from ends of array"** $\rightarrow$ LeetCode 486 (Minimax DP).
* **"Merge contiguous piles of stones in groups of K"** $\rightarrow$ LeetCode 1000.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Minimax Game DP subtract the subproblem value?**  
  *A:* Because subproblem $DP[i+1][j]$ represents the optimal relative lead for the opponent during their turn. Subtracting it computes the current player's net lead after the opponent plays.

* **Q: What is the feasibility condition for merging $N$ piles in groups of $K$?**  
  *A:* $(N - 1) \pmod{K - 1} == 0$. Each merge operation reduces the total pile count by $K - 1$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: INTERVAL DP & GAME THEORY                             |
+-----------------------------------------------------------------------+
| • Minimax Game : dp[i] = max(nums[i] - dp[i+1], nums[j] - dp[i])       |
| • Win Condition: Player 1 wins if dp[0] >= 0                          |
| • Merge Stones : Feasible if (N - 1) % (K - 1) == 0                   |
| • Remove Boxes : Requires 3-parameter state dp[i][j][k] in O(N^4) Time |
| • Performance  : O(N^2) for Game DP | O(N^3 * K) for Merge Stones ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 486 (`Predict the Winner`) in $O(N^2)$ time and $O(N)$ space.
- [ ] I can write LeetCode 1000 (`Minimum Cost to Merge Stones`) in Java.
- [ ] I can write LeetCode 546 (`Remove Boxes`) using 3-parameter memoization.
- [ ] I can state the $K$-pile merge feasibility condition $(N-1) \% (K-1) == 0$.
- [ ] I can explain why Minimax DP subtracts opponent subproblem values.
