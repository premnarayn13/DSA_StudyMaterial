# 03. Fractional Knapsack: Value Density Sorting, Continuous Choices & Proofs

## 1. Introduction
The **Fractional Knapsack Problem** (also known as the **Continuous Knapsack Problem**) is the classic greedy optimization problem demonstrating how continuous item divisible properties enable an optimal solution in **$O(N \log N)$ Time Complexity**. Given $N$ items, where each item $i$ has a value $v_i > 0$ and a weight $w_i > 0$, and a knapsack with maximum weight capacity $W$, the goal is to select full items or fractional parts of items ($x_i \in [0, 1]$) to maximize the total accumulated value $\sum_{i=1}^N x_i \cdot v_i$ subject to the weight constraint $\sum_{i=1}^N x_i \cdot w_i \le W$. By sorting items in descending order of **Value Density** ($d_i = \frac{v_i}{w_i}$), the greedy algorithm achieves absolute optimality in **$O(1)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Fractional Knapsack:
> 1. **Value Density Definition ($d_i$)**:
>    - Value Density $d_i = \frac{v_i}{w_i}$ represents the monetary value yielded per unit of weight ($1\text{ kg}$).
> 2. **Greedy Selection Policy**:
>    - Process items in strictly non-increasing order of value density ($d_1 \ge d_2 \ge \dots \ge d_N$).
> 3. **Fractional Splitting Property ($x_i \in [0, 1]$)**:
>    - If remaining capacity $W_{\text{rem}} \ge w_i \implies$ Take 100% of item $i$ ($x_i = 1$).
>    - If remaining capacity $W_{\text{rem}} < w_i \implies$ Take fraction $x_i = \frac{W_{\text{rem}}}{w_i}$ of item $i$, filling the knapsack completely ($W_{\text{rem}} = 0$).
> 4. **Exchange Argument Proof Invariant**:
>    - Replacing any fraction of a higher-density item with a lower-density item strictly reduces total total value, proving that the greedy choice is globally optimal! ⚡

```
Fractional Knapsack Value Density Topology (Capacity W = 50):

Item 1: Value = 60,  Weight = 10 ──► Density d1 = 60/10 = 6.0 $/kg
Item 2: Value = 100, Weight = 20 ──► Density d2 = 100/20 = 5.0 $/kg
Item 3: Value = 120, Weight = 30 ──► Density d3 = 120/30 = 4.0 $/kg

Greedy Selection Steps:
1. Sort by Density: Item 1 (6.0), Item 2 (5.0), Item 3 (4.0).
2. Take 100% Item 1: Weight = 10, Value = 60, Rem Capacity = 40.
3. Take 100% Item 2: Weight = 20, Value = 100, Rem Capacity = 20.
4. Take Fraction of Item 3: Fraction = 20/30 = 2/3. Value Added = (2/3)*120 = 80, Rem Capacity = 0!

Total Optimal Value = 60 + 100 + 80 = 240.0! ⚡
```

---

## 2. Core Concepts & Knapsack Strategy Matrix

### 2.1 Knapsack Variants Strategy Matrix
```
Knapsack Problem Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Knapsack Variant      | Item Choice $x_i$ | Optimal Strategy  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Fractional**        | **$x_i \in [0, 1]$ ⚡**| **Greedy Density Sort⚡**| **$O(N \log N)$ ⚡**| **$O(1)$ Memory ⚡**|
| **0/1 Knapsack**      | $x_i \in \{0, 1\}$| Dynamic Programming| $O(N \cdot W)$ Pseudo | $O(N \cdot W)$ Table |
| **Unbounded**         | $x_i \in \mathbb{Z}_{\ge 0}$| Dynamic Programming| $O(N \cdot W)$ Pseudo | $O(W)$ Array      |
| **Bounded**           | $x_i \in \{0 \dots c_i\}$| Binary Decomp DP   | $O(W \cdot \sum \log c_i)$| $O(W)$ Array      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fractional Knapsack uses Greedy Density Sort v_i / w_i! Divisible items allow linear/log-linear speed!"**

---

## 3. Characteristics & Exchange Argument Mathematical Proof

### 3.1 Mathematical Proof of Optimality via Exchange Argument
* **Theorem**: Sorting items by descending value density $d_i = \frac{v_i}{w_i}$ and taking items greedily yields an optimal solution $G = (g_1, g_2 \dots g_N)$ for Fractional Knapsack.
* **Proof**:
  1. Let $G = (g_1, g_2 \dots g_N)$ be the greedy solution, where items are ordered such that $d_1 \ge d_2 \ge \dots \ge d_N$.
  2. Assume there exists an optimal solution $O = (o_1, o_2 \dots o_N)$ such that $O \neq G$.
  3. Find the first item index $k$ where $g_k \neq o_k$.
  4. By definition of the greedy choice, $g_k > o_k$ (Greedy took more of item $k$ because it has the highest remaining density $d_k$).
  5. Since total weight $\sum o_i = W = \sum g_i$, there must exist some item $j > k$ where $o_j > g_j$ (Optimal took more of a lower-density item $j$).
  6. **Exchange Step**: Decrease $o_j$ by amount $\Delta = \min(o_j - g_j, (g_k - o_k) \cdot w_k / w_j)$ and increase $o_k$ by an equivalent weight $\Delta \cdot w_j / w_k$.
  7. **Value Change Calculation**:
     $$\Delta \text{Value} = \Delta \cdot w_j \cdot (d_k - d_j)$$
     Since $k < j \implies d_k \ge d_j$, the value change $\Delta \text{Value} \ge 0$.
  8. Therefore, the modified solution $O'$ has total value $\ge O$, and $O'$ matches $G$ on one more element.
  9. By induction, $O$ can be transformed into $G$ without losing value, proving that the Greedy solution $G$ is globally optimal! ⚡

---

## 4. Internal Working Mechanics: Complete Step-by-Step Dry Run

Tracing Fractional Knapsack for $W = 60$, Items: $(v_1=100, w_1=20)$, $(v_2=120, w_2=30)$, $(v_3=120, w_3=40)$:

```
Step 1: Calculate Densities:
- Item 1: d1 = 100 / 20 = 5.0 $/kg
- Item 2: d2 = 120 / 30 = 4.0 $/kg
- Item 3: d3 = 120 / 40 = 3.0 $/kg

Step 2: Sort Items Descending by Density:
Sorted Order: Item 1 (5.0), Item 2 (4.0), Item 3 (3.0).

Step 3: Process Items Greedily:
- Initial Capacity W = 60, Total Value = 0.0

- Iteration 1 (Item 1, w=20, v=100, d=5.0):
  w1 (20) <= W (60) -> Take 100% (x1 = 1.0)
  Capacity W = 60 - 20 = 40
  Total Value = 0 + 100 = 100.0

- Iteration 2 (Item 2, w=30, v=120, d=4.0):
  w2 (30) <= W (40) -> Take 100% (x2 = 1.0)
  Capacity W = 40 - 30 = 10
  Total Value = 100.0 + 120.0 = 220.0

- Iteration 3 (Item 3, w=40, v=120, d=3.0):
  w3 (40) > W (10) -> Take Fraction!
  Fraction x3 = 10 / 40 = 0.25 (25%)
  Value Added = 120.0 * 0.25 = 30.0
  Capacity W = 10 - 10 = 0 (FULL!)
  Total Value = 220.0 + 30.0 = 250.0

Final Max Fractional Value = 250.0! ✅
```

---

## 5. Visual Diagram: Continuous Density Filling Pipeline

```
Knapsack Capacity Bar W = 60:

[ Item 1 (Density 5.0): Weight 20 | Value 100 ]  (Filled 0 .. 20)
[ Item 2 (Density 4.0): Weight 30 | Value 120 ]  (Filled 20 .. 50)
[ Item 3 (Density 3.0): Weight 10 | Value 30  ]  (Filled 50 .. 60 - 25% Fraction!)

Knapsack Completely Full! Total Value = 250.0! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Fractional Knapsack, LeetCode 1710 (Maximum Units on a Truck), and LeetCode 2279 (Maximum Bags With Full Capacity of Rocks).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Fractional Knapsack,
 * Density Sorting, and Real-World Resource Allocation Problems.
 */
public class FractionalKnapsackMaster {

    public static class KnapsackItem {
        public final int id;
        public final double value;
        public final double weight;
        public final double density; // Value / Weight ratio

        public KnapsackItem(int id, double value, double weight) {
            this.id = id;
            this.value = value;
            this.weight = weight;
            this.density = value / weight;
        }

        @Override
        public String toString() {
            return String.format("Item%d[v=%.1f, w=%.1f, d=%.2f]", id, value, weight, density);
        }
    }

    public static class FractionalResult {
        public final double totalValue;
        public final double[] fractionsTaken; // Fraction x_i taken for each item

        public FractionalResult(double totalValue, double[] fractionsTaken) {
            this.totalValue = totalValue;
            this.fractionsTaken = fractionsTaken;
        }
    }

    // =========================================================================
    // 1. STANDARD FRACTIONAL KNAPSACK (O(N log N) Time, O(N) Space)
    // =========================================================================
    /**
     * Calculates maximum value obtained by filling knapsack of capacity W.
     *
     * @param items list of items with values and weights
     * @param capacity maximum weight capacity W
     * @return FractionalResult containing total value and item fractions taken
     */
    public FractionalResult solveFractionalKnapsack(List<KnapsackItem> items, double capacity) {
        if (items == null || items.isEmpty() || capacity <= 0) {
            return new FractionalResult(0.0, new double[0]);
        }

        int n = items.size();
        double[] fractions = new double[n];

        // Create item wrapper with original indices for fraction mapping
        List<Integer> indices = new ArrayList<>();
        for (int i = 0; i < n; i++) indices.add(i);

        // Sort indices by item density descending (b.density vs a.density)
        indices.sort((i1, i2) -> Double.compare(items.get(i2).density, items.get(i1).density));

        double currentCapacity = capacity;
        double totalValue = 0.0;

        for (int idx : indices) {
            if (currentCapacity == 0) break;

            KnapsackItem item = items.get(idx);

            if (item.weight <= currentCapacity) {
                // Take 100% of item
                fractions[idx] = 1.0;
                currentCapacity -= item.weight;
                totalValue += item.value;
            } else {
                // Take fraction of item
                double fraction = currentCapacity / item.weight;
                fractions[idx] = fraction;
                totalValue += item.value * fraction;
                currentCapacity = 0; // Full!
            }
        }

        return new FractionalResult(totalValue, fractions);
    }

    // =========================================================================
    // 2. LEETCODE 1710: MAXIMUM UNITS ON A TRUCK (O(N log N) Time)
    // =========================================================================
    /**
     * Solves LeetCode 1710: Maximum Units on a Truck.
     * boxTypes[i] = [numberOfBoxes_i, unitsPerBox_i].
     */
    public int maximumUnits(int[][] boxTypes, int truckSize) {
        if (boxTypes == null || boxTypes.length == 0 || truckSize <= 0) return 0;

        // Sort boxTypes by unitsPerBox descending
        Arrays.sort(boxTypes, (a, b) -> Integer.compare(b[1], a[1]));

        int totalUnits = 0;
        int remainingCapacity = truckSize;

        for (int[] box : boxTypes) {
            if (remainingCapacity == 0) break;

            int count = Math.min(remainingCapacity, box[0]);
            totalUnits += count * box[1];
            remainingCapacity -= count;
        }

        return totalUnits;
    }

    // =========================================================================
    // 3. LEETCODE 2279: MAXIMUM BAGS WITH FULL CAPACITY OF ROCKS (O(N log N))
    // =========================================================================
    /**
     * Solves LeetCode 2279 using Greedy sorting on remaining capacity needed.
     */
    public int maximumBags(int[] capacity, int[] rocks, int additionalRocks) {
        int n = capacity.length;
        int[] needed = new int[n];

        for (int i = 0; i < n; i++) {
            needed[i] = capacity[i] - rocks[i];
        }

        // Sort by minimum rocks needed to fill bag
        Arrays.sort(needed);

        int fullBags = 0;
        for (int req : needed) {
            if (additionalRocks >= req) {
                additionalRocks -= req;
                fullBags++;
            } else {
                break;
            }
        }

        return fullBags;
    }
}
```

> **Quick Syntax:**
```java
// Item Density Sorting Line
indices.sort((i1, i2) -> Double.compare(items.get(i2).density, items.get(i1).density));
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1710 - Maximum Units on a Truck**:
   - Equivalent to Fractional Knapsack where units per box represents density.

2. **LeetCode 2279 - Maximum Bags With Full Capacity of Rocks**:
   - Greedy allocation of rocks to bags needing smallest additional capacity.

3. **Oil Refinery Crude Distillation & Commodity Trading**:
   - Filling tanker ships with liquid commodities (petroleum, grain, gold dust) based on value per barrel/ton.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class FractionalKnapsackDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   FRACTIONAL KNAPSACK GREEDY DEMO              ");
        System.out.println("=================================================\n");

        FractionalKnapsackMaster master = new FractionalKnapsackMaster();

        // 1. Standard Fractional Knapsack Test
        List<FractionalKnapsackMaster.KnapsackItem> items = List.of(
            new FractionalKnapsackMaster.KnapsackItem(1, 100, 20), // Density 5.0
            new FractionalKnapsackMaster.KnapsackItem(2, 120, 30), // Density 4.0
            new FractionalKnapsackMaster.KnapsackItem(3, 120, 40)  // Density 3.0
        );

        double capacity = 60.0;
        FractionalKnapsackMaster.FractionalResult result = master.solveFractionalKnapsack(items, capacity);

        System.out.println("1. Items List: " + items);
        System.out.println("   Capacity  : " + capacity);
        System.out.println("   Max Total Value Obtained: " + result.totalValue + " (Optimal)");
        System.out.println("   Fractions Taken (Item1, Item2, Item3): " + Arrays.toString(result.fractionsTaken));
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 1710 Truck Units Test
        int[][] boxTypes = {{1, 3}, {2, 2}, {3, 1}};
        int truckSize = 4;
        int maxUnits = master.maximumUnits(boxTypes, truckSize);
        System.out.println("2. LeetCode 1710 Maximum Units for Truck Size 4: " + maxUnits + " Units");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Knapsack Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Density Sorting** | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Sorting Space | Dual pivot QuickSort |
| **Greedy Loop Pass**| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Single forward scan |
| **Overall Algorithm**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Space | Optimal Greedy Strategy |

---

## 10. Edge Cases & Boundary Handling

1. **Items With Equal Densities ($d_i == d_j$)**:
   - `Double.compare` handles equal densities cleanly without infinite loops or unstable sort errors.

2. **Capacity Exceeds Total Weight of All Items ($\sum w_i \le W$)**:
   - Takes 100% of all items ($x_i = 1.0$ for all $i$), returning total value $\sum v_i$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Sorting by Value Alone or Weight Alone**:
  - Sorting by value alone ignores heavy item costs; sorting by weight alone ignores item profits. **ALWAYS sort by DENSITY $v_i / w_i$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Fractional Knapsack is $O(N \log N)$ but 0/1 Knapsack is $O(N \cdot W)$:
> * **Fractional Knapsack**: Divisible items guarantee that local density choices lead to a global optimum ($O(N \log N)$ sorting time).
> * **0/1 Knapsack**: Indivisible choices create a combinatorial NP-complete space requiring Dynamic Programming ($O(N \cdot W)$ pseudo-polynomial time). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Fractional Knapsack | 0/1 Knapsack (DP) | Unbounded Knapsack |
| :--- | :--- | :--- | :--- |
| **Item Divisibility** | **Divisible (Fractions)⚡**| Indivisible (0 or 1) | Indivisible (Infinite copies) |
| **Algorithm Class**   | **Greedy Algorithm ⚡** | Dynamic Programming | Dynamic Programming |
| **Time Complexity**   | **$O(N \log N)$ ⚡**    | $O(N \cdot W)$      | $O(N \cdot W)$ |

---

## 14. How to Recognize This in Questions

* **"Maximize total value where items can be split into continuous fractions"** $\rightarrow$ Fractional Knapsack.
* **"Maximize units loaded onto truck with limited box capacity"** $\rightarrow$ LeetCode 1710.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does the Greedy strategy work for Fractional Knapsack but fail for 0/1 Knapsack?**  
  *A:* Because allowing fractions ensures that the knapsack can be filled 100% to capacity with the highest density items available without leaving empty, unusable weight gaps.

* **Q: How is item value density defined?**  
  *A:* Value density is $d_i = \frac{v_i}{w_i}$, representing monetary value per unit of weight.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: FRACTIONAL KNAPSACK                                   |
+-----------------------------------------------------------------------+
| • Core Strategy: Sort items by Value Density (d_i = v_i / w_i) desc   |
| • Greedy Choice: Take 100% of items while weight <= capacity          |
| • Fractional   : Take fraction W_rem / w_i for final item             |
| • Proof Method : Verified optimal via Exchange Argument               |
| • Performance  : O(N log N) Sorting Time | O(1) Auxiliary Space ⚡       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write standard Fractional Knapsack using Greedy density sorting in Java.
- [ ] I can prove why Fractional Knapsack is optimal using an Exchange Argument.
- [ ] I can solve LeetCode 1710 (`Maximum Units on a Truck`).
- [ ] I can solve LeetCode 2279 (`Maximum Bags With Full Capacity of Rocks`).
- [ ] I can state why Greedy fails for 0/1 Knapsack but succeeds for Fractional Knapsack.
