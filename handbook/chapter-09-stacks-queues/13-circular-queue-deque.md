# 13. Circular Queue & Double-Ended Queue (Deque) Architecture, Ring Wraparounds & Sentinel Invariants

## 1. Introduction
A **Double-Ended Queue (Deque)** extends standard FIFO Queue functionality by permitting insertions and deletions at BOTH boundaries—the **Front (`front`)** and the **Rear (`rear`)**. When combined with a circular array topology, **Design Circular Queue (LeetCode 622)** and **Design Circular Deque (LeetCode 641)** achieve **$O(1)$ constant time operations across all four access points** (`insertFront`, `insertLast`, `deleteFront`, `deleteLast`) with zero memory reallocation overhead.

> **Important:** In **Design Circular Deque (LeetCode 641)**, moving the `front` pointer backward during `insertFront()` requires circular array wrapping:
> $$\text{front} = (\text{front} - 1 + K) \bmod K$$
> Adding $K$ before modulo prevents negative index values in Java arithmetic!

```
Circular Deque Operational Access Point Topology:
insertFront() / deleteFront() ---> | [ Front ] | [ Element B ] | [ Rear ] | <--- insertLast() / deleteLast()
                                   +------------------------------------+
                                   ^                                    ^
                                 Index 0                             Index K-1
```

---

## 2. Core Concepts & Circular Deque Array Wraparound Mechanics (LeetCode 641)

### 2.1 Design Circular Deque (LeetCode 641)
Design a circular double-ended queue supporting 8 core operational methods:

#### Pointer Wraparound Equations (Capacity $K$):
1. **`insertFront(value)`**:
   - Check if full (`count == K`). If full, return `false`.
   - Update `front = (front - 1 + K) % K`.
   - Assign `elements[front] = value`.
   - Increment `count++`. Return `true`.
2. **`insertLast(value)`**:
   - Check if full (`count == K`). If full, return `false`.
   - Assign `elements[rear] = value`.
   - Update `rear = (rear + 1) % K`.
   - Increment `count++`. Return `true`.
3. **`deleteFront()`**:
   - Check if empty (`count == 0`). If empty, return `false`.
   - `elements[front] = null`.
   - Update `front = (front + 1) % K`.
   - Decrement `count--`. Return `true`.
4. **`deleteLast()`**:
   - Check if empty (`count == 0`). If empty, return `false`.
   - Update `rear = (rear - 1 + K) % K`.
   - `elements[rear] = null`.
   - Decrement `count--`. Return `true`.

```
Circular Deque Pointer Movement Rules:
- Front Moves Backward on InsertFront : (front - 1 + K) % K
- Front Moves Forward  on DeleteFront : (front + 1) % K
- Rear  Moves Forward  on InsertLast  : (rear + 1) % K
- Rear  Moves Backward on DeleteLast  : (rear - 1 + K) % K
Note: Added +K before modulo to handle negative indices safely! ⚡
```

> **Memory Trick:** **"Front Insert moves BACKWARD ((front - 1 + K) % K)! Rear Delete moves BACKWARD ((rear - 1 + K) % K)!"**

---

## 3. Characteristics & Design Circular Queue (LeetCode 622)

### 3.1 Design Circular Queue (LeetCode 622)
Design a FIFO circular queue supporting `enQueue(value)`, `deQueue()`, `Front()`, `Rear()`, `isEmpty()`, `isFull()`:
* **`Rear()` Calculation**: When `rear` points to the next available write slot, the current rear element resides at **`elements[(rear - 1 + K) % K]`**!

```java
public int Rear() {
    if (isEmpty()) return -1;
    return elements[(rear - 1 + capacity) % capacity];
}
```

---

## 4. Internal Working Mechanics
Tracing Design Circular Deque (LeetCode 641) on capacity $K = 3$:

```
Init: capacity = 3, front = 0, rear = 0, count = 0. Array: [ _, _, _ ]

insertLast(1)  : arr[rear(0)] = 1. rear = (0+1)%3 = 1. count = 1. Array: [ 1, _, _ ]
insertLast(2)  : arr[rear(1)] = 2. rear = (1+1)%3 = 2. count = 2. Array: [ 1, 2, _ ]
insertFront(3) : front = (0-1+3)%3 = 2. arr[2] = 3. count = 3 (FULL!). Array: [ 1, 2, 3 ]
                 Pointers: front = 2 (val 3), rear = 2 (write slot)

getFront()     : Returns arr[front(2)] = 3. ✅
getRear()      : Returns arr[(rear-1+3)%3 = 1] = 2. ✅
isFull()       : count == 3 -> true. ✅

deleteLast()   : rear = (2-1+3)%3 = 1. arr[1] = null. count = 2. Array: [ 1, _, 3 ]
insertFront(4) : front = (2-1+3)%3 = 1. arr[1] = 4. count = 3. Array: [ 1, 4, 3 ]

All operations execute in O(1) Constant Time! ✅
```

---

## 5. Visual Diagram
Circular Deque Front & Rear Access Point Topography:

```
Array (Capacity 3): [ 1 (idx 0) | 4 (idx 1) | 3 (idx 2) ]
                                    ^           ^
                                  front       rear (Wrap point)
getFront() -> arr[front] = 4
getRear()  -> arr[(rear - 1 + K) % K] = 1
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Design Circular Queue (LeetCode 622) and Design Circular Deque (LeetCode 641):

```java
import java.util.*;

public class CircularQueueDequeMaster {

    // 1. Design Circular Deque (LeetCode 641) O(1) Operations Across All 4 Boundaries
    public static class MyCircularDeque {
        private final int[] elements;
        private int front;
        private int rear;
        private int count;
        private final int capacity;

        public MyCircularDeque(int k) {
            this.capacity = k;
            this.elements = new int[k];
            this.front = 0;
            this.rear = 0;
            this.count = 0;
        }

        public boolean insertFront(int value) {
            if (isFull()) return false;
            front = (front - 1 + capacity) % capacity;
            elements[front] = value;
            count++;
            return true;
        }

        public boolean insertLast(int value) {
            if (isFull()) return false;
            elements[rear] = value;
            rear = (rear + 1) % capacity;
            count++;
            return true;
        }

        public boolean deleteFront() {
            if (isEmpty()) return false;
            front = (front + 1) % capacity;
            count--;
            return true;
        }

        public boolean deleteLast() {
            if (isEmpty()) return false;
            rear = (rear - 1 + capacity) % capacity;
            count--;
            return true;
        }

        public int getFront() {
            if (isEmpty()) return -1;
            return elements[front];
        }

        public int getRear() {
            if (isEmpty()) return -1;
            return elements[(rear - 1 + capacity) % capacity];
        }

        public boolean isEmpty() { return count == 0; }
        public boolean isFull() { return count == capacity; }
    }

    // 2. Design Circular Queue (LeetCode 622) O(1) Constant Time Operations
    public static class MyCircularQueue {
        private final int[] elements;
        private int front;
        private int rear;
        private int count;
        private final int capacity;

        public MyCircularQueue(int k) {
            this.capacity = k;
            this.elements = new int[k];
            this.front = 0;
            this.rear = 0;
            this.count = 0;
        }

        public boolean enQueue(int value) {
            if (isFull()) return false;
            elements[rear] = value;
            rear = (rear + 1) % capacity;
            count++;
            return true;
        }

        public boolean deQueue() {
            if (isEmpty()) return false;
            front = (front + 1) % capacity;
            count--;
            return true;
        }

        public int Front() {
            if (isEmpty()) return -1;
            return elements[front];
        }

        public int Rear() {
            if (isEmpty()) return -1;
            return elements[(rear - 1 + capacity) % capacity];
        }

        public boolean isEmpty() { return count == 0; }
        public boolean isFull() { return count == capacity; }
    }
}
```

> **Quick Syntax:**
```java
// Safe Negative Modulo Wraparound Formulas
front = (front - 1 + capacity) % capacity; // Backward front movement
rear  = (rear - 1 + capacity) % capacity;  // Backward rear movement
```

---

## 7. Concrete Problem Examples
* **LeetCode 641 - Design Circular Deque**: 4-boundary circular array ops.
* **LeetCode 622 - Design Circular Queue**: Standard circular queue.
* **Sliding Window Maximum (LeetCode 239)**: Double-ended deque applications.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `MyCircularDeque` and `MyCircularQueue`:

```java
public class CircularQueueDequeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Design Circular Deque (LeetCode 641) ===");
        CircularQueueDequeMaster.MyCircularDeque deque = new CircularQueueDequeMaster.MyCircularDeque(3);
        System.out.println("Insert Last 1: " + deque.insertLast(1));  // true
        System.out.println("Insert Last 2: " + deque.insertLast(2));  // true
        System.out.println("Insert Front 3: " + deque.insertFront(3));// true
        System.out.println("Get Front: " + deque.getFront());        // 3
        System.out.println("Get Rear: "  + deque.getRear());         // 2
        System.out.println("Is Full? "   + deque.isFull());          // true

        System.out.println("\n=== 2. Design Circular Queue (LeetCode 622) ===");
        CircularQueueDequeMaster.MyCircularQueue queue = new CircularQueueDequeMaster.MyCircularQueue(3);
        queue.enQueue(10);
        queue.enQueue(20);
        System.out.println("Queue Front: " + queue.Front()); // 10
        System.out.println("Queue Rear:  " + queue.Rear());  // 20
    }
}
```

---

## 9. Complexity Analysis

| Deque / Queue Operation | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **`insertFront()` / `insertLast()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Modulo wraparound arithmetic |
| **`deleteFront()` / `deleteLast()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Pointer offset decrements |
| **`getFront()` / `getRear()`** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Direct index access |

---

## 10. Edge Cases & Boundary Handling
* **Negative Modulo Evaluation**: `(front - 1) % K` evaluates to `-1` in Java. `(front - 1 + K) % K` prevents negative array index bounds.
* **Empty / Full State Queries**: Verified via `count == 0` and `count == capacity`.

---

## 11. Common Mistakes & Anti-Patterns
* **Writing `front = (front - 1) % capacity` Without $+K$**:
  - In Java, `-1 % 3` evaluates to `-1`! Using negative indices throws `ArrayIndexOutOfBoundsException`.
  - **Always add `+ capacity` before modulo when moving backward (`(idx - 1 + capacity) % capacity`)**.
* **Returning `elements[rear]` for `getRear()`**:
  - `rear` points to the NEXT AVAILABLE WRITE SLOT, not the current element.
  - **Access `elements[(rear - 1 + capacity) % capacity]`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Correct Java Circular Index Arithmetic Rules:
> * **Moving Forward**: `(idx + 1) % capacity`
> * **Moving Backward**: `(idx - 1 + capacity) % capacity`
> * **Reading Last Enqueued Item**: `elements[(rear - 1 + capacity) % capacity]`

> **Memory Trick:** **"Always add +capacity before modulo when decrementing indices in Java!"**

---

## 13. System & Implementation Comparisons

| Feature | Count Variable Tracking | Sentinel Empty Slot Strategy |
| :--- | :--- | :--- |
| **Capacity Utilization** | **100% Full Array Capacity ⚡** | Uses $K - 1$ Slots (1 Empty Sentinel) |
| **Code Simplicity** | High (`count == 0`) | Medium (`front == rear`) |
| **Space Footprint** | 1 Extra Integer (`count`) | 0 Extra Variables |

---

## 14. How to Recognize This in Questions
* **"Design a circular double-ended queue supporting O(1) front/rear operations"** $\rightarrow$ LeetCode 641.
* **"Design a FIFO circular queue"** $\rightarrow$ LeetCode 622.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `getRear()` use `(rear - 1 + capacity) % capacity` instead of `elements[rear]`?**  
  *A:* Because `rear` stores the array index of the NEXT unwritten slot. The most recently inserted rear element resides at index `rear - 1`. Modulo handles circular wraparound when `rear == 0`.
* **Q: Can Circular Deque operations be implemented without a `count` variable?**  
  *A:* Yes, by allocating an array of size $K + 1$ and using sentinel pointer conditions: `isEmpty()` when `front == rear`, and `isFull()` when `(rear + 1) % (K + 1) == front`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CIRCULAR QUEUE & DEQUE ARCHITECTURE                   |
+-----------------------------------------------------------------------+
| • Front Insert Backward: front = (front - 1 + capacity) % capacity    |
| • Rear Insert Forward  : rear = (rear + 1) % capacity                 |
| • Rear Delete Backward : rear = (rear - 1 + capacity) % capacity      |
| • Get Rear Index Rule  : idx = (rear - 1 + capacity) % capacity       |
| • Negative Modulo Rule : ALWAYS add +capacity before modulo!          |
| • Time Complexity: All 8 operations execute in O(1) Constant Time ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement Design Circular Deque (LeetCode 641) from scratch.
- [ ] I can implement Design Circular Queue (LeetCode 622).
- [ ] I know why `+ capacity` is required for negative modulo.
- [ ] I know how to calculate `getRear()` index correctly.
- [ ] I can state all 4 circular pointer wraparound formulas.
