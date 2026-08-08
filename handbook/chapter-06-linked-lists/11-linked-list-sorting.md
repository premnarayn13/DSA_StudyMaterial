# 11. Linked List Sorting Algorithms (Merge Sort & Insertion Sort)

## 1. Introduction
Sorting a linked list in **$O(N \log N)$ time and $O(1)$ auxiliary space** (LeetCode 148 - Sort List) is a classic technical coding interview requirement. Unlike arrays where QuickSort or HeapSort are preferred due to cache locality and random index access, **Merge Sort** is the undisputed optimal sorting algorithm for Linked Lists because it requires **zero extra memory allocations** and accesses nodes sequentially via pointer relinking.

> **Important:** Merge Sort on linked lists achieves **$O(N \log N)$ time and $O(\log N)$ stack space (or $O(1)$ space with bottom-up iterative merge sort)** because merging two sorted linked lists takes $O(1)$ auxiliary space (relinking pointers in-place)!

## 2. Core Concepts
* **Linked List Merge Sort Pipeline**:
  1. **Find Middle Node**: Divide list into two equal halves using Fast & Slow Pointers (`fast.next != null && fast.next.next != null`).
  2. **Sever Link**: Split list into `left` and `right` chains by setting `mid.next = null`.
  3. **Recurse**: Recursively call `sortList(left)` and `sortList(right)`.
  4. **Merge**: Combine sorted sub-lists using `mergeTwoLists(l1, l2)` via Dummy Head.
* **Insertion Sort on Linked List (LeetCode 147)**: Building a sorted list one node at a time by finding the insertion spot from `dummy` head ($O(N^2)$ time, $O(1)$ space).

> **Memory Trick for List Merge Sort:** **"1. Find Mid (fast.next & fast.next.next) -> 2. Sever mid.next = null -> 3. Recurse left/right -> 4. Merge Two Lists!"**

## 3. Characteristics / Properties
* **Why Merge Sort Beats QuickSort for Linked Lists**:
  * QuickSort requires $O(1)$ random index access for partition swaps (expensive in lists!).
  * Merge Sort operates sequentially, merging sub-lists in-place without array shifting or buffer allocations.

```
Linked List Sorting Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Sorting Algorithm     | Time Complexity   | Space Complexity  | Best Use Case     |
+-----------------------+-------------------+-------------------+-------------------+
| Merge Sort (Top-Down) | O(N log N)        | O(log N) Call Stack| OPTIMAL STANDARD ⚡|
| Merge Sort (Bottom-Up)| O(N log N)        | O(1) Constant ⚡  | OPTIMAL IN-PLACE  |
| Insertion Sort        | O(N²)             | O(1) Constant     | Small / Nearly Sorted|
| QuickSort             | O(N log N) avg    | O(log N) Stack    | Poor for lists 🐢 |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Top-Down Merge Sort on `4 -> 2 -> 1 -> 3 -> null`:

```
Divide Phase:
[ 4, 2, 1, 3 ] -> Mid node 2 -> Split into [ 4, 2 ] and [ 1, 3 ]
[ 4, 2 ] -> Split into [ 4 ] and [ 2 ]
[ 1, 3 ] -> Split into [ 1 ] and [ 3 ]

Conquer & Merge Phase:
Merge [ 4 ] & [ 2 ] -> [ 2, 4 ]
Merge [ 1 ] & [ 3 ] -> [ 1, 3 ]
Merge [ 2, 4 ] & [ 1, 3 ] -> [ 1, 2, 3, 4 ] ✅ (Sorted in O(N log N) time!)
```

## 5. Visual Diagram
Linked List Merge Sort Splitting & Merging Mechanics:

```
                  [ 4 -> 2 -> 1 -> 3 ]
                     /            \
             [ 4 -> 2 ]          [ 1 -> 3 ]  (Set mid.next = null!)
              /      \            /      \
            [ 4 ]    [ 2 ]      [ 1 ]    [ 3 ]  (Base cases)
              \      /            \      /
             [ 2 -> 4 ]          [ 1 -> 3 ]  (Merge Two Sorted Lists)
                     \            /
                  [ 1 -> 2 -> 3 -> 4 ]
```

## 6. Operations / Algorithms
LeetCode 148 Master Implementation:

```java
public ListNode sortList(ListNode head) {
    // Base case: empty or single node list is already sorted
    if (head == null || head.next == null) {
        return head;
    }

    // Step 1: Find 1st middle node to split list into equal halves
    ListNode mid = getMid(head);
    ListNode rightHead = mid.next;
    mid.next = null; // Step 2: Sever link to cut list into two halves

    // Step 3: Recursively sort left and right halves
    ListNode left = sortList(head);
    ListNode right = sortList(rightHead);

    // Step 4: Merge sorted halves in-place
    return merge(left, right);
}

// Helper: Get 1st Middle Node (fast.next != null && fast.next.next != null)
private ListNode getMid(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}

// Helper: Merge Two Sorted Lists
private ListNode merge(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(-1);
    ListNode curr = dummy;

    while (l1 != null && l2 != null) {
        if (l1.val <= l2.val) {
            curr.next = l1;
            l1 = l1.next;
        } else {
            curr.next = l2;
            l2 = l2.next;
        }
        curr = curr.next;
    }

    curr.next = (l1 != null) ? l1 : l2;
    return dummy.next;
}
```

> **Quick Syntax:**
```java
// Middle Node Condition for Splitting
while (fast.next != null && fast.next.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}
```

## 7. Examples
* **LeetCode 148 - Sort List**: $O(N \log N)$ Merge Sort implementation.
* **LeetCode 147 - Insertion Sort List**: $O(N^2)$ Insertion Sort implementation.
* **Sort a Doubly Linked List**: Merge Sort adapted for bidirectional `prev` and `next` pointers.

## 8. Java Code
Complete interview-ready Java suite implementing Top-Down Merge Sort and Insertion Sort on Linked Lists:

```java
public class LinkedListSortingMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Merge Sort List (LeetCode 148) O(N log N) Time, O(log N) Call Stack Space
    public static ListNode sortList(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode mid = getMid(head);
        ListNode rightHead = mid.next;
        mid.next = null; // Sever link

        ListNode left = sortList(head);
        ListNode right = sortList(rightHead);

        return merge(left, right);
    }

    // 2. Insertion Sort List (LeetCode 147) O(N^2) Time, O(1) Space
    public static ListNode insertionSortList(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode dummy = new ListNode(-1);
        ListNode curr = head;

        while (curr != null) {
            ListNode nextTemp = curr.next; // Save next node
            ListNode prev = dummy;

            // Find insertion position in sorted chain starting from dummy
            while (prev.next != null && prev.next.val < curr.val) {
                prev = prev.next;
            }

            // Insert curr between prev and prev.next
            curr.next = prev.next;
            prev.next = curr;

            curr = nextTemp; // Move to next node in original list
        }

        return dummy.next;
    }

    // Helper: 1st Middle Node
    private static ListNode getMid(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    // Helper: Merge Two Lists
    private static ListNode merge(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(-1), curr = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                curr.next = l1; l1 = l1.next;
            } else {
                curr.next = l2; l2 = l2.next;
            }
            curr = curr.next;
        }
        curr.next = (l1 != null) ? l1 : l2;
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
        // Construct: 4 -> 2 -> 1 -> 3 -> null
        ListNode head = new ListNode(4);
        head.next = new ListNode(2);
        head.next.next = new ListNode(1);
        head.next.next.next = new ListNode(3);

        System.out.print("Unsorted List: ");
        printList(head);

        head = sortList(head);
        System.out.print("Sorted List (Merge Sort): ");
        printList(head); // Output: 1 -> 2 -> 3 -> 4 -> null
    }
}
```

## 9. Complexity Analysis
| Sorting Algorithm | Time Complexity (Best) | Time Complexity (Worst) | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Top-Down Merge Sort** | **$O(N \log N)$** | **$O(N \log N)$** | $O(\log N)$ Call Stack |
| **Bottom-Up Merge Sort**| **$O(N \log N)$** | **$O(N \log N)$** | **$O(1)$ Constant ⚡** |
| **Insertion Sort List** | $\Omega(N)$ | $O(N^2)$ | **$O(1)$ Constant** |

## 10. Edge Cases
* **2-Element List (`4 -> 2 -> null`)**: Must split into `[4]` and `[2]`. Using `getMid` with `fast.next != null && fast.next.next != null` correctly returns node `4` as mid, enabling clean split into `4.next = null`.
* **Already Sorted List**: Merge Sort still executes in $O(N \log N)$ time, whereas Insertion Sort completes in linear $O(N)$ time.
* **Empty List or Single Element List**: Base case returns `head` immediately.

## 11. Common Mistakes
* Using `while (fast != null && fast.next != null)` for `getMid` in Merge Sort (returns 2nd middle node `2` for `[4, 2]`, leading to `mid.next = null` leaving `head` as `[4, 2]` $\implies$ **Infinite Recursion Call Stack Overflow!**). You MUST use **`while (fast.next != null && fast.next.next != null)`**!
* Forgetting to sever the link `mid.next = null` before recursing.
* Creating new `ListNode` instances during Merge instead of relinking existing pointers.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why MUST you use `while (fast.next != null && fast.next.next != null)` for `getMid` in Merge Sort?
> For a 2-element list `[4, 2]`:
> * Standard `fast != null && fast.next != null` sets `mid = node 2`. `mid.next = null` leaves left half as `[4, 2]` (Unchanged!). Recursing on `[4, 2]` causes **Infinite Recursion Stack Overflow!**
> * 1st middle condition `fast.next != null && fast.next.next != null` sets `mid = node 4`. `mid.next = null` splits list into `[4]` and `[2]`, terminating recursion cleanly!

> **Memory Trick:** **"Merge Sort Mid Condition: Check fast.next AND fast.next.next!"**

## 13. Comparisons
| Feature | Array Merge Sort | Linked List Merge Sort |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log N)$ | $O(N \log N)$ |
| **Auxiliary Space** | $O(N)$ (Temporary copy array required) | **$O(1)$ Auxiliary (In-Place Pointer Relinking)** |
| **Random Access** | $O(1)$ | $O(N)$ |
| **Sorting Efficiency**| High for Arrays | **HIGHEST FOR LINKED LISTS ⚡** |

## 14. How to Recognize This in Questions
* **"Sort a linked list in O(N log N) time and O(1) / O(log N) space"** $\rightarrow$ Linked List Merge Sort (LeetCode 148).
* **"Sort a linked list in-place using insertion sort"** $\rightarrow$ Insertion Sort List (LeetCode 147).

## 15. Frequently Asked Interview Questions
* **Q: Why is Merge Sort preferred over QuickSort for Linked Lists?**  
  *A:* QuickSort requires random element access for pivot partitioning and swaps, which takes $O(N)$ per element in linked lists. Merge Sort operates sequentially, finding middle and merging sub-lists in-place with zero element swaps or auxiliary array allocations.
* **Q: How does Bottom-Up Iterative Merge Sort achieve $O(1)$ space for Linked Lists?**  
  *A:* By merging sub-lists of size $1, 2, 4, 8 \dots$ iteratively using loops rather than recursion, eliminating the $O(\log N)$ JVM call stack space.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST SORTING (MERGE SORT)                      |
+-----------------------------------------------------------------------+
| • Mid Condition Rule: while (fast.next != null && fast.next.next != null)|
| • Prevents infinite recursion on 2-element lists [4, 2]!              |
| • Sever Link Step: rightHead = mid.next; mid.next = null;             |
| • Recurse & Merge: sortList(head) & sortList(rightHead) -> Merge      |
| • Merge Helper: Uses Dummy Head + 2-pointer relinking in O(1) space   |
| • Time Complexity: O(N log N) | Space: O(log N) Call Stack / O(1) Iter|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `fast.next != null && fast.next.next != null` is mandatory for list splitting.
- [ ] I can write the 4-step Merge Sort algorithm for Linked Lists.
- [ ] I can sever `mid.next = null` correctly to avoid infinite recursion.
- [ ] I can merge two sorted lists in-place using a Dummy Head Node.
- [ ] I can explain why Merge Sort is preferred over QuickSort for Linked Lists.
