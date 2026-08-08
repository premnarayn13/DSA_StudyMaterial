# 06. Cycle Detection & Floyd's Cycle-Finding Algorithm

## 1. Introduction
A **Cycle** in a linked list occurs when a node's `next` pointer references an earlier node in the list chain, creating an infinite loop. In technical coding interviews, **Floyd's Cycle-Finding Algorithm** detects whether a cycle exists (LeetCode 141 - Linked List Cycle) AND finds the exact starting node of the cycle (LeetCode 142 - Linked List Cycle II) in **$O(N)$ linear time and $O(1)$ auxiliary space**.

> **Important:** If a cycle exists, `fast` (moving 2 steps) and `slow` (moving 1 step) will **GUARANTEE TO MEET** inside the cycle loop! Once they meet, resetting `slow = head` while keeping `fast` at the meeting point and moving both 1 step at a time will cause them to meet at the **Cycle Entry Node**!

## 2. Core Concepts
* **Cycle Existence Check (LeetCode 141)**: If `fast` and `slow` meet (`slow == fast`), a cycle exists. If `fast == null` or `fast.next == null`, no cycle exists.
* **Mathematical Proof of Cycle Entry Node (LeetCode 142)**:
  Let distance from `head` to cycle entry be $X$, distance from cycle entry to meeting point be $Y$, and remaining cycle loop distance be $Z$ (Total Cycle Length $C = Y + Z$).
  * Distance by `slow` $= X + Y$
  * Distance by `fast` $= X + Y + K \cdot C = 2(X + Y)$
  * Simplifying: $X + Y = K \cdot C \implies \mathbf{X = K \cdot C - Y = (K - 1)C + Z}$
  * **Conclusion**: The distance from `head` to the cycle entry ($X$) equals the distance from the meeting point to the cycle entry ($Z$)!

> **Memory Trick:** **"Meeting point found? Reset slow to head! Move both 1 step at a time — they WILL meet at the cycle entry node!"**

## 3. Characteristics / Properties
* **$O(1)$ Space Optimality**: Detects cycles without allocating a `HashSet<ListNode>` to store visited node references.
* **Bounded Steps to Intersection**: Inside a cycle of length $C$, `fast` reduces distance to `slow` by 1 step per iteration, ensuring intersection within at most $C$ steps inside the cycle loop.

```
Cycle Detection Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Detection Method      | Time Complexity   | Space Complexity  | Mutates Input?    |
+-----------------------+-------------------+-------------------+-------------------+
| Visited HashSet       | O(N) Linear       | O(N) Extra Memory | No                |
| Floyd's Tortoise & Hare| O(N) Linear ⚡   | O(1) Constant ⚡  | No (Optimal!)     |
| Node Flag Modification| O(N) Linear       | O(1)              | YES (Corrupts Data)|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Floyd's Cycle Entry Finding (LeetCode 142) on `3 -> 2 -> 0 -> -4 -> (back to 2)`:

```
Distance X (head=3 to entry=2): 1 step
Cycle Entry=2, Meeting Point=-4 (Y=2, Z=1, Cycle Length C=3)

Phase 1: Fast & Slow pointers meet at node -4
slow = node -4, fast = node -4

Phase 2: Find Cycle Entry
- Reset slow = head (node 3)
- Keep fast = node -4 (meeting point)
- Move BOTH 1 step at a time:

Step 1:
- slow = 3.next = node 2 (Cycle Entry!)
- fast = (-4).next = node 2 (Cycle Entry!)

slow == fast at Node 2! Return Node 2 (Cycle Entry Node!) ✅
```

## 5. Visual Diagram
Mathematical Layout of Floyd's Cycle Entry Proof:

```
Head ---- (Distance X) ----> [ Cycle Entry Node ]
                                /          \
                               /            \
                  (Distance Z)             (Distance Y)
                             \              /
                              v            v
                           [ Meeting Point ]
```

$$\text{Distance}(Head \to Entry) = X \quad \text{matches} \quad \text{Distance}(Meeting \to Entry) = Z$$

## 6. Operations / Algorithms
LeetCode 141 & LeetCode 142 Master Implementation:

```java
// 1. Detect Has Cycle (LeetCode 141) O(N) Time, O(1) Space
public boolean hasCycle(ListNode head) {
    if (head == null || head.next == null) return false;

    ListNode slow = head;
    ListNode fast = head;

    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            return true; // Cycle detected!
        }
    }
    return false; // Reached end -> No cycle
}

// 2. Find Cycle Entry Node (LeetCode 142) O(N) Time, O(1) Space
public ListNode detectCycle(ListNode head) {
    if (head == null || head.next == null) return null;

    ListNode slow = head;
    ListNode fast = head;
    boolean hasCycle = false;

    // Phase 1: Find meeting point inside cycle
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            hasCycle = true;
            break;
        }
    }

    if (!hasCycle) return null; // No cycle

    // Phase 2: Reset slow to head and move both 1 step at a time
    slow = head;
    while (slow != fast) {
        slow = slow.next;
        fast = fast.next; // Move 1 step!
    }

    return slow; // Both meet at Cycle Entry Node!
}
```

> **Quick Syntax:**
```java
// Phase 2 Cycle Entry Step Syntax
slow = head;
while (slow != fast) {
    slow = slow.next;
    fast = fast.next; // Move 1 step (NOT 2)!
}
```

## 7. Examples
* **LeetCode 141 - Linked List Cycle**: Detecting if a cycle exists in $O(1)$ space.
* **LeetCode 142 - Linked List Cycle II**: Finding the exact cycle entry node.
* **LeetCode 287 - Find the Duplicate Number**: Mapping array values to linked list pointers (`nums[i]` as `next`) and using Floyd's Cycle Algorithm in $O(N)$ time and $O(1)$ space.

## 8. Java Code
Complete interview-ready Java suite implementing Cycle Detection, Cycle Entry Node Discovery, and Cycle Length Calculation:

```java
public class CycleDetectionMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Detect Cycle Entry Node (LeetCode 142) O(N) Time, O(1) Space
    public static ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;

        ListNode slow = head, fast = head;
        boolean hasCycle = false;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                hasCycle = true;
                break;
            }
        }

        if (!hasCycle) return null;

        // Reset slow to head, move both 1 step at a time
        slow = head;
        while (slow != fast) {
            slow = slow.next;
            fast = fast.next;
        }

        return slow;
    }

    // 2. Calculate Cycle Length O(N) Time, O(1) Space
    public static int getCycleLength(ListNode head) {
        ListNode slow = head, fast = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // Count steps around cycle
                int length = 0;
                do {
                    slow = slow.next;
                    length++;
                } while (slow != fast);
                return length;
            }
        }
        return 0; // No cycle
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Construct List: 3 -> 2 -> 0 -> -4 -> (back to 2)
        ListNode head = new ListNode(3);
        ListNode node2 = new ListNode(2);
        ListNode node0 = new ListNode(0);
        ListNode node4 = new ListNode(-4);

        head.next = node2;
        node2.next = node0;
        node0.next = node4;
        node4.next = node2; // Cycle back to node 2!

        ListNode cycleEntry = detectCycle(head);
        System.out.println("Cycle Entry Node Value: " + (cycleEntry != null ? cycleEntry.val : "None")); // Output: 2
        System.out.println("Cycle Length: " + getCycleLength(head)); // Output: 3
    }
}
```

## 9. Complexity Analysis
| Phase | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Phase 1 (Cycle Intersection)**| $O(N)$ Linear | **$O(1)$ Constant** | Fast & slow meet in $< N$ steps |
| **Phase 2 (Cycle Entry Node)** | $O(N)$ Linear | **$O(1)$ Constant** | Both move 1 step at a time |
| **Total Floyd's Algorithm** | **$O(N)$ Linear** | **$O(1)$ Constant** | Optimal time and space ⚡ |

## 10. Edge Cases
* **No Cycle (`fast == null || fast.next == null`)**: Returns `false` or `null` cleanly.
* **Single Node Cyclic List (`head.next == head`)**: `slow` and `fast` meet immediately at `head`.
* **Cycle Encompasses Entire List ($X = 0$)**: Meeting point phase 2 immediately finds `slow == fast == head`.

## 11. Common Mistakes
* Moving `fast` by 2 steps during Phase 2 cycle entry discovery (Phase 2 MUST move `fast` by **1 step** at a time!).
* Returning the meeting point node instead of Phase 2's entry node (the initial meeting point is NOT the cycle entry!).
* Using `HashSet` to store visited nodes when an $O(1)$ space solution was explicitly requested.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Phase 1 vs Phase 2 Pointer Speeds:
> * **Phase 1 (Find Meeting Point)**: `slow = slow.next` (1 step), `fast = fast.next.next` (2 steps).
> * **Phase 2 (Find Cycle Entry)**: Reset `slow = head`. `slow = slow.next` (1 step), **`fast = fast.next` (1 step)**!

> **Memory Trick:** **"Phase 1: Fast moves 2 steps. Phase 2: BOTH move 1 step!"**

## 13. Comparisons
| Feature | HashSet Visited Tracking | Floyd's Cycle Algorithm |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Space Complexity**| $O(N)$ Extra Memory | **$O(1)$ Constant Space ⚡** |
| **Input Modification**| None | None |
| **Interview Score** | Naive | **OPTIMAL & EXPECTED** |

## 14. How to Recognize This in Questions
* **"Determine if linked list has a cycle in O(1) space"** $\rightarrow$ Floyd's Cycle Algorithm (LeetCode 141).
* **"Find node where cycle begins in O(1) space"** $\rightarrow$ Floyd's Cycle Algorithm Phase 1 + Phase 2 (LeetCode 142).
* **"Find duplicate number in array of 1..N in O(1) space without modifying array"** $\rightarrow$ Map array to linked list and run Floyd's Cycle Algorithm (LeetCode 287).

## 15. Frequently Asked Interview Questions
* **Q: Why are `fast` and `slow` guaranteed to meet inside a cycle?**  
  *A:* Once both pointers are inside a cycle loop of size $C$, `fast` is behind `slow` by some distance $D < C$. In each step, `fast` closes the gap by 1 node ($2 - 1 = 1$). Therefore, `fast` is guaranteed to catch up to `slow` in at most $D$ steps.
* **Q: How does LeetCode 287 (Find Duplicate Number) use Floyd's Cycle Algorithm?**  
  *A:* View the array as a implicit functional graph where index $i$ points to node `nums[i]`. Since values are in range $1 \dots N$ and array size is $N + 1$, at least two indices point to the same value, creating a cycle. The entry node of the cycle corresponds to the duplicate number!

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CYCLE DETECTION & FLOYD'S ALGORITHM                  |
+-----------------------------------------------------------------------+
| • Phase 1 (Detect): slow=1 step, fast=2 steps; meet when slow == fast |
| • Phase 2 (Entry): Reset slow = head; move slow=1 step, fast=1 step   |
| • Entry Condition: Both meet at Cycle Entry Node!                      |
| • Cycle Length: Keep fast fixed, move slow around loop counting steps |
| • Complexity: O(N) Linear Time | O(1) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write Phase 1 cycle detection `hasCycle` in under 2 minutes.
- [ ] I can prove why $X = Z$ mathematically for Phase 2 cycle entry.
- [ ] I can implement Phase 2 cycle entry `detectCycle` (LeetCode 142).
- [ ] I know why `fast` moves 1 step per iteration in Phase 2.
- [ ] I can solve LeetCode 287 (Find Duplicate Number) using Floyd's Cycle algorithm.
