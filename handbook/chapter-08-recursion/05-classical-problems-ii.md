# 05. Classical Recursion Problems II: Gray Code, Grid Flood Fill & Flattening Nested Structures

## 1. Introduction
**Classical Recursion Problems II** explores advanced structural and combinatorial recursive patterns that form the direct bridge between basic call stack execution and complex State Space Backtracking. Key classical domains include **Recursive Gray Code Generation (LeetCode 89)** (constructing binary sequences where adjacent values differ by exactly 1 bit), **Grid Flood Fill Engines (LeetCode 733)**, and **Flattening Nested List Data Structures (LeetCode 341)**. Mastering these patterns equips developers to handle non-linear recursive data structures, 2D matrix exploration, and bit-level sequence reflection in **$O(2^N)$** and **$O(M \cdot N)$** time complexities.

> **Important:** Core Invariants of Classical Recursion Problems II:
> 1. **Gray Code Recursive Reflection Principle**: An $N$-bit Gray Code sequence is generated recursively from an $(N-1)$-bit Gray Code sequence by:
>    - Taking the $(N-1)$-bit sequence.
>    - Prefixing `0` to the sequence.
>    - Reversing the $(N-1)$-bit sequence and prefixing `1` (bit-shift `1 << (N-1)`).
> 2. **Grid Flood Fill Invariant (LeetCode 733)**:
>    - Match initial target color `originalColor = image[sr][sc]`.
>    - Fill current cell `image[r][c] = newColor`.
>    - Recurse 4 directions: $(r+1, c), (r-1, c), (r, c+1), (r, c-1)$.
>    - **Safety Guard**: If `originalColor == newColor`, return immediately to avoid infinite recursion! ⚡

```
Gray Code 2-Bit to 3-Bit Recursive Reflection Topography:
2-Bit Sequence:   [00, 01, 11, 10]
Prefix 0:         [000, 001, 011, 010]  (First 4 elements)
Reversed 2-Bit:   [10, 11, 01, 00]
Prefix 1 (100|):  [110, 111, 101, 100]  (Last 4 elements)

Combined 3-Bit Sequence: [000, 001, 011, 010, 110, 111, 101, 100]! (Adjacent elements differ by 1 bit!). ⚡
```

---

## 2. Core Concepts & Classical Problem Strategy Matrix

### 2.1 Problem Strategy Matrix
```
Classical Recursion Problems II Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem               | Primary Strategy  | Base Case Guard   | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Gray Code (89)**    | Binary Reflection | $N = 0 \to [0]$   | **$O(2^N)$ Exponential ⚡**|
| **Flood Fill (733)**  | 2D Grid DFS       | Color Match Guard | **$O(M \cdot N)$ Linear ⚡**|
| **Flatten List (341)**| Deep Traversal    | Leaf Element Check| **$O(N)$ Total Nodes ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Gray Code: Reverse (N-1) bit list and add (1 << N-1)! Flood Fill: Guard against originalColor == newColor!"**

---

## 3. Characteristics & $O(2^N)$ Gray Code Complexity Proof

### 3.1 Mathematical Proof of Gray Code Length $2^N$
* An $N$-bit Gray Code sequence contains $2^N$ unique integers.
* At step $k$, generating the $k$-bit sequence takes double the time of step $k-1$:
  $$T(k) = T(k-1) + O(2^{k-1})$$
* Unfolding the recurrence from $k = 1 \dots N$:
  $$\sum_{k=1}^{N} 2^{k-1} = 2^N - 1 = O(2^N)$$
* Total Time Complexity: $\mathbf{O(2^N) \text{ Exponential Time}}$. Total Space: $\mathbf{O(2^N) \text{ Result Array Memory}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing 2D Grid Flood Fill

The **Flood Fill Engine** starts at seed coordinate `(sr, sc)` with target color `newColor`.

```
Tracing Flood Fill on 3x3 Image (sr = 1, sc = 1, newColor = 2):

Initial Image Matrix:
[ 1, 1, 1 ]
[ 1, 1, 0 ]   originalColor at (1, 1) = 1.
[ 1, 0, 1 ]

DFS(1, 1): image[1][1] = 2.
- Recurse Top (0, 1): image[0][1] = 2.
  - Recurse Left (0, 0): image[0][0] = 2.
    - Neighbors are 2 or out of bounds. Return.
  - Recurse Right (0, 2): image[0][2] = 2.
    - Neighbors are 2 or 0. Return.
- Recurse Bottom (2, 1): image[2][1] = 0 != 1 -> Skip!
- Recurse Left (1, 0): image[1][0] = 2.
  - Recurse Bottom (2, 0): image[2][0] = 2.

Final Filled Image Matrix:
[ 2, 2, 2 ]
[ 2, 2, 0 ]
[ 2, 0, 1 ]

Connected Component Sunk Successfully! ✅ (O(M * N) Time!)
```

---

## 5. Visual Diagram: Gray Code Binary Reflection Sequence

```
Bit Length N = 1:   [0, 1]

Bit Length N = 2:
  Original N=1:     00, 01  (Prefix 0)
  Reversed N=1:     11, 10  (Prefix 1: 10 + [1, 0])
  Combined N=2:     [0, 1, 3, 2]

Bit Length N = 3:
  Original N=2:     000, 001, 011, 010  (Prefix 0)
  Reversed N=2:     110, 111, 101, 100  (Prefix 1: 100 + [2, 3, 1, 0])
  Combined N=3:     [0, 1, 3, 2, 6, 7, 5, 4] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 89 (Gray Code via Reflection), LeetCode 733 (Flood Fill), and a Recursive Nested List Flattener.

```java
import java.util.*;

/**
 * Production-Grade Suite for Classical Recursion Problems II:
 * Gray Code Reflection, 2D Grid Flood Fill, and Nested Structure Flattening.
 */
public class ClassicalProblemsIIMaster {

    // =========================================================================
    // 1. GRAY CODE GENERATION (Recursive Binary Reflection O(2^N))
    // =========================================================================
    /**
     * Generates an n-bit Gray Code sequence recursively using reflection.
     * LeetCode 89 Solution.
     *
     * @param n number of bits (0 <= n <= 16)
     * @return list of integers in Gray Code sequence order
     */
    public List<Integer> grayCode(int n) {
        if (n < 0) return new ArrayList<>();

        // Base Case: 0-bit Gray Code contains only 0
        if (n == 0) {
            List<Integer> base = new ArrayList<>();
            base.add(0);
            return base;
        }

        // Subproblem Reduction: Get (n-1)-bit Gray Code sequence
        List<Integer> prevSequence = grayCode(n - 1);
        List<Integer> result = new ArrayList<>(prevSequence);

        // Reflection Step: Add (1 << (n - 1)) to reversed (n-1)-bit sequence
        int mask = 1 << (n - 1);
        for (int i = prevSequence.size() - 1; i >= 0; i--) {
            result.add(mask | prevSequence.get(i));
        }

        return result;
    }

    // =========================================================================
    // 2. 2D GRID FLOOD FILL ENGINE (LeetCode 733 O(M * N))
    // =========================================================================
    /**
     * Performs flood fill on a 2D image matrix recursively.
     * LeetCode 733 Solution.
     *
     * @param image 2D grid matrix
     * @param sr starting row index
     * @param sc starting column index
     * @param color target replacement color
     * @return updated image matrix
     */
    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        if (image == null || image.length == 0 || image[0].length == 0) return image;

        int originalColor = image[sr][sc];

        // Safety Guard: Avoid infinite recursion when originalColor == color
        if (originalColor != color) {
            dfsFloodFill(image, sr, sc, originalColor, color);
        }

        return image;
    }

    private void dfsFloodFill(int[][] image, int r, int c, int originalColor, int newColor) {
        // Boundary Check & Color Guard
        if (r < 0 || r >= image.length || c < 0 || c >= image[0].length) {
            return;
        }
        if (image[r][c] != originalColor) {
            return;
        }

        // Fill cell with new color
        image[r][c] = newColor;

        // Recurse 4 Orthogonal Directions
        dfsFloodFill(image, r + 1, c, originalColor, newColor);
        dfsFloodFill(image, r - 1, c, originalColor, newColor);
        dfsFloodFill(image, r, c + 1, originalColor, newColor);
        dfsFloodFill(image, r, c - 1, originalColor, newColor);
    }

    // =========================================================================
    // 3. FLATTEN NESTED LIST STRUCTURE (Recursive Tree Flattening)
    // =========================================================================
    /**
     * Interface representing a nested element (either single int or sub-list).
     */
    public interface NestedInteger {
        boolean isInteger();
        Integer getInteger();
        List<NestedInteger> getList();
    }

    /**
     * Flattens a nested list structure recursively into a flat integer list.
     *
     * @param nestedList input nested structure
     * @return flat integer list
     */
    public List<Integer> flattenNestedList(List<NestedInteger> nestedList) {
        List<Integer> result = new ArrayList<>();
        if (nestedList == null) return result;

        flattenHelper(nestedList, result);
        return result;
    }

    private void flattenHelper(List<NestedInteger> list, List<Integer> result) {
        for (NestedInteger item : list) {
            if (item.isInteger()) {
                result.add(item.getInteger());
            } else {
                flattenHelper(item.getList(), result); // Subproblem: Recurse into sub-list
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Gray Code Recursive Reflection Step Line
int mask = 1 << (n - 1);
for (int i = prev.size() - 1; i >= 0; i--) result.add(mask | prev.get(i));
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 89 - Gray Code**:
   - Digital Circuit State Switching Optimization.
   - Rotational Shaft Encoder Angle Measurement.

2. **LeetCode 733 - Flood Fill**:
   - MS Paint Bucket Fill Tool.
   - Image Segmentation & Connected Component Sinking.

3. **LeetCode 341 - Flatten Nested List Iterator**:
   - JSON / XML Document Tree Traversal.
   - Directory Hierarchy File Tree Unrolling.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class ClassicalProblemsIIDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   CLASSICAL RECURSION PROBLEMS II DEMONSTRATION ");
        System.out.println("=================================================\n");

        ClassicalProblemsIIMaster master = new ClassicalProblemsIIMaster();

        // 1. Gray Code Test (N = 3 Bits)
        int bits = 3;
        List<Integer> grayList = master.grayCode(bits);
        System.out.println("1. Gray Code Sequence for " + bits + " Bits:");
        System.out.println("   Integers: " + grayList);
        System.out.print("   Binary  : ");
        for (int val : grayList) {
            String binary = String.format("%" + bits + "s", Integer.toBinaryString(val)).replace(' ', '0');
            System.out.print(binary + " ");
        }
        System.out.println("\n-------------------------------------------------");

        // 2. Flood Fill Test
        int[][] image = {
            {1, 1, 1},
            {1, 1, 0},
            {1, 0, 1}
        };
        System.out.println("2. Original Image Matrix:");
        printMatrix(image);

        int[][] filled = master.floodFill(image, 1, 1, 2);
        System.out.println("   Flood Filled Image (sr=1, sc=1, color=2):");
        printMatrix(filled);
        System.out.println("=================================================");
    }

    private static void printMatrix(int[][] mat) {
        for (int[] row : mat) {
            System.out.println("   " + Arrays.toString(row));
        }
    }
}
```

---

## 9. Complexity Analysis Table

| Classical Problem | Time Complexity | Auxiliary Space | Primary Memory Factor | Key Optimization |
| :--- | :--- | :--- | :--- | :--- |
| **Gray Code (89)** | $\mathbf{O(2^N)}$ Exponential | $\mathbf{O(2^N)}$ Sequence Array| $2^N$ Integer Allocations | Bitwise OR Masking |
| **Flood Fill (733)** | $\mathbf{O(M \cdot N)}$ Linear ⚡ | $\mathbf{O(M \cdot N)}$ Call Stack | Grid Dimension Stack | In-Place Cell Mutation |
| **Flatten Nested List**| $\mathbf{O(K)}$ Total Elements | $\mathbf{O(D)}$ Max Nest Depth | Call Stack Depth $D$ | Lazy Iterator Evaluation |

---

## 10. Edge Cases & Boundary Handling

1. **Flood Fill with `originalColor == newColor`**:
   - Omitting the check `if (originalColor != newColor)` when original and target colors are identical results in infinite recursion and `StackOverflowError`.

2. **Gray Code for $N = 0$**:
   - Handled by returning `[0]` list directly.

3. **Empty Sub-Lists in Nested Lists**:
   - `flattenHelper` handles empty lists `[]` cleanly via standard empty loop skipping.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Reverse Iteration in Gray Code Reflection**:
  ```java
  // BAD: Iterating forward does NOT produce Gray Code!
  for (int i = 0; i < prev.size(); i++) result.add(mask | prev.get(i)); 
  // GOOD: MUST iterate in REVERSE order to ensure 1-bit difference at boundary!
  for (int i = prev.size() - 1; i >= 0; i--) result.add(mask | prev.get(i));
  ```

* **Anti-Pattern 2: Allocating Extra `boolean[][] visited` Arrays in Grid DFS**:
  - In-place mutation `image[r][c] = newColor` serves as the visited mark. Allocating a separate `visited` array wastes $O(M \cdot N)$ extra heap memory.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Gray Code Bitwise Formula:
> While Gray Code can be generated recursively via reflection, it can also be calculated directly in $O(1)$ time for any integer $k$ using the bitwise XOR formula:
> $$G(k) = k \oplus (k \gg 1)$$
> For any sequence index $k$, `k ^ (k >> 1)` produces the exact $k$-th Gray Code integer in constant time! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Recursive Gray Code | Iterative Bitwise Gray Code |
| :--- | :--- | :--- |
| **Time Complexity** | $O(2^N)$ Exponential | **$O(2^N)$ Exponential ⚡** |
| **Auxiliary Memory** | $O(N)$ Call Stack Memory | **$O(1)$ Zero Stack Space ⚡** |
| **Code Length** | ~12 Lines | **~4 Lines (`k ^ (k >> 1)`) ⚡** |

---

## 14. How to Recognize This in Questions

* **"Generate binary sequence where adjacent numbers differ by 1 bit"** $\rightarrow$ Gray Code (LeetCode 89).
* **"Change color of connected region in 2D grid"** $\rightarrow$ Flood Fill (LeetCode 733).
* **"Unroll arbitrary nested lists into flat array"** $\rightarrow$ Recursive Tree Flattening (LeetCode 341).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does the reflection step in Gray Code iterate in reverse order?**  
  *A:* Reversing the $(N-1)$-bit sequence ensures that the last element of the first half and the first element of the second half differ ONLY in the newly added most significant bit ($1 \ll (N-1)$).

* **Q: How does Flood Fill prevent visiting the same cell twice?**  
  *A:* By mutating `image[r][c] = newColor` immediately upon entry. Since the base guard checks `image[r][c] != originalColor`, filled cells are ignored automatically.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: CLASSICAL RECURSION PROBLEMS II                       |
+-----------------------------------------------------------------------+
| • Gray Code Reflection: Take prev(N-1) -> Append prev(N-1) reversed   |
|                         with bitwise OR (1 << (N-1))                  |
| • Gray Code Formula   : G(k) = k ^ (k >> 1) in O(1) time ⚡            |
| • Flood Fill Guard    : if (originalColor == newColor) return;        |
| • Grid DFS Direction  : Recurse (r+1,c), (r-1,c), (r,c+1), (r,c-1)    |
| • Performance         : Gray Code O(2^N) | Flood Fill O(M * N) ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 89 (`Gray Code`) using recursive reflection.
- [ ] I can state and write the $O(1)$ bitwise Gray Code formula `k ^ (k >> 1)`.
- [ ] I can write LeetCode 733 (`Flood Fill`) in Java.
- [ ] I know why `originalColor != color` check is mandatory in Flood Fill.
- [ ] I can write a recursive flattener for nested list data structures.
