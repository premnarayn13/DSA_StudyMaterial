# 04. In-Place Pointer Manipulation & Reversal Techniques

## 1. Introduction
In-place pointer manipulation is the core skill required for solving advanced linked list problems in technical coding interviews. Reversing a linked list (LeetCode 206), reversing a subrange of nodes (LeetCode 92), reversing nodes in $K$-group blocks (LeetCode 25), and reordering list nodes (LeetCode 143) test a candidate's ability to manipulate pointer references in **$O(N)$ time and $O(1)$ auxiliary space** without breaking node links.

> **Important:** Reversing a linked list in-place requires **3 pointers**: `prev` (initialized to `null`), `curr` (initialized to `head`), and `nextTemp` (saves `curr.next` before overwriting).

## 2. Core Concepts
* **Iterative 3-Pointer Reversal**: Reversing pointer directions in a single linear pass by setting `curr.next = prev` while advancing `prev` and `curr`.
* **Recursive List Reversal**: Base case `head == null || head.next == null`. Recursive step: `ListNode newHead = reverse(head.next); head.next.next = head; head.next = null;`.
* **Subrange Reversal ($M$ to $N$)**: Reversing nodes strictly between index $M$ and index $N$ using a `prev` anchor pointer and iterative node shifting.
* **$K$-Group Reversal**: Reversing nodes in blocks of size $K$, leaving remaining trailing nodes unchanged if count $< K$.

> **Memory Trick for Iterative Reversal:** **"Save next, Reverse link, Move prev, Move curr!"**
> 1. `nextTemp = curr.next;`
> 2. `curr.next = prev;`
> 3. `prev = curr;`
> 4. `curr = nextTemp;`

## 3. Characteristics / Properties
* **In-Place Memory Guarantee**: Iterative pointer manipulation operates strictly in **$O(1)$ auxiliary space** by modifying pointer references in memory directly.
* **Recursive Stack Space**: Recursive list reversal takes $O(N)$ call stack space (making iterative reversal preferred in interviews for space optimality).

```
Pointer Manipulation Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm / Problem   | Time Complexity   | Space Complexity  | Best Approach     |
+-----------------------+-------------------+-------------------+-------------------+
| Reverse Whole List    | O(N) Linear       | O(1) Constant     | Iterative 3-Pointer⚡|
| Reverse Range [M, N]  | O(N) Linear       | O(1) Constant     | In-Place Shifting |
| Reverse K-Group       | O(N) Linear       | O(1) Constant     | Iterative Blocks  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Iterative 3-Pointer Reversal on `1 -> 2 -> 3 -> null`:

```
Initial State: prev = null, curr = [ 1 ]

Step 1 (curr = 1):
- Save next:  nextTemp = 2
- Reverse:    curr.next = prev (1.next = null)
- Advance:    prev = 1, curr = 2
List State:   null <- 1   2 -> 3 -> null

Step 2 (curr = 2):
- Save next:  nextTemp = 3
- Reverse:    curr.next = prev (2.next = 1)
- Advance:    prev = 2, curr = 3
List State:   null <- 1 <- 2   3 -> null

Step 3 (curr = 3):
- Save next:  nextTemp = null
- Reverse:    curr.next = prev (3.next = 2)
- Advance:    prev = 3, curr = null

Loop terminates (curr == null). Return prev ([ 3 ] is new head!) ✅
Result List: 3 -> 2 -> 1 -> null
```

## 5. Visual Diagram
Pointer Reversal Step Mechanics:

```
Pointers:    prev       curr     nextTemp
              |          |          |
              v          v          v
State:      [ A ]      [ B ] ---> [ C ]

Action:     curr.next = prev  (B.next now points to A!)
            prev = curr       (prev advances to B)
            curr = nextTemp   (curr advances to C)

Result:     [ A ] <--- [ B ]      [ C ]
                        ^           ^
                      prev        curr
```

## 6. Operations / Algorithms
LeetCode 206 Master Implementation:

```java
// 1. Iterative 3-Pointer Reversal O(N) Time, O(1) Auxiliary Space (PREFERRED)
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;

    while (curr != null) {
        ListNode nextTemp = curr.next; // 1. Save next node
        curr.next = prev;              // 2. Reverse current link
        prev = curr;                   // 3. Advance prev
        curr = nextTemp;               // 4. Advance curr
    }

    return prev; // prev is the new head of the reversed list
}

// 2. Recursive List Reversal O(N) Time, O(N) Call Stack Space
public ListNode reverseListRecursive(ListNode head) {
    if (head == null || head.next == null) {
        return head; // Base case: empty or single node list
    }

    ListNode newHead = reverseListRecursive(head.next);
    head.next.next = head; // Make next node point back to head
    head.next = null;      // Discard forward link

    return newHead;
}
```

> **Quick Syntax:**
```java
// 3-Pointer Iterative Reversal Idiom
ListNode nextTemp = curr.next;
curr.next = prev;
prev = curr;
curr = nextTemp;
```

## 7. Examples
* **LeetCode 206 - Reverse Linked List**: Standard iterative 3-pointer reversal.
* **LeetCode 92 - Reverse Linked List II**: Reversing subrange between index $left$ and $right$.
* **LeetCode 25 - Reverse Nodes in k-Group**: Reversing list in $K$-sized blocks in $O(1)$ space.

## 8. Java Code
Complete interview-ready Java suite implementing Iterative Reversal, Recursive Reversal, and Range Reversal (LeetCode 92):

```java
public class PointerManipulationMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Iterative Whole List Reversal O(N) Time, O(1) Space
    public static ListNode reverseList(ListNode head) {
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

    // 2. Reverse Linked List Subrange [left, right] (LeetCode 92) O(N) Time, O(1) Space
    public static ListNode reverseBetween(ListNode head, int left, int right) {
        if (head == null || left == right) return head;

        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode prev = dummy;

        // Step 1: Reach node at position (left - 1)
        for (int i = 0; i < left - 1; i++) {
            prev = prev.next;
        }

        // Step 2: Reverse subrange using head-pointing shift
        ListNode curr = prev.next;
        for (int i = 0; i < right - left; i++) {
            ListNode nextNode = curr.next;
            curr.next = nextNode.next;
            nextNode.next = prev.next;
            prev.next = nextNode;
        }

        return dummy.next;
    }

    // Helper: Print List
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

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct: 1 -> 2 -> 3 -> 4 -> 5 -> null
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);

        System.out.print("Original List: ");
        printList(head);

        // Reverse Range [2, 4] (nodes 2, 3, 4)
        head = reverseBetween(head, 2, 4);
        System.out.print("After Reversing Range [2, 4]: ");
        printList(head); // Output: 1 -> 4 -> 3 -> 2 -> 5 -> null

        // Reverse Entire List
        head = reverseList(head);
        System.out.print("After Reversing Full List: ");
        printList(head); // Output: 5 -> 2 -> 3 -> 4 -> 1 -> null
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Iterative Reversal** | **$O(N)$ Linear** | **$O(1)$ Constant** | Preferred for space optimality ⚡ |
| **Recursive Reversal** | **$O(N)$ Linear** | $O(N)$ Call Stack | Risk of stack overflow on large $N$ |
| **Subrange Reversal [M, N]**| **$O(N)$ Linear** | **$O(1)$ Constant** | Single pass pointer shifts |

## 10. Edge Cases
* **Empty List or Single Node (`head == null || head.next == null`)**: Return `head` immediately.
* **$left == right$ in Range Reversal**: No reversals needed; return `head`.
* **Reversing Range Starting at Index 1 ($left == 1$)**: Dummy Head Node (`dummy.next = head`) cleanly handles updating the head of the entire list.

## 11. Common Mistakes
* Overwriting `curr.next` BEFORE saving `curr.next` into `nextTemp` (loses reference to rest of list!).
* Returning `head` instead of `prev` at the end of iterative reversal (returns the old tail node which now points to `null`!).
* Using recursive reversal when $N > 10,000$ (triggers `StackOverflowError` in Java).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Iterative 4-step reversal sequence:
> 1. `ListNode nextTemp = curr.next;` (Save next link)
> 2. `curr.next = prev;` (Reverse link)
> 3. `prev = curr;` (Advance prev pointer)
> 4. `curr = nextTemp;` (Advance curr pointer)
> Return **`prev`** as the new head when loop finishes!

> **Memory Trick:** **"Save next, Reverse, Advance prev, Advance curr. Return prev at end!"**

## 13. Comparisons
| Metric | Iterative Reversal | Recursive Reversal |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Space Complexity**| **$O(1)$ (In-Place Optimal)** | $O(N)$ (JVM Recursion Call Stack) |
| **Stack Overflow Risk**| ZERO | High for large $N$ |
| **Interview Recommendation** | **PREFERRED** | Secondary |

## 14. How to Recognize This in Questions
* **"Reverse linked list in-place with O(1) space"** $\rightarrow$ Iterative 3-Pointer Reversal (`prev`, `curr`, `nextTemp`).
* **"Reverse subrange of linked list from position M to N"** $\rightarrow$ Dummy Head + Subrange In-Place Shifting.

## 15. Frequently Asked Interview Questions
* **Q: How does `head.next.next = head` work in recursive list reversal?**  
  *A:* In the recursive step, `head.next` is the node immediately following `head`. Setting `head.next.next = head` makes that follower node point BACK to `head`, reversing the link direction. Setting `head.next = null` breaks the original forward link to prevent a 2-node cycle.
* **Q: Why is Dummy Head Node essential for LeetCode 92 (Reverse Subrange)?**  
  *A:* When $left = 1$, the subrange being reversed includes the original head node of the list. A Dummy Head Node (`dummy.next = head`) ensures `prev` points to `dummy` (position 0), unifying the subrange reversal logic regardless of whether $left = 1$ or $left > 1$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: IN-PLACE POINTER MANIPULATION & REVERSAL              |
+-----------------------------------------------------------------------+
| • Iterative Loop: nextTemp=curr.next; curr.next=prev; prev=curr; curr=nextTemp|
| • Return Value: Return `prev` as new head when `curr == null`         |
| • Recursive Formula: head.next.next = head; head.next = null;          |
| • Range Reversal [M, N]: Use Dummy Head (prev at left - 1)            |
| • Space Complexity: Iterative O(1) Constant vs Recursive O(N) Stack   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the 4-step iterative reversal sequence in under 1 minute.
- [ ] I know why returning `prev` at the end gives the new head node.
- [ ] I can explain `head.next.next = head` in recursive reversal.
- [ ] I can implement LeetCode 92 (Reverse Subrange) using Dummy Head.
- [ ] I understand why iterative reversal is preferred over recursive reversal.
