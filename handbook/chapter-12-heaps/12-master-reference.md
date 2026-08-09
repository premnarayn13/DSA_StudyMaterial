# 12. Master Reference — Heaps & Priority Queues

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 12: Heaps & Priority Queues**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Array Index Navigation (`left = 2i + 1`, `right = 2i + 2`, `parent = (i-1)/2`), Floyd's $O(N)$ Linear `buildHeap()`, Java `PriorityQueue` API invariants, Safe `Integer.compare(a, b)` rules, Top-K Capped Min-Heap, K-Way Merge Heap size $K$, Two-Heaps Median Balancing, Task Scheduler Greedy Formula `(maxFreq-1)*(N+1)+maxCount`, Reorganize String Feasibility `maxCount <= (N+1)/2`, and Dijkstra Lazy Deletion `if (d > dist[u]) continue`!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **0-Indexed Array Navigation Formulas**:
  - $\text{left}(i) = 2i + 1$
  - $\text{right}(i) = 2i + 2$
  - $\text{parent}(i) = \left\lfloor \frac{i - 1}{2} \right\rfloor$
* **1-Indexed Array Navigation Formulas**:
  - $\text{left}(i) = 2i \quad (i \ll 1)$
  - $\text{right}(i) = 2i + 1 \quad ((i \ll 1) \mid 1)$
  - $\text{parent}(i) = \lfloor i / 2 \rfloor \quad (i \gg 1)$
* **Internal Nodes Range**:
  - All internal nodes reside at indices **$0 \dots \lfloor \frac{N-2}{2} \rfloor$**.
  - Leaves reside at indices **$\lfloor \frac{N}{2} \rfloor \dots N-1$**.
* **Floyd's Linear Build Heap Summation Proof**:
  - $T(N) = \sum_{h=0}^{\log_2 N} \frac{N}{2^{h+1}} \cdot O(h) = \frac{N}{2} \sum_{h=0}^{\infty} \frac{h}{2^h} = \mathbf{O(N) \text{ Linear Time}}$.
* **Dual-Heap Running Median Balancing Invariant**:
  - $0 \le \text{small.size}() - \text{large.size}() \le 1$.
  - Median (Odd Total) = $\text{small.peek}()$.
  - Median (Even Total) = $(\text{small.peek}() + \text{large.peek}()) / 2.0$.
* **Task Scheduler Greedy CPU Cycles Formula**:
  - $\text{Total Cycles} = \max\left(\text{tasks.length}, \ (\text{maxFreq} - 1) \cdot (N + 1) + \text{maxCount}\right)$.
* **Reorganize String Feasibility Condition**:
  - $\text{maxCount} \le \lfloor \frac{N + 1}{2} \rfloor$.

```
Heaps & Priority Queues Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Min Heap Order                    | Parent <= Children; Root = Global Minimum         |
| Max Heap Order                    | Parent >= Children; Root = Global Maximum         |
| Floyd's Build Heap                | Loop i = (N - 2) / 2 down to 0 calling siftDown   |
| Safe Comparator Rule              | (a, b) -> Integer.compare(a, b) (Prevents overflow)|
| Top K Largest                     | Fixed Min-Heap size K -> if (pq.size() > k) poll  |
| K-Way Merge                       | Min-Heap size K -> poll min -> offer node.next    |
| Two-Heaps Median                  | 0 <= small.size() - large.size() <= 1             |
| Task Scheduler Cycles             | Math.max(length, (maxFreq - 1) * (N + 1) + maxCount)|
| Reorganize String Feasible        | maxCount <= (N + 1) / 2                           |
| Dijkstra Lazy Deletion            | if (d > dist[u]) continue (Avoids O(V) removals) |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Get Min/Max (`peek`)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Access `array[0]` directly |
| **Heap Insert (`offer`)** | **$O(1)$ Amortized ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | $O(1)$ Space | Sift-up swaps |
| **Heap Delete (`poll`)** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | $O(1)$ Space | Sift-down swaps |
| **Floyd's `buildHeap`** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ In-Place ⚡** | Bottom-up `siftDown` from $(N-2)/2$ |
| **Heapsort** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(1)$ In-Place ⚡** | Build Max Heap -> Swap root to end |
| **Top K Elements (215)** | **$O(N \log K)$ ⚡** | **$O(N \log K)$ ⚡** | **$O(N \log K)$ ⚡** | **$O(K)$ Space ⚡** | Fixed-size Min-Heap of capacity $K$ |
| **QuickSelect (215)** | **$O(N)$ Avg Linear ⚡**| **$O(N)$ Avg Linear ⚡**| $O(N^2)$ (Worst) | **$O(1)$ Space ⚡** | In-place partition around pivot |
| **K-Way Merge (23)** | **$O(N \log K)$ ⚡** | **$O(N \log K)$ ⚡** | **$O(N \log K)$ ⚡** | **$O(K)$ Space ⚡** | Min-Heap of size $K$ interleaving |
| **Data Stream Median (295)**| **$O(\log N)$ add ⚡**| **$O(\log N)$ add ⚡**| **$O(\log N)$ add ⚡**| $O(N)$ Space | $O(1)$ median query via Two Heaps |
| **Task Scheduler (621)** | **$O(\text{Tasks})$ ⚡** | **$O(\text{Tasks})$ ⚡** | **$O(\text{Tasks})$ ⚡** | **$O(1)$ Space ⚡** | Greedy formula `(maxFreq-1)*(N+1)+maxCount`|
| **Reorganize String (767)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Space ⚡** | Even/Odd index placement `idx += 2` |
| **Timer Queue Manager** | **$O(1)$ Timeout ⚡**| **$O(1)$ Timeout ⚡**| **$O(1)$ Timeout ⚡**| $O(N)$ Space | Min-Heap head query |
| **Dijkstra Engine** | **$O((E+V)\log V)$ ⚡**| **$O((E+V)\log V)$ ⚡**| **$O((E+V)\log V)$ ⚡**| $O(V)$ Space | Min-Heap priority vertex relaxation |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Heap Implementations                                         |
+-----------------------------------------------------------------------------------+
| Contiguous Primitive Array (`int[]`) : Optimal CPU Cache Line Locality (0 Overhead)⚡ |
| `java.util.PriorityQueue<Integer>`   : 16 Bytes Header + Boxed Object References  |
| Resizing Strategy                    : Grows 1.5x (or 2x if initial capacity < 64)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Min-Heap & Max-Heap Instantiation
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// 2. Safe Multi-Property Comparator
PriorityQueue<Pair> pq = new PriorityQueue<>((a, b) -> {
    if (a.freq != b.freq) return Integer.compare(b.freq, a.freq);
    return Integer.compare(a.val, b.val);
});

// 3. Floyd's Build Heap Loop
for (int i = (n - 2) / 2; i >= 0; i--) siftDownMin(arr, i, n);

// 4. Fixed-Size Min-Heap Top-K Eviction Line
minHeap.offer(num);
if (minHeap.size() > k) minHeap.poll();

// 5. Dual-Heap Running Median Balancing Lines
if (small.size() > large.size() + 1) large.offer(small.poll());
else if (small.size() < large.size()) small.offer(large.poll());
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Comparator Subtraction Overflow `(a, b) -> a - b`**: If `a = Integer.MIN_VALUE` and `b = 1`, `a - b` overflows to positive, reversing comparison order. Always use `Integer.compare(a, b)`.
* **Pitfall 2: Top-Down `siftUp` for `buildHeap` ($O(N \log N)$ Penalty)**: Sifting up from index 0 processes leaves across maximum height paths. Always iterate backward from `(N-2)/2` down to 0 with `siftDown` for $O(N)$ linear time.
* **Pitfall 3: Swapping with Larger Child During Sift-Down**: Swapping parent with the larger child violates min heap property against the smaller child. Always swap with the **SMALLEST CHILD**.
* **Pitfall 4: Integer Division Truncation in Median**: `(small.peek() + large.peek()) / 2` returns an `int`, stripping decimals. Always divide by `2.0`.
* **Pitfall 5: $O(N)$ Heap Removals in Dijkstra**: Calling `pq.remove(staleTask)` performs an $O(N)$ array scan. Always use lazy deletion `if (d > dist[u]) continue`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 12 (HEAPS & PRIORITY QUEUES)      |
+-----------------------------------------------------------------------+
| 1. Index Formulas : left = 2i + 1 | right = 2i + 2 | parent = (i-1)/2 |
| 2. Internal Nodes : Indices 0 to (N - 2) / 2                          |
| 3. Floyd's Build  : Iterate (N-2)/2 down to 0 with siftDown -> O(N) ⚡ |
| 4. Safe Comparator: (a, b) -> Integer.compare(a, b) (NO a - b!)       |
| 5. Top K Largest  : Min-Heap size K -> if (pq.size() > k) pq.poll()   |
| 6. K-Way Merge    : Min-Heap size K -> poll min -> offer node.next    |
| 7. Running Median : Max-Heap 'small' + Min-Heap 'large' (size diff <= 1)|
| 8. Task Scheduler : Math.max(tasks.length, (maxFreq-1)*(N+1)+maxCount)|
| 9. Reorganize Feas: maxCount <= (N + 1) / 2                           |
| 10. Dijkstra Lazy : if (d > dist[u]) continue (Avoids O(V) removals) |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write array navigation formulas from memory.
- [ ] I can write custom `MinHeap` with `siftUp` and `siftDown`.
- [ ] I can write Floyd's `buildHeap` in $O(N)$ time.
- [ ] I can write Heapsort in $O(N \log N)$ time and $O(1)$ space.
- [ ] I can write Kth Largest Element (LeetCode 215) using Min-Heap and QuickSelect.
- [ ] I can write Merge k Sorted Lists (LeetCode 23).
- [ ] I can write Find Median from Data Stream (LeetCode 295).
- [ ] I can write Task Scheduler (LeetCode 621) using the Greedy Formula.
- [ ] I can write Reorganize String (LeetCode 767) using Even/Odd index placement.
- [ ] I can write Dijkstra's Shortest Path with lazy deletion.
