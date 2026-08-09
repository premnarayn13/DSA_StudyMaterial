# 11. Search Applications: Industrial Indexing, Stream Searching & System Integration

## 1. Introduction
**Searching Applications** bridge mathematical searching algorithms with production-grade software engineering systems. Real-world applications—such as **Database B+ Tree Indexing**, **Distributed Log Searching**, **Rate Limiter Threshold Optimization**, **Stream Median Location**, and **Resource Capacity Allocators**—depend on searching invariants to query millions of records per second with low latency. Understanding how binary search on answer, lower/upper bounds, and self-organizing heuristics integrate into real-world architectures equips developers to design high-throughput system engines in Java.

> **Important:** Core Industrial Search System Invariants:
> 1. **B+ Tree Block Indexing**: Database indexes group keys into contiguous disk blocks of size $B$ ($\approx 4\text{KB} - 64\text{KB}$). Binary search locates the target block in $O(\log_B N)$ disk I/O steps.
> 2. **Distributed Log Stream Search**: Log lines are appended sequentially with monotonic timestamps. Exponential search + Binary Search locates target log entries by timestamp in $O(\log \text{Pos})$ time without loading full logs into memory.
> 3. **Stream Median Locator (Dual Priority Queue)**: Manages dynamic data streams by maintaining a Max-Heap for the lower half and a Min-Heap for the upper half, allowing $O(1)$ median lookups and $O(\log N)$ insertions. ⚡

```
Database B+ Tree Index Search Architecture:
Root Index Node:        [  100  |  500  |  900  ]
                          /        |        \
Child Index Nodes:   [10..99]  [100..499]  [500..899]
                         |          |          |
Leaf Data Blocks:    [Block 1]  [Block 2]  [Block 3] (Contiguous Disk Range Search!) ⚡
```

---

## 2. Core Concepts & System Search Architecture Matrix

### 2.1 Industrial System Search Matrix
```
Industrial System Search Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| System Application    | Searching Paradigm| Primary Invariant | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Database Indexing** | B+ Tree Binary    | Monotonic Disk Block| **$O(\log_B N)$ Disk I/O ⚡**|
| **Log Stream Search** | Exponential + BS  | Monotonic Timestamp| **$O(\log \text{Pos})$ Log ⚡**|
| **Stream Median**     | Dual Heap Balancing| Equal Heap Sizes | **$O(1)$ Median / $O(\log N)$ Add**|
| **Rate Limiter**      | Upper Bound Window| Sliding Window Sum| **$O(\log N)$ Bound ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"B+ Tree = Disk Block BS O(log_B N); Stream Median = Dual Heap O(1) Lookup!"**

---

## 3. Characteristics & Dual Heap Stream Median Proof

### 3.1 Mathematical Proof of Dual Heap Stream Median $O(1)$ Lookup
* Maintain two priority queues:
  - `maxHeap` (lower half of elements, max element on top).
  - `minHeap` (upper half of elements, min element on top).
* Balance Condition: $\text{size}(\text{maxHeap}) = \text{size}(\text{minHeap})$ or $\text{size}(\text{maxHeap}) = \text{size}(\text{minHeap}) + 1$.
* If combined count $N$ is odd, median $= \text{maxHeap.peek()}$.
* If combined count $N$ is even, median $= \frac{\text{maxHeap.peek()} + \text{minHeap.peek()}}{2.0}$.
* Median Lookup Time: $\mathbf{O(1) \text{ Constant Time}}$. Insertion Time: $\mathbf{O(\log N) \text{ Time}}$. ⚡

---

## 4. Internal Working Mechanics: B+ Tree Block Index Binary Search

Tracing Database B+ Tree Block Index Search for `Key = 350`:

```
Root Node Range: [100, 500, 900]

Step 1: Perform Upper Bound Binary Search on Root Node keys [100, 500, 900] for Key = 350.
        Upper Bound Index = 1 (val 500 > 350).
        Follow Pointer at index 1 -> Directs to Child Node [100 ... 499].

Step 2: Read Child Node Disk Block into L1 Cache.
        Perform Binary Search on Child Node keys [100, 250, 350, 450].
        Match Found at Index 2!

Disk I/O Reads Required: EXACTLY 2 BLOCK READS for 1,000,000 Records! ✅ (O(log_B N) Time!)
```

---

## 5. Visual Diagram: Dual Heap Stream Median Architecture

```
Stream Median Dual Heap Balancing Topology:

Incoming Numbers: [ 5, 15, 1, 3, 2, 8, 7, 9 ]

         Lower Half (Max-Heap)              Upper Half (Min-Heap)
         Max on top: [ 3 ]                  Min on top: [ 7 ]
                     /   \                              /   \
                   [ 2 ] [ 1 ]                        [ 8 ] [ 9 ] [ 15 ]

Median (Even Count): (MaxHeap.peek() + MinHeap.peek()) / 2.0 = (3 + 7) / 2.0 = 5.0! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing a Stream Median Finder (LeetCode 295), a B+ Tree Block Index Simulator, and a Sliding Window Timestamp Rate Limiter.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Real-World System Search Applications:
 * Stream Median Finding (LeetCode 295), B+ Tree Block Search, and Rate Limiter Window Search.
 */
public class SearchApplicationsMaster {

    // =========================================================================
    // 1. STREAM MEDIAN FINDER (LeetCode 295 Dual Heap O(1) Median Lookup)
    // =========================================================================
    public static class MedianFinder {
        private final PriorityQueue<Integer> maxHeap; // Lower half
        private final PriorityQueue<Integer> minHeap; // Upper half

        public MedianFinder() {
            // maxHeap stores smaller half, max element on top
            this.maxHeap = new PriorityQueue<>(Collections.reverseOrder());
            // minHeap stores larger half, min element on top
            this.minHeap = new PriorityQueue<>();
        }

        /**
         * Adds a number to the data stream in O(log N) time.
         */
        public void addNum(int num) {
            if (maxHeap.isEmpty() || num <= maxHeap.peek()) {
                maxHeap.add(num);
            } else {
                minHeap.add(num);
            }

            // Rebalance heaps to enforce size invariant: size(maxHeap) == size(minHeap) (+1)
            if (maxHeap.size() > minHeap.size() + 1) {
                minHeap.add(maxHeap.poll());
            } else if (minHeap.size() > maxHeap.size()) {
                maxHeap.add(minHeap.poll());
            }
        }

        /**
         * Returns median of stream in O(1) time.
         */
        public double findMedian() {
            if (maxHeap.isEmpty()) return 0.0;

            if (maxHeap.size() > minHeap.size()) {
                return maxHeap.peek();
            } else {
                return (maxHeap.peek() + minHeap.peek()) / 2.0;
            }
        }
    }

    // =========================================================================
    // 2. B+ TREE BLOCK INDEX SEARCH SIMULATOR (O(log_B N) Disk I/O)
    // =========================================================================
    public static class BTreeBlockNode {
        public List<Integer> keys;
        public List<BTreeBlockNode> children;
        public boolean isLeaf;

        public BTreeBlockNode(boolean isLeaf) {
            this.keys = new ArrayList<>();
            this.children = new ArrayList<>();
            this.isLeaf = isLeaf;
        }
    }

    /**
     * Searches target key in B+ Tree block index structure.
     */
    public boolean searchBTree(BTreeBlockNode root, int target) {
        if (root == null) return false;

        BTreeBlockNode curr = root;

        while (curr != null) {
            // Perform Binary Search (Upper Bound) on current node keys
            int idx = upperBound(curr.keys, target);

            if (curr.isLeaf) {
                // Leaf node: Check exact match
                return idx > 0 && curr.keys.get(idx - 1) == target;
            }

            // Non-leaf node: Navigate to child block
            curr = curr.children.get(idx);
        }

        return false;
    }

    private int upperBound(List<Integer> keys, int target) {
        int low = 0, high = keys.size();
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (keys.get(mid) > target) high = mid;
            else low = mid + 1;
        }
        return low;
    }

    // =========================================================================
    // 3. SLIDING WINDOW TIMESTAMP RATE LIMITER (Upper Bound Window Search)
    // =========================================================================
    public static class TimestampRateLimiter {
        private final List<Long> requestTimestamps = new ArrayList<>();

        /**
         * Checks if request at currentTimestamp is allowed under maxRequests limit per windowMs.
         */
        public synchronized boolean allowRequest(long currentTimestamp, long windowMs, int maxRequests) {
            requestTimestamps.add(currentTimestamp);

            long cutoffTime = currentTimestamp - windowMs;

            // Use Upper Bound Binary Search to find count of expired timestamps <= cutoffTime
            int expiredCount = upperBoundTimestamp(requestTimestamps, cutoffTime);

            int activeRequests = requestTimestamps.size() - expiredCount;

            return activeRequests <= maxRequests;
        }

        private int upperBoundTimestamp(List<Long> timestamps, long cutoff) {
            int low = 0, high = timestamps.size();
            while (low < high) {
                int mid = low + (high - low) / 2;
                if (timestamps.get(mid) > cutoff) high = mid;
                else low = mid + 1;
            }
            return low;
        }
    }
}
```

> **Quick Syntax:**
```java
// Dual Heap Balance Lines
if (maxHeap.size() > minHeap.size() + 1) minHeap.add(maxHeap.poll());
```

---

## 7. Concrete Problem Examples & System Applications

1. **LeetCode 295 - Find Median from Data Stream**:
   - High-throughput Dual Heap Median Tracking ($O(1)$ Median Lookup).

2. **Database Engine Indexing (MySQL InnoDB / PostgreSQL)**:
   - B+ Tree Index Range Scans ($O(\log_B N)$ Disk Block Reads).

3. **API Gateway Rate Limiting**:
   - Sliding Window Log Rate Limiter using Binary Search.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class SearchApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("    INDUSTRIAL SEARCH APPLICATIONS DEMO          ");
        System.out.println("=================================================\n");

        // 1. Stream Median Finder Test (LeetCode 295)
        SearchApplicationsMaster.MedianFinder mf = new SearchApplicationsMaster.MedianFinder();
        mf.addNum(1);
        mf.addNum(2);
        System.out.println("1. Added [1, 2] to Stream. Median: " + mf.findMedian());
        mf.addNum(3);
        System.out.println("   Added 3 to Stream. Median: " + mf.findMedian());
        System.out.println("-------------------------------------------------");

        // 2. Timestamp Rate Limiter Test
        SearchApplicationsMaster.TimestampRateLimiter rateLimiter = new SearchApplicationsMaster.TimestampRateLimiter();
        long now = 1000L;
        long window = 500L; // 500ms window
        int maxReq = 2;

        System.out.println("2. Timestamp Rate Limiter Test (Max 2 requests / 500ms):");
        System.out.println("   Req 1 at t=1000ms: Allowed = " + rateLimiter.allowRequest(now, window, maxReq));
        System.out.println("   Req 2 at t=1100ms: Allowed = " + rateLimiter.allowRequest(now + 100, window, maxReq));
        System.out.println("   Req 3 at t=1200ms: Allowed = " + rateLimiter.allowRequest(now + 200, window, maxReq) + " (Rate Limited!)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Application System | Search Paradigm | Time (Insertion) | Time (Query) | Auxiliary Memory | Key Architectural Advantage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stream Median (295)**| Dual Priority Queues| $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $O(N)$ Heap Memory | Dual Heap Balance |
| **B+ Tree Indexing**  | Monotonic Block BS | $O(\log_B N)$ Disk | $\mathbf{O(\log_B N)}$ Disk ⚡| $O(N)$ Index Block | Sequential I/O Scans |
| **Rate Limiter**      | Binary Search Window| $\mathbf{O(1)}$ Append | $\mathbf{O(\log N)}$ Log ⚡ | $O(N)$ Log History | Accurate Window Bounds |

---

## 10. Edge Cases & Boundary Handling

1. **Dual Heap Equal Size Balancing**:
   - `size(maxHeap)` must be maintained as either equal to `size(minHeap)` or exactly 1 element larger.

2. **Empty Priority Queues**:
   - `findMedian()` checks `maxHeap.isEmpty()` before calling `.peek()` to avoid `NullPointerException`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Sorting Full Data Stream Per New Arrival**:
  - Sorting an $N$-element list on every stream arrival takes $O(N \log N)$ time per insertion. Dual Heap insertion takes $O(\log N)$ time.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Dual Heap Stream Invariants:
> * `maxHeap` holds lower $50\%$ of numbers (max on top).
> * `minHeap` holds upper $50\%$ of numbers (min on top).
> * Invariant: `maxHeap.peek() <= minHeap.peek()` for all stream elements! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Dual Heap Stream Median | Sorted Array Insertion Stream |
| :--- | :--- | :--- |
| **Insertion Time** | **$O(\log N)$ Logarithmic ⚡** | $O(N)$ Linear Array Shift |
| **Median Lookup**  | **$O(1)$ Instant Lookup ⚡**| **$O(1)$ Instant Lookup ⚡**|
| **Memory Access**  | Contiguous Heap Memory | Contiguous Array Memory |

---

## 14. How to Recognize This in Questions

* **"Find median dynamically from continuous data stream"** $\rightarrow$ LeetCode 295 Dual Heap.
* **"Count active log requests in sliding window of timestamp logs"** $\rightarrow$ Upper Bound Window Binary Search.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does a B+ Tree use a large branching factor $B \approx 1000$?**  
  *A:* Because disk I/O reads entire memory blocks ($\approx 4\text{KB}$). A large branching factor $B$ reduces tree height to 3 or 4 levels, allowing database queries over 1,000,000,000 records to finish in 3 or 4 disk block reads.

* **Q: Why is Max-Heap used for the lower half in Stream Median Finder?**  
  *A:* The median is the largest element of the lower half, which is instantly accessible at the top of a Max-Heap (`maxHeap.peek()`).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEARCH APPLICATIONS                                   |
+-----------------------------------------------------------------------+
| • Stream Median : MaxHeap (lower 50%), MinHeap (upper 50%)            |
| • Heap Balance  : size(maxHeap) == size(minHeap) (+1)                 |
| • Median Time   : O(1) Median Lookup | O(log N) Insertion ⚡            |
| • B+ Tree Index : Binary search over disk blocks -> O(log_B N) I/O    |
| • Rate Limiter  : Upper bound search on timestamps to count expired   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 295 (`Find Median from Data Stream`) using Dual Heaps.
- [ ] I can explain why Max-Heap stores lower half and Min-Heap stores upper half.
- [ ] I can write a sliding window timestamp rate limiter using binary search.
- [ ] I can state the disk I/O complexity of B+ Tree searching ($O(\log_B N)$).
- [ ] I can trace dual heap balancing step by step.
