# 09. Optimal Binary Search Trees (OBST), Access Frequency Cost Minimization & DP Formulations

## 1. Introduction
An **Optimal Binary Search Tree (OBST)** is a static Binary Search Tree constructed for a known set of $N$ keys $K_1 < K_2 < \dots < K_N$ with corresponding search access probabilities (frequencies) $p_1, p_2, \dots, p_N$. The goal is to build a valid BST that **minimizes the Expected Search Cost**:

$$\text{Expected Search Cost} = \sum_{i=1}^{N} p_i \cdot (1 + \text{depth}(K_i))$$

By evaluating candidate root choices across all contiguous key ranges using **Dynamic Programming (DP)**, the Optimal BST algorithm computes the minimum search cost in **$O(N^3)$ time** (optimizable to **$O(N^2)$ time** using Knuth's Optimization) and **$O(N^2)$ auxiliary space**.

> **Important:** Why does a Balanced BST NOT always yield the minimum search cost?
> If key frequencies are skewed (e.g. key $K_1$ is queried 90% of the time, while keys $K_2 \dots K_N$ are queried 1% of the time):
> Placing $K_1$ at the **ROOT** (depth 0) reduces the average search cost to near $O(1)$, even if it creates an unbalanced tree topology! ⚡

```
Balanced BST vs Optimal BST Topology (Key Frequencies: K1: 90%, K2: 5%, K3: 5%):
Balanced BST (Root K2):                    Optimal BST (Root K1):
          [ K2 (5%) ]                             [ K1 (90%) ]  <--- Querying K1 takes 1 step!
         /          \                                        \
   [ K1 (90%) ]   [ K3 (5%) ]                               [ K2 (5%) ]
                                                               \
                                                              [ K3 (5%) ]
Expected Cost: 0.9*2 + 0.05*1 + 0.05*2 = 1.95    Expected Cost: 0.9*1 + 0.05*2 + 0.05*3 = 1.15! ⚡
```

---

## 2. Core Concepts & Dynamic Programming Formulation

### 2.1 The DP Recurrence Relation
Let $dp[i][j]$ be the minimum expected search cost for key sequence $K_i, \dots, K_j$:
* **Choice**: Pick key $K_k$ ($i \le k \le j$) as the root of the subtree.
* When $K_k$ becomes root, all nodes in the left subtree ($K_i \dots K_{k-1}$) and right subtree ($K_{k+1} \dots K_j$) move 1 level deeper, increasing their total cost by the sum of their probabilities $\sum_{m=i}^{j} p_m$!

$$\mathbf{dp[i][j] = w(i, j) + \min_{i \le k \le j} \left( dp[i][k-1] + dp[k+1][j] \right)}$$

where $w(i, j) = \sum_{m=i}^{j} p_m$ is the total weight (sum of frequencies) from index $i$ to $j$.

```
Optimal BST Strategy Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| OBST Strategy         | Time Complexity   | Auxiliary Space   | Key Optimization  |
+-----------------------+-------------------+-------------------+-------------------+
| **Standard DP**       | **$O(N^3)$ ⚡**   | $O(N^2)$ DP Table | Range length $L = 1 \dots N$|
| Knuth's Optimization  | **$O(N^2)$ ⚡**   | $O(N^2)$ DP Table | Monotonic root bounds $opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"OBST DP Formula: dp[i][j] = w(i, j) + min_k(dp[i][k-1] + dp[k+1][j])! w(i, j) is the sum of frequencies!"**

---

## 3. Characteristics & Knuth's $O(N^2)$ Optimization

### 3.1 Knuth's Optimization on OBST
The optimal root choice $opt[i][j]$ for range $[i..j]$ is monotonically bounded by the optimal roots of its sub-problems:

$$opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$$

Restricting the inner loop search for root $k$ to $[opt[i][j-1] \dots opt[i+1][j]]$ reduces total time complexity from $O(N^3)$ down to **$O(N^2)$ Linear-Quadratic Time**! ⚡

---

## 4. Internal Working Mechanics
Tracing Optimal BST DP on Keys `[10, 20, 30]` with Frequencies `[34, 8, 50]`:

```
Init: N = 3. Keys: [10, 20, 30], Freqs: [34, 8, 50].

Base Cases (Length L = 1):
- dp[0][0] = 34 (Key 10)
- dp[1][1] = 8  (Key 20)
- dp[2][2] = 50 (Key 30)

Length L = 2:
- dp[0][1] (Range 10..20, weight 34+8=42):
    - k=0 (root 10): 0 + dp[1][1] = 8  -> Total = 42 + 8 = 50.
    - k=1 (root 20): dp[0][0] + 0 = 34 -> Total = 42 + 34 = 76.
    - min = 50 (Root 10).

- dp[1][2] (Range 20..30, weight 8+50=58):
    - k=1 (root 20): min = 58 + 50 = 108.
    - k=2 (root 30): min = 58 + 8 = 66 (Root 30).

Length L = 3 (Full Range 0..2):
- dp[0][2] (weight 34+8+50=92):
    - k=0 (root 10): 92 + 0 + 66 = 158.
    - k=1 (root 20): 92 + 34 + 50 = 176.
    - k=2 (root 30): 92 + 50 + 0 = 142 (Root 30!).

Minimum Expected Cost = 142! Root of Optimal BST is Key 30! ✅ (O(N^3) DP!)
```

---

## 5. Visual Diagram
Optimal BST DP Sub-problem Range Partition Topography:

```
Range [i ... j]:                [ Key K_k (Chosen Root) ]
                               /                         \
              Left Subtree [i ... k-1]          Right Subtree [k+1 ... j]
              (Depth increases by 1)            (Depth increases by 1)

Cost Addition = w(i, j) + dp[i][k-1] + dp[k+1][j] ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Optimal Binary Search Tree using Dynamic Programming ($O(N^3)$ Time, $O(N^2)$ Space):

```java
import java.util.*;

public class OptimalBSTMaster {

    // 1. Optimal BST Search Cost Dynamic Programming O(N^3) Time, O(N^2) Space
    public static int optimalSearchTree(int[] keys, int[] freq, int n) {
        // dp[i][j] stores minimum cost for keys[i...j]
        int[][] dp = new int[n][n];

        // Base Case: Subtrees of length 1
        for (int i = 0; i < n; i++) {
            dp[i][i] = freq[i];
        }

        // Iterate over subtree range lengths L = 2 to n
        for (int L = 2; L <= n; L++) {
            for (int i = 0; i <= n - L; i++) {
                int j = i + L - 1;
                dp[i][j] = Integer.MAX_VALUE;

                // Compute sum of frequencies for range [i...j]
                int weightSum = getWeightSum(freq, i, j);

                // Try each key K_k (i <= k <= j) as the root
                for (int k = i; k <= j; k++) {
                    int leftCost = (k > i) ? dp[i][k - 1] : 0;
                    int rightCost = (k < j) ? dp[k + 1][j] : 0;

                    int totalCost = weightSum + leftCost + rightCost;
                    dp[i][j] = Math.min(dp[i][j], totalCost);
                }
            }
        }

        return dp[0][n - 1]; // Minimum cost for full range [0...n-1]
    }

    private static int getWeightSum(int[] freq, int i, int j) {
        int sum = 0;
        for (int k = i; k <= j; k++) {
            sum += freq[k];
        }
        return sum;
    }
}
```

> **Quick Syntax:**
```java
// Optimal BST DP Inner Recurrence Line
int totalCost = weightSum + ((k > i) ? dp[i][k-1] : 0) + ((k < j) ? dp[k+1][j] : 0);
dp[i][j] = Math.min(dp[i][j], totalCost);
```

---

## 7. Concrete Problem Examples
* **Compiler Keyword Lookup Tables**: Structuring language keywords in an OBST based on usage frequencies.
* **Database Query Cache Indexing**: Frequently searched record keys placed near root.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `optimalSearchTree`:

```java
public class OptimalBSTDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Optimal BST Search Cost DP Test ===");
        int[] keys = {10, 20, 30};
        int[] freq = {34, 8, 50};

        int minCost = OptimalBSTMaster.optimalSearchTree(keys, freq, keys.length);
        System.out.println("Minimum Expected Search Cost: " + minCost);
        // Output: 142 (Root = 30) ✅
    }
}
```

---

## 9. Complexity Analysis

| Implementation Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Standard DP Solution**| **$O(N^3)$ Cubic ⚡** | **$O(N^2)$ DP Table** | Range length $L = 2 \dots N$ |
| **Knuth's Optimization**| **$O(N^2)$ Quadratic ⚡**| **$O(N^2)$ DP Table** | Monotonic root bounds $opt[i][j]$ |

---

## 10. Edge Cases & Boundary Handling
* **Single Key ($N = 1$)**: Search cost is equal to `freq[0]` (depth 0).
* **Zero Frequency Keys**: Handled correctly by DP weight summation.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Add Range Weight Sum $w(i, j)$**:
  - Failing to add $w(i, j) = \sum_{m=i}^{j} \text{freq}[m]$ neglects the cost increase experienced by subtrees when moved 1 level deeper!
  - **ALWAYS add $w(i, j)$ to the minimum child subtree costs**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why $w(i, j)$ is Added to Subtree Costs:
> When key $K_k$ is chosen as the root for sub-problem $[i..j]$:
> All nodes in the left subtree $[i..k-1]$ and right subtree $[k+1..j]$ move down 1 depth level.
> Moving down 1 level increases every node's search depth by $+1$, which increases the expected cost by $1 \times \text{freq}$ for EVERY node in the range!
> Adding $w(i, j) = \sum_{m=i}^{j} \text{freq}[m]$ captures this depth increment automatically!

> **Memory Trick:** **"Moving subtrees down 1 level increases cost by w(i, j) = sum of frequencies in range!"**

---

## 13. System & Implementation Comparisons

| Feature | Optimal BST (OBST) | Height-Balanced BST (AVL) |
| :--- | :--- | :--- |
| **Optimization Target** | **Expected Search Cost (Frequency-Weighted) ⚡**| Maximum Path Length ($H \le 1.44 \log_2 N$) |
| **Input Requirement** | Requires Known Access Frequencies | Frequency-Agonistic |
| **Construction Time** | $O(N^3)$ DP Pre-computation | **$O(N \log N)$ Dynamic Rotations ⚡** |

---

## 14. How to Recognize This in Questions
* **"Construct a BST for known key access probabilities to minimize average search cost"** $\rightarrow$ Optimal BST (OBST DP).

---

## 15. Frequently Asked Interview Questions
* **Q: Can an Optimal BST be skewed?**  
  *A:* Yes! If one key has a dominant search probability (e.g. 99%), placing it at the root yields the lowest average search cost, even if remaining low-frequency keys form a skewed chain.
* **Q: How does Knuth's Optimization reduce OBST time complexity to $O(N^2)$?**  
  *A:* By proving that the optimal root $opt[i][j]$ satisfies $opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$, eliminating redundant inner loop iterations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: OPTIMAL BINARY SEARCH TREES (OBST)                    |
+-----------------------------------------------------------------------+
| • Objective : Minimize Expected Search Cost = Sum(freq * depth)       |
| • DP Formula: dp[i][j] = w(i, j) + min_k(dp[i][k-1] + dp[k+1][j])      |
| • Weight Sum: w(i, j) = Sum of frequencies from index i to j          |
| • Time Bounds : Standard DP O(N^3) | Knuth's Optimized O(N^2) ⚡        |
| • Space Bounds: O(N^2) DP Table Memory                                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Optimal BST DP recurrence relation.
- [ ] I can write the $O(N^3)$ OBST DP algorithm in Java.
- [ ] I know why $w(i, j)$ is added to subtree costs.
- [ ] I know why an OBST may be unbalanced.
- [ ] I can state Knuth's Optimization monotonic root property.
