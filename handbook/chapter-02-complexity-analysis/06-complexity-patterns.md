# 06. Complexity Patterns

## 1. Introduction
Recognizing recurring code structures and algorithmic patterns is essential for rapid time and space complexity evaluation in technical interviews. By identifying standard structural archetypes (linear loops, logarithmic halving, two-pointer convergence, recursive branching), you can instantly deduce time and auxiliary space bounds without writing manual recurrence trees.

> **Important:** Master these standard code patterns to analyze code complexity in under 10 seconds during interview coding rounds.

## 2. Core Concepts
* **Pattern 1: Constant Iteration $O(1)$**: Loops with hardcoded bounds independent of input parameters ($N$).
* **Pattern 2: Linear Traversal $O(N)$**: Single loop running from $0$ to $N$ with constant step increments.
* **Pattern 3: Logarithmic Reduction $O(\log N)$**: Loop variables multiplied or divided by a constant factor $k \ge 2$ each iteration.
* **Pattern 4: Linearithmic Combination $O(N \log N)$**: Outer loop running $N$ times with inner logarithmic loop (or divide-and-conquer splitting).
* **Pattern 5: Polynomial Expansion $O(N^k)$**: $k$-level deeply nested loops each running $N$ times.
* **Pattern 6: Branching Decision Tree $O(B^D)$**: Recursive functions branching $B$ times per frame down to depth $D$.

> **Memory Trick:** **"Multiply step `*=2` $\rightarrow O(\log N)$, Divide range `/2` $\rightarrow O(\log N)$, Branch twice `f(n-1)+f(n-2)` $\rightarrow O(2^N)$"**.

## 3. Characteristics / Properties
* **Pattern Analysis Summary Matrix**:

```
Loop Condition                     Step Modifier        Time Complexity
-----------------------------------------------------------------------
for (i = 0; i < N; i++)            i++                  O(N)
for (i = 1; i < N; i *= 2)         i *= 2               O(log N)
for (i = N; i > 0; i /= 2)         i /= 2               O(log N)
for (i = 0; i < N; i += k)         i += k (constant)    O(N)
for (i = 0; i * i < N; i++)        i++                  O(sqrt(N))
for (i = 0; i < N; i++) 
  for (j = 0; j < i; j++)          j++                  O(N²)
```

## 4. Internal Working
Visualizing loop step reductions:

```
[ Logarithmic Reduction: i *= 2 ]
i = 1 --> 2 --> 4 --> 8 --> 16 ... N
Total Steps = log₂ N iterations

[ Square Root Bound: i * i < N ]
i = 1 --> 2 --> 3 --> 4 ... √N
Total Steps = √N iterations
```

## 5. Visual Diagram
Tree Branching vs Loop Complexity Archetypes:

```
       [ Single Loop O(N) ]                 [ Dual Branch Recursion O(2^N) ]
  ( 0 ) -> ( 1 ) -> ( 2 ) ... ( N )                        ( N )
                                                         /       \
                                                   ( N-1 )      ( N-1 )
                                                   /     \      /     \
                                                (N-2)   (N-2) (N-2)  (N-2)
```

## 6. Operations / Algorithms
Code Pattern Identification Guide:
1. Locate loop counters or recursive parameters.
2. Check step modification (`+1`, `*2`, `/2`, `-1`).
3. Check nesting depth ($k$ levels $\rightarrow O(N^k)$).
4. Evaluate auxiliary data structure allocation inside loops.

> **Quick Syntax:**
```java
// Pattern: Square Root O(sqrt(N))
for (int i = 1; i * i <= n; i++) {
    // Prime factor checking or trial division
}

// Pattern: Two-Pointer Convergence O(N)
int left = 0, right = n - 1;
while (left < right) {
    if (condition) left++;
    else right--;
}
```

## 7. Examples
* **$O(1)$**: `for (int i = 0; i < 100; i++)` (Constant bound).
* **$O(\sqrt{N})$**: Finding divisors of $N$ via `for (int i = 1; i * i <= N; i++)`.
* **$O(N)$**: Two-pointer array traversal (`while (left < right)` moves $N$ steps total).
* **$O(N \log N)$**: `Arrays.sort(primitiveArray)` (Dual-Pivot Quicksort).
* **$O(2^N)$**: Recursive Subset generation (`generateSubsets(index + 1)` called twice).
* **$O(N!)$**: Recursive Permutation generation (`generatePermutations(remaining)`).

## 8. Java Code
Code suite illustrating the 6 foundational complexity code patterns in Java:

```java
public class ComplexityPatternsDemo {

    // Pattern 1: O(sqrt(N)) - Square Root Loop
    public static int countDivisors(int n) {
        int count = 0;
        for (int i = 1; i * i <= n; i++) {
            if (n % i == 0) {
                count += (i * i == n) ? 1 : 2;
            }
        }
        return count; // O(sqrt(N)) time
    }

    // Pattern 2: O(N) - Two Pointer Converging Loop
    public static boolean twoSumSorted(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left < right) { // Runs at most N steps total -> O(N)
            int sum = arr[left] + arr[right];
            if (sum == target) return true;
            if (sum < target) left++;
            else right--;
        }
        return false;
    }

    // Pattern 3: O(N log N) - Outer Linear, Inner Logarithmic
    public static void processGrid(int n) {
        int ops = 0;
        for (int i = 0; i < n; i++) {           // Runs N times
            for (int j = 1; j < n; j *= 2) {     // Runs log2(N) times
                ops++;
            }
        }
        System.out.println("N = " + n + ", Executed " + ops + " ops (O(N log N)).");
    }

    public static void main(String[] args) {
        System.out.println("Divisors of 36: " + countDivisors(36));
        int[] sorted = {1, 3, 5, 8, 11, 15};
        System.out.println("Two Sum Target 13 Found? " + twoSumSorted(sorted, 13));
        processGrid(16);
    }
}
```

## 9. Complexity Analysis
Master Pattern-to-Complexity Reference Table:

| Code Pattern Archetype | Step Operation | Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Fixed Loop (`i < 100`)** | $i = i + 1$ | $O(1)$ | $O(1)$ |
| **Simple Loop (`i < N`)** | $i = i + 1$ | $O(N)$ | $O(1)$ |
| **Step Halving (`i /= 2`)** | $i = i / 2$ | $O(\log N)$ | $O(1)$ |
| **Square Root (`i * i <= N`)**| $i = i + 1$ | $O(\sqrt{N})$ | $O(1)$ |
| **Dependent Inner Loop** | $j = i \dots N$ | $O(N^2)$ | $O(1)$ |
| **Binary Tree Recursion** | 2 calls per node | $O(2^N)$ naive | $O(N)$ stack space |
| **N-Way Branching Recursion**| $N$ calls per node | $O(N!)$ | $O(N)$ stack space |

## 10. Edge Cases
* **Outer Variable Mutation inside Inner Loop**: If inner loop modifies outer loop index `i += j`, total iterations drop to $O(N)$!
* **String Substring in Loop**: `s.substring(i, j)` takes $O(j - i)$ time! A nested loop creating substrings runs in $O(N^3)$ total time, NOT $O(N^2)$.

## 11. Common Mistakes
* Assuming two pointers `left` and `right` running in a `while` loop take $O(N^2)$ time because there are two pointer variables (it takes $O(N)$ because the distance `right - left` decreases by at least 1 each iteration).
* Forgetting that `String.substring()` in Java creates a copy of the characters ($O(k)$ time/space).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Watch out for `String.substring(start, end)` inside loops! In Java 7+, `substring()` copies the underlying `char[]` array, taking $O(K)$ time where $K$ is substring length.

> **Memory Trick:** **"Pointer Distance Bounds total iterations"**. In Two-Pointer algorithms, total iterations equal `right - left` $\le N \implies O(N)$ time complexity.

## 13. Comparisons
| Pattern Archetype | Input Scale $N = 10^6$ Ops | Real-world Verdict |
| :--- | :--- | :--- |
| **$O(\log N)$** | $\approx 20$ operations | Instantaneous |
| **$O(\sqrt{N})$** | $1,000$ operations | Instantaneous |
| **$O(N)$** | $1,000,000$ operations | Fast ($\approx 1$ ms) |
| **$O(N \log N)$** | $\approx 20,000,000$ operations | Highly Efficient ($\approx 0.05$ sec) |
| **$O(N^2)$** | $1,000,000,000,000$ ops | **Time Limit Exceeded (TLE)** |

## 14. How to Recognize This in Questions
* **"Find pair summing to Target in Sorted Array"** $\rightarrow$ Two Pointers ($O(N)$ time, $O(1)$ space).
* **"Find prime factors or divisors"** $\rightarrow$ Square Root Loop ($O(\sqrt{N})$ time).

## 15. Frequently Asked Interview Questions
* **Q: What is the complexity of `for (int i = 1; i <= N; i *= 2)`?**  
  *A:* $O(\log_2 N)$ logarithmic time because $i$ takes values $1, 2, 4, 8, \dots, 2^k \le N \implies k = \log_2 N$.
* **Q: What is the complexity of `for (int i = 0; i < N; i++) for (int j = 0; j < i; j++)`?**  
  *A:* $O(N^2)$ because total iterations = $0 + 1 + 2 + \dots + (N-1) = \frac{N(N-1)}{2} = \frac{1}{2}N^2 - \frac{1}{2}N = O(N^2)$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: COMPLEXITY PATTERNS                                  |
+-----------------------------------------------------------------------+
| • Step doubling (i *= 2) -> O(log N)                                  |
| • Square root condition (i * i <= N) -> O(sqrt(N))                    |
| • Two-Pointer convergence (left < right) -> O(N)                      |
| • String.substring() inside loop -> O(N³) [Not O(N²)]                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can instantly recognize $O(\log N)$, $O(\sqrt{N})$, $O(N)$, and $O(N^2)$ code patterns.
- [ ] I can derive the exact operation sum for dependent nested loops $\frac{N(N-1)}{2}$.
- [ ] I know why Two-Pointer while loops run in $O(N)$ time.
- [ ] I understand the hidden $O(K)$ complexity of `String.substring()`.
- [ ] I can recognize recursive branching factor complexity $O(B^D)$.
