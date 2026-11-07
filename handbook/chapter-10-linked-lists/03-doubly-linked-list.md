# 03. Doubly Linked List Architecture, Bidirectional Navigation & $O(1)$ Unlinking

## 1. Introduction
A **Doubly Linked List (DLL)** is a linear linked data structure where every node contains two pointer references: a **`next` pointer** pointing to the subsequent node and a **`prev` pointer** pointing to the preceding node. In systems engineering and technical interviews, Doubly Linked Lists underpin critical data structures such as Java's `java.util.LinkedList`, `LinkedHashMap` (for access-order tracking), LRU Caches (LeetCode 146), and operating system thread schedulers.

> **Important:** The primary architectural power of a Doubly Linked List is **Strict $O(1)$ Constant-Time Node Deletion given a direct node reference**. Unlike a Singly Linked List (which requires traversing from `head` to find the predecessor node), a DLL node can unlink ITSELF in $O(1)$ time using `node.prev.next = node.next` and `node.next.prev = node.prev`!

```
Doubly Linked List Memory Architecture:
+-----------------------------------------------------------------------------------+
| Head <===> [ Node 1 ] <===> [ Node 2 ] <===> [ Node 3 ] <===> Tail                |
| Node Structure: [ prev reference | val payload | next reference ]                 |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Pointer Re-linking Mechanics

### 2.1 Node Anatomy & 64-Bit Memory Overhead
A Doubly Linked List node object contains:
* **Value Field (`val`)**: Data payload.
* **Next Reference (`next`)**: Pointer to subsequent node.
* **Prev Reference (`prev`)**: Pointer to preceding node.

```java
public class Node {
    public int val;
    public Node next;
    public Node prev;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.prev = null;
    }
}
```

* **Memory Footprint on 64-Bit HotSpot JVM (Compressed OOPs)**:
  - Header: 12 Bytes
  - `val` (`int`): 4 Bytes
  - `next` pointer: 4 Bytes
  - `prev` pointer: 4 Bytes
  - Padding: 8 Bytes (to align to 8-byte boundary)
  - **Total Memory per Node**: **32 Bytes** (800% memory overhead compared to a 4-byte primitive).

### 2.2 $O(1)$ Arbitrary Node Unlinking
Given a direct reference to a target node `node` in a Doubly Linked List:
```java
public void unlink(Node node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
    node.next = null; // Unlink for GC
    node.prev = null;
}
```

```
Unlinking Node 2 in-place:
Before : ( Node 1 ) <====> ( Node 2 ) <====> ( Node 3 )
Action : 1. Node 1.next = Node 3
         2. Node 3.prev = Node 1
After  : ( Node 1 ) <=======================> ( Node 3 ) ✅ (O(1) Time!)
```

> **Memory Trick:** **"DLL node unlinks ITSELF in O(1) time: node.prev.next = node.next AND node.next.prev = node.prev!"**

---

## 3. Characteristics & Dummy Head/Tail Sentinel Pattern

### 3.1 Dummy Head and Dummy Tail Sentinels
In a raw Doubly Linked List, updating pointers requires checking whether `node.prev == null` (head edge case) or `node.next == null` (tail edge case).
By using **Dummy Head and Dummy Tail Sentinel Nodes**:
* `head.next` points to the first real node.
* `tail.prev` points to the last real node.
* **Benefit**: Every real node has a non-null `prev` and non-null `next`, completely eliminating null checks during insertion, deletion, and reordering!

```
Dummy Head & Tail Layout:
( Dummy Head @0x100 ) <===> [ Real Node 1 ] <===> [ Real Node 2 ] <===> ( Dummy Tail @0x900 )
```

---

## 4. Internal Working Mechanics
Tracing Insertion of a Node `X` between `head` (Dummy Head) and `head.next` (Push Front in LRU Cache):

```
Initial List : ( Dummy Head ) <=========================> ( Node 1 )
Target Position: Insert Node X right after Dummy Head.

Step 1: newNode.next = head.next  (X.next = Node 1)
Step 2: newNode.prev = head       (X.prev = Dummy Head)
Step 3: head.next.prev = newNode  (Node 1.prev = X)
Step 4: head.next = newNode       (Dummy Head.next = X)

Resulting List: ( Dummy Head ) <===> ( Node X ) <===> ( Node 1 ) ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
Doubly Linked List Bidirectional Linkage Topography:

```
               +-----------------+         +-----------------+         +-----------------+
 dummyHead <==>| prev: 0x100     |<=======>| prev: 0x200     |<=======>| prev: 0x300     |<==> dummyTail
               | val: 10         |         | val: 20         |         | val: 30         |
               | next: 0x300     |========>| next: 0x400     |========>| next: 0x900     |
               +-----------------+         +-----------------+         +-----------------+
                 Node @ 0x200                Node @ 0x300                Node @ 0x400
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a Doubly Linked List utilizing Dummy Head and Tail sentinels:

```java
import java.util.*;

public class DoublyLinkedListMaster {

    public static class Node {
        public int val;
        public Node prev;
        public Node next;

        public Node(int val) {
            this.val = val;
            this.prev = null;
            this.next = null;
        }
    }

    public static class DoublyLinkedList {
        private final Node head; // Dummy Head
        private final Node tail; // Dummy Tail
        private int size;

        public DoublyLinkedList() {
            this.head = new Node(0);
            this.tail = new Node(0);
            head.next = tail;
            tail.prev = head;
            this.size = 0;
        }

        public int size() { return size; }
        public boolean isEmpty() { return size == 0; }

        // 1. Insert at Head (Right after Dummy Head) O(1) Time
        public void addFirst(int val) {
            Node newNode = new Node(val);
            newNode.next = head.next;
            newNode.prev = head;
            head.next.prev = newNode;
            head.next = newNode;
            size++;
        }

        // 2. Insert at Tail (Right before Dummy Tail) O(1) Time
        public void addLast(int val) {
            Node newNode = new Node(val);
            newNode.next = tail;
            newNode.prev = tail.prev;
            tail.prev.next = newNode;
            tail.prev = newNode;
            size++;
        }

        // 3. Unlink Node in O(1) Constant Time given Node reference
        public void removeNode(Node node) {
            if (node == head || node == tail) return;
            node.prev.next = node.next;
            node.next.prev = node.prev;
            node.next = null;
            node.prev = null;
            size--;
        }

        // 4. Remove First Element O(1) Time
        public int removeFirst() {
            if (isEmpty()) throw new NoSuchElementException("List is empty");
            Node first = head.next;
            int val = first.val;
            removeNode(first);
            return val;
        }

        // 5. Remove Last Element O(1) Time
        public int removeLast() {
            if (isEmpty()) throw new NoSuchElementException("List is empty");
            Node last = tail.prev;
            int val = last.val;
            removeNode(last);
            return val;
        }

        public int[] toArray() {
            int[] arr = new int[size];
            Node curr = head.next;
            int idx = 0;
            while (curr != tail) {
                arr[idx++] = curr.val;
                curr = curr.next;
            }
            return arr;
        }
    }
}
```

> **Quick Syntax:**
```java
// O(1) Node Unlinking Pattern
node.prev.next = node.next;
node.next.prev = node.prev;
```

---

## 7. Concrete Problem Examples
* **LeetCode 146 - LRU Cache**: HashMap + Doubly Linked List for $O(1)$ access and eviction.
* **LeetCode 430 - Flatten a Multilevel Doubly Linked List**: Recursive child list flattening.

---

## 8. Java Code Demonstration & Dry Run
Demonstration inserting nodes at head and tail, removing nodes, and converting to array:

```java
public class DoublyLinkedListDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Building Doubly Linked List ===");
        DoublyLinkedListMaster.DoublyLinkedList list = 
            new DoublyLinkedListMaster.DoublyLinkedList();

        list.addFirst(20);
        list.addFirst(10);
        list.addLast(30);
        list.addLast(40);

        System.out.println("Elements: " + Arrays.toString(list.toArray())); // Output: [10, 20, 30, 40]

        System.out.println("\n=== 2. Removing First and Last Elements ===");
        System.out.println("Removed First: " + list.removeFirst()); // Output: 10
        System.out.println("Removed Last:  " + list.removeLast());  // Output: 40
        System.out.println("New Elements:   " + Arrays.toString(list.toArray())); // Output: [20, 30]
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **`addFirst()` / `addLast()`**| **$O(1)$ Constant ⚡**| $O(1)$ | Head/Tail sentinel re-linking |
| **`removeNode(node)`** | **$O(1)$ Constant ⚡**| $O(1)$ | Direct `prev` and `next` unlinking |
| **Search by Value** | $O(N)$ Linear | $O(1)$ | Sequential bidirectional search |

---

## 10. Edge Cases & Boundary Handling
* **Removing from Empty List**: Throws `NoSuchElementException`.
* **Single Element List**: Dummy head and tail sentinels handle single-node unlinking cleanly without null pointers.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Update `node.next.prev`**:
  - Updating `node.prev.next = node.next` without setting `node.next.prev = node.prev` breaks backward traversal!
  - **Always update BOTH forward (`next`) and backward (`prev`) pointers**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why LRU Cache Uses Doubly Linked List:
> An LRU (Least Recently Used) Cache requires moving a key to the front of the queue upon access in $O(1)$ time.
> A HashMap provides $O(1)$ key-to-node lookup. Once the `Node` reference is obtained, a **Doubly Linked List unlinks the node in $O(1)$ time** and pushes it to the head!

> **Memory Trick:** **"HashMap + Doubly Linked List = LRU Cache in O(1) time!"**

---

## 13. System & Implementation Comparisons

| Feature | Singly Linked List | Doubly Linked List |
| :--- | :--- | :--- |
| **Node Unlinking (Given Node)**| $O(N)$ Linear Search | **$O(1)$ Constant ⚡** |
| **Backward Traversal** | Impossible | **Supported ⚡** |
| **Memory per Node** | 24 Bytes | 32 Bytes (Extra `prev` pointer) |

---

## 14. How to Recognize This in Questions
* **"Design LRU Cache with O(1) get and put operations"** $\rightarrow$ LeetCode 146 (HashMap + Doubly Linked List).
* **"Flatten a multilevel doubly linked list"** $\rightarrow$ LeetCode 430.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Doubly Linked List node take 32 bytes of heap memory on 64-bit JVMs?**  
  *A:* Object header takes 12 bytes, `val` takes 4 bytes, `next` and `prev` pointers take 4 bytes each (compressed OOPs), totaling 24 bytes + 8 bytes padding = 32 bytes.
* **Q: Why are Dummy Head and Tail sentinels recommended in Doubly Linked List design?**  
  *A:* Sentinels guarantee that every real node has a non-null `prev` and `next` pointer, eliminating null pointer checks during insertions and deletions.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DOUBLY LINKED LIST & O(1) UNLINKING                   |
+-----------------------------------------------------------------------+
| • Node Structure: prev pointer + val data + next pointer              |
| • JVM Heap Memory: 32 Bytes per node on 64-bit JVM                    |
| • O(1) Unlink Formula: node.prev.next = node.next; node.next.prev = node.prev|
| • Dummy Sentinels: dummyHead & dummyTail eliminate null edge cases    |
| • Primary Application: LRU Cache (LeetCode 146) with HashMap          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [.] I can write `removeNode(Node node)` in $O(1)$ time from memory.
- [ ] I can state the 32-byte JVM memory breakdown of a `Node` object.
- [ ] I can implement a Doubly Linked List using Dummy Head and Tail.
- [ ] I know why LRU Cache uses a Doubly Linked List paired with a HashMap.
- [ ] I can solve LeetCode 146 (LRU Cache).
