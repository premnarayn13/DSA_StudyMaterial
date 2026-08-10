# 16. Master Reference — Sorting Algorithms & Foundations

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 23: Sorting Algorithms**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Sorting Taxonomy, Comparison Lower Bound Proof ($\Omega(N \log N)$), Stability Invariants, Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort (Hoare vs Lomuto), Heap Sort, Counting Sort, Radix Sort, Bucket Sort, TimSort, Internal vs External K-Way Merge Sort, System Sorting Algorithm Routers, Dutch National Flag (LeetCode 75), and QuickSelect (LeetCode 215).

> **Important:** Review this master reference 15 minutes before an interview to refresh the 10 Sorting Stability Statuses, $\Omega(N \log N)$ Decision Tree proof, QuickSort Hoare partitioning vs Lomuto, Java Primitive (`Arrays.sort(int[])` Dual-Pivot QuickSort) vs Object (`Arrays.sort(Object[])` TimSort) rules, $O(N)$ Build Heap, Counting Sort Prefix Sums, Base-256 Bitwise Shifts (`(val >> shift) & 0xFF`), and Dutch National Flag 3-pointer logic!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Comparison-Based Lower Bound Equation**:
  - $H \ge \lceil \log_2 (N!) \rceil = \mathbf{\Omega(N \log N) \text{ Minimum Comparisons}}$.
* **Stability Invariant Equation**:
  - $A[i] = A[j] \land i < j \implies \text{pos}_{\text{out}}(A[i]) < \text{pos}_{\text{out}}(A[j])$.
* **Bubble Sort Adaptive Flag Check**:
  - `if (!swapped) break;` (Halts loop in $O(N)$ time for pre-sorted inputs).
* **Selection Sort Minimal Swaps Bound**:
  - Executes at most $N - 1 = \mathbf{O(N) \text{ Total Swaps}}$ (Ideal for expensive flash memory writes!).
* **Insertion Sort Nearly-Sorted Performance**:
  - $T(N) = \mathbf{O(N \cdot K) \text{ Time}}$ when elements are at most $K$ positions away.
* **Merge Sort Inversion Counting Formula**:
  - $\text{inversions} += (mid - i + 1)$ when $arr[j] < arr[i]$ during merge.
* **Hoare Partition Pointer Loop**:
  - `do { i++; } while (arr[i] < pivot); do { j--; } while (arr[j] > pivot);` (3x fewer swaps than Lomuto!).
* **Max-Heap Index Arithmetic**:
  - $\text{leftChild} = 2i + 1, \quad \text{rightChild} = 2i + 2, \quad \text{parent} = \lfloor (i - 1) / 2 \rfloor$.
* **Counting Sort Prefix Sum Transformation**:
  - $\text{count}[i] = \text{count}[i] + \text{count}[i - 1]$ (Output placement backward from $N-1$ down to 0).
* **Bitwise Base-256 Digit Extraction**:
  - $\text{byteVal} = (\text{val} \gg \text{shift}) \,\&\, 0xFF$ (4 passes for 32-bit integers in $O(N)$ time).
* **Bucket Sort Hash Indexing**:
  - $\text{bucketIndex} = \lfloor \text{val} \times B \rfloor$ (Clamped to $B - 1$).
* **TimSort $minRun$ Length Computation**:
  - Computes $minRun \in [32, 64]$ via 6 most significant bits of $N$.
* **External Sorting Disk Merge Passes**:
  - $P = \lceil \log_K (N / M) \rceil \text{ Disk Passes}$ where $K$ is Min-Heap size.

```
Master Sorting Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm             | Best Case Time    | Worst Case Time   | Auxiliary Space   | Stability Invariant|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Bubble Sort**       | $O(N)$ (Adaptive) | $O(N^2)$          | **$O(1)$ In-Place⚡**| **Stable ⚡**      |
| **Selection Sort**    | $O(N^2)$          | $O(N^2)$          | **$O(1)$ In-Place⚡**| Unstable ❌       |
| **Insertion Sort**    | **$O(N)$ Adaptive⚡**| $O(N^2)$       | **$O(1)$ In-Place⚡**| **Stable ⚡**      |
| **Merge Sort**        | **$O(N \log N)$⚡**| **$O(N \log N)$⚡**| $O(N)$ Extra      | **Stable ⚡**      |
| **Quick Sort**        | **$O(N \log N)$⚡**| $O(N^2)$          | **$O(\log N)$ Stack**| Unstable ❌       |
| **Heap Sort**         | **$O(N \log N)$⚡**| **$O(N \log N)$⚡**| **$O(1)$ In-Place⚡**| Unstable ❌       |
| **Counting Sort**     | **$O(N + K)$ ⚡** | **$O(N + K)$ ⚡** | $O(N + K)$ Extra  | **Stable ⚡**      |
| **Radix Sort**        | **$O(d \cdot (N+K))$⚡**| **$O(d \cdot (N+K))$⚡**| $O(N + K)$ Extra  | **Stable ⚡**      |
| **Bucket Sort**       | **$O(N + B)$ ⚡** | $O(N^2)$ (Skewed) | $O(N + B)$ Extra  | **Stable ⚡**      |
| **TimSort**           | **$O(N)$ Adaptive⚡**| **$O(N \log N)$⚡**| $O(N)$ Extra      | **Stable ⚡**      |
| **External K-Way Merge**| $O(N \log_K(N/M))$| $O(N \log_K(N/M))$| $O(M)$ RAM        | **Stable ⚡**      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Sorting Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Comparison Model | Stability Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort (Flag)** | $\mathbf{O(N)}$ Adaptive ⚡| $O(N^2)$ | $O(N^2)$ | $\mathbf{O(1)}$ In-Place ⚡| Comparison | **Stable ⚡** |
| **Selection Sort**    | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $\mathbf{O(1)}$ In-Place ⚡| Comparison | Unstable ❌ |
| **Insertion Sort**    | $\mathbf{O(N)}$ Adaptive ⚡| $O(N^2)$ | $O(N^2)$ | $\mathbf{O(1)}$ In-Place ⚡| Comparison | **Stable ⚡** |
| **Binary Insertion**  | $\mathbf{O(N)}$ Adaptive ⚡| $O(N^2)$ Shifts | $O(N^2)$ Shifts | $\mathbf{O(1)}$ In-Place ⚡| $O(N \log N)$ Comp | **Stable ⚡** |
| **Shell Sort**        | $O(N \log N)$ | $O(N^{1.3})$ | $O(N^{1.5})$ | $\mathbf{O(1)}$ In-Place ⚡| Comparison | Unstable ❌ |
| **Merge Sort**        | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Extra | Comparison | **Stable ⚡** |
| **Quick Sort (Hoare)**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N^2)$ | $\mathbf{O(\log N)}$ Stack ⚡| Comparison | Unstable ❌ |
| **Dual-Pivot Quick**  | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N^2)$ | $\mathbf{O(\log N)}$ Stack ⚡| Comparison | Unstable ❌ |
| **Heap Sort**         | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(1)}$ In-Place ⚡| Comparison | Unstable ❌ |
| **Counting Sort**     | $\mathbf{O(N + K)}$ ⚡| $\mathbf{O(N + K)}$ ⚡| $\mathbf{O(N + K)}$ ⚡| $O(N + K)$ Extra | **Non-Comparison ⚡**| **Stable ⚡** |
| **Radix Sort (Base 256)**| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $\mathbf{O(4N)} = \mathbf{O(N)}$ ⚡| $O(N + 256)$ | **Non-Comparison ⚡**| **Stable ⚡** |
| **Bucket Sort**       | $\mathbf{O(N + B)}$ ⚡| $\mathbf{O(N + B)}$ ⚡| $O(N^2)$ (Skewed) | $O(N + B)$ Extra | **Non-Comparison ⚡**| **Stable ⚡** |
| **TimSort**           | $\mathbf{O(N)}$ Adaptive ⚡| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Extra | Hybrid Merge/Insert | **Stable ⚡** |
| **Dutch Flag (75)**   | $\mathbf{O(N)}$ ⚡| $\mathbf{O(N)}$ ⚡| $\mathbf{O(N)}$ ⚡| $\mathbf{O(1)}$ In-Place ⚡| 3-Way Partition | Unstable ❌ |
| **QuickSelect (215)** | $\mathbf{O(N)}$ ⚡| $\mathbf{O(N)}$ Average ⚡| $O(N^2)$ | $\mathbf{O(1)}$ Space ⚡| Partial QuickSort | Unstable ❌ |

---

## 4. Hardware & Standard Library Architecture Audit
```
+-----------------------------------------------------------------------------------+
| Standard Library Sorting Engines Audit                                            |
+-----------------------------------------------------------------------------------+
| Java Primitive Arrays (`Arrays.sort(int[])`)    : Dual-Pivot QuickSort (O(1) Memory)|
| Java Object Collections (`Arrays.sort(Object[])`): TimSort (Strict Stability)      |
| C++ Standard Library (`std::sort`)              : IntroSort (Quick + Heap + Insertion)|
| Python (`list.sort()`)                          : TimSort                         |
| GPU Hardware Sorting                            : Bitonic Sorting Networks        |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Early Termination Bubble Sort Flag
> boolean swapped = false; for (int j = 0; j < n - 1 - i; j++) { if (arr[j] > arr[j+1]) { swap(arr, j, j+1); swapped = true; } } if (!swapped) break;
> 
> // 2. Insertion Sort Shifting Loop
> int key = arr[i], j = i - 1; while (j >= 0 && arr[j] > key) { arr[j + 1] = arr[j]; j--; } arr[j + 1] = key;
> 
> // 3. Merge Sort Stable Merge Check
> if (leftArr[i] <= rightArr[j]) temp[k++] = leftArr[i++]; else temp[k++] = rightArr[j++];
> 
> // 4. Hoare Inward Partition Loop
> do { i++; } while (arr[i] < pivot); do { j--; } while (arr[j] > pivot); if (i >= j) return j; swap(arr, i, j);
> 
> // 5. Heap Sort Parent / Child Index Arithmetic
> int left = 2 * i + 1, right = 2 * i + 2, parent = (i - 1) / 2;
> 
> // 6. Stable Counting Sort Backward Output Placement
> for (int i = n - 1; i >= 0; i--) output[--count[arr[i] - minVal]] = arr[i];
> 
> // 7. Bitwise Base-256 Byte Extraction
> int byteVal = (arr[i] >> shift) & 0xFF;
> 
> // 8. Dutch National Flag 3-Way Partitioning (LeetCode 75)
> if (nums[mid] == 0) swap(nums, low++, mid++); else if (nums[mid] == 1) mid++; else swap(nums, mid, high--);
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using Forward Loop in Counting Sort Output Placement**: Forward placement (`0 ... N-1`) destroys stability. Always iterate BACKWARDS (`N-1` down to `0`).
* **Pitfall 2: Advancing `mid` Pointer on 2-Swap in Dutch National Flag**: Swapping `nums[mid]` with `nums[high]` brings an uninspected element from `high`. Keep `mid` unchanged (`high--`).
* **Pitfall 3: Using QuickSort for Multi-Column Sorting**: QuickSort is unstable and destroys secondary key order. Always use **TimSort** for Object collections.
* **Pitfall 4: Allocating Auxiliary Array Inside Merge Recursive Calls**: Allocating `new int[N]` inside `merge()` creates thousands of short-lived heap objects. Allocate a single auxiliary array `temp` upfront in the top-level method.
* **Pitfall 5: Building Max-Heap via `siftUp` Insertions ($O(N \log N)$)**: Building a heap via `siftUp` takes $O(N \log N)$ time. Use bottom-up `siftDown` from $(N/2)-1$ down to 0 for **$O(N)$ Linear Build Heap**.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 23 (SORTING ALGORITHMS)         |
+-----------------------------------------------------------------------+
| 1. Lower Bound  : Comparison limit is Omega(N log N) (Decision Tree) |
| 2. Stability    : Insertion, Bubble, Merge, Counting, Radix, TimSort ⚡|
| 3. Unstable     : Selection, Quick, Heap, Shell ❌                     |
| 4. Java Engine  : Primitives -> Dual-Pivot QuickSort; Objects -> TimSort|
| 5. Hoare Scheme : 2 inward pointers -> 3x fewer swaps than Lomuto! ⚡  |
| 6. Build Heap   : O(N) Linear Time via bottom-up siftDown            |
| 7. Non-Compare  : Counting & Radix run in O(N + K) linear time ⚡      |
| 8. Dutch Flag   : 3-pointer 1-pass O(N) sort for 0s, 1s, 2s (LC 75)   |
| 9. QuickSelect  : Partial QuickSort locates K-th element in O(N) avg |
| 10. External    : K-Way Min-Heap merge minimizes disk passes log_K(N/M)|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can state and prove the $\Omega(N \log N)$ comparison lower bound using decision trees.
- [ ] I can categorize all 10 major sorting algorithms as Stable or Unstable.
- [ ] I can write Optimized Bubble Sort with early termination flag.
- [ ] I can write Selection Sort and explain its $N - 1 = O(N)$ minimal swaps bound.
- [ ] I can write Insertion Sort and explain why TimSort uses it for $N \le 32$.
- [ ] I can write Top-Down and Bottom-Up Merge Sort with a single upfront temp array.
- [ ] I can count inversions in $O(N \log N)$ time using Merge Sort.
- [ ] I can write QuickSort using Hoare inward pointer partitioning.
- [ ] I can implement Tail Call Stack Optimization to guarantee $O(\log N)$ stack depth.
- [ ] I can write in-place Heap Sort with $O(N)$ linear Build Heap.
- [ ] I can write Stable Counting Sort with negative range offsets.
- [ ] I can write Bitwise Base-256 Fast Radix Sort (4-pass $O(N)$ for 32-bit ints).
- [ ] I can write Floating-Point Bucket Sort over $[0.0, 1.0)$.
- [ ] I can write TimSort $minRun$ calculation and Natural Run Detection.
- [ ] I can write an External Multi-Way Merge Sort Engine using a Min-Heap.
- [ ] I can write LeetCode 75 (`Sort Colors / Dutch National Flag`) in 1 pass $O(1)$ space.
- [ ] I can write LeetCode 215 (`K-th Largest Element`) using QuickSelect in $O(N)$ average time.
