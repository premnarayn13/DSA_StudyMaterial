# 09. Priority Task Scheduling & Reorganization Algorithms

## 1. Introduction
Task scheduling under cooling intervals (LeetCode 621 - Task Scheduler) and string character reorganization (LeetCode 767 - Reorganize String) are classic greedy priority queue problems in technical coding interviews. These problems evaluate combining a **Max-Heap Priority Queue** (for highest frequency task execution) with a **Cooling Wait Queue** (`Queue<int[]>`) to schedule tasks or rearrange characters such that no identical items execute within a specified cooldown interval $N$.

> **Important:** In Task Scheduler (LeetCode 621), greedily executing the task with the **highest remaining frequency** first using a Max-Heap guarantees the minimum total time intervals required to complete all tasks!

## 2. Core Concepts
* **Max-Heap + Cooldown Queue Architecture**:
  * **Max-Heap (`maxHeap`)**: Holds available tasks ordered by remaining execution frequency.
  * **Cooldown Queue (`waitQueue`)**: Holds cooling tasks as `int[]{remainingFreq, availableTime}` until current time $T \ge \text{availableTime}$.
* **Time Step Pipeline (Each Clock Cycle $T$)**:
  1. **Release Cooled Tasks**: If `waitQueue.peek()[1] <= T`, poll from `waitQueue` and offer back to `maxHeap`.
  2. **Execute Highest Frequency Task**: If `maxHeap` is non-empty, poll top task, decrement its frequency, and if `freq > 0`, push to `waitQueue` with `availableTime = T + N + 1`.
  3. **Idle Cycle**: If `maxHeap` is empty, CPU executes an IDLE cycle.
* **Mathematical Formula Shortcut for Task Scheduler**:
  $$\text{Min Intervals} = \max\Big(\text{tasks.length}, (\text{maxFreq} - 1) \cdot (N + 1) + \text{maxFreqCount}\Big)$$

> **Memory Trick:** **"Max-Heap for highest frequency task! Queue holds cooling tasks until time T >= availableTime!"**

## 3. Characteristics / Properties
* **Greedy Frequency Choice**: Executing tasks with maximum remaining frequency minimizes mandatory CPU IDLE slots.
* **Reorganize String Adjacency Constraint**: Reorganizing a string such that no two adjacent characters are identical is mathematically impossible if any character frequency exceeds $\lceil \frac{\text{length}}{2} \rceil$.

```
Task Scheduling & Reorganization Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Application | Core Data Struct  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| Task Scheduler (621)  | Max-Heap + Queue  | O(T) / O(26) ⚡   | O(26) Constant ⚡ |
| Reorganize String(767)| Max-Heap          | O(N log 26) ⚡    | O(26) Constant ⚡ |
| Rearrange K Apart     | Max-Heap + Queue  | O(N log 26) ⚡    | O(26) Constant ⚡ |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Task Scheduler (LeetCode 621) on `tasks = ["A","A","A","B","B","B"], N = 2` (Cooldown = 2):

```
Frequencies: A:3, B:3. Max-Heap = [A:3, B:3], waitQueue = [], Time T = 0

T=0: Exec A (freq becomes 2). Wait slot: [A:2, avail=0+2+1=3]. Time=1 | Heap: [B:3]
T=1: Exec B (freq becomes 2). Wait slot: [B:2, avail=1+2+1=4]. Time=2 | Heap: []
T=2: Heap empty! IDLE cycle. Time=3 | Wait: [A:2(avail 3), B:2(avail 4)]

T=3: Release A(avail 3)! Heap: [A:2]. Exec A (freq 1). Wait slot: [A:1, avail=6]. Time=4
T=4: Release B(avail 4)! Heap: [B:2]. Exec B (freq 1). Wait slot: [B:1, avail=7]. Time=5
T=5: IDLE cycle. Time=6

T=6: Release A! Exec A. Time=7
T=7: Release B! Exec B. Time=8

Total Time Intervals: 8 (Sequence: A -> B -> IDLE -> A -> B -> IDLE -> A -> B) ✅
```

## 5. Visual Diagram
Max-Heap + Cooldown Queue CPU Scheduling Pipeline:

```
                  +--------------------------------+
                  |  MAX-HEAP (Available Tasks)   |
                  |     [ Task A: 3, Task B: 2 ]   |
                  +--------------------------------+
                                  |
                                  v  (Poll highest freq task)
                         [ CPU EXECUTION ]
                                  |
                                  v  (If freq > 0, move to wait queue)
                  +--------------------------------+
                  | COOLDOWN QUEUE (Wait Buffer)   |
                  | [ Task A: 2, AvailTime: T+N+1 ]|
                  +--------------------------------+
```

## 6. Operations / Algorithms
LeetCode 621 & LeetCode 767 Master Implementation:

```java
// 1. Task Scheduler (LeetCode 621) O(N) Time, O(1) Space
public int leastInterval(char[] tasks, int n) {
    int[] freq = new int[26];
    for (char t : tasks) freq[t - 'A']++;

    Arrays.sort(freq);
    int maxFreq = freq[25];
    int maxCount = 0;

    for (int f : freq) {
        if (f == maxFreq) maxCount++;
    }

    int partCount = maxFreq - 1;
    int partLength = n - (maxCount - 1);
    int emptySlots = partCount * partLength;
    int availableTasks = tasks.length - (maxFreq * maxCount);
    int idles = Math.max(0, emptySlots - availableTasks);

    return tasks.length + idles;
}

// 2. Reorganize String (LeetCode 767) O(N log 26) Time, O(1) Space
public String reorganizeString(String s) {
    int[] freq = new int[26];
    for (char c : s.toCharArray()) freq[c - 'a']++;

    // Max-Heap ordered by character frequency
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
        (a, b) -> Integer.compare(b[1], a[1])
    );

    for (int i = 0; i < 26; i++) {
        if (freq[i] > 0) {
            // Impossible if max frequency exceeds (N + 1) / 2
            if (freq[i] > (s.length() + 1) / 2) return "";
            maxHeap.offer(new int[]{i + 'a', freq[i]});
        }
    }

    StringBuilder sb = new StringBuilder();
    int[] prev = null;

    while (!maxHeap.isEmpty()) {
        int[] curr = maxHeap.poll();

        // Re-insert previous character once a different character is placed
        if (prev != null && prev[1] > 0) {
            maxHeap.offer(prev);
        }

        sb.append((char) curr[0]);
        curr[1]--; // Decrement frequency
        prev = curr; // Store current as previous for next step
    }

    return sb.length() == s.length() ? sb.toString() : "";
}
```

> **Quick Syntax:**
```java
// Reorganize String Impossible Check
if (freq[i] > (s.length() + 1) / 2) return "";
```

## 7. Examples
* **LeetCode 621 - Task Scheduler**: Priority queue scheduling with cooling intervals.
* **LeetCode 767 - Reorganize String**: Max-Heap character interleaving.
* **LeetCode 358 - Rearrange String k Distance Apart**: Generalization of Reorganize String for distance $K$.

## 8. Java Code
Complete interview-ready Java suite implementing Task Scheduler and Reorganize String:

```java
import java.util.*;

public class TaskSchedulingMaster {

    // 1. Task Scheduler (LeetCode 621) O(N) Time, O(1) Space
    public static int leastInterval(char[] tasks, int n) {
        int[] freq = new int[26];
        for (char c : tasks) freq[c - 'A']++;

        Arrays.sort(freq);
        int maxFreq = freq[25];
        int maxCount = 0;

        for (int f : freq) {
            if (f == maxFreq) maxCount++;
        }

        int minTime = (maxFreq - 1) * (n + 1) + maxCount;
        return Math.max(tasks.length, minTime);
    }

    // 2. Reorganize String (LeetCode 767) O(N) Time, O(1) Space
    public static String reorganizeString(String s) {
        int[] freq = new int[26];
        for (char c : s.toCharArray()) freq[c - 'a']++;

        PriorityQueue<int[]> maxHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(b[1], a[1])
        );

        for (int i = 0; i < 26; i++) {
            if (freq[i] > 0) {
                if (freq[i] > (s.length() + 1) / 2) return "";
                maxHeap.offer(new int[]{i + 'a', freq[i]});
            }
        }

        StringBuilder sb = new StringBuilder();
        int[] prev = null;

        while (!maxHeap.isEmpty()) {
            int[] curr = maxHeap.poll();

            if (prev != null && prev[1] > 0) {
                maxHeap.offer(prev);
            }

            sb.append((char) curr[0]);
            curr[1]--;
            prev = curr;
        }

        return sb.toString();
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        char[] tasks = {'A','A','A','B','B','B'};
        int n = 2;
        System.out.println("Least Intervals Required: " + leastInterval(tasks, n)); // Output: 8

        String str = "aab";
        System.out.println("Reorganized 'aab': '" + reorganizeString(str) + "'"); // Output: "aba"

        String impossible = "aaab";
        System.out.println("Reorganized 'aaab': '" + reorganizeString(impossible) + "'"); // Output: ""
    }
}
```

## 9. Complexity Analysis
| Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Task Scheduler (Math)** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Fixed 26-element frequency array |
| **Task Scheduler (Heap)** | $O(\text{Total Intervals})$ | $O(1)$ Constant | Simulation step by step |
| **Reorganize String** | **$O(N \log 26) = O(N)$**| **$O(1)$ Constant ⚡**| Alphabet size bounded to 26 |

## 10. Edge Cases
* **Cooldown Interval $N = 0$**: Tasks execute back-to-back without idle cycles; answer is `tasks.length`.
* **Impossible Reorganization**: Max frequency $> (N + 1) / 2$ returns `""` immediately.
* **All Tasks Have Identical Frequency**: `maxCount` handles multiple highest frequency tasks seamlessly.

## 11. Common Mistakes
* Returning `minTime` without checking `Math.max(tasks.length, minTime)` (when $N$ is small, idle slots calculation can evaluate to negative values!).
* Inserting `curr` back into `maxHeap` immediately before popping the next character in Reorganize String (causes adjacent duplicate characters!).
* Using `Integer.compare(a[1], b[1])` instead of `Integer.compare(b[1], a[1])` for Max-Heap.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Task Scheduler Math Formula:
> **`minTime = (maxFreq - 1) * (n + 1) + maxCount;`**
> **`return Math.max(tasks.length, minTime);`**
> This 2-line math formula eliminates complex heap simulations and solves LeetCode 621 in $O(N)$ time and $O(1)$ space!

> **Memory Trick:** **"Min Intervals = Math.max(tasks.length, (maxFreq - 1) * (N + 1) + maxCount)"**

## 13. Comparisons
| Feature | Simulation via Max-Heap + Queue | Mathematical Formula Shortcut |
| :--- | :--- | :--- |
| **Time Complexity** | $O(\text{Total Intervals})$ | **$O(N)$ Linear Time ⚡** |
| **Auxiliary Space** | $O(26)$ Constant | **$O(1)$ Constant ⚡** |
| **Code Length** | ~40 lines | **~10 lines** |
| **Interview Recommendation** | Good backup | **OPTIMAL PREFERRED** |

## 14. How to Recognize This in Questions
* **"Find minimum CPU intervals to execute tasks with cooling distance N"** $\rightarrow$ Task Scheduler (LeetCode 621).
* **"Rearrange string so no two adjacent characters are identical"** $\rightarrow$ Reorganize String (LeetCode 767).

## 15. Frequently Asked Interview Questions
* **Q: Why does the Task Scheduler math formula take `Math.max(tasks.length, minTime)`?**  
  *A:* When the cooling interval $N$ is small or there are many distinct tasks, available tasks fill all empty cooling slots completely, leaving ZERO idle cycles. In that case, total intervals equals `tasks.length`.
* **Q: Why is Reorganize String impossible if max frequency $> (N + 1) / 2$?**  
  *A:* By the Pigeonhole Principle, even if we place the most frequent character at all alternate indices ($0, 2, 4 \dots$), there are only $\lceil N / 2 \rceil$ non-adjacent slots available. Exceeding this count forces at least two identical characters to be adjacent.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRIORITY TASK SCHEDULING & REORGANIZATION             |
+-----------------------------------------------------------------------+
| • Task Scheduler Math: minTime = (maxFreq - 1) * (n + 1) + maxCount   |
| • Final Answer: return Math.max(tasks.length, minTime);               |
| • Reorganize String Check: if (maxFreq > (N + 1) / 2) return "";      |
| • Reorganize Strategy: Max-Heap + prev pointer holding last placed char|
| • Complexity: O(N) Linear Time | O(1) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the 2-line Task Scheduler math formula.
- [ ] I know why `Math.max(tasks.length, minTime)` is mandatory.
- [ ] I know the Pigeonhole limit `(N + 1) / 2` for string reorganization.
- [ ] I can implement Reorganize String (LeetCode 767) using Max-Heap + `prev`.
- [ ] I can implement Task Scheduler (LeetCode 621) in $O(N)$ time.
