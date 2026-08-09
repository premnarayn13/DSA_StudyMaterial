# 05. Graph Cycle Detection, 3-Color DFS States & Directed Back-Edge Invariants

## 1. Introduction
**Cycle Detection** in graphs determines whether a graph contains at least one closed loop path. Because cycle detection rules fundamentally differ between **Undirected Graphs** (where a cycle is detected if a neighbor $v \ne \text{parent}$ is already visited) and **Directed Graphs** (where a cycle is detected IF AND ONLY IF an edge points to an active node in the CURRENT RECURSION STACK), algorithms use **Parent-Tracking DFS/BFS** for undirected graphs and **3-Color DFS States (White, Gray, Black)** or **Kahn's Topological Algorithm** for directed graphs in **$O(V + E)$ Linear Time**.

> **Important:** Core Invariants of Undirected vs Directed Cycle Detection:
> 1. **Undirected Graph Cycle Invariant**: In undirected DFS/BFS, if neighbor $v$ is `visited[v] == true` AND $v \ne \text{parent}$, a cycle exists!
> 2. **Directed Graph 3-Color State Invariant**:
>    - **White (0 / Unvisited)**: Node has not been visited yet.
>    - **Gray (1 / Visiting / On Stack)**: Node is currently active in the call stack frame!
>    - **Black (2 / Visited)**: Node and all its subtrees have been fully explored.
>    - **Back-Edge Rule**: If edge $(u \to v)$ encounters a **GRAY node (`state[v] == 1`)**, a **DIRECTED CYCLE IS DETECTED**! ⚡

```
Directed Graph 3-Color DFS Cycle Detection Topology (Course Schedule LeetCode 207):
Nodes: (0) ---> (1) ---> (2) ---> (0)  <--- Back-Edge (2 -> 0) points to GRAY Node 0!

DFS Call Stack:
1. dfs(0): Set state[0] = GRAY (1)
2. dfs(1): Set state[1] = GRAY (1)
3. dfs(2): Set state[2] = GRAY (1)
4. Edge (2 -> 0): Check state[0] == 1 (GRAY!) ---> DIRECTED CYCLE DETECTED! ⚡
```

---

## 2. Core Concepts & Undirected vs Directed Cycle Detection Algorithms

### 2.1 Cycle Detection Strategy Matrix
```
Cycle Detection Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Graph Type            | Algorithm Mechanism| Cycle Condition   | Primary Problem   |
+-----------------------+-------------------+-------------------+-------------------+
| **Undirected Graph**  | Parent-Track DFS  | `visited[v] && v != parent`| Redundant Edge |
| **Directed Graph**    | 3-Color DFS States| `state[v] == 1 (GRAY)` | Course Schedule (207)|
| **Directed Graph**    | Kahn's In-Degree  | `processed < V`   | Course Schedule II|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Undirected Cycle: visited[v] && v != parent! Directed Cycle: state[v] == 1 (GRAY node on stack)!"**

---

## 3. Characteristics & 3-Color State Transition Invariants

### 3.1 3-Color State Transition Diagram
* Initial State: All nodes initialized to **0 (WHITE)**.
* Enter `dfs(u)`: Mark `state[u] = 1` (**GRAY - Currently Visiting**).
* Recurse Neighbors:
  - If `state[v] == 1` (**GRAY**): **CYCLE DETECTED! Return `true`**.
  - If `state[v] == 0` (**WHITE**): Recurse `dfs(v)`. If `dfs(v)` returns `true`, return `true`.
* Exit `dfs(u)`: Mark `state[u] = 2` (**BLACK - Fully Explored**).

---

## 4. Internal Working Mechanics
Tracing Directed Cycle Detection (LeetCode 207 Course Schedule) on Edges `[[1,0], [0,1]]` (0 -> 1, 1 -> 0):

```
Init: state = [0, 0] (WHITE).

Outer Loop i = 0: Call dfs(0):
1. Set state[0] = 1 (GRAY).
2. Neighbor 1: state[1] == 0 (WHITE) -> Recurse dfs(1).
3. Set state[1] = 1 (GRAY).
4. Neighbor 0: state[0] == 1 (GRAY!) ---> DIRECTED CYCLE DETECTED!
5. Return true up the call stack!

Course Schedule Impossible! Returns false! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
3-Color DFS State Machine Topography:

```
[ 0: WHITE (Unvisited) ]
           |
           v (Enter DFS: Push onto Call Stack)
[ 1: GRAY (Visiting / On Stack) ]  ==== (Encounters GRAY Node!) ====> CYCLE DETECTED! ⚡
           |
           v (Exit DFS: Backtrack & Finish Subtree)
[ 2: BLACK (Fully Explored) ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Undirected Cycle Detection (Parent Tracking) and Directed Cycle Detection (LeetCode 207 3-Color DFS):

```java
import java.util.*;

// LeetCode 207: Course Schedule (Cycle Detection in Directed Graphs)
public class GraphCycleDetectionMaster {

    // 1. Directed Graph Cycle Detection via 3-Color DFS O(V + E) Time
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());

        for (int[] pre : prerequisites) {
            int course = pre[0];
            int req = pre[1];
            adj.get(req).add(course); // Edge: req -> course
        }

        int[] state = new int[numCourses]; // 0 = WHITE, 1 = GRAY, 2 = BLACK

        for (int i = 0; i < numCourses; i++) {
            if (state[i] == 0) { // If WHITE (Unvisited)
                if (hasDirectedCycleDFS(adj, state, i)) {
                    return false; // Cycle detected! Cannot finish courses.
                }
            }
        }

        return true; // No cycles! All courses can be completed.
    }

    private boolean hasDirectedCycleDFS(List<List<Integer>> adj, int[] state, int u) {
        state[u] = 1; // Mark GRAY (Visiting / On Stack)

        for (int v : adj.get(u)) {
            if (state[v] == 1) {
                return true; // Back-edge detected! Neighbor is GRAY on stack -> CYCLE!
            }
            if (state[v] == 0) {
                if (hasDirectedCycleDFS(adj, state, v)) {
                    return true;
                }
            }
        }

        state[u] = 2; // Mark BLACK (Fully Explored)
        return false;
    }

    // 2. Undirected Graph Cycle Detection via Parent Tracking DFS O(V + E) Time
    public boolean hasUndirectedCycle(int numVertices, List<List<Integer>> adj) {
        boolean[] visited = new boolean[numVertices];

        for (int i = 0; i < numVertices; i++) {
            if (!visited[i]) {
                if (hasUndirectedCycleDFS(adj, visited, i, -1)) {
                    return true; // Cycle detected!
                }
            }
        }

        return false;
    }

    private boolean hasUndirectedCycleDFS(List<List<Integer>> adj, boolean[] visited, int u, int parent) {
        visited[u] = true;

        for (int v : adj.get(u)) {
            if (!visited[v]) {
                if (hasUndirectedCycleDFS(adj, visited, v, u)) {
                    return true;
                }
            } else if (v != parent) {
                return true; // Visited neighbor that is NOT parent -> CYCLE!
            }
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Directed 3-Color Cycle Check Line
if (state[v] == 1) return true; // GRAY node on stack = Cycle!
```

---

## 7. Concrete Problem Examples
* **LeetCode 207 - Course Schedule**: Directed graph cycle detection.
* **LeetCode 684 - Redundant Connection**: Undirected graph cycle detection.
* **Deadlock Detection Engines**: OS resource allocation graph cycles.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 207 `canFinish`:

```java
public class GraphCycleDetectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 207 Course Schedule Test ===");
        GraphCycleDetectionMaster solver = new GraphCycleDetectionMaster();

        int numCourses1 = 2;
        int[][] pre1 = {{1, 0}}; // 0 -> 1 (No cycle)
        System.out.println("Can finish pre1 (0 -> 1)? " + solver.canFinish(numCourses1, pre1)); // Output: true

        int numCourses2 = 2;
        int[][] pre2 = {{1, 0}, {0, 1}}; // 0 -> 1 and 1 -> 0 (Cycle!)
        System.out.println("Can finish pre2 (0 <-> 1)? " + solver.canFinish(numCourses2, pre2)); // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Cycle Detection Mode | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Directed 3-Color DFS** | **$O(V + E)$ Linear ⚡** | **$O(V)$ State Array & Stack**| Back-edge to GRAY (1) node |
| **Undirected Parent DFS**| **$O(V + E)$ Linear ⚡** | **$O(V)$ Visited & Stack**| `visited[v] && v != parent` |

---

## 10. Edge Cases & Boundary Handling
* **Self-Loops (`u -> u`)**: Immediately sets `state[u] = 1`, sees neighbor `u` with `state[u] == 1`, returning `true` (cycle detected).
* **Multiple Disconnected Components**: Outer loop `for (int i = 0; i < V; i++)` checks all components.

---

## 11. Common Mistakes & Anti-Patterns
* **Using a Simple 2-State `visited` Array for Directed Graph Cycle Detection**:
  - A 2-state `boolean[] visited` cannot distinguish between a node active in the current recursion stack (GRAY) vs a node fully explored in a previous component (BLACK).
  - **ALWAYS use 3-Color States (0, 1, 2) or Kahn's In-Degree BFS for directed graphs**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why 3-Color DFS States Prevent False Cycle Alarms:
> In a Directed Acyclic Graph (DAG) with cross-edges (e.g. $A \to B \to D$ and $A \to C \to D$), node $D$ is visited twice.
> A simple boolean `visited` flags $D$ as visited during the second path, causing a **FALSE CYCLE ALARM**.
> 3-Color DFS sets $D$ to **BLACK (2)** after exploring its subtrees. When path $A \to C$ reaches $D$, seeing `state[D] == 2` correctly skips $D$ without flagging a false cycle! ⚡

> **Memory Trick:** **"State 1 (GRAY) = On Stack (Cycle!). State 2 (BLACK) = Explored (Safe!)."**

---

## 13. System & Implementation Comparisons

| Feature | 3-Color DFS Cycle Detection | Kahn's In-Degree BFS Cycle |
| :--- | :--- | :--- |
| **Data Structure** | Call Stack Recursion | **FIFO Queue + In-Degree Array** |
| **Cycle Signal** | Edge to `state[v] == 1` (GRAY) | `processedCount < numVertices` |
| **Code Length** | **~15 Lines Clean Code ⚡** | ~30 Lines |

---

## 14. How to Recognize This in Questions
* **"Determine if prerequisite dependencies or circular deadlocks exist"** $\rightarrow$ LeetCode 207 (Directed Cycle Detection).

---

## 15. Frequently Asked Interview Questions
* **Q: What does a GRAY (1) state represent in 3-Color DFS?**  
  *A:* A node that is currently active inside the call stack frame of the DFS search path.
* **Q: How does Kahn's Algorithm detect cycles using BFS?**  
  *A:* By processing nodes with in-degree 0. If the total number of processed nodes is less than $V$, a cycle exists!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRAPH CYCLE DETECTION                                 |
+-----------------------------------------------------------------------+
| • Undirected Cycle: visited[v] == true && v != parent                 |
| • Directed 3-Color: 0 = WHITE (Unvisited), 1 = GRAY (On Stack), 2 = BLACK|
| • Directed Cycle  : state[v] == 1 (GRAY back-edge) signals a cycle! ⚡ |
| • LeetCode 207    : If cycle exists -> return false (cannot finish)   |
| • Time Bounds     : O(V + E) Linear Time | O(V) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 207 (`Course Schedule`) using 3-Color DFS in Java.
- [ ] I can write Undirected Graph Cycle Detection with parent tracking.
- [ ] I know what 0 (WHITE), 1 (GRAY), and 2 (BLACK) states represent.
- [ ] I know why simple boolean `visited` causes false cycle alarms in DAGs.
- [ ] I can trace 3-Color DFS state transitions step by step.
