# 06. Topological Sort, Kahn's In-Degree BFS & Dependency Order Resolution

## 1. Introduction
**Topological Sort** is a linear ordering of all vertices in a **Directed Acyclic Graph (DAG)** such that for every directed edge $u \to v$, vertex $u$ comes BEFORE vertex $v$ in the ordering. Used extensively in **Build Dependency Resolvers (e.g. Maven/Gradle, Makefiles)**, **Task Schedulers**, and **Course Schedule II (LeetCode 210)**, Topological Sorting can be computed using two primary algorithms: **Kahn's In-Degree BFS Algorithm** and **Post-Order DFS with Reverse Stack**, both executing in **$O(V + E)$ Strict Linear Time**.

> **Important:** Core Invariants of Topological Sorting:
> 1. **DAG Pre-Condition**: Topological Sort is possible IF AND ONLY IF the directed graph contains **ZERO CYCLES**! If a cycle exists, no valid topological ordering can exist.
> 2. **Kahn's In-Degree BFS Invariant**: Nodes with `inDegree[v] == 0` have NO remaining dependencies and can be safely processed!
>    - Decrement `inDegree[neighbor]--` when dequeuing a node. When `inDegree[neighbor] == 0`, enqueue it!
> 3. **Cycle Verification**: If the number of nodes processed by Kahn's Algorithm is LESS than $V$, a cycle exists! Return empty array `[]`! ⚡

```
Directed Acyclic Graph (DAG) Topological Ordering Topology:
Edges: (0 -> 1), (0 -> 2), (1 -> 3), (2 -> 3)

In-Degree Table: Node 0: 0, Node 1: 1, Node 2: 1, Node 3: 2

Kahn's BFS Order:
1. Enqueue Node 0 (inDegree=0). Result = [0].
2. Process Node 0 -> Decrement inDegree of 1 and 2 to 0 -> Enqueue 1 and 2.
3. Process Node 1 -> Decrement inDegree of 3 (becomes 1). Result = [0, 1].
4. Process Node 2 -> Decrement inDegree of 3 (becomes 0) -> Enqueue 3. Result = [0, 1, 2].
5. Process Node 3 -> Result = [0, 1, 2, 3]! Valid Topological Order! ⚡
```

---

## 2. Core Concepts & Kahn's BFS vs Post-Order DFS

### 2.1 Topological Sort Strategy Matrix
```
Topological Sort Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm Variant     | Data Structure    | Cycle Detection   | Ordering Logic    |
+-----------------------+-------------------+-------------------+-------------------+
| **Kahn's BFS**        | In-Degree Array + Queue| `count < V`   | Direct (Natural)  |
| **Post-Order DFS**    | LIFO Stack / List | 3-Color States    | Reverse Stack Pop |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Kahn's Algo: Process nodes with inDegree == 0! Decrement neighbor inDegrees! If count < V -> Cycle!"**

---

## 3. Characteristics & Uniqueness of Topological Ordering

### 3.1 Multiple Valid Topological Orderings
* A DAG can have MULTIPLE valid topological orderings (e.g. both `[0, 1, 2, 3]` and `[0, 2, 1, 3]` are valid for the graph above).
* A topological ordering is **UNIQUE** IF AND ONLY IF at every step of Kahn's Algorithm, the Queue contains AT MOST 1 element!

---

## 4. Internal Working Mechanics
Tracing LeetCode 210 (Course Schedule II) on 4 Courses with Edges `[[1,0], [2,0], [3,1], [3,2]]` (0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3):

```
In-Degrees: [0: 0, 1: 1, 2: 1, 3: 2].

Step 1: Enqueue Node 0 (inDegree = 0). Queue = [0].

Step 2: Pop 0. Add 0 to order [0].
- Neighbors: 1 and 2. Decrement inDegree[1] (becomes 0), inDegree[2] (becomes 0).
- Queue = [1, 2].

Step 3: Pop 1. Add 1 to order [0, 1].
- Neighbor: 3. Decrement inDegree[3] (becomes 1).

Step 4: Pop 2. Add 2 to order [0, 1, 2].
- Neighbor: 3. Decrement inDegree[3] (becomes 0). Queue = [3].

Step 5: Pop 3. Add 3 to order [0, 1, 2, 3].

Total Processed = 4 == V! Return [0, 1, 2, 3]! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
Kahn's In-Degree Reduction Topography:

```
Initial In-Degrees: Node 0 (0) ---> Node 1 (1) ---> Node 3 (2)
                               \-> Node 2 (1) --/

Processing Node 0:  Node 0 [DONE] -> Node 1 (0) -> Enqueue 1!
                                  -> Node 2 (0) -> Enqueue 2!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 210 (Course Schedule II using Kahn's In-Degree BFS and Post-Order DFS):

```java
import java.util.*;

// LeetCode 210: Course Schedule II (Topological Sort)
public class TopologicalSortMaster {

    // 1. Kahn's In-Degree BFS Algorithm (LeetCode 210 Primary Solution) O(V + E) Time
    public int[] findOrderKahn(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());

        int[] inDegree = new int[numCourses];

        // Step 1: Build Adjacency List & Compute In-Degrees
        for (int[] pre : prerequisites) {
            int course = pre[0];
            int req = pre[1];
            adj.get(req).add(course); // Edge: req -> course
            inDegree[course]++;        // Increment in-degree of course
        }

        // Step 2: Enqueue all nodes with inDegree == 0 (Zero Dependencies)
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }

        int[] topoOrder = new int[numCourses];
        int index = 0;

        // Step 3: Process Queue Level by Level
        while (!queue.isEmpty()) {
            int u = queue.poll();
            topoOrder[index++] = u; // Add node to topological order

            for (int v : adj.get(u)) {
                inDegree[v]--; // Remove edge dependency (u -> v)
                if (inDegree[v] == 0) {
                    queue.offer(v); // Enqueue neighbor when all dependencies resolved
                }
            }
        }

        // Step 4: Cycle Check (If processed count < numCourses, a cycle exists!)
        if (index != numCourses) {
            return new int[0]; // Return empty array if cycle detected
        }

        return topoOrder;
    }

    // 2. Post-Order DFS Topological Sort O(V + E) Time
    public int[] findOrderDFS(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] pre : prerequisites) adj.get(pre[1]).add(pre[0]);

        int[] state = new int[numCourses]; // 0=WHITE, 1=GRAY, 2=BLACK
        Deque<Integer> stack = new ArrayDeque<>();

        for (int i = 0; i < numCourses; i++) {
            if (state[i] == 0) {
                if (dfsTopological(adj, state, stack, i)) {
                    return new int[0]; // Cycle detected!
                }
            }
        }

        int[] topoOrder = new int[numCourses];
        int idx = 0;
        while (!stack.isEmpty()) {
            topoOrder[idx++] = stack.pop(); // Pop from stack to reverse post-order
        }

        return topoOrder;
    }

    private boolean dfsTopological(List<List<Integer>> adj, int[] state, Deque<Integer> stack, int u) {
        state[u] = 1; // Mark GRAY

        for (int v : adj.get(u)) {
            if (state[v] == 1) return true; // Cycle detected!
            if (state[v] == 0) {
                if (dfsTopological(adj, state, stack, v)) return true;
            }
        }

        state[u] = 2; // Mark BLACK
        stack.push(u); // Push to stack in post-order!
        return false;
    }
}
```

> **Quick Syntax:**
```java
// Kahn's In-Degree BFS Processing Line
inDegree[v]--; if (inDegree[v] == 0) queue.offer(v);
```

---

## 7. Concrete Problem Examples
* **LeetCode 210 - Course Schedule II**: Full topological ordering output.
* **LeetCode 269 - Alien Dictionary**: Character dependency topological sort.
* **LeetCode 310 - Minimum Height Trees**: In-degree leaf trimming BFS.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 210 `findOrderKahn`:

```java
public class TopologicalSortDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 210 Course Schedule II Test ===");
        TopologicalSortMaster solver = new TopologicalSortMaster();

        int numCourses = 4;
        int[][] pre = {{1,0}, {2,0}, {3,1}, {3,2}};

        int[] order = solver.findOrderKahn(numCourses, pre);
        System.out.println("Topological Course Order: " + Arrays.toString(order));
        // Output: [0, 1, 2, 3] (or [0, 2, 1, 3]) ✅
    }
}
```

---

## 9. Complexity Analysis

| Topological Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Kahn's BFS Algorithm** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Queue & InDegree**| Process nodes with in-degree 0 |
| **Post-Order DFS** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Stack Memory** | Reverse post-order stack pop |

---

## 10. Edge Cases & Boundary Handling
* **Graph Has a Cycle**: Kahn's Algorithm processes fewer than $V$ nodes (`index != numCourses`), returning `[]`.
* **No Prerequisites ($E = 0$)**: All nodes have `inDegree == 0`, returning default `[0, 1, ..., V-1]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Check if `index == numCourses` at the End of Kahn's Algorithm**:
  - Failing to check processed count allows cyclic graphs to return incomplete, corrupted ordering arrays.
  - **ALWAYS check `if (index != numCourses) return new int[0];`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Kahn's BFS Algorithm Is Preferred for Interviews:
> 1. Kahn's Algorithm processes nodes in natural forward topological order (no stack reversing needed!).
> 2. It performs cycle detection automatically via the `index != V` count check without needing 3-Color DFS states.
> 3. It easily adapts to PriorityQueues for **Lexicographically Smallest Topological Sort**! ⚡

> **Memory Trick:** **"Kahn's BFS: Natural forward order, built-in cycle check (count < V), easily lexicographical with PriorityQueue!"**

---

## 13. System & Implementation Comparisons

| Feature | Kahn's In-Degree BFS Algorithm | Post-Order DFS Algorithm |
| :--- | :--- | :--- |
| **Ordering Output** | **Natural Forward Order ⚡** | Reverse Order (Requires Stack Pop) |
| **Cycle Detection** | Built-in (`count < V`) | Requires 3-Color States (0,1,2) |
| **Lexicographical Sort**| Easy (Replace Queue with PriorityQueue)| Difficult |

---

## 14. How to Recognize This in Questions
* **"Order tasks or courses given prerequisite dependencies, or return [] if impossible"** $\rightarrow$ LeetCode 210 (Topological Sort).

---

## 15. Frequently Asked Interview Questions
* **Q: How does Kahn's Algorithm detect cycles?**  
  *A:* Nodes in a cycle never reach in-degree 0, so they are never enqueued. If total processed nodes $< V$, a cycle exists.
* **Q: How can you find the lexicographically smallest topological sort?**  
  *A:* Replace `Queue<Integer>` with `PriorityQueue<Integer>` (Min-Heap) in Kahn's Algorithm.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TOPOLOGICAL SORT (LEETCODE 210)                       |
+-----------------------------------------------------------------------+
| • Pre-condition  : Applies ONLY to Directed Acyclic Graphs (DAGs)     |
| • Kahn's Step 1  : Compute in-degree for all V nodes                  |
| • Kahn's Step 2  : Enqueue nodes with inDegree == 0                   |
| • Kahn's Step 3  : Pop u -> for v in adj[u]: inDegree[v]--; if 0 offer|
| • Cycle Check    : If (processedCount != V) return new int[0];        |
| • Time Bounds    : O(V + E) Linear Time | O(V) Auxiliary Memory Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 210 (`Course Schedule II`) using Kahn's BFS in Java.
- [ ] I can write Topological Sort using Post-Order DFS with a Stack.
- [ ] I know why `processedCount != V` signals a cycle in Kahn's Algorithm.
- [ ] I know how to get the lexicographically smallest topological order.
- [ ] I can trace Kahn's In-Degree BFS step by step.
