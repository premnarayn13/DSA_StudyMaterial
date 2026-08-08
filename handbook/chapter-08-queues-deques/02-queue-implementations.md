# 02. Queue Implementations (Circular Array & Linked List)

## 1. Introduction
Implementing a Queue from scratch using a **Circular Array** or a **Singly Linked List** is a fundamental technical interview design problem (LeetCode 622 - Design Circular Queue). Naive array queue implementations suffer from $O(N)$ front element shifting penalties or memory drift. The **Circular Array Ring Buffer** technique overcomes this by using modulo arithmetic (`(tail + 1) % capacity`) to wrap around array boundaries in **Strict $O(1)$ constant time**.

> **Important:** In a fixed-size Circular Queue, distinguishing between an **Empty Queue** and a **Full Queue** requires either maintaining an explicit `count` variable, or allocating an extra sentinel slot (`(tail + 1) % capacity == head`). Using a `count` variable is cleaner and error-free!

## 2. Core Concepts
* **Modulo Arithmetic Wrapping**:
  * **Enqueue (Rear)**: `rear = (rear + 1) % capacity; data[rear] = val;`
  * **Dequeue (Front)**: `front = (front + 1) % capacity;`
* **Linked List Queue**: Maintains `head` (for dequeue $O(1)$) and `tail` (for enqueue $O(1)$) pointers.
* **Design Circular Queue (LeetCode 622)**: Fixed-size ring buffer queue supporting `enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, and `isFull` in $O(1)$ time per operation.

> **Memory Trick:** **"Circular Queue Enqueue: rear = (rear + 1) % capacity; Dequeue: front = (front + 1) % capacity"**.

## 3. Characteristics / Properties
* **Circular Array vs Linked List Queue**:

```
Queue Implementation Trade-Offs Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric                | Circular Array    | Linked List Queue | Winner / Choice   |
+-----------------------+-------------------+-------------------+-------------------+
| Enqueue / Dequeue Time| Strict O(1) ⚡    | Strict O(1) ⚡    | Tie               |
| Memory Allocations    | 1 Array Allocation| Node per Enqueue  | Circular Array ⚡ |
| Cache Locality        | High L1 Hits ⚡   | High Cache Misses | Circular Array ⚡ |
| Bounded Capacity      | Fixed Capacity    | Unbounded Dynamic | Linked List       |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Circular Queue ($k=3$) on `enQueue(10), enQueue(20), enQueue(30), deQueue(), enQueue(40)`:

```
Init: capacity = 3, front = 0, rear = -1, count = 0, data = [0, 0, 0]

enQueue(10): rear = (0) % 3 = 0, data[0] = 10, count = 1 | arr: [10, 0, 0]
enQueue(20): rear = (1) % 3 = 1, data[1] = 20, count = 2 | arr: [10, 20, 0]
enQueue(30): rear = (2) % 3 = 2, data[2] = 30, count = 3 (FULL!) | arr: [10, 20, 30]

deQueue():   front = (0 + 1) % 3 = 1, count = 2 | Front is now at index 1 (val 20)
enQueue(40): rear = (2 + 1) % 3 = 0 (WRAPS TO INDEX 0!), data[0] = 40, count = 3 | arr: [40, 20, 30] ✅
```

## 5. Visual Diagram
Circular Array Modulo Wrapping Architecture:

```
Index:    [ 0 ]   [ 1 ]   [ 2 ]   [ 3 ]
Data:     [ 40 ]  [ 20 ]  [ 30 ]  [ -- ]
            ^       ^       ^
           Rear   Front   (Count = 3, Capacity = 4)
           
Notice: Rear wrapped back to index 0 via (2 + 1) % 4 = 0!
```

## 6. Operations / Algorithms
LeetCode 622 Design Circular Queue Implementation:

```java
public class MyCircularQueue {
    private final int[] data;
    private int head;
    private int count;
    private final int capacity;

    public MyCircularQueue(int k) {
        this.capacity = k;
        this.data = new int[k];
        this.head = 0;
        this.count = 0;
    }

    public boolean enQueue(int value) {
        if (isFull()) return false;
        int tail = (head + count) % capacity;
        data[tail] = value;
        count++;
        return true;
    }

    public boolean deQueue() {
        if (isEmpty()) return false;
        head = (head + 1) % capacity;
        count--;
        return true;
    }

    public int Front() {
        return isEmpty() ? -1 : data[head];
    }

    public int Rear() {
        if (isEmpty()) return -1;
        int tail = (head + count - 1) % capacity;
        return data[tail];
    }

    public boolean isEmpty() { return count == 0; }
    public boolean isFull()  { return count == capacity; }
}
```

> **Quick Syntax:**
```java
// Tail Calculation using Head and Count
int tail = (head + count) % capacity;
```

## 7. Examples
* **LeetCode 622 - Design Circular Queue**: Fixed capacity ring buffer queue.
* **LeetCode 641 - Design Circular Deque**: Double-ended circular queue.
* **Custom Linked List Queue**: Head/Tail pointer queue design.

## 8. Java Code
Complete interview-ready Java suite implementing Custom Linked List Queue and Design Circular Queue (LeetCode 622):

```java
public class QueueImplementationsMaster {

    // 1. Custom Singly Linked List Queue (Unbounded) O(1) All Operations
    public static class LinkedListQueue {
        private static class Node {
            int val;
            Node next;
            Node(int val) { this.val = val; }
        }

        private Node head = null; // Dequeue from Head
        private Node tail = null; // Enqueue at Tail
        private int size = 0;

        public void offer(int val) {
            Node newNode = new Node(val);
            if (isEmpty()) {
                head = tail = newNode;
            } else {
                tail.next = newNode;
                tail = newNode;
            }
            size++;
        }

        public int poll() {
            if (isEmpty()) throw new IllegalStateException("Queue Underflow");
            int val = head.val;
            head = head.next;
            if (head == null) tail = null; // Queue became empty
            size--;
            return val;
        }

        public int peek() {
            if (isEmpty()) throw new IllegalStateException("Queue Underflow");
            return head.val;
        }

        public boolean isEmpty() { return head == null; }
        public int size() { return size; }
    }

    // 2. LeetCode 622: Design Circular Queue (Bounded Ring Buffer) O(1) All Operations
    public static class MyCircularQueue {
        private final int[] data;
        private int head;
        private int count;
        private final int capacity;

        public MyCircularQueue(int k) {
            this.capacity = k;
            this.data = new int[k];
            this.head = 0;
            this.count = 0;
        }

        public boolean enQueue(int value) {
            if (isFull()) return false;
            int tail = (head + count) % capacity;
            data[tail] = value;
            count++;
            return true;
        }

        public boolean deQueue() {
            if (isEmpty()) return false;
            head = (head + 1) % capacity;
            count--;
            return true;
        }

        public int Front() {
            return isEmpty() ? -1 : data[head];
        }

        public int Rear() {
            if (isEmpty()) return -1;
            int tail = (head + count - 1) % capacity;
            return data[tail];
        }

        public boolean isEmpty() { return count == 0; }
        public boolean isFull()  { return count == capacity; }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        MyCircularQueue circularQueue = new MyCircularQueue(3);
        System.out.println("enQueue 1: " + circularQueue.enQueue(1)); // true
        System.out.println("enQueue 2: " + circularQueue.enQueue(2)); // true
        System.out.println("enQueue 3: " + circularQueue.enQueue(3)); // true
        System.out.println("enQueue 4: " + circularQueue.enQueue(4)); // false (Full!)
        System.out.println("Rear:      " + circularQueue.Rear());     // 3
        System.out.println("deQueue:   " + circularQueue.deQueue());  // true
        System.out.println("enQueue 4: " + circularQueue.enQueue(4)); // true
        System.out.println("Rear:      " + circularQueue.Rear());     // 4
    }
}
```

## 9. Complexity Analysis
| Queue Implementation | Enqueue Time | Dequeue Time | Peek Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Circular Array Queue** | **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| $O(K)$ Fixed Array |
| **Linked List Queue** | **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| $O(N)$ Heap Nodes |
| **Naive Array Shift** | $O(1)$ | $O(N)$ (Shifting) | $O(1)$ | $O(N)$ Space |

## 10. Edge Cases
* **Enqueue on Full Queue**: `enQueue` returns `false` without overwriting un-dequeued elements.
* **Dequeue on Empty Queue**: `deQueue` returns `false` and `Front()` / `Rear()` return `-1`.
* **Single Element Circular Queue ($k=1$)**: `head` and `tail` align at index 0.

## 11. Common Mistakes
* Implementing an array queue without modulo arithmetic (forces $O(N)$ front element shifting on dequeue!).
* In Linked List Queue `poll()`, forgetting to set `tail = null` when `head` becomes `null` after dequeuing the last node.
* Calculating `Rear()` as `data[head + count]` without modulo wrapping `(head + count - 1) % capacity`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `Rear()` Index Calculation Formula:
> Correct Rear Index: **`(head + count - 1) % capacity`**
> (Note the `-1` offset to point to the last inserted element!).

> **Memory Trick:** **"Rear Index = (head + count - 1) % capacity"**

## 13. Comparisons
| Feature | Naive Array Queue | Circular Ring Buffer Queue |
| :--- | :--- | :--- |
| **Dequeue Time Complexity**| $O(N)$ Array Shifting | **Strict $O(1)$ Modulo Offset ⚡** |
| **Memory Reuse** | No (Drifts to array end) | **100% Memory Reuse (Wraps around)** |
| **Interview Recommendation** | AVOID | **MANDATORY PREFERRED** |

## 14. How to Recognize This in Questions
* **"Design a circular queue / ring buffer with O(1) operations"** $\rightarrow$ LeetCode 622.
* **"Implement bounded Queue without dynamic memory allocations"** $\rightarrow$ Circular Array Queue.

## 15. Frequently Asked Interview Questions
* **Q: Why does a Circular Queue maintain a `count` variable?**  
  *A:* Maintaining a `count` variable makes `isEmpty()` (`count == 0`) and `isFull()` (`count == capacity`) trivial $O(1)$ checks, eliminating ambiguity between full and empty queue states.
* **Q: Why is a Circular Array Queue preferred over a Linked List Queue in low-latency systems?**  
  *A:* A Circular Array allocates memory in a single contiguous block at initialization, providing near 100% CPU L1/L2 cache hits and zero runtime Garbage Collection pauses.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE IMPLEMENTATIONS & CIRCULAR RING BUFFERS         |
+-----------------------------------------------------------------------+
| • Circular Queue State: data[capacity], head, count                   |
| • Tail Formula: tail = (head + count) % capacity                      |
| • Rear Index: (head + count - 1) % capacity                           |
| • Dequeue Step: head = (head + 1) % capacity; count--;                |
| • Linked List Queue: Enqueue at TAIL, Dequeue from HEAD               |
| • Complexity: All core ops execute in Strict O(1) Constant Time       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the `(head + count) % capacity` tail index formula.
- [ ] I can write the `(head + count - 1) % capacity` Rear index formula.
- [ ] I can implement Design Circular Queue (LeetCode 622) in under 5 minutes.
- [ ] I can implement a Linked List Queue maintaining `head` and `tail` pointers.
- [ ] I know why Circular Arrays are preferred in low-latency systems.
