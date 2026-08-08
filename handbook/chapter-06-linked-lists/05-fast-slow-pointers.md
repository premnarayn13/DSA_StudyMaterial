# 05. Fast & Slow Pointers (Floyd's Tortoise & Hare)

## 1. Introduction
The **Fast and Slow Pointers** pattern (also known as Floyd's Tortoise and Hare algorithm) is a two-pointer technique where two pointers traverse a linked list at different speeds: a `slow` pointer advancing 1 step at a time (`slow = slow.next`) and a `fast` pointer advancing 2 steps at a time (`fast = fast.next.next`). In technical coding interviews, this pattern solves finding the **Middle of a Linked List** (LeetCode 876), **$N$-th Node from End** (LeetCode 19), **Palindrome Linked List** (LeetCode 234), and **Cycle Detection** in **$O(N)$ time and $O(1)$ space**.

> **Important:** The loop condition for Fast & Slow Pointers MUST check BOTH `fast` AND `fast.next`: **`while (fast != null && fast.next != null)`**. Missing `fast.next != null` triggers a `NullPointerException` when calling `fast.next.next`!

## 2. Core Concepts
* **Middle Node Finding**: When `fast` reaches the end of the list (`null`), `slow` sits exactly at the **middle node**!
  * **Odd Length List ($N=5$)**: `slow` stops at the exact middle (node 3).
  * **Even Length List ($N=6$)**: `slow` stops at the 2nd middle (node 4). (If 1st middle is desired, use `while (fast.next != null && fast.next.next != null)`).
* **$N$-th Node from End (Gap Technique)**: Advance `fast` pointer $N$ steps ahead first. Then advance both `fast` and `slow` 1 step at a time until `fast == null`. `slow` will sit at the $N$-th node from the end!
* **Palindrome Linked List**: Find middle node using Fast/Slow pointers, reverse second half in-place, and compare first half against reversed second half in $O(N)$ time and $O(1)$ space.

> **Memory Trick:** **"Fast moves 2 steps, Slow moves 1 step! When Fast hits the end, Slow is in the middle!"**

## 3. Characteristics / Properties
* **$O(1)$ Auxiliary Space**: Eliminates the need to copy linked list nodes into an auxiliary array or ArrayList to find middle/palindrome elements.
* **Single Pass Efficiency**: Finds middle or $N$-th node from end in a single linear pass without calculating total list length $N$ first.

```
Fast & Slow Pointer Applications Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Application | Fast Speed        | Slow Speed        | Target Result     |
+-----------------------+-------------------+-------------------+-------------------+
| Find Middle Node      | 2 steps / iter    | 1 step / iter     | `slow` is middle  |
| N-th Node from End    | Advance N steps   | Advance 1 step    | `slow` is target  |
| Palindrome Check      | 2 steps / iter    | 1 step / iter     | Compare 1st & 2nd |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Middle Node Finding on `1 -> 2 -> 3 -> 4 -> 5 -> null` ($N = 5$):

```
Init: slow = 1, fast = 1

Step 1:
- slow = slow.next -> 2
- fast = fast.next.next -> 3
List: 1 -> [2(slow)] -> [3(fast)] -> 4 -> 5 -> null

Step 2:
- slow = slow.next -> 3
- fast = fast.next.next -> 5
List: 1 -> 2 -> [3(slow)] -> 4 -> [5(fast)] -> null

Step 3:
- Loop check: fast.next is null! Loop terminates.

Result: slow sits at Node 3 (Exact Middle Node!) ✅
```

## 5. Visual Diagram
Fast & Slow Pointer Middle Traversal:

```
Odd Length List (N = 5):
[ 1 ] ---> [ 2 ] ---> [ 3 ] ---> [ 4 ] ---> [ 5 ] ---> null
                        ^                     ^
                      slow                  fast
                  (Exact Middle)         (Last Node)

Even Length List (N = 6):
[ 1 ] ---> [ 2 ] ---> [ 3 ] ---> [ 4 ] ---> [ 5 ] ---> [ 6 ] ---> null
                                   ^                                ^
                                 slow                             fast
                             (2nd Middle)                        (null)
```

## 6. Operations / Algorithms
LeetCode 876 & LeetCode 19 Master Implementation:

```java
// 1. Find Middle Node of Linked List (LeetCode 876) O(N) Time, O(1) Space
public ListNode middleNode(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;        // 1 step
        fast = fast.next.next;   // 2 steps
    }

    return slow; // Returns 2nd middle for even length lists
}

// 2. Remove N-th Node From End of List (LeetCode 19) O(N) Time, O(1) Space
public ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(-1);
    dummy.next = head;
    ListNode fast = dummy;
    ListNode slow = dummy;

    // Advance fast pointer n + 1 steps ahead
    for (int i = 0; i <= n; i++) {
        fast = fast.next;
    }

    // Move both pointers until fast hits null
    while (fast != null) {
        slow = slow.next;
        fast = fast.next;
    }

    // slow is now right before the N-th node from end!
    slow.next = slow.next.next; // Unlink target node

    return dummy.next;
}
```

> **Quick Syntax:**
```java
// Fast & Slow Pointer Loop Boundary
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}
```

## 7. Examples
* **LeetCode 876 - Middle of the Linked List**: Standard Fast/Slow pointer application.
* **LeetCode 19 - Remove Nth Node From End of List**: Fast/Slow gap technique with Dummy Head.
* **LeetCode 234 - Palindrome Linked List**: Fast/Slow middle find + In-place reversal of second half.

## 8. Java Code
Complete interview-ready Java suite implementing Middle Node, Remove $N$-th From End, and Palindrome Linked List (LeetCode 234):

```java
public class FastSlowPointersMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Find Middle Node O(N) Time, O(1) Space
    public static ListNode findMiddle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    // 2. Palindrome Linked List Check (LeetCode 234) O(N) Time, O(1) Space
    public static boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) return true;

        // Step 1: Find middle using Fast/Slow pointers
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // Step 2: Reverse second half in-place
        ListNode secondHalf = reverseList(slow);
        ListNode firstHalf = head;

        // Step 3: Compare first half and reversed second half
        ListNode p1 = firstHalf, p2 = secondHalf;
        boolean isPalin = true;
        while (p2 != null) {
            if (p1.val != p2.val) {
                isPalin = false;
                break;
            }
            p1 = p1.next;
            p2 = p2.next;
        }

        // Step 4: Restore second half back to original state (Good Hygiene)
        reverseList(secondHalf);

        return isPalin;
    }

    // Helper: Reverse List In-Place
    private static ListNode reverseList(ListNode head) {
        ListNode prev = null, curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        return prev;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct Palindrome: 1 -> 2 -> 2 -> 1 -> null
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(2);
        head.next.next.next = new ListNode(1);

        System.out.println("Middle Node Value: " + findMiddle(head).val); // Output: 2
        System.out.println("Is Palindrome? " + isPalindrome(head));        // Output: true
    }
}
```

## 9. Complexity Analysis
| Application | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Middle Node Search** | **$O(N)$ Linear** | **$O(1)$ Constant** | Single pass |
| **Remove N-th From End**| **$O(N)$ Linear** | **$O(1)$ Constant** | Gap pointer technique |
| **Palindrome Check** | **$O(N)$ Linear** | **$O(1)$ Constant** | Reverses 2nd half in-place |

## 10. Edge Cases
* **Even vs Odd Length Lists**: For even lengths, standard `fast != null && fast.next != null` returns the **second** middle node.
* **$N$ Equals List Length in Remove $N$-th From End**: Removing the head node! **Fix**: Always use a Dummy Head Node (`dummy.next = head`) so `slow` points to `dummy` (node 0).
* **Single Node List**: Fast/Slow loop exits immediately; returns `head`.

## 11. Common Mistakes
* Writing `while (fast.next != null)` without checking `fast != null` first (triggers `NullPointerException` on even length lists when `fast` is `null`).
* Forgetting to use a Dummy Head Node in Remove $N$-th From End (crashes when removing the head node).
* Not restoring the reversed second half back to its original order in Palindrome Linked List (violates read-only input contracts).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Always write Fast & Slow pointer loop condition as:
> **`while (fast != null && fast.next != null)`**
> Order matters! `fast != null` MUST be evaluated before `fast.next != null` to prevent `NullPointerException` short-circuiting!

> **Memory Trick:** **"Fast != null FIRST, fast.next != null SECOND!"**

## 13. Comparisons
| Metric | Single Pass (Fast/Slow Pointers) | Two Pass (Count Length First) |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ (1 Pass)** | $O(N)$ (2 Passes) |
| **Code Length** | Short & Elegant | Longer |
| **Streaming List Support**| **YES** | NO (Cannot recount stream) |
| **Interview Recommendation** | **PREFERRED & EXPECTED**| Acceptable Naive |

## 14. How to Recognize This in Questions
* **"Find middle node of linked list in 1 pass"** $\rightarrow$ Fast & Slow Pointers (`slow = slow.next, fast = fast.next.next`).
* **"Remove N-th node from end of list in 1 pass"** $\rightarrow$ Fast & Slow Gap Technique with Dummy Head.
* **"Check if linked list is a palindrome in O(1) space"** $\rightarrow$ Fast/Slow Middle + Reverse 2nd Half.

## 15. Frequently Asked Interview Questions
* **Q: Why does Fast & Slow pointers find the exact middle node?**  
  *A:* Because `fast` moves at twice the speed of `slow` ($2v$ vs $v$). When `fast` covers distance $D = N$, `slow` has covered distance $d = N/2$, placing `slow` at the exact middle of the list.
* **Q: How do you get the FIRST middle node instead of the SECOND middle node for even-length lists?**  
  *A:* Change the loop condition to: **`while (fast.next != null && fast.next.next != null)`**.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FAST & SLOW POINTERS                                  |
+-----------------------------------------------------------------------+
| • Loop Condition: while (fast != null && fast.next != null)           |
| • Speeds: slow = slow.next (1 step), fast = fast.next.next (2 steps)  |
| • Middle Node: When fast hits null/tail, slow is at the middle node   |
| • Remove N-th From End: Advance fast N+1 steps ahead, then move both  |
| • Palindrome List: Find middle -> Reverse 2nd half -> Compare halves   |
| • Auxiliary Space: O(1) Constant Space for all operations             |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the `while (fast != null && fast.next != null)` guard from memory.
- [ ] I can find the middle node of a linked list in a single pass.
- [ ] I can remove the $N$-th node from end using Fast/Slow gap technique with Dummy Head.
- [ ] I can solve Palindrome Linked List (LeetCode 234) in $O(1)$ space.
- [ ] I know how to get the 1st middle vs 2nd middle node for even-length lists.
