# 05. Histogram Area & Trapping Rain Water Algorithms

## 1. Introduction
Calculating the largest rectangle area in a histogram (LeetCode 84) and computing total trapped rain water (LeetCode 42 - Trapping Rain Water, LeetCode 85 - Maximal Rectangle) are benchmark hard technical coding interview problems. These problems evaluate **Monotonic Stack** range boundary computation, where element indices on the stack demarcate left and right boundaries in **$O(N)$ linear time and $O(N)$ space**.

> **Important:** In Largest Rectangle in Histogram, when an index `i` is popped from a **Monotonic Increasing Stack**, its height is `heights[popped]`, its right boundary is `i`, and its left boundary is `stack.peek()`! The width is **`width = i - stack.peek() - 1`**!

## 2. Core Concepts
* **Largest Rectangle in Histogram (LeetCode 84)**:
  * Maintain a **Monotonic Increasing Stack** of bar indices.
  * When current height `heights[i]` is strictly smaller than `heights[stack.peek()]`, pop the top bar index `h = heights[stack.pop()]`.
  * The width of the rectangle with height `h` is:
    $$\text{width} = \begin{cases} i & \text{if stack is empty} \\ i - \text{stack.peek()} - 1 & \text{if stack non-empty} \end{cases}$$
  * Calculate $\text{area} = h \cdot \text{width}$ and update `maxArea`.
* **Trapping Rain Water (LeetCode 42 - Monotonic Stack Approach)**:
  * Maintain a **Monotonic Decreasing Stack** of indices.
  * When `height[i] > height[stack.peek()]`, pop bounded bottom index `bottom = stack.pop()`.
  * If stack is non-empty, left wall is `left = stack.peek()`, right wall is `right = i`.
  * Trapped water depth $= \min(\text{height}[left], \text{height}[right]) - \text{height}[bottom]$; width $= i - left - 1$.

> **Memory Trick:** **"Histogram Width Formula: width = stack.isEmpty() ? i : (i - stack.peek() - 1)"**.

## 3. Characteristics / Properties
* **Dummy Sentinel Heights**: Adding a dummy height `0` at index $N$ forces the histogram stack to pop all remaining bars, processing all potential rectangles before loop exit without extra code duplication!
* **$O(N)$ Time Guarantee**: Every bar index enters and leaves the stack at most once.

```
Histogram & Water Trapping Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Application | Stack Monotonicity| Pop Formula       | Key Result        |
+-----------------------+-------------------+-------------------+-------------------+
| Histogram Max Area    | Increasing        | `h * (i - peek - 1)`| Max Rectangle Area⚡|
| Trapping Rain Water   | Decreasing        | `(min(L,R)-bot)*(i-L-1)`| Total Water Volume⚡|
| Maximal 2D Rectangle  | Increasing per row| Row DP + Histogram| Max 2D Matrix Area|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Largest Rectangle in Histogram on `[2, 1, 5, 6, 2, 3]`:

```
Array with Dummy Sentinel: [2, 1, 5, 6, 2, 3, 0]

i=0 (2): Push 0 | Stack: [0]
i=1 (1): 1 < heights[0](2) -> Pop 0 (h=2, width=1 -> area=2). Push 1 | Stack: [1]
i=2 (5): Push 2 | Stack: [1, 2]
i=3 (6): Push 3 | Stack: [1, 2, 3]
i=4 (2):
  - 2 < heights[3](6) -> Pop 3 (h=6, width=4-2-1=1 -> area=6)
  - 2 < heights[2](5) -> Pop 2 (h=5, width=4-1-1=2 -> area=10 🎉 MAX!)
  - Push 4 | Stack: [1, 4]
i=5 (3): Push 5 | Stack: [1, 4, 5]
i=6 (0 - Sentinel): Pops remaining bars (5, 4, 1).

Max Area Found: 10 ✅ (Correct!)
```

## 5. Visual Diagram
Histogram Rectangle Width Boundary Mechanics:

```
Histogram Heights: [ 2, 1, 5, 6, 2, 3 ]
                           +---+
                           | 6 |
                       +---+---+
                       | 5 |   |
                       +---+---+---+
                       |   | 2 | 3 |
                   +---+---+---+---+
                   | 2 | 1 |   |   |
                   +---+---+---+---+
Index:               0   1   2   3   4   5

When popping index 3 (height 6) at i=4:
- Right Boundary: i = 4
- Left Boundary: stack.peek() = 2 (index of bar height 5)
- Width = 4 - 2 - 1 = 1. Area = 6 * 1 = 6.
```

## 6. Operations / Algorithms
LeetCode 84 & LeetCode 42 Master Implementation:

```java
// 1. Largest Rectangle in Histogram (LeetCode 84) O(N) Time, O(N) Space
public int largestRectangleArea(int[] heights) {
    int n = heights.length;
    Deque<Integer> stack = new ArrayDeque<>();
    int maxArea = 0;

    for (int i = 0; i <= n; i++) {
        // Dummy sentinel height 0 at index n
        int currentHeight = (i == n) ? 0 : heights[i];

        while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
            int h = heights[stack.pop()];
            int w = stack.isEmpty() ? i : (i - stack.peek() - 1);
            maxArea = Math.max(maxArea, h * w);
        }
        stack.push(i);
    }

    return maxArea;
}

// 2. Trapping Rain Water (LeetCode 42 - Stack Approach) O(N) Time, O(N) Space
public int trap(int[] height) {
    Deque<Integer> stack = new ArrayDeque<>(); // Monotonic Decreasing
    int water = 0;

    for (int i = 0; i < height.length; i++) {
        while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
            int bottom = stack.pop();
            if (stack.isEmpty()) break; // No left boundary wall

            int left = stack.peek();
            int boundedHeight = Math.min(height[left], height[i]) - height[bottom];
            int distance = i - left - 1;

            water += boundedHeight * distance;
        }
        stack.push(i);
    }

    return water;
}
```

> **Quick Syntax:**
```java
// Histogram Width Boundary Check
int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
```

## 7. Examples
* **LeetCode 84 - Largest Rectangle in Histogram**: Monotonic Increasing Stack area calculation.
* **LeetCode 42 - Trapping Rain Water**: Monotonic Decreasing Stack volume calculation.
* **LeetCode 85 - Maximal Rectangle**: 2D binary matrix largest rectangle using Histogram DP per row.

## 8. Java Code
Complete interview-ready Java suite implementing Histogram Max Area, Trapping Rain Water, and 2D Matrix Maximal Rectangle (LeetCode 85):

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class HistogramWaterTrappingMaster {

    // 1. Largest Rectangle in Histogram (LeetCode 84) O(N) Time, O(N) Space
    public static int largestRectangleArea(int[] heights) {
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;

        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && h < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : (i - stack.peek() - 1);
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }

        return maxArea;
    }

    // 2. Maximal Rectangle in 2D Binary Matrix (LeetCode 85) O(R * C) Time, O(C) Space
    public static int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) return 0;

        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;

        for (char[] row : matrix) {
            // Build histogram for current row
            for (int j = 0; j < cols; j++) {
                heights[j] = (row[j] == '1') ? heights[j] + 1 : 0;
            }
            // Run Histogram Max Area on current row
            maxArea = Math.max(maxArea, largestRectangleArea(heights));
        }

        return maxArea;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] histogram = {2, 1, 5, 6, 2, 3};
        System.out.println("Largest Histogram Area: " + largestRectangleArea(histogram)); // Output: 10

        char[][] matrix = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        System.out.println("Maximal 2D Matrix Rectangle: " + maximalRectangle(matrix)); // Output: 6
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Histogram Max Area** | **$O(N)$ Linear** | $O(N)$ Stack Space | Monotonic Increasing Stack |
| **Trapping Rain Water** | **$O(N)$ Linear** | $O(N)$ Stack Space | Monotonic Decreasing Stack |
| **Maximal 2D Rectangle** | **$O(R \cdot C)$** | $O(C)$ Column Array | Row Histogram DP + Stack |

## 10. Edge Cases
* **Histogram with Monotonically Increasing Heights (e.g. `[1, 2, 3, 4]`)**: Handled seamlessly by dummy sentinel `0` at index $N$, popping all bars cleanly.
* **Empty Matrix / Zero Width Histogram**: Return `0` immediately.
* **Single Column / Single Row Matrix**: Heights array DP handles single dimensions smoothly.

## 11. Common Mistakes
* Calculating width as `i - stack.peek()` instead of **`i - stack.peek() - 1`** (overcounts width by 1 bar!).
* Forgetting to add dummy sentinel height `0` at index $n$ in Histogram Max Area (leaves un-popped elements on stack!).
* For Trapping Rain Water stack, forgetting to check `if (stack.isEmpty()) break;` after popping `bottom` (causes `EmptyStackException` when no left wall exists).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Histogram Width Formula Rule:
> After popping top height `heights[stack.pop()]`:
> * If stack is EMPTY $\implies$ `width = i`
> * If stack is NON-EMPTY $\implies$ **`width = i - stack.peek() - 1`**
> Always write: `int w = stack.isEmpty() ? i : (i - stack.peek() - 1);`

> **Memory Trick:** **"Width is ALWAYS (i - stack.peek() - 1) when stack is non-empty!"**

## 13. Comparisons
| Feature | 2-Pointer Trapping Rain Water | Monotonic Stack Trapping Rain Water |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Auxiliary Space** | **$O(1)$ Constant ⚡** | $O(N)$ Stack Memory |
| **Code Simplicity** | Two pointers `left` & `right` | Horizontal water layer popping |
| **Interview Choice** | **Optimal Space** | Optimal Multi-Problem Pattern |

## 14. How to Recognize This in Questions
* **"Find largest rectangular area in bar chart"** $\rightarrow$ Histogram Monotonic Increasing Stack (LeetCode 84).
* **"Calculate total volume of water trapped after raining"** $\rightarrow$ Trapping Rain Water (LeetCode 42).
* **"Find largest sub-rectangle of 1s in binary matrix"** $\rightarrow$ Row DP + Histogram Stack (LeetCode 85).

## 15. Frequently Asked Interview Questions
* **Q: Why is dummy height `0` at index $N$ necessary for Histogram Max Area?**  
  *A:* Without the dummy sentinel `0`, an increasing sequence like `[1, 2, 3, 4]` remains on the stack when the loop finishes. The sentinel `0` forces the `while` loop to pop every single remaining bar and calculate its maximal area before exiting.
* **Q: How does LeetCode 85 (Maximal Rectangle) reuse the Histogram algorithm?**  
  *A:* It converts each matrix row into a histogram heights array where `heights[j]` represents the number of consecutive `1`s ending at `(row, j)`. Running the $O(C)$ Histogram algorithm on each row takes $O(R \cdot C)$ total time.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HISTOGRAM AREA & TRAPPING RAIN WATER                  |
+-----------------------------------------------------------------------+
| • Histogram Rule: Loop i from 0 to N with sentinel h=(i==N ? 0 : heights[i])|
| • Pop Condition: while (!stack.isEmpty() && h < heights[stack.peek()]) |
| • Width Formula: width = stack.isEmpty() ? i : (i - stack.peek() - 1) |
| • Trapping Water Rule: Water += (min(L, R) - bottom) * (i - left - 1) |
| • Maximal 2D Matrix: Row DP + Histogram Max Area                      |
| • Complexity: O(N) Linear Time | O(N) Stack Space                     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the `width = stack.isEmpty() ? i : (i - stack.peek() - 1)` formula from memory.
- [ ] I know why dummy sentinel height `0` at index $N$ is required.
- [ ] I can implement Largest Rectangle in Histogram (LeetCode 84) in under 5 minutes.
- [ ] I can implement Trapping Rain Water (LeetCode 42) using a Monotonic Stack.
- [ ] I can solve Maximal Rectangle in 2D Matrix (LeetCode 85) using Row DP + Histogram.
