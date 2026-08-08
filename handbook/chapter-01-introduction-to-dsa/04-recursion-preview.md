# 04. Recursion Preview

## 1. Introduction
Recursion is a fundamental problem-solving technique where a method calls itself with a reduced subproblem until reaching a trivial base condition. In interviews, recursion provides the conceptual backbone for tree traversals, graph DFS, divide-and-conquer, and dynamic programming.

> **Important:** Every recursive function must have two mandatory components: (1) a **Base Case** to stop execution, and (2) a **Recursive Relation** that reduces the problem size toward the base case.

## 2. Core Concepts
* **Base Case**: The stopping condition that returns a constant value without making further recursive calls.
* **Recursive Step**: The self-referential call executed with smaller parameters ($n-1$, $n/2$, etc.).
* **Call Stack**: The implicit internal data structure (LIFO) managed by the JVM to store stack frames (parameters, local variables, return addresses) during execution.
* **Stack Overflow**: Exception thrown when recursive depth exceeds available JVM call stack memory (default limits $\approx 10,000$ calls depending on frame size).

> **Memory Trick:** **"Trust the Function (Leap of Faith)"**. When writing recursive code, assume `solve(n-1)` correctly returns the answer for size $n-1$, and focus solely on how to combine that result to solve for size $n$.

## 3. Characteristics / Properties
* **Tail Recursion vs Non-Tail Recursion**: Tail recursion occurs when the recursive call is the final statement in the function (optimizable by compilers into loops). Non-tail recursion performs operations after the recursive call returns.
* **Recursion vs Iteration**: Any recursive function can be converted to an iterative function using an explicit Stack data structure.
* **Branching Factor**: Number of recursive calls made per frame. Single branch $\rightarrow O(n)$ stack depth; dual branch (e.g., Fibonacci) $\rightarrow O(2^n)$ time without memoization.

## 4. Internal Working
JVM Call Stack execution flow for `factorial(3)`:

```
[ Call Phase - Pushing Frames ]       [ Return Phase - Popping Frames ]
| factorial(1) -> returns 1   |       | factorial(1) = 1              |
| factorial(2) -> waits f(1)  |  ==>  | factorial(2) = 2 * 1 = 2      |
| factorial(3) -> waits f(2)  |       | factorial(3) = 3 * 2 = 6      |
+-----------------------------+       +-------------------------------+
```

## 5. Visual Diagram
Tree Representation of Dual Branching Recursion (`fib(4)`):

```
                       fib(4)
                     /        \
                fib(3)        fib(2)
               /      \       /     \
          fib(2)     fib(1) fib(1)  fib(0)
         /      \
    fib(1)     fib(0)
```

## 6. Operations / Algorithms
General Template for Recursive Problem Solving:
1. Identify the base case(s) and return immediate values.
2. Define the subproblem parameters (e.g., `index + 1`, `left` and `right` pointers).
3. Perform pre-processing logic (if applicable).
4. Invoke recursive calls.
5. Perform post-processing logic (combining results).

> **Quick Syntax:**
```java
// Standard Recursive Template
public int solve(int n) {
    // 1. Base Case
    if (n <= 1) {
        return n;
    }
    // 2. Recursive Call & Processing
    return solve(n - 1) + solve(n - 2);
}
```

## 7. Examples
* **Factorial Calculation**: Single branch recursion $O(n)$ time, $O(n)$ stack space.
* **Fibonacci Numbers**: Dual branch naive recursion $O(2^n)$ time, $O(n)$ stack space.
* **Binary Tree Traversals**: Inorder, Preorder, Postorder traversals $O(n)$ time, $O(h)$ space (where $h$ is tree height).
* **Binary Search**: Divide-and-conquer single branch recursion $O(\log n)$ time, $O(\log n)$ stack space.

## 8. Java Code
Interview-ready Java implementation contrasting naive recursion with explicit accumulator tail recursion.

```java
public class RecursionPreviewDemo {

    // Standard Head/Non-Tail Recursion: Factorial
    public static long factorial(int n) {
        if (n <= 1) {
            return 1; // Base case
        }
        return n * factorial(n - 1); // Post-call multiplication
    }

    // Tail Recursion using Accumulator Pattern
    public static long factorialTail(int n, long accumulator) {
        if (n <= 1) {
            return accumulator; // Base case returns aggregated result
        }
        return factorialTail(n - 1, n * accumulator); // Pure tail call
    }

    // Binary Search (Recursive)
    public static int binarySearch(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Base case: Target not found
        }
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid; // Base case: Target found
        }
        if (arr[mid] > target) {
            return binarySearch(arr, target, left, mid - 1); // Search left half
        }
        return binarySearch(arr, target, mid + 1, right); // Search right half
    }

    public static void main(String[] args) {
        System.out.println("Factorial(5): " + factorial(5));
        System.out.println("FactorialTail(5): " + factorialTail(5, 1));

        int[] sorted = {10, 20, 30, 40, 50};
        System.out.println("Binary Search Index of 40: " + binarySearch(sorted, 40, 0, sorted.length - 1));
    }
}
```

## 9. Complexity Analysis
* **Time Complexity**: Sum of work done across all nodes in the recursion tree.
  * Formula: $\text{Time Complexity} = (\text{Total Recursive Nodes}) \times (\text{Work Per Node})$.
* **Space Complexity**: Maximum height/depth of the recursion call stack.
  * Single branch ($n \to n-1$): $O(n)$ stack frames.
  * Tree splitting ($n \to n/2$): $O(\log n)$ stack frames.

## 10. Edge Cases
* **Missing Base Case**: Causes infinite recursive looping leading to `java.lang.StackOverflowError`.
* **Incorrect Base Case Range**: E.g., handling $n=0$ but failing on negative numbers $n < 0$.
* **Excessive Recursion Depth**: Arrays/Strings of size $N = 10^5$ cause stack overflow in Java if recursion depth is $O(n)$. Convert to iteration or use explicit `Stack`.

## 11. Common Mistakes
* Forgetting that recursive call frames consume JVM stack memory (assuming space is $O(1)$ when no objects are created).
* Recalculating identical subproblems repeatedly without memoization (e.g., naive $O(2^n)$ Fibonacci).
* Mutating shared state/globals inside recursive branches without backtracking/restoring state.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** If an interviewer asks you to solve a problem recursively, ALWAYS mention the call stack space complexity! For instance, state: *"The algorithm takes $O(N)$ time and $O(H)$ auxiliary space where $H$ is the recursion stack depth."*

> **Memory Trick:** **"Base Case First, Shrink Input Second"**. Always write your stopping condition on line 1 of the function. Ensure every recursive step strictly reduces parameter distance to the base case.

## 13. Comparisons
| Characteristic | Recursion | Iteration |
| :--- | :--- | :--- |
| **Code Structure** | Compact, declarative, elegant | Requires explicit loop control (`for`/`while`) |
| **Memory Overhead** | High (allocates $O(h)$ JVM stack frames) | Low ($O(1)$ memory using loop variables) |
| **Execution Speed** | Slightly slower due to function call overhead | Faster (direct register/CPU loop jumps) |
| **State Management** | Implicitly handled by call stack | Explicitly managed via variables/Stack data structure |

## 14. How to Recognize This in Questions
* **Subproblem Overlap**: Problems asking for all combinations, permutations, or paths $\rightarrow$ Recursion / Backtracking.
* **Hierarchical Structure**: Traversing parent-child tree nodes or nested folders $\rightarrow$ Recursive DFS.
* **Divide & Conquer**: "Split array into halves, solve independently, and merge" $\rightarrow$ Recursion.

## 15. Frequently Asked Interview Questions
* **Q: Does Java support Automatic Tail Call Optimization (TCO)?**  
  *A:* No. Unlike Scala or Scheme, the Java Virtual Machine (JVM) does NOT eliminate tail-recursive call frames automatically. Tail recursive methods still consume stack frames in standard HotSpot JVM implementations.
* **Q: How do you prevent StackOverflowError in deep recursion?**  
  *A:* Either convert the recursive algorithm into an iterative loop using an explicit Java `Stack` / `ArrayDeque`, or increase the thread stack size via JVM parameter `-Xss` (though iteration is the preferred interview answer).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RECURSION PREVIEW                                    |
+-----------------------------------------------------------------------+
| • Recursion = Base Case (Stop) + Reduction Step (Shrink Input)         |
| • Space Complexity = Maximum Call Stack Depth (Height of Recursion)   |
| • JVM does NOT optimize Tail Recursion automatically                  |
| • Deep recursion (N >= 10^5) risks StackOverflowError -> Use Iteration|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the mandatory 2 parts of any recursive algorithm (Base case & reduction step).
- [ ] I can trace recursive calls using a recursion call stack frame diagram.
- [ ] I know how to calculate the time complexity from a recursion tree.
- [ ] I understand why recursion uses auxiliary space even without creating new objects.
- [ ] I can convert simple single-branch recursive functions into iterative loops.
