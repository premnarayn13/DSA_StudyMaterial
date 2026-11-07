# 09. Merge & Intersection Algorithms, Two-Pointer Alignment & Boundary Handling

## 1. Introduction
Merging two sorted sequences and finding the intersection node of two converging linked lists are fundamental algorithmic operations. Problems like **Merge Two Sorted Lists (LeetCode 21)** and **Intersection of Two Linked Lists (LeetCode 160)** demonstrate how 2-pointer techniques can manipulate list structures in **$O(M + N)$ linear time and $O(1)$ constant auxiliary space**.

> **Important:** In Intersection of Two Linked Lists (LeetCode 160), the **2-Pointer Length Alignment Trick (`pA = (pA == null) ? headB : pA.next`)** eliminates the need to calculate list lengths $M$ and $N$ beforehand! By making pointer $A$ traverse list $A + B$ and pointer $B$ traverse list $B + A$, both pointers cover identical total distances ($M + N$) and collide PRECISELY at the intersection node!

```
Intersection 2-Pointer Equivalence:
+-----------------------------------------------------------------------------------+
| Path A: Length M (List A) + Length N (List B) = Total Distance M + N               |
| Path B: Length N (List B) + Length M (List A) = Total Distance M + N               |
| Invariant: Both pointers collide at Intersection Node or null at step M + N! ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Merge Two Sorted Lists (LeetCode 21)
Given heads of two sorted singly linked lists `l1` and `l2`:
1. Use a **Dummy Sentinel Node** `dummy = new ListNode(0)` and `curr = dummy`.
2. While `l1 != null && l2 != null`:
   - If `l1.val <= l2.val`: `curr.next = l1; l1 = l1.next;`
   - Else: `curr.next = l2; l2 = l2.next;`
   - `curr = curr.next;`
3. Append remaining nodes: **`curr.next = (l1 != null) ? l1 : l2;`**
4. Return `dummy.next`!

```
Merging [1, 3, 5] and [2, 4]:
Pass 1: Compare 1 vs 2 -> Take 1. curr = 1. l1 = 3.
Pass 2: Compare 3 vs 2 -> Take 2. curr = 2. l2 = 4.
Pass 3: Compare 3 vs 4 -> Take 3. curr = 3. l1 = 5.
Pass 4: Compare 5 vs 4 -> Take 4. curr = 4. l2 = null.
Loop ends. Append remaining l1 (5): curr.next = 5.
Result: 1 -> 2 -> 3 -> 4 -> 5 -> null ✅ (O(M + N) Time, O(1) Space!)
```

### 2.2 Intersection of Two Linked Lists (LeetCode 160)
Given heads `headA` and `headB` of two linked lists that merge at a common node:

#### Two Pointer Swap Protocol:
1. Initialize `pA = headA`, `pB = headB`.
2. While `pA != pB`:
   - `pA = (pA == null) ? headB : pA.next;`
   - `pB = (pB == null) ? headA : pB.next;`
3. Return `pA` (either the intersection node or `null` if no intersection exists!).

```
Intersection 2-Pointer Alignment Proof:
List A: [ a1, a2, c1, c2, c3 ] (M = 5)
List B: [ b1, b2, b3, c1, c2, c3 ] (N = 6)
Common Intersection: [ c1, c2, c3 ]

Pointer A Path: a1 -> a2 -> c1 -> c2 -> c3 -> (null -> b1) -> b2 -> b3 -> c1 (Match!)
Pointer B Path: b1 -> b2 -> b3 -> c1 -> c2 -> c3 -> (null -> a1) -> a2 -> c1 (Match!)
Total steps taken by both = 5 + 6 - 3 = 8 steps. Collision at c1! ✅
```

> **Memory Trick:** **"Intersection of two lists: pA = (pA == null) ? headB : pA.next! Collides at intersection or null in O(M+N) time!"**

---

## 3. Characteristics & Alternative Intersection Strategies

### 3.3 Difference of Lengths Strategy for Intersection ($O(M + N)$ Time, $O(1)$ Space)
Alternative approach without pointer swapping:
1. Calculate length $M$ of list $A$ and length $N$ of list $B$.
2. Calculate difference $D = |M - N|$.
3. Advance pointer of the **longer list** $D$ steps ahead.
4. Advance both pointers 1 step at a time until `pA == pB`.

```
Length Difference Alignment:
Length A = 5, Length B = 7 -> Diff = 2.
Advance pB 2 steps ahead: pB is now aligned with pA!
Advance both together until pA == pB.
```

---

## 4. Internal Working Mechanics
Tracing Merge Two Sorted Lists on `l1: [1, 2, 4]` and `l2: [1, 3, 4]`:

```
Init: dummy -> null, curr = dummy

Step 1: 1 <= 1 -> curr.next = l1(1). l1 = 2. curr = 1.
Step 2: 2 > 1  -> curr.next = l2(1). l2 = 3. curr = 1.
Step 3: 2 <= 3 -> curr.next = l1(2). l1 = 4. curr = 2.
Step 4: 4 > 3  -> curr.next = l2(3). l2 = 4. curr = 3.
Step 5: 4 <= 4 -> curr.next = l1(4). l1 = null. curr = 4.
Loop Ends. Append l2(4): curr.next = 4.

Result: dummy -> 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> null ✅
```

---

## 5. Visual Diagram
Intersection 2-Pointer Path Concatenation Topography:

```
List A:  A1 ---> A2 ---\
                        +---> C1 ---> C2 ---> C3 ---> null (Shared Tail)
List B:  B1 ---> B2 ---> B3 ---/

Pointer A Traverses: A1 -> A2 -> C1 -> C2 -> C3 -> B1 -> B2 -> B3 -> [ C1 ]
Pointer B Traverses: B1 -> B2 -> B3 -> C1 -> C2 -> C3 -> A1 -> A2 -> [ C1 ]
Both reach C1 simultaneously!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Merge Two Sorted Lists (LeetCode 21), Intersection of Two Linked Lists (LeetCode 160 - Both 2-Pointer Swap and Length Difference methods), and Add Two Numbers (LeetCode 2):

```java
import java.util.*;

public class MergeIntersectionMaster {

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

    // 1. Merge Two Sorted Lists (LeetCode 21) O(M + N) Time, O(1) Space
    public static ListNode mergeTwoLists(ListNode l1, ListNode l2) {
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

        // Append remaining nodes
        curr.next = (l1 != null) ? l1 : l2;

        return dummy.next;
    }

    // 2. Intersection of Two Linked Lists 2-Pointer Swap (LeetCode 160) O(M + N) Time, O(1) Space
    public static ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        if (headA == null || headB == null) return null;

        ListNode pA = headA;
        ListNode pB = headB;

        while (pA != pB) {
            pA = (pA == null) ? headB : pA.next;
            pB = (pB == null) ? headA : pB.next;
        }

        return pA; // Returns intersection node or null
    }

    // 3. Intersection of Two Linked Lists Length Difference Strategy O(M + N) Time, O(1) Space
    public static ListNode getIntersectionNodeLengthDiff(ListNode headA, ListNode headB) {
        int lenA = getLength(headA);
        int lenB = getLength(headB);

        ListNode pA = headA;
        ListNode pB = headB;

        // Advance longer list pointer
        while (lenA > lenB) {
            pA = pA.next;
            lenA--;
        }
        while (lenB > lenA) {
            pB = pB.next;
            lenB--;
        }

        // Traverse together until collision
        while (pA != pB) {
            pA = pA.next;
            pB = pB.next;
        }

        return pA;
    }

    private static int getLength(ListNode head) {
        int len = 0;
        while (head != null) {
            len++;
            head = head.next;
        }
        return len;
    }

    // 4. Add Two Numbers represented by Linked Lists (LeetCode 2) O(max(M, N)) Time
    public static ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        int carry = 0;

        while (l1 != null || l2 != null || carry != 0) {
            int sum = carry;
            if (l1 != null) {
                sum += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                sum += l2.val;
                l2 = l2.next;
            }

            carry = sum / 10;
            curr.next = new ListNode(sum % 10);
            curr = curr.next;
        }

        return dummy.next;
    }
}
```

> **Quick Syntax:**
```java
// 2-Pointer Swap Intersection Syntax
ListNode pA = headA, pB = headB;
while (pA != pB) {
    pA = (pA == null) ? headB : pA.next;
    pB = (pB == null) ? headA : pB.next;
}
return pA;
```

---

## 7. Concrete Problem Examples
* **LeetCode 21 - Merge Two Sorted Lists**: Standard dummy node list merge.
* **LeetCode 160 - Intersection of Two Linked Lists**: 2-pointer swap alignment.
* **LeetCode 2 - Add Two Numbers**: Elementary math addition on digit lists.

---

## 8. Java Code Demonstration & Dry Run
Demonstration merging sorted lists, finding intersection, and adding number lists:

```java
public class MergeIntersectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Merge Two Sorted Lists (LeetCode 21) ===");
        MergeIntersectionMaster.ListNode l1 = new MergeIntersectionMaster.ListNode(1);
        l1.next = new MergeIntersectionMaster.ListNode(2);
        l1.next.next = new MergeIntersectionMaster.ListNode(4);

        MergeIntersectionMaster.ListNode l2 = new MergeIntersectionMaster.ListNode(1);
        l2.next = new MergeIntersectionMaster.ListNode(3);
        l2.next.next = new MergeIntersectionMaster.ListNode(4);

        MergeIntersectionMaster.ListNode merged = MergeIntersectionMaster.mergeTwoLists(l1, l2);
        System.out.print("Merged List: ");
        while (merged != null) {
            System.out.print(merged.val + " -> ");
            merged = merged.next;
        }
        System.out.println("null"); // Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> null

        System.out.println("\n=== 2. Intersection of Two Linked Lists (LeetCode 160) ===");
        MergeIntersectionMaster.ListNode common = new MergeIntersectionMaster.ListNode(8);
        common.next = new MergeIntersectionMaster.ListNode(4);

        MergeIntersectionMaster.ListNode headA = new MergeIntersectionMaster.ListNode(4);
        headA.next = new MergeIntersectionMaster.ListNode(1);
        headA.next.next = common;

        MergeIntersectionMaster.ListNode headB = new MergeIntersectionMaster.ListNode(5);
        headB.next = new MergeIntersectionMaster.ListNode(6);
        headB.next.next = new MergeIntersectionMaster.ListNode(1);
        headB.next.next.next = common;

        MergeIntersectionMaster.ListNode inter = MergeIntersectionMaster.getIntersectionNode(headA, headB);
        System.out.println("Intersection Node Value: " + (inter != null ? inter.val : "None")); // Output: 8
    }
}
```

---

## 9. Complexity Analysis

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Merge Two Lists (21)** | **$O(M + N)$ ⚡** | **$O(M + N)$ ⚡** | **$O(M + N)$ ⚡** | **$O(1)$ In-Place ⚡**|
| **Intersection Swap (160)**| **$O(M + N)$ ⚡** | **$O(M + N)$ ⚡** | **$O(M + N)$ ⚡** | **$O(1)$ In-Place ⚡**|
| **Add Two Numbers (2)** | **$O(\max(M,N))$ ⚡**| **$O(\max(M,N))$ ⚡**| **$O(\max(M,N))$ ⚡**| $O(\max(M,N))$ Output |

---

## 10. Edge Cases & Boundary Handling
* **One or Both Lists Empty (`headA == null || headB == null`)**: Returns `null` immediately.
* **No Intersection Exists**: Pointers `pA` and `pB` both become `null` at step $M + N$, terminating loop cleanly returning `null`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Hash Set for Intersection ($\text{Set}<\text{ListNode}>$)**:
  - Pushing all nodes of list $A$ into a set takes $O(M)$ extra heap space.
  - **Use 2-pointer swap for $O(1)$ constant memory**.
* **Swapping Pointers on `pA.next == null` Instead of `pA == null`**:
  - Writing `pA = (pA.next == null) ? headB : pA.next` skips the tail node!
  - **Always check `pA == null`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** 2-Pointer Swap Intersection Invariant:
> When $pA$ reaches `null` at the end of List $A$, redirect it to `headB`.
> When $pB$ reaches `null` at the end of List $B$, redirect it to `headA`.
> Both pointers walk total distance $M + N$. If lists intersect, they meet at the intersection node; if not, both reach `null` simultaneously!

> **Memory Trick:** **"Redirect pA to headB when pA is null! Both walk distance M+N and collide at intersection!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Swap Strategy | Hash Set Strategy |
| :--- | :--- | :--- |
| **Auxiliary Space** | **$O(1)$ Constant ⚡** | $O(M)$ Heap Memory |
| **Time Complexity** | **$O(M + N)$ Linear ⚡** | $O(M + N)$ Linear |
| **Code Length** | 6 Lines | 10 Lines |

---

## 14. How to Recognize This in Questions
* **"Merge two sorted linked lists into a single sorted list"** $\rightarrow$ LeetCode 21 (Dummy node merge).
* **"Find node at which two singly linked lists intersect"** $\rightarrow$ LeetCode 160 (2-pointer swap).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the 2-pointer swap algorithm work if two linked lists do not intersect?**  
  *A:* Pointer $A$ travels $M + N$ steps and pointer $B$ travels $N + M$ steps. Since $M + N = N + M$, both pointers reach `null` at the exact same step, causing `pA == pB == null` to terminate the loop cleanly.
* **Q: Why is dummy sentinel node used when merging two sorted lists?**  
  *A:* It holds the head reference of the merged list without needing special `if (mergedHead == null)` branching logic when selecting the first element.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MERGE & INTERSECTION ALGORITHMS                       |
+-----------------------------------------------------------------------+
| • Merge Sorted (21): Dummy node; compare l1.val & l2.val; append remaining|
| • Intersection Swap (160): pA = (pA == null) ? headB : pA.next        |
| • Both pointers walk M+N steps; collide at intersection node or null   |
| • Length Diff Strategy: Advance longer pointer by |M - N| steps first  |
| • Add Two Numbers (2): Maintain carry = sum / 10; digit = sum % 10    |
| • Space Invariant: Merge and Intersection run in O(1) Auxiliary Space ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Merge Two Sorted Lists (LeetCode 21) using dummy node.
- [ ] I can write 2-pointer swap Intersection (LeetCode 160) in 6 lines.
- [ ] I can derive why both pointers walk distance $M + N$ in LeetCode 160.
- [ ] I can write Add Two Numbers (LeetCode 2) with carry propagation.
- [ ] I know why `pA == null` must be checked rather than `pA.next == null`.
