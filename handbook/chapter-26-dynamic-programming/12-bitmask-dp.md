# 12. Bitmask DP: Subset State Representations, TSP & Exponential-to-Polynomial Reductions

## 1. Introduction
**Bitmask Dynamic Programming** is a specialized DP technique used to solve NP-hard combinatorial problems over small subset sizes ($N \le 20$). By representing a subset of visited items, completed tasks, or covered cities as an integer **Bitmask** ($\text{mask} \in [0 \dots 2^N - 1]$), Bitmask DP compresses subset state checks into $O(1)$ CPU bitwise operations. Bitmask DP replaces exponential factorial brute-force searches ($O(N!)$ or $O(K^N)$) with **Pseudo-Polynomial / Exponential Bounds $O(N^2 \cdot 2^N)$ or $O(N \cdot 2^N)$**. Key benchmark problems include the **Travelling Salesperson Problem (TSP)**, **Partition to K Equal Sum Subsets (LeetCode 698)**, **Smallest Sufficient Team (LeetCode 1125)**, and **Matchsticks to Square (LeetCode 473)**.

> **Important:** Core Structural Invariants of Bitmask DP:
> 1. **Integer Subset Representation**:
>    - An integer `mask` encodes subset inclusion: if the $i$-th bit of `mask` is 1 (`(mask & (1 << i)) != 0`), item $i$ is included in the subset.
> 2. **Bitwise Helper Operations Table**:
>    - Check $i$-th bit set  : `(mask & (1 << i)) != 0`
>    - Set $i$-th bit to 1   : `mask | (1 << i)`
>    - Clear $i$-th bit to 0 : `mask & ~(1 << i)`
>    - Toggle $i$-th bit     : `mask ^ (1 << i)`
>    - Subset size count     : `Integer.bitCount(mask)`
> 3. **TSP Recurrence Equation (Held-Karp Algorithm)**:
>    - Let $DP[\text{mask}][u]$ be min cost to visit all cities in `mask`, ending at city $u$:
>      $$DP[\text{mask}][u] = \min_{v \in \text{mask}, v \neq u} \left( DP[\text{mask} \setminus \{u\}][v] + \text{dist}[v][u] \right)$$
> 4. **Full Mask Sentinel ($2^N - 1$)**:
>    - Base or goal condition `mask == (1 << N) - 1` signifies that ALL $N$ items/cities have been visited. ⚡

```
Bitmask Binary Representation Topology (N = 4 Items):

Mask Integer = 13 (Binary: 1101_2):
Bit 3 (1): Item 3 Included  ──► [ Item 3 ]
Bit 2 (1): Item 2 Included  ──► [ Item 2 ]
Bit 1 (0): Item 1 EXCLUDED  ──► [ Skipped ]
Bit 0 (1): Item 0 Included  ──► [ Item 0 ]

Subset Encoded: { Item 0, Item 2, Item 3 } in O(1) Memory! ⚡
```

---

## 2. Core Concepts & Bitmask DP Strategy Matrix

### 2.1 Bitmask DP Strategy Matrix
```
Bitmask DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | State Representation| Target Goal Mask| Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Travelling Salesperson**| $DP[\text{mask}][u]$| $(1 \ll N) - 1$ | **$O(N^2 \cdot 2^N)$ ⚡**| **$O(N \cdot 2^N)$ Table⚡**|
| **Partition K Subsets**| $DP[\text{mask}]$ | $(1 \ll N) - 1$ | **$O(N \cdot 2^N)$ ⚡**| **$O(2^N)$ Table ⚡**|
| **Smallest Team (1125)**| $DP[\text{skills}]$| $(1 \ll S) - 1$ | **$O(P \cdot 2^S)$ ⚡**| **$O(2^S)$ Table ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Bitmask encodes subsets as integers mask 0..(2^N - 1); Bitwise (mask & (1<<i)) checks set bit; TSP DP[mask][u] runs in O(N^2 * 2^N)!"**

---

## 3. Characteristics & Held-Karp Complexity Reduction Mathematical Proof

### 3.1 Mathematical Proof of Held-Karp TSP ($O(N^2 \cdot 2^N)$ vs $O(N!)$)
* Given $N$ cities and distance matrix $D[N][N]$. Find minimum cost Hamiltonian Cycle visiting every city once and returning to origin.
* **Brute Force Permutation Cost**:
  - Total tour permutations: $(N - 1)!$.
  - For $N = 20$: $19! \approx 1.21 \times 10^{17}$ operations (Requires thousands of execution years!). ❌
* **Held-Karp Bitmask DP Cost**:
  - Subproblem State: $DP[\text{mask}][u]$ = Min cost to visit cities in `mask`, ending at city $u$.
  - Total States: $2^N \text{ masks} \times N \text{ ending cities} = N \cdot 2^N \text{ states}$.
  - Transitions per state: $O(N)$ candidate previous cities $v$.
  - Total Time Complexity:
    $$T(N) = O(N^2 \cdot 2^N)$$
  - For $N = 20$: $20^2 \cdot 2^{20} = 400 \cdot 1,048,576 \approx 4.19 \times 10^8$ operations (Executes in **under 0.5 Seconds**!).
  - Speedup Factor: Over $200,000,000\times$ FASTER! ⚡

---

## 4. Internal Working Mechanics: Smallest Sufficient Team Bitmask DP

Tracing LeetCode 1125 (Smallest Sufficient Team) with Skills Mask Target:

```
Target Skills Mask = (1 << S) - 1 (e.g. S=3 skills -> Target Mask = 7 [111_2]).

State Table: dp[skill_mask] = Min team size to cover skill_mask.
Base Case: dp[0] = 0, dp[1..7] = infinity.

Process Person p (Person's Skill Mask = p_skills):
For each existing skill_mask from 0 to Target:
  int new_mask = skill_mask | p_skills;
  if (dp[skill_mask] + 1 < dp[new_mask]) {
      dp[new_mask] = dp[skill_mask] + 1;
      parent[new_mask] = skill_mask;
      personUsed[new_mask] = p;
  }

Bitwise OR (|) accumulates covered skills in O(P * 2^S) Time! ✅ ⚡
```

---

## 5. Visual Diagram: Held-Karp State Transition Flow

```
Held-Karp TSP State Transitions (Target Mask = 1111_2 [Cities 0, 1, 2, 3]):

Visited Subset Mask = {0, 1, 2} (Mask 0111_2):
- Ending at City 1: DP[0111_2][1]
- Ending at City 2: DP[0111_2][2]

Transition to Add City 3 (Mask 1111_2):
DP[1111_2][3] = min( DP[0111_2][1] + dist[1][3],
                     DP[0111_2][2] + dist[2][3] ) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Held-Karp TSP, Partition to K Equal Sum Subsets (LeetCode 698), and Smallest Sufficient Team (LeetCode 1125).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bitmask Dynamic Programming:
 * Held-Karp TSP, Partition to K Equal Subsets, and Smallest Sufficient Team.
 */
public class BitmaskDPProblemsMaster {

    // =========================================================================
    // 1. TRAVELLING SALESPERSON PROBLEM (HELD-KARP O(N^2 * 2^N) Time, O(N * 2^N) Space)
    // =========================================================================
    /**
     * Solves Travelling Salesperson Problem using Held-Karp Bitmask DP.
     *
     * @param dist 2D adjacency matrix of edge distances
     * @return minimum tour distance starting and ending at city 0
     */
    public int solveTSP(int[][] dist) {
        if (dist == null || dist.length == 0) return 0;
        int n = dist.length;

        int finalMask = (1 << n) - 1; // All cities visited sentinel ⚡
        int[][] dp = new int[1 << n][n];
        for (int[] row : dp) Arrays.fill(row, Integer.MAX_VALUE / 2);

        // Base Case: Start at city 0 (Mask = 1 [0001_2])
        dp[1][0] = 0;

        // Iterate over all subset masks
        for (int mask = 1; mask <= finalMask; mask++) {
            for (int u = 0; u < n; u++) {
                if ((mask & (1 << u)) == 0 || dp[mask][u] >= Integer.MAX_VALUE / 2) continue;

                // Try transitioning to unvisited city v
                for (int v = 0; v < n; v++) {
                    if ((mask & (1 << v)) == 0) { // City v unvisited!
                        int nextMask = mask | (1 << v);
                        dp[nextMask][v] = Math.min(dp[nextMask][v], dp[mask][u] + dist[u][v]);
                    }
                }
            }
        }

        // Return min cost returning to origin city 0
        int minTour = Integer.MAX_VALUE;
        for (int u = 1; u < n; u++) {
            minTour = Math.min(minTour, dp[finalMask][u] + dist[u][0]);
        }

        return minTour;
    }

    // =========================================================================
    // 2. LEETCODE 698: PARTITION TO K EQUAL SUM SUBSETS (O(N * 2^N) Time)
    // =========================================================================
    /**
     * Checks if array can be partitioned into K subsets with equal sum.
     */
    public boolean canPartitionKSubsets(int[] nums, int k) {
        if (nums == null || nums.length < k) return false;

        int totalSum = 0;
        for (int num : nums) totalSum += num;
        if (totalSum % k != 0) return false;

        int target = totalSum / k;
        int n = nums.length;
        int finalMask = (1 << n) - 1;

        int[] dp = new int[1 << n];
        Arrays.fill(dp, -1);
        dp[0] = 0; // Base case: 0 sum

        for (int mask = 0; mask <= finalMask; mask++) {
            if (dp[mask] == -1) continue;

            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) == 0) { // Item i unused
                    if (dp[mask] + nums[i] <= target) {
                        int nextMask = mask | (1 << i);
                        dp[nextMask] = (dp[mask] + nums[i]) % target; // Reset remainder on bucket fill! ⚡
                    }
                }
            }
        }

        return dp[finalMask] == 0;
    }

    // =========================================================================
    // 3. LEETCODE 1125: SMALLEST SUFFICIENT TEAM (O(P * 2^S) Time)
    // =========================================================================
    /**
     * Solves Smallest Sufficient Team returning array of person indices.
     */
    public int[] smallestSufficientTeam(String[] req_skills, List<List<String>> people) {
        int s = req_skills.length;
        Map<String, Integer> skillMap = new HashMap<>();
        for (int i = 0; i < s; i++) skillMap.put(req_skills[i], i);

        int pCount = people.size();
        int[] personSkills = new int[pCount];
        for (int i = 0; i < pCount; i++) {
            int mask = 0;
            for (String skill : people.get(i)) {
                if (skillMap.containsKey(skill)) {
                    mask |= (1 << skillMap.get(skill));
                }
            }
            personSkills[i] = mask;
        }

        int totalMasks = 1 << s;
        long[] dp = new long[totalMasks]; // Store bitmask of person indices!
        Arrays.fill(dp, (1L << 60) - 1);  // Sentinel infinity
        dp[0] = 0;

        for (int mask = 0; mask < totalMasks; mask++) {
            if (dp[mask] == ((1L << 60) - 1)) continue;

            for (int i = 0; i < pCount; i++) {
                int combinedSkill = mask | personSkills[i];
                long candidateTeam = dp[mask] | (1L << i);

                if (Long.bitCount(candidateTeam) < Long.bitCount(dp[combinedSkill])) {
                    dp[combinedSkill] = candidateTeam;
                }
            }
        }

        long bestTeamMask = dp[totalMasks - 1];
        int teamSize = Long.bitCount(bestTeamMask);
        int[] res = new int[teamSize];
        int idx = 0;
        for (int i = 0; i < pCount; i++) {
            if ((bestTeamMask & (1L << i)) != 0) {
                res[idx++] = i;
            }
        }

        return res;
    }
}
```

> **Quick Syntax:**
```java
// Bitmask Subset Bit Check & Set Lines
if ((mask & (1 << i)) == 0) int nextMask = mask | (1 << i);
```

---

## 7. Concrete Problem Examples & Applications

1. **Travelling Salesperson Problem (TSP)**:
   - Held-Karp Bitmask DP benchmark ($O(N^2 \cdot 2^N)$ time).

2. **LeetCode 698 - Partition to K Equal Sum Subsets**:
   - Equal subset partitioning ($O(N \cdot 2^N)$ time).

3. **LeetCode 1125 - Smallest Sufficient Team**:
   - Team skill coverage optimization ($O(P \cdot 2^S)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class BitmaskDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BITMASK DYNAMIC PROGRAMMING BENCHMARK DEMO    ");
        System.out.println("=================================================\n");

        BitmaskDPProblemsMaster master = new BitmaskDPProblemsMaster();

        // 1. TSP Held-Karp Test
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };

        int minTour = master.solveTSP(dist);
        System.out.println("1. Travelling Salesperson (TSP) Held-Karp for 4 Cities:");
        System.out.println("   Minimum Tour Distance (O(N^2 * 2^N)): " + minTour + " Distance (Optimal = 80)");
        System.out.println("-------------------------------------------------");

        // 2. Partition K Subsets Test (LeetCode 698)
        int[] nums = {4, 3, 2, 3, 5, 2, 1};
        int k = 4;
        boolean canPart = master.canPartitionKSubsets(nums, k);
        System.out.println("2. LeetCode 698 Partition to " + k + " Equal Subsets:");
        System.out.println("   Can Partition: " + canPart + " (Target sum per subset = 5)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bitmask DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **TSP (Held-Karp)**    | $\mathbf{O(N^2 \cdot 2^N)}$ ⚡| $\mathbf{O(N \cdot 2^N)}$ Table| Full mask $(1 \ll N) - 1$ |
| **Partition K Subsets**| $\mathbf{O(N \cdot 2^N)}$ ⚡| $\mathbf{O(2^N)}$ Array ⚡| Remainder reset `(rem + val) % target` |
| **Smallest Team (1125)**| $\mathbf{O(P \cdot 2^S)}$ ⚡| $\mathbf{O(2^S)}$ Array ⚡| Bitwise OR `mask \| personSkills` |

---

## 10. Edge Cases & Boundary Handling

1. **Subset Size Exceeds 30 ($N > 30$)**:
   - Standard 32-bit `int` mask overflows. Use `long` mask for $N \le 60$, or switch to Branch-and-Bound / Approximation algorithms for $N > 60$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Operator Precedence in Bitwise Checks**:
  - Writing `if (mask & (1 << i) == 0)` causes syntax errors due to `==` having higher precedence than `&`. ALWAYS use parentheses: `if ((mask & (1 << i)) == 0)`!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Bitmask Threshold Limit:
> Bitmask Dynamic Programming is designed specifically for problems where subset size **$N \le 20$**! For $N \le 20$, $2^{20} \approx 10^6$ states, allowing linear state transitions to complete in under 0.5s! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Exponential Backtracking | Bitmask DP (Held-Karp) |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N!)$ Permutations ❌ | **$O(N^2 \cdot 2^N)$ Pseudo-Poly ⚡** |
| **State Caching** | None | Integer Mask Table ($O(2^N)$) |
| **Limit for N** | $N \le 12$ | **$N \le 20$ ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find shortest tour visiting all N cities (N <= 20)"** $\rightarrow$ TSP Held-Karp Bitmask DP.
* **"Partition array into K subsets with equal sum (N <= 16)"** $\rightarrow$ LeetCode 698.

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Bitmask DP limited to $N \le 20$?**  
  *A:* Because $2^N$ represents the state table size. For $N = 20$, $2^{20} = 1,048,576$ states. For $N = 30$, $2^{30} \approx 10^9$ states, which exceeds memory limits.

* **Q: How do you check if the $i$-th element is in a bitmask?**  
  *A:* `(mask & (1 << i)) != 0`.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BITMASK DP                                            |
+-----------------------------------------------------------------------+
| • Mask Invariant: Integer mask encodes subset (Bit 1 = included)       |
| • Bit Operations: Check bit -> (mask & (1<<i)) != 0; Set bit -> mask|(1<<i)|
| • TSP Held-Karp : dp[mask][u] = min(dp[mask \ {u}][v] + dist[v][u])   |
| • Subsets 698   : dp[nextMask] = (dp[mask] + val) % target            |
| • Limit Rule    : Applies when N <= 20 | O(N^2 * 2^N) Time ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Held-Karp TSP in $O(N^2 \cdot 2^N)$ time in Java.
- [ ] I can solve LeetCode 698 (`Partition to K Equal Sum Subsets`).
- [ ] I can solve LeetCode 1125 (`Smallest Sufficient Team`) using bitmask DP.
- [ ] I can write the 4 essential bitwise operations (check bit, set bit, clear bit, toggle bit).
- [ ] I can explain why Bitmask DP reduces $O(N!)$ brute force to $O(N^2 \cdot 2^N)$.
