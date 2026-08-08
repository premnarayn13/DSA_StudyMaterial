# 03. Deque Fundamentals & Monotonic Deque Architecture

## 1. Introduction
A **Deque (Double-Ended Queue)** (pronounced "deck") is a linear sequence supporting element insertion, deletion, and inspection at **BOTH the Front and Rear ends in $O(1)$ constant time**. In technical coding interviews, Deques serve as the foundation for **Monotonic Deque** algorithms (LeetCode 239 - Sliding Window Maximum), Work-Stealing thread schedulers (JVM ForkJoinPool), and unified LIFO Stack / FIFO Queue implementations.

> **Important:** In Java, `java.util.Deque` is an interface implemented by `ArrayDeque` and `LinkedList`. **`ArrayDeque` is the standard, high-performance implementation** providing $O(1)$ operations at both ends with zero garbage collection overhead!

## 2. Core Concepts
* **Dual-Ended Primitive Operations**:
  * **Front Operations**: `offerFirst(e)`, `pollFirst()`, `peekFirst()`.
  * **Rear Operations**: `offerLast(e)`, `pollLast()`, `peekLast()`.
* **Stack vs Queue vs Deque API Equivalence**:

```
Java Deque Method Mapping Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Intent      | Standard Queue    | Standard Stack    | Deque Dual API    |
+-----------------------+-------------------+-------------------+-------------------+
| Enqueue / Push        | `offer(e)`        | `push(e)`         | `offerLast(e)`    |
| Dequeue / Pop         | `poll()`          | `pop()`           | `pollFirst()`     |
| Peek / Inspect        | `peek()`          | `peek()`          | `peekFirst()`     |
+-----------------------+-------------------+-------------------+-------------------+
```

* **Monotonic Deque**: Maintains elements in strictly increasing or decreasing order by removing elements from the **Rear** (`pollLast()`) before inserting a new element, while serving max/min queries from the **Front** (`peekFirst()`).

> **Memory Trick:** **"Front is for Dequeuing/Popping (pollFirst), Rear is for Enqueuing/Monotonic eviction (offerLast, pollLast)!"**

## 3. Characteristics / Properties
* **Strict $O(1)$ Both Ends**: Unlike a primitive array where prepending at index 0 requires $O(N)$ element shifts, `ArrayDeque` uses a circular head/tail offset buffer to achieve **Strict $O(1)$ time at both ends**.
* **Monotonic Decreasing Deque Property**: The **Front** of the deque (`peekFirst()`) ALWAYS holds the **Maximum Element** of the current active window!

```
Deque Performance Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Implementation        | Head Ops Time     | Tail Ops Time     | Memory Allocation |
+-----------------------+-------------------+-------------------+-------------------+
| `ArrayDeque`          | Strict O(1) ⚡    | Strict O(1) ⚡    | Contiguous Array  |
| `LinkedList`          | Strict O(1) ⚡    | Strict O(1) ⚡    | 24B Node Objects  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Monotonic Decreasing Deque Eviction on elements `[1, 3, -1, -3, 5]`:

```
Process 1: Deque: [ 1 ]
Process 3: 3 > 1 -> pollLast() 1! offerLast(3) | Deque: [ 3 ]
Process -1: -1 < 3 -> offerLast(-1)            | Deque: [ 3, -1 ] (Front is 3 = MAX!)
Process -3: -3 < -1 -> offerLast(-3)           | Deque: [ 3, -1, -3 ] (Front is 3 = MAX!)
Process 5: 5 > all -> pollLast() -3, -1, 3! offerLast(5) | Deque: [ 5 ] (Front is 5 = MAX!) ✅
```

## 5. Visual Diagram
Monotonic Deque Eviction & Query Mechanics:

```
                  FRONT (peekFirst = MAX)       REAR (Monotonic Eviction)
                         +-----------------------------+
   Window Maximum <----- |  Node 5  |  Node 3  | Node 1| <----- pollLast() when 
                         +-----------------------------+        curr > peekLast()
```

## 6. Operations / Algorithms
LeetCode 641 Design Circular Deque & Monotonic Deque Setup:

```java
// Standard Modern Java Deque Setup
Deque<Integer> deque = new ArrayDeque<>();

// Front Operations
deque.offerFirst(10); // Insert at Front
int headVal = deque.pollFirst(); // Remove from Front
int headPeek = deque.peekFirst(); // Inspect Front

// Rear Operations
deque.offerLast(20); // Insert at Rear
int tailVal = deque.pollLast(); // Remove from Rear
int tailPeek = deque.peekLast(); // Inspect Rear
```

> **Quick Syntax:**
```java
// Monotonic Eviction Loop at Rear
while (!deque.isEmpty() && arr[i] > arr[deque.peekLast()]) {
    deque.pollLast(); // Evict smaller elements from Rear
}
deque.offerLast(i); // Insert current index at Rear
```

## 7. Examples
* **LeetCode 641 - Design Circular Deque**: Double-ended circular queue design.
* **LeetCode 239 - Sliding Window Maximum**: Monotonic Deque window tracking.
* **LeetCode 1425 - Constrained Subsequence Sum**: Dynamic Programming + Monotonic Deque optimization.

## 8. Java Code
Complete interview-ready Java suite implementing Design Circular Deque (LeetCode 641) with $O(1)$ operations at both ends:

```java
public class DequeFundamentalsMaster {

    // LeetCode 641: Design Circular Deque O(1) All Operations
    public static class MyCircularDeque {
        private final int[] data;
        private int head;
        private int count;
        private final int capacity;

        public MyCircularDeque(int k) {
            this.capacity = k;
            this.data = new int[k];
            this.head = 0;
            this.count = 0;
        }

        public boolean insertFront(int value) {
            if (isFull()) return false;
            head = (head - 1 + capacity) % capacity; // Modulo decrement
            data[head] = value;
            count++;
            return true;
        }

        public boolean insertLast(int value) {
            if (isFull()) return false;
            int tail = (head + count) % capacity;
            data[tail] = value;
            count++;
            return true;
        }

        public boolean deleteFront() {
            if (isEmpty()) return false;
            head = (head + 1) % capacity;
            count--;
            return true;
        }

        public boolean deleteLast() {
            if (isEmpty()) return false;
            count--; // Tail is implicitly decremented via count!
            return true;
        }

        public int getFront() {
            return isEmpty() ? -1 : data[head];
        }

        public int getRear() {
            if (isEmpty()) return -1;
            int tail = (head + count - 1) % capacity;
            return data[tail];
        }

        public boolean isEmpty() { return count == 0; }
        public boolean isFull()  { return count == capacity; }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        MyCircularDeque deque = new MyCircularDeque(3);
        System.out.println("insertLast 1:  " + deque.insertLast(1));  // true
        System.out.println("insertLast 2:  " + deque.insertLast(2));  // true
        System.out.println("insertFront 3: " + deque.insertFront(3)); // true (Deque: [3, 1, 2])
        System.out.println("getFront:      " + deque.getFront());      // 3
        System.out.println("getRear:       " + deque.getRear());       // 2
        System.out.println("deleteLast:    " + deque.deleteLast());    // true
        System.out.println("getRear:       " + deque.getRear());       // 1
    }
}
```

## 9. Complexity Analysis
| Deque Implementation | Front Ops Time | Rear Ops Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **`ArrayDeque`** | **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| $O(N)$ Dynamic Array |
| **Circular Array Deque** | **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| $O(K)$ Fixed Array |
| **`LinkedList`** | **Strict $O(1)$ ⚡**| **Strict $O(1)$ ⚡**| $O(N)$ Heap Nodes |

## 10. Edge Cases
* **Modulo Decrement in Circular Deque**: Front insertion decrement requires adding `capacity` before modulo: **`(head - 1 + capacity) % capacity`** to prevent negative index results!
* **Empty Deque Operations**: `getFront()` and `getRear()` return `-1` or `null` safely.

## 11. Common Mistakes
* Writing `(head - 1) % capacity` for front insertion (produces negative array indices in Java!). Always use **`(head - 1 + capacity) % capacity`**.
* Confusing `pollFirst()` (dequeues from Front) with `pollLast()` (evicts from Rear in Monotonic Deque).
* Using `LinkedList` when `ArrayDeque` provides superior cache locality and zero GC pauses.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Modulo Decrement Formula:
> When moving front pointer backward in a Circular Deque:
> Use **`(head - 1 + capacity) % capacity`**
> In Java, `-1 % 5 = -1` (negative result!). Adding `capacity` ensures the dividend is strictly positive!

> **Memory Trick:** **"Always add capacity before modulo decrement: (head - 1 + capacity) % capacity!"**

## 13. Comparisons
| Feature | `ArrayDeque` | `LinkedList` |
| :--- | :--- | :--- |
| **Data Alignment** | Contiguous Array Buffer | Scattered Heap Nodes |
| **Cache Locality** | **High L1/L2 Hits ⚡** | High Cache Misses |
| **Memory Overhead** | Compact Array | 24 Bytes per Node |
| **Interview Recommendation** | **PREFERRED DEFAULT** | Secondary |

## 14. How to Recognize This in Questions
* **"Insert and delete at both ends in O(1) time"** $\rightarrow$ `Deque` / `ArrayDeque`.
* **"Maintain sliding window maximum / minimum in O(N) time"** $\rightarrow$ Monotonic Deque (`peekFirst()`).

## 15. Frequently Asked Interview Questions
* **Q: Why does Java `-1 % 5` return `-1`, and how does Circular Deque fix it?**  
  *A:* In Java, the remainder operator `%` preserves the sign of the dividend (e.g. `-1 % 5 = -1`). Circular Deque fixes this by adding `capacity` before applying modulo: `(head - 1 + capacity) % capacity`, guaranteeing a positive index range `0..capacity-1`.
* **Q: How does a Monotonic Deque retrieve the maximum element of a sliding window in $O(1)$ time?**  
  *A:* By maintaining indices in strictly decreasing order of their array values. The largest element in the active window is ALWAYS located at the front of the deque (`peekFirst()`).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DEQUE FUNDAMENTALS & MONOTONIC ARCHITECTURE           |
+-----------------------------------------------------------------------+
| • Front Ops: offerFirst(e), pollFirst(), peekFirst()                  |
| • Rear Ops:  offerLast(e), pollLast(), peekLast()                     |
| • Modulo Decrement: head = (head - 1 + capacity) % capacity            |
| • Monotonic Deque Eviction: while (!d.isEmpty() && arr[i] > arr[d.peekLast()]) d.pollLast();|
| • Window Maximum Query: peekFirst() holds current max in O(1) time   |
| • Modern Java Setup: Deque<Integer> deque = new ArrayDeque<>();       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the positive modulo decrement formula `(head - 1 + capacity) % capacity`.
- [ ] I know why `peekFirst()` holds the window maximum in a Monotonic Decreasing Deque.
- [ ] I can implement Design Circular Deque (LeetCode 641) in $O(1)$ time.
- [ ] I can select between `offerFirst` / `offerLast` and `pollFirst` / `pollLast`.
- [ ] I know why `ArrayDeque` is preferred over `LinkedList`.
