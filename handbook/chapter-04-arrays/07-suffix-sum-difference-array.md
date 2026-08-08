# 07. Suffix Sum & Difference Array Technique

## 1. Introduction
While Prefix Sum answers range sum queries on static arrays, the **Difference Array** technique solves the inverse problem: performing range update operations (e.g., adding value $V$ to all elements in range $[L, R]$) across multiple queries in **$O(1)$ time per update** instead of $O(N)$ per update. Combined with **Suffix Sums** (cumulative sum from right to left), these two array techniques form the backbone for range range updates, corporate meeting scheduling, and flight booking booking problems.

> **Important:** Applying $Q$ range updates $[L, R, V]$ naively takes $O(Q \cdot N)$ time. With a Difference Array, performing $Q$ range updates and reconstructing the final array via prefix sum takes **$O(N + Q)$** total execution time!

## 2. Core Concepts
* **Suffix Sum**: Cumulative sum calculated from right to left (index $n-1$ down to $0$):
  $$\text{suffix}[i] = \text{arr}[i] + \text{suffix}[i+1]$$
* **Difference Array ($D$)**: An array $D$ where each element $D[i] = \text{arr}[i] - \text{arr}[i-1]$ (with $D[0] = \text{arr}[0]$).
* **Difference Array Range Update Rule**: To add value $V$ to every element in range $[L, R]$:
  1. Add $V$ to lower bound $L$: **`D[L] += V`**
  2. Subtract $V$ from upper bound $R+1$: **`D[R + 1] -= V`** (if $R+1 < N$)
* **Array Reconstruction**: Computing the prefix sum of Difference Array $D$ restores the modified final array values in $O(N)$ time!

> **Memory Trick:** **"Range Add V to [L, R] -> D[L] += V and D[R + 1] -= V"**.

## 3. Characteristics / Properties
* **Deferred Computation**: Range updates modify boundary markers $D[L]$ and $D[R+1]$ instantly ($O(1)$ time). The actual array values are computed once at the end using a single prefix sum sweep ($O(N)$ time).
* **Dual Technique Complementarity**:
  * **Prefix Sum**: Answers Range *Read* Queries in $O(1)$.
  * **Difference Array**: Executes Range *Write/Update* Operations in $O(1)$.

```
Range Update Strategy Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Range Update Method   | Time per Update   | Final Build Time  | Total for Q Updates|
+-----------------------+-------------------+-------------------+-------------------+
| Naive Loop Update     | O(N)              | O(0)              | O(Q * N) (SLOW!)  |
| Difference Array      | O(1)              | O(N)              | O(N + Q) (FAST!⚡)|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Difference Array Range Updates on `arr = [0, 0, 0, 0, 0]` ($N = 5$):

### Step 1: Initial Difference Array $D = [0, 0, 0, 0, 0]$

### Step 2: Query 1 — Add $V = 10$ to Range $[1, 3]$
* `D[1] += 10` $\to$ `D = [0, 10, 0, 0, 0]`
* `D[3 + 1] -= 10` $\to$ `D = [0, 10, 0, 0, -10]`

### Step 3: Query 2 — Add $V = 5$ to Range $[0, 2]$
* `D[0] += 5` $\to$ `D = [5, 10, 0, 0, -10]`
* `D[2 + 1] -= 5` $\to$ `D = [5, 10, 0, -5, -10]`

### Step 4: Reconstruct Final Array via Prefix Sum on $D$
* `result[0] = D[0] = 5`
* `result[1] = result[0] + D[1] = 5 + 10 = 15`
* `result[2] = result[1] + D[2] = 15 + 0 = 15`
* `result[3] = result[2] + D[3] = 15 + (-5) = 10`
* `result[4] = result[3] + D[4] = 10 + (-10) = 0`

Final Reconstructed Array: **`[5, 15, 15, 10, 0]`** ✅ (Correct!)

## 5. Visual Diagram
Difference Array Boundary Marking Mechanism:

```
Index:        0      1      2      3      4      5
D Array:    [ +5 ] [ +10] [  0 ] [ -5 ] [ -10] [  0 ]
              ^      ^            ^       ^
           Add Q2  Add Q1       Sub Q2  Sub Q1
           (L=0)   (L=1)        (R+1=3) (R+1=4)

Prefix Sum: [ 5 ]  [ 15 ] [ 15 ] [ 10 ]  [ 0 ]
            (Values active between L and R remain elevated by V!)
```

## 6. Operations / Algorithms
Difference Array Master Implementation:

```java
public class DifferenceArray {
    private int[] diff;
    private int n;

    public DifferenceArray(int[] arr) {
        this.n = arr.length;
        this.diff = new int[n];
        diff[0] = arr[0];
        for (int i = 1; i < n; i++) {
            diff[i] = arr[i] - arr[i - 1];
        }
    }

    // O(1) Range Update [L, R] by val
    public void update(int L, int R, int val) {
        diff[L] += val;
        if (R + 1 < n) {
            diff[R + 1] -= val;
        }
    }

    // O(N) Reconstruction of final array
    public int[] build() {
        int[] result = new int[n];
        result[0] = diff[0];
        for (int i = 1; i < n; i++) {
            result[i] = result[i - 1] + diff[i];
        }
        return result;
    }
}
```

> **Quick Syntax:**
```java
// Difference Array Boundary Update Rules
diff[L] += val;
if (R + 1 < N) {
    diff[R + 1] -= val;
}
```

## 7. Examples
* **LeetCode 370 - Range Addition**: Performing multiple range additions on an initially zeroed array in $O(N + Q)$ time.
* **LeetCode 1109 - Corporate Flight Bookings**: Accumulating passenger seat reservations across flight ranges $[L, R]$.
* **LeetCode 1094 - Car Pooling**: Tracking passenger capacity changes at pickup $L$ and dropoff $R$ locations.

## 8. Java Code
Complete interview-ready Java implementation demonstrating Corporate Flight Bookings (LeetCode 1109) using Difference Array:

```java
import java.util.Arrays;

public class DifferenceArrayMaster {

    // LeetCode 1109: Corporate Flight Bookings O(N + Q) Time, O(N) Auxiliary Space
    public static int[] corpFlightBookings(int[][] bookings, int n) {
        // Difference array of size n + 1 (1-indexed for 1-based flight numbers)
        int[] diff = new int[n + 2];

        // Process each booking update in O(1)
        for (int[] booking : bookings) {
            int first = booking[0];  // 1-indexed L
            int last = booking[1];   // 1-indexed R
            int seats = booking[2];  // Value V

            diff[first] += seats;
            diff[last + 1] -= seats;
        }

        // Reconstruct result array using Prefix Sum in O(N)
        int[] result = new int[n];
        int currentSeats = 0;
        for (int i = 1; i <= n; i++) {
            currentSeats += diff[i];
            result[i - 1] = currentSeats;
        }

        return result;
    }

    // Suffix Sum Calculation Utility O(N) Time
    public static long[] computeSuffixSum(int[] arr) {
        if (arr == null) return new long[0];
        int n = arr.length;
        long[] suffix = new long[n];
        suffix[n - 1] = arr[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            suffix[i] = suffix[i + 1] + arr[i];
        }
        return suffix;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Bookings: [firstFlight, lastFlight, seats]
        int[][] bookings = {
            {1, 2, 10},
            {2, 3, 20},
            {2, 5, 25}
        };
        int n = 5; // 5 flights

        int[] result = corpFlightBookings(bookings, n);
        System.out.println("Flight Seats: " + Arrays.toString(result));
        // Output: [10, 55, 45, 25, 25]

        // Test Suffix Sum
        int[] data = {1, 2, 3, 4, 5};
        System.out.println("Suffix Sum of {1,2,3,4,5}: " + Arrays.toString(computeSuffixSum(data)));
        // Output: [15, 14, 12, 9, 5]
    }
}
```

## 9. Complexity Analysis
| Operation | Naive Approach | Difference Array Approach | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Single Range Update $[L, R]$** | $O(N)$ | **$O(1)$** | Boundary modification only |
| **$Q$ Range Updates** | $O(Q \cdot N)$ | **$O(Q)$** | Instantaneous additions |
| **Final Array Reconstruction** | $O(0)$ | **$O(N)$** | Single prefix sum sweep |
| **Total Execution Time** | $O(Q \cdot N)$ | **$O(N + Q)$** | Over **100x faster** for large $Q$ |

## 10. Edge Cases
* **$R + 1 = N$ (Boundary Overflow)**: When range update ends at the last element ($R = N - 1$), $R + 1 = N$ is outside array bounds. Always guard: `if (R + 1 < N) diff[R + 1] -= val;`.
* **1-Based vs 0-Based Indexing**: Problems like Flight Bookings use 1-based indexing ($1 \le L \le R \le N$). Allocate `diff` of size $N + 2$ to safely accommodate index $N + 1$.
* **Integer Overflow in Accumulated Seats**: Large values $V$ across $10^5$ queries require `long[]` for difference and result arrays.

## 11. Common Mistakes
* Index out of bounds error by writing `diff[R + 1] -= val` without checking `R + 1 < N`.
* Trying to read intermediate array values *before* executing the final prefix sum build sweep.
* Using Difference Array when updates and queries are **interleaved** (e.g., Update $\to$ Read $\to$ Update $\to$ Read). Interleaved updates/reads require **Segment Tree** or **Fenwick Tree** ($O(\log N)$ update/query).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Difference Array is optimal ONLY when all range updates are performed FIRST, followed by a SINGLE final read/build pass! If updates and queries are mixed dynamically, use a **Fenwick Tree (Binary Indexed Tree)** or **Segment Tree** for $O(\log N)$ updates.

> **Memory Trick:** **"D[L] += V, D[R+1] -= V, then Prefix Sum at the end!"**

## 13. Comparisons
| Requirement | Difference Array | Segment Tree / Fenwick Tree |
| :--- | :--- | :--- |
| **Update Pattern** | Batch Updates First, Reads Last | Dynamic Interleaved Updates & Reads |
| **Update Time** | **$O(1)$** | $O(\log N)$ |
| **Build / Read Time** | $O(N)$ final sweep | $O(\log N)$ query |
| **Code Complexity** | Ultra-Simple ($\approx 5$ lines) | Complex ($\approx 50$ lines) |

## 14. How to Recognize This in Questions
* **"Given an array of zeros, apply Q range addition operations [L, R, V]"** $\rightarrow$ Difference Array ($O(N + Q)$).
* **"Car Pooling / Meeting Room Capacity Overlap"** $\rightarrow$ Difference Array on time line.

## 15. Frequently Asked Interview Questions
* **Q: Why does adding $V$ to $D[L]$ and subtracting $V$ from $D[R+1]$ work?**  
  *A:* Because prefix sum accumulates values from left to right. Adding $V$ at $D[L]$ causes all elements from index $L$ onward to be increased by $V$. Subtracting $V$ at $D[R+1]$ cancels out the addition for all elements after $R$, restricting the net increase of $V$ strictly to the range $[L, R]$.
* **Q: What is a Suffix Sum array used for?**  
  *A:* Suffix sums are used in right-to-left traversal problems, such as computing Trapping Rain Water, Best Time to Buy and Sell Stock, and suffix range queries.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUFFIX SUM & DIFFERENCE ARRAY                         |
+-----------------------------------------------------------------------+
| • Range Add V to [L, R]: diff[L] += V; if (R+1 < N) diff[R+1] -= V;   |
| • Final Array Reconstruction: Prefix sum sweep over diff array        |
| • Total Time Complexity: O(N + Q) for Q range updates                 |
| • Limitation: Batch updates first! (Use Fenwick Tree if interleaved)  |
| • Suffix Sum: Cumulative sum right-to-left: suffix[i] = val + suffix[i+1]|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the Difference Array update rules from memory.
- [ ] I know how to guard against $R + 1 \ge N$ index boundary overflow.
- [ ] I can reconstruct the final array from a difference array using prefix sum.
- [ ] I know when to use Difference Array vs Fenwick / Segment Trees.
- [ ] I can solve LeetCode 1109 (Corporate Flight Bookings) in $O(N + Q)$ time.
