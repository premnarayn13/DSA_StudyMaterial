# 07. Heap Sort: Max-Heap Invariants, In-Place Heapify & $O(1)$ Auxiliary Memory

## 1. Introduction
**Heap Sort** is a comparison-based sorting algorithm that combines the strict **$O(N \log N)$ Time Guarantee** of Merge Sort with the **$O(1)$ Auxiliary Memory Space** of Selection Sort. By representing an array as an implicit complete binary **Max-Heap**, Heap Sort converts sorting into two sequential operational phases: (1) **Build Max-Heap** in $O(N)$ time using bottom-up `siftDown` heapification, and (2) **Extraction Phase** in $O(N \log N)$ time, repeatedly swapping the root (maximum element) with the last unsorted array position and restoring the heap property over the shrinking prefix.

> **Important:** Core Invariants of Heap Sort:
> 1. **Max-Heap Property**: For every node at index $i$, the parent value is greater than or equal to both child values:
>    $$\text{arr}[i] \ge \text{arr}[2i + 1] \quad \text{and} \quad \text{arr}[i] \ge \text{arr}[2i + 2]$$
> 2. **Bottom-Up $O(N)$ Build Heap**: Heapifying nodes starting from the last non-leaf parent $\lfloor N/2 \rfloor - 1$ down to root index $0$ constructs a Max-Heap in **$O(N)$ Linear Time** (NOT $O(N \log N)$!).
> 3. **Strict $O(1)$ In-Place Memory**: Operates directly within the input array via index arithmetic, avoiding call stack recursion or auxiliary array allocations.
> 4. **Instability Invariant**: Non-adjacent root-to-leaf swaps break the relative input order of equal keys, rendering Heap Sort **Unstable**. ⚡

```
Array Implicit Max-Heap Tree Topology (arr = [4, 10, 3, 5, 1]):
Array Indices: [ 0,  1,  2,  3,  4 ]
Values:        [ 4, 10,  3,  5,  1 ]

Implicit Tree View:                10 (Index 1, Parent of 5 & 1)
                                 /    \
            (Root Index 0)      4      3 (Index 2)
                              /   \
          (Index 3)          5     1 (Index 4)

Max-Heapify(0): Swaps 4 with 10 -> Max-Heap Formed! ⚡
```

---

## 2. Core Concepts & Heap Sort Strategy Matrix

### 2.1 Heap Sort Strategy Matrix
```
Heap Sort Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Phase                 | Primary Operation | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **Phase 1: Build Heap**| Bottom-Up `siftDown`| **$O(N)$ Linear ⚡**| **$O(1)$ In-Place ⚡**|
| **Phase 2: Extract**  | Swap Root + Heapify| **$O(N \log N)$ ⚡** | **$O(1)$ In-Place ⚡**|
| **Overall Algorithm** | Heap Sort Engine  | **$O(N \log N)$ Strict**| **$O(1)$ In-Place ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Build Max-Heap in O(N) time! Swap root to end and heapify down in O(N log N) total!"**

---

## 3. Characteristics & $O(N)$ Build Heap Mathematical Proof

### 3.1 Mathematical Proof of $O(N)$ Linear Build Heap Time
* A complete binary tree of height $H = \lfloor \log_2 N \rfloor$ has $2^h$ nodes at height $h$ above the leaves.
* Moving a node down height $h$ takes at most $h$ comparisons.
* Sum of all `siftDown` operations across the tree:
  $$T(N) = \sum_{h=0}^{\log_2 N} \frac{N}{2^{h+1}} \cdot h = \frac{N}{2} \sum_{h=0}^{\infty} \frac{h}{2^h}$$
* The infinite series $\sum_{h=0}^{\infty} \frac{h}{2^h} = 2$.
* Total Build Heap Work: $T(N) = \frac{N}{2} \cdot 2 = \mathbf{O(N) \text{ Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Extraction Phase

Tracing Extraction Phase on Max-Heap `[ 10, 5, 3, 4, 1 ]` (N = 5):

```
Pass 1 (i = 4):
- Swap Root (10) at index 0 with Last Unsorted Element (1) at index 4.
- Array: [ 1, 5, 3, 4 | 10 ]  (10 locked at index 4!).
- Max-Heapify(0) on size 4: Sifts 1 down.
- Heap restored: [ 5, 4, 3, 1 | 10 ].

Pass 2 (i = 3):
- Swap Root (5) at index 0 with Last Unsorted Element (1) at index 3.
- Array: [ 1, 4, 3 | 5, 10 ]  (5 locked at index 3!).
- Max-Heapify(0) on size 3: Sifts 1 down.
- Heap restored: [ 4, 1, 3 | 5, 10 ].

Pass 3 & 4: Repeat until array is fully sorted!
Final Array: [ 1, 3, 4, 5, 10 ]! ✅ (Executed in O(1) Extra Space!)
```

---

## 5. Visual Diagram: Array Indexing to Tree Node Mapping

```
Parent and Child Index Arithmetic Equations:

            Parent Node Index: i
                 /        \
                /          \
Left Child: 2i + 1        Right Child: 2i + 2

Parent Index from Child: parent = (i - 1) / 2 ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Heap Sort, $O(N)$ Build Heap, and `siftDown` heapification.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Heap Sort Algorithms,
 * O(N) Build Heap Construction, and In-Place Max-Heapification.
 */
public class HeapSortMaster {

    // =========================================================================
    // 1. HEAP SORT ENGINE (O(N log N) Strict Time, O(1) Auxiliary Space)
    // =========================================================================
    /**
     * Sorts an array using in-place Heap Sort.
     * Guarantees O(N log N) worst-case time and O(1) auxiliary space.
     *
     * @param arr input integer array
     */
    public void heapSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;

        // Phase 1: Build Max-Heap in O(N) Linear Time
        // Start from last non-leaf parent node: (n / 2) - 1 down to 0
        for (int i = (n / 2) - 1; i >= 0; i--) {
            siftDown(arr, i, n);
        }

        // Phase 2: Extraction Phase in O(N log N) Time
        // Repeatedly swap root (max) to end and siftDown remaining heap
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);  // Swap max element to end of unsorted array
            siftDown(arr, 0, i); // Heapify reduced heap size i
        }
    }

    /**
     * Sifts node down at index i to restore Max-Heap property.
     *
     * @param arr array heap
     * @param i current parent index
     * @param heapSize current active heap boundary size
     */
    private void siftDown(int[] arr, int i, int heapSize) {
        int maxIndex = i;
        int leftChild = 2 * i + 1;
        int rightChild = 2 * i + 2;

        // Check if Left Child is larger than current parent
        if (leftChild < heapSize && arr[leftChild] > arr[maxIndex]) {
            maxIndex = leftChild;
        }

        // Check if Right Child is larger than max of parent and left child
        if (rightChild < heapSize && arr[rightChild] > arr[maxIndex]) {
            maxIndex = rightChild;
        }

        // If parent is not the maximum, swap and continue sifting down
        if (maxIndex != i) {
            swap(arr, i, maxIndex);
            siftDown(arr, maxIndex, heapSize); // Recurse on affected sub-tree
        }
    }

    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Parent / Child Index Arithmetic
int left = 2 * i + 1, right = 2 * i + 2, parent = (i - 1) / 2;
```

---

## 7. Concrete Problem Examples & Systems Integration

1. **Embedded Systems & Real-Time Kernel Solvers**:
   - Systems requiring **Strict $O(N \log N)$ Time** with zero memory allocations ($O(1)$ space).

2. **Top-K Element Priority Retrieval**:
   - Extracting K largest/smallest elements in $O(N + K \log N)$ time without full array sorting.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class HeapSortDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     HEAP SORT IN-PLACE DEMONSTRATION            ");
        System.out.println("=================================================\n");

        HeapSortMaster master = new HeapSortMaster();

        // 1. In-Place Heap Sort Test
        int[] arr = {4, 10, 3, 5, 1};
        System.out.println("1. Original Array for Heap Sort: " + Arrays.toString(arr));
        master.heapSort(arr);
        System.out.println("   Sorted Array (O(1) Space)   : " + Arrays.toString(arr));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Heap Sort Phase | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Build Max-Heap** | $\mathbf{O(N)}$ Linear ⚡ | $\mathbf{O(1)}$ Constant Space ⚡| Bottom-up `siftDown` |
| **Extraction Phase**| $\mathbf{O(N \log N)}$ Strict ⚡| $\mathbf{O(1)}$ Constant Space ⚡| Swap root + `siftDown` |
| **Overall HeapSort**| $\mathbf{O(N \log N)}$ Strict ⚡| $\mathbf{O(1)}$ Constant Space ⚡| In-place complete tree |

---

## 10. Edge Cases & Boundary Handling

1. **Array of Size 1**:
   - Handled by `(n / 2) - 1 = -1`, skipping Build Heap loop and returning immediately.

2. **Already Sorted Array**:
   - Still executes $O(N \log N)$ operations because Heap Sort is **Non-Adaptive**.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Building Heap via `siftUp` Insertions ($O(N \log N)$)**:
  - Inserting elements one-by-one via `siftUp` takes $O(N \log N)$ time. Bottom-up `siftDown` takes $O(N)$ linear time!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Heap Sort is Unstable:
> Root-to-leaf swaps move elements across long array distances, swapping non-adjacent equal keys out of order (e.g. `5[A]` at root swapped to end behind `5[B]`). Heap Sort is inherently **Unstable**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Heap Sort | Merge Sort | Quick Sort |
| :--- | :--- | :--- | :--- |
| **Time (Worst Case)** | **$O(N \log N)$ Strict ⚡** | **$O(N \log N)$ Strict ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| $O(N)$ Extra Memory | $O(\log N)$ Stack Space |
| **Stability** | Unstable | **Stable ⚡** | Unstable |

---

## 14. How to Recognize This in Questions

* **"Sort array in-place with guaranteed O(N log N) worst-case time and O(1) space"** $\rightarrow$ Heap Sort.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Build Heap take $O(N)$ linear time instead of $O(N \log N)$?**  
  *A:* Because most nodes reside near the bottom leaves of the tree (height $h = 0, 1$). `siftDown` performs very few operations for the vast majority of nodes.

* **Q: Why is Heap Sort rarely used as the default in-memory sorting engine?**  
  *A:* Because parent-child index jumps (`2i + 1`) cause frequent L1/L2 CPU cache line misses compared to QuickSort's contiguous memory scans.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: HEAP SORT                                             |
+-----------------------------------------------------------------------+
| • Max-Heap Invariant: arr[i] >= arr[2i + 1] and arr[i] >= arr[2i + 2] |
| • Build Heap Time   : O(N) Linear Time (siftDown from (n/2)-1 to 0)   |
| • Extract Phase     : Swap root with arr[i] and siftDown(0)           |
| • Performance       : Strict O(N log N) Time | O(1) In-Place Memory ⚡ |
| • Stability         : Unstable due to long-distance swaps ❌          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write in-place Heap Sort in Java.
- [ ] I can write `siftDown` heapification.
- [ ] I can prove why Build Heap takes $O(N)$ linear time.
- [ ] I can state parent/child index arithmetic formulas.
- [ ] I can explain why Heap Sort is unstable.
