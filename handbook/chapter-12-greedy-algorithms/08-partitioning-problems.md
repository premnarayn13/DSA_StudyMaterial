# 08. Partitioning Problems: Meeting Rooms, Sweep-Line Events & Minimum Platforms

## 1. Introduction
**Greedy Partitioning Problems** involve partitioning a collection of elements or overlapping intervals into the **Minimum Number of Disjoint Groups/Resources** (such as railway platforms, conference meeting rooms, or CPU execution clusters) so that no two elements in the same group conflict. Exemplified by the **Minimum Railway Platforms Problem** and **LeetCode 253 (Meeting Rooms II)**, partitioning problems sort events chronologically and track overlapping concurrency. By utilizing either a **Sweep-Line Event Sorting Strategy** or a **Min-Heap Resource Reservation System**, Greedy Partitioning algorithms find the absolute optimal minimum number of required resources in **$O(N \log N)$ Time Complexity** and **$O(N)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Greedy Partitioning:
> 1. **Sweep-Line Event Sorting Invariant**:
>    - Split every interval $[s_i, e_i]$ into 2 discrete events: an Arrival Event $(s_i, +1)$ and a Departure Event $(e_i, -1)$.
>    - Sort all $2N$ events chronologically. If arrival and departure occur at the same timestamp, process Departure FIRST (freeing up the resource before allocating to new arrival!).
> 2. **Peak Concurrency Theorem**:
>    - The minimum number of resources (platforms/rooms) required equals the **Maximum Peak Concurrency** of overlapping intervals at any instant in time!
> 3. **Min-Heap Resource Reuse Strategy**:
>    - Sort intervals by Start Time ($s_i$). Maintain a Min-Heap storing the End Times ($e_i$) of active rooms.
>    - If earliest ending room $e_{\min} \le s_i \implies$ Reuse existing room (`minHeap.poll()`)!
>    - If earliest ending room $e_{\min} > s_i \implies$ Allocate NEW room (`minHeap.add(e_i)`)! ⚡

```
Sweep-Line Concurrency Topology (Meeting Rooms / Railway Platforms):

Interval 1: [ 1 ======= 4 ]
Interval 2:      [ 2 ======= 6 ]
Interval 3:              [ 5 ======= 8 ]

Chronological Events:
Time 1: Arrival (+1)  ──► Active Rooms = 1
Time 2: Arrival (+1)  ──► Active Rooms = 2 (PEAK CONCURRENCY = 2!) ⚡
Time 4: Departure (-1)──► Active Rooms = 1
Time 5: Arrival (+1)  ──► Active Rooms = 2
Time 6: Departure (-1)──► Active Rooms = 1
Time 8: Departure (-1)──► Active Rooms = 0

Minimum Rooms / Platforms Required = 2! ⚡
```

---

## 2. Core Concepts & Partitioning Strategy Matrix

### 2.1 Partitioning Problem Strategy Matrix
```
Partitioning Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Approach / Strategy   | Primary Mechanism | Time Complexity   | Auxiliary Space   | Advantage         |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Sweep-Line Events** | Chronological Sort| **$O(N \log N)$ ⚡**| **$O(N)$ Events ⚡**| Simplest Coding   |
| **Two-Pointer Scan**  | Separate Arr/Dep  | **$O(N \log N)$ ⚡**| **$O(N)$ Arrays ⚡**| **$O(1)$ Space Opt**|
| **Min-Heap Strategy** | End Time Heap     | **$O(N \log N)$ ⚡**| $O(N)$ Min-Heap   | Room Assignments  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Minimum platforms/rooms = Peak Concurrency! Use Sweep-Line +1/-1 events or Min-Heap end times!"**

---

## 3. Characteristics & Peak Concurrency Mathematical Proof

### 3.1 Mathematical Proof of Peak Concurrency Optimality
* **Theorem**: The minimum number of rooms/platforms required to accommodate $N$ intervals equals the maximum number of mutually overlapping intervals at any timestamp $t^*$.
* **Proof**:
  1. Let $K$ be the maximum number of overlapping intervals at timestamp $t^*$.
  2. Since all $K$ intervals exist simultaneously at $t^*$, no two of these $K$ intervals can share a room.
  3. Therefore, ANY valid partitioning scheme MUST use at least $K$ distinct rooms ($\text{Rooms} \ge K$).
  4. The Greedy Min-Heap algorithm assigns intervals to rooms in order of start time $s_i$.
  5. When processing interval $i$, if an existing room $r$ has ended ($e_r \le s_i$), Greedy reuses room $r$.
  6. A new room $K+1$ is opened ONLY when all currently active rooms are occupied (i.e. at a timestamp of peak concurrency $K$).
  7. Thus, the Greedy algorithm opens at most $K$ rooms, proving that $\text{Minimum Rooms} = K$! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Execution Dry Run

Tracing Minimum Platforms for Arrivals $A = [9:00, 9:40, 9:50, 11:00]$ and Departures $D = [9:10, 12:00, 11:20, 11:30]$:

```
Step 1: Sort Arrivals and Departures Separately:
Sorted Arrivals  : [ 9:00,  9:40,  9:50, 11:00 ]
Sorted Departures: [ 9:10, 11:20, 11:30, 12:00 ]

Step 2: Two-Pointer Concurrent Traversal (i=0 for Arr, j=0 for Dep):

- i=0 (Arr 9:00) vs j=0 (Dep 9:10): 9:00 < 9:10
  Train arrives! Active Platforms = 1. Max Platforms = 1. i++ (i=1).

- i=1 (Arr 9:40) vs j=0 (Dep 9:10): 9:40 > 9:10
  Train departs! Active Platforms = 1 - 1 = 0. j++ (j=1).

- i=1 (Arr 9:40) vs j=1 (Dep 11:20): 9:40 < 11:20
  Train arrives! Active Platforms = 1. Max Platforms = 1. i++ (i=2).

- i=2 (Arr 9:50) vs j=1 (Dep 11:20): 9:50 < 11:20
  Train arrives! Active Platforms = 2. Max Platforms = 2! ⚡ i++ (i=3).

- i=3 (Arr 11:00) vs j=1 (Dep 11:20): 11:00 < 11:20
  Train arrives! Active Platforms = 3. Max Platforms = 3! ⚡ i++ (i=4).

- i=4 (End of Arrivals).

Final Minimum Platforms Required = 3! ✅
```

---

## 5. Visual Diagram: Min-Heap Room Allocation Flow

```
Interval Processing Order (Sorted by Start Time):

[ Interval 1: 1 -> 4 ] ──► Allocate Room 1. Heap = [ 4 ]
[ Interval 2: 2 -> 6 ] ──► Start 2 < MinEnd 4 -> Allocate Room 2. Heap = [ 4, 6 ]
[ Interval 3: 5 -> 8 ] ──► Start 5 >= MinEnd 4 -> Reuse Room 1! Poll 4, Add 8. Heap = [ 6, 8 ]

Heap Size = 2 Rooms Total! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Minimum Platforms (Two-Pointer $O(N \log N)$), LeetCode 253 (Meeting Rooms II via Min-Heap), and Partition Array into Disjoint Subsets.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Partitioning Problems,
 * Sweep-Line Concurrency, Min-Heap Room Allocation, and Platform Scheduling.
 */
public class PartitioningProblemsMaster {

    // =========================================================================
    // 1. MINIMUM RAILWAY PLATFORMS (Two-Pointer O(N log N) Time, O(N) Space)
    // =========================================================================
    /**
     * Calculates minimum railway platforms required for given arrival and departure times.
     *
     * @param arr array of arrival times
     * @param dep array of departure times
     * @return minimum number of platforms
     */
    public int findMinimumPlatforms(int[] arr, int[] dep) {
        if (arr == null || dep == null || arr.length == 0) return 0;

        int n = arr.length;

        // Step 1: Sort arrival and departure arrays independently
        Arrays.sort(arr);
        Arrays.sort(dep);

        int activePlatforms = 0;
        int maxPlatforms = 0;

        int i = 0; // Pointer for arrivals
        int j = 0; // Pointer for departures

        // Step 2: Two-pointer chronological traversal
        while (i < n && j < n) {
            if (arr[i] <= dep[j]) {
                // Train arrives before or at departure -> Allocate platform!
                activePlatforms++;
                maxPlatforms = Math.max(maxPlatforms, activePlatforms);
                i++;
            } else {
                // Train departs -> Free platform!
                activePlatforms--;
                j++;
            }
        }

        return maxPlatforms;
    }

    // =========================================================================
    // 2. LEETCODE 253: MEETING ROOMS II (Min-Heap Strategy O(N log N) Time)
    // =========================================================================
    /**
     * Finds minimum conference rooms required for meeting intervals.
     * intervals[i] = [start_i, end_i].
     */
    public int minMeetingRooms(int[][] intervals) {
        if (intervals == null || intervals.length == 0) return 0;

        // Step 1: Sort meeting intervals by START TIME ascending
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        // Step 2: Min-Heap storing END TIMES of occupied rooms
        PriorityQueue<Integer> roomMinHeap = new PriorityQueue<>();

        // Add first meeting's end time
        roomMinHeap.add(intervals[0][1]);

        for (int i = 1; i < intervals.length; i++) {
            // Check if earliest ending room is free
            if (intervals[i][0] >= roomMinHeap.peek()) {
                roomMinHeap.poll(); // Reuse existing room! ⚡
            }

            // Allocate room (add current meeting's end time)
            roomMinHeap.add(intervals[i][1]);
        }

        return roomMinHeap.size(); // Heap size equals total rooms allocated!
    }

    // =========================================================================
    // 3. SWEEP-LINE EVENT CLASS FOR ARBITRARY INTERVALS
    // =========================================================================
    public static class Event implements Comparable<Event> {
        public final int time;
        public final int type; // +1 for Arrival/Start, -1 for Departure/End

        public Event(int time, int type) {
            this.time = time;
            this.type = type;
        }

        @Override
        public int compareTo(Event o) {
            if (this.time != o.time) return Integer.compare(this.time, o.time);
            return Integer.compare(this.type, o.type); // Process -1 (Departure) before +1! ⚡
        }
    }

    public int minResourcesSweepLine(int[][] intervals) {
        if (intervals == null || intervals.length == 0) return 0;

        List<Event> events = new ArrayList<>();
        for (int[] interval : intervals) {
            events.add(new Event(interval[0], 1));  // Start Event (+1)
            events.add(new Event(interval[1], -1)); // End Event (-1)
        }

        Collections.sort(events);

        int active = 0;
        int maxActive = 0;

        for (Event event : events) {
            active += event.type;
            maxActive = Math.max(maxActive, active);
        }

        return maxActive;
    }
}
```

> **Quick Syntax:**
```java
// Sweep-Line Event Tie-Breaking Line
if (this.time != o.time) return Integer.compare(this.time, o.time); return Integer.compare(this.type, o.type); // -1 before +1
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 253 - Meeting Rooms II**:
   - Primary meeting room allocation problem ($O(N \log N)$ time).

2. **Minimum Platforms Problem (GeeksforGeeks)**:
   - Calculating railway station platform requirements.

3. **Cloud VM Thread Scheduling & Distributed Task Execution**:
   - Assigning concurrent computing tasks to minimum number of virtual machines.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class PartitioningProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GREEDY PARTITIONING & SWEEP-LINE DEMO        ");
        System.out.println("=================================================\n");

        PartitioningProblemsMaster master = new PartitioningProblemsMaster();

        // 1. Railway Minimum Platforms Test
        int[] arr = {900, 940, 950, 1100, 1500, 1800};
        int[] dep = {910, 1200, 1120, 1130, 1900, 2000};
        int minPlatforms = master.findMinimumPlatforms(arr, dep);

        System.out.println("1. Railway Platforms Test:");
        System.out.println("   Arrivals  : [9:00, 9:40, 9:50, 11:00, 15:00, 18:00]");
        System.out.println("   Departures: [9:10, 12:00, 11:20, 11:30, 19:00, 20:00]");
        System.out.println("   Minimum Platforms Required: " + minPlatforms + " Platforms");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 253 Meeting Rooms II Test
        int[][] intervals = {{0, 30}, {5, 10}, {15, 20}};
        int minRooms = master.minMeetingRooms(intervals);
        System.out.println("2. LeetCode 253 Meeting Rooms II Test:");
        System.out.println("   Intervals : [[0,30], [5,10], [15,20]]");
        System.out.println("   Minimum Rooms Required: " + minRooms + " Rooms");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Partitioning Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Two-Pointer Arr/Dep** | $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N)}$ Arrays ⚡| Independent array sorting |
| **Min-Heap Strategy**   | $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Min-Heap | End time heap poll/add |
| **Sweep-Line Events**   | $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Events List | Tie-breaker: `-1` before `+1` |

---

## 10. Edge Cases & Boundary Handling

1. **Arrival and Departure at Exact Same Time ($s_i = e_j$)**:
   - If train $A$ arrives at 11:00 and train $B$ departs at 11:00, train $B$ departs FIRST (freeing the platform before $A$ arrives).
   - Handled cleanly by `arr[i] <= dep[j]` or sorting departure `-1` before arrival `+1`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Processing Arrival `+1` Before Departure `-1` on Same Timestamp**:
  - Processing arrival before departure falsely inflates peak concurrency by 1. **ALWAYS process departure `-1` first when timestamps match!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Meeting Rooms I vs Meeting Rooms II:
> * **Meeting Rooms I (LeetCode 252)**: Can 1 person attend all meetings? (Check if ANY intervals overlap $\to$ True/False).
> * **Meeting Rooms II (LeetCode 253)**: Find MINIMUM rooms required for all meetings? (Find PEAK CONCURRENCY $\to$ Return Integer). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Two-Pointer Array Sort | Min-Heap Strategy | Sweep-Line Events |
| :--- | :--- | :--- | :--- |
| **Primary Data Structure** | Primitive Arrays | PriorityQueue | Custom Event List |
| **Room Assignment Info** | Count Only | End Time Tracking | Count Only |
| **Implementation Complexity**| **Simplest Code ⚡** | Moderate | Moderate |

---

## 14. How to Recognize This in Questions

* **"Find minimum number of meeting rooms required for overlapping intervals"** $\rightarrow$ Meeting Rooms II.
* **"Find minimum railway platforms required"** $\rightarrow$ Two-Pointer / Sweep-Line.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does the minimum number of platforms equal peak concurrency?**  
  *A:* Because peak concurrency represents the maximum number of trains physically present at the station simultaneously, each requiring a separate platform.

* **Q: Why does Min-Heap strategy sort intervals by start time?**  
  *A:* Sorting by start time ensures meetings are assigned to rooms chronologically, allowing `heap.peek()` to check if the earliest ending room is available for reuse.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PARTITIONING PROBLEMS                                 |
+-----------------------------------------------------------------------+
| • Core Theorem  : Min Resources Required = Peak Concurrency Count     |
| • Two-Pointer   : Sort Arr and Dep separately -> if(arr[i]<=dep[j]) i++|
| • Min-Heap      : Sort by Start Time -> if(start >= heap.peek()) poll()|
| • Sweep-Line    : Sort events -> Process Departure -1 BEFORE Arrival +1|
| • Performance   : O(N log N) Sorting Time | O(N) Auxiliary Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the Two-Pointer Minimum Platforms algorithm in Java.
- [ ] I can solve LeetCode 253 (`Meeting Rooms II`) using Min-Heap.
- [ ] I can write Sweep-Line event sorting with departure tie-breaking.
- [ ] I can prove why minimum rooms equals peak concurrency.
- [ ] I can state the difference between Meeting Rooms I and Meeting Rooms II.
