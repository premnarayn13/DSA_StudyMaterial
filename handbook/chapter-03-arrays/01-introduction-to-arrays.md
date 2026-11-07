# 01. Introduction to Arrays

## 1. Introduction
An **Array** is a linear data structure that stores a collection of elements of the same data type in contiguous memory locations. In technical coding interviews, arrays represent the most fundamental building block for data storage and algorithm design. Understanding how array indices map directly to memory hardware offsets enables constant-time $O(1)$ random access, making arrays the preferred choice for high-performance data processing.

> **Important:** Array elements occupy a single unbroken block of physical RAM. Because memory is contiguous, the location of any element `arr[i]` can be calculated mathematically in constant CPU cycles using base address arithmetic.

## 2. Core Concepts
* **Fixed Size / Static Allocation**: In Java, traditional primitive arrays (`int[]`) have a fixed capacity assigned upon creation. Once allocated, an array cannot grow or shrink dynamically in place.
* **0-Based Indexing**: Array indices range from `0` to `n-1` (where `n` is array length). Index `i` represents the displacement offset from the base memory address of the first element.
* **Random Access Property**: Retrieving or updating any element at index `i` takes strict constant time $O(1)$, independent of array size or position.
* **Homogeneity**: All elements stored within an array must share the exact same data type (or object class type), ensuring identical memory byte width per element.

> **Memory Trick:** **"Index is Offset, Not Element Number"**. Index `0` means zero bytes displacement from the array's start address in RAM. Index `i` means displacement of $i \times \text{elementSize}$ bytes.

## 3. Characteristics / Properties
* **Contiguous Memory**: Sequential indices $(0, 1, 2, \dots, n-1)$ map to physically adjacent RAM memory locations $(A, A+S, A+2S, \dots, A+(n-1)S)$.
* **Spatial Cache Locality**: Sequential arrangement enables CPU hardware L1/L2 caches to prefetch adjacent array elements into cache lines, yielding blazing-fast sequential traversal speeds compared to pointer-based structures.
* **Insertion & Deletion Overhead**: Inserting or deleting elements at arbitrary non-end positions requires shifting subsequent elements, incurring linear $O(n)$ time complexity.

```
Array Characteristics Matrix:
+------------------------+-------------------------------------------------------+
| Characteristic         | Technical Detail & Impact                             |
+------------------------+-------------------------------------------------------+
| Access Time            | O(1) via base address pointer arithmetic              |
| Search Time            | O(n) unsorted linear search / O(log n) binary search  |
| Insertion / Deletion   | O(n) due to shifting elements (O(1) at end if space)   |
| Resizing Cost          | O(n) re-allocation and memory block copy              |
| Memory Efficiency      | Maximum (Zero per-element pointer overhead)           |
+------------------------+-------------------------------------------------------+
```

## 4. Internal Working
At the CPU and Operating System hardware level, array index access leverages pure pointer arithmetic. 

Given an array starting at memory address $B$ (Base Address) where each element consumes $S$ bytes (e.g., $S = 4$ bytes for `int`):

$$\text{MemoryAddress}(\text{arr}[i]) = B + (i \times S)$$

### Step-by-Step Hardware Address Calculation:
Suppose an integer array `int[] arr = new int[5]` is allocated starting at RAM address `0x1000` (Base Address $B = 4096$). Each `int` requires $S = 4$ bytes.

1. **Access `arr[0]`**: Address = $4096 + (0 \times 4) = 4096$ (`0x1000`)
2. **Access `arr[1]`**: Address = $4096 + (1 \times 4) = 4100$ (`0x1004`)
3. **Access `arr[2]`**: Address = $4096 + (2 \times 4) = 4104$ (`0x1008`)
4. **Access `arr[3]`**: Address = $4096 + (3 \times 4) = 4108$ (`0x100C`)
5. **Access `arr[4]`**: Address = $4096 + (4 \times 4) = 4112$ (`0x1010`)

Because multiplication and addition execute in a single CPU clock cycle, array lookup by index is strictly $O(1)$.

```
Physical Hardware RAM Layout for int[] arr = {10, 20, 30, 40, 50}:

  RAM Address:    0x1000      0x1004      0x1008      0x100C      0x1010
                 +-----------+-----------+-----------+-----------+-----------+
  Array Contents:|    10     |    20     |    30     |    40     |    50     |
                 +-----------+-----------+-----------+-----------+-----------+
  Array Index:     arr[0]      arr[1]      arr[2]      arr[3]      arr[4]
```

## 5. Visual Diagram
Contiguous Array vs Non-Contiguous Pointer List:

```
[ CONTIGUOUS ARRAY MEMORY ] (Cache Line Prefetch Friendly ⚡)
RAM Block:  | Addr 100: Val 10 | Addr 104: Val 20 | Addr 108: Val 30 | Addr 112: Val 40 |
            +------------------+------------------+------------------+------------------+
            (Single contiguous CPU Cache Line read loads all 4 elements!)

[ LINKED LIST POINTER MEMORY ] (Cache Miss Heavy 🐢)
RAM Block:  | Addr 204: Val 10 | Next: 850 | ---> [RAM JUMP to 850]
            +------------------------------+
                                                  | Addr 850: Val 20 | Next: 104 |
                                                  +------------------------------+
```

## 6. Operations / Algorithms
Core operations supported by Arrays and their technical mechanics:

### 1. Read / Access (`arr[i]`)
* **Purpose**: Fetch element stored at index `i`.
* **Mechanism**: Direct hardware pointer arithmetic calculation ($B + i \times S$).
* **Time Complexity**: $O(1)$ constant time.

### 2. Update (`arr[i] = value`)
* **Purpose**: Overwrite element at index `i` with a new value.
* **Mechanism**: Direct memory write at computed target address.
* **Time Complexity**: $O(1)$ constant time.

### 3. Linear Search (`search(value)`)
* **Purpose**: Locate index of target value in an unsorted array.
* **Mechanism**: Iterate sequentially from index `0` to `n-1` comparing each element.
* **Time Complexity**: $O(n)$ worst/average case; $\Omega(1)$ best case (if at index 0).

### 4. Insertion at Index `k` (`insert(k, value)`)
* **Purpose**: Insert value at index `k` in an array of current size `size < capacity`.
* **Mechanism**: Shift all elements from index `size - 1` down to `k` one spot to the right to open a gap at index `k`.
* **Time Complexity**: $O(n)$ due to element shifting.

### 5. Deletion at Index `k` (`delete(k)`)
* **Purpose**: Remove element at index `k`.
* **Mechanism**: Shift all elements from index `k + 1` up to `size - 1` one spot to the left to close the gap.
* **Time Complexity**: $O(n)$ due to element shifting.

> **Quick Syntax:**
```java
// Common Array Declarations & Operations in Java
int[] arr = new int[5];                 // Allocate fixed array of size 5 (default 0s)
int[] initialized = {10, 20, 30, 40};  // Literal initialization
int length = initialized.length;        // Read array size property (O(1))

// Iterating over Array
for (int i = 0; i < initialized.length; i++) {
    int val = initialized[i];           // O(1) random access
}
```

## 7. Examples
* **Frequency Counting**: Using an array `int[26]` to count occurrences of lowercase English characters in $O(1)$ space.
* **Prefix Sum Array**: Precomputing cumulative sums to answer range sum queries in $O(1)$ time.
* **Fixed Window Sliding Buffer**: Maintaining $K$ consecutive elements in linear array algorithms.

## 8. Java Code
Interview-ready Java implementation demonstrating complete array operations (insertion, deletion, traversal, and linear search) with boundary safety checks:

```java
public class ArrayOperationsMaster {

    private int[] data;
    private int capacity;
    private int size;

    // Constructor to initialize array with specified capacity
    public ArrayOperationsMaster(int capacity) {
        this.capacity = capacity;
        this.data = new int[capacity];
        this.size = 0;
    }

    // O(1) Amortized / O(1) End Insertion
    public void insertEnd(int value) {
        if (size == capacity) {
            throw new IllegalStateException("Array capacity full! Cannot insert at end.");
        }
        data[size++] = value;
    }

    // O(n) Arbitrary Index Insertion with Right Shifting
    public void insertAt(int index, int value) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException("Invalid index for insertion: " + index);
        }
        if (size == capacity) {
            throw new IllegalStateException("Array capacity full! Cannot insert.");
        }

        // Shift elements to the right to open gap at target index
        for (int i = size - 1; i >= index; i--) {
            data[i + 1] = data[i];
        }

        data[index] = value;
        size++;
    }

    // O(n) Arbitrary Index Deletion with Left Shifting
    public int deleteAt(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Invalid index for deletion: " + index);
        }

        int removedValue = data[index];

        // Shift elements to the left to close gap
        for (int i = index; i < size - 1; i++) {
            data[i] = data[i + 1];
        }

        data[--size] = 0; // Clear last slot for hygiene
        return removedValue;
    }

    // O(1) Constant Time Access
    public int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("Index out of bounds: " + index);
        }
        return data[index];
    }

    // O(n) Unsorted Linear Search
    public int search(int target) {
        for (int i = 0; i < size; i++) {
            if (data[i] == target) {
                return i;
            }
        }
        return -1; // Target not found
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        ArrayOperationsMaster arr = new ArrayOperationsMaster(5);

        arr.insertEnd(10); // [10]
        arr.insertEnd(20); // [10, 20]
        arr.insertEnd(40); // [10, 20, 40]

        System.out.println("Search 20: Index " + arr.search(20)); // Output: 1

        arr.insertAt(2, 30); // Insert 30 at index 2 -> [10, 20, 30, 40]
        System.out.println("Element at index 2 after insertion: " + arr.get(2)); // Output: 30

        int deleted = arr.deleteAt(1); // Delete at index 1 -> [10, 30, 40]
        System.out.println("Deleted Element: " + deleted); // Output: 20
        System.out.println("New Element at index 1: " + arr.get(1)); // Output: 30
    }
}
```

## 9. Complexity Analysis
Detailed breakdown of time and space complexity across core array operations:

| Operation | Best Case ($\Omega$) | Average Case ($\Theta$) | Worst Case ($O$) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **Access (`arr[i]`)** | $\Omega(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |
| **Search (Unsorted)** | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| **Search (Sorted)** | $\Omega(1)$ | $\Theta(\log n)$ | $O(\log n)$ | $O(1)$ iterative |
| **Insert at Beginning**| $\Omega(n)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| **Insert at End** | $\Omega(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ (if capacity exists) |
| **Delete at Beginning**| $\Omega(n)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ |
| **Delete at End** | $\Omega(1)$ | $\Theta(1)$ | $O(1)$ | $O(1)$ |

## 10. Edge Cases
* **Empty Array (`size == 0`)**: Accessing or deleting from an empty array must be guarded by `size == 0` check.
* **Array Index Out of Bounds**: Index $i < 0$ or $i \ge n$ throws `java.lang.ArrayIndexOutOfBoundsException`.
* **Array Full Capacity**: Attempting to insert into a full static array requires creating a new larger array and copying elements over.
* **Integer Pointer Arithmetic Overflow**: In systems with huge arrays ($n > 2^{31}-1$), array indexing exceeds standard 32-bit signed `int` ranges.

## 11. Common Mistakes
* **Off-By-One Errors**: Iterating up to `i <= arr.length` instead of `i < arr.length` (causes `ArrayIndexOutOfBoundsException`).
* **Confusing Length with Capacity**: `arr.length` represents total allocated slot capacity, NOT the number of populated data elements (`size`).
* **Forgetting Right Shifting Order during Insertion**: Shifting elements from left-to-right during insertion overwrites subsequent values! Insertion shifting MUST proceed from **right-to-left** (`i = size-1` down to `k`).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Insertion shifting order vs Deletion shifting order:
> * **Insertion**: Shift elements **Right** starting from the **End** (`for (int i = size - 1; i >= k; i--) arr[i + 1] = arr[i]`).
> * **Deletion**: Shift elements **Left** starting from the **Target Index** (`for (int i = k; i < size - 1; i++) arr[i] = arr[i + 1]`).

> **Memory Trick:** **"Insertion = Right-to-Left Shift, Deletion = Left-to-Right Shift"**. Getting this backwards in an interview will corrupt array contents!

## 13. Comparisons
| Feature | Primitive Array (`int[]`) | Dynamic Array (`ArrayList<Integer>`) |
| :--- | :--- | :--- |
| **Size Flexibility** | Fixed capacity set at allocation | Resizes dynamically ($1.5\times$ expansion) |
| **Performance** | Maximum ($O(1)$ raw memory access) | Amortized $O(1)$ (slight pointer overhead) |
| **Primitive Storage** | Direct primitive values | Autoboxed object wrappers (`Integer`) |
| **Memory Footprint** | $4$ bytes per `int` | $\approx 24$ bytes per `Integer` object |

## 14. How to Recognize This in Questions
* **"Find element at k-th position"** $\rightarrow$ Direct Array Indexing ($O(1)$ time).
* **"Subarray with given sum / Window of size K"** $\rightarrow$ Two Pointers / Sliding Window on Array.
* **"In-place element modification"** $\rightarrow$ Array index swap operations.

## 15. Frequently Asked Interview Questions
* **Q: Why does array random access take constant time $O(1)$?**  
  *A:* Because elements are stored in contiguous memory addresses, allowing the CPU to compute any element's exact RAM address using the formula `Address = BaseAddress + (index * elementSize)` in a single hardware cycle.
* **Q: Why does Java throw `ArrayIndexOutOfBoundsException`?**  
  *A:* Java performs mandatory runtime boundary checks on every array access. If `index < 0` or `index >= arr.length`, the JVM halts execution to prevent arbitrary RAM buffer overflow vulnerabilities.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: INTRODUCTION TO ARRAYS                               |
+-----------------------------------------------------------------------+
| • Formula: Address(i) = BaseAddress + (index * ElementSize)           |
| • Access: O(1) Constant | Search: O(n) Unsorted | Insert/Delete: O(n) |
| • Insertion Shifting: Shift Right (Right-to-Left loop)                |
| • Deletion Shifting: Shift Left (Left-to-Right loop)                  |
| • Spatial Cache Locality: Sequential Memory enables CPU pre-fetching  |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the hardware address calculation formula for array indexing.
- [ ] I know why array index access is $O(1)$ at the CPU instruction level.
- [ ] I can implement array insertion with right-shifting from memory.
- [ ] I can implement array deletion with left-shifting from memory.
- [ ] I know how to prevent off-by-one `ArrayIndexOutOfBoundsException` bugs.
