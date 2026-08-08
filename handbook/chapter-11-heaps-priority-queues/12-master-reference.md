# 12. Master Reference — Heaps & Priority Queues

## 1. Introduction
This Master Reference consolidates all mathematical proofs, index navigation formulas, heap invariants, JDK `PriorityQueue` internals, Heapsort mechanics, pattern decision matrices, and advanced variants for **Chapter 11: Heaps & Priority Queues**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh array index navigation (`(i-1)/2`, `2i+1`, `2i+2`), Floyd's $O(N)$ Heapify proof ($\sum \frac{h}{2^h} = 2$), `PriorityQueue` dynamic growth formula, Min-Heap of size $K$ Top-K rule, Two-Heaps stream median invariants, and Indexed Priority Queue 3-array coordinate mapping!

---

## 2. Master Mathematical & JDK Formula Cheat Sheet
* **0-Based Index Navigation**:
  - `parent = (i - 1) / 2`
  - `leftChild = 2 * i + 1`
  - `rightChild = 2 * i + 2`
  - `isLeaf = (2 * i + 1 >= N)` (Leaves occupy indices $\lfloor N/2 \rfloor \dots N - 1$).
* **1-Based Index Navigation**:
  - `parent = i / 2`
  - `leftChild = 2 * i`
  - `rightChild = 2 * i + 1`
* **Floyd's Heapify Start Index**: `startIndex = (N / 2) - 1` (Loops backwards down to 0 calling `siftDown`).
* **Floyd's Heapify Mathematical Work Sum**: $S = 2^H \sum_{h=0}^{H} \frac{h}{2^h} = 2^H \cdot 2 = 2^{H+1} \approx \mathbf{2N = O(N)\text{ Linear Time}}$.
* **JDK PriorityQueue Growth Formula**:
  - `newCapacity = oldCapacity + ((oldCapacity < 64) ? (oldCapacity + 2) : (oldCapacity >> 1))`
  - Double (+2) if size $< 64$; 50% growth if size $\ge 64$.
* **Median Stream Addition Overflow Guard**: `return ((double) maxHeap.peek() + (double) minHeap.peek()) / 2.0`.
* **Fibonacci Heap Dijkstra Complexity**: $O(E + V \log V)$ (reduces dense graph time from $O(V^2 \log V)$ to $O(V^2)$ linear in edges).
* **IPQ Dual-Swap Rule**: Must update `pm[im[i]] = j`, `pm[im[j]] = i`, then swap `im[i]` and `im[j]` in sync.

```
Heap Invariants & Structures Summary:
+-----------------------------------+---------------------------------------------------+
| Heap Concept / Structure          | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Min-Heap Invariant                | Parent <= Children (Root array[0] is Minimum)     |
| Max-Heap Invariant                | Parent >= Children (Root array[0] is Maximum)     |
| Complete Binary Tree              | All levels full except last (filled left-aligned) |
| Fixed-Size Top-K Largest          | Min-Heap of size K (poll when size > K)           |
| Fixed-Size Top-K Smallest         | Max-Heap of size K (poll when size > K)           |
| Two-Heaps Stream Median           | maxHeap (Small Half N/2) & minHeap (Large Half N/2)|
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Heap Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`peek()`** | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ | Direct `array[0]` read |
| **`insert(val)` / `offer(e)`**| $O(1)$ | **$O(\log N)$ Logarithmic⚡**| $O(\log N)$ | $O(1)$ | Sift-Up through tree height $H$ |
| **`extractMin()` / `poll()`** | $O(\log N)$ | **$O(\log N)$ Logarithmic⚡**| $O(\log N)$ | $O(1)$ | Root swap + Sift-Down |
| **`remove(Object o)`** | $O(1)$ | **$O(N)$ Linear ❌** | **$O(N)$ Linear ❌** | $O(1)$ | Linear array search for `o` |
| **Floyd's Heapify** | **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ In-Place ⚡**| Bottom-up `siftDown` loop from `(N/2)-1` |
| **Heapsort Algorithm** | **$O(N \log N)$** | **$O(N \log N)$ ⚡**| **$O(N \log N)$ ⚡**| **$O(1)$ Strict In-Place ⚡**| Phase 1 Heapify + Phase 2 Extract |
| **Quickselect (215)** | $O(N)$ | **$O(N)$ Average ⚡**| $O(N^2)$ (Worst case) | **$O(1)$ In-Place ⚡**| Partition target index $N-k$ |
| **Two-Heaps Median (295)** | **$O(1)$ Median** | **$O(\log N)$ Add** | **$O(\log N)$ Add** | $O(N)$ | `maxHeap` small half & `minHeap` large half |
| **K-Way List Merge (23)** | **$O(N \log K)$** | **$O(N \log K)$ ⚡**| **$O(N \log K)$ ⚡**| $O(K)$ Heap | 1 candidate head / stream |
| **Indexed PQ DecreaseKey**| **$O(1)$** | **$O(\log N)$ ⚡**| **$O(\log N)$ ⚡**| $O(N)$ 3-Arrays | Direct position lookup `pm[ki]` + `siftUp` |
| **Fibonacci Heap DecreaseKey**| **$O(1)$ Amortized ⚡**| **$O(1)$ Amortized ⚡**| $O(\log N)$ | $O(N)$ Pointers | Lazy circular root list + cascading cuts |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Heap Structures on 64-Bit JVM (Compressed OOPs)               |
+-----------------------------------------------------------------------------------+
| Primitive Heap (int[] heap)   : 24 Bytes Header + 4 Bytes per Integer (Zero Pointers ⚡)|
| Object Heap (PriorityQueue<E>): 24 Bytes Header + 4 Bytes per Object Reference    |
| Indexed Priority Queue (IPQ)  : 3 Arrays of Size N (values[], pm[], im[]) (~12N Bytes)|
| Fibonacci Heap Node           : 48 Bytes per Node (Header + 4 Pointers + Degree + Mark)|
| Pairing Heap Node             : 32 Bytes per Node (Header + child + sibling + prev)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Min-Heap & Max-Heap Declarations
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
PriorityQueue<Integer> maxHeapLambda = new PriorityQueue<>((a, b) -> Integer.compare(b, a));

// 2. Fixed-Size Top-K Largest Pattern
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll();
}

// 3. Floyd's In-Place Heapify Loop
for (int i = (n / 2) - 1; i >= 0; i--) {
    siftDownMin(arr, n, i);
}

// 4. Two-Heaps Stream Median Addition
maxHeap.offer(num);
minHeap.offer(maxHeap.poll());
if (minHeap.size() > maxHeap.size()) maxHeap.offer(minHeap.poll());

// 5. Indexed Priority Queue Dual Swap Helper
private void swap(int i, int j) {
    pm[im[i]] = j;
    pm[im[j]] = i;
    int tempIm = im[i];
    im[i] = im[j];
    im[j] = tempIm;
}
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using `(a, b) -> a - b` Comparator with Negative Numbers**: Causes integer overflow bugs. Always use `Integer.compare(a, b)`.
* **Pitfall 2: Calling `PriorityQueue.remove(Object o)` in Loops**: `remove(o)` requires an $O(N)$ linear array search. Calling it in a loop degrades algorithms to $O(N^2)$ quadratic time. Use **Lazy Deletion** or **Indexed Priority Queue**.
* **Pitfall 3: Using Max-Heap for Top K Largest Elements**: Storing all $N$ elements in a Max-Heap takes $O(N \log N)$ time and $O(N)$ space. Use a **Min-Heap of size $K$** ($O(N \log K)$ time, $O(K)$ space).
* **Pitfall 4: Building Min-Heap for Ascending Heapsort**: Swapping min root `array[0]` to the end produces a DESCENDING sorted array. Ascending Heapsort REQUIRES a **Max-Heap**.
* **Pitfall 5: 32-Bit Integer Overflow in Stream Median Addition**: `(max.peek() + min.peek()) / 2.0` overflows if values are near `Integer.MAX_VALUE`. Cast to `(double)` BEFORE addition.
* **Pitfall 6: Loading ALL Stream Elements in K-Way Merge**: Pushing all $N$ elements into a heap defeats K-Way Merge. Keep ONLY 1 candidate head per stream in the Min-Heap of size $K$.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 11 (HEAPS & PRIORITY QUEUES)     |
+-----------------------------------------------------------------------+
| 1. Index Navigation: Parent (i-1)/2 | Left 2i+1 | Right 2i+2          |
| 2. Floyd's Heapify: Start (N/2)-1 down to 0 calling siftDown O(N) ⚡   |
| 3. PriorityQueue Growth: Double (+2) if <64; 50% if >=64              |
| 4. Top-K Largest Rule: Min-Heap of size K (poll when size > K)        |
| 5. Top-K Smallest Rule: Max-Heap of size K (poll when size > K)       |
| 6. Two-Heaps Median: maxHeap (Small Half) & minHeap (Large Half)      |
| 7. Median Overflow Guard: Cast to (double) BEFORE adding peak values! |
| 8. Heapsort Ascending: MAX-HEAP required! Swap root to i, siftDown(i, 0)|
| 9. K-Way Merge: PriorityQueue of size K holding 1 candidate / stream  |
| 10. Task Scheduler SJF: Min-Heap ordered by processing time           |
| 11. IPQ 3-Arrays: values[ki], pm[ki] (Pos Map), im[pos] (Inv Map)     |
| 12. IPQ DecreaseKey: values[ki] = val -> siftUp(pm[ki]) in O(log N) ⚡|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write 0-indexed parent and child index formulas.
- [ ] I can write the mathematical proof of $O(N)$ Heapify using $\sum \frac{h}{2^h} = 2$.
- [ ] I can state the default capacity (11) and growth formula of `PriorityQueue`.
- [ ] I know why `Integer.compare(a, b)` MUST be used over `a - b`.
- [ ] I can write the 2-phase Heapsort algorithm from memory in 5 minutes.
- [ ] I can write the Min-Heap of size $K$ pattern for Top K Largest elements.
- [ ] I can write Quickselect (LeetCode 215) in $O(N)$ average time.
- [ ] I can write `MedianFinder` (LeetCode 295) using the Two-Heaps pattern.
- [ ] I can write Merge K Sorted Lists (LeetCode 23) using a Min-Heap of size $K$.
- [ ] I can write Task Scheduler (LeetCode 621) using the math formula.
- [ ] I can state why Fibonacci Heap reduces Dijkstra to $O(E + V \log V)$.
- [ ] I can implement an `IndexMinPQ` with $O(\log N)$ `decreaseKey`.
