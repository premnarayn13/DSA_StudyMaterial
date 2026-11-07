# 01. Greedy Fundamentals: Invariants, Choice Property & Proof Techniques

## 1. Introduction
A **Greedy Algorithm** is an algorithmic paradigm that builds up a solution piece-by-piece, always making the choice that offers the most immediate (local) benefit, under the expectation that local optimal choices will lead to a globally optimal solution. Unlike **Dynamic Programming** (which evaluates all candidate subproblem choices and caches results) or **Backtracking** (which explores full decision trees with exhaustive state rollbacks), a Greedy algorithm makes an **Irrevocable Choice** at each step without ever backtracking or re-evaluating past choices. To guarantee correctness, a problem solved via Greedy MUST satisfy two fundamental properties: the **Greedy Choice Property** and **Optimal Substructure**.

> **Important:** The 4 Structural Invariants of Greedy Algorithms:
> 1. **Greedy Choice Property**:
>    - A globally optimal solution can be arrived at by making locally optimal (greedy) choices at each step without considering future consequences or backtracking.
> 2. **Optimal Substructure**:
>    - An optimal solution to the problem contains within it optimal solutions to its subproblems.
> 3. **Irrevocability Invariant**:
>    - Once a decision is made (e.g., picking the shortest edge or highest density item), it is NEVER undone or reconsidered.
> 4. **Mathematical Verification Necessity**:
>    - Greedy choices are notoriously deceptive! An algorithm that appears intuitively optimal may fail on edge cases unless mathematically verified via **Exchange Arguments** or the **Staying Ahead Technique**. ⚡

```
Greedy Decision Topology (Local Optimum -> Global Optimum):

                     [ Initial State S_0 ]
                              │
                     Make Greedy Choice (Max Local Benefit)
                              │
                              ▼
                     [ Subproblem State S_1 ]
                              │
                     Make Greedy Choice (Max Local Benefit)
                              │
                              ▼
                 [ Global Optimal Solution S* ]

No Backtracking! No State Re-evaluation! Instant Linear / Log-Linear Speed! ⚡
```

---

## 2. Core Concepts & Paradigm Comparison Strategy Matrix

### 2.1 Greedy vs DP vs Backtracking Strategy Matrix
```
Algorithm Paradigm Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Paradigm              | Decision Policy   | Backtracking?     | Subproblem Overlap| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Greedy Paradigm**   | **Locally Best ⚡**| **NEVER ⚡**      | Not Required      | **$O(N \log N)$ Fast⚡**|
| **Dynamic Programming**| Global Combination| Never             | **REQUIRED (Table)**| $O(N \cdot W)$ Pseudo |
| **Backtracking**      | Exhaustive Tree   | **ALWAYS ⚡**      | Not Required      | $O(2^N)$ Exponential|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Greedy picks the local optimum instantly with zero backtracking! DP evaluates subproblem tables; Backtracking explores all states!"**

---

## 3. Characteristics & Proof Techniques Mathematical Foundations

### 3.1 Mathematical Proof Technique 1: Exchange Argument
* **Objective**: Prove that greedy solution $G$ is as good as any arbitrary optimal solution $O$.
* **Proof Procedure**:
  1. Assume an optimal solution $O = (o_1, o_2 \dots o_k)$ that differs from greedy solution $G = (g_1, g_2 \dots g_k)$.
  2. Find the first index $i$ where $g_i \neq o_i$.
  3. **Exchange Step**: Replace $o_i$ with $g_i$ in $O$, forming a modified solution $O'$.
  4. Show mathematically that $O'$ is still valid and its cost/value is $\le$ (or $\ge$) $O$.
  5. By induction, transform $O$ into $G$ without losing optimality, proving that $G$ is optimal! ⚡

### 3.2 Mathematical Proof Technique 2: Staying Ahead Technique
* Measure progress of greedy choice $G_i$ against optimal choice $O_i$ at each step $i$.
* Show by induction that for all steps $i$, greedy solution parameter $f(G_i)$ is at least as good as optimal solution parameter $f(O_i)$ ($f(G_i) \ge f(O_i)$). ⚡

---

## 4. Internal Working Mechanics: When Greedy Succeeds vs Fails

Why Greedy works for Fractional Knapsack but FAILS for 0/1 Knapsack:

```
Fractional Knapsack (Greedy Succeeds ✅):
Items can be split! Greedy strategy picks items with highest Value/Weight ratio (density v_i / w_i).
Since fractions are allowed, filling capacity with highest density items guarantees max total value!

0/1 Knapsack (Greedy FAILS ❌):
Items CANNOT be split (must take 100% or 0%).
Example: Capacity W = 50.
- Item 1: v=60, w=10 (Density = 6.0)
- Item 2: v=100, w=20 (Density = 5.0)
- Item 3: v=120, w=30 (Density = 4.0)

Greedy Pick by Density: Picks Item 1 (w=10, v=60), then Item 2 (w=20, v=100). Total Weight = 30. Remaining W = 20 (Cannot fit Item 3!).
Greedy Total Value = 160.

OPTIMAL Pick (DP): Pick Item 2 (w=20, v=100) + Item 3 (w=30, v=120). Total Weight = 50.
Optimal Total Value = 220!

Greedy failed because items cannot be split! 0/1 Knapsack requires Dynamic Programming! ⚡
```

---

## 5. Visual Diagram: Local vs Global Optima Trajectory

```
State Space Search Topology:

                (Global Optimum: 220)
                       /\
                      /  \
  (Local Optimum: 160)   \
         /\               \
        /  \               \
       /    \               \
   [Greedy Choice]      [DP State Search]

Greedy choices must align with the global peak to be correct! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing a generic Greedy Choice Template, Density-Based Sorting, and Comparison of Greedy vs DP Solutions.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Greedy Fundamentals,
 * Item Density Sorting, and Greedy vs DP Comparisons.
 */
public class GreedyFundamentalsMaster {

    public static class Item {
        public final int id;
        public final double value;
        public final double weight;
        public final double density; // Value per unit weight

        public Item(int id, double value, double weight) {
            this.id = id;
            this.value = value;
            this.weight = weight;
            this.density = value / weight;
        }

        @Override
        public String toString() {
            return String.format("Item%d[v=%.1f, w=%.1f, density=%.2f]", id, value, weight, density);
        }
    }

    // =========================================================================
    // 1. FRACTIONAL KNAPSACK (GREEDY PARADIGM O(N log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves Fractional Knapsack in O(N log N) time using Greedy Density Sorting.
     *
     * @param items list of items
     * @param capacity max knapsack weight capacity
     * @return maximum total value obtained
     */
    public double getOptimalFractionalKnapsack(List<Item> items, double capacity) {
        if (items == null || items.isEmpty() || capacity <= 0) return 0.0;

        // Step 1: Sort items in descending order of density (value / weight)
        List<Item> sortedItems = new ArrayList<>(items);
        sortedItems.sort((a, b) -> Double.compare(b.density, a.density));

        double totalValue = 0.0;
        double currentCapacity = capacity;

        // Step 2: Make Greedy Choices sequentially
        for (Item item : sortedItems) {
            if (currentCapacity == 0) break;

            if (item.weight <= currentCapacity) {
                // Take 100% of the item
                currentCapacity -= item.weight;
                totalValue += item.value;
            } else {
                // Take fraction of the item
                double fraction = currentCapacity / item.weight;
                totalValue += item.value * fraction;
                currentCapacity = 0; // Knapsack full!
            }
        }

        return totalValue;
    }

    // =========================================================================
    // 2. 0/1 KNAPSACK DYNAMIC PROGRAMMING (FOR GREEDY VS DP COMPARISON O(N * W))
    // =========================================================================
    /**
     * Solves 0/1 Knapsack using Dynamic Programming to demonstrate Greedy failure on discrete choices.
     */
    public int solve01KnapsackDP(int[] values, int[] weights, int capacity) {
        int n = values.length;
        int[][] dp = new int[n + 1][capacity + 1];

        for (int i = 1; i <= n; i++) {
            for (int w = 0; w <= capacity; w++) {
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]);
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }

        return dp[n][capacity];
    }
}
```

> **Quick Syntax:**
```java
// Greedy Density Sorting Line
items.sort((a, b) -> Double.compare(b.density, a.density));
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1710 - Maximum Units on a Truck**:
   - Equivalent to Fractional Knapsack solved in $O(N \log N)$ time using Greedy box density sorting.

2. **Network Routing Protocols (Dijkstra's Algorithm)**:
   - Always picks unvisited node with minimal tentative distance (Greedy Choice).

3. **Huffman Data Compression Trees**:
   - Always merges two smallest frequency nodes (Greedy Min-Heap Choice).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class GreedyFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GREEDY FUNDAMENTALS & PARADIGM DEMO           ");
        System.out.println("=================================================\n");

        GreedyFundamentalsMaster master = new GreedyFundamentalsMaster();

        // 1. Fractional Knapsack Test (Greedy Succeeds)
        List<GreedyFundamentalsMaster.Item> items = List.of(
            new GreedyFundamentalsMaster.Item(1, 60, 10),  // Density 6.0
            new GreedyFundamentalsMaster.Item(2, 100, 20), // Density 5.0
            new GreedyFundamentalsMaster.Item(3, 120, 30)  // Density 4.0
        );

        double capacity = 50.0;
        double maxFractionalValue = master.getOptimalFractionalKnapsack(items, capacity);

        System.out.println("1. Fractional Knapsack (Greedy Succeeds):");
        System.out.println("   Items List        : " + items);
        System.out.println("   Capacity          : " + capacity);
        System.out.println("   Max Value (Greedy): " + maxFractionalValue + " (Optimal = 240.0)");
        System.out.println("-------------------------------------------------");

        // 2. 0/1 Knapsack Test (Greedy Fails vs DP)
        int[] values = {60, 100, 120};
        int[] weights = {10, 20, 30};
        int intCapacity = 50;

        int dpValue = master.solve01KnapsackDP(values, weights, intCapacity);
        System.out.println("2. 0/1 Knapsack (Greedy Fails vs DP):");
        System.out.println("   Greedy Pick (160) vs Optimal DP Value (" + dpValue + ")");
        System.out.println("   Proves Greedy cannot solve discrete 0/1 choice problems!");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Greedy Operation | Time Complexity | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- |
| **Density Sorting** | $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Space | Sort by $v_i / w_i$ |
| **Greedy Pass**     | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Single forward scan |
| **Overall Fractional**| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Space | Greedy Choice Property |

---

## 10. Edge Cases & Boundary Handling

1. **All Items Fit (`Capacity >= Sum of Weights`)**:
   - Takes 100% of all items. Handled cleanly in single pass.

2. **Capacity Zero or Negative**:
   - Returns 0.0 immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Assuming Intuitive Greedy Choices Are Always Correct**:
  - Applying Greedy to 0/1 Knapsack or Coin Change with non-standard denominations produces incorrect results. ALWAYS verify via Exchange Arguments or counter-examples!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Conditions Required for Greedy Correctness:
> 1. **Greedy Choice Property**: Local optimal choices lead to global optimal solution.
> 2. **Optimal Substructure**: An optimal solution contains optimal subproblem solutions. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Greedy Algorithm | Dynamic Programming | Backtracking |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | **Fast $O(N \log N)$ ⚡** | $O(N \cdot W)$ Pseudo-Polynomial | $O(2^N)$ Exponential |
| **Backtracking** | **Never ⚡** | Never | Always |
| **Memory Footprint**| **Minimal $O(1)$ ⚡** | $O(N \cdot W)$ DP Table | $O(N)$ Stack Depth |

---

## 14. How to Recognize This in Questions

* **"Maximize total value where items can be split continuously"** $\rightarrow$ Greedy Fractional Knapsack.
* **"Find minimum intervals to cover full range"** $\rightarrow$ Greedy Interval Covering.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the Greedy Choice Property?**  
  *A:* The property that a globally optimal solution can be arrived at by making locally optimal choices without looking ahead or backtracking.

* **Q: Why does Greedy fail for 0/1 Knapsack?**  
  *A:* Because items cannot be split. Taking a high-density item might leave unused capacity that prevents fitting a higher total value combination of heavier items.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: GREEDY FUNDAMENTALS                                   |
+-----------------------------------------------------------------------+
| • Core Strategy: Make locally optimal choice at each step without backtrack|
| • 2 Invariants : Greedy Choice Property & Optimal Substructure        |
| • Proof Methods: Exchange Argument & Staying Ahead Technique          |
| • Fractional   : Greedy works via density sorting (v_i / w_i) -> O(N log N)|
| • 0/1 Knapsack : Greedy FAILS! Requires Dynamic Programming O(N * W)  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the 2 mathematical conditions required for Greedy correctness.
- [ ] I can write Fractional Knapsack using Greedy density sorting in Java.
- [ ] I can explain why Greedy fails for 0/1 Knapsack.
- [ ] I can explain the Exchange Argument proof technique.
- [ ] I can state the time complexity of Greedy Fractional Knapsack ($O(N \log N)$).
