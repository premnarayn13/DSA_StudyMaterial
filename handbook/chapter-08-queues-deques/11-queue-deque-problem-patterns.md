# 11. Queue & Deque Problem Recognition Patterns

## 1. Introduction
Solving queue and deque problems in technical coding interviews requires rapid pattern recognition. Identifying problem signals—such as level-order tree traversal, sliding window maximums, stream top-$K$ elements, $K$-way stream merging, or running median tracking—dictates the optimal algorithmic pattern: Snapshot FIFO Queue, Monotonic Decreasing Deque, Min-Heap Bounded Priority Queue, $K$-Way Merge Heap, or Two Heaps Dual Balancing.

> **Important:** Recognizing whether a sliding window query requires a **Monotonic Deque** ($O(N)$ linear time) vs a **PriorityQueue** ($O(N \log K)$ time) distinguishes expert interview candidates.

## 2. Core Concepts
* **Pattern 1: FIFO Snapshot Queue (`ArrayDeque`)**: Triggered by "Level-order tree traversal", "Shortest path in unweighted graph". Snapshot level size via `int size = queue.size()`.
* **Pattern 2: Monotonic Decreasing Deque**: Triggered by "Sliding window maximum of size K". Store indices, evict expired indices from Front (`peekFirst() <= i - K`), evict smaller values from Rear (`nums[i] >= nums[peekLast()]`).
* **Pattern 3: Bounded Min-Heap Priority Queue**: Triggered by "Top K frequent elements", "Kth largest element in stream". Bounded heap size to $K$ (`pq.size() > K \implies pq.poll()`).
* **Pattern 4: Bucket Sort Frequency Array**: Triggered by "Top K frequent elements in linear time". Array index represents element frequency ($O(N)$ time).
* **Pattern 5: K-Way Stream Merge**: Triggered by "Merge K sorted lists", "Find K pairs with smallest sums". Bounded heap size to $K$ streams.
* **Pattern 6: Two Heaps Dual Partitioning**: Triggered by "Find median from data stream in O(1) time". Max-Heap for small half, Min-Heap for large half.

> **Memory Trick:** **"Level BFS? Snapshot Queue! Sliding Window Max? Monotonic Deque! Running Median? Two Heaps!"**

## 3. Characteristics / Properties
* **Pattern Recognition Decision Matrix**:

```
Problem Phrasing / Signal                      Optimal Queue/Deque Pattern  Target Complexity
---------------------------------------------------------------------------------------------
Level order tree / Unweighted shortest path   Snapshot FIFO Queue (BFS)    O(V + E) Time
Sliding window maximum of size K               Monotonic Decreasing Deque   O(N) Time, O(K) Space ⚡
Top K frequent elements (Linear Time)          Bucket Sort Frequency Array  O(N) Time, O(N) Space ⚡
Top K frequent elements (Stream)               Min-Heap Bounded Size K      O(N log K) Time, O(K) Space
Merge K sorted lists / streams                 K-Way Merge Heap             O(N log K) Time, O(K) Space
Find running median from data stream           Two Heaps (Max-Heap + Min-Heap) O(log N) Add, O(1) Find ⚡
Task scheduling with cooldown N                Max-Heap + Cooldown Queue    O(N) Time, O(1) Space ⚡
LRU Cache with O(1) get & put                  HashMap + Doubly LinkedList  O(1) Time, O(N) Space ⚡
```

## 4. Internal Working
Decision Tree for Selecting Queue and Deque Patterns:

```
                    [ Queue / Deque Problem ]
                               |
            +------------------+------------------+
            |                                     |
   [ Unweighted Sequence ]                [ Priority / Order ]
            |                                     |
   +--------+--------+                   +--------+--------+
   |                 |                   |                 |
[Level BFS]    [Sliding Window]       [Top-K / Stream]    [Running Median]
   |                 |                   |                 |
(FIFO Queue)  (Monotonic Deque)       (PriorityQueue)     (Two Heaps)
```

## 5. Visual Diagram
Summary of All Core Queue/Deque Patterns:

```
[ FIFO SNAPSHOT QUEUE ]
int size = q.size(); for (int i = 0; i < size; i++) { curr = q.poll(); }

[ MONOTONIC DEQUE (SLIDING WINDOW MAX) ]
Front (peekFirst() = Window Max) <=== Deque ===> Rear (pollLast() evicts smaller)

[ TWO HEAPS PATTERN ]
Max-Heap (Small Half) <=== Median Boundary ===> Min-Heap (Large Half)
```

## 6. Operations / Algorithms
Master Pattern Recognition Code Snippets:

```java
// Pattern 1: Monotonic Deque Window Max
if (!deque.isEmpty() && deque.peekFirst() <= i - k) deque.pollFirst();
while (!deque.isEmpty() && nums[i] >= nums[deque.peekLast()]) deque.pollLast();
deque.offerLast(i);
if (i >= k - 1) res[i - k + 1] = nums[deque.peekFirst()];

// Pattern 2: Bounded Min-Heap Top-K
pq.offer(num);
if (pq.size() > k) pq.poll();

// Pattern 3: Two Heaps Rebalance
if (maxHeap.size() > minHeap.size() + 1) minHeap.offer(maxHeap.poll());
else if (maxHeap.size() < minHeap.size()) maxHeap.offer(minHeap.poll());
```

> **Quick Syntax:**
```java
// Modern Java Deque Setup
Deque<Integer> deque = new ArrayDeque<>();
```

## 7. Examples
* **LeetCode 239 - Sliding Window Maximum**: Monotonic Deque pattern.
* **LeetCode 295 - Find Median from Data Stream**: Two Heaps pattern.
* **LeetCode 347 - Top K Frequent Elements**: Bucket Sort / Min-Heap pattern.

## 8. Java Code
Complete interview-ready Java suite demonstrating pattern selection across major queue/deque interview problems:

```java
import java.util.*;

public class QueueDequePatternRecognitionMaster {

    // Pattern 1: Binary Tree Level Order Traversal (LeetCode 102) O(N) Time, O(N) Space
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        while (!queue.isEmpty()) {
            int levelSize = queue.size(); // Snapshot level size
            List<Integer> currentLevel = new ArrayList<>();

            for (int i = 0; i < levelSize; i++) {
                TreeNode curr = queue.poll();
                currentLevel.add(curr.val);

                if (curr.left != null)  queue.offer(curr.left);
                if (curr.right != null) queue.offer(curr.right);
            }

            result.add(currentLevel);
        }

        return result;
    }

    public static class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);

        System.out.println("Level Order Traversal: " + levelOrder(root));
        // Output: [[3], [9, 20], [15, 7]]
    }
}
```

## 9. Complexity Analysis
| Pattern / Technique | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Snapshot FIFO Queue** | **$O(V + E)$ Linear** | **$O(V)$ Queue Space**| Guarantees level-by-level processing |
| **Monotonic Deque** | **$O(N)$ Linear** | **$O(K)$ Deque Space**| Amortized $O(N)$ window queries ⚡ |
| **Bounded Min-Heap** | **$O(N \log K)$** | **$O(K)$ Heap Space**| Bounded memory stream processing |
| **Two Heaps Pattern** | **$O(\log N)$ Add** | **$O(N)$ Space** | $O(1)$ constant-time running median |

## 10. Edge Cases
* **Level Size Dynamic Mutation Bug**: Forgetting `int levelSize = queue.size()` causes BFS to mix levels.
* **Modulo Negative Result Bug**: Circular Deque front insertion must use `(head - 1 + capacity) % capacity`.
* **Equal Priority Ties**: Add explicit tie-breaking comparator when required.

## 11. Common Mistakes
* Writing `i < queue.size()` inside BFS level loops.
* Using `PriorityQueue` for Sliding Window Maximum (takes $O(N \log K)$ instead of $O(N)$ Monotonic Deque!).
* Using `LinkedList` when `ArrayDeque` offers superior cache hits and zero GC pressure.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Master Pattern Selection Rules:
> 1. **Level BFS / Unweighted Graph?** $\implies$ Snapshot FIFO Queue (`int size = queue.size()`).
> 2. **Sliding Window Max / Min?** $\implies$ Monotonic Deque (`peekFirst()`).
> 3. **Top K Frequent Elements?** $\implies$ Bucket Sort ($O(N)$) or Bounded Min-Heap ($O(N \log K)$).
> 4. **Merge K Streams?** $\implies$ $K$-Way Merge Heap (`[val, i, j]`).
> 5. **Running Median?** $\implies$ Two Heaps (`maxHeap` small half, `minHeap` large half).

> **Memory Trick:** **"Snapshot size for BFS; Monotonic Deque for Window Max; Two Heaps for Running Median!"**

## 13. Comparisons
| Problem Signal | Sub-Optimal Pattern | Optimal Queue/Deque Pattern |
| :--- | :--- | :--- |
| **Sliding Window Maximum** | PriorityQueue ($O(N \log K)$) | **Monotonic Deque ($O(N)$ Linear ⚡)** |
| **Top K Frequent Elements** | Full Array Sort ($O(N \log N)$) | **Bucket Sort Array ($O(N)$ Linear ⚡)** |
| **Running Median** | Re-sorting Array ($O(N \log N)$) | **Two Heaps ($O(1)$ Query ⚡)** |

## 14. How to Recognize This in Questions
* **"Find maximum in every window of size K"** $\rightarrow$ Monotonic Deque (LeetCode 239).
* **"Find median of data stream in O(1) query time"** $\rightarrow$ Two Heaps Pattern (LeetCode 295).

## 15. Frequently Asked Interview Questions
* **Q: Why does Monotonic Deque beat PriorityQueue for Sliding Window Maximum?**  
  *A:* PriorityQueue takes $O(\log K)$ to offer and poll elements, taking $O(N \log K)$ total time. Monotonic Deque evicts elements from both ends in $O(1)$ amortized time, processing all $N$ elements in $O(N)$ total time.
* **Q: Why is `ArrayDeque` preferred over `LinkedList` for Queues and Deques in Java?**  
  *A:* `ArrayDeque` uses a contiguous array buffer, maximizing CPU L1/L2 cache hits and incurring zero runtime Garbage Collection pressure. `LinkedList` allocates individual 24-byte node objects scattered across heap memory.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUEUE & DEQUE PROBLEM RECOGNITION PATTERNS            |
+-----------------------------------------------------------------------+
| • BFS Template: int levelSize = queue.size(); for (0..levelSize-1)    |
| • Monotonic Deque: Evict Front if peekFirst() <= i-k; Evict Rear if   |
|   nums[i] >= nums[peekLast()]; Result = nums[peekFirst()]             |
| • Top K Linear: Bucket Sort List<Integer>[] buckets = new List[N + 1] |
| • Two Heaps: maxHeap (left small half) & minHeap (right large half)   |
| • Target Performance: Prefer O(N) Monotonic Deque & Bucket Sort       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can select the optimal queue/deque pattern within 60 seconds.
- [ ] I always capture `int levelSize = queue.size()` before BFS loops.
- [ ] I can write the 4-step Monotonic Deque loop for Sliding Window Maximum.
- [ ] I can implement Two Heaps for Running Median (LeetCode 295).
- [ ] I know why `ArrayDeque` is superior to `LinkedList` in Java.
