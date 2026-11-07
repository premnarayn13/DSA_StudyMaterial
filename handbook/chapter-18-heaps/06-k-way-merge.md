# 06. K-Way Merge Pattern, Heap-Based Pointer Interleaving & Matrix Traversals

## 1. Introduction
The **K-Way Merge Pattern** combines $K$ sorted streams (such as arrays, linked lists, or matrix rows) into a single sorted stream. By maintaining a **Min-Heap of size $K$** containing the current head element of each sorted sequence, the K-Way Merge pattern extracts the overall minimum element and advances the corresponding sequence pointer in **$O(N \log K)$ Total Time and $O(K)$ Auxiliary Space** (where $N$ is total elements across all $K$ streams).

> **Important:** Why does K-Way Merge use a Min-Heap of size $K$?
> * At any instant, the next smallest element in the merged sequence MUST be among the current heads of the $K$ sorted streams.
> * Pushing 1 element from each of the $K$ streams into a Min-Heap places the overall smallest candidate at `minHeap.peek()` in **$O(1)$ time**.
> * Polling `curr = minHeap.poll()` appends `curr` to result and advances `curr.next` into the heap in **$O(\log K)$ time**! ⚡

```
K-Way Merge Heap State Topology (Merging 3 Lists):
List 1: [ 1, 4, 5 ] ---> Head Node 1
List 2: [ 1, 3, 4 ] ---> Head Node 1
List 3: [ 2, 6 ]    ---> Head Node 2

Min-Heap (Size K=3): [ Node(1, L1), Node(1, L2), Node(2, L3) ]
Poll Node(1, L1) -> Append 1 -> Offer List 1 Next (4) -> Heap: [ Node(1, L2), Node(2, L3), Node(4, L1) ] ⚡
```

---

## 2. Core Concepts & K-Way Merge Tuple Structure

### 2.1 The Pointer Tuple Architecture
When merging matrix rows or arrays, heap elements store coordinate tuples:
* **Array / Matrix Element Tuple**: `(value, rowIndex, colIndex)`.
* **Linked List Node**: Directly uses `ListNode` pointers (`(node.val, node)`).

```
K-Way Merge Operational Sequence:
1. Insert head of all K sorted sequences into Min-Heap (Heap size = K).
2. While `!minHeap.isEmpty()`:
   - `curr = minHeap.poll()`.
   - Add `curr.val` to output.
   - If `curr` has a next element in its sequence, `minHeap.offer(nextElement)`.
Total Comparisons = O(N log K)! ⚡
```

> **Memory Trick:** **"K-Way Merge: Load 1 head element from each of the K streams into a Min-Heap! Poll min, offer next from same stream!"**

---

## 3. Characteristics & Sorted Matrix Searching (LeetCode 378)

### 3.1 Kth Smallest Element in a Sorted Matrix (LeetCode 378)
Given an $N \times N$ matrix where each row and column is sorted in ascending order, find the $K$-th smallest element:
* **K-Way Merge Strategy ($O(K \log N)$ Time, $O(N)$ Space)**:
  - Offer `(matrix[r][0], r, 0)` for all $N$ rows into a Min-Heap.
  - Poll $K - 1$ times. On each poll `(val, r, c)`: if `c + 1 < N`, offer `(matrix[r][c+1], r, c+1)`.
  - The $K$-th polled element is the exact $K$-th smallest item!

---

## 4. Internal Working Mechanics
Tracing Merge k Sorted Lists (LeetCode 23) on `lists = [[1,4,5], [1,3,4], [2,6]]`:

```
Init: Offer head nodes -> Min-Heap: [1(L1), 1(L2), 2(L3)]. Output: []

Step 1: Poll 1(L1). Append 1. Offer 4(L1) -> Heap: [1(L2), 2(L3), 4(L1)]. Output: [1]
Step 2: Poll 1(L2). Append 1. Offer 3(L2) -> Heap: [2(L3), 3(L2), 4(L1)]. Output: [1, 1]
Step 3: Poll 2(L3). Append 2. Offer 6(L3) -> Heap: [3(L2), 4(L1), 6(L3)]. Output: [1, 1, 2]
Step 4: Poll 3(L2). Append 3. Offer 4(L2) -> Heap: [4(L1), 4(L2), 6(L3)]. Output: [1, 1, 2, 3]

Output sequence constructed flawlessly in O(N log K) Time! ✅
```

---

## 5. Visual Diagram
Min-Heap Interleaving Pointer Topography:

```
Stream 0: (1) ---> 4 ---> 5
            |
Stream 1: (1) ---> 3 ---> 4     Min-Heap (Size K=3) ---> [ (1), (1), (2) ]
            |                                                   |
Stream 2: (2) ---> 6                                      Poll Min (1)
                                                          Advance Stream 0 to 4! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Merge k Sorted Lists (LeetCode 23), Kth Smallest Element in Sorted Matrix (LeetCode 378), and Find K Pairs with Smallest Sums (LeetCode 373):

```java
import java.util.*;

public class KWayMergeMaster {

    public static class ListNode {
        public int val;
        public ListNode next;

        public ListNode(int val) {
            this.val = val;
        }

        public ListNode(int val, ListNode next) {
            this.val = val;
            this.next = next;
        }
    }

    // 1. Merge k Sorted Lists (LeetCode 23) O(N log K) Time, O(K) Space
    public static ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;

        // Min-Heap ordered by ListNode value
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
            lists.length, (a, b) -> Integer.compare(a.val, b.val)
        );

        // Step 1: Offer head node of each non-null list
        for (ListNode node : lists) {
            if (node != null) {
                minHeap.offer(node);
            }
        }

        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;

        // Step 2: Interleave nodes using Min-Heap
        while (!minHeap.isEmpty()) {
            ListNode minNode = minHeap.poll();
            curr.next = minNode;
            curr = curr.next;

            if (minNode.next != null) {
                minHeap.offer(minNode.next); // Advance list pointer
            }
        }

        return dummy.next;
    }

    // 2. Kth Smallest Element in a Sorted Matrix (LeetCode 378) O(K log N) Time
    public static int kthSmallestMatrix(int[][] matrix, int k) {
        int n = matrix.length;
        // Heap element tuple: [val, row, col]
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            n, (a, b) -> Integer.compare(a[0], b[0])
        );

        // Offer first element of each row
        for (int r = 0; r < Math.min(n, k); r++) {
            minHeap.offer(new int[]{matrix[r][0], r, 0});
        }

        int count = 0;
        int result = 0;

        while (!minHeap.isEmpty()) {
            int[] curr = minHeap.poll();
            result = curr[0];
            count++;

            if (count == k) return result;

            int r = curr[1];
            int c = curr[2];

            if (c + 1 < n) {
                minHeap.offer(new int[]{matrix[r][c + 1], r, c + 1});
            }
        }

        return result;
    }

    // 3. Find K Pairs with Smallest Sums (LeetCode 373) O(K log K) Time
    public static List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums1 == null || nums2 == null || nums1.length == 0 || nums2.length == 0 || k <= 0) {
            return result;
        }

        // Tuple: [sum, i, j] (i = nums1 index, j = nums2 index)
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        // Offer initial pairs (nums1[i], nums2[0])
        for (int i = 0; i < Math.min(nums1.length, k); i++) {
            minHeap.offer(new int[]{nums1[i] + nums2[0], i, 0});
        }

        while (!minHeap.isEmpty() && result.size() < k) {
            int[] curr = minHeap.poll();
            int i = curr[1];
            int j = curr[2];

            result.add(Arrays.asList(nums1[i], nums2[j]));

            if (j + 1 < nums2.length) {
                minHeap.offer(new int[]{nums1[i] + nums2[j + 1], i, j + 1});
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// K-Way Merge Heap Loop
ListNode minNode = minHeap.poll();
curr.next = minNode;
if (minNode.next != null) minHeap.offer(minNode.next);
```

---

## 7. Concrete Problem Examples
* **LeetCode 23 - Merge k Sorted Lists**: Core K-Way Heap Merge.
* **LeetCode 378 - Kth Smallest Element in a Sorted Matrix**: Matrix row interleaving.
* **LeetCode 373 - Find K Pairs with Smallest Sums**: Dual array pair interleaving.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Merge K Sorted Lists and K Smallest Pairs:

```java
public class KWayMergeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Merge k Sorted Lists (LeetCode 23) ===");
        KWayMergeMaster.ListNode l1 = new KWayMergeMaster.ListNode(1, 
            new KWayMergeMaster.ListNode(4, new KWayMergeMaster.ListNode(5)));
        KWayMergeMaster.ListNode l2 = new KWayMergeMaster.ListNode(1, 
            new KWayMergeMaster.ListNode(3, new KWayMergeMaster.ListNode(4)));
        KWayMergeMaster.ListNode l3 = new KWayMergeMaster.ListNode(2, 
            new KWayMergeMaster.ListNode(6));

        KWayMergeMaster.ListNode[] lists = {l1, l2, l3};
        KWayMergeMaster.ListNode merged = KWayMergeMaster.mergeKLists(lists);

        System.out.print("Merged List: ");
        while (merged != null) {
            System.out.print(merged.val + (merged.next != null ? " -> " : ""));
            merged = merged.next;
        }
        System.out.println(); // Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6 ✅

        System.out.println("\n=== 2. K Pairs with Smallest Sums (LeetCode 373) ===");
        int[] nums1 = {1, 7, 11};
        int[] nums2 = {2, 4, 6};
        List<List<Integer>> pairs = KWayMergeMaster.kSmallestPairs(nums1, nums2, 3);
        System.out.println("Top 3 Smallest Pairs: " + pairs);
        // Output: [[1, 2], [1, 4], [1, 6]] ✅
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Strategy | Time Complexity | Auxiliary Space | Key Optimization |
| :--- | :--- | :--- | :--- |
| **Naive Concatenate & Sort**| $O(N \log N)$ | $O(N)$ Space | Ignores existing sorted order |
| **Divide-and-Conquer Merge**| **$O(N \log K)$ ⚡** | $O(\log K)$ Call Stack| Pairwise list merging |
| **Heap-Based K-Way Merge**  | **$O(N \log K)$ ⚡** | **$O(K)$ Heap Space ⚡**| Heap size strictly $K$ |

---

## 10. Edge Cases & Boundary Handling
* **Empty Lists Array (`lists = []`)**: Returns `null` immediately.
* **Lists Containing `null` Head Nodes**: Skipped during initial heap population loop `if (node != null)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Offering Null Nodes Into `minHeap`**:
  - Adding `null` to Java `PriorityQueue` throws `NullPointerException`.
  - **Always check `if (node.next != null)` before offering `node.next`**.
* **Offering All Matrix Elements into Heap ($O(N^2 \log N^2)$ Penalty)**:
  - Loading all $N^2$ elements of a matrix into the heap at once wastes memory.
  - **Offer only the first column ($N$ items) and advance rightward lazily**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why K-Way Heap Merge runs in $O(N \log K)$ Time:
> Let $N$ be the total number of elements across all $K$ streams.
> 1. Initial Heap Creation: Takes $O(K)$ time.
> 2. Every element of the $N$ total items is polled once and inserted once into a Min-Heap of size $K$.
> 3. Each poll/offer step takes $O(\log K)$ time.
> Total Execution Time = $\mathbf{O(N \log K)}$!

> **Memory Trick:** **"K-Way Merge takes O(N log K) time because heap size never exceeds K!"**

---

## 13. System & Implementation Comparisons

| Feature | Heap-Based K-Way Merge | Divide-and-Conquer Pairwise Merge |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \log K)$ ⚡** | **$O(N \log K)$ ⚡** |
| **Auxiliary Memory** | $O(K)$ Heap Space | **$O(\log K)$ Call Stack Space ⚡**|
| **Streaming Inputs** | **100% Streaming Compatible ⚡**| Requires Static Lists Upfront |

---

## 14. How to Recognize This in Questions
* **"Merge K sorted linked lists or arrays into one sorted list"** $\rightarrow$ LeetCode 23 (Min-Heap size $K$).
* **"Find K-th smallest element in an N x N sorted matrix"** $\rightarrow$ LeetCode 378 (Matrix row heap interleaving).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `kSmallestPairs` (LeetCode 373) avoid duplicate pair insertions?**  
  *A:* By initializing the heap with `(nums1[i], nums2[0])` for all $i$, and ONLY offering `(nums1[i], nums2[j+1])` when polling `(nums1[i], nums2[j])`. This guarantees every pair $(i, j)$ is visited along a unique rightward path without duplicates.
* **Q: Can Binary Search solve LeetCode 378 in $O(N \log(\text{max} - \text{min}))$ time?**  
  *A:* Yes! Binary searching the value range `[matrix[0][0] ... matrix[N-1][N-1]]` and counting elements $\le \text{mid}$ in $O(N)$ time per step solves the problem in $O(N \log(\text{Range}))$ time.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: K-WAY MERGE PATTERN                                   |
+-----------------------------------------------------------------------+
| • Core Rule : Min-Heap stores 1 head element from each of the K streams|
| • Heap Size : Capped at size K -> O(N log K) Time | O(K) Space ⚡      |
| • Poll Rule : minNode = heap.poll(); if (minNode.next != null) offer; |
| • Matrix    : Offer first column (matrix[r][0]); advance (r, c+1)    |
| • NPE Guard : ALWAYS check for null before offering next stream node! |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Merge k Sorted Lists (LeetCode 23) in $O(N \log K)$ time.
- [ ] I can write Kth Smallest Element in Sorted Matrix (LeetCode 378).
- [ ] I can write Find K Pairs with Smallest Sums (LeetCode 373).
- [ ] I know why heap size is strictly bounded by $K$.
- [ ] I know how to prevent `NullPointerException` during stream pointer advancements.
