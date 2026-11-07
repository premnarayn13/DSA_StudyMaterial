# 07. Recursive Trees: Visual Call Graph Analysis & Work-per-Level Summations

## 1. Introduction
The **Recursion Tree Method** is a powerful analytical and visual technique for determining the exact time and space complexity of recursive algorithms. By expanding a recurrence relation into a pictorial **Tree of Subproblem Calls**, engineers can analyze the degree of branching at each level, calculate the precise work performed per level, sum the total work across all levels from root to leaf, and visually discover **Overlapping Subproblems**. Mastery of recursion tree analysis is essential for evaluating Divide and Conquer algorithms (like Merge Sort and Quick Sort) and for recognizing when a naive recursive tree must be optimized via Dynamic Programming.

> **Important:** The 4 Structural Formulas of Recursion Tree Analysis:
> 1. **Branching Factor ($a$)**: The number of recursive child calls spawned by each parent node per frame.
> 2. **Subproblem Shrink Factor ($b$)**: The factor by which the input size $N$ is reduced at each deeper level ($N \to N/b$).
> 3. **Tree Height ($H$)**: The total depth from root to leaf:
>    $$H = \log_b N$$
> 4. **Total Work Formula**: The sum of work across all levels $l = 0 \dots H$:
>    $$T(N) = \sum_{l=0}^{H} (\text{Nodes at level } l) \times (\text{Work per node at level } l) = \sum_{l=0}^{\log_b N} a^l \cdot f\left(\frac{N}{b^l}\right)$$ ⚡

```
Recursion Tree Topology for T(N) = 2T(N/2) + O(N) [Merge Sort]:
Level 0 (Root):                     N                   ---> Work = N
                               /        \
Level 1:                     N/2        N/2             ---> Work = 2*(N/2) = N
                           /    \      /    \
Level 2:                 N/4    N/4  N/4    N/4         ---> Work = 4*(N/4) = N
                          ...    ...  ...    ...
Level log2(N) (Leaves):   1   1   1   1   1   1   1 ... ---> Work = N*1 = N

Total Work T(N) = N * (log2 N + 1) = O(N log N)! ⚡
```

---

## 2. Core Concepts & Recurrence Tree Archetypes Matrix

### 2.1 Common Recurrence Tree Archetypes
```
Recurrence Tree Archetypes Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Recurrence Relation   | Branching Factor  | Tree Height       | Total Time Bound  |
+-----------------------+-------------------+-------------------+-------------------+
| $T(N) = T(N-1) + O(1)$| $a = 1$           | $H = N$           | **$O(N)$ Linear ⚡**|
| $T(N) = 2T(N/2) + O(N)$| $a = 2, b = 2$   | $H = \log_2 N$    | **$O(N \log N)$ ⚡**|
| $T(N) = 2T(N/2) + O(1)$| $a = 2, b = 2$   | $H = \log_2 N$    | **$O(N)$ Linear ⚡**|
| $T(N) = 2T(N-1) + O(1)$| $a = 2$ (Subtract)| $H = N$           | **$O(2^N)$ Exponential**|
| $T(N) = T(N/2) + O(1)$| $a = 1, b = 2$    | $H = \log_2 N$    | **$O(\log N)$ Log ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Tree Work = (Nodes at level l) * (Work per node)! Sum across all levels 0..log_b(N)!"**

---

## 3. Characteristics & 3 Work-Summation Patterns

Depending on how work per level changes from root to leaves, recursion trees fall into 3 mathematical categories:

1. **Root-Dominated Work Tree ($f(n)$ decreases exponentially down the tree)**:
   - Most work is concentrated at the root node.
   - Total Time Complexity is dominated by root work: $T(N) = \mathbf{O(f(N))}$.
   - Example: $T(N) = 2T(N/2) + O(N^2) \implies O(N^2)$.

2. **Evenly Balanced Work Tree (Work per level is constant)**:
   - Every level performs the exact same total amount of work.
   - Total Time Complexity: $T(N) = \mathbf{O(f(N) \cdot \log N)}$.
   - Example: Merge Sort $T(N) = 2T(N/2) + O(N) \implies O(N \log N)$.

3. **Leaf-Dominated Work Tree (Work increases exponentially down the tree)**:
   - Most work is concentrated at the leaf nodes.
   - Total Time Complexity is dominated by the total number of leaves: $T(N) = \mathbf{O(a^{\log_b N})} = \mathbf{O(N^{\log_b a})}$.
   - Example: $T(N) = 3T(N/2) + O(N) \implies O(N^{\log_2 3}) \approx O(N^{1.58})$. ⚡

---

## 4. Internal Working Mechanics: Tracing Fibonacci $O(2^N)$ Tree Explosion

```
Tracing Fibonacci Tree for N = 4:

Level 0:                    fib(4)                     [1 Call]
                          /        \
Level 1:             fib(3)        fib(2)              [2 Calls]
                    /      \       /     \
Level 2:        fib(2)   fib(1)  fib(1)  fib(0)        [4 Calls]
               /      \
Level 3:   fib(1)   fib(0)                             [2 Calls]

Total Node Count = 1 + 2 + 4 + 2 = 9 Activation Records!
Notice Overlapping Subproblems:
- fib(2) is calculated TWICE!
- fib(1) is calculated THREE TIMES!
- fib(0) is calculated TWICE!

Redundant Work Percentage = 66% of calls are completely redundant!
Memoization converts this $O(2^N)$ tree into an $O(N)$ linear chain! ✅
```

---

## 5. Visual Diagram: Root-Dominated vs Leaf-Dominated Trees

```
1. Root-Dominated Tree (T(N) = 2T(N/2) + N^2):
Level 0:                 N^2                    = N^2  <-- DOMINANT ROOT!
                       /     \
Level 1:        (N/2)^2       (N/2)^2           = N^2 / 2
                 /   \         /   \
Level 2:   (N/4)^2 (N/4)^2 (N/4)^2 (N/4)^2     = N^2 / 4
Geometric Series Sum = N^2 * (1 + 1/2 + 1/4 + ...) = O(N^2) Total!

2. Leaf-Dominated Tree (T(N) = 3T(N/2) + N):
Level 0:                  N                     = N
                       /  |  \
Level 1:            N/2  N/2  N/2               = 1.5 N
                 / | \  / | \  / | \
Level 2:       9 nodes of size N/4              = 2.25 N
Work INCREASES per level! Total bounded by Leaf Count = O(N^(log2 3))! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing an interactive Recursion Tree Tracing and Node Metrics Analysis Engine.

```java
import java.util.*;

/**
 * Production-Grade Suite for Recursion Tree Visual Tracing,
 * Level Work Calculation, and Overlapping Subproblem Auditing.
 */
public class RecursiveTreesMaster {

    /**
     * Data class capturing metrics for a recursion tree level.
     */
    public static class LevelMetric {
        public int level;
        public int nodeCount;
        public long workPerNode;
        public long totalLevelWork;

        public LevelMetric(int level, int nodeCount, long workPerNode) {
            this.level = level;
            this.nodeCount = nodeCount;
            this.workPerNode = workPerNode;
            this.totalLevelWork = nodeCount * workPerNode;
        }

        @Override
        public String toString() {
            return String.format("Level %2d | Nodes: %6d | Work/Node: %6d | Total Work: %8d",
                    level, nodeCount, workPerNode, totalLevelWork);
        }
    }

    /**
     * Simulates and computes level-by-level work metrics for a balanced divide and conquer recurrence:
     * T(N) = a * T(N / b) + f(N)
     *
     * @param n initial input size N
     * @param a branching factor (number of child calls per node)
     * @param b shrink factor (input reduction divisor)
     * @return list of metrics per level
     */
    public List<LevelMetric> analyzeDivideAndConquerTree(int n, int a, int b) {
        List<LevelMetric> metrics = new ArrayList<>();
        if (n <= 0 || a <= 0 || b <= 1) return metrics;

        int level = 0;
        int currentNodes = 1;
        int currentSize = n;

        while (currentSize >= 1) {
            // Assume f(N) = N (Linear work per node)
            long workPerNode = currentSize;
            metrics.add(new LevelMetric(level, currentNodes, workPerNode));

            currentNodes *= a;   // Nodes multiply by branching factor 'a'
            currentSize /= b;    // Subproblem size divides by shrink factor 'b'
            level++;
        }

        return metrics;
    }

    /**
     * Audit overlapping subproblem calls in naive Fibonacci tree recursion.
     * Counts how many times each subproblem state is re-calculated.
     *
     * @param n Fibonacci number to compute
     * @param callFrequencyMap map tracking invocation frequency per subproblem state
     * @return Fibonacci result
     */
    public int auditFibonacciOverlaps(int n, Map<Integer, Integer> callFrequencyMap) {
        callFrequencyMap.put(n, callFrequencyMap.getOrDefault(n, 0) + 1);

        if (n <= 0) return 0;
        if (n == 1) return 1;

        return auditFibonacciOverlaps(n - 1, callFrequencyMap) + 
               auditFibonacciOverlaps(n - 2, callFrequencyMap);
    }
}
```

> **Quick Syntax:**
```java
// Level Work Calculation Line
long totalLevelWork = (long) Math.pow(a, level) * f(n / Math.pow(b, level));
```

---

## 7. Concrete Problem Examples & Applications

1. **Algorithm Analysis**:
   - Merge Sort Tree: $T(N) = 2T(N/2) + O(N) \implies O(N \log N)$ total work.
   - Binary Search Tree: $T(N) = T(N/2) + O(1) \implies O(\log N)$ total work.
   - Strassen's Matrix Multiplication: $T(N) = 7T(N/2) + O(N^2) \implies O(N^{\log_2 7}) \approx O(N^{2.81})$.

2. **Optimization Discovery**:
   - Visualizing redundant subproblem calls in Fibonacci / Coin Change trees to justify Dynamic Programming memoization.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class RecursiveTreesDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    RECURSION TREE ANALYSIS & METRICS SUITE      ");
        System.out.println("=================================================\n");

        RecursiveTreesMaster master = new RecursiveTreesMaster();

        // 1. Analyze Merge Sort Recurrence Tree: T(N) = 2T(N/2) + N for N = 16
        int n = 16, a = 2, b = 2;
        System.out.println("1. Merge Sort Recursion Tree Metrics (N = " + n + ", a = " + a + ", b = " + b + "):");
        List<RecursiveTreesMaster.LevelMetric> metrics = master.analyzeDivideAndConquerTree(n, a, b);

        long grandTotalWork = 0;
        for (RecursiveTreesMaster.LevelMetric lm : metrics) {
            System.out.println("   " + lm);
            grandTotalWork += lm.totalLevelWork;
        }
        System.out.println("   Grand Total Work Across All Levels: " + grandTotalWork);
        System.out.println("   Theoretical Bound N * (log2(N) + 1): " + (n * (4 + 1)));
        System.out.println("-------------------------------------------------");

        // 2. Audit Overlapping Calls in Naive Fibonacci (N = 5)
        int fibN = 5;
        Map<Integer, Integer> callMap = new TreeMap<>(Collections.reverseOrder());
        master.auditFibonacciOverlaps(fibN, callMap);

        System.out.println("2. Naive Fibonacci(" + fibN + ") Call Frequency Audit:");
        System.out.println("   Subproblem State -> Invocation Count:");
        for (Map.Entry<Integer, Integer> entry : callMap.entrySet()) {
            System.out.println("   fib(" + entry.getKey() + ") -> Called " + entry.getValue() + " times" +
                    (entry.getValue() > 1 ? " [REDUNDANT!]" : ""));
        }
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Recurrence Relation Pattern | Tree Height $H$ | Leaf Count | Level Work Pattern | Total Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **$T(N) = T(N/2) + O(1)$** | $\log_2 N$ | $1$ Leaf | Shrinks $O(1)$ | $\mathbf{O(\log N)}$ Log ⚡ |
| **$T(N) = 2T(N/2) + O(N)$**| $\log_2 N$ | $N$ Leaves | Constant $O(N)$ per level | $\mathbf{O(N \log N)}$ |
| **$T(N) = 2T(N/2) + O(1)$**| $\log_2 N$ | $N$ Leaves | Halves per level | $\mathbf{O(N)}$ Linear ⚡ |
| **$T(N) = 2T(N-1) + O(1)$**| $N$ | $2^N$ Leaves | Doubles per level | $\mathbf{O(2^N)}$ Exponential |
| **$T(N) = 4T(N/2) + O(N)$**| $\log_2 N$ | $N^2$ Leaves | Quadruples per level | $\mathbf{O(N^2)}$ Quadratic |

---

## 10. Edge Cases & Boundary Handling

1. **Unbalanced Subproblem Shrinking ($T(N) = T(N/3) + T(2N/3) + O(N)$)**:
   - The longest branch has height $\log_{3/2} N$, while the shortest branch has height $\log_3 N$.
   - The upper bound is governed by the longest path: $O(N \log_{3/2} N) = O(N \log N)$.

2. **Base Case Work Costs**:
   - If work at base case leaves is $O(1)$, total leaf work equals $(\text{Leaf Count}) \times O(1) = O(a^H)$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Ignoring Branching Factor Growth**:
  - Assuming tree height alone dictates complexity. A tree of height $\log_2 N$ with branching factor $a = 4$ performs $O(N^2)$ work, NOT $O(\log N)$!

* **Anti-Pattern 2: Confusing Call Tree Height with Node Count**:
  - Tree height $H = \log N$ does not mean $O(\log N)$ time if the tree has $N$ leaves!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 3-Step Master Theorem Shortcut via Recursion Trees:
> For $T(N) = a T(N/b) + f(N)$, compare $f(N)$ with the critical leaf count function $N^{\log_b a}$:
> 1. If $f(N) < N^{\log_b a} \implies$ **Leaf-Dominated**: $T(N) = \mathbf{\Theta(N^{\log_b a})}$.
> 2. If $f(N) = N^{\log_b a} \implies$ **Balanced**: $T(N) = \mathbf{\Theta(N^{\log_b a} \cdot \log N)}$.
> 3. If $f(N) > N^{\log_b a} \implies$ **Root-Dominated**: $T(N) = \mathbf{\Theta(f(N))}$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Recursion Tree Analysis | Master Theorem | Substitution Method |
| :--- | :--- | :--- | :--- |
| **Applicability** | **Universal for All Recurrences ⚡**| Restricted Form $aT(N/b)+f(N)$| Universal (Requires Guess) |
| **Visual Intuition** | **Extremely High ⚡** | Math Formula Only | Mathematical Proof |
| **Proof Rigor** | Medium (Provides Intuition) | High | Absolute Mathematical |

---

## 14. How to Recognize This in Questions

* **"Evaluate overall time complexity of a new divide-and-conquer algorithm"** $\rightarrow$ Recursion Tree Method.
* **"Identify redundant subproblem calls to justify DP"** $\rightarrow$ Overlapping Subproblem Call Tree Audit.

---

## 15. Frequently Asked Interview Questions

* **Q: How do you determine the height of a recursion tree where $N$ shrinks by a factor of $b$?**  
  *A:* Set the subproblem size at level $H$ to $1$: $N / b^H = 1 \implies b^H = N \implies H = \log_b N$.

* **Q: Why does Merge Sort perform $O(N \log N)$ work using a recursion tree analysis?**  
  *A:* The tree has height $\log_2 N$. At every level $l$, there are $2^l$ nodes each performing $N / 2^l$ work. Total level work $= 2^l \times (N / 2^l) = N$. Summing across $\log_2 N + 1$ levels gives $N (\log_2 N + 1) = O(N \log N)$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RECURSION TREES                                       |
+-----------------------------------------------------------------------+
| • Tree Parameters: Branching factor a, Shrink factor b, Height log_b N|
| • Level Work     : Nodes(l) * WorkPerNode(l) = a^l * f(N / b^l)       |
| • Total Work     : Sum of level work from l = 0 to log_b N            |
| • Work Patterns  : Root-Dominated -> O(f(N))                          |
|                    Balanced       -> O(f(N) * log N)                  |
|                    Leaf-Dominated -> O(N^(log_b a)) ⚡                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can draw a recursion tree for any given linear or divide-and-conquer recurrence.
- [ ] I can compute tree height $H = \log_b N$ and leaf node count $a^H$.
- [ ] I can calculate total work per level and sum work across all levels.
- [ ] I can categorize a recursion tree as Root-Dominated, Balanced, or Leaf-Dominated.
- [ ] I can audit overlapping subproblems in a call tree to justify Dynamic Programming.
