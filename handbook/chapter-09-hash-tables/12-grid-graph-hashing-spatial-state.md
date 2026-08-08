# 12. Grid & Graph Hashing (Spatial Coordinate & State Encoding)

## 1. Introduction
Encoding 2D grid coordinates $(r, c)$, 3D spatial points $(x, y, z)$, matrix sub-grid configurations (Sudoku verification - LeetCode 36), game board states (Sudoku Solver, N-Queens, 8-Puzzle BFS state tracking), and graph node pairs into **Unique Integer / String Hash Keys** is a fundamental technical coding interview technique. In graph algorithms and memoized dynamic programming, custom Spatial Coordinate and State Encoding allows using standard Hash Maps and Hash Sets to track visited nodes, memoize sub-problems, and detect cycles in **$O(1)$ constant time**.

> **Important:** Converting 2D coordinates $(r, c)$ into a 1D integer index using **Linear Coordinate Flattening `key = r * COLS + c`** eliminates String object allocations, achieving maximum execution speed and zero garbage collection overhead!

```
Spatial Coordinate Hashing Spectrum:
+-----------------------------------------------------------------------------------+
| String Key Formatting : "r,c" -> String Allocation Overhead -> O(N) GC Memory     |
| Linear Index Mapping  : key = r * COLS + c                  -> O(1) Primitive Int ⚡|
| Bitwise 64-bit Packing: key = ((long) r << 32) | c           -> O(1) Primitive Long⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Encoding Formulas

### 2.1 2D Coordinate Linear Flattening
For a 2D grid matrix of dimension $\text{ROWS} \times \text{COLS}$, any coordinate $(r, c)$ where $0 \le r < \text{ROWS}$ and $0 \le c < \text{COLS}$ maps to a unique 1D integer index:

$$\text{Key}_{1D} = r \cdot \text{COLS} + c$$

#### Decoding 1D Index back to 2D Coordinates $(r, c)$:
$$r = \lfloor \frac{\text{Key}_{1D}}{\text{COLS}} \rfloor \quad \text{and} \quad c = \text{Key}_{1D} \pmod{\text{COLS}}$$

### 2.2 Bitwise 64-Bit Packing (Zero Collision, Infinite Bounds)
When grid dimensions are dynamic or large (e.g. $r, c \in [-10^9, 10^9]$), Linear Flattening overflows 32-bit integers.
We can pack 32-bit signed row $r$ and 32-bit signed column $c$ into a single 64-bit `long` primitive:

$$\text{PackedKey} = ((r \text{ as unsigned 32-bit long}) \ll 32) \ \vert \ (c \text{ as unsigned 32-bit long})$$

In Java syntax:
```java
long key = (((long) r) << 32) | (c & 0xFFFFFFFFL);
```
* **Advantage**: Zero hash collisions, zero object allocations, handles positive and negative coordinates seamlessly!

### 2.3 3x3 Sudoku Sub-Grid Encoding (LeetCode 36)
In Valid Sudoku (LeetCode 36), a $9 \times 9$ board is partitioned into nine $3 \times 3$ sub-grids.
The sub-grid index for cell $(r, c)$ is computed as:

$$\text{SubGridIndex} = \left\lfloor \frac{r}{3} \right\rfloor \cdot 3 + \left\lfloor \frac{c}{3} \right\rfloor$$

```
Sudoku 3x3 Sub-Grid Index Layout (0..8):
+-------+-------+-------+
|  0    |  1    |  2    |  (Rows 0..2)
+-------+-------+-------+
|  3    |  4    |  5    |  (Rows 3..5)
+-------+-------+-------+
|  6    |  7    |  8    |  (Rows 6..8)
+-------+-------+-------+
 Cols 0..2 Cols 3..5 Cols 6..8
```

> **Memory Trick:** **"2D Flattening: r * COLS + c! Bitwise Packing: (((long) r) << 32) | (c & 0xFFFFFFFFL)! Sudoku Box: (r / 3) * 3 + (c / 3)!"**

---

## 3. Characteristics & State Canonical Serialization

### 3.1 Board State Serialization for BFS / DP Memoization
In puzzle solving (e.g. 8-Puzzle, Slidings Puzzle LeetCode 773), BFS must track visited board configurations to prevent infinite loops.
* **Matrix State to Canonical String**: Convert $2 \times 3$ board `[[1,2,3],[4,0,5]]` to string key `"123405"`.
* **State Hash Set**: Use `Set<String> visited = new HashSet<>()` to store string representations of board states.

---

## 4. Internal Working Mechanics
Tracing Valid Sudoku (LeetCode 36) Bitmask / Hash Mapping:

```
Cell (r=4, c=7), Value = '5'

1. Row Check    : Check rows[4] for bit (1 << 5).
2. Column Check : Check cols[7] for bit (1 << 5).
3. SubGrid Check: Box Index = (4 / 3) * 3 + (7 / 3) = 1 * 3 + 2 = 5!
                  Check boxes[5] for bit (1 << 5).

If bit (1 << 5) exists in any set/bitmask -> INVALID SUDOKU! ❌
Else set bit (1 << 5) in rows[4], cols[7], and boxes[5]. ✅
```

---

## 5. Visual Diagram
Bitwise 64-Bit Coordinate Packing & Sudoku 3x3 Sub-Grid Index Layout:

```
[ BITWISE 64-BIT PACKING OF (r=5, c=12) ]
Row 5  (32-bit): 0000 0000 0000 0000 0000 0000 0000 0101
Col 12 (32-bit): 0000 0000 0000 0000 0000 0000 0000 1100

Shift Row Left 32 bits:
High 32 bits: 0000 0000 0000 0000 0000 0000 0000 0101
Low 32 bits : 0000 0000 0000 0000 0000 0000 0000 0000

Bitwise OR with Col 12:
Packed Long : 0000 0000 0000 0000 0000 0000 0000 0101  0000 0000 0000 0000 0000 0000 0000 1100
              |-------------------------------------| |-------------------------------------|
                            High 32 (Row)                           Low 32 (Col)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Valid Sudoku (LeetCode 36), Sliding Puzzle BFS State Hashing (LeetCode 773), and Spatial Coordinate Bitwise Packing:

```java
import java.util.*;

public class GridGraphHashingMaster {

    // 1. Valid Sudoku (LeetCode 36) using Bitmask Arrays O(1) Time, O(1) Space
    public static boolean isValidSudoku(char[][] board) {
        int[] rows = new int[9];
        int[] cols = new int[9];
        int[] boxes = new int[9];

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char val = board[r][c];
                if (val == '.') continue;

                int num = val - '1'; // 0..8
                int bit = 1 << num;
                int boxIndex = (r / 3) * 3 + (c / 3);

                // Bitwise AND check if number already exists
                if ((rows[r] & bit) != 0 || (cols[c] & bit) != 0 || (boxes[boxIndex] & bit) != 0) {
                    return false;
                }

                // Bitwise OR to record number presence
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[boxIndex] |= bit;
            }
        }

        return true;
    }

    // 2. Spatial Coordinate 64-bit Bitwise Packing Helper
    public static class CoordinatePacker {
        public static long pack(int row, int col) {
            return (((long) row) << 32) | (col & 0xFFFFFFFFL);
        }

        public static int unpackRow(long packed) {
            return (int) (packed >> 32);
        }

        public static int unpackCol(long packed) {
            return (int) packed;
        }
    }

    // 3. Sliding Puzzle BFS State Hashing (LeetCode 773) O(6! * 6) Time, O(6!) Space
    public static int slidingPuzzle(int[][] board) {
        String target = "123450";
        StringBuilder sb = new StringBuilder();
        for (int r = 0; r < 2; r++) {
            for (int c = 0; c < 3; c++) {
                sb.append(board[r][c]);
            }
        }
        String startState = sb.toString();

        // Neighbor adjacency for 2x3 grid flattened 1D indices 0..5
        int[][] swapMoves = {
            {1, 3},       // 0 moves to 1, 3
            {0, 2, 4},    // 1 moves to 0, 2, 4
            {1, 5},       // 2 moves to 1, 5
            {0, 4},       // 3 moves to 0, 4
            {1, 3, 5},    // 4 moves to 1, 3, 5
            {2, 4}        // 5 moves to 2, 4
        };

        Queue<String> queue = new ArrayDeque<>();
        Set<String> visited = new HashSet<>();

        queue.offer(startState);
        visited.add(startState);
        int steps = 0;

        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                String curr = queue.poll();
                if (curr.equals(target)) return steps;

                int zeroIdx = curr.indexOf('0');
                for (int nextIdx : swapMoves[zeroIdx]) {
                    String nextState = swapString(curr, zeroIdx, nextIdx);
                    if (!visited.contains(nextState)) {
                        visited.add(nextState);
                        queue.offer(nextState);
                    }
                }
            }
            steps++;
        }

        return -1;
    }

    private static String swapString(String str, int i, int j) {
        char[] ca = str.toCharArray();
        char temp = ca[i];
        ca[i] = ca[j];
        ca[j] = temp;
        return new String(ca);
    }
}
```

> **Quick Syntax:**
```java
// 64-Bit Coordinate Packing Syntax
long packedKey = (((long) row) << 32) | (col & 0xFFFFFFFFL);
int row = (int) (packedKey >> 32);
int col = (int) packedKey;
```

---

## 7. Concrete Problem Examples
* **LeetCode 36 - Valid Sudoku**: Sub-grid $3 \times 3$ coordinate hashing.
* **LeetCode 773 - Sliding Puzzle**: BFS state string serialization.
* **LeetCode 149 - Max Points on a Line**: Slope $dY/dX$ fraction reduction hashing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Valid Sudoku, 64-bit Coordinate Packing, and Sliding Puzzle BFS:

```java
public class GridGraphHashingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing 64-Bit Coordinate Packing ===");
        int r = -42, c = 105;
        long packed = GridGraphHashingMaster.CoordinatePacker.pack(r, c);
        int unpackedR = GridGraphHashingMaster.CoordinatePacker.unpackRow(packed);
        int unpackedC = GridGraphHashingMaster.CoordinatePacker.unpackCol(packed);

        System.out.println("Original: (" + r + ", " + c + ")");
        System.out.println("Packed Key Long: " + packed);
        System.out.println("Unpacked: (" + unpackedR + ", " + unpackedC + ") -> MATCHES: " + (r == unpackedR && c == unpackedC));

        System.out.println("\n=== 2. Testing Sliding Puzzle BFS State Hashing ===");
        int[][] puzzle = {{1, 2, 3}, {4, 0, 5}};
        System.out.println("Min Steps to Solve [[1,2,3],[4,0,5]]: " + GridGraphHashingMaster.slidingPuzzle(puzzle)); // Output: 1 step
    }
}
```

---

## 9. Complexity Analysis

| Encoding Strategy | Compression Time | Memory Footprint | Key Factor |
| :--- | :--- | :--- | :--- |
| **Linear Index `r*COLS + c`**| **Strict $O(1)$ ⚡** | **$O(1)$ Primitive `int`**| Bounded grid dimensions |
| **64-bit Packing `(r<<32)\|c`**| **Strict $O(1)$ ⚡** | **$O(1)$ Primitive `long`**| Unlimited 32-bit grid coordinates |
| **Bitmask Arrays (`int[9]`)** | **Strict $O(1)$ ⚡** | **$O(1)$ Stack Space** | Fast bitwise AND/OR operations |
| **State String ("123405")** | $O(L)$ String Alloc | $O(L)$ Heap Memory | Useful for BFS visited sets |

---

## 10. Edge Cases & Boundary Handling
* **Negative Coordinate Packing**: In Java, right shifting a negative signed int extends the sign bit. When bitwise ORing with `c`, `c & 0xFFFFFFFFL` MUST be masked with `0xFFFFFFFFL` long literal to prevent negative sign bit corruption!
* **Fractional Slopes for Lines (LeetCode 149)**: Floating point slopes (`dY / dX`) suffer from IEEE 754 precision rounding errors! Store slopes as **Reduced Pair Fractions `(dY / GCD, dX / GCD)`** as string keys `"dY/dX"`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using String Format `"r,c"` inside Hot BFS Loops**: Creating thousands of `"10,20"` string objects per second stresses the Java Garbage Collector! Use `long` packing or `int` linear indexing.
* **Floating Point Slope Hashing**: Using `double slope = (double) dy / dx` as a Hash Map key leads to precision bug failures due to `0.1 + 0.2 != 0.3`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Line Slope Encoding Rule (LeetCode 149):
> NEVER use floating point division `(double) dy / dx` as a Hash Map key!
> Always reduce slope fractions by their **Greatest Common Divisor (GCD)**:
> `int g = gcd(dy, dx); String slopeKey = (dy / g) + "/" + (dx / g);`

> **Memory Trick:** **"Never use double slope keys! Reduce dy and dx by gcd(dy, dx) and format as dy/dx!"**

---

## 13. System & Implementation Comparisons

| Feature | String Formatting `"r,c"` | Linear Index `r*COLS+c` | Bitwise 64-Bit Packing |
| :--- | :--- | :--- | :--- |
| **Execution Speed** | Slow (GC Object Heap) | **Blazing Fast ⚡** | **Blazing Fast ⚡** |
| **Grid Boundary** | Unlimited | Must know `COLS` | Unlimited 32-bit range |
| **Primitive Type** | Object `String` | Primitive `int` | Primitive `long` |

---

## 14. How to Recognize This in Questions
* **"Check if a 9x9 Sudoku board is valid"** $\rightarrow$ Bitmask arrays for rows, cols, and 3x3 boxes (`(r/3)*3 + (c/3)`).
* **"Find min moves to solve sliding puzzle board"** $\rightarrow$ Board State String Serialization BFS.

---

## 15. Frequently Asked Interview Questions
* **Q: How does `(r / 3) * 3 + (c / 3)` calculate the 3x3 box index in Sudoku?**  
  *A:* Integer division `r / 3` groups rows 0..2 to 0, 3..5 to 1, and 6..8 to 2. Multiplying by 3 scales this to box row offsets 0, 3, 6. Adding `c / 3` (which evaluates to 0, 1, 2) offsets to the exact box index from 0 to 8.
* **Q: Why is bitwise `rows[r] & (1 << num)` faster than `HashSet<Character>` for Sudoku?**  
  *A:* A bitmask array of size 9 uses 36 bytes of stack memory and checks presence in a single CPU clock cycle via bitwise AND (`&`), whereas 27 `HashSet` instances allocate thousands of bytes on the heap and require object hashing.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRID & GRAPH HASHING                                  |
+-----------------------------------------------------------------------+
| • 2D Linear Index: key = r * COLS + c (Decode: r = key/COLS, c = key%COLS)|
| • 64-Bit Bitwise Packing: long key = (((long) r) << 32) | (c & 0xFFFFFFFFL);|
| • Sudoku 3x3 Box Index: boxIndex = (r / 3) * 3 + (c / 3)              |
| • Sudoku Bitmask: rows[r] & (1 << num) checks presence in 1 CPU cycle  |
| • Slope Key (Line 149): Never use double! Use (dy/gcd) + "/" + (dx/gcd)|
| • State Serialization: Format board as string "123405" for BFS visited|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 2D linear flattening `r * COLS + c` and its decoding math.
- [ ] I can write 64-bit coordinate bitwise packing `(((long)r)<<32) | (c & 0xFFFFFFFFL)`.
- [ ] I can derive the Sudoku box index formula `(r / 3) * 3 + (c / 3)`.
- [ ] I can implement Valid Sudoku (LeetCode 36) using bitmask arrays.
- [ ] I know why GCD fraction reduction is mandatory for slope hashing.
- [ ] I can implement Sliding Puzzle (LeetCode 773) state serialization BFS.
