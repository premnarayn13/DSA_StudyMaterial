# 02. Memory Representation & Cache Locality of Arrays

## 1. Introduction
At the hardware level, an array's efficiency is rooted entirely in its contiguous physical memory allocation and CPU cache alignment. In technical interviews, explaining how 1D and 2D arrays are laid out in physical RAM, computing Row-Major and Column-Major address mapping formulas, and demonstrating CPU Spatial Cache Locality distinguishes top-tier engineers.

> **Important:** In Java, 2D arrays (`int[][]`) are NOT allocated as a single continuous 2D matrix in memory. They are implemented as **Arrays of Arrays** (an array of reference pointers pointing to independent 1D heap arrays), which can lead to CPU cache misses if traversed incorrectly!

## 2. Core Concepts
* **Row-Major Order**: Storing array elements row by row sequentially in contiguous RAM addresses. Used by C, C++, and standard 1D linearizations of 2D grids.
* **Column-Major Order**: Storing array elements column by column sequentially in memory. Used by Fortran and MATLAB.
* **CPU Cache Line**: The minimum block of memory transferred between main RAM and CPU L1/L2/L3 caches (typically **64 bytes**).
* **Spatial Locality**: Principle stating that accessing memory address $A$ makes accessing nearby addresses $A+4, A+8$ extremely fast because they are pre-loaded into the CPU Cache Line.

> **Memory Trick:** **"Row-Outer, Col-Inner = Cache Winner ⚡"**. Always iterate through 2D matrices using `for (int r = 0) for (int c = 0)` in Java to access elements sequentially in memory!

## 3. Characteristics / Properties
* **Java Array Memory Layout (64-bit JVM)**:
  * **Mark Word**: 8 bytes (locking, GC metadata).
  * **Klass Word**: 4 bytes (compressed OOP reference to class metadata).
  * **Array Length**: 4 bytes (`int` storing length).
  * **Padding**: 0 to 4 bytes (aligns object to 8-byte boundary).
  * **Total Base Overhead**: **16 to 24 bytes** before storing any element data!

```
JVM 64-bit Memory Layout for int[5]:
+------------------+------------------+------------------+------------------+-----------------------+
| Mark Word (8B)   | Klass Word (4B)  | Length = 5 (4B)  | Data: 5 x 4B int | Padding (0B)          |
+------------------+------------------+------------------+------------------+-----------------------+
| <---------------- Total Array Object Header (16 Bytes) ---------------->| Total Size = 36 Bytes |
```

## 4. Internal Working
Row-Major vs Column-Major Address Formula Derivation:

Given a 2D matrix of dimensions $R \times C$ (Rows $\times$ Columns) starting at Base Address $B$, where each element consumes $S$ bytes:

### 1. Row-Major Mapping Formula (0-indexed `matrix[r][c]`):
$$\text{Address}(\text{matrix}[r][c]) = B + (r \times C + c) \times S$$

### 2. Column-Major Mapping Formula (0-indexed `matrix[r][c]`):
$$\text{Address}(\text{matrix}[r][c]) = B + (c \times R + r) \times S$$

```
Row-Major Storage (Row 0, then Row 1, then Row 2):
+-------------------+-------------------+-------------------+
| Row 0 (Cols 0..2) | Row 1 (Cols 0..2) | Row 2 (Cols 0..2) |
+-------------------+-------------------+-------------------+
Address: 100 104 108   112 116 120   124 128 132

Column-Major Storage (Col 0, then Col 1, then Col 2):
+-------------------+-------------------+-------------------+
| Col 0 (Rows 0..2) | Col 1 (Rows 0..2) | Col 2 (Rows 0..2) |
+-------------------+-------------------+-------------------+
```

## 5. Visual Diagram
Java "Array of Arrays" Memory Structure (`int[3][3]`):

```
Heap Memory Layout for int[][] matrix = new int[3][3]:

Matrix Reference (Stack)
       |
       v
+------------------+
| Header (16 Bytes)|
| Ref to Row 0  ----------------> [ int[] Row 0: Val0, Val1, Val2 ] @ Addr 0x500
| Ref to Row 1  ----------------> [ int[] Row 1: Val0, Val1, Val2 ] @ Addr 0x820
| Ref to Row 2  ----------------> [ int[] Row 2: Val0, Val1, Val2 ] @ Addr 0x104
+------------------+
  (Outer Array)                     (Independent Heap 1D Array Allocations)
```

## 6. Operations / Algorithms
Optimizing Matrix Traversal for CPU Cache Locality:

```java
// Cache-Friendly Traversal (Row-Major Order)
// Reads contiguous memory addresses -> 1 Cache Miss per 16 ints (64-byte line / 4B int)
for (int r = 0; r < R; r++) {
    for (int c = 0; c < C; c++) {
        sum += matrix[r][c]; // FAST! ⚡
    }
}

// Cache-Unfriendly Traversal (Column-Major Order in Java)
// Jumps across independent arrays -> CACHE MISS ON EVERY STEP! 🐢
for (int c = 0; c < C; c++) {
    for (int r = 0; r < R; r++) {
        sum += matrix[r][c]; // SLOW!
    }
}
```

> **Quick Syntax:**
```java
// Linearizing a 2D Matrix (r, c) into a 1D Array of size (R * C)
int index1D = r * C + c; // Convert 2D (r, c) -> 1D index

// De-linearizing a 1D Index back into 2D (r, c)
int r = index1D / C;     // Row index
int c = index1D % C;     // Column index
```

## 7. Examples
* **Matrix Traversal Benchmarking**: Demonstrating 5x to 10x performance differences between row-wise and column-wise matrix traversals.
* **Jagged / Ragged Arrays**: Java allows rows of varying lengths (`int[][] jagged = new int[3][]; jagged[0] = new int[2]; jagged[1] = new int[5];`).
* **Flattening 2D Board for State Hashing**: Converting a Sudoku or $N \times N$ Grid into a 1D String or 1D array using `r * C + c`.

## 8. Java Code
Complete benchmark code demonstrating memory address linearization and measuring CPU cache locality impacts in Java:

```java
public class ArrayMemoryLocalityDemo {

    // 1. Matrix Linearization Utility: 2D <-> 1D Mapping
    public static int get1DIndex(int r, int c, int numCols) {
        return r * numCols + c;
    }

    public static int getRowFrom1D(int index1D, int numCols) {
        return index1D / numCols;
    }

    public static int getColFrom1D(int index1D, int numCols) {
        return index1D % numCols;
    }

    // 2. Cache Locality Benchmark
    public static void runCacheBenchmark(int size) {
        int[][] matrix = new int[size][size];
        
        // Cache-Friendly Traversal (Row-Wise)
        long startRow = System.nanoTime();
        long rowSum = 0;
        for (int r = 0; r < size; r++) {
            for (int c = 0; c < size; c++) {
                rowSum += matrix[r][c];
            }
        }
        long durationRow = (System.nanoTime() - startRow) / 1_000_000;

        // Cache-Unfriendly Traversal (Column-Wise)
        long startCol = System.nanoTime();
        long colSum = 0;
        for (int c = 0; c < size; c++) {
            for (int r = 0; r < size; r++) {
                colSum += matrix[r][c];
            }
        }
        long durationCol = (System.nanoTime() - startCol) / 1_000_000;

        System.out.println("Matrix Size: " + size + "x" + size);
        System.out.println("Row-Wise Traversal (Cache-Friendly): " + durationRow + " ms");
        System.out.println("Col-Wise Traversal (Cache-Miss Heavy): " + durationCol + " ms");
    }

    public static void main(String[] args) {
        // Test Linearization Math
        int R = 4, C = 5;
        int r = 2, c = 3;
        int index1D = get1DIndex(r, c, C);
        System.out.println("2D (" + r + ", " + c + ") -> 1D Index: " + index1D); // 2*5 + 3 = 13
        System.out.println("1D Index " + index1D + " -> 2D: (" + getRowFrom1D(index1D, C) + ", " + getColFrom1D(index1D, C) + ")");

        System.out.println("--- Running Cache Locality Benchmark ---");
        runCacheBenchmark(8000); // 8000 x 8000 matrix
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Cache Locality | Memory Footprint |
| :--- | :--- | :--- | :--- |
| **Row-Major Traversal** | $O(R \cdot C)$ | **High (L1/L2 Cache Hit)** | $4 \cdot R \cdot C$ bytes |
| **Col-Major Traversal (Java)**| $O(R \cdot C)$ | **Low (L1/L2 Cache Miss)**| $4 \cdot R \cdot C + 24R$ bytes (Pointers) |
| **2D $\to$ 1D Conversion Math**| $O(1)$ | N/A | $O(1)$ auxiliary |

## 10. Edge Cases
* **Ragged Arrays (`null` Row Check)**: In Java, `matrix[r]` can be `null` or have `matrix[r].length != matrix[0].length`. Always verify `matrix[r] != null` before accessing `matrix[r][c]`.
* **Integer Overflow in 1D Indexing**: When linearizing a matrix where $R \cdot C > 2^{31}-1$, `r * C + c` overflows signed 32-bit `int`. Cast to `long`: `(long) r * C + c`.

## 11. Common Mistakes
* Assuming Java allocates 2D arrays as a single contiguous memory block like C (`int matrix[R][C]`). (Java allocates an outer array of references pointing to separate 1D inner arrays!).
* Swapping inner and outer loop order during matrix operations, accidentally triggering column-major cache misses.
* Forgetting to use `r * C + c` when flattening 2D matrices for Binary Search or State Memoization.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** How to Binary Search a 2D Sorted Matrix of size $R \times C$:
> Treat the matrix as a flattened 1D array of size $N = R \cdot C$ with range `left = 0` to `right = N - 1`.
> Midpoint element mapping: **`matrix[mid / C][mid % C]`**.

> **Memory Trick:** **"Flattening Formula: Index = r * C + c; Unflattening: r = Index / C, c = Index % C"**.

## 13. Comparisons
| Aspect | 1D Flattened Array (`int[R * C]`) | 2D Array of Arrays (`int[R][C]`) |
| :--- | :--- | :--- |
| **Memory Allocation** | Single contiguous heap block | $R + 1$ independent heap objects |
| **Cache Efficiency** | Absolute Maximum | Good row-wise, terrible col-wise |
| **Memory Overhead** | 24 bytes total header | $24 + (24 \cdot R)$ bytes header overhead |
| **Indexing Syntax** | `arr[r * C + c]` | `matrix[r][c]` |

## 14. How to Recognize This in Questions
* **"Search in a 2D Row-and-Column Sorted Matrix"** $\rightarrow$ Flattening formula `mid / C` and `mid % C`.
* **"Encode Grid Configuration into HashSet Key"** $\rightarrow$ Flatten 2D grid into 1D array or String.

## 15. Frequently Asked Interview Questions
* **Q: Why is Row-Major traversal faster than Column-Major traversal in Java?**  
  *A:* CPU L1/L2 caches fetch memory in 64-byte Cache Lines. Row-major order reads adjacent bytes sequentially within the same cache line ($15/16$ cache hits). Column-major order jumps across separate array references in heap memory, triggering a CPU cache miss on almost every access.
* **Q: What is the memory footprint of an empty `int[0]` array in 64-bit Java JVM?**  
  *A:* 16 bytes (16-byte object header + 0 bytes data + 0 padding = 16 bytes).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MEMORY REPRESENTATION & CACHE LOCALITY                |
+-----------------------------------------------------------------------+
| • Row-Major Indexing: Address = Base + (r * C + c) * ElementSize     |
| • 2D -> 1D Flattening: index1D = r * C + c                           |
| • 1D -> 2D Unflattening: r = index1D / C, c = index1D % C             |
| • Matrix Binary Search Access: matrix[mid / C][mid % C]              |
| • Java 2D Arrays = Array of Reference Pointers -> Traverse Row-Wise!  |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the Row-Major address calculation formula from memory.
- [ ] I can convert 2D coordinates `(r, c)` to 1D index and vice versa.
- [ ] I know why Row-Wise matrix traversal is cache-friendly compared to Column-Wise.
- [ ] I can implement 2D Matrix Binary Search using `mid / C` and `mid % C`.
- [ ] I understand the memory layout of Java's "Array of Arrays".
