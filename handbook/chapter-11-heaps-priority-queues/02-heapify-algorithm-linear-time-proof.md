# 02. Floyd's $O(N)$ Heapify Algorithm & Mathematical Proof of Linear Time

## 1. Introduction
Converting an unsorted array of $N$ elements into a valid Binary Heap is a foundational operation in computer science. While inserting $N$ elements one by one into an initially empty heap takes $O(N \log N)$ time, **Floyd's Heapify Algorithm** (bottom-up heap construction) converts an unsorted array into a heap in **Strict $O(N)$ Linear Time**. Understanding the mathematical proof behind this $O(N)$ time complexity is a classic senior engineering and competitive programming interview benchmark.

> **Important:** Floyd's Heapify Algorithm works **bottom-up**, starting from the last non-leaf node ($\text{startIndex} = \lfloor N/2 \rfloor - 1$) and calling `siftDown` on each internal node down to the root (`index 0`). This operates in $O(N)$ time because the vast majority of nodes reside near the bottom of the tree where the `siftDown` height $h$ is tiny!

```
Heap Construction Strategy Comparison:
+-----------------------------------------------------------------------------------+
| Naive Top-Down Insertions  : Call insert() N times       -> O(N log N) Time ❌    |
| Floyd's Bottom-Up Heapify  : Sift-Down from N/2-1 to 0  -> O(N) Linear Time ⚡     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & The Bottom-Up Heapify Algorithm

### 2.1 Why Naive Insertion Takes $O(N \log N)$ Time
If we build a heap by starting with an empty array and calling `insert(val)` (which calls `siftUp`) $N$ times:
* Leaves (at depth $\approx \log N$) are inserted last.
* Each leaf performs `siftUp` up through the full height of the tree ($\approx \log N$ swaps).
* Since there are $\approx N/2$ leaf nodes, the total work is:

$$W_{\text{naive}}(N) \approx \sum_{i=1}^{N} \log i = \log(N!) = \mathbf{O(N \log N)}$$

### 2.2 Floyd's Bottom-Up Heapify Algorithm ($O(N)$ Time)
Instead of sifting UP from the leaves, Floyd's algorithm operates **bottom-up** using `siftDown`:
1. Start at the **last non-leaf node**: $\text{startIndex} = \lfloor N/2 \rfloor - 1$.
   - Why? Nodes from index $\lfloor N/2 \rfloor$ to $N - 1$ are ALREADY leaf nodes (valid 1-element heaps of height 0!).
2. Iterate backwards from `i = startIndex` down to `i = 0`.
3. At each index `i`, execute **`siftDown(i)`**.

```
Floyd's Heapify Iteration Loop:
for (int i = (N / 2) - 1; i >= 0; i--) {
    siftDown(array, N, i);
}
```

> **Memory Trick:** **"Heapify starts at (N/2)-1 and loops BACKWARDS to 0 calling siftDown! Takes O(N) linear time!"**

---

## 3. Rigorous Mathematical Proof of $O(N)$ Linear Time

### 3.1 Step 1: Counting Nodes at Each Height
Consider a Perfect Binary Tree of height $H$ containing total nodes $N = 2^{H+1} - 1$:
* Nodes at height $h = 0$ (Leaves): $2^H \approx \mathbf{N/2\text{ nodes}}$. Max `siftDown` work = $0$.
* Nodes at height $h = 1$: $2^{H-1} \approx \mathbf{N/4\text{ nodes}}$. Max `siftDown` work = $1$.
* Nodes at height $h = 2$: $2^{H-2} \approx \mathbf{N/8\text{ nodes}}$. Max `siftDown` work = $2$.
* Nodes at height $h$: $2^{H-h}$ nodes. Max `siftDown` work = $h$.

### 3.2 Step 2: Formulating Total Work Sum $S$
The total number of `siftDown` swap operations $S$ is the sum of (number of nodes at height $h$) $\times$ (max height $h$):

$$S = \sum_{h=0}^{H} h \cdot 2^{H-h} = 2^H \sum_{h=0}^{H} \frac{h}{2^h}$$

### 3.3 Step 3: Evaluating the Arithmetico-Geometric Series
Let $A = \sum_{h=0}^{\infty} \frac{h}{2^h}$:

$$A = \frac{1}{2^1} + \frac{2}{2^2} + \frac{3}{2^3} + \frac{4}{2^4} + \dots \quad \text{--- (Equation 1)}$$

Multiply $A$ by $\frac{1}{2}$:

$$\frac{1}{2}A = \frac{1}{2^2} + \frac{2}{2^3} + \frac{3}{2^4} + \frac{4}{2^5} + \dots \quad \text{--- (Equation 2)}$$

Subtract Equation 2 from Equation 1:

$$A - \frac{1}{2}A = \frac{1}{2^1} + \left(\frac{2}{2^2} - \frac{1}{2^2}\right) + \left(\frac{3}{2^3} - \frac{2}{2^3}\right) + \left(\frac{4}{2^4} - \frac{3}{2^4}\right) + \dots$$

$$\frac{1}{2}A = \frac{1}{2^1} + \frac{1}{2^2} + \frac{1}{2^3} + \frac{1}{2^4} + \dots$$

The right side is an infinite geometric series with first term $a = 1/2$ and common ratio $r = 1/2$:

$$\frac{1}{2}A = \frac{a}{1 - r} = \frac{1/2}{1 - 1/2} = 1 \implies \mathbf{A = 2}$$

### 3.4 Step 4: Final Time Complexity Synthesis
Substituting $A = 2$ back into the total work sum $S$:

$$S = 2^H \cdot A = 2^H \cdot 2 = 2^{H+1} \approx \mathbf{N}$$

Thus, total work $S \le 2N$, proving that Floyd's Heapify Algorithm executes in **Strict $O(N)$ Linear Time**! $\blacksquare$

```
Mathematical Intuition Breakdown:
+-----------------------------------------------------------------------------------+
| 50% of nodes are at height 0 (Leaves) -> 0 swaps                                  |
| 25% of nodes are at height 1          -> At most 1 swap                           |
| 12.5% of nodes are at height 2        -> At most 2 swaps                          |
| Only 1 node (Root) is at height H     -> H swaps                                  |
| Sum of (Nodes * Height) converges to 2N operations -> O(N) LINEAR TIME! ⚡         |
+-----------------------------------------------------------------------------------+
```

---

## 4. Internal Working Mechanics
Tracing Floyd's Min-Heapify on unsorted array `[40, 10, 30, 5, 20, 15]` ($N = 6$):

```
Initial Unsorted Array: [40, 10, 30, 5, 20, 15]

Tree Topology:
                ( 40 )  <- Index 0
               /      \
            ( 10 )    ( 30 ) <- Index 1 & 2
           /      \   /
         ( 5 )  ( 20)( 15 ) <- Index 3, 4, 5

StartIndex = (6 / 2) - 1 = 2 (Node 30).

Step 1: i = 2 (Node 30). Children: 15 (idx 5).
        30 > 15 -> Swap 30 & 15. Array: [40, 10, 15, 5, 20, 30]

Step 2: i = 1 (Node 10). Children: 5 (idx 3), 20 (idx 4).
        Min child is 5. 10 > 5 -> Swap 10 & 5. Array: [40, 5, 15, 10, 20, 30]

Step 3: i = 0 (Node 40). Children: 5 (idx 1), 15 (idx 2).
        Min child is 5. 40 > 5 -> Swap 40 & 5. Array: [5, 40, 15, 10, 20, 30]
        Continue Sift-Down(1): Children of 40 at idx 1 are 10 (idx 3) & 20 (idx 4).
        Min child is 10. 40 > 10 -> Swap 40 & 10. Array: [5, 10, 15, 40, 20, 30]

Final Valid Min-Heap: [5, 10, 15, 40, 20, 30] ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Bottom-Up Sift-Down Execution Direction Topography:

```
                  ( 0 )  <--- Step 3: Sift-Down Root (Max Height, 1 Node)
                 /     \
   Step 2:     ( 1 )   ( 2 )   <--- Step 1: Start Heapify at (N/2)-1
  Sift-Down   /     \   /           (Height 1)
            ( 3 )  ( 4)( 5 )  <--- Leaves (Height 0, 50% of Nodes, 0 Swaps!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Floyd's In-Place $O(N)$ Min-Heapify and Max-Heapify algorithms:

```java
import java.util.*;

public class HeapifyMaster {

    // 1. Floyd's In-Place Min-Heapify Algorithm O(N) Time, O(1) Auxiliary Space
    public static void minHeapify(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        int n = arr.length;

        // Start at last non-leaf node (n / 2 - 1) and move backwards to 0
        for (int i = (n / 2) - 1; i >= 0; i--) {
            siftDownMin(arr, n, i);
        }
    }

    // 2. Floyd's In-Place Max-Heapify Algorithm O(N) Time, O(1) Auxiliary Space
    public static void maxHeapify(int[] arr) {
        if (arr == null || arr.length <= 1) return;
        int n = arr.length;

        for (int i = (n / 2) - 1; i >= 0; i--) {
            siftDownMax(arr, n, i);
        }
    }

    // Sift-Down for Min-Heap
    private static void siftDownMin(int[] arr, int n, int index) {
        while (2 * index + 1 < n) {
            int leftChild = 2 * index + 1;
            int rightChild = 2 * index + 2;
            int smallest = leftChild;

            if (rightChild < n && arr[rightChild] < arr[leftChild]) {
                smallest = rightChild;
            }

            if (arr[index] > arr[smallest]) {
                swap(arr, index, smallest);
                index = smallest;
            } else {
                break;
            }
        }
    }

    // Sift-Down for Max-Heap
    private static void siftDownMax(int[] arr, int n, int index) {
        while (2 * index + 1 < n) {
            int leftChild = 2 * index + 1;
            int rightChild = 2 * index + 2;
            int largest = leftChild;

            if (rightChild < n && arr[rightChild] > arr[leftChild]) {
                largest = rightChild;
            }

            if (arr[index] < arr[largest]) {
                swap(arr, index, largest);
                index = largest;
            } else {
                break;
            }
        }
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Floyd's Heapify Loop Formula
for (int i = (n / 2) - 1; i >= 0; i--) {
    siftDownMin(arr, n, i);
}
```

---

## 7. Concrete Problem Examples
* **Java `PriorityQueue(Collection c)` Constructor**: Uses Floyd's $O(N)$ Heapify to convert collections into priority queues.
* **Heapsort Step 1**: Building the initial Max-Heap in $O(N)$ time.

---

## 8. Java Code Demonstration & Dry Run
Demonstration converting an unsorted array into Min-Heap and Max-Heap using Floyd's $O(N)$ algorithm:

```java
public class HeapifyDemo {

    public static void main(String[] args) {
        int[] data1 = {40, 10, 30, 5, 20, 15};
        System.out.println("Original Unsorted Array: " + Arrays.toString(data1));

        System.out.println("\n=== 1. Executing Floyd's Min-Heapify O(N) ===");
        HeapifyMaster.minHeapify(data1);
        System.out.println("Valid Min-Heap Array:    " + Arrays.toString(data1)); // Output: [5, 10, 15, 40, 20, 30]

        int[] data2 = {40, 10, 30, 5, 20, 15};
        System.out.println("\n=== 2. Executing Floyd's Max-Heapify O(N) ===");
        HeapifyMaster.maxHeapify(data2);
        System.out.println("Valid Max-Heap Array:    " + Arrays.toString(data2)); // Output: [40, 20, 30, 5, 10, 15]
    }
}
```

---

## 9. Complexity Analysis

| Construction Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Floyd's Heapify** | **$O(N)$ Strict Linear ⚡**| **$O(1)$ In-Place ⚡**| Bottom-Up `siftDown` loop from $(N/2)-1$ |
| **Naive $N$ Insertions**| $O(N \log N)$ Quadratic-like | $O(N)$ Copy Space | Top-Down `siftUp` calls on leaf nodes |

---

## 10. Edge Cases & Boundary Handling
* **Array of Length 0 or 1**: Already valid heaps; `(n/2) - 1 < 0`, loop body does not execute.
* **Array of Length 2**: Starts at `i = 0`, compares `arr[0]` with `arr[1]`, performs at most 1 swap.

---

## 11. Common Mistakes & Anti-Patterns
* **Starting Heapify Loop at Index 0 Moving Forward**:
  - `for (int i = 0; i < n; i++) siftDown(i)` DOES NOT WORK!
  - Sifting down from top to bottom before subtrees are heapified fails to preserve heap invariants. **Heapify MUST run bottom-up** from `(n/2) - 1` down to `0`.
* **Including Leaves in the Heapify Loop**: Starting at `i = n - 1` is redundant because leaves have no children to sift down into. Starting at `(n/2) - 1` saves 50% of loop iterations!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Floyd's Heapify is $O(N)$ while Naive Insertion is $O(N \log N)$:
> * **Naive Insertion (Top-Down)**: $N/2$ leaf nodes are at depth $\log N$ and perform $O(\log N)$ `siftUp` work $\implies \mathbf{O(N \log N)}$.
> * **Floyd's Heapify (Bottom-Up)**: $N/2$ leaf nodes perform **0 work**, $N/4$ nodes perform 1 work, $N/8$ nodes perform 2 work. The series converges to $\sum \frac{h}{2^h} = 2 \implies \mathbf{O(N)\text{ Linear Time}}$.

> **Memory Trick:** **"Bottom-up siftDown puts the least work (0 swaps) on the most nodes (leaves)! Gives linear O(N) time!"**

---

## 13. System & Implementation Comparisons

| Feature | Naive $N$ Insertions | Floyd's Heapify |
| :--- | :--- | :--- |
| **Execution Direction** | Top-Down (`insert` / `siftUp`) | **Bottom-Up (`siftDown`) ⚡** |
| **Start Index** | Index 0 to $N-1$ | **Index $(N/2)-1$ down to 0 ⚡** |
| **Time Complexity** | $O(N \log N)$ | **$O(N)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Convert an unsorted array into a heap in-place in optimal time"** $\rightarrow$ Floyd's $O(N)$ Heapify (`for (int i = n/2 - 1; i >= 0; i--) siftDown(i)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the heapify loop start at index `(n / 2) - 1`?**  
  *A:* Because in a complete binary tree of $N$ nodes, nodes from index `n / 2` to `n - 1` are leaf nodes. Since leaf nodes have no children, calling `siftDown` on them is a no-op. Index `(n / 2) - 1` is the last internal node that possesses at least one child.
* **Q: Evaluate the sum $\sum_{h=0}^{\infty} \frac{h}{2^h}$ algebraically.**  
  *A:* By forming $A = \sum \frac{h}{2^h}$ and subtracting $\frac{1}{2}A$, the series reduces to an infinite geometric progression $\frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots = 1$. Thus $\frac{1}{2}A = 1 \implies A = 2$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLOYD'S O(N) HEAPIFY ALGORITHM                        |
+-----------------------------------------------------------------------+
| • Start Index Formula: int startIndex = (n / 2) - 1;                  |
| • Loop Condition: for (int i = startIndex; i >= 0; i--) siftDown(i);  |
| • Execution Direction: Bottom-Up using siftDown                       |
| • Why O(N)? 50% of nodes (leaves) do 0 work; height 1 nodes do 1 work |
| • Math Sum: S = 2^H * sum(h / 2^h) = 2^H * 2 = 2^(H+1) = O(N) ⚡       |
| • Space: O(1) In-Place Array Mutation                                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the mathematical proof of $O(N)$ Heapify using $\sum \frac{h}{2^h} = 2$.
- [ ] I can state why the loop starts at `(n / 2) - 1`.
- [ ] I can implement `minHeapify` and `maxHeapify` in 10 lines of code.
- [ ] I know why naive insertion takes $O(N \log N)$ while Floyd's algorithm takes $O(N)$.
