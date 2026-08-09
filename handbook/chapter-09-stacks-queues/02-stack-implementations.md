# 02. Stack Implementations, Array vs Linked List Backings & Memory Audits

## 1. Introduction
Implementing a Stack requires choosing between two underlying data structures: a **Contiguous Resizing Array** (`ArrayStack`) or a **Doubly/Singly Linked List** (`LinkedListStack`). While both implementations fulfill the **$O(1)$ LIFO operational contract**, they present distinct trade-offs in **CPU cache locality**, **heap memory overhead**, **garbage collection latency**, and **garbage object creation footprint**.

> **Important:** In modern computer architecture, **Array-backed Stacks (`ArrayDeque`) outperform Linked List Stacks (`LinkedList`) by up to $3\times \text{ to } 5\times$**! This speed advantage stems from **CPU Cache Line Locality**: array elements reside in contiguous memory addresses, triggering pre-fetching hardware caches!

```
Array vs Linked List Stack Memory Topology:
+-----------------------------------------------------------------------------------+
| Array Stack      : [ Val 10 | Val 20 | Val 30 | Val 40 ] (Contiguous Cache Memory)⚡|
| Linked List Stack: [ Node A ] ---> [ Node B ] ---> [ Node C ] (Fragmented Heap)   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Architectural Comparison

### 2.1 Array-backed Stack (`ArrayStack`)
* Stores elements in a contiguous primitive array `Object[]`.
* **Pros**: Superior CPU L1/L2 cache locality, zero pointer overhead per element, minimal garbage collection pressure.
* **Cons**: Requires reallocation resizing when capacity is reached ($O(N)$ worst-case copy latency during resize).

### 2.2 Linked List-backed Stack (`LinkedListStack`)
* Stores elements in dynamically allocated node objects (`Node<T> { T data; Node<T> next; }`).
* **Pros**: Truly predictable $O(1)$ worst-case push/pop operations (no resize spikes).
* **Cons**: High heap memory overhead (24 bytes per node object + 8 bytes reference pointer), poor CPU cache locality, heavy Garbage Collection overhead.

```
Architectural Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature Metrics       | Array Stack       | Linked List Stack | Legacy Vector Stack|
+-----------------------+-------------------+-------------------+-------------------+
| CPU Cache Locality    | **Excellent ⚡**  | Poor              | Good              |
| Memory Overhead/Elem  | **0 Bytes Extra** | ~32 Bytes per Node| 0 Bytes Extra     |
| Push Time (Average)   | **$O(1)$ Amortized**| **$O(1)$ Constant**| $O(1)$ Amortized  |
| Worst-Case Push Time  | $O(N)$ (On Resize)| **$O(1)$ Constant**| $O(N)$ (On Resize)|
| Thread Safety         | Non-Synchronized  | Non-Synchronized  | Synchronized      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Array Stacks win on CPU cache and low memory footprint! Linked List Stacks win on zero resize latency!"**

---

## 3. Characteristics & 64-Bit JVM Memory Footprint Audit

### 3.1 64-Bit JVM Object Memory Calculation
On a 64-bit JVM with Compressed OOPs (`-XX:+UseCompressedOops`):
* **Linked List Node Object Footprint**:
  - Mark Word + Class Pointer: 12 Bytes.
  - Data Reference (`T item`): 4 Bytes.
  - Next Reference (`Node next`): 4 Bytes.
  - Padding (8-byte alignment): 4 Bytes.
  - **Total Node Memory Overhead**: **24 Bytes per element!**
* **Array-backed Object Reference Footprint**:
  - Array elements store 4-byte compressed reference pointers in contiguous memory addresses.
  - **Total Array Overhead**: **4 Bytes per element!**

```
Memory Footprint Audit (1,000,000 Integer Elements):
- Linked List Stack : 1,000,000 * 24 B (Node) + 1,000,000 * 16 B (Integer Box) = ~40 MB Heap
- Array Stack       : 1,000,000 * 4 B (Ref Array) + 1,000,000 * 16 B (Integer Box) = ~20 MB Heap
Array Stack saves 50% Heap Memory! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Linked List Stack Push and Pop Operations:

```
Init: top = null. Size = 0.

Push("A"):
  - Create newNode("A"). newNode.next = null.
  - top = newNode. Size = 1.
  - Stack: [ "A" ] (top)

Push("B"):
  - Create newNode("B"). newNode.next = top ("A").
  - top = newNode. Size = 2.
  - Stack: [ "B" ] -> [ "A" ]

Pop():
  - Extract val = top.data ("B").
  - top = top.next ("A"). Size = 1.
  - Unlinked Node("B") becomes eligible for Garbage Collection!

All operations completed in strict O(1) Constant Time! ✅
```

---

## 5. Visual Diagram
Linked List Stack Node Traversal Topography:

```
  Push / Pop Boundary
         |
         v
     +-------+--------+      +-------+--------+      +-------+--------+
     |  "C"  |  next  | ---> |  "B"  |  next  | ---> |  "A"  |  null  |
     +-------+--------+      +-------+--------+      +-------+--------+
         ^
         |
    top Pointer
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementations of a Linked List Stack (`LinkedListStack`) and an Optimized Resizing Array Stack (`ArrayStack`):

```java
import java.util.EmptyStackException;

public class StackImplementationsMaster {

    // 1. Linked List-backed Stack Implementation O(1) Push/Pop Guaranteed
    public static class LinkedListStack<T> {
        private static class Node<T> {
            T data;
            Node<T> next;

            Node(T data, Node<T> next) {
                this.data = data;
                this.next = next;
            }
        }

        private Node<T> top;
        private int size;

        public LinkedListStack() {
            this.top = null;
            this.size = 0;
        }

        // Guaranteed O(1) Constant Time Push (No resize latency!)
        public void push(T item) {
            top = new Node<>(item, top);
            size++;
        }

        // Guaranteed O(1) Constant Time Pop
        public T pop() {
            if (isEmpty()) {
                throw new EmptyStackException();
            }
            T data = top.data;
            top = top.next; // Advance head reference
            size--;
            return data;
        }

        public T peek() {
            if (isEmpty()) {
                throw new EmptyStackException();
            }
            return top.data;
        }

        public boolean isEmpty() {
            return top == null;
        }

        public int size() {
            return size;
        }
    }

    // 2. Optimized Resizing Array-backed Stack Implementation
    public static class ArrayStack<T> {
        private Object[] elements;
        private int top;

        public ArrayStack(int initialCapacity) {
            elements = new Object[initialCapacity];
            top = -1;
        }

        public void push(T item) {
            if (top == elements.length - 1) {
                resize(elements.length * 2);
            }
            elements[++top] = item;
        }

        @SuppressWarnings("unchecked")
        public T pop() {
            if (isEmpty()) throw new EmptyStackException();
            T val = (T) elements[top];
            elements[top--] = null; // Prevent memory leak
            if (top > 0 && top == elements.length / 4) {
                resize(elements.length / 2);
            }
            return val;
        }

        @SuppressWarnings("unchecked")
        public T peek() {
            if (isEmpty()) throw new EmptyStackException();
            return (T) elements[top];
        }

        public boolean isEmpty() { return top == -1; }
        public int size() { return top + 1; }

        private void resize(int newCapacity) {
            Object[] copy = new Object[newCapacity];
            System.arraycopy(elements, 0, copy, 0, top + 1);
            elements = copy;
        }
    }
}
```

> **Quick Syntax:**
```java
// Linked List Stack Node Pointer Re-linking Syntax
top = new Node<>(item, top); // Atomically prepends node to head!
```

---

## 7. Concrete Problem Examples
* **Real-time Embedded Systems (Strict Latency Constraints)**: Preferred Linked List Stack (predictable $O(1)$ worst-case without resize pauses).
* **High-Throughput Financial Systems**: Preferred Array Stack (maximum CPU cache locality).

---

## 8. Java Code Demonstration & Dry Run
Demonstration benchmarking `LinkedListStack` and `ArrayStack`:

```java
public class StackImplementationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Linked List Stack Demonstration ===");
        StackImplementationsMaster.LinkedListStack<Integer> llStack = new StackImplementationsMaster.LinkedListStack<>();
        llStack.push(10);
        llStack.push(20);
        llStack.push(30);

        System.out.println("Top Element: " + llStack.peek()); // 30
        System.out.println("Popped: " + llStack.pop());      // 30
        System.out.println("New Top: " + llStack.peek());     // 20

        System.out.println("\n=== 2. Resizing Array Stack Demonstration ===");
        StackImplementationsMaster.ArrayStack<String> arrStack = new StackImplementationsMaster.ArrayStack<>(2);
        arrStack.push("Alpha");
        arrStack.push("Beta");
        arrStack.push("Gamma"); // Resizes automatically!

        System.out.println("Array Stack Top: " + arrStack.peek()); // Gamma
        System.out.println("Popped: " + arrStack.pop());          // Gamma
    }
}
```

---

## 9. Complexity Analysis

| Metric / Parameter | Array-backed Stack (`ArrayStack`) | Linked List-backed Stack (`LinkedListStack`) |
| :--- | :--- | :--- |
| **Amortized Push Time** | **$O(1)$ Amortized ⚡** | **$O(1)$ Strict Constant ⚡** |
| **Worst-case Push Time**| $O(N)$ (Array Copy on Resize) | **$O(1)$ Strict Constant ⚡** |
| **Cache Line Performance**| **High L1/L2 Cache Hit Rate ⚡**| Low Cache Hit Rate (Pointer Chasing) |
| **Memory Overhead per Node**| **0 Bytes** | 24 Bytes Object Header + Pointers |

---

## 10. Edge Cases & Boundary Handling
* **Underflow Exception Handling**: Both implementations throw `EmptyStackException` on popping empty structures.
* **Array Resizing Memory Spikes**: Resizing temporarily requires $1.5\times$ to $2\times$ array memory during `System.arraycopy`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `LinkedList` for General Stack Needs**:
  - Instantiating `List<T> stack = new LinkedList<>()` creates thousands of unnecessary heap node objects, increasing Garbage Collection pauses.
  - **Use `ArrayDeque` (`Deque<T> stack = new ArrayDeque<>()`) for 99% of stack applications**.
* **Failing to Nullify References on Array Pop**: Leaving array indices un-nullified causes memory leaks.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** When to Choose Linked List Stack Over Array Stack:
> Choose a Linked List Stack ONLY when **Strict Real-Time Latency Guarantees** are mandatory (e.g. hard real-time systems where an $O(N)$ array copy resize pause would breach latency deadlines).
> For all general software engineering tasks, Array Stack (`ArrayDeque`) is vastly superior due to CPU cache locality!

> **Memory Trick:** **"Use Linked List Stack for zero resize latency! Use Array Stack for maximum speed and lowest memory overhead!"**

---

## 13. System & Implementation Comparisons

| Feature | `ArrayDeque` | Custom `LinkedListStack` |
| :--- | :--- | :--- |
| **Garbage Collection Overhead** | **Near Zero (Reusable Array) ⚡** | High (Node churn per push/pop) |
| **Speed Benchmark** | **3x Faster ⚡** | Slower |
| **Memory Contiguity** | Contiguous Block | Scattered Heap Locations |

---

## 14. How to Recognize This in Questions
* **"Implement a stack with strict O(1) worst-case time without array resize delays"** $\rightarrow$ Linked List Stack.
* **"Implement a stack with maximum memory efficiency and speed"** $\rightarrow$ Array Stack (`ArrayDeque`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does array stack resizing use a $2\times$ multiplication factor instead of a fixed $+100$ addition factor?**  
  *A:* Doubling capacity ($2\times$) ensures that $N$ pushes incur a total of $O(N)$ copy operations, resulting in **$O(1)$ amortized time per push**. Adding a fixed $+100$ capacity incurs $O(N^2)$ total copies, degrading push time to $O(N)$ average time!
* **Q: What is pointer chasing in Linked List Stacks?**  
  *A:* Pointer chasing occurs when the CPU traverses heap references (`node.next`). Because nodes are allocated at random heap addresses, traversing pointers causes frequent CPU L1/L2 cache misses.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK IMPLEMENTATIONS & MEMORY AUDIT                  |
+-----------------------------------------------------------------------+
| • Array Stack: Contiguous memory; 3x faster due to CPU Cache Locality |
| • Linked List Stack: Guaranteed O(1) worst-case push (Zero resize delay)|
| • Node Memory Overhead: ~24 Bytes per element in Linked List          |
| • Array Resizing Rule: Double capacity (2x) for O(1) Amortized Push   |
| • Industry Standard: Always prefer ArrayDeque over LinkedList         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement both ArrayStack and LinkedListStack from scratch.
- [ ] I can state the 64-bit JVM memory footprint of a Linked List node.
- [ ] I know why $2\times$ array doubling achieves $O(1)$ amortized push time.
- [ ] I can explain CPU cache line locality advantages of Array stacks.
- [ ] I know when a Linked List stack is preferred over an Array stack.
