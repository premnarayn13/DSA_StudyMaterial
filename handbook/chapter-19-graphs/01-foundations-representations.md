# 01. Graph Foundations, Topologies & Storage Representations

## 1. Introduction
A **Graph** $G = (V, E)$ is a non-linear data structure consisting of a set of **Vertices (Nodes)** $V$ connected by a set of **Edges (Links)** $E$. Graphs model complex relational topologies across computer networks, web search crawlers, social recommendation graphs, and geographic maps. Graph storage representations balance memory footprint and operational time, choosing between **Adjacency Lists ($O(V + E)$ Memory)**, **Adjacency Matrices ($O(V^2)$ Memory)**, and **Edge Lists ($O(E)$ Memory)**.

> **Important:** Graph Classification & Structural Invariants:
> 1. **Directed vs Undirected**: Directed edges $(u \to v)$ possess strict one-way directionality; Undirected edges $(u \leftrightarrow v)$ permit symmetric traversal in both directions.
> 2. **Weighted vs Unweighted**: Weighted edges assign numerical costs/distances $w(u, v)$ to connections.
> 3. **Dense vs Sparse Graphs**:
>    - **Sparse Graph**: $E \ll V^2$ (e.g. $E \approx O(V)$). Best stored via **Adjacency List** ($O(V + E)$ space).
>    - **Dense Graph**: $E \approx V^2$. Best queried via **Adjacency Matrix** ($O(V^2)$ space, $O(1)$ edge lookup). ⚡

```
Graph Topologies & Adjacency Representation Models:
Directed Graph:                   Undirected Weighted Graph:
    (0) ---> (1)                        (0) --- [5] --- (1)
     |        |                          |               |
     v        v                         [2]             [8]
    (2) ---> (3)                         |               |
                                        (2) --- [1] --- (3)
```

---

## 2. Core Concepts & Adjacency List vs Matrix vs Edge List

### 2.1 Storage Representation Matrix Comparison
```
Graph Storage Representations Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Representation        | Space Complexity  | Edge Lookup $(u,v)$| All Neighbors of $u$|
+-----------------------+-------------------+-------------------+-------------------+
| **Adjacency List**    | **$O(V + E)$ ⚡** | $O(\text{deg}(u))$| **$O(\text{deg}(u))$ ⚡**|
| **Adjacency Matrix**  | $O(V^2)$ Space    | **$O(1)$ Instant ⚡**| $O(V)$ Full Scan |
| **Edge List**         | **$O(E)$ Space ⚡**| $O(E)$ Linear Scan| $O(E)$ Linear Scan|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Use Adjacency Lists for sparse graphs O(V + E); use Adjacency Matrices for instant O(1) edge lookups!"**

---

## 3. Characteristics & Handshaking Lemma Proof

### 3.1 Mathematical Proof of the Handshaking Lemma
In any undirected graph $G = (V, E)$, the sum of degrees of all vertices equals TWICE the total number of edges:

$$\sum_{v \in V} \text{deg}(v) = 2 |E|$$

* **Proof**: Every single undirected edge $e = (u, v)$ contributes $+1$ to the degree of vertex $u$ and $+1$ to the degree of vertex $v$.
* Therefore, summing vertex degrees counts every edge exactly twice!
* **Corollary**: The number of vertices with an ODD degree is ALWAYS EVEN! ⚡

---

## 4. Internal Working Mechanics
Tracing Storage of Undirected Weighted Graph with Edges `(0, 1, 5)`, `(0, 2, 2)`, `(1, 3, 8)`:

```
1. Adjacency List (List<List<Edge>>):
- adj[0] -> [Node 1 (wt 5), Node 2 (wt 2)]
- adj[1] -> [Node 0 (wt 5), Node 3 (wt 8)]
- adj[2] -> [Node 0 (wt 2)]
- adj[3] -> [Node 1 (wt 8)]

2. Adjacency Matrix (int[][] mat):
- mat[0][1] = 5, mat[1][0] = 5
- mat[0][2] = 2, mat[2][0] = 2
- mat[1][3] = 8, mat[3][1] = 8

Adjacency List uses O(V + E) memory; Adjacency Matrix allows O(1) edge weight lookup! ✅
```

---

## 5. Visual Diagram
Adjacency List vs Adjacency Matrix Memory Topography:

```
Adjacency List:                        Adjacency Matrix:
Node 0: -> [1 (wt 5)] -> [2 (wt 2)]    mat:  0  1  2  3
Node 1: -> [0 (wt 5)] -> [3 (wt 8)]       0 [0, 5, 2, 0]
Node 2: -> [0 (wt 2)]                     1 [5, 0, 0, 8]
Node 3: -> [1 (wt 8)]                     2 [2, 0, 0, 0]
                                          3 [0, 8, 0, 0]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Adjacency List, Adjacency Matrix, and Edge List Graph representations:

```java
import java.util.*;

public class GraphRepresentationsMaster {

    public static class Edge {
        public int to;
        public int weight;

        public Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    // 1. Adjacency List Representation (Optimal for Sparse Graphs)
    public static class AdjacencyListGraph {
        private final int numVertices;
        private final List<List<Edge>> adj;

        public AdjacencyListGraph(int numVertices) {
            this.numVertices = numVertices;
            this.adj = new ArrayList<>();
            for (int i = 0; i < numVertices; i++) {
                adj.add(new ArrayList<>());
            }
        }

        public void addEdge(int from, int to, int weight, boolean directed) {
            adj.get(from).add(new Edge(to, weight));
            if (!directed) {
                adj.get(to).add(new Edge(from, weight));
            }
        }

        public List<Edge> getNeighbors(int u) {
            return adj.get(u);
        }

        public int getNumVertices() { return numVertices; }
    }

    // 2. Adjacency Matrix Representation (Optimal for Dense Graphs)
    public static class AdjacencyMatrixGraph {
        private final int numVertices;
        private final int[][] matrix;

        public AdjacencyMatrixGraph(int numVertices) {
            this.numVertices = numVertices;
            this.matrix = new int[numVertices][numVertices];
        }

        public void addEdge(int from, int to, int weight, boolean directed) {
            matrix[from][to] = weight;
            if (!directed) {
                matrix[to][from] = weight;
            }
        }

        public boolean hasEdge(int u, int v) {
            return matrix[u][v] != 0;
        }

        public int getWeight(int u, int v) {
            return matrix[u][v];
        }
    }
}
```

> **Quick Syntax:**
```java
// Adjacency List Initialization Block
List<List<Edge>> adj = new ArrayList<>();
for (int i = 0; i < V; i++) adj.add(new ArrayList<>());
```

---

## 7. Concrete Problem Examples
* **LeetCode 133 - Clone Graph**: Graph structural traversal.
* **Network Topology Modeling**: High-concurrency graph building.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Adjacency List and Adjacency Matrix creation:

```java
public class GraphRepresentationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Graph Storage Representations Test ===");
        GraphRepresentationsMaster.AdjacencyListGraph graph = 
            new GraphRepresentationsMaster.AdjacencyListGraph(4);

        graph.addEdge(0, 1, 5, false);
        graph.addEdge(0, 2, 2, false);
        graph.addEdge(1, 3, 8, false);

        System.out.println("Neighbors of Node 0:");
        for (GraphRepresentationsMaster.Edge edge : graph.getNeighbors(0)) {
            System.out.println(" -> Node " + edge.to + " (Weight: " + edge.weight + ")");
        }
        // Output:
        // -> Node 1 (Weight: 5)
        // -> Node 2 (Weight: 2) ✅
    }
}
```

---

## 9. Complexity Analysis

| Graph Representation | Space Complexity | Add Edge | Lookup Edge $(u, v)$ | Iterate Neighbors of $u$ |
| :--- | :--- | :--- | :--- | :--- |
| **Adjacency List** | **$O(V + E)$ Linear ⚡**| **$O(1)$ Constant ⚡**| $O(\text{deg}(u))$ | **$O(\text{deg}(u))$ ⚡**|
| **Adjacency Matrix**| $O(V^2)$ Quadratic | **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡**| $O(V)$ Scan |

---

## 10. Edge Cases & Boundary Handling
* **Disconnected Vertices (Degree 0)**: Stored as empty lists `adj.get(u)` in Adjacency List.
* **Self-Loops (`u == v`)**: `adj.get(u).add(new Edge(u, w))` handles self-loops safely.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Adjacency Matrix for $V = 100,000$ Vertices**:
  - `new int[100000][100000]` allocates $10^{10}$ integers $\approx 40$ GB memory, crashing with `OutOfMemoryError`.
  - **ALWAYS use Adjacency Lists (`List<List<Integer>>`) for large sparse graphs**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The Golden Rule of Graph Storage Selection:
> * Use **Adjacency List ($O(V + E)$ space)** when $E \ll V^2$ (Sparse graphs, standard BFS/DFS, Dijkstra).
> * Use **Adjacency Matrix ($O(V^2)$ space)** when $E \approx V^2$ (Dense graphs, Floyd-Warshall all-pairs shortest paths).

> **Memory Trick:** **"Sparse Graph = Adjacency List! Dense Graph = Adjacency Matrix!"**

---

## 13. System & Implementation Comparisons

| Feature | Adjacency List | Adjacency Matrix |
| :--- | :--- | :--- |
| **Memory Footprint** | **$O(V + E)$ Minimal ⚡** | $O(V^2)$ Heavy |
| **Iterating Neighbors**| **Instant $O(\text{deg}(u))$ ⚡**| $O(V)$ Scanning zeros |
| **Edge Lookup $(u, v)$**| $O(\text{deg}(u))$ Search | **Instant $O(1)$ Direct ⚡**|

---

## 14. How to Recognize This in Questions
* **"Represent graph structure for optimal memory traversal"** $\rightarrow$ Adjacency List Representation.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Handshaking Lemma?**  
  *A:* The mathematical identity stating that the sum of all vertex degrees in an undirected graph equals $2 |E|$.
* **Q: Why are Adjacency Lists preferred for Dijkstra's Algorithm?**  
  *A:* Because iterating over neighbors of vertex $u$ takes $O(\text{deg}(u))$ time in an Adjacency List instead of scanning $V$ matrix columns.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRAPH FOUNDATIONS & REPRESENTATIONS                   |
+-----------------------------------------------------------------------+
| • Adjacency List  : List<List<Edge>> adj -> Space O(V + E) (Sparse!) ⚡ |
| • Adjacency Matrix: int[][] mat          -> Space O(V^2), Edge Lookup O(1)|
| • Handshake Lemma : Sum of deg(v) = 2 * |E|                           |
| • Rule of Thumb   : Default to Adjacency List for all BFS/DFS/Dijkstra|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write an Adjacency List representation in Java.
- [ ] I can write an Adjacency Matrix representation in Java.
- [ ] I can prove the Handshaking Lemma ($\sum \text{deg}(v) = 2|E|$).
- [ ] I know when to choose Adjacency List vs Adjacency Matrix.
- [ ] I can trace neighbor iterations for sparse graphs.
