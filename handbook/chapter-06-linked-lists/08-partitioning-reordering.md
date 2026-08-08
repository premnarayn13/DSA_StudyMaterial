# 08. Linked List Partitioning & Reordering Operations

## 1. Introduction
Partitioning and reordering linked list nodes are advanced pointer manipulation techniques tested in technical coding interviews. Problems such as Partition List (LeetCode 86), Reorder List (LeetCode 143), and Odd Even Linked List (LeetCode 328) require splitting a single linked list into two independent sub-chains using two dummy head nodes, processing nodes according to specific predicates or index positions, and relinking the sub-chains back together in **$O(N)$ linear time and $O(1)$ auxiliary space**.

> **Important:** When building two separate sub-chains (e.g., `smallHead` and `largeHead`), you MUST terminate the end of the second sub-chain by setting **`largeCurr.next = null`**! Failing to clear `next` creates a memory reference cycle, causing infinite loops!

## 2. Core Concepts
* **Dual Dummy Head Partitioning (LeetCode 86)**: Allocating `smallDummy` and `largeDummy` head nodes. Iterate through the input list, appending nodes $< X$ to `small` and nodes $\ge X$ to `large`. Finally, connect `small.next = largeDummy.next` and `large.next = null`.
* **Odd Even List Partitioning (LeetCode 328)**: Grouping nodes at odd indices first, followed by nodes at even indices, while preserving original relative node order.
* **3-Step List Reordering (LeetCode 143)**: Reordering list $L_0 \to L_1 \dots \to L_{n-1} \to L_n$ into $L_0 \to L_n \to L_1 \to L_{n-1} \to \dots$:
  1. Find middle node using Fast & Slow Pointers.
  2. Reverse the second half of the list in-place.
  3. Interleave/weave nodes from first half and reversed second half!

> **Memory Trick:** **"Split into 2 lists via Dual Dummy Heads -> Relink -> Set tail.next = null!"**

## 3. Characteristics / Properties
* **In-Place Structural Reorganization**: All node partitioning and reordering algorithms run in **$O(1)$ auxiliary space** by modifying existing pointer links without creating new node objects.
* **Relative Order Preservation**: Dual dummy partitioning maintains the original relative insertion order of elements in both partitioned sub-chains.

```
Partitioning & Reordering Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Pattern     | Time Complexity   | Space Complexity  | Best Technique    |
+-----------------------+-------------------+-------------------+-------------------+
| Partition List (< X)  | O(N) Linear       | O(1) Constant ⚡  | Dual Dummy Heads  |
| Odd Even Linked List  | O(N) Linear       | O(1) Constant ⚡  | Odd/Even Pointers |
| Reorder List (143)    | O(N) Linear       | O(1) Constant ⚡  | Mid + Reverse + Weave|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing 3-Step List Reordering (LeetCode 143) on `1 -> 2 -> 3 -> 4 -> 5 -> null`:

```
Step 1: Find Middle Node using Fast/Slow pointers
List split: First Half = 1 -> 2 -> 3 -> null | Second Half = 4 -> 5 -> null

Step 2: Reverse Second Half In-Place
Reversed Second Half = 5 -> 4 -> null

Step 3: Interleave / Weave First Half and Reversed Second Half
Pointers: p1 = 1 -> 2 -> 3, p2 = 5 -> 4

Iter 1: Link 1 -> 5 -> 2
Iter 2: Link 2 -> 4 -> 3

Final Reordered List: 1 -> 5 -> 2 -> 4 -> 3 -> null ✅ (Correct!)
```

## 5. Visual Diagram
Dual Dummy Head Partitioning Architecture (`Partition List`):

```
Input List: 1 -> 4 -> 3 -> 2 -> 5 -> 2, Pivot X = 3

Small Chain (nodes < 3):   smallDummy -> 1 -> 2 -> 2
Large Chain (nodes >= 3):  largeDummy -> 4 -> 3 -> 5 -> null  (MUST set last next = null!)

Relink Step: small.next = largeDummy.next
Result: 1 -> 2 -> 2 -> 4 -> 3 -> 5 -> null ✅
```

## 6. Operations / Algorithms
LeetCode 86 & LeetCode 328 Master Implementation:

```java
// 1. Partition List around value X (LeetCode 86) O(N) Time, O(1) Space
public ListNode partition(ListNode head, int x) {
    ListNode smallDummy = new ListNode(0);
    ListNode largeDummy = new ListNode(0);
    ListNode small = smallDummy;
    ListNode large = largeDummy;

    ListNode curr = head;
    while (curr != null) {
        if (curr.val < x) {
            small.next = curr;
            small = small.next;
        } else {
            large.next = curr;
            large = large.next;
        }
        curr = curr.next;
    }

    large.next = null; // MANDATORY: Clear tail pointer to prevent cycles!
    small.next = largeDummy.next; // Connect small chain to large chain

    return smallDummy.next;
}

// 2. Odd Even Linked List (LeetCode 328) O(N) Time, O(1) Space
public ListNode oddEvenList(ListNode head) {
    if (head == null) return null;

    ListNode odd = head;
    ListNode even = head.next;
    ListNode evenHead = even;

    while (even != null && even.next != null) {
        odd.next = even.next;
        odd = odd.next;
        even.next = odd.next;
        even = even.next;
    }

    odd.next = evenHead; // Connect odd chain to even head
    return head;
}
```

> **Quick Syntax:**
```java
// Mandatory Cycle Prevention Step
large.next = null;
```

## 7. Examples
* **LeetCode 86 - Partition List**: Partitioning nodes around pivot $X$ using Dual Dummy Heads.
* **LeetCode 328 - Odd Even Linked List**: Grouping odd-indexed nodes before even-indexed nodes.
* **LeetCode 143 - Reorder List**: 3-step reordering (Find Mid $\to$ Reverse 2nd Half $\to$ Interleave).

## 8. Java Code
Complete interview-ready Java suite implementing Partition List, Odd Even List, and Reorder List:

```java
public class PartitioningReorderingMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Partition List (LeetCode 86) O(N) Time, O(1) Space
    public static ListNode partition(ListNode head, int x) {
        ListNode smallDummy = new ListNode(0), largeDummy = new ListNode(0);
        ListNode small = smallDummy, large = largeDummy;

        ListNode curr = head;
        while (curr != null) {
            if (curr.val < x) {
                small.next = curr;
                small = small.next;
            } else {
                large.next = curr;
                large = large.next;
            }
            curr = curr.next;
        }

        large.next = null; // Clear tail to prevent cycles!
        small.next = largeDummy.next;

        return smallDummy.next;
    }

    // 2. Reorder List (LeetCode 143) O(N) Time, O(1) Space
    public static void reorderList(ListNode head) {
        if (head == null || head.next == null) return;

        // Step 1: Find middle using Fast/Slow pointers
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // Step 2: Reverse second half
        ListNode secondHalf = reverse(slow.next);
        slow.next = null; // Cut list into two halves

        // Step 3: Interleave first half and reversed second half
        ListNode firstHalf = head;
        while (secondHalf != null) {
            ListNode temp1 = firstHalf.next;
            ListNode temp2 = secondHalf.next;

            firstHalf.next = secondHalf;
            secondHalf.next = temp1;

            firstHalf = temp1;
            secondHalf = temp2;
        }
    }

    // Helper: Reverse List
    private static ListNode reverse(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
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
        // Test Reorder List: 1 -> 2 -> 3 -> 4 -> 5
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);

        System.out.print("Original List: ");
        printList(head);

        reorderList(head);
        System.out.print("After Reorder List: ");
        printList(head); // Output: 1 -> 5 -> 2 -> 4 -> 3 -> null
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Technique |
| :--- | :--- | :--- | :--- |
| **Partition List (LeetCode 86)** | **$O(N)$ Linear** | **$O(1)$ Constant** | Dual Dummy Head sub-chains |
| **Odd Even List (LeetCode 328)** | **$O(N)$ Linear** | **$O(1)$ Constant** | Separate odd/even pointer tracks |
| **Reorder List (LeetCode 143)** | **$O(N)$ Linear** | **$O(1)$ Constant** | Mid + Reverse + Weave |

## 10. Edge Cases
* **Forgetting `large.next = null`**: Causes memory reference cycle, leading to `Memory Limit Exceeded` or infinite loops during list traversal!
* **Empty or Single Node List**: Return immediately without modification.
* **All Nodes Small or All Nodes Large**: Handled seamlessly by Dual Dummy Head pointers.

## 11. Common Mistakes
* Forgetting to set `large.next = null` at the end of Partition List.
* Overwriting `firstHalf.next` or `secondHalf.next` during list interleaving without saving temporary `next` pointers.
* Forgetting to sever the link `slow.next = null` after finding middle node in Reorder List.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is `large.next = null` mandatory in Partition List?
> Before partitioning, a node in the large chain might have pointed to a node that was moved to the small chain. If you don't explicitly set `large.next = null`, that stale pointer will form a cyclic loop between small and large chains!

> **Memory Trick:** **"Always clear tail pointer: large.next = null!"**

## 13. Comparisons
| Feature | Single Dummy Head | Dual Dummy Head |
| :--- | :--- | :--- |
| **Use Case** | Merging or deleting nodes | **Partitioning into 2 sub-chains** |
| **Pointer Management**| 1 tracker (`curr`) | **2 trackers (`small`, `large`)** |
| **Cycle Risk** | Minimal | **High (Must set `large.next = null`)** |

## 14. How to Recognize This in Questions
* **"Partition linked list around pivot X preserving relative order"** $\rightarrow$ Dual Dummy Head Partitioning (LeetCode 86).
* **"Reorder list to L0 -> Ln -> L1 -> Ln-1"** $\rightarrow$ 3-Step Reordering (Mid $\to$ Reverse 2nd Half $\to$ Weave).
* **"Group odd-indexed nodes before even-indexed nodes"** $\rightarrow$ Odd Even Linked List (LeetCode 328).

## 15. Frequently Asked Interview Questions
* **Q: How does 3-step list reordering run in $O(N)$ time and $O(1)$ space?**  
  *A:* (1) Finding middle using Fast/Slow pointers takes $O(N)$ time and $O(1)$ space. (2) Reversing second half takes $O(N)$ time and $O(1)$ space. (3) Interleaving two halves takes $O(N)$ time and $O(1)$ space $\implies$ Total $O(N)$ time and $O(1)$ space.
* **Q: Why does Dual Dummy Head partitioning preserve relative node order?**  
  *A:* Because we scan the input list sequentially from `head` to `tail`. Appending elements to `small` or `large` sub-chains in the order they appear preserves their original relative ordering.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PARTITIONING & REORDERING OPERATIONS                  |
+-----------------------------------------------------------------------+
| • Partition List: Dual Dummy Heads (smallDummy & largeDummy)          |
| • Cycle Prevention Rule: ALWAYS set `large.next = null`               |
| • Odd Even List: Connect odd.next = evenHead after loop               |
| • Reorder List: 1. Find Mid  2. Reverse 2nd Half  3. Weave Halves     |
| • Complexity: O(N) Linear Time | O(1) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement Dual Dummy Head partitioning in $O(1)$ space.
- [ ] I know why `large.next = null` is mandatory to prevent cycles.
- [ ] I can implement Odd Even Linked List (LeetCode 328).
- [ ] I can write the 3-step Reorder List algorithm (LeetCode 143).
- [ ] I can interleave two linked list halves using temporary next pointers.
