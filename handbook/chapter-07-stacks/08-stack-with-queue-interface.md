# 08. Implementing Queues Using Stacks & Stacks Using Queues

## 1. Introduction
Cross-implementing fundamental data structures—specifically implementing a **Queue using Stacks** (LeetCode 232 - Implement Queue using Stacks) and a **Stack using Queues** (LeetCode 225 - Implement Stack using Queues)—is a foundational technical interview topic. These problems evaluate amortized analysis, dual-buffer transfer dynamics, FIFO vs LIFO structural translation, and operational efficiency trade-offs.

> **Important:** Implementing a Queue using 2 Stacks (`inStack` and `outStack`) achieves **Amortized $O(1)$ time per operation**! Elements are pushed onto `inStack` in $O(1)$ time, and transferred to `outStack` ONLY when `outStack` becomes empty!

## 2. Core Concepts
* **Implement Queue Using 2 Stacks (LeetCode 232)**:
  * **`inStack`**: Accepts new elements via `push()` ($O(1)$ time).
  * **`outStack`**: Serves `pop()` and `peek()` operations.
  * **Lazy Transfer Rule**: If `outStack` is empty, pop ALL elements from `inStack` and push them onto `outStack` (reversing their order to FIFO!).
  * **Amortized Proof**: Each element is pushed to `inStack` once, moved to `outStack` once, and popped from `outStack` once $\implies$ **Amortized $O(1)$ Time per Operation**!
* **Implement Stack Using 1 Queue (LeetCode 225)**:
  * Push element `x` into queue.
  * Rotate queue `size - 1` times: `queue.add(queue.poll())`.
  * Moves newly added element `x` to the FRONT of the queue ($O(N)$ push time, $O(1)$ pop time)!

> **Memory Trick:** **"Queue via 2 Stacks: Lazy transfer from inStack to outStack ONLY when outStack is empty!"**

## 3. Characteristics / Properties
* **Dual Stack FIFO Realization**: Reversing LIFO twice yields FIFO ($LIFO \times LIFO = FIFO$).
* **Amortized $O(1)$ Efficiency Guarantee**: While a single `pop()` call may take $O(N)$ time when transferring elements from `inStack` to `outStack`, that cost is spread across $N$ subsequent $O(1)$ pops.

```
Cross Implementation Operations Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Design Problem        | Push Time         | Pop Time          | Peak / Front Time |
+-----------------------+-------------------+-------------------+-------------------+
| Queue using 2 Stacks  | Strict O(1) ⚡    | Amortized O(1) ⚡ | Amortized O(1) ⚡ |
| Stack using 1 Queue   | O(N) Linear       | Strict O(1) ⚡    | Strict O(1) ⚡    |
| Stack using 2 Queues  | O(N) Linear       | Strict O(1) ⚡    | Strict O(1) ⚡    |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Queue using 2 Stacks (LeetCode 232) on `push(1), push(2), peek(), pop(), push(3), pop()`:

```
push(1): inStack = [1],         outStack = []
push(2): inStack = [1, 2],      outStack = []

peek(): outStack is empty! Transfer all from inStack -> outStack:
        - pop 2 from inStack -> push 2 to outStack
        - pop 1 from inStack -> push 1 to outStack
        inStack = [], outStack = [2, 1] (Top is 1) -> Returns 1 ✅

pop():  outStack.pop() -> Returns 1. inStack = [], outStack = [2]
push(3): inStack = [3], outStack = [2]

pop():  outStack is NOT empty! outStack.pop() -> Returns 2 (Zero Transfer Overhead!) ✅
```

## 5. Visual Diagram
Lazy Dual-Stack Queue Transfer Architecture:

```
[ PUSH PHASE ]                    [ POP / PEEK PHASE ]
Elements enter inStack             Lazy Transfer to outStack
      +---+                              +---+
      | 3 |                              | 1 |  <--- Front of Queue (Pop first!)
      +---+                              +---+
      | 2 |                              | 2 |
      +---+                              +---+
      | 1 |  === (Transfer when empty) =>| 3 |
      +---+                              +---+
     inStack                            outStack
```

## 6. Operations / Algorithms
LeetCode 232 Master Implementation:

```java
public class MyQueue {
    private final Deque<Integer> inStack;
    private final Deque<Integer> outStack;

    public MyQueue() {
        this.inStack = new ArrayDeque<>();
        this.outStack = new ArrayDeque<>();
    }

    // Strict O(1) Time
    public void push(int x) {
        inStack.push(x);
    }

    // Amortized O(1) Time
    public int pop() {
        transferIfNeeded();
        return outStack.pop();
    }

    // Amortized O(1) Time
    public int peek() {
        transferIfNeeded();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    // Helper: Transfer elements from inStack to outStack ONLY when outStack is empty
    private void transferIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Lazy Transfer Condition
if (outStack.isEmpty()) {
    while (!inStack.isEmpty()) {
        outStack.push(inStack.pop());
    }
}
```

## 7. Examples
* **LeetCode 232 - Implement Queue using Stacks**: Amortized $O(1)$ dual stack implementation.
* **LeetCode 225 - Implement Stack using Queues**: $O(N)$ push / $O(1)$ pop queue rotation implementation.

## 8. Java Code
Complete interview-ready Java suite implementing Queue using 2 Stacks and Stack using 1 Queue:

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

public class StackQueueCrossImplementationMaster {

    // 1. Queue using 2 Stacks (LeetCode 232) Amortized O(1) All Operations
    public static class MyQueue {
        private final Deque<Integer> inStack = new ArrayDeque<>();
        private final Deque<Integer> outStack = new ArrayDeque<>();

        public void push(int x) {
            inStack.push(x);
        }

        public int pop() {
            transferIfNeeded();
            return outStack.pop();
        }

        public int peek() {
            transferIfNeeded();
            return outStack.peek();
        }

        public boolean empty() {
            return inStack.isEmpty() && outStack.isEmpty();
        }

        private void transferIfNeeded() {
            if (outStack.isEmpty()) {
                while (!inStack.isEmpty()) {
                    outStack.push(inStack.pop());
                }
            }
        }
    }

    // 2. Stack using 1 Queue (LeetCode 225) O(N) Push, O(1) Pop
    public static class MyStack {
        private final Queue<Integer> q = new LinkedList<>();

        public void push(int x) {
            q.add(x);
            int sz = q.size();
            // Rotate queue size-1 times to move new element to front
            for (int i = 0; i < sz - 1; i++) {
                q.add(q.poll());
            }
        }

        public int pop() {
            return q.poll();
        }

        public int top() {
            return q.peek();
        }

        public boolean empty() {
            return q.isEmpty();
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        MyQueue queue = new MyQueue();
        queue.push(10);
        queue.push(20);
        System.out.println("Queue Peek: " + queue.peek()); // Output: 10
        System.out.println("Queue Pop:  " + queue.pop());  // Output: 10
        System.out.println("Queue Pop:  " + queue.pop());  // Output: 20

        MyStack stack = new MyStack();
        stack.push(100);
        stack.push(200);
        System.out.println("Stack Top:  " + stack.top());  // Output: 200
        System.out.println("Stack Pop:  " + stack.pop());  // Output: 200
    }
}
```

## 9. Complexity Analysis
| Operation | Queue using 2 Stacks | Stack using 1 Queue |
| :--- | :--- | :--- |
| **`push()`** | **Strict $O(1)$ Constant ⚡**| $O(N)$ Queue Rotation |
| **`pop()`** | **Amortized $O(1)$ Constant ⚡**| **Strict $O(1)$ Constant ⚡** |
| **`peek() / top()`** | **Amortized $O(1)$ Constant ⚡**| **Strict $O(1)$ Constant ⚡** |
| **Auxiliary Space** | $O(N)$ Space | $O(N)$ Space |

## 10. Edge Cases
* **Empty Structure Exception**: Guard `pop()` and `peek()` or let native `ArrayDeque` / `Queue` throw `EmptyStackException` / `NoSuchElementException`.
* **Interleaved Push and Pop Operations**: Handled seamlessly by the lazy transfer condition (`if (outStack.isEmpty())`).

## 11. Common Mistakes
* Transferring elements from `inStack` to `outStack` on EVERY `pop()` call (ruins amortized $O(1)$ time complexity!). Transfer MUST occur **ONLY when `outStack.isEmpty()` is true**.
* Moving elements back from `outStack` to `inStack` after popping (corrupts reversed FIFO element ordering!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is transfer from `inStack` to `outStack` Amortized $O(1)$?
> Every element experiences:
> 1. Pushed to `inStack`: 1 operation.
> 2. Popped from `inStack` to `outStack`: 1 operation.
> 3. Popped from `outStack`: 1 operation.
> Total operations per element $= 3 \implies O(1)$ Amortized Time per operation!

> **Memory Trick:** **"Transfer inStack to outStack ONLY when outStack is empty! NEVER move elements back!"**

## 13. Comparisons
| Feature | Immediate Transfer Queue | Lazy Transfer Queue (Optimal) |
| :--- | :--- | :--- |
| **Push Time** | $O(N)$ Linear | **Strict $O(1)$ Constant ⚡** |
| **Pop Time** | $O(1)$ Constant | **Amortized $O(1)$ Constant ⚡** |
| **Total Operations**| $O(N^2)$ for $N$ pushes | **$O(N)$ Total for $N$ operations** |

## 14. How to Recognize This in Questions
* **"Implement FIFO Queue using LIFO Stacks"** $\rightarrow$ Dual Stack Lazy Transfer (LeetCode 232).
* **"Implement LIFO Stack using FIFO Queue"** $\rightarrow$ Queue Rotation (LeetCode 225).

## 15. Frequently Asked Interview Questions
* **Q: Explain why transferring elements from `inStack` to `outStack` only when `outStack` is empty yields amortized $O(1)$ time.**  
  *A:* Because each pushed element is transferred to `outStack` at most once in its lifetime. For $N$ elements pushed, at most $N$ transfer operations occur across all pops, yielding $O(N) / N = O(1)$ amortized cost per operation.
* **Q: How can a Stack be implemented using only 1 Queue?**  
  *A:* When pushing a new element `x`, append it to the queue and rotate the queue `size - 1` times by polling from front and re-offering to back. This places `x` at the front of the queue, making `pop()` and `top()` simple $O(1)$ queue poll/peek operations.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE VIA STACKS & STACK VIA QUEUES                   |
+-----------------------------------------------------------------------+
| • Queue via 2 Stacks: inStack (push) & outStack (pop/peek)            |
| • Lazy Transfer Rule: if (outStack.isEmpty()) while(!inStack.isEmpty()) outStack.push(inStack.pop())|
| • Never move elements back from outStack to inStack!                  |
| • Stack via 1 Queue: Add x, then rotate q.add(q.poll()) (size-1) times |
| • Amortized Complexity: Queue via 2 Stacks runs in Amortized O(1) Time|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write `transferIfNeeded()` for Queue using 2 Stacks.
- [ ] I know why transfer MUST occur ONLY when `outStack.isEmpty()`.
- [ ] I can prove why Queue via 2 Stacks achieves amortized $O(1)$ time.
- [ ] I can implement Stack using 1 Queue with $O(N)$ push queue rotation.
- [ ] I can solve LeetCode 232 and 225 from memory in under 5 minutes.
