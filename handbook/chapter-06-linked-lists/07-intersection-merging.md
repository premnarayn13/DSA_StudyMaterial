# 07. Linked List Intersection & Merging Algorithms

## 1. Introduction
Finding the intersection point of two linked lists (LeetCode 160) and merging sorted linked lists (LeetCode 21, LeetCode 23 "Merge K Sorted Lists") are fundamental operations in technical coding interviews. These problems evaluate two-pointer alignment tricks, min-heap priority queue processing, dummy head node techniques, and divide-and-conquer strategies in **$O(N)$ linear time and $O(1)$ auxiliary space**.

> **Important:** The 2-pointer approach for finding the intersection of List A and List B operates by redirecting pointer $pA$ to `headB` when it reaches the end of List A, and pointer $pB$ to `headA` when it reaches the end of List B. Both pointers will travel **equal total distance ($L_A + L_B$)** and meet at the exact **Intersection Node** in $O(L_A + L_B)$ time!

## 2. Core Concepts
* **Intersection of Two Linked Lists (LeetCode 160)**:
  * Pointer $pA$ traverses List A, then List B.
  * Pointer $pB$ traverses List B, then List A.
  * $pA$ and $pB$ will meet at the intersection node (or meet at `null` if no intersection exists) after at most $L_A + L_B$ steps.
* **Merge Two Sorted Lists (LeetCode 21)**: Using a `dummy` head node and two pointers (`p1`, `p2`) to construct a new sorted linked list by relinking existing nodes in $O(N_1 + N_2)$ time and $O(1)$ space.
* **Merge $K$ Sorted Lists (LeetCode 23)**:
  * **Min-Heap Approach**: Store the current head of each of the $K$ lists in a `PriorityQueue` ($O(N \log K)$ time, $O(K)$ space).
  * **Divide & Conquer Approach**: Pairwise merge lists using Divide and Conquer ($O(N \log K)$ time, $O(1)$ auxiliary space).

> **Memory Trick:** **"Pointer A = (pA == null) ? headB : pA.next; Pointer B = (pB == null) ? headA : pB.next"**.

## 3. Characteristics / Properties
* **Total Distance Equality Proof**:
  If List A has $a$ unique nodes, List B has $b$ unique nodes, and both share $c$ common nodes:
  * $pA$ path: $a + c + b$
  * $pB$ path: $b + c + a$
  * Both paths equal $a + b + c$ nodes, guaranteeing convergence at the intersection node!

```
Merging & Intersection Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Algorithm   | Time Complexity   | Space Complexity  | Best Technique    |
+-----------------------+-------------------+-------------------+-------------------+
| Intersection Node     | O(L_A + L_B)      | O(1) Constant ⚡  | 2-Pointer Switch  |
| Merge 2 Sorted Lists  | O(N_1 + N_2)      | O(1) Constant ⚡  | Dummy Head        |
| Merge K Sorted Lists  | O(N log K)        | O(K) Space        | Min-Heap (PriorityQueue)|
| Merge K Divide/Conquer| O(N log K)        | O(1) Auxiliary ⚡ | Pairwise Merge    |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing 2-Pointer Intersection Alignment (LeetCode 160):

```
List A: 4 -> 1 -\
                  -> 8 -> 4 -> 5 -> null (Shared c = 3 nodes)
List B: 5 -> 6 -> 1 -/

List A unique (a = 2), List B unique (b = 3), Shared (c = 3)

Pointer pA sequence: 4 -> 1 -> 8 -> 4 -> 5 -> null -> [Switches to headB] -> 5 -> 6 -> 1 -> 8!
Pointer pB sequence: 5 -> 6 -> 1 -> 8 -> 4 -> 5 -> null -> [Switches to headA] -> 4 -> 1 -> 8!

pA and pB meet at Node 8! (Intersection Node Found in 8 total steps!) ✅
```

## 5. Visual Diagram
2-Pointer List Switching Mechanics:

```
Path A:  [ List A Unique ] ----> [ Shared Intersection ] ----> [ List B Unique ] ----> [ Shared ]
Path B:  [ List B Unique ] ----> [ Shared Intersection ] ----> [ List A Unique ] ----> [ Shared ]

Both paths cover (Length A + Length B) nodes! Pointers intersect at the first shared node!
```

## 6. Operations / Algorithms
LeetCode 160 & LeetCode 21 Master Implementation:

```java
// 1. Get Intersection Node (LeetCode 160) O(L_A + L_B) Time, O(1) Space
public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
    if (headA == null || headB == null) return null;

    ListNode pA = headA;
    ListNode pB = headB;

    // Loop until pA and pB meet at intersection node OR both become null
    while (pA != pB) {
        pA = (pA == null) ? headB : pA.next;
        pB = (pB == null) ? headA : pB.next;
    }

    return pA; // Returns intersection node or null
}

// 2. Merge Two Sorted Lists (LeetCode 21) O(N_1 + N_2) Time, O(1) Space
public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
    ListNode dummy = new ListNode(-1);
    ListNode curr = dummy;

    while (list1 != null && list2 != null) {
        if (list1.val <= list2.val) {
            curr.next = list1;
            list1 = list1.next;
        } else {
            curr.next = list2;
            list2 = list2.next;
        }
        curr = curr.next;
    }

    // Attach remaining unlinked chain
    curr.next = (list1 != null) ? list1 : list2;

    return dummy.next;
}
```

> **Quick Syntax:**
```java
// 2-Pointer Switch Line
pA = (pA == null) ? headB : pA.next;
pB = (pB == null) ? headA : pB.next;
```

## 7. Examples
* **LeetCode 160 - Intersection of Two Linked Lists**: 2-Pointer switching algorithm in $O(1)$ space.
* **LeetCode 21 - Merge Two Sorted Lists**: Dummy head node two-pointer merging.
* **LeetCode 23 - Merge K Sorted Lists**: Min-Heap (`PriorityQueue`) or Divide and Conquer pairwise merging.

## 8. Java Code
Complete interview-ready Java suite implementing Intersection Node Discovery, Merge Two Sorted Lists, and Merge $K$ Sorted Lists (LeetCode 23) using `PriorityQueue`:

```java
import java.util.PriorityQueue;

public class IntersectionMergingMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Get Intersection Node (LeetCode 160) O(L_A + L_B) Time, O(1) Space
    public static ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        if (headA == null || headB == null) return null;

        ListNode pA = headA, pB = headB;
        while (pA != pB) {
            pA = (pA == null) ? headB : pA.next;
            pB = (pB == null) ? headA : pB.next;
        }
        return pA;
    }

    // 2. Merge Two Sorted Lists (LeetCode 21) O(N) Time, O(1) Space
    public static ListNode mergeTwoLists(ListNode l1, ListNode l2) {
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

    // 3. Merge K Sorted Lists (LeetCode 23) O(N log K) Time, O(K) Space
    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        // Min-Heap ordered by node value
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));

        // Add non-null head of each list to heap
        for (ListNode node : lists) {
            if (node != null) {
                pq.offer(node);
            }
        }

        ListNode dummy = new ListNode(-1);
        ListNode curr = dummy;

        while (!pq.isEmpty()) {
            ListNode smallest = pq.poll();
            curr.next = smallest;
            curr = curr.next;

            if (smallest.next != null) {
                pq.offer(smallest.next); // Push next node of processed list
            }
        }

        return dummy.next;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct List 1: 1 -> 4 -> 5
        ListNode l1 = new ListNode(1);
        l1.next = new ListNode(4);
        l1.next.next = new ListNode(5);

        // Construct List 2: 1 -> 3 -> 4
        ListNode l2 = new ListNode(1);
        l2.next = new ListNode(3);
        l2.next.next = new ListNode(4);

        ListNode merged = mergeTwoLists(l1, l2);
        System.out.print("Merged 2 Sorted Lists: ");
        ListNode curr = merged;
        while (curr != null) {
            System.out.print(curr.val + " -> ");
            curr = curr.next;
        }
        System.out.println("null"); // 1 -> 1 -> 3 -> 4 -> 4 -> 5 -> null
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Intersection Node Search** | **$O(L_A + L_B)$** | **$O(1)$ Constant** | Both pointers traverse equal distance |
| **Merge 2 Sorted Lists** | **$O(N_1 + N_2)$** | **$O(1)$ Constant** | Relinks existing nodes in-place |
| **Merge K Sorted Lists (Heap)**| **$O(N \log K)$** | $O(K)$ Space | PriorityQueue holds at most $K$ nodes |
| **Merge K (Divide & Conquer)**| **$O(N \log K)$** | **$O(1)$ Auxiliary** | Pairwise merges $K$ lists |

## 10. Edge Cases
* **No Intersection Exists**: $pA$ and $pB$ both reach `null` after $L_A + L_B$ steps and terminate loop with $pA == pB == null$, returning `null` cleanly.
* **Empty Lists in Merge K**: Null list elements inside `lists` array must be checked before pushing to PriorityQueue (`if (node != null)`).
* **Lists of Equal Length**: Pointers meet at intersection node during the first pass without switching heads.

## 11. Common Mistakes
* Writing `pA.next == null` instead of `pA == null` when switching heads (prevents pointers from switching lists properly!).
* Using `a.val - b.val` inside `PriorityQueue` comparator (causes integer underflow when `a.val` is negative and `b.val` is positive!). Always use **`Integer.compare(a.val, b.val)`**.
* Creating new `ListNode` objects inside Merge algorithms instead of relinking existing node references in-place.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `PriorityQueue` Comparator Rule:
> Never write: `new PriorityQueue<>((a, b) -> a.val - b.val);` (Underflow risk!).
> Always write: **`new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));`**

> **Memory Trick:** **"pA == null ? headB : pA.next (Switch heads on NULL, not null.next!)"**

## 13. Comparisons
| Feature | PriorityQueue Merge K Lists | Divide & Conquer Merge K Lists |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log K)$ | $O(N \log K)$ |
| **Auxiliary Space** | $O(K)$ Heap memory | **$O(1)$ Auxiliary (Iterative)** |
| **Code Length** | Short & Clean ($\approx 15$ lines) | Slightly longer |
| **Interview Recommendation** | **PREFERRED DEFAULT** | Advanced $O(1)$ space upgrade |

## 14. How to Recognize This in Questions
* **"Find node where two singly linked lists intersect in O(1) space"** $\rightarrow$ 2-Pointer Head Switch Algorithm (LeetCode 160).
* **"Merge K sorted linked lists into a single sorted list"** $\rightarrow$ Min-Heap `PriorityQueue` ($O(N \log K)$).

## 15. Frequently Asked Interview Questions
* **Q: Why does the 2-Pointer Intersection algorithm work when lists have different lengths?**  
  *A:* Because pointer $pA$ travels $L_A + L_B$ total nodes, and pointer $pB$ travels $L_B + L_A$ total nodes. Since $L_A + L_B = L_B + L_A$, both pointers reach the intersection node simultaneously at the end of their second list traversal!
* **Q: How does Divide & Conquer merge K sorted lists in $O(N \log K)$ time and $O(1)$ space?**  
  *A:* Pairwise merge adjacent list pairs in rounds: $K \to K/2 \to K/4 \dots \to 1$. There are $\log_2 K$ rounds, and each round processes all $N$ total nodes in linear time $\implies O(N \log K)$ time.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST INTERSECTION & MERGING                   |
+-----------------------------------------------------------------------+
| • Intersection Switch: pA = (pA == null) ? headB : pA.next;           |
|                       pB = (pB == null) ? headA : pB.next;            |
| • Merge 2 Lists: Dummy head node + 2 pointers; append remainder       |
| • Merge K Lists: PriorityQueue<ListNode>((a,b) -> Integer.compare(a.val, b.val))|
| • PriorityQueue Comparator: Always use Integer.compare(a.val, b.val)   |
| • Complexity: Intersection O(L_A + L_B) | Merge K O(N log K)          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement 2-pointer list intersection search in $O(1)$ space.
- [ ] I know why switching heads occurs on `pA == null`, NOT `pA.next == null`.
- [ ] I can merge 2 sorted linked lists in-place using Dummy Head.
- [ ] I can implement Merge K Sorted Lists using `PriorityQueue`.
- [ ] I know why `Integer.compare(a.val, b.val)` is required to prevent underflow.
