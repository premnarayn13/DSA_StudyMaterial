# 01. Stack Fundamentals, LIFO Mechanics & Call Stack Management

## 1. Introduction
A **Stack** is a fundamental linear data structure following the **LIFO (Last-In, First-Out)** operational principle. The last element pushed onto a stack is strictly the first element to be popped off. Stacks power core computer architecture mechanisms—including the CPU **Function Call Stack**, recursion tracking, expression evaluation, syntax parsing, and back-tracking algorithms—operating in **$O(1)$ constant time for push, pop, and peek operations**.

> **Important:** In memory management and algorithm design, a Stack enforces **Strict Single-Boundary Access**. All mutations (insertions and deletions) occur exclusively at one designated end called the **Top of Stack (`top`)**.

```
LIFO Stack Operational Topology:
Push (Insert at Top)  ---> | [ Element C ] | <--- Top of Stack
                           | [ Element B ] |
Pop (Remove from Top) ---> | [ Element A ] | <--- Bottom of Stack
                           +---------------+
```

---

## 2. Core Concepts & LIFO Stack Taxonomy

### 2.1 The 4 Core Stack Operations
1. **`push(E item)`**: Inserts `item` onto the top of the stack. Time Complexity: **$O(1)$ Constant**.
2. **`pop()`**: Removes and returns the top element of the stack. Throws `EmptyStackException` if stack is empty. Time Complexity: **$O(1)$ Constant**.
3. **`peek()` / `top()`**: Returns the top element without removing it. Time Complexity: **$O(1)$ Constant**.
4. **`isEmpty()`**: Checks whether the stack contains 0 elements. Time Complexity: **$O(1)$ Constant**.

```
Stack Operational Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Stack Operation       | Time Complexity   | Auxiliary Space   | Exception Case    |
+-----------------------+-------------------+-------------------+-------------------+
| `push(item)`          | **$O(1)$ Constant**| $O(1)$ Heap Space | Stack Overflow    |
| `pop()`               | **$O(1)$ Constant**| $O(1)$ Constant   | Stack Underflow   |
| `peek()`              | **$O(1)$ Constant**| $O(1)$ Constant   | Stack Underflow   |
| `isEmpty()`           | **$O(1)$ Constant**| $O(1)$ Constant   | None              |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LIFO: Last In, First Out! Push, Pop, Peek operate exclusively at the TOP in O(1) time!"**

---

## 3. Characteristics & Computer System Applications

### 3.1 The System Call Stack & Recursion
In low-level runtime systems (JVM, C/C++ execution environments), every function invocation creates a **Stack Frame** pushed onto the thread's call stack:
* **Stack Frame Contents**: Function arguments, local variables, return memory address, and evaluation registers.
* **Stack Overflow (`java.lang.StackOverflowError`)**: Occurs when infinite recursion or excessively deep call stacks exceed memory boundaries allocated for the thread stack (typically 1 MB).

```
Call Stack Execution Trace for Factorial Recursive Function (factorial(3)):
Call Stack Growth (Pushing Frames):       Stack Frame Unwinding (Popping Frames):
| Frame: factorial(1) -> returns 1 |      | Frame: factorial(1) -> popped | -> returns 1
| Frame: factorial(2) -> waits    |  ===>| Frame: factorial(2) -> popped | -> 2 * 1 = 2
| Frame: factorial(3) -> waits    |      | Frame: factorial(3) -> popped | -> 3 * 2 = 6
+----------------------------------+      +----------------------------------+
```

---

## 4. Internal Working Mechanics
Tracing Stack Push and Pop Operations on an Array-backed Stack:

```
Init: Capacity = 4, top = -1. Stack: [ _ , _ , _ , _ ]

Push(10): top++ (0). Stack: [ 10 , _ , _ , _ ] (top = 0)
Push(20): top++ (1). Stack: [ 10 , 20 , _ , _ ] (top = 1)
Push(30): top++ (2). Stack: [ 10 , 20 , 30 , _ ] (top = 2)

Peek(): Returns stack[2] = 30. Stack unchanged.

Pop(): Returns stack[2] = 30. top-- (1). Stack: [ 10 , 20 , _ , _ ] (top = 1)
Pop(): Returns stack[1] = 20. top-- (0). Stack: [ 10 , _ , _ , _ ] (top = 0)

All operations completed in O(1) Constant Time! ✅
```

---

## 5. Visual Diagram
LIFO Stack Mutation Boundaries:

```
          Push (70)                    Pop ()
             |                           ^
             v                           |
      +--------------+            +--------------+
      |  Val: 70     | <--- Top   |  Val: 70     | (Removed)
      +--------------+            +--------------+
      |  Val: 40     |            |  Val: 40     | <--- New Top
      +--------------+            +--------------+
      |  Val: 10     |            |  Val: 10     |
      +--------------+            +--------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a thread-safe Fixed-Capacity Array Stack and Dynamic Resizing Array Stack:

```java
import java.util.EmptyStackException;

public class ArrayStackMaster<T> {

    private Object[] array;
    private int top;
    private int capacity;

    @SuppressWarnings("unchecked")
    public ArrayStackMaster(int initialCapacity) {
        this.capacity = initialCapacity;
        this.array = new Object[initialCapacity];
        this.top = -1;
    }

    // O(1) Push Operation with Automatic Dynamic Resizing
    public void push(T item) {
        if (top == capacity - 1) {
            resize(capacity * 2); // Double capacity when full
        }
        array[++top] = item;
    }

    // O(1) Pop Operation with Automatic Shrinking
    @SuppressWarnings("unchecked")
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T item = (T) array[top];
        array[top--] = null; // Prevent memory leak

        // Shrink array if size falls below 25% capacity
        if (top > 0 && top == capacity / 4) {
            resize(capacity / 2);
        }
        return item;
    }

    // O(1) Peek Operation
    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return (T) array[top];
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public int size() {
        return top + 1;
    }

    private void resize(int newCapacity) {
        Object[] temp = new Object[newCapacity];
        System.arraycopy(array, 0, temp, 0, top + 1);
        this.array = temp;
        this.capacity = newCapacity;
    }
}
```

> **Quick Syntax:**
```java
// Standard Java Stack / Deque Usage (Prefer ArrayDeque over java.util.Stack!)
Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);
int val = stack.pop();
int topVal = stack.peek();
```

---

## 7. Concrete Problem Examples
* **Browser Back Button Navigation**: Maintaining history URL stacks.
* **Undo / Redo Mechanism in Text Editors**: Dual undo/redo stacks.
* **Function Call Stack Execution**: Call frame management in compiler runtimes.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `ArrayStackMaster` and `ArrayDeque`:

```java
public class StackFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Custom Array Stack Demonstration ===");
        ArrayStackMaster<String> history = new ArrayStackMaster<>(2);
        history.push("google.com");
        history.push("github.com");
        history.push("leetcode.com"); // Triggers dynamic resize!

        System.out.println("Current Page (Peek): " + history.peek()); // leetcode.com
        System.out.println("Popped Page: " + history.pop());          // leetcode.com
        System.out.println("Back to Page: " + history.peek());        // github.com

        System.out.println("\n=== 2. Recommended Production Java Stack (ArrayDeque) ===");
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(100);
        stack.push(200);
        System.out.println("Top Element: " + stack.peek()); // 200
        System.out.println("Popped Value: " + stack.pop()); // 200
    }
}
```

---

## 9. Complexity Analysis

| Stack Implementation | Push Time | Pop Time | Peek Time | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Fixed Array Stack** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(N)$ Space** |
| **Resizing Array Stack**| **$O(1)$ Amortized ⚡**| **$O(1)$ Amortized ⚡**| **$O(1)$ Constant ⚡** | **$O(N)$ Space** |
| **Linked List Stack** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(N)$ Node Memory** |

---

## 10. Edge Cases & Boundary Handling
* **Stack Underflow**: Calling `pop()` or `peek()` on an empty stack (`top == -1`). Handled via `EmptyStackException`.
* **Stack Overflow**: Array bounds exceeded in fixed-size arrays. Handled via dynamic array resizing.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `java.util.Stack` in Production Java Code**:
  - `java.util.Stack` inherits from `java.util.Vector`, making all methods `synchronized` (adds lock overhead) and allowing invalid mid-stack index insertions (`stack.add(1, val)`).
  - **Use `java.util.ArrayDeque` as a LIFO Stack (`Deque<T> stack = new ArrayDeque<>()`)**.
* **Memory Leaks in Array-backed Stacks**:
  - Forgetting to nullify popped elements (`array[top--] = null`) leaves dereferenced object references in the array, preventing Garbage Collection.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `ArrayDeque` is Superior to `java.util.Stack`:
> 1. **No Locking Overhead**: `ArrayDeque` is non-synchronized, running faster than legacy synchronized `Vector`-backed `java.util.Stack`.
> 2. **Strict LIFO API**: `Deque` interface enforces clean LIFO stack contracts (`push`, `pop`, `peek`).
> 3. **Better Cache Locality**: Array-backed layout outperforms node-based `LinkedList` stacks in CPU cache utilization.

> **Memory Trick:** **"Never use java.util.Stack! Always use Deque<T> stack = new ArrayDeque<>()!"**

---

## 13. System & Implementation Comparisons

| Feature | `ArrayDeque` Stack | `LinkedList` Stack | Legacy `java.util.Stack` |
| :--- | :--- | :--- | :--- |
| **Cache Locality** | **Excellence (Contiguous Array) ⚡**| Poor (Heap Pointers) | Moderate |
| **Synchronization** | Non-Synchronized (Fast) | Non-Synchronized | **Synchronized (Slow)** |
| **Memory Overhead** | Low (Primitive Array) | High (Node Object Pointers)| Moderate |

---

## 14. How to Recognize This in Questions
* **"Evaluate expression, parse nested brackets, or track call back-tracking"** $\rightarrow$ Stack (LIFO).
* **"Maintain reverse history or undo/redo sequence"** $\rightarrow$ Stack (LIFO).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does array resizing in a Dynamic Stack take $O(1)$ amortized time?**  
  *A:* Doubling array capacity on overflow spreads the $O(N)$ reallocation cost across $N$ subsequent $O(1)$ push operations, yielding $O(1)$ amortized time per push.
* **Q: What is the difference between `ArrayDeque.push()` and `ArrayDeque.add()`?**  
  *A:* `push()` inserts elements at the FRONT (top) of the deque (LIFO stack behavior). `add()` inserts elements at the END of the deque (FIFO queue behavior).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK FUNDAMENTALS & LIFO MECHANICS                   |
+-----------------------------------------------------------------------+
| • LIFO Principle: Last-In, First-Out                                  |
| • Operational Boundary: Mutations occur exclusively at Top of Stack   |
| • Time Complexity: push, pop, peek operate in O(1) Constant Time ⚡   |
| • Recommended Java Class: Deque<T> stack = new ArrayDeque<>()         |
| • Memory Leak Prevention: Set array[top] = null on pop                |
| • System Role: Powers system Call Stacks, Expression Parsing & Undo    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a custom Array-backed Stack with dynamic resizing.
- [ ] I know why `ArrayDeque` is preferred over `java.util.Stack`.
- [ ] I can explain LIFO mechanics and call stack frame management.
- [ ] I know how to prevent memory leaks in array stacks.
- [ ] I can state the amortized complexity of stack push operations.
