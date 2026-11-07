# 05. Linked List Core Operations, Pointer Swapping & Partitioning Mechanics

## 1. Introduction
Mastering core linked list operations—such as arbitrary insertion, value search, node deletion, node swapping without modifying values, list partitioning, and list rotation—is the foundation of technical coding interviews on linear data structures. Operations on linked lists rely on **Pointer Manipulation Invariants** rather than element shifting in memory (as in arrays), enabling **$O(1)$ constant-time node re-linking** when predecessor node references are known.

> **Important:** Swapping nodes in a linked list MUST be performed by **re-linking pointer references (`next` fields)** rather than copying node values (`val` fields)! In enterprise applications, nodes contain heavy data payloads or references; swapping pointers avoids expensive memory copies and preserves external node reference identity!

```
Pointer Re-linking vs Value Copying:
+-----------------------------------------------------------------------------------+
| Value Copying (Bad)    : nodeA.val = nodeB.val (Breaks node identity references)  |
| Pointer Re-linking (Good): Re-wire prevA.next, nodeA.next, prevB.next, nodeB.next   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Pointer Re-linking Invariants

### 2.1 Swapping Two Nodes $A$ and $B$ by Reference ($O(N)$ Search, $O(1)$ Swap)
To swap two nodes $A$ and $B$ in a Singly Linked List without swapping their data values:
1. Locate predecessor node `prevA` for node $A$ and predecessor `prevB` for node $B$.
2. Handle head cases cleanly using a **Dummy Sentinel Node**.
3. Re-wire predecessor references:
   - `if (prevA != null) prevA.next = B; else head = B;`
   - `if (prevB != null) prevB.next = A; else head = A;`
4. Re-wire forward references:
   - `ListNode temp = A.next; A.next = B.next; B.next = temp;`

```
Swapping Node A (10) and Node B (30):
Before : dummy -> (prevA: 5) -> (A: 10) -> (15) -> (prevB: 20) -> (B: 30) -> (35) -> null
Action : 1. prevA.next = B (5.next = 30)
         2. prevB.next = A (20.next = 10)
         3. A.next <-> B.next swap (10.next = 35, 30.next = 15)
After  : dummy -> (5) -> (B: 30) -> (15) -> (20) -> (A: 10) -> (35) -> null ✅
```

### 2.2 List Partitioning Around Value $X$ (LeetCode 86)
Given a linked list and a target value $X$, partition the list such that all nodes less than $X$ come before nodes greater than or equal to $X$:
* Maintain two separate lists using Dummy Nodes: **`lessDummy`** and **`greaterDummy`**.
* Traverse original list:
  - If `curr.val < X`: Append to `lessTail.next = curr; lessTail = lessTail.next;`.
  - Else (`curr.val >= X`): Append to `greaterTail.next = curr; greaterTail = greaterTail.next;`.
* Terminate `greaterTail.next = null` to prevent cycles!
* Connect lists: **`lessTail.next = greaterDummy.next`**.

```
Partitioning List around X = 3:
Original List : [ 1, 4, 3, 2, 5, 2 ]
Less List     : lessDummy -> 1 -> 2 -> 2
Greater List  : greaterDummy -> 4 -> 3 -> 5
Connected     : 1 -> 2 -> 2 -> 4 -> 3 -> 5 -> null ✅
```

> **Memory Trick:** **"Partition List: Create lessDummy and greaterDummy! Connect lessTail.next = greaterDummy.next and set greaterTail.next = null!"**

---

## 3. Characteristics & List Rotation Mechanics (LeetCode 61)

### 3.1 Rotate List Right by $K$ Places
Given a linked list, rotate the list to the right by $K$ places:
1. If `head == null || head.next == null || k == 0`, return `head`.
2. Compute list length $N$ and find the tail node `tail`.
3. Normalize $K$: `k = k % N`. If `k == 0`, return `head`.
4. Connect tail to head to form a **Circular Loop**: `tail.next = head`.
5. Find the new tail position at step $N - k - 1$ from `head`: `newTail`.
6. New head is `newHead = newTail.next`.
7. Break circular loop: **`newTail.next = null`**.

```
Rotate Right by K = 2 on List [1, 2, 3, 4, 5] (N = 5):
Normalized K = 2 % 5 = 2.
1. Connect tail(5) to head(1): 1 -> 2 -> 3 -> 4 -> 5 -> 1 (Ring)
2. New Tail index: 5 - 2 - 1 = 2 (Node 3).
3. New Head: Node 4 (3.next).
4. Break loop: 3.next = null.
Result: [4, 5, 1, 2, 3] ✅ (O(N) Time, O(1) Space!)
```

---

## 4. Internal Working Mechanics
Tracing Partition List (LeetCode 86) on `[1, 4, 3, 2, 5, 2]`, `X = 3`:

```
Init: lessDummy(0), greaterDummy(0)
      lessTail = lessDummy, greaterTail = greaterDummy

Node 1 (<3) : lessTail.next = 1; lessTail = 1.
Node 4 (>=3): greaterTail.next = 4; greaterTail = 4.
Node 3 (>=3): greaterTail.next = 3; greaterTail = 3.
Node 2 (<3) : lessTail.next = 2; lessTail = 2.
Node 5 (>=3): greaterTail.next = 5; greaterTail = 5.
Node 2 (<3) : lessTail.next = 2; lessTail = 2.

End Traversal:
1. Terminate greater tail: greaterTail.next = null (5.next = null).
2. Connect partitions   : lessTail.next = greaterDummy.next (2.next = 4).

Resulting List: 1 -> 2 -> 2 -> 4 -> 3 -> 5 -> null ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
List Partitioning Dual-Pointer Topology:

```
Original List:  [ 1 ] -> [ 4 ] -> [ 3 ] -> [ 2 ] -> [ 5 ] -> [ 2 ] -> null
                           |        |        |        |        |
                           v        v        |        v        |
Less List    : lessDummy -> 1 --------------> 2 --------------> 2
                                                               |
Greater List : greaterDummy -------> 4 -----> 3 -----> 5 ------+
                                                       |
                                                     null
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Node Swapping, List Partitioning (LeetCode 86), and List Rotation (LeetCode 61):

```java
import java.util.*;

public class CoreOperationsMaster {

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

    // 1. Swap Two Nodes by Reference O(N) Search, O(1) Swap
    public static ListNode swapNodes(ListNode head, int valA, int valB) {
        if (valA == valB || head == null) return head;

        ListNode dummy = new ListNode(0, head);
        ListNode prevA = null, currA = null;
        ListNode prevB = null, currB = null;

        ListNode prev = dummy;
        while (prev.next != null) {
            if (prev.next.val == valA) {
                prevA = prev;
                currA = prev.next;
            }
            if (prev.next.val == valB) {
                prevB = prev;
                currB = prev.next;
            }
            prev = prev.next;
        }

        // If either node does not exist, return original list
        if (currA == null || currB == null) return head;

        // Re-wire predecessor pointers
        prevA.next = currB;
        prevB.next = currA;

        // Re-wire next pointers
        ListNode temp = currA.next;
        currA.next = currB.next;
        currB.next = temp;

        return dummy.next;
    }

    // 2. Partition List Around Value X (LeetCode 86) O(N) Time, O(1) Auxiliary Space
    public static ListNode partition(ListNode head, int x) {
        ListNode lessDummy = new ListNode(0);
        ListNode greaterDummy = new ListNode(0);

        ListNode lessTail = lessDummy;
        ListNode greaterTail = greaterDummy;
        ListNode curr = head;

        while (curr != null) {
            if (curr.val < x) {
                lessTail.next = curr;
                lessTail = lessTail.next;
            } else {
                greaterTail.next = curr;
                greaterTail = greaterTail.next;
            }
            curr = curr.next;
        }

        // Terminate greater list to prevent cycle!
        greaterTail.next = null;
        // Connect less list tail to greater list head
        lessTail.next = greaterDummy.next;

        return lessDummy.next;
    }

    // 3. Rotate List Right by K Places (LeetCode 61) O(N) Time, O(1) Auxiliary Space
    public static ListNode rotateRight(ListNode head, int k) {
        if (head == null || head.next == null || k == 0) return head;

        // Step 1: Compute length and find tail
        int length = 1;
        ListNode tail = head;
        while (tail.next != null) {
            tail = tail.next;
            length++;
        }

        // Step 2: Normalize K
        k = k % length;
        if (k == 0) return head;

        // Step 3: Connect tail to head to form ring
        tail.next = head;

        // Step 4: Find new tail position at (length - k - 1)
        int stepsToNewTail = length - k - 1;
        ListNode newTail = head;
        for (int i = 0; i < stepsToNewTail; i++) {
            newTail = newTail.next;
        }

        // Step 5: Set new head and break ring
        ListNode newHead = newTail.next;
        newTail.next = null;

        return newHead;
    }
}
```

> **Quick Syntax:**
```java
// Partition List Linkage Syntax
greaterTail.next = null; // Mandatory cycle prevention!
lessTail.next = greaterDummy.next;
```

---

## 7. Concrete Problem Examples
* **LeetCode 86 - Partition List**: Preserving relative order around target $X$.
* **LeetCode 61 - Rotate List**: Right rotation by $K$ places using circular ring.
* **LeetCode 24 - Swap Nodes in Pairs**: Pairwise node re-linking.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing List Partitioning and List Rotation:

```java
public class CoreOperationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Partition List (LeetCode 86, X = 3) ===");
        CoreOperationsMaster.ListNode head = new CoreOperationsMaster.ListNode(1);
        head.next = new CoreOperationsMaster.ListNode(4);
        head.next.next = new CoreOperationsMaster.ListNode(3);
        head.next.next.next = new CoreOperationsMaster.ListNode(2);
        head.next.next.next.next = new CoreOperationsMaster.ListNode(5);
        head.next.next.next.next.next = new CoreOperationsMaster.ListNode(2);

        CoreOperationsMaster.ListNode partitioned = CoreOperationsMaster.partition(head, 3);
        System.out.print("Partitioned List: ");
        while (partitioned != null) {
            System.out.print(partitioned.val + " -> ");
            partitioned = partitioned.next;
        }
        System.out.println("null"); // Output: 1 -> 2 -> 2 -> 4 -> 3 -> 5 -> null

        System.out.println("\n=== 2. Rotate List Right (LeetCode 61, K = 2) ===");
        CoreOperationsMaster.ListNode list2 = new CoreOperationsMaster.ListNode(1);
        list2.next = new CoreOperationsMaster.ListNode(2);
        list2.next.next = new CoreOperationsMaster.ListNode(3);
        list2.next.next.next = new CoreOperationsMaster.ListNode(4);
        list2.next.next.next.next = new CoreOperationsMaster.ListNode(5);

        CoreOperationsMaster.ListNode rotated = CoreOperationsMaster.rotateRight(list2, 2);
        System.out.print("Rotated List: ");
        while (rotated != null) {
            System.out.print(rotated.val + " -> ");
            rotated = rotated.next;
        }
        System.out.println("null"); // Output: 4 -> 5 -> 1 -> 2 -> 3 -> null
    }
}
```

---

## 9. Complexity Analysis

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Node Swap by Reference** | $O(N)$ Search | $O(N)$ Linear | $O(N)$ Linear | **$O(1)$ In-Place ⚡**|
| **Partition List (86)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ In-Place ⚡**|
| **Rotate List (61)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ In-Place ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **$K$ Larger Than List Length ($K > N$)**: Handled using modulo: `k = k % length`.
* **Cycle Creation in Partition List**: If `greaterTail.next` is not set to `null`, a infinite cycle is created! Always set `greaterTail.next = null`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Terminate `greaterTail.next = null` in Partition List**:
  - If the last node in the original list went into the `less` list, the last node in `greater` list still points to it $\implies$ Infinite Memory Cycle!
  - **Always explicitly execute `greaterTail.next = null`**.
* **Swapping Data Values Instead of Pointers**: Swapping `nodeA.val` and `nodeB.val` alters object state instead of list structure.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `greaterTail.next = null` is Mandatory:
> When building two separate lists (`lessDummy` and `greaterDummy`) by re-linking existing nodes, the last node added to `greaterTail` might still point to a node that was added to `lessTail`.
> Failing to set `greaterTail.next = null` creates a **Cycle in the Linked List**, causing infinite loop crashes during iteration!

> **Memory Trick:** **"Always set greaterTail.next = null after partitioning to break memory cycles!"**

---

## 13. System & Implementation Comparisons

| Feature | Pointer Re-linking Partitioning | Array Element Shifting |
| :--- | :--- | :--- |
| **Memory Allocation** | **Zero Allocation ($O(1)$ Space) ⚡**| $O(N)$ New Array |
| **Node Identity** | Preserved | Overwritten |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(N)$ |

---

## 14. How to Recognize This in Questions
* **"Partition list around value X preserving relative order"** $\rightarrow$ LeetCode 86 (`lessDummy` and `greaterDummy`).
* **"Rotate list to the right by K places"** $\rightarrow$ LeetCode 61 (Ring creation + `k % length` offset break).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is `k = k % length` required when rotating a linked list right by K places?**  
  *A:* Because rotating a list of length $N$ by $N$ places results in the exact same original list. Modulo operation `k % length` eliminates redundant full-circle rotations.
* **Q: How does `partition` preserve relative order of elements in LeetCode 86?**  
  *A:* By traversing the list sequentially and appending nodes to `lessTail` or `greaterTail` in the exact order they appear, relative ordering within both partitions is strictly preserved.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST CORE OPERATIONS & PARTITIONING            |
+-----------------------------------------------------------------------+
| • Swap by Reference: Re-wire prevA.next, prevB.next, nodeA.next, nodeB.next|
| • Partition List (86): Dual dummy nodes (lessDummy & greaterDummy)    |
| • Cycle Guard: ALWAYS set greaterTail.next = null!                    |
| • Rotate List (61): Compute length -> k = k % len -> Form circular ring|
|   Find newTail at (len - k - 1) -> newHead = newTail.next -> break ring|
| • Complexity: All core operations run in O(N) Time & O(1) Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `partition` (LeetCode 86) with `lessDummy` and `greaterDummy`.
- [ ] I know why `greaterTail.next = null` is mandatory to prevent cycles.
- [ ] I can write `rotateRight` (LeetCode 61) using the circular ring method.
- [ ] I can swap two nodes by pointer references without modifying values.
- [ ] I know why `k = k % length` is used in list rotations.
