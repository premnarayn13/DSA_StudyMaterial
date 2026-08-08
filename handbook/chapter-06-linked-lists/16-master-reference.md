# 16. Master Reference — Linked Lists

## 1. Introduction
This Master Reference consolidates all core principles, node architectures, pointer manipulation formulas, complexity matrices, and Java syntax templates for **Chapter 6: Linked Lists**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Fast & Slow pointer guards, 3-pointer reversal steps, LRU Cache doubly linked list setups, and Floyd's cycle entry proofs.

## 2. Core Concepts & Formulas Cheat Sheet
* **Dummy Head Sentinel**: `ListNode dummy = new ListNode(-1); dummy.next = head;`
* **Fast & Slow Loop Guard**: `while (fast != null && fast.next != null)`
* **Middle Node Condition (Merge Sort)**: `while (fast.next != null && fast.next.next != null)`
* **Iterative Reversal Steps**:
  1. `ListNode nextTemp = curr.next;`
  2. `curr.next = prev;`
  3. `prev = curr;`
  4. `curr = nextTemp;`
* **Doubly Linked List Node Removal**: `node.prev.next = node.next; node.next.prev = node.prev;`
* **2-Pointer Intersection Switch**: `pA = (pA == null) ? headB : pA.next; pB = (pB == null) ? headA : pB.next;`
* **Floyd's Cycle Entry Phase 2**: Reset `slow = head`, move both 1 step at a time (`slow = slow.next`, `fast = fast.next`).
* **Addition Carry Loop Guard**: `while (l1 != null || l2 != null || carry != 0)`
* **PriorityQueue Comparator**: `new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val))`

> **Memory Trick:** **"Always check fast != null FIRST, then fast.next != null SECOND!"**

## 3. Master Linked List Algorithm Complexity Table
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Triggers / Use Case |
| :--- | :--- | :--- | :--- |
| **Singly List Head Insertion** | **$O(1)$** | $O(1)$ | `newNode.next = head; head = newNode;` |
| **Singly List Access Index K** | $O(K)$ | $O(1)$ | Sequential pointer traversal |
| **Doubly Node Removal (Known)**| **$O(1)$** | **$O(1)$** | `node.prev.next = node.next;` |
| **Iterative List Reversal** | **$O(N)$** | **$O(1)$** | `prev`, `curr`, `nextTemp` 3-pointer loop |
| **Find Middle Node** | **$O(N)$** | **$O(1)$** | Fast (2 steps) & Slow (1 step) pointers |
| **Remove N-th From End** | **$O(N)$** | **$O(1)$** | Fast/Slow gap technique with Dummy Head |
| **Floyd's Cycle Detection** | **$O(N)$** | **$O(1)$** | Phase 1: `slow == fast`; Phase 2: `slow=head` |
| **Intersection Node Search** | **$O(L_A + L_B)$**| **$O(1)$** | 2-Pointer Head Switch (`pA==null?headB`) |
| **Merge 2 Sorted Lists** | **$O(N_1 + N_2)$** | **$O(1)$** | Dummy head node pointer relinking |
| **Merge K Sorted Lists** | **$O(N \log K)$** | $O(K)$ | Min-Heap (`PriorityQueue`) |
| **Partition List (< X)** | **$O(N)$** | **$O(1)$** | Dual Dummy Heads (`large.next = null`) |
| **Copy List with Random** | **$O(N)$** | **$O(1)$** | Interleaved Weaving (`curr.next.random`) |
| **Flatten Multilevel List** | **$O(N)$** | $O(N)$ | Iterative `ArrayDeque` DFS Stack |
| **Merge Sort List** | **$O(N \log N)$** | $O(\log N)$ Stack | Sever `mid.next = null`, recurse, merge |
| **Add Two Numbers** | **$O(N)$** | $O(1)$ Aux | Carry loop `while (l1!=null || l2!=null || carry!=0)`|
| **LRU Cache** | **$O(1)$ get/put**| $O(N)$ Space | `HashMap<Key, Node>` + DoublyLinkedList |

## 4. Hardware & Memory Footprint Summary
```
+-----------------------------------------------------------------------------------+
| Node Architecture Element   | Memory Footprint & Details                          |
+-----------------------------------------------------------------------------------+
| ListNode (64-bit JVM)       | 24 Bytes (8B Mark + 4B Klass + 4B val + 4B next + 4B pad)|
| Array Footprint (int[1000]) | ~4,016 Bytes (Near 100% L1 CPU Cache Hits)          |
| ListNode Footprint (1,000)  | ~24,000 Bytes (6x Memory Overhead, High Cache Misses)|
| Compressed OOPs (-XX)       | Compresses 64-bit object references to 32 bits (<32GB)|
+-----------------------------------------------------------------------------------+
```

## 5. Java Code Templates & Snippets

> **Quick Syntax:**
```java
// 1. Dummy Head
ListNode dummy = new ListNode(-1); dummy.next = head;

// 2. Iterative Reversal
ListNode prev = null, curr = head;
while (curr != null) {
    ListNode nextTemp = curr.next;
    curr.next = prev;
    prev = curr;
    curr = nextTemp;
}

// 3. Fast & Slow Middle
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}

// 4. PriorityQueue Comparator
PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: Null Pointer in Fast/Slow Loop**: Always write `while (fast != null && fast.next != null)`.
* **Trap 2: Severing Link in Merge Sort**: Always set `mid.next = null` before recursing. Use `while (fast.next != null && fast.next.next != null)` for `getMid` to avoid infinite recursion on 2-element lists `[4, 2]`.
* **Trap 3: Forgetting `large.next = null` in Partition**: Failing to clear tail pointer creates cyclic reference loops.
* **Trap 4: `PriorityQueue` Underflow Risk**: Use `Integer.compare(a.val, b.val)` instead of `a.val - b.val`.
* **Trap 5: Missing `carry != 0` in Addition**: Truncates final carry digit node (e.g. returning $99 + 1 = 00$ instead of $100$).

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 6 (LINKED LISTS)                 |
+-----------------------------------------------------------------------+
| 1. Dummy Head: ListNode dummy = new ListNode(-1); dummy.next = head   |
| 2. Reversal: nextTemp=curr.next; curr.next=prev; prev=curr; curr=nextTemp|
| 3. Fast/Slow Guard: while (fast != null && fast.next != null)         |
| 4. Cycle Entry Phase 2: Reset slow = head, move BOTH 1 step at a time  |
| 5. Intersection: pA = (pA == null) ? headB : pA.next                  |
| 6. LRU Cache: HashMap<Key, Node> + DoublyLinkedList with Sentinels     |
| 7. List Merge Sort: Split at 1st mid (fast.next & fast.next.next),    |
|    sever mid.next = null, sort halves, merge in-place                 |
| 8. Memory: 1 ListNode = 24 Bytes (6x RAM overhead compared to array)  |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write Dummy Head setup and iterative 3-pointer list reversal from memory.
- [ ] I can write Fast & Slow pointer middle finding, cycle detection, and cycle entry discovery.
- [ ] I can write 2-pointer list intersection search in $O(1)$ space.
- [ ] I can implement LRU Cache (LeetCode 146) in under 10 minutes.
- [ ] I can write linked list Merge Sort (LeetCode 148) with proper `mid.next = null` severing.
