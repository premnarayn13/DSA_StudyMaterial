# 01. Big-O Notation

## 1. Introduction
Big-O Notation ($O$) establishes the formal mathematical upper bound on the execution time or auxiliary space of an algorithm as the input size $n$ approaches infinity ($n \to \infty$). In technical coding interviews, Big-O is the standard tool used to evaluate worst-case algorithmic performance.

> **Important:** Big-O measures the asymptotic worst-case growth rate. It provides a strict upper bound guarantee: the algorithm will NEVER exceed this execution ceiling.

## 2. Core Concepts
* **Mathematical Definition**: A function $f(n) = O(g(n))$ if there exist positive constants $c > 0$ and $n_0 \ge 1$ such that $f(n) \le c \cdot g(n)$ for all $n \ge n_0$.
* **Worst-Case Focus**: In interview settings, $O(g(n))$ guarantees that under the most adverse input permutations, execution time scales at most proportionally to $g(n)$.
* **Simplification Rules**:
  1. Drop constant coefficients: $O(5 \cdot n^2) \rightarrow O(n^2)$.
  2. Drop non-dominant terms: $O(n^3 + 100n^2 + 5000) \rightarrow O(n^3)$.

> **Memory Trick:** **"O = Upper Limit / Ceiling"**. Think of Big-O as an architectural ceiling above your algorithm's step count; actual execution will sit under or touch this ceiling.

## 3. Characteristics / Properties
* **Dominance Hierarchy**: $O(1) < O(\log n) < O(\sqrt{n}) < O(n) < O(n \log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)$.
* **Upper Bound Flexibility**: Technically, if an algorithm is $O(n)$, it is also $O(n^2)$ and $O(2^n)$, but in interviews you MUST state the tightest possible upper bound.
* **Space-Time Trade-off**: Improving Big-O time complexity often requires increasing Big-O space complexity (e.g., using a Hash Table $O(n)$ space to reduce search from $O(n)$ to $O(1)$ time).

## 4. Internal Working
Graph of $f(n) \le c \cdot g(n)$ beyond threshold $n_0$:

```
  Execution Steps (T)
    ^
    |                       / c * g(n)  [Big-O Upper Ceiling]
    |                      /
    |          f(n)       /             [Actual Algorithm Steps]
    |           /\       /
    |          /  \_____/
    |   ______/        /
    |  /              /
    +----------------+--------------------> Input Size (n)
                     n0 (Threshold)
```

## 5. Visual Diagram
Big-O Hierarchy Ladder:

```
Fastest / Best Scaling  ^  O(1)        --> Constant
                        |  O(log n)    --> Logarithmic
                        |  O(n)        --> Linear
                        |  O(n log n)  --> Linearithmic
                        |  O(n²)       --> Quadratic
                        |  O(2ⁿ)       --> Exponential
Slowest / TLE Threshold v  O(n!)       --> Factorial
```

## 6. Operations / Algorithms
Determining Big-O step-by-step:
1. Express total execution steps $T(n)$ as a function of input parameters.
2. Identify loops, recursive depth, and internal operations.
3. Apply dominant term rule to isolate the asymptotic term.

> **Quick Syntax:**
```java
// Identifying O(n log n) pattern in code
public void printLogN(int n) {
    for (int i = 0; i < n; i++) {           // O(n) outer loop
        for (int j = 1; j < n; j *= 2) {     // O(log n) inner loop
            // Step count: n * log2(n) -> O(n log n)
        }
    }
}
```

## 7. Examples
* **$O(1)$**: Accessing array index `arr[3]`, computing `Math.abs(x)`.
* **$O(\log n)$**: Binary search on a sorted array of size $n$.
* **$O(n)$**: Single loop finding maximum element in an unsorted array.
* **$O(n \log n)$**: Merge sort, Quick sort average case.
* **$O(n^2)$**: Brute-force two-sum using nested loops.
* **$O(2^n)$**: Recursive generation of all subsets (Power Set).

## 8. Java Code
Demonstrating code patterns for distinct Big-O classes in Java:

```java
public class BigONotationDemo {

    // O(1) - Constant Time
    public static int getHead(int[] arr) {
        return (arr != null && arr.length > 0) ? arr[0] : -1;
    }

    // O(n) - Linear Time
    public static boolean containsTarget(int[] arr, int target) {
        for (int val : arr) {
            if (val == target) return true;
        }
        return false;
    }

    // O(n^2) - Quadratic Time
    public static int countDuplicates(int[] arr) {
        int duplicates = 0;
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (arr[i] == arr[j]) duplicates++;
            }
        }
        return duplicates;
    }

    public static void main(String[] args) {
        int[] data = {5, 2, 9, 1, 5, 6};
        System.out.println("O(1) Head: " + getHead(data));
        System.out.println("O(n) Search: " + containsTarget(data, 9));
        System.out.println("O(n^2) Duplicates: " + countDuplicates(data));
    }
}
```

## 9. Complexity Analysis
| Code Pattern | Operation Step Formula | Big-O Simplification |
| :--- | :--- | :--- |
| **Single Loop ($1 \dots n$)** | $T(n) = c_1 \cdot n + c_2$ | $O(n)$ |
| **Nested Loop ($1 \dots n \times 1 \dots n$)** | $T(n) = c_1 \cdot n^2 + c_2 \cdot n$ | $O(n^2)$ |
| **Nested Dependent Loop ($i = 0 \dots n, j = i \dots n$)** | $T(n) = \frac{n(n+1)}{2} = \frac{1}{2}n^2 + \frac{1}{2}n$ | $O(n^2)$ |
| **Divide by 2 Loop (`i /= 2`)** | $T(n) = \log_2 n + 1$ | $O(\log n)$ |

## 10. Edge Cases
* **Constants Matter for Small Inputs**: $T_1(n) = 1000n$ is $O(n)$ and $T_2(n) = n^2$ is $O(n^2)$. However, for $n < 1000$, $T_2(n)$ runs faster!
* **Multiple Constraints**: Input with both $N$ elements and $K$ queries is $O(N + K)$ if sequential or $O(N \cdot K)$ if nested.
* **Variable Bounds**: A loop running `for (int i = 0; i < Math.min(n, 100); i++)` is $O(1)$ constant time because the cap is 100!

## 11. Common Mistakes
* Dropping variables when multiple distinct inputs exist (e.g., calling $O(N + M)$ simply $O(N)$).
* Assuming Big-O only measures worst-case time—it also applies to auxiliary memory / stack frames.
* Confusing loop iteration count with total operations when inner operations are non-constant (e.g., `list.contains()` inside a loop makes it $O(n^2)$, not $O(n)$).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never forget hidden method complexities! Methods like `String.indexOf()`, `List.contains()`, `Arrays.copyOf()`, or `Collections.sort()` are NOT $O(1)$. Always factor their internal Big-O into your total complexity calculation.

> **Memory Trick:** **"Nested = Multiply, Sequential = Add"**:
> * Sequential loops: $O(A) + O(B) = O(A + B)$
> * Nested loops: $O(A) \times O(B) = O(A \cdot B)$

## 13. Comparisons
| Feature | Big-O ($O$) | Big-Omega ($\Omega$) | Big-Theta ($\Theta$) |
| :--- | :--- | :--- | :--- |
| **Bound Type** | Upper Bound (Ceiling) | Lower Bound (Floor) | Tight Bound (Exact) |
| **Mathematical Meaning** | $f(n) \le c \cdot g(n)$ | $f(n) \ge c \cdot g(n)$ | $c_1 g(n) \le f(n) \le c_2 g(n)$ |
| **Interview Purpose** | Standard requirement | Rarely required | Best formal description |

## 14. How to Recognize This in Questions
* **"Find worst-case time/space limit"** $\rightarrow$ Calculate Big-O upper bound.
* **"Constraints: $N \le 10^5$"** $\rightarrow$ Solution must be $O(N)$ or $O(N \log N)$.

## 15. Frequently Asked Interview Questions
* **Q: Is an algorithm of $O(n)$ always faster than $O(n^2)$?**  
  *A:* Asymptotically (for large $n$), yes. However, for tiny values of $n$, large constant factors in the $O(n)$ algorithm could make it run slower than the $O(n^2)$ algorithm.
* **Q: What is the Big-O complexity of `ArrayList.add()` in Java?**  
  *A:* It is **Amortized $O(1)$**. Most insertions take $O(1)$ time, but when the backing array fills up, a reallocation copy step takes $O(n)$ time. Averaged over $n$ insertions, cost per insertion is $O(1)$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BIG-O NOTATION                                       |
+-----------------------------------------------------------------------+
| • Big-O = Upper Bound Guarantee (Worst Case)                          |
| • Drop constants and lower-order terms: O(3n² + 10n) -> O(n²)         |
| • Sequential Loops = O(A + B) | Nested Loops = O(A * B)                |
| • Watch for hidden method costs: List.contains() is O(n), NOT O(1)    |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the formal mathematical inequality definition of Big-O.
- [ ] I know the Big-O dominance hierarchy from $O(1)$ to $O(n!)$.
- [ ] I can derive Big-O complexity for nested loops and dependent loops.
- [ ] I can identify hidden $O(n)$ library methods in Java code.
- [ ] I know how to combine complexities for multiple input parameters ($N, M$).
