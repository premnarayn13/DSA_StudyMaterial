# 03. Queue Fundamentals, FIFO Mechanics & Task Scheduling Systems

## 1. Introduction
A **Queue** is a foundational linear data structure operating under the **FIFO (First-In, First-Out)** operational contract. Elements enter the queue at one end—the **Rear / Tail (`rear`)**—and exit the queue exclusively from the opposite end—the **Front / Head (`front`)**. Queues power operating system process schedulers, web server request processing, asynchronous messaging systems (RabbitMQ, Kafka), and **Breadth-First Search (BFS)** graph traversals in **$O(1)$ constant time**.

> **Important:** In contrast to a Stack (single-boundary LIFO access), a Queue maintains **Dual-Boundary Access**. Enqueue operations mutate the `rear` pointer, while dequeue operations mutate the `front` pointer.

```
FIFO Queue Operational Topology:
Enqueue (Insert at Rear) ---> | [ Val C ] | [ Val B ] | [ Val A ] | ---> Dequeue (Remove from Front)
                              +-----------------------------------+
                              ^                                   ^
                              Rear / Tail                         Front / Head
```

---

## 2. Core Concepts & FIFO Queue Taxonomy

### 2.1 The 4 Core Queue Operations
1. **`enqueue(E item)` / `offer(E item)`**: Inserts `item` at the rear of the queue. Returns `false` or throws exception if full. Time Complexity: **$O(1)$ Constant**.
2. **`dequeue()` / `poll()`**: Removes and returns the element at the front of the queue. Returns `null` if queue is empty. Time Complexity: **$O(1)$ Constant**.
3. **`peek()` / `element()`**: Returns the front element without removing it. Time Complexity: **$O(1)$ Constant**.
4. **`isEmpty()`**: Checks whether the queue contains 0 elements. Time Complexity: **$O(1)$ Constant**.

```
Queue Operational Method Contract (Java Queue API):
+-----------------------+-------------------+-------------------+-------------------+
| Operation Intent      | Throws Exception  | Returns Special   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| Insert at Rear        | `add(e)`          | `offer(e)`        | **$O(1)$ Constant**|
| Remove from Front     | `remove()`        | `poll()`          | **$O(1)$ Constant**|
| Examine Front         | `element()`       | `peek()`          | **$O(1)$ Constant**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"FIFO: First In, First Out! Enqueue at REAR, Dequeue at FRONT in O(1) time!"**

---

## 3. Characteristics & Computer System Applications

### 3.1 Systems & Algorithmic Applications
1. **Breadth-First Search (BFS)**: Uses a Queue to explore graph/tree nodes level-by-level in shortest path search algorithms.
2. **CPU Task Scheduling & Producer-Consumer Queues**: Operating systems queue processes in Ready Queues for time-sliced CPU allocation.
3. **Asynchronous Buffer Streaming**: Buffering audio/video data packets between network streams and media players.

```
Producer-Consumer Buffer Queue Architecture:
Producer Threads  ---> [ Enqueue (Offer) ] ---> [ SHARED FIFO QUEUE ] ---> [ Dequeue (Poll) ] ---> Consumer Threads
```

---

## 4. Internal Working Mechanics
Tracing FIFO Queue Enqueue and Dequeue Operations:

```
Init: Capacity = 4, front = 0, rear = 0, count = 0. Queue: [ _ , _ , _ , _ ]

Enqueue(10): Queue[rear(0)] = 10. rear = (0+1)%4 = 1. count = 1. Queue: [ 10 , _ , _ , _ ]
Enqueue(20): Queue[rear(1)] = 20. rear = (1+1)%4 = 2. count = 2. Queue: [ 10 , 20 , _ , _ ]
Enqueue(30): Queue[rear(2)] = 30. rear = (2+1)%4 = 3. count = 3. Queue: [ 10 , 20 , 30 , _ ]

Peek(): Returns Queue[front(0)] = 10. Queue unchanged.

Dequeue(): Returns Queue[front(0)] = 10. front = (0+1)%4 = 1. count = 2. Queue: [ _ , 20 , 30 , _ ]
Dequeue(): Returns Queue[front(1)] = 20. front = (1+1)%4 = 2. count = 1. Queue: [ _ , _ , 30 , _ ]

All operations completed in O(1) Constant Time! ✅
```

---

## 5. Visual Diagram
FIFO Queue Boundary Pointer Progression:

```
          Enqueue (40)                                   Dequeue ()
             |                                              |
             v                                              v
      +--------------+--------------+--------------+--------------+
      |  Val: 40     |  Val: 30     |  Val: 20     |  Val: 10     |
      +--------------+--------------+--------------+--------------+
      ^                                             ^
      Rear (Tail)                                   Front (Head)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a Fixed-Capacity Array Circular Queue (`ArrayQueue`):

```java
import java.util.NoSuchElementException;

public class ArrayQueueMaster<T> {

    private final Object[] array;
    private int front;
    private int rear;
    private int count;
    private final int capacity;

    public ArrayQueueMaster(int capacity) {
        this.capacity = capacity;
        this.array = new Object[capacity];
        this.front = 0;
        this.rear = 0;
        this.count = 0;
    }

    // O(1) Enqueue Operation (Offer)
    public boolean offer(T item) {
        if (isFull()) {
            return false; // Queue is full
        }
        array[rear] = item;
        rear = (rear + 1) % capacity; // Circular wrap
        count++;
        return true;
    }

    // O(1) Dequeue Operation (Poll)
    @SuppressWarnings("unchecked")
    public T poll() {
        if (isEmpty()) {
            return null;
        }
        T item = (T) array[front];
        array[front] = null; // Prevent memory leak
        front = (front + 1) % capacity; // Circular wrap
        count--;
        return item;
    }

    // O(1) Peek Operation
    @SuppressWarnings("unchecked")
    public T peek() {
        if (isEmpty()) {
            return null;
        }
        return (T) array[front];
    }

    public boolean isEmpty() {
        return count == 0;
    }

    public boolean isFull() {
        return count == capacity;
    }

    public int size() {
        return count;
    }
}
```

> **Quick Syntax:**
```java
// Standard Java Queue Usage (Prefer ArrayDeque over LinkedList!)
Queue<Integer> queue = new ArrayDeque<>();
queue.offer(10);  // Enqueue at rear
int val = queue.poll(); // Dequeue from front
int frontVal = queue.peek(); // Examine front
```

---

## 7. Concrete Problem Examples
* **Tree Level-Order Traversal (LeetCode 102)**: BFS queue level processing.
* **Rotting Oranges (LeetCode 994)**: Multi-source BFS grid traversal.
* **Task Scheduler (LeetCode 621)**: CPU cooldown queue management.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing custom `ArrayQueueMaster` and standard `ArrayDeque`:

```java
public class QueueFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Custom Array Circular Queue Demonstration ===");
        ArrayQueueMaster<String> printQueue = new ArrayQueueMaster<>(3);
        printQueue.offer("Doc1.pdf");
        printQueue.offer("Doc2.pdf");
        printQueue.offer("Doc3.pdf");

        System.out.println("Front Document (Peek): " + printQueue.peek()); // Doc1.pdf
        System.out.println("Printing (Poll): " + printQueue.poll());        // Doc1.pdf
        System.out.println("Next Document: " + printQueue.peek());          // Doc2.pdf

        System.out.println("\n=== 2. Production Java Queue (ArrayDeque) ===");
        Queue<Integer> bfsQueue = new ArrayDeque<>();
        bfsQueue.offer(1);
        bfsQueue.offer(2);
        System.out.println("BFS Dequeue: " + bfsQueue.poll()); // Output: 1
    }
}
```

---

## 9. Complexity Analysis

| Queue Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`offer(item)`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Index increment with modulo `(rear+1)%capacity` |
| **`poll()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Index increment with modulo `(front+1)%capacity` |
| **`peek()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Direct index lookup `array[front]` |

---

## 10. Edge Cases & Boundary Handling
* **Queue Underflow**: Calling `poll()` or `peek()` on an empty queue returns `null` or throws exception.
* **Queue Overflow**: Attempting `offer()` on a full fixed-capacity queue returns `false`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Naive Non-Circular Array Queue ($O(N)$ Dequeue Time)**:
  - Shifting array elements left by 1 position on every dequeue (`array[i] = array[i+1]`) results in an $O(N)$ dequeue operation!
  - **Use a Circular Array Queue (`front = (front + 1) % capacity`) for $O(1)$ time**.
* **Using `LinkedList` as a Standard Queue in High-Performance Java**:
  - `LinkedList` generates heap node objects for every enqueued item. Use `ArrayDeque`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Difference Between `add()`/`remove()` vs `offer()`/`poll()`:
> * **`add()` / `remove()`**: Throws unchecked exceptions (`IllegalStateException`, `NoSuchElementException`) on capacity bounds.
> * **`offer()` / `poll()`**: Returns special values (`false` / `null`) on capacity bounds.
> Always use `offer()` and `poll()` for robust error handling!

> **Memory Trick:** **"Use offer() and poll() for safe queue mutation without throwing exceptions!"**

---

## 13. System & Implementation Comparisons

| Feature | `offer()` / `poll()` API | `add()` / `remove()` API |
| :--- | :--- | :--- |
| **Full Queue Handling** | Returns `false` | Throws `IllegalStateException` |
| **Empty Queue Handling** | Returns `null` | Throws `NoSuchElementException` |
| **Code Safety** | High (Graceful null checking) | Requires try-catch blocks |

---

## 14. How to Recognize This in Questions
* **"Process items in exact order of arrival"** $\rightarrow$ FIFO Queue.
* **"Traverse tree/graph level-by-level (BFS)"** $\rightarrow$ FIFO Queue.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Naive Array Queue have $O(N)$ dequeue time, while a Circular Array Queue has $O(1)$ dequeue time?**  
  *A:* A naive array queue leaves `front` fixed at index 0 and shifts all remaining $N-1$ elements left on every dequeue ($O(N)$ time). A circular array queue advances the `front` index using modulo arithmetic `(front + 1) % capacity`, achieving $O(1)$ constant time.
* **Q: Why is `ArrayDeque` preferred over `LinkedList` for Queue implementation in Java?**  
  *A:* `ArrayDeque` uses a contiguous resizing circular array with superior CPU cache locality and zero node object overhead, outperforming pointer-based `LinkedList`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE FUNDAMENTALS & FIFO MECHANICS                   |
+-----------------------------------------------------------------------+
| • FIFO Principle: First-In, First-Out                                 |
| • Dual Boundary Access: Enqueue at REAR, Dequeue from FRONT           |
| • Circular Array Index Formula: idx = (idx + 1) % capacity            |
| • Preferred Method API: offer() and poll() (returns false / null)     |
| • Preferred Java Class: Queue<T> queue = new ArrayDeque<>()           |
| • System Role: Powers BFS, Task Scheduling, and Message Streams       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a custom Circular Array Queue from scratch.
- [ ] I know the difference between `offer()`/`poll()` and `add()`/`remove()`.
- [ ] I know why circular modulo indexing achieves $O(1)$ dequeue time.
- [ ] I can explain FIFO mechanics and BFS queue applications.
- [ ] I know why `ArrayDeque` is faster than `LinkedList` for queues.
