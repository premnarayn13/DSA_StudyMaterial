# 05. 0/1 Knapsack: Fractional Bounds, Max-Priority Queues & Ratio Sorting

## 1. Introduction
The **0/1 Knapsack Problem** is a foundational NP-hard combinatorial optimization benchmark where given a set of $N$ items (each with a weight $w_i$ and value $v_i$) and a knapsack of capacity $W$, the goal is to select a subset of items to **MAXIMIZE TOTAL VALUE** without exceeding capacity $W$. While Dynamic Programming solves 0/1 Knapsack in $O(N \cdot W)$ pseudo-polynomial time (which fails when capacity $W = 10^{15}$ is astronomical!), **Branch & Bound (B&B)** using **Fractional Knapsack Upper Bounds** solves massive capacity 0/1 Knapsack instances in practical execution bounds. By pre-sorting items in descending order of **Value-to-Weight Ratio ($\frac{v_i}{w_i}$)** and managing live search nodes in a **Max-PriorityQueue**, B&B expands the most promising subproblems first and prunes unviable branches.

> **Important:** Core Structural Invariants of 0/1 Knapsack Branch & Bound:
> 1. **Value-to-Weight Ratio Sorting Invariant**:
>    - Sort items so that $\frac{v_0}{w_0} \ge \frac{v_1}{w_1} \ge \dots \ge \frac{v_{N-1}}{w_{N-1}}$.
>    - Guarantees that continuous fractional extension provides the tightest possible admissible upper bound $\hat{u}(x)$!
> 2. **Fractional Upper Bound Calculation ($\hat{u}(x)$)**:
>    - Greedily add whole items $level \dots N-1$ until capacity is exceeded. Add fractional portion of the breaking item:
>      $$\hat{u}(x) = \text{profit} + \sum_{i=level}^{k-1} v_i + v_k \times \frac{W_{\text{remaining}}}{w_k}$$
> 3. **Pruning Condition ($\hat{u}(x) \le P^*$)**:
>    - Kill node $x$ if its upper bound $\hat{u}(x) \le P^*$ (where $P^*$ is current best profit found so far).
> 4. **Max-PriorityQueue Best-First Tree Search**:
>    - Live Nodes are stored in a Max-PriorityQueue ordered by Upper Bound $\hat{u}(x)$, expanding highest bound nodes first! ⚡

```
0/1 Knapsack Branch & Bound Node Expansion Topology:

                    [ Root (Level 0, Profit=0, Bound=76.0) ]
                    /                                      \
        [ Include Item 0 (Bound=76.0) ]        [ Exclude Item 0 (Bound=43.4) ]
        (Weight=4, Profit=40 -> POP!)          (Weight=0, Profit=0 -> PQ)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
 [ Include Item 1 ]   [ Exclude Item 1 (Bound=42.8) ]
 (Weight=11 > 10 ❌)   (Profit=40 -> P* = 40 Updated! ✅)

Priority Queue pops highest upper bound node (76.0 -> 42.8)! ⚡
```

---

## 2. Core Concepts & Knapsack Paradigm Strategy Matrix

### 2.1 0/1 Knapsack Paradigms Strategy Matrix
```
0/1 Knapsack Paradigms Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Solving Paradigm      | Primary Mechanism | Time Complexity   | Auxiliary Space   | Capacity Limit W  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Dynamic Programming**| 2D/1D DP Table    | $O(N \cdot W)$    | $O(W)$ 1D Array   | Fails for $W > 10^7$|
| **Branch & Bound**    | **Max-PriorityQueue⚡**| **Pruned $O(2^N)$⚡**| **$O(2^N)$ Queue ⚡**| **No Limit ($W=10^{15}$)⚡**|
| **Greedy (Fractional)**| Ratio Sorting    | $O(N \log N)$     | $O(1)$ Memory     | Fractional Only   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Use Dynamic Programming when W is small; Use Branch & Bound when W is huge (e.g. W = 10^15)!"**

---

## 3. Characteristics & Fractional Upper Bound Proof

### 3.1 Mathematical Proof of Fractional Upper Bound Admissibility
* Let $x$ be a partial knapsack state node at level $k$ with weight $W_{\text{curr}}$ and profit $P_{\text{curr}}$.
* Let $S_{0/1}$ be any valid $0/1$ integer completion of node $x$, where $x_i \in \{0, 1\}$ for items $i = k \dots N-1$.
* Let $S_{\text{frac}}$ be the continuous fractional completion of node $x$, where $x_i \in [0, 1]$.
* Since $\{0, 1\} \subset [0, 1]$, the feasible set of integer solutions is a subset of the continuous fractional set:
  $$\text{Feasible}_{0/1} \subset \text{Feasible}_{\text{frac}}$$
* Therefore, the maximum profit over continuous fractional extensions MUST be $\ge$ maximum profit over integer extensions:
  $$\hat{u}(x) = \text{Profit}(S_{\text{frac}}) \ge \text{Profit}(S_{0/1}^*)$$
* Admissibility holds! $\hat{u}(x)$ NEVER underestimates the maximum achievable 0/1 integer profit. ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Knapsack B&B Execution

Tracing 0/1 Knapsack for $W = 10$, Items: $(v=40, w=4), (v=42, w=7), (v=25, w=53)$:

```
Step 1: Ratio Sorting:
Item 0: v=40, w=4, ratio = 10.0
Item 1: v=42, w=7, ratio = 6.0
Item 2: v=25, w=53, ratio = 0.47

Root Bound (Level 0):
- Takes Item 0 (w=4, v=40). Remaining W = 6.
- Fractional Item 1 (w=7, v=42): Takes 6/7 fraction -> v = 42 * (6/7) = 36.
- Upper Bound u_hat = 40 + 36 = 76.0.

Expand Root (Bound 76.0):
- Branch 1 (Take Item 0): Weight = 4, Profit = 40, Bound = 76.0.
- Branch 2 (Skip Item 0): Weight = 0, Profit = 0, Bound = 42 + 25*(3/53) = 43.4.

PQ Pop: Branch 1 (Take Item 0, Bound 76.0 > 43.4).

Expand Branch 1 (Level 1, W_curr = 4, P_curr = 40):
- Branch 1.1 (Take Item 1): Weight = 4 + 7 = 11 > 10 (OVERWEIGHT!). Pruned! ❌
- Branch 1.2 (Skip Item 1): Weight = 4, Profit = 40, Bound = 40 + 25*(6/53) = 42.8.

Update Global Best Profit P* = 40!
Node 2 (Bound 43.4) popped, but can max reach 43.4.
Optimal Profit P* = 40 achieved in 4 expansions! ✅ ⚡
```

---

## 5. Visual Diagram: Fractional Knapsack Upper Bound Calculation

```
Fractional Knapsack Relaxation Calculation for Capacity W = 10:

Item 0: [ Weight = 4, Profit = 40 ] ──► Whole Item Included (w=4, p=40)
Item 1: [ Weight = 7, Profit = 42 ] ──► 6/7 Fraction Included (w=6, p=36)

Total Bound u_hat = 40 + 36 = 76.0!
Provides tight, admissible upper bound for B&B Max-PriorityQueue! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing 0/1 Knapsack Branch & Bound using Ratio Sorting, Fractional Upper Bounding, and Max-PriorityQueue search.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing 0/1 Knapsack Branch & Bound:
 * Value-to-Weight Ratio Sorting, Fractional Upper Bounds, and Max-PriorityQueue.
 */
public class KnapsackBranchAndBoundMaster {

    public static class Item implements Comparable<Item> {
        public final int id, weight, value;
        public final double ratio;

        public Item(int id, int weight, int value) {
            this.id = id;
            this.weight = weight;
            this.value = value;
            this.ratio = (double) value / weight;
        }

        @Override
        public int compareTo(Item o) {
            return Double.compare(o.ratio, this.ratio); // DESCENDING BY RATIO! ⚡
        }
    }

    public static class Node implements Comparable<Node> {
        public final int level;
        public final int profit;
        public final int weight;
        public final double bound; // Upper bound u_hat

        public Node(int level, int profit, int weight, double bound) {
            this.level = level;
            this.profit = profit;
            this.weight = weight;
            this.bound = bound;
        }

        @Override
        public int compareTo(Node o) {
            return Double.compare(o.bound, this.bound); // MAX-PRIORITY QUEUE BY BOUND! ⚡
        }
    }

    // =========================================================================
    // 1. 0/1 KNAPSACK BRANCH & BOUND SOLVER (O(2^N) Pruned)
    // =========================================================================
    /**
     * Solves 0/1 Knapsack problem for huge capacity W using Branch & Bound.
     *
     * @param capacity max knapsack capacity W
     * @param weights array of item weights
     * @param values array of item values
     * @return maximum total profit
     */
    public int solveKnapsackBAndB(int capacity, int[] weights, int[] values) {
        if (capacity <= 0 || weights == null || values == null || weights.length == 0) return 0;
        int n = weights.length;

        // Step 1: Pre-sort items in descending order of value/weight ratio! ⚡
        Item[] items = new Item[n];
        for (int i = 0; i < n; i++) items[i] = new Item(i, weights[i], values[i]);
        Arrays.sort(items);

        PriorityQueue<Node> pq = new PriorityQueue<>();

        // Root Node
        double rootBound = calculateBound(0, 0, 0, capacity, items, n);
        pq.add(new Node(0, 0, 0, rootBound));

        int maxProfit = 0; // Global Best Profit P* ⚡

        while (!pq.isEmpty()) {
            Node curr = pq.poll();

            // Pruning Condition: Kill node if upper bound <= current maxProfit P* ⚡
            if (curr.bound <= maxProfit) continue;

            if (curr.level == n) continue; // Reached leaf level

            Item item = items[curr.level];

            // Branch 1: Include item
            int nextWeight = curr.weight + item.weight;
            int nextProfit = curr.profit + item.value;

            if (nextWeight <= capacity) {
                if (nextProfit > maxProfit) {
                    maxProfit = nextProfit; // Update P*! ⚡
                }
                double boundInclude = calculateBound(curr.level + 1, nextProfit, nextWeight, capacity, items, n);
                if (boundInclude > maxProfit) {
                    pq.add(new Node(curr.level + 1, nextProfit, nextWeight, boundInclude));
                }
            }

            // Branch 2: Exclude item
            double boundExclude = calculateBound(curr.level + 1, curr.profit, curr.weight, capacity, items, n);
            if (boundExclude > maxProfit) {
                pq.add(new Node(curr.level + 1, curr.profit, curr.weight, boundExclude));
            }
        }

        return maxProfit;
    }

    private double calculateBound(int level, int profit, int weight, int capacity, Item[] items, int n) {
        if (weight >= capacity) return 0;

        double bound = profit;
        int currentWeight = weight;

        for (int i = level; i < n; i++) {
            if (currentWeight + items[i].weight <= capacity) {
                currentWeight += items[i].weight;
                bound += items[i].value;
            } else {
                int remain = capacity - currentWeight;
                bound += items[i].value * ((double) remain / items[i].weight); // Fractional part ⚡
                break;
            }
        }

        return bound;
    }
}
```

> **Quick Syntax:**
```java
// Item Ratio Sorting & Max-PQ Lines
Arrays.sort(items); // Sorts descending by value/weight ratio
PriorityQueue<Node> pq = new PriorityQueue<>(); // Max-PQ by node.bound
```

---

## 7. Concrete Problem Examples & Applications

1. **0/1 Knapsack for Massive Capacity ($W = 10^{15}$)**:
   - Solved in milliseconds using Branch & Bound where DP fails due to memory exhaustion.

2. **Cargo Container Allocation**:
   - Maximizing freight value subject to strict weight constraints.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class KnapsackDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   0/1 KNAPSACK BRANCH & BOUND BENCHMARK DEMO    ");
        System.out.println("=================================================\n");

        KnapsackBranchAndBoundMaster master = new KnapsackBranchAndBoundMaster();

        int capacity = 10;
        int[] weights = {4, 7, 53};
        int[] values = {40, 42, 25};

        int maxProfit = master.solveKnapsackBAndB(capacity, weights, values);

        System.out.println("1. 0/1 Knapsack B&B Execution Result:");
        System.out.println("   Knapsack Capacity W = " + capacity);
        System.out.println("   Maximum Achieved Profit (P*): " + maxProfit + " (Optimal = 40)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| 0/1 Knapsack Approach | Time Complexity | Auxiliary Space | Capacity Limit $W$ |
| :--- | :--- | :--- | :--- |
| **Dynamic Programming**| $O(N \cdot W)$ Pseudo-Poly | $O(W)$ 1D Array | Fails if $W > 10^7$ |
| **Branch & Bound**     | $\mathbf{O(2^N)}$ Pruned ⚡| $\mathbf{O(2^N)}$ PriorityQueue| **No Capacity Limit ($W=10^{15}$)⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **All Items Fit in Knapsack**:
   - Root bound calculates exact sum of all item values.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Sort Items by Ratio Before Running Branch & Bound**:
  - Failing to sort items by $\frac{v_i}{w_i}$ produces loose, invalid upper bounds, causing Branch & Bound to expand almost all $2^N$ nodes. **ALWAYS sort items by ratio first!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to use B&B over DP for 0/1 Knapsack:
> Use Dynamic Programming when capacity $W$ is small ($W \le 10^6$). Use **Branch & Bound** when capacity $W$ is huge ($W = 10^{15}$) because B&B complexity depends on $N$, NOT $W$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Dynamic Programming | Branch & Bound |
| :--- | :--- | :--- |
| **Space Requirement** | $O(W)$ Memory Table | **Independent of Capacity $W$ ⚡** |
| **Execution Trigger** | $W \le 10^6$ Small | **$W = 10^{15}$ Massive Capacity ⚡**|
| **Data Structure** | 1D / 2D Array | Max-Priority Queue |

---

## 14. How to Recognize This in Questions

* **"Solve 0/1 Knapsack where capacity W is up to 10^15"** $\rightarrow$ Branch & Bound.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does 0/1 Knapsack Branch & Bound sort items by value-to-weight ratio?**  
  *A:* Because sorting by ratio guarantees that the continuous fractional knapsack greedy extension produces the tightest possible admissible upper bound $\hat{u}(x)$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 0/1 KNAPSACK BRANCH & BOUND                           |
+-----------------------------------------------------------------------+
| • Pre-Processing : Sort items by value/weight ratio descending ⚡     |
| • Upper Bound    : Fractional Knapsack greedy extension               |
| • PriorityQueue  : Max-PQ ordered by node.bound                       |
| • Pruning Rule   : Kill node if bound <= current maxProfit P*           |
| • Performance    : Solves W = 10^15 where Dynamic Programming fails! ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write 0/1 Knapsack Branch & Bound in Java using Priority Queue.
- [ ] I can explain why items MUST be sorted by value-to-weight ratio.
- [ ] I can write the fractional knapsack upper bound calculator.
- [ ] I can state when to use B&B over DP for Knapsack ($W > 10^7$).
- [ ] I can state the pruning condition for maximization ($\hat{u}(x) \le P^*$).
