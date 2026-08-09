# 10. Master Reference — Disjoint Set Union (DSU / Union-Find)

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 18: Disjoint Set Union (DSU / Union-Find)**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for set partitioning algorithms, graph connectivity, and technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Path Compression (`parent[i] = find(parent[i])`), Union by Rank/Size rules, Inverse Ackermann Function $\alpha(N) \approx O(1)$ Amortized Near-Constant Time, Undirected Graph Cycle Detection (`!dsu.union(u, v)`), Kruskal's MST, 2D Grid Coordinate Flattening (`id = r * N + c`) for LeetCode 305, Accounts Merge (LeetCode 721), and $O(N)$ Longest Consecutive Sequence (LeetCode 128)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **2D to 1D Grid Flattening Formula**:
  - `id = r * N + c;` (Maps 2D cell $(r, c)$ in an $M \times N$ grid to a 1D DSU ID).
* **Inverse Ackermann Complexity Bound**:
  - $\alpha(N) \le 4$ for all $N \le 10^{80} \implies \mathbf{\alpha(N) \approx O(1) \text{ Amortized Constant Time}}$.
* **Path Compression 1-Liner**:
  - `public int find(int i) { if (i == parent[i]) return i; return parent[i] = find(parent[i]); }`
* **Union by Size Rule**:
  - `if (size[rootX] < size[rootY]) { parent[rootX] = rootY; size[rootY] += size[rootX]; }`
* **Undirected Cycle Detection Rule**:
  - Edge $(u, v)$ completes a cycle IF AND ONLY IF `find(u) == find(v)` (`!dsu.union(u, v)`).

```
DSU Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Path Compression Assignment       | return parent[i] = find(parent[i]);               |
| Tree Height Bound (Union Rank)    | H <= log2 N strictly guaranteed                   |
| Combined Amortized Complexity     | alpha(N) approx O(1) Near-Constant Time ⚡         |
| 2D Grid Index Formula             | id = r * N + c                                    |
| Cycle Detection Signal            | if (!dsu.union(u, v)) -> CYCLE DETECTED!          |
| Component Count Tracking          | count-- on every successful root merge            |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Quick Find `find(x)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ Array Space | Direct `id[x]` lookup |
| **Quick Find `union(x, y)`**| $O(N)$ Linear Scan | $O(N)$ Linear Scan | $O(N)$ Linear Scan | $O(N)$ Array Space | Scans entire array |
| **Quick Union `find(x)`**| $O(1)$ Constant | $O(H)$ Path Hops | $O(N)$ (Skewed Tree) | $O(N)$ Array Space | Unoptimized parent traversal |
| **Path Compression Only**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Amortized**| $O(N)$ Array Space | Tree flattening recursion |
| **Rank/Size + Compression**| **$\alpha(N) \approx O(1)$ ⚡**| **$\alpha(N) \approx O(1)$ ⚡**| **$\alpha(N) \approx O(1)$ ⚡**| $O(N)$ Array Space | Height bounding + flattening |
| **Redundant Edge (684)**| **$O(E \cdot \alpha(V))$ ⚡**| **$O(E \cdot \alpha(V))$ ⚡**| **$O(E \cdot \alpha(V))$ ⚡**| $O(V)$ DSU Array | Cycle detection via `!union` |
| **Islands II (305)**   | **$O(K \cdot \alpha(MN))$ ⚡**| **$O(K \cdot \alpha(MN))$ ⚡**| **$O(K \cdot \alpha(MN))$ ⚡**| $O(M \cdot N)$ DSU | 2D DSU dynamic land union |
| **Accounts Merge (721)**| **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | $O(N)$ Hash Map | Email ID union + sorting |
| **Consecutive (128)**  | **$O(N \cdot \alpha(N))$ ⚡**| **$O(N \cdot \alpha(N))$ ⚡**| **$O(N \cdot \alpha(N))$ ⚡**| $O(N)$ Hash Map | Map lookup + neighbor union |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for DSU Data Structures                                          |
+-----------------------------------------------------------------------------------+
| `parent[]` Integer Array             : 4 Bytes per Element ($4N$ Bytes Total)         |
| `size[]` or `rank[]` Integer Array   : 4 Bytes per Element ($4N$ Bytes Total)         |
| Total DSU Footprint for $N = 100,000$ : 800 KB Total Memory (Fits in CPU L2 Cache!)⚡  |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Recursive Path Compression find Method
public int find(int i) { if (i == parent[i]) return i; return parent[i] = find(parent[i]); }

// 2. Union by Size with Boolean Return Block
public boolean union(int x, int y) {
    int rootX = find(x), rootY = find(y);
    if (rootX == rootY) return false; // Cycle signal!
    if (size[rootX] < size[rootY]) { parent[rootX] = rootY; size[rootY] += size[rootX]; }
    else { parent[rootY] = rootX; size[rootX] += size[rootY]; }
    count--; return true;
}

// 3. 2D to 1D Grid Index Line
int id = r * n + c;

// 4. Undirected Graph Cycle Detection Check
if (!dsu.union(u, v)) return edge; // Cycle detected!

// 5. LeetCode 128 Consecutive Sequence Union Line
if (numToId.containsKey(num + 1)) dsu.union(numToId.get(num), numToId.get(num + 1));
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Linking Child Nodes Instead of Roots**: Writing `parent[y] = x` instead of `parent[rootY] = rootX` corrupts tree components. Always find roots first before linking!
* **Pitfall 2: Using DSU for Directed Graph Cycle Detection**: DSU assumes undirected edges. Using DSU on directed graphs produces incorrect results. Use Topological Sort for directed graphs!
* **Pitfall 3: Returning `void` from `union()`**: Returning `void` prevents clean cycle detection. Always return `boolean` (`true` if merged, `false` if cycle/already connected).
* **Pitfall 4: Using Account Names as DSU Keys in LeetCode 721**: Different people can share the same name. Always use globally unique EMAILS as DSU keys!
* **Pitfall 5: Scanning 2D Grids with $O(M \cdot N)$ BFS/DFS on Dynamic Stream Input**: Dynamic land addition streams (LeetCode 305) require 2D DSU ($\alpha(MN) \approx O(1)$ time) to prevent TLE.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 18 (DISJOINT SET UNION - DSU)    |
+-----------------------------------------------------------------------+
| 1. Path Compression: return parent[i] = find(parent[i]);              |
| 2. Height Bound    : Union by Rank/Size guarantees H <= log2 N        |
| 3. Operational Cost: Path Compression + Rank = $\alpha(N) \approx O(1)$ ⚡|
| 4. Cycle Detection : !dsu.union(u, v) signals cycle in UNDIRECTED graph|
| 5. Grid Mapping    : id = r * N + c for 2D dynamic islands (305)      |
| 6. Accounts Merge  : Map unique emails to IDs; union emails per account|
| 7. Consecutive (128): Union num with num+1; return max component size  |
| 8. Component Count : count-- on every successful root union           |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Path Compression + Union by Size in Java in under 2 minutes.
- [ ] I can write LeetCode 684 (`Redundant Connection`) using DSU.
- [ ] I can write LeetCode 305 (`Number of Islands II`) using 2D DSU.
- [ ] I can write LeetCode 721 (`Accounts Merge`) using DSU email mapping.
- [ ] I can write LeetCode 128 (`Longest Consecutive Sequence`) in $O(N)$ time.
- [ ] I can write Kruskal's Minimum Spanning Tree algorithm using DSU.
- [ ] I know why DSU cycle detection applies ONLY to undirected graphs.
- [ ] I can state the Inverse Ackermann bound $\alpha(N) \le 4$.
