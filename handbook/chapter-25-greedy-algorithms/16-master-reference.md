# 16. Master Reference — Greedy Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 25: Greedy Algorithms**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Greedy Fundamentals, Activity Selection, Fractional Knapsack, Job Sequencing (DSU), Huffman Coding, Minimum Spanning Trees (Kruskal & Prim), Shortest Path (Dijkstra), Partitioning Problems (Meeting Rooms II / Minimum Platforms), Scheduling Problems (SPT & EDF), Coin Change (Greedy vs DP), Greedy Choice Property & Matroids, Optimal Substructure, Proof Techniques (Exchange & Staying Ahead), Pattern Recognition, and Advanced Regret Priority Queues.

> **Important:** Review this master reference 15 minutes before an interview to refresh the 6 Greedy Master Archetypes, Activity Selection finish time sort ($f_i$), Fractional Knapsack density sort ($v_i / w_i$), Job Sequencing DSU path compression, Kruskal DSU vs Prim Min-Heap, Dijkstra's non-negative edge requirement, Meeting Rooms II peak concurrency, Huffman min-heap merges, Canonical Coin Change boundary, Rado-Edmonds Matroid Theorem, and Greedy Regret Max-Heap swaps!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Fractional Knapsack Density Formula**:
  - Value Density $d_i = \frac{v_i}{w_i}$. Sort descending ($d_1 \ge d_2 \ge \dots \ge d_N$).
* **Activity Selection Selection Invariant**:
  - Sort by Earliest Finish Time ($f_i$ ASC). Select activity if $s_i \ge f_{\text{last}}$.
* **Job Sequencing DSU Union Rule**:
  - Schedule job at $s = \text{find}(d_i)$. If $s > 0$, claim slot and `union(s, find(s - 1))`.
* **Cut Property (MST Invariant)**:
  - Lightest edge crossing ANY cut $(S, V \setminus S)$ belongs to the Minimum Spanning Tree.
* **Dijkstra's Edge Relaxation Formula**:
  - `if (dist[u] + w < dist[v]) dist[v] = dist[u] + w;` (Requires non-negative edges $w \ge 0$).
* **Peak Concurrency Partitioning Theorem**:
  - $\text{Minimum Rooms / Platforms} = \text{Maximum Peak Concurrency}$ of overlapping intervals.
* **Shortest Processing Time (SPT / Smith's Rule)**:
  - Minimizes average completion time $\sum C_i$ by sorting task durations $p_i$ ASCENDING.
* **Earliest Deadline First (EDF / Jackson's Rule)**:
  - Minimizes maximum lateness $L_{\max} = \max(0, C_i - d_i)$ by sorting task deadlines $d_i$ ASCENDING.
* **Task Scheduler Interval Formula (LeetCode 621)**:
  - $\text{Intervals} = \max\left( \text{tasks.length}, (f_{\max} - 1) \cdot (n + 1) + k \right)$.
* **Shannon Entropy Limit**:
  - $H(X) = -\sum p_i \log_2 p_i \le L(C) < H(X) + 1 \text{ bits per char}$.
* **Matroid Structure & Rado-Edmonds Theorem**:
  - Matroid $M = (E, \mathcal{I})$ satisfies Non-Emptiness, Hereditary, and Exchange Axioms. Greedy is optimal for ALL weights if and ONLY if $(E, \mathcal{I})$ is a Matroid.
* **Ski-Rental Competitive Ratio**:
  - Online strategy achieves competitive ratio $c = \frac{2P - 1}{P} < 2$ against offline adversary.

```
Master Greedy Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm / Problem   | Sorting Key       | Core Data Structure| Time Complexity  | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Fractional Knapsack**| Density $v_i/w_i$ DESC| Sorted Array  | **$O(N \log N)$ ⚡**| **$O(1)$ Memory ⚡**|
| **Activity Selection**| Finish Time $f_i$ ASC| Sorted Array   | **$O(N \log N)$ ⚡**| **$O(1)$ Memory ⚡**|
| **Job Sequencing**    | Profit $p_i$ DESC | DSU Parent Array  | **$O(N \log N)$ ⚡**| $O(\max D)$ DSU   |
| **Huffman Coding**    | Frequency ASC     | Min-Heap (Priority)| **$O(N \log |\Sigma|)$⚡**| $O(|\Sigma|)$ Tree|
| **Kruskal's MST**     | Edge Weight ASC   | DSU Path Compress | **$O(E \log E)$ ⚡**| $O(V + E)$ DSU    |
| **Prim's MST**        | Outgoing Weight ASC| Min-Heap (Priority)| **$O(E \log V)$ ⚡**| $O(V + E)$ Heap   |
| **Dijkstra's SSSP**   | Tentative Dist ASC| PriorityQueue     | **$O((V+E)\log V)$⚡**| $O(V + E)$ Heap   |
| **Meeting Rooms II**  | Start Time $s_i$ ASC| End Time Min-Heap | **$O(N \log N)$ ⚡**| $O(N)$ Min-Heap   |
| **Task Scheduler**    | Task Frequency    | Frequency Array   | **$O(N)$ Linear ⚡**| $O(26)$ Array     |
| **Coin Change (Canonical)**| Coin Value DESC| Array / Loop      | **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Greedy Regret**     | Max Expense / Len | Max-Heap (Priority)| **$O(N \log N)$ ⚡**| $O(N)$ Max-Heap   |
| **Remove K Digits**   | Digit Value       | Monotone Stack     | **$O(N)$ Linear ⚡**| $O(N)$ Stack      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Greedy Problem / Engine | Purpose | Primary Sorting Key | Operational Complexity | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fractional Knapsack** | Maximize value | Density $v_i / w_i$ DESC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Divisible items |
| **Activity Selection** | Maximize meetings count | Finish Time $f_i$ ASC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Earliest finish time |
| **Job Sequencing** | Maximize job profit | Profit $p_i$ DESC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $O(\max D)$ DSU | DSU latest free slot |
| **Huffman Coding** | Lossless compression | Frequency ASC | $\mathbf{O(N \log |\Sigma|)}$ Log-Linear⚡| $O(|\Sigma|)$ Tree | Merge 2 smallest |
| **Kruskal's MST** | Min Spanning Tree | Edge Weight ASC | $\mathbf{O(E \log E)}$ Log-Linear⚡| $O(V + E)$ DSU | Edge sort + DSU |
| **Prim's MST** | Min Spanning Tree | Outgoing Weight ASC | $\mathbf{O(E \log V)}$ Log-Linear⚡| $O(V + E)$ Heap | Visited cut growing |
| **Dijkstra's SSSP** | Min path non-negative | Tentative Dist ASC | $\mathbf{O((V + E) \log V)}$⚡| $O(V + E)$ Heap | Non-negative edges |
| **Meeting Rooms II** | Min rooms required | Start Time $s_i$ ASC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $O(N)$ Min-Heap | Peak concurrency |
| **SPT Latency Rule** | Min average wait time | Duration $p_i$ ASC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Shortest job first |
| **EDF Lateness Rule**| Min max lateness | Deadline $d_i$ ASC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Earliest deadline |
| **Task Scheduler** | CPU clock cycles | Task Frequency | $\mathbf{O(N)}$ Strict Linear ⚡| $O(26)$ Array | Max frequency frame |
| **Canonical Coins** | Min coins change | Coin Value DESC | $\mathbf{O(N)}$ Strict Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Canonical coins ONLY |
| **Matroid Solver** | Max weight independent | Weight $w(e)$ DESC | $\mathbf{O(N \log N)}$ Log-Linear⚡| $O(N)$ Set | Rado-Edmonds Theorem |
| **Greedy Regret** | Min refuel / Course | Event Order / Duration | $\mathbf{O(N \log N)}$ Log-Linear⚡| $O(N)$ Max-Heap | Retroactive Max-Heap swap |
| **Remove K Digits** | Smallest integer | Digit Order | $\mathbf{O(N)}$ Strict Linear ⚡| $O(N)$ Stack | Monotone Stack |

---

## 4. Architectural System & Library Audit
```
+-----------------------------------------------------------------------------------+
| Production System Greedy Architectures                                            |
+-----------------------------------------------------------------------------------+
| OS CPU Process Schedulers                      : Shortest Processing Time (SPT / SJF) |
| Real-Time Embedded Systems Dispatcher          : Earliest Deadline First (EDF)        |
| Telecommunication & Fiber Optic Cable Networks : Kruskal's / Prim's MST Algorithms |
| GPS Route Satellite Navigation (Google Maps)   : Dijkstra's Shortest Path Engine     |
| Network Intrusion Detection & GZIP Compression : Huffman Coding Min-Heap Trees    |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Fractional Knapsack Density Sorting
> items.sort((a, b) -> Double.compare(b.density, a.density));
> 
> // 2. Activity Selection Earliest Finish Time Sorting
> sorted.sort(Comparator.comparingInt(a -> a.finish));
> 
> // 3. Job Sequencing DSU Path Compression Slot Search
> int slot = dsu.find(job.deadline); if (slot > 0) { slots[slot] = job.id; dsu.union(slot, dsu.find(slot - 1)); }
> 
> // 4. Huffman Min-Heap Iterative Node Merge
> while (minHeap.size() > 1) { HuffmanNode left = minHeap.poll(), right = minHeap.poll(); minHeap.add(new HuffmanNode(left.freq + right.freq, left, right)); }
> 
> // 5. Kruskal DSU Union Loop
> if (dsu.union(edge.src, edge.dest)) { mstEdges.add(edge); totalWeight += edge.weight; }
> 
> // 6. Dijkstra Greedy Relaxation Formula
> if (dist[u] + weight < dist[next]) { dist[next] = dist[u] + weight; minHeap.add(new PathNode(next, dist[next])); }
> 
> // 7. Meeting Rooms II Min-Heap Room Reuse
> if (intervals[i][0] >= roomMinHeap.peek()) roomMinHeap.poll(); roomMinHeap.add(intervals[i][1]);
> 
> // 8. Task Scheduler Frame Formula (LeetCode 621)
> int ans = Math.max(tasks.length, (maxFreq - 1) * (n + 1) + countMaxFreq);
> 
> // 9. Coin Change DP Unbounded Knapsack
> if (amt - coin >= 0) dp[amt] = Math.min(dp[amt], 1 + dp[amt - coin]);
> 
> // 10. Greedy Regret Retroactive Max-Heap Swap (LeetCode 630)
> if (totalTime + duration > lastDay && durationMaxHeap.peek() > duration) totalTime += duration - durationMaxHeap.poll();
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Sorting Intervals by Start Time $s_i$ for Non-Overlapping Count**: Sorting by start time fails when an early interval has a massive duration. **ALWAYS sort by FINISH TIME $f_i$**!
* **Pitfall 2: Applying Greedy Coin Change to Arbitrary Coins**: Greedy coin change fails on non-canonical systems like $\{1, 3, 4\}$ for amount $6$. **ALWAYS use Dynamic Programming for LeetCode 322**!
* **Pitfall 3: Running Dijkstra's Algorithm on Graphs with Negative Edges**: Negative edges break Dijkstra's distance finality assumption. Use **Bellman-Ford Algorithm** ($O(V \cdot E)$)!
* **Pitfall 4: Naive $O(N^2)$ Slot Search in Job Sequencing**: Scanning slots linearly backwards takes $O(N^2)$ time. **ALWAYS use DSU Path Compression** ($O(N \log N)$ total time)!
* **Pitfall 5: Processing Arrival `+1` Before Departure `-1` on Same Timestamp**: Falsely inflates peak concurrency. **ALWAYS process departure `-1` first when timestamps match**!
* **Pitfall 6: Assuming Intuitive Heuristics Are Always Correct**: Applying Greedy without checking Matroid Axioms or Exchange Arguments leads to wrong algorithms. Always verify!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 25 (GREEDY ALGORITHMS)           |
+-----------------------------------------------------------------------+
| 1. Fractional Knapsack : Sort Value Density v_i/w_i DESC -> O(N log N) |
| 2. Activity Selection : Sort Finish Time f_i ASC -> O(N log N)        |
| 3. Job Sequencing DSU : Sort Profit p_i DESC + DSU find(d) -> O(N log N)|
| 4. Huffman Coding     : Min-Heap merge 2 smallest nodes -> O(N log |S|)|
| 5. Kruskal's MST      : Sort edges ASC + DSU cycle check -> O(E log E) |
| 6. Prim's MST         : Min-Heap cut crossing edge -> O(E log V)       |
| 7. Dijkstra's SSSP    : Min-Heap relaxation (Requires w >= 0) -> O((V+E)logV)|
| 8. Meeting Rooms II   : Sort Start Time + End Time Min-Heap -> O(N log N)|
| 9. Task Scheduler     : max(tasks.length, (maxFreq-1)*(n+1) + countMax)|
| 10. Greedy Regret     : Retroactive Max-Heap swap for past choices    |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can state the 2 mathematical conditions required for Greedy correctness (Greedy Choice & Optimal Substructure).
- [ ] I can write Fractional Knapsack using Greedy density sorting in Java.
- [ ] I can write Activity Selection using Earliest Finish Time sorting.
- [ ] I can solve LeetCode 435 (`Non-Overlapping Intervals`).
- [ ] I can write Job Sequencing with DSU Path Compression slot allocation.
- [ ] I can build a Huffman Min-Heap Tree and generate prefix-free bit codes in Java.
- [ ] I can write Kruskal's MST with DSU Path Compression & Rank.
- [ ] I can write Prim's MST using Min-Heap Priority Queue.
- [ ] I can write Dijkstra's Shortest Path Algorithm and explain why it fails on negative edge weights.
- [ ] I can solve LeetCode 253 (`Meeting Rooms II`) using Min-Heap.
- [ ] I can solve LeetCode 621 (`Task Scheduler`) using the bucket formula.
- [ ] I can state why Greedy fails for non-canonical coin systems ($\{1, 3, 4\}$ for amount $6$).
- [ ] I can state the Rado-Edmonds Matroid Theorem.
- [ ] I can write a formal Exchange Argument proof template.
- [ ] I can write a formal Staying Ahead proof template.
- [ ] I can solve LeetCode 871 (`Minimum Refueling Stops`) using Greedy Regret Max-Heap.
- [ ] I can solve LeetCode 402 (`Remove K Digits`) using Monotone Stack.
