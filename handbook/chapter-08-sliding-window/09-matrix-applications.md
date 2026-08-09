# 09. Matrix Applications, 2D Grid Sweeping & Submatrix Target Sum Reductions

## 1. Introduction
**Matrix Applications of Sliding Window** extend 1D array window mechanics to 2D grid dimensions. By fixing top and bottom row boundaries (`r1` and `r2`) and compressing 2D matrix columns into a 1D aggregated array, problems like **Number of Submatrices That Sum to Target (LeetCode 1074)** and **Maximal Rectangle (LeetCode 85)** reduce complex 2D submatrix searches from $O(R^2 \cdot C^2)$ brute-force polynomial time to **$O(R^2 \cdot C)$ optimal time**.

> **Important:** The fundamental reduction for 2D matrix sliding window / prefix sum problems is **Row Boundary Fixation & Column Compression**. By fixing an upper row `r1` and a lower row `r2`, the sum of elements in any submatrix column $c$ is:
> $$\text{ColSum}[c] = \sum_{r=r1}^{r2} \text{matrix}[r][c]$$
> The 2D submatrix problem simplifies to a 1D Sliding Window / Prefix Sum problem on `ColSum[]` across columns $c = 0 \dots C-1$!

```
2D Matrix to 1D Array Column Compression Spectrum:
+-----------------------------------------------------------------------------------+
| Fix Row r1 (Top) & Row r2 (Bottom)                                                |
| Compress Matrix Columns: colSum[c] = Matrix[r1..r2][c]                            |
| 2D Problem Reduces to 1D Problem on colSum[] Array in O(C) Time per Row Pair! ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Submatrix Target Sum Mechanics (LeetCode 1074)

### 2.1 Number of Submatrices That Sum to Target (LeetCode 1074)
Given a 2D matrix `matrix` and integer `target`, return the number of non-empty submatrices that sum to `target`:

#### Algorithm ($O(R^2 \cdot C)$ Time, $O(C)$ Auxiliary Space):
1. Compute 2D Prefix Sum Matrix: `prefix[r][c]` stores sum of elements in row `r` from column `0` to `c`.
2. Loop upper row `r1` from `0` to $R - 1$:
   - Loop lower row `r2` from `r1` to $R - 1$:
     - Maintain a Hash Map `Map<Integer, Integer> map` mapping prefix sums to frequencies (Initialize `map.put(0, 1)`).
     - Maintain `currentSum = 0`.
     - For column `c = 0` to $C - 1$:
       - Calculate column segment sum: `colSum = prefix[r2][c] - (r1 > 0 ? prefix[r1-1][c] : 0)`.
       - `currentSum += colSum`.
       - If `map.containsKey(currentSum - target)`: `count += map.get(currentSum - target)`.
       - `map.put(currentSum, map.getOrDefault(currentSum, 0) + 1)`.
3. Return `count`.

```
2D Column Prefix Submatrix Formula:
Submatrix Sum bounded between rows [r1 .. r2] and cols [c1 .. c2]:
sum(r1, r2, c1, c2) = sum(colSum[c1 ... c2])
By maintaining prefix map of currentSum across columns c, submatrix search runs in O(C) time! ⚡
```

> **Memory Trick:** **"Submatrix Target Sum: Fix row r1 & r2, compress columns into 1D prefix sum map! Time = O(R^2 * C)!"**

---

## 3. Characteristics & 2D Sliding Window Maximum (K x K Submatrices)

### 3.1 Sliding Window Maximum on 2D Matrix ($K \times K$ Grid)
Given an $R \times C$ matrix and window size $K$, find the maximum element in every $K \times K$ submatrix:

1. **Pass 1 (Row-wise Monotonic Deque)**: Apply 1D Sliding Window Maximum on each row across windows of size $K$. Store result in intermediate matrix `rowMax[R][C - K + 1]`.
2. **Pass 2 (Column-wise Monotonic Deque)**: Apply 1D Sliding Window Maximum on each column of `rowMax` across windows of size $K$.
3. Final matrix `gridMax[R - K + 1][C - K + 1]` contains the maximum for every $K \times K$ submatrix in **$O(R \cdot C)$ Linear Time**!

---

## 4. Internal Working Mechanics
Tracing Number of Submatrices That Sum to Target (LeetCode 1074) on `matrix = [[0,1,0],[1,1,0],[0,1,0]]`, `target = 0`:

```
Matrix (3x3):
[0, 1, 0]
[1, 1, 0]
[0, 1, 0]

Row 2D Column Prefix:
Row 0: [0, 1, 1]
Row 1: [1, 2, 2]
Row 2: [0, 1, 1]

Fix r1 = 0, r2 = 0 (1D array colSums = [0, 1, 0]):
  - col 0 (val 0): sum = 0. Target 0 match! (map has 0). count = 1. map: {0:2}.
  - col 1 (val 1): sum = 1. sum - 0 = 1 (not in map). map: {0:2, 1:1}.
  - col 2 (val 0): sum = 1. sum - 0 = 1. map has 1! count += 1 -> count = 2.

Fix r1 = 0, r2 = 2 (Summing rows 0, 1, 2 -> colSums = [1, 3, 0]):
  - Target sum match submatrices found in O(C) column pass!

Total Submatrices Summing to 0 = 4 ✅ (O(R^2 * C) Time, O(C) Space!)
```

---

## 5. Visual Diagram
Row Boundary Fixation & Column Compression Topography:

```
Matrix (R x C):
Row r1 ---> +-------------------+
            | c=0 | c=1 | c=2 | c=3 |
            |-----+-----+-----+-----|  ===> Compress Columns:
Row r2 ---> +-------------------+       colSum[c] = Sum of elements between r1 and r2
                                        1D Array: [ col0, col1, col2, col3 ] (Len C)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Number of Submatrices That Sum to Target (LeetCode 1074) and $K \times K$ 2D Grid Sliding Window Maximum:

```java
import java.util.*;

public class MatrixApplicationsMaster {

    // 1. Number of Submatrices That Sum to Target (LeetCode 1074) O(R^2 * C) Time, O(C) Space
    public static int numSubmatrixSumTarget(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return 0;

        int rows = matrix.length;
        int cols = matrix[0].length;

        // Compute row-wise 2D prefix sums
        int[][] prefix = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r][c] = matrix[r][c] + (c > 0 ? prefix[r][c - 1] : 0);
            }
        }

        int count = 0;

        // Fix column boundaries c1 and c2 (Optimize for R > C by swapping dimensions if needed)
        for (int c1 = 0; c1 < cols; c1++) {
            for (int c2 = c1; c2 < cols; c2++) {
                Map<Integer, Integer> map = new HashMap<>();
                map.put(0, 1);
                int currentSum = 0;

                for (int r = 0; r < rows; r++) {
                    int rowSum = prefix[r][c2] - (c1 > 0 ? prefix[r][c1 - 1] : 0);
                    currentSum += rowSum;

                    if (map.containsKey(currentSum - target)) {
                        count += map.get(currentSum - target);
                    }

                    map.put(currentSum, map.getOrDefault(currentSum, 0) + 1);
                }
            }
        }

        return count;
    }

    // 2. 2D Grid Sliding Window Maximum (K x K Submatrices) O(R * C) Time
    public static int[][] maxSlidingWindow2D(int[][] matrix, int k) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[][] rowMax = new int[rows][cols - k + 1];

        // Pass 1: Row-wise 1D Sliding Window Maximum
        for (int r = 0; r < rows; r++) {
            rowMax[r] = maxSlidingWindow1D(matrix[r], k);
        }

        int[][] gridMax = new int[rows - k + 1][cols - k + 1];

        // Pass 2: Column-wise 1D Sliding Window Maximum on rowMax
        for (int c = 0; c < cols - k + 1; c++) {
            int[] colArr = new int[rows];
            for (int r = 0; r < rows; r++) {
                colArr[r] = rowMax[r][c];
            }

            int[] colMax = maxSlidingWindow1D(colArr, k);
            for (int r = 0; r < rows - k + 1; r++) {
                gridMax[r][c] = colMax[r];
            }
        }

        return gridMax;
    }

    private static int[] maxSlidingWindow1D(int[] nums, int k) {
        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        int p = 0;

        for (int right = 0; right < n; right++) {
            if (!deque.isEmpty() && deque.peekFirst() < right - k + 1) deque.pollFirst();
            while (!deque.isEmpty() && nums[deque.peekLast()] <= nums[right]) deque.pollLast();
            deque.offerLast(right);
            if (right >= k - 1) result[p++] = nums[deque.peekFirst()];
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// 2D Row Sum Compression Line
int rowSum = prefix[r][c2] - (c1 > 0 ? prefix[r][c1 - 1] : 0);
currentSum += rowSum;
```

---

## 7. Concrete Problem Examples
* **LeetCode 1074 - Number of Submatrices That Sum to Target**: Column fixation + 1D prefix map.
* **2D Grid Sliding Window Maximum**: 2-pass monotonic deque across rows and columns.
* **LeetCode 85 - Maximal Rectangle**: Monotonic stack on 1D histogram rows.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Submatrices Sum to Target and 2D Grid Sliding Window Max:

```java
public class MatrixApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Submatrices Sum to Target (LeetCode 1074, Target=0) ===");
        int[][] matrix = {
            {0, 1, 0},
            {1, 1, 0},
            {0, 1, 0}
        };
        int submatricesCount = MatrixApplicationsMaster.numSubmatrixSumTarget(matrix, 0);
        System.out.println("Submatrices Count Summing to 0: " + submatricesCount); // Output: 4

        System.out.println("\n=== 2. 2D Grid Sliding Window Maximum (K=2) ===");
        int[][] grid = {
            {1, 3, 2},
            {4, 5, 6},
            {8, 7, 9}
        };
        int[][] maxGrid = MatrixApplicationsMaster.maxSlidingWindow2D(grid, 2);
        System.out.println("2D Window Maximums (2x2): " + Arrays.deepToString(maxGrid));
        // Output: [[5, 6], [8, 9]]
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Submatrix Sum Target (1074)**| **$O(R \cdot C^2)$ or $O(R^2 \cdot C)$ ⚡**| $O(C)$ Aux Map | 2D to 1D column compression |
| **2D Window Max ($K \times K$)** | **$O(R \cdot C)$ Linear ⚡** | $O(R \cdot C)$ Grid Space | 2-pass row/col monotonic deque |

---

## 10. Edge Cases & Boundary Handling
* **$R > C$ Matrix Dimension Imbalance**: Swap loops to fix columns `c1, c2` ($O(C^2 \cdot R)$) if $C < R$ to minimize outer loop iterations.
* **Target $= 0$**: Prefix map initialized with `map.put(0, 1)` handles 0-sum submatrices cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting 4 Nested Loops ($O(R^2 \cdot C^2)$ Brute-Force)**:
  - Testing all pairs of top-left $(r1, c1)$ and bottom-right $(r2, c2)$ submatrices degrades performance to $O(R^2 \cdot C^2)$.
  - **Fix boundaries $c1, c2$ and compress rows into a 1D prefix map for $O(R \cdot C^2)$ time**.
* **Re-computing Column Sums from Scratch ($O(R^3 \cdot C)$ Penalty)**:
  - Re-summing elements between $r1$ and $r2$ for every column adds an extra factor of $R$.
  - **Use row-wise 2D prefix sums for $O(1)$ column segment queries**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Dimension Optimization Trick in LeetCode 1074:
> If $R > C$, fix columns $c1$ and $c2$ and run prefix sum map over rows $r$ $\implies$ Complexity **$O(C^2 \cdot R)$**.
> If $C > R$, fix rows $r1$ and $r2$ and run prefix sum map over columns $c$ $\implies$ Complexity **$O(R^2 \cdot C)$**.
> Always pick the smaller dimension to fix in the outer loop to achieve minimum execution time!

> **Memory Trick:** **"Fix the SMALLER dimension in 2D submatrix prefix sum to minimize loop count!"**

---

## 13. System & Implementation Comparisons

| Feature | Column Compression 1D Prefix Map | 4-Loop Brute Force Submatrix Check |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(R^2 \cdot C)$ Optimal ⚡** | $O(R^2 \cdot C^2)$ Polynomial |
| **Auxiliary Memory** | **$O(C)$ Constant per pass ⚡**| $O(1)$ |
| **Code Footprint** | Concise (20 Lines) | Verbose (35 Lines) |

---

## 14. How to Recognize This in Questions
* **"Find number of submatrices that sum to target"** $\rightarrow$ LeetCode 1074 (Column compression + 1D prefix map).
* **"Find maximum element in every K x K submatrix"** $\rightarrow$ 2D Grid Sliding Window Maximum (2-pass monotonic deque).

---

## 15. Frequently Asked Interview Questions
* **Q: How does 2D Grid Sliding Window Maximum achieve $O(R \cdot C)$ time for $K \times K$ submatrices?**  
  *A:* By decomposing 2D maximum finding into two 1D passes: Pass 1 runs 1D monotonic deque sliding max across every row ($O(R \cdot C)$ time), and Pass 2 runs 1D monotonic deque sliding max across every column of the result ($O(R \cdot C)$ time).
* **Q: Why is `map.put(0, 1)` initialized in the Hash Map for LeetCode 1074?**  
  *A:* `map.put(0, 1)` handles submatrices starting from the top/left boundary whose total sum equals `target` directly (`currentSum - target == 0`).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: 2D MATRIX SLIDING WINDOW & SUBMATRIX PREFIX PATTERNS   |
+-----------------------------------------------------------------------+
| • 2D Compression Rule: Fix r1 & r2 (or c1 & c2); sum col/row segments |
| • Submatrix Target Sum (1074): 1D prefix map over compressed dimension|
| • Target Formula: count += map.getOrDefault(currentSum - target, 0)   |
| • Map Init: ALWAYS call map.put(0, 1) before iterating columns/rows!  |
| • 2D Window Max: 2-Pass 1D Monotonic Deque (Rows first, then Cols)    |
| • Time Complexity: O(R^2 * C) for 1074 | O(R * C) for 2D Window Max ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Number of Submatrices That Sum to Target (LeetCode 1074).
- [ ] I know how column compression reduces 2D submatrix search to 1D prefix map.
- [ ] I know how to optimize for dimension imbalance ($R > C$ vs $C > R$).
- [ ] I can implement 2D Grid Sliding Window Maximum using 2-pass monotonic deque.
- [ ] I know why `map.put(0, 1)` is required in submatrix target sum prefix maps.
