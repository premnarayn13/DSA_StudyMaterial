# 15. Eulerian Paths, Hierholzer's Algorithm & Hamiltonian NP-Completeness

## 1. Introduction
An **Eulerian Path** is a trail in a finite graph that visits **EVERY EDGE EXACTLY ONCE**. An **Eulerian Circuit** is an Eulerian path that starts and ends at the same vertex. In contrast, a **Hamiltonian Path** is a trail that visits **EVERY VERTEX EXACTLY ONCE**. While testing and finding Eulerian paths can be executed in **$O(E)$ Linear Time** using **Hierholzer's Algorithm (Reconstruct Itinerary - LeetCode 332)**, finding Hamiltonian paths is a famous **NP-Complete Problem** requiring **Bitmask Dynamic Programming ($O(2^N \cdot N^2)$ Time)** or Backtracking!

> **Important:** Eulerian Path Theorems & Hierholzer's Algorithm:
> 1. **Eulerian Path Existence Theorems**:
>    - **Undirected Graph**: Has an Eulerian Path IF AND ONLY IF the graph is connected AND has **EXACTLY 0 or 2 vertices with ODD degree**! (If 0 odd, it's a circuit; if 2 odd, path starts at 1 odd vertex and ends at the other!).
>    - **Directed Graph (LeetCode 332)**: Has an Eulerian Path IF AND ONLY IF at most 1 vertex has $\text{outDegree} - \text{inDegree} = 1$ (start), at most 1 vertex has $\text{inDegree} - \text{outDegree} = 1$ (end), and all other vertices have $\text{inDegree} == \text{outDegree}$!
> 2. **Hierholzer's Post-Order Edge Traversal**:
>    - Mutate adjacency lists using PriorityQueues `PriorityQueue<String>` (to guarantee lexicographical ordering in LeetCode 332).
>    - Dequeue used edges dynamically during DFS. Push nodes onto a LinkedList / Stack in post-order: `result.addFirst(u)`. ⚡

```
Hierholzer's Eulerian Path Edge Traversal Topology (LeetCode 332 Reconstruct Itinerary):
Flight Edges: JFK -> ATL, JFK -> SFO, ATL -> JFK, ATL -> SFO, SFO -> ATL

PriorityQueue Neighbors from JFK: [ATL, SFO]
Hierholzer DFS Traversal:
JFK ---> ATL ---> JFK ---> SFO ---> ATL ---> SFO

Post-Order Reversal Order: JFK -> ATL -> JFK -> SFO -> ATL -> SFO (Visits every flight edge ONCE!). ⚡
```

---

## 2. Core Concepts & Eulerian vs Hamiltonian Comparison

### 2.1 Eulerian vs Hamiltonian Feature Comparison Matrix
```
Eulerian vs Hamiltonian Feature Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Traversal Concept     | Target Constraint | Time Complexity   | Primary Algorithm |
+-----------------------+-------------------+-------------------+-------------------+
| **Eulerian Path**     | **Every EDGE once ⚡**| **$O(E)$ Linear ⚡**| Hierholzer's Algo |
| **Hamiltonian Path**  | **Every VERTEX once**| **$O(2^N \cdot N^2)$ NP-Complete**| Bitmask DP / TSP |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Eulerian = Every EDGE once in O(E) time! Hamiltonian = Every VERTEX once in O(2^N * N^2) NP-Complete time!"**

---

## 3. Characteristics & $O(E)$ Hierholzer Time Complexity Proof

### 3.1 Mathematical Proof of $O(E \log E)$ / $O(E)$ Hierholzer Complexity
* Hierholzer's algorithm removes each edge from the graph as soon as it is traversed.
* Every edge $e \in E$ is polled from the neighbor `PriorityQueue` exactly ONCE.
* Inserting and polling $E$ edges from PriorityQueues takes $O(E \log E)$ time.
* Node insertion into `LinkedList.addFirst()` takes $O(1)$ constant time.
* Total Time Complexity: $\mathbf{O(E \log E) \text{ Time}}$ (or $O(E)$ with standard queues)! ⚡

---

## 4. Internal Working Mechanics
Tracing Hierholzer's Algorithm on LeetCode 332 (Reconstruct Itinerary) for `[["MUC","LHR"], ["JFK","MUC"], ["SFO","SJC"], ["LHR","SFO"]]`:

```
Graph: JFK -> MUC -> LHR -> SFO -> SJC.

DFS Hierholzer from "JFK":
1. JFK poll "MUC" -> Recurse "MUC".
2. MUC poll "LHR" -> Recurse "LHR".
3. LHR poll "SFO" -> Recurse "SFO".
4. SFO poll "SJC" -> Recurse "SJC".
5. SJC has no outgoing edges -> Terminal node! Add "SJC" to result LinkedList: ["SJC"].
6. Backtrack to SFO: Add "SFO": ["SFO", "SJC"].
7. Backtrack to LHR: Add "LHR": ["LHR", "SFO", "SJC"].
8. Backtrack to MUC: Add "MUC": ["MUC", "LHR", "SFO", "SJC"].
9. Backtrack to JFK: Add "JFK": ["JFK", "MUC", "LHR", "SFO", "SJC"].

Result: ["JFK", "MUC", "LHR", "SFO", "SJC"]! Valid Eulerian Itinerary! ✅
```

---

## 5. Visual Diagram
Hierholzer Post-Order Edge Consumption Topography:

```
Traversal Path: (JFK) ===> (MUC) ===> (LHR) ===> (SFO) ===> (SJC) [NO EDGES LEFT!]
                                                                    |
                                                                    v (Pop Backwards)
Result List:    [JFK,       MUC,        LHR,        SFO,        SJC]  (Constructed in Reverse!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 332 (Reconstruct Itinerary using Hierholzer's Algorithm):

```java
import java.util.*;

// LeetCode 332: Reconstruct Itinerary (Hierholzer's Eulerian Path Algorithm)
public class EulerHamiltonMaster {

    // LeetCode 332 Solution O(E log E) Time, O(E) Space
    public List<String> findItinerary(List<List<String>> tickets) {
        // Step 1: Build Weighted Adjacency Map with PriorityQueue for Lexicographical Order
        Map<String, PriorityQueue<String>> adj = new HashMap<>();

        for (List<String> ticket : tickets) {
            String u = ticket.get(0);
            String v = ticket.get(1);
            adj.putIfAbsent(u, new PriorityQueue<>());
            adj.get(u).offer(v); // PriorityQueue ensures lexicographically smallest flight is picked first
        }

        LinkedList<String> itinerary = new LinkedList<>();

        // Step 2: Launch Hierholzer's DFS from starting airport "JFK"
        dfsHierholzer("JFK", adj, itinerary);

        return itinerary;
    }

    private void dfsHierholzer(String u, Map<String, PriorityQueue<String>> adj, LinkedList<String> itinerary) {
        PriorityQueue<String> neighbors = adj.get(u);

        // Dequeue edges dynamically while neighbors exist
        while (neighbors != null && !neighbors.isEmpty()) {
            String v = neighbors.poll(); // Consume flight edge (u -> v) immediately!
            dfsHierholzer(v, adj, itinerary);
        }

        // Post-Order Step: Add node to head of LinkedList AFTER all outgoing edges are consumed!
        itinerary.addFirst(u);
    }
}
```

> **Quick Syntax:**
```java
// Hierholzer Edge Dequeue & Post-Order Add Line
while (adj.get(u) != null && !adj.get(u).isEmpty()) dfs(adj.get(u).poll());
itinerary.addFirst(u); // Post-order prepend
```

---

## 7. Concrete Problem Examples
* **LeetCode 332 - Reconstruct Itinerary**: Primary Eulerian path problem.
* **LeetCode 753 - Cracking the Safe**: De Bruijn sequence Eulerian circuit.
* **Travelling Salesperson Problem (TSP)**: Hamiltonian cycle NP-hard problem.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 332 `findItinerary`:

```java
public class EulerHamiltonDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 332 Reconstruct Itinerary Test ===");
        EulerHamiltonMaster solver = new EulerHamiltonMaster();

        List<List<String>> tickets = Arrays.asList(
            Arrays.asList("JFK","SFO"),
            Arrays.asList("JFK","ATL"),
            Arrays.asList("SFO","ATL"),
            Arrays.asList("ATL","JFK"),
            Arrays.asList("ATL","SFO")
        );

        List<String> itinerary = solver.findItinerary(tickets);
        System.out.println("Lexicographical Itinerary: " + itinerary);
        // Output: ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Hierholzer Eulerian Path**| **$O(E \log E)$ Linear-Log ⚡**| **$O(E)$ Flight Stack Space**| Consumes edges via PriorityQueue |
| **Hamiltonian Path (TSP)**  | **$O(2^N \cdot N^2)$ Exponential**| **$O(2^N \cdot N)$ DP Memory**| Bitmask DP over subset masks |

---

## 10. Edge Cases & Boundary Handling
* **Graph with Dead-End Sub-Loops**: Hierholzer's post-order `addFirst(u)` automatically handles dead-end sub-loops by prepending them after the main Eulerian loop finishes.
* **Disconnected Flight Graph**: Handled safely by starting at `"JFK"`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Standard Post-Order Stack `add(u)` Instead of `addFirst(u)`**:
  - Pushing nodes to the end of a list without reversing yields the inverse Eulerian path!
  - **ALWAYS use `itinerary.addFirst(u)` (or reverse the resulting list at the end)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `itinerary.addFirst(u)` Works for Hierholzer's Algorithm:
> When DFS hits a dead-end vertex with no remaining outgoing edges, that vertex MUST be the terminal end of the Eulerian path!
> Prepending nodes to the head (`addFirst(u)`) as DFS backtracks constructs the valid forward path in exact Eulerian order! ⚡

> **Memory Trick:** **"Hierholzer's Algorithm: Poll edges dynamically, prepend nodes post-order using addFirst(u)!"**

---

## 13. System & Implementation Comparisons

| Feature | Eulerian Path (Hierholzer) | Hamiltonian Path (Bitmask DP) |
| :--- | :--- | :--- |
| **Definition** | Every EDGE visited once | Every VERTEX visited once |
| **Complexity Class** | **P (Polynomial $O(E)$) ⚡** | **NP-Complete ($O(2^N \cdot N^2)$)** |
| **Decision Rule** | Check degree conditions | Exponential state search |

---

## 14. How to Recognize This in Questions
* **"Reconstruct valid itinerary visiting all given flight tickets exactly once"** $\rightarrow$ LeetCode 332 (Hierholzer's Eulerian Path).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the difference between an Eulerian path and a Hamiltonian path?**  
  *A:* An Eulerian path visits every EDGE exactly once ($O(E)$ time); a Hamiltonian path visits every VERTEX exactly once ($O(2^N \cdot N^2)$ time).
* **Q: Why does LeetCode 332 use a `PriorityQueue` for neighbor adjacency lists?**  
  *A:* To ensure that when multiple valid flight destinations exist, the lexicographically smaller airport is picked first.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: EULERIAN PATHS & HIERHOLZER'S ALGORITHM              |
+-----------------------------------------------------------------------+
| • Eulerian Path   : Traverses every EDGE in graph exactly ONCE!       |
| • Undirected Rule : 0 or 2 vertices with odd degree                    |
| • Hierholzer Loop : while (!pq.isEmpty()) dfs(pq.poll()); itinerary.addFirst(u);|
| • LeetCode 332    : PriorityQueue adjacency list for lexicographical order|
| • Performance     : O(E log E) Time | O(E) Auxiliary Memory Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 332 (`Reconstruct Itinerary`) in Java.
- [ ] I can state the Eulerian path existence theorems for directed and undirected graphs.
- [ ] I know why `itinerary.addFirst(u)` is used in post-order DFS.
- [ ] I can explain the difference between Eulerian and Hamiltonian paths.
- [ ] I can trace Hierholzer's edge traversal step by step.
