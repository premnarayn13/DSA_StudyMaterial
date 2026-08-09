# 10. System Applications: OS Schedulers, Timer Wheels, Heavy Hitters & Graph Engines

## 1. Introduction
Heaps and Priority Queues are core system primitives powering real-time operating system task schedulers, network event loops, distributed streaming analytics engines, and graph optimization algorithms. Systems like **Linux RT Task Schedulers**, **Netty / Node.js Hashed Timer Wheels**, **Apache Flink Stream Heavy Hitters**, and **Graph Routing Engines (Dijkstra / Prim)** rely on Min/Max Heaps to execute priority task dispatches and top-K analytics in **$O(1)$ peek time and $O(\log N)$ update time**.

> **Important:** Core Industrial Systems Powered by Heaps:
> 1. **OS Real-Time Priority Schedulers**: Min-Heaps order runnable processes by deadline or priority score (`vruntime`).
> 2. **Network Event Loops & Timer Queues**: Min-Heaps track scheduled timer callbacks e.g. `setTimeout(fn, delay)`; head contains the **EARLIEST EXPIRING TIMER**!
> 3. **Streaming Heavy Hitters (Count-Min Sketch + Min-Heap)**: Maintains real-time Top-K most frequent search queries or network IP addresses.
> 4. **Graph Shortest Path & MST Engines**: Dijkstra's Algorithm and Prim's Algorithm use Min-Heaps to select the next minimum-distance vertex in $O((E + V) \log V)$ time! ⚡

```
Event-Driven Network Loop Timer Queue Topology:
Timer Queue (Min-Heap by Expiration Time T):
                     [ Head: T = 10ms (Next Expiring Callback!) ]
                    /                                          \
    [ Callback T = 25ms ]                               [ Callback T = 50ms ]

Event Loop Action: Sleep until T = 10ms -> Poll Head -> Execute Callback!
Sleep duration computed in O(1) time from Min-Heap head! ⚡
```

---

## 2. Core Concepts & Timer Queue Architecture

### 2.1 Event Loop Scheduled Timer Queue
In network frameworks (such as Netty, Tokio, or Node.js):
* Timers are registered with expiration timestamps `expirationTime = currentTime + delay`.
* Storing timers in a **Min-Heap** allows the event loop to query `minHeap.peek().expirationTime` in **$O(1)$ time**.
* The CPU can sleep for exact duration `sleepDuration = minHeap.peek().expirationTime - currentTime`, waking up precisely when the earliest timer expires!

```
System Applications Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| System Component      | Priority Key      | Heap Architecture | Operational Goal  |
+-----------------------+-------------------+-------------------+-------------------+
| **OS RT Scheduler**   | Task Deadline / Priority| Min-Heap        | Dispatch highest priority|
| **Event Timer Queue** | Expiration Timestamp| Min-Heap         | $O(1)$ earliest timer query|
| **Stream Heavy Hitters**| Frequency Counter| Capped Min-Heap   | Track Top-K items |
| **Dijkstra Engine**   | Path Distance     | Min-Heap          | $O((E+V)\log V)$ shortest path|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Event loop timer queues use Min-Heaps so the CPU can query the earliest expiring timer in O(1) time!"**

---

## 3. Characteristics & Streaming Heavy Hitters (Top-K Frequency)

### 3.1 Streaming Top-K Heavy Hitters Engine
In high-throughput analytics (e.g. tracking top 10 trending hashtags on Twitter):
* Data stream contains millions of items per second ($N \to \infty$).
* Storing all items in memory is impossible.
* **Architecture**: Combine a **Frequency Map** (or Count-Min Sketch) with a **Capped Min-Heap of size $K$** to maintain the Top-K heavy hitters in $O(1)$ average update time per stream item!

---

## 4. Internal Working Mechanics
Tracing Network Event Loop Execution with Min-Heap Timer Queue:

```
Current Time = 0ms. Timers Registered: T1(delay=15ms), T2(delay=5ms), T3(delay=20ms).

Min-Heap Queue: [ T2(5ms), T1(15ms), T3(20ms) ]

1. Event Loop Queries Head: T2.expirationTime = 5ms.
   - Sleep for 5ms!

2. Clock reaches 5ms: Event Loop Wakes Up!
   - Poll T2 -> Execute T2 Callback!
   - New Head = T1(15ms).
   - Sleep for 15ms - 5ms = 10ms!

Zero CPU polling spin cycles! Optimal power and latency! ✅
```

---

## 5. Visual Diagram
Dijkstra's Shortest Path Min-Heap Priority Queue Topography:

```
Graph Vertices Distance Heap:
                [ (Dist: 0, Node: A) ]  <--- Minimum Unvisited Distance Node
               /                      \
    [ (Dist: 4, Node: B) ]          [ (Dist: 2, Node: C) ]

Poll (Dist: 2, Node C) -> Relax Edges from Node C -> Update Min-Heap in O(log V) time! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing an Event Loop Timer Manager and a Dijkstra Shortest Path Engine powered by Min-Heap Priority Queues:

```java
import java.util.*;

public class SystemApplicationsMaster {

    // 1. Event Loop Timer Queue System O(1) Peek, O(log N) Register
    public static class TimerManager {
        public static class TimerTask implements Comparable<TimerTask> {
            long expirationTime; // Epoch millis
            Runnable callback;

            public TimerTask(long delayMillis, Runnable callback) {
                this.expirationTime = System.currentTimeMillis() + delayMillis;
                this.callback = callback;
            }

            @Override
            public int compareTo(TimerTask other) {
                return Long.compare(this.expirationTime, other.expirationTime);
            }
        }

        private final PriorityQueue<TimerTask> timerHeap;

        public TimerManager() {
            this.timerHeap = new PriorityQueue<>();
        }

        public void schedule(long delayMillis, Runnable callback) {
            timerHeap.offer(new TimerTask(delayMillis, callback));
        }

        // Get milliseconds until next timer expires O(1) Time
        public long getNextTimeoutMillis() {
            if (timerHeap.isEmpty()) return -1;
            long now = System.currentTimeMillis();
            return Math.max(0, timerHeap.peek().expirationTime - now);
        }

        // Process all expired timers
        public void processExpiredTimers() {
            long now = System.currentTimeMillis();
            while (!timerHeap.isEmpty() && timerHeap.peek().expirationTime <= now) {
                TimerTask task = timerHeap.poll();
                task.callback.run();
            }
        }
    }

    // 2. Dijkstra's Shortest Path Engine O((E + V) log V) Time
    public static class Edge {
        int target;
        int weight;
        public Edge(int target, int weight) { this.target = target; this.weight = weight; }
    }

    public static int[] dijkstraShortestPath(int numVertices, List<List<Edge>> graph, int source) {
        int[] dist = new int[numVertices];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[source] = 0;

        // Min-Heap ordered by shortest tentative distance: [vertex, distance]
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(
            (a, b) -> Integer.compare(a[1], b[1])
        );

        minHeap.offer(new int[]{source, 0});

        while (!minHeap.isEmpty()) {
            int[] curr = minHeap.poll();
            int u = curr[0];
            int d = curr[1];

            if (d > dist[u]) continue; // Stale distance entry -> Skip!

            for (Edge edge : graph.get(u)) {
                int v = edge.target;
                int weight = edge.weight;

                if (dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    minHeap.offer(new int[]{v, dist[v]}); // Relax edge
                }
            }
        }

        return dist;
    }
}
```

> **Quick Syntax:**
```java
// Event Loop Timeout Query Line
long sleepDuration = Math.max(0, timerHeap.peek().expirationTime - System.currentTimeMillis());
```

---

## 7. Concrete Problem Examples
* **Netty / Node.js Event Loop**: Scheduled timer queues using Min-Heap / Hashed Timing Wheels.
* **Dijkstra's Algorithm**: Min-Heap edge relaxation.
* **Linux Kernel Task Scheduler**: Red-Black / Heap priority task dispatching.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `TimerManager` and `dijkstraShortestPath`:

```java
public class SystemApplicationsDemo {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 1. Event Loop Timer Queue Test ===");
        SystemApplicationsMaster.TimerManager timerMgr = 
            new SystemApplicationsMaster.TimerManager();

        timerMgr.schedule(50, () -> System.out.println("Timer 1 Expired (50ms)"));
        timerMgr.schedule(10, () -> System.out.println("Timer 2 Expired (10ms)"));

        System.out.println("Next Timeout Millis: " + timerMgr.getNextTimeoutMillis()); // ~10ms

        Thread.sleep(20);
        timerMgr.processExpiredTimers(); // Output: "Timer 2 Expired (10ms)" ✅

        System.out.println("\n=== 2. Dijkstra Shortest Path Engine Test ===");
        int V = 3;
        List<List<SystemApplicationsMaster.Edge>> graph = new ArrayList<>();
        for (int i = 0; i < V; i++) graph.add(new ArrayList<>());

        graph.get(0).add(new SystemApplicationsMaster.Edge(1, 4));
        graph.get(0).add(new SystemApplicationsMaster.Edge(2, 1));
        graph.get(2).add(new SystemApplicationsMaster.Edge(1, 2));

        int[] dist = SystemApplicationsMaster.dijkstraShortestPath(V, graph, 0);
        System.out.println("Shortest Distance 0 -> 1: " + dist[1]); // Output: 3 (Path: 0 -> 2 -> 1) ✅
    }
}
```

---

## 9. Complexity Analysis

| System Engine | Operation / Action | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Timer Manager Queue**| Query Earliest Expiration| **$O(1)$ Constant ⚡** | $O(N)$ Space | Head `peek()` inspection |
| **Timer Manager Queue**| Register New Timer | **$O(\log N)$ ⚡** | $O(N)$ Space | Heap sift-up insertion |
| **Dijkstra Engine** | Shortest Path Execution | **$O((E + V) \log V)$ ⚡**| $O(V)$ Distance Array | Priority vertex relaxation |

---

## 10. Edge Cases & Boundary Handling
* **Stale Distance Entries in Dijkstra**: Solved cleanly by skipping processed entries `if (d > dist[u]) continue`.
* **Clock Skew / Epoch Millis Rollover**: System relative nanosecond timers (`System.nanoTime()`) avoid NTP clock adjustment bugs.

---

## 11. Common Mistakes & Anti-Patterns
* **Calling `PriorityQueue.remove(staleTask)` in Dijkstra ($O(V^2)$ Time Penalty)**:
  - Attempting to update a vertex's distance by calling `pq.remove()` scans the array linearly in $O(V)$ time.
  - **Use Lazy Deletion: Offer new `(v, newDist)` tuple into heap and skip stale entries (`if (d > dist[u]) continue`) for $O((E+V)\log V)$ time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Lazy Deletion is Critical in Dijkstra's Algorithm:
> Updating a vertex distance `dist[v]` occurs frequently during edge relaxation.
> Instead of calling expensive $O(V)$ heap updates (`pq.remove()`), Dijkstra simply offers a NEW tuple `(v, newDist)` into the Min-Heap.
> When old stale tuples `(v, oldDist)` are polled later, checking `if (d > dist[u]) continue` ignores them in **$O(1)$ time**, preserving $O((E + V) \log V)$ global complexity!

> **Memory Trick:** **"In Dijkstra's algorithm, use lazy deletion with `if (d > dist[u]) continue` to avoid O(V) heap removals!"**

---

## 13. System & Implementation Comparisons

| Feature | Min-Heap Timer Queue | Hashed Timing Wheel |
| :--- | :--- | :--- |
| **Timer Registration** | $O(\log N)$ Logarithmic | **$O(1)$ Strict Constant ⚡** |
| **Earliest Expiration Query**| **$O(1)$ Constant ⚡** | $O(1)$ Ring Buffer Step |
| **Memory Footprint** | Low (Stores active timers) | Fixed Ring Buffer Buckets |

---

## 14. How to Recognize This in Questions
* **"Design an event-driven timer callback queue"** $\rightarrow$ Min-Heap Priority Queue by expiration timestamp.
* **"Find shortest path in weighted graph with non-negative edges"** $\rightarrow$ Dijkstra's Algorithm with Min-Heap.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Dijkstra's algorithm require non-negative edge weights?**  
  *A:* Because a Min-Heap greedily finalizes the shortest distance to a vertex when it is polled. Negative edge weights break this greedy choice invariant, requiring Bellman-Ford or SPFA instead.
* **Q: How does a Hashed Timing Wheel optimize timer queues over a Binary Heap?**  
  *A:* A Hashed Timing Wheel uses a circular array of buckets (ticks) where timers are added to bucket lists in $O(1)$ time, eliminating the $O(\log N)$ heap sift overhead.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SYSTEM APPLICATIONS OF HEAPS                          |
+-----------------------------------------------------------------------+
| • Event Loop Timers: Min-Heap by expiration time -> O(1) timeout query|
| • Dijkstra Engine  : Min-Heap by path distance -> O((E + V) log V)    |
| • Lazy Deletion    : If (d > dist[u]) continue; avoids O(V) removals |
| • Heavy Hitters    : Frequency Map + Capped Min-Heap size K           |
| • OS Schedulers    : Min-Heap tracks lowest deadline process          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write an Event Loop Timer Manager using a Min-Heap.
- [ ] I can write Dijkstra's Shortest Path algorithm with Min-Heap.
- [ ] I know why lazy deletion `if (d > dist[u]) continue` is mandatory in Dijkstra.
- [ ] I know how CPU sleep durations are calculated from heap heads.
- [ ] I can state the differences between Heap Timer Queues and Hashed Timing Wheels.
