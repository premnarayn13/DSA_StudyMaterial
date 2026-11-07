# 11. Heap Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly mapping problem statements to optimal Heap design patterns during a technical coding interview enables solving top-K streaming analytics, multi-stream merging, running median calculations, and task scheduling in **$O(1)$ peek time and $O(\log K)$ update time**. Heap problems resolve into **5 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal data structure strategies, along with copy-paste production Java templates.

> **Important:** Master the primary selection rules:
> 1. **Fixed-Size Min-Heap of Capacity $K$**: Use for $K$ largest elements, $K$ most frequent elements, and streaming Top-K.
> 2. **K-Way Min-Heap Merge**: Use for merging $K$ sorted lists, matrices, or streams into 1 sorted output.
> 3. **Two Heaps (Max-Heap `small` + Min-Heap `large`)**: Use for continuous running median of data streams.
> 4. **Max-Heap + Cooldown Queue**: Use for CPU task scheduling with cooldown intervals or character separation.
> 5. **Lazy Deletion Heap**: Use for custom object priority updates or sliding window median.

---

## 2. Master Heap Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER HEAP PROBLEM DECISION MATRIX                                                               |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Find K largest / K most frequent items"          | Top K Capped Min-Heap | `if(pq.size()>k) pq.poll()`|
| "Merge K sorted lists / matrices into one list"   | K-Way Min-Heap Merge  | `pq.offer(node.next)` |
| "Find running median of dynamic data stream"      | Two Heaps Median Split| `small.size() - large.size() <= 1`|
| "Schedule tasks separated by cooldown period N"   | Max-Heap + Cooldown   | `cooldownQ.offer(readyTime)`|
| "Update priorities / Dijkstra shortest path"      | Lazy Deletion Heap    | `if (d > dist[u]) continue`|
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Top K Capped Min-Heap Template
* **Signal**: K largest, K most frequent, Kth smallest element (215, 347, 703).

```java
public static int topKCappedHeapTemplate(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);
    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll(); // Evict smallest candidate
        }
    }
    return minHeap.peek(); // Head is Kth largest
}
```

---

## 4. Pattern 2: K-Way Min-Heap Merge Template
* **Signal**: Merging K sorted lists, matrix row interleaving, K smallest pairs (23, 378, 373).

```java
public static ListNode kWayMergeTemplate(ListNode[] lists) {
    if (lists == null || lists.length == 0) return null;
    PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
        lists.length, (a, b) -> Integer.compare(a.val, b.val)
    );
    for (ListNode node : lists) {
        if (node != null) minHeap.offer(node);
    }

    ListNode dummy = new ListNode(0);
    ListNode curr = dummy;
    while (!minHeap.isEmpty()) {
        ListNode minNode = minHeap.poll();
        curr.next = minNode;
        curr = curr.next;
        if (minNode.next != null) minHeap.offer(minNode.next);
    }
    return dummy.next;
}
```

---

## 5. Pattern 3: Two Heaps Running Median Template
* **Signal**: Running median of data stream, IPO capital maximization (295, 502).

```java
public static class TwoHeapsMedianTemplate {
    private final PriorityQueue<Integer> small = new PriorityQueue<>(Collections.reverseOrder()); // Max-Heap
    private final PriorityQueue<Integer> large = new PriorityQueue<>(); // Min-Heap

    public void addNum(int num) {
        if (small.isEmpty() || num <= small.peek()) small.offer(num);
        else large.offer(num);

        if (small.size() > large.size() + 1) large.offer(small.poll());
        else if (small.size() < large.size()) small.offer(large.poll());
    }

    public double findMedian() {
        if (small.size() > large.size()) return small.peek();
        return (small.peek() + (double) large.peek()) / 2.0;
    }
}
```

---

## 6. Pattern 4: Max-Heap + Cooldown Queue Template
* **Signal**: Task scheduler, reorganize string, K distance separation (621, 767, 358).

```java
public static int taskSchedulerTemplate(char[] tasks, int n) {
    int[] freq = new int[26];
    for (char t : tasks) freq[t - 'A']++;
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    for (int f : freq) if (f > 0) maxHeap.offer(f);

    Queue<int[]> cooldownQueue = new ArrayDeque<>();
    int cycles = 0;
    while (!maxHeap.isEmpty() || !cooldownQueue.isEmpty()) {
        cycles++;
        if (!cooldownQueue.isEmpty() && cooldownQueue.peek()[1] <= cycles) {
            maxHeap.offer(cooldownQueue.poll()[0]);
        }
        if (!maxHeap.isEmpty()) {
            int rem = maxHeap.poll() - 1;
            if (rem > 0) cooldownQueue.offer(new int[]{rem, cycles + n});
        }
    }
    return cycles;
}
```

---

## 7. Pattern 5: Lazy Deletion Heap Template
* **Signal**: Dijkstra shortest path, priority updates without $O(N)$ removal (882, Dijkstra).

```java
public static int[] lazyDeletionDijkstraTemplate(int V, List<List<int[]>> graph, int src) {
    int[] dist = new int[V];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
    minHeap.offer(new int[]{src, 0});

    while (!minHeap.isEmpty()) {
        int[] curr = minHeap.poll();
        int u = curr[0], d = curr[1];
        if (d > dist[u]) continue; // Lazy deletion check!

        for (int[] edge : graph.get(u)) {
            int v = edge[0], weight = edge[1];
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                minHeap.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}
```

---

## 8. Edge Case & Trap Checklist
* **Integer Overflow in Comparators**: Never use `(a, b) -> a - b`! Always use `Integer.compare(a, b)`.
* **Null Element Invariant**: PriorityQueue throws `NullPointerException` on `null` insertions.
* **Median Truncation**: Always divide by `2.0` when calculating even median `(small.peek() + large.peek()) / 2.0`.
* **Lazy Deletion**: Always include `if (d > dist[u]) continue` in Dijkstra to prevent $O(N)$ removal penalties.

---

## 9. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: HEAP PATTERN RECOGNITION                             |
+-----------------------------------------------------------------------+
| 1. Top K Largest   : Min-Heap size K -> if (pq.size() > k) pq.poll()  |
| 2. K-Way Merge     : Min-Heap size K -> poll min -> offer node.next   |
| 3. Running Median  : Max-Heap 'small' + Min-Heap 'large' (size diff <= 1)|
| 4. Task Scheduler  : Max-Heap + Cooldown Queue                        |
| 5. Lazy Deletion   : Skip stale tuples with if (d > dist[u]) continue  |
| 6. Safe Comparator : (a, b) -> Integer.compare(a, b)                 |
| 7. Reorganize Feas : If maxCount > (N + 1) / 2 -> Return ""           |
+-----------------------------------------------------------------------+
```

---

## 10. Practice Checklist
- [ ] I can write all 5 production heap templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why `(a, b) -> Integer.compare(a, b)` prevents comparison bugs.
- [ ] I know how lazy deletion optimizes priority updates.
- [ ] I can derive the running median size balance condition.
