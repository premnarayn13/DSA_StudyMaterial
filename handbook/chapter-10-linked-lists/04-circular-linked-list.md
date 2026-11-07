# 04. Circular Linked List Architecture, Ring Buffers & Josephus Problem

## 1. Introduction
A **Circular Linked List** is a variation of linked list structures where the last node (**Tail**) does NOT point to `null`, but instead points back to the first node (**Head**), forming a closed continuous ring. Circular Linked Lists exist in two forms: **Singly Circular Linked List** and **Doubly Circular Linked List**. In systems architecture and software engineering, circular linked lists power CPU round-robin task schedulers, multiplayer turn-based gaming queues, circular ring audio buffers, and the classic **Josephus Problem (LeetCode 1823)**.

> **Important:** Maintaining a SINGLE **`tail` reference** (instead of a `head` reference) in a Singly Circular Linked List gives instant $O(1)$ constant-time access to BOTH the tail node (`tail`) and the head node (`tail.next`) without needing a separate head pointer!

```
Circular Linked List Ring Topology:
+-----------------------------------------------------------------------------------+
| Head Node: tail.next                                                              |
| Tail Node: tail (tail.next points back to Head, forming a closed ring loop!)      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Tail Pointer Representation

### 2.1 The Single Tail Pointer Trick
In a traditional Singly Linked List, inserting at the tail requires an $O(N)$ traversal from `head` unless a `tail` reference is explicitly maintained.
In a **Singly Circular Linked List**:
* `tail` points to the last node.
* **`tail.next`** automatically points to the **Head Node**!
* **Inserting at Head ($O(1)$ Time)**: Insert node between `tail` and `tail.next`.
* **Inserting at Tail ($O(1)$ Time)**: Insert node between `tail` and `tail.next`, then advance `tail = tail.next`.

```
Tail Pointer Representation:
tail -------> [ Node 3 (Tail) ]
                  |
                  v  (tail.next)
              [ Node 1 (Head) ] ---> [ Node 2 ] ---> [ Node 3 ]
```

### 2.2 Doubly Circular Linked List
In a **Doubly Circular Linked List**:
* `head.prev` points to `tail`.
* `tail.next` points to `head`.
* Enables $O(1)$ constant time forward and backward circular navigation (used in Linux kernel IPC queues).

> **Memory Trick:** **"In Singly Circular List: tail.next is ALWAYS the Head node! Single tail reference gives O(1) head and tail access!"**

---

## 3. Characteristics & Josephus Problem Algorithm

### 3.1 The Josephus Problem (LeetCode 1823 - Find Winner of Circular Game)
Given $N$ friends sitting in a circle numbered $1 \dots N$, and a step count $K$:
1. Start at friend 1.
2. Count $K$ friends in clockwise order (including current friend).
3. The $K$-th friend is eliminated from the circle, and the circle closes.
4. Repeat counting $K$ friends from the next friend until **only 1 winner remains**.

#### Solution Approaches:
* **Circular Linked List Simulation**: Build a circular list of $N$ nodes. Step $K-1$ times, delete target node `prev.next = target.next` in $O(N \cdot K)$ time.
* **Mathematical DP Formula ($O(N)$ Time, $O(1)$ Space)**:

$$J(n, k) = (J(n - 1, k) + k) \bmod n$$

  With base case $J(1, k) = 0$ (0-indexed winner).

```
Josephus Problem DP Progression:
J(1, k) = 0
J(2, k) = (J(1, k) + k) % 2
J(n, k) = (J(n - 1, k) + k) % n
Winner (1-Indexed) = J(N, K) + 1  ✅ (O(N) Time, O(1) Space!)
```

---

## 4. Internal Working Mechanics
Tracing Insertion at Head of Circular List `[10, 20]` with `newNode(5)`:

```
Initial State: tail -> [20], tail.next -> [10] (Head)

Step 1: Create `newNode(5)`.
Step 2: Set `newNode.next = tail.next` (5.next = 10).
Step 3: Set `tail.next = newNode`     (20.next = 5).

Resulting Ring: tail(20) -> [5 (Head)] -> [10] -> [20] -> [5] ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
Singly Circular Linked List Ring Layout Topology:

```
                  +-----------------------------------+
                  |                                   |
                  v                                   |
           ( Node 10: Head ) <--- (tail.next)         |
             /             \                          |
            /               \                         |
    ( Node 30 ) <--------- ( Node 20: Tail ) ---------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a Singly Circular Linked List with Tail pointer representation and the Josephus Problem solver (LeetCode 1823):

```java
import java.util.*;

public class CircularLinkedListMaster {

    public static class Node {
        public int val;
        public Node next;

        public Node(int val) {
            this.val = val;
            this.next = null;
        }
    }

    // 1. Singly Circular Linked List with Tail Pointer Representation
    public static class CircularLinkedList {
        private Node tail;
        private int size;

        public CircularLinkedList() {
            this.tail = null;
            this.size = 0;
        }

        public int size() { return size; }
        public boolean isEmpty() { return tail == null; }

        // Insert at Head (Right after tail) O(1) Time
        public void insertHead(int val) {
            Node newNode = new Node(val);
            if (isEmpty()) {
                newNode.next = newNode; // Points to itself!
                tail = newNode;
            } else {
                newNode.next = tail.next; // Head is tail.next
                tail.next = newNode;
            }
            size++;
        }

        // Insert at Tail O(1) Time
        public void insertTail(int val) {
            insertHead(val);
            tail = tail.next; // Advance tail reference
        }

        // Delete Head O(1) Time
        public int deleteHead() {
            if (isEmpty()) throw new NoSuchElementException("List is empty");
            Node head = tail.next;
            int val = head.val;

            if (tail == head) { // Single element
                tail = null;
            } else {
                tail.next = head.next;
                head.next = null; // Unlink for GC
            }
            size--;
            return val;
        }

        public int[] toArray() {
            if (isEmpty()) return new int[0];
            int[] arr = new int[size];
            Node curr = tail.next; // Start at head
            for (int i = 0; i < size; i++) {
                arr[i] = curr.val;
                curr = curr.next;
            }
            return arr;
        }
    }

    // 2. Josephus Problem Solver (LeetCode 1823) O(N) Time, O(1) Space
    public static int findTheWinner(int n, int k) {
        int winner = 0; // Base case for 1 person (0-indexed)
        for (int i = 2; i <= n; i++) {
            winner = (winner + k) % i;
        }
        return winner + 1; // Convert to 1-indexed
    }
}
```

> **Quick Syntax:**
```java
// Circular Linked List Loop Traversal Pattern
if (tail != null) {
    Node curr = tail.next; // Start at Head
    do {
        System.out.println(curr.val);
        curr = curr.next;
    } while (curr != tail.next);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 1823 - Find the Winner of the Circular Game**: Josephus problem.
* **Operating System Round-Robin Task Scheduler**: Process time-slice allocation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration inserting nodes into a circular linked list, checking ring traversal, and solving the Josephus Problem:

```java
public class CircularLinkedListDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Singly Circular Linked List Operations ===");
        CircularLinkedListMaster.CircularLinkedList list = 
            new CircularLinkedListMaster.CircularLinkedList();

        list.insertHead(20);
        list.insertHead(10);
        list.insertTail(30);

        System.out.println("Elements (Head to Tail): " + Arrays.toString(list.toArray())); // Output: [10, 20, 30]

        System.out.println("\n=== 2. Josephus Problem (N=5, K=2) ===");
        int winner = CircularLinkedListMaster.findTheWinner(5, 2);
        System.out.println("Winner for (N=5, K=2): Person " + winner); // Output: Person 3
    }
}
```

---

## 9. Complexity Analysis

| Operation / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`insertHead()`** | **$O(1)$ Constant ⚡** | $O(1)$ | Tail pointer re-linking `newNode.next = tail.next` |
| **`insertTail()`** | **$O(1)$ Constant ⚡** | $O(1)$ | `insertHead()` + `tail = tail.next` |
| **`deleteHead()`** | **$O(1)$ Constant ⚡** | $O(1)$ | `tail.next = head.next` |
| **Josephus DP (1823)**| **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Formula `winner = (winner + k) % i` |

---

## 10. Edge Cases & Boundary Handling
* **Single Element Circular List**: Node's `next` pointer points to ITSELF (`node.next == node`).
* **Traversing Circular List**: Standard `while (curr != null)` loop causes an **INFINITE LOOP**! Always use `do { ... } while (curr != head)` or track iteration count using `size`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `while (curr != null)` for Circular Traversal**:
  - In a circular list, `curr.next` NEVER equals `null`!
  - **Always check `curr != head` or use a counter `for (int i = 0; i < size; i++)`**.
* **Losing Tail Reference on Tail Insertion**: Forgetting `tail = tail.next` after inserting at the end leaves `tail` pointing to the previous last node.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `do-while` is Required for Circular List Traversal:
> A `while (curr != head)` loop fails on the first iteration because `curr` is initialized to `head` (`head != head` evaluates `false` immediately!).
> Using a **`do { ... } while (curr != head)`** loop executes the loop body first before checking the termination condition!

> **Memory Trick:** **"Circular traversal loop: do { ... } while (curr != head)! Check curr != head, not curr != null!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard Singly List | Circular Linked List |
| :--- | :--- | :--- |
| **Tail Pointer `next`** | `null` | **Points to Head Node ⚡** |
| **Head Access from Tail**| $O(N)$ without tail pointer | **$O(1)$ Constant via `tail.next` ⚡** |
| **Loop Condition** | `curr != null` | `curr != head` (via `do-while`) |

---

## 14. How to Recognize This in Questions
* **"Find winner of circular game where every K-th person is eliminated"** $\rightarrow$ LeetCode 1823 (Josephus Problem DP).
* **"Implement Round-Robin CPU scheduling queue"** $\rightarrow$ Circular Linked List.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does maintaining a single `tail` pointer give $O(1)$ access to both head and tail in a circular list?**  
  *A:* Because `tail` is the last node, and `tail.next` is defined as the head node. Thus `tail` gives $O(1)$ tail access and `tail.next` gives $O(1)$ head access.
* **Q: Explain the Josephus DP formula $J(n, k) = (J(n - 1, k) + k) \bmod n$.**  
  *A:* Eliminating person $K$ reduces the problem size from $N$ to $N-1$. The indices of the remaining people are shifted by $K$. Adding $K \bmod N$ maps the winner's position in the smaller subproblem back to the original circle.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CIRCULAR LINKED LIST & JOSEPHUS PROBLEM               |
+-----------------------------------------------------------------------+
| • Single Tail Representation: tail points to end; tail.next = Head    |
| • O(1) Head & Tail Ops: Insert Head/Tail in O(1) constant time ⚡       |
| • Traversal Rule: Use do { ... } while (curr != head) (Avoid infinite while)|
| • Single Element Invariant: node.next == node                         |
| • Josephus Formula (1823): winner = (winner + k) % i (for i=2..N)      |
| • Winner 1-Indexed: Return winner + 1 in O(N) time and O(1) space     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement a Singly Circular List with a single `tail` reference.
- [ ] I know why `while (curr != null)` causes an infinite loop in circular lists.
- [ ] I can write the `do-while` circular traversal template.
- [ ] I can solve the Josephus Problem (LeetCode 1823) using DP in $O(N)$ time.
- [ ] I know why `tail.next` provides instant $O(1)$ head access.
