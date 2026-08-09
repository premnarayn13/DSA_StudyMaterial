# 01. Search Fundamentals: Search Problem Taxonomy, Monotonicity & Time-Space Tradeoffs

## 1. Introduction
**Searching** is the algorithmic process of locating a specific target item, key, condition, or optimal decision state within a dataset or search space. As the foundation of computer systems engineering, searching underpins database indexing, file systems, graph engines, optimization solvers, and AI decision systems. The choice of searching paradigm—ranging from **Unordered Linear Search ($O(N)$)** to **Ordered Binary Search ($O(\log N)$)** and **Direct Hash Indexing ($O(1)$)**—is governed by data structural invariants such as **Monotonicity**, **Ordering**, and **Time-Space Tradeoffs**.

> **Important:** The 3 Foundational Pillars of Search Engine Design:
> 1. **Search Space Definition**: The universe of candidate elements or decision boundaries being inspected (discrete array, continuous range, or implicit decision function).
> 2. **Monotonicity Invariant**: A non-decreasing or non-increasing structural property ($f(x_1) \le f(x_2)$ for $x_1 < x_2$) that enables discarding half the remaining search space at each step.
> 3. **Search Predicate Function $P(x)$**: A boolean test evaluated at candidate position $x$ that returns `true` or `false`, dividing the search domain into two contiguous partitions: `[false, false, ..., true, true]`. ⚡

```
Monotonic Search Space Partitioning Topology:
Candidate Space:   [ 1,  3,  5,  7,  9, 12, 15, 18, 21 ]
Predicate P(x >= 10): [ F,  F,  F,  F,  F,  T,  T,  T,  T ]
                                           ^
                               First True Boundary Index! ⚡
```

---

## 2. Core Concepts & Searching Paradigms Comparison Matrix

### 2.1 Searching Paradigm Matrix
```
Searching Paradigms Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Searching Paradigm    | Data Requirement  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **Linear Search**     | None (Unordered)  | **$O(N)$ Linear** | **$O(1)$ Auxiliary ⚡**|
| **Binary Search**     | Sorted / Monotonic| **$O(\log N)$ Log ⚡**| **$O(1)$ Iterative ⚡**|
| **Hash Indexing**     | Key Hash Function | **$O(1)$ Average ⚡**| $O(N)$ Hash Table |
| **B-Tree Indexing**   | Disk Block Sorted | **$O(\log_B N)$ Log**| $O(N)$ Node Memory |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Linear Search = Unordered O(N); Binary Search = Sorted O(log N); Hash Index = O(1) space trade!"**

---

## 3. Characteristics & Time-Space Tradeoffs

### 3.1 Time-Space Tradeoff Matrix
* **No Preprocessing ($O(1)$ Setup Time)**:
  - If array is unsorted and queries are rare ($Q = 1$), run **Linear Search** in $O(N)$ time. Preprocessing (sorting) takes $O(N \log N)$, which is wasteful for 1 query.
* **Pre-Sorted Indexing ($O(N \log N)$ Setup Time)**:
  - If queries are frequent ($Q \gg 1$), sort the array once in $O(N \log N)$ time and execute $Q$ queries using **Binary Search** in $O(Q \log N)$ time.
* **Hash-Based Indexing ($O(N)$ Space & Setup Time)**:
  - Allocate a hash table in $O(N)$ space to achieve $O(1)$ query lookups.

```
Query Threshold Decision Table:
Q = 1 Query        ---> Use Linear Search: Cost = O(N) Total.
Q = N Queries      ---> Sort + Binary Search: Cost = O(N log N + N log N) = O(N log N) Total.
Q = 1,000,000      ---> Hash Table Index: Cost = O(N) Build + O(Q) Lookups. ⚡
```

---

## 4. Internal Working Mechanics: Predicate Binary Search Partitioning

A search space is monotonic with respect to a predicate function $P(x)$ if $P(x) \implies P(y)$ for all $y > x$.

```
Tracing Binary Search Predicate Partitioning on Array: [2, 4, 6, 8, 10, 12, 14]
Target: Find first element >= 7 (Predicate P(x): x >= 7)

Step 1: low = 0, high = 6. mid = 3 (val = 8).
        P(8) = (8 >= 7) = TRUE.
        Boundary can be mid=3 or to the left! Set high = mid (3). Search Range: [0 ... 3].

Step 2: low = 0, high = 3. mid = 1 (val = 4).
        P(4) = (4 >= 7) = FALSE.
        Boundary MUST be to the right of mid! Set low = mid + 1 (2). Search Range: [2 ... 3].

Step 3: low = 2, high = 3. mid = 2 (val = 6).
        P(6) = (6 >= 7) = FALSE.
        Set low = mid + 1 (3). Search Range: [3 ... 3].

Step 4: low == high (3). Loop terminates!
Result: Index 3 (val = 8) is the FIRST element satisfying P(x) >= 7! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram: Monotonic Predicate Partitioning

```
Monotonic Search Space Division:

   [ false,  false,  false,  false | true,  true,  true,  true ]
   |<--------- Region 1 ---------->|<-------- Region 2 --------->|
   | P(x) = false                  | P(x) = true                 |
                                   ^
                           First True Boundary (Target Index!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing foundational search algorithms, query-based strategy selection, and generic predicate binary search partitioning.

```java
import java.util.*;
import java.util.function.Predicate;

/**
 * Production-Grade Master Suite Demonstrating Search Fundamentals,
 * Query Threshold Strategy Selection, and Generic Predicate Partitioning.
 */
public class SearchFundamentalsMaster {

    // =========================================================================
    // 1. UNORDERED LINEAR SEARCH (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Performs linear search over an unsorted array.
     * Best for single-query searches on unordered datasets.
     *
     * @param arr input array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int linearSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i; // First match found!
            }
        }
        return -1;
    }

    // =========================================================================
    // 2. ORDERED BINARY SEARCH (O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Performs iterative binary search over a sorted array.
     * Overflow-safe midpoint calculation.
     *
     * @param arr sorted array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int binarySearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int low = 0;
        int high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2; // Overflow-safe mid!

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    // =========================================================================
    // 3. GENERIC PREDICATE BINARY SEARCH (First True Boundary O(log N))
    // =========================================================================
    /**
     * Generic Binary Search finding the FIRST index in [0 ... N-1] where predicate P(i) is true.
     * Monotonic Predicate Array: [false, false, ..., true, true]
     *
     * @param n search space size
     * @param predicate boolean condition function
     * @return first index satisfying predicate or -1 if none
     */
    public int findFirstTrueIndex(int n, Predicate<Integer> predicate) {
        if (n <= 0 || predicate == null) return -1;

        int low = 0;
        int high = n - 1;
        int ans = -1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (predicate.test(mid)) {
                ans = mid;        // Candidate found, search left for earlier match
                high = mid - 1;
            } else {
                low = mid + 1;    // Search right
            }
        }

        return ans;
    }
}
```

> **Quick Syntax:**
```java
// First True Predicate Binary Search Loop
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (P(mid)) { ans = mid; high = mid - 1; } else { low = mid + 1; }
}
```

---

## 7. Concrete Problem Examples & System Applications

1. **Database Query Engines**:
   - Single Query Unindexed Scan: Linear Search.
   - B-Tree Index Range Search: Monotonic Binary Search ($O(\log N)$).

2. **Operating System Memory Management**:
   - Page Table Virtual Address Translation.
   - Binary Search on Allocated Memory Chunk Boundaries.

3. **Algorithm Optimization**:
   - Binary Search on Answer (Capacity, Speed, Threshold Optimization).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class SearchFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     SEARCH FUNDAMENTALS DEMONSTRATION SUITE     ");
        System.out.println("=================================================\n");

        SearchFundamentalsMaster master = new SearchFundamentalsMaster();

        // 1. Linear Search Test
        int[] unsorted = {42, 15, 8, 99, 23, 7};
        int target1 = 23;
        int linearIdx = master.linearSearch(unsorted, target1);
        System.out.println("1. Linear Search Target " + target1 + " in Unsorted Array: Index = " + linearIdx);
        System.out.println("-------------------------------------------------");

        // 2. Binary Search Test
        int[] sorted = {7, 8, 15, 23, 42, 99};
        int target2 = 23;
        int binaryIdx = master.binarySearch(sorted, target2);
        System.out.println("2. Binary Search Target " + target2 + " in Sorted Array: Index = " + binaryIdx);
        System.out.println("-------------------------------------------------");

        // 3. Generic Predicate Binary Search Test (First Element >= 20)
        int n = sorted.length;
        int firstIdx = master.findFirstTrueIndex(n, index -> sorted[index] >= 20);
        System.out.println("3. First Index where sorted[i] >= 20: Index = " + firstIdx + " (Value = " + sorted[firstIdx] + ")");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Searching Paradigm | Data Precondition | Best Case Time | Worst Case Time | Auxiliary Space | Query Threshold |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Search** | Unordered | $\mathbf{O(1)}$ Constant | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | $Q = 1$ Query |
| **Binary Search** | Sorted / Monotonic| $\mathbf{O(1)}$ Constant | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | $Q \ge \log N$ Queries |
| **Hash Lookup** | Key Hashing | $\mathbf{O(1)}$ Constant ⚡| $O(N)$ (Collisions) | $O(N)$ Extra Table | High Frequency |

---

## 10. Edge Cases & Boundary Handling

1. **Searching in Empty Container ($N = 0$)**:
   - `arr == null || arr.length == 0` returns `-1` immediately.

2. **Searching Element Smaller Than All Elements**:
   - Binary search narrows `high` to `-1`, terminating loop with `low = 0, high = -1`. Returns `-1` cleanly.

3. **Searching Element Larger Than All Elements**:
   - Binary search advances `low` to $N$, terminating loop with `low = N, high = N - 1`. Returns `-1` cleanly.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Sorting Array for a Single Query**:
  - Sorting an $N$-element unsorted array in $O(N \log N)$ time just to perform 1 binary search query ($O(\log N)$) takes $O(N \log N)$ total time! Linear search takes $O(N)$ total time, which is faster for $Q = 1$.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Use Binary Search on Unsorted Data:
> Binary Search does NOT strictly require a sorted array!
> It requires a **MONOTONIC PREDICATE FUNCTION** $P(x)$ that partitions the search domain into two contiguous regions `[false, ..., true]`.
> Problems like Peak Index in Mountain Array (LeetCode 852) operate on unsorted data using slope predicates (`arr[i] < arr[i + 1]`)! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Search | Binary Search | Hash Table Index |
| :--- | :--- | :--- | :--- |
| **Preprocessing Cost**| **$O(1)$ Zero Setup ⚡** | $O(N \log N)$ Sort Time | $O(N)$ Build Time |
| **Query Cost** | $O(N)$ Linear | **$O(\log N)$ Logarithmic ⚡**| **$O(1)$ Constant ⚡** |
| **Extra Memory** | **$O(1)$ Zero Extra ⚡** | **$O(1)$ Zero Extra ⚡** | $O(N)$ Hash Allocations |

---

## 14. How to Recognize This in Questions

* **"Search element in unsorted list with single query"** $\rightarrow$ Linear Search.
* **"Find element in sorted array or monotonic condition"** $\rightarrow$ Binary Search ($O(\log N)$).
* **"Constant time search lookups"** $\rightarrow$ Hash Table Index ($O(1)$).

---

## 15. Frequently Asked Interview Questions

* **Q: Why is `mid = low + (high - low) / 2` preferred over `(low + high) / 2`?**  
  *A:* To prevent signed 32-bit integer overflow when `low + high > 2,147,483,647`.

* **Q: Does Binary Search strictly require a sorted array?**  
  *A:* No. It requires a monotonic predicate function $P(x)$ dividing the domain into contiguous `false` and `true` regions.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEARCH FUNDAMENTALS                                   |
+-----------------------------------------------------------------------+
| • Linear Search : Unordered data | Time O(N) | Space O(1)             |
| • Binary Search : Sorted / Monotonic data | Time O(log N) | Space O(1) |
| • Predicate BS  : Divides search space into [false, false, true, true]|
| • Mid Formula   : mid = low + (high - low) / 2 (Overflow Safe)        |
| • Strategy Rule : Q = 1 -> Linear; Q >> 1 -> Sort + Binary Search! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state time/space tradeoffs between Linear, Binary, and Hash Search.
- [ ] I can write overflow-safe Binary Search in Java.
- [ ] I can write a generic predicate binary search to find first `true` index.
- [ ] I can choose the optimal searching strategy based on query frequency $Q$.
- [ ] I can trace predicate binary search state transitions step by step.
