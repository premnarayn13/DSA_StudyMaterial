# 03. Heapify Mechanics, Floyd's $O(N)$ Linear Build Heap & Sift-Down Mathematical Proof

## 1. Introduction
Converting an unsorted array of $N$ elements into a valid Binary Heap is a fundamental prerequisite for heap operations and Heapsort. While inserting elements one by one using `siftUp` takes $O(N \log N)$ time, **Floyd's Algorithm (`buildHeap`)** constructs a valid heap in **$O(N)$ Strict Linear Time** by applying **Bottom-Up `siftDown`** starting from the last internal node down to the root.

> **Important:** Why does Bottom-Up `siftDown` build a heap in $O(N)$ linear time while Top-Down `siftUp` takes $O(N \log N)$?
> * **Top-Down `siftUp`**: Leaves (50% of all nodes) sit at depth $H = \log_2 N$ and are sifted UP across $\log N$ levels $\implies N/2 \cdot \log N = \mathbf{O(N \log N)}$!
> * **Bottom-Up `siftDown`**: Leaves (50% of all nodes) have height $h = 0$ and require ZERO sifts! Most nodes sit near the bottom with small heights ($h=1, 2$), while only 1 root node sits at height $h = \log_2 N$.
> * The infinite sum converges to **$\mathbf{O(N)}$ Strict Linear Time**! ⚡

```
Floyd's O(N) Build-Heap Node Work Distribution:
Level 3 (Leaves, 50% nodes)  : Height h = 0 -> 0 Sift Steps Work!
Level 2 (25% nodes)          : Height h = 1 -> 1 Sift Step Work.
Level 1 (12.5% nodes)        : Height h = 2 -> 2 Sift Steps Work.
Level 0 (Root, 1 node)       : Height h = log2 N -> log2 N Sift Work.
Sum of Work across all nodes converges strictly to O(N)! ⚡
```

---

## 2. Core Concepts & Floyd's Build Heap Algorithm

### 2.1 Floyd's Algorithm Step-by-Step
Given an unsorted array `arr` of size $N$:
1. Identify the index of the **LAST INTERNAL NODE**:
   $$\text{lastInternal} = \left\lfloor \frac{N - 2}{2} \right\rfloor$$
2. Iterate **BACKWARD** from `i = lastInternal` down to `i = 0`:
   - Call `siftDown(arr, i, N)`.
3. Array is now a valid Min/Max Heap in **$O(N)$ Linear Time**!

```
Floyd's Build Heap Algorithm Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Build Strategy        | Time Complexity   | Work Workload     | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| **Bottom-Up SiftDown**| **$O(N)$ Linear ⚡**| Minimal (Leaves = 0)| `buildHeap()` / Heapsort|
| Top-Down SiftUp       | $O(N \log N)$     | High (Leaves = $\log N$)| Streaming Insertions|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Build Heap: Iterate backward from (N-2)/2 down to 0, calling siftDown(i)! Runs in O(N) Linear Time!"**

---

## 3. Mathematical Proof of $O(N)$ Linear Time

### 3.1 Summation Proof of Floyd's Algorithm
In a complete binary tree of height $H = \log_2 N$, the number of nodes at height $h$ is at most $\lceil N / 2^{h+1} \rceil$.
Since a node at height $h$ can sift down at most $h$ steps:

$$T(N) = \sum_{h=0}^{\log_2 N} \frac{N}{2^{h+1}} \cdot O(h) = \frac{N}{2} \sum_{h=0}^{\log_2 N} \frac{h}{2^h}$$

Using the standard arithmetico-geometric series summation formula:

$$\sum_{h=0}^{\infty} \frac{h}{2^h} = 2 \implies T(N) = \frac{N}{2} \cdot 2 = \mathbf{O(N) \text{ Linear Time}}$$

---

## 4. Internal Working Mechanics
Tracing `buildHeap` on Unsorted Array `[4, 10, 3, 5, 1]`:

```
Input Array: [4, 10, 3, 5, 1] (N = 5).
Last Internal Node = (5 - 2) / 2 = 1 (Value 10).

Step 1: i = 1 (val 10). Children: 5 (idx 3), 1 (idx 4).
  - Smallest child = 1 (idx 4).
  - 10 > 1 -> Swap 10 and 1! Array becomes: [4, 1, 3, 5, 10].

Step 2: i = 0 (val 4). Children: 1 (idx 1), 3 (idx 2).
  - Smallest child = 1 (idx 1).
  - 4 > 1 -> Swap 4 and 1! Array becomes: [1, 4, 3, 5, 10].
  - Sift-down 4 (idx 1). Children: 5 (idx 3), 10 (idx 4). Smallest = 5.
  - 4 < 5 -> Stop!

Final Min Heap = [1, 4, 3, 5, 10] built in 2 swaps! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Floyd's Backward Sift-Down Work Topography:

```
Start Work at Last Internal Node (Index 1):
             [ 4 ]                          [ 4 ]                        [ 1 ]
            /     \   Step 1 (i=1)         /     \     Step 2 (i=0)     /     \
        [ 10 ]   [ 3 ] ----------->    [ 1 ]    [ 3 ] -------------> [ 4 ]   [ 3 ]
       /     \                        /     \                       /    \
    [ 5 ]   [ 1 ]                  [ 5 ]   [ 10 ]                [ 5 ]  [ 10 ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Floyd's $O(N)$ Linear Time Build Heap and Heapsort:

```java
import java.util.*;

public class HeapifyBuildHeapMaster {

    // 1. Floyd's Build Min Heap In-Place O(N) Time, O(1) Auxiliary Space
    public static void buildMinHeap(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        // Start from last internal node and iterate backward to 0
        for (int i = (n - 2) / 2; i >= 0; i--) {
            siftDownMin(arr, i, n);
        }
    }

    // 2. Floyd's Build Max Heap In-Place O(N) Time, O(1) Auxiliary Space
    public static void buildMaxHeap(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        for (int i = (n - 2) / 2; i >= 0; i--) {
            siftDownMax(arr, i, n);
        }
    }

    // 3. Heapsort Implementation O(N log N) Time, O(1) Space
    public static void heapSort(int[] arr) {
        if (arr == null || arr.length <= 1) return;

        int n = arr.length;
        buildMaxHeap(arr); // Step 1: Build Max Heap in O(N) time

        // Step 2: Extract maximum one by one and move to array end
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i); // Swap current max (root) with last element
            siftDownMax(arr, 0, i); // Re-heapify remaining elements
        }
    }

    private static void siftDownMin(int[] arr, int index, int size) {
        int curr = index;
        while (2 * curr + 1 < size) {
            int left = 2 * curr + 1;
            int right = 2 * curr + 2;
            int smallest = left;

            if (right < size && arr[right] < arr[left]) {
                smallest = right;
            }

            if (arr[curr] > arr[smallest]) {
                swap(arr, curr, smallest);
                curr = smallest;
            } else {
                break;
            }
        }
    }

    private static void siftDownMax(int[] arr, int index, int size) {
        int curr = index;
        while (2 * curr + 1 < size) {
            int left = 2 * curr + 1;
            int right = 2 * curr + 2;
            int largest = left;

            if (right < size && arr[right] > arr[left]) {
                largest = right;
            }

            if (arr[curr] < arr[largest]) {
                swap(arr, curr, largest);
                curr = largest;
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
// Floyd's Build Heap Loop
for (int i = (n - 2) / 2; i >= 0; i--) siftDownMin(arr, i, n);
```

---

## 7. Concrete Problem Examples
* **Heapsort ($O(N \log N)$ Time, $O(1)$ Space)**: Uses Max Heap `buildMaxHeap()` to sort arrays in-place.
* **Top K Elements Pre-Processing**: Converting input array to Min/Max heap in $O(N)$ linear time.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Floyd's `buildMinHeap` and `heapSort`:

```java
public class HeapifyBuildHeapDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Floyd's O(N) Build Min Heap Test ===");
        int[] arr = {4, 10, 3, 5, 1};
        HeapifyBuildHeapMaster.buildMinHeap(arr);
        System.out.println("Built Min Heap Array: " + Arrays.toString(arr));
        // Output: [1, 4, 3, 5, 10] (Root is Min!)

        System.out.println("\n=== 2. Heapsort In-Place Test ===");
        int[] unsorted = {12, 11, 13, 5, 6, 7};
        HeapifyBuildHeapMaster.heapSort(unsorted);
        System.out.println("Sorted Array: " + Arrays.toString(unsorted));
        // Output: [5, 6, 7, 11, 12, 13] in Sorted Ascending Order! ✅
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Phase | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Floyd's `buildHeap()`** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ In-Place ⚡** |
| **Top-Down Sift-Up Build**| $O(N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ In-Place |
| **Heapsort** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(1)$ In-Place ⚡** |

---

## 10. Edge Cases & Boundary Handling
* **Single Element / Empty Array**: Handled by early check `arr.length <= 1`.
* **Already Sorted Array**: `buildHeap` still executes in $O(N)$ time, confirming heap properties.

---

## 11. Common Mistakes & Anti-Patterns
* **Iterating Forward `0 ... N-1` with Sift-Up for `buildHeap` ($O(N \log N)$ Penalty)**:
  - Sifting up from index 0 processes leaf nodes across maximum height paths, incurring $O(N \log N)$ time.
  - **Iterate BACKWARD from `(N-2)/2` down to 0 with `siftDown` for $O(N)$ time**.
* **Starting Sift-Down Iteration from Leaf Nodes**:
  - Leaf nodes (`N/2 ... N-1`) have no children. Sifting down leaves does zero work and wastes CPU cycles.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Heapsort uses a MAX HEAP to sort an array in ASCENDING order:
> 1. Building a **Max Heap** places the global maximum element at `arr[0]`.
> 2. Swapping `arr[0]` with the last element `arr[i]` places the largest element in its correct final sorted position at the end of the array!
> 3. Shrinking heap size by 1 and calling `siftDown(0)` restores the Max Heap for remaining elements in **$O(1)$ auxiliary space**!

> **Memory Trick:** **"To sort ASCENDING in-place: Build MAX Heap and swap root to array end!"**

---

## 13. System & Implementation Comparisons

| Feature | Floyd's Bottom-Up `buildHeap` | Sequential Insertion `offer()` |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡** | $O(N \log N)$ Logarithmic |
| **Primary Algorithm**| Bottom-Up `siftDown(i)` | Top-Down `siftUp(i)` |
| **Input Type** | Batch Static Array | Dynamic Streaming Inputs |

---

## 14. How to Recognize This in Questions
* **"Convert an unsorted array into a heap in O(N) linear time"** $\rightarrow$ Floyd's `buildHeap()` algorithm.
* **"Sort an array in O(N log N) time and O(1) auxiliary space"** $\rightarrow$ Heapsort using Max Heap.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Floyd's `buildHeap()` run in $O(N)$ time while `siftUp` insertion takes $O(N \log N)$?**  
  *A:* Because in a binary tree, 50% of nodes are leaves. Floyd's algorithm starts from the bottom up, so 50% of nodes (leaves) do 0 work, 25% do 1 work step, 12.5% do 2 work steps. Summing this series yields $\frac{N}{2} \sum \frac{h}{2^h} = O(N)$.
* **Q: Is Heapsort a stable sorting algorithm?**  
  *A:* No! Heapsort performs long-distance swaps between `arr[0]` and `arr[i]`, which can alter the relative order of equal key elements.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLOYD'S O(N) BUILD HEAP & HEAPSORT                    |
+-----------------------------------------------------------------------+
| • Floyd's Algorithm: Iterate i = (N - 2) / 2 down to 0 calling siftDown|
| • Build Time Bound : O(N) Strict Linear Time ⚡                        |
| • Heapsort Strategy: Build Max Heap -> Swap root to end -> siftDown   |
| • Heapsort Bounds  : O(N log N) Time | O(1) Auxiliary Space ⚡         |
| • Stability        : UNSTABLE (Long-distance swaps disrupt duplicate order)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Floyd's `buildMinHeap` and `buildMaxHeap` in $O(N)$ time.
- [ ] I can write Heapsort in $O(N \log N)$ time and $O(1)$ space.
- [ ] I can prove why Floyd's algorithm runs in $O(N)$ linear time.
- [ ] I know why Max Heap is used to sort arrays in ascending order.
- [ ] I know why Heapsort is an unstable sort.
