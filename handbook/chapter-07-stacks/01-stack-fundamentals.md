# 01. Stack Fundamentals & LIFO Protocol

## 1. Introduction
A **Stack** is a linear data structure that strictly enforces the **LIFO (Last-In, First-Out)** access protocol. Elements are added (pushed) and removed (popped) exclusively from a single end, known as the **Top of the Stack**. In technical coding interviews, Stacks serve as the core data structure for runtime call stacks, expression evaluation, back-tracking, depth-first search (DFS), and Monotonic Stack algorithms.

> **Important:** In Java, legacy `java.util.Stack` inherits from `Vector` and synchronizes all operations. In interviews and production, **`java.util.ArrayDeque`** MUST be used as the standard LIFO Stack implementation!

## 2. Core Concepts
* **LIFO Access Protocol**: The item inserted most recently is the first item removed.
* **Core Primitive Operations**:
  * **`push(element)`**: Insert element onto top of stack ($O(1)$ time).
  * **`pop()`**: Remove and return element from top of stack ($O(1)$ time).
  * **`peek()`**: Read top element without removing it ($O(1)$ time).
  * **`isEmpty()`**: Check if stack contains zero elements ($O(1)$ time).
* **Call Stack / Recursion Analogy**: Function calls in programming languages are stored in JVM runtime Call Stack frames following exact LIFO order.

> **Memory Trick:** **"Last-In, First-Out! Always use ArrayDeque<Integer> stack = new ArrayDeque<>()"**.

## 3. Characteristics / Properties
* **Restricted Access**: Direct access to middle or bottom elements is strictly forbidden. Only the top element can be inspected or modified.
* **ArrayDeque vs Legacy Stack**:
  * `java.util.Stack`: Synchronized (Lock overhead), extends `Vector`, slower performance.
  * `java.util.ArrayDeque`: Unsynchronized, dynamic resizable array buffer, maximum cache locality, **100% thread-safe within single-threaded execution**.

```
Stack Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Stack Operation       | Time Complexity   | Auxiliary Space   | Interface Method  |
+-----------------------+-------------------+-------------------+-------------------+
| `push(val)`           | Amortized O(1) ⚡ | O(1) Constant     | `stack.push(val)` |
| `pop()`               | O(1) Constant ⚡  | O(1) Constant     | `stack.pop()`     |
| `peek()`              | O(1) Constant ⚡  | O(1) Constant     | `stack.peek()`    |
| `isEmpty()`           | O(1) Constant ⚡  | O(1) Constant     | `stack.isEmpty()` |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing `ArrayDeque` LIFO Operations:

```
State 1: Push 10 -> Stack: [ 10 ] (Top = 10)
State 2: Push 20 -> Stack: [ 10, 20 ] (Top = 20)
State 3: Push 30 -> Stack: [ 10, 20, 30 ] (Top = 30)

State 4: Peek()  -> Returns 30 (Stack remains [ 10, 20, 30 ])
State 5: Pop()   -> Returns 30 (Stack becomes [ 10, 20 ], Top = 20)
State 6: Pop()   -> Returns 20 (Stack becomes [ 10 ], Top = 10)
```

## 5. Visual Diagram
LIFO Stack Push and Pop Architecture:

```
       POP  ^   | PUSH
            |   v
        +-----------+
        |  Element3 |  <--- TOP (Most Recently Pushed)
        +-----------+
        |  Element2 |
        +-----------+
        |  Element1 |  <--- BOTTOM (First Pushed, Last Out)
        +-----------+
```

## 6. Operations / Algorithms
Standard Java Stack Declaration Idiom:

```java
// Standard Modern Java Stack Setup
Deque<Integer> stack = new ArrayDeque<>();

// Push
stack.push(10);
stack.push(20);

// Inspect Top
int top = stack.peek(); // 20

// Remove Top
int popped = stack.pop(); // 20

// Guarded Pop Pattern
if (!stack.isEmpty()) {
    int val = stack.pop();
}
```

> **Quick Syntax:**
```java
// Always check isEmpty() before pop() or peek()!
if (!stack.isEmpty()) {
    int topVal = stack.peek();
}
```

## 7. Examples
* **LeetCode 20 - Valid Parentheses**: Bracket matching using Stack.
* **LeetCode 155 - Min Stack**: Constant-time minimum tracking.
* **LeetCode 71 - Simplify Path**: POSIX directory path normalization.

## 8. Java Code
Complete interview-ready Java suite implementing Valid Parentheses (LeetCode 20) using `ArrayDeque`:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class StackFundamentalsMaster {

    // LeetCode 20: Valid Parentheses O(N) Time, O(N) Space
    public static boolean isValidParentheses(String s) {
        if (s == null || s.length() % 2 != 0) return false;

        Deque<Character> stack = new ArrayDeque<>();

        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else {
                // If closing bracket encountered, verify against top of stack
                if (stack.isEmpty() || stack.pop() != c) {
                    return false;
                }
            }
        }

        return stack.isEmpty(); // Must be empty for valid matching
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        System.out.println("Is '()' Valid? " + isValidParentheses("()"));       // true
        System.out.println("Is '()[]{}' Valid? " + isValidParentheses("()[]{}")); // true
        System.out.println("Is '(]' Valid? " + isValidParentheses("(]"));       // false
        System.out.println("Is '([)]' Valid? " + isValidParentheses("([)]"));   // false
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **`push()`** | **Amortized $O(1)$**| $O(1)$ | Dynamic array buffer resize ($2\times$) |
| **`pop()`** | **$O(1)$ Constant** | $O(1)$ | Array head/tail pointer decrement |
| **`peek()`** | **$O(1)$ Constant** | $O(1)$ | Direct element lookup |
| **`isEmpty()`** | **$O(1)$ Constant** | $O(1)$ | Size comparison |

## 10. Edge Cases
* **Empty Stack Exception**: Calling `stack.pop()` or `stack.peek()` on an empty `ArrayDeque` throws `NoSuchElementException`. Guard with `!stack.isEmpty()`.
* **Odd Length Parentheses String**: `s.length() % 2 != 0` CANNOT contain matching pairs; return `false` in $O(1)$ time.
* **Unmatched Opening Brackets**: String like `"((("` ends with non-empty stack (`!stack.isEmpty()`), evaluating to `false`.

## 11. Common Mistakes
* Using `java.util.Stack` instead of `java.util.ArrayDeque` in interview code.
* Calling `stack.pop()` without checking `!stack.isEmpty()`.
* Pushing open brackets onto stack and matching with `if (c == ')' && stack.peek() == '(')` (creates verbose, error-prone code!). Pushing the **expected closing bracket** `stack.push(')')` makes matching code ultra-clean!

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Bracket Matching Trick:
> When reading an opening bracket (`'('`), push its **expected closing bracket** (`')'`) onto the stack!
> When encountering a closing bracket, simply check: **`if (stack.isEmpty() || stack.pop() != c) return false;`**
> This reduces bracket matching logic from 15 lines down to 4 lines!

> **Memory Trick:** **"Push expected CLOSING bracket onto stack for clean matching!"**

## 13. Comparisons
| Feature | `java.util.Stack` (Legacy) | `java.util.ArrayDeque` (Modern) |
| :--- | :--- | :--- |
| **Inheritance** | Extends `Vector` | Implements `Deque` |
| **Synchronization**| Synchronized (Slow) | **Unsynchronized (Fast⚡)** |
| **Null Elements** | Allowed | Forbidden (`null` throws NPE) |
| **Interview Recommendation** | AVOID | **MANDATORY PREFERRED** |

## 14. How to Recognize This in Questions
* **"Validate matching parentheses / brackets"** $\rightarrow$ Stack expected closing bracket trick.
* **"Evaluate reverse polish notation / infix expression"** $\rightarrow$ LIFO Stack parsing.

## 15. Frequently Asked Interview Questions
* **Q: Why is `ArrayDeque` preferred over `Stack` in Java?**  
  *A:* `java.util.Stack` extends `Vector` and synchronizes all methods, incurring locking overhead. `ArrayDeque` is unsynchronized, faster, and provides a clean LIFO Stack interface via `push()`, `pop()`, and `peek()`.
* **Q: How does `ArrayDeque` handle dynamic array resizes?**  
  *A:* `ArrayDeque` uses a circular array buffer. When the buffer fills to capacity, it doubles its array capacity ($2\times$), yielding **Amortized $O(1)$ push time**.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK FUNDAMENTALS & LIFO PROTOCOL                   |
+-----------------------------------------------------------------------+
| • LIFO Protocol: Last-In, First-Out                                   |
| • Standard Java Stack: Deque<Integer> stack = new ArrayDeque<>();      |
| • Always guard pop/peek: if (!stack.isEmpty()) { val = stack.pop(); } |
| • Bracket Trick: Push expected closing bracket (if c=='(' push ')')   |
| • Match Check: if (stack.isEmpty() || stack.pop() != c) return false; |
| • Complexity: All core ops push/pop/peek run in O(1) Constant Time    |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `ArrayDeque` is preferred over legacy `java.util.Stack`.
- [ ] I can write the expected closing bracket push trick for Valid Parentheses.
- [ ] I always guard `stack.pop()` with `!stack.isEmpty()`.
- [ ] I know why odd-length bracket strings can be rejected in $O(1)$ time.
- [ ] I can implement Valid Parentheses (LeetCode 20) in under 3 minutes.
