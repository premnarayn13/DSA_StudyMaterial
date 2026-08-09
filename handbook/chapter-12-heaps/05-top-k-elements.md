# 05. Top K Elements Pattern, Fixed-Size Min-Heap & QuickSelect Optimization

## 1. Introduction
The **Top K Elements Pattern** solves problems demanding the $K$ largest, $K$ smallest, or $K$ most frequent items from an unsorted dataset. While sorting the entire dataset takes $O(N \log N)$ time, maintaining a **Fixed-Size Min-Heap of Capacity $K$** reduces time complexity down to **$O(N \log K)$ Time and $O(K)$ Auxiliary Space**. For static arrays, **QuickSelect** further optimizes the search to **$O(N)$ Average Linear Time**.

> **Important:** Why does finding the $K$ LARGEST elements require a **MIN-HEAP** of size $K$?
> * A Min-Heap of capacity $K$ holds the $K$ largest candidates seen so far.
> * The **head of the Min-Heap** (`pq.peek()`) stores the **SMALLEST candidate among the top $K$**!
> * When a new element $X$ arrives: if $X > \text{pq.peek()}$, $X$ is strictly larger than the worst candidate in the top $K$!
> * Action: `pq.poll()` (evict smallest candidate) and `pq.offer(X)`!
> * Result: After processing $N$ items, the heap contains the **EXACT $K$ LARGEST ELEMENTS** in $O(N \log K)$ time! ⚡

```
Top K Largest Min-Heap Window Topology (Heap Capacity K = 3):
Heap Elements : [ 10, 15, 20 ] (Head is Min = 10)
New Element   : 25 > 10 (Head)
Action        : Poll 10 -> Offer 25 -> Heap becomes [ 15, 20, 25 ] (Head is 15!)
Guarantees O(N log K) time and O(K) space! ⚡
```

---

## 2. Core Concepts & Fixed-Size Min-Heap Architecture

### 2.1 Top K Largest vs Top K Smallest Decision Matrix

```
Top K Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Goal          | Heap Type         | Heap Capacity     | Eviction Rule     |
+-----------------------+-------------------+-------------------+-------------------+
| **K Largest Elements**| **Min-Heap ⚡**   | **Fixed Size $K$**| If $X > \text{head}$, `poll()` & `offer(X)`|
| **K Smallest Elements**| **Max-Heap ⚡**  | **Fixed Size $K$**| If $X < \text{head}$, `poll()` & `offer(X)`|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"K Largest = Min-Heap of size K! K Smallest = Max-Heap of size K!"**

---

## 3. Characteristics & QuickSelect Average $O(N)$ Optimization (LeetCode 215)

### 3.1 QuickSelect Partition Algorithm
QuickSelect is a divide-and-conquer algorithm based on QuickSort partitioning:
1. Pick a pivot element `nums[pivot]`.
2. Partition array into 2 halves around pivot.
3. If pivot index equals $N - K$, the pivot is the $K$-th largest element!
4. If pivot index $> N - K$, search left half; else search right half.
5. Average Time: **$O(N)$ Linear Time**, Worst Case: $O(N^2)$ (Random pivot eliminates worst case!).

---

## 4. Internal Working Mechanics
Tracing Top K Frequent Elements (LeetCode 347) on `nums = [1,1,1,2,2,3]`, `K = 2`:

```
Step 1: Build Frequency Map -> {1: 3, 2: 2, 3: 1}.

Step 2: Maintain Min-Heap of size K = 2 ordered by frequency:
  - Offer (1, freq 3) -> Heap: [(1, 3)]
  - Offer (2, freq 2) -> Heap: [(2, 2), (1, 3)] (Head is (2, freq 2))
  - Offer (3, freq 1) -> (3, freq 1) < Head (2, freq 2) -> IGNORED!

Final Heap Contains: [(2, freq 2), (1, freq 3)].
Top 2 Frequent Elements = [1, 2]! ✅ (O(N log K) Time!)
```

---

## 5. Visual Diagram
Min-Heap Size $K$ Eviction Mechanics Topography:

```
Stream Input: 3, 2, 1, 5, 6, 4 (K = 2)

Step 1: Push 3, 2       -> Heap: [2, 3] (Head 2)
Step 2: Push 1 (1 < 2)  -> Ignored! Heap: [2, 3]
Step 3: Push 5 (5 > 2)  -> Poll 2, Offer 5 -> Heap: [3, 5] (Head 3)
Step 4: Push 6 (6 > 3)  -> Poll 3, Offer 6 -> Heap: [5, 6] (Head 5)
Step 5: Push 4 (4 < 5)  -> Ignored! Heap: [5, 6]

2 Largest Elements = [5, 6]! Head (5) is 2nd Largest! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Kth Largest Element (LeetCode 215 - Heap & QuickSelect), Top K Frequent Elements (LeetCode 347), and Kth Largest Element in a Stream (LeetCode 703):

```java
import java.util.*;

public class TopKElementsMaster {

    // 1. Kth Largest Element using Fixed-Size Min-Heap (LeetCode 215) O(N log K) Time, O(K) Space
    public static int findKthLargestHeap(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);

        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) {
                minHeap.poll(); // Evict smallest candidate
            }
        }

        return minHeap.peek(); // Head is the Kth largest element!
    }

    // 2. Kth Largest Element using QuickSelect O(N) Avg Time, O(1) Auxiliary Space
    public static int findKthLargestQuickSelect(int[] nums, int k) {
        int targetIndex = nums.length - k;
        int left = 0, right = nums.length - 1;
        Random rand = new Random();

        while (left <= right) {
            int pivotIndex = left + rand.nextInt(right - left + 1);
            int finalPivotIndex = partition(nums, left, right, pivotIndex);

            if (finalPivotIndex == targetIndex) {
                return nums[finalPivotIndex];
            } else if (finalPivotIndex < targetIndex) {
                left = finalPivotIndex + 1;
            } else {
                right = finalPivotIndex - 1;
            }
        }

        return -1;
    }

    private static int partition(int[] nums, int left, int right, int pivotIndex) {
        int pivotValue = nums[pivotIndex];
        swap(nums, pivotIndex, right); // Move pivot to end
        int storeIndex = left;

        for (int i = left; i < right; i++) {
            if (nums[i] < pivotValue) {
                swap(nums, i, storeIndex);
                storeIndex++;
            }
        }

        swap(nums, storeIndex, right); // Move pivot to final position
        return storeIndex;
    }

    private static void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    // 3. Top K Frequent Elements (LeetCode 347) O(N log K) Time, O(N) Space
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freqMap = new HashMap<>();
        for (int num : nums) {
            freqMap.put(num, freqMap.getOrDefault(num, 0) + 1);
        }

        // Min-Heap ordered by frequency
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(freqMap.get(a), freqMap.get(b))
        );

        for (int key : freqMap.keySet()) {
            minHeap.offer(key);
            if (minHeap.size() > k) {
                minHeap.poll(); // Evict lowest frequency candidate
            }
        }

        int[] result = new int[k];
        for (int i = 0; i < k; i++) {
            result[i] = minHeap.poll();
        }

        return result;
    }

    // 4. Kth Largest Element in a Stream (LeetCode 703) O(log K) per add()
    public static class KthLargestStream {
        private final PriorityQueue<Integer> minHeap;
        private final int k;

        public KthLargestStream(int k, int[] nums) {
            this.k = k;
            this.minHeap = new PriorityQueue<>(k);
            for (int num : nums) {
                add(num);
            }
        }

        public int add(int val) {
            minHeap.offer(val);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
            return minHeap.peek();
        }
    }
}
```

> **Quick Syntax:**
```java
// Fixed-Size Min-Heap Pattern
minHeap.offer(num);
if (minHeap.size() > k) minHeap.poll();
```

---

## 7. Concrete Problem Examples
* **LeetCode 215 - Kth Largest Element in an Array**: Fixed Min-Heap vs QuickSelect.
* **LeetCode 347 - Top K Frequent Elements**: Frequency Map + Min-Heap.
* **LeetCode 703 - Kth Largest Element in a Stream**: Streaming Min-Heap.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Heap & QuickSelect Top-K solutions:

```java
public class TopKElementsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Kth Largest Element (LeetCode 215) ===");
        int[] nums = {3, 2, 1, 5, 6, 4};
        int k = 2;

        int kthHeap = TopKElementsMaster.findKthLargestHeap(nums, k);
        System.out.println("2nd Largest (Min-Heap):   " + kthHeap); // Output: 5

        int kthQuick = TopKElementsMaster.findKthLargestQuickSelect(nums, k);
        System.out.println("2nd Largest (QuickSelect): " + kthQuick); // Output: 5 ✅

        System.out.println("\n=== 2. Top K Frequent Elements (LeetCode 347) ===");
        int[] freqNums = {1, 1, 1, 2, 2, 3};
        int[] top2Freq = TopKElementsMaster.topKFrequent(freqNums, 2);
        System.out.println("Top 2 Frequent Elements: " + Arrays.toString(top2Freq));
        // Output: [2, 1] ✅
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Full Array Sort** | $O(N \log N)$ | $O(1)$ Space | Sorts entire array |
| **Fixed Min-Heap Size $K$**| **$O(N \log K)$ ⚡** | **$O(K)$ Space ⚡** | Keeps heap capacity $K$ |
| **QuickSelect** | **$O(N)$ Avg Linear ⚡**| **$O(1)$ Auxiliary Space ⚡**| In-place partitioning |
| **Bucket Sort (347)** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Array of frequency buckets |

---

## 10. Edge Cases & Boundary Handling
* **$K = 1$**: Min-Heap of size 1 tracks maximum element.
* **$K = N$**: Retains all array elements in heap; `peek()` returns overall minimum.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Max-Heap for K Largest Elements ($O(N \log N)$ Time Penalty)**:
  - Offering all $N$ elements into a Max-Heap takes $O(N \log N)$ time and $O(N)$ space.
  - **Use a Min-Heap capped at size $K$ for $O(N \log K)$ time and $O(K)$ space**.
* **Forgetting Random Pivot Selection in QuickSelect**:
  - Picking deterministic pivot (e.g. always first element) causes QuickSelect to degrade to $O(N^2)$ on already sorted arrays!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Capped Min-Heap Size $K$ is Optimal for Data Streams:
> For infinite streaming data where $N \to \infty$:
> QuickSelect cannot be used because all elements are not available upfront.
> A **Min-Heap of size $K$** maintains the $K$ largest elements in **$O(\log K)$ time per incoming data point**, independent of total stream length $N$!

> **Memory Trick:** **"Capped Min-Heap size K is mandatory for streaming Top-K problems!"**

---

## 13. System & Implementation Comparisons

| Feature | Min-Heap Size $K$ | QuickSelect |
| :--- | :--- | :--- |
| **Average Time** | **$O(N \log K)$ ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Memory** | $O(K)$ Heap Space | **$O(1)$ Auxiliary Space ⚡** |
| **Streaming Compatibility**| **100% Streaming Ready ⚡** | Requires Static Array Upfront |

---

## 14. How to Recognize This in Questions
* **"Find K largest / smallest elements in an array or data stream"** $\rightarrow$ Fixed-Size Min-Heap of capacity $K$.
* **"Find K most frequent elements in array"** $\rightarrow$ Frequency Map + Min-Heap of size $K$.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Min-Heap of size $K$ store the $K$ largest elements?**  
  *A:* Because the head of a Min-Heap contains the minimum value among its elements. When size exceeds $K$, polling evicts the smallest item, leaving only the $K$ largest values in the heap.
* **Q: How can Top K Frequent Elements (LeetCode 347) be solved in $O(N)$ time?**  
  *A:* By using **Bucket Sort**! Create an array of lists `List<Integer>[] buckets` of size $N+1$, where `buckets[i]` stores elements that appear with frequency `i`. Iterate backward from `N` to 1 to collect $K$ elements in $O(N)$ time.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TOP K ELEMENTS PATTERN                                |
+-----------------------------------------------------------------------+
| • K Largest Elements : Use MIN-HEAP of fixed size K -> O(N log K) Time|
| • K Smallest Elements: Use MAX-HEAP of fixed size K -> O(N log K) Time|
| • Heap Eviction Rule : offer(x); if (pq.size() > K) pq.poll();        |
| • QuickSelect Bounds : O(N) Avg Time | O(1) Auxiliary Space ⚡         |
| • Top K Frequent (347): Freq Map + Capped Min-Heap OR Bucket Sort O(N)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Kth Largest Element (LeetCode 215) using fixed-size Min-Heap.
- [ ] I can write Kth Largest Element using QuickSelect in $O(N)$ avg time.
- [ ] I can write Top K Frequent Elements (LeetCode 347).
- [ ] I know why Min-Heap is used for K largest and Max-Heap for K smallest.
- [ ] I know how Bucket Sort achieves $O(N)$ time for Top K Frequent elements.
