# 01. Singly Linked List Fundamentals & Node Pointer Operations

## 1. Introduction
A **Singly Linked List** is a linear data structure composed of self-referential **Nodes** stored in non-contiguous heap memory. Each node contains a data payload and a single pointer (`next`) referencing the subsequent node in the sequence. In technical coding interviews, linked lists test pointer manipulation, memory allocation mechanics, dummy head nodes, and structural traversal without breaking reference chains.

> **Important:** Unlike arrays, linked lists do NOT support $O(1)$ random index access. Accessing the $K$-th element requires traversing $K$ pointer links from `head` in **$O(K)$ linear time**. However, inserting or deleting a node at a known pointer position takes **$O(1)$ constant time**!

## 2. Core Concepts
* **Node Architecture**: A standalone object containing value `val` and reference pointer `next`:
  ```java
  class ListNode {
      int val;
      ListNode next;
      ListNode(int val) { this.val = val; }
  }
  ```
* **Head Pointer**: A pointer reference marking the entry point of the linked list. If `head == null`, the list is empty.
* **Tail Pointer**: The final node in the list whose `next` reference points to `null`.
* **Dummy Head Node Trick**: Allocating a sentinel `ListNode dummy = new ListNode(-1); dummy.next = head;` to unify edge-case handling for insertions or deletions at the start of the list.

> **Memory Trick:** **"Always use a Dummy Head Node (dummy.next = head) when inserting or deleting at the head of a linked list!"**

## 3. Characteristics / Properties
* **Non-Contiguous Heap Allocation**: Each node is allocated independently on the JVM Heap. Nodes are connected via memory references rather than contiguous RAM offsets.
* **Cache Locality Penalty**: Because nodes are scattered across Heap RAM, sequential linked list traversal triggers frequent CPU L1/L2 Cache Misses compared to arrays.
* **No Resizing Penalty**: Dynamically grows and shrinks per element without array reallocation or copying overhead.

```
Singly Linked List Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation             | Head (Position 0) | Tail (Known Tail) | Arbitrary Position|
+-----------------------+-------------------+-------------------+-------------------+
| Access / Read (`get`)| O(1)              | O(N)              | O(N)              |
| Insertion (`insert`)  | O(1) ⚡           | O(1) (with tail)  | O(N) traversal    |
| Deletion (`delete`)   | O(1) ⚡           | O(N) (needs prev) | O(N) traversal    |
| Search (`search`)     | O(1) (if target 0)| O(N)              | O(N)              |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Insertion at Head vs Insertion after Target Node:

```
[ INSERTION AT HEAD: O(1) Time ]
New Node: [ 99 | next ]
Current List: Head -> [ 10 | next ] -> [ 20 | null ]

Step 1: newNode.next = head;       (New Node points to [ 10 ])
Step 2: head = newNode;           (Head now points to [ 99 ])
Result: Head -> [ 99 | next ] -> [ 10 | next ] -> [ 20 | null ] ✅

[ DELETION AFTER TARGET NODE: O(1) Time ]
List: [ 10 | next ] -> [ 20 | next ] -> [ 30 | null ]
Target node: curr = [ 10 ]

Step 1: curr.next = curr.next.next; (Bypasses [ 20 ], pointing [ 10 ] directly to [ 30 ])
Node [ 20 ] is unlinked and reclaimed by JVM Garbage Collector! ✅
```

## 5. Visual Diagram
Singly Linked List Memory Pointer Layout & Dummy Head:

```
Dummy Head Node Pattern:
[ Dummy (-1) | next ] ---> [ Node A (10) | next ] ---> [ Node B (20) | next ] ---> null
      ^                           ^
  dummyHead                     head

Inserting before Head:
newNode.next = dummy.next;
dummy.next = newNode;
Return: dummy.next; (Automatically returns new valid head!)
```

## 6. Operations / Algorithms
Singly Linked List Master Operations Implementation:

```java
public class SinglyLinkedListMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Insert at Head O(1) Time
    public static ListNode insertAtHead(ListNode head, int val) {
        ListNode newNode = new ListNode(val);
        newNode.next = head;
        return newNode; // New head
    }

    // 2. Insert at Tail O(N) Time (or O(1) if tail pointer maintained)
    public static ListNode insertAtTail(ListNode head, int val) {
        ListNode newNode = new ListNode(val);
        if (head == null) return newNode;

        ListNode curr = head;
        while (curr.next != null) {
            curr = curr.next;
        }
        curr.next = newNode;
        return head;
    }

    // 3. Delete Value using Dummy Head O(N) Time, O(1) Space
    public static ListNode deleteValue(ListNode head, int target) {
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode curr = dummy;

        while (curr.next != null) {
            if (curr.next.val == target) {
                curr.next = curr.next.next; // Unlink target node
                break; // Stop after first deletion
            }
            curr = curr.next;
        }

        return dummy.next; // Return updated head
    }
}
```

> **Quick Syntax:**
```java
// Dummy Head Pattern Idiom
ListNode dummy = new ListNode(-1);
dummy.next = head;
ListNode curr = dummy;
// Perform pointer operations...
return dummy.next;
```

## 7. Examples
* **LeetCode 203 - Remove Linked List Elements**: Deleting all nodes matching target value using Dummy Head.
* **LeetCode 237 - Delete Node in a Linked List**: Deleting node given only reference to that node (Copy value from `node.next` and bypass).
* **LeetCode 21 - Merge Two Sorted Lists**: Merging lists via Dummy Head and pointer comparisons.

## 8. Java Code
Complete interview-ready Java suite demonstrating Singly Linked List operations, Dummy Head utilization, and node deletion:

```java
public class SinglyLinkedListDemo {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Print Linked List Helper
    public static void printList(ListNode head) {
        ListNode curr = head;
        StringBuilder sb = new StringBuilder();
        while (curr != null) {
            sb.append(curr.val).append(" -> ");
            curr = curr.next;
        }
        sb.append("null");
        System.out.println(sb.toString());
    }

    // 2. Delete All Occurrences of Value (LeetCode 203) O(N) Time, O(1) Space
    public static ListNode removeElements(ListNode head, int val) {
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode curr = dummy;

        while (curr.next != null) {
            if (curr.next.val == val) {
                curr.next = curr.next.next; // Unlink matching node
            } else {
                curr = curr.next; // Advance only when no deletion occurred
            }
        }

        return dummy.next;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct: 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6 -> null
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(6);
        head.next.next.next = new ListNode(3);
        head.next.next.next.next = new ListNode(4);
        head.next.next.next.next.next = new ListNode(5);
        head.next.next.next.next.next.next = new ListNode(6);

        System.out.print("Original List: ");
        printList(head);

        // Delete all '6's
        head = removeElements(head, 6);
        System.out.print("After Removing 6s: ");
        printList(head); // Output: 1 -> 2 -> 3 -> 4 -> 5 -> null
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Insert at Head** | **$O(1)$ Constant**| **$O(1)$** | Update head reference |
| **Insert at Tail (No Tail Ref)**| $O(N)$ Linear | **$O(1)$** | Requires traversing to end |
| **Delete Node (Known Prev)** | **$O(1)$ Constant**| **$O(1)$** | `prev.next = prev.next.next` |
| **Search / Get Index $K$** | $O(K)$ | **$O(1)$** | Pointer traversal |

## 10. Edge Cases
* **Empty List (`head == null`)**: Attempting `head.val` or `head.next` throws `NullPointerException`. Guard with `if (head == null)`.
* **Deleting the Head Node**: Using a **Dummy Head Node** (`dummy.next = head`) unifies deleting the first node with deleting internal nodes.
* **List with Single Node**: Operations must handle transition from 1 node to 0 nodes (`null`) cleanly.

## 11. Common Mistakes
* Dereferencing a `null` pointer (`curr.next.val` when `curr.next == null`). Always verify `curr.next != null` inside loop conditions.
* Losing reference to the rest of the list during insertion by overwriting `curr.next` before saving the trailing node chain!
* Forgetting to update `curr` pointer inside traversal while loops (causes infinite loops!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Insertion Pointer Order Rule:
> To insert `newNode` between `prev` and `curr`:
> 1. Set **`newNode.next = curr;`** FIRST!
> 2. Set **`prev.next = newNode;`** SECOND!
> Reversing these steps breaks the link to `curr`, causing a memory leak loss of the rest of the list!

> **Memory Trick:** **"Connect the New Node's next FIRST, then point prev to New Node!"**

## 13. Comparisons
| Feature | Primitive Array (`int[]`) | Singly Linked List (`ListNode`) |
| :--- | :--- | :--- |
| **Memory Allocation** | Contiguous block | Scattered heap nodes |
| **Access Time** | **$O(1)$ Random Access** | $O(N)$ Linear Traversal |
| **Insertion at Head** | $O(N)$ (Shifting required) | **$O(1)$ Constant** |
| **Cache Locality** | **High (CPU Cache Hits)** | Low (CPU Cache Misses) |

## 14. How to Recognize This in Questions
* **"Modify linked list in-place with O(1) auxiliary space"** $\rightarrow$ Pointer manipulation with Dummy Head.
* **"Remove elements matching value / Remove head"** $\rightarrow$ Dummy Head Pattern (`dummy.next = head`).

## 15. Frequently Asked Interview Questions
* **Q: Why is a Dummy Head Node used in Linked List problems?**  
  *A:* Dummy Head Node (`dummy.next = head`) eliminates special conditional branches for operations modifying the head node. It ensures `curr.next` always points to a valid target node, simplifying edge case handling.
* **Q: What happens to unlinked nodes in Java?**  
  *A:* When a node is unlinked (`curr.next = curr.next.next`), no variables reference that node object anymore. The JVM Garbage Collector automatically identifies and reclaims its heap memory during the next GC cycle.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SINGLY LINKED LIST FUNDAMENTALS                       |
+-----------------------------------------------------------------------+
| • Node Structure: int val; ListNode next;                             |
| • Dummy Head Rule: ListNode dummy = new ListNode(-1); dummy.next=head |
| • Insertion Order: newNode.next = curr FIRST, then prev.next = newNode|
| • Deletion Rule: prev.next = prev.next.next (Unlinks target node)     |
| • Head Insertion: O(1) Constant | Access Index K: O(K) Traversal      |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the `ListNode` class definition from memory.
- [ ] I know why Dummy Head (`dummy.next = head`) simplifies head deletions.
- [ ] I can write the 2-step pointer order for node insertion without breaking list links.
- [ ] I can delete nodes matching a target value in $O(N)$ time and $O(1)$ space.
- [ ] I understand JVM garbage collection of unlinked nodes.
