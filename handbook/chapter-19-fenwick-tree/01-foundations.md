# 01. Fenwick Tree (BIT) Foundations, Tree Topology & Space Efficiency

## 1. Introduction
A **Fenwick Tree**—also widely known as a **Binary Indexed Tree (BIT)**—is an extraordinarily space-efficient data structure invented by Peter M. Fenwick in 1994. Designed to perform dynamic prefix sum queries and point updates over an array of size $N$, a Fenwick Tree achieves **$O(\log N)$ Logarithmic Query Time** and **$O(\log N)$ Logarithmic Update Time** using **$O(N)$ Space** (exactly $N + 1$ integers!). Compared to a Segment Tree (which requires $4N$ space and complex tree recursion), a Fenwick Tree uses **Bitwise Least Significant Bit (LSB)** index arithmetic to navigate implicit tree paths in a simple 1D array with zero pointer overhead.

> **Important:** Core Invariants of the Fenwick Tree (BIT):
> 1. **1-Based Indexing Invariant**: A Fenwick Tree `tree[]` is strictly 1-indexed (indices $1 \dots N$). Index 0 is a dummy node representing the empty prefix.
> 2. **Responsible Range Invariant**: Element `tree[i]` stores the cumulative sum of a range of length $\text{LSB}(i) = i \mathbin{\&} (-i)$, spanning the array range:
>    $$[i - \text{LSB}(i) + 1 \dots i]$$
> 3. **Space Minimization Invariant**: Allocate an array of size **$N + 1$** (unlike Segment Trees that demand $4N$ space!), saving 75% memory footprint! ⚡

```
Fenwick Tree Responsible Range Topology (Array size N = 8):
Index i (Binary)  LSB(i) = i & (-i)   Responsible Range   Stored Range Sum
-------------------------------------------------------------------------
1  (0001)         1                   [1 ... 1]           nums[0]
2  (0010)         2                   [1 ... 2]           nums[0] + nums[1]
3  (0011)         1                   [3 ... 3]           nums[2]
4  (0100)         4                   [1 ... 4]           nums[0] + ... + nums[3]
5  (0101)         1                   [5 ... 5]           nums[4]
6  (0110)         2                   [5 ... 6]           nums[4] + nums[5]
7  (0111)         1                   [7 ... 7]           nums[6]
8  (1000)         8                   [1 ... 8]           nums[0] + ... + nums[7] ⚡
```

---

## 2. Core Concepts & Fenwick Tree vs Segment Tree Architectural Trade-Offs

### 2.1 Operational Comparison Matrix
```
Dynamic Range Data Structure Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | Fenwick Tree (BIT)| Segment Tree      | Prefix Sum Array  |
+-----------------------+-------------------+-------------------+-------------------+
| **Memory Allocation** | **$N + 1$ Space ⚡**| $4N$ Space        | $N + 1$ Space     |
| **Prefix Sum Query**  | **$O(\log N)$ ⚡**| **$O(\log N)$ ⚡**| **$O(1)$ Constant ⚡**|
| **Point Update**      | **$O(\log N)$ ⚡**| **$O(\log N)$ ⚡**| $O(N)$ Linear     |
| **Range Min/Max Query**| Non-trivial       | **Native $O(\log N)$ ⚡**| Non-trivial    |
| **Code Length**       | **~10 Lines ⚡**  | ~50 Lines         | ~10 Lines         |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fenwick Tree = N+1 space, O(log N) prefix query, O(log N) update, 10 lines of bitwise code!"**

---

## 3. Characteristics & 1-Based Indexing Requirement

### 3.1 Why 1-Based Indexing Is Mandatory
In 0-based indexing:
* For $i = 0$, $\text{LSB}(0) = 0 \mathbin{\&} (-0) = 0$.
* Updating or querying at index 0 results in $i \pm \text{LSB}(0) = 0 \pm 0 = 0$, causing an **INFINITE LOOP**!
* Therefore, Fenwick Trees strictly enforce **1-based indexing** where $\text{LSB}(i) \ge 1$ for all valid nodes $i \in [1 \dots N]$.

---

## 4. Internal Working Mechanics
Tracing Fenwick Tree Stored Ranges for Array `[3, 2, -1, 6, 5, 4, -3, 3]` ($N=8$):

```
1-Based Indices:
- tree[1] (LSB 1): Range [1..1] = 3.
- tree[2] (LSB 2): Range [1..2] = 3 + 2 = 5.
- tree[3] (LSB 1): Range [3..3] = -1.
- tree[4] (LSB 4): Range [1..4] = 3 + 2 + (-1) + 6 = 10.
- tree[5] (LSB 1): Range [5..5] = 5.
- tree[6] (LSB 2): Range [5..6] = 5 + 4 = 9.
- tree[7] (LSB 1): Range [7..7] = -3.
- tree[8] (LSB 8): Range [1..8] = Total Sum = 19.

Every tree[i] stores range of length LSB(i)! ✅
```

---

## 5. Visual Diagram
Fenwick Tree Responsible Subsegment Range Topography:

```
tree[8] (Range 1..8)  ================================================>
tree[4] (Range 1..4)  ===============>
tree[6] (Range 5..6)                  =======>
tree[2] (Range 1..2)  ===>
tree[1] (1..1)        =>
tree[3] (3..3)              =>
tree[5] (5..5)                        =>
tree[7] (7..7)                                  =>
                      [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  (Indices)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Fenwick Tree initialization and basic structure:

```java
import java.util.*;

public class FenwickTreeFoundationsMaster {

    private final int[] tree;
    private final int n;

    // Initialize Fenwick Tree of size N + 1 O(N) Space
    public FenwickTreeFoundationsMaster(int n) {
        this.n = n;
        this.tree = new int[n + 1]; // 1-based indexing array
    }

    // Helper: Calculate Least Significant Bit (LSB) O(1) Time
    public static int lsb(int i) {
        return i & (-i);
    }

    // Get range length covered by tree[i]
    public int getRangeLength(int i) {
        return lsb(i);
    }

    public int getSize() { return n; }
    public int[] getTree() { return tree; }
}
```

> **Quick Syntax:**
```java
// LSB Bitwise Magic Formula Line
int lsb = i & (-i);
```

---

## 7. Concrete Problem Examples
* **LeetCode 307 - Range Sum Query - Mutable**: Fenwick Tree implementation.
* **Inversion Count in Arrays**: Frequency Fenwick Tree.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LSB calculation and responsible range lengths:

```java
public class FenwickTreeFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Fenwick Tree Foundations Test ===");
        int n = 8;
        FenwickTreeFoundationsMaster bit = new FenwickTreeFoundationsMaster(n);

        System.out.println("LSB(1): " + FenwickTreeFoundationsMaster.lsb(1)); // Output: 1
        System.out.println("LSB(2): " + FenwickTreeFoundationsMaster.lsb(2)); // Output: 2
        System.out.println("LSB(4): " + FenwickTreeFoundationsMaster.lsb(4)); // Output: 4
        System.out.println("LSB(6): " + FenwickTreeFoundationsMaster.lsb(6)); // Output: 2
        System.out.println("LSB(8): " + FenwickTreeFoundationsMaster.lsb(8)); // Output: 8 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`lsb(i)` Calculation**| **$O(1)$ Constant ⚡** | $O(1)$ Space | Bitwise `i & (-i)` formula |
| **Space Footprint** | **$N + 1$ Array Space ⚡**| $N + 1$ Integers | 75% memory savings vs Segment Tree |

---

## 10. Edge Cases & Boundary Handling
* **Index 0 Query**: Handled by guarding `while (i > 0)`. Index 0 returns identity `0`.
* **Index $N$ Bounds**: Upper bound loop condition `while (i <= n)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using 0-Based Indexing for `tree[]` Array Access**:
  - Accessing `tree[0]` causes `i & (-i) = 0`, crashing in an infinite loop!
  - **ALWAYS convert 0-based input index `idx` to 1-based index `i = idx + 1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Fenwick Trees Use 75% Less Memory Than Segment Trees:
> A Segment Tree allocates $4N$ space because it explicitly maintains internal non-leaf summary nodes.
> A Fenwick Tree stores ONLY $N$ entries, relying on binary bit manipulation `i & (-i)` to dynamically reconstruct tree parent-child links on-the-fly!

> **Memory Trick:** **"Fenwick Tree saves 75% memory by storing only N elements and calculating links via i & (-i)!"**

---

## 13. System & Implementation Comparisons

| Feature | Fenwick Tree (BIT) | Segment Tree |
| :--- | :--- | :--- |
| **Memory Allocation** | **$N + 1$ Space ⚡** | $4N$ Space |
| **Code Length** | **~10 Lines ⚡** | ~50 Lines |
| **Recursion Call Stack**| **Zero Stack (Iterative) ⚡**| Recursive Stack Depth $\log N$ |

---

## 14. How to Recognize This in Questions
* **"Dynamic prefix sum queries and point updates in O(log N) time with minimum memory"** $\rightarrow$ Fenwick Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the formula for the Least Significant Bit (LSB)?**  
  *A:* $\text{LSB}(i) = i \mathbin{\&} (-i)$.
* **Q: Why does `tree[i]` store a range of length $\text{LSB}(i)$?**  
  *A:* Because clearing the lowest set bit of $i$ removes the lowest binary power of 2, defining the exact subsegment range ending at $i$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FENWICK TREE FOUNDATIONS                              |
+-----------------------------------------------------------------------+
| • Space Allocation : ALWAYS allocate (N + 1) space (1-based indexing) |
| • LSB Formula      : LSB(i) = i & (-i)                                |
| • Stored Range     : tree[i] stores sum over [i - LSB(i) + 1 ... i]   |
| • 0-Based Conversion: Always pass (0-based index + 1) into BIT        |
| • Performance      : O(log N) Query & Update | 75% Memory Savings! ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the LSB formula `i & (-i)` in Java.
- [ ] I know why 1-based indexing is mandatory for Fenwick Trees.
- [ ] I can state the stored range for `tree[i]`.
- [ ] I know why Fenwick Trees save 75% memory compared to Segment Trees.
- [ ] I can trace `LSB(i)` for numbers 1 through 8.
