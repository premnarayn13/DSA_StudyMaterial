# 08. Floyd's Cycle Detection Algorithm, Cycle Start Recovery & Mathematical Proofs

## 1. Introduction
**Floyd's Cycle Detection Algorithm** (popularly known as the **Tortoise and Hare Cycle Finding Algorithm**) is a landmark algorithm in computer science for detecting cycles in linked lists or functional iteration sequences in **$O(N)$ linear time and $O(1)$ constant auxiliary space**. It solves **Linked List Cycle (LeetCode 141)**, **Linked List Cycle II (LeetCode 142)**, and **Find the Duplicate Number (LeetCode 287)**.

> **Important:** While a Hash Set (`Set<ListNode> visited`) detects cycles in $O(N)$ time, it requires **$O(N)$ auxiliary memory**. Floyd's algorithm proves mathematically that a `slow` pointer (moving 1 step) and a `fast` pointer (moving 2 steps) WILL meet inside a cycle if one exists, achieving cycle detection and cycle start node recovery in **$O(1)$ constant memory**!

```
Cycle Detection Strategy Spectrum:
+-----------------------------------------------------------------------------------+
| Hash Set Approach   : Set<ListNode> visited -> O(N) Time, O(N) Space (High Memory)|
| Floyd's Algorithm   : Slow & Fast Pointers  -> O(N) Time, O(1) Space ⚡ (Optimal)   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Proof of Floyd's Algorithm

### 2.1 Cycle Detection Phase (LeetCode 141)
1. Initialize `slow = head`, `fast = head`.
2. Advance `slow = slow.next` (1 step) and `fast = fast.next.next` (2 steps).
3. If a cycle exists, `fast` will eventually overlap with `slow` (`slow == fast`).
4. If `fast == null` or `fast.next == null`, the list has no cycle!

### 2.2 Mathematical Proof of Cycle Start Recovery (LeetCode 142)
Let:
* $L$ = Distance from `head` to the **Cycle Entry Node**.
* $a$ = Distance from the Cycle Entry Node to the **Meeting Point** where `slow == fast`.
* $C$ = Total Length of the Cycle.
* $k$ = Number of full loop laps completed by `fast` inside the cycle.

```
Mathematical Setup Topology:
head ---- L steps ----> ( Entry Node ) ---- a steps ----> ( Meeting Point: slow == fast )
                             ^                                   |
                             |----------- (C - a) steps ---------|
```

* Distance traveled by `slow`: $D_{\text{slow}} = L + a$
* Distance traveled by `fast`: $D_{\text{fast}} = L + a + k \cdot C$
* Since `fast` moves at **twice the speed** of `slow`:

$$D_{\text{fast}} = 2 \cdot D_{\text{slow}}$$

$$L + a + k \cdot C = 2(L + a)$$

$$L + a + k \cdot C = 2L + 2a$$

$$\mathbf{L = k \cdot C - a = (k - 1)C + (C - a)}$$

#### Fundamental Conclusion:
The distance $L$ from `head` to the Cycle Entry Node is **EXACTLY EQUAL** to the distance $(C - a)$ from the Meeting Point to the Cycle Entry Node (plus any number of full cycle laps)!

#### Algorithm to Find Cycle Start (LeetCode 142):
1. When `slow == fast` meet at the Meeting Point, **reset `slow = head`**.
2. Keep `fast` at the Meeting Point.
3. Advance BOTH `slow` and `fast` at **1 step per iteration**.
4. The exact node where `slow` and `fast` meet again is the **Cycle Entry Node**!

> **Memory Trick:** **"When slow and fast meet, reset slow to head! Move both 1 step at a time; they WILL meet at the cycle entry node!"**

---

## 3. Characteristics & Cycle Length Calculation

### 3.1 Computing Cycle Length $C$
Once `slow == fast` meet inside the cycle:
1. Keep `slow` stationary at the Meeting Point.
2. Advance `fast = fast.next` 1 step at a time, incrementing a `length` counter.
3. Stop when `fast == slow` again.
4. The value of `length` is the **Exact Number of Nodes in the Cycle $C$**!

---

## 4. Internal Working Mechanics
Tracing Floyd's Cycle Start Recovery on List `3 -> 2 -> 0 -> -4 -> 2` (Entry at node 2):

```
List Layout: 3 (head) -> 2 (entry) -> 0 -> -4 -> 2 (cycle: 2, 0, -4)
L = 1 (node 3 to 2), C = 3 (nodes 2, 0, -4)

Phase 1: Detect Meeting Point:
- Step 0: slow=3, fast=3
- Step 1: slow=2, fast=0
- Step 2: slow=0, fast=2
- Step 3: slow=-4, fast=-4  ===> MEETING POINT at node -4! (a = 2)

Phase 2: Find Cycle Entry Node:
- Reset slow = 3 (head), Keep fast = -4.
- Step 1: slow = 2 (slow.next), fast = 2 (-4.next)  ===> MATCH AT NODE 2!

Cycle Entry Node = Node 2! ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Floyd's Algorithm Meeting & Entry Node Topography:

```
                  L steps                           a steps
head (3) ---------------------> [ Node 2: ENTRY ] -------------> [ Node -4: MEETING ]
                                    ^                                    |
                                    |----------- (C - a) steps ----------|
                                                (1 step)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Cycle Detection (LeetCode 141), Cycle Start Recovery (LeetCode 142), and Find Duplicate Number (LeetCode 287):

```java
import java.util.*;

public class FloydCycleDetectionMaster {

    public static class ListNode {
        public int val;
        public ListNode next;

        public ListNode(int val) {
            this.val = val;
            this.next = null;
        }
    }

    // 1. Detect Cycle Existence (LeetCode 141) O(N) Time, O(1) Space
    public static boolean hasCycle(ListNode head) {
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

        return false; // Reached end, no cycle
    }

    // 2. Find Cycle Entry Node (LeetCode 142) O(N) Time, O(1) Space
    public static ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;

        ListNode slow = head;
        ListNode fast = head;
        boolean hasCycle = false;

        // Phase 1: Find Meeting Point
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
            fast = fast.next;
        }

        return slow; // Cycle entry node!
    }

    // 3. Compute Length of Cycle O(N) Time, O(1) Space
    public static int getCycleLength(ListNode head) {
        ListNode entry = detectCycle(head);
        if (entry == null) return 0;

        int length = 1;
        ListNode curr = entry.next;
        while (curr != entry) {
            length++;
            curr = curr.next;
        }

        return length;
    }

    // 4. Find the Duplicate Number (LeetCode 287) O(N) Time, O(1) Space
    public static int findDuplicate(int[] nums) {
        // Model array as linked list: f(i) = nums[i]
        int slow = nums[0];
        int fast = nums[0];

        // Phase 1: Find Meeting Point
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: Reset slow to start
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }

        return slow; // Duplicate number!
    }
}
```

> **Quick Syntax:**
```java
// Cycle Entry Recovery Phase 2 Loop
slow = head;
while (slow != fast) {
    slow = slow.next;
    fast = fast.next;
}
return slow;
```

---

## 7. Concrete Problem Examples
* **LeetCode 141 - Linked List Cycle**: Boolean cycle detection.
* **LeetCode 142 - Linked List Cycle II**: Cycle start node recovery.
* **LeetCode 287 - Find the Duplicate Number**: Modeling array as linked list cycle.
* **LeetCode 202 - Happy Number**: Cycle detection in digit sum sequence.

---

## 8. Java Code Demonstration & Dry Run
Demonstration detecting cycles, finding entry node, measuring cycle length, and solving LeetCode 287:

```java
public class FloydCycleDetectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Floyd Cycle Detection (LeetCode 142) ===");
        FloydCycleDetectionMaster.ListNode node1 = new FloydCycleDetectionMaster.ListNode(3);
        FloydCycleDetectionMaster.ListNode node2 = new FloydCycleDetectionMaster.ListNode(2);
        FloydCycleDetectionMaster.ListNode node3 = new FloydCycleDetectionMaster.ListNode(0);
        FloydCycleDetectionMaster.ListNode node4 = new FloydCycleDetectionMaster.ListNode(-4);

        node1.next = node2;
        node2.next = node3;
        node3.next = node4;
        node4.next = node2; // Cycle back to node 2

        FloydCycleDetectionMaster.ListNode entry = FloydCycleDetectionMaster.detectCycle(node1);
        System.out.println("Cycle Entry Node Value: " + (entry != null ? entry.val : "None")); // Output: 2

        int cycleLen = FloydCycleDetectionMaster.getCycleLength(node1);
        System.out.println("Cycle Length: " + cycleLen); // Output: 3

        System.out.println("\n=== 2. Find Duplicate Number (LeetCode 287) ===");
        int[] nums = {1, 3, 4, 2, 2};
        int duplicate = FloydCycleDetectionMaster.findDuplicate(nums);
        System.out.println("Duplicate Number: " + duplicate); // Output: 2
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Cycle Detection (141)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `slow` moves 1x, `fast` moves 2x |
| **Cycle Entry Node (142)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Mathematical proof $L = (k-1)C + (C-a)$ |
| **Find Duplicate (287)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Modeling `nums[i]` as pointer |

---

## 10. Edge Cases & Boundary Handling
* **Null or Single Element List Without Cycle (`head == null || head.next == null`)**: Returns `false` or `null` immediately.
* **Self-Loop Node (`node.next == node`)**: `slow` and `fast` meet immediately at `node`.

---

## 11. Common Mistakes & Anti-Patterns
* **Advancing Both Pointers 1 Step at a Time in Phase 1**:
  - `slow = slow.next; fast = fast.next;` (Pointers stay at the same distance, never catching up!).
  - **Phase 1 requires `fast` to move at 2x speed (`fast = fast.next.next`)**.
* **Advancing Fast 2 Steps in Phase 2**:
  - In Phase 2 (Cycle Entry Recovery), **BOTH `slow` and `fast` MUST move at 1 step per iteration** (`slow = slow.next; fast = fast.next;`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Modeling Array as Linked List Cycle (LeetCode 287):
> An array of $N+1$ integers where elements are in range $[1 \dots N]$ contains at least one duplicate.
> Modeling index $i \to \text{nums}[i]$ creates a directed functional graph.
> Because a value appears multiple times, **multiple indices point to the same value**, creating a **Cycle Entry Node at the Duplicate Value**!

> **Memory Trick:** **"Phase 1: fast moves 2x! Phase 2 (Entry Recovery): reset slow to head, move BOTH 1x!"**

---

## 13. System & Implementation Comparisons

| Feature | Hash Set Cycle Detection | Floyd's Cycle Detection Algorithm |
| :--- | :--- | :--- |
| **Auxiliary Memory** | $O(N)$ Heap Space (High Footprint) | **$O(1)$ Constant Space ⚡** |
| **Time Complexity** | $O(N)$ Average | **$O(N)$ Linear ⚡** |
| **Modifies Data Structure**| No | No |

---

## 14. How to Recognize This in Questions
* **"Determine if a linked list has a cycle in O(1) memory"** $\rightarrow$ LeetCode 141 (Floyd's algorithm).
* **"Find node where cycle begins in linked list"** $\rightarrow$ LeetCode 142 (Reset `slow` to `head`, move both 1x).
* **"Find duplicate number in array of size N+1 in O(1) space"** $\rightarrow$ LeetCode 287 (Model array as linked list).

---

## 15. Frequently Asked Interview Questions
* **Q: Why are `slow` and `fast` guaranteed to meet if a cycle exists?**  
  *A:* Inside a cycle, `fast` closes the gap to `slow` by 1 node per iteration. Since the relative distance decreases by 1 step each time, `fast` is mathematically guaranteed to overtake and overlap `slow` within $C$ iterations!
* **Q: Why must both pointers move 1 step at a time during Phase 2 of Floyd's algorithm?**  
  *A:* Because the distance $L$ from `head` to entry node equals $(C - a)$ from meeting point to entry node. Moving both pointers 1 step at a time ensures they cover equal distances and meet precisely at the entry node.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLOYD'S CYCLE DETECTION ALGORITHM                      |
+-----------------------------------------------------------------------+
| • Phase 1 (Detection): slow moves 1x, fast moves 2x                   |
| • Meeting Guarantee: Relative distance closes by 1 node per step      |
| • Proof Formula: L = (k - 1)C + (C - a)                               |
| • Phase 2 (Entry Recovery): Reset slow to head, move BOTH 1x          |
| • Re-meeting Point: Exactly at Cycle Entry Node (LeetCode 142)!       |
| • Array Duplicate Trick (287): Model index i -> nums[i] as linked list|
| • Space Invariant: Strictly O(1) Auxiliary Memory ⚡                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Linked List Cycle (LeetCode 141) in under 2 minutes.
- [ ] I can state and derive the mathematical proof $L = (k-1)C + (C-a)$.
- [ ] I can write Linked List Cycle II (LeetCode 142) cycle entry recovery.
- [ ] I can solve Find the Duplicate Number (LeetCode 287) in $O(1)$ space.
- [ ] I know how to calculate the exact number of nodes in a cycle.
