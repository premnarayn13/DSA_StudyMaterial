# 10. Deep Copy & Flattening Algorithms: Random Pointers & Multilevel Lists

## 1. Introduction
Cloning complex linked lists with arbitrary pointers—such as **Copy List with Random Pointer (LeetCode 138)**—and flattening hierarchical node structures—such as **Flatten a Multilevel Doubly Linked List (LeetCode 430)**—represent advanced linked list manipulation challenges. These problems test an engineer's ability to maintain graph node mapping identity, manage nested pointer references (`child`, `random`, `prev`, `next`), and achieve **$O(1)$ constant auxiliary space** without relying on extra hash tables.

> **Important:** While cloning a linked list with random pointers can be solved using an auxiliary `Map<Node, Node>` in $O(N)$ space, the optimal **Interleaving Strategy (3-Pass Algorithm)** achieves deep cloning in **$O(N)$ linear time with $O(1)$ constant auxiliary space** by weaving duplicate nodes directly alongside original nodes!

```
Copy List Strategy Spectrum:
+-----------------------------------------------------------------------------------+
| HashMap Strategy   : Map<Node, Node> cloneMap -> O(N) Time, O(N) Space (High Mem) |
| Interleaving Method: Weave A -> A' -> B -> B'  -> O(N) Time, O(1) Space ⚡ (Optimal) |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Copy List with Random Pointer (LeetCode 138 - Interleaving $O(1)$ Space Strategy)
Given a linked list where each node contains an extra `random` pointer pointing to any node in the list or `null`:

#### 3-Pass Interleaving Protocol:
1. **Pass 1 (Interweave Nodes)**: For every original node `curr`, create a duplicate node `cloned = new Node(curr.val)` and insert it immediately after `curr`:
   - `cloned.next = curr.next; curr.next = cloned;`
   - Original: `A -> B -> C` $\implies$ Interleaved: `A -> A' -> B -> B' -> C -> C'`.
2. **Pass 2 (Assign Random Pointers)**: For each original node `curr`:
   - If `curr.random != null`: `curr.next.random = curr.random.next` (Since `curr.next` is `curr'`, and `curr.random.next` is `curr.random'`!).
3. **Pass 3 (Unweave & Restore Lists)**: Separate interleaved list into original list and cloned list:
   - `original.next = cloned.next; cloned.next = (cloned.next != null) ? cloned.next.next : null;`

```
Interleaving 3-Pass Breakdown:
Pass 1 (Weave)   : [ A ] -> [ A' ] -> [ B ] -> [ B' ] -> null
Pass 2 (Random)  : A'.random = A.random.next (Points directly to target copy!)
Pass 3 (Unweave) : Original: A -> B, Cloned: A' -> B'  ✅ (O(N) Time, O(1) Space!)
```

### 2.2 Flatten a Multilevel Doubly Linked List (LeetCode 430)
Given a doubly linked list where nodes can have a `child` pointer to a child doubly linked list:
1. Traverse list with `curr`.
2. If `curr.child != null`:
   - Save `nextTemp = curr.next`.
   - Recursively/Iteratively flatten child list: `childHead = curr.child`.
   - Re-wire `curr.next = childHead; childHead.prev = curr; curr.child = null;`.
   - Find tail of child list `childTail`.
   - Re-wire `if (nextTemp != null) { childTail.next = nextTemp; nextTemp.prev = childTail; }`.
3. Advance `curr = curr.next`.

> **Memory Trick:** **"Copy Random List: Pass 1 Weave (A->A'), Pass 2 Wire random (A'.random = A.random.next), Pass 3 Unweave! O(1) Space!"**

---

## 3. Characteristics & HashMap Alternative

### 3.1 HashMap Deep Copy Approach ($O(N)$ Time, $O(N)$ Space)
1. Pass 1: Traverse original list, create new node copy for each original node, store in `Map<Node, Node> map`.
2. Pass 2: Traverse original list again, set `map.get(curr).next = map.get(curr.next)` and `map.get(curr).random = map.get(curr.random)`.
3. Return `map.get(head)`.
* **Trade-Off**: Extremely clean code, but consumes $O(N)$ extra heap memory for hash table buckets.

---

## 4. Internal Working Mechanics
Tracing Interleaving Strategy (LeetCode 138) on `A(1) -> B(2)`, where `A.random = B`, `B.random = B`:

```
Pass 1 (Interweave):
A -> A' -> B -> B' -> null
A.val = 1, A'.val = 1, B.val = 2, B'.val = 2

Pass 2 (Assign Random):
- A.random is B -> A'.random = B.next = B'
- B.random is B -> B'.random = B.next = B'

Pass 3 (Unweave):
- A.next = B
- A'.next = B'
- B.next = null
- B'.next = null

Cloned List: A'(1) -> B'(2), A'.random = B', B'.random = B' ✅ (Matches Original!)
```

---

## 5. Visual Diagram
Copy List Interleaving & Unweaving Topology:

```
Pass 1 (Interleaved Structure):
+-------+     +--------+     +-------+     +--------+
| A (1) | --> | A' (1) | --> | B (2) | --> | B' (2) | --> null
+-------+     +--------+     +-------+     +--------+
    |             ^              |             ^
    +-- random ---+--------------+-- random ---+ (A.random = B -> A'.random = B')

Pass 3 (Separated Independent Lists):
Original List : [ A ] -------> [ B ] -------> null
Cloned List   : [ A' ] ------> [ B' ] ------> null
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Deep Copy with Random Pointers (LeetCode 138 - Both Interleaving $O(1)$ space and HashMap methods) and Multilevel Doubly List Flattening (LeetCode 430):

```java
import java.util.*;

public class CloneFlattenMaster {

    public static class Node {
        public int val;
        public Node next;
        public Node random;
        public Node prev;
        public Node child;

        public Node(int val) {
            this.val = val;
            this.next = null;
            this.random = null;
            this.prev = null;
            this.child = null;
        }
    }

    // 1. Copy List with Random Pointer Interleaving Strategy (LeetCode 138) O(N) Time, O(1) Auxiliary Space
    public static Node copyRandomListInterleaving(Node head) {
        if (head == null) return null;

        // Pass 1: Interweave cloned nodes alongside original nodes (A -> A' -> B -> B')
        Node curr = head;
        while (curr != null) {
            Node clone = new Node(curr.val);
            clone.next = curr.next;
            curr.next = clone;
            curr = clone.next;
        }

        // Pass 2: Assign random pointers to cloned nodes
        curr = head;
        while (curr != null) {
            if (curr.random != null) {
                curr.next.random = curr.random.next; // A'.random = A.random.next
            }
            curr = curr.next.next;
        }

        // Pass 3: Unweave & restore original and cloned lists
        curr = head;
        Node dummy = new Node(0);
        Node cloneTail = dummy;

        while (curr != null) {
            Node nextOriginal = curr.next.next;
            Node clone = curr.next;

            cloneTail.next = clone;
            cloneTail = clone;

            curr.next = nextOriginal; // Restore original list
            curr = nextOriginal;
        }

        return dummy.next;
    }

    // 2. Copy List with Random Pointer HashMap Strategy (LeetCode 138) O(N) Time, O(N) Space
    public static Node copyRandomListHashMap(Node head) {
        if (head == null) return null;

        Map<Node, Node> cloneMap = new HashMap<>();

        // Pass 1: Create clone nodes
        Node curr = head;
        while (curr != null) {
            cloneMap.put(curr, new Node(curr.val));
            curr = curr.next;
        }

        // Pass 2: Connect next and random pointers
        curr = head;
        while (curr != null) {
            cloneMap.get(curr).next = cloneMap.get(curr.next);
            cloneMap.get(curr).random = cloneMap.get(curr.random);
            curr = curr.next;
        }

        return cloneMap.get(head);
    }

    // 3. Flatten Multilevel Doubly Linked List (LeetCode 430) O(N) Time, O(1) Auxiliary Space
    public static Node flatten(Node head) {
        if (head == null) return head;

        Node curr = head;
        while (curr != null) {
            if (curr.child != null) {
                Node nextTemp = curr.next;
                Node childHead = curr.child;

                // Connect curr to child head
                curr.next = childHead;
                childHead.prev = curr;
                curr.child = null; // Clear child pointer!

                // Find tail of child list
                Node childTail = childHead;
                while (childTail.next != null) {
                    childTail = childTail.next;
                }

                // Connect child tail to saved nextTemp
                if (nextTemp != null) {
                    childTail.next = nextTemp;
                    nextTemp.prev = childTail;
                }
            }
            curr = curr.next;
        }

        return head;
    }
}
```

> **Quick Syntax:**
```java
// Interleaving Random Pointer Assignment Syntax
if (curr.random != null) {
    curr.next.random = curr.random.next;
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 138 - Copy List with Random Pointer**: 3-pass interleaving deep copy.
* **LeetCode 430 - Flatten a Multilevel Doubly Linked List**: Child list splice re-linking.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Interleaving Deep Copy and Multilevel List Flattening:

```java
public class CloneFlattenDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Copy List with Random Pointer (LeetCode 138) ===");
        CloneFlattenMaster.Node n1 = new CloneFlattenMaster.Node(7);
        CloneFlattenMaster.Node n2 = new CloneFlattenMaster.Node(13);
        CloneFlattenMaster.Node n3 = new CloneFlattenMaster.Node(11);

        n1.next = n2; n2.next = n3;
        n1.random = null; n2.random = n1; n3.random = n2;

        CloneFlattenMaster.Node cloneHead = CloneFlattenMaster.copyRandomListInterleaving(n1);
        System.out.println("Cloned Head Val: " + cloneHead.val); // Output: 7
        System.out.println("Cloned Node 2 Random Val (Expected 7): " + cloneHead.next.random.val); // Output: 7

        System.out.println("\n=== 2. Flatten Multilevel Doubly List (LeetCode 430) ===");
        CloneFlattenMaster.Node p1 = new CloneFlattenMaster.Node(1);
        CloneFlattenMaster.Node p2 = new CloneFlattenMaster.Node(2);
        CloneFlattenMaster.Node c1 = new CloneFlattenMaster.Node(3);

        p1.next = p2; p2.prev = p1;
        p1.child = c1; // Child on Node 1

        CloneFlattenMaster.Node flattened = CloneFlattenMaster.flatten(p1);
        System.out.print("Flattened Sequence: ");
        while (flattened != null) {
            System.out.print(flattened.val + " -> ");
            flattened = flattened.next;
        }
        System.out.println("null"); // Output: 1 -> 3 -> 2 -> null
    }
}
```

---

## 9. Complexity Analysis

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Interleaving Deep Copy (138)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**|
| **HashMap Deep Copy (138)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| $O(N)$ Map Memory |
| **Flatten Multilevel List (430)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Null Random Pointers (`curr.random == null`)**: Guard `if (curr.random != null)` before dereferencing `curr.random.next`.
* **Nodes Without Child Pointers (`curr.child == null`)**: Traversal advances cleanly without modification.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Clear `curr.child = null` in Multilevel Flattening**:
  - Leaving `curr.child` populated creates ambiguous tree-graph pointers.
  - **Always execute `curr.child = null` after connecting child list to `curr.next`**.
* **Dereferencing `curr.random.next` When `curr.random` is Null**: Causes `NullPointerException`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Interleaving Deep Copy Trick:
> In Pass 2 of the interleaving algorithm, why is `curr.next.random = curr.random.next` valid?
> Because `curr.next` is the CLONED node $A'$, and `curr.random` is the target original node $B$.
> Since $B$'s cloned copy $B'$ is placed immediately after $B$ (`B.next`), **`curr.random.next` points directly to $B'$**!

> **Memory Trick:** **"A'.random = A.random.next works because B' is placed right after B!"**

---

## 13. System & Implementation Comparisons

| Feature | Interleaving Strategy | HashMap Strategy |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Hash Table |
| **Pass Count** | 3 Linear Passes | 2 Linear Passes |
| **Graph Node Isolation**| Excellent (Unweaves clean) | Excellent |

---

## 14. How to Recognize This in Questions
* **"Deep copy linked list with random pointers in O(1) extra space"** $\rightarrow$ LeetCode 138 (3-pass interleaving).
* **"Flatten multilevel doubly linked list so child nodes appear in main list"** $\rightarrow$ LeetCode 430.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the interleaving algorithm achieve $O(1)$ space while the HashMap approach requires $O(N)$ space?**  
  *A:* The HashMap approach stores original-to-clone node mappings in an external hash table. The interleaving algorithm uses the original linked list itself as the temporary mapping structure by inserting each clone node immediately after its parent.
* **Q: Why MUST `curr.child = null` be executed when flattening a multilevel list in LeetCode 430?**  
  *A:* LeetCode 430 specifies that the output must be a standard 1D Doubly Linked List. Leaving child pointers populated creates invalid hybrid list-tree structures.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CLONE & FLATTEN LINKED LISTS                          |
+-----------------------------------------------------------------------+
| • Interleaving Copy (138): Pass 1 Weave (A->A'), Pass 2 Random        |
|   (A'.random = A.random.next), Pass 3 Unweave!                        |
| • Space Advantage: Achieves O(N) Time & O(1) Auxiliary Space ⚡        |
| • HashMap Strategy: Map<Node, Node>; map.get(curr).next = map.get(curr.next)|
| • Flatten Multilevel List (430): Splice child list between curr & next|
| • Child Cleanup Rule: ALWAYS set curr.child = null after splicing!    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 3-pass Interleaving Deep Copy (LeetCode 138) in $O(1)$ space.
- [ ] I know why `curr.next.random = curr.random.next` works.
- [ ] I can write HashMap Deep Copy for random pointer lists.
- [ ] I can solve Flatten Multilevel Doubly List (LeetCode 430).
- [ ] I know why `curr.child = null` is mandatory in LeetCode 430.
