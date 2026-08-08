# 07. K-Way Merge Pattern, Multi-Stream Merging & Matrix Selection

## 1. Introduction
The **K-Way Merge Pattern** is a fundamental algorithmic pattern for merging $K$ sorted data streams, lists, arrays, or matrix rows into a single unified sorted sequence. It powers **Merge k Sorted Lists (LeetCode 23)**, **Kth Smallest Element in a Sorted Matrix (LeetCode 378)**, and **Find K Pairs with Smallest Sums (LeetCode 373)**. By using a **Min-Heap of size $K$** storing current stream head references, the K-Way Merge pattern processes $N$ total elements across $K$ sorted streams in **$O(N \log K)$ time and $O(K)$ space**.

> **Important:** Instead of loading all $N$ elements into memory simultaneously ($O(N \log N)$ time and $O(N)$ memory), K-Way Merge maintains only **1 candidate element per active stream** in the Min-Heap. When the minimum candidate is polled, its stream immediately advances to push the next candidate into the heap!

```
K-Way Merge Pattern Spectrum:
+-----------------------------------------------------------------------------------+
| Naive Full Sort     : Flatten streams -> Arrays.sort() -> O(N log N) Time, O(N) Space|
| Min-Heap K-Way Merge: Priority Queue of size K    -> O(N log K) Time, O(K) Space⚡|
| Divide & Conquer Merge: Pairwise Merge Lists       -> O(N log K) Time, O(1) Space⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 The Min-Heap K-Way Merge Algorithm
Given $K$ sorted linked lists or streams containing $N$ total elements:
1. Instantiate a `PriorityQueue<ListNode> minHeap` of size $K$ ordering nodes by value (`Integer.compare(a.val, b.val)`).
2. Push the **head node of each non-empty list** into `minHeap`.
3. Create a dummy head pointer: `dummy = new ListNode(0)`, `curr = dummy`.
4. While `!minHeap.isEmpty()`:
   - Poll the smallest node: `minNode = minHeap.poll()`.
   - Append `minNode` to the merged list: `curr.next = minNode; curr = curr.next;`.
   - **Stream Advancement**: If `minNode.next != null`, push the next node from that specific list into the heap: **`minHeap.offer(minNode.next)`**!

### 2.2 K-Way Matrix Traversal (LeetCode 378 / LeetCode 373)
When merging 2D sorted matrices or array pairs:
* Each matrix row is an independent sorted stream.
* Store a tuple `Element{val, row, col}` in the Min-Heap.
* Initially push the first element of each row `matrix[r][0]` for $r \in [0 \dots K-1]$.
* When polling element `(val, r, c)`: If $c + 1 < \text{COLS}$, push the next column neighbor `matrix[r][c + 1]`!

```
K-Way Merge Node Pointer Advancement:
Stream 1: ( 1 ) -> ( 4 ) -> ( 5 )  ===> Push 1 to Min-Heap
Stream 2: ( 1 ) -> ( 3 ) -> ( 4 )  ===> Push 1 to Min-Heap
Stream 3: ( 2 ) -> ( 6 )           ===> Push 2 to Min-Heap

Heap: [1(s1), 1(s2), 2(s3)]
Poll 1(s1) -> Append 1 -> Push next from Stream 1: ( 4 ) -> Heap: [1(s2), 2(s3), 4(s1)]
```

> **Memory Trick:** **"K-Way Merge keeps 1 candidate per stream in Min-Heap of size K! Poll min -> Push next node from SAME stream!"**

---

## 3. Characteristics & Divide and Conquer Alternative

### 3.1 Divide & Conquer Pairwise List Merging ($O(N \log K)$ Time, $O(1)$ Space)
Merge $K$ sorted lists pairwise without using a Priority Queue:
* Pair lists up: `list[0]` with `list[K-1]`, `list[1]` with `list[K-2]`, etc.
* Merge each pair using standard 2-pointer linked list merge (`mergeTwoLists`).
* Repeat recursively for $\log_2 K$ rounds until only 1 merged list remains.
* **Advantage**: Achieves $O(N \log K)$ time with **$O(1)$ constant auxiliary memory** (zero priority queue memory allocation!).

```
Divide & Conquer Pairwise Merge Reduction Tree:
Round 0: L0   L1   L2   L3   L4   L5   L6   L7  (8 Lists)
          \ /  \ /  \ /  \ /
Round 1:  L0'   L1'  L2'  L3'                    (4 Lists)
            \   /      \   /
Round 2:    L0''        L1''                     (2 Lists)
               \       /
Round 3:        L0'''                            (1 Merged List!)
```

---

## 4. Internal Working Mechanics
Tracing Merge 3 Sorted Lists on `L1: [1, 4]`, `L2: [2, 5]`, `L3: [3, 6]`:

```
Init: minHeap = [1(L1), 2(L2), 3(L3)] | Merged: dummy

Step 1: Poll 1(L1). Append 1. L1 has next (4) -> Push 4(L1).
        minHeap = [2(L2), 3(L3), 4(L1)] | Merged: 1

Step 2: Poll 2(L2). Append 2. L2 has next (5) -> Push 5(L2).
        minHeap = [3(L3), 4(L1), 5(L2)] | Merged: 1 -> 2

Step 3: Poll 3(L3). Append 3. L3 has next (6) -> Push 6(L3).
        minHeap = [4(L1), 5(L2), 6(L3)] | Merged: 1 -> 2 -> 3

Step 4: Poll 4(L1). Append 4. L1 next is null.
        minHeap = [5(L2), 6(L3)] | Merged: 1 -> 2 -> 3 -> 4

Step 5: Poll 5(L2). Append 5. L2 next is null.
        minHeap = [6(L3)] | Merged: 1 -> 2 -> 3 -> 4 -> 5

Step 6: Poll 6(L3). Append 6. Heap Empty!

Final List: 1 -> 2 -> 3 -> 4 -> 5 -> 6 ✅ (O(N log K) Time!)
```

---

## 5. Visual Diagram
K-Way Matrix Traversal Topology (LeetCode 378):

```
Matrix (Rows Sorted Left-to-Right):
Row 0: [ 10,  20,  30 ]  ---> Initial Push: (10, r=0, c=0)
Row 1: [ 12,  25,  35 ]  ---> Initial Push: (12, r=1, c=0)
Row 2: [ 15,  28,  40 ]  ---> Initial Push: (15, r=2, c=0)

Initial Min-Heap: [ (10, r0, c0), (12, r1, c0), (15, r2, c0) ]

Poll (10, r0, c0) -> Advance to Col 1 -> Push (20, r0, c1)!
Heap becomes:     [ (12, r1, c0), (15, r2, c0), (20, r0, c1) ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Merge K Sorted Lists (LeetCode 23 - Min-Heap & Divide-and-Conquer), Kth Smallest Element in a Sorted Matrix (LeetCode 378), and Find K Pairs with Smallest Sums (LeetCode 373):

```java
import java.util.*;

public class KWayMergeMaster {

    public static class ListNode {
        public int val;
        public ListNode next;
        public ListNode(int val) { this.val = val; }
    }

    // 1. Merge k Sorted Lists using Min-Heap (LeetCode 23) O(N log K) Time, O(K) Space
    public static ListNode mergeKListsHeap(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a.val, b.val)
        );

        // Push head of each non-empty list into Min-Heap
        for (ListNode node : lists) {
            if (node != null) minHeap.offer(node);
        }

        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        while (!minHeap.isEmpty()) {
            ListNode minNode = minHeap.poll();
            curr.next = minNode;
            curr = curr.next;

            // Advance stream: Push next node from same list
            if (minNode.next != null) {
                minHeap.offer(minNode.next);
            }
        }

        return dummy.next;
    }

    // 2. Merge k Sorted Lists using Divide & Conquer O(N log K) Time, O(1) Auxiliary Space
    public static ListNode mergeKListsDivideConquer(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;
        int interval = 1;

        while (interval < lists.length) {
            for (int i = 0; i + interval < lists.length; i += interval * 2) {
                lists[i] = mergeTwoLists(lists[i], lists[i + interval]);
            }
            interval *= 2;
        }

        return lists[0];
    }

    private static ListNode mergeTwoLists(ListNode l1, ListNode l2) {
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
        curr.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }

    // 3. Kth Smallest Element in a Sorted Matrix (LeetCode 378) O(K log K) Time, O(K) Space
    public static int kthSmallestMatrix(int[][] matrix, int k) {
        int n = matrix.length;
        // PriorityQueue storing int[]{val, row, col}
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        // Push first element of each row (up to min(n, k))
        for (int r = 0; r < Math.min(n, k); r++) {
            minHeap.offer(new int[]{matrix[r][0], r, 0});
        }

        int count = 0;
        while (!minHeap.isEmpty()) {
            int[] curr = minHeap.poll();
            count++;
            if (count == k) return curr[0];

            int r = curr[1];
            int c = curr[2];

            // Advance to next column in same row
            if (c + 1 < n) {
                minHeap.offer(new int[]{matrix[r][c + 1], r, c + 1});
            }
        }

        return -1;
    }

    // 4. Find K Pairs with Smallest Sums (LeetCode 373) O(K log K) Time, O(K) Space
    public static List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums1 == null || nums2 == null || nums1.length == 0 || nums2.length == 0 || k <= 0) {
            return result;
        }

        // PriorityQueue storing int[]{i, j} where sum = nums1[i] + nums2[j]
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(nums1[a[0]] + nums2[a[1]], nums1[b[0]] + nums2[b[1]])
        );

        // Push initial pairs (nums1[i], nums2[0])
        for (int i = 0; i < Math.min(nums1.length, k); i++) {
            minHeap.offer(new int[]{i, 0});
        }

        while (!minHeap.isEmpty() && result.size() < k) {
            int[] curr = minHeap.poll();
            int i = curr[0];
            int j = curr[1];

            result.add(Arrays.asList(nums1[i], nums2[j]));

            // Advance nums2 index
            if (j + 1 < nums2.length) {
                minHeap.offer(new int[]{i, j + 1});
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// K-Way Matrix Row-to-Column Stream Advancement
int[] curr = minHeap.poll();
int r = curr[1], c = curr[2];
if (c + 1 < COLS) minHeap.offer(new int[]{matrix[r][c + 1], r, c + 1});
```

---

## 7. Concrete Problem Examples
* **LeetCode 23 - Merge k Sorted Lists**: Classic K-Way PriorityQueue merge.
* **LeetCode 378 - Kth Smallest Element in a Sorted Matrix**: Matrix row stream merge.
* **LeetCode 373 - Find K Pairs with Smallest Sums**: Array pair stream expansion.

---

## 8. Java Code Demonstration & Dry Run
Demonstration merging 3 sorted lists and finding $K$ smallest matrix element:

```java
public class KWayMergeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Merge K Sorted Lists (LeetCode 23) ===");
        KWayMergeMaster.ListNode l1 = new KWayMergeMaster.ListNode(1);
        l1.next = new KWayMergeMaster.ListNode(4);
        l1.next.next = new KWayMergeMaster.ListNode(5);

        KWayMergeMaster.ListNode l2 = new KWayMergeMaster.ListNode(1);
        l2.next = new KWayMergeMaster.ListNode(3);
        l2.next.next = new KWayMergeMaster.ListNode(4);

        KWayMergeMaster.ListNode[] lists = {l1, l2};
        KWayMergeMaster.ListNode merged = KWayMergeMaster.mergeKListsHeap(lists);

        System.out.print("Merged List: ");
        while (merged != null) {
            System.out.print(merged.val + " -> ");
            merged = merged.next;
        }
        System.out.println("null");

        System.out.println("\n=== 2. Kth Smallest Element in Sorted Matrix (LeetCode 378) ===");
        int[][] matrix = {
            {1,  5,  9},
            {10, 11, 13},
            {12, 13, 15}
        };
        System.out.println("8th Smallest Element: " + KWayMergeMaster.kthSmallestMatrix(matrix, 8)); // Output: 13
    }
}
```

---

## 9. Complexity Analysis

| K-Way Merge Strategy | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Min-Heap K-Way Merge**| **$O(N \log K)$ Time ⚡** | **$O(K)$ Space ⚡**| PriorityQueue of size $K$ |
| **Divide & Conquer Merge**| **$O(N \log K)$ Time ⚡** | **$O(1)$ Auxiliary ⚡**| Pairwise 2-pointer list merge |
| **Naive Flatten & Sort**| $O(N \log N)$ Time | $O(N)$ Space | Suboptimal memory usage |

---

## 10. Edge Cases & Boundary Handling
* **Empty Lists Array (`lists == null || lists.length == 0`)**: Return `null` immediately.
* **Array Containing Null Heads (`lists = [null, null]`)**: `minHeap` remains empty, returns `null` cleanly without NPE.
* **Matrix $K > N^2$**: Returns invalid or bounded result based on constraint validation.

---

## 11. Common Mistakes & Anti-Patterns
* **Loading ALL $N$ Elements into Priority Queue At Once**:
  - `for (ListNode head : lists) while (head != null) minHeap.offer(head);`
  - Consumes $O(N)$ space and $O(N \log N)$ time, defeating the entire purpose of K-Way Merge!
  - **Always load ONLY 1 element per active stream** into a Min-Heap of size $K$.
* **Null Pointer Exception on Node Advancement**: Accessing `minNode.next.val` when `minNode.next == null`. Always check `if (minNode.next != null)`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Min-Heap K-Way Merge vs Divide & Conquer Choice:
> * **Min-Heap ($O(N \log K)$ time, $O(K)$ space)**: Best for data streams or non-linked-list structures (e.g. matrix rows, file streams).
> * **Divide & Conquer ($O(N \log K)$ time, $O(1)$ space)**: Best for in-memory Singly Linked Lists because it requires zero heap pointer allocation!

> **Memory Trick:** **"Min-Heap holds K stream heads! Poll min -> Push next node from SAME stream!"**

---

## 13. System & Implementation Comparisons

| Feature | Min-Heap K-Way Merge | Divide & Conquer Pairwise |
| :--- | :--- | :--- |
| **Stream Suitability** | **File / Network Streams ⚡** | Linked Lists Only |
| **Time Complexity** | $O(N \log K)$ | $O(N \log K)$ |
| **Auxiliary Memory** | $O(K)$ PriorityQueue | **$O(1)$ Strict In-Place ⚡** |

---

## 14. How to Recognize This in Questions
* **"Merge K sorted linked lists into one sorted list"** $\rightarrow$ LeetCode 23 (Min-Heap of size $K$ or Divide & Conquer).
* **"Find K-th smallest element in an N x N sorted matrix"** $\rightarrow$ LeetCode 378 (Min-Heap row stream advancement).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Min-Heap K-Way Merge execute in $O(N \log K)$ time instead of $O(N \log N)$ time?**  
  *A:* Because the Min-Heap size never exceeds $K$. Pushing and polling from a heap of size $K$ takes $O(\log K)$ time. Executing $N$ total insertions and extractions takes $N \times O(\log K) = \mathbf{O(N \log K)\text{ Time}}$.
* **Q: How does LeetCode 373 (Find K Pairs with Smallest Sums) prevent duplicate pair insertions?**  
  *A:* By initializing the heap with `(i, 0)` for $i \in [0 \dots \min(N1, K)-1]$ and ONLY advancing the second index `(i, j + 1)` upon polling `(i, j)`. This guarantees every unique index pair $(i, j)$ is visited exactly once!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: K-WAY MERGE PATTERN & MATRIX SELECTION                |
+-----------------------------------------------------------------------+
| • K-Way Merge Heap Invariant: Min-Heap of size K storing stream heads |
| • Stream Advancement Rule: When minNode is polled, push minNode.next  |
| • Divide & Conquer Alternative: Pairwise 2-pointer merge in O(1) space|
| • Matrix Search (378): Push matrix[r][0]; when (r,c) polled, push (r, c+1)|
| • Memory Advantage: Keeps only 1 candidate per stream in memory       |
| • Complexity: O(N log K) Time | O(K) Heap Auxiliary Memory            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Merge K Sorted Lists (LeetCode 23) using a Min-Heap of size $K$.
- [ ] I can write Merge K Sorted Lists using Divide & Conquer in $O(1)$ space.
- [ ] I can solve Kth Smallest Element in a Sorted Matrix (LeetCode 378).
- [ ] I can solve Find K Pairs with Smallest Sums (LeetCode 373).
- [ ] I know why K-Way Merge takes $O(N \log K)$ time instead of $O(N \log N)$.
