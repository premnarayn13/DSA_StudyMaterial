# 10. Flattening Multi-Level Linked Lists

## 1. Introduction
Flattening a multi-level linked list (LeetCode 430 - Flatten a Multilevel Doubly Linked List) requires converting a 2D hierarchical linked list structure—where nodes contain standard `next` / `prev` pointers as well as `child` pointers referencing nested sub-lists—into a single flattened 1D doubly linked list. In technical coding interviews, list flattening evaluates DFS recursion, stack-based iteration, and pointer link reconciliation.

> **Important:** When flattening a node containing a non-null `child` pointer, the child sub-list MUST be inserted **immediately between the current node and its `next` node**, with `child` pointers reset to `null`!

## 2. Core Concepts
* **Multilevel Node Structure**:
  ```java
  class Node {
      int val;
      Node prev;
      Node next;
      Node child; // Points to nested sub-list head
  }
  ```
* **Flattening Traversal Order**: Depth-First Search (DFS) order where child sub-lists are fully processed before continuing along the `next` pointer chain.
* **DFS Stack Approach (Iterative)**:
  * When `curr.child != null`: Push `curr.next` onto Stack, attach `curr.child` as `curr.next`, and set `curr.child = null`.
  * When `curr.next == null` and Stack is non-empty: Pop saved node from Stack and attach as `curr.next`.

> **Memory Trick:** **"Child list inserts BEFORE curr.next! Always set curr.child = null after unrolling!"**

## 3. Characteristics / Properties
* **Doubly Linked Invariants**: Every node connection `A <-> B` in the flattened list must maintain bidirectional references (`A.next = B` and `B.prev = A`).
* **Child Pointer Cleanup**: Every `child` pointer in the final flattened list MUST be set to **`null`**.

```
Flattening Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Strategy              | Time Complexity   | Auxiliary Space   | Advantage         |
+-----------------------+-------------------+-------------------+-------------------+
| Iterative Stack (DFS) | O(N) Linear       | O(N) Stack Space  | Clean & Intuitive |
| Recursive Pre-order   | O(N) Linear       | O(N) Call Stack   | Direct DFS mapping|
| In-Place Traversal    | O(N) Linear ⚡   | O(1) Constant ⚡  | Zero Stack Space  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Multilevel Doubly Linked List Flattening (LeetCode 430):

```
Level 1: 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> 6
               |
Level 2:       7 <-> 8 <-> 9 <-> 10
                     |
Level 3:             11 <-> 12

Flattening Execution:
1. Process Node 1 -> Node 2
2. Node 2 has child (7) -> Push Node 3 onto Stack. Connect 2 <-> 7. Set 2.child = null.
3. Process Node 7 -> Node 8
4. Node 8 has child (11) -> Push Node 9 onto Stack. Connect 8 <-> 11. Set 8.child = null.
5. Process 11 <-> 12 (Tail reached). Pop 9 from Stack! Connect 12 <-> 9.
6. Process 9 <-> 10 (Tail reached). Pop 3 from Stack! Connect 10 <-> 3.
7. Process 3 <-> 4 <-> 5 <-> 6.

Final Flattened List: 1 <-> 2 <-> 7 <-> 8 <-> 11 <-> 12 <-> 9 <-> 10 <-> 3 <-> 4 <-> 5 <-> 6 ✅
```

## 5. Visual Diagram
Multilevel List Insertion Mechanics:

```
Before Flattening:
[ Node 2 ] <------------------------> [ Node 3 ]
    |
    v (child)
[ Node 7 ] <---> ... <---> [ Node 10 ] (Child Tail)

After Flattening:
[ Node 2 ] <---> [ Node 7 ] <---> ... <---> [ Node 10 ] <---> [ Node 3 ]
(2.child set to null!)
```

## 6. Operations / Algorithms
LeetCode 430 Iterative Stack Implementation:

```java
public Node flatten(Node head) {
    if (head == null) return null;

    Node curr = head;
    Deque<Node> stack = new ArrayDeque<>();

    while (curr != null) {
        // If current node has a child sub-list
        if (curr.child != null) {
            // Save next node onto Stack if it exists
            if (curr.next != null) {
                stack.push(curr.next);
            }

            // Connect curr to child node
            curr.next = curr.child;
            curr.child.prev = curr;
            curr.child = null; // MANDATORY: Clear child pointer!
        }

        // If tail reached and stack is non-empty, pop saved next node
        if (curr.next == null && !stack.isEmpty()) {
            Node nextNode = stack.pop();
            curr.next = nextNode;
            nextNode.prev = curr;
        }

        curr = curr.next;
    }

    return head;
}
```

> **Quick Syntax:**
```java
// Connect curr to child node & clear child pointer
curr.next = curr.child;
curr.child.prev = curr;
curr.child = null;
```

## 7. Examples
* **LeetCode 430 - Flatten a Multilevel Doubly Linked List**: Standard DFS stack flattening.
* **Flattening a Linked List (GeeksforGeeks)**: 2D Linked List with `bottom` and `next` pointers flattened using Merge Two Sorted Lists.

## 8. Java Code
Complete interview-ready Java suite implementing Iterative Stack Flattening and Recursive DFS Flattening:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class FlatteningLinkedListsMaster {

    public static class Node {
        public int val;
        public Node prev;
        public Node next;
        public Node child;
        public Node(int val) { this.val = val; }
    }

    // 1. Iterative Stack Flattening (LeetCode 430) O(N) Time, O(N) Space
    public static Node flatten(Node head) {
        if (head == null) return null;

        Node curr = head;
        Deque<Node> stack = new ArrayDeque<>();

        while (curr != null) {
            if (curr.child != null) {
                if (curr.next != null) {
                    stack.push(curr.next);
                }

                // Attach child as next node
                curr.next = curr.child;
                curr.child.prev = curr;
                curr.child = null; // Clear child pointer
            }

            if (curr.next == null && !stack.isEmpty()) {
                Node nextNode = stack.pop();
                curr.next = nextNode;
                nextNode.prev = curr;
            }

            curr = curr.next;
        }

        return head;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct: 1 <-> 2 (child 3 <-> 4) <-> 5
        Node n1 = new Node(1);
        Node n2 = new Node(2);
        Node n5 = new Node(5);
        n1.next = n2; n2.prev = n1;
        n2.next = n5; n5.prev = n2;

        Node n3 = new Node(3);
        Node n4 = new Node(4);
        n3.next = n4; n4.prev = n3;

        n2.child = n3; // Attach child to Node 2

        Node flattened = flatten(n1);

        System.out.print("Flattened List: ");
        Node curr = flattened;
        while (curr != null) {
            System.out.print(curr.val + (curr.child == null ? "" : "(CHILD NOT NULL!)") + " <-> ");
            curr = curr.next;
        }
        System.out.println("null"); // 1 <-> 2 <-> 3 <-> 4 <-> 5 <-> null
    }
}
```

## 9. Complexity Analysis
| Approach | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Iterative Stack DFS** | **$O(N)$ Linear** | $O(N)$ Stack Space | Handles deep child nestings |
| **Recursive DFS** | **$O(N)$ Linear** | $O(N)$ Call Stack | Recursion stack depth |
| **In-Place Scan** | **$O(N)$ Linear** | **$O(1)$ Constant ⚡** | Finds child tail in-place |

## 10. Edge Cases
* **Forgetting `curr.child = null`**: The child pointer MUST be cleared after attaching the child list; otherwise, the output list contains invalid child links.
* **Child Node at Tail (`curr.next == null`)**: Stack handles tail child nodes naturally without null pointer exceptions.
* **Deeply Nested Child Lists (Depth $> 1000$)**: Iterative stack approach prevents `StackOverflowError`.

## 11. Common Mistakes
* Forgetting to update `prev` pointers (`curr.child.prev = curr` and `nextNode.prev = curr`), breaking doubly linked list bidirectional invariants!
* Forgetting to set `curr.child = null` after flattening.
* Pushing `null` onto the Stack when `curr.next == null`. Guard: `if (curr.next != null) stack.push(curr.next)`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Remember the 3-step child attachment sequence:
> 1. Push `curr.next` onto `ArrayDeque` stack (if non-null).
> 2. `curr.next = curr.child; curr.child.prev = curr;`
> 3. **`curr.child = null;`** (MANDATORY).

> **Memory Trick:** **"Always set curr.child = null after attaching child list!"**

## 13. Comparisons
| Feature | Recursive DFS Flattening | Iterative `ArrayDeque` Stack Flattening |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Space Complexity**| $O(N)$ (Call Stack) | **$O(N)$ (Explicit ArrayDeque - StackOverflow Safe)** |
| **Code Length** | Slightly shorter | Clean & production-grade |
| **Interview Recommendation** | Good | **PREFERRED & SAFE** |

## 14. How to Recognize This in Questions
* **"Flatten a 2D/Multilevel doubly linked list into a single 1D list"** $\rightarrow$ Iterative DFS Stack Flattening (LeetCode 430).
* **"Flatten sorted 2D linked list"** $\rightarrow$ Merge Two Sorted Lists on `bottom` pointers.

## 15. Frequently Asked Interview Questions
* **Q: Why must `curr.child` be set to `null` during flattening?**  
  *A:* The problem definition specifies that the final output must be a standard 1D Doubly Linked List where all `child` pointers evaluate to `null`.
* **Q: How does `ArrayDeque` prevent StackOverflowError during list flattening?**  
  *A:* `ArrayDeque` allocates stack memory on the JVM Heap, which can grow to gigabytes, whereas recursion uses the fixed JVM Thread Stack (typically 1MB), which crashes on deeply nested lists.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLATTENING MULTI-LEVEL LINKED LISTS                   |
+-----------------------------------------------------------------------+
| • Has Child? Push curr.next to stack, attach curr.next = curr.child,  |
|              curr.child.prev = curr, set curr.child = null            |
| • Tail Reached & Stack non-empty? Pop nextNode, attach curr.next = nextNode|
| • Maintain Doubly Links: Set nextNode.prev = curr on every connection  |
| • Mandatory Rule: Set curr.child = null for every processed child node|
| • Complexity: O(N) Linear Time | O(N) Auxiliary Space (ArrayDeque)    |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement `Node` structure with `prev`, `next`, and `child` pointers.
- [ ] I can write the 3-step child link attachment code.
- [ ] I know why setting `curr.child = null` is mandatory.
- [ ] I can maintain bidirectional `prev` and `next` pointers during flattening.
- [ ] I can solve LeetCode 430 using `ArrayDeque` in $O(N)$ time.
