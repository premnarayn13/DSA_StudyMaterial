# 01. Binary Heap Fundamentals, Array Representation & Percolate Operations

## 1. Introduction
A **Binary Heap** is a specialized non-linear tree-based data structure that satisfies two fundamental structural and order invariants: the **Complete Binary Tree Property** and the **Heap Order Property**. Binary Heaps serve as the primary underlying data structure for **Priority Queues** in modern runtime environments, operating system task schedulers, Dijkstra's Shortest Path Algorithm, Prim's Minimum Spanning Tree Algorithm, Huffman Compression Coding, and Heapsort.

> **Important:** Unlike general binary search trees that use node objects with pointers (`left` and `right`), a Binary Heap is represented as a contiguous **1D Array** without any node pointer overhead. Array indexing arithmetic (`left = 2i + 1`, `right = 2i + 2`, `parent = (i - 1) / 2`) guarantees **$O(1)$ constant time index navigation** and exceptional CPU L1 cache locality!

```
Binary Heap Array Mapping Invariant:
+-----------------------------------------------------------------------------------+
| Tree Topology : Complete Binary Tree (All levels full, last level left-aligned)   |
| Array Storage : Contiguous Array [Root at index 0, No Null Pointer Overhead ⚡]    |
| Order Invariant: Min-Heap (Parent <= Children) OR Max-Heap (Parent >= Children)   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Invariants

### 2.1 The Two Fundamental Heap Invariants

#### 1. Complete Binary Tree Structural Invariant
A Binary Heap is ALWAYS a **Complete Binary Tree**. Every level of the tree is completely filled with nodes, except possibly the last level, which MUST be filled sequentially from **left to right**.
* *Architectural Benefit*: Eliminates gaps in array storage, enabling seamless mapping to a contiguous 1D array.

#### 2. Heap Order Invariant
* **Min-Heap**: For every node $X$ other than the root:

$$\text{Parent}(X).\text{val} \le X.\text{val}$$

  The minimum element in the entire heap is ALWAYS located at the **Root Node** (`array[0]`).
* **Max-Heap**: For every node $X$ other than the root:

$$\text{Parent}(X).\text{val} \ge X.\text{val}$$

  The maximum element in the entire heap is ALWAYS located at the **Root Node** (`array[0]`).

```
Min-Heap vs Max-Heap Topology:
        Min-Heap (Root = Min)                   Max-Heap (Root = Max)
                ( 10 )                                  ( 90 )
               /      \                                /      \
            ( 15 )    ( 20 )                        ( 70 )    ( 50 )
           /      \                                /      \
        ( 30 )    ( 40 )                        ( 30 )    ( 40 )

Array: [10, 15, 20, 30, 40]             Array: [90, 70, 50, 30, 40]
```

### 2.2 1D Array Index Navigation Math
Let $i$ be the 0-based array index of a node:

* **Parent Index**: $\text{Parent}(i) = \lfloor \frac{i - 1}{2} \rfloor$ (`(i - 1) / 2`)
* **Left Child Index**: $\text{Left}(i) = 2i + 1$
* **Right Child Index**: $\text{Right}(i) = 2i + 2$
* **Is Leaf Node Check**: Node $i$ is a leaf if $2i + 1 \ge N$ (where $N$ is total element count). Leaf nodes occupy array indices $\lfloor N/2 \rfloor \dots N - 1$.

```
0-Based vs 1-Based Index Navigation Reference:
+-----------------------+-------------------+-------------------+
| Relationship Metric   | 0-Based Indexing  | 1-Based Indexing  |
+-----------------------+-------------------+-------------------+
| Root Index            | Index `0`         | Index `1`         |
| Parent of Index `i`   | `(i - 1) / 2`     | `i / 2`           |
| Left Child of `i`     | `2 * i + 1`       | `2 * i`           |
| Right Child of `i`    | `2 * i + 2`       | `2 * i + 1`       |
+-----------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Min-Heap root is MIN (array[0])! Parent at (i-1)/2, Left at 2i+1, Right at 2i+2!"**

---

## 3. Structural Shifts: Sift-Up & Sift-Down Mechanics

When elements are inserted into or removed from a heap, the heap order invariant may be temporarily violated. Two fundamental restoration routines—**Sift-Up (Percolate-Up)** and **Sift-Down (Percolate-Down)**—restore the order invariant in **$O(\log N)$ logarithmic time**.

### 3.1 Insertion & Sift-Up (Percolate-Up / Bubble-Up)
When inserting a new element `val`:
1. Append `val` at the end of the array (at index $N$, preserving the Complete Binary Tree structural invariant).
2. Increment element count $N++$.
3. Execute **`siftUp(N - 1)`**:
   - Compare node $i$ with its parent $P = (i - 1) / 2$.
   - If `array[i] < array[P]` (in a Min-Heap), swap `array[i]` and `array[P]`.
   - Update $i = P$ and repeat until the root is reached or `array[i] >= array[P]`.

### 3.2 Extract-Min/Max & Sift-Down (Percolate-Down / Bubble-Down)
When removing the root element:
1. Save the root element `minVal = array[0]`.
2. Move the **last element** of the array `array[N - 1]` to the root position `array[0]`.
3. Decrement element count $N--$.
4. Execute **`siftDown(0)`**:
   - Compare node $i$ with its left child ($2i + 1$) and right child ($2i + 2$).
   - Find the **smallest child** $S$ among valid children.
   - If `array[i] > array[S]` (in a Min-Heap), swap `array[i]` and `array[S]`.
   - Update $i = S$ and repeat until $i$ becomes a leaf node or `array[i] <= array[S]`.

```
Percolate Shift Operations Summary:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Name        | Trigger Event     | Movement Path     | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| `siftUp` (Bubble-Up)  | `insert(val)`     | Bottom-to-Top (Up)| $O(\log N)$ ⚡    |
| `siftDown` (Bubble-Dn)| `extractMin()`    | Top-to-Bottom(Dn) | $O(\log N)$ ⚡    |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Insertion of `5` into Min-Heap `[10, 15, 20, 30, 40]`:

```
Step 1: Append 5 at end -> Array: [10, 15, 20, 30, 40, 5] (index 5)

Tree View:
                ( 10 )
               /      \
            ( 15 )    ( 20 )
           /      \   /
        ( 30 )  ( 40)( 5 )

Step 2: Sift-Up(5):
- Compare 5 with Parent at index (5-1)/2 = 2 (val 20).
  5 < 20 -> Swap 5 and 20. Array: [10, 15, 5, 30, 40, 20]
- Compare 5 with Parent at index (2-1)/2 = 0 (val 10).
  5 < 10 -> Swap 5 and 10. Array: [5, 15, 10, 30, 40, 20]
- Reached Root (index 0). Sift-Up complete!

Final Heap: [5, 15, 10, 30, 40, 20] ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Min-Heap Array Storage and Index Mapping Topography:

```
Array Index:   [ 0 ]   [ 1 ]   [ 2 ]   [ 3 ]   [ 4 ]   [ 5 ]
Array Value:   ( 5 )   ( 15 )  ( 10 )  ( 30 )  ( 40 )  ( 20 )
                 |       |       |       |       |       |
                 +-------+-------+       |       |       |
                 |  L=1     R=2          |       |       |
                 v                       v       v       v
               ( 5 )                   ( 30 )  ( 40 )  ( 20 )
              /     \
          ( 15 )   ( 10 )
         /      \   /
      ( 30 )  ( 40)( 20 )
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a dynamic array-based `MinHeap` with full `siftUp`, `siftDown`, `insert`, `extractMin`, and `peek` operations:

```java
import java.util.*;

public class BinaryHeapMaster {

    public static class MinHeap {
        private int[] heap;
        private int size;
        private int capacity;

        public MinHeap(int initialCapacity) {
            this.capacity = initialCapacity;
            this.size = 0;
            this.heap = new int[initialCapacity];
        }

        public int size() {
            return size;
        }

        public boolean isEmpty() {
            return size == 0;
        }

        public int peek() {
            if (isEmpty()) throw new NoSuchElementException("Heap is empty!");
            return heap[0];
        }

        // 1. Insert Element O(log N) Time
        public void insert(int val) {
            ensureCapacity();
            heap[size] = val; // Place at end
            size++;
            siftUp(size - 1); // Percolate Up
        }

        // 2. Extract Minimum Element O(log N) Time
        public int extractMin() {
            if (isEmpty()) throw new NoSuchElementException("Heap is empty!");

            int minVal = heap[0];
            heap[0] = heap[size - 1]; // Move last element to root
            size--;

            if (size > 0) {
                siftDown(0); // Percolate Down
            }

            return minVal;
        }

        // 3. Sift-Up (Percolate Up) O(log N) Time
        private void siftUp(int index) {
            while (index > 0) {
                int parentIndex = (index - 1) / 2;
                if (heap[index] < heap[parentIndex]) {
                    swap(index, parentIndex);
                    index = parentIndex;
                } else {
                    break;
                }
            }
        }

        // 4. Sift-Down (Percolate Down) O(log N) Time
        private void siftDown(int index) {
            while (2 * index + 1 < size) { // While left child exists
                int leftChild = 2 * index + 1;
                int rightChild = 2 * index + 2;
                int smallest = leftChild;

                if (rightChild < size && heap[rightChild] < heap[leftChild]) {
                    smallest = rightChild;
                }

                if (heap[index] > heap[smallest]) {
                    swap(index, smallest);
                    index = smallest;
                } else {
                    break;
                }
            }
        }

        private void swap(int i, int j) {
            int temp = heap[i];
            heap[i] = heap[j];
            heap[j] = temp;
        }

        private void ensureCapacity() {
            if (size == capacity) {
                capacity *= 2;
                heap = Arrays.copyOf(heap, capacity);
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Sift-Down Child Index Calculation
int leftChild = 2 * index + 1;
int rightChild = 2 * index + 2;
int smallest = (rightChild < size && heap[rightChild] < heap[leftChild]) ? rightChild : leftChild;
```

---

## 7. Concrete Problem Examples
* **LeetCode 703 - Kth Largest Element in a Stream**: Fixed-size Min-Heap maintenance.
* **LeetCode 215 - Kth Largest Element in an Array**: Min-Heap vs Max-Heap partitioning.
* **Java `PriorityQueue` Internals**: Unbounded priority queue implemented via array min-heap.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing MinHeap insertions, peeking minimum element, and extracting elements in ascending sorted order:

```java
public class BinaryHeapDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Building Min-Heap ===");
        BinaryHeapMaster.MinHeap minHeap = new BinaryHeapMaster.MinHeap(10);

        int[] values = {40, 10, 30, 5, 20, 15};
        for (int v : values) {
            minHeap.insert(v);
            System.out.println("Inserted: " + v + " | Current Min (Peek): " + minHeap.peek());
        }

        System.out.println("\n=== 2. Extracting Elements in Sorted Order ===");
        System.out.print("Extracted Sequence: ");
        while (!minHeap.isEmpty()) {
            System.out.print(minHeap.extractMin() + " ");
        }
        System.out.println(); // Output: 5 10 15 20 30 40 (Sorted order!)
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`peek()`** | **$O(1)$ Constant ⚡** | $O(1)$ | Root element at `array[0]` |
| **`insert(val)`** | **$O(\log N)$ Logarithmic⚡**| $O(1)$ Space | Sift-Up through tree height $H$ |
| **`extractMin()`** | **$O(\log N)$ Logarithmic⚡**| $O(1)$ Space | Sift-Down through tree height $H$ |
| **Array Space** | $O(N)$ Linear | **Zero Pointers ⚡** | Contiguous 1D array storage |

---

## 10. Edge Cases & Boundary Handling
* **Extract from Empty Heap**: Throws `NoSuchElementException`.
* **Single Element Heap**: Extracting returns root, size becomes `0`, no sift-down required.
* **Inserting Duplicate Values**: Heap handles duplicate values seamlessly without violating invariants.

---

## 11. Common Mistakes & Anti-Patterns
* **Off-By-One Parent/Child Index Calculation**:
  - Writing `2 * i` for left child in 0-indexed arrays instead of `2 * i + 1`.
  - Always remember: **0-Indexed Left Child is `2i + 1`, Right Child is `2i + 2`, Parent is `(i - 1) / 2`**.
* **Evaluating Out-Of-Bounds Right Child**: Accessing `heap[rightChild]` without checking `rightChild < size` causes `ArrayIndexOutOfBoundsException`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Binary Heaps Use Array Representation over Node Objects:
> Node object trees require storing 2 pointer references (`left`, `right`) per node (16 bytes of pointer overhead on 64-bit JVMs).
> Array representation uses **zero pointer references**, provides $O(1)$ index navigation, and maximizes CPU L1 cache line pre-fetching efficiency!

> **Memory Trick:** **"Parent = (i-1)/2! Left = 2i+1! Right = 2i+2! Sift-Up for insert, Sift-Down for extract!"**

---

## 13. System & Implementation Comparisons

| Feature | Min-Heap | Max-Heap |
| :--- | :--- | :--- |
| **Root Value** | Minimum Element (`array[0]`) | Maximum Element (`array[0]`) |
| **Order Rule** | `parent <= child` | `parent >= child` |
| **Sift-Down Selection**| Swap with **Smaller Child** | Swap with **Larger Child** |

---

## 14. How to Recognize This in Questions
* **"Find K-th largest element in a stream"** $\rightarrow$ Min-Heap of size $K$.
* **"Continuously extract maximum/minimum priority element"** $\rightarrow$ Binary Heap (PriorityQueue).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is a Binary Heap's array representation cache-friendly?**  
  *A:* Because array elements are stored in contiguous memory locations. When the CPU accesses `heap[i]`, nearby child elements `heap[2i + 1]` and `heap[2i + 2]` are pre-fetched into the L1/L2 cache line automatically.
* **Q: What is the maximum height of a Binary Heap with $N$ nodes?**  
  *A:* Because a Binary Heap is a Complete Binary Tree, its height is strictly bounded by $H = \lfloor \log_2 N \rfloor = \mathbf{O(\log N)}$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY HEAP FUNDAMENTALS & ARRAY MATH                 |
+-----------------------------------------------------------------------+
| • Complete Binary Tree: Levels full, last level left-aligned          |
| • Min-Heap Invariant: Root is Minimum (parent <= child)               |
| • Max-Heap Invariant: Root is Maximum (parent >= child)               |
| • Index Math (0-Based): Parent (i-1)/2 | Left 2i+1 | Right 2i+2       |
| • Insert: Append at end -> Sift-Up (Bubble-Up) O(log N)               |
| • Extract-Min: Replace root with last element -> Sift-Down O(log N)   |
| • Space Advantage: Zero node pointer memory overhead!                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 0-indexed parent and child index formulas.
- [ ] I can implement `siftUp` and `siftDown` from scratch.
- [ ] I can implement `MinHeap` with `insert` and `extractMin`.
- [ ] I know why array heaps are CPU L1 cache friendly.
- [ ] I can state the height bound $H = \lfloor \log_2 N \rfloor$.
