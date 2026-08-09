# 10. Histogram Area Problems, Monotonic Boundary Sweeping & 2D Grid Reductions

## 1. Introduction
**Histogram Area Problems** represent the most celebrated advanced applications of Monotonic Stacks in technical interviews. By maintaining a **Monotonic Increasing Stack** of bar indices, algorithms like **Largest Rectangle in Histogram (LeetCode 84)**, **Maximal Rectangle (LeetCode 85)**, and **Trapping Rain Water (LeetCode 42 - Stack Variant)** solve complex geometric area calculations in **$O(N)$ linear time and $O(N)$ space**, reducing cubic $O(N^3)$ brute-force sub-array area calculations down to optimal single passes.

> **Important:** In **Largest Rectangle in Histogram (LeetCode 84)**, when a bar at index $i$ is smaller than the bar at `stack.peek()`, popping `heights[stack.pop()]` reveals its exact left and right boundaries:
> * **Height**: $H = \text{heights}[\text{popped}]$
> * **Right Boundary**: $R = i$ (First index to the right with smaller height).
> * **Left Boundary**: $L = \text{stack.isEmpty()} ? -1 : \text{stack.peek()}$ (First index to the left with smaller height).
> * **Width**: $W = R - L - 1$.
> * **Area**: $\text{Area} = H \times (R - L - 1)$!

```
Monotonic Stack Histogram Area Calculation Topology:
+-----------------------------------------------------------------------------------+
| Popped Bar Height : H = heights[popped]                                           |
| Left Boundary L   : stack.peek() (if empty, L = -1)                                 |
| Right Boundary R  : Current index i                                               |
| Rectangle Width W : R - L - 1                                                     |
| Rectangle Area    : H * (R - L - 1)  (Calculated in O(1) time per popped bar!) ⚡  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Histogram Area Mechanics (LeetCode 84)

### 2.1 Largest Rectangle in Histogram (LeetCode 84)
Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram:

#### Monotonic Increasing Stack Algorithm ($O(N)$ Time, $O(N)$ Space):
1. Create index stack `Deque<Integer> stack = new ArrayDeque<>()`.
2. `maxArea = 0`, $N = \text{heights.length}$.
3. Iterate index `i` from `0` to $N$ (Using virtual index $N$ with height `0` to flush remaining elements!):
   - `currHeight = (i == N) ? 0 : heights[i]`.
   - While `!stack.isEmpty() && heights[stack.peek()] >= currHeight`:
     - `h = heights[stack.pop()]`.
     - `w = stack.isEmpty() ? i : i - stack.peek() - 1`.
     - `area = h * w`.
     - `maxArea = Math.max(maxArea, area)`.
   - `stack.push(i)`.
4. Return `maxArea`.

```
Virtual Sentinel Height 0 at Index N:
Adding a virtual bar of height 0 at index N guarantees that any elements remaining in the stack
at the end of the array traversal are popped and evaluated against the full array right boundary N! ⚡
```

> **Memory Trick:** **"Largest Rectangle Histogram: Monotonic Increasing Stack! When h[stack.peek()] >= curr, pop! h = popped, w = stack.isEmpty() ? i : i - stack.peek() - 1!"**

---

## 3. Characteristics & 2D Maximal Rectangle (LeetCode 85)

### 3.1 Maximal Rectangle (LeetCode 85 - 2D Grid Reduction)
Given a 2D binary matrix filled with `'0'`s and `'1'`s, find the largest rectangle containing only `'1'`s:

#### Reduction to 1D Histogram Problem ($O(R \cdot C)$ Time, $O(C)$ Auxiliary Space):
* Treat each row in the 2D matrix as the base of a 1D Histogram!
* Maintain a 1D histogram array `int[] heights = new int[C]`.
* For row `r = 0` to $R - 1$:
  - For column `c = 0` to $C - 1$:
    - If `matrix[r][c] == '1'`, `heights[c] += 1` (Accumulate height!).
    - Else, `heights[c] = 0` (Reset height!).
  - Run **LeetCode 84 `largestRectangleArea(heights)`** on current row histogram!
  - `maxRectangle = Math.max(maxRectangle, rowMaxArea)`.
* Return `maxRectangle`.

---

## 4. Internal Working Mechanics
Tracing Largest Rectangle in Histogram (LeetCode 84) on `heights = [2, 1, 5, 6, 2, 3]`:

```
i = 0 (h 2): stack = [0(2)]
i = 1 (h 1): 2 >= 1 -> Pop 0(h=2). stack empty -> w = 1. Area = 2 * 1 = 2. maxArea = 2. Push 1(1). stack = [1(1)]
i = 2 (h 5): 5 > 1 -> Push 2(5). stack = [1(1), 2(5)]
i = 3 (h 6): 6 > 5 -> Push 3(6). stack = [1(1), 2(5), 3(6)]
i = 4 (h 2):
  - Pop 3(h=6). stack.peek() = 2. w = 4 - 2 - 1 = 1. Area = 6 * 1 = 6. maxArea = max(2, 6) = 6.
  - Pop 2(h=5). stack.peek() = 1. w = 4 - 1 - 1 = 2. Area = 5 * 2 = 10. maxArea = max(6, 10) = 10!
  - Push 4(2). stack = [1(1), 4(2)]
i = 5 (h 3): Push 5(3). stack = [1(1), 4(2), 5(3)]
i = 6 (Virtual h=0):
  - Pop 5(h=3). stack.peek() = 4. w = 6 - 4 - 1 = 1. Area = 3 * 1 = 3.
  - Pop 4(h=2). stack.peek() = 1. w = 6 - 1 - 1 = 4. Area = 2 * 4 = 8.
  - Pop 1(h=1). stack empty. w = 6. Area = 1 * 6 = 6.

Maximal Rectangle Area = 10 ✅ (O(N) Time, O(N) Space!)
```

---

## 5. Visual Diagram
Largest Rectangle Histogram Boundary Expansion Topography:

```
Heights:   2     1     5     6     2     3
                      +-----+-----+
                      |  5  |  6  |  (Height H = 5, Width W = 2)
                      +-----+-----+
                      |  5  |  6  |  Maximal Area = 5 * 2 = 10! ✅
                      +-----+-----+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Largest Rectangle in Histogram (LeetCode 84) and Maximal Rectangle (LeetCode 85):

```java
import java.util.*;

public class HistogramAreaMaster {

    // 1. Largest Rectangle in Histogram (LeetCode 84) O(N) Time, O(N) Space
    public static int largestRectangleArea(int[] heights) {
        if (heights == null || heights.length == 0) return 0;

        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;

        // Iterate to index n (virtual sentinel height 0)
        for (int i = 0; i <= n; i++) {
            int currentHeight = (i == n) ? 0 : heights[i];

            while (!stack.isEmpty() && heights[stack.peek()] >= currentHeight) {
                int h = heights[stack.pop()];
                int w = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, h * w);
            }

            stack.push(i);
        }

        return maxArea;
    }

    // 2. Maximal Rectangle in 2D Binary Matrix (LeetCode 85) O(R * C) Time, O(C) Auxiliary Space
    public static int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return 0;

        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxRectangle = 0;

        for (int r = 0; r < rows; r++) {
            // Update 1D histogram heights for current row base
            for (int c = 0; c < cols; c++) {
                if (matrix[r][c] == '1') {
                    heights[c] += 1;
                } else {
                    heights[c] = 0; // Reset height on '0'
                }
            }

            // Calculate max histogram area for current row
            int rowMaxArea = largestRectangleArea(heights);
            maxRectangle = Math.max(maxRectangle, rowMaxArea);
        }

        return maxRectangle;
    }
}
```

> **Quick Syntax:**
```java
// Histogram Area Calculation Line
int h = heights[stack.pop()];
int w = stack.isEmpty() ? i : i - stack.peek() - 1;
maxArea = Math.max(maxArea, h * w);
```

---

## 7. Concrete Problem Examples
* **LeetCode 84 - Largest Rectangle in Histogram**: Core 1D histogram area.
* **LeetCode 85 - Maximal Rectangle**: 2D grid matrix reduction to 1D histogram.
* **LeetCode 42 - Trapping Rain Water**: Monotonic stack horizontal water trapping.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Largest Rectangle in Histogram and 2D Maximal Rectangle:

```java
public class HistogramAreaDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Largest Rectangle in Histogram (LeetCode 84) ===");
        int[] heights = {2, 1, 5, 6, 2, 3};
        int maxHistArea = HistogramAreaMaster.largestRectangleArea(heights);
        System.out.println("Max Histogram Area: " + maxHistArea); // Output: 10

        System.out.println("\n=== 2. Maximal Rectangle in 2D Matrix (LeetCode 85) ===");
        char[][] matrix = {
            {'1', '0', '1', '0', '0'},
            {'1', '0', '1', '1', '1'},
            {'1', '1', '1', '1', '1'},
            {'1', '0', '0', '1', '0'}
        };
        int maxRect2D = HistogramAreaMaster.maximalRectangle(matrix);
        System.out.println("Maximal 2D Rectangle Area: " + maxRect2D); // Output: 6
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Histogram Area (84)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Monotonic increasing stack |
| **Maximal Rectangle (85)**| **$O(R \cdot C)$ Linear ⚡**| $O(C)$ Aux Array | 2D matrix reduction to 1D histogram |

---

## 10. Edge Cases & Boundary Handling
* **All Heights Equal (`[2, 2, 2, 2]`)**: Processed cleanly by virtual index $N$ flush; returns $2 \times 4 = 8$.
* **Strictly Increasing Heights (`[1, 2, 3, 4]`)**: All elements pushed onto stack; virtual index $N$ pops all bars sequentially.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Virtual Sentinel Height 0 at Index $N$**:
  - Omitting index $N$ flush leaves elements remaining in the stack, missing rectangles extended to the extreme right edge!
  - **Loop up to `i <= N` with `currHeight = (i == N) ? 0 : heights[i]`**.
* **Incorrect Width Calculation When Stack is Empty**:
  - Writing `w = i - stack.peek()` when stack is empty causes `EmptyStackException`.
  - **Use ternary `w = stack.isEmpty() ? i : i - stack.peek() - 1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `w = stack.isEmpty() ? i : i - stack.peek() - 1` Works:
> If the stack is EMPTY after popping bar $H$, it means bar $H$ was the SMALLEST bar encountered so far.
> Therefore, a rectangle of height $H$ can extend all the way from index 0 to index $i - 1$, spanning a total width of exactly **`i`**!

> **Memory Trick:** **"If stack is empty after pop, width W is simply current index i!"**

---

## 13. System & Implementation Comparisons

| Feature | Monotonic Stack Histogram Algorithm | Brute-Force Subarray Min Height |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N^3)$ or $O(N^2)$ Quadratic |
| **Auxiliary Memory** | $O(N)$ Stack Space | $O(1)$ |
| **2D Matrix Adaptation**| Enables $O(R \cdot C)$ Maximal Rect | Requires $O(R^3 \cdot C^3)$ Brute-Force |

---

## 14. How to Recognize This in Questions
* **"Find largest rectangle area in 1D histogram"** $\rightarrow$ LeetCode 84 (Monotonic Increasing Stack).
* **"Find largest rectangle containing only 1s in 2D binary matrix"** $\rightarrow$ LeetCode 85 (Row-by-row 1D histogram reduction).

---

## 15. Frequently Asked Interview Questions
* **Q: How does LeetCode 85 reduce 2D matrix maximal rectangle to 1D histogram?**  
  *A:* By treating each row of the matrix as the base of a histogram. Running LeetCode 84 on each row's cumulative height array evaluates all candidate rectangles in $R \times O(C) = \mathbf{O(R \cdot C)\text{ Time}}$.
* **Q: Why MUST a Monotonic INCREASING stack be used in Largest Rectangle in Histogram?**  
  *A:* Because bars in increasing order can extend further to the right. When a shorter bar is encountered, it limits the right boundary of all taller bars in the stack, triggering area calculations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HISTOGRAM AREA PROBLEMS & 2D MATRIX REDUCTION         |
+-----------------------------------------------------------------------+
| • Histogram Stack Type: Monotonic INCREASING stack storing indices    |
| • Sentinel Virtual Flush: Loop up to i <= N with currHeight 0 at i=N  |
| • Height Formula: h = heights[stack.pop()]                            |
| • Width Formula: w = stack.isEmpty() ? i : i - stack.peek() - 1       |
| • Maximal Rect (85): heights[c] += 1 on '1', reset to 0 on '0'        |
| • Time Complexity: O(N) for 84 | O(R * C) for 85 ⚡                     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Largest Rectangle in Histogram (LeetCode 84) in under 5 minutes.
- [ ] I know why virtual index $N$ sentinel is required.
- [ ] I can derive the width formula `w = stack.isEmpty() ? i : i - stack.peek() - 1`.
- [ ] I can solve Maximal Rectangle in 2D Matrix (LeetCode 85).
- [ ] I can explain how row-by-row histogram updates work.
