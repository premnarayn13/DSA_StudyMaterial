# 02. Binary Heap Implementation, Sift-Up & Sift-Down Percolate Engines

## 1. Introduction
Implementing a custom **Binary Heap** from scratch requires maintaining the Complete Binary Tree structural invariant and Min/Max ordering invariant during dynamic modifications. By implementing **`siftUp` (`percolateUp`)** for insertion (`offer`) and **`siftDown` (`percolateDown`)** for removal (`poll`), a custom Binary Heap guarantees **$O(1)$ Minimum/Maximum Retrieval** and **$O(\log N)$ Insertion and Deletion operations**.

> **Important:** The Two Core Re-balancing Percolate Engines:
> 1. **`siftUp(index)`**: Used during **`offer(val)`**. Appends new element to array end, then bubbles it UP by swapping with its parent while `element < parent`!
> 2. **`siftDown(index)`**: Used during **`poll()`**. Replaces root element with last element, then bubbles it DOWN by swapping with its **SMALLEST CHILD** while `element > child`! ⚡

```
Sift-Up vs Sift-Down Percolation Topology:
Sift-Up (Insertion - Bottom-Up) : [ New Elem ] --Bubbles Up--> Parent (if Elem < Parent)
Sift-Down (Removal - Top-Down)  : [ Root Swap ] --Bubbles Down-> Smallest Child (if Root > Child) ⚡
```

---

## 2. Core Concepts & Sift-Up / Sift-Down Mechanics

### 2.1 Sift-Up (`percolateUp`) Mechanics
When a new element is offered to the heap:
1. Increment `size++` and place element at `elements[size - 1]`.
2. `curr = size - 1`.
3. While `curr > 0`:
   - `parent = (curr - 1) / 2`.
   - If `elements[curr] < elements[parent]` (for Min Heap):
     - Swap `elements[curr]` and `elements[parent]`.
     - `curr = parent`.
   - Else: Break loop! Order restored!

### 2.2 Sift-Down (`percolateDown`) Mechanics
When the minimum element at `elements[0]` is polled:
1. Store result `minVal = elements[0]`.
2. Overwrite `elements[0] = elements[size - 1]`. Decrement `size--`.
3. `curr = 0`.
4. While `hasLeftChild(curr)`:
   - Identify **SMALLEST CHILD**:
     - `smallestChild = leftChild`.
     - If `hasRightChild(curr)` AND `rightChild < leftChild`, `smallestChild = rightChild`.
   - If `elements[curr] > elements[smallestChild]`:
     - Swap `elements[curr]` and `elements[smallestChild]`.
     - `curr = smallestChild`.
   - Else: Break loop! Order restored!

```
Binary Heap Method Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Heap Operation Method | Average Time      | Worst Case Time   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **`peek()`**          | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(1)$ Space      |
| **`offer(val)`**      | **$O(1)$ Amortized ⚡**| **$O(\log N)$ ⚡**| $O(1)$ Space      |
| **`poll()`**          | **$O(\log N)$ ⚡**| **$O(\log N)$ ⚡**| $O(1)$ Space      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sift-Up bubbles new elements UP to parent! Sift-Down bubbles root DOWN to smallest child!"**

---

## 3. Characteristics & Smallest Child Swap Requirement

### 3.1 Why Sift-Down MUST Swap with SMALLEST Child (Min Heap)
When sifting down an element in a Min Heap with two child nodes (e.g. parent 20, left child 10, right child 5):
* Swapping parent 20 with left child 10 produces parent 10, left 20, right 5 $\rightarrow$ VIOLATION! (Parent 10 > Right child 5!).
* **Rule**: Sift-Down MUST ALWAYS swap with the **SMALLEST CHILD**!
* Swapping 20 with right child 5 produces parent 5, left 10, right 20 $\rightarrow$ VALID MIN HEAP! ⚡

---

## 4. Internal Working Mechanics
Tracing `poll()` on Min Heap `[2, 10, 5, 12, 15]`:

```
Init: Poll root 2. Last element 15 replaces root -> Array: [15, 10, 5, 12]. size = 4.

Sift-Down from Index 0 (val 15):
- Children of Index 0: Left 10 (idx 1), Right 5 (idx 2).
- Smallest Child = Right Child 5 (idx 2).
- 15 > 5 -> Swap 15 and 5! Array becomes: [5, 10, 15, 12].
- Move curr = 2 (val 15).

Children of Index 2: Left (2*2+1 = 5) >= size 4 (No children!).
Loop terminates!

Final Polled Min Heap = [5, 10, 15, 12] in Valid Order! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Sift-Down Smallest Child Swap Topography:

```
Before Sift-Down:             Swap with SMALLEST Child (5):      After Sift-Down:
       [ 15 ]                             [ 5 ]                       [ 5 ]
      /      \                           /     \                     /     \
   [ 10 ]   [ 5 ]                      [ 10 ] [ 15 ]               [ 10 ] [ 15 ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a custom dynamic Resizing Min Heap (`CustomMinHeap`):

```java
import java.util.*;

public class BinaryHeapImplementationMaster {

    // Complete Production-Grade Dynamic Resizing Min Heap Implementation
    public static class CustomMinHeap {
        private int[] elements;
        private int capacity;
        private int size;

        public CustomMinHeap(int initialCapacity) {
            this.capacity = initialCapacity;
            this.elements = new int[initialCapacity];
            this.size = 0;
        }

        // O(1) Constant Time Peek
        public int peek() {
            if (isEmpty()) throw new NoSuchElementException("Heap is empty!");
            return elements[0];
        }

        // O(log N) Amortized Offer / Push
        public void offer(int val) {
            if (size == capacity) {
                resize(capacity * 2); // Double capacity on overflow
            }
            elements[size] = val;
            size++;
            siftUp(size - 1); // Bubble up new element
        }

        // O(log N) Poll / Pop
        public int poll() {
            if (isEmpty()) throw new NoSuchElementException("Heap is empty!");

            int minVal = elements[0];
            elements[0] = elements[size - 1]; // Overwrite root with last element
            size--;

            if (size > 0) {
                siftDown(0); // Bubble down new root to restore min heap order
            }

            return minVal;
        }

        // Sift-Up (Percolate Up): Bottom-Up Rebalancing
        private void siftUp(int index) {
            int curr = index;
            while (curr > 0) {
                int parent = (curr - 1) / 2;
                if (elements[curr] < elements[parent]) {
                    swap(curr, parent);
                    curr = parent;
                } else {
                    break;
                }
            }
        }

        // Sift-Down (Percolate Down): Top-Down Rebalancing
        private void siftDown(int index) {
            int curr = index;
            while (2 * curr + 1 < size) { // While left child exists
                int leftChild = 2 * curr + 1;
                int rightChild = 2 * curr + 2;
                int smallestChild = leftChild;

                // Select smallest child
                if (rightChild < size && elements[rightChild] < elements[leftChild]) {
                    smallestChild = rightChild;
                }

                if (elements[curr] > elements[smallestChild]) {
                    swap(curr, smallestChild);
                    curr = smallestChild;
                } else {
                    break;
                }
            }
        }

        private void swap(int i, int j) {
            int temp = elements[i];
            elements[i] = elements[j];
            elements[j] = temp;
        }

        private void resize(int newCap) {
            this.capacity = newCap;
            this.elements = Arrays.copyOf(this.elements, newCap);
        }

        public int size() { return size; }
        public boolean isEmpty() { return size == 0; }
    }
}
```

> **Quick Syntax:**
```java
// Sift-Down Smallest Child Selection Lines
int smallestChild = leftChild;
if (rightChild < size && elements[rightChild] < elements[leftChild]) smallestChild = rightChild;
```

---

## 7. Concrete Problem Examples
* **Java `java.util.PriorityQueue`**: Array-backed heap implementation.
* **Top K Streaming Elements**: Constant size Min Heap maintenance.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `CustomMinHeap` offer, poll, and dynamic resizing:

```java
public class BinaryHeapImplementationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Custom Min Heap Test ===");
        BinaryHeapImplementationMaster.CustomMinHeap minHeap = 
            new BinaryHeapImplementationMaster.CustomMinHeap(2); // Small initial capacity

        minHeap.offer(15);
        minHeap.offer(10);
        minHeap.offer(5);  // Triggers resize and sifts 5 to root!
        minHeap.offer(20);

        System.out.println("Min Element (peek): " + minHeap.peek()); // Output: 5
        System.out.println("Polled Min: " + minHeap.poll());         // Output: 5
        System.out.println("New Min (peek): " + minHeap.peek());     // Output: 10
        System.out.println("Polled Min: " + minHeap.poll());         // Output: 10 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Method | Average Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **`peek()`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Access `elements[0]` |
| **`offer(val)`** | **$O(1)$ Amortized ⚡** | **$O(\log N)$ ⚡** | $O(1)$ Space | Sift-up swaps |
| **`poll()`** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | $O(1)$ Space | Sift-down swaps |

---

## 10. Edge Cases & Boundary Handling
* **Polling Single Element Heap**: Size becomes 0, no `siftDown` executed.
* **Polling Empty Heap**: Throws `NoSuchElementException`.

---

## 11. Common Mistakes & Anti-Patterns
* **Swapping with Larger Child During Sift-Down**:
  - Swapping parent with the larger child violates min heap property against the smaller child!
  - **ALWAYS identify and swap with the SMALLEST CHILD**.
* **Forgetting Boundary Check `rightChild < size`**:
  - Accessing `elements[rightChild]` without verifying `rightChild < size` causes `ArrayIndexOutOfBoundsException`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Sift-Up vs Sift-Down Comparison:
> * **`siftUp`**: Moves a single element UP to find its correct position. Compares element with 1 Parent. At most $H = \log N$ comparisons!
> * **`siftDown`**: Moves a single element DOWN to find its correct position. Compares element with 2 Children. At most $2H = 2 \log N$ comparisons!

> **Memory Trick:** **"Sift-Up compares with 1 Parent; Sift-Down compares with 2 Children to find smallest child!"**

---

## 13. System & Implementation Comparisons

| Feature | Sift-Up (`percolateUp`) | Sift-Down (`percolateDown`) |
| :--- | :--- | :--- |
| **Primary Use Case** | Used during **`offer()`** insertion | Used during **`poll()`** removal & **`heapify()`** |
| **Comparisons per Step**| **1 Comparison (Parent)** | **2 Comparisons (Left vs Right child)** |
| **Direction** | Bottom-Up (Index $N-1 \to 0$) | Top-Down (Index $0 \to N-1$) |

---

## 14. How to Recognize This in Questions
* **"Implement a PriorityQueue from scratch"** $\rightarrow$ Binary Heap with `siftUp` and `siftDown`.
* **"Maintain dynamic min/max element in O(log N) time"** $\rightarrow$ Binary Heap.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `offer()` run in $O(1)$ amortized time?**  
  *A:* Because in a complete binary tree, 50% of all nodes reside in the bottom leaf level. Most inserted elements sift up only 1 or 2 levels before finding their correct position, averaging $O(1)$ time.
* **Q: How does a Max Heap differ from a Min Heap implementation?**  
  *A:* In a Max Heap, `siftUp` swaps while `element > parent`, and `siftDown` swaps with the **LARGEST CHILD** while `element < largestChild`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY HEAP IMPLEMENTATION                            |
+-----------------------------------------------------------------------+
| • Offer (Insert): Add to end -> siftUp(size - 1)                      |
| • Poll (Remove): Overwrite root with last elem -> siftDown(0)         |
| • Sift-Up Rule : Swap with parent while curr < parent                 |
| • Sift-Down Rule: Swap with SMALLEST child while curr > smallestChild |
| • Peak Time: O(1) | Offer Time: O(log N) | Poll Time: O(log N) ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a complete custom `MinHeap` from scratch.
- [ ] I can implement `siftUp` and `siftDown` methods.
- [ ] I know why siftDown MUST swap with the smallest child.
- [ ] I know how dynamic resizing works in array heaps.
- [ ] I can state the differences between Min Heap and Max Heap implementations.
