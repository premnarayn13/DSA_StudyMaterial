# 04. Queue Implementations, Ring Buffers & Dynamic Circular Array Resizing

## 1. Introduction
Implementing a Queue requires balancing **Memory Contiguity**, **Circular Index Wrapping**, and **Dynamic Capacity Resizing**. The two primary structural approaches are **Array Ring Buffers (`CircularArrayQueue`)** and **Linked List Queues (`LinkedListQueue`)**. Understanding how ring buffers manipulate `front` and `rear` pointers using bitwise or modulo mask arithmetic enables building high-throughput low-latency systems (such as LMAX Disruptor and IPC Ring Buffers) in **$O(1)$ constant time**.

> **Important:** In an **Array Circular Ring Buffer**, distinguishing between an **EMPTY Queue** and a **FULL Queue** requires either:
> 1. Maintaining an explicit `count` variable.
> 2. Leaving 1 empty array slot as a sentinel (`(rear + 1) % capacity == front`).
> 3. Enforcing power-of-2 array capacities and using bitwise masking (`idx & (capacity - 1)`).

```
Circular Array Ring Buffer Topology:
[ Val 30 ] | [ Val 40 ] | [  _   ] | [ Val 10 ] | [ Val 20 ]
   idx 0       idx 1       idx 2       idx 3       idx 4
                             ^           ^
                           Rear        Front
(Elements wrap around array boundaries seamlessly!) ⚡
```

---

## 2. Core Concepts & Architectural Implementations

### 2.1 Circular Array Ring Buffer (`CircularArrayQueue`)
* Uses a fixed or dynamically resizing array.
* Advances `rear = (rear + 1) % capacity` on enqueue and `front = (front + 1) % capacity` on dequeue.
* **Pros**: Superior L1/L2 cache line locality, zero pointer memory overhead.
* **Cons**: Resizing requires copying elements from ring buffer layout into contiguous linear layout.

### 2.2 Linked List Queue (`LinkedListQueue`)
* Maintains `head` (front) and `tail` (rear) pointers across dynamic Node objects.
* Enqueue appends to `tail.next`, Dequeue advances `head = head.next`.
* **Pros**: Infinite dynamic growth without resize latency spikes.
* **Cons**: Poor cache locality, high memory footprint (24B per node object).

```
Architectural Comparison Matrix:
+-----------------------+-------------------+-------------------+
| Feature Metrics       | Circular Array    | Linked List Queue |
+-----------------------+-------------------+-------------------+
| Cache Line Locality   | **Excellent ⚡**  | Poor              |
| Memory Overhead/Elem  | **0 Bytes Extra** | ~24 Bytes / Node  |
| Enqueue Time          | **$O(1)$ Amortized**| **$O(1)$ Constant**|
| Dequeue Time          | **$O(1)$ Constant**| **$O(1)$ Constant**|
| Resizing Mechanics    | Ring Unwrapping   | No Resize Needed  |
+-----------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Ring Buffer: Resizing requires unwrapping circular elements into contiguous layout!"**

---

## 3. Characteristics & Power-of-2 Bitwise Masking Optimization

### 3.1 Power-of-2 Masking (`idx & (capacity - 1)`)
In high-performance ring buffers (e.g. `ArrayDeque`, LMAX Disruptor):
* Array capacity $C$ is strictly constrained to a power of 2 ($C = 2^k$, e.g. 16, 32, 64, 1024).
* Modulo division `(idx + 1) % C` is replaced by bitwise AND masking: **`(idx + 1) & (capacity - 1)`**.
* **Performance Gain**: Bitwise AND executes in 1 CPU clock cycle, compared to 15–30 CPU cycles for integer modulo division (`%`)!

```
Modulo (%) vs Bitwise AND (&) Masking (Capacity = 16, Mask = 15):
(15 + 1) % 16 = 0  (Requires slow integer division instruction)
(15 + 1) & 15 = 16 & 15 = 00010000 & 00001111 = 00000000 = 0 ⚡ (1 CPU Cycle!)
```

---

## 4. Internal Working Mechanics
Tracing Dynamic Resizing in a Circular Array Queue:

```
Full Queue (Capacity 4): front = 2, rear = 2, count = 4
Array: [ 30 , 40 , 10 , 20 ]
         idx0 idx1 idx2 idx3 (front=2, rear=2)

Resize Action to Capacity 8:
Unwrap items from front to rear into new linear array:
New Array: [ 10 , 20 , 30 , 40 ,  _  ,  _  ,  _  ,  _  ]
             idx0 idx1 idx2 idx3
Reset pointers: front = 0, rear = 4, count = 4.

Queue successfully resized with correct LIFO/FIFO ordering intact! ✅
```

---

## 5. Visual Diagram
Circular Array Unwrapping during Dynamic Resizing:

```
Old Ring Buffer:  [ C | D | A | B ]  (front = 2 "A", rear = 2)
                    0   1   2   3

New Resized Array: [ A | B | C | D | _ | _ | _ | _ ]  (front = 0, rear = 4)
                     0   1   2   3   4   5   6   7
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementations of a Resizing Circular Array Queue (`ResizingArrayQueue`) and a Linked List Queue (`LinkedListQueue`):

```java
import java.util.NoSuchElementException;

public class QueueImplementationsMaster {

    // 1. Linked List Queue Implementation O(1) Enqueue/Dequeue Guaranteed
    public static class LinkedListQueue<T> {
        private static class Node<T> {
            T data;
            Node<T> next;

            Node(T data) {
                this.data = data;
                this.next = null;
            }
        }

        private Node<T> head; // Front of queue
        private Node<T> tail; // Rear of queue
        private int size;

        public LinkedListQueue() {
            this.head = null;
            this.tail = null;
            this.size = 0;
        }

        // Guaranteed O(1) Enqueue at Tail
        public void offer(T item) {
            Node<T> newNode = new Node<>(item);
            if (isEmpty()) {
                head = newNode;
                tail = newNode;
            } else {
                tail.next = newNode;
                tail = newNode;
            }
            size++;
        }

        // Guaranteed O(1) Dequeue at Head
        public T poll() {
            if (isEmpty()) return null;
            T data = head.data;
            head = head.next;
            if (head == null) {
                tail = null; // Queue is now empty
            }
            size--;
            return data;
        }

        public T peek() {
            return isEmpty() ? null : head.data;
        }

        public boolean isEmpty() { return size == 0; }
        public int size() { return size; }
    }

    // 2. Resizing Circular Array Queue Implementation (Power of 2 Capacity Bitwise Masking)
    public static class ResizingArrayQueue<T> {
        private Object[] elements;
        private int front;
        private int rear;
        private int count;

        public ResizingArrayQueue(int initialCapacity) {
            int cap = getPowerOfTwoCapacity(initialCapacity);
            elements = new Object[cap];
            front = 0;
            rear = 0;
            count = 0;
        }

        public void offer(T item) {
            if (count == elements.length) {
                resize(elements.length * 2);
            }
            elements[rear] = item;
            rear = (rear + 1) & (elements.length - 1); // Bitwise Masking
            count++;
        }

        @SuppressWarnings("unchecked")
        public T poll() {
            if (isEmpty()) return null;
            T item = (T) elements[front];
            elements[front] = null; // Prevent memory leak
            front = (front + 1) & (elements.length - 1); // Bitwise Masking
            count--;

            if (count > 0 && count == elements.length / 4 && elements.length > 16) {
                resize(elements.length / 2);
            }
            return item;
        }

        @SuppressWarnings("unchecked")
        public T peek() {
            return isEmpty() ? null : (T) elements[front];
        }

        public boolean isEmpty() { return count == 0; }
        public int size() { return count; }

        private void resize(int newCapacity) {
            Object[] copy = new Object[newCapacity];
            // Unwrap circular array items into linear contiguous layout
            for (int i = 0; i < count; i++) {
                copy[i] = elements[(front + i) & (elements.length - 1)];
            }
            elements = copy;
            front = 0;
            rear = count;
        }

        private int getPowerOfTwoCapacity(int cap) {
            int n = cap - 1;
            n |= n >>> 1; n |= n >>> 2; n |= n >>> 4; n |= n >>> 8; n |= n >>> 16;
            return (n < 0) ? 1 : n + 1;
        }
    }
}
```

> **Quick Syntax:**
```java
// Resizing Circular Array Unwrapping Loop Syntax
for (int i = 0; i < count; i++) {
    copy[i] = elements[(front + i) % elements.length];
}
```

---

## 7. Concrete Problem Examples
* **LMAX Disruptor & High-Frequency Trading Ring Buffers**: Power-of-2 bitwise masking circular queues.
* **IPC Shared Memory Messaging Channels**: Single-producer single-consumer ring buffers.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `LinkedListQueue` and `ResizingArrayQueue`:

```java
public class QueueImplementationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Linked List Queue Demonstration ===");
        QueueImplementationsMaster.LinkedListQueue<String> llQueue = new QueueImplementationsMaster.LinkedListQueue<>();
        llQueue.offer("Task1");
        llQueue.offer("Task2");
        System.out.println("Front Task: " + llQueue.peek()); // Task1
        System.out.println("Processed: " + llQueue.poll());  // Task1

        System.out.println("\n=== 2. Resizing Circular Array Queue (Bitwise Masking) ===");
        QueueImplementationsMaster.ResizingArrayQueue<Integer> ringQueue = new QueueImplementationsMaster.ResizingArrayQueue<>(4);
        ringQueue.offer(10);
        ringQueue.offer(20);
        ringQueue.offer(30);
        ringQueue.offer(40);
        ringQueue.offer(50); // Triggers circular unwrapping resize!

        System.out.println("Front Element: " + ringQueue.peek()); // 10
        System.out.println("Polled Element: " + ringQueue.poll()); // 10
    }
}
```

---

## 9. Complexity Analysis

| Queue Implementation | Enqueue Time | Dequeue Time | Bitwise Masking Gain | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Resizing Circular Array**| **$O(1)$ Amortized ⚡** | **$O(1)$ Constant ⚡** | **`idx & (cap - 1)` (1 Cycle)** | **$O(N)$ Contiguous** |
| **Linked List Queue** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | N/A (Modulo not used) | **$O(N)$ Heap Nodes** |

---

## 10. Edge Cases & Boundary Handling
* **Unwrapping Circular Elements During Resize**: Failing to copy elements relative to `front` (`(front + i) % length`) corrupts FIFO order during resize.
* **Power of 2 Capacity Bitwise Masking**: Works ONLY if capacity is strictly a power of 2 ($2, 4, 8, 16 \dots$).

---

## 11. Common Mistakes & Anti-Patterns
* **Using Naive `System.arraycopy` Directly During Circular Array Resize**:
  - `System.arraycopy(elements, 0, copy, 0, length)` fails when items wrap around the end of the circular array!
  - **Unwrap items sequentially from `front` to `front + count` into index `0 ... count-1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Correct Circular Array Resizing Unwrapping Rule:
> You CANNOT copy a circular ring buffer with a single `System.arraycopy`!
> You MUST copy in 2 steps:
> 1. Copy `elements[front ... capacity-1]` to `copy[0 ... len1-1]`.
> 2. Copy `elements[0 ... rear-1]` to `copy[len1 ... count-1]`.
> Or use a single loop: `copy[i] = elements[(front + i) & (capacity - 1)]`.

> **Memory Trick:** **"Circular Array Resize requires 2-segment copy or (front + i) unwrapping loop!"**

---

## 13. System & Implementation Comparisons

| Feature | Bitwise Masking Ring Buffer | Modulo (`%`) Ring Buffer |
| :--- | :--- | :--- |
| **CPU Clock Cycles** | **1 CPU Cycle (`&`) ⚡** | 15–30 CPU Cycles (`%`) |
| **Capacity Constraint** | Must be Power of 2 | Any Integer Capacity |
| **Latency Consistency** | Ultra-Low Latency | Moderate Latency |

---

## 14. How to Recognize This in Questions
* **"Implement high-throughput circular buffer for real-time streaming"** $\rightarrow$ Power-of-2 Bitwise Masking Ring Buffer.
* **"Design a circular queue with dynamic resizing"** $\rightarrow$ Resizing Circular Array Queue.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does bitwise masking `(idx + 1) & (capacity - 1)` work only for power-of-2 capacities?**  
  *A:* For power-of-2 values $2^k$, `capacity - 1` has a bit binary pattern of all 1s in lower bits (e.g. $16 - 1 = 15 = \text{00001111}_2$). Bitwise AND with 15 acts as a zero-cost truncation modulo operation.
* **Q: How does `ArrayDeque` resize its underlying circular array in Java?**  
  *A:* When `head == tail`, `ArrayDeque` doubles capacity, calls `System.arraycopy` to copy `elements[head ... N-1]` to index 0, and copies `elements[0 ... head-1]` to index $N - \text{head}$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE IMPLEMENTATIONS & RING BUFFERS                  |
+-----------------------------------------------------------------------+
| • Circular Array Rule: rear = (rear + 1) % cap; front = (front + 1) % cap|
| • Bitwise Masking Optimization: (idx + 1) & (capacity - 1) for 2^k cap|
| • Unwrapping Resizing: Copy items from front to count into copy[0..count-1]|
| • Linked List Queue: Maintains head (front) and tail (rear) references|
| • CPU Performance: Array Ring Buffer outperforms LinkedList by 3x     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a Resizing Circular Array Queue with bitwise masking.
- [ ] I know how to correctly unwrap a circular array during resizing.
- [ ] I can write a Linked List Queue with head and tail pointers.
- [ ] I know why bitwise AND masking is faster than integer modulo (`%`).
- [ ] I know why `ArrayDeque` doubles capacity using power of 2.
