# 02. Time & Space Complexity

## 1. Introduction
Complexity analysis measures how an algorithm's execution time and memory footprint scale as the input size ($n$) grows toward infinity. In technical interviews, calculating complexity determines whether an approach passes strict execution time limits (usually $\le 1.0$ second / $10^8$ operations).

> **Important:** Time complexity measures the number of fundamental execution steps relative to input size $n$, NOT hardware clock time. Space complexity measures auxiliary memory allocated relative to $n$.

## 2. Core Concepts
* **Time Complexity**: Function $T(n)$ representing execution step growth rate.
* **Space Complexity**: Total memory consumed = Auxiliary Space (extra space allocated by algorithm) + Input Space.
* **Input Size Bottleneck**: An operation count of $10^8$ basic instructions takes roughly 1 second in modern Java execution environments.

> **Memory Trick:** **"Auxiliary is what YOU create"**. When an interviewer asks for space complexity, they usually mean **Auxiliary Space** (excluding the input data structures provided).

## 3. Characteristics / Properties
* **Dominant Term Rule**: Ignore lower-order terms and constant coefficients. $O(3n^2 + 5n + 100) \rightarrow O(n^2)$.
* **Tight Upper Bound**: Focus on worst-case execution guarantees unless specified otherwise.
* **Primitive vs Reference Memory**: Primitive types (`int`, `long`, `double`) occupy fixed stack memory, while objects (`Integer`, `ArrayList`, custom class nodes) incur object headers (12-16 bytes overhead in Java 64-bit JVM).

## 4. Internal Working
How different execution loops scale:

```
O(1)       : Direct Arithmetic / Index Access
O(log n)   : Input halved each step (e.g., n = n / 2)
O(n)       : Single loop over n elements
O(n log n) : Nested structure where inner operation takes log n (Divide & Conquer)
O(n²)      : Nested loop (Outer n * Inner n)
O(2ⁿ)      : Recursion branching twice per level (Subsets / Decision Tree)
O(n!)      : Permutation generation
```

## 5. Visual Diagram
Complexity Growth Curve Comparison:

```
Operations (T)
  ^
  |                                                / O(n!)
  |                                               /
  |                                              / O(2ⁿ)
  |                                             /
  |                                            / O(n²)
  |                                           /
  |                                          / O(n log n)
  |                                         /
  |                                        / O(n)
  |                                       /
  |______________________________________/ O(log n)
  |_______________________________________ O(1)
  +----------------------------------------------------> Input Size (n)
```

## 6. Operations / Algorithms
Determining complexity from code structure:
1. **Additive Rule**: Sequential loops add complexity. $O(a) + O(b) = O(a + b)$.
2. **Multiplicative Rule**: Nested loops multiply complexity. $O(a) \times O(b) = O(a \cdot b)$.
3. **Logarithmic Halving**: Any loop variable multiplied or divided by a constant $k > 1$ each iteration runs in $O(\log_k n)$.

> **Quick Syntax:**
```java
// O(log n) loop pattern
for (int i = 1; i < n; i *= 2) {
    // Halving search space or doubling pointer
}

// O(n^2) loop pattern
for (int i = 0; i < n; i++) {
    for (int j = i + 1; j < n; j++) {
        // Pair processing
    }
}
```

## 7. Examples
* **$O(1)$**: Accessing `arr[i]`, push/pop on stack, array length lookup.
* **$O(\log n)$**: Binary search, finding height of balanced binary tree, Euclidean GCD algorithm.
* **$O(n)$**: Linear search, single array traversal, finding minimum/maximum element.
* **$O(n \log n)$**: Merge sort, Quick sort (average), Heap sort, sorting primitives (`Arrays.sort()`).
* **$O(n^2)$**: Bubble sort, Selection sort, Insertion sort, matrix generation.
* **$O(2^n)$**: Generating all subsets of a set (power set recursion).
* **$O(n!)$**: Generating all permutations of a string of length $n$.

## 8. Java Code
Below is a code suite demonstrating various complexity patterns in Java.

```java
public class ComplexityExamples {

    // O(1) - Constant Time
    public static int getFirstElement(int[] arr) {
        return (arr != null && arr.length > 0) ? arr[0] : -1;
    }

    // O(log n) - Logarithmic Time
    public static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2; // Prevents integer overflow
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    // O(n) Time, O(1) Space - Linear Time
    public static int findSum(int[] arr) {
        int sum = 0;
        for (int val : arr) {
            sum += val;
        }
        return sum;
    }

    // O(n log n) Time - Sorting
    public static void sortArray(int[] arr) {
        java.util.Arrays.sort(arr); // Dual-Pivot Quicksort: O(n log n)
    }

    // O(n^2) Time, O(1) Auxiliary Space
    public static void printPairs(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                // System.out.println(arr[i] + ", " + arr[j]);
            }
        }
    }
}
```

## 9. Complexity Analysis
Understanding time bounds based on constraints:

| Input Size ($n$) | Target Complexity | Typical Algorithms |
| :--- | :--- | :--- |
| $n \le 10$ to $12$ | $O(n!)$ or $O(2^n \cdot n)$ | Permutations, Bitmask DP, Traveling Salesperson |
| $n \le 20$ to $25$ | $O(2^n)$ | Backtracking, Generating Subsets |
| $n \le 500$ | $O(n^3)$ | Floyd-Warshall, 3D Dynamic Programming |
| $n \le 5000$ | $O(n^2)$ | Matrix traversal, Pair combinations, DP on pairs |
| $n \le 10^5$ to $10^6$ | $O(n \log n)$ or $O(n)$ | Sorting, Segment Tree, Binary Search + Greedy |
| $n \ge 10^8$ | $O(\log n)$ or $O(1)$ | Math formulas, Binary Search on Answer |

## 10. Edge Cases
* **Recursion Stack Overhead**: Auxiliary space includes stack call frames. Deep recursion of depth $d$ takes $O(d)$ space.
* **String Concatenation in Loops**: In Java, `s += char` inside a loop takes $O(n^2)$ time because strings are immutable; use `StringBuilder` for $O(n)$.
* **Integer Overflow during Mid Calculation**: `(left + right) / 2` overflows when `left + right > Integer.MAX_VALUE`. Always use `left + (right - left) / 2`.

## 11. Common Mistakes
* Assuming space complexity only accounts for variables created inside loops (recursion stack space is often forgotten!).
* Counting amortized $O(1)$ dynamic array resizing as worst-case $O(n)$ per single element push.
* Ignoring log base ($O(\log_2 n)$ vs $O(\log_{10} n)$ differ only by constant factor $\frac{1}{\log_2 10}$, so both are $O(\log n)$).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Use problem input constraints ($N$) to deduce the required algorithm complexity BEFORE writing code! If $N = 10^5$, your solution MUST be $O(n \log n)$ or $O(n)$. An $O(n^2)$ solution will yield a **Time Limit Exceeded (TLE)** verdict.

> **Memory Trick:** **"Input Size to Complexity Guide"**:
> * $N \le 20 \rightarrow O(2^N)$
> * $N \le 500 \rightarrow O(N^3)$
> * $N \le 5000 \rightarrow O(N^2)$
> * $N \le 10^5 \rightarrow O(N \log N)$
> * $N \ge 10^8 \rightarrow O(\log N) \text{ or } O(1)$

## 13. Comparisons
| Time Complexity | Operations for $n = 1000$ | Feasible in 1 sec limit ($10^8$ ops)? |
| :--- | :--- | :--- |
| $O(1)$ | $1$ | Yes (Instant) |
| $O(\log n)$ | $\approx 10$ | Yes (Instant) |
| $O(n)$ | $1,000$ | Yes |
| $O(n \log n)$ | $\approx 10,000$ | Yes |
| $O(n^2)$ | $1,000,000$ ($10^6$) | Yes |
| $O(n^3)$ | $1,000,000,000$ ($10^9$) | **NO (TLE)** |
| $O(2^n)$ | $\approx 10^{301}$ | **NO (TLE)** |

## 14. How to Recognize This in Questions
* **$N \le 10^5$**: Demands $O(N)$ or $O(N \log N)$. Think Two Pointers, HashMap, Sorting, or Binary Search.
* **$N \le 1000$**: Permits $O(N^2)$. Think Nested Loops or Matrix Dynamic Programming.
* **Finding Minimal Operations under Constraints**: Signals Binary Search on Answer ($O(N \log (\text{Range}))$).

## 15. Frequently Asked Interview Questions
* **Q: What is the difference between Time Complexity and Execution Time?**  
  *A:* Execution time depends on CPU, hardware compiler, and load. Time complexity measures how operation counts grow abstractly as $n \to \infty$.
* **Q: Does recursion take extra space?**  
  *A:* Yes. Each recursive call allocates a stack frame to store parameters and local variables. Space complexity equals the maximum depth of the call tree.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TIME & SPACE COMPLEXITY                              |
+-----------------------------------------------------------------------+
| • 1 Second Constraint ≈ 10^8 Operations in Java JVM                   |
| • Space Complexity = Auxiliary Memory + Recursion Call Stack Depth    |
| • String Concatenation loop: String (O(n²)) vs StringBuilder (O(n))    |
| • Prevents Mid Overflow: mid = left + (right - left) / 2               |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can derive time complexity for single, nested, and logarithmic loops.
- [ ] I can calculate auxiliary space complexity, including recursion stack frames.
- [ ] I know how to deduce expected complexity from input size constraints $N$.
- [ ] I know how to avoid integer overflow when calculating midpoints.
- [ ] I understand why `StringBuilder` must be used over `String` concatenation in loops.
