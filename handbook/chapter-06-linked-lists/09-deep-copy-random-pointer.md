# 09. Deep Copying Linked Lists with Random Pointers

## 1. Introduction
Cloning a linked list with random pointers (LeetCode 138 - Copy List with Random Pointer) requires constructing a deep copy of a list where each node contains both a standard `next` pointer and an arbitrary `random` pointer pointing to any node in the list or `null`. In technical coding interviews, solving this problem in **$O(N)$ time and $O(1)$ auxiliary space** using the **Interleaved Node Weaving** technique demonstrates master-level pointer manipulation.

> **Important:** While a HashMap approach solves Deep Copy in $O(N)$ time and $O(N)$ auxiliary space, the **Interleaved Weaving Trick** achieves $O(N)$ time and **$O(1)$ auxiliary space** by temporarily weaving cloned nodes directly next to their original nodes (`curr -> copy -> curr.next`)!

## 2. Core Concepts
* **Node Structure**:
  ```java
  class Node {
      int val;
      Node next;
      Node random;
      Node(int val) { this.val = val; }
  }
  ```
* **HashMap Approach ($O(N)$ Space)**: Storing a mapping of `map.put(oldNode, newNode)` in Pass 1, then connecting `newNode.next = map.get(oldNode.next)` and `newNode.random = map.get(oldNode.random)` in Pass 2.
* **Interleaved Weaving Approach ($O(1)$ Space)**:
  * **Step 1 (Weave)**: Create copy node `A'` and insert it immediately after original node `A`: `A -> A' -> B -> B' -> C -> C'`.
  * **Step 2 (Assign Random)**: Set `copy.random = (curr.random != null) ? curr.random.next : null`.
  * **Step 3 (Unweave)**: Separate the interleaved list back into original list and cloned list!

> **Memory Trick:** **"1. Weave copy nodes (A -> A' -> B) | 2. Assign copy.random = orig.random.next | 3. Unweave lists!"**

## 3. Characteristics / Properties
* **Deep Copy Guarantee**: New node objects share ZERO memory references with original node objects on the JVM Heap.
* **Interleaved Random Reference Formula**: If original node $A$ has `random` pointer to node $X$, then cloned node $A'$ (`A.next`) has its `random` pointer pointing to $X'$ (`A.random.next`)!

```
Deep Copy Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Approach              | Time Complexity   | Auxiliary Space   | Code Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| HashMap Node Mapping  | O(N) Linear       | O(N) Extra Map    | Easy & Intuitive  |
| Interleaved Weaving   | O(N) Linear       | O(1) Constant ⚡  | OPTIMAL & CLEVER  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Interleaved Weaving Step-by-Step:

```
Original List: A -> B -> C -> null (where A.random = C, B.random = A, C.random = null)

Step 1: Weave Copy Nodes
A -> A' -> B -> B' -> C -> C' -> null

Step 2: Assign Random Pointers to Copy Nodes
- A'.random = A.random.next = C.next = C'
- B'.random = B.random.next = A.next = A'
- C'.random = C.random (null)

Step 3: Unweave Lists
Original List Restored: A -> B -> C -> null
Cloned List Extracted:  A' -> B' -> C' -> null ✅ (Deep Copy Complete in O(1) space!)
```

## 5. Visual Diagram
Interleaved Node Weaving Architecture:

```
Step 1:  [ Orig A ] -------> [ Orig B ] -------> [ Orig C ]
            |                   ^                   ^
            +-------------------|-------------------+  (A.random -> C)
            
Weaved:  [ Orig A ] -> [ Copy A' ] -> [ Orig B ] -> [ Copy B' ] -> [ Orig C ] -> [ Copy C' ]
                            |                                           ^
                            +-------------------------------------------+ (A'.random = A.random.next = C')
```

## 6. Operations / Algorithms
LeetCode 138 Interleaved Weaving Implementation:

```java
public Node copyRandomList(Node head) {
    if (head == null) return null;

    // Step 1: Weave cloned nodes next to original nodes (A -> A' -> B -> B')
    Node curr = head;
    while (curr != null) {
        Node copy = new Node(curr.val);
        copy.next = curr.next;
        curr.next = copy;
        curr = copy.next;
    }

    // Step 2: Assign random pointers to cloned nodes
    curr = head;
    while (curr != null) {
        if (curr.random != null) {
            curr.next.random = curr.random.next; // Copy node gets original.random.next!
        }
        curr = curr.next.next;
    }

    // Step 3: Unweave original and cloned lists
    curr = head;
    Node dummyCopy = new Node(0);
    Node copyCurr = dummyCopy;

    while (curr != null) {
        Node nextOrig = curr.next.next;

        // Extract copy node
        Node copy = curr.next;
        copyCurr.next = copy;
        copyCurr = copy;

        // Restore original node link
        curr.next = nextOrig;
        curr = nextOrig;
    }

    return dummyCopy.next;
}
```

> **Quick Syntax:**
```java
// Assign Copy Random Link
if (curr.random != null) {
    curr.next.random = curr.random.next;
}
```

## 7. Examples
* **LeetCode 138 - Copy List with Random Pointer**: Optimal $O(N)$ time and $O(1)$ space interleaved weaving solution.
* **Clone Graph (LeetCode 133)**: Deep copy graph nodes using BFS / DFS + HashMap.
* **Clone Binary Tree with Random Pointer**: Deep copy binary tree using node mapping.

## 8. Java Code
Complete interview-ready Java suite implementing BOTH HashMap $O(N)$ space and Interleaved Weaving $O(1)$ space solutions:

```java
import java.util.HashMap;
import java.util.Map;

public class DeepCopyRandomPointerMaster {

    public static class Node {
        public int val;
        public Node next;
        public Node random;
        public Node(int val) { this.val = val; }
    }

    // 1. HashMap Approach O(N) Time, O(N) Space
    public static Node copyRandomListHashMap(Node head) {
        if (head == null) return null;

        Map<Node, Node> map = new HashMap<>();

        // Pass 1: Clone all nodes and store in map
        Node curr = head;
        while (curr != null) {
            map.put(curr, new Node(curr.val));
            curr = curr.next;
        }

        // Pass 2: Connect next and random pointers
        curr = head;
        while (curr != null) {
            map.get(curr).next = map.get(curr.next);
            map.get(curr).random = map.get(curr.random);
            curr = curr.next;
        }

        return map.get(head);
    }

    // 2. Interleaved Weaving Approach (LeetCode 138) O(N) Time, O(1) Auxiliary Space
    public static Node copyRandomListOptimal(Node head) {
        if (head == null) return null;

        // Step 1: Weave cloned nodes (A -> A' -> B -> B')
        Node curr = head;
        while (curr != null) {
            Node copy = new Node(curr.val);
            copy.next = curr.next;
            curr.next = copy;
            curr = copy.next;
        }

        // Step 2: Assign random pointers to copy nodes
        curr = head;
        while (curr != null) {
            if (curr.random != null) {
                curr.next.random = curr.random.next;
            }
            curr = curr.next.next;
        }

        // Step 3: Unweave original and cloned lists
        curr = head;
        Node dummyCopy = new Node(0);
        Node copyCurr = dummyCopy;

        while (curr != null) {
            Node nextOrig = curr.next.next;

            Node copy = curr.next;
            copyCurr.next = copy;
            copyCurr = copy;

            curr.next = nextOrig; // Restore original list link
            curr = nextOrig;
        }

        return dummyCopy.next;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct: Node 1 -> Node 2 (1.random -> 2, 2.random -> 2)
        Node n1 = new Node(1);
        Node n2 = new Node(2);
        n1.next = n2;
        n1.random = n2;
        n2.random = n2;

        Node cloned = copyRandomListOptimal(n1);

        System.out.println("Original N1 Val: " + n1.val + ", Random Val: " + n1.random.val);
        System.out.println("Cloned   N1 Val: " + cloned.val + ", Random Val: " + cloned.random.val);
        System.out.println("Memory Addresses Distinct? " + (n1 != cloned && n1.random != cloned.random)); // true
    }
}
```

## 9. Complexity Analysis
| Approach | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **HashMap Node Mapping** | **$O(N)$ Linear** | $O(N)$ Extra Map | Intuitive pass 1 + pass 2 |
| **Interleaved Node Weaving**| **$O(N)$ Linear** | **$O(1)$ Constant ⚡** | OPTIMAL & NO EXTRA MAP |

## 10. Edge Cases
* **`random` Pointer is `null`**: Check `if (curr.random != null)` before setting `curr.next.random = curr.random.next`.
* **`random` Pointer Points to Self (`node.random == node`)**: Handled seamlessly by `curr.random.next`.
* **Single Node List**: Weaving converts `1 -> null` into `1 -> 1' -> null`, unweaving restores original and cloned correctly.

## 11. Common Mistakes
* Omitting Step 3 unweaving pass (leaves original list corrupted with weaved copy nodes!).
* Setting `curr.next.random = curr.random` instead of **`curr.random.next`** (causes copy node's random pointer to reference original node instead of cloned node!).
* Forgetting to restore original list links in Step 3 (violates input read-only contract).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is `curr.next.random = curr.random.next` correct in Step 2?
> * `curr` is original node $A$.
> * `curr.next` is cloned node $A'$.
> * `curr.random` is original target node $C$.
> * `curr.random.next` is cloned target node $C'$!
> Therefore, $A'$'s random pointer must point to $C'$ (`curr.random.next`).

> **Memory Trick:** **"Copy's random = Original's random's next! (curr.next.random = curr.random.next)"**

## 13. Comparisons
| Feature | HashMap Node Mapping | Interleaved Node Weaving |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Auxiliary Space** | $O(N)$ (Allocates HashMap) | **$O(1)$ Constant Space** |
| **Original List Mutation**| Read-only | Temporarily modified, then restored |
| **Interview Recommendation** | Good start | **PREFERRED OPTIMAL FINAL ANSWER** |

## 14. How to Recognize This in Questions
* **"Clone linked list with random pointers in O(1) auxiliary space"** $\rightarrow$ Interleaved Weaving Technique (LeetCode 138).
* **"Deep copy structure with arbitrary cross-references"** $\rightarrow$ Node Mapping or Weaving.

## 15. Frequently Asked Interview Questions
* **Q: Why does Interleaved Weaving achieve $O(1)$ auxiliary space?**  
  *A:* Instead of using an external HashMap to store original-to-clone node mappings, it uses the original list's own `.next` pointers as a temporary spatial mapping structure (`orig -> clone -> orig.next`).
* **Q: What happens if you forget to unweave the original list?**  
  *A:* The original list remains corrupted in an interleaved state (`A -> A' -> B -> B'`), failing caller expectations and unit tests. Unweaving cleanly restores the original list structure.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DEEP COPY LINKED LIST WITH RANDOM POINTERS            |
+-----------------------------------------------------------------------+
| • Step 1 (Weave): Create copy node after orig (curr -> copy -> curr.next)|
| • Step 2 (Random): curr.next.random = (curr.random != null) ?        |
|                    curr.random.next : null;                           |
| • Step 3 (Unweave): Disentangle original list and cloned list         |
| • Target Complexity: O(N) Linear Time | O(1) Auxiliary Space (Optimal!)|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain why `curr.random.next` points to the cloned random target.
- [ ] I can implement Step 1 (node weaving) without losing `curr.next`.
- [ ] I can implement Step 2 (random pointer assignment).
- [ ] I can implement Step 3 (unweaving original and cloned lists).
- [ ] I can solve LeetCode 138 in $O(1)$ auxiliary space from memory.
