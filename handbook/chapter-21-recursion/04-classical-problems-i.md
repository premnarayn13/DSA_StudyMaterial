# 04. Classical Recursion Problems I: Tower of Hanoi, Fibonacci & Josephus Problem

## 1. Introduction
**Classical Recursion Problems I** focuses on foundational mathematical and structural puzzles that illustrate how complex multi-step processes decompose elegantly into recursive subproblems. Benchmark problems including the **Tower of Hanoi**, **Fibonacci Sequence Generation**, and the **Josephus Elimination Problem** serve as essential training grounds for mastering Divide and Conquer, Call Stack Unwinding, and Recurrence Relation Analysis. Solving these problems requires translating physical/mathematical rules into precise recursive state transitions executing in time complexities ranging from **$O(\log N)$** and **$O(N)$** to exponential **$O(2^N)$**.

> **Important:** Core Invariants of Classical Recursion Problems I:
> 1. **Tower of Hanoi Rule**: To move $N$ disks from Source $A$ to Destination $C$ using Auxiliary $B$:
>    - Move top $N-1$ disks from $A$ to $B$ using $C$.
>    - Move remaining $N$-th disk directly from $A$ to $C$.
>    - Move $N-1$ disks from $B$ to $C$ using $A$.
>    - Minimum Total Moves: $T(N) = 2^N - 1$.
> 2. **Josephus Elimination Recurrence**:
>    - For $n$ people standing in a circle eliminated every $k$-th step, 0-indexed position:
>      $$J(n, k) = (J(n - 1, k) + k) \pmod n \quad \text{with Base Case } J(1, k) = 0$$ ⚡

```
Tower of Hanoi Disks Transfer Topography (N = 3 Disks):
Step 1: Move 2 disks from Source (A) -> Aux (B) using Dest (C)
Step 2: Move disk 3 directly from Source (A) -> Dest (C)
Step 3: Move 2 disks from Aux (B) -> Dest (C) using Source (A)

Total Moves = 2^3 - 1 = 7 Moves! ⚡
```

---

## 2. Core Concepts & Classical Problem Strategy Matrix

### 2.1 Problem Strategy Matrix
```
Classical Recursion Problems I Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem               | State Recurrence  | Base Case Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Tower of Hanoi**    | $T(N) = 2T(N-1)+1$| $N = 1$ (1 move)  | **$O(2^N)$ Exponential ⚡**|
| **Fibonacci Sequence**| $F(N)=F(N-1)+F(N-2)$| $N=0 \to 0, N=1 \to 1$| **$O(2^N)$ Naive / $O(N)$ Memo**|
| **Josephus Problem**  | $J(n)=(J(n-1)+k)\%n$| $n = 1 \to 0$     | **$O(N)$ Linear ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Hanoi: 2^N - 1 moves! Josephus 0-index formula: J(n, k) = (J(n-1, k) + k) % n!"**

---

## 3. Characteristics & $O(2^N)$ Hanoi Complexity Proof

### 3.1 Mathematical Proof of Tower of Hanoi Moves $2^N - 1$
Let $T(N)$ be the number of moves required to solve Tower of Hanoi for $N$ disks:
* Recurrence Relation: $T(N) = 2 T(N-1) + 1$, with $T(1) = 1$.
* Unfolding the recurrence:
  $$T(N) = 2(2 T(N-2) + 1) + 1 = 2^2 T(N-2) + 2 + 1$$
  $$T(N) = 2^k T(N-k) + \sum_{i=0}^{k-1} 2^i$$
* Substituting $k = N-1$ (since $T(1) = 1$):
  $$T(N) = 2^{N-1}(1) + (2^{N-1} - 1) = 2^N - 1$$
* Total Moves = $\mathbf{2^N - 1 = O(2^N) \text{ Exponential Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing the Josephus Problem

The **Josephus Problem** considers $n$ people standing in a circle numbered $0 \dots n-1$. Counting starts from $0$, and every $k$-th person is executed around the circle until only $1$ survivor remains.

```
Tracing Josephus(n = 5, k = 2):

Circle of 5 People: [0, 1, 2, 3, 4]
1st Elimination (count 2): Person 1 eliminated. Remaining: [0, 2, 3, 4]
2nd Elimination (count 2): Person 3 eliminated. Remaining: [0, 2, 4]
3rd Elimination (count 2): Person 0 eliminated. Remaining: [2, 4]
4th Elimination (count 2): Person 4 eliminated. Remaining: [2]

Survivor = 2!

Recursive Computation (Bottom-Up Unwinding):
J(1, 2) = 0
J(2, 2) = (J(1, 2) + 2) % 2 = (0 + 2) % 2 = 0
J(3, 2) = (J(2, 2) + 2) % 3 = (0 + 2) % 3 = 2
J(4, 2) = (J(3, 2) + 2) % 4 = (2 + 2) % 4 = 0
J(5, 2) = (J(4, 2) + 2) % 5 = (0 + 2) % 5 = 2!

Exact Match: Survivor is Index 2! ✅ (Calculated in O(N) Time!)
```

---

## 5. Visual Diagram: Tower of Hanoi Move Sequence (N = 3)

```
Initial State:          Tower A: [1, 2, 3]    Tower B: []          Tower C: []

Move 1 (A -> C):        Tower A: [2, 3]       Tower B: []          Tower C: [1]
Move 2 (A -> B):        Tower A: [3]          Tower B: [2]         Tower C: [1]
Move 3 (C -> B):        Tower A: [3]          Tower B: [1, 2]      Tower C: []
Move 4 (A -> C):        Tower A: []           Tower B: [1, 2]      Tower C: [3]  <-- Largest Disk Placed!
Move 5 (B -> A):        Tower A: [1]          Tower B: [2]         Tower C: [3]
Move 6 (B -> C):        Tower A: [1]          Tower B: []          Tower C: [2, 3]
Move 7 (A -> C):        Tower A: []           Tower B: []          Tower C: [1, 2, 3] <-- Complete! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Tower of Hanoi, Josephus Elimination, and recursive string/array utilities.

```java
import java.util.*;

/**
 * Production-Grade Implementation of Classical Recursion Problems I:
 * Tower of Hanoi, Josephus Problem, and Fibonacci Mechanics.
 */
public class ClassicalProblemsIMaster {

    // =========================================================================
    // 1. TOWER OF HANOI (Exponential Disks Transfer O(2^N))
    // =========================================================================
    /**
     * Solves Tower of Hanoi puzzle recursively and returns all step moves.
     *
     * @param n number of disks
     * @param src source rod name
     * @param aux auxiliary rod name
     * @param dest destination rod name
     * @return list of move instruction strings
     */
    public List<String> solveHanoi(int n, char src, char aux, char dest) {
        List<String> moves = new ArrayList<>();
        if (n <= 0) return moves;

        hanoiHelper(n, src, aux, dest, moves);
        return moves;
    }

    private void hanoiHelper(int n, char src, char aux, char dest, List<String> moves) {
        // Base Case: Only 1 disk to move directly
        if (n == 1) {
            moves.add("Move disk 1 from " + src + " -> " + dest);
            return;
        }

        // Step 1: Move top n-1 disks from src to aux using dest
        hanoiHelper(n - 1, src, dest, aux, moves);

        // Step 2: Move current nth disk from src to dest
        moves.add("Move disk " + n + " from " + src + " -> " + dest);

        // Step 3: Move n-1 disks from aux to dest using src
        hanoiHelper(n - 1, aux, src, dest, moves);
    }

    // =========================================================================
    // 2. JOSEPHUS PROBLEM (0-Indexed Circle Elimination O(N))
    // =========================================================================
    /**
     * Finds 0-based index of the survivor in Josephus circle elimination.
     * Recurrence: J(n, k) = (J(n - 1, k) + k) % n
     *
     * @param n number of people (1-indexed count)
     * @param k step count for elimination
     * @return 0-based index of the survivor
     */
    public int josephus(int n, int k) {
        if (n <= 0 || k <= 0) {
            throw new IllegalArgumentException("n and k must be positive integers.");
        }
        // Base Case: 1 person remaining -> 0-based index 0 survivor
        if (n == 1) {
            return 0;
        }
        // Subproblem Reduction & Modular Shift
        return (josephus(n - 1, k) + k) % n;
    }

    /**
     * Converts Josephus 0-based index result to 1-based index survivor.
     */
    public int josephusOneBased(int n, int k) {
        return josephus(n, k) + 1;
    }

    // =========================================================================
    // 3. RECURSIVE STRING REVERSAL (Linear Memory Stack O(N))
    // =========================================================================
    /**
     * Reverses a string recursively.
     *
     * @param str input string
     * @return reversed string
     */
    public String reverseString(String str) {
        if (str == null || str.length() <= 1) {
            return str;
        }
        // Subproblem: last char + reverse of remaining substring
        return reverseString(str.substring(1)) + str.charAt(0);
    }
}
```

> **Quick Syntax:**
```java
// Josephus Recurrence Line (0-based)
public int josephus(int n, int k) {
    if (n == 1) return 0;
    return (josephus(n - 1, k) + k) % n;
}
```

---

## 7. Concrete Problem Examples & Applications

1. **Tower of Hanoi**:
   - Backup/Restore Operations in Nested Hierarchies.
   - Stack-Based Disk Moving Puzzles.

2. **Josephus Elimination**:
   - Round-Robin Process Scheduling with Removal.
   - Circular Ring Network Node Elimination.

3. **Recursive String Processing**:
   - String Reversal and Palindrome Parsing.
   - Parsing Nested Expressions (LISP / Calculator Evaluators).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class ClassicalProblemsIDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    CLASSICAL RECURSION PROBLEMS I DEMONSTRATION ");
        System.out.println("=================================================\n");

        ClassicalProblemsIMaster master = new ClassicalProblemsIMaster();

        // 1. Tower of Hanoi Test (N = 3 Disks)
        int disks = 3;
        List<String> hanoiMoves = master.solveHanoi(disks, 'A', 'B', 'C');
        System.out.println("1. Tower of Hanoi (" + disks + " Disks, Total Moves = " + hanoiMoves.size() + "):");
        for (String move : hanoiMoves) {
            System.out.println("   " + move);
        }
        System.out.println("-------------------------------------------------");

        // 2. Josephus Problem Test
        int n = 5, k = 2;
        int survivor0 = master.josephus(n, k);
        int survivor1 = master.josephusOneBased(n, k);
        System.out.println("2. Josephus Survivor (n = " + n + ", k = " + k + "):");
        System.out.println("   0-Based Survivor Index: " + survivor0);
        System.out.println("   1-Based Survivor Index: " + survivor1);
        System.out.println("-------------------------------------------------");

        // 3. String Reversal Test
        String original = "antigravity";
        String reversed = master.reverseString(original);
        System.out.println("3. Recursive String Reversal:");
        System.out.println("   Original: " + original);
        System.out.println("   Reversed: " + reversed);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Classical Problem | Time Complexity | Auxiliary Stack Space | Total Moves / Recurrence | Key Driver |
| :--- | :--- | :--- | :--- | :--- |
| **Tower of Hanoi** | $\mathbf{O(2^N)}$ Exponential | $\mathbf{O(N)}$ Linear Stack | $T(N) = 2^N - 1$ moves | Dual recursive calls |
| **Josephus Problem** | $\mathbf{O(N)}$ Linear ⚡ | $\mathbf{O(N)}$ Linear Stack | $J(n, k) = (J(n-1, k) + k) \% n$ | Modular index shift |
| **Recursive String Reversal**| $\mathbf{O(N^2)}$ (String concat)| $\mathbf{O(N)}$ Linear Stack | Substring allocation | Char appending |

---

## 10. Edge Cases & Boundary Handling

1. **Tower of Hanoi with $N = 0$**:
   - Handled by base case guard, returning empty move list immediately.

2. **Josephus with $K = 1$**:
   - When $k = 1$, every person is eliminated in sequential order $0, 1, 2 \dots n-2$.
   - The last remaining survivor is ALWAYS the last person: index $n - 1$.

3. **String Reversal with Null / Empty Input**:
   - `str == null || str.length() <= 1` returns input directly, avoiding `NullPointerException`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Swapping Source and Destination Rods in Hanoi Step 1 vs Step 3**:
  - In Hanoi, Step 1 moves $N-1$ disks from `src` to `aux` using `dest`. Step 3 moves $N-1$ disks from `aux` to `dest` using `src`. Swapping parameter roles causes illegal larger-on-smaller disk placement!

* **Anti-Pattern 2: Forgetting Modular Arithmetic in Josephus**:
  - Forgetting `% n` in `(josephus(n-1, k) + k) % n` causes out-of-bounds index calculation as circle count shrinks.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Understanding 0-Based vs. 1-Based Josephus Indexing:
> The standard recursive Josephus formula $J(n, k) = (J(n-1, k) + k) \bmod n$ produces a **0-Based Index** result ($0 \dots n-1$).
> If the interviewer asks for a **1-Based Index** survivor ($1 \dots n$), simply add $+1$ to the final result: $J_1(n, k) = J(n, k) + 1$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Tower of Hanoi (Recursive) | Josephus (Recursive) | Josephus (Iterative Loop) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(2^N)$ Exponential | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Memory** | $O(N)$ Stack Memory | $O(N)$ Stack Memory | **$O(1)$ Zero Stack ⚡** |
| **Implementation** | Extremely Natural | 3 Lines Code | 4 Lines Loop |

---

## 14. How to Recognize This in Questions

* **"Move items between 3 pegs following size restriction rules"** $\rightarrow$ Tower of Hanoi.
* **"Eliminate every K-th element in a circular ring"** $\rightarrow$ Josephus Problem.

---

## 15. Frequently Asked Interview Questions

* **Q: How many total moves are required to solve Tower of Hanoi for 64 disks?**  
  *A:* $2^{64} - 1 \approx 1.84 \times 10^{19}$ moves (would take over 584 billion years at 1 move per second!).

* **Q: Can Josephus Problem be solved in $O(1)$ space?**  
  *A:* Yes! By converting the bottom-up recurrence into an iterative `for` loop starting from $i = 2 \dots n$:
  ```java
  int ans = 0;
  for (int i = 2; i <= n; i++) ans = (ans + k) % i;
  return ans; // O(1) space!
  ```

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: CLASSICAL RECURSION PROBLEMS I                        |
+-----------------------------------------------------------------------+
| • Tower of Hanoi : Move N-1 to Aux -> Move N to Dest -> Move N-1 to Dest|
| • Hanoi Moves    : T(N) = 2^N - 1 moves | Time O(2^N)                 |
| • Josephus (0-based): J(n, k) = (J(n - 1, k) + k) % n | Base J(1, k) = 0|
| • Josephus (1-based): J(n, k) + 1                                     |
| • Iterative Opt  : for (i = 2..n) ans = (ans + k) % i -> O(1) Space! ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the recursive Tower of Hanoi solution in Java.
- [ ] I can prove that Tower of Hanoi requires $2^N - 1$ total moves.
- [ ] I can write the 0-based Josephus recursive recurrence relation.
- [ ] I can convert 0-based Josephus result to 1-based index.
- [ ] I can convert the Josephus recursive recurrence into an $O(1)$ space iterative loop.
