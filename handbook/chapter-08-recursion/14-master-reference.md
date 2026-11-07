# 14. Master Reference — Recursion Algorithms & Foundations

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, call stack bounds, operational complexities, design patterns, and interview pitfalls for **Chapter 21: Recursion**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Call Stack Architecture, Tail Recursion Accumulators, Systematic 4-Step Design, Tower of Hanoi ($2^N - 1$), Josephus Problem ($J(n, k)$), Gray Code Reflection ($k \oplus (k \gg 1)$), Flood Fill DFS, Choose-Recurse-Unchoose Backtracking, Recursion Tree Work Summations, Core Search/Sort Engines, Top-Down Memoization, Bitmasking, Defensive Edge-Case Guards, Expression Precedence Undo, and Trampoline Continuation Engines.

> **Important:** Review this master reference 15 minutes before an interview to refresh the 3 Pillars of Recursion (Base Case, Reduction, Combination), Descent vs Unwinding execution order, Accumulator Pattern (`factTail(n - 1, n * acc)`), Josephus 0-indexed formula `(J(n - 1, k) + k) % n`, Gray Code formula `k ^ (k >> 1)`, Backtracking Triad (`add -> recurse -> remove`), Mid Overflow Formula `low + (high - low) / 2`, and Expression Multiplication Undo `(eval - prev) + (prev * val)`!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **The 3 Pillars of Recursive Design**:
  - Base Case Guard + Subproblem Monotonic Reduction + Combination / Return Logic.
* **Call Stack Memory Bound**:
  - $M(D) = C \cdot D = \mathbf{O(D) \text{ Auxiliary Memory}}$, where $D$ is max stack depth.
* **Accumulator Transformation Equation**:
  - `factTail(n, acc) = factTail(n - 1, n * acc)` (Base case $n \le 1$ returns `acc`).
* **Tower of Hanoi Move Counter**:
  - $T(N) = 2^N - 1$ moves (Exponential $O(2^N)$ time).
* **Josephus Elimination 0-Based Formula**:
  - $J(n, k) = (J(n - 1, k) + k) \pmod n \quad \text{with } J(1, k) = 0$.
  - 1-Based Survivor Index: $J_1(n, k) = J(n, k) + 1$.
* **Gray Code Bitwise Formula**:
  - $G(k) = k \oplus (k \gg 1)$ (Constant $O(1)$ time for index $k$).
* **Recursion Tree Total Work Equation**:
  - $T(N) = \sum_{l=0}^{\log_b N} a^l \cdot f\left(\frac{N}{b^l}\right)$ ($a$ = branching factor, $b$ = shrink factor).
* **Overflow-Safe Midpoint Calculation**:
  - `mid = low + (high - low) / 2`.
* **Expression Add Operators Multiplication Undo Formula**:
  - `newEval = (eval - prevOperand) + (prevOperand * val); newPrev = prevOperand * val;`

```
Recursion Master Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Search Paradigm   | Key Data Structure| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **State Expansion**   | Combinatorial Tree| `(index, path)`   | **$O(2^N)$ / $O(N!)$ ⚡**|
| **Window Shrink**     | Two-Pointer Inward| `(left, right)`   | **$O(N)$ Linear ⚡**|
| **Divide Halving**    | Interval Split    | `(low, high)`     | **$O(\log N)$ Log ⚡**|
| **Grid DFS Masking**  | 2D Connected Fill | In-place Mask `0` | **$O(M \cdot N)$ Linear ⚡**|
| **Top-Down Memo DP**  | Subproblem Cache  | `memo[index][tgt]`| **$O(N \cdot K)$ Poly ⚡**|
| **Trampoline Engine** | Continuation Loop | Supplier Object   | **$O(1)$ Stack Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Recursive Algorithm / Pattern | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Stack Space | Key Mechanism / Driver |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Recursion (Factorial)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| $O(N)$ Stack Memory | 1 self-call per frame |
| **Tail Recursion (Java)**     | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| $O(N)$ Stack (No TCO)| Accumulator parameter |
| **Tail Recursion (Iterative)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Zero Stack ⚡**| `while` loop conversion |
| **Tower of Hanoi**            | **$O(2^N)$ Exp**   | **$O(2^N)$ Exp**   | **$O(2^N)$ Exp**   | $O(N)$ Stack Memory | $2^N - 1$ moves |
| **Josephus Problem**          | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| $O(N)$ Stack Memory | $(J(n-1, k) + k) \% n$ |
| **Gray Code (Reflection)**    | **$O(2^N)$ Exp**   | **$O(2^N)$ Exp**   | **$O(2^N)$ Exp**   | $O(2^N)$ Output Array | Reverse + bit shift `1<<n` |
| **Gray Code (Bitwise)**       | **$O(1)$ Const ⚡**| **$O(1)$ Const ⚡**| **$O(1)$ Const ⚡**| **$O(1)$ Constant ⚡**| `k ^ (k >> 1)` |
| **Flood Fill 2D DFS**         | **$O(M \cdot N)$** | **$O(M \cdot N)$** | **$O(M \cdot N)$** | $O(M \cdot N)$ Stack | In-place color overwrite |
| **Permutations (Backtracking)**| **$O(N! \cdot N)$**| **$O(N! \cdot N)$**| **$O(N! \cdot N)$**| $O(N)$ Path Memory | Choose-Recurse-Unchoose |
| **Recursive Binary Search**   | **$O(1)$ Const ⚡**| **$O(\log N)$ Log**| **$O(\log N)$ Log**| $O(\log N)$ Stack | Interval halving `mid` |
| **Recursive Merge Sort**       | **$O(N \log N)$**  | **$O(N \log N)$**  | **$O(N \log N)$ ⚡**| $O(N)$ Aux Array | Stable Divide & Conquer |
| **Recursive Quick Sort**       | **$O(N \log N)$**  | **$O(N \log N)$**  | $O(N^2)$ (Sorted)  | $O(\log N)$ Stack ⚡| In-place Lomuto partition|
| **Top-Down Memoized DP**      | **$O(N \cdot K)$** | **$O(N \cdot K)$** | **$O(N \cdot K)$ ⚡**| $O(N \cdot K)$ Table | Lookup cache `memo[i][j]` |
| **Expression Add Operators**   | **$O(4^N)$ Exp**   | **$O(4^N)$ Exp**   | **$O(4^N)$ Exp**   | $O(N)$ Stack Memory | `(eval - prev) + (prev * val)`|
| **Trampoline Continuation**   | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Constant ⚡**| Iterative Supplier Loop |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Call Stack Memory Breakdown for Recursive Systems                                |
+-----------------------------------------------------------------------------------+
| JVM Thread Stack Frame Allocation              : ~48 to 128 Bytes per Frame       |
| Default Thread Stack Memory (-Xss)             : 1 MB (Limits depth to ~10,000)   |
| Primary Stack Overflow Guard                   : Explicit depth check (depth > 5000)|
| Primary Heap Memory Optimization               : Shared Path List + Choose/Unchoose|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Tail Recursion Accumulator Line
public long tail(int n, long acc) { if (n <= 1) return acc; return tail(n - 1, n * acc); }

// 2. Josephus 0-Based Recurrence Line
public int josephus(int n, int k) { if (n == 1) return 0; return (josephus(n - 1, k) + k) % n; }

// 3. Gray Code Constant Formula Line
public int grayCodeBitwise(int k) { return k ^ (k >> 1); }

// 4. Backtracking Choose-Recurse-Unchoose Triad
path.add(candidate); backtrack(nextState, path); path.remove(path.size() - 1);

// 5. Overflow-Safe Midpoint Calculation
int mid = low + (high - low) / 2;

// 6. Matrix Bounds Order Invariant Guard
if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == 0) return;

// 7. Expression Add Operators Multiplication Undo Line
long newEval = (eval - prevOperand) + (prevOperand * val);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Forgetting `new ArrayList<>(path)` Deep Copy in Backtracking**: Storing `result.add(path)` adds mutable references that become empty `[]` when unwinding. Always store deep copies `new ArrayList<>(path)`.
* **Pitfall 2: Forgetting `path.remove(path.size() - 1)` Cleanup**: Omitting the unchoose step pollutes state across sibling decision branches.
* **Pitfall 3: Assuming Java JVM Performs Tail Call Optimization (TCO)**: JVM does NOT automatically optimize tail recursion. Manually convert to `while` loops for deep scale.
* **Pitfall 4: Integer Overflow in Mid Calculation**: Writing `(low + high) / 2` overflows signed 32-bit `int`. Always use `low + (high - low) / 2`.
* **Pitfall 5: Reversing Matrix Boundary Guard Order**: Accessing `grid[r][c]` before checking bounds throws `ArrayIndexOutOfBoundsException`. Bounds MUST be checked first.
* **Pitfall 6: Negating `Integer.MIN_VALUE`**: `-Integer.MIN_VALUE` remains negative in 32-bit math. Cast to `long` before negating.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 21 (RECURSION)                   |
+-----------------------------------------------------------------------+
| 1. Pillars     : Base Guard + Monotonic Reduction + Result Combination |
| 2. Execution   : Descent (Before Call) vs Unwinding (After Call)      |
| 3. Josephus    : J(n, k) = (J(n - 1, k) + k) % n | Base J(1, k) = 0    |
| 4. Gray Code   : G(k) = k ^ (k >> 1) in O(1) time                     |
| 5. Backtrack   : CHOOSE -> RECURSE -> UNCHOOSE (deep copy snapshot!)   |
| 6. Mid Formula : mid = low + (high - low) / 2 (Overflow Safe)         |
| 7. Mult Undo   : (eval - prev) + (prev * val)                         |
| 8. Trampoline  : Converts stack frames into O(1) iterative supplier loop|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can implement the 3 pillars of recursive function design.
- [ ] I can trace JVM call stack descent and unwinding phases.
- [ ] I can convert non-tail recursion to tail recursion using accumulators.
- [ ] I can solve Tower of Hanoi ($2^N - 1$ moves) and Josephus Problem ($J(n, k)$).
- [ ] I can generate Gray Code via recursive reflection and bitwise formula `k ^ (k >> 1)`.
- [ ] I can write 2D Grid Flood Fill DFS with in-place cell masking.
- [ ] I can write the Choose-Recurse-Unchoose Triad in Java.
- [ ] I can analyze recursion trees to calculate work-per-level summations.
- [ ] I can write overflow-safe Binary Search, Merge Sort, and Quick Sort.
- [ ] I can optimize exponential recursion using Top-Down Memoization and Bitmasking.
- [ ] I can write public defensive entry wrappers handling null, empty, and boundary edge cases.
- [ ] I can evaluate mathematical expressions with multiplication precedence undo.
- [ ] I can write an $O(1)$ stack-safe Trampoline continuation engine.
