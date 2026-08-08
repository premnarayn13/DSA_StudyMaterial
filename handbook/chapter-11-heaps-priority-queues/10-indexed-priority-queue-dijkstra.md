# 10. Indexed Priority Queue (IPQ) Architecture & $O(\log N)$ Decrease-Key in Dijkstra

## 1. Introduction
Standard Priority Queues in standard libraries (like Java's `java.util.PriorityQueue`) lack a fast mechanism for updating an arbitrary element's priority. Calling `pq.remove(object)` takes **$O(N)$ linear time**, which degrades Dijkstra's Shortest Path Algorithm or Prim's MST Algorithm to $O(V^2)$ when distance keys are updated dynamically. An **Indexed Priority Queue (IPQ)** solves this flaw by combining a 1D Array Min-Heap with an **Inverse Lookup Position Map**, enabling **$O(\log N)$ Logarithmic Decrease-Key, Delete, and Update operations**!

> **Important:** An Indexed Priority Queue assigns a fixed **Key Index `ki`** (an integer $0 \dots N-1$, such as Vertex ID in a graph) to every element. By maintaining a Position Map `pm[ki] -> heapIndex` and Inverse Map `im[heapIndex] -> ki`, the IPQ locates ANY vertex's position in the heap array in **$O(1)$ constant time**, allowing `siftUp` or `siftDown` to execute in **$O(\log N)$ time**!

```
Indexed Priority Queue Mapping Architecture:
+-----------------------------------------------------------------------------------+
| Vertex Key Index (ki) : 0, 1, 2 ... V-1 (Graph Vertex IDs)                        |
| Position Map (pm[])   : pm[ki] -> Stores exact heapIndex of vertex ki in Heap ⚡   |
| Inverse Map (im[])    : im[heapIndex] -> Stores vertex ki at heapIndex ⚡         |
| Result                : O(1) Lookup of any Vertex -> O(log N) Decrease-Key ⚡     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & The 3-Array IPQ Mapping Infrastructure

To implement an Indexed Priority Queue efficiently, we maintain 3 primary arrays of size $N$:

### 2.1 The 3 Dual-Mapping Arrays
1. **`values[ki]`**: Stores the priority value (e.g. `distTo[v]`) associated with key index `ki`.
2. **`pm[ki]` (Position Map)**: Maps key index `ki` to its current position `heapIndex` in the heap array (`pm[ki] = heapIndex`).
   - If `ki` is not currently in the heap, `pm[ki] = -1`.
3. **`im[heapIndex]` (Inverse Map)**: Maps a heap array position `heapIndex` back to its assigned key index `ki` (`im[heapIndex] = ki`).

### 2.2 Dual-Swap Mechanics (`swap(i, j)`)
Whenever two heap nodes at positions `i` and `j` are swapped during `siftUp` or `siftDown`, BOTH mapping arrays MUST be updated in sync:

```java
private void swap(int i, int j) {
    // 1. Swap Inverse Map entries (Swap ki values at heap positions i and j)
    pm[im[i]] = j;
    pm[im[j]] = i;

    int tempIm = im[i];
    im[i] = im[j];
    im[j] = tempIm;
}
```

```
3-Array IPQ Lookup Equation:
Value Lookup       : values[ki]
Heap Position      : heapIndex = pm[ki]
Reverse Key Lookup : ki = im[heapIndex]
Invariant Rule     : im[pm[ki]] == ki AND pm[im[heapIndex]] == heapIndex
```

> **Memory Trick:** **"pm[ki] maps key index to heap position! im[heapIndex] maps heap position to key index! Updating heap MUST swap pm and im in sync!"**

---

## 3. Operations & Decrease-Key Algorithm

### 3.1 `decreaseKey(ki, newVal)` Algorithm ($O(\log N)$ Time)
1. Verify key index `ki` exists in heap (`pm[ki] != -1`).
2. Update value: `values[ki] = newVal`.
3. Get heap position: `heapIndex = pm[ki]`.
4. Execute **`siftUp(heapIndex)`** (since value decreased, element moves UP towards root!).

### 3.2 `delete(ki)` Algorithm ($O(\log N)$ Time)
1. Get heap position `i = pm[ki]`.
2. Swap element `i` with last heap element `lastIdx = size - 1`: `swap(i, lastIdx)`.
3. Decrement `size--`.
4. Mark `pm[ki] = -1`.
5. Execute `siftUp(i)` and `siftDown(i)` to restore heap order!

```
IPQ Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Name        | Standard PQ Time  | Indexed PQ Time   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| `insert(ki, val)`     | $O(\log N)$       | **$O(\log N)$ ⚡** | `pm[ki] = size; siftUp`|
| `peekMinKey()`        | $O(1)$            | **$O(1)$ Constant⚡**| `im[0]`           |
| `pollMinKey()`        | $O(\log N)$       | **$O(\log N)$ ⚡** | `swap(0, size-1)` |
| `decreaseKey(ki, val)`| **$O(N)$ Linear❌**| **$O(\log N)$ ⚡** | `siftUp(pm[ki])`  |
| `delete(ki)`          | **$O(N)$ Linear❌**| **$O(\log N)$ ⚡** | `swap(pm[ki], end)`|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Dijkstra's Algorithm using IPQ on Vertices $V = 3$ (`distTo = [0, inf, inf]`):

```
Init: IPQ size = 0. Values = [0, inf, inf], pm = [-1, -1, -1], im = [-1, -1, -1]

1. insert(v=0, dist=0):
   pm[0] = 0, im[0] = 0, values[0] = 0. Heap: [v0 (dist 0)]

2. Relax Edge 0 -> 1 (weight 4):
   values[1] = 4. insert(v=1, dist=4).
   pm[1] = 1, im[1] = 1. Heap: [v0(0), v1(4)]

3. Relax Edge 0 -> 2 (weight 10):
   values[2] = 10. insert(v=2, dist=10).
   pm[2] = 2, im[2] = 2. Heap: [v0(0), v1(4), v2(10)]

4. pollMinKey() -> Returns v0 (dist 0).
   Swap 0 & 2. Heap: [v1(4), v2(10)]. pm[1]=0, pm[2]=1.

5. Relax Edge 1 -> 2 (weight 3): New distTo[2] = 4 + 3 = 7 < 10!
   Call decreaseKey(v=2, dist=7):
   values[2] = 7. Heap position pm[2] = 1.
   siftUp(1) -> Compare v2(7) with v1(4). 7 > 4 -> No swap.
   Updated Heap: [v1(dist 4), v2(dist 7)] ✅ (O(log V) Decrease-Key!)
```

---

## 5. Visual Diagram
Indexed Priority Queue Dual Mapping Topography:

```
Key Index Array (ki):        [ 0 ]      [ 1 ]      [ 2 ]     (Vertex IDs)
                              |          |          |
                              v          v          v
Position Map (pm[ki]):       [ 0 ]      [ 2 ]      [ 1 ]     (Heap Array Positions)
                              |          |          |
                              +----------+----------+
                                         |
                                         v
Heap Array (im[pos]):        [ 0 ]      [ 1 ]      [ 2 ]     (Heap Index)
Inverse Map (im[]):          v0(d=0)    v2(d=7)    v1(d=4)   (Vertex at Position)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a complete **Min-Indexed Priority Queue (IndexMinPQ)** and **Dijkstra's Shortest Path Algorithm**:

```java
import java.util.*;

public class IndexedPriorityQueueMaster {

    // 1. Min-Indexed Priority Queue Implementation O(log N) DecreaseKey
    public static class IndexMinPQ<T extends Comparable<T>> {
        private int maxSize;
        private int size;
        private int[] pm;   // Position Map: pm[ki] -> heapIndex
        private int[] im;   // Inverse Map : im[heapIndex] -> ki
        private T[] values; // Priority Values: values[ki]

        @SuppressWarnings("unchecked" )
        public IndexMinPQ(int maxSize) {
            this.maxSize = maxSize;
            this.size = 0;
            this.pm = new int[maxSize];
            this.im = new int[maxSize];
            this.values = (T[]) new Comparable[maxSize];

            Arrays.fill(pm, -1);
            Arrays.fill(im, -1);
        }

        public int size() { return size; }
        public boolean isEmpty() { return size == 0; }
        public boolean contains(int ki) { return pm[ki] != -1; }

        // Insert key index ki with priority val. O(log N) Time
        public void insert(int ki, T val) {
            if (contains(ki)) throw new IllegalArgumentException("Key index already in IPQ!");
            values[ki] = val;
            pm[ki] = size;
            im[size] = ki;
            siftUp(size);
            size++;
        }

        // Returns key index with minimum priority. O(1) Time
        public int peekMinKey() {
            if (isEmpty()) throw new NoSuchElementException("IPQ is empty!");
            return im[0];
        }

        // Returns minimum priority value. O(1) Time
        public T peekMinValue() {
            if (isEmpty()) throw new NoSuchElementException("IPQ is empty!");
            return values[im[0]];
        }

        // Removes and returns minimum key index. O(log N) Time
        public int pollMinKey() {
            if (isEmpty()) throw new NoSuchElementException("IPQ is empty!");
            int minKey = im[0];
            swap(0, size - 1);
            size--;
            siftDown(0);
            pm[minKey] = -1;
            im[size] = -1;
            values[minKey] = null;
            return minKey;
        }

        // Decrease priority value associated with key index ki. O(log N) Time
        public void decreaseKey(int ki, T newVal) {
            if (!contains(ki)) throw new NoSuchElementException("Key index not in IPQ!");
            if (newVal.compareTo(values[ki]) >= 0) {
                throw new IllegalArgumentException("New value must be strictly smaller!");
            }
            values[ki] = newVal;
            siftUp(pm[ki]); // Value decreased -> Move UP in Min-Heap!
        }

        private void siftUp(int i) {
            while (i > 0) {
                int p = (i - 1) / 2;
                if (values[im[i]].compareTo(values[im[p]]) < 0) {
                    swap(i, p);
                    i = p;
                } else {
                    break;
                }
            }
        }

        private void siftDown(int i) {
            while (2 * i + 1 < size) {
                int left = 2 * i + 1;
                int right = 2 * i + 2;
                int smallest = left;

                if (right < size && values[im[right]].compareTo(values[im[left]]) < 0) {
                    smallest = right;
                }

                if (values[im[i]].compareTo(values[im[smallest]]) > 0) {
                    swap(i, smallest);
                    i = smallest;
                } else {
                    break;
                }
            }
        }

        private void swap(int i, int j) {
            pm[im[i]] = j;
            pm[im[j]] = i;
            int tempIm = im[i];
            im[i] = im[j];
            im[j] = tempIm;
        }
    }

    // 2. Optimized Dijkstra's Algorithm using IndexMinPQ O(E log V) Time
    public static class Edge {
        int to;
        int weight;
        Edge(int to, int weight) { this.to = to; this.weight = weight; }
    }

    public static int[] dijkstraIPQ(int V, List<List<Edge>> adj, int src) {
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

                    if (ipq.contains(v)) {
                        ipq.decreaseKey(v, dist[v]); // O(log V) Decrease-Key!
                    } else {
                        ipq.insert(v, dist[v]);
                    }
                }
            }
        }

        return dist;
    }
}
```

> **Quick Syntax:**
```java
// Dijkstra IPQ Decrease-Key vs Insert Syntax
if (ipq.contains(v)) ipq.decreaseKey(v, dist[v]);
else ipq.insert(v, dist[v]);
```

---

## 7. Concrete Problem Examples
* **Dijkstra's Shortest Path Algorithm**: Eliminates duplicate node pushes in Priority Queue.
* **Prim's Minimum Spanning Tree Algorithm**: Updating vertex distances to MST in $O(E \log V)$ time.
* **A* Search Algorithm**: Updating $g(n) + h(n)$ heuristic node priorities.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing IndexMinPQ and Dijkstra's algorithm:

```java
public class IndexedPriorityQueueDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing IndexMinPQ DecreaseKey ===");
        IndexedPriorityQueueMaster.IndexMinPQ<Integer> ipq = new IndexedPriorityQueueMaster.IndexMinPQ<>(10);

        ipq.insert(0, 50); // Vertex 0, dist 50
        ipq.insert(1, 30); // Vertex 1, dist 30
        ipq.insert(2, 40); // Vertex 2, dist 40

        System.out.println("Min Key: " + ipq.peekMinKey() + " | Min Value: " + ipq.peekMinValue()); // Vertex 1, Dist 30

        System.out.println("Executing decreaseKey(0, 10)...");
        ipq.decreaseKey(0, 10); // Vertex 0 updated to dist 10

        System.out.println("New Min Key: " + ipq.peekMinKey() + " | Min Value: " + ipq.peekMinValue()); // Vertex 0, Dist 10

        System.out.println("\n=== 2. Dijkstra Shortest Path with IPQ ===");
        int V = 5;
        List<List<IndexedPriorityQueueMaster.Edge>> adj = new ArrayList<>();
        for (int i = 0; i < V; i++) adj.add(new ArrayList<>());

        adj.get(0).add(new IndexedPriorityQueueMaster.Edge(1, 4));
        adj.get(0).add(new IndexedPriorityQueueMaster.Edge(2, 1));
        adj.get(2).add(new IndexedPriorityQueueMaster.Edge(1, 2));
        adj.get(1).add(new IndexedPriorityQueueMaster.Edge(3, 1));
        adj.get(2).add(new IndexedPriorityQueueMaster.Edge(3, 5));

        int[] dist = IndexedPriorityQueueMaster.dijkstraIPQ(V, adj, 0);
        System.out.println("Shortest Distances from Src 0: " + Arrays.toString(dist)); // Output: [0, 3, 1, 4, INF]
    }
}
```

---

## 9. Complexity Analysis

| IPQ Method | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`insert(ki, val)`** | **$O(\log N)$ Logarithmic⚡**| $O(1)$ | Position map assignment `pm[ki] = size` |
| **`decreaseKey(ki, val)`**| **$O(\log N)$ Logarithmic⚡**| $O(1)$ | Direct $O(1)$ position lookup via `pm[ki]` |
| **`delete(ki)`** | **$O(\log N)$ Logarithmic⚡**| $O(1)$ | Swap with last element + `siftDown` |
| **Space Footprint** | $O(N)$ Linear | **3 Arrays of Size $N$ ⚡**| `values[]`, `pm[]`, `im[]` |

---

## 10. Edge Cases & Boundary Handling
* **Key Index Out of Bounds**: `ki < 0 || ki >= maxSize` throws `IndexOutOfBoundsException`.
* **Decreasing Key with Larger Value**: `decreaseKey(ki, val)` throws `IllegalArgumentException` if `val >= values[ki]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Swap Position Maps in `swap(i, j)`**:
  - Only swapping `im[i]` and `im[j]` without updating `pm[im[i]] = j` breaks position lookups permanently!
  - **Always update BOTH `pm` and `im` simultaneously in `swap()`**.
* **Lazy Deletion Duplicates in Java Standard `PriorityQueue`**: Standard `PriorityQueue` without IPQ requires pushing duplicate node entries `(dist, v)` into the queue, causing queue size to grow to $O(E)$ instead of $O(V)$!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Standard PQ Lazy Dijkstra vs IPQ Dijkstra:
> * **Standard PQ (Lazy Deletion)**: Pushes duplicate `(dist, v)` pairs. Heap size can reach $O(E)$. Time: $O(E \log E) = O(E \log V)$, Memory: $O(E)$.
> * **Indexed PQ**: Updates distances in-place via `decreaseKey(v, newDist)`. Heap size is strictly bounded by $O(V)$. Time: **$O(E \log V)$**, Memory: **$O(V)$**.

> **Memory Trick:** **"IPQ keeps heap size <= V! In-place decreaseKey replaces duplicate PQ node pushes!"**

---

## 13. System & Implementation Comparisons

| Feature | Standard `PriorityQueue` Dijkstra | Indexed Priority Queue (IPQ) Dijkstra |
| :--- | :--- | :--- |
| **Max Heap Size** | Up to $O(E)$ (Duplicate nodes) | **Strictly bounded by $O(V)$ ⚡** |
| **`decreaseKey` Time** | $O(N)$ Linear (or duplicate push) | **$O(\log V)$ In-Place Logarithmic ⚡** |
| **Memory Footprint** | $O(E)$ Array | **$O(V)$ 3 Mapping Arrays ⚡** |

---

## 14. How to Recognize This in Questions
* **"Implement Dijkstra's algorithm without duplicate vertex pushes in priority queue"** $\rightarrow$ Indexed Priority Queue (`IndexMinPQ`).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `swap(i, j)` update both `pm` and `im` in an Indexed Priority Queue?**  
  *A:* `pm[im[i]] = j` updates the position of the key index currently at position `i` to `j`. `pm[im[j]] = i` updates the position of the key index at `j` to `i`. Then `im[i]` and `im[j]` are swapped.
* **Q: Why does IPQ keep memory strictly bounded to $O(V)$ in graph algorithms?**  
  *A:* Because each vertex ID $v \in [0 \dots V-1]$ exists at most ONCE in the IPQ. Instead of pushing duplicate nodes when a shorter path is discovered, `decreaseKey(v, newDist)` updates vertex $v$'s priority in-place.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: INDEXED PRIORITY QUEUE (IPQ) ARCHITECTURE             |
+-----------------------------------------------------------------------+
| • 3 Arrays: values[ki] (Priority), pm[ki] (Pos Map), im[pos] (Inv Map)|
| • Direct Lookup: Position of key index ki in heap is pm[ki]           |
| • Inverse Lookup: Key index at heap position pos is im[pos]           |
| • Dual Swap: Must swap pm[im[i]] = j and im[i] = im[j] in sync        |
| • Decrease-Key: values[ki] = newVal -> siftUp(pm[ki]) in O(log N)     |
| • Dijkstra Advantage: Bounds heap size to O(V); O(E log V) Time       |
| • Space: Strictly O(V) memory allocation                              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the 3-array IPQ data structures (`values`, `pm`, `im`).
- [ ] I can write the dual-swap `swap(i, j)` updating `pm` and `im`.
- [ ] I can implement `decreaseKey(ki, newVal)` in $O(\log N)$ time.
- [ ] I know why IPQ bounds Dijkstra heap memory to $O(V)$.
- [ ] I can write Dijkstra's algorithm with `IndexMinPQ`.
