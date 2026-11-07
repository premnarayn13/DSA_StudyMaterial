# 11. Min Stack & Max Stack Design, Auxiliary Tracking & $O(1)$ Space Formula Encoding

## 1. Introduction
Designing a **Min Stack** or **Max Stack** requires supporting standard stack operations (`push`, `pop`, `top`) while retrieving the minimum or maximum element in the entire stack in **$O(1)$ constant time**. Algorithms like **Min Stack (LeetCode 155)** and **Max Stack (LeetCode 716)** achieve this using either an **Auxiliary Tracking Stack** ($O(N)$ space overhead) or an **$O(1)$ Auxiliary Space Mathematical Difference Encoding Formula** ($2 \times \text{val} - \text{minVal}$).

> **Important:** Why can't a simple variable `minVal` maintain the minimum element on a stack?
> While `minVal` works when pushing new smaller elements, **popping the current minimum element loses historical minimum context**! A Min Stack MUST preserve historical minimum states as elements are popped!

```
Dual Stack vs Single Encoded Stack Strategy:
+-----------------------------------------------------------------------------------+
| 1. Dual Stack Strategy   : Main Stack + Auxiliary Min Stack (Easy, O(N) Space)     |
| 2. Encoded Math Strategy : Encodes diff (2*val - minVal) in single stack (O(1) Space)⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Min Stack Dual Stack Architecture (LeetCode 155)

### 2.1 Auxiliary Min Stack Strategy (LeetCode 155 - Dual Stack)
* **Main Stack (`mainStack`)**: Stores all pushed elements.
* **Min Stack (`minStack`)**: Stores the minimum element corresponding to each stack level.

#### Operational Rules:
1. **`push(val)`**:
   - Push `val` onto `mainStack`.
   - If `minStack.isEmpty()` OR `val <= minStack.peek()`, push `val` onto `minStack`! (Must use `<=` to handle duplicate minimums!).
2. **`pop()`**:
   - If `mainStack.peek().equals(minStack.peek())`, pop `minStack`!
   - Pop `mainStack`.
3. **`getMin()`**:
   - Return `minStack.peek()`. (Runs in **$O(1)$ Constant Time**!).

```
Auxiliary Min Stack Invariant:
minStack.peek() is ALWAYS equal to the minimum element in mainStack from bottom up to current top! ⚡
```

> **Memory Trick:** **"Min Stack Dual Strategy: Push onto minStack if val <= minStack.peek()! Pop minStack if mainStack.peek() == minStack.peek()!"**

---

## 3. Characteristics & $O(1)$ Auxiliary Space Mathematical Difference Encoding

### 3.1 $O(1)$ Auxiliary Space Difference Encoding Formula
To achieve **$O(1)$ Auxiliary Memory** (without an extra `minStack`):
* Store encoded difference values in a single 64-bit `long` stack!

#### Mathematical Formula:
1. **Push Rule (`val`)**:
   - If stack is empty: Set `min = val`, push `val`.
   - Else if `val < min`:
     - Push encoded value: **`encoded = 2 * (long) val - min`**! (Since `val < min`, `encoded < val`).
     - Update global minimum: `min = val`.
   - Else (`val >= min`):
     - Push `val` directly.

2. **Pop Rule**:
   - Let `top = stack.pop()`.
   - If `top < min`:
     - The popped element was the minimum!
     - The true minimum value to return is `current min`.
     - Restore previous minimum: **`min = 2 * min - top`**!
   - Else:
     - Return `top`.

3. **GetMin Rule**:
   - Return `(int) min`.

```
Proof of Difference Encoding Restoration:
When val < prevMin, we pushed encoded = 2*val - prevMin and updated min = val.
During pop(), since top < min, we restore prevMin via:
prevMin = 2 * min - top = 2 * val - (2 * val - prevMin) = prevMin! ⚡ (Flawless O(1) Space Restoration!)
```

---

## 4. Internal Working Mechanics
Tracing Min Stack Dual Strategy (LeetCode 155) on operations `push(-2)`, `push(0)`, `push(-3)`, `getMin()`, `pop()`, `top()`, `getMin()`:

```
push(-2): mainStack = [-2], minStack = [-2]. min = -2.
push(0) : mainStack = [-2, 0], minStack = [-2] (0 > -2, minStack unchanged).
push(-3): mainStack = [-2, 0, -3], minStack = [-2, -3] (-3 <= -2, push -3).

getMin(): Returns minStack.peek() = -3. ✅

pop()   : mainStack.peek() (-3) == minStack.peek() (-3) -> Pop minStack!
          mainStack = [-2, 0], minStack = [-2].

top()   : Returns mainStack.peek() = 0. ✅
getMin(): Returns minStack.peek() = -2. ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
Dual Stack Min Tracking Topology:

```
Main Stack             Min Stack
+----------+          +----------+
|  Val: -3 | <--- Top |  Val: -3 | <--- Current Min (-3)
+----------+          +----------+
|  Val:  0 |          |  Val: -2 | <--- Previous Min (-2)
+----------+          +----------+
|  Val: -2 |
+----------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementations of Min Stack Dual Strategy (LeetCode 155) and $O(1)$ Space Difference Encoded Min Stack:

```java
import java.util.*;

public class MinStackMaster {

    // 1. Min Stack: Dual Stack Strategy (LeetCode 155) O(1) Time, O(N) Space
    public static class MinStackDual {
        private Deque<Integer> mainStack;
        private Deque<Integer> minStack;

        public MinStackDual() {
            mainStack = new ArrayDeque<>();
            minStack = new ArrayDeque<>();
        }

        public void push(int val) {
            mainStack.push(val);
            if (minStack.isEmpty() || val <= minStack.peek()) {
                minStack.push(val); // Must use <= for duplicates!
            }
        }

        public void pop() {
            if (mainStack.isEmpty()) return;
            int popped = mainStack.pop();
            if (!minStack.isEmpty() && popped == minStack.peek()) {
                minStack.pop();
            }
        }

        public int top() {
            return mainStack.peek();
        }

        public int getMin() {
            return minStack.peek();
        }
    }

    // 2. Min Stack: O(1) Auxiliary Space Mathematical Encoding Engine
    public static class MinStackEncoded {
        private Deque<Long> stack;
        private long min;

        public MinStackEncoded() {
            stack = new ArrayDeque<>();
        }

        public void push(int val) {
            if (stack.isEmpty()) {
                min = val;
                stack.push((long) val);
            } else if (val < min) {
                // Encode difference: 2 * val - min
                stack.push(2 * (long) val - min);
                min = val; // Update min to current val
            } else {
                stack.push((long) val);
            }
        }

        public void pop() {
            if (stack.isEmpty()) return;

            long top = stack.pop();
            if (top < min) {
                // Popped element was min; restore previous min
                min = 2 * min - top;
            }
        }

        public int top() {
            long top = stack.peek();
            if (top < min) {
                return (int) min;
            }
            return (int) top;
        }

        public int getMin() {
            return (int) min;
        }
    }
}
```

> **Quick Syntax:**
```java
// Dual Stack Pop Duplicate Handling
if (mainStack.peek().equals(minStack.peek())) {
    minStack.pop();
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 155 - Min Stack**: Standard $O(1)$ min retrieval stack.
* **LeetCode 716 - Max Stack**: Dual stack + double linked list $O(1)$ max retrieval and removal.
* **Sliding Window Minimum**: Pairing 2 Min Stacks to build an $O(1)$ Queue.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `MinStackDual` and `MinStackEncoded`:

```java
public class MinStackDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Min Stack (Dual Strategy) ===");
        MinStackMaster.MinStackDual minStack = new MinStackMaster.MinStackDual();
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);
        System.out.println("Current Min: " + minStack.getMin()); // -3
        minStack.pop();
        System.out.println("Top Element: " + minStack.top());   // 0
        System.out.println("New Min: " + minStack.getMin());    // -2

        System.out.println("\n=== 2. Min Stack (O(1) Space Difference Encoding) ===");
        MinStackMaster.MinStackEncoded encodedStack = new MinStackMaster.MinStackEncoded();
        encodedStack.push(5);
        encodedStack.push(3);
        encodedStack.push(7);
        System.out.println("Encoded Min: " + encodedStack.getMin()); // 3
        encodedStack.pop(); // pops 7
        encodedStack.pop(); // pops 3 (restores min=5!)
        System.out.println("Restored Min: " + encodedStack.getMin()); // 5
    }
}
```

---

## 9. Complexity Analysis

| Implementation Strategy | Push Time | Pop Time | GetMin Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Dual Stack Strategy** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Space |
| **Encoded Difference Math**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Strict In-Place ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Minimum Values (`push(2)`, `push(2)`)**: Dual stack MUST use `val <= minStack.peek()` to push duplicate minimums onto `minStack`.
* **Integer Overflow in Encoded Math**: `2 * (long) val - min` uses 64-bit `long` to prevent 32-bit integer arithmetic overflow.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `val < minStack.peek()` (Strict Less Than) in Dual Strategy**:
  - Pushing duplicates without `<=` fails to record duplicate minimums in `minStack`. Popping the first instance removes the minimum entry, leaving subsequent duplicates un-tracked!
  - **Always use `val <= minStack.peek()`**.
* **Using `Integer` Reference Equality (`mainStack.peek() == minStack.peek()`)**:
  - In Java, `Integer` values outside `-128 ... 127` cache range fail `==` comparison!
  - **Always use `.equals()` or unbox primitives (`popped == minStack.peek()`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Dual Stack vs Encoded Math Choice:
> In technical coding interviews:
> 1. **Dual Stack Strategy** is preferred by interviewers for clean readability, type safety, and handling arbitrary data types.
> 2. **Encoded Difference Math Strategy** is an impressive follow-up answer when asked: *"Can you optimize Auxiliary Space to O(1)?"*

> **Memory Trick:** **"Dual Stack handles duplicate minimums using <= ! Encoded Math restores prevMin using 2*min - top!"**

---

## 13. System & Implementation Comparisons

| Feature | Dual Stack Strategy | Encoded Math Strategy |
| :--- | :--- | :--- |
| **Readability** | High (Industry Standard) | Medium (Mathematical trick) |
| **Type Support** | Generic Types (`T`) | Numerical Primitives Only |
| **Auxiliary Memory** | $O(N)$ Memory Overhead | **$O(1)$ Constant Memory ⚡** |

---

## 14. How to Recognize This in Questions
* **"Design a stack that retrieves the minimum element in O(1) time"** $\rightarrow$ LeetCode 155 (Min Stack).
* **"Retrieve min element in O(1) time with O(1) extra space"** $\rightarrow$ Difference Encoded Min Stack.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `val <= minStack.peek()` use `<=` instead of `<`?**  
  *A:* If `nums = [2, 1, 1]`, `minStack` stores `[2, 1, 1]`. When popping the top `1`, `mainStack` still contains a `1`, which is correctly preserved as `minStack.peek() = 1`.
* **Q: How does `2 * min - top` restore the previous minimum value in the encoded stack?**  
  *A:* When `val < prevMin`, we stored `top = 2*val - prevMin` and set `min = val`. During pop, `2 * min - top = 2 * val - (2*val - prevMin) = prevMin`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MIN STACK & MAX STACK DESIGN                          |
+-----------------------------------------------------------------------+
| • Dual Strategy Rule: Push onto minStack if val <= minStack.peek()    |
| • Dual Pop Rule: Pop minStack if mainStack.peek() equals minStack.peek()|
| • Encoded Push Rule: If val < min, push 2*val - min and set min = val |
| • Encoded Pop Rule: If top < min, restore min = 2*min - top           |
| • Time Complexity: push, pop, top, getMin operate in O(1) Time ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement Min Stack using Dual Stack Strategy (LeetCode 155).
- [ ] I know why `<=` is required for duplicate minimums in Dual Stack.
- [ ] I can write $O(1)$ Space Difference Encoded Min Stack.
- [ ] I can derive the restoration formula `min = 2 * min - top`.
- [ ] I know why `.equals()` must be used for Java `Integer` comparisons.
