# 07. K-Way Merge Pattern & Priority Queue Processing

## 1. Introduction
The **$K$-Way Merge Pattern** is a foundational algorithmic technique used to combine $K$ sorted data streams (arrays, linked lists, or files) into a single unified sorted sequence. In technical coding interviews, problems such as Merge $K$ Sorted Lists (LeetCode 23), Find K Pairs with Smallest Sums (LeetCode 373), Smallest Range Covering Elements from K Lists (LeetCode 632), and Kth Smallest Element in a Sorted Matrix (LeetCode 378) leverage a **Min-Heap Priority Queue** of size $K$ to achieve **$O(N \log K)$ time complexity**, where $N$ is the total number of elements across all $K$ streams.

> **Important:** The key advantage of $K$-Way Merge with a Min-Heap is that the heap size is strictly bounded by $K$ (the number of streams), guaranteeing that each insertion and deletion takes **$O(\log K)$ time** rather than $O(\log N)$!

## 2. Core Concepts
* **Min-Heap Stream Pointer Tuple**: The Min-Heap stores a tuple/array representing `[value, streamIndex, elementIndex]`.
* **Initialization Phase**: Push the 1st element of each of the $K$ streams into the Min-Heap ($O(K \log K)$ time).
* **Extraction & Advance Loop**:
  1. Extract the minimum element `[val, i, j]` from the Min-Heap (`pq.poll()`).
  2. Append `val` to the result list.
  3. If stream $i$ has a next element at index $j + 1$, push `[stream[i][j+1], i, j+1]` into the Min-Heap (`pq.offer(...)`).
* **Matrix Traversal Variant**: Treating rows of an $N \times N$ sorted matrix as $K = N$ sorted streams.

> **Memory Trick:** **"Push head of all K streams into Min-Heap! Extract min, advance that stream's pointer, repeat!"**

## 3. Characteristics / Properties
* **Bounded Auxiliary Memory**: Auxiliary heap memory is strictly $O(K)$, independent of the total number of elements $N$.
* **External Merge Sort Foundation**: $K$-Way Merge powers multi-terabyte external sorting engines (e.g. MapReduce, PostgreSQL disk merges, LSM-Tree compaction in RocksDB).

```
K-Way Merge Applications Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Application | Stream Data Type  | Heap Element Tuple| Target Complexity |
+-----------------------+-------------------+-------------------+-------------------+
| Merge K Sorted Lists  | ListNode References| `ListNode`       | O(N log K) Time ⚡|
| Find K Smallest Sums  | 2 Sorted Arrays   | `[val, i, j]`     | O(K log K) Time ⚡|
| Smallest Range (632)  | K Sorted Arrays   | `[val, i, j]`     | O(N log K) Time ⚡|
| Sorted Matrix K-th    | N Matrix Rows     | `[val, r, c]`     | O(K log N) Time ⚡|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Find $K$ Pairs with Smallest Sums (LeetCode 373) on `nums1 = [1, 7, 11], nums2 = [2, 4, 6], K = 3`:

```
Init Heap: Store [nums1[i] + nums2[0], i, 0] for all i in nums1 up to K:
Heap contains: [ (1+2=3, i=0, j=0), (7+2=9, i=1, j=0), (11+2=13, i=2, j=0) ]

Iter 1: Poll min (3, i=0, j=0) -> Add pair [1, 2] to result.
        Advance stream 0 to j=1: Push (nums1[0] + nums2[1] = 1+4=5, i=0, j=1).
        Heap: [ (5, i=0, j=1), (9, i=1, j=0), (13, i=2, j=0) ]

Iter 2: Poll min (5, i=0, j=1) -> Add pair [1, 4] to result.
        Advance stream 0 to j=2: Push (nums1[0] + nums2[2] = 1+6=7, i=0, j=2).
        Heap: [ (7, i=0, j=2), (9, i=1, j=0), (13, i=2, j=0) ]

Iter 3: Poll min (7, i=0, j=2) -> Add pair [1, 6] to result. Target K=3 reached!

Final Pairs Result: [[1, 2], [1, 4], [1, 6]] ✅ (O(K log K) Time!)
```

## 5. Visual Diagram
Min-Heap Stream Extraction & Pointer Advance Mechanics:

```
Stream 0: [ 1 ] ---> [ 4 ] ---> [ 5 ]
Stream 1: [ 1 ] ---> [ 3 ] ---> [ 4 ]
Stream 2: [ 2 ] ---> [ 6 ] ---> [ 10 ]

          [ MIN-HEAP (Size K = 3) ]
          Root: [ 1 (Stream 0) ]
         /                      \
  [ 1 (Stream 1) ]       [ 2 (Stream 2) ]

Step 1: Poll Root (1 from Stream 0).
Step 2: Advance Stream 0 -> Push 4 into Heap.
Step 3: Heap re-balances in O(log K) time!
```

## 6. Operations / Algorithms
LeetCode 373 & LeetCode 632 Master Implementation:

```java
// 1. Find K Pairs with Smallest Sums (LeetCode 373) O(K log K) Time, O(K) Space
public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
    List<List<Integer>> result = new ArrayList<>();
    if (nums1 == null || nums2 == null || nums1.length == 0 || nums2.length == 0 || k <= 0) {
        return result;
    }

    // Min-Heap storing int[]{sum, i, j}
    PriorityQueue<int[]> minHeap = new PriorityQueue<>(
        (a, b) -> Integer.compare(a[0], b[0])
    );

    // Push initial pairs (nums1[i], nums2[0]) up to K elements
    for (int i = 0; i < Math.min(nums1.length, k); i++) {
        minHeap.offer(new int[]{nums1[i] + nums2[0], i, 0});
    }

    while (!minHeap.isEmpty() && result.size() < k) {
        int[] curr = minHeap.poll();
        int i = curr[1];
        int j = curr[2];

        result.add(Arrays.asList(nums1[i], nums2[j]));

        // If next element exists in nums2 for stream i, push to heap
        if (j + 1 < nums2.length) {
            minHeap.offer(new int[]{nums1[i] + nums2[j + 1], i, j + 1});
        }
    }

    return result;
}
```

> **Quick Syntax:**
```java
// Min-Heap Tuple Comparator
PriorityQueue<int[]> minHeap = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[0], b[0])
);
```

## 7. Examples
* **LeetCode 23 - Merge K Sorted Lists**: $K$-Way Merge on singly linked list streams.
* **LeetCode 373 - Find K Pairs with Smallest Sums**: Matrix implicit stream $K$-Way Merge.
* **LeetCode 632 - Smallest Range Covering Elements from K Lists**: Priority Queue tracking current min & max.

## 8. Java Code
Complete interview-ready Java suite implementing Find K Pairs with Smallest Sums (LeetCode 373) and Smallest Range Covering K Lists (LeetCode 632):

```java
import java.util.*;

public class KWayMergeMaster {

    // 1. Find K Pairs with Smallest Sums (LeetCode 373) O(K log K) Time, O(K) Space
    public static List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums1.length == 0 || nums2.length == 0 || k <= 0) return result;

        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        for (int i = 0; i < Math.min(nums1.length, k); i++) {
            minHeap.offer(new int[]{nums1[i] + nums2[0], i, 0});
        }

        while (!minHeap.isEmpty() && result.size() < k) {
            int[] curr = minHeap.poll();
            int i = curr[1], j = curr[2];

            result.add(Arrays.asList(nums1[i], nums2[j]));

            if (j + 1 < nums2.length) {
                minHeap.offer(new int[]{nums1[i] + nums2[j + 1], i, j + 1});
            }
        }

        return result;
    }

    // 2. Smallest Range Covering Elements from K Lists (LeetCode 632) O(N log K) Time, O(K) Space
    public static int[] smallestRange(List<List<Integer>> nums) {
        int k = nums.size();
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[0], b[0])
        );

        int currentMax = Integer.MIN_VALUE;
        for (int i = 0; i < k; i++) {
            int val = nums.get(i).get(0);
            minHeap.offer(new int[]{val, i, 0});
            currentMax = Math.max(currentMax, val);
        }

        int rangeStart = 0, rangeEnd = Integer.MAX_VALUE;

        while (minHeap.size() == k) {
            int[] curr = minHeap.poll();
            int currentMin = curr[0];
            int i = curr[1], j = curr[2];

            // Update smallest range if narrower range found
            if (currentMax - currentMin < rangeEnd - rangeStart) {
                rangeStart = currentMin;
                rangeEnd = currentMax;
            }

            // Advance stream i
            if (j + 1 < nums.get(i).size()) {
                int nextVal = nums.get(i).get(j + 1);
                minHeap.offer(new int[]{nextVal, i, j + 1});
                currentMax = Math.max(currentMax, nextVal);
            }
        }

        return new int[]{rangeStart, rangeEnd};
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] n1 = {1, 7, 11}, n2 = {2, 4, 6};
        System.out.println("K Smallest Pairs (K=3): " + kSmallestPairs(n1, n2, 3));
        // Output: [[1, 2], [1, 4], [1, 6]]

        List<List<Integer>> lists = Arrays.asList(
            Arrays.asList(4, 10, 15, 24, 26),
            Arrays.asList(0, 9, 12, 20),
            Arrays.asList(5, 18, 22, 30)
        );
        System.out.println("Smallest Range: " + Arrays.toString(smallestRange(lists)));
        // Output: [20, 24]
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Find K Smallest Sums** | **$O(K \log K)$** | **$O(K)$ Space** | Bounded initial loop $\min(N, K)$ |
| **Smallest Range (632)** | **$O(N \log K)$** | **$O(K)$ Space** | Heap size fixed at $K$ |
| **Merge K Lists (23)** | **$O(N \log K)$** | **$O(K)$ Space** | List head priority queue |

## 10. Edge Cases
* **Empty Streams**: Check `nums1.length == 0 || nums2.length == 0` before populating heap.
* **$K$ Greater than Total Elements**: Loops terminate when heap becomes empty without throwing exceptions.
* **Duplicates in Streams**: Priority Queue preserves equal element sums smoothly.

## 11. Common Mistakes
* Pushing all $N \times M$ pairs into PriorityQueue (ruins time complexity to $O(N \cdot M \log(N \cdot M))$!). Initializing heap with only $\min(N, K)$ elements keeps heap size $\le K$.
* Forgetting to update `currentMax` when inserting the next stream element in Smallest Range (LeetCode 632).
* Using `a[0] - b[0]` in comparator instead of `Integer.compare(a[0], b[0])`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Initializing $K$-Way Merge Heap Bounded Size:
> For Find $K$ Pairs with Smallest Sums:
> Initialize heap ONLY with `(nums1[i] + nums2[0], i, 0)` for `i` from $0$ to $\min(N_1, K)$.
> As each pair `(i, j)` is popped, push `(i, j + 1)`.
> This guarantees heap size NEVER exceeds $K$, bounding time complexity to **$O(K \log K)$**!

> **Memory Trick:** **"Only push 1st element of each stream! Advance stream pointer j -> j+1 on poll!"**

## 13. Comparisons
| Feature | All Pairs Heap Push | K-Way Stream Advance Heap |
| :--- | :--- | :--- |
| **Heap Insertion Count** | All $N \times M$ pairs | **At most $K$ elements** |
| **Time Complexity** | $O(N \cdot M \log(N \cdot M))$ | **$O(K \log K)$ ⚡** |
| **Auxiliary Space** | $O(N \cdot M)$ | **$O(K)$ ⚡** |
| **Interview Recommendation** | Failure / TLE | **OPTIMAL EXPECTED** |

## 14. How to Recognize This in Questions
* **"Find K pairs with smallest sums from 2 sorted arrays"** $\rightarrow$ $K$-Way Merge ($O(K \log K)$).
* **"Find smallest range covering at least 1 element from K sorted lists"** $\rightarrow$ Min-Heap + Range tracking.

## 15. Frequently Asked Interview Questions
* **Q: Why does $K$-Way Merge take $O(N \log K)$ time instead of $O(N \log N)$?**  
  *A:* Because the Min-Heap contains at most $K$ elements (one active head per stream). Each of the $N$ total elements is offered and polled from the heap at most once. Each heap operation takes $O(\log K)$ time $\implies O(N \log K)$ total time.
* **Q: How does Smallest Range (LeetCode 632) track the active window range?**  
  *A:* The Min-Heap top (`minHeap.peek()`) ALWAYS holds the minimum element among the active heads, while a running variable `currentMax` tracks the maximum element. The current range span is `currentMax - currentMin`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: K-WAY MERGE PATTERN                                   |
+-----------------------------------------------------------------------+
| • Heap Tuple: int[]{value/sum, streamIdx i, elementIdx j}             |
| • Heap Size Limit: Bounded to K (number of streams)                   |
| • Loop Step: Poll min [val, i, j], process, offer [stream[i][j+1], i, j+1]|
| • Smallest Range Rule: Track min via minHeap.peek(), max via currentMax|
| • Comparator Rule: Use (a, b) -> Integer.compare(a[0], b[0])          |
| • Complexity: O(N log K) Time | O(K) Auxiliary Heap Space             |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the bounded $K$-element heap initialization loop.
- [ ] I know why $K$-Way Merge runs in $O(N \log K)$ time instead of $O(N \log N)$.
- [ ] I can implement Find K Smallest Pairs (LeetCode 373) in $O(K \log K)$ time.
- [ ] I can implement Smallest Range Covering K Lists (LeetCode 632).
- [ ] I know how to track `currentMax` alongside `minHeap.poll()`.
