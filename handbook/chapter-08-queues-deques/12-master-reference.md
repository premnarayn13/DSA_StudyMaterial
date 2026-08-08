# 12. Master Reference — Queues & Deques

## 1. Introduction
This Master Reference consolidates all core principles, FIFO protocols, Deque dual-ended APIs, Monotonic Deque algorithms, Heap data structures, and Java syntax templates for **Chapter 8: Queues & Deques**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh BFS level snapshot patterns, Monotonic Deque window maximum steps, Two Heaps balancing invariants, and Circular Deque modulo formulas.

## 2. Core Concepts & Formulas Cheat Sheet
* **Modern Java Queue Setup**: `Queue<Integer> queue = new ArrayDeque<>();`
* **Modern Java Deque Setup**: `Deque<Integer> deque = new ArrayDeque<>();`
* **BFS Level Size Snapshot**: `int levelSize = queue.size(); for (int i = 0; i < levelSize; i++)`
* **Circular Queue Modulo Increments**: `rear = (head + count) % capacity; head = (head + 1) % capacity;`
* **Circular Deque Positive Modulo Decrement**: `head = (head - 1 + capacity) % capacity;`
* **Circular Queue Rear Index Formula**: `(head + count - 1) % capacity`
* **Monotonic Deque Eviction Step**: `while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) deque.pollLast();`
* **Monotonic Deque Out-of-Bounds Eviction**: `if (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();`
* **Default Min-Heap Setup**: `PriorityQueue<Integer> minHeap = new PriorityQueue<>();`
* **Max-Heap Setup**: `PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());`
* **Safe Comparator Syntax**: `new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]))`
* **Two Heaps Median Calculation**: `double med = (maxHeap.size() > minHeap.size()) ? maxHeap.peek() : ((double)maxHeap.peek() + minHeap.peek()) / 2.0;`
* **Task Scheduler Math Formula**: `minTime = (maxFreq - 1) * (n + 1) + maxCount; return Math.max(tasks.length, minTime);`

> **Memory Trick:** **"Always snapshot queue.size() before BFS loop! Store INDICES on Monotonic Deque!"**

## 3. Master Queue & Deque Complexity Table
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Triggers / Use Case |
| :--- | :--- | :--- | :--- |
| **`offer()` / `poll()` / `peek()`**| **$O(1)$ Constant** | $O(1)$ Constant | Core Queue / Deque primitives |
| **Binary Tree Level Order (102)**| **$O(N)$ Linear** | $O(W)$ Queue Space | BFS snapshot level size `queue.size()` |
| **Design Circular Queue (622)** | **$O(1)$ all ops**| $O(K)$ Fixed Array | Modulo arithmetic `(head+count)%capacity` |
| **Design Circular Deque (641)** | **$O(1)$ all ops**| $O(K)$ Fixed Array | Modulo decrement `(head-1+cap)%cap` |
| **Sliding Window Max (239)** | **$O(N)$ Amortized**| $O(K)$ Deque Space | Monotonic Decreasing Deque (`peekFirst`) |
| **Kth Largest in Stream (703)**| **$O(\log K)$ Add** | $O(K)$ Heap Space | Bounded Min-Heap of size $K$ |
| **Top K Frequent (347)** | **$O(N)$ Linear** | $O(N)$ Bucket Array| Bucket Sort Array (`index = frequency`) |
| **K Closest Points (973)** | **$O(N \log K)$** | $O(K)$ Heap Space | Max-Heap of size $K$ (`dist = x^2 + y^2`) |
| **Find K Smallest Sums (373)** | **$O(K \log K)$** | $O(K)$ Heap Space | $K$-Way Merge Heap (`[sum, i, j]`) |
| **Smallest Range K Lists (632)**| **$O(N \log K)$** | $O(K)$ Heap Space | Min-Heap + running `currentMax` |
| **Find Median Stream (295)** | **$O(\log N)$ Add** | $O(N)$ Dual Heaps | Two Heaps (`maxHeap` small, `minHeap` large) |
| **IPO Maximized Capital (502)** | **$O(N \log N)$** | $O(N)$ Dual Heaps | Min Capital Heap + Max Profit Heap |
| **Task Scheduler (621)** | **$O(N)$ Linear** | **$O(1)$ Space ⚡**| Math formula `(maxFreq-1)*(n+1)+maxCount` |
| **Reorganize String (767)** | **$O(N)$ Linear** | **$O(1)$ Space ⚡**| Max-Heap + `prev` char pointer |
| **LRU Cache (146)** | **$O(1)$ get/put**| $O(\text{Cap})$ Space | HashMap + DoublyLinkedList (`tail.prev`) |
| **LFU Cache (460)** | **$O(1)$ get/put**| $O(\text{Cap})$ Space | Dual Maps + Freq LinkedLists + `minFreq` |

## 4. Hardware & Memory Footprint Summary
```
+-----------------------------------------------------------------------------------+
| Queue Structure / Memory     | Memory Footprint & Details                         |
+-----------------------------------------------------------------------------------+
| ArrayDeque Circular Buffer   | Dynamic array buffer on Heap (Near 100% L1 Hits ⚡) |
| LinkedList Queue             | Scattered 24-byte Node objects (High Cache Misses)|
| Heap Index Math              | Parent: (i-1)/2 | Left: 2i+1 | Right: 2i+2          |
| Linear Heapify Array         | Bottom-up sift-down takes O(N) Linear Time         |
+-----------------------------------------------------------------------------------+
```

## 5. Java Code Templates & Snippets

> **Quick Syntax:**
```java
// 1. Monotonic Deque Window Maximum Loop
if (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) deque.pollLast();
deque.offerLast(i);
if (i >= k - 1) result[i - k + 1] = nums[deque.peekFirst()];

// 2. Bucket Sort Array Setup
List<Integer>[] buckets = new List[nums.length + 1];

// 3. Two Heaps Median Calculation
double median = (maxHeap.size() > minHeap.size()) 
    ? maxHeap.peek() 
    : ((double) maxHeap.peek() + minHeap.peek()) / 2.0;

// 4. Task Scheduler Math Shortcut
int minTime = (maxFreq - 1) * (n + 1) + maxCount;
return Math.max(tasks.length, minTime);
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: Dynamic BFS Loop Size**: Capture `int size = queue.size()` BEFORE entering loop.
* **Trap 2: Java Negative Modulo Bug**: Use `(head - 1 + capacity) % capacity` for front insertion.
* **Trap 3: Monotonic Deque Stacking**: Store INDICES `i`, NOT values (`deque.offerLast(i)`).
* **Trap 4: PriorityQueue Comparator Underflow**: Use `Integer.compare(a, b)` instead of `a - b`.
* **Trap 5: PriorityQueue Iteration Order**: `for-each` on `PriorityQueue` does NOT output sorted items! Call `poll()` to extract in order.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 8 (QUEUES & DEQUES)              |
+-----------------------------------------------------------------------+
| 1. Queue Standard: Queue<Integer> q = new ArrayDeque<>();             |
| 2. BFS Level Snapshot: int size = q.size(); for (int i = 0; i < size; i++)|
| 3. Circular Queue Modulo: head = (head + 1) % cap; rear = (head+count-1)%cap|
| 4. Monotonic Deque: Evict front if expired (<= i-k); Evict rear if smaller|
| 5. Top-K Linear: Bucket Sort List<Integer>[] buckets = new List[N + 1]|
| 6. K-th Largest Stream: Min-Heap of size K (peek is K-th largest)     |
| 7. Two Heaps Median: maxHeap (left small half) & minHeap (right large half)|
| 8. Task Scheduler Math: Math.max(tasks.length, (maxFreq-1)*(n+1)+maxCount)|
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can write the snapshot level BFS template from memory.
- [ ] I can write the 4-step Monotonic Deque loop for Sliding Window Maximum (LeetCode 239).
- [ ] I can write Bucket Sort Top K Frequent Elements (LeetCode 347) in $O(N)$ linear time.
- [ ] I can implement Two Heaps for Running Median (LeetCode 295) in $O(1)$ query time.
- [ ] I can write LRU Cache (LeetCode 146) and Task Scheduler (LeetCode 621) math shortcut.
