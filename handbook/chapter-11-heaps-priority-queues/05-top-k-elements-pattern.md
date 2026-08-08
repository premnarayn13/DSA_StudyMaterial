# 05. Top-K Elements Pattern, Fixed-Size Heaps & Quickselect Architecture

## 1. Introduction
The **Top-K Elements Pattern** is one of the most frequently tested algorithmic patterns in technical coding interviews. Problems requiring finding the $K$ largest, $K$ smallest, $K$ most frequent, or $K$ closest elements (e.g. LeetCode 215, 347, 692, 973, 767) can be solved efficiently in **$O(N \log K)$ time and $O(K)$ space** using a **Fixed-Size Priority Queue**. Furthermore, for static array selection, the **Quickselect Algorithm** optimizes selection to **$O(N)$ average linear time**.

> **Important:** To find the **Top K LARGEST** elements, maintain a **MIN-HEAP of size $K$**! Pushing elements into a Min-Heap and polling when `heap.size() > K` evicts the smallest numbers, leaving the $K$ largest elements in the heap! Conversely, to find the **Top K SMALLEST** elements, maintain a **MAX-HEAP of size $K$**!

```
Top-K Pattern Optimization Spectrum:
+-----------------------------------------------------------------------------------+
| Full Array Sorting       : Arrays.sort(arr)          -> O(N log N) Time, O(1) Space|
| Fixed-Size Heap Pattern  : Min-Heap of size K        -> O(N log K) Time, O(K) Space⚡|
| Quickselect Algorithm    : Partitioning (LeetCode 215)-> O(N) Avg Time, O(1) Space ⚡ |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Fixed-Size Heap Rule

### 2.1 The Min-Heap for Top K Largest Rule
Why do we use a Min-Heap of size $K$ to find the Top $K$ largest elements?
1. We iterate through $N$ elements.
2. We `offer(num)` into `minHeap`.
3. If `minHeap.size() > K`, we call **`minHeap.poll()`**.
4. Since `poll()` removes the **minimum element** currently in the heap, any small number is evicted immediately!
5. After processing all $N$ elements, the Min-Heap contains the **$K$ largest elements**, with the $K$-th largest element sitting at the top of the heap (`minHeap.peek()`).

```
Min-Heap vs Max-Heap Selection Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Selection Goal        | Required Heap Type| Size Limit Rule   | Eviction Trigger  |
+-----------------------+-------------------+-------------------+-------------------+
| Top K **Largest**     | **Min-Heap**      | Maintain Size $K$ | `if (size > K) poll()`|
| Top K **Smallest**    | **Max-Heap**      | Maintain Size $K$ | `if (size > K) poll()`|
+-----------------------+-------------------+-------------------+-------------------+
```

### 2.2 Quickselect Algorithm ($O(N)$ Average Time)
Quickselect adapts Quicksort partitioning to find the $K$-th largest element without sorting the entire array:
* Pick a pivot element.
* Partition array into elements $> \text{pivot}$ and elements $< \text{pivot}$.
* If pivot index equals $K-1$, return `pivot`!
* If pivot index $> K-1$, recurse on Left partition only.
* If pivot index $< K-1$, recurse on Right partition only.
* **Time Complexity**: $N + N/2 + N/4 + \dots = 2N = \mathbf{O(N)\text{ Average Time}}$.

> **Memory Trick:** **"Top K Largest = Min-Heap of size K! Top K Smallest = Max-Heap of size K! Quickselect = O(N) average time!"**

---

## 3. Characteristics & Complex Ranking Criteria (LeetCode 692)

### 3.1 Custom Multi-Tier Comparators (Top K Frequent Words)
In LeetCode 692 (Top K Frequent Words), elements must be sorted by **Frequency (Descending)**, but words with equal frequency must be sorted **Alphabetically (Ascending)**!
When using a Min-Heap of size $K$, the comparator must invert logic:
* If frequencies differ: Min-Heap orders by lower frequency first (`Integer.compare(freqA, freqB)`).
* If frequencies are equal: Min-Heap orders by lexicographically LARGER string first (`wordB.compareTo(wordA)`), so that lexicographically larger words are evicted first during `poll()`!

```java
PriorityQueue<String> minHeap = new PriorityQueue<>(
    (w1, w2) -> {
        int f1 = freqMap.get(w1);
        int f2 = freqMap.get(w2);
        if (f1 != f2) return Integer.compare(f1, f2); // Primary: Frequency Ascending
        return w2.compareTo(w1); // Secondary: Lexicographically Descending for eviction!
    }
);
```

---

## 4. Internal Working Mechanics
Tracing Top 2 Largest Elements on array `[3, 10, 5, 20, 2]` using Min-Heap of size $K=2$:

```
Initial Min-Heap = []

- Num 3 : offer(3).  Heap: [3]. Size <= 2.
- Num 10: offer(10). Heap: [3, 10]. Size <= 2.
- Num 5 : offer(5).  Heap: [3, 10, 5]. Size 3 > 2 -> poll() evicts MIN (3).
          Heap becomes: [5, 10]
- Num 20: offer(20). Heap: [5, 10, 20]. Size 3 > 2 -> poll() evicts MIN (5).
          Heap becomes: [10, 20]
- Num 2 : offer(2).  Heap: [2, 20, 10]. Size 3 > 2 -> poll() evicts MIN (2).
          Heap becomes: [10, 20]

Result: Top 2 Largest Elements = [10, 20] ✅ (O(N log K) Time!)
```

---

## 5. Visual Diagram
Min-Heap Eviction Mechanics for Top K Largest:

```
Incoming Stream: 3, 10, 5, 20, 2 (K = 2)

Step 1: Push 3, 10        ===> Heap: [3, 10]
Step 2: Push 5 -> [3,10,5]===> Evict Min (3)  ===> Heap: [5, 10]
Step 3: Push 20-> [5,10,20]===> Evict Min (5)  ===> Heap: [10, 20]
Step 4: Push 2 -> [2,10,20]===> Evict Min (2)  ===> Heap: [10, 20]

Final Heap contains 2 Largest Elements [10, 20]!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Top K Frequent Words (LeetCode 692), K Closest Points to Origin (LeetCode 973), Reorganize String (LeetCode 767), and Quickselect (LeetCode 215):

```java
import java.util.*;

public class TopKPatternMaster {

    // 1. Top K Frequent Words (LeetCode 692) O(N log K) Time, O(N) Space
    public static List<String> topKFrequent(String[] words, int k) {
        Map<String, Integer> freqMap = new HashMap<>();
        for (String w : words) {
            freqMap.put(w, freqMap.getOrDefault(w, 0) + 1);
        }

        // Min-Heap based on frequency; reverse alphabetical for tie-breaking
        PriorityQueue<String> minHeap = new PriorityQueue<>((w1, w2) -> {
            int f1 = freqMap.get(w1);
            int f2 = freqMap.get(w2);
            if (f1 != f2) return Integer.compare(f1, f2);
            return w2.compareTo(w1);
        });

        for (String word : freqMap.keySet()) {
            minHeap.offer(word);
            if (minHeap.size() > k) {
                minHeap.poll();
            }
        }

        List<String> result = new ArrayList<>();
        while (!minHeap.isEmpty()) {
            result.add(minHeap.poll());
        }
        Collections.reverse(result); // Reverse to get highest frequency first
        return result;
    }

    // 2. K Closest Points to Origin (LeetCode 973) O(N log K) Time, O(K) Space
    public static int[][] kClosest(int[][] points, int k) {
        // Max-Heap storing points ordered by distance squared (x^2 + y^2)
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
            (p1, p2) -> Integer.compare(p2[0]*p2[0] + p2[1]*p2[1], p1[0]*p1[0] + p1[1]*p1[1])
        );

        for (int[] point : points) {
            maxHeap.offer(point);
            if (maxHeap.size() > k) {
                maxHeap.poll(); // Evict point with furthest distance!
            }
        }

        int[][] result = new int[k][2];
        for (int i = 0; i < k; i++) {
            result[i] = maxHeap.poll();
        }
        return result;
    }

    // 3. Reorganize String (LeetCode 767) Max-Heap Greedy Placement
    public static String reorganizeString(String s) {
        int[] counts = new int[26];
        for (char c : s.toCharArray()) counts[c - 'a']++;

        // Max-Heap storing [char, count]
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b[1], a[1]));
        for (int i = 0; i < 26; i++) {
            if (counts[i] > 0) {
                if (counts[i] > (s.length() + 1) / 2) return ""; // Impossible!
                maxHeap.offer(new int[]{i + 'a', counts[i]});
            }
        }

        StringBuilder sb = new StringBuilder();
        int[] prev = null;

        while (!maxHeap.isEmpty()) {
            int[] curr = maxHeap.poll();
            sb.append((char) curr[0]);
            curr[1]--;

            if (prev != null && prev[1] > 0) {
                maxHeap.offer(prev); // Re-insert previous character
            }

            prev = curr;
        }

        return sb.length() == s.length() ? sb.toString() : "";
    }

    // 4. Quickselect Algorithm for Kth Largest Element (LeetCode 215) O(N) Avg Time, O(1) Space
    public static int findKthLargestQuickselect(int[] nums, int k) {
        int targetIdx = nums.length - k; // Kth largest is at index N - k in sorted array
        return quickselect(nums, 0, nums.length - 1, targetIdx);
    }

    private static int quickselect(int[] nums, int left, int right, int k) {
        if (left == right) return nums[left];

        int pivotIdx = partition(nums, left, right);

        if (pivotIdx == k) return nums[k];
        else if (pivotIdx < k) return quickselect(nums, pivotIdx + 1, right, k);
        else return quickselect(nums, left, pivotIdx - 1, k);
    }

    private static int partition(int[] nums, int left, int right) {
        int pivot = nums[right];
        int i = left;
        for (int j = left; j < right; j++) {
            if (nums[j] <= pivot) {
                swap(nums, i, j);
                i++;
            }
        }
        swap(nums, i, right);
        return i;
    }

    private static void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Fixed-Size Min-Heap Top-K Eviction Syntax
minHeap.offer(element);
if (minHeap.size() > k) minHeap.poll(); // Evicts smallest element!
```

---

## 7. Concrete Problem Examples
* **LeetCode 692 - Top K Frequent Words**: Multi-tier priority queue sorting.
* **LeetCode 973 - K Closest Points to Origin**: Fixed-size Max-Heap.
* **LeetCode 767 - Reorganize String**: Greedy character placement with Max-Heap.
* **LeetCode 215 - Kth Largest Element**: Quickselect $O(N)$ average time.

---

## 8. Java Code Demonstration & Dry Run
Demonstration finding Top 2 Frequent Words and K Closest Points:

```java
public class TopKPatternDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Top K Frequent Words (LeetCode 692) ===");
        String[] words = {"i", "love", "leetcode", "i", "love", "coding"};
        List<String> topWords = TopKPatternMaster.topKFrequent(words, 2);
        System.out.println("Top 2 Frequent Words: " + topWords); // Output: ["i", "love"]

        System.out.println("\n=== 2. K Closest Points to Origin (LeetCode 973) ===");
        int[][] points = {{1, 3}, {-2, 2}, {5, 8}, {0, 1}};
        int[][] closest = TopKPatternMaster.kClosest(points, 2);
        System.out.println("2 Closest Points: " + Arrays.deepToString(closest)); // Output: [[0, 1], [-2, 2]]
    }
}
```

---

## 9. Complexity Analysis

| Algorithm Strategy | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Fixed-Size Min-Heap**| **$O(N \log K)$ Time ⚡** | **$O(K)$ Space ⚡**| Works online on data streams |
| **Quickselect (215)** | **$O(N)$ Average ⚡** | **$O(1)$ In-Place ⚡**| Fastest static array selection |
| **Full Array Sort** | $O(N \log N)$ Time | $O(1)$ / $O(N)$ Space | Suboptimal for small $K \ll N$ |

---

## 10. Edge Cases & Boundary Handling
* **$K$ Equals Array Length ($K = N$)**: Min-Heap retains all $N$ elements; returning sorted heap takes $O(N \log N)$ time.
* **$K = 1$**: Reduces to finding single minimum or maximum element in $O(N)$ linear time without a priority queue.

---

## 11. Common Mistakes & Anti-Patterns
* **Using a Max-Heap for Top K Largest Elements**:
  - Using a Max-Heap requires storing ALL $N$ elements in the heap $\implies \mathbf{O(N \log N)\text{ Time and }O(N)\text{ Space}}$.
  - **Fix**: Use a **Min-Heap of size $K$** to achieve $O(N \log K)$ time and $O(K)$ space.
* **Inverting Tie-Breaking Comparator Logic**: In Top K Frequent Words, forgetting to invert the string comparison (`w2.compareTo(w1)`) causes lexicographically larger words to be retained instead of evicted.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Fixed-Size Heap vs Quickselect Choice:
> * **Data Stream / Online Queries** $\implies$ **Fixed-Size Min-Heap ($O(N \log K)$ time, $O(K)$ space)**.
> * **Static Array in Memory** $\implies$ **Quickselect ($O(N)$ average time, $O(1)$ space)**.

> **Memory Trick:** **"Top K Largest Stream -> Min-Heap size K! Static Array -> Quickselect O(N)!"**

---

## 13. System & Implementation Comparisons

| Feature | Fixed-Size Min-Heap | Quickselect Algorithm |
| :--- | :--- | :--- |
| **Data Stream Friendly**| **YES (Online Streaming) ⚡**| NO (Requires full array in memory) |
| **Worst-Case Time** | **$O(N \log K)$ Guaranteed ⚡**| $O(N^2)$ (Worst-case quadratic) |
| **Auxiliary Memory** | $O(K)$ Heap Storage | **$O(1)$ In-Place ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find top K most frequent elements"** $\rightarrow$ HashMap frequency count + Min-Heap of size $K$.
* **"Find K closest points to origin"** $\rightarrow$ Max-Heap of size $K$ ordering by distance squared.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a Min-Heap of size $K$ find the Top $K$ LARGEST elements?**  
  *A:* Because `minHeap.peek()` exposes the SMALLEST element among the $K$ elements currently in the heap. When a new element comes in, polling the min-heap evicts the smallest number. At the end, only the $K$ largest elements remain.
* **Q: Why does Reorganize String (LeetCode 767) return `""` if `maxFreq > (N + 1) / 2`?**  
  *A:* By the Pigeonhole Principle, if a single character appears more than `(N + 1) / 2` times, it is mathematically impossible to place it without two identical characters being adjacent.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TOP-K ELEMENTS PATTERN & QUICKSELECT                  |
+-----------------------------------------------------------------------+
| • Top K LARGEST Rule: Min-Heap of size K (poll when size > K)         |
| • Top K SMALLEST Rule: Max-Heap of size K (poll when size > K)        |
| • Quickselect: Partitioning target idx N-k -> O(N) Average Time       |
| • Multi-Tier Comparators: Primary = Freq Ascending; Secondary = Lex   |
|   Descending for correct Min-Heap eviction                            |
| • Reorganize String: Max-Heap greedy placement + prev buffer          |
| • Streaming Advantage: Min-Heap works online on continuous data streams|
| • Complexity: Heap O(N log K) Time, O(K) Space | Quickselect O(N) Time|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Min-Heap of size $K$ pattern in under 2 minutes.
- [ ] I know why Min-Heap finds top $K$ largest while Max-Heap finds top $K$ smallest.
- [ ] I can write Top K Frequent Words (LeetCode 692) with tie-breaking comparator.
- [ ] I can write K Closest Points to Origin (LeetCode 973).
- [ ] I can write Quickselect (LeetCode 215) in $O(N)$ average time.
