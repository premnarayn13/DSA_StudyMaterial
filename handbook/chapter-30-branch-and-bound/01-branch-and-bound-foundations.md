# 01. Branch & Bound Foundations: Optimization Spaces, Bound Functions & Best-First Search

## 1. Introduction
**Branch & Bound (B&B)** is an algorithmic design paradigm specifically tailored for solving discrete NP-hard combinatorial optimization problems (e.g. 0/1 Knapsack, Traveling Salesperson Problem, Job Assignment Problem). Unlike Backtracking (which explores search trees via Depth-First Search to find all valid discrete constraint solutions), Branch & Bound systematically explores state space trees using **Best-First Search (Priority Queue)** or **Breadth-First Search (FIFO Queue)**, applying two core operational mechanics: (1) **Branching**: Dividing a candidate decision node $u$ into smaller subproblems (child nodes), and (2) **Bounding**: Computing a optimistic theoretical **Upper Bound $\hat{u}(x)$** (for maximization) or **Lower Bound $\hat{l}(x)$** (for minimization) to determine the best possible solution achievable from node $x$. If a node's optimistic bound cannot beat the cost of the best solution found so far ($C^*$), node $x$ is killed immediately (pruned).

> **Important:** Core Structural Invariants of Branch & Bound:
> 1. **Best-First Priority Queue Invariant**:
>    - Live Nodes are stored in a Max-PriorityQueue (for maximization) or Min-PriorityQueue (for minimization) ordered by their optimistic bound $\hat{c}(x)$.
>    - Always expands the most promising node first, reaching optimal solutions orders of magnitude faster than blind DFS!
> 2. **Optimistic Bound Function Calculation**:
>    - Minimization: $\hat{l}(x) \le \text{True Optimal Cost achievable from node } x$.
>    - Maximization: $\hat{u}(x) \ge \text{True Optimal Profit achievable from node } x$.
> 3. **The Killing / Pruning Condition**:
>    - Minimization: Kill node $x$ if $\hat{l}(x) \ge C^*$ (where $C^*$ is current best solution cost).
>    - Maximization: Kill node $x$ if $\hat{u}(x) \le P^*$ (where $P^*$ is current best solution profit). ⚡

```
Branch & Bound Priority Queue Traversal Topology:

                      [ Root Node (Bound = 100) ]
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
       [ Child A (Bound = 120) ]       [ Child B (Bound = 85) ]
       (Promising Node -> Expanded!)   (Less Promising -> Queued)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
[ Child A1 (115) ]   [ Child A2 (80) ] ❌ (Pruned if P* = 90!)

Priority Queue selects highest bound node first (Child A -> A1 -> B)! ⚡
```

---

## 2. Core Concepts & Branch & Bound Strategy Matrix

### 2.1 Optimization Paradigm Comparison Matrix
```
Optimization Paradigm Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithmic Paradigm  | Traversal Engine  | Node Selection    | Pruning Mechanism | Ideal Application |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Backtracking**      | **DFS Call Stack⚡**| Deepest First     | Constraint Checks | Satisfiability    |
| **Branch & Bound**    | **Priority Queue⚡**| **Best Bound First⚡**| **Upper/Lower Bound⚡**| **Optimization ⚡**|
| **Dynamic Programming**| Subproblem DAG    | Topological Order | Overlapping Sub   | Polynomial Time   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Branch & Bound uses Priority Queue ordered by optimistic bound; Prunes if node bound cannot beat current best C* / P*!"**

---

## 3. Characteristics & Bounding Function Proof

### 3.1 Mathematical Formalism of Branch & Bound
* Let $P$ be a maximization problem with objective function $f(S)$.
* Let $P^*$ be the maximum valid profit achieved by any complete leaf solution generated so far ($P^* = \max f(S_{\text{leaf}})$).
* For any partial decision node $x$, let $\hat{u}(x)$ be an **Admissible Upper Bound** on the maximum profit achievable by extending node $x$.
* **Admissibility Requirement**:
  $$\hat{u}(x) \ge \max_{S \in \text{Subtree}(x)} f(S)$$
* **The B&B Pruning Theorem**:
  - If $\hat{u}(x) \le P^*$, then for all complete solutions $S \in \text{Subtree}(x)$, $f(S) \le \hat{u}(x) \le P^*$.
  - Therefore, no solution in the subtree of $x$ can strictly improve upon $P^*$. Node $x$ can be safely killed without expanding its children, guaranteeing global optimality! ⚡

---

## 4. Internal Working Mechanics: Branch & Bound 0/1 Knapsack Priority Queue Engine

Tracing Branch & Bound 0/1 Knapsack ($W = 10$, Items: $(v=40, w=4), (v=42, w=7), (v=25, w=53)$):

```
Bounding Function: Fractional Knapsack Upper Bound!

Root Node (Level 0):
- Taken = {}, Weight = 0, Profit = 0.
- Fractional Upper Bound = 40 + 42 + (25 * (10 - 11)/53) -> Cap 10: 40 + 42*(6/7) = 40 + 36 = 76.
- Queue Node(Profit=0, Bound=76).

Expand Root (Bound 76):
- Branch 1 (Take Item 0): Weight = 4, Profit = 40, Bound = 40 + 42*(6/7) = 76.
- Branch 2 (Skip Item 0): Weight = 0, Profit = 0, Bound = 42 + 25*(3/53) = 43.4.

Priority Queue Pop: Branch 1 (Bound 76 > 43.4)!

Expand Branch 1 (Weight 4, Profit 40):
- Branch 1.1 (Take Item 1): Weight = 11 > 10 (OVERWEIGHT!). Killed! ❌
- Branch 1.2 (Skip Item 1): Weight = 4, Profit = 40, Bound = 40 + 25*(6/53) = 42.8.

Update Best Profit P* = 40. Node 2 (Bound 43.4) popped next...
Optimal Profit P* = 40 achieved in 4 expansions! ✅ ⚡
```

---

## 5. Visual Diagram: Priority Queue B&B Execution Tree

```
Priority Queue State Tree Traversal:

                 [ Node 0 (Bound = 76) ]
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
[ Node 1 (Bound = 76) ]         [ Node 2 (Bound = 43.4) ]
(Item 0 Taken)                   (Item 0 Skipped)
         │
 ┌───────┴───────┐
 ▼               ▼
[ Overweight ] [ Node 1.2 (Bound = 42.8) ]
 (Killed ❌)    (Best Profit P* = 40 Updated!)

Priority Queue guarantees minimal node expansions! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Branch & Bound Foundations, Priority Queue Node Selectors, and Upper/Lower Bound Evaluators.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Branch & Bound Foundations:
 * Priority Queue Best-First Search, Bounding Functions, and Pruning Engines.
 */
public class BranchAndBoundFoundationsMaster {

    public static class BBNode implements Comparable<BBNode> {
        public final int id;
        public final int level;
        public final int profit;
        public final int weight;
        public final double bound; // Optimistic upper bound ⚡

        public BBNode(int id, int level, int profit, int weight, double bound) {
            this.id = id;
            this.level = level;
            this.profit = profit;
            this.weight = weight;
            this.bound = bound;
        }

        @Override
        public int compareTo(BBNode o) {
            return Double.compare(o.bound, this.bound); // MAX-PRIORITY QUEUE BY BOUND! ⚡
        }
    }

    public static class Item {
        public final int weight, value;
        public final double ratio;
        public Item(int weight, int value) {
            this.weight = weight;
            this.value = value;
            this.ratio = (double) value / weight;
        }
    }

    // =========================================================================
    // 1. BRANCH & BOUND 0/1 KNAPSACK SOLVER (BEST-FIRST PRIORITY QUEUE)
    // =========================================================================
    /**
     * Solves 0/1 Knapsack using Priority Queue Branch & Bound.
     *
     * @param capacity max knapsack capacity W
     * @param weights array of item weights
     * @param values array of item values
     * @return maximum achievable profit
     */
    public int solveKnapsackBranchAndBound(int capacity, int[] weights, int[] values) {
        if (capacity <= 0 || weights == null || values == null || weights.length == 0) return 0;
        int n = weights.length;

        // Step 1: Sort items by Value-to-Weight ratio descending! ⚡
        Item[] items = new Item[n];
        for (int i = 0; i < n; i++) items[i] = new Item(weights[i], values[i]);
        Arrays.sort(items, (a, b) -> Double.compare(b.ratio, a.ratio));

        PriorityQueue<BBNode> pq = new PriorityQueue<>();
        int nodeId = 0;

        // Root Node Calculation
        double rootBound = calculateBound(0, 0, 0, capacity, items, n);
        BBNode root = new BBNode(nodeId++, 0, 0, 0, rootBound);
        pq.add(root);

        int maxProfit = 0; // Global Best Profit P* ⚡

        while (!pq.isEmpty()) {
            BBNode curr = pq.poll();

            // Kills node if its optimistic bound cannot beat current maxProfit P*! ⚡
            if (curr.bound <= maxProfit) continue;

            int level = curr.level;
            if (level == n) continue; // Reached leaf

            Item nextItem = items[level];

            // Branch 1: Include nextItem
            int nextWeight = curr.weight + nextItem.weight;
            int nextProfit = curr.profit + nextItem.value;

            if (nextWeight <= capacity) {
                if (nextProfit > maxProfit) {
                    maxProfit = nextProfit; // Update best P*! ⚡
                }
                double boundInclude = calculateBound(level + 1, nextProfit, nextWeight, capacity, items, n);
                if (boundInclude > maxProfit) {
                    pq.add(new BBNode(nodeId++, level + 1, nextProfit, nextWeight, boundInclude));
                }
            }

            // Branch 2: Exclude nextItem
            double boundExclude = calculateBound(level + 1, curr.profit, curr.weight, capacity, items, n);
            if (boundExclude > maxProfit) {
                pq.add(new BBNode(nodeId++, level + 1, curr.profit, curr.weight, boundExclude));
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
                bound += items[i].value * ((double) remain / items[i].weight); // Fractional knapsack bound! ⚡
                break;
            }
        }

        return bound;
    }
}
```

> **Quick Syntax:**
```java
// Branch & Bound Priority Queue Max-Bound Line
PriorityQueue<BBNode> pq = new PriorityQueue<>((a, b) -> Double.compare(b.bound, a.bound));
```

---

## 7. Concrete Problem Examples & Applications

1. **0/1 Knapsack Branch & Bound**:
   - Best-first search knapsack solver using fractional bounds ($O(2^N)$ worst, fast pruned).

2. **Traveling Salesperson Problem (TSP)**:
   - Matrix reduction lower bounds for TSP tour optimization.

3. **Job Shop Scheduling & Resource Allocation**:
   - Minimizing total completion time under machine constraints.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class BranchAndBoundFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BRANCH & BOUND FOUNDATIONS BENCHMARK DEMO     ");
        System.out.println("=================================================\n");

        BranchAndBoundFoundationsMaster master = new BranchAndBoundFoundationsMaster();

        int capacity = 10;
        int[] weights = {4, 7, 53};
        int[] values = {40, 42, 25};

        int maxProfit = master.solveKnapsackBranchAndBound(capacity, weights, values);

        System.out.println("1. 0/1 Knapsack Branch & Bound Solver:");
        System.out.println("   Knapsack Capacity W = " + capacity);
        System.out.println("   Maximum Achievable Profit (P*): " + maxProfit + " (Optimal = 40)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Branch & Bound Algorithm | Traversal Strategy | Worst-Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **0/1 Knapsack B&B** | Best-First PriorityQueue| $O(2^N)$ Pruned | $O(2^N)$ Queue Space| Fractional upper bound |
| **Job Assignment B&B** | Best-First PriorityQueue| $O(N!)$ Pruned | $O(N!)$ Queue Space | Matrix reduction bound |

---

## 10. Edge Cases & Boundary Handling

1. **Capacity Exceeded at Root**:
   - `calculateBound` returns `0` if initial weight exceeds capacity.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using FIFO Queue (BFS) Instead of Priority Queue (Best-First)**:
  - Using a plain FIFO Queue expands level by level without regard to node quality, degrading performance toward brute-force BFS. **ALWAYS use a Priority Queue ordered by optimistic bound!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Branch & Bound Priority Queue Rule:
> For Maximization problems, store live nodes in a **Max-PriorityQueue** ordered by Upper Bound $\hat{u}(x)$. For Minimization problems, store live nodes in a **Min-PriorityQueue** ordered by Lower Bound $\hat{l}(x)$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Backtracking (DFS) | Branch & Bound (Best-First) |
| :--- | :--- | :--- |
| **Data Structure** | Call Stack ($O(H)$) | **Priority Queue ($O(2^N)$) ⚡** |
| **Target Problem** | Constraint Satisfaction | **Combinatorial Optimization ⚡**|
| **Node Order** | Deepest Node First | **Most Promising Bound First ⚡**|

---

## 14. How to Recognize This in Questions

* **"Find optimal solution for NP-hard optimization problem using upper/lower bounds"** $\rightarrow$ Branch & Bound.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the main difference between Backtracking and Branch & Bound?**  
  *A:* Backtracking uses Depth-First Search (stack) to solve constraint satisfaction problems, while Branch & Bound uses Best-First Search (Priority Queue) with optimistic bounds to solve optimization problems.

* **Q: Why does 0/1 Knapsack B&B use Fractional Knapsack to calculate upper bounds?**  
  *A:* Because Fractional Knapsack relaxes the 0/1 integer constraint, providing a quick, optimistic upper bound that is guaranteed to be $\ge$ the true 0/1 integer optimal profit.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BRANCH & BOUND FOUNDATIONS                            |
+-----------------------------------------------------------------------+
| • Core Mechanics : Branching (Split subproblems) + Bounding (Bound)   |
| • Node Queue     : Best-First Search via Priority Queue (Max/Min) ⚡  |
| • Pruning Rule   : Maximization -> Kill if bound <= maxProfit P*      |
| • Knapsack Bound : Uses Fractional Knapsack value/weight ratio        |
| • Performance    : Solves NP-hard optimization faster than DFS! ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can explain the difference between Backtracking and Branch & Bound.
- [ ] I can write 0/1 Knapsack Branch & Bound in Java using Priority Queue.
- [ ] I can explain why Fractional Knapsack provides an admissible upper bound.
- [ ] I can state the pruning condition for maximization ($\hat{u}(x) \le P^*$).
- [ ] I can state why Priority Queue is preferred over FIFO Queue.
