# 02. Stack Implementations (Array-Based & Linked List-Based)

## 1. Introduction
Implementing a Stack from scratch using primitive arrays or linked list nodes is a foundational interview topic. Technical interviews often ask candidates to design a custom Stack data structure, implement a **Min Stack** (LeetCode 155) returning the minimum element in $O(1)$ time, or design a Stack with dynamic resizing capabilities to evaluate low-level data structure design and memory management.

> **Important:** Array-based stack implementations offer superior CPU L1/L2 cache locality, while Linked List-based stack implementations guarantee **Strict $O(1)$ worst-case time per push** (eliminating array resizing latency spikes).

## 2. Core Concepts
* **Array-Based Stack**: Uses an internal array `int[] arr` and an integer pointer `top` (initialized to `-1`).
  * `push(val)`: `arr[++top] = val;`
  * `pop()`: `return arr[top--];`
  * `peek()`: `return arr[top];`
* **Linked List-Based Stack**: Uses a singly linked list where insertions and deletions occur strictly at the **Head Node** ($O(1)$ constant time).
* **Min Stack (LeetCode 155)**: Maintains two parallel stacks or paired value nodes (`val`, `currentMin`) to retrieve the minimum element in $O(1)$ constant time.

> **Memory Trick for Min Stack:** **"Push (val, Math.min(val, currentMin)) onto stack! Peak minStack to get min in O(1) time!"**

## 3. Characteristics / Properties
* **Array-Based vs Linked List-Based**:

```
Stack Implementation Trade-Offs Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric                | Array-Based Stack | Linked List Stack | Winner / Choice   |
+-----------------------+-------------------+-------------------+-------------------+
| Amortized Push Time   | Amortized O(1)    | Strict O(1) ⚡    | Linked List       |
| Memory Overhead       | Compact Array     | 24B Node Header   | Array-Based       |
| Cache Locality        | High L1 Hits ⚡   | High Cache Misses | Array-Based       |
| Dynamic Resizing      | Requires 2x Copy  | No Resize Needed  | Linked List       |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Min Stack ($O(1)$ Min Retrieval) on `push(5), push(3), push(7), push(2), pop()`:

```
Push 5: Value Stack = [5],        Min Stack = [5]        (Current Min = 5)
Push 3: Value Stack = [5, 3],     Min Stack = [5, 3]     (Current Min = 3)
Push 7: Value Stack = [5, 3, 7],  Min Stack = [5, 3, 3]  (Current Min = 3)
Push 2: Value Stack = [5, 3, 7, 2], Min Stack = [5, 3, 3, 2] (Current Min = 2)

getMin() -> Returns Min Stack Top = 2 ✅
pop()    -> Pops 2 from Value Stack, Pops 2 from Min Stack
getMin() -> Returns Min Stack Top = 3 ✅
```

## 5. Visual Diagram
Min Stack Dual Stack Mechanics:

```
Main Stack:     [ 2 ] (top)      Min Stack:     [ 2 ] (top)
                [ 7 ]                           [ 3 ]
                [ 3 ]                           [ 3 ]
                [ 5 ]                           [ 5 ]

Notice: Min Stack top ALWAYS holds the minimum element of the main stack!
```

## 6. Operations / Algorithms
Array-Based Custom Stack Implementation:

```java
public class CustomArrayStack {
    private int[] data;
    private int top;
    private static final int INITIAL_CAPACITY = 10;

    public CustomArrayStack() {
        this.data = new int[INITIAL_CAPACITY];
        this.top = -1;
    }

    public void push(int val) {
        if (top == data.length - 1) {
            resize(); // Double array capacity
        }
        data[++top] = val;
    }

    public int pop() {
        if (isEmpty()) throw new IllegalStateException("Stack Underflow");
        return data[top--];
    }

    public int peek() {
        if (isEmpty()) throw new IllegalStateException("Stack Underflow");
        return data[top];
    }

    public boolean isEmpty() {
        return top == -1;
    }

    private void resize() {
        int[] newData = new int[data.length * 2];
        System.arraycopy(data, 0, newData, 0, data.length);
        data = newData;
    }
}
```

> **Quick Syntax:**
```java
// Array Stack Push / Pop Idioms
data[++top] = val; // Push
int val = data[top--]; // Pop
```

## 7. Examples
* **LeetCode 155 - Min Stack**: $O(1)$ minimum element retrieval using dual stacks.
* **Custom Array-Based Stack**: Dynamic array stack implementation.
* **Custom Linked List-Based Stack**: Node-based stack implementation.

## 8. Java Code
Complete interview-ready Java suite implementing Custom Linked List Stack and LeetCode 155 Min Stack:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class StackImplementationsMaster {

    // 1. Custom Linked List Stack Implementation
    public static class LinkedListStack {
        private static class Node {
            int val;
            Node next;
            Node(int val) { this.val = val; }
        }

        private Node head = null;
        private int size = 0;

        public void push(int val) {
            Node newNode = new Node(val);
            newNode.next = head;
            head = newNode;
            size++;
        }

        public int pop() {
            if (isEmpty()) throw new IllegalStateException("Stack Underflow");
            int val = head.val;
            head = head.next;
            size--;
            return val;
        }

        public int peek() {
            if (isEmpty()) throw new IllegalStateException("Stack Underflow");
            return head.val;
        }

        public boolean isEmpty() { return head == null; }
        public int size() { return size; }
    }

    // 2. LeetCode 155: Min Stack O(1) All Operations
    public static class MinStack {
        private final Deque<Integer> stack;
        private final Deque<Integer> minStack;

        public MinStack() {
            this.stack = new ArrayDeque<>();
            this.minStack = new ArrayDeque<>();
        }

        public void push(int val) {
            stack.push(val);
            if (minStack.isEmpty() || val <= minStack.peek()) {
                minStack.push(val);
            } else {
                minStack.push(minStack.peek()); // Repeat current minimum
            }
        }

        public void pop() {
            stack.pop();
            minStack.pop();
        }

        public int top() {
            return stack.peek();
        }

        public int getMin() {
            return minStack.peek();
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        MinStack minStack = new MinStack();
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);

        System.out.println("Get Min: " + minStack.getMin()); // Output: -3
        minStack.pop();
        System.out.println("Top: "     + minStack.top());    // Output: 0
        System.out.println("Get Min: " + minStack.getMin()); // Output: -2
    }
}
```

## 9. Complexity Analysis
| Stack Implementation | Push Time | Pop Time | Peek Time | Space Overhead |
| :--- | :--- | :--- | :--- | :--- |
| **Array-Based Stack** | Amortized $O(1)$ | $O(1)$ | $O(1)$ | Compact Array (Low) |
| **Linked List Stack** | Strict $O(1)$ ⚡ | $O(1)$ | $O(1)$ | 24 Bytes / Node (High) |
| **Min Stack (Dual)** | Amortized $O(1)$ | $O(1)$ | $O(1)$ | $2 \times O(N)$ Space |

## 10. Edge Cases
* **Stack Underflow**: Attempting to pop/peek an empty stack. Throw `IllegalStateException` or guard with `isEmpty()`.
* **Stack Overflow**: In fixed-size array stacks, pushing beyond max capacity. Solved by dynamic array resizing ($2\times$).
* **Min Stack Duplicates**: When pushing duplicates of the minimum element (e.g. `push(2), push(2)`), `val <= minStack.peek()` MUST use `<=` (not `<`) so that popping one `2` does not discard the minimum prematurely!

## 11. Common Mistakes
* Using `val < minStack.peek()` instead of `val <= minStack.peek()` in Min Stack (causes minimum tracking corruption when duplicate minimum values are pushed and popped!).
* In Array Stack `pop()`, failing to decrement `top--`.
* In Linked List Stack, inserting at the **Tail** instead of the **Head** (forces $O(N)$ pop traversal!). Always insert/delete at **Head** for $O(1)$ stack performance.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Min Stack Duplicate Condition Rule:
> When pushing to `minStack`:
> Use **`val <= minStack.peek()`** (with `<=` equality!).
> If you use `<` strictly, popping a duplicate minimum value will pop the ONLY copy from `minStack`, corrupting future `getMin()` queries!

> **Memory Trick:** **"Min Stack Push Rule: val <= minStack.peek() (Keep duplicates!)"**

## 13. Comparisons
| Feature | Single Stack Node Object Pair | Dual Stack (`stack` + `minStack`) |
| :--- | :--- | :--- |
| **Implementation**| Stores `Pair(val, min)` in 1 stack | Stores 2 separate `ArrayDeque` stacks |
| **Memory Footprint**| Allocates Pair objects | Primitive boxing or integer array |
| **Code Cleanliness**| Slightly verbose | **Clean & Standard Interview Setup** |

## 14. How to Recognize This in Questions
* **"Design a Stack supporting getMin() in O(1) time"** $\rightarrow$ LeetCode 155 Min Stack.
* **"Implement Stack using primitive arrays or linked nodes"** $\rightarrow$ Custom Stack Design.

## 15. Frequently Asked Interview Questions
* **Q: How does Min Stack achieve $O(1)$ time for `getMin()`?**  
  *A:* By pairing every pushed value with the minimum value seen up to that point using a secondary `minStack`. The top of `minStack` always holds the current minimum in $O(1)$ lookup time.
* **Q: Why MUST Linked List stack operations occur at the Head node?**  
  *A:* Head insertion (`newNode.next = head; head = newNode;`) and head deletion (`head = head.next;`) execute in **Strict $O(1)$ constant time**. Inserting/deleting at the tail of a singly linked list requires $O(N)$ linear traversal.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK IMPLEMENTATIONS & MIN STACK                     |
+-----------------------------------------------------------------------+
| • Array Stack: data[++top] = val (push) | return data[top--] (pop)    |
| • Linked List Stack: Always insert/delete at HEAD for Strict O(1) ops |
| • Min Stack Rule: Maintain dual minStack holding current min at top   |
| • Min Push Condition: if (minStack.isEmpty() || val <= minStack.peek())|
| • Equality Check: Use `<=` to handle duplicate minimum values!        |
| • Min Stack Complexity: O(1) Push, Pop, Peek, getMin | O(N) Space     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement an Array-based Stack with dynamic resizing.
- [ ] I can implement a Linked List-based Stack operating at Head.
- [ ] I know why `val <= minStack.peek()` requires `<=` for duplicates.
- [ ] I can implement Min Stack (LeetCode 155) in under 5 minutes.
- [ ] I know the trade-offs between Array-based and Linked List-based stacks.
