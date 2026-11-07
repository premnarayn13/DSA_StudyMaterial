# 02. Linear Search: Sentinel Search, Self-Organizing Heuristics & Multi-Target Processing

## 1. Introduction
**Linear Search (Sequential Search)** is the simplest and most universal searching algorithm. It operates by iterating sequentially through a collection of $N$ elements from index $0$ to $N-1$, comparing each item against a target key until a match is found or the end of the container is reached. Despite its basic $O(N)$ time complexity, advanced production variants—such as **Sentinel Linear Search** (eliminating array bound checks inside loop conditions) and **Self-Organizing Heuristics** (**Move-to-Front** and **Transpose** heuristics)—optimize cache locality and search latency in dynamically queried un-indexed systems.

> **Important:** Core Invariants of Linear Search Variants:
> 1. **Standard Linear Search**: Performs 2 comparisons per iteration: (1) `i < N` loop bound check, and (2) `arr[i] == target` value match.
> 2. **Sentinel Linear Search Optimization**: Places the target key at the last index (`arr[N-1] = target`), reducing loop overhead to ONLY 1 comparison per iteration (`arr[i] != target`).
> 3. **Move-to-Front Self-Organizing Heuristic**: Upon finding a target at index $i$, moves it to index $0$. Frequently accessed elements migrate to the front, reducing future search costs to $O(1)$!
> 4. **Transpose Heuristic**: Moves accessed element 1 position left ($i \to i-1$), gradually building frequency order without volatile position shifts. ⚡

```
Sentinel Linear Search Memory Topology:
Original Array:   [ 42, 15, 8, 99, 23 ]   Target = 8
Append Sentinel:  [ 42, 15, 8, 99, 23 | 8 ] (Index N = 5)

Loop Condition:   while (arr[i] != target) i++;  <-- Single Comparison Per Step! ⚡
```

---

## 2. Core Concepts & Linear Search Variants Comparison Matrix

### 2.1 Linear Search Variants Matrix
```
Linear Search Variants Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variant               | Comparisons/Step  | Cache Benefit     | Best Use Case     |
+-----------------------+-------------------+-------------------+-------------------+
| **Standard Search**   | 2 (Bound + Value) | Baseline          | Simple Scans      |
| **Sentinel Search**   | **1 (Value Only)⚡**| Low Overhead      | High-Speed Loops  |
| **Move-to-Front**     | 2 + Swap          | **Temporal Locality ⚡**| Repeated Queries|
| **Transpose Search**  | 2 + Swap          | Stable Order      | Frequency Ordering|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sentinel Search removes bound check! Move-to-Front shifts found element to index 0!"**

---

## 3. Characteristics & $O(N)$ Time Complexity Proof

### 3.1 Mathematical Proof of Sentinel Loop Speedup
* Standard Linear Search loop evaluates $2N$ comparisons in worst case:
  $$C_{\text{standard}}(N) = N \text{ (bounds checks)} + N \text{ (value checks)} = 2N \text{ comparisons}$$
* Sentinel Linear Search appends `target` to `arr[N]`:
  $$C_{\text{sentinel}}(N) = N+1 \text{ (value checks ONLY)} \approx N \text{ comparisons}$$
* Reduces loop comparison CPU cycles by **50%**! Time Complexity remains $\mathbf{O(N) \text{ Linear}}$, Space Complexity remains $\mathbf{O(1) \text{ Auxiliary}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Move-to-Front Self-Organization

Tracing 3 sequential queries `[8, 8, 8]` on Array `[42, 15, 8, 99, 23]`:

```
Initial State: [ 42, 15, 8, 99, 23 ]

Query 1 (Target = 8):
- Linear Scan finds 8 at index 2 (3 comparisons).
- Apply Move-to-Front: Swap 8 with index 0.
- Array state becomes: [ 8, 42, 15, 99, 23 ]

Query 2 (Target = 8):
- Linear Scan finds 8 at index 0 (1 comparison!).
- Array state remains: [ 8, 42, 15, 99, 23 ]

Query 3 (Target = 8):
- Linear Scan finds 8 at index 0 (1 comparison!).

Total Comparisons for 3 queries: 3 + 1 + 1 = 5 comparisons (vs 9 for standard search)! ✅ (O(1) Amortized Time!)
```

---

## 5. Visual Diagram: Self-Organizing Heuristics Movement

```
1. Move-to-Front Heuristic:
Found element at index 3:  [ A, B, C, TARGET, E ]
Move directly to index 0:  [ TARGET, A, B, C, E ] ⚡

2. Transpose Heuristic:
Found element at index 3:  [ A, B, C, TARGET, E ]
Swap with index 2 (i - 1): [ A, B, TARGET, C, E ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Standard Linear Search, Sentinel Optimization, Move-to-Front Heuristic, Transpose Heuristic, and Multi-Target Occurrence Indexing.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Linear Search Algorithms,
 * Sentinel Optimizations, and Self-Organizing Heuristics.
 */
public class LinearSearchMaster {

    // =========================================================================
    // 1. STANDARD LINEAR SEARCH (O(N) Time, O(1) Space)
    // =========================================================================
    public int standardSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }

    // =========================================================================
    // 2. SENTINEL LINEAR SEARCH (50% Loop Comparison Reduction)
    // =========================================================================
    /**
     * Performs Sentinel Linear Search.
     * Replaces array end check with a temporary sentinel element at last position.
     *
     * @param arr input array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int sentinelSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        int n = arr.length;
        int last = arr[n - 1]; // Save original last element

        // Step 1: Place sentinel at last position
        arr[n - 1] = target;

        int i = 0;
        // Step 2: High-speed loop with ONLY 1 value comparison per step!
        while (arr[i] != target) {
            i++;
        }

        // Step 3: Restore original last element
        arr[n - 1] = last;

        // Step 4: Verify match
        if (i < n - 1 || last == target) {
            return i;
        }

        return -1;
    }

    // =========================================================================
    // 3. MOVE-TO-FRONT SELF-ORGANIZING SEARCH (Temporal Locality Optimization)
    // =========================================================================
    /**
     * Moves found element directly to index 0 to optimize future queries.
     */
    public int moveToFrontSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                if (i > 0) {
                    // Shift elements right and place target at index 0
                    int temp = arr[i];
                    System.arraycopy(arr, 0, arr, 1, i);
                    arr[0] = temp;
                }
                return 0; // Target is now at index 0!
            }
        }
        return -1;
    }

    // =========================================================================
    // 4. TRANSPOSE SELF-ORGANIZING SEARCH (Gradual Frequency Ordering)
    // =========================================================================
    /**
     * Swaps found element with its left neighbor (index i - 1).
     */
    public int transposeSearch(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                if (i > 0) {
                    // Swap with left neighbor
                    int temp = arr[i];
                    arr[i] = arr[i - 1];
                    arr[i - 1] = temp;
                    return i - 1; // New index after swap
                }
                return i;
            }
        }
        return -1;
    }

    // =========================================================================
    // 5. MULTI-TARGET ALL OCCURRENCES SEARCH
    // =========================================================================
    /**
     * Returns all indices matching target.
     */
    public List<Integer> findAllOccurrences(int[] arr, int target) {
        List<Integer> indices = new ArrayList<>();
        if (arr == null || arr.length == 0) return indices;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                indices.add(i);
            }
        }
        return indices;
    }
}
```

> **Quick Syntax:**
```java
// Sentinel Loop Line (Single Value Comparison)
arr[n - 1] = target; int i = 0; while (arr[i] != target) i++; arr[n - 1] = last;
```

---

## 7. Concrete Problem Examples & Applications

1. **Unordered In-Memory Scanning**:
   - Searching unsorted array lists or linked lists ($O(N)$).

2. **Self-Organizing Cache Lists**:
   - LRU Cache List Reordering via Move-to-Front Heuristic.
   - Frequency-Based Symbol Tables via Transpose Heuristic.

3. **Compiler Keyword Validation**:
   - Scanning small fixed array sets (e.g. 30 C keywords) where linear scan cache locality beats binary search branch overhead.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class LinearSearchDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     LINEAR SEARCH VARIANTS DEMONSTRATION        ");
        System.out.println("=================================================\n");

        LinearSearchMaster master = new LinearSearchMaster();

        // 1. Sentinel Search Test
        int[] arr1 = {42, 15, 8, 99, 23};
        int target = 8;
        int sentinelIdx = master.sentinelSearch(arr1, target);
        System.out.println("1. Sentinel Search Target " + target + " in " + Arrays.toString(arr1) + ": Index = " + sentinelIdx);
        System.out.println("-------------------------------------------------");

        // 2. Move-to-Front Heuristic Test
        int[] arr2 = {42, 15, 8, 99, 23};
        System.out.println("2. Move-to-Front Search for Target " + target + ":");
        System.out.println("   Original Array: " + Arrays.toString(arr2));
        master.moveToFrontSearch(arr2, target);
        System.out.println("   After 1st Search: " + Arrays.toString(arr2) + " (Target moved to index 0!)");
        System.out.println("-------------------------------------------------");

        // 3. Multi-Occurrence Search Test
        int[] arr3 = {5, 2, 8, 5, 9, 5, 1};
        List<Integer> occurrences = master.findAllOccurrences(arr3, 5);
        System.out.println("3. All Occurrences of 5 in " + Arrays.toString(arr3) + ": Indices = " + occurrences);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Linear Search Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | CPU Cache Benefit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Search** | $\mathbf{O(1)}$ Constant | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | Baseline |
| **Sentinel Search** | $\mathbf{O(1)}$ Constant | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | **50% Loop Cut ⚡**|
| **Move-to-Front**   | $\mathbf{O(1)}$ Amortized | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | **High Temporal ⚡**|
| **Transpose Search**| $\mathbf{O(1)}$ Amortized | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Linear | $\mathbf{O(1)}$ Constant ⚡ | Gradual Frequency |

---

## 10. Edge Cases & Boundary Handling

1. **Target at Index 0**:
   - `moveToFrontSearch` and `transposeSearch` check `i > 0` before swapping, handling index 0 safely without out-of-bounds errors.

2. **Target at Last Index $N - 1$**:
   - Sentinel Search saves `last = arr[n - 1]`, sets `arr[n - 1] = target`, and verifies `last == target` cleanly.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Restore Array Element in Sentinel Search**:
  - Failing to restore `arr[n - 1] = last` mutates the input array permanently and corrupts subsequent data operations.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Small Fixed Arrays Prefer Linear Search:
> For small datasets ($N \le 32$ items), Linear Search outperforms Binary Search on modern hardware!
> Binary Search introduces CPU branch mispredictions and non-sequential memory accesses. Linear Search reads contiguous memory blocks sequentially, maximizing CPU L1 cache line hits! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard Linear Search | Sentinel Linear Search | Move-to-Front Heuristic |
| :--- | :--- | :--- | :--- |
| **Loop Overhead** | 2 Comparisons / Step | **1 Comparison / Step ⚡**| 2 Comparisons + Shift |
| **Array Mutation**| None                   | Temporary (Restored)   | **Permanent Reordering ⚡**|
| **Repeated Query Cost**| $O(N)$ per query    | $O(N)$ per query       | **$O(1)$ Amortized ⚡** |

---

## 14. How to Recognize This in Questions

* **"Search unsorted array with high temporal query locality"** $\rightarrow$ Move-to-Front Linear Search.
* **"Optimize single-pass scanning loop overhead"** $\rightarrow$ Sentinel Linear Search.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Sentinel Linear Search reduce loop comparisons by 50%?**  
  *A:* By placing the target key at the last index, the loop is guaranteed to find a match without needing an explicit index boundary check `i < N`. The loop condition simplifies from `while (i < N && arr[i] != target)` to `while (arr[i] != target)`.

* **Q: What is the difference between Move-to-Front and Transpose heuristics?**  
  *A:* Move-to-Front moves a found item directly to index 0 (aggressive temporal optimization). Transpose swaps a found item with its left neighbor $i-1$ (gradual frequency ordering).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: LINEAR SEARCH VARIANTS                                |
+-----------------------------------------------------------------------+
| • Standard Search : 2 comparisons per step (bound check + value match)|
| • Sentinel Search : Place target at arr[n-1] -> 1 comparison per step! |
| • Move-to-Front   : Move found element to index 0 for repeated queries|
| • Transpose       : Swap found element with left neighbor (i - 1)     |
| • Small Data Opt  : Linear search beats binary search for N <= 32! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Sentinel Linear Search in Java with array restoration.
- [ ] I can explain how Sentinel Search cuts loop comparisons by 50%.
- [ ] I can write Move-to-Front and Transpose self-organizing search heuristics.
- [ ] I can explain why small arrays ($N \le 32$) prefer linear search over binary search.
- [ ] I can write a multi-occurrence index collector in Java.
