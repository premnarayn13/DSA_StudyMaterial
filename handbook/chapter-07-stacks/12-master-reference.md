# 12. Master Reference — Stacks

## 1. Introduction
This Master Reference consolidates all core principles, LIFO protocols, Monotonic Stack formulas, expression evaluation algorithms, and Java syntax templates for **Chapter 7: Stacks**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Monotonic Stack loop conditions, histogram width formulas, expression operand pop order, and `ArrayDeque` idiomatic setups.

## 2. Core Concepts & Formulas Cheat Sheet
* **Modern Java Stack Setup**: `Deque<Integer> stack = new ArrayDeque<>();`
* **Guarded Pop Pattern**: `if (!stack.isEmpty()) { int val = stack.pop(); }`
* **Histogram Width Formula**: `int width = stack.isEmpty() ? i : (i - stack.peek() - 1);`
* **Monotonic Stack Index Push**: `stack.push(i);` (Store INDICES, not values!).
* **Monotonic Decreasing Pop (Next Greater)**: `while (!stack.isEmpty() && arr[i] > arr[stack.peek()])`
* **Monotonic Increasing Pop (Histogram)**: `while (!stack.isEmpty() && currentHeight < heights[stack.peek()])`
* **Postfix Subtraction/Division Pop Order**: `int b = stack.pop(); int a = stack.pop(); stack.push(a - b);`
* **Longest Valid Parentheses Base Index**: `stack.push(-1);` (Valid length $= i - \text{stack.peek()}$).
* **Dual-Stack Queue Transfer Condition**: `if (outStack.isEmpty()) while(!inStack.isEmpty()) outStack.push(inStack.pop());`
* **Bottom-to-Top Iteration**: `Iterator<String> it = stack.descendingIterator();`

> **Memory Trick:** **"Pop b FIRST (right), pop a SECOND (left)! Compute (a - b) or (a / b)"**.

## 3. Master Stack Algorithm Complexity Table
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Triggers / Use Case |
| :--- | :--- | :--- | :--- |
| **`stack.push()` / `pop()` / `peek()`**| **$O(1)$ Constant** | $O(1)$ Constant | Core LIFO primitives |
| **Valid Parentheses (20)** | **$O(N)$ Linear** | $O(N)$ Stack | Push expected closing bracket |
| **Min Stack (155)** | **$O(1)$ all ops**| $O(N)$ Space | Dual stack (`val <= minStack.peek()`) |
| **Evaluate RPN (150)** | **$O(N)$ Linear** | $O(N)$ Stack | Postfix operand stack |
| **Basic Calculator II (227)** | **$O(N)$ Linear** | $O(N)$ Stack | Evaluate `*` and `/` immediately |
| **Daily Temperatures (739)**| **$O(N)$ Amortized**| $O(N)$ Index Stack| Monotonic Decreasing Stack |
| **Histogram Max Area (84)** | **$O(N)$ Amortized**| $O(N)$ Index Stack| Monotonic Increasing + Dummy 0 |
| **Trapping Rain Water (42)** | **$O(N)$ Amortized**| $O(N)$ Index Stack| Monotonic Decreasing Stack |
| **Maximal 2D Matrix (85)** | **$O(R \cdot C)$** | $O(C)$ Column Array| Row Histogram DP + Stack |
| **Min Add Parentheses (921)** | **$O(N)$ Linear** | **$O(1)$ Space ⚡**| 2 Counters (`open` & `needed`) |
| **Longest Valid Parentheses (32)**| **$O(N)$ Linear** | $O(N)$ Stack | Pre-push base index `-1` |
| **Sort Stack (Aux Stack)** | $O(N^2)$ Quadratic| $O(N)$ Temp Stack | `while (tmpStack.peek() > curr)` |
| **Reverse Stack (Recursive)**| $O(N^2)$ Quadratic| $O(N)$ Call Stack | `reverse()` + `insertAtBottom()` |
| **Queue using 2 Stacks (232)**| **Amortized $O(1)$**| $O(N)$ Dual Stacks| Lazy transfer `outStack.isEmpty()` |
| **Decode String (394)** | **$O(N \cdot \text{maxK})$** | $O(N)$ Dual Stacks| `countStack` + `stringStack` |
| **Simplify Path (71)** | **$O(N)$ Linear** | $O(N)$ Stack | `stack.descendingIterator()` |

## 4. Hardware & Memory Footprint Summary
```
+-----------------------------------------------------------------------------------+
| Stack Element / Runtime      | Memory Footprint & Details                         |
+-----------------------------------------------------------------------------------+
| JVM Thread Stack (-Xss)      | Default ~1MB per Thread (Stores method call frames)|
| Stack Frame Structure        | Local Variable Array + Operand Stack + Frame Data  |
| StackOverflowError Trigger   | Recursion depth > ~10,000 frames                   |
| ArrayDeque Stack (Heap)      | Resizable array buffer on Heap (Scales to GBs ⚡)  |
+-----------------------------------------------------------------------------------+
```

## 5. Java Code Templates & Snippets

> **Quick Syntax:**
```java
// 1. ArrayDeque Setup
Deque<Integer> stack = new ArrayDeque<>();

// 2. Monotonic Stack Loop
while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {
    int poppedIdx = stack.pop();
    result[poppedIdx] = i - poppedIdx;
}
stack.push(i);

// 3. Histogram Width Formula
int width = stack.isEmpty() ? i : (i - stack.peek() - 1);

// 4. Decode String Reset on '['
countStack.push(k);
stringStack.push(currString);
currString = new StringBuilder();
k = 0;
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: Empty Stack Exceptions**: Always guard `pop()` and `peek()` with `!stack.isEmpty()`.
* **Trap 2: Subtraction/Division Operand Order**: First pop is $B$, second pop is $A$. Compute `a - b` or `a / b`.
* **Trap 3: Histogram Width Under-Counting**: Use `(i - stack.peek() - 1)` (not `i - stack.peek()`).
* **Trap 4: Min Stack Duplicate Dropping**: Use `val <= minStack.peek()` with `<=` equality.
* **Trap 5: Queue Transfer Frequency**: Transfer `inStack` to `outStack` ONLY when `outStack.isEmpty()` is true.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 7 (STACKS)                        |
+-----------------------------------------------------------------------+
| 1. Modern Java Stack: Deque<Integer> stack = new ArrayDeque<>();      |
| 2. Monotonic Index Stacking: Store INDICES i; access val via arr[peek]|
| 3. Histogram Width: width = stack.isEmpty() ? i : (i - stack.peek() - 1)|
| 4. Postfix Non-Commutative: b = pop(); a = pop(); compute (a - b)     |
| 5. Longest Valid Parentheses: Pre-push stack.push(-1); len = i - peek |
| 6. Min Add Parentheses: 2 counters (open/needed) for O(1) space       |
| 7. Queue via 2 Stacks: Lazy transfer ONLY when outStack.isEmpty()     |
| 8. Decode String: Push state on '[', reset k=0 & currString           |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write the Monotonic Stack Next Greater Element loop from memory.
- [ ] I can write the Histogram Max Area algorithm (LeetCode 84) using dummy sentinel 0.
- [ ] I can evaluate Reverse Polish Notation (LeetCode 150) without operand order bugs.
- [ ] I can implement Queue using 2 Stacks (LeetCode 232) in amortized $O(1)$ time.
- [ ] I can implement Decode String (LeetCode 394) using dual stacks.
