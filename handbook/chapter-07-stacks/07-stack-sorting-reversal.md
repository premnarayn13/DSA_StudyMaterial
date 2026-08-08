# 07. Stack Sorting & Recursion-Based Stack Reversal

## 1. Introduction
Sorting a stack and reversing a stack using only stack operations or recursion are fundamental data structure manipulation problems in technical coding interviews. These problems evaluate a candidate's mastery of implicit JVM recursion call stacks, auxiliary stack buffer usage, and call frame unwinding without allocating arrays or auxiliary lists.

> **Important:** Reversing a stack **without using any extra memory structures (in-place using recursion)** relies on two recursive algorithms: `reverse(stack)` and `insertAtBottom(stack, item)`. The JVM Call Stack implicitly acts as the temporary storage buffer!

## 2. Core Concepts
* **Sorting a Stack Using an Auxiliary Stack ($O(N^2)$ Time, $O(N)$ Space)**:
  * Maintain input `stack` and auxiliary `tmpStack`.
  * While `stack` is non-empty: pop `curr = stack.pop()`.
  * While `tmpStack` is non-empty AND `tmpStack.peek() > curr`: pop from `tmpStack` back into `stack`.
  * Push `curr` onto `tmpStack`.
  * When done, `tmpStack` holds elements in sorted order!
* **In-Place Stack Reversal via Recursion ($O(N^2)$ Time, $O(N)$ Call Stack Space)**:
  * **`reverse(stack)`**: If stack is non-empty, pop top item `temp = stack.pop()`, recursively call `reverse(stack)`, and then call `insertAtBottom(stack, temp)`.
  * **`insertAtBottom(stack, item)`**: If stack is empty, push `item`. Else pop `top = stack.pop()`, recursively call `insertAtBottom(stack, item)`, then push `top` back!

> **Memory Trick:** **"Sort Stack: While tmpStack.peek() > curr, pop back to main stack! Reverse Stack: Recursively pop to bottom!"**

## 3. Characteristics / Properties
* **Strict Interface Constraint**: All operations must strictly adhere to standard stack primitives (`push`, `pop`, `peek`, `isEmpty`). Direct index access is forbidden.
* **Implicit Storage**: Recursion-based stack algorithms replace explicit data structures with the JVM Call Stack frame hierarchy.

```
Stack Sorting & Reversal Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Algorithm   | Auxiliary Space   | Time Complexity   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| Sort Stack (Aux Stack)| O(N) Temp Stack   | O(N²) Quadratic   | Two-stack insertion|
| Reverse Stack (Recur) | O(N) Call Stack   | O(N²) Quadratic   | Recursion Bottom  |
| Sort Stack (Recursive)| O(N) Call Stack   | O(N²) Quadratic   | Recursion Insert  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Stack Sorting on `Input Stack: [34, 3, 31, 98, 92]` (Top is 92):

```
Init: tmpStack = []

Iter 1: curr = 92 -> tmpStack.push(92) | tmpStack: [92]
Iter 2: curr = 98 -> 98 > 92 -> tmpStack.push(98) | tmpStack: [92, 98]
Iter 3: curr = 31 -> 31 < 98 & 31 < 92 -> Pop 98 & 92 back to main stack!
        tmpStack.push(31). Push 92, 98 back to tmpStack | tmpStack: [31, 92, 98]
...
Final tmpStack: [3, 31, 34, 92, 98] (Top is 98) ✅
```

## 5. Visual Diagram
`insertAtBottom(stack, item)` Call Stack Mechanics:

```
Goal: Insert 99 at bottom of Stack [ 1, 2, 3 ]

Call 1: Pop 3 -> Call insertAtBottom([1, 2], 99)
Call 2: Pop 2 -> Call insertAtBottom([1], 99)
Call 3: Pop 1 -> Call insertAtBottom([], 99)
Call 4: Stack is empty! Push 99. Stack: [ 99 ]

Unwind Call 3: Push 1 back. Stack: [ 99, 1 ]
Unwind Call 2: Push 2 back. Stack: [ 99, 1, 2 ]
Unwind Call 1: Push 3 back. Stack: [ 99, 1, 2, 3 ]  (99 inserted at bottom!) ✅
```

## 6. Operations / Algorithms
Stack Sorting & Recursive Reversal Master Implementation:

```java
// 1. Sort Stack Using Auxiliary Stack O(N^2) Time, O(N) Space
public static Deque<Integer> sortStack(Deque<Integer> stack) {
    Deque<Integer> tmpStack = new ArrayDeque<>();

    while (!stack.isEmpty()) {
        int curr = stack.pop();

        // Move elements from tmpStack back to stack while they are > curr
        while (!tmpStack.isEmpty() && tmpStack.peek() > curr) {
            stack.push(tmpStack.pop());
        }

        tmpStack.push(curr);
    }

    return tmpStack; // Sorted with smallest at bottom, largest at top
}

// 2. Reverse Stack In-Place Using Recursion O(N^2) Time, O(N) Call Stack
public static void reverseStack(Deque<Integer> stack) {
    if (stack.isEmpty()) return;

    int temp = stack.pop();
    reverseStack(stack);
    insertAtBottom(stack, temp);
}

// Helper: Insert Item at Bottom of Stack Recursively
private static void insertAtBottom(Deque<Integer> stack, int item) {
    if (stack.isEmpty()) {
        stack.push(item);
        return;
    }

    int top = stack.pop();
    insertAtBottom(stack, item);
    stack.push(top);
}
```

> **Quick Syntax:**
```java
// Sort Stack Inner Loop Condition
while (!tmpStack.isEmpty() && tmpStack.peek() > curr) {
    stack.push(tmpStack.pop());
}
tmpStack.push(curr);
```

## 7. Examples
* **Sort a Stack**: Auxiliary stack sorting or fully recursive sorting.
* **Reverse a Stack using Recursion**: In-place reversal via `reverse` and `insertAtBottom`.
* **Sort a Stack using Recursion**: In-place recursive sorting without auxiliary data structures.

## 8. Java Code
Complete interview-ready Java suite implementing Stack Sorting and In-Place Recursive Reversal:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class StackSortingReversalMaster {

    // 1. Sort Stack using Auxiliary Stack O(N^2) Time, O(N) Space
    public static Deque<Integer> sortStack(Deque<Integer> input) {
        Deque<Integer> tmpStack = new ArrayDeque<>();

        while (!input.isEmpty()) {
            int curr = input.pop();
            while (!tmpStack.isEmpty() && tmpStack.peek() > curr) {
                input.push(tmpStack.pop());
            }
            tmpStack.push(curr);
        }

        return tmpStack;
    }

    // 2. Reverse Stack In-Place via Recursion O(N^2) Time, O(N) Call Stack
    public static void reverseStack(Deque<Integer> stack) {
        if (stack.isEmpty()) return;

        int temp = stack.pop();
        reverseStack(stack);
        insertAtBottom(stack, temp);
    }

    private static void insertAtBottom(Deque<Integer> stack, int item) {
        if (stack.isEmpty()) {
            stack.push(item);
            return;
        }

        int top = stack.pop();
        insertAtBottom(stack, item);
        stack.push(top);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(34);
        stack.push(3);
        stack.push(31);
        stack.push(98);
        stack.push(92);

        System.out.println("Original Stack (top to bot): " + stack);

        Deque<Integer> sorted = sortStack(stack);
        System.out.println("Sorted Stack   (top to bot): " + sorted);

        reverseStack(sorted);
        System.out.println("Reversed Stack (top to bot): " + sorted);
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Sort Stack (Aux Stack)** | $O(N^2)$ Quadratic | $O(N)$ Temp Stack | Outer $N$ pass, inner pop back |
| **Reverse Stack (Recursive)**| $O(N^2)$ Quadratic | $O(N)$ Call Stack | $N$ calls to `insertAtBottom` ($O(N)$ each)|
| **Sort Stack (Recursive)** | $O(N^2)$ Quadratic | $O(N)$ Call Stack | Zero explicit object allocations |

## 10. Edge Cases
* **Empty Stack**: Base cases `if (stack.isEmpty()) return;` prevent recursion crashes.
* **Single Element Stack**: Solves instantly without popping loops.
* **Already Sorted Stack**: Auxiliary stack sorting executes in $O(N)$ best-case time.

## 11. Common Mistakes
* Forgetting to push `top` back onto the stack in `insertAtBottom` after the recursive call unwinds.
* Confusing ascending vs descending sort conditions (`tmpStack.peek() > curr` vs `tmpStack.peek() < curr`).
* Attempting to use a standard `for` loop to reverse a stack in-place (violates strict stack LIFO interface constraints!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Recursive Stack Reversal Structure:
> Recursive reversal requires TWO functions:
> 1. `reverse(stack)`: Pops current top and recurses until stack is empty.
> 2. **`insertAtBottom(stack, item)`**: Recursively drains stack, pushes `item` at bottom, and restores popped elements during call unwinding!

> **Memory Trick:** **"Reverse stack requires TWO recursive methods: reverse() and insertAtBottom()!"**

## 13. Comparisons
| Feature | Auxiliary Stack Reversal | In-Place Recursive Reversal |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Data Struct**| Requires 2 extra stacks | **Zero extra stack objects** |
| **Call Stack Memory** | $O(1)$ | $O(N)$ JVM Recursion Frames |
| **Interview Constraint** | Standard approach | **Required when "No Extra Memory" specified** |

## 14. How to Recognize This in Questions
* **"Sort a stack using an auxiliary stack"** $\rightarrow$ Insertion sort into `tmpStack`.
* **"Reverse a stack in-place using recursion without extra data structures"** $\rightarrow$ `reverse(stack)` + `insertAtBottom(stack, item)`.

## 15. Frequently Asked Interview Questions
* **Q: Why does in-place recursive stack reversal run in $O(N^2)$ time?**  
  *A:* `reverse(stack)` makes $N$ recursive calls. For each call, `insertAtBottom` traverses to the bottom of the remaining stack, making $O(k)$ operations. Sum of operations: $1 + 2 + \dots + N = \frac{N(N+1)}{2} \implies O(N^2)$ time.
* **Q: How can a stack be reversed in $O(N)$ time?**  
  *A:* By transferring all elements into a Queue and pushing them back into the Stack, or using two auxiliary stacks in linear time.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK SORTING & RECURSION-BASED REVERSAL              |
+-----------------------------------------------------------------------+
| • Sort Stack: Pop curr from stack; while tmpStack.peek() > curr,      |
|               pop from tmpStack back to stack. Push curr to tmpStack. |
| • Reverse Stack (In-Place): Pop temp; reverse(stack); insertAtBottom(temp)|
| • Insert At Bottom: If empty, push item. Else pop top, recurse, push top|
| • Target Complexity: Aux Sort O(N^2) Time, O(N) Space                 |
|                      Recursive Reverse O(N^2) Time, O(N) Call Stack   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement stack sorting using an auxiliary stack in $O(N^2)$ time.
- [ ] I can write the recursive `insertAtBottom(stack, item)` helper.
- [ ] I can write the recursive `reverseStack(stack)` function.
- [ ] I know why in-place recursive reversal takes $O(N^2)$ time.
- [ ] I can explain how the JVM Call Stack acts as implicit storage.
