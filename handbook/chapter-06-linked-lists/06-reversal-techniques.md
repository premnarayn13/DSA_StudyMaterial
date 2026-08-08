# 06. Linked List Reversal Techniques, Sub-List Reversal & K-Group Processing

## 1. Introduction
**Linked List Reversal** is a cornerstone algorithmic category in data structures and technical coding interviews. Reversal techniques range from **Standard Iterative/Recursive Reversal (LeetCode 206)** to **Sub-List Reversal between positions Left and Right (LeetCode 92)** and **Reverse Nodes in $K$-Group (LeetCode 25)**. Achieving in-place reversal requires re-orienting pointer directions (`curr.next = prev`) in **$O(N)$ time and $O(1)$ constant auxiliary space**.

> **Important:** In-place pointer reversal NEVER creates new node objects on the JVM heap. Instead, it re-wires existing `.next` references in memory. Master the **3-Pointer Iterative Loop (`prev`, `curr`, `nextTemp`)** to solve all linked list reversal problems bug-free!

```
In-Place Pointer Reversal Spectrum:
+-----------------------------------------------------------------------------------+
| Full List Reversal (206)   : Reverse entire list from head to tail                |
| Range Sub-List Reversal (92): Reverse sub-segment between indices Left and Right  |
| K-Group Reversal (25)       : Reverse nodes in chunks of size K continuously        |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 3-Pointer Iterative Reversal Algorithm (LeetCode 206)
Given `head` pointer of a Singly Linked List:
1. Initialize `ListNode prev = null`, `ListNode curr = head`.
2. While `curr != null`:
   - Save next node: **`ListNode nextTemp = curr.next;`**
   - Reverse pointer direction: **`curr.next = prev;`**
   - Advance prev pointer: **`prev = curr;`**
   - Advance curr pointer: **`curr = nextTemp;`**
3. Return **`prev`** as the new head of the reversed list!

```
Iteration Step in 3-Pointer Reversal:
Before : ( prev )    ( curr ) ----> ( nextTemp )
Action : curr.next = prev
After  : ( prev ) <---- ( curr )    ( nextTemp )
Next   : prev = curr, curr = nextTemp
```

### 2.2 Sub-List Reversal Between Left and Right (LeetCode 92)
To reverse nodes from position `left` to `right` (1-indexed) in a single pass:
1. Use a **Dummy Sentinel Node** `dummy` pointing to `head`.
2. Advance a pointer `pre` $left - 1$ steps from `dummy`.
3. Pointer `curr` points to `pre.next` (the first node of sub-list).
4. Perform $right - left$ pointer head-insertions:
   - `ListNode temp = curr.next;`
   - `curr.next = temp.next;`
   - `temp.next = pre.next;`
   - `pre.next = temp;`
5. Return `dummy.next`!

```
Sub-List Head-Insertion Mechanics (Reverse Left=2, Right=4):
List: pre(1) -> curr(2) -> temp(3) -> 4 -> 5
Action: Move temp(3) between pre(1) and pre.next(2):
State: pre(1) -> 3 -> curr(2) -> temp(4) -> 5
Action: Move temp(4) between pre(1) and pre.next(3):
State: pre(1) -> 4 -> 3 -> curr(2) -> 5  ✅ (Sub-list [2, 3, 4] reversed!)
```

> **Memory Trick:** **"Sub-List Reversal (92): Advance pre to left-1! Repeatedly insert curr.next between pre and pre.next!"**

---

## 3. Characteristics & $K$-Group Processing (LeetCode 25)

### 3.1 Reverse Nodes in $K$-Group (LeetCode 25)
Given a linked list, reverse the nodes of the list $K$ at a time and return its modified list.
* If the number of nodes is not a multiple of $K$, the remaining left-over nodes at the end MUST remain in their original order.
* **Strategy**:
  1. Count if $K$ nodes exist ahead from `curr`. If $< K$ nodes remain, break!
  2. If $\ge K$ nodes exist, reverse the $K$ nodes using standard iterative reversal.
  3. Connect the predecessor group's tail to the new reversed head.
  4. Repeat for subsequent groups.

```
K-Group Reversal (K = 3) on List [1, 2, 3, 4, 5]:
Group 1 (Size 3: 1->2->3): Has >= 3 nodes -> Reverse -> [3, 2, 1]
Group 2 (Size 2: 4->5)  : Has < 3 nodes  -> Keep original order -> [4, 5]
Combined Result: [3, 2, 1, 4, 5] ✅
```

---

## 4. Internal Working Mechanics
Tracing Sub-List Reversal (LeetCode 92) on `[1, 2, 3, 4, 5]`, `left = 2`, `right = 4`:

```
Init: dummy -> 1 -> 2 -> 3 -> 4 -> 5
      pre = node(1), curr = node(2)

Pass 1 (i = 0): temp = curr.next (node 3)
                curr.next = temp.next (2.next = 4)
                temp.next = pre.next  (3.next = 2)
                pre.next = temp       (1.next = 3)
                List: 1 -> 3 -> 2 -> 4 -> 5

Pass 2 (i = 1): temp = curr.next (node 4)
                curr.next = temp.next (2.next = 5)
                temp.next = pre.next  (4.next = 3)
                pre.next = temp       (1.next = 4)
                List: 1 -> 4 -> 3 -> 2 -> 5

Reversal Complete! Result: 1 -> 4 -> 3 -> 2 -> 5 ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Sub-List In-Place Reversal Topology (LeetCode 92):

```
              +-------------------------------------+
              |                                     |
              v                                     |
    pre ---> ( 1 )       ( 2: curr ) <--- ( 3 ) <--- ( 4: temp )      ( 5 )
              |                             ^                       ^
              |                             |                       |
              +-----------------------------+-----------------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Full Reversal (LeetCode 206), Sub-List Reversal II (LeetCode 92), and Reverse Nodes in K-Group (LeetCode 25):

```java
import java.util.*;

public class ReversalTechniquesMaster {

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

    // 1. Full Reverse Linked List Iterative (LeetCode 206) O(N) Time, O(1) Space
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

    // 2. Full Reverse Linked List Recursive (LeetCode 206) O(N) Time, O(N) Stack Space
    public static ListNode reverseListRecursive(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }

        ListNode newHead = reverseListRecursive(head.next);
        head.next.next = head; // Re-wire next node's pointer back to self
        head.next = null;      // Disconnect original forward pointer

        return newHead;
    }

    // 3. Reverse Sub-List Between Left and Right (LeetCode 92) O(N) Time, O(1) Space
    public static ListNode reverseBetween(ListNode head, int left, int right) {
        if (head == null || left == right) return head;

        ListNode dummy = new ListNode(0, head);
        ListNode pre = dummy;

        // Step 1: Advance pre to (left - 1) position
        for (int i = 0; i < left - 1; i++) {
            pre = pre.next;
        }

        // Step 2: Head-insertion loop for (right - left) times
        ListNode curr = pre.next;
        for (int i = 0; i < right - left; i++) {
            ListNode temp = curr.next;
            curr.next = temp.next;
            temp.next = pre.next;
            pre.next = temp;
        }

        return dummy.next;
    }

    // 4. Reverse Nodes in K-Group (LeetCode 25) O(N) Time, O(1) Space
    public static ListNode reverseKGroup(ListNode head, int k) {
        if (head == null || k == 1) return head;

        ListNode dummy = new ListNode(0, head);
        ListNode groupPrev = dummy;

        while (true) {
            // Check if k nodes exist ahead
            ListNode kth = getKthNode(groupPrev, k);
            if (kth == null) break;

            ListNode groupNext = kth.next;

            // Reverse current k-group
            ListNode prev = groupNext;
            ListNode curr = groupPrev.next;
            while (curr != groupNext) {
                ListNode temp = curr.next;
                curr.next = prev;
                prev = curr;
                curr = temp;
            }

            // Re-link boundary pointers
            ListNode newGroupTail = groupPrev.next;
            groupPrev.next = kth;
            groupPrev = newGroupTail;
        }

        return dummy.next;
    }

    private static ListNode getKthNode(ListNode curr, int k) {
        while (curr != null && k > 0) {
            curr = curr.next;
            k--;
        }
        return curr;
    }
}
```

> **Quick Syntax:**
```java
// Recursive Reversal Base & Pointer Wire
if (head == null || head.next == null) return head;
ListNode newHead = reverseListRecursive(head.next);
head.next.next = head;
head.next = null;
```

---

## 7. Concrete Problem Examples
* **LeetCode 206 - Reverse Linked List**: Iterative vs recursive reversal.
* **LeetCode 92 - Reverse Linked List II**: Range sub-list head-insertion reversal.
* **LeetCode 25 - Reverse Nodes in k-Group**: Chunked $K$-group list reversal.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Reverse Between (LeetCode 92) and Reverse K-Group (LeetCode 25):

```java
public class ReversalTechniquesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Reverse Sub-List (LeetCode 92, Left=2, Right=4) ===");
        ReversalTechniquesMaster.ListNode list1 = new ReversalTechniquesMaster.ListNode(1);
        list1.next = new ReversalTechniquesMaster.ListNode(2);
        list1.next.next = new ReversalTechniquesMaster.ListNode(3);
        list1.next.next.next = new ReversalTechniquesMaster.ListNode(4);
        list1.next.next.next.next = new ReversalTechniquesMaster.ListNode(5);

        ReversalTechniquesMaster.ListNode res1 = ReversalTechniquesMaster.reverseBetween(list1, 2, 4);
        System.out.print("Reversed (2..4): ");
        while (res1 != null) {
            System.out.print(res1.val + " -> ");
            res1 = res1.next;
        }
        System.out.println("null"); // Output: 1 -> 4 -> 3 -> 2 -> 5 -> null

        System.out.println("\n=== 2. Reverse K-Group (LeetCode 25, K=3) ===");
        ReversalTechniquesMaster.ListNode list2 = new ReversalTechniquesMaster.ListNode(1);
        list2.next = new ReversalTechniquesMaster.ListNode(2);
        list2.next.next = new ReversalTechniquesMaster.ListNode(3);
        list2.next.next.next = new ReversalTechniquesMaster.ListNode(4);
        list2.next.next.next.next = new ReversalTechniquesMaster.ListNode(5);

        ReversalTechniquesMaster.ListNode res2 = ReversalTechniquesMaster.reverseKGroup(list2, 3);
        System.out.print("Reversed (K=3):  ");
        while (res2 != null) {
            System.out.print(res2.val + " -> ");
            res2 = res2.next;
        }
        System.out.println("null"); // Output: 3 -> 2 -> 1 -> 4 -> 5 -> null
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Iterative Reverse (206)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| 3-Pointer loop (`prev`, `curr`, `nextTemp`) |
| **Recursive Reverse (206)**| **$O(N)$ Linear ⚡** | $O(N)$ Recursion Stack | JVM call stack height $N$ |
| **Sub-List Reverse (92)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Single-pass head insertion |
| **K-Group Reverse (25)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Group checking + in-place reversal |

---

## 10. Edge Cases & Boundary Handling
* **$left = 1$ in Reverse Between**: Reversing from position 1 changes the list head; handled cleanly by `dummy.next`.
* **$K > N$ in K-Group Reversal**: `getKthNode` returns `null`, loop breaks cleanly leaving list unchanged.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `head.next = null` in Recursive Reversal**:
  - Failing to set `head.next = null` after `head.next.next = head` creates a **2-node cyclic loop** at the tail!
  - **Always execute `head.next = null` in recursive base case unwind**.
* **Losing Node References in Sub-List Reversal**: Assigning `pre.next = temp` without saving `temp.next` breaks forward list linkage.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Iterative vs Recursive Linked List Reversal:
> * **Iterative ($O(N)$ Time, $O(1)$ Space)**: Preferred in production and memory-constrained environments due to zero stack allocation.
> * **Recursive ($O(N)$ Time, $O(N)$ Stack Space)**: Elegant, but risks `StackOverflowError` if list length $N > 10,000$.

> **Memory Trick:** **"Recursive reversal: head.next.next = head AND head.next = null!"**

---

## 13. System & Implementation Comparisons

| Feature | Iterative Reversal | Recursive Reversal |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Call Stack |
| **Stack Overflow Risk**| Zero Risk | High for $N > 10^4$ |
| **Code Length** | 6 Lines | 4 Lines |

---

## 14. How to Recognize This in Questions
* **"Reverse linked list between positions left and right"** $\rightarrow$ LeetCode 92 (Sub-list head-insertion).
* **"Reverse nodes in k-group"** $\rightarrow$ LeetCode 25 (`getKthNode` check + in-place chunk reversal).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `head.next.next = head` work in recursive linked list reversal?**  
  *A:* When the recursion unwinds from the end of the list, `head.next` is the original next node. `head.next.next = head` points that node's `.next` field back to `head`, reversing the link direction in $O(1)$ time.
* **Q: Why is dummy node required for Reverse Linked List II (LeetCode 92)?**  
  *A:* Because if `left = 1`, the original head node itself is reversed. Using a dummy node allows `pre` to start at `dummy` (index 0), preserving uniform pointer manipulations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST REVERSAL TECHNIQUES                       |
+-----------------------------------------------------------------------+
| • Iterative 3-Pointer: nextTemp = curr.next; curr.next = prev;        |
|   prev = curr; curr = nextTemp;                                       |
| • Recursive Formula: head.next.next = head; head.next = null;         |
| • Sub-List (92): Advance pre to left-1; temp = curr.next;             |
|   curr.next = temp.next; temp.next = pre.next; pre.next = temp;       |
| • K-Group (25): If k nodes exist, reverse chunk; re-link group tails  |
| • Space Invariant: All iterative reversals run in O(1) Space ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 3-pointer iterative reversal in under 2 minutes.
- [ ] I can write recursive list reversal and explain `head.next.next = head`.
- [ ] I can solve Reverse Linked List II (LeetCode 92) in a single pass.
- [ ] I can solve Reverse Nodes in K-Group (LeetCode 25) in $O(1)$ space.
- [ ] I know why dummy node is essential when `left = 1` in sub-list reversal.
