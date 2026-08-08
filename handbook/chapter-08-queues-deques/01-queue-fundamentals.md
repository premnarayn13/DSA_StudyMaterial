# 01. Queue Fundamentals & FIFO Protocol

## 1. Introduction
A **Queue** is a linear data structure that strictly enforces the **FIFO (First-In, First-Out)** access protocol. Elements are inserted (enqueued) at the **Rear / Tail** and removed (dequeued) from the **Front / Head**. In technical coding interviews, Queues serve as the core data structure for Breadth-First Search (BFS) graph traversals, task scheduling algorithms, asynchronous event queues, and sliding window buffer management.

> **Important:** In Java, `java.util.Queue` is an interface. For standard FIFO queue operations in technical interviews, **`java.util.ArrayDeque`** or **`java.util.LinkedList`** MUST be used!

## 2. Core Concepts
* **FIFO Access Protocol**: The item inserted earliest (first) is the first item removed.
* **Core Primitive Operations**:
  * **`offer(element)` / `add(element)`**: Enqueue element at the rear ($O(1)$ time).
  * **`poll()` / `remove()`**: Dequeue and return element from the front ($O(1)$ time).
  * **`peek()` / `element()`**: Read front element without removing ($O(1)$ time).
  * **`isEmpty()`**: Check if queue contains zero elements ($O(1)$ time).
* **Exception-Throwing vs Special Value APIs**:
  * **Throws Exception on Failure**: `add(e)` (Capacity full), `remove()` (Empty), `element()` (Empty).
  * **Returns Special Value (`false` / `null`)**: `offer(e)` (Capacity full), `poll()` (Empty), `peek()` (Empty). **(PREFERRED IN INTERVIEWS)**.

> **Memory Trick:** **"Offer, Poll, Peek! Safe Queue APIs return null/false instead of throwing exceptions!"**

## 3. Characteristics / Properties
* **Restricted Access**: Direct access to middle elements is strictly forbidden. Insertions occur strictly at Tail, deletions occur strictly at Head.
* **Java Queue Interface Hierarchy**:

```
Java Queue API Methods Summary:
+-----------------------+-------------------+-------------------+-------------------+
| Action / Operation    | Throws Exception  | Returns Special   | Best Method Choice|
+-----------------------+-------------------+-------------------+-------------------+
| Enqueue (Insert Tail) | `add(e)`          | `offer(e)` ⚡     | `queue.offer(e)`  |
| Dequeue (Remove Head) | `remove()`        | `poll()` ⚡       | `queue.poll()`    |
| Inspect (Read Head)   | `element()`       | `peek()` ⚡       | `queue.peek()`    |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Queue Operations on `offer(10), offer(20), offer(30), poll(), peek()`:

```
State 1: offer(10) -> Queue: [ 10 ] (Front=10, Rear=10)
State 2: offer(20) -> Queue: [ 10, 20 ] (Front=10, Rear=20)
State 3: offer(30) -> Queue: [ 10, 20, 30 ] (Front=10, Rear=30)

State 4: poll()   -> Removes & Returns 10 (Queue becomes [ 20, 30 ], Front=20) ✅
State 5: peek()   -> Returns 20 (Queue remains [ 20, 30 ]) ✅
```

## 5. Visual Diagram
FIFO Queue Enqueue & Dequeue Architecture:

```
DEQUEUE (Front / Head) <--- [ 10 ] [ 20 ] [ 30 ] <--- ENQUEUE (Rear / Tail)
                              ^               ^
                            Front           Rear
```

## 6. Operations / Algorithms
Standard Java Queue Setup & BFS Queue Template:

```java
// Standard Queue Setup
Queue<Integer> queue = new ArrayDeque<>();

// Enqueue
queue.offer(10);
queue.offer(20);

// Inspect Front
Integer front = queue.peek(); // 10

// Dequeue
Integer popped = queue.poll(); // 10

// Level-by-Level BFS Queue Loop Template
while (!queue.isEmpty()) {
    int levelSize = queue.size();
    for (int i = 0; i < levelSize; i++) {
        int curr = queue.poll();
        // Process current node & enqueue valid neighbors...
    }
}
```

> **Quick Syntax:**
```java
// BFS Level Size Capture Pattern
int levelSize = queue.size();
for (int i = 0; i < levelSize; i++) {
    int curr = queue.poll();
}
```

## 7. Examples
* **LeetCode 933 - Number of Recent Calls**: Sliding window queue.
* **LeetCode 102 - Binary Tree Level Order Traversal**: BFS Queue traversal.
* **LeetCode 200 - Number of Islands**: Graph BFS Queue traversal.

## 8. Java Code
Complete interview-ready Java suite implementing Number of Recent Calls (LeetCode 933) using Queue:

```java
import java.util.ArrayDeque;
import java.util.Queue;

public class QueueFundamentalsMaster {

    // LeetCode 933: Number of Recent Calls O(1) Amortized Time, O(N) Space
    public static class RecentCounter {
        private final Queue<Integer> queue;

        public RecentCounter() {
            this.queue = new ArrayDeque<>();
        }

        public int ping(int t) {
            queue.offer(t);

            // Evict all timestamps older than 3000ms (t - 3000)
            while (!queue.isEmpty() && queue.peek() < t - 3000) {
                queue.poll();
            }

            return queue.size(); // Number of calls in range [t - 3000, t]
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        RecentCounter counter = new RecentCounter();
        System.out.println("ping(1):    " + counter.ping(1));    // Output: 1
        System.out.println("ping(100):  " + counter.ping(100));  // Output: 2
        System.out.println("ping(3001): " + counter.ping(3001)); // Output: 3
        System.out.println("ping(3002): " + counter.ping(3002)); // Output: 3 (Evicts 1!)
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **`offer(val)`** | **Amortized $O(1)$**| $O(1)$ | Enqueues at Rear |
| **`poll()`** | **$O(1)$ Constant** | $O(1)$ | Dequeues from Front |
| **`peek()`** | **$O(1)$ Constant** | $O(1)$ | Direct Front lookup |
| **`isEmpty()`** | **$O(1)$ Constant** | $O(1)$ | Size comparison |

## 10. Edge Cases
* **Polling Empty Queue**: Calling `queue.poll()` on an empty Queue returns `null` safely (whereas `queue.remove()` throws `NoSuchElementException`).
* **BFS Level Size Stale Pointer Bug**: Capturing `queue.size()` into a variable `int size = queue.size()` BEFORE entering the `for` loop is MANDATORY for level-by-level processing!

## 11. Common Mistakes
* Writing `for (int i = 0; i < queue.size(); i++)` directly in BFS (causes `queue.size()` to change dynamically during child enqueues, corrupting level processing!).
* Using `add()` / `remove()` instead of `offer()` / `poll()` (risks unhandled exceptions).
* Using `java.util.Vector` or manual arrays with linear $O(N)$ front element shifting.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** BFS Level Stacking Rule:
> ALWAYS snapshot queue size BEFORE entering level processing loops:
> **`int size = queue.size();`**
> **`for (int i = 0; i < size; i++) { ... }`**
> Never write `i < queue.size()` inside the loop condition!

> **Memory Trick:** **"Snapshot queue.size() into a variable BEFORE entering BFS level loops!"**

## 13. Comparisons
| Feature | `offer()` / `poll()` / `peek()` | `add()` / `remove()` / `element()` |
| :--- | :--- | :--- |
| **Failure Behavior**| **Returns `false` / `null` ⚡** | Throws Exceptions |
| **Empty Queue Check**| Safe (`poll()` returns `null`) | Crashes (`NoSuchElementException`) |
| **Interview Recommendation** | **PREFERRED DEFAULT** | Secondary |

## 14. How to Recognize This in Questions
* **"Process items in First-In, First-Out order"** $\rightarrow$ Queue (`offer`, `poll`).
* **"Level-order traversal of binary tree / shortest path in unweighted graph"** $\rightarrow$ BFS Queue.

## 15. Frequently Asked Interview Questions
* **Q: Why are `offer()`, `poll()`, and `peek()` preferred over `add()`, `remove()`, and `element()`?**  
  *A:* `offer()`, `poll()`, and `peek()` return special values (`false` or `null`) upon capacity exhaustion or empty queue conditions instead of throwing runtime exceptions, creating cleaner and safer control flows.
* **Q: Why does BFS guarantee the shortest path in an unweighted graph?**  
  *A:* Because BFS uses a Queue to explore graph nodes level-by-level in non-decreasing order of distance from the source. The first time a target node is dequeued, it is guaranteed to have been reached via the minimum number of edge transitions.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE FUNDAMENTALS & FIFO PROTOCOL                    |
+-----------------------------------------------------------------------+
| • FIFO Protocol: First-In, First-Out                                  |
| • Standard Java Queue: Queue<Integer> queue = new ArrayDeque<>();     |
| • Preferred APIs: offer() [enqueue], poll() [dequeue], peek() [inspect]|
| • BFS Template: int size = queue.size(); for (int i = 0; i < size; i++)|
| • Complexity: All core ops offer/poll/peek run in O(1) Constant Time  |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `offer()`, `poll()`, and `peek()` are preferred over exception-throwing methods.
- [ ] I can write the snapshot level BFS `int size = queue.size()` template.
- [ ] I can implement Recent Counter (LeetCode 933) using Queue eviction.
- [ ] I know why BFS guarantees shortest path in unweighted graphs.
- [ ] I can instantiate `Queue` using `ArrayDeque` in Java.
