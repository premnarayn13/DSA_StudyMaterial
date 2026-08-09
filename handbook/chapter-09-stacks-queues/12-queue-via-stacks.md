# 12. Queue via Stacks, Stack via Queues & Amortized Dual-Stack Conversions

## 1. Introduction
Converting between linear operational semantics—such as building a **FIFO Queue using Stacks (LeetCode 232)** or a **LIFO Stack using Queues (LeetCode 225)**—is a classic system design exercise in data structure adaptation. Using the **Dual-Stack Transfer Architecture** (`inStack` and `outStack`), a Queue constructed from two LIFO Stacks achieves **$O(1)$ Amortized Time for enqueue (`push`) and dequeue (`pop`) operations**.

> **Important:** Why does a Queue implemented with two Stacks achieve $O(1)$ Amortized Time?
> Popping elements from `inStack` and pushing them onto `outStack` reverses their LIFO order into FIFO order.
> Every element is pushed onto `inStack` once, moved to `outStack` once, and popped from `outStack` once!
> Total operations across $N$ elements = $3N \implies \mathbf{O(1)\text{ Amortized Time per Operation}}$!

```
Dual-Stack Queue Transfer Topology:
Enqueue Phase -> [ inStack (LIFO) ]
                       |
                 Transfer (On demand when outStack is empty)
                       v
Dequeue Phase <- [ outStack (FIFO Reversed) ]
```

---

## 2. Core Concepts & Dual-Stack Queue Architecture (LeetCode 232)

### 2.1 Implement Queue using Stacks (LeetCode 232)
Implement a First-In, First-Out (FIFO) queue using only two LIFO stacks:

#### Dual-Stack Strategy:
* **`inStack`**: Receives all incoming `push(x)` operations.
* **`outStack`**: Supplies all outgoing `pop()` and `peek()` operations.

#### Operational Invariants:
1. **`push(x)`**: Push `x` directly onto `inStack`. Time Complexity: **$O(1)$ Constant**.
2. **`pop()` / `peek()`**:
   - If `outStack.isEmpty()`, transfer ALL elements from `inStack` to `outStack`:
     - `while (!inStack.isEmpty()) outStack.push(inStack.pop());`
   - Return `outStack.pop()` or `outStack.peek()`. Time Complexity: **$O(1)$ Amortized**.
3. **`empty()`**: Return `inStack.isEmpty() && outStack.isEmpty()`.

```
Dual-Stack Element Reversal Invariant:
inStack Order  (LIFO) : [ Bottom: 10 | 20 | Top: 30 ]
Transfer Action       : Pop 30 -> Push 30; Pop 20 -> Push 20; Pop 10 -> Push 10
outStack Order (FIFO) : [ Bottom: 30 | 20 | Top: 10 ]  (Top of outStack is FRONT of Queue!) ⚡
```

> **Memory Trick:** **"Queue via 2 Stacks: Push to inStack; Pop/Peek from outStack! Transfer inStack to outStack ONLY when outStack is empty!"**

---

## 3. Characteristics & Stack via Queues Mechanics (LeetCode 225)

### 3.1 Implement Stack using Queues (LeetCode 225 - Single Queue Rotation)
Implement a Last-In, First-Out (LIFO) stack using a single FIFO queue:

#### Single Queue Rotation Strategy ($O(N)$ Push, $O(1)$ Pop):
1. Maintain a single `Queue<Integer> queue = new ArrayDeque<>()`.
2. **`push(x)`**:
   - `queue.offer(x)`.
   - Rotate previous elements behind `x`:
     - `for (int i = 0; i < queue.size() - 1; i++) queue.offer(queue.poll());`
3. **`pop()`**: Return `queue.poll()`. Time Complexity: **$O(1)$ Constant**.
4. **`top()`**: Return `queue.peek()`. Time Complexity: **$O(1)$ Constant**.

```
Single Queue Rotation Visual (Push 30 into Queue [10, 20]):
Step 1: Offer 30 -> Queue: [ 10, 20, 30 ] (30 is at rear)
Step 2: Rotate 2 items -> Poll 10, Offer 10 -> [ 20, 30, 10 ]
Step 3: Rotate again  -> Poll 20, Offer 20 -> [ 30, 10, 20 ] (30 is now at FRONT!) ⚡
```

---

## 4. Internal Working Mechanics
Tracing Queue via Stacks (LeetCode 232) on `push(1)`, `push(2)`, `peek()`, `pop()`, `empty()`:

```
push(1): inStack = [1], outStack = []
push(2): inStack = [1, 2], outStack = []

peek() : outStack is empty -> Transfer inStack to outStack:
         Pop 2 -> Push 2 to outStack.
         Pop 1 -> Push 1 to outStack.
         inStack = [], outStack = [1, 2] (Top of outStack is 1).
         Returns outStack.peek() = 1. ✅

pop()  : outStack is NOT empty -> Returns outStack.pop() = 1.
         inStack = [], outStack = [2]. ✅

empty(): inStack.isEmpty() && outStack.isEmpty() -> false. ✅ (O(1) Amortized Time!)
```

---

## 5. Visual Diagram
Dual Stack LIFO to FIFO Transformation Topology:

```
Step 1: inStack (Pushed 1, 2, 3)          Step 2: Transfer to outStack
          +-------+                                  +-------+
          |   3   | <--- Top                         |   1   | <--- Top (Front of Queue!)
          +-------+                                  +-------+
          |   2   |                                  |   2   |
          +-------+                                  +-------+
          |   1   |                                  |   3   |
          +-------+                                  +-------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Queue using Stacks (LeetCode 232) and Stack using Queues (LeetCode 225):

```java
import java.util.*;

public class QueueViaStacksMaster {

    // 1. Implement Queue using 2 Stacks (LeetCode 232) O(1) Amortized Time, O(N) Space
    public static class MyQueue {
        private Deque<Integer> inStack;
        private Deque<Integer> outStack;

        public MyQueue() {
            inStack = new ArrayDeque<>();
            outStack = new ArrayDeque<>();
        }

        // O(1) Push
        public void push(int x) {
            inStack.push(x);
        }

        // O(1) Amortized Pop
        public int pop() {
            transferIfNeeded();
            return outStack.pop();
        }

        // O(1) Amortized Peek
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

    // 2. Implement Stack using Single Queue (LeetCode 225) O(N) Push, O(1) Pop
    public static class MyStack {
        private Queue<Integer> queue;

        public MyStack() {
            queue = new ArrayDeque<>();
        }

        // O(N) Push (Rotates queue so newest element is at front)
        public void push(int x) {
            queue.offer(x);
            int size = queue.size();
            for (int i = 0; i < size - 1; i++) {
                queue.offer(queue.poll());
            }
        }

        // O(1) Pop
        public int pop() {
            return queue.poll();
        }

        // O(1) Top
        public int top() {
            return queue.peek();
        }

        public boolean empty() {
            return queue.isEmpty();
        }
    }
}
```

> **Quick Syntax:**
```java
// Transfer Invariant Method Line
private void transferIfNeeded() {
    if (outStack.isEmpty()) {
        while (!inStack.isEmpty()) outStack.push(inStack.pop());
    }
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 232 - Implement Queue using Stacks**: Dual-stack FIFO adaptation.
* **LeetCode 225 - Implement Stack using Queues**: Single-queue LIFO rotation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `MyQueue` and `MyStack`:

```java
public class QueueViaStacksDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. MyQueue Demonstration (LeetCode 232) ===");
        QueueViaStacksMaster.MyQueue queue = new QueueViaStacksMaster.MyQueue();
        queue.push(1);
        queue.push(2);
        System.out.println("Queue Peek: " + queue.peek()); // Output: 1
        System.out.println("Queue Pop:  " + queue.pop());  // Output: 1
        System.out.println("Is Empty?   " + queue.empty());// Output: false

        System.out.println("\n=== 2. MyStack Demonstration (LeetCode 225) ===");
        QueueViaStacksMaster.MyStack stack = new QueueViaStacksMaster.MyStack();
        stack.push(10);
        stack.push(20);
        System.out.println("Stack Top: " + stack.top());   // Output: 20
        System.out.println("Stack Pop: " + stack.pop());   // Output: 20
    }
}
```

---

## 9. Complexity Analysis

| Implementation Variant | Operation | Amortized Time | Worst-Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **MyQueue (LeetCode 232)**| `push(x)` | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(N)$ Space |
| **MyQueue (LeetCode 232)**| `pop()` / `peek()` | **$O(1)$ Amortized ⚡**| $O(N)$ (On Transfer) | $O(N)$ Space |
| **MyStack (LeetCode 225)**| `push(x)` | $O(N)$ Linear | $O(N)$ Linear | $O(N)$ Space |
| **MyStack (LeetCode 225)**| `pop()` / `top()` | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(N)$ Space |

---

## 10. Edge Cases & Boundary Handling
* **Pop/Peek on Empty Structure**: Returns exception or `null` depending on standard contracts.
* **Interleaved Push and Pop Operations**: `outStack` preserves correct FIFO ordering until empty before triggering next transfer.

---

## 11. Common Mistakes & Anti-Patterns
* **Transferring Elements on Every Single `pop()` / `peek()` Call**:
  - Transferring from `inStack` to `outStack` and back to `inStack` on every operation degrades performance to $O(N)$ per operation!
  - **Transfer ONLY when `outStack.isEmpty()` and leave items in `outStack`**.
* **Rotating Full Queue Length in `MyStack.push()`**:
  - Rotating `queue.size()` times leaves the element at the rear instead of front.
  - **Rotate exactly `queue.size() - 1` times**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Amortized $O(1)$ Proof for Queue via 2 Stacks:
> For any sequence of $N$ pushes and $N$ pops:
> 1. Each element is pushed onto `inStack` once ($1$ op).
> 2. Each element is popped from `inStack` once ($1$ op).
> 3. Each element is pushed onto `outStack` once ($1$ op).
> 4. Each element is popped from `outStack` once ($1$ op).
> Total operations across $N$ elements = $4N$.
> Average time per operation = $4N / N = \mathbf{O(1)\text{ Amortized Time}}$!

> **Memory Trick:** **"Transfer inStack to outStack ONLY when outStack is empty! Yields O(1) Amortized Time!"**

---

## 13. System & Implementation Comparisons

| Feature | Dual-Stack Queue (`MyQueue`) | Single Queue Stack (`MyStack`) |
| :--- | :--- | :--- |
| **Push Complexity** | **$O(1)$ Constant ⚡** | $O(N)$ Linear |
| **Pop Complexity** | **$O(1)$ Amortized ⚡** | **$O(1)$ Constant ⚡** |
| **Transfer Condition**| Lazy (On `outStack.isEmpty()`) | Eager (During `push`) |

---

## 14. How to Recognize This in Questions
* **"Implement a FIFO Queue using LIFO Stacks"** $\rightarrow$ LeetCode 232 (`inStack` and `outStack`).
* **"Implement a LIFO Stack using FIFO Queues"** $\rightarrow$ LeetCode 225 (Single queue rotation).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is transfer from `inStack` to `outStack` lazy?**  
  *A:* Lazy transfer ensures elements already in `outStack` are popped in correct FIFO order. Transferring only when `outStack` is empty guarantees that elements are moved at most once, maintaining $O(1)$ amortized time.
* **Q: Can a LIFO Stack be implemented with 2 FIFO Queues?**  
  *A:* Yes! Push into `q2`, transfer all elements from `q1` to `q2`, then swap `q1` and `q2` references.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE VIA STACKS & STACK VIA QUEUES                   |
+-----------------------------------------------------------------------+
| • MyQueue (232): Push to inStack; pop/peek from outStack              |
| • Transfer Rule: Move inStack to outStack ONLY when outStack.isEmpty()|
| • Amortized Proof: Each item moved at most once -> O(1) Amortized Time|
| • MyStack (225): Offer x, then rotate size-1 items behind x in Queue  |
| • Time Complexity: O(1) Amortized for MyQueue | O(N) Push for MyStack ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement MyQueue using 2 Stacks (LeetCode 232).
- [ ] I can prove why MyQueue runs in $O(1)$ amortized time.
- [ ] I can implement MyStack using a single Queue (LeetCode 225).
- [ ] I know why transfer from `inStack` to `outStack` must be lazy.
- [ ] I can explain the `transferIfNeeded()` invariant method.
