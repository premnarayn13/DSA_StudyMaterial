# 06. Top-K Elements & Frequency Bucket Algorithms

## 1. Introduction
Finding the Top-$K$ Frequent Elements (LeetCode 347), $K$ Closest Points to Origin (LeetCode 973), and Top-$K$ Frequent Words (LeetCode 692) are fundamental data processing tasks in technical coding interviews. These problems evaluate two primary algorithmic paradigms: **Min-Heap Bounded Priority Queue** ($O(N \log K)$ time, $O(K)$ space) and **Bucket Sort Frequency Array** ($O(N)$ linear time, $O(N)$ space).

> **Important:** To find Top-$K$ Frequent Elements in **$O(N \log K)$ time**, use a **Min-Heap of size $K$** ordered by character/element frequency (`(a, b) -> Integer.compare(freqMap.get(a), freqMap.get(b))`). For optimal **$O(N)$ linear time**, use **Bucket Sort** where array index represents character frequency!

## 2. Core Concepts
* **Min-Heap Bounded Priority Queue ($O(N \log K)$ Time)**:
  * Count frequencies into a `HashMap<Integer, Integer>`.
  * Maintain a `PriorityQueue` of size $K$ ordered by frequency.
  * When `pq.size() > K`, `pq.poll()` evicts the least frequent element, leaving Top-$K$ elements in heap.
* **Bucket Sort Frequency Array ($O(N)$ Linear Time)**:
  * Index of bucket array `List<Integer>[] buckets` represents element frequency ($0 \dots N$).
  * Group elements into `buckets[freq]`.
  * Scan bucket array from index $N$ down to $0$, accumulating $K$ elements.

> **Memory Trick:** **"Top-K via Heap: Size K Min-Heap (O(N log K))! Top-K via Bucket Sort: Frequency Index Array (O(N) Linear Time)!"**

## 3. Characteristics / Properties
* **Complexity Comparison**:

```
Top-K Algorithmic Paradigms Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithmic Paradigm  | Time Complexity   | Auxiliary Space   | Best Use Case     |
+-----------------------+-------------------+-------------------+-------------------+
| Full Array Sorting    | O(N log N)        | O(N) Space         | Small inputs      |
| Min-Heap Bounded Size | O(N log K) ⚡     | O(K) Space ⚡     | Streaming inputs  |
| Bucket Sort Array     | O(N) Linear ⚡    | O(N) Space         | Static bounded $N$|
| QuickSelect (Hoare)   | O(N) Average      | O(1) Auxiliary    | In-place array    |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Bucket Sort Top-2 Frequent Elements on `nums = [1, 1, 1, 2, 2, 3], K = 2`:

```
Step 1: Build Frequency Map
map = {1: 3, 2: 2, 3: 1}

Step 2: Construct Bucket Array (index = frequency, max freq = 6)
buckets[1] = [3]
buckets[2] = [2]
buckets[3] = [1]

Step 3: Scan Buckets from index 6 down to 1 until K=2 elements collected
- Scan bucket 3 -> add 1 (collected = 1)
- Scan bucket 2 -> add 2 (collected = 2 -> Target K reached!)

Result Array: [1, 2] ✅ (Linear O(N) Time!)
```

## 5. Visual Diagram
Bucket Sort Frequency Index Mapping:

```
Frequency (Index):  [ 0 ]   [ 1 ]   [ 2 ]   [ 3 ]   [ 4 ]   [ 5 ]
Elements List:      [   ]   [ 3 ]   [ 2 ]   [ 1 ]   [   ]   [   ]
                              |       |       |
                              v       v       v
                           Freq=1  Freq=2  Freq=3

Scan Right-to-Left: Collect element '1' (freq 3), then element '2' (freq 2)!
```

## 6. Operations / Algorithms
LeetCode 347 Master Implementation (Both Approaches):

```java
// 1. Min-Heap Approach O(N log K) Time, O(N + K) Space
public int[] topKFrequentHeap(int[] nums, int k) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int num : nums) map.put(num, map.getOrDefault(num, 0) + 1);

    // Min-Heap ordered by element frequency
    PriorityQueue<Integer> pq = new PriorityQueue<>(
        (a, b) -> Integer.compare(map.get(a), map.get(b))
    );

    for (int num : map.keySet()) {
        pq.offer(num);
        if (pq.size() > k) {
            pq.poll(); // Evict least frequent
        }
    }

    int[] result = new int[k];
    for (int i = 0; i < k; i++) {
        result[i] = pq.poll();
    }
    return result;
}

// 2. Bucket Sort Approach O(N) Time, O(N) Space (OPTIMAL LINEAR TIME)
public int[] topKFrequentBucket(int[] nums, int k) {
    Map<Integer, Integer> map = new HashMap<>();
    for (int num : nums) map.put(num, map.getOrDefault(num, 0) + 1);

    List<Integer>[] buckets = new List[nums.length + 1];
    for (int num : map.keySet()) {
        int freq = map.get(num);
        if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
        buckets[freq].add(num);
    }

    int[] result = new int[k];
    int idx = 0;
    for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
        if (buckets[i] != null) {
            for (int num : buckets[i]) {
                result[idx++] = num;
                if (idx == k) break;
            }
        }
    }
    return result;
}
```

> **Quick Syntax:**
```java
// Bucket Sort List Array Setup
List<Integer>[] buckets = new List[nums.length + 1];
```

## 7. Examples
* **LeetCode 347 - Top K Frequent Elements**: Min-Heap vs Bucket Sort solutions.
* **LeetCode 973 - K Closest Points to Origin**: Max-Heap of size $K$ based on Euclidean distance $x^2 + y^2$.
* **LeetCode 692 - Top K Frequent Words**: Priority Queue with alphabetical tie-breaking.

## 8. Java Code
Complete interview-ready Java suite implementing Top K Frequent Elements (LeetCode 347) and K Closest Points to Origin (LeetCode 973):

```java
import java.util.*;

public class TopKElementsMaster {

    // 1. Top K Frequent Elements Bucket Sort O(N) Time, O(N) Space
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> countMap = new HashMap<>();
        for (int num : nums) countMap.put(num, countMap.getOrDefault(num, 0) + 1);

        List<Integer>[] buckets = new List[nums.length + 1];
        for (int key : countMap.keySet()) {
            int freq = countMap.get(key);
            if (buckets[freq] == null) buckets[freq] = new ArrayList<>();
            buckets[freq].add(key);
        }

        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null) {
                for (int num : buckets[i]) {
                    result[idx++] = num;
                    if (idx == k) break;
                }
            }
        }

        return result;
    }

    // 2. K Closest Points to Origin (LeetCode 973) O(N log K) Time, O(K) Space
    public static int[][] kClosest(int[][] points, int k) {
        // Max-Heap keeping K smallest distance points
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(b[0]*b[0] + b[1]*b[1], a[0]*a[0] + a[1]*a[1])
        );

        for (int[] point : points) {
            maxHeap.offer(point);
            if (maxHeap.size() > k) {
                maxHeap.poll(); // Evict point furthest from origin
            }
        }

        int[][] result = new int[k][2];
        for (int i = 0; i < k; i++) {
            result[i] = maxHeap.poll();
        }

        return result;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums = {1, 1, 1, 2, 2, 3};
        System.out.println("Top 2 Frequent Elements: " + Arrays.toString(topKFrequent(nums, 2)));
        // Output: [1, 2]

        int[][] points = {{1, 3}, {-2, 2}};
        int[][] closest = kClosest(points, 1);
        System.out.println("1 Closest Point to Origin: [" + closest[0][0] + ", " + closest[0][1] + "]");
        // Output: [-2, 2] (distance 8 < 10)
    }
}
```

## 9. Complexity Analysis
| Approach | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Bucket Sort** | **$O(N)$ Linear ⚡** | $O(N)$ Array Space | Index = Frequency |
| **Min-Heap (Size K)** | **$O(N \log K)$** | **$O(K)$ Heap Space ⚡**| Best for real-time streams |
| **Max-Heap Distance** | **$O(N \log K)$** | $O(K)$ Heap Space | Evicts furthest point |

## 10. Edge Cases
* **$K$ Equals Number of Unique Elements**: Bucket sort or heap returns all unique elements seamlessly.
* **Ties in Frequency**: Order of elements with identical frequency does not matter unless alphabetical tie-breaking is explicitly required (e.g. LeetCode 692).
* **Euclidean Distance Underflow**: $x^2 + y^2$ fits safely inside 32-bit `int` when coordinates are bounded within $[-10000, 10000]$.

## 11. Common Mistakes
* Using a Max-Heap of size $N$ for Top-$K$ elements (wastes memory and takes $O(N \log N)$ time!).
* Instantiating generic array of lists as `new ArrayList[N]` (causes Java generic array creation error!). Always write: **`List<Integer>[] buckets = new List[N + 1];`**.
* Forgetting to break out of bucket loops when `idx == k` is reached.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Bucket Sort Generic Array Syntax:
> Java does NOT allow `new ArrayList<Integer>[N]` generic array creation.
> Always write: **`List<Integer>[] buckets = new List[nums.length + 1];`**
> Then initialize entries on demand: `if (buckets[freq] == null) buckets[freq] = new ArrayList<>();`

> **Memory Trick:** **"Bucket Array Size must be nums.length + 1 (since max frequency is N)!"**

## 13. Comparisons
| Feature | Min-Heap PriorityQueue | Bucket Sort Array |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log K)$ | **$O(N)$ Linear Time ⚡** |
| **Auxiliary Space** | **$O(K)$ Space** | $O(N)$ Space |
| **Real-time Streams** | **YES (Supports dynamic `add()`)**| NO (Requires static count map) |
| **Interview Score** | Standard Optimal | **ADVANCED OPTIMAL LINEAR** |

## 14. How to Recognize This in Questions
* **"Find Top K most frequent elements"** $\rightarrow$ Bucket Sort ($O(N)$) or Min-Heap ($O(N \log K)$).
* **"Find K closest points to origin"** $\rightarrow$ Max-Heap of size $K$ based on distance.

## 15. Frequently Asked Interview Questions
* **Q: Why does Bucket Sort achieve $O(N)$ time for Top-$K$ Frequent Elements?**  
  *A:* Because element frequency cannot exceed $N$ (the array size). Building the frequency map takes $O(N)$, building the bucket array takes $O(N)$, and scanning buckets from $N$ down to 1 takes $O(N)$ total step iterations.
* **Q: Why do we use a MAX-HEAP of size $K$ for K Closest Points (LeetCode 973)?**  
  *A:* A Max-Heap of size $K$ keeps the point with the largest distance at its root. When a new point is closer than the root (`maxHeap.peek()`), we poll the root, evicting the furthest point and retaining the $K$ closest points.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TOP-K ELEMENTS & FREQUENCY BUCKETS                   |
+-----------------------------------------------------------------------+
| • Bucket Sort Array: List<Integer>[] buckets = new List[nums.length + 1];|
| • Bucket Index: Frequency (0..N). Store elements in buckets[freq]     |
| • Bucket Scan: Iterate from N down to 0; collect K elements in O(N) time|
| • Min-Heap Method: Maintain PQ of size K ordered by map.get(x)        |
| • K Closest Points: Max-Heap of size K based on dist = x^2 + y^2      |
| • Complexity: Bucket Sort O(N) Time | Min-Heap O(N log K) Time          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the Bucket Sort `List<Integer>[] buckets = new List[N + 1]` syntax.
- [ ] I know why Bucket Sort runs in $O(N)$ linear time.
- [ ] I can implement Top K Frequent Elements (LeetCode 347) using Bucket Sort.
- [ ] I can implement K Closest Points to Origin (LeetCode 973) using Max-Heap of size $K$.
- [ ] I can choose between Min-Heap and Bucket Sort based on streaming vs static constraints.
