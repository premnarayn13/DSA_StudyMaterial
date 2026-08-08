# 11. Heap & Priority Queue Problem Patterns, Decision Matrix & Code Templates

## 1. Introduction
Recognizing heap problem patterns instantly during a 45-minute technical coding interview is the key to solving priority queue and stream processing problems bug-free. Heap problems can be categorized into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping problem requirements to optimal priority queue strategies, along with copy-paste production Java templates.

> **Important:** Master the primary heap selection invariants:
> 1. **Top-K Largest**: Use a **Min-Heap of size $K$** (`if (size > K) poll()`).
> 2. **Top-K Smallest**: Use a **Max-Heap of size $K$** (`if (size > K) poll()`).
> 3. **Continuous Median**: Use **Two Heaps** (`maxHeap` small half $N/2$, `minHeap` large half $N/2$).
> 4. **K-Way Merge**: Use a **Min-Heap of size $K$** holding 1 candidate element per stream.

---

## 2. Master Heap Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER HEAP PROBLEM DECISION MATRIX                                                               |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Top K largest / K-th largest in stream"          | Fixed-Size Min-Heap   | `minHeap.size() > K`  |
| "Top K smallest / K-th smallest in array"         | Fixed-Size Max-Heap   | `maxHeap.size() > K`  |
| "Find median dynamically in continuous stream"    | Two-Heaps Pattern     | `maxHeap` & `minHeap` |
| "Merge K sorted lists / matrix rows"              | K-Way Stream Merge    | 1 Candidate / Stream  |
| "Shortest processing time / CPU Task Cooldown"    | Greedy Priority Queue | Max-Heap + Cooldown   |
| "Fast decrease-key without linear scan in Dijkstra"| Indexed Priority Queue| `IndexMinPQ` 3-Arrays |
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Fixed-Size Min-Heap (Top K Largest Elements)
* **Signal**: Finding Top K largest, K-th largest in a stream (215, 703).
* **Invariant**: `minHeap` holds the $K$ largest elements seen so far; `minHeap.peek()` gives the $K$-th largest element.

```java
public static List<Integer> topKLargestTemplate(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);

    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) {
            minHeap.poll(); // Evicts smallest number!
        }
    }

    List<Integer> result = new ArrayList<>(minHeap);
    return result;
}
```

---

## 4. Pattern 2: Two-Heaps Stream Median Finding
* **Signal**: Continuous stream median (295), Sliding window median (480).
* **Invariant**: `maxHeap` stores small half, `minHeap` stores large half; `maxHeap.size() >= minHeap.size()`.

```java
public static class TwoHeapsMedianTemplate {
    private final PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Integer> minHeap = new PriorityQueue<>();

    public void addNum(int num) {
        maxHeap.offer(num);
        minHeap.offer(maxHeap.poll()); // Balance order

        if (minHeap.size() > maxHeap.size()) {
            maxHeap.offer(minHeap.poll()); // Balance size
        }
    }

    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) return maxHeap.peek();
        return ((double) maxHeap.peek() + (double) minHeap.peek()) / 2.0;
    }
}
```

---

## 5. Pattern 3: K-Way Stream Merge
* **Signal**: Merge K sorted lists (23), Sorted matrix selection (378), K smallest pair sums (373).
* **Invariant**: Min-Heap holds 1 candidate head per active stream; polling min advances that specific stream.

```java
public static ListNode kWayMergeTemplate(ListNode[] lists) {
    PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
        (a, b) -> Integer.compare(a.val, b.val)
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

        if (minNode.next != null) {
            minHeap.offer(minNode.next); // Stream advancement!
        }
    }

    return dummy.next;
}
```

---

## 6. Pattern 4: Greedy Priority Queue Scheduling
* **Signal**: Task Scheduler (621), Shortest Job First CPU (1834), Minimum Refueling Stops (871).
* **Invariant**: Max-Heap stores available tasks/fuel; greedily select max available resource.

```java
public static int greedyRefuelTemplate(int target, int startFuel, int[][] stations) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    long fuel = startFuel;
    int stops = 0, i = 0, n = stations.length;

    while (fuel < target) {
        while (i < n && stations[i][0] <= fuel) {
            maxHeap.offer(stations[i][1]); // Collect reachable fuel
            i++;
        }
        if (maxHeap.isEmpty()) return -1;
        fuel += maxHeap.poll(); // Greedily pick largest fuel station
        stops++;
    }
    return stops;
}
```

---

## 7. Pattern 5: Multi-Tier Custom Comparator Sorting
* **Signal**: Top K Frequent Words (692), Reorganize String (767).
* **Invariant**: Frequency primary order; lexicographical/character tie-breaking secondary order.

```java
public static List<String> topKFrequentWordsTemplate(String[] words, int k) {
    Map<String, Integer> freqMap = new HashMap<>();
    for (String w : words) freqMap.put(w, freqMap.getOrDefault(w, 0) + 1);

    PriorityQueue<String> minHeap = new PriorityQueue<>((w1, w2) -> {
        int f1 = freqMap.get(w1), f2 = freqMap.get(w2);
        if (f1 != f2) return Integer.compare(f1, f2);
        return w2.compareTo(w1); // Invert string order for eviction!
    });

    for (String word : freqMap.keySet()) {
        minHeap.offer(word);
        if (minHeap.size() > k) minHeap.poll();
    }

    List<String> res = new ArrayList<>();
    while (!minHeap.isEmpty()) res.add(minHeap.poll());
    Collections.reverse(res);
    return res;
}
```

---

## 8. Pattern 6: Indexed Priority Queue ($O(\log N)$ Decrease-Key)
* **Signal**: Dijkstra's algorithm without duplicate vertex pushes, In-place distance updates.
* **Invariant**: 3 Arrays (`values[]`, `pm[]` position map, `im[]` inverse map) in sync.

```java
public static int[] dijkstraIPQTemplate(int V, List<List<Edge>> adj, int src) {
    int[] dist = new int[V];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;

    IndexMinPQ<Integer> ipq = new IndexMinPQ<>(V);
    ipq.insert(src, 0);

    while (!ipq.isEmpty()) {
        int u = ipq.pollMinKey();

        for (Edge edge : adj.get(u)) {
            int v = edge.to;
            int weight = edge.weight;

            if (dist[u] != Integer.MAX_VALUE && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                if (ipq.contains(v)) ipq.decreaseKey(v, dist[v]); // O(log V) Decrease-Key!
                else ipq.insert(v, dist[v]);
            }
        }
    }
    return dist;
}
```

---

## 9. Edge Case Checklist for Heap Problems
* **Heap underflow (`peek()` / `poll()` on empty heap)**: Check `!heap.isEmpty()`.
* **Integer Subtraction Overflow in Comparator**: Always use `Integer.compare(a, b)` instead of `a - b`.
* **Null Pointer Exception**: Java's `PriorityQueue` DOES NOT allow `null` elements.
* **`PriorityQueue.remove(obj)` Linear Time Penalty**: Calling `pq.remove(obj)` takes $O(N)$ linear time. Use **Lazy Deletion** or **Indexed Priority Queue**.
* **Median Addition Overflow**: Cast to `(double)` BEFORE adding two `int` peaks: `((double) max + (double) min) / 2.0`.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: HEAP & PRIORITY QUEUE PROBLEM PATTERNS               |
+-----------------------------------------------------------------------+
| 1. Top K Largest: Min-Heap of size K (poll when size > K)             |
| 2. Top K Smallest: Max-Heap of size K (poll when size > K)            |
| 3. Two-Heaps Median: maxHeap (Small Half) & minHeap (Large Half)      |
| 4. Median Addition Guard: Cast to (double) BEFORE adding peak values! |
| 5. K-Way Merge: Push 1 candidate head per stream in Min-Heap of size K |
| 6. Greedy SJF Scheduling: Min-Heap ordered by processing time         |
| 7. Removal Pitfall: pq.remove(obj) is O(N) LINEAR time search! ❌     |
| 8. IPQ Dijkstra: 3-Arrays (values, pm, im) for O(log N) decreaseKey    |
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 heap code templates from memory.
- [ ] I can select the correct pattern within 30 seconds of reading a problem prompt.
- [ ] I know why `(a, b) -> Integer.compare(a, b)` MUST be used over `a - b`.
- [ ] I know why `PriorityQueue.remove(obj)` takes $O(N)$ linear time.
- [ ] I know how `IndexMinPQ` achieves $O(\log N)$ decrease-key operations.
