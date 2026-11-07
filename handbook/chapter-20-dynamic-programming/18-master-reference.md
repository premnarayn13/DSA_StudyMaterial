# 18. Master Reference — Dynamic Programming Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 26: Dynamic Programming**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering DP Fundamentals, Recursion-to-DP Transformation, Memoization vs Tabulation, 1D DP Problems, 2D Grid DP, 0/1 Knapsack & Variations, Unbounded Knapsack & Coin Change, Subsequence DP & String Alignment, Edit Distance & Regex Matching, Matrix & Interval DP, Minimax Game Theory DP, Bitmask DP (TSP), Digit DP, Tree DP, Monotonic Deque & CHT Optimizations, 8 DP Master Archetypes, Matrix Exponentiation ($O(\log N)$), and Sum Over Subsets (SOS DP).

> **Important:** Review this master reference 15 minutes before an interview to refresh the 8 DP Master Archetypes, 0/1 Knapsack Reverse 1D Loop ($W \to w_i$), Unbounded Coin Forward 1D Loop ($c_i \to W$), Combinations (Outer Coins) vs Permutations (Outer Amounts), Grid DP 1D compression (`dp[j] += dp[j-1]`), LCS match formula ($1 + dp[i-1][j-1]$), Edit Distance 3 choices, Burst Balloons Reverse Choice ($k$ burst LAST), Bitmask TSP ($O(N^2 \cdot 2^N)$), Digit DP `tight` guard, Tree DP `[rob, skip]` tuple return, Monotonic Deque sliding window DP ($O(N)$), and Matrix Exponentiation ($O(\log N)$)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **The 5-Step DP Formulation Framework**:
  1. Define State $DP[\text{state}]$. 2. Formulate Recurrence Equation. 3. Identify Base Cases. 4. Determine Topological Order. 5. Optimize Auxiliary Space.
* **0/1 Knapsack Reverse 1D Loop Formula**:
  - `for (int w = W; w >= w_i; w--) dp[w] = Math.max(v_i + dp[w - w_i], dp[w]);` (Reverse loop prevents item re-use!).
* **Unbounded Knapsack / Coin Change Forward 1D Loop Formula**:
  - `for (int w = w_i; w <= W; w++) dp[w] = Math.min(1 + dp[w - c_i], dp[w]);` (Forward loop enables infinite re-use!).
* **Combinations vs Permutations Loop Order Rule**:
  - **Combinations (LC 518)**: Outer Loop = Coins, Inner Loop = Amounts.
  - **Permutations (LC 377)**: Outer Loop = Amounts, Inner Loop = Coins.
* **Target Sum Algebraic Subset Sum Reduction (LC 494)**:
  - $\text{SubsetSum}(P) = \frac{\text{TotalSum} + \text{Target}}{2}$.
* **Grid DP 1D Compression Formula**:
  - $DP[j] = \text{grid}[i][j] + \min(DP[j], DP[j-1])$ (Replaces 2D matrix with 1D array).
* **Longest Common Subsequence (LCS - LC 1143)**:
  - Match ($S_1[i-1] == S_2[j-1]$): $DP[i][j] = 1 + DP[i-1][j-1]$.
  - Mismatch: $DP[i][j] = \max(DP[i-1][j], DP[i][j-1])$.
* **Longest Palindromic Subsequence (LPS - LC 516)**:
  - $\text{LPS}(S) = \text{LCS}(S, S^R)$.
* **Edit Distance 3-Choice Recurrence (LC 72)**:
  - $DP[i][j] = 1 + \min\left( DP[i][j-1] \text{ (Insert)}, \, DP[i-1][j] \text{ (Delete)}, \, DP[i-1][j-1] \text{ (Replace)} \right)$.
* **Matrix / Interval DP Window Order**:
  - Outer loop MUST iterate over Increasing Window Length $L = 2 \dots N$.
  - Recurrence: $DP[i][j] = \min_{i \le k < j} \left( DP[i][k] + DP[k+1][j] + \text{Cost} \right)$.
* **Burst Balloons Reverse Choice Invariant (LC 312)**:
  - Pick balloon $k$ burst **LAST** in $[i \dots j]$ $\implies \text{Coins} = A[i-1] \cdot A[k] \cdot A[j+1]$.
* **Predict the Winner Minimax Recurrence (LC 486)**:
  - $DP[i][j] = \max\left( A[i] - DP[i+1][j], \; A[j] - DP[i][j-1] \right)$ (Player 1 wins if $DP[0][N-1] \ge 0$).
* **Held-Karp TSP Bitmask DP (N <= 20)**:
  - $DP[\text{mask}][u] = \min_{v \in \text{mask}} \left( DP[\text{mask} \setminus \{u\}][v] + \text{dist}[v][u] \right)$ in $O(N^2 \cdot 2^N)$ time.
* **Digit DP Range Decomposition & Tight Bound**:
  - $\text{Count}([A \dots B]) = \text{Count}(B) - \text{Count}(A - 1)$.
  - `limit = tight ? digit[idx] : 9; nextTight = tight && (d == limit);` (ONLY memoize when `tight == false`).
* **Tree DP Post-Order House Robber III (LC 337)**:
  - $\text{rob}_u = u.\text{val} + \text{skip}_{\text{left}} + \text{skip}_{\text{right}}$; $\text{skip}_u = \max(\text{rob}_L, \text{skip}_L) + \max(\text{rob}_R, \text{skip}_R)$.
* **Monotonic Deque DP Optimization (LC 1425)**:
  - Evict head if index $< i - K$; Evict tail if $DP[\text{tail}] \le DP[i]$ $\implies O(N)$ time.
* **Matrix Exponentiation ($O(\log N)$)**:
  - Evaluates linear DP recurrences for $N = 10^{18}$ via logarithmic binary matrix squaring $T^{N-1}$.

```
Master Dynamic Programming Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| DP Archetype / Problem| State Dimension   | Primary 1D Loop   | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1D Linear (70/198)**| 1D Index $i$      | Forward $1 \dots N$| **$O(N)$ Linear 3⚡**| **$O(1)$ Memory ⚡**|
| **2D Grid DP (62/64)**| 2D Cell $(i, j)$  | Forward Columns   | **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array ⚡**|
| **0/1 Knapsack (416)**| Capacity $w$      | **Reverse ($W \to w_i$)⚡**| **$O(N \cdot W)$ ⚡**| **$O(W)$ 1D Array ⚡**|
| **Coin Change (322)** | Amount $a$        | **Forward ($c_i \to A$)⚡**| **$O(N \cdot A)$ ⚡**| **$O(A)$ 1D Array ⚡**|
| **LCS / Alignment**   | String Prefixes   | Row-by-Row 1D      | **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array ⚡**|
| **Edit Distance (72)**| String Prefixes   | Row-by-Row 1D      | **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array ⚡**|
| **Interval DP (312)** | Interval $[i..j]$ | **Window $L = 2..N$ ⚡**| **$O(N^3)$ Cubic ⚡**| $O(N^2)$ Matrix   |
| **Bitmask TSP**       | Mask Integer      | Subsets $0..2^N-1$ | **$O(N^2 \cdot 2^N)$ ⚡**| $O(N \cdot 2^N)$ Table|
| **Digit DP [A..B]**   | Digit Index       | MSD to LSD DFS    | **$O(\log_{10} B)$⚡**| $O(\log_{10} B)$ Memo|
| **Tree DP (337/124)** | Subtree Node $u$  | Post-Order DFS    | **$O(N)$ Linear ⚡**| $O(H)$ Stack      |
| **Monotonic Deque**   | Sliding Window $K$| Linear Index $i$   | **$O(N)$ Linear ⚡**| $O(K)$ Deque      |
| **Matrix Exponent**   | Transition Matrix | Binary Squaring   | **$O(K^3 \log N)$ ⚡**| $O(K^2)$ Matrix   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| DP Topic / Pattern | Primary Target | Core Recurrence / Mechanism | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Climbing Stairs (70)** | Total ways reach step | $DP[i] = DP[i-1] + DP[i-2]$ | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| 2 State variables |
| **House Robber (198)** | Max non-adjacent loot | $DP[i] = \max(v_i + DP[i-2], DP[i-1])$ | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| `curr = max(num+p2, p1)` |
| **Unique Paths (62)** | Total grid paths | $DP[j] += DP[j-1]$ | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| Top + Left addition |
| **Min Path Sum (64)** | Min grid path cost | $DP[j] = \text{grid} + \min(DP[j], DP[j-1])$ | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| Top vs Left min |
| **0/1 Knapsack (416)**| Equal subset sum | $DP[w] = DP[w] \lor DP[w - w_i]$ | $\mathbf{O(N \cdot W)}$ ⚡| $\mathbf{O(W)}$ 1D Array ⚡| **Reverse loop $W \to w_i$** |
| **Target Sum (494)** | Count sign assignments | $P = (\text{Total} + \text{Target}) / 2$ | $\mathbf{O(N \cdot W)}$ ⚡| $\mathbf{O(W)}$ 1D Array ⚡| Subset sum reduction |
| **Min Coins (322)** | Min coins for amount | $DP[a] = \min(DP[a], 1 + DP[a - c])$ | $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| **Forward loop $c_i \to A$** |
| **Coin Combinations (518)**| Unordered combinations | $DP[a] += DP[a - c]$ | $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| **Outer loop = Coins** |
| **Coin Permutations (377)**| Ordered permutations | $DP[a] += DP[a - c]$ | $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| **Outer loop = Amounts** |
| **LCS (1143)** | Common subsequence | Match: $1 + DP[i-1][j-1]$ | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| `prevDiag` variable |
| **Edit Distance (72)**| Min edits (Ins/Del/Rep) | $1 + \min(\text{Ins, Del, Rep})$ | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| 3-choice min |
| **Burst Balloons (312)**| Max coins balloon pop | Balloon $k$ burst LAST | $\mathbf{O(N^3)}$ Cubic ⚡| $O(N^2)$ Matrix | Reverse choice $k$ |
| **Predict Winner (486)**| Minimax relative lead | $\max(A[i] - dp, A[j] - dp)$ | $\mathbf{O(N^2)}$ Quadratic⚡| $\mathbf{O(N)}$ 1D Array ⚡| Opponent subtraction |
| **TSP (Held-Karp)** | Shortest tour N cities | $DP[\text{mask}][u] = \min(DP[\text{mask}\setminus u][v] + \text{dist})$ | $\mathbf{O(N^2 \cdot 2^N)}$ ⚡| $O(N \cdot 2^N)$ Table | Mask for $N \le 20$ |
| **Digit DP [A..B]** | Digit property count | Range $\text{Count}(B) - \text{Count}(A-1)$ | $\mathbf{O(\log_{10} B)}$ ⚡| $O(\log_{10} B)$ Memo| `tight` bound guard |
| **House Robber III (337)**| Non-adjacent tree loot | `[rob_u, skip_u]` tuple return | $\mathbf{O(N)}$ Strict ⚡| $O(H)$ Stack | Post-Order DFS |
| **Tree Max Path Sum (124)**| Max binary tree path | Global max = Arch; Return Branch | $\mathbf{O(N)}$ Strict ⚡| $O(H)$ Stack | Post-Order DFS |
| **Monotonic Deque (1425)**| Sliding window K DP | Evict head out-of-window; tail smaller | $\mathbf{O(N)}$ Strict ⚡| $O(K)$ Deque | Amortized $O(N)$ |
| **Matrix Exponentiation**| $F(10^{18})$ Linear DP | Binary matrix squaring $T^{N-1}$ | $\mathbf{O(K^3 \log N)}$ ⚡| $O(K^2)$ Matrix | Logarithmic time |
| **Sum Over Subsets (SOS)**| Sub-mask sums | $DP[\text{mask}] += DP[\text{mask} \setminus 2^i]$ | $\mathbf{O(N \cdot 2^N)}$ ⚡| $O(2^N)$ Array | $O(N \cdot 2^N)$ vs $O(3^N)$ |

---

## 4. Architectural System & Production Use Cases
```
+-----------------------------------------------------------------------------------+
| Production System Dynamic Programming Architectures                               |
+-----------------------------------------------------------------------------------+
| Natural Language Processing & Spell-Checking  : Edit Distance / Levenshtein DP    |
| Version Control Systems (Git Diff Engine)      : Longest Common Subsequence (LCS)  |
| Compiler Lexers & Regex Matching Engines       : Regular Expression Matching DP   |
| High-Frequency Trading & Logistics (N <= 20)   : Held-Karp Bitmask TSP DP         |
| Financial Options Pricing & Risk Analysis      : Monotonic Deque & CHT DP         |
| DNA Sequence Alignment (Bioinformatics)        : Needleman-Wunsch String Alignment|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Space-Optimized Fibonacci / Climbing Stairs
> int curr = prev1 + prev2; prev2 = prev1; prev1 = curr;
> 
> // 2. 0/1 Knapsack Reverse 1D Loop (Single Use)
> for (int w = capacity; w >= weight; w--) dp[w] = Math.max(dp[w], value + dp[w - weight]);
> 
> // 3. Unbounded Coin Change Forward 1D Loop (Infinite Use)
> for (int amt = coin; amt <= target; amt++) dp[amt] = Math.min(dp[amt], 1 + dp[amt - coin]);
> 
> // 4. Unordered Combinations (LeetCode 518) vs Ordered Permutations (LeetCode 377)
> for (int c : coins) for (int a = c; a <= A; a++) dp[a] += dp[a - c]; // Combinations
> for (int a = 1; a <= A; a++) for (int c : coins) if (a >= c) dp[a] += dp[a - c]; // Permutations
> 
> // 5. Grid DP 1D Compression
> dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]);
> 
> // 6. LCS 1D Compression with prevDiag
> if (s1.charAt(i-1) == s2.charAt(j-1)) dp[j] = 1 + prevDiag; else dp[j] = Math.max(dp[j], dp[j-1]);
> 
> // 7. Burst Balloons Reverse Choice (k burst LAST)
> int coins = dp[i][k - 1] + dp[k + 1][j] + A[i - 1] * A[k] * A[j + 1]; dp[i][j] = Math.max(dp[i][j], coins);
> 
> // 8. Bitmask Bit Manipulation
> if ((mask & (1 << i)) == 0) int nextMask = mask | (1 << i);
> 
> // 9. Digit DP Tight Limit
> int limit = tight ? (sN.charAt(idx) - '0') : 9; boolean nextTight = tight && (d == limit);
> 
> // 10. Monotonic Deque Sliding Window Eviction
> while (!deque.isEmpty() && deque.peekFirst() < i - k) deque.pollFirst();
> while (!deque.isEmpty() && dp[deque.peekLast()] <= dp[i]) deque.pollLast();
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Forward Iteration in 0/1 Knapsack**: Running `w = w_i ... W` in 0/1 Knapsack allows items to be reused multiple times. **ALWAYS iterate capacity BACKWARDS ($W \to w_i$) for 0/1 Knapsack**!
* **Pitfall 2: Reversing Outer Loop Order in Coin Change II (LeetCode 518)**: Putting amounts on the outside in Coin Change II generates ordered permutations instead of unordered combinations. **ALWAYS put Coins on the outside for Combinations**!
* **Pitfall 3: Memoizing States When `tight == true` in Digit DP**: Memoizing constrained states pollutes the cache for future unconstrained searches. **ONLY memoize when `tight == false && !isLeadingZero`**!
* **Pitfall 4: Choosing First Balloon Burst in Burst Balloons**: Picking the first balloon creates dependencies between subproblems. **ALWAYS pick the balloon burst LAST in $[i \dots j]$**!
* **Pitfall 5: Returning Arch Path Sum to Parent in Tree Max Path Sum (LeetCode 124)**: Returning `u.val + left + right` to parent forms an invalid branching tree path. **ALWAYS return single branch `u.val + max(left, right)` to parent**!
* **Pitfall 6: Forgetting Bitwise Precedence Parentheses**: Writing `mask & (1 << i) == 0` evaluates incorrectly due to `==` precedence. **ALWAYS use `((mask & (1 << i)) == 0)`**!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 26 (DYNAMIC PROGRAMMING)         |
+-----------------------------------------------------------------------+
| 1. 0/1 Knapsack   : Reverse 1D Loop W -> w_i (Single Use) -> O(N*W)    |
| 2. Unbounded Coin : Forward 1D Loop c_i -> A (Infinite Use) -> O(N*A)  |
| 3. Combinations 518: Outer Loop = COINS (Order does not matter)       |
| 4. Permutations 377: Outer Loop = AMOUNTS (Order matters)             |
| 5. Grid DP 1D     : dp[j] = grid + min(dp[j], dp[j-1]) -> O(N) Space  |
| 6. LCS Alignment  : Match -> 1 + prevDiag; Mismatch -> max(top, left) |
| 7. Burst Balloons : Balloon k burst LAST -> coins = A[i-1]*A[k]*A[j+1]|
| 8. Predict Winner : dp[i] = max(nums[i] - dp[i+1], nums[j] - dp[i])   |
| 9. Bitmask TSP    : dp[mask][u] = min(dp[mask\u][v] + dist) (N <= 20) |
| 10. Digit DP      : Count([A..B]) = Count(B) - Count(A-1)             |
| 11. Tree DP 337   : Post-order DFS return [rob_u, skip_u] pair        |
| 12. Monotonic DP  : Deque eviction -> O(N * K) to O(N) Linear Time ⚡  |
| 13. Matrix Exp    : Evaluates F(10^18) in O(K^3 log N) Log Time ⚡    |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can state the 2 requirements for Dynamic Programming (Overlapping Subproblems & Optimal Substructure).
- [ ] I can state the 5-step DP formulation framework.
- [ ] I can write Climbing Stairs (LeetCode 70) and House Robber (LeetCode 198) in $O(1)$ space.
- [ ] I can write Unique Paths (LeetCode 62) and Minimum Path Sum (LeetCode 64) with 1D space compression.
- [ ] I can write 0/1 Knapsack (LeetCode 416) with Reverse 1D loop.
- [ ] I can write Coin Change (LeetCode 322) with Forward 1D loop.
- [ ] I can state why outer coin loop produces combinations and outer amount loop produces permutations.
- [ ] I can solve Target Sum (LeetCode 494) using algebraic subset sum reduction.
- [ ] I can write LCS (LeetCode 1143) and Edit Distance (LeetCode 72) with 1D space compression.
- [ ] I can solve Burst Balloons (LeetCode 312) using Reverse Choice DP ($k$ burst LAST).
- [ ] I can solve Predict the Winner (LeetCode 486) using Minimax relative score DP.
- [ ] I can write Held-Karp TSP in $O(N^2 \cdot 2^N)$ time using Bitmask DP.
- [ ] I can write Digit DP range decomposition $\text{Count}(B) - \text{Count}(A-1)$ with `tight` bound.
- [ ] I can write House Robber III (LeetCode 337) and Tree Max Path Sum (LeetCode 124) in Java.
- [ ] I can solve Constrained Subsequence Sum (LeetCode 1425) in $O(N)$ time using Monotonic Deque.
- [ ] I can write Matrix Exponentiation for $N$-th Fibonacci in $O(\log N)$ time.
- [ ] I can write Sum Over Subsets (SOS DP) in $O(N \cdot 2^N)$ time.
- [ ] I can match any DP interview question to one of the 8 Master Archetypes in under 10 seconds.
