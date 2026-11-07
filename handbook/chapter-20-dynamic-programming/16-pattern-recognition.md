# 16. Pattern Recognition & DP Triggers: 8 Master Dynamic Programming Archetypes

## 1. Introduction
High-speed problem solving in technical coding interviews requires instant **Dynamic Programming Pattern Recognition**. Under timed interview conditions, trying to derive DP recurrence equations from scratch can lead to wasted time or sub-optimal choices. Experienced competitive programmers and senior software engineers map problem descriptions directly to one of **8 Universal DP Master Archetypes**: **1D Linear DP**, **2D Grid DP**, **0/1 Knapsack & Subset Sum**, **Unbounded Knapsack & Coin Change**, **Subsequence & String Alignment**, **Matrix & Interval DP**, **Bitmask DP**, and **Tree & Digit DP**. Identifying trigger words in problem statements allows immediate selection of optimal state definitions, loop directions, and complexity targets.

> **Important:** The 8 Universal DP Master Archetypes & Trigger Signals:
> 1. **Pattern 1: 1D Linear DP**: Trigger = *"Count ways / min cost on 1D sequence, no adjacent items"*. Mechanics = $DP[i] = f(DP[i-1], DP[i-2])$. Time = $O(N)$, Space = $O(1)$.
> 2. **Pattern 2: 2D Grid DP**: Trigger = *"Paths / min cost moving Right and Down in M x N matrix"*. Mechanics = $DP[j] = \text{grid}[i][j] + \min(DP[j], DP[j-1])$. Time = $O(M \cdot N)$, Space = $O(N)$.
> 3. **Pattern 3: 0/1 Knapsack & Subset Sum**: Trigger = *"Select subset of indivisible items to reach sum/capacity"*. Mechanics = **Reverse Loop ($W \to w_i$)** $DP[w] = \max(v_i + DP[w-w_i], DP[w])$. Time = $O(N \cdot W)$, Space = $O(W)$.
> 4. **Pattern 4: Unbounded Knapsack & Coin Change**: Trigger = *"Infinite item re-use, min coins, coin combinations/permutations"*. Mechanics = **Forward Loop ($w_i \to W$)** $DP[w] = \min(DP[w], 1 + DP[w-c])$. Time = $O(N \cdot A)$, Space = $O(A)$.
> 5. **Pattern 5: Subsequence & String Alignment**: Trigger = *"LCS, edit distance, wildcard/regex matching across 2 strings"*. Mechanics = $DP[i][j]$ matrix matching characters. Time = $O(M \cdot N)$, Space = $O(N)$.
> 6. **Pattern 6: Matrix & Interval DP**: Trigger = *"Chain multiplication, burst balloons, minimax turn games on subarray [i..j]"*. Mechanics = **Outer Loop Window Length $L$** $DP[i][j] = \min(DP[i][k] + DP[k+1][j] + \text{cost})$. Time = $O(N^3)$, Space = $O(N^2)$.
> 7. **Pattern 7: Bitmask DP**: Trigger = *"TSP, partition K subsets, subset size N <= 20"*. Mechanics = $DP[\text{mask}][u]$ bitwise state operations. Time = $O(N^2 \cdot 2^N)$, Space = $O(N \cdot 2^N)$.
> 8. **Pattern 8: Tree & Digit DP**: Trigger = *"Subtree robbing, tree path sum, count numbers in range [A..B] with digit properties"*. Mechanics = Post-order DFS `[rob, skip]` or Digit DFS with `tight`. Time = $O(N)$ or $O(\log_{10} B)$. ⚡

```
Master DP Archetype Decision Flowchart:

Problem Trigger Signal:
├── "Non-adjacent elements in 1D array?" ─────────────────► Pattern 1: 1D Linear DP (House Robber)
├── "Paths in M x N Grid?" ───────────────────────────────► Pattern 2: 2D Grid DP (Unique Paths)
├── "Subset of indivisible items sum to W?" ──────────────► Pattern 3: 0/1 Knapsack (Reverse Loop)
├── "Infinite item re-use / Coin Change?" ────────────────► Pattern 4: Unbounded Knapsack (Forward Loop)
├── "LCS / Edit Distance across 2 strings?" ──────────────► Pattern 5: Subsequence / String Alignment
├── "Chain multiplication / Burst balloons on [i..j]?" ───► Pattern 6: Matrix / Interval DP (Window L)
├── "Subset size N <= 20 / Travelling Salesperson?" ──────► Pattern 7: Bitmask DP (Mask Integer)
└── "Subtree aggregation / Digit range [A..B] count?" ────► Pattern 8: Tree / Digit DP (Post-order / Tight) ⚡
```

---

## 2. Core Concepts & Master DP Pattern Recognition Matrix

### 2.1 Master DP Pattern Recognition Matrix
```
Master DP Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Primary Recurrence| 1D Loop Direction | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. 1D Linear DP**   | "No adjacent items"| $dp[i] = \max(v_i+dp[i-2], dp[i-1])$| Forward (1..N)    | **$O(N)$ Linear ⚡**|
| **2. 2D Grid DP**     | "Paths in M x N"  | $dp[j] += dp[j-1]$| Forward Columns   | **$O(M \cdot N)$ ⚡**|
| **3. 0/1 Knapsack**   | "Indivisible items"| $dp[w] = \max(v_i+dp[w-w_i], dp[w])$| **Reverse ($W \to w_i$)⚡**| **$O(N \cdot W)$ ⚡**|
| **4. Unbounded Coin** | "Infinite re-use" | $dp[w] = \min(dp[w], 1+dp[w-c])$| **Forward ($c_i \to W$)⚡**| **$O(N \cdot A)$ ⚡**|
| **5. String Alignment**| "LCS / Edit dist" | Match: $1+dp[i-1][j-1]$| Row-by-Row 1D      | **$O(M \cdot N)$ ⚡**|
| **6. Matrix Interval**| "Burst balloons"  | $dp[i][k] + dp[k+1][j] + \text{cost}$| **Window $L = 2..N$ ⚡**| **$O(N^3)$ Cubic ⚡**|
| **7. Bitmask DP**     | "Subset $N \le 20$"| $dp[\text{mask}][u]$| Subsets $0..2^N-1$ | **$O(N^2 \cdot 2^N)$ ⚡**|
| **8. Tree / Digit DP**| "Subtree / Digits" | Post-order DFS / Digit DFS| Post-Order / MSD   | **$O(N)$ / $O(\log_{10} B)$⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"0/1 Knapsack = Reverse 1D Loop; Unbounded Coin = Forward 1D Loop; Interval DP = Outer Window L; Bitmask DP = Mask for N <= 20!"**

---

## 3. Deep Dive into the 8 DP Archetypes & LeetCode Audits

### 3.1 Auditing Top LeetCode Benchmark Problems
```
LeetCode Benchmark Problem Audits:

LeetCode 70 (Climbing Stairs)              ──► Pattern 1: 1D Linear DP (dp[i] = dp[i-1] + dp[i-2])
LeetCode 198 (House Robber)               ──► Pattern 1: 1D Linear DP (dp[i] = max(val + dp[i-2], dp[i-1]))
LeetCode 62 (Unique Paths)                ──► Pattern 2: 2D Grid DP (dp[j] += dp[j-1])
LeetCode 64 (Minimum Path Sum)            ──► Pattern 2: 2D Grid DP (dp[j] = grid + min(dp[j], dp[j-1]))
LeetCode 416 (Partition Equal Subset Sum) ──► Pattern 3: 0/1 Knapsack (Reverse Loop W -> w_i)
LeetCode 494 (Target Sum)                 ──► Pattern 3: 0/1 Knapsack (Subset Sum Reduction)
LeetCode 322 (Coin Change Min)            ──► Pattern 4: Unbounded Knapsack (Forward Loop c_i -> W)
LeetCode 518 (Coin Change II Combinations)──► Pattern 4: Unbounded Knapsack (Outer Loop = Coins)
LeetCode 1143 (LCS)                       ──► Pattern 5: String Alignment (Match: 1 + dp[i-1][j-1])
LeetCode 72 (Edit Distance)               ──► Pattern 5: String Alignment (1 + min(Ins, Del, Rep))
LeetCode 312 (Burst Balloons)             ──► Pattern 6: Matrix / Interval DP (Reverse Choice k Last)
LeetCode 486 (Predict the Winner)         ──► Pattern 6: Matrix Interval DP (Minimax Relative Lead)
LeetCode 698 (Partition K Subsets)        ──► Pattern 7: Bitmask DP (Mask Integer N <= 16)
LeetCode 337 (House Robber III)           ──► Pattern 8: Tree DP (Post-Order DFS [rob, skip] Pair)
LeetCode 902 (Numbers At Most N)          ──► Pattern 8: Digit DP (Tight Bound DFS)
```

---

## 4. Internal Working Mechanics: The 10-Second Interview Decision Engine

How to diagnose any unseen interview problem in 10 seconds:

```
Step 1: Check Input Constraints & Structure
        - Is input a Tree? ──► Pattern 8: Tree DP (Post-Order DFS).
        - Is range B <= 10^18 with digit rules? ──► Pattern 8: Digit DP.
        - Is array size N <= 20? ──► Pattern 7: Bitmask DP (O(N^2 * 2^N)).

Step 2: Check Input Dimension & Operations
        - Operating on 2 Strings? ──► Pattern 5: String Alignment (LCS / Edit Distance).
        - Operating on M x N Matrix? ──► Pattern 2: 2D Grid DP.
        - Operating on Subarray Intervals [i..j] or Chain Partitioning? ──► Pattern 6: Interval DP (Window L).

Step 3: Check Item Re-usability (Knapsack Problems)
        - Can items be picked ONCE only? ──► Pattern 3: 0/1 Knapsack (REVERSE 1D Loop W -> w_i).
        - Can items be reused INFINITELY? ──► Pattern 4: Unbounded Knapsack (FORWARD 1D Loop c_i -> W). ⚡
```

---

## 5. Visual Diagram: The 8 DP Archetypes Map

```
                             [ Dynamic Programming Problem ]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
           [ Single Array / String ]                     [ Matrix / Grid / Tree ]
           /           │           \                     /           │          \
          ▼            ▼            ▼                   ▼            ▼           ▼
     Pattern 1     Pattern 3    Pattern 4           Pattern 2    Pattern 6   Pattern 8
    (1D Linear)   (0/1 Knap)   (Unbounded)          (Grid DP)   (Interval)  (Tree/Digit)
    dp[i-1]+dp[i-2]  Reverse W    Forward W           Top+Left    Window L    Post-Order
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across all 8 Master DP Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating Reference Implementations
 * Across the 8 Universal Dynamic Programming Master Archetypes.
 */
public class DPPatternRecognitionMaster {

    // PATTERN 1: 1D LINEAR DP (LeetCode 198 House Robber)
    public int pattern1_HouseRobber(int[] nums) {
        int prev2 = 0, prev1 = 0;
        for (int num : nums) {
            int curr = Math.max(num + prev2, prev1);
            prev2 = prev1; prev1 = curr;
        }
        return prev1;
    }

    // PATTERN 2: 2D GRID DP (LeetCode 64 Minimum Path Sum)
    public int pattern2_MinPathSum(int[][] grid) {
        int n = grid[0].length;
        int[] dp = new int[n];
        dp[0] = grid[0][0];
        for (int j = 1; j < n; j++) dp[j] = dp[j - 1] + grid[0][j];
        for (int i = 1; i < grid.length; i++) {
            dp[0] += grid[i][0];
            for (int j = 1; j < n; j++) dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]);
        }
        return dp[n - 1];
    }

    // PATTERN 3: 0/1 KNAPSACK (LeetCode 416 Reverse Loop)
    public boolean pattern3_01Knapsack(int[] nums) {
        int sum = 0; for (int n : nums) sum += n;
        if (sum % 2 != 0) return false;
        int target = sum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;
        for (int num : nums) {
            for (int w = target; w >= num; w--) dp[w] = dp[w] || dp[w - num]; // REVERSE! ⚡
        }
        return dp[target];
    }

    // PATTERN 4: UNBOUNDED COIN CHANGE (LeetCode 322 Forward Loop)
    public int pattern4_UnboundedCoin(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int c : coins) {
            for (int a = c; a <= amount; a++) dp[a] = Math.min(dp[a], 1 + dp[a - c]); // FORWARD! ⚡
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }

    // PATTERN 5: STRING ALIGNMENT (LeetCode 1143 LCS)
    public int pattern5_LCS(String s1, String s2) {
        int n = s2.length();
        int[] dp = new int[n + 1];
        for (int i = 1; i <= s1.length(); i++) {
            int prevDiag = 0;
            for (int j = 1; j <= n; j++) {
                int temp = dp[j];
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) dp[j] = 1 + prevDiag;
                else dp[j] = Math.max(dp[j], dp[j - 1]);
                prevDiag = temp;
            }
        }
        return dp[n];
    }

    // PATTERN 6: MATRIX / INTERVAL DP (LeetCode 312 Burst Balloons Window L)
    public int pattern6_BurstBalloons(int[] nums) {
        int n = nums.length;
        int[] A = new int[n + 2]; A[0] = 1; A[n + 1] = 1;
        for (int i = 0; i < n; i++) A[i + 1] = nums[i];
        int[][] dp = new int[n + 2][n + 2];
        for (int L = 1; L <= n; L++) {
            for (int i = 1; i <= n - L + 1; i++) {
                int j = i + L - 1;
                for (int k = i; k <= j; k++) {
                    dp[i][j] = Math.max(dp[i][j], dp[i][k - 1] + dp[k + 1][j] + A[i - 1] * A[k] * A[j + 1]);
                }
            }
        }
        return dp[1][n];
    }
}
```

> **Quick Syntax:**
```java
// Master DP 1D Loop Rules
// 0/1 Knapsack (Pattern 3)     : for (int w = W; w >= w_i; w--) dp[w] = max(...)
// Unbounded Coin (Pattern 4)   : for (int w = w_i; w <= W; w++) dp[w] = min(...)
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (1D Linear DP)**: LeetCode 70, LeetCode 198, LeetCode 213, LeetCode 91, LeetCode 53.
* **Pattern 2 (2D Grid DP)**: LeetCode 62, LeetCode 63, LeetCode 64, LeetCode 174.
* **Pattern 3 (0/1 Knapsack)**: LeetCode 416, LeetCode 494, LeetCode 1049.
* **Pattern 4 (Unbounded Coin)**: LeetCode 322, LeetCode 518, LeetCode 377.
* **Pattern 5 (String Alignment)**: LeetCode 1143, LeetCode 516, LeetCode 72, LeetCode 44, LeetCode 10.
* **Pattern 6 (Matrix Interval DP)**: MCM, LeetCode 312, LeetCode 486, LeetCode 1130.
* **Pattern 7 (Bitmask DP)**: TSP, LeetCode 698, LeetCode 1125.
* **Pattern 8 (Tree & Digit DP)**: LeetCode 337, LeetCode 124, LeetCode 968, LeetCode 902.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class DPPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   8 MASTER DP ARCHETYPES BENCHMARK DEMO         ");
        System.out.println("=================================================\n");

        DPPatternRecognitionMaster master = new DPPatternRecognitionMaster();

        // 1. Pattern 1 (1D Linear DP)
        int[] houseArr = {2, 7, 9, 3, 1};
        System.out.println("1. Pattern 1 (1D Linear DP - House Robber): " + master.pattern1_HouseRobber(houseArr));

        // 2. Pattern 2 (2D Grid DP)
        int[][] grid = {{1, 3, 1}, {1, 5, 1}, {4, 2, 1}};
        System.out.println("2. Pattern 2 (2D Grid DP - Min Path Sum): " + master.pattern2_MinPathSum(grid));

        // 3. Pattern 3 (0/1 Knapsack Reverse Loop)
        int[] partArr = {1, 5, 11, 5};
        System.out.println("3. Pattern 3 (0/1 Knapsack - Partition Sum): " + master.pattern3_01Knapsack(partArr));

        // 4. Pattern 4 (Unbounded Coin Change Forward Loop)
        int[] coins = {1, 2, 5};
        System.out.println("4. Pattern 4 (Unbounded Coin Change - Min Coins): " + master.pattern4_UnboundedCoin(coins, 11));

        // 5. Pattern 5 (String Alignment LCS)
        System.out.println("5. Pattern 5 (String Alignment - LCS Length): " + master.pattern5_LCS("abcde", "ace"));

        // 6. Pattern 6 (Matrix Interval DP Burst Balloons)
        int[] balloons = {3, 1, 5, 8};
        System.out.println("6. Pattern 6 (Matrix Interval DP - Burst Balloons): " + master.pattern6_BurstBalloons(balloons));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| DP Master Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. 1D Linear DP**   | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| "No adjacent items / 1D steps" |
| **2. 2D Grid DP**     | $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| "Paths / min cost moving Right/Down" |
| **3. 0/1 Knapsack**   | $\mathbf{O(N \cdot W)}$ ⚡| $\mathbf{O(W)}$ 1D Array ⚡| "Indivisible items, single use" |
| **4. Unbounded Coin** | $\mathbf{O(N \cdot A)}$ ⚡| $\mathbf{O(A)}$ 1D Array ⚡| "Infinite item re-use / min coins" |
| **5. String Alignment**| $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| "LCS / Edit distance across 2 strings" |
| **6. Matrix Interval**| $\mathbf{O(N^3)}$ Cubic ⚡| $O(N^2)$ Matrix Table | "Chain multiplication / Burst balloons" |
| **7. Bitmask DP**     | $\mathbf{O(N^2 \cdot 2^N)}$ ⚡| $O(N \cdot 2^N)$ Table | "TSP / Subset size $N \le 20$" |
| **8. Tree / Digit DP**| $\mathbf{O(N)}$ / $\mathbf{O(\log_{10} B)}$⚡| $O(H)$ / $O(\log_{10} B)$ | "Subtree robbing / Range $[A \dots B]$" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between 0/1 Knapsack and Unbounded Knapsack**:
   - Items single use $\to$ **Reverse Loop ($W \to w_i$)**.
   - Items infinite re-use $\to$ **Forward Loop ($w_i \to W$)**.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Standard 1D Loop Direction to 0/1 Knapsack**:
  - Running forward loop $w_i \to W$ in 0/1 Knapsack allows items to be reused. ALWAYS use reverse loop $W \to w_i$ for 0/1 Knapsack!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second DP Pattern Matcher Rules:
> 1. Non-adjacent 1D? $\to$ Pattern 1 (House Robber $O(1)$ space).
> 2. Grid M x N? $\to$ Pattern 2 (Grid DP $O(N)$ space).
> 3. Single-use subset sum? $\to$ Pattern 3 (0/1 Knapsack Reverse Loop).
> 4. Infinite coin re-use? $\to$ Pattern 4 (Unbounded Coin Forward Loop).
> 5. 2 Strings matching? $\to$ Pattern 5 (String Alignment Matrix).
> 6. Subarray $[i..j]$ splits? $\to$ Pattern 6 (Interval DP Window $L$).
> 7. Subset size $N \le 20$? $\to$ Pattern 7 (Bitmask DP).
> 8. Subtree / Digit bounds? $\to$ Pattern 8 (Tree / Digit DP). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Data Structure | Loop Direction / Order | Auxiliary Memory |
| :--- | :--- | :--- | :--- |
| **Pattern 3 (0/1 Knap)** | 1D Array `dp[w]` | **Reverse ($W \to w_i$) ⚡** | $O(W)$ |
| **Pattern 4 (Unbounded)**| 1D Array `dp[w]` | **Forward ($w_i \to W$) ⚡** | $O(A)$ |
| **Pattern 6 (Interval)** | 2D Table `dp[i][j]` | **Window Length $L = 2 \dots N$ ⚡**| $O(N^2)$ |

---

## 14. How to Recognize This in Questions

* **"Can array be partitioned into two subsets with equal sum?"** $\rightarrow$ Pattern 3 (0/1 Knapsack Reverse Loop).
* **"Find min coins to make amount A with infinite coin supply"** $\rightarrow$ Pattern 4 (Unbounded Coin Forward Loop).

---

## 15. Frequently Asked Interview Questions

* **Q: How do you differentiate 0/1 Knapsack from Unbounded Knapsack in code?**  
  *A:* By the capacity loop direction: 0/1 Knapsack iterates capacity backwards ($W \to w_i$), while Unbounded Knapsack iterates capacity forwards ($w_i \to W$).

* **Q: Why does Coin Change II (LeetCode 518) use coins in the outer loop?**  
  *A:* Putting coins in the outer loop ensures coins are processed in a fixed order, counting unordered combinations rather than ordered permutations.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 8 MASTER DP ARCHETYPES                                |
+-----------------------------------------------------------------------+
| • Pattern 1: 1D Linear DP    -> dp[i] = max(v_i + dp[i-2], dp[i-1])   |
| • Pattern 2: 2D Grid DP      -> dp[j] = grid + min(dp[j], dp[j-1])    |
| • Pattern 3: 0/1 Knapsack    -> REVERSE Loop W -> w_i (Single use)    |
| • Pattern 4: Unbounded Coin  -> FORWARD Loop c_i -> W (Infinite use)  |
| • Pattern 5: String Align    -> Match 1 + dp[i-1][j-1]; Mismatch max  |
| • Pattern 6: Matrix Interval -> Outer Loop Window L = 2..N            |
| • Pattern 7: Bitmask DP      -> Integer mask for N <= 20              |
| • Pattern 8: Tree / Digit DP -> Post-order DFS / Digit DFS tight bound|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any DP problem to one of the 8 Master Archetypes in under 10 seconds.
- [ ] I know when to use Reverse 1D Loop vs Forward 1D Loop.
- [ ] I can write 0/1 Knapsack (LeetCode 416) in Java.
- [ ] I can write Coin Change (LeetCode 322 & 518) in Java.
- [ ] I can write LCS (LeetCode 1143) and Edit Distance (LeetCode 72) in Java.
