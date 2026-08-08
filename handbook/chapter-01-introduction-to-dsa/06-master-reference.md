# 06. Master Reference — Introduction to DSA

## 1. Introduction
This Master Reference acts as a ultra-dense revision summary for **Chapter 1: Introduction to Data Structures & Algorithms**. It consolidates foundational principles, Big-O bounds, space rules, recursion facts, and mathematical formulas into a rapid-scanning interview cheat sheet.

> **Important:** Review this file 15 minutes prior to a technical coding interview to refresh fundamental bounds, memory models, and Java syntax patterns.

## 2. Core Concepts Cheat Sheet
* **Structure Selection Rules**:
  * $O(1)$ random index access $\rightarrow$ **Array / ArrayList**.
  * $O(1)$ head/tail modification without re-allocation $\rightarrow$ **LinkedList / Deque**.
  * $O(1)$ key lookup & frequency counts $\rightarrow$ **HashMap / HashSet**.
  * $O(\log N)$ dynamic ordering / top elements $\rightarrow$ **PriorityQueue (Heap)**.
* **Complexity Bounds Threshold**:
  * 1 Second JVM Execution Limit $\approx 10^8$ operations.
  * $N \le 10^5 \implies O(N)$ or $O(N \log N)$ algorithm required.

> **Memory Trick:** **"Know your N to pick your O"**. Always check problem input size $N$ before picking your data structure.

## 3. Asymptotic Notation Summary
```
+-------------------------------------------------------------------------+
| Notation     | Name        | Meaning                   | Bound Type     |
+-------------------------------------------------------------------------+
| Big-O (O)    | Upper Bound | Worst-case growth limit   | Maximum work   |
| Big-Omega (Ω)| Lower Bound | Best-case growth limit    | Minimum work   |
| Big-Theta (Θ)| Tight Bound | Exact growth rate match   | Average work   |
+-------------------------------------------------------------------------+
```

## 4. Hardware & Memory Layout Mechanics
* **Spatial Cache Locality**: Arrays store elements sequentially, enabling CPU L1/L2 cache pre-fetching.
* **Pointer Overhead**: Reference-based structures (LinkedList, Binary Tree) incur 8-16 bytes object header overhead per node, causing frequent CPU cache misses.

```
Array (Cache Friendly):     [ Val 1 ][ Val 2 ][ Val 3 ][ Val 4 ]  <-- Sequential CPU Cache Line
LinkedList (Cache Misses):  ( Node 1 ) ---> [ Ram Jump ] ---> ( Node 2 )
```

## 5. Master Complexity Table
| Data Structure / Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Array Access** | $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ |
| **Array Search (Unsorted)**| $O(1)$ | $O(N)$ | $O(N)$ | $O(1)$ |
| **Binary Search (Sorted)** | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ iterative |
| **ArrayList Insert (End)** | $O(1)$ | $O(1)$ amortized | $O(N)$ reallocation | $O(N)$ backing array |
| **LinkedList Insert (Head)**| $O(1)$ | $O(1)$ | $O(1)$ | $O(1)$ node creation |
| **Recursion Call Stack**   | $O(1)$ | $O(H)$ stack depth | $O(N)$ stack depth | $O(H)$ JVM frames |
| **Euclidean GCD**          | $O(1)$ | $O(\log(\min(A, B)))$ | $O(\log(\min(A, B)))$ | $O(1)$ iterative |
| **Binary Exponentiation**   | $O(1)$ | $O(\log B)$ | $O(\log B)$ | $O(1)$ iterative |

## 6. Java Syntax Reminders & Snippets

> **Quick Syntax:**
```java
// 1. Array Allocation & Safe Bound Check
int[] arr = new int[N];
if (index >= 0 && index < arr.length) {
    int val = arr[index];
}

// 2. Safe Midpoint Calculation (Prevents Integer Overflow)
int mid = left + (right - left) / 2;

// 3. Positive Modular Indexing in Java
int safeIndex = (index % N + N) % N;

// 4. Safe LCM Formula
long lcm = (a / gcd(a, b)) * b;

// 5. Fast Bitwise Odd/Even Test
boolean isEven = (val & 1) == 0;
```

## 7. Mandatory Edge Case Audit
* **Empty / Null Input**: Always handle `if (arr == null || arr.length == 0)`.
* **Single Element Input**: Handle `N = 1` boundary conditions.
* **Large Integer Operations**: Cast intermediate products to `long` before applying `% MOD` to avoid 32-bit integer wrapping.
* **Recursion Stack Overflow**: Ensure base case is explicitly defined at line 1 of the function body.

## 8. Common Interview Traps
* **Trap 1**: Claiming string concatenation inside a loop is $O(N)$ time. (In Java, `String` is immutable; `s += char` in a loop takes $O(N^2)$ time. Use `StringBuilder` for $O(N)$).
* **Trap 2**: Forgetting space occupied by recursion stack frames.
* **Trap 3**: Simplification of multiple input variables ($O(N + M)$ reduced incorrectly to $O(N)$).

## 9. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 1                               |
+-----------------------------------------------------------------------+
| 1. Input Constraints Guide: N <= 10^5 -> O(N log N) or O(N)          |
| 2. Overflow-Free Midpoint: mid = left + (right - left) / 2            |
| 3. Positive Modulo: (x % M + M) % M                                   |
| 4. Safe LCM: (a / gcd(a,b)) * b                                       |
| 5. Recursion Space = Max Stack Depth (H)                             |
+-----------------------------------------------------------------------+
```

## 10. Final Practice Checklist
- [ ] I can articulate the difference between Time Complexity and Execution Time.
- [ ] I can pick the correct data structure based on input size $N$ and operation queries.
- [ ] I know how to write overflow-safe midpoint calculations in Java.
- [ ] I can write Euclidean GCD in one line using the ternary operator.
- [ ] I have memorized the modular addition, subtraction, and multiplication formulas.
