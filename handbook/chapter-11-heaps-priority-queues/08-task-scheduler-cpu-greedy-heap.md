# 08. Task Scheduling, CPU Resource Allocation & Greedy Heap Algorithms

## 1. Introduction
Solving complex CPU scheduling and resource allocation problems—such as **Task Scheduler (LeetCode 621)**, **Single-Threaded CPU (LeetCode 1834)**, **Minimum Number of Refueling Stops (LeetCode 871)**, and **Minimum Cost to Hire K Workers (LeetCode 857)**—represents an advanced application of Priority Queues. These problems combine **Greedy Decision Making** with dynamic Max-Heap or Min-Heap tracking to optimize CPU execution cycles, idle time, fuel consumption, or wage ratios in **$O(N \log N)$ time**.

> **Important:** In Task Scheduler (LeetCode 621), the optimal greedy policy always executes the task with the **Highest Remaining Frequency** first! Using a **Max-Heap** paired with a **Cooldown Buffer Queue** simulates CPU execution cycles dynamically while respecting the mandatory $N$-cycle cooldown constraint!

```
Task Scheduling & Greedy Heap Spectrum:
+-----------------------------------------------------------------------------------+
| CPU Task Scheduler (621)  : Max-Heap + Cooldown Queue    -> Simulates CPU Cycles ⚡|
| Single-Threaded CPU (1834): Min-Heap Processing Time     -> Shortest Job First ⚡  |
| Refueling Stops (871)     : Max-Heap Available Fuel      -> Greedy Max Refuel ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Greedy Task Scheduling Architecture

### 2.1 Task Scheduler (LeetCode 621)
Given a character array of tasks `tasks` and a non-negative cooldown integer `n`:
* **Rule**: Identical tasks must be separated by at least `n` CPU cycles (where the CPU can execute another task or remain IDLE).
* **Greedy Max-Heap Strategy**:
  1. Count task frequencies into an array `counts[26]`.
  2. Push all non-zero task frequencies into a **Max-Heap** `maxHeap`.
  3. Maintain a **Cooldown Queue** storing `Pair{remainingCount, availableTime}`.
  4. At each time unit `time`:
     - If `maxHeap` has tasks, poll max frequency `currCount`, decrement `currCount--`. If `currCount > 0`, push into `cooldownQueue` with `availableTime = time + n + 1`.
     - Check `cooldownQueue`: If front task's `availableTime == time`, poll from queue and re-insert into `maxHeap`!
     - Increment `time++`.

### 2.2 Mathematical Formula Alternative for LeetCode 621 ($O(N)$ Time)
Task Scheduler can also be solved mathematically without simulating individual cycles:
* Find the maximum task frequency `maxFreq`.
* Count how many tasks share this maximum frequency: `maxFreqCount`.
* The minimum total cycles required is:

$$\text{TotalCycles} = \mathbf{\max(\text{tasks.length}, (\text{maxFreq} - 1) \cdot (n + 1) + \text{maxFreqCount})}$$

```
Mathematical Grid Layout for Task Scheduler:
Tasks: [A, A, A, B, B, B], n = 2
maxFreq = 3 ('A' and 'B'), maxFreqCount = 2

Frame Layout (maxFreq - 1 = 2 chunks of size n + 1 = 3):
Chunk 1: A B IDLE
Chunk 2: A B IDLE
Last   : A B
Total Cycles = (3 - 1) * (2 + 1) + 2 = 2 * 3 + 2 = 8 cycles! ✅
```

> **Memory Trick:** **"Greedy Task Scheduler: Max-Heap executes highest frequency first! Math formula: (maxFreq - 1) * (n + 1) + maxFreqCount!"**

---

## 3. Characteristics & Complex Greedy Heap Scenarios

### 3.1 Single-Threaded CPU (LeetCode 1834 - Shortest Job First)
* **Goal**: Process tasks on a single-threaded CPU ordering by **Shortest Processing Time** (and tie-breaking by smallest original index).
* **Strategy**:
  - Sort tasks by `enqueueTime`.
  - Maintain a **Min-Heap** ordering by `[processingTime, index]`.
  - At time `currTime`:
    - Push all tasks whose `enqueueTime <= currTime` into `minHeap`.
    - If `minHeap` is empty, advance `currTime` to the `enqueueTime` of the next available task!
    - Poll shortest job `[procTime, idx]` from `minHeap`, execute task, and increment `currTime += procTime`.

### 3.2 Minimum Number of Refueling Stops (LeetCode 871)
* **Goal**: Reach target distance with minimum refueling stops.
* **Strategy**:
  - Travel along stations.
  - Maintain a **Max-Heap** storing capacities of all gas stations passed so far.
  - When current fuel is insufficient to reach the next station/target:
    - Greedily poll the **largest fuel capacity** from `maxHeap` (`fuel += maxHeap.poll()`) and increment `stopCount++`.
    - Repeat until fuel is sufficient or `maxHeap` becomes empty (unreachable!).

```
Greedy Refueling Heap Strategy:
Current Fuel < Station Distance?
===> Greedily poll MAX FUEL station passed from Max-Heap!
```

---

## 4. Internal Working Mechanics
Tracing Task Scheduler (LeetCode 621) on `tasks = [A, A, A, B, B, B], n = 2`:

```
Counts: A=3, B=3 -> Max-Heap = [3, 3] (Frequencies)

Time 1: Poll 3 (A). Remaining = 2. Cooldown Queue: Push (2, avail=1+2+1=4). maxHeap: [3]
Time 2: Poll 3 (B). Remaining = 2. Cooldown Queue: Push (2, avail=2+2+1=5). maxHeap: []
Time 3: maxHeap empty, cooldownQueue has (2, avail=4) -> IDLE cycle!
Time 4: Time == 4 -> Cooldown queue releases (2, A). maxHeap: [2].
        Poll 2 (A). Remaining = 1. Cooldown Queue: Push (1, avail=4+2+1=7).
Time 5: Time == 5 -> Cooldown queue releases (2, B). maxHeap: [2].
        Poll 2 (B). Remaining = 1. Cooldown Queue: Push (1, avail=5+2+1=8).
Time 6: IDLE cycle!
Time 7: Process A.
Time 8: Process B.

Total Time Units = 8 ✅ (Matches Math Formula!)
```

---

## 5. Visual Diagram
Single-Threaded CPU Task Pipeline Topology (LeetCode 1834):

```
Time Line:  0 -------- 2 ----------------- 6 ------------ 9
            |          |                   |              |
          Task 0     Task 1              Task 2         Task 3
       (enq=0, p=2) (enq=2, p=4)        (enq=3, p=2)   (enq=6, p=1)

Min-Heap Task Buffer (Shortest Processing Time First):
At t=2: Available = [ (p=4, idx=1) ] -> Executing Task 1 (t=2..6)
At t=6: Available = [ (p=2, idx=2), (p=1, idx=3) ]
        Min-Heap polls (p=1, idx=3) FIRST! (Shortest Job First!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Task Scheduler (LeetCode 621), Single-Threaded CPU (LeetCode 1834), and Minimum Refueling Stops (LeetCode 871):

```java
import java.util.*;

public class CPUTaskSchedulerMaster {

    // 1. Task Scheduler (LeetCode 621) Math O(N) Time, O(1) Space
    public static int leastIntervalMath(char[] tasks, int n) {
        int[] counts = new int[26];
        for (char c : tasks) {
            counts[c - 'A']++;
        }

        int maxFreq = 0;
        for (int count : counts) {
            maxFreq = Math.max(maxFreq, count);
        }

        int maxFreqCount = 0;
        for (int count : counts) {
            if (count == maxFreq) {
                maxFreqCount++;
            }
        }

        int partCount = maxFreq - 1;
        int partLength = n - (maxFreqCount - 1);
        int emptySlots = partCount * partLength;
        int availableTasks = tasks.length - (maxFreq * maxFreqCount);
        int idles = Math.max(0, emptySlots - availableTasks);

        return tasks.length + idles;
    }

    // 2. Single-Threaded CPU (LeetCode 1834) O(N log N) Time, O(N) Space
    public static int[] getOrder(int[][] tasks) {
        int n = tasks.length;
        int[][] extendedTasks = new int[n][3];
        for (int i = 0; i < n; i++) {
            extendedTasks[i][0] = tasks[i][0]; // enqueueTime
            extendedTasks[i][1] = tasks[i][1]; // processingTime
            extendedTasks[i][2] = i;           // original index
        }

        // Sort by enqueueTime ascending
        Arrays.sort(extendedTasks, (a, b) -> Integer.compare(a[0], b[0]));

        // Min-Heap sorting by [processingTime, originalIndex]
        PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> {
            if (a[1] != b[1]) return Integer.compare(a[1], b[1]);
            return Integer.compare(a[2], b[2]);
        });

        int[] result = new int[n];
        int resultIdx = 0;
        int taskIdx = 0;
        long currentTime = 0;

        while (resultIdx < n) {
            // Push all tasks available at or before currentTime
            while (taskIdx < n && extendedTasks[taskIdx][0] <= currentTime) {
                minHeap.offer(extendedTasks[taskIdx]);
                taskIdx++;
            }

            if (minHeap.isEmpty()) {
                // Advance currentTime to enqueueTime of next available task
                currentTime = extendedTasks[taskIdx][0];
                continue;
            }

            // Process shortest job
            int[] curr = minHeap.poll();
            result[resultIdx++] = curr[2];
            currentTime += curr[1]; // Advance time by processingTime
        }

        return result;
    }

    // 3. Minimum Number of Refueling Stops (LeetCode 871) O(N log N) Time, O(N) Space
    public static int minRefuelStops(int target, int startFuel, int[][] stations) {
        // Max-Heap storing fuel capacity of passed stations
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

        long currentFuel = startFuel;
        int stops = 0;
        int i = 0;
        int n = stations.length;

        while (currentFuel < target) {
            // Add all stations reachable with currentFuel to Max-Heap
            while (i < n && stations[i][0] <= currentFuel) {
                maxHeap.offer(stations[i][1]);
                i++;
            }

            // If no station available to refuel and target not reached -> Impossible!
            if (maxHeap.isEmpty()) return -1;

            // Greedily pick station with largest fuel capacity
            currentFuel += maxHeap.poll();
            stops++;
        }

        return stops;
    }
}
```

> **Quick Syntax:**
```java
// Single-Threaded CPU Heap Comparator (Shortest Processing Time First)
PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> {
    if (a[1] != b[1]) return Integer.compare(a[1], b[1]); // Shortest proc time
    return Integer.compare(a[2], b[2]);                   // Tie-break by index
});
```

---

## 7. Concrete Problem Examples
* **LeetCode 621 - Task Scheduler**: CPU idle cycle calculation.
* **LeetCode 1834 - Single-Threaded CPU**: Shortest Job First scheduling.
* **LeetCode 871 - Minimum Number of Refueling Stops**: Greedy max-fuel collection.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Task Scheduler math and Single-Threaded CPU task execution:

```java
public class CPUTaskSchedulerDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Task Scheduler Math (LeetCode 621) ===");
        char[] tasks = {'A', 'A', 'A', 'B', 'B', 'B'};
        int leastCycles = CPUTaskSchedulerMaster.leastIntervalMath(tasks, 2);
        System.out.println("Least CPU Cycles (n=2): " + leastCycles); // Output: 8

        System.out.println("\n=== 2. Single-Threaded CPU (LeetCode 1834) ===");
        int[][] cpuTasks = {{1, 2}, {2, 4}, {3, 2}, {4, 1}};
        int[] executionOrder = CPUTaskSchedulerMaster.getOrder(cpuTasks);
        System.out.println("Execution Order: " + Arrays.toString(executionOrder)); // Output: [0, 2, 3, 1]
    }
}
```

---

## 9. Complexity Analysis

| Problem Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Task Scheduler Math (621)**| **$O(N)$ Linear ⚡** | **$O(1)$ Space ⚡**| `counts[26]` frequency calculation |
| **Single-Threaded CPU (1834)**| **$O(N \log N)$ ⚡** | $O(N)$ Space | Sort by enqueueTime + Min-Heap SJF |
| **Refueling Stops (871)** | **$O(N \log N)$ ⚡** | $O(N)$ Space | Max-Heap greedy fuel polling |

---

## 10. Edge Cases & Boundary Handling
* **Cooldown $n = 0$**: No idle cycles required; returns `tasks.length`.
* **CPU Idle Gap in Task Execution**: In LeetCode 1834, if `minHeap` is empty but un-enqueued tasks remain, `currentTime` MUST jump directly to `extendedTasks[taskIdx][0]` to avoid infinite zero-progress loops.

---

## 11. Common Mistakes & Anti-Patterns
* **Simulating CPU Cycles One-by-One when $N$ is Huge**:
  - Simulating single cycle increments (`time++`) when `n = 1,000,000` causes TLE (Time Limit Exceeded)!
  - Use the **Math Formula** `(maxFreq - 1) * (n + 1) + maxFreqCount` for $O(N)$ time.
* **Forgetting to Cast Current Time to `long`**: In Single-Threaded CPU, accumulated processing time `currentTime += procTime` can exceed 32-bit `Integer.MAX_VALUE`. **Use `long currentTime`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Shortest Job First (SJF) Rule in CPU Scheduling:
> When multiple tasks are available at current time, the optimal greedy choice is to execute the task with the **Shortest Processing Time**.
> Storing available tasks in a **Min-Heap ordered by processing time** guarantees $O(\log N)$ task selection!

> **Memory Trick:** **"SJF CPU Scheduler: Min-Heap sorting by processing time! Jump currentTime when heap is empty!"**

---

## 13. System & Implementation Comparisons

| Feature | Single-Threaded CPU (1834) | Refueling Stops (871) |
| :--- | :--- | :--- |
| **Heap Type** | **Min-Heap (Shortest Job First)** | **Max-Heap (Largest Fuel First)** |
| **Primary Order** | `processingTime` ascending | `fuelCapacity` descending |
| **Time Variable** | `currentTime += procTime` | `currentFuel += maxFuel` |

---

## 14. How to Recognize This in Questions
* **"Schedule tasks with cooldown n to minimize CPU execution time"** $\rightarrow$ LeetCode 621 (Task Scheduler Math).
* **"Process tasks on single CPU by shortest processing time"** $\rightarrow$ LeetCode 1834 (Min-Heap SJF).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the Task Scheduler math formula `(maxFreq - 1) * (n + 1) + maxFreqCount` work?**  
  *A:* The task(s) with maximum frequency `maxFreq` divide the execution timeline into `maxFreq - 1` blocks. Each block requires size `n + 1` to satisfy cooldown. The final trailing block needs `maxFreqCount` slots for all max-frequency tasks.
* **Q: Why does the Refueling Stops problem use a Max-Heap greedily?**  
  *A:* Because passing a gas station allows us to "save" its fuel capacity. When we run out of fuel before reaching the next station, picking the station with the largest fuel capacity from our saved Max-Heap minimizes the total number of refueling stops required.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CPU TASK SCHEDULING & GREEDY HEAP ALGORITHMS          |
+-----------------------------------------------------------------------+
| • Task Scheduler Math (621): (maxFreq - 1) * (n + 1) + maxFreqCount   |
| • Task Scheduler Result: max(tasks.length, MathFormulaResult)         |
| • Single-Threaded CPU (1834): Min-Heap[processingTime, originalIdx]   |
| • Empty Heap Jump: If minHeap empty, currentTime = nextTask.enqueueTime|
| • Refueling Stops (871): Max-Heap passed stations -> poll max fuel    |
| • Overflow Guard: Use long currentTime and long currentFuel           |
| • Complexity: Task Scheduler O(N) | CPU/Refuel O(N log N)             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Task Scheduler (LeetCode 621) using the math formula in 10 lines.
- [ ] I can write Single-Threaded CPU (LeetCode 1834) with Shortest Job First.
- [ ] I know why `currentTime` must jump when `minHeap` is empty.
- [ ] I can write Minimum Refueling Stops (LeetCode 871) using a Max-Heap.
- [ ] I know how to avoid integer overflow in time accumulator variables.
