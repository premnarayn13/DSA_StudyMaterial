# 11. Linked List Sorting Algorithms: Merge Sort, Insertion Sort & Quick Sort

## 1. Introduction
Sorting a linked list efficiently is a fundamental requirement in data structures and algorithmic design. While array sorting algorithms like Quicksort rely heavily on $O(1)$ random indexing, **Merge Sort** is the optimal, canonical sorting algorithm for **Linked Lists (LeetCode 148)**. Merge Sort executes in **$O(N \log N)$ time** without requiring random array access, making optimal use of sequential pointer traversal and $O(1)$ node re-linking.

> **Important:** Why is Merge Sort preferred for Linked Lists while Quicksort is preferred for Arrays?
> 1. Linked lists allow **$O(1)$ constant-time merging** of two sorted halves without allocating auxiliary memory arrays!
> 2. Middle finding is performed in $O(N)$ time using Fast & Slow pointers (`findFirstMiddle`).
> 3. Unlike arrays where Merge Sort requires $O(N)$ auxiliary array space, Linked List Merge Sort operates strictly by re-wiring pointers!

```
Linked List Sorting Algorithms Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Sorting Algorithm     | Time Complexity   | Space Complexity  | Stability & Notes |
+-----------------------+-------------------+-------------------+-------------------+
| Top-Down Merge Sort   | **$O(N \log N)$⚡**| $O(\log N)$ Stack | Stable (Best Choice)|
| Bottom-Up Merge Sort  | **$O(N \log N)$⚡**| **$O(1)$ Constant⚡**| Stable (Optimal)  |
| Insertion Sort List   | $O(N^2)$          | **$O(1)$ Constant⚡**| Stable (Small N)  |
| Quick Sort            | $O(N \log N)$ Avg | $O(\log N)$ Stack | Unstable          |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 2. Core Concepts & Top-Down Merge Sort Architecture

### 2.1 Top-Down Recursive Merge Sort (LeetCode 148)
1. **Base Case**: If `head == null || head.next == null`, return `head` (List of size 0 or 1 is already sorted!).
2. **Split List**: Use Fast & Slow pointers (`findFirstMiddle`) to find the mid-point node `mid`.
   - Disconnect list: `rightHead = mid.next; mid.next = null;`.
3. **Recursive Divide**:
   - `leftSorted = sortList(head);`
   - `rightSorted = sortList(rightHead);`
4. **Merge Conquer**:
   - Return **`mergeTwoLists(leftSorted, rightSorted)`**!

```
Top-Down Merge Sort Divide & Conquer Tree:
                     [ 4, 2, 1, 3 ]
                      /          \
                [ 4, 2 ]        [ 1, 3 ]   (Split at first middle)
                /      \        /      \
             [ 4 ]    [ 2 ]  [ 1 ]    [ 3 ]
                \      /        \      /
                [ 2, 4 ]        [ 1, 3 ]   (Merge Two Sorted Lists)
                      \          /
                     [ 1, 2, 3, 4 ]        (Final Merged Sorted List!)
```

### 2.2 Bottom-Up Iterative Merge Sort ($O(N \log N)$ Time, $O(1)$ Auxiliary Space)
To eliminate the $O(\log N)$ recursion stack space:
* Iteratively merge sub-lists of size $step = 1, 2, 4, 8 \dots < N$.
* In each pass, split the list into chunks of size $step$, merge adjacent pairs using dummy head sentinel node, and re-link output.

> **Memory Trick:** **"Linked List Merge Sort: Split at first middle (mid.next = null), recursively sort left and right, then mergeTwoLists!"**

---

## 3. Characteristics & Insertion Sort List (LeetCode 147)

### 3.1 Insertion Sort List ($O(N^2)$ Time, $O(1)$ Space)
For small linked lists ($N < 50$) or nearly sorted lists, Insertion Sort provides a simple in-place algorithm:
1. Maintain a **Dummy Sentinel Node** `dummy` representing the sorted sub-list head.
2. Maintain pointer `curr = head`.
3. For each node `curr`:
   - Find insertion position in sorted sub-list starting from `dummy`: advance `prev` while `prev.next != null && prev.next.val < curr.val`.
   - Insert `curr` between `prev` and `prev.next`.
   - Advance `curr = nextTemp`.

```
Insertion Sort Sub-List Insertion Layout:
dummy -> [ 1 (Sorted) ] -> [ 3 (Sorted) ] ------> [ 4 (Unsorted curr) ]
           ^                 ^
         prev             prev.next (3 < 4 < infinity -> Insert after 3!)
```

---

## 4. Internal Working Mechanics
Tracing Top-Down Merge Sort on `[4, 2, 1, 3]`:

```
Step 1: Split [4, 2, 1, 3] at first middle node (2).
        Left:  [4, 2]
        Right: [1, 3]

Step 2: Split Left [4, 2]:
        Left: [4], Right: [2] -> Merge -> [2, 4]

Step 3: Split Right [1, 3]:
        Left: [1], Right: [3] -> Merge -> [1, 3]

Step 4: Merge [2, 4] and [1, 3]:
        Compare 2 vs 1 -> Take 1
        Compare 2 vs 3 -> Take 2
        Compare 4 vs 3 -> Take 3
        Append 4 -> Take 4

Result: [1, 2, 3, 4] ✅ (O(N log N) Time!)
```

---

## 5. Visual Diagram
Linked List Merge Sort Recursive Partitioning Topography:

```
               [ 4 -> 2 -> 1 -> 3 ]
                   /          \
        [ 4 -> 2 ]              [ 1 -> 3 ]
         /      \                /      \
      [ 4 ]    [ 2 ]          [ 1 ]    [ 3 ]
         \      /                \      /
        [ 2 -> 4 ]              [ 1 -> 3 ]
           \                       /
         [ 1 -> 2 -> 3 -> 4 -> null ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Top-Down Merge Sort (LeetCode 148), Insertion Sort List (LeetCode 147), and Bottom-Up $O(1)$ Space Merge Sort:

```java
import java.util.*;

public class LinkedListSortingMaster {

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

    // 1. Top-Down Recursive Merge Sort (LeetCode 148) O(N log N) Time, O(log N) Stack Space
    public static ListNode sortList(ListNode head) {
        if (head == null || head.next == null) {
            return head; // Base case: 0 or 1 element is already sorted
        }

        // Step 1: Find first middle node to split list
        ListNode mid = getFirstMiddle(head);
        ListNode rightHead = mid.next;
        mid.next = null; // Break list into two halves

        // Step 2: Recursively sort both halves
        ListNode leftSorted = sortList(head);
        ListNode rightSorted = sortList(rightHead);

        // Step 3: Merge sorted halves
        return mergeTwoLists(leftSorted, rightSorted);
    }

    // Helper: Find First Middle Node
    private static ListNode getFirstMiddle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;

        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow;
    }

    // Helper: Merge Two Sorted Lists
    private static ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
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

    // 2. Insertion Sort List (LeetCode 147) O(N^2) Time, O(1) Space
    public static ListNode insertionSortList(ListNode head) {
        if (head == null || head.next == null) return head;

        ListNode dummy = new ListNode(0);
        ListNode curr = head;

        while (curr != null) {
            ListNode nextTemp = curr.next;
            ListNode prev = dummy;

            // Find insertion position in sorted list
            while (prev.next != null && prev.next.val < curr.val) {
                prev = prev.next;
            }

            // Insert curr between prev and prev.next
            curr.next = prev.next;
            prev.next = curr;

            curr = nextTemp;
        }

        return dummy.next;
    }

    // 3. Bottom-Up Iterative Merge Sort (LeetCode 148) O(N log N) Time, O(1) Auxiliary Space
    public static ListNode sortListBottomUp(ListNode head) {
        if (head == null || head.next == null) return head;

        int length = getLength(head);
        ListNode dummy = new ListNode(0, head);

        for (int step = 1; step < length; step *= 2) {
            ListNode prev = dummy;
            ListNode curr = dummy.next;

            while (curr != null) {
                ListNode left = curr;
                ListNode right = split(left, step);
                curr = split(right, step);

                prev.next = mergeTwoLists(left, right);
                while (prev.next != null) {
                    prev = prev.next;
                }
            }
        }

        return dummy.next;
    }

    private static int getLength(ListNode head) {
        int len = 0;
        while (head != null) {
            len++;
            head = head.next;
        }
        return len;
    }

    // Splits list by size step, returns head of second half
    private static ListNode split(ListNode head, int step) {
        if (head == null) return null;
        for (int i = 1; i < step && head.next != null; i++) {
            head = head.next;
        }
        ListNode secondHalf = head.next;
        head.next = null; // Disconnect first half
        return secondHalf;
    }
}
```

> **Quick Syntax:**
```java
// Linked List Merge Sort Split Loop Syntax
ListNode mid = getFirstMiddle(head);
ListNode rightHead = mid.next;
mid.next = null; // Mandatory list split!
```

---

## 7. Concrete Problem Examples
* **LeetCode 148 - Sort List**: $O(N \log N)$ time linked list sorting.
* **LeetCode 147 - Insertion Sort List**: $O(N^2)$ in-place insertion sorting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Top-Down Merge Sort and Insertion Sort List:

```java
public class LinkedListSortingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Top-Down Merge Sort (LeetCode 148) ===");
        LinkedListSortingMaster.ListNode head1 = new LinkedListSortingMaster.ListNode(4);
        head1.next = new LinkedListSortingMaster.ListNode(2);
        head1.next.next = new LinkedListSortingMaster.ListNode(1);
        head1.next.next.next = new LinkedListSortingMaster.ListNode(3);

        LinkedListSortingMaster.ListNode sorted1 = LinkedListSortingMaster.sortList(head1);
        System.out.print("Sorted List: ");
        while (sorted1 != null) {
            System.out.print(sorted1.val + " -> ");
            sorted1 = sorted1.next;
        }
        System.out.println("null"); // Output: 1 -> 2 -> 3 -> 4 -> null

        System.out.println("\n=== 2. Insertion Sort List (LeetCode 147) ===");
        LinkedListSortingMaster.ListNode head2 = new LinkedListSortingMaster.ListNode(-1);
        head2.next = new LinkedListSortingMaster.ListNode(5);
        head2.next.next = new LinkedListSortingMaster.ListNode(3);
        head2.next.next.next = new LinkedListSortingMaster.ListNode(4);
        head2.next.next.next.next = new LinkedListSortingMaster.ListNode(0);

        LinkedListSortingMaster.ListNode sorted2 = LinkedListSortingMaster.insertionSortList(head2);
        System.out.print("Insertion Sorted: ");
        while (sorted2 != null) {
            System.out.print(sorted2.val + " -> ");
            sorted2 = sorted2.next;
        }
        System.out.println("null"); // Output: -1 -> 0 -> 3 -> 4 -> 5 -> null
    }
}
```

---

## 9. Complexity Analysis

| Sorting Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Top-Down Merge Sort (148)**| **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | $O(\log N)$ Call Stack |
| **Bottom-Up Merge Sort (148)**| **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(1)$ Strict In-Place ⚡**|
| **Insertion Sort List (147)** | $O(N)$ Best | $O(N^2)$ Quadratic | $O(N^2)$ Quadratic | **$O(1)$ Strict In-Place ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Empty or Single Node List (`head == null || head.next == null`)**: Returns `head` immediately.
* **Two Element List (`4 -> 2`)**: `mid` lands on 4, splits into `[4]` and `[2]`, merges to `[2 -> 4]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using 2nd Middle Node Split (`while (fast != null && fast.next != null)`)**:
  - For a 2-node list `[4, 2]`, 2nd middle lands on node `2` (`mid = 2`).
  - Disconnecting `mid.next = null` sets `2.next = null`, leaving left list as `[4, 2]` and right list as `[]` $\implies$ Infinite Recursion Stack Overflow!
  - **Always use First Middle Node Split (`fast.next != null && fast.next.next != null`)**.
* **Forgetting `mid.next = null` Disconnection**: Failing to sever the link between the two halves causes infinite loops during merge.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** First Middle Node Split Rule in Linked List Merge Sort:
> When splitting a list of even length (e.g. `[4, 2]`), you MUST pick the **First Middle Node** (`node 4`).
> If you pick the second middle node (`node 2`), `mid.next = null` fails to shorten the left sub-list, causing infinite recursive calls and `StackOverflowError`!

> **Memory Trick:** **"Merge Sort Split MUST use fast.next != null && fast.next.next != null to pick 1st middle!"**

---

## 13. System & Implementation Comparisons

| Feature | Linked List Merge Sort | Array Quick Sort |
| :--- | :--- | :--- |
| **Random Access Dependency**| Zero (Sequential Traversal) | Required $O(1)$ Array Access |
| **Merge Space** | **$O(1)$ Pointer Re-linking ⚡**| $O(N)$ Auxiliary Array Space |
| **Worst-Case Time** | **Guaranteed $O(N \log N)$ ⚡**| $O(N^2)$ (Unbalanced Pivot) |

---

## 14. How to Recognize This in Questions
* **"Sort a linked list in O(n log n) time and O(1) space"** $\rightarrow$ LeetCode 148 (Linked List Merge Sort).
* **"Sort a linked list using insertion sort"** $\rightarrow$ LeetCode 147 (Insertion Sort List).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is Merge Sort $O(1)$ space for linked lists but $O(N)$ space for arrays?**  
  *A:* Array merging requires copying elements into a secondary temporary array of size $N$ to prevent overwriting unmerged elements. Linked lists merge by re-wiring existing `.next` pointer references in-place without creating new objects.
* **Q: Why does 2nd middle node selection cause infinite recursion in 2-element lists?**  
  *A:* On `[4, 2]`, 2nd middle is `2`. Setting `mid.next = null` disconnects nothing after `2`, so left sub-list remains `[4, 2]` (length 2), making zero progress and overflowing the call stack.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST SORTING ALGORITHMS                        |
+-----------------------------------------------------------------------+
| • Merge Sort Invariant: Guaranteed O(N log N) time & stable sorting ⚡ |
| • First Middle Rule: while (fast.next != null && fast.next.next != null)|
| • Mandatory Disconnect: mid.next = null before recursive calls!       |
| • Merge Step: Use mergeTwoLists(left, right) with dummy node          |
| • Bottom-Up Merge Sort: Iterative step size 1, 2, 4.. for O(1) Space ⚡ |
| • Insertion Sort (147): O(N^2) in-place insertion using dummy head    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Linked List Merge Sort (LeetCode 148) in under 5 minutes.
- [ ] I know why First Middle Node split MUST be used to avoid stack overflow.
- [ ] I can write `mergeTwoLists` and `getFirstMiddle` helper routines.
- [ ] I can solve Insertion Sort List (LeetCode 147).
- [ ] I know why Merge Sort is preferred for linked lists over Quicksort.
