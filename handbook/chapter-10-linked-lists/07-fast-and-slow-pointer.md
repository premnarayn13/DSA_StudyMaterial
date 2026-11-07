# 07. Fast & Slow Pointer Pattern, Middle Finding & $K$-th Node Operations

## 1. Introduction
The **Fast & Slow Pointer Pattern** (also known as the **Tortoise and Hare Algorithm**) is a core two-pointer strategy tailored for linked lists. By advancing two pointers at different speeds—typically a `slow` pointer moving 1 step at a time (`slow = slow.next`) and a `fast` pointer moving 2 steps at a time (`fast = fast.next.next`)—this pattern solves complex pointer problems in a **single pass with $O(N)$ linear time and $O(1)$ constant auxiliary space**.

> **Important:** Fast & Slow pointer techniques eliminate the need to calculate list length $N$ in a preliminary pass! Whether finding the **Middle Node (LeetCode 876)**, deleting the **$N$-th Node From End of List (LeetCode 19)**, or checking if a list is a **Palindrome (LeetCode 234)**, fast and slow pointers achieve optimal single-pass execution!

```
Fast & Slow Pointer Speed Differential:
+-----------------------------------------------------------------------------------+
| Slow Pointer (1x Speed) : Advances 1 node per iteration  (`slow = slow.next`)     |
| Fast Pointer (2x Speed) : Advances 2 nodes per iteration (`fast = fast.next.next`)|
| Invariant               : When fast reaches end, slow is AT THE MIDDLE NODE! ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Finding Middle of Linked List (Even vs Odd Length Invariants)
Given the `head` node of a Singly Linked List:
* **Odd Length List (`1 -> 2 -> 3 -> 4 -> 5`)**:
  - Loop condition: `while (fast != null && fast.next != null)`
  - When `fast` reaches node 5 (`fast.next == null`), `slow` lands EXACTLY on node 3 (**exact middle**).
* **Even Length List (`1 -> 2 -> 3 -> 4 -> 5 -> 6`)**:
  - **Second Middle Variant (`LeetCode 876`)**: Condition `while (fast != null && fast.next != null)`. `slow` lands on node 4 (**second middle**).
  - **First Middle Variant (For List Splitting)**: Condition `while (fast.next != null && fast.next.next != null)`. `slow` lands on node 3 (**first middle**).

```
Even Length Middle Selection Invariants:
Second Middle (876) : while (fast != null && fast.next != null)        ===> Slow = Node 4
First Middle (Split): while (fast.next != null && fast.next.next != null) ===> Slow = Node 3
```

### 2.2 Finding $K$-th Node From End of List (LeetCode 19)
To remove or find the $K$-th node from the end of a linked list in a SINGLE pass:
1. Use a **Dummy Sentinel Node** `dummy` pointing to `head`.
2. Initialize `fast = dummy`, `slow = dummy`.
3. Advance `fast` pointer $K + 1$ steps ahead.
4. Advance BOTH `fast` and `slow` pointers 1 step at a time until `fast == null`.
5. `slow.next` is now the target $K$-th node from the end! Delete target via **`slow.next = slow.next.next`**.

```
Removing 2nd Node From End on List [1, 2, 3, 4, 5] (K = 2):
1. Advance fast 2+1 = 3 steps ahead: fast points to Node 3.
2. Advance fast and slow together until fast is null:
   - Step 1: slow -> 1, fast -> 4
   - Step 2: slow -> 2, fast -> 5
   - Step 3: slow -> 3, fast -> null
3. slow is at Node 3 (predecessor of Node 4). Set 3.next = 5!
Result: [1, 2, 3, 5] ✅ (Single-pass O(N) Time, O(1) Space!)
```

> **Memory Trick:** **"Fast & Slow Middle: fast moves 2x, slow moves 1x! K-th from end: advance fast K+1 steps first!"**

---

## 3. Characteristics & Palindrome Linked List Architecture

### 3.1 Palindrome Linked List Verification (LeetCode 234)
To verify if a singly linked list is a palindrome in $O(N)$ time and $O(1)$ space:
1. **Find First Middle**: Use fast and slow pointers (`fast.next != null && fast.next.next != null`) to find the end of the first half.
2. **Reverse Second Half**: In-place reverse the sub-list starting at `slow.next` using 3-pointer iterative reversal.
3. **Compare Halves**: Compare values starting from `p1 = head` and `p2 = reversedSecondHalfHead`.
4. **Restore List (Optional)**: Re-reverse the second half back to preserve original data structure.

```
Palindrome Verification Protocol [ 1, 2, 2, 1 ]:
1. Find Middle  : slow lands on 2 (first half end).
2. Reverse 2nd  : Reverse [2, 1] -> [1, 2]. List becomes 1 -> 2 and 1 -> 2.
3. Compare      : p1(1)==p2(1), p1(2)==p2(2) -> Is Palindrome = true! ✅
```

---

## 4. Internal Working Mechanics
Tracing Middle Finding on `[1, 2, 3, 4, 5, 6]`:

```
Init: slow = 1, fast = 1

Pass 1: slow = 2, fast = 3 (fast.next != null)
Pass 2: slow = 3, fast = 5 (fast.next != null)
Pass 3: fast = 5 -> fast.next.next is null! Loop terminates.

Second Middle (LeetCode 876):
Condition: while (fast != null && fast.next != null)
Pass 3: slow = 4, fast = null! Loop terminates -> slow = Node 4 ✅
```

---

## 5. Visual Diagram
Fast & Slow Pointer Speed Gap Topology:

```
Step 0:  ( S, F ) -> 1 -> 2 -> 3 -> 4 -> 5 -> null
Step 1:   1 -> ( S ) -> 2 -> ( F ) -> 3 -> 4 -> 5 -> null
Step 2:   1 -> 2 -> ( S ) -> 3 -> 4 -> ( F ) -> null

Slow is at Node 3 (Exact Middle of 5 nodes!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Middle Finding (LeetCode 876), Remove N-th Node From End (LeetCode 19), and Palindrome Verification (LeetCode 234):

```java
import java.util.*;

public class FastSlowPointerMaster {

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

    // 1. Find Middle of Linked List (LeetCode 876) O(N) Time, O(1) Space
    public static ListNode findMiddle(ListNode head) {
        if (head == null) return null;
        ListNode slow = head;
        ListNode fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow; // Returns second middle for even length
    }

    // 2. Find First Middle (For Splitting List into Two Equal Halves)
    public static ListNode findFirstMiddle(ListNode head) {
        if (head == null) return null;
        ListNode slow = head;
        ListNode fast = head;

        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        return slow; // Returns first middle for even length
    }

    // 3. Remove N-th Node From End of List (LeetCode 19) O(N) Time, O(1) Space
    public static ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0, head);
        ListNode fast = dummy;
        ListNode slow = dummy;

        // Advance fast (n + 1) steps ahead
        for (int i = 0; i <= n; i++) {
            if (fast == null) return head; // n out of bounds
            fast = fast.next;
        }

        // Advance both until fast reaches end
        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }

        // Delete target node (slow.next)
        ListNode target = slow.next;
        slow.next = target.next;
        target.next = null; // Unlink for GC

        return dummy.next;
    }

    // 4. Palindrome Linked List (LeetCode 234) O(N) Time, O(1) Auxiliary Space
    public static boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) return true;

        // Step 1: Find first middle
        ListNode firstMiddle = findFirstMiddle(head);

        // Step 2: Reverse second half
        ListNode secondHalfHead = reverseList(firstMiddle.next);

        // Step 3: Compare values
        ListNode p1 = head;
        ListNode p2 = secondHalfHead;
        boolean isPalin = true;

        while (p2 != null) {
            if (p1.val != p2.val) {
                isPalin = false;
                break;
            }
            p1 = p1.next;
            p2 = p2.next;
        }

        // Step 4: Restore original list structure
        firstMiddle.next = reverseList(secondHalfHead);

        return isPalin;
    }

    private static ListNode reverseList(ListNode head) {
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
}
```

> **Quick Syntax:**
```java
// Remove N-th From End Fast Gap Loop
ListNode fast = dummy, slow = dummy;
for (int i = 0; i <= n; i++) fast = fast.next;
while (fast != null) { slow = slow.next; fast = fast.next; }
slow.next = slow.next.next;
```

---

## 7. Concrete Problem Examples
* **LeetCode 876 - Middle of the Linked List**: Fast and slow middle finder.
* **LeetCode 19 - Remove Nth Node From End of List**: Single-pass gap traversal.
* **LeetCode 234 - Palindrome Linked List**: Middle + Reverse + Compare strategy.

---

## 8. Java Code Demonstration & Dry Run
Demonstration finding middle node, removing N-th from end, and checking palindrome:

```java
public class FastSlowPointerDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Find Middle Node (LeetCode 876) ===");
        FastSlowPointerMaster.ListNode head = new FastSlowPointerMaster.ListNode(1);
        head.next = new FastSlowPointerMaster.ListNode(2);
        head.next.next = new FastSlowPointerMaster.ListNode(3);
        head.next.next.next = new FastSlowPointerMaster.ListNode(4);
        head.next.next.next.next = new FastSlowPointerMaster.ListNode(5);

        FastSlowPointerMaster.ListNode mid = FastSlowPointerMaster.findMiddle(head);
        System.out.println("Middle Node Value: " + mid.val); // Output: 3

        System.out.println("\n=== 2. Remove 2nd Node From End (LeetCode 19) ===");
        FastSlowPointerMaster.ListNode updatedHead = FastSlowPointerMaster.removeNthFromEnd(head, 2);
        System.out.print("Updated List: ");
        while (updatedHead != null) {
            System.out.print(updatedHead.val + " -> ");
            updatedHead = updatedHead.next;
        }
        System.out.println("null"); // Output: 1 -> 2 -> 3 -> 5 -> null

        System.out.println("\n=== 3. Palindrome Check [1, 2, 2, 1] (LeetCode 234) ===");
        FastSlowPointerMaster.ListNode palin = new FastSlowPointerMaster.ListNode(1);
        palin.next = new FastSlowPointerMaster.ListNode(2);
        palin.next.next = new FastSlowPointerMaster.ListNode(2);
        palin.next.next.next = new FastSlowPointerMaster.ListNode(1);

        System.out.println("Is Palindrome? " + FastSlowPointerMaster.isPalindrome(palin)); // Output: true
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Middle Finding (876)** | **$O(N)$ Single Pass ⚡**| **$O(1)$ Strict In-Place ⚡**| `fast` moves 2x, `slow` moves 1x |
| **Remove N-th From End (19)**| **$O(N)$ Single Pass ⚡**| **$O(1)$ Strict In-Place ⚡**| Advance `fast` $N+1$ steps first |
| **Palindrome Check (234)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Middle + Reverse 2nd Half + Compare |

---

## 10. Edge Cases & Boundary Handling
* **Removing Head Node ($N = \text{length}$)**: Dummy sentinel node `dummy` ensures `slow` remains before `head`, allowing `dummy.next = head.next` to execute cleanly.
* **Even Length Middle Selection**: Choose `fast != null && fast.next != null` for 2nd middle, vs `fast.next != null && fast.next.next != null` for 1st middle.

---

## 11. Common Mistakes & Anti-Patterns
* **Dereferencing `fast.next.next` Without Checking `fast.next != null`**:
  - If `fast.next` is `null`, evaluating `fast.next.next` causes `NullPointerException`!
  - **Always check `while (fast != null && fast.next != null)`**.
* **Two-Pass Length Counting for $N$-th Node From End**:
  - Counting length $N$ in pass 1, then traversing $N-K$ in pass 2 requires 2 full traversals.
  - **Use Fast & Slow gap pointer for single-pass $O(N)$ execution**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Single-Pass $K$-th Node Gap Rule:
> To find the $K$-th node from the end, create a **Gap of size $K$** between `fast` and `slow`.
> When `fast` reaches the end of the list (`null`), `slow` is guaranteed to be at the node right BEFORE the target node!

> **Memory Trick:** **"Gap of size K+1 between fast and slow points slow directly to the predecessor node!"**

---

## 13. System & Implementation Comparisons

| Feature | Fast & Slow Pointer Gap | Two-Pass Length Calculation |
| :--- | :--- | :--- |
| **List Passes** | **1 Single Pass ⚡** | 2 Full Passes |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(1)$ |

---

## 14. How to Recognize This in Questions
* **"Find middle node of linked list in a single pass"** $\rightarrow$ LeetCode 876 (`fast` moves 2x, `slow` moves 1x).
* **"Remove N-th node from end of linked list in one pass"** $\rightarrow$ LeetCode 19 (Advance `fast` $N+1$ steps first).
* **"Determine if linked list is a palindrome in O(1) space"** $\rightarrow$ LeetCode 234 (Middle + Reverse 2nd half).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does advancing `fast` by $N+1$ steps position `slow` at the predecessor node in LeetCode 19?**  
  *A:* Because there are $N$ nodes from the target node to the end. Maintaining a gap of $N+1$ nodes ensures that when `fast` reaches `null` (1 step past the tail), `slow` is exactly 1 node BEFORE the target node.
* **Q: Why is it important to restore the second half of a linked list after palindrome checking?**  
  *A:* In production software, data structures passed into read-only query methods should not suffer permanent structural mutations as an unexpected side effect.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FAST & SLOW POINTER PATTERN                           |
+-----------------------------------------------------------------------+
| • Middle Finding: slow = slow.next, fast = fast.next.next             |
| • 2nd Middle (876): while (fast != null && fast.next != null)          |
| • 1st Middle (Split): while (fast.next != null && fast.next.next != null)|
| • Remove N-th From End (19): Advance fast N+1 steps ahead first!      |
| • Palindrome Check (234): Middle -> Reverse 2nd Half -> Compare -> Restore|
| • Space Complexity: Strictly O(1) Auxiliary Space across all patterns ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write middle node finding (LeetCode 876) in under 1 minute.
- [ ] I know the difference between 1st middle and 2nd middle loop conditions.
- [ ] I can write single-pass Remove N-th Node From End (LeetCode 19).
- [ ] I can write Palindrome Linked List (LeetCode 234) in $O(1)$ space.
- [ ] I know why `fast.next != null` MUST be checked before `fast.next.next`.
