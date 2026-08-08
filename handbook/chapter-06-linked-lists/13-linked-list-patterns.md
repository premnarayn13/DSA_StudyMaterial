# 13. Linked List Problem Patterns, Decision Matrix & Production Templates

## 1. Introduction
Solving linked list interview problems cleanly under high-pressure technical coding rounds requires instant pattern recognition. Linked list problems can be categorized into **6 Core Pattern Families**. This section provides a master decision matrix mapping problem descriptions to optimal pointer strategies, along with copy-paste production Java templates.

> **Important:** Master the primary linked list invariants:
> 1. **Dummy Sentinel Node**: Always prepend `ListNode dummy = new ListNode(0, head)` whenever head operations or list partitions occur.
> 2. **Fast & Slow Pointers**: Use $2x / 1x$ speed differential for middle finding and cycle detection.
> 3. **3-Pointer Loop**: Use `prev`, `curr`, `nextTemp` for in-place reversal.

---

## 2. Master Linked List Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER LINKED LIST PROBLEM DECISION MATRIX                                                        |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Eliminate head node special checks / partitions" | Dummy Sentinel Node   | `dummy.next = head`   |
| "Find middle / N-th node from end / cycle"        | Fast & Slow Pointers  | `fast` moves 2x       |
| "Reverse entire list or sub-segment in-place"     | 3-Pointer Reversal    | `curr.next = prev`    |
| "Check if list is palindrome in O(1) space"       | Middle + Reverse 2nd  | `isPalindrome` combo  |
| "Find intersection of two lists without memory"   | 2-Pointer Swap        | `pA = pA == null ? B` |
| "Deep copy list with random pointers in O(1) space"| 3-Pass Interleaving   | `A -> A' -> B -> B'`  |
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Dummy Sentinel Head Node Template
* **Signal**: Operations that insert, delete, or partition nodes at or near the head node.

```java
public static ListNode dummySentinelTemplate(ListNode head, int targetVal) {
    ListNode dummy = new ListNode(0, head);
    ListNode prev = dummy;

    while (prev.next != null) {
        if (prev.next.val == targetVal) {
            ListNode target = prev.next;
            prev.next = target.next;
            target.next = null; // GC unlink
        } else {
            prev = prev.next;
        }
    }

    return dummy.next;
}
```

---

## 4. Pattern 2: Fast & Slow Pointer Gap Template
* **Signal**: Finding middle node, single-pass $N$-th node from end.

```java
public static ListNode removeNthFromEndTemplate(ListNode head, int n) {
    ListNode dummy = new ListNode(0, head);
    ListNode fast = dummy, slow = dummy;

    for (int i = 0; i <= n; i++) {
        if (fast == null) return head;
        fast = fast.next;
    }

    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }

    slow.next = slow.next.next;
    return dummy.next;
}
```

---

## 5. Pattern 3: 3-Pointer Iterative Reversal Template
* **Signal**: In-place reversal of entire list or sub-segment.

```java
public static ListNode reverseListTemplate(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;

    while (curr != null) {
        ListNode nextTemp = curr.next;
        curr.next = prev;
        prev = curr;
        curr = nextTemp;
    }

    return prev;
}
```

---

## 6. Pattern 4: Floyd's Cycle Detection & Entry Recovery Template
* **Signal**: Detecting loops or finding cycle entry node in $O(1)$ space.

```java
public static ListNode detectCycleTemplate(ListNode head) {
    if (head == null || head.next == null) return null;
    ListNode slow = head, fast = head;
    boolean hasCycle = false;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            hasCycle = true;
            break;
        }
    }

    if (!hasCycle) return null;

    slow = head;
    while (slow != fast) {
        slow = slow.next;
        fast = fast.next;
    }

    return slow; // Entry node
}
```

---

## 7. Pattern 5: 2-Pointer Swap Intersection Template
* **Signal**: Finding node where two lists merge without extra hash set memory.

```java
public static ListNode intersectionTemplate(ListNode headA, ListNode headB) {
    if (headA == null || headB == null) return null;
    ListNode pA = headA, pB = headB;

    while (pA != pB) {
        pA = (pA == null) ? headB : pA.next;
        pB = (pB == null) ? headA : pB.next;
    }

    return pA;
}
```

---

## 8. Pattern 6: 3-Pass Interleaving Deep Copy Template
* **Signal**: Deep copy linked list with arbitrary `random` pointers in $O(1)$ space.

```java
public static Node copyRandomListTemplate(Node head) {
    if (head == null) return null;

    // Pass 1: Weave A -> A'
    Node curr = head;
    while (curr != null) {
        Node clone = new Node(curr.val);
        clone.next = curr.next;
        curr.next = clone;
        curr = clone.next;
    }

    // Pass 2: Wire random
    curr = head;
    while (curr != null) {
        if (curr.random != null) {
            curr.next.random = curr.random.next;
        }
        curr = curr.next.next;
    }

    // Pass 3: Unweave
    curr = head;
    Node dummy = new Node(0), cloneTail = dummy;
    while (curr != null) {
        Node nextOriginal = curr.next.next;
        Node clone = curr.next;

        cloneTail.next = clone;
        cloneTail = clone;

        curr.next = nextOriginal;
        curr = nextOriginal;
    }

    return dummy.next;
}
```

---

## 9. Edge Case & Trap Checklist
* **Null Pointer Dereference (`NullPointerException`)**: Always check `curr != null` before `curr.next`.
* **Cycle Creation in Partitioning**: Set `greaterTail.next = null` when splitting list into partitions.
* **Loss of Head Node**: Set `dummy.next = head` to preserve head reference during head deletions/reversals.
* **Infinite Loops in Circular List Traversal**: Use `do { ... } while (curr != head)` instead of `while (curr != null)`.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: LINKED LIST PROBLEM PATTERNS                         |
+-----------------------------------------------------------------------+
| 1. Dummy Head: Eliminates special checks when index = 0               |
| 2. Middle Finding: slow 1x, fast 2x -> slow lands on middle node      |
| 3. Remove K-th From End: Advance fast K+1 steps ahead first!          |
| 4. In-Place Reversal: nextTemp = curr.next; curr.next = prev; prev=curr|
| 5. Cycle Recovery: Reset slow to head when meeting point found; move 1x|
| 6. Intersection 2-Pointer: pA = (pA == null) ? headB : pA.next        |
| 7. Partition Cycle Guard: ALWAYS set greaterTail.next = null!         |
| 8. Merge Sort Split: Use 1st middle (fast.next != null && fast.next.next != null)|
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why `greaterTail.next = null` is mandatory in list partitioning.
- [ ] I know how to recover the cycle entry node using Floyd's algorithm.
- [ ] I know why 1st middle split is required in Linked List Merge Sort.
