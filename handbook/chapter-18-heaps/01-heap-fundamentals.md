# 01. Heap Fundamentals, Complete Binary Tree Property & Priority Queue Invariants

## 1. Introduction
A **Heap** is a specialized tree-based data structure that satisfies the **Heap Property** while maintaining the structural shape of a **Complete Binary Tree**. Heaps serve as the computational backbone for **Priority Queues**, Dijkstra's Shortest Path Algorithm, Prim's Minimum Spanning Tree, **Heapsort ($O(N \log N)$)**, and Top-K streaming analytics. By storing elements in a contiguous 1D array without explicit node pointers, Heaps achieve **$O(1)$ Minimum / Maximum Retrieval**, **$O(\log N)$ Insertion and Deletion**, and **Optimal CPU Cache Locality**.

> **Important:** The Two Foundational Properties of a Binary Heap:
> 1. **Structural Invariant (Complete Binary Tree)**: Every level of the tree is completely filled except possibly the last level, and all nodes in the last level are filled as far **LEFT** as possible.
> 2. **Order Invariant (Heap Property)**:
>    - **Min Heap**: For every node $X$ (except the root), $\text{Key}(\text{parent}(X)) \le \text{Key}(X)$. Root contains the **GLOBAL MINIMUM**!
>    - **Max Heap**: For every node $X$ (except the root), $\text{Key}(\text{parent}(X)) \ge \text{Key}(X)$. Root contains the **GLOBAL MAXIMUM**! ⚡

```
Min Heap vs Max Heap Array Representation Topology:
Min Heap Topology (Root is Min):           Max Heap Topology (Root is Max):
             [ 2 ]                                      [ 100 ]
            /     \                                    /       \
        [ 5 ]     [ 8 ]                            [ 80 ]     [ 90 ]
       /     \                                    /      \
    [ 12 ]  [ 15 ]                             [ 30 ]   [ 40 ]

Array: [ 2, 5, 8, 12, 15 ] (0-indexed)     Array: [ 100, 80, 90, 30, 40 ]
```

---

## 2. Core Concepts & Array Index Navigation Mechanics

### 2.1 0-Indexed Array Mapping Formulas
Because a Binary Heap is a Complete Binary Tree, it can be mapped into a 1D array without storing left, right, or parent pointers!
For any element sitting at array index **$i$**:

* **Left Child Index**: $$\text{left}(i) = 2i + 1$$
* **Right Child Index**: $$\text{right}(i) = 2i + 2$$
* **Parent Index**: $$\text{parent}(i) = \left\lfloor \frac{i - 1}{2} \right\rfloor$$

```
Array Index Navigation Spectrum (0-Indexed):
+-----------------------+-------------------+-------------------+-------------------+
| Target Navigation     | Mathematical Formula| Array Index (i=1) | Target Result     |
+-----------------------+-------------------+-------------------+-------------------+
| Left Child of i=1     | $2(1) + 1$        | Index 3           | Left Child        |
| Right Child of i=1    | $2(1) + 2$        | Index 4           | Right Child       |
| Parent of i=3         | $(3 - 1) / 2$     | Index 1           | Parent Node       |
| Parent of i=4         | $(4 - 1) / 2$     | Index 1           | Parent Node       |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Left Child = 2i + 1! Right Child = 2i + 2! Parent = (i - 1) / 2!"**

---

## 3. Characteristics & 1-Indexed Alternative Mapping

### 3.1 1-Indexed Array Mapping Formulas (Legacy & Textbook Convention)
In 1-indexed heap arrays (where index 0 is left empty as a sentinel):
* **Left Child**: $\text{left}(i) = 2i$ (Bitwise left shift `i << 1`).
* **Right Child**: $\text{right}(i) = 2i + 1$ (Bitwise `(i << 1) | 1`).
* **Parent**: $\text{parent}(i) = \lfloor i / 2 \rfloor$ (Bitwise right shift `i >> 1`).
* **Advantage**: Multiplication and division by 2 convert into single-cycle CPU bit-shifting instructions!

---

## 4. Internal Working Mechanics
Tracing Min Heap vs Max Heap Operational Contracts:

```
Min Heap Operational Contract:
- peek() / getMin() : Returns array[0] in O(1) Constant Time.
- offer(val) / add(): Appends to end of array, then siftUp() in O(log N) Time.
- poll() / remove() : Overwrites array[0] with last element, then siftDown() in O(log N) Time.

Heap Invariants preserve strict log(N) tree height! ✅
```

---

## 5. Visual Diagram
Array Index Navigation & Tree Equivalence Topography:

```
Tree Representation:                  Array Representation (0-Indexed):
          [0: 10]                      Index:  0    1    2    3    4    5
         /       \                     Value: [10 | 20 | 15 | 30 | 40 | 50]
     [1: 20]   [2: 15]                        ^    ^----+----^    ^----+----^
     /     \     /                             |    Left/Right     Left/Right
  [3:30] [4:40][5:50]                         Root  Children (1)   Children (2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java simulation demonstrating Array Index Navigation, Heap Property Verification, and Min/Max Heap Classification:

```java
import java.util.*;

public class HeapFundamentalsMaster {

    // Helper utilities for 0-Indexed Array Navigation
    public static int getLeftChildIndex(int parentIndex) {
        return 2 * parentIndex + 1;
    }

    public static int getRightChildIndex(int parentIndex) {
        return 2 * parentIndex + 2;
    }

    public static int getParentIndex(int childIndex) {
        return (childIndex - 1) / 2;
    }

    // 1. Verify Min Heap Property O(N) Time, O(1) Space
    public static boolean isMinHeap(int[] arr) {
        if (arr == null || arr.length <= 1) return true;

        int n = arr.length;
        // Check all internal nodes (indices 0 to (N-2)/2)
        for (int i = 0; i <= (n - 2) / 2; i++) {
            int left = getLeftChildIndex(i);
            int right = getRightChildIndex(i);

            if (left < n && arr[i] > arr[left]) {
                return false; // Min Heap Violation! Parent > Left Child
            }

            if (right < n && arr[i] > arr[right]) {
                return false; // Min Heap Violation! Parent > Right Child
            }
        }

        return true;
    }

    // 2. Verify Max Heap Property O(N) Time, O(1) Space
    public static boolean isMaxHeap(int[] arr) {
        if (arr == null || arr.length <= 1) return true;

        int n = arr.length;
        for (int i = 0; i <= (n - 2) / 2; i++) {
            int left = getLeftChildIndex(i);
            int right = getRightChildIndex(i);

            if (left < n && arr[i] < arr[left]) {
                return false; // Max Heap Violation! Parent < Left Child
            }

            if (right < n && arr[i] < arr[right]) {
                return false; // Max Heap Violation! Parent < Right Child
            }
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// 0-Indexed Parent Formula
int parentIdx = (i - 1) / 2;
```

---

## 7. Concrete Problem Examples
* **Priority Queue Runtime Engines**: Array-backed Min/Max Heaps.
* **LeetCode 215 - Kth Largest Element in an Array**: Min Heap top-K extraction.
* **Dijkstra's Shortest Path Algorithm**: Min Heap priority queue distance updates.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Min Heap and Max Heap array property verifiers:

```java
public class HeapFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Min Heap Property Verification ===");
        int[] minHeapArr = {2, 5, 8, 12, 15};
        int[] invalidHeap = {10, 5, 20};

        System.out.println("Is [2, 5, 8, 12, 15] a Min Heap? " + 
            HeapFundamentalsMaster.isMinHeap(minHeapArr)); // true

        System.out.println("Is [10, 5, 20] a Min Heap? " + 
            HeapFundamentalsMaster.isMinHeap(invalidHeap)); // false (5 < 10!)

        System.out.println("\n=== 2. Max Heap Property Verification ===");
        int[] maxHeapArr = {100, 80, 90, 30, 40};
        System.out.println("Is [100, 80, 90, 30, 40] a Max Heap? " + 
            HeapFundamentalsMaster.isMaxHeap(maxHeapArr)); // true ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Metric | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Get Min / Max (`peek`)**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | Access `array[0]` directly |
| **Heap Verification** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡** | Scan internal nodes $0 \dots (N-2)/2$ |
| **Index Navigation** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | Direct arithmetic formulas |

---

## 10. Edge Cases & Boundary Handling
* **Empty or 1-Element Array**: `isMinHeap` and `isMaxHeap` return `true` automatically.
* **Out-of-Bound Child Indices**: Checked via `left < n` and `right < n` before comparing child values.

---

## 11. Common Mistakes & Anti-Patterns
* **Confusing Min Heap Property with Sorted Array**:
  - A Min Heap is NOT a sorted array! In a Min Heap array `[2, 8, 5, 12, 15]`, element 8 precedes 5.
  - **Min Heap ONLY guarantees Parent $\le$ Children, not sibling ordering**.
* **Off-by-One Parent Formula Error**:
  - Writing `i / 2` for 0-indexed arrays calculates the wrong parent index for odd numbers (e.g. `1 / 2 = 0`, but `2 / 2 = 1` wrong!).
  - **Always use `(i - 1) / 2` for 0-indexed arrays**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Internal Nodes Range in Complete Binary Tree:
> In a 0-indexed complete binary tree of $N$ nodes:
> * All **Internal Nodes** reside at indices **$0 \dots \lfloor \frac{N-2}{2} \rfloor$**.
> * All **Leaf Nodes** reside at indices **$\lfloor \frac{N}{2} \rfloor \dots N-1$**.
> This distinction allows heap verification and `heapify()` to process ONLY internal nodes!

> **Memory Trick:** **"Internal nodes reside at indices 0 to (N-2)/2! Leaves start at N/2!"**

---

## 13. System & Implementation Comparisons

| Feature | Contiguous Array Heap | Pointer-Based Node Tree |
| :--- | :--- | :--- |
| **CPU Cache Locality** | **Optimal (Contiguous Memory) ⚡**| Poor (Heap Pointer Chasing) |
| **Parent/Child Links** | Direct Arithmetic Formula | 24 Bytes Reference Overhead |
| **Tree Completeness** | Always Complete Binary Tree | Flexible Shapes |

---

## 14. How to Recognize This in Questions
* **"Retrieve minimum/maximum element in O(1) constant time"** $\rightarrow$ Min / Max Heap.
* **"Determine if array represents a valid complete binary heap"** $\rightarrow$ Check parent-child heap property.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Binary Heap use an Array instead of Node objects?**  
  *A:* Complete binary trees can map perfectly into contiguous 1D arrays without missing slots. Array storage eliminates 24-byte node object pointer overheads and provides maximum CPU L1/L2 cache line locality.
* **Q: What is the height $H$ of a Binary Heap with $N$ nodes?**  
  *A:* Height $H = \lfloor \log_2 N \rfloor$, guaranteeing logarithmic bounds for insertion and deletion operations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HEAP FUNDAMENTALS & ARRAY NAVIGATION                  |
+-----------------------------------------------------------------------+
| • Min Heap Property: Parent <= Children; Root = Global Minimum        |
| • Max Heap Property: Parent >= Children; Root = Global Maximum        |
| • Left Child Formula : 2i + 1                                         |
| • Right Child Formula: 2i + 2                                         |
| • Parent Formula     : (i - 1) / 2                                    |
| • Internal Nodes Range: 0 to (N - 2) / 2                              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can state the 0-indexed array navigation formulas for left, right, and parent.
- [ ] I can write `isMinHeap` and `isMaxHeap` verifiers.
- [ ] I know why array heaps outperform pointer-based trees in cache performance.
- [ ] I know the index range of internal nodes `0 ... (N-2)/2`.
- [ ] I know why a Min Heap is NOT a fully sorted array.
