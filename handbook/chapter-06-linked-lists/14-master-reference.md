# 14. Master Reference — Linked Lists

## 1. Introduction
This Master Reference consolidates all node memory structures, pointer manipulation formulas, mathematical proofs, operational complexities, design patterns, and interview pitfalls for **Chapter 6: Linked Lists**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh JVM node heap footprints (24B Singly, 32B Doubly), Dummy Sentinel Head Node usage, 3-Pointer Iterative Reversal (`prev`, `curr`, `nextTemp`), Fast & Slow Pointer Middle Finding, Floyd's Cycle Entry Recovery proof $L = (k-1)C + (C-a)$, Intersection 2-Pointer Swap, and Skip List probabilistic express lanes!

---

## 2. Master Mathematical & Memory Breakdown Cheat Sheet
* **Singly Node Heap Footprint (64-Bit HotSpot JVM with Compressed OOPs)**:
  - Header: 12 Bytes + Data (`int`): 4 Bytes + `next` pointer: 4 Bytes + Padding: 4 Bytes = **24 Bytes per Node**.
* **Doubly Node Heap Footprint (64-Bit HotSpot JVM with Compressed OOPs)**:
  - Header: 12 Bytes + Data (`int`): 4 Bytes + `next` ptr: 4 Bytes + `prev` ptr: 4 Bytes + Padding: 8 Bytes = **32 Bytes per Node**.
* **Floyd's Cycle Entry Proof Equation**:
  - Distance to entry = $L$, Distance to meeting point = $a$, Cycle length = $C$.
  - $D_{\text{fast}} = 2 \cdot D_{\text{slow}} \implies L + a + kC = 2(L + a) \implies \mathbf{L = (k - 1)C + (C - a)}$.
* **Josephus Problem Winner DP Formula**:
  - $J(1, k) = 0$; $J(n, k) = (J(n - 1, k) + k) \bmod n$.
  - Winner (1-Indexed) = $J(N, K) + 1$ (Executes in $O(N)$ Time and $O(1)$ Space).
* **XOR Doubly Pointer Compression**: $\text{ptr} = \text{prev} \oplus \text{next}$. $\text{next} = \text{ptr} \oplus \text{prev}$, $\text{prev} = \text{ptr} \oplus \text{next}$.

```
Linked List Types & Node Invariants Summary:
+-----------------------------------+---------------------------------------------------+
| Linked List Variant               | Invariant Rule / Memory Structure                 |
+-----------------------------------+---------------------------------------------------+
| Singly Linked List                | Node contains data + next pointer (24B JVM Heap)  |
| Doubly Linked List                | Node contains prev + data + next (32B JVM Heap)   |
| Singly Circular Linked List       | tail.next points to Head (O(1) Head & Tail access)|
| Skip List                         | Multi-level express lanes; O(log N) expected time |
| XOR Doubly Linked List            | Node stores ptr = prev XOR next (50% ptr memory)  |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Insert / Delete Head** | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ | Head pointer re-linking |
| **Insert / Delete Tail** | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ | Tail pointer re-linking |
| **Access Index `i`** | $O(1)$ | $O(i)$ Linear | $O(N)$ Linear | $O(1)$ | Sequential pointer traversal |
| **Node Unlinking (DLL)** | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ | `node.prev.next = node.next` |
| **Iterative Reversal (206)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| 3-Pointer loop (`prev`, `curr`, `nextTemp`) |
| **Sub-List Reverse (92)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| Range head-insertion loop |
| **K-Group Reverse (25)** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| Group check + chunk reversal |
| **Fast & Slow Middle (876)**| **$O(N)$ Single Pass ⚡**| **$O(N)$ Single Pass ⚡**| **$O(N)$ Single Pass ⚡**| **$O(1)$ Strict In-Place ⚡**| `fast` moves 2x, `slow` moves 1x |
| **Remove N-th End (19)** | **$O(N)$ Single Pass ⚡**| **$O(N)$ Single Pass ⚡**| **$O(N)$ Single Pass ⚡**| **$O(1)$ Strict In-Place ⚡**| Fast gap of $N+1$ steps |
| **Floyd Cycle Entry (142)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| Phase 1 2x speed, Phase 2 1x speed |
| **Intersection Swap (160)**| **$O(M + N)$ Linear ⚡**| **$O(M + N)$ Linear ⚡**| **$O(M + N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| `pA = (pA == null) ? headB : pA.next` |
| **Interleaving Copy (138)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Strict In-Place ⚡**| 3-Pass weave (A->A'), wire, unweave |
| **Merge Sort List (148)** | **$O(N \log N)$ ⚡**| **$O(N \log N)$ ⚡**| **$O(N \log N)$ ⚡**| $O(\log N)$ Stack | 1st middle split + `mergeTwoLists` |
| **Skip List Search (1206)**| **$O(1)$ Best** | **$O(\log N)$ Logarithmic⚡**| $O(N)$ Worst | $O(N)$ Array | Multi-level express lanes |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Linked List Nodes on 64-Bit JVM (Compressed OOPs)            |
+-----------------------------------------------------------------------------------+
| Singly Node (`val`, `next`)   : 12B Header + 4B Val + 4B Next + 4B Pad = 24 Bytes |
| Doubly Node (`prev`, `val`, `next`): 12B Header + 4B Val + 4B Next + 4B Prev + 8B Pad = 32 Bytes|
| Memory Efficiency Penalty     : 2000% memory overhead vs primitive int[] array!    |
| L1 Cache Line Penalty        : High cache miss rate due to pointer chasing in heap |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Dummy Sentinel Head Template
ListNode dummy = new ListNode(0, head);

// 2. 3-Pointer Iterative Reversal
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode nextTemp = curr.next;
    curr.next = prev;
    prev = curr;
    curr = nextTemp;
}

// 3. Fast & Slow Middle Finding (1st Middle for Split)
ListNode slow = head, fast = head;
while (fast.next != null && fast.next.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}

// 4. Floyd's Cycle Entry Recovery
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next; fast = fast.next.next;
    if (slow == fast) break;
}
slow = head;
while (slow != fast) { slow = slow.next; fast = fast.next; }

// 5. Intersection 2-Pointer Swap
ListNode pA = headA, pB = headB;
while (pA != pB) {
    pA = (pA == null) ? headB : pA.next;
    pB = (pB == null) ? headA : pB.next;
}
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Dereferencing `null.next` (`NullPointerException`)**: Always verify `curr != null` before accessing `curr.next`.
* **Pitfall 2: Memory Cycle Creation in List Partitioning**: Failing to execute `greaterTail.next = null` leaves stale pointers that create infinite loops.
* **Pitfall 3: Wrong Middle Split in Linked List Merge Sort**: Using 2nd middle (`fast != null && fast.next != null`) on a 2-element list `[4, 2]` causes infinite recursion. Always use **First Middle** (`fast.next != null && fast.next.next != null`).
* **Pitfall 4: `PriorityQueue.remove(Object o)` Linear Time Penalty**: Calling `pq.remove(node)` takes $O(N)$ linear time.
* **Pitfall 5: Infinite Loops in Circular Linked List Traversal**: Using `while (curr != null)` in circular list creates an infinite loop. Always use `do { ... } while (curr != head)`.
* **Pitfall 6: Forgetting `head.next = null` in Recursive Reversal**: Creates 2-node cycle at tail. Always set `head.next = null` after `head.next.next = head`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 6 (LINKED LISTS)                 |
+-----------------------------------------------------------------------+
| 1. Node Heap Footprint: Singly 24 Bytes, Doubly 32 Bytes on 64B JVM   |
| 2. Dummy Sentinel: ListNode dummy = new ListNode(0, head) for head ops|
| 3. O(1) DLL Unlink: node.prev.next = node.next; node.next.prev = node.prev|
| 4. Circular List: Single tail reference gives O(1) head & tail access!|
| 5. Partitioning Guard: ALWAYS set greaterTail.next = null!            |
| 6. Reversal Formula: nextTemp = curr.next; curr.next = prev; prev=curr|
| 7. Middle Split: Use fast.next != null && fast.next.next != null for Merge Sort|
| 8. Floyd's Proof: L = (k-1)C + (C-a); Reset slow to head when meeting |
| 9. Intersection Swap: pA = (pA == null) ? headB : pA.next             |
| 10. Interleaving Copy (138): Pass 1 Weave, Pass 2 Wire, Pass 3 Unweave|
| 11. Josephus Winner (1823): winner = (winner + k) % i in O(N) Time    |
| 12. Skip List (1206): Probabilistic express lanes give O(log N) time  |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write the 64-bit JVM heap memory breakdown of Singly and Doubly nodes.
- [ ] I can write `addAtIndex` using the Dummy Head sentinel node pattern.
- [ ] I can write 3-pointer iterative reversal in under 2 minutes.
- [ ] I can write recursive reversal and explain `head.next.next = head`.
- [ ] I can solve Reverse Linked List II (LeetCode 92) in a single pass.
- [ ] I can solve Reverse Nodes in K-Group (LeetCode 25) in $O(1)$ space.
- [ ] I can write single-pass Remove N-th Node From End (LeetCode 19).
- [ ] I can state and derive the mathematical proof $L = (k-1)C + (C-a)$ for Floyd's algorithm.
- [ ] I can write 2-pointer swap Intersection (LeetCode 160) in 6 lines.
- [ ] I can write 3-pass Interleaving Deep Copy (LeetCode 138) in $O(1)$ space.
- [ ] I can write Linked List Merge Sort (LeetCode 148) in $O(N \log N)$ time.
- [ ] I know why Skip Lists achieve $O(\log N)$ expected time in Redis Sorted Sets.
