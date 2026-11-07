# 14. Pattern Recognition & Greedy Triggers: Identifying Algorithmic Archetypes

## 1. Introduction
High-speed problem-solving in technical coding interviews requires instant **Greedy Pattern Recognition**. Rather than spending valuable time attempting to derive new greedy heuristics under pressure, experienced engineers map problem descriptions directly to one of six universal **Greedy Master Archetypes**: **Interval Scheduling & Partitioning**, **Fractional Resource Allocation**, **Profit-Deadline Scheduling**, **Graph Minimum Spanning Trees**, **Shortest Path Relaxation**, and **Frequency-Based Merging & Encoding**. Identifying trigger words in problem statements allows instant selection of optimal sorting keys, priority queue configurations, and complexity bounds.

> **Important:** The 6 Universal Greedy Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Interval Scheduling & Partitioning**: Trigger = *"Maximize non-overlapping meetings, minimum rooms/platforms, burst balloons"*. Mechanics = Sort by Finish Time $f_i$ or Start Time + Min-Heap. Time = $O(N \log N)$.
> 2. **Pattern 2: Fractional Resource Allocation**: Trigger = *"Maximize value where items can be split continuously, truck box loading"*. Mechanics = Sort by Value Density $v_i / w_i$. Time = $O(N \log N)$.
> 3. **Pattern 3: Profit-Deadline Scheduling**: Trigger = *"Maximize profit executing unit-time jobs under deadlines"*. Mechanics = Sort by Profit $p_i$ + DSU Slot Allocation. Time = $O(N \log N)$.
> 4. **Pattern 4: Graph Minimum Spanning Tree (MST)**: Trigger = *"Connect all points/cities with minimum total edge weight"*. Mechanics = Kruskal (Edge Sort + DSU) or Prim (Min-Heap). Time = $O(E \log E)$.
> 5. **Pattern 5: Shortest Path Relaxation**: Trigger = *"Find min cost path in non-negative weighted graph, network delay time"*. Mechanics = Dijkstra Min-Heap Edge Relaxation. Time = $O((V + E) \log V)$.
> 6. **Pattern 6: Frequency-Based Merging & Encoding**: Trigger = *"Optimal prefix-free codes, minimum cost to merge $K$ piles of stones"*. Mechanics = Min-Heap iterative 2-node merging. Time = $O(N \log N)$. ⚡

```
Greedy Master Archetype Decision Tree Topography:
Problem Trigger Signal:
├── "Non-overlapping meetings / Min rooms or platforms?" ──► Pattern 1: Interval Scheduling
├── "Items divisible / Max truck units loading?" ─────────► Pattern 2: Fractional Knapsack
├── "Maximize profit with deadlines / DSU slot search?" ────► Pattern 3: Profit-Deadline Scheduling
├── "Connect all graph points with minimum total weight?" ──► Pattern 4: Minimum Spanning Tree (MST)
├── "Single source min cost path in non-negative graph?" ──► Pattern 5: Dijkstra's Relaxation
└── "Merge two smallest frequency nodes / Huffman codes?" ──► Pattern 6: Frequency Min-Heap Merging ⚡
```

---

## 2. Core Concepts & Master Pattern Strategy Matrix

### 2.1 Master Greedy Pattern Recognition Matrix
```
Master Greedy Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Primary Sorting Key| Key Structure    | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. Interval Schedule**| "Non-overlapping" | **Finish Time $f_i$ ASC⚡**| Sorted Array / Min-Heap| **$O(N \log N)$ ⚡**|
| **2. Fractional Alloc**| "Divisible items" | **Density $v_i/w_i$ DESC⚡**| Sorted Array      | **$O(N \log N)$ ⚡**|
| **3. Profit Deadline**| "Max job profit"  | **Profit $p_i$ DESC⚡**| DSU Path Compress | **$O(N \log N)$ ⚡**|
| **4. Minimum Spanning**| "Connect all points"| Edge Weight ASC   | DSU / Min-Heap    | **$O(E \log E)$ ⚡**|
| **5. Shortest Path**  | "Network delay"   | Distance Tentative| PriorityQueue     | **$O((V+E)\log V)$⚡**|
| **6. Frequency Merge**| "Huffman codes"   | Node Frequency ASC| Min-Heap          | **$O(N \log N)$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Intervals = Sort Finish Time; Fractional = Sort Density; Profit Jobs = Sort Profit + DSU; MST = Kruskal DSU; Shortest Path = Dijkstra!"**

---

## 3. Deep Dive into the 6 Greedy Archetypes

### 3.1 Archetype 1: Interval Scheduling & Partitioning
* **Triggers**: *"Non-overlapping intervals"*, *"Minimum meeting rooms"*, *"Minimum arrows to burst balloons"*.
* **Template**: Sort by Finish Time ($f_i$) for non-overlapping count ($O(N \log N)$), or Start Time + Min-Heap for room count ($O(N \log N)$).

### 3.2 Archetype 2: Fractional Resource Allocation
* **Triggers**: *"Fractional knapsack"*, *"Maximum units on a truck"*, *"Max bags with full capacity of rocks"*.
* **Template**: Sort items by density $v_i / w_i$ descending. Take 100% while capacity remains, take fraction for last item.

### 3.3 Archetype 3: Profit-Deadline Scheduling
* **Triggers**: *"Job sequencing with deadlines"*, *"Maximize profit scheduling unit-time jobs"*.
* **Template**: Sort jobs by Profit $p_i$ descending. Allocate job at latest free slot $t \le d_i$ using DSU (`find(d)`).

---

## 4. Internal Working Mechanics: Matching LeetCode Problems to Archetypes

```
LeetCode Problem Match Audits:

LeetCode 435 (Non-Overlapping Intervals)         ──► Pattern 1: Interval Scheduling (Finish Time Sort)
LeetCode 253 (Meeting Rooms II)                  ──► Pattern 1: Interval Partitioning (Min-Heap)
LeetCode 452 (Minimum Arrows to Burst Balloons)   ──► Pattern 1: Interval Scheduling (End Coordinate Sort)
LeetCode 1710 (Maximum Units on a Truck)         ──► Pattern 2: Fractional Resource Allocation (Density Sort)
LeetCode 2279 (Max Bags Full Capacity of Rocks)  ──► Pattern 2: Fractional Allocation (Needed Rocks Sort)
LeetCode 1584 (Min Cost to Connect All Points)   ──► Pattern 4: Minimum Spanning Tree (Kruskal/Prim)
LeetCode 743 (Network Delay Time)                ──► Pattern 5: Shortest Path Relaxation (Dijkstra)
LeetCode 621 (Task Scheduler CPU Intervals)       ──► Pattern 6: Frequency-Based Bucket Allocation
```

---

## 5. Visual Diagram: Greedy Pattern Selector Flowchart

```
                          [ New Greedy Problem ]
                                     │
                       Is it about INTERVALS / Meetings / Rooms?
                             /                  \
                         (Yes)                  (No)
                          /                        \
           [ Pattern 1: Interval Schedule ]      Is it about DIVISIBLE ITEMS / Density?
                                                     /                  \
                                                 (Yes)                  (No)
                                                  /                        \
                                   [ Pattern 2: Fractional Alloc ]     Is it about GRAPH CONNECTIVITY / Paths?
                                                                           /                  \
                                                                       (Yes)                  (No)
                                                                        /                        \
                                                       [ Pattern 4/5: MST / Dijkstra ]     [ Pattern 3/6: Job/Huffman ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across all 6 Greedy Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating the 6 Greedy Algorithmic Archetypes.
 */
public class GreedyPatternRecognitionMaster {

    // =========================================================================
    // PATTERN 1: INTERVAL SCHEDULING (LeetCode 435 Non-Overlapping Intervals)
    // =========================================================================
    public int pattern1_EraseOverlapIntervals(int[][] intervals) {
        if (intervals == null || intervals.length <= 1) return 0;
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1])); // Sort by Finish Time!

        int countKept = 1;
        int lastEnd = intervals[0][1];

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= lastEnd) {
                countKept++;
                lastEnd = intervals[i][1];
            }
        }
        return intervals.length - countKept;
    }

    // =========================================================================
    // PATTERN 2: FRACTIONAL ALLOCATION (LeetCode 1710 Max Units on Truck)
    // =========================================================================
    public int pattern2_MaximumUnits(int[][] boxTypes, int truckSize) {
        Arrays.sort(boxTypes, (a, b) -> Integer.compare(b[1], a[1])); // Sort Density DESC!

        int totalUnits = 0;
        int remCap = truckSize;

        for (int[] box : boxTypes) {
            if (remCap == 0) break;
            int take = Math.min(remCap, box[0]);
            totalUnits += take * box[1];
            remCap -= take;
        }
        return totalUnits;
    }

    // =========================================================================
    // PATTERN 3: PROFIT-DEADLINE SCHEDULING (Job Sequencing DSU)
    // =========================================================================
    public static class Job {
        int id, deadline, profit;
        public Job(int id, int deadline, int profit) {
            this.id = id; this.deadline = deadline; this.profit = profit;
        }
    }

    public int pattern3_JobSequencingDSU(List<Job> jobs) {
        jobs.sort((a, b) -> Integer.compare(b.profit, a.profit)); // Sort Profit DESC!
        int maxD = 0;
        for (Job j : jobs) maxD = Math.max(maxD, j.deadline);

        int[] parent = new int[maxD + 1];
        for (int i = 0; i <= maxD; i++) parent[i] = i;

        int totalProfit = 0;
        for (Job j : jobs) {
            int slot = find(parent, j.deadline);
            if (slot > 0) {
                totalProfit += j.profit;
                parent[slot] = find(parent, slot - 1);
            }
        }
        return totalProfit;
    }

    private int find(int[] parent, int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent, parent[i]);
    }
}
```

> **Quick Syntax:**
```java
// Greedy Pattern Selector Rule
// Trigger: "Non-overlapping intervals" -> Pattern 1: Sort by Finish Time
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Interval Scheduling)**: LeetCode 435, LeetCode 252, LeetCode 253, LeetCode 452.
* **Pattern 2 (Fractional Allocation)**: LeetCode 1710, LeetCode 2279, Fractional Knapsack.
* **Pattern 3 (Profit-Deadline)**: Job Sequencing with Deadlines, Minimum Delay Scheduling.
* **Pattern 4 (Graph MST)**: LeetCode 1584, Kruskal's MST, Prim's MST.
* **Pattern 5 (Shortest Path)**: LeetCode 743, LeetCode 787, Dijkstra's Algorithm.
* **Pattern 6 (Frequency Merging)**: LeetCode 621, Huffman Coding, Minimum Stone Merging.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class GreedyPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GREEDY PATTERN RECOGNITION DEMONSTRATION      ");
        System.out.println("=================================================\n");

        GreedyPatternRecognitionMaster master = new GreedyPatternRecognitionMaster();

        // 1. Pattern 1 Test (Interval Scheduling)
        int[][] intervals = {{1, 2}, {2, 3}, {3, 4}, {1, 3}};
        int minRemovals = master.pattern1_EraseOverlapIntervals(intervals);
        System.out.println("1. Pattern 1 (Interval Scheduling) Min Removals: " + minRemovals);
        System.out.println("-------------------------------------------------");

        // 2. Pattern 2 Test (Fractional Allocation)
        int[][] boxTypes = {{1, 3}, {2, 2}, {3, 1}};
        int maxUnits = master.pattern2_MaximumUnits(boxTypes, 4);
        System.out.println("2. Pattern 2 (Fractional Allocation) Max Truck Units: " + maxUnits);
        System.out.println("-------------------------------------------------");

        // 3. Pattern 3 Test (Job Sequencing DSU)
        List<GreedyPatternRecognitionMaster.Job> jobs = List.of(
            new GreedyPatternRecognitionMaster.Job(1, 2, 100),
            new GreedyPatternRecognitionMaster.Job(2, 1, 19),
            new GreedyPatternRecognitionMaster.Job(3, 2, 27)
        );
        int maxProfit = master.pattern3_JobSequencingDSU(new java.util.ArrayList<>(jobs));
        System.out.println("3. Pattern 3 (Profit-Deadline DSU) Max Profit: " + maxProfit);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Greedy Master Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Interval Schedule**| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Sorting Space | "Non-overlapping / Min rooms or platforms" |
| **2. Fractional Alloc**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(1)}$ Memory ⚡| "Divisible items / Max truck box loading" |
| **3. Profit Deadline**| $\mathbf{O(N \log N)}$ ⚡| $O(\max D)$ DSU Space | "Maximize job profit under deadlines" |
| **4. Minimum Spanning**| $\mathbf{O(E \log E)}$ ⚡| $O(V + E)$ Space | "Connect all graph points with min cost" |
| **5. Shortest Path**  | $\mathbf{O((V+E)\log V)}$⚡| $O(V + E)$ Heap Space | "Min cost path in non-negative graph" |
| **6. Frequency Merge**| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Min-Heap Space | "Optimal prefix codes / 2 smallest nodes" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Pattern 1 (Finish Time Sort) and Pattern 1 (Start Time Sort)**:
   - Maximize non-overlapping meetings count $\to$ Sort by **Finish Time $f_i$**.
   - Merge overlapping interval ranges $\to$ Sort by **Start Time $s_i$**.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Sorting Intervals by Start Time to Find Max Non-Overlapping Count**:
  - Sorting by start time fails when early intervals have huge durations. ALWAYS sort by **Finish Time $f_i$** to maximize count!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Greedy Selector Rule:
> 1. Non-overlapping meetings? $\to$ Pattern 1 (Sort Finish Time).
> 2. Divisible items / Density? $\to$ Pattern 2 (Sort Density $v_i / w_i$).
> 3. Job deadlines & profit? $\to$ Pattern 3 (Sort Profit + DSU).
> 4. Connect all points? $\to$ Pattern 4 (Kruskal DSU / Prim).
> 5. Non-negative min path? $\to$ Pattern 5 (Dijkstra Min-Heap). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Data Structure | Sorting Order | Space Cost |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Intervals)** | Sorted Array / Min-Heap | Finish Time $f_i$ ASC | $O(N)$ |
| **Pattern 2 (Fractional)** | Sorted Array | Density $v_i / w_i$ DESC | $O(1)$ |
| **Pattern 3 (Jobs DSU)** | DSU Array `parent[]` | Profit $p_i$ DESC | $O(\max D)$ |

---

## 14. How to Recognize This in Questions

* **"Select maximum number of non-overlapping intervals"** $\rightarrow$ Pattern 1 (Finish Time Sort).
* **"Connect all graph vertices with minimum total edge weight"** $\rightarrow$ Pattern 4 (Kruskal / Prim MST).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does interval scheduling sort by finish time instead of start time?**  
  *A:* Because finishing an activity as early as possible leaves the maximum remaining time window for scheduling all subsequent activities.

* **Q: Why is DSU used in Job Sequencing?**  
  *A:* To optimize finding the latest available free time slot $\le d_i$ in $O(\alpha(N))$ time, reducing total runtime from $O(N^2)$ to $O(N \log N)$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: GREEDY PATTERN RECOGNITION                            |
+-----------------------------------------------------------------------+
| • Pattern 1: Interval Scheduling  -> Sort Finish Time f_i ASC         |
| • Pattern 2: Fractional Allocation-> Sort Value Density v_i/w_i DESC  |
| • Pattern 3: Job Sequencing DSU   -> Sort Profit p_i DESC + DSU Find  |
| • Pattern 4: Minimum Spanning Tree-> Kruskal DSU / Prim Min-Heap      |
| • Pattern 5: Dijkstra's SSSP      -> Min-Heap Relaxation (w >= 0)     |
| • Pattern 6: Huffman Coding       -> Min-Heap Merge 2 smallest nodes  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any greedy problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I know when to sort by finish time vs start time.
- [ ] I can implement Interval Scheduling (LeetCode 435) in Java.
- [ ] I can implement Fractional Allocation (LeetCode 1710) in Java.
- [ ] I can implement Job Sequencing with DSU in Java.
