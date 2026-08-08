# 03. Circular Linked List & Ring Buffer Data Structures

## 1. Introduction
A **Circular Linked List (CLL)** is a variation of a linked list in which the final node's `next` pointer references the `head` node instead of `null`, forming an infinite closed ring buffer. In technical coding interviews, circular linked lists evaluate cyclic traversal guards, Josephus problem algorithms, Round-Robin CPU scheduling buffers, and ring queue mechanics.

> **Important:** Traversal loops on a Circular Linked List cannot use `while (curr != null)`. Using standard `null` checks triggers an **infinite loop**! Traversals MUST terminate when `curr.next == head` or `curr == tail`.

## 2. Core Concepts
* **Circular Singly Linked List (CSLL)**: Last node's `next` pointer points to `head` (`tail.next = head`).
* **Circular Doubly Linked List (CDLL)**: Last node's `next` points to `head`, AND `head.prev` points to `tail` (`tail.next = head; head.prev = tail;`).
* **Josephus Problem Algorithm**: A famous circular linked list problem where every $K$-th person in a circle is repeatedly eliminated until 1 survivor remains.
* **Tail Pointer Preference**: Maintaining a single `tail` reference in CSLL enables $O(1)$ constant-time insertion at BOTH Head (`tail.next = newNode`) AND Tail!

> **Memory Trick:** **"Maintain a Tail pointer in Circular Linked Lists for O(1) access to both Head and Tail!"**

## 3. Characteristics / Properties
* **Infinite Loop Vulnerability**: Standard linear list traversals (`while (curr != null)`) will spin indefinitely.
* **Do-While Loop Traversal Pattern**:
  ```java
  ListNode curr = head;
  if (head != null) {
      do {
          // Process curr node
          curr = curr.next;
      } while (curr != head);
  }
  ```

```
Circular Linked List Insertion Complexity:
+-----------------------+-------------------+-------------------+-------------------+
| Circular List Type    | Head Pointer Only | Tail Pointer Only | Tail + Head Ref   |
+-----------------------+-------------------+-------------------+-------------------+
| Insert at Head        | O(N) Traversal    | O(1) Constant ⚡  | O(1) Constant ⚡  |
| Insert at Tail        | O(N) Traversal    | O(1) Constant ⚡  | O(1) Constant ⚡  |
| Delete Head           | O(N) Traversal    | O(1) Constant ⚡  | O(1) Constant ⚡  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing $O(1)$ Head Insertion in a CSLL maintaining ONLY a `tail` pointer:

```
Current CSLL (Tail points to Node 30, Tail.next is Head Node 10):
Tail: [ 30 | next --------------------------------> Head: [ 10 | next ] ]

Goal: Insert New Node 99 at Head position

Step 1: newNode.next = tail.next; (New Node 99 points to old Head [ 10 ])
Step 2: tail.next = newNode;      (Tail's next points to New Node 99)

New CSLL:
Tail: [ 30 | next ] ---> New Head: [ 99 | next ] ---> [ 10 | next ] ---> [ 30 ] ✅
Both Head Insertion and Tail Insertion complete in O(1) Constant Time! ⚡
```

## 5. Visual Diagram
Circular Singly Linked List Tail Pointer Layout:

```
                     +---------------------------------------+
                     |                                       |
                     v                                       |
Head Pointer ---> [ Node 10 | next ] ---> [ Node 20 | next ] ---> [ Node 30 | next ]
                                                                       ^
                                                                  Tail Pointer

Notice: tail.next points back to Head (Node 10). Zero null pointers!
```

## 6. Operations / Algorithms
Josephus Problem Implementation (Circle Elimination):

```java
// Simulates Josephus Circle Elimination: Every K-th person is eliminated
public int findJosephusSurvivor(int N, int K) {
    if (N == 1) return 1;

    // Create Circular Singly Linked List 1..N
    ListNode head = new ListNode(1);
    ListNode curr = head;
    for (int i = 2; i <= N; i++) {
        curr.next = new ListNode(i);
        curr = curr.next;
    }
    curr.next = head; // Make circular (tail.next = head)

    // Eliminate every K-th person
    ListNode prev = curr; // prev starts at tail
    curr = head;

    while (prev != curr) { // Loop until 1 person remains (prev == curr)
        // Count K-1 steps to reach person BEFORE elimination target
        for (int count = 1; count < K; count++) {
            prev = curr;
            curr = curr.next;
        }
        // Eliminate K-th person (curr)
        prev.next = curr.next;
        curr = prev.next;
    }

    return curr.val; // Survivor
}
```

> **Quick Syntax:**
```java
// Do-While Traversal Pattern
ListNode curr = head;
if (head != null) {
    do {
        // Code processing curr
        curr = curr.next;
    } while (curr != head);
}
```

## 7. Examples
* **Josephus Problem**: Circle elimination using a circular linked list or mathematical DP (`f(N, K) = (f(N-1, K) + K - 1) % N + 1`).
* **Round-Robin CPU Scheduler**: Rotating active process threads continuously using a Circular Linked List.
* **Ring Buffer / Circular Queue**: Fixed-size circular memory buffer.

## 8. Java Code
Complete interview-ready Java suite implementing Circular Singly Linked List with `tail` pointer, Head/Tail Insertions, Deletions, and Josephus Elimination:

```java
public class CircularLinkedListMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    private ListNode tail; // Single reference pointer

    public CircularLinkedListMaster() {
        this.tail = null;
    }

    // 1. Insert at Head O(1) Time
    public void insertHead(int val) {
        ListNode newNode = new ListNode(val);
        if (tail == null) {
            tail = newNode;
            tail.next = tail; // Self-reference
        } else {
            newNode.next = tail.next; // tail.next is current head
            tail.next = newNode;
        }
    }

    // 2. Insert at Tail O(1) Time
    public void insertTail(int val) {
        insertHead(val); // Insert at head, then advance tail pointer to new node!
        tail = tail.next;
    }

    // 3. Print CSLL Contents
    public void printList() {
        if (tail == null) {
            System.out.println("Empty Circular List");
            return;
        }

        ListNode head = tail.next;
        ListNode curr = head;
        StringBuilder sb = new StringBuilder();

        do {
            sb.append(curr.val).append(" -> ");
            curr = curr.next;
        } while (curr != head);

        sb.append("(Back to Head: ").append(head.val).append(")");
        System.out.println(sb.toString());
    }

    // 4. Josephus Problem Solver O(N * K) Time, O(N) Space
    public static int josephus(int n, int k) {
        if (n == 1) return 1;

        ListNode head = new ListNode(1);
        ListNode curr = head;
        for (int i = 2; i <= n; i++) {
            curr.next = new ListNode(i);
            curr = curr.next;
        }
        curr.next = head; // Close circle

        ListNode prev = curr;
        curr = head;

        while (prev != curr) {
            for (int i = 1; i < k; i++) {
                prev = curr;
                curr = curr.next;
            }
            prev.next = curr.next; // Eliminate K-th node
            curr = prev.next;
        }

        return curr.val;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        CircularLinkedListMaster cll = new CircularLinkedListMaster();

        cll.insertTail(10);
        cll.insertTail(20);
        cll.insertTail(30);
        cll.insertHead(5); // [5, 10, 20, 30]

        System.out.print("Circular List: ");
        cll.printList();

        // Josephus N=7, K=3
        System.out.println("Josephus Survivor (N=7, K=3): Person " + josephus(7, 3)); // Output: 4
    }
}
```

## 9. Complexity Analysis
| Operation | CSLL (Head Reference Only) | CSLL (Tail Reference Only) |
| :--- | :--- | :--- |
| **Insert at Head** | $O(N)$ (Find tail to update `.next`)| **$O(1)$ Constant ⚡** |
| **Insert at Tail** | $O(N)$ (Traverse to end) | **$O(1)$ Constant ⚡** |
| **Delete Head** | $O(N)$ | **$O(1)$ Constant ⚡** |
| **Traversal Pass** | $O(N)$ (Stops when `curr == head`)| $O(N)$ (Stops when `curr == head`)|

## 10. Edge Cases
* **Empty List (`tail == null`)**: Guard methods with `if (tail == null)`.
* **Single Node Circular List (`tail.next == tail`)**: Deleting the only node requires setting `tail = null`.
* **Infinite Loop in Traversal**: Occurs when using `while (curr != null)` instead of `do { ... } while (curr != head)`.

## 11. Common Mistakes
* Using `while (curr != null)` for traversal (spins in an infinite loop!).
* Maintaining only a `head` reference in CSLL (forces $O(N)$ traversal to find tail for every insertion!).
* Forgetting to update `tail.next = head` when inserting or deleting nodes.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** In a Circular Singly Linked List, maintain a **Tail Pointer**, NOT a Head Pointer!
> If you maintain `tail`:
> * **Head** is instantly accessible via **`tail.next`** ($O(1)$).
> * **Tail** is instantly accessible via **`tail`** ($O(1)$).
> * Inserting at Head AND Tail executes in **$O(1)$ constant time**!

> **Memory Trick:** **"Tail.next is Head! Store Tail to get both Head and Tail in O(1) time!"**

## 13. Comparisons
| Feature | Linear Singly Linked List | Circular Singly Linked List |
| :--- | :--- | :--- |
| **Tail Node `.next` Pointer**| `null` | References `head` |
| **Traversal Termination** | `curr == null` | **`curr == head` (do-while loop)** |
| **Head & Tail Insertions** | Requires 2 references (`head`, `tail`)| **Single `tail` reference handles both $O(1)$** |

## 14. How to Recognize This in Questions
* **"Simulate circular elimination / Josephus problem"** $\rightarrow$ Circular Linked List or Josephus DP formula.
* **"Design continuous Round-Robin ring buffer"** $\rightarrow$ Circular Linked List with `tail.next = head`.

## 15. Frequently Asked Interview Questions
* **Q: How do you traverse a Circular Linked List without an infinite loop?**  
  *A:* Use a `do-while` loop starting at `head` and continuing `while (curr != head)`. The `do-while` loop executes the body for `head` once before checking the termination condition when `curr` wraps back around to `head`.
* **Q: What is the mathematical $O(N)$ DP solution for Josephus Problem?**  
  *A:* $J(1, K) = 0$; for $N > 1$, $J(N, K) = (J(N-1, K) + K) \pmod N$. Convert to 1-based indexing by adding 1. Runs in $O(N)$ time and $O(1)$ space without creating nodes.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CIRCULAR LINKED LIST & RING BUFFERS                   |
+-----------------------------------------------------------------------+
| • Tail Reference Advantage: tail.next is Head => O(1) Head & Tail Ops |
| • Traversal Pattern: do { curr = curr.next; } while (curr != head);   |
| • Head Insertion (via Tail): newNode.next = tail.next; tail.next = newNode|
| • Tail Insertion (via Tail): Insert at head, then tail = tail.next    |
| • Josephus Elimination: Delete prev.next = curr.next until prev==curr |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why maintaining a `tail` pointer provides $O(1)$ head & tail operations.
- [ ] I can write the `do-while` traversal pattern for Circular Linked Lists.
- [ ] I can implement $O(1)$ head and tail insertions on CSLL.
- [ ] I can solve the Josephus problem using a Circular Linked List.
- [ ] I can write the $O(N)$ mathematical DP solution for Josephus problem.
