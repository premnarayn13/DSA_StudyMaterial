# 03. Big-Theta Notation

## 1. Introduction
Big-Theta Notation ($\Theta$) establishes the formal mathematical tight bound on an algorithm's execution time or space complexity as input size $n$ approaches infinity ($n \to \infty$). It signifies that an algorithm's execution steps are bounded both from above (Big-O) and from below (Big-Omega) by the exact same growth function $g(n)$.

> **Important:** Big-Theta describes an exact asymptotic fit ($\Theta(g(n)) = O(g(n)) \cap \Omega(g(n))$). It indicates that the worst-case and best-case performance scale at the precise same rate.

## 2. Core Concepts
* **Mathematical Definition**: A function $f(n) = \Theta(g(n))$ if there exist positive constants $c_1 > 0$, $c_2 > 0$, and $n_0 \ge 1$ such that $c_1 \cdot g(n) \le f(n) \le c_2 \cdot g(n)$ for all $n \ge n_0$.
* **Tight Envelope**: $f(n)$ is trapped between $c_1 g(n)$ and $c_2 g(n)$ for all large inputs $n$.
* **Equivalence Criterion**: $f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \text{ AND } f(n) = \Omega(g(n))$.

> **Memory Trick:** **"Θ = Sandwich / Tight Fit"**. Actual execution steps are sandwiched between two constant multiples of the exact same function $g(n)$.

## 3. Characteristics / Properties
* **Symmetry**: $f(n) = \Theta(g(n)) \iff g(n) = \Theta(f(n))$.
* **Strict Characterization**: Merge Sort is $\Theta(n \log n)$ because its best-case, worst-case, and average-case time complexities are ALL $O(n \log n)$ and $\Omega(n \log n)$.
* **Not Applicable to Conditional Algorithms**: Linear search is NOT $\Theta(n)$ overall because its best-case is $\Omega(1)$ while its worst-case is $O(n)$. (It is $\Theta(n)$ ONLY for its worst-case analysis).

## 4. Internal Working
Graph of $c_1 g(n) \le f(n) \le c_2 g(n)$ beyond threshold $n_0$:

```
  Execution Steps (T)
    ^
    |                       / c2 * g(n)   [Upper Ceiling]
    |                      /
    |          f(n)       / /             [Actual Steps trapped inside]
    |           /\       / /
    |          /  \_____/_/ c1 * g(n)     [Lower Floor]
    |   ______/        /
    |  /              /
    +----------------+--------------------> Input Size (n)
                     n0 (Threshold)
```

## 5. Visual Diagram
Big-Theta Sandwich Architecture:

```
  Upper Bound  -->  c₂ · g(n)   ===============================
                    f(n)       ------------------------------- (Actual steps)
  Lower Bound  -->  c₁ · g(n)   ===============================
```

## 6. Operations / Algorithms
Proving Big-Theta step-by-step:
1. Prove algorithm execution takes at most $c_2 g(n)$ steps $\implies f(n) = O(g(n))$.
2. Prove algorithm execution takes at least $c_1 g(n)$ steps $\implies f(n) = \Omega(g(n))$.
3. Conclude $f(n) = \Theta(g(n))$.

> **Quick Syntax:**
```java
// Unconditional Array Summation is Theta(n)
public static int sumArray(int[] arr) {
    int sum = 0;
    // ALWAYS executes exactly N iterations regardless of array contents -> Theta(n)
    for (int i = 0; i < arr.length; i++) {
        sum += arr[i];
    }
    return sum;
}
```

## 7. Examples
* **Merge Sort**: $\Theta(n \log n)$ in best, average, and worst cases.
* **Finding Maximum in Unsorted Array**: $\Theta(n)$ because every element MUST be inspected at least once.
* **Matrix Addition ($N \times N$)**: $\Theta(N^2)$ because every element in the $N \times N$ grid must be added.
* **Heap Sort**: $\Theta(n \log n)$ in all cases.

## 8. Java Code
Demonstrating an algorithm with an unconditional tight bound $\Theta(n)$:

```java
public class BigThetaDemo {

    // Finding Max and Min in single pass -> Theta(n) unconditional tight bound
    public static int[] findMinMax(int[] arr) {
        if (arr == null || arr.length == 0) return new int[]{};

        int min = arr[0];
        int max = arr[0];

        // Loop runs EXACTLY n-1 times for any input array configuration -> Theta(n)
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < min) min = arr[i];
            if (arr[i] > max) max = arr[i];
        }

        return new int[]{min, max};
    }

    public static void main(String[] args) {
        int[] data = {45, 12, 89, 3, 27};
        int[] result = findMinMax(data);
        System.out.println("Min: " + result[0] + ", Max: " + result[1]);
    }
}
```

## 9. Complexity Analysis
| Algorithm | Best Case | Worst Case | Is Tight Bound $\Theta$? |
| :--- | :--- | :--- | :--- |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | **YES $\Theta(n \log n)$** |
| **Matrix Addition** | $O(n^2)$ | $O(n^2)$ | **YES $\Theta(n^2)$** |
| **Linear Search** | $O(1)$ | $O(n)$ | **NO** (Only $\Theta(n)$ for worst-case) |
| **Quick Sort** | $O(n \log n)$ | $O(n^2)$ | **NO** (Average case is $\Theta(n \log n)$) |

## 10. Edge Cases
* **Misusing $\Theta$ for Variable Algorithms**: Saying *"Linear Search is $\Theta(n)$"* is technically inaccurate unless you explicitly qualify *"Linear Search worst-case time is $\Theta(n)$"*.
* **Constant Factor Width**: The constants $c_1$ and $c_2$ can be widely separated (e.g., $c_1 = 0.001$, $c_2 = 1000$), but as long as both bounds scale as $g(n)$, the algorithm is $\Theta(g(n))$.

## 11. Common Mistakes
* Using Big-O ($O$) when Big-Theta ($\Theta$) is technically more informative (though informal tech interview culture frequently uses "Big-O" when referring to tight bounds).
* Believing Big-Theta applies only when best-case equals worst-case for ALL inputs—Big-Theta can also specify the tight bound for a *specific* case (e.g., Average-Case Big-Theta).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** In formal computer science publications, $\Theta(n)$ is preferred over $O(n)$ when the bound is exact. In coding interviews, interviewers often ask for "Big-O", but providing a precise tight-bound answer demonstrates deeper mathematical rigor.

> **Memory Trick:** **"Theta = Total Exact Match"**.

## 13. Comparisons
| Metric | Big-O ($O$) | Big-Omega ($\Omega$) | Big-Theta ($\Theta$) |
| :--- | :--- | :--- | :--- |
| **Bound Type** | Upper Ceiling | Lower Floor | Exact Tight Envelope |
| **Condition** | $f \le c \cdot g$ | $f \ge c \cdot g$ | $c_1 g \le f \le c_2 g$ |
| **Merge Sort** | $O(n \log n)$ | $\Omega(n \log n)$ | $\Theta(n \log n)$ |
| **Linear Search (Overall)**| $O(n)$ | $\Omega(1)$ | No single $\Theta$ expression |

## 14. How to Recognize This in Questions
* **"Give the exact tight asymptotic bound"** $\rightarrow$ Provide $\Theta$ notation.
* **"Unconditional traversal algorithm"** $\rightarrow$ Almost certainly has a matching $O$ and $\Omega \implies \Theta$.

## 15. Frequently Asked Interview Questions
* **Q: Why is Heap Sort $\Theta(n \log n)$ in all cases?**  
  *A:* Because building the heap takes $\Theta(n)$ time, and popping $n$ elements each requires $O(\log n)$ heapify steps regardless of the input array's initial arrangement.
* **Q: Does an algorithm always have a Big-Theta bound?**  
  *A:* Yes, for any specific execution case (best, worst, or average). However, across *all* possible inputs, an algorithm only has a global Big-Theta bound if its best-case and worst-case functions scale asymptotically at the same rate.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BIG-THETA NOTATION                                   |
+-----------------------------------------------------------------------+
| • Big-Theta (Θ) = Exact Tight Bound (Sandwiched between c1*g & c2*g)  |
| • Exists when Big-O upper bound matches Big-Omega lower bound         |
| • Merge Sort = Θ(n log n) in ALL cases                                |
| • Unconditional array iterations (Sum, Max) = Θ(n)                    |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the formal mathematical inequality definition of Big-Theta.
- [ ] I can explain why Merge Sort is $\Theta(n \log n)$ across all input permutations.
- [ ] I understand why conditional algorithms (like Linear Search) lack a global $\Theta$ bound.
- [ ] I know how to prove $\Theta(g(n))$ by demonstrating matching $O(g(n))$ and $\Omega(g(n))$.
- [ ] I can distinguish between informal "Big-O" usage in interviews and formal Big-Theta notation.
