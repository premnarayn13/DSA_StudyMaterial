# 02. Singly Linked List Architecture, Core Operations & Pointer Manipulation

## 1. Introduction
A **Singly Linked List** is the foundational variant of linked data structures where each node contains a single forward pointer (`next`) pointing to the subsequent node in the sequence. In computer science and technical coding interviews, mastering Singly Linked List pointer manipulation—such as node insertion, arbitrary deletion, index traversal, and in-place pointer reversal—is a non-negotiable fundamental skill.

> **Important:** In a Singly Linked List, pointer navigation is strictly **one-way (Forward Only)**. Finding or deleting the node BEFORE a target node requires traversing from the `head` pointer or maintaining a `prev` tracking reference!

```
Singly Linked List Direction Topology:
+-----------------------------------------------------------------------------------+
| Head -> [ Node 1 ] -> [ Node 2 ] -> [ Node 3 ] -> null  (Forward Traversal Only)|
| Tail -> Points to [ Node 3 ]                            (Tail.next == null)       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Pointer Re-linking Mechanics

### 2.1 Inserting at Index $K$ ($O(K)$ Time)
To insert a new node `newNode` at 0-based index $K$:
1. If $K = 0$: Insert at head (`newNode.next = head; head = newNode;`).
2. Else: Traverse $K - 1$ steps from `head` to reach the predecessor node `prev`.
3. Re-link pointers:
   - `newNode.next = prev.next`
   - `prev.next = newNode`

```
Inserting Node (Val 15) at Index 2:
Before : ( Head: 5 ) -> ( Index 1: 10 ) ----------> ( Index 2: 20 ) -> null
                               ^                       ^
                              prev                    prev.next

Action : 1. newNode.next = prev.next (15.next = 20)
         2. prev.next = newNode      (10.next = 15)

After  : ( Head: 5 ) -> ( Index 1: 10 ) -> ( Index 2: 15 ) -> ( Index 3: 20 ) -> null ✅
```

### 2.2 Deleting Node at Index $K$ ($O(K)$ Time)
To delete a node at 0-based index $K$:
1. If $K = 0$: Delete head (`head = head.next`).
2. Else: Traverse $K - 1$ steps to reach predecessor `prev`.
3. Node to delete: `target = prev.next`.
4. Bypass target node: `prev.next = target.next`.
5. Nullify target pointer: `target.next = null` (for garbage collection).

```
Deleting Node at Index 1 (Val 10):
Before : ( Head: 5 ) -> ( Index 1: 10 ) -> ( Index 2: 20 ) -> null
           ^               ^
          prev           target

Action : prev.next = target.next (5.next = 20)

After  : ( Head: 5 ) ---------------------> ( Index 1: 20 ) -> null ✅
```

> **Memory Trick:** **"Insertion: Set newNode.next = prev.next FIRST, then prev.next = newNode! Deletion: Set prev.next = target.next!"**

---

## 3. Characteristics & Dummy Node Optimization

### 3.1 The Dummy Sentinel Head Node Pattern
When performing node insertions and deletions, handling index `0` (head node) usually requires special `if (index == 0)` branching logic.
By prepending a **Dummy Sentinel Node (`ListNode dummy = new ListNode(0); dummy.next = head;`)**, index `0` becomes an internal node relative to `dummy`!
* **Benefit**: Eliminates special null checks and head-node edge case branching, allowing clean unified loop pointer manipulation.

```
Dummy Sentinel Node Layout:
Dummy Head (val 0) -> [ Node 0 (Head) ] -> [ Node 1 ] -> [ Node 2 ] -> null
     ^                        ^
Predecessor for Index 0   Target Index 0
```

---

## 4. Internal Working Mechanics
Tracing Insertion of value `15` at Index `2` using Dummy Sentinel Head:

```
List: [5, 10, 20], Target Index = 2, Value = 15

Step 1: Create Dummy Sentinel: dummy -> [5, 10, 20]
Step 2: Advance `prev` pointer index 2 times from dummy:
        - i = 0: prev = dummy (val 0)
        - i = 1: prev = node(5)
        - i = 2: prev = node(10)
Step 3: Perform re-linking:
        - newNode = new Node(15)
        - newNode.next = prev.next (15.next = 20)
        - prev.next = newNode      (10.next = 15)
Step 4: Return `dummy.next` as updated list head!

Result: [5, 10, 15, 20] ✅ (Zero special head checks required!)
```

---

## 5. Visual Diagram
Singly Linked List Dummy Sentinel Head Pointer Topology:

```
          +-------------+      +-------------+      +-------------+      +-------------+
dummy --> | val: 0      | ---> | val: 5 (H)  | ---> | val: 10     | ---> | val: 20     | ---> null
          | next: 0x100 |      | next: 0x200 |      | next: 0x300 |      | next: null  |
          +-------------+      +-------------+      +-------------+      +-------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a complete Singly Linked List class featuring Dummy Head insertion, deletion by index, deletion by value, reversal, and search:

```java
import java.util.*;

public class SinglyLinkedListMaster {

    public static class ListNode {
        public int val;
        public ListNode next;

        public ListNode(int val) {
            this.val = val;
            this.next = null;
        }

        public ListNode(int val, ListNode next) {
            this.val = val;
            this.next = next;
        }
    }

    public static class SinglyLinkedList {
        private ListNode head;
        private int size;

        public SinglyLinkedList() {
            this.head = null;
            this.size = 0;
        }

        public int size() { return size; }
        public boolean isEmpty() { return head == null; }

        // 1. Get Element at Index O(K) Time
        public int get(int index) {
            if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Invalid index: " + index);
            ListNode curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
            return curr.val;
        }

        // 2. Insert at Index O(K) Time (Dummy Head Pattern)
        public void addAtIndex(int index, int val) {
            if (index < 0 || index > size) throw new IndexOutOfBoundsException("Invalid index: " + index);

            ListNode dummy = new ListNode(0, head);
            ListNode prev = dummy;

            for (int i = 0; i < index; i++) {
                prev = prev.next;
            }

            ListNode newNode = new ListNode(val, prev.next);
            prev.next = newNode;

            head = dummy.next; // Restore head
            size++;
        }

        // 3. Delete at Index O(K) Time (Dummy Head Pattern)
        public int deleteAtIndex(int index) {
            if (index < 0 || index >= size) throw new IndexOutOfBoundsException("Invalid index: " + index);

            ListNode dummy = new ListNode(0, head);
            ListNode prev = dummy;

            for (int i = 0; i < index; i++) {
                prev = prev.next;
            }

            ListNode target = prev.next;
            prev.next = target.next;
            target.next = null; // Unlink target for GC

            head = dummy.next; // Restore head
            size--;
            return target.val;
        }

        // 4. Delete First Occurrence of Value O(N) Time
        public boolean removeValue(int val) {
            ListNode dummy = new ListNode(0, head);
            ListNode prev = dummy;

            while (prev.next != null) {
                if (prev.next.val == val) {
                    ListNode target = prev.next;
                    prev.next = target.next;
                    target.next = null;
                    head = dummy.next;
                    size--;
                    return true;
                }
                prev = prev.next;
            }

            return false; // Value not found
        }

        // 5. In-Place Iterative Reversal O(N) Time, O(1) Space
        public void reverse() {
            ListNode prev = null;
            ListNode curr = head;

            while (curr != null) {
                ListNode nextTemp = curr.next;
                curr.next = prev;
                prev = curr;
                curr = nextTemp;
            }

            head = prev;
        }

        public int[] toArray() {
            int[] arr = new int[size];
            ListNode curr = head;
            int i = 0;
            while (curr != null) {
                arr[i++] = curr.val;
                curr = curr.next;
            }
            return arr;
        }
    }
}
```

> **Quick Syntax:**
```java
// Dummy Head Insertion Template
ListNode dummy = new ListNode(0, head);
ListNode prev = dummy;
for (int i = 0; i < index; i++) prev = prev.next;
prev.next = new ListNode(val, prev.next);
head = dummy.next;
```

---

## 7. Concrete Problem Examples
* **LeetCode 206 - Reverse Linked List**: In-place 3-pointer reversal.
* **LeetCode 203 - Remove Linked List Elements**: Deleting values using dummy head.
* **LeetCode 707 - Design Linked List**: Standard singly linked list design.

---

## 8. Java Code Demonstration & Dry Run
Demonstration adding elements at indices, deleting elements, reversing list, and inspecting output:

```java
public class SinglyLinkedListDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Building Singly Linked List ===");
        SinglyLinkedListMaster.SinglyLinkedList list = 
            new SinglyLinkedListMaster.SinglyLinkedList();

        list.addAtIndex(0, 10); // [10]
        list.addAtIndex(1, 20); // [10, 20]
        list.addAtIndex(1, 15); // [10, 15, 20]
        list.addAtIndex(0, 5);  // [5, 10, 15, 20]

        System.out.println("Elements: " + Arrays.toString(list.toArray())); // Output: [5, 10, 15, 20]

        System.out.println("\n=== 2. Deleting Element at Index 2 (Val 15) ===");
        list.deleteAtIndex(2);
        System.out.println("After Delete Index 2: " + Arrays.toString(list.toArray())); // Output: [5, 10, 20]

        System.out.println("\n=== 3. In-Place Reversing List ===");
        list.reverse();
        System.out.println("Reversed Elements:   " + Arrays.toString(list.toArray())); // Output: [20, 10, 5]
    }
}
```

---

## 9. Complexity Analysis

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Insert Head (`index 0`)**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ |
| **Insert at Index $K$** | $O(1)$ | $O(K)$ Linear | $O(N)$ Linear | $O(1)$ |
| **Delete at Index $K$** | $O(1)$ | $O(K)$ Linear | $O(N)$ Linear | $O(1)$ |
| **In-Place Reversal** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ In-Place ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Inserting at Index 0**: Handled cleanly via `dummy.next = head`.
* **Inserting at Index `size` (Tail)**: Loops $size$ steps, appends to end of list.
* **Out of Bounds Index (`index < 0 || index > size`)**: Throws `IndexOutOfBoundsException`.

---

## 11. Common Mistakes & Anti-Patterns
* **Updating `prev.next` BEFORE Setting `newNode.next`**:
  - `prev.next = newNode; newNode.next = prev.next;` (Causes `newNode.next` to point to ITSELF, creating a memory loop!).
  - **Always assign `newNode.next = prev.next` FIRST, then `prev.next = newNode`**.
* **Losing Head Reference When Deleting Index 0**: Deleting head without updating `head = head.next` leaves stale references.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The 3-Pointer Iterative Reversal Algorithm:
> Maintaining `prev`, `curr`, and `nextTemp` pointers:
> 1. `nextTemp = curr.next` (Save next node reference).
> 2. `curr.next = prev` (Reverse current pointer direction).
> 3. `prev = curr` (Advance prev pointer).
> 4. `curr = nextTemp` (Advance curr pointer).

> **Memory Trick:** **"Reversal loop: Save nextTemp -> Reverse pointer -> Advance prev -> Advance curr!"**

---

## 13. System & Implementation Comparisons

| Feature | Dummy Head Pattern | Standard Branching Pattern |
| :--- | :--- | :--- |
| **Index 0 Special Check** | **NO (Unified Loop) ⚡** | Required `if (index == 0)` |
| **Code Length** | Short & Clean | Longer & Error Prone |
| **Auxiliary Memory** | 1 Temporary Stack Object | 0 Objects |

---

## 14. How to Recognize This in Questions
* **"Delete a node in a singly linked list given only access to that node"** $\rightarrow$ LeetCode 237 (`node.val = node.next.val; node.next = node.next.next;`).
* **"Reverse a singly linked list in-place"** $\rightarrow$ LeetCode 206 (3-pointer iterative reversal).

---

## 15. Frequently Asked Interview Questions
* **Q: How does LeetCode 237 delete a node in $O(1)$ time without access to the head pointer?**  
  *A:* Copy the value of the next node into the current node (`node.val = node.next.val`), then bypass the next node (`node.next = node.next.next`).
* **Q: Why does the Dummy Head Node pattern prevent `NullPointerException` during head deletion?**  
  *A:* Because `dummy.next` always points to `head`, so deleting `index 0` executes `prev.next = target.next` where `prev` is `dummy`, completely eliminating special null head checks.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SINGLY LINKED LIST OPERATIONS & REVERSAL              |
+-----------------------------------------------------------------------+
| • Pointer Insertion: newNode.next = prev.next; prev.next = newNode    |
| • Pointer Deletion: target = prev.next; prev.next = target.next       |
| • Dummy Sentinel Head: ListNode dummy = new ListNode(0, head);        |
| • Eliminates index 0 special if-branching checks!                     |
| • 3-Pointer Reversal: nextTemp = curr.next; curr.next = prev;         |
|   prev = curr; curr = nextTemp;                                       |
| • Complexity: Insert/Delete at head O(1) ⚡; Index traversal O(K)      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `addAtIndex` using the Dummy Head pattern in under 3 minutes.
- [ ] I can write 3-pointer iterative reversal (`prev`, `curr`, `nextTemp`).
- [ ] I can write $O(1)$ value-copying deletion for LeetCode 237.
- [ ] I know why `newNode.next` must be set BEFORE `prev.next`.
- [ ] I can solve LeetCode 203 (Remove Linked List Elements).
