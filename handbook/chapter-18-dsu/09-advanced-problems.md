# 09. Advanced DSU Problems: Longest Consecutive Sequence & Swim in Rising Water

## 1. Introduction
**Advanced DSU Problems** push the limits of set partitioning by combining DSU with **Value Offset Hash Tables**, **Grid Water-Level Binary Search**, and **Character Index Grouping**. Problems like **Longest Consecutive Sequence (LeetCode 128)**, **Swim in Rising Water (LeetCode 778)**, and **Smallest String With Swaps (LeetCode 1202)** execute in **$O(N \cdot \alpha(N)) \approx O(N)$ Near-Linear Time** by leveraging DSU to group contiguous numbers and graph paths without running slow sorting or Dijkstra algorithms.

> **Important:** Why DSU Solves Longest Consecutive Sequence in $O(N)$ Time (LeetCode 128):
> 1. **Value Mapping**: Put all numbers in a `Map<Integer, Integer> numToId` mapping each number to a 0-indexed ID.
> 2. **Adjacent Union Invariant**: For each number `num` in input array:
>    - Check if `num + 1` exists in map. If yes: `dsu.union(num, num + 1)`.
>    - Check if `num - 1` exists in map. If yes: `dsu.union(num, num - 1)`.
> 3. **Size Query**: Find `max(dsu.getComponentSize(x))` across all numbers in **$O(N)$ Strict Linear Time**! ⚡

```
LeetCode 128 Longest Consecutive Sequence DSU Topology:
Input = [100, 4, 200, 1, 3, 2]

Processing:
- Number 1: Neighbor 2 exists -> union(1, 2)
- Number 2: Neighbor 3 exists -> union(2, 3)
- Number 3: Neighbor 4 exists -> union(3, 4)

Resulting Component: Set {1, 2, 3, 4} (Component Size = 4!)
Max Consecutive Sequence Length = 4! ⚡
```

---

## 2. Core Concepts & LeetCode 778 Swim in Rising Water Architecture

### 2.1 LeetCode 778 Swim in Rising Water DSU Algorithm
Given an $N \times N$ grid of water elevations: find minimum time $T$ to swim from top-left `(0, 0)` to bottom-right `(N-1, N-1)`:
1. Collect all grid cells `(r, c, grid[r][c])` and sort by elevation ascending ($O(N^2 \log N)$).
2. Initialize DSU for $N^2$ cells.
3. Mark grid cells as active one by one in ascending order of elevation $T$:
   - For cell `(r, c)` at elevation $T$:
     - Check 4 orthogonal active neighbors. Call `dsu.union(r * N + c, nr * N + nc)`.
     - Check if `dsu.connected(0, N*N - 1)` is TRUE!
     - **If connected**: Return current elevation $T$ immediately! ⚡

```
Advanced DSU Problem Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Consecutive (128)** | Neighbor Offsets  | **$O(N \cdot \alpha(N)) \approx O(N)$ ⚡**| $O(N)$ Hash Map   |
| **Swim Water (778)**  | Sort Elevation+DSU| **$O(N^2 \log N)$ ⚡**| $O(N^2)$ DSU Array|
| **String Swaps (1202)**| Index Group Sort | **$O(N \log N)$ ⚡**| $O(N)$ DSU Array  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 128: Map num to ID -> Union num with num+1 and num-1 -> Max size is answer!"**

---

## 3. Characteristics & Smallest String With Swaps (LeetCode 1202)

### 3.1 Smallest String With Swaps (LeetCode 1202)
Given string `s` and pairs of indices that can be swapped:
* **Insight**: Swappable index pairs form connected components. Characters within any component can be arranged in ANY lexicographical order!
* **Algorithm**:
  - `dsu.union(u, v)` for all swap pairs.
  - Group characters by component root ID.
  - Sort characters within each component.
  - Re-assign sorted characters back to original indices in **$O(N \log N)$ Time**.

---

## 4. Internal Working Mechanics
Tracing Swim in Rising Water (LeetCode 778) on $2 \times 2$ Grid `[[0, 2], [1, 3]]`:

```
Grid Size 2x2. Goal: Connect Cell 0 (0,0) to Cell 3 (1,1).

Cells sorted by elevation:
- T = 0: Cell (0, 0) active.
- T = 1: Cell (1, 0) active. Neighbor (0,0) active -> union((1,0), (0,0)).
  - Component { (0,0), (1,0) }. Connected to (1,1)? False.
- T = 2: Cell (0, 1) active. Neighbor (0,0) active -> union((0,1), (0,0)).
- T = 3: Cell (1, 1) active. Neighbors (0,1) and (1,0) active -> union((1,1), (0,1)).
  - Check connected(0, 3) -> TRUE!

Time T = 3 is the minimum required swim time! ✅ (O(N^2 log N) Time!)
```

---

## 5. Visual Diagram
LeetCode 778 Water Level Union Topography:

```
Water Level T = 3:
   (0,0) [T=0] ---- (0,1) [T=2]
     |                 |
   (1,0) [T=1] ---- (1,1) [T=3]

Path (0,0) -> (1,0) -> (1,1) connected at T = 3! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 128 (Longest Consecutive Sequence) and LeetCode 778 (Swim in Rising Water) using DSU:

```java
import java.util.*;

// LeetCode 128 & LeetCode 778 Advanced DSU Solutions
public class AdvancedDSUProblemsMaster {

    // 1. LeetCode 128: Longest Consecutive Sequence O(N) Time
    public static class LongestConsecutiveDSU {
        private final int[] parent;
        private final int[] size;

        public LongestConsecutiveDSU(int n) {
            this.parent = new int[n];
            this.size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1;
            }
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]);
        }

        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX != rootY) {
                if (size[rootX] < size[rootY]) {
                    parent[rootX] = rootY;
                    size[rootY] += size[rootX];
                } else {
                    parent[rootY] = rootX;
                    size[rootX] += size[rootY];
                }
            }
        }

        public int getComponentSize(int i) {
            return size[find(i)];
        }
    }

    public int longestConsecutive(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int n = nums.length;
        Map<Integer, Integer> numToId = new HashMap<>();
        LongestConsecutiveDSU dsu = new LongestConsecutiveDSU(n);

        // Step 1: Map unique numbers to 0-indexed IDs
        for (int i = 0; i < n; i++) {
            if (numToId.containsKey(nums[i])) continue; // Skip duplicates
            numToId.put(nums[i], i);
        }

        // Step 2: Union consecutive neighbors (num - 1 and num + 1)
        for (int num : numToId.keySet()) {
            int currentId = numToId.get(num);

            if (numToId.containsKey(num + 1)) {
                dsu.union(currentId, numToId.get(num + 1));
            }
            if (numToId.containsKey(num - 1)) {
                dsu.union(currentId, numToId.get(num - 1));
            }
        }

        // Step 3: Find maximum component size
        int maxConsecutive = 0;
        for (int num : numToId.keySet()) {
            maxConsecutive = Math.max(maxConsecutive, dsu.getComponentSize(numToId.get(num)));
        }

        return maxConsecutive;
    }

    // 2. LeetCode 778: Swim in Rising Water O(N^2 log N) Time
    public int swimInWater(int[][] grid) {
        int n = grid.length;
        int totalCells = n * n;

        List<int[]> cells = new ArrayList<>();
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                cells.add(new int[]{r, c, grid[r][c]});
            }
        }

        // Sort cells by water elevation ascending
        cells.sort(Comparator.comparingInt(a -> a[2]));

        LongestConsecutiveDSU dsu = new LongestConsecutiveDSU(totalCells);
        boolean[][] active = new boolean[n][n];

        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        for (int[] cell : cells) {
            int r = cell[0];
            int c = cell[1];
            int time = cell[2];
            active[r][c] = true;

            int currentId = r * n + c;

            // Check 4 active orthogonal neighbors
            for (int[] d : dirs) {
                int nr = r + d[0];
                int nc = c + d[1];

                if (nr >= 0 && nr < n && nc >= 0 && nc < n && active[nr][nc]) {
                    int neighborId = nr * n + nc;
                    dsu.union(currentId, neighborId);
                }
            }

            // Check if top-left (0) is connected to bottom-right (n*n - 1)
            if (dsu.find(0) == dsu.find(totalCells - 1)) {
                return time; // Minimum swim time reached!
            }
        }

        return 0;
    }
}
```

> **Quick Syntax:**
```java
// LeetCode 128 Neighbor Union Check Line
if (numToId.containsKey(num + 1)) dsu.union(numToId.get(num), numToId.get(num + 1));
```

---

## 7. Concrete Problem Examples
* **LeetCode 128 - Longest Consecutive Sequence**: Core DSU problem.
* **LeetCode 778 - Swim in Rising Water**: Grid elevation DSU.
* **LeetCode 1202 - Smallest String With Swaps**: Connected index component sorting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 128 `longestConsecutive`:

```java
public class AdvancedDSUProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 128 Longest Consecutive Sequence Test ===");
        AdvancedDSUProblemsMaster solver = new AdvancedDSUProblemsMaster();

        int[] nums = {100, 4, 200, 1, 3, 2};
        int longest = solver.longestConsecutive(nums);

        System.out.println("Input Array: " + Arrays.toString(nums));
        System.out.println("Longest Consecutive Sequence Length: " + longest); 
        // Output: 4 (Sequence {1, 2, 3, 4}) ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Consecutive Sequence (128)**| **$O(N \cdot \alpha(N)) \approx O(N)$ ⚡**| **$O(N)$ Hash Map Space**| DSU neighbor union |
| **Swim in Water (778)** | **$O(N^2 \log N)$ Optimal ⚡**| **$O(N^2)$ DSU Array** | Elevation sorting + DSU union |
| **String Swaps (1202)** | **$O(N \log N)$ Optimal ⚡**| **$O(N)$ DSU Array** | Component character sorting |

---

## 10. Edge Cases & Boundary Handling
* **Single Element Array (`[100]`)**: `longestConsecutive` returns `1`.
* **Grid Size $1 \times 1$ (`[[0]]`)**: `swimInWater` returns `0` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Sorting Input Array for LeetCode 128**:
  - Sorting takes $O(N \log N)$ time, violating the $O(N)$ time complexity constraint.
  - **Use DSU with Hash Map lookup to solve in strict $O(N)$ linear time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why DSU Achieves $O(N)$ Time for LeetCode 128:
> Checking `containsKey(num + 1)` and `containsKey(num - 1)` takes $O(1)$ time per element.
> DSU `union` and `getComponentSize` execute in $\alpha(N) \approx O(1)$ near-constant time.
> Total time across $N$ elements is strictly **$O(N)$ Linear Time**, outperforming $O(N \log N)$ sorting! ⚡

> **Memory Trick:** **"Hash Map lookup + DSU union = O(N) linear time for consecutive sequence!"**

---

## 13. System & Implementation Comparisons

| Feature | LeetCode 128 DSU Solution | $O(N \log N)$ Sorting Solution |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \cdot \alpha(N)) \approx O(N)$ Strict ⚡**| $O(N \log N)$ Sorting Penalty ❌ |
| **Dynamic Capability**| **Supports dynamic stream inserts ⚡**| Requires full re-sorting |
| **Component Size Query**| **$O(1)$ Constant Time ⚡** | $O(N)$ Scan |

---

## 14. How to Recognize This in Questions
* **"Find length of longest consecutive elements sequence in O(N) time"** $\rightarrow$ LeetCode 128 (DSU).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is DSU better than Dijkstra for LeetCode 778 (Swim in Rising Water)?**  
  *A:* Because sorting grid cells by elevation upfront and performing DSU dynamic unions is easier to code and achieves $O(N^2 \log N)$ time with lower constant factors.
* **Q: How does LeetCode 1202 (Smallest String With Swaps) use DSU?**  
  *A:* By grouping indices connected via swap pairs into DSU components, then sorting characters independently within each component.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED DSU PROBLEMS (LEETCODE 128 & 778)            |
+-----------------------------------------------------------------------+
| • LeetCode 128 : Map num -> ID; union(num, num+1); return max size (O(N))|
| • LeetCode 778 : Sort grid cells by elevation; activate & union 4-neighbors|
|                  Return elevation T as soon as (0) connects to (N^2 - 1)|
| • LeetCode 1202: Union swap pairs; sort characters per DSU component  |
| • Performance  : $O(N)$ Linear Time for LeetCode 128! ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 128 (`Longest Consecutive Sequence`) in $O(N)$ time.
- [ ] I can write LeetCode 778 (`Swim in Rising Water`) using DSU.
- [ ] I can write LeetCode 1202 (`Smallest String With Swaps`).
- [ ] I know why DSU outperforms sorting for LeetCode 128.
- [ ] I can trace dynamic grid connectivity step by step.
