# 10. Master Reference — Branch & Bound Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 28: Branch & Bound**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Branch & Bound Foundations, State Space Trees (FIFO, LIFO, LC-B&B), Bounding Functions (Admissibility, LP Relaxation, Matrix Reductions), Job Assignment Problem, 0/1 Knapsack Branch & Bound, Travelling Salesperson Problem (TSP), Search Strategies (DFB&B vs LC-B&B), Architectural Comparison with Backtracking & Dynamic Programming, Advanced Optimizations (Warm-Starting, Dominance Pruning, Memory Bounding), and Master B&B Reference Patterns.

> **Important:** Review this master reference 15 minutes before an interview to refresh the Branch & Bound Principle (Branching + Bounding), Admissibility condition ($\hat{l}(x) \le C^*$ for min; $\hat{u}(x) \ge P^*$ for max), Monotonicity property ($\hat{l}(u) \le \hat{l}(v)$), LC-B&B Priority Queue node ordering, Fractional Knapsack ratio sorting, Job Assignment worker-job matching, TSP Matrix Transformation rules (Row $u = \infty$, Col $v = \infty$, Cell $(v,u) = \infty$), DFB&B $O(H)$ linear memory stack with $C^*$ pruning, Warm-starting greedy initial $P^*$, and Dominance Pruning ($\text{Profit}_A \ge \text{Profit}_B \land \text{Weight}_A \le \text{Weight}_B$)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Branch & Bound Operational Principle**:
  - Branching: Divide state node $x$ into child subproblems. Bounding: Calculate optimistic limit ($\hat{l}(x)$ or $\hat{u}(x)$).
* **Admissibility Condition (No Over / Under-estimation)**:
  - Minimization: $\hat{l}(x) \le f(S^*_{\text{subtree}(x)})$ (Lower bound MUST NOT overestimate cost!).
  - Maximization: $\hat{u}(x) \ge f(S^*_{\text{subtree}(x)})$ (Upper bound MUST NOT underestimate profit!).
* **Monotonicity Property**:
  - Minimization: $\hat{l}(u) \le \hat{l}(v)$ for child $v$ of parent $u$.
  - Maximization: $\hat{u}(u) \ge \hat{u}(v)$ for child $v$ of parent $u$.
* **The B&B Pruning Conditions**:
  - Minimization: Kill node $x$ if $\hat{l}(x) \ge C^*$ (where $C^*$ is current best cost).
  - Maximization: Kill node $x$ if $\hat{u}(x) \le P^*$ (where $P^*$ is current best profit).
* **0/1 Knapsack Value-to-Weight Ratio Sorting**:
  - Sort items so $\frac{v_0}{w_0} \ge \frac{v_1}{w_1} \ge \dots \ge \frac{v_{N-1}}{w_{N-1}}$.
* **Fractional Knapsack Upper Bound Formula**:
  - $\hat{u}(x) = \text{profit} + \sum_{i=level}^{k-1} v_i + v_k \times \frac{W_{\text{remaining}}}{w_k}$.
* **Row-Column Matrix Reduction Lower Bound Formula**:
  - $\hat{l}(\text{Root}) = \sum \text{Row Minimums} + \sum \text{Column Minimums}$.
* **Job Assignment Lower Bound Formula**:
  - $\hat{l}(x) = C_{\text{acc}}(x) + \sum_{i \in U_{\text{workers}}} \min_{j \in U_{\text{jobs}}} C[i][j]$.
* **TSP Edge $u \to v$ Matrix Transformation Rules**:
  1. Set Row $u = \infty$ (No more departures from $u$).
  2. Set Column $v = \infty$ (No more arrivals at $v$).
  3. Set Cell $(v, u) = \infty$ (Prevents 2-city sub-tour cycle).
* **TSP Child Lower Bound Formula**:
  - $\hat{l}(\text{Child}) = \hat{l}(\text{Parent}) + \text{ReducedMatrix}[u][v] + \text{New Reduction Cost of Transformed Matrix}$.
* **Depth-First Branch & Bound (DFB&B) Memory Bound**:
  - Uses recursive call stack $\implies$ **$O(H)$ Linear Memory Footprint** with global $C^*$ pruning!
* **Warm-Starting Initial Best Profit**:
  - Run fast $O(N \log N)$ greedy algorithm to initialize $P^*_{\text{greedy}}$ before running B&B.
* **Dominance Pruning Condition (Knapsack)**:
  - If $\text{Profit}_A \ge \text{Profit}_B$ AND $\text{Weight}_A \le \text{Weight}_B$, then **Node $A$ Dominates Node $B$** (Kill Node $B$!).

```
Master Branch & Bound Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| B&B Archetype         | Bounding Engine   | Priority Queue    | Pruning Condition | Ideal Application |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **0/1 Knapsack B&B**  | Fractional Relaxation| **Max-PQ Bound ⚡**| $\hat{u}(x) \le P^*$| Huge Capacity $W$ |
| **Job Assignment**    | Matrix Reduction  | **Min-PQ Bound ⚡**| $\hat{l}(x) \ge C^*$| Worker-Job Match  |
| **TSP Matrix B&B**    | Matrix Transformation| **Min-PQ Bound ⚡**| $\hat{l}(x) \ge C^*$| $N = 30+$ Cities  |
| **DFB&B Search**      | Admissible Bounds | **DFS Stack O(H)⚡**| $C \ge C^*$       | Deep Trees ($H>50$)|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| B&B Topic | Purpose | Traversal Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B&B Foundations** | Optimization spaces | Priority Queue | $O(2^N)$ Pruned | $O(2^N)$ Queue Space | Optimistic bounds |
| **FIFO B&B** | Level order search | FIFO Queue | $O(B^H)$ High | $O(B^H)$ Queue Space | Level-by-level |
| **LIFO B&B** | Depth first search | LIFO Stack | $O(B^H)$ High | $\mathbf{O(H)}$ Stack Depth ⚡| Stack memory |
| **LC B&B (Best-First)**| Minimal expansions | Max/Min PriorityQueue| **Pruned $O(B^H)$ ⚡**| $O(B^H)$ Queue Space | **Minimum nodes ⚡** |
| **DFB&B Search** | Memory-safe B&B | DFS Call Stack | Pruned $O(B^H)$ | $\mathbf{O(H)}$ Stack Depth ⚡| **$O(H)$ Memory ⚡** |
| **Bounding Functions**| State pruning bounds| Matrix Reduction / LP| $O(N^2)$ / $O(N)$ | $O(N^2)$ Matrix | Admissibility |
| **Job Assignment** | Worker-job matching | Min-PriorityQueue | $\mathbf{O(N!)}$ Pruned ⚡| $O(N!)$ Queue Space | `assignedJobs[]` |
| **0/1 Knapsack B&B** | Huge capacity W | Max-PriorityQueue | $\mathbf{O(2^N)}$ Pruned ⚡| $O(2^N)$ Queue Space | Ratio sorting |
| **TSP Matrix B&B** | Shortest tour | Min-PriorityQueue | $\mathbf{O(N!)}$ Pruned ⚡| $O(N!)$ Queue Space | Row $u=\infty$, Col $v=\infty$ |
| **Warm-Starting** | Speed up convergence| Greedy Initialization| $O(N \log N)$ | $\mathbf{O(1)}$ Memory ⚡| Initial $P^*$ |
| **Dominance Pruning** | Eliminate redundant| State Map Check | $O(N)$ Map Check | $O(N)$ Map Space | Subsumption check |

---

## 4. Architectural System & Production Use Cases
```
+-----------------------------------------------------------------------------------+
| Production System Branch & Bound Architectures                                    |
+-----------------------------------------------------------------------------------+
| Large-Scale Cargo Container & Freight Allocation : 0/1 Knapsack B&B ($W=10^{15}$) |
| Commercial Drone & Delivery Route Optimizers    : TSP Reduced Cost Matrix B&B     |
| Cloud Distributed Task & Worker Schedulers       : Job Assignment LC-B&B Solvers  |
| Integer Linear Programming Solvers (Gurobi/Cplex): Simplex LP Relaxation B&B      |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Max-PriorityQueue Node Order (Maximization)
> PriorityQueue<Node> pq = new PriorityQueue<>((a, b) -> Double.compare(b.bound, a.bound));
> 
> // 2. Min-PriorityQueue Node Order (Minimization)
> PriorityQueue<Node> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.lowerBound, b.lowerBound));
> 
> // 3. 0/1 Knapsack Ratio Sorting
> Arrays.sort(items, (a, b) -> Double.compare(b.ratio, a.ratio));
> 
> // 4. Fractional Knapsack Upper Bound Line
> bound += values[i] * ((double) remainingCapacity / weights[i]);
> 
> // 5. Job Assignment Lower Bound Check
> if (nextBound < bestCost) pq.add(new AssignmentNode(...));
> 
> // 6. TSP Edge Transformation Lines (u -> v)
> for (int i = 0; i < n; i++) { matrix[u][i] = INF; matrix[i][v] = INF; } matrix[v][u] = INF;
> 
> // 7. DFB&B Optimality Cutoff
> if (currentCost >= bestCostDFBB) return;
> 
> // 8. Dominance Pruning Check
> if (prevProfit >= node.profit && prevWeight <= node.weight) return true; // Dominated!
> 
> // 9. Warm-Starting Greedy Initial Profit
> int maxProfit = calculateGreedyInitialProfit(capacity, weights, values, n);
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using FIFO Queue Instead of Priority Queue in B&B**: Plain Queue expands level by level without regard to node quality, turning B&B into slow BFS. **ALWAYS use a Priority Queue ordered by optimistic bound**!
* **Pitfall 2: Forgetting Ratio Sorting in 0/1 Knapsack B&B**: Running Knapsack B&B without pre-sorting items by $\frac{v_i}{w_i}$ produces loose upper bounds, expanding almost all $2^N$ nodes. **ALWAYS sort items by ratio first**!
* **Pitfall 3: Forgetting Edge Mask `Cell(v, u) = INF` in TSP B&B**: Failing to set `matrix[v][u] = INF` when stepping $u \to v$ permits early 2-city sub-tour cycles. **ALWAYS set `matrix[v][u] = INF`**!
* **Pitfall 4: Violating the Admissibility Property**: Constructing a lower bound that overestimates true cost causes B&B to falsely prune subtrees containing optimal solutions. **ALWAYS ensure $\hat{l}(x) \le \text{True Cost}$**!
* **Pitfall 5: Running LC-B&B on Huge Search Trees Without Memory Guards**: Pushing millions of nodes into Priority Queue causes `OutOfMemoryError`. **Use DFB&B or Memory-Capped Queues for deep search trees**!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 28 (BRANCH & BOUND)              |
+-----------------------------------------------------------------------+
| 1. B&B Principle  : Branching (Split) + Bounding (Optimistic limit)   |
| 2. Admissibility  : l_hat(x) <= True Cost (Min); u_hat(x) >= True Profit|
| 3. LC-B&B Order   : PriorityQueue pops node with best bound first ⚡  |
| 4. Knapsack Ratio : Pre-sort items by value/weight ratio descending   |
| 5. Knapsack Bound : Fractional knapsack continuous LP relaxation      |
| 6. Job Assignment : Min-PQ matching worker to job + assignedJobs[]    |
| 7. TSP Matrix B&B : Set Row u = INF, Col v = INF, Cell(v,u) = INF     |
| 8. DFB&B Search   : DFS Call Stack + C* Pruning -> O(H) Memory ⚡      |
| 9. Warm-Starting  : Initialize P* using fast greedy heuristic first   |
| 10. Dominance     : Kill node B if node A has higher profit & lower w |
| 11. B&B vs DP     : Use B&B when DP table capacity W = 10^15 explodes!|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can state the Branch & Bound Principle (Branching + Bounding).
- [ ] I can define the Admissibility property for lower and upper bounds.
- [ ] I can explain why LC Branch & Bound uses a Priority Queue.
- [ ] I can write 0/1 Knapsack Branch & Bound in Java with ratio sorting.
- [ ] I can state when to use B&B over Dynamic Programming for Knapsack ($W > 10^7$).
- [ ] I can write Job Assignment LC Branch & Bound in Java.
- [ ] I can write TSP LC Branch & Bound in Java with matrix transformations.
- [ ] I can state the 3 TSP matrix transformation rules for edge $u \to v$.
- [ ] I can write Depth-First Branch & Bound (DFB&B) in Java.
- [ ] I can explain why DFB&B uses $O(H)$ memory compared to LC-B&B $O(B^H)$.
- [ ] I can write Warm-Started B&B solvers in Java.
- [ ] I can write Dominance Pruning state checkers.
- [ ] I can state the differences between Backtracking and Branch & Bound.
