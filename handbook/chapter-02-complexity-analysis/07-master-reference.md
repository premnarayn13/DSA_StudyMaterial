# 07. Master Reference — Complexity Analysis

## 1. Introduction
This Master Reference acts as a rapid-scanning summary for **Chapter 2: Complexity Analysis**. It consolidates Big-O, Big-Omega, and Big-Theta definitions, operational case bounds, amortized proofs, and code structural patterns into a concentrated interview cheat sheet.

> **Important:** Review this master reference 15 minutes before an interview to lock in asymptotic formulas, hardware limits, and Java-specific complexity gotchas.

## 2. Asymptotic Notations Cheat Sheet
```
+-----------------------------------------------------------------------------------+
| Notation  | Formal Inequality            | Bound Type | Primary Interview Usage   |
+-----------------------------------------------------------------------------------+
| Big-O (O) | f(n) <= c * g(n)             | Upper      | Worst-case guarantee (SLA)|
| Big-Ω (Ω) | f(n) >= c * g(n)             | Lower      | Best-case / Theoretical   |
| Big-Θ (Θ) | c1*g(n) <= f(n) <= c2*g(n)   | Tight Fit  | Exact asymptotic match    |
+-----------------------------------------------------------------------------------+
```

## 3. Structural Code Pattern Formulas
* **Single Loop ($0 \dots N$, `i++`)**: $O(N)$
* **Loop Halving/Doubling (`i /= 2` or `i *= 2`)**: $O(\log N)$
* **Square Root Bound (`i * i <= N`)**: $O(\sqrt{N})$
* **Nested Dependent Loops (`j = i ... N`)**: $\frac{N(N-1)}{2} \rightarrow O(N^2)$
* **Two Pointer Converging Loop (`left < right`)**: $O(N)$ total step bound
* **Recursive Branching (Branching factor $B$, Depth $D$)**: $O(B^D)$

> **Memory Trick:** **"O(N) operations inside a loop of size N = O(N²); log N operations inside loop of size N = O(N log N)"**.

## 4. Master Algorithm Complexity Table
| Algorithm | Best Case ($\Omega$) | Average Case ($\Theta$) | Worst Case ($O$) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | $\Omega(1)$ | $\Theta(N)$ | $O(N)$ | $O(1)$ |
| **Binary Search** | $\Omega(1)$ | $\Theta(\log N)$ | $O(\log N)$ | $O(1)$ iterative |
| **Insertion Sort** | $\Omega(N)$ | $\Theta(N^2)$ | $O(N^2)$ | $O(1)$ |
| **Quick Sort (Naive)** | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N^2)$ | $O(N)$ call stack worst |
| **Merge Sort** | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(N)$ auxiliary array |
| **Heap Sort** | $\Omega(N \log N)$ | $\Theta(N \log N)$ | $O(N \log N)$ | $O(1)$ in-place |
| **HashMap Lookup** | $\Omega(1)$ | $\Theta(1)$ | $O(N)$ list / $O(\log N)$ tree | $O(N)$ space |
| **`ArrayList.add()`** | $\Omega(1)$ | $\Theta(1)$ amortized | $O(N)$ single resize | $O(N)$ backing array |

## 5. Java Hardware & JVM Specifics

> **Quick Syntax:**
```java
// 1. Safe Midpoint (Prevents Integer Overflow)
int mid = left + (right - left) / 2;

// 2. Fast Bitwise Even Check
boolean isEven = (val & 1) == 0;

// 3. Dynamic Array Expansion Formula in JDK 8+
int newCapacity = oldCapacity + (oldCapacity >> 1); // 1.5x growth
```

## 6. Common Interview Pitfalls & Traps
* **Hidden String Costs**: Calling `String.substring(i, j)` inside nested loops takes $O(K)$ time per call $\implies O(N^3)$ total time!
* **Calling `List.contains()` inside loop**: `contains()` is $O(N)$ search. Calling it inside a loop makes the overall algorithm $O(N^2)$.
* **Forgetting Recursion Stack Space**: A recursive algorithm with no local allocations still takes $O(H)$ auxiliary space where $H$ is the call stack depth.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 2                               |
+-----------------------------------------------------------------------+
| 1. 1 Second Constraint = 10^8 Operations                              |
| 2. Input Size N <= 10^5 -> Goal: O(N) or O(N log N)                   |
| 3. ArrayList Growth Factor = 1.5x -> Amortized O(1) Push              |
| 4. HashMap Bucket Treeification: >8 items converts List -> RB Tree   |
| 5. Two Pointers = O(N) Time, O(1) Space                               |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write the formal math definitions for $O$, $\Omega$, and $\Theta$.
- [ ] I know why naive Quick Sort degrades to $O(N^2)$ and how randomized pivots fix it.
- [ ] I can prove why `ArrayList.add()` has an Amortized $O(1)$ time complexity.
- [ ] I can identify hidden $O(N)$ library methods inside nested loops.
- [ ] I know how to select algorithms based on input size constraints ($N$).
