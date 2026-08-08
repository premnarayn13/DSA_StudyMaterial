# 15. Linked List Problem Recognition Patterns

## 1. Introduction
Solving linked list problems in technical coding interviews requires rapid pattern recognition. Rather than getting bogged down in complex pointer reassignment, top candidates recognize structural problem signals—such as finding the middle, detecting cycles, reversing subranges, or partitioning around a pivot—and instantly select the optimal algorithmic pattern: Dummy Head Sentinel, Fast & Slow Pointers, Iterative 3-Pointer Reversal, 2-Pointer List Switch, or Min-Heap PriorityQueue.

> **Important:** In technical interviews, identifying whether a linked list problem can be solved in **$O(1)$ auxiliary space** via pointer manipulation dictates whether your solution achieves maximum performance marks.

## 2. Core Concepts
* **Pattern 1: Dummy Head Sentinel (`dummy.next = head`)**: Triggered whenever operations modify the head node (e.g., removing head, insertion at head, merging, partitioning). Unifies head edge cases with internal node logic.
* **Pattern 2: Fast & Slow Pointers (`slow = slow.next, fast = fast.next.next`)**: Triggered by "Find middle node", "Remove N-th from end", "Palindrome check", or "Cycle detection".
* **Pattern 3: Iterative 3-Pointer Reversal (`prev`, `curr`, `nextTemp`)**: Triggered by "Reverse list in-place", "Reverse subrange [M, N]", or "Reverse nodes in K-group".
* **Pattern 4: 2-Pointer List Switching**: Triggered by "Find intersection node of List A and List B in $O(1)$ space".
* **Pattern 5: Dual Dummy Head Sub-Chains**: Triggered by "Partition list around pivot $X$" or "Separate odd and even nodes".
* **Pattern 6: Interleaved Weaving**: Triggered by "Deep copy linked list with random pointers in $O(1)$ space".
* **Pattern 7: Min-Heap (`PriorityQueue`)**: Triggered by "Merge K sorted linked lists in $O(N \log K)$ time".

> **Memory Trick:** **"Modifying Head? Use Dummy Head! Middle or Cycle? Fast & Slow Pointers! Reverse? 3 Pointers (prev, curr, nextTemp)!"**

## 3. Characteristics / Properties
* **Pattern Recognition Decision Matrix**:

```
Problem Phrasing / Signal                      Optimal Linked List Pattern  Target Complexity
---------------------------------------------------------------------------------------------
Delete head node / Merge 2 sorted lists        Dummy Head Sentinel          O(N) Time, O(1) Space
Find middle node / 2nd middle                  Fast & Slow Pointers         O(N) Time, O(1) Space
Remove N-th node from end of list              Fast & Slow Gap + Dummy Head O(N) Time, O(1) Space
Detect cycle / Find cycle entry node           Floyd's Tortoise & Hare      O(N) Time, O(1) Space
Reverse list / Reverse subrange [M, N]         Iterative 3-Pointer Reversal O(N) Time, O(1) Space
Find intersection node of 2 lists              2-Pointer List Switch        O(L_A+L_B) Time, O(1) Space
Partition list around pivot X preserving order  Dual Dummy Heads             O(N) Time, O(1) Space
Clone list with random pointers in O(1) space  Interleaved Weaving          O(N) Time, O(1) Space
Merge K sorted lists                           PriorityQueue (Min-Heap)     O(N log K) Time, O(K) Space
LRU Cache with O(1) get and put                HashMap + Doubly Linked List O(1) Time, O(N) Space
```

## 4. Internal Working
Decision Tree for Selecting Linked List Patterns:

```
                     [ Linked List Problem ]
                                |
             +------------------+------------------+
             |                                     |
    [ Pointer Manipulation ]               [ Multi-List Operations ]
             |                                     |
    +--------+--------+                   +--------+--------+
    |                 |                   |                 |
[Middle/Cycle]  [Reversal]            [Intersection]     [Merge K]
    |                 |                   |                 |
(Fast & Slow)  (3-Pointer Prev)    (2-Pointer Switch)  (PriorityQueue)
```

## 5. Visual Diagram
Summary of All Core Pointer Patterns:

```
[ DUMMY HEAD SENTINEL ]
[ Dummy (-1) ] ---> [ Head Node ] ---> [ Node 2 ] ---> null

[ FAST & SLOW POINTERS ]
slow = slow.next (1 step)  |  fast = fast.next.next (2 steps)

[ ITERATIVE 3-POINTER REVERSAL ]
nextTemp = curr.next; curr.next = prev; prev = curr; curr = nextTemp;

[ 2-POINTER LIST SWITCH ]
pA = (pA == null) ? headB : pA.next;
pB = (pB == null) ? headA : pB.next;
```

## 6. Operations / Algorithms
Master Pattern Recognition Code Snippet (Selecting Patterns at a Glance):

```java
// Pattern 1: Fast & Slow Middle Finding
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}

// Pattern 2: Iterative 3-Pointer Reversal
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode nextTemp = curr.next;
    curr.next = prev;
    prev = curr;
    curr = nextTemp;
}

// Pattern 3: 2-Pointer List Switch Intersection
ListNode pA = headA, pB = headB;
while (pA != pB) {
    pA = (pA == null) ? headB : pA.next;
    pB = (pB == null) ? headA : pB.next;
}
```

> **Quick Syntax:**
```java
// Dummy Head Creation Pattern
ListNode dummy = new ListNode(-1);
dummy.next = head;
```

## 7. Examples
* **LeetCode 141 / 142 - Cycle Detection**: Floyd's Tortoise and Hare algorithm.
* **LeetCode 146 - LRU Cache**: HashMap + Doubly Linked List.
* **LeetCode 23 - Merge K Sorted Lists**: Min-Heap (`PriorityQueue`).

## 8. Java Code
Complete interview-ready Java suite demonstrating pattern selection across major linked list interview problems:

```java
public class LinkedListPatternRecognitionMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // Pattern 1: Remove N-th Node From End (Fast/Slow Gap + Dummy Head)
    public static ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode fast = dummy, slow = dummy;

        for (int i = 0; i <= n; i++) {
            fast = fast.next;
        }

        while (fast != null) {
            slow = slow.next;
            fast = fast.next;
        }

        slow.next = slow.next.next;
        return dummy.next;
    }

    // Pattern 2: Reverse Subrange [left, right] (Dummy Head + 3-Pointer Shift)
    public static ListNode reverseBetween(ListNode head, int left, int right) {
        if (head == null || left == right) return head;

        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode prev = dummy;

        for (int i = 0; i < left - 1; i++) {
            prev = prev.next;
        }

        ListNode curr = prev.next;
        for (int i = 0; i < right - left; i++) {
            ListNode nextNode = curr.next;
            curr.next = nextNode.next;
            nextNode.next = prev.next;
            prev.next = nextNode;
        }

        return dummy.next;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct List: 1 -> 2 -> 3 -> 4 -> 5 -> null
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);
        head.next.next.next.next = new ListNode(5);

        // Remove 2nd node from end (node 4)
        head = removeNthFromEnd(head, 2);

        ListNode curr = head;
        System.out.print("After Removing 2nd from end: ");
        while (curr != null) {
            System.out.print(curr.val + " -> ");
            curr = curr.next;
        }
        System.out.println("null"); // Output: 1 -> 2 -> 3 -> 5 -> null
    }
}
```

## 9. Complexity Analysis
| Pattern / Technique | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Dummy Head Sentinel** | **$O(N)$ Linear** | **$O(1)$ Constant** | Eliminates head node `null` checks |
| **Fast & Slow Pointers** | **$O(N)$ Linear** | **$O(1)$ Constant** | Single pass middle & cycle detection |
| **Iterative 3-Pointer Reversal**| **$O(N)$ Linear** | **$O(1)$ Constant** | In-place list reversal |
| **Interleaved Weaving** | **$O(N)$ Linear** | **$O(1)$ Constant** | Clones random pointers in $O(1)$ space |

## 10. Edge Cases
* **Modifying Head Node**: Using `dummy.next = head` prevents edge-case null pointer crashes.
* **Empty List or Single Node**: Base case `head == null || head.next == null` returns `head` immediately.
* **Cycle in List**: Fast & Slow pointers handle cycles without infinite loops.

## 11. Common Mistakes
* Omitting Dummy Head Node when operations modify the head of the list.
* Writing `fast.next != null` without checking `fast != null` in Fast & Slow pointer loops.
* Forgetting `large.next = null` in Partition List (creates cyclic reference loops).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Master Pattern Quick Cheat:
> 1. **Modifying Head?** $\implies$ Dummy Head (`dummy.next = head`).
> 2. **Middle / Cycle / Palindrome?** $\implies$ Fast & Slow Pointers (`slow.next`, `fast.next.next`).
> 3. **Reverse / Reorder?** $\implies$ 3-Pointer Iterative (`prev`, `curr`, `nextTemp`).
> 4. **Intersection of 2 Lists?** $\implies$ 2-Pointer Head Switch (`pA == null ? headB : pA.next`).
> 5. **Merge K Lists?** $\implies$ PriorityQueue (`(a, b) -> Integer.compare(a.val, b.val)`).

> **Memory Trick:** **"Dummy Head for Head edits; Fast/Slow for Middle & Cycles; 3 Pointers for Reversals!"**

## 13. Comparisons
| Problem Signal | Sub-Optimal Approach | Optimal Pattern |
| :--- | :--- | :--- |
| **Find Middle Node** | Count length $N$ then loop $N/2$ | **Fast & Slow Pointers (1 Pass)** |
| **Intersection of 2 Lists** | HashSet of List A nodes ($O(N)$ space) | **2-Pointer Head Switch ($O(1)$ space)** |
| **Clone List with Random** | HashMap of nodes ($O(N)$ space) | **Interleaved Weaving ($O(1)$ space)** |

## 14. How to Recognize This in Questions
* **"Modify linked list in-place with O(1) space"** $\rightarrow$ Fast/Slow pointers or 3-pointer reversal.
* **"Find node where 2 lists intersect"** $\rightarrow$ 2-Pointer Head Switch ($O(1)$ space).

## 15. Frequently Asked Interview Questions
* **Q: Why is $O(1)$ auxiliary space so strongly emphasized in Linked List interview questions?**  
  *A:* Linked lists are inherently dynamic pointer structures. Candidates who use external data structures (like arrays or HashMaps) miss the primary architectural purpose of linked lists: modifying node relationships directly in memory without extra allocations.
* **Q: When should you use a Dummy Head Node?**  
  *A:* Whenever an algorithm might delete, insert, or swap the head node of a linked list. `dummy.next = head` provides a static anchor node preceding the head, unifying all node modifications into a single code path.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINKED LIST PROBLEM RECOGNITION PATTERNS              |
+-----------------------------------------------------------------------+
| • Head Edits / Merging: Dummy Head Node (ListNode dummy = new ListNode(-1))|
| • Middle / Cycle: Fast & Slow Pointers (while fast!=null && fast.next!=null)|
| • Reversal: Iterative 3-Pointer (nextTemp=curr.next; curr.next=prev; ...)|
| • Intersection: pA = (pA == null) ? headB : pA.next                    |
| • Merge K Lists: PriorityQueue<ListNode>((a,b)->Integer.compare(a.val,b.val))|
| • Target Space Complexity: O(1) Auxiliary Space for all pointer ops   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can select the optimal pattern for any linked list problem within 60 seconds.
- [ ] I know when Dummy Head Node (`dummy.next = head`) is required.
- [ ] I can implement Fast & Slow pointers for middle finding and cycle detection.
- [ ] I can implement iterative 3-pointer reversal from memory in 1 minute.
- [ ] I can implement 2-pointer head switching for list intersection in $O(1)$ space.
