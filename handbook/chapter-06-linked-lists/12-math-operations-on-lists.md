# 12. Arithmetic & Mathematical Operations on Linked Lists

## 1. Introduction
Mathematical operations on linked lists represent numbers as sequences of digit nodes. Problems such as Add Two Numbers (LeetCode 2 - digits in reverse order), Add Two Numbers II (LeetCode 445 - digits in forward order), and Plus One Linked List (LeetCode 369) test a candidate's ability to handle **Carry Propagation**, arbitrary precision arithmetic, list reversals, and stack-based digit processing in **$O(N)$ time and $O(1)$ space**.

> **Important:** Linked list arithmetic avoids integer overflow errors! Since lists can store thousands of digit nodes, they serve as a native structure for **BigInteger** arithmetic.

## 2. Core Concepts
* **Reverse Order Digits (LeetCode 2)**: Least Significant Digit (LSD) at `head` (e.g., $2 \to 4 \to 3$ represents number $342$). Single pass left-to-right addition with carry propagation.
* **Forward Order Digits (LeetCode 445)**: Most Significant Digit (MSD) at `head` (e.g., $3 \to 4 \to 2$ represents number $342$). Solved by:
  * **Option A**: Reversing input lists first, adding LSD-first, and reversing the result list ($O(N)$ time, $O(1)$ auxiliary space).
  * **Option B**: Using two Stacks to pop digits LSD-first ($O(N)$ time, $O(N)$ space).
* **Carry Propagation Formula**:
  $$\text{sum} = \text{val}_1 + \text{val}_2 + \text{carry} \implies \text{digit} = \text{sum} \% 10, \quad \text{carry} = \text{sum} / 10$$

> **Memory Trick:** **"Carry = sum / 10; Digit = sum % 10; Loop condition: while (p1 != null || p2 != null || carry != 0)"**.

## 3. Characteristics / Properties
* **Loop Condition Safety**: The addition loop MUST run while `p1 != null || p2 != null || carry != 0`. Including `carry != 0` in the loop condition automatically appends a final overflow digit node (e.g., $99 + 1 = 100$)!
* **Zero Arbitrary Precision Limits**: Processes numbers with thousands of digits without 64-bit `long` primitive overflow.

```
Linked List Arithmetic Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Digit Alignment   | Optimal Approach  | Time / Space      |
+-----------------------+-------------------+-------------------+-------------------+
| Add Two Numbers (LSD) | Reverse Order     | Single Pass       | O(N) | O(1) Aux ⚡ |
| Add Two Numbers II    | Forward Order     | Reverse -> Add    | O(N) | O(1) Aux ⚡ |
| Plus One Linked List  | Forward Order     | Reverse / Fast-Slow| O(N) | O(1) Aux ⚡|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Add Two Numbers (LeetCode 2) on $l_1 = [2 \to 4 \to 3]$ ($342$), $l_2 = [5 \to 6 \to 4]$ ($465$):

```
Initialization: dummy = [-1], curr = dummy, carry = 0

Iter 1 (l1=2, l2=5): sum = 2 + 5 + 0 = 7 -> digit = 7, carry = 0 -> Append [7]
Iter 2 (l1=4, l2=6): sum = 4 + 6 + 0 = 10 -> digit = 0, carry = 1 -> Append [0]
Iter 3 (l1=3, l2=4): sum = 3 + 4 + 1 = 8  -> digit = 8, carry = 0 -> Append [8]

Loop terminates (l1=null, l2=null, carry=0).
Result List: dummy.next -> [ 7 -> 0 -> 8 -> null ] (Represents 807 = 342 + 465) ✅
```

## 5. Visual Diagram
Carry Propagation & Final Carry Node Attachment:

```
Addition: 99 + 1 = 100

Input l1: [ 9 ] -> [ 9 ] -> null  (LSD first: 99)
Input l2: [ 1 ] -> null           (LSD first: 1)

Iter 1: 9 + 1 + 0 = 10 -> append [0], carry = 1
Iter 2: 9 + 0 + 1 = 10 -> append [0], carry = 1
Iter 3: l1=null, l2=null, carry=1 -> append [1] (Final carry node!)

Result: [ 0 ] -> [ 0 ] -> [ 1 ] -> null (100 in reverse order)
```

## 6. Operations / Algorithms
LeetCode 2 Master Implementation:

```java
public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
    ListNode dummy = new ListNode(-1);
    ListNode curr = dummy;
    int carry = 0;

    // Loop continues as long as there is a digit or remaining carry
    while (l1 != null || l2 != null || carry != 0) {
        int val1 = (l1 != null) ? l1.val : 0;
        int val2 = (l2 != null) ? l2.val : 0;

        int sum = val1 + val2 + carry;
        carry = sum / 10;
        int digit = sum % 10;

        curr.next = new ListNode(digit);
        curr = curr.next;

        if (l1 != null) l1 = l1.next;
        if (l2 != null) l2 = l2.next;
    }

    return dummy.next;
}
```

> **Quick Syntax:**
```java
// Standard Addition Loop Guard
while (l1 != null || l2 != null || carry != 0) {
    int sum = ((l1 != null) ? l1.val : 0) + ((l2 != null) ? l2.val : 0) + carry;
    carry = sum / 10;
    curr.next = new ListNode(sum % 10);
    curr = curr.next;
    if (l1 != null) l1 = l1.next;
    if (l2 != null) l2 = l2.next;
}
```

## 7. Examples
* **LeetCode 2 - Add Two Numbers**: Single pass LSD addition.
* **LeetCode 445 - Add Two Numbers II**: Forward order addition using reversal or stacks.
* **LeetCode 369 - Plus One Linked List**: Adding 1 to forward-order linked list.

## 8. Java Code
Complete interview-ready Java suite implementing Add Two Numbers, Add Two Numbers II, and Plus One Linked List:

```java
public class MathOperationsOnListsMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Add Two Numbers LSD First (LeetCode 2) O(N) Time, O(N) Output Space
    public static ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(-1);
        ListNode curr = dummy;
        int carry = 0;

        while (l1 != null || l2 != null || carry != 0) {
            int v1 = (l1 != null) ? l1.val : 0;
            int v2 = (l2 != null) ? l2.val : 0;

            int sum = v1 + v2 + carry;
            carry = sum / 10;

            curr.next = new ListNode(sum % 10);
            curr = curr.next;

            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }

        return dummy.next;
    }

    // 2. Add Two Numbers II MSD First (LeetCode 445) O(N) Time, O(1) Auxiliary Space
    public static ListNode addTwoNumbersII(ListNode l1, ListNode l2) {
        // Step 1: Reverse input lists
        ListNode r1 = reverse(l1);
        ListNode r2 = reverse(l2);

        // Step 2: Add reversed LSD lists
        ListNode sumLSD = addTwoNumbers(r1, r2);

        // Step 3: Reverse result back to forward order
        return reverse(sumLSD);
    }

    // Helper: Reverse List In-Place
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
        // l1 = 2 -> 4 -> 3 (342)
        ListNode l1 = new ListNode(2);
        l1.next = new ListNode(4);
        l1.next.next = new ListNode(3);

        // l2 = 5 -> 6 -> 4 (465)
        ListNode l2 = new ListNode(5);
        l2.next = new ListNode(6);
        l2.next.next = new ListNode(4);

        ListNode sum = addTwoNumbers(l1, l2);
        System.out.print("342 + 465 (LSD First): ");
        printList(sum); // Output: 7 -> 0 -> 8 -> null (807)
    }
}
```

## 9. Complexity Analysis
| Problem | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Add Two Numbers (LSD)** | **$O(\max(N_1, N_2))$** | **$O(1)$ Auxiliary** | Single pass |
| **Add Two Numbers II (Reversal)**| **$O(N_1 + N_2)$** | **$O(1)$ Auxiliary ⚡**| Reverse $\to$ Add $\to$ Reverse |
| **Add Two Numbers II (Stack)** | $O(N_1 + N_2)$ | $O(N_1 + N_2)$ Stack | Avoids input list mutation |

## 10. Edge Cases
* **Final Carry Overflow (e.g., $99 + 1 = 100$)**: Including `carry != 0` in the while loop condition automatically appends the final carry digit node.
* **Lists of Unequal Lengths**: Handled by ternary checks `(l1 != null) ? l1.val : 0`.
* **Zero Input (`0 + 0 = 0`)**: Loop runs once, returning single `[0]` node.

## 11. Common Mistakes
* Omitting `carry != 0` from the loop condition (truncates the final carry node, e.g. returning $99 + 1 = 00$ instead of $100$!).
* Forgetting to update `l1 = l1.next` and `l2 = l2.next` inside the loop (causes infinite loop!).
* Converting linked list digits into a primitive `long` or `int` variable (causes arithmetic integer overflow for long lists!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never convert linked list digits to `long` or `BigInteger`!
> Do NOT write: `long num1 = convertToListNum(l1); long sum = num1 + num2;`
> This fails interview constraints when inputs contain 100+ digit nodes! Always implement digit-by-digit stream addition with `carry = sum / 10` and `digit = sum % 10`.

> **Memory Trick:** **"Loop condition: while (l1 != null || l2 != null || carry != 0)"**.

## 13. Comparisons
| Feature | Reverse Input Lists First | Dual Stack Processing |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N_1 + N_2)$ | $O(N_1 + N_2)$ |
| **Auxiliary Space** | **$O(1)$ Auxiliary Space ⚡** | $O(N_1 + N_2)$ Stack Memory |
| **Input Modification**| Modifies then restores | Read-only |
| **Interview Recommendation** | **PREFERRED FOR O(1) SPACE**| Secondary |

## 14. How to Recognize This in Questions
* **"Add two numbers represented as linked lists with LSD at head"** $\rightarrow$ Single Pass Addition with Carry.
* **"Add two numbers represented as linked lists with MSD at head"** $\rightarrow$ Reverse $\to$ Add $\to$ Reverse.

## 15. Frequently Asked Interview Questions
* **Q: Why is `carry != 0` included in the addition loop condition?**  
  *A:* Including `carry != 0` ensures that when both lists reach `null` but a non-zero carry remains (e.g. $99 + 1$), the loop executes one additional iteration to append a new node with value `carry`.
* **Q: How does `(l1 != null) ? l1.val : 0` handle lists of different lengths?**  
  *A:* When the shorter list finishes traversing, its pointer evaluates to `null`. The ternary operator supplies `0` for missing digits, allowing addition to continue seamlessly until the longer list finishes.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ARITHMETIC OPERATIONS ON LINKED LISTS                 |
+-----------------------------------------------------------------------+
| • Loop Condition: while (l1 != null || l2 != null || carry != 0)      |
| • Sum Formula: sum = val1 + val2 + carry; carry = sum / 10;           |
| • Node Creation: curr.next = new ListNode(sum % 10);                  |
| • MSD First Trick (Add Two II): Reverse l1 & l2 -> Add -> Reverse sum|
| • Complexity: O(N) Linear Time | O(1) Auxiliary Space (Optimal!)     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `carry != 0` must be in the `while` loop condition.
- [ ] I can write the digit-by-digit stream addition loop from memory.
- [ ] I know why converting linked list digits to primitive `long` fails.
- [ ] I can implement Add Two Numbers II (LeetCode 445) in $O(1)$ auxiliary space.
- [ ] I can handle lists of unequal lengths using ternary operators.
