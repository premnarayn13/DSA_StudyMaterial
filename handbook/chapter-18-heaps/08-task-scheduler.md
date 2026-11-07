# 08. Task Scheduler, CPU Cooldown Queues & Priority Frequency Mechanics

## 1. Introduction
The **Task Scheduler Problem (LeetCode 621)** simulates a CPU executing tasks subject to a strict **Cooldown Period ($N$)**: identical tasks must be separated by at least $N$ time intervals (idle slots). By combining a **Max-Heap (Priority Queue)** ordered by task frequency with a **Cooldown Queue** (or evaluating the **Greedy Frequency Formula**), task scheduling algorithms compute minimum execution CPU time in **$O(\text{Total Tasks})$ Linear Time and $O(1)$ Auxiliary Space** (for 26 uppercase English tasks).

> **Important:** The Dual Strategy for Task Scheduler (LeetCode 621):
> 1. **Max-Heap + Cooldown Queue Strategy**: Always execute the task with the **HIGHEST REMAINING FREQUENCY**! After execution, place the task into a Cooldown Queue until `currentCycle >= coolDownTime`.
> 2. **Mathematical Greedy Formula**:
>    $$\text{Total Slots} = \max\left(\text{tasks.length}, \ (\text{maxFreq} - 1) \cdot (N + 1) + \text{maxCount}\right)$$
>    - $\text{maxFreq}$: Highest frequency of any single task.
>    - $\text{maxCount}$: Number of distinct tasks that share the maximum frequency $\text{maxFreq}$. ⚡

```
Task Scheduler CPU Execution Frame Topology (Tasks: A,A,A,B,B,B, Cooldown N = 2):
Frame 1 : [ A ] (A rem=2) -> Cooldown Queue until t = 1+2 = 3
Frame 2 : [ B ] (B rem=2) -> Cooldown Queue until t = 2+2 = 4
Frame 3 : [ IDLE ] (No task available in Heap!)
Frame 4 : [ A ] (Available again at t=3)
Frame 5 : [ B ] (Available again at t=4)
Frame 6 : [ IDLE ]
Frame 7 : [ A ]
Frame 8 : [ B ]
Total CPU Time = 8 Cycles! ⚡
```

---

## 2. Core Concepts & Max-Heap + Cooldown Queue Architecture

### 2.1 The Cooldown Queue Tuple Structure
When executing tasks with a Max-Heap and Cooldown Queue:
* **Max-Heap**: Holds tasks currently available for CPU execution (Ordered by remaining frequency descending).
* **Cooldown Queue**: Stores `Tuple(remainingFreq, readyTime)` for tasks currently cooling down.

```
Task Scheduling Loop Protocol:
1. `currentCycle = 0`.
2. While `!maxHeap.isEmpty()` OR `!cooldownQueue.isEmpty()`:
   - `currentCycle++`.
   - Re-offer tasks from `cooldownQueue` back to `maxHeap` if `cooldownQueue.peek().readyTime <= currentCycle`.
   - If `!maxHeap.isEmpty()`:
     - `curr = maxHeap.poll()`.
     - Decrement `curr.freq--`.
     - If `curr.freq > 0`, offer `(curr.freq, currentCycle + N)` into `cooldownQueue`.
   - Else: CPU executes IDLE slot!
```

> **Memory Trick:** **"Always execute the task with highest remaining frequency! If no task is ready, CPU sits IDLE!"**

---

## 3. Characteristics & Greedy Formula Derivation

### 3.1 Derivation of $(\text{maxFreq} - 1) \cdot (N + 1) + \text{maxCount}$
Let task `A` have the highest frequency $\text{maxFreq} = 3$, with cooldown $N = 2$:
* Arrange `A` into $(\text{maxFreq} - 1) = 2$ execution blocks of size $N + 1 = 3$:
  `A _ _ | A _ _ | A`
* Each block of size $N + 1$ guarantees $N$ cooldown slots after `A`.
* The final block contains ONLY the final instances of all tasks that share frequency $\text{maxFreq}$ ($\text{maxCount}$).
* If total tasks $> (\text{maxFreq} - 1) \cdot (N + 1) + \text{maxCount}$, remaining tasks fill idle slots without increasing total time!

---

## 4. Internal Working Mechanics
Tracing Task Scheduler (LeetCode 621) on `tasks = ['A','A','A','B','B','B']`, `N = 2`:

```
Task Frequencies: A = 3, B = 3.
maxFreq = 3, maxCount = 2 (Both A and B have freq 3).

Apply Mathematical Formula:
Formula Result = (maxFreq - 1) * (N + 1) + maxCount
               = (3 - 1) * (2 + 1) + 2
               = 2 * 3 + 2 = 8.

Compare with tasks.length (6):
Math.max(6, 8) = 8 CPU Cycles! ✅ (Calculated in O(N) Time!)
```

---

## 5. Visual Diagram
Greedy Execution Block Frame Topography:

```
Block 1 (Size N+1=3)    Block 2 (Size N+1=3)    Final Block (Size maxCount=2)
  [ A | B | IDLE ]        [ A | B | IDLE ]             [ A | B ]
  |<--- N = 2 --->|       |<--- N = 2 --->|
Total CPU Cycles = 3 + 3 + 2 = 8 Cycles! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Task Scheduler using Max-Heap + Cooldown Queue (Simulation) and Mathematical Greedy Formula (LeetCode 621):

```java
import java.util.*;

public class TaskSchedulerMaster {

    // 1. Task Scheduler Mathematical Greedy Formula (LeetCode 621) O(Tasks) Time, O(1) Space
    public static int leastIntervalGreedy(char[] tasks, int n) {
        if (tasks == null || tasks.length == 0) return 0;

        int[] freq = new int[26];
        int maxFreq = 0;

        for (char t : tasks) {
            freq[t - 'A']++;
            maxFreq = Math.max(maxFreq, freq[t - 'A']);
        }

        int maxCount = 0;
        for (int f : freq) {
            if (f == maxFreq) {
                maxCount++;
            }
        }

        // Greedy formula calculation
        int partCount = maxFreq - 1;
        int partLength = n + 1;
        int emptySlots = partCount * partLength + maxCount;

        return Math.max(tasks.length, emptySlots);
    }

    // 2. Task Scheduler Max-Heap + Cooldown Queue Simulation O(Tasks log 26) Time
    public static int leastIntervalSimulation(char[] tasks, int n) {
        if (tasks == null || tasks.length == 0) return 0;

        int[] freq = new int[26];
        for (char t : tasks) {
            freq[t - 'A']++;
        }

        // Max-Heap ordered by remaining frequency
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int f : freq) {
            if (f > 0) maxHeap.offer(f);
        }

        // Cooldown Queue storing int[]{remainingFreq, readyTime}
        Queue<int[]> cooldownQueue = new ArrayDeque<>();
        int currentCycle = 0;

        while (!maxHeap.isEmpty() || !cooldownQueue.isEmpty()) {
            currentCycle++;

            // Step 1: Re-offer ready tasks from cooldown queue
            if (!cooldownQueue.isEmpty() && cooldownQueue.peek()[1] <= currentCycle) {
                maxHeap.offer(cooldownQueue.poll()[0]);
            }

            // Step 2: Execute task with highest remaining frequency
            if (!maxHeap.isEmpty()) {
                int remaining = maxHeap.poll() - 1;
                if (remaining > 0) {
                    cooldownQueue.offer(new int[]{remaining, currentCycle + n});
                }
            }
            // Else CPU sits IDLE for this cycle
        }

        return currentCycle;
    }
}
```

> **Quick Syntax:**
```java
// Task Scheduler Greedy Formula Line
int emptySlots = (maxFreq - 1) * (n + 1) + maxCount;
return Math.max(tasks.length, emptySlots);
```

---

## 7. Concrete Problem Examples
* **LeetCode 621 - Task Scheduler**: CPU cooldown scheduling.
* **LeetCode 358 - Rearrange String k Distance Apart**: Character $K$-distance cooldown.
* **LeetCode 767 - Reorganize String**: Adjacent character separation ($N = 1$).

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Greedy Formula and Simulation strategies:

```java
public class TaskSchedulerDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Task Scheduler (LeetCode 621) ===");
        char[] tasks = {'A','A','A','B','B','B'};
        int n = 2;

        int cyclesGreedy = TaskSchedulerMaster.leastIntervalGreedy(tasks, n);
        System.out.println("Least CPU Cycles (Greedy):     " + cyclesGreedy); // Output: 8

        int cyclesSim = TaskSchedulerMaster.leastIntervalSimulation(tasks, n);
        System.out.println("Least CPU Cycles (Simulation): " + cyclesSim);   // Output: 8 ✅
    }
}
```

---

## 9. Complexity Analysis

| Implementation Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Greedy Formula (621)**| **$O(\text{Tasks})$ Linear ⚡**| **$O(1)$ Constant Space ⚡**| Fixed 26-element array |
| **Max-Heap Simulation**  | **$O(\text{Total Cycles})$ ⚡**| $O(26) = O(1)$ Space | Cooldown Queue tracking |

---

## 10. Edge Cases & Boundary Handling
* **Cooldown $N = 0$**: Returns `tasks.length` immediately (no idle slots required).
* **High Variety of Unique Tasks**: If total tasks $> (\text{maxFreq} - 1) \cdot (N + 1) + \text{maxCount}$, returns `tasks.length`.

---

## 11. Common Mistakes & Anti-Patterns
* **Executing Low-Frequency Tasks First**:
  - Scheduling low-frequency tasks first leaves high-frequency tasks for the end, forcing maximum CPU idle slots!
  - **Always schedule the task with HIGHEST remaining frequency first**.
* **Forgetting `Math.max(tasks.length, emptySlots)`**:
  - When unique tasks are plentiful, no idle slots are created, but `emptySlots` formula might calculate a smaller number than `tasks.length`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why the Greedy Task Scheduler Formula Works:
> The task with frequency `maxFreq` forms the structural skeleton of the schedule.
> Spacing each instance of `maxFreq` by $N$ slots creates $(\text{maxFreq} - 1)$ blocks of size $N + 1$.
> Any other task fills empty slots inside these blocks. If empty slots are exhausted, extra tasks simply expand the blocks without violating cooldown rules!

> **Memory Trick:** **"Result = Math.max(tasks.length, (maxFreq - 1) * (N + 1) + maxCount)!"**

---

## 13. System & Implementation Comparisons

| Feature | Greedy Formula Strategy | Max-Heap Simulation Strategy |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\text{Tasks})$ Linear ⚡** | $O(\text{CPU Cycles})$ |
| **Schedule Recovery**| Calculates total cycles count | **Generates actual execution order ⚡**|
| **Memory Usage** | **$O(1)$ Constant ⚡** | $O(26)$ Queue Memory |

---

## 14. How to Recognize This in Questions
* **"Find minimum CPU time to complete tasks separated by cooldown period N"** $\rightarrow$ Task Scheduler (LeetCode 621).
* **"Rearrange characters such that same characters are at least K distance apart"** $\rightarrow$ LeetCode 358 (Max-Heap + Cooldown Queue).

---

## 15. Frequently Asked Interview Questions
* **Q: When does the Greedy Task Scheduler formula return `tasks.length`?**  
  *A:* When there are enough distinct tasks to fill all idle slots created between instances of the most frequent task.
* **Q: How does Max-Heap simulation generate the actual task execution sequence?**  
  *A:* By appending the polled character (e.g. `'A'`) or `"IDLE"` string to a `StringBuilder` at each cycle step.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TASK SCHEDULER & CPU COOLDOWN                         |
+-----------------------------------------------------------------------+
| • Greedy Formula: Math.max(tasks.length, (maxFreq - 1) * (N + 1) + maxCount)|
| • maxFreq       : Frequency of most frequent task                     |
| • maxCount      : Number of distinct tasks sharing maxFreq            |
| • Simulation    : Max-Heap (Highest Freq First) + Cooldown Queue      |
| • Space Complexity: O(1) Constant (Fixed 26-alphabet frequency array) |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Task Scheduler (LeetCode 621) using the Greedy Formula.
- [ ] I can write Task Scheduler using Max-Heap + Cooldown Queue simulation.
- [ ] I know why `maxFreq` forms the structural skeleton of the schedule.
- [ ] I know why `Math.max(tasks.length, ...)` handles high task variety.
- [ ] I can extend this pattern to Rearrange String K Distance Apart (LeetCode 358).
