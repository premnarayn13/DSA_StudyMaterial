# 10. Coordinate Compression Technique

## 1. Introduction
**Coordinate Compression** is an advanced array technique that maps large, sparse, or negative value coordinates into small, dense, 0-indexed rank values while strictly preserving their relative ordering. In technical coding interviews and competitive programming, coordinate compression allows algorithms with space dependencies like Segment Trees, Fenwick Trees, or Frequency Arrays (which fail when values are $10^9$ or negative) to run in **$O(N \log N)$ time and $O(N)$ space**.

> **Important:** When array element values are huge ($10^9$) or negative, allocating a frequency array of size $10^9$ causes an `OutOfMemoryError`. Coordinate compression maps $N$ arbitrary values to compressed ranks $0, 1, 2, \dots, K-1$ (where $K \le N$).

## 2. Core Concepts
* **Relative Order Preservation**: If element $A < B$ in the original array, then $\text{compressed}(A) < \text{compressed}(B)$ in the transformed array.
* **Rank Mapping**: Each unique element in the sorted array is assigned a 0-based rank index $0, 1, 2, \dots, K-1$.
* **Compression Pipeline**:
  1. Clone input array and **Sort** the copy: $O(N \log N)$ time.
  2. Remove duplicates or map unique sorted elements to 0-based ranks using a HashMap or Binary Search: $O(N)$ or $O(N \log N)$ time.
  3. Replace original array values with their compressed ranks: $O(N)$ time.

> **Memory Trick:** **"Sort Copy -> De-duplicate -> Map to Ranks (0..K-1)"**.

## 3. Characteristics / Properties
* **Range Reduction**: Transforms arbitrary value ranges ($[-10^9, 10^9]$) into bounded integer ranks ($[0, N-1]$).
* **Information Retention**: Retains relative inequality relationships ($<, >, ==$) while stripping absolute magnitude values.

```
Coordinate Compression Reduction Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Metric                | Original Array    | Compressed Array  | Impact / Benefit  |
+-----------------------+-------------------+-------------------+-------------------+
| Value Range           | [-10⁹, 10⁹]       | [0, N - 1]        | Fits in Array Index|
| Memory for Freq Array | IMPOSSIBLE (OOM)  | O(N) Array        | Enables Freq Array|
| Relative Order        | Preserved         | Preserved         | Exact Same Logic  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Coordinate Compression on `nums = [1000000, -500, 1000000, 42, -500]` ($N = 5$):

### Step 1: Copy and Sort Unique Elements
Unique sorted values: `[-500, 42, 1000000]`

### Step 2: Assign 0-Based Rank Mapping
* `-500` $\to$ Rank `0`
* `42` $\to$ Rank `1`
* `1000000` $\to$ Rank `2`

### Step 3: Replace Original Array Values with Ranks
* `nums[0] = 1000000` $\to$ `2`
* `nums[1] = -500` $\to$ `0`
* `nums[2] = 1000000` $\to$ `2`
* `nums[3] = 42` $\to$ `1`
* `nums[4] = -500` $\to$ `0`

Final Compressed Array: **`[2, 0, 2, 1, 0]`** ✅  
*(Relative order preserved: $-500 < 42 < 1000000 \implies 0 < 1 < 2$).*

## 5. Visual Diagram
Coordinate Compression Mapping Pipeline:

```
Original Values:    [ 1,000,000 ][ -500 ][ 1,000,000 ][ 42 ][ -500 ]
                           |         |         |        |      |
                           v         v         v        v      v
Rank Lookup Map:        [  Map: -500->0, 42->1, 1,000,000->2  ]
                           |         |         |        |      |
                           v         v         v        v      v
Compressed Values:  [     2     ][   0  ][     2     ][ 1  ][  0   ]
```

## 6. Operations / Algorithms
Coordinate Compression Master Implementation (HashMap Approach):

```java
public static int[] compressCoordinates(int[] nums) {
    int n = nums.length;
    int[] sortedCopy = nums.clone();
    Arrays.sort(sortedCopy);

    // Map unique sorted values to 0-based ranks
    Map<Integer, Integer> rankMap = new HashMap<>();
    int rank = 0;
    for (int val : sortedCopy) {
        if (!rankMap.containsKey(val)) {
            rankMap.put(val, rank++);
        }
    }

    // Replace original values with ranks
    int[] compressed = new int[n];
    for (int i = 0; i < n; i++) {
        compressed[i] = rankMap.get(nums[i]);
    }
    return compressed;
}
```

> **Quick Syntax:**
```java
// Alternative Binary Search Compression (Zero HashMap Overhead)
int[] sortedUnique = Arrays.stream(nums).distinct().sorted().toArray();
int rank = Arrays.binarySearch(sortedUnique, originalVal); // Returns 0-based rank
```

## 7. Examples
* **LeetCode 1331 - Rank Transform of an Array**: Standard coordinate compression problem.
* **Count Inversions / Smaller Elements After Self (LeetCode 315)**: Coordinate compression + Fenwick Tree / Segment Tree.
* **Rectangle Area II / Line Sweep Algorithms**: Compressing 2D grid coordinates for line sweep area computation.

## 8. Java Code
Complete interview-ready Java suite demonstrating HashMap Coordinate Compression, Binary Search Compression, and Rank Transformation:

```java
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class CoordinateCompressionMaster {

    // 1. HashMap Approach: O(N log N) Time, O(N) Space
    public static int[] arrayRankTransform(int[] arr) {
        if (arr == null || arr.length == 0) return new int[0];

        int[] sortedCopy = arr.clone();
        Arrays.sort(sortedCopy);

        // Map unique elements to 1-based or 0-based ranks
        Map<Integer, Integer> rankMap = new HashMap<>();
        int rank = 1; // 1-based ranking (LeetCode 1331 standard)

        for (int val : sortedCopy) {
            if (!rankMap.containsKey(val)) {
                rankMap.put(val, rank++);
            }
        }

        // Replace original values with ranks
        int[] result = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            result[i] = rankMap.get(arr[i]);
        }

        return result;
    }

    // 2. Binary Search Approach (No HashMap): O(N log N) Time, O(N) Space
    public static int[] compressWithBinarySearch(int[] arr) {
        if (arr == null || arr.length == 0) return new int[0];

        // Extract unique sorted elements using Java Streams / Arrays
        int[] sortedUnique = Arrays.stream(arr).distinct().sorted().toArray();

        int[] compressed = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            // Binary search returns 0-based rank index in sortedUnique
            compressed[i] = Arrays.binarySearch(sortedUnique, arr[i]);
        }

        return compressed;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums = {40, 10, 20, 30, 10, 40};

        System.out.println("Original: " + Arrays.toString(nums));
        
        // Test HashMap Rank Transform (1-based)
        int[] ranks = arrayRankTransform(nums);
        System.out.println("Rank Transform (1-based): " + Arrays.toString(ranks));
        // Output: [4, 1, 2, 3, 1, 4]

        // Test Binary Search Compression (0-based)
        int[] compressed = compressWithBinarySearch(nums);
        System.out.println("Compressed Ranks (0-based): " + Arrays.toString(compressed));
        // Output: [3, 0, 1, 2, 0, 3]
    }
}
```

## 9. Complexity Analysis
| Step | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Clone & Sort Array** | $O(N \log N)$ | $O(N)$ | Dominant time bottleneck |
| **Rank Map Construction**| $O(N)$ | $O(N)$ | HashMap insertion / De-duplication |
| **Binary Search Rank Lookup**| $O(N \log N)$ | $O(N)$ | Binary search per element |
| **Total Pipeline** | **$O(N \log N)$** | **$O(N)$** | Enables $O(N)$ frequency algorithms |

## 10. Edge Cases
* **Duplicate Elements**: Duplicate elements MUST share the exact same rank! (Guarded by `!rankMap.containsKey(val)`).
* **Negative Coordinates**: Negative numbers compress seamlessly into positive 0-based ranks (`-100000` $\to$ rank `0`).
* **Already Compressed Array**: If input is already `[0, 1, 2]`, output remains `[0, 1, 2]`.

## 11. Common Mistakes
* Incrementing rank on duplicates (e.g., assigning ranks `0, 1, 2` to `[10, 10, 20]` instead of `0, 0, 1`).
* Sorting the original array in-place without cloning (destroys the original array index order!).
* Attempting to compress floating point numbers without handling precision epsilon boundaries.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is Coordinate Compression necessary before using Fenwick Trees / Segment Trees? Fenwick Trees use values as array indices (`tree[val]`). If values are $10^9$, tree size becomes $10^9$ (causes `OutOfMemoryError`). Compressing $N$ values to ranks $0 \dots N-1$ reduces Fenwick Tree size to **$O(N)$** space!

> **Memory Trick:** **"Clone first before sorting!"** Never sort the input array directly if original element positions matter!

## 13. Comparisons
| Feature | HashMap Strategy | Binary Search Strategy |
| :--- | :--- | :--- |
| **De-duplication** | Handled by `rankMap.containsKey()` | Handled by `Arrays.stream().distinct()` |
| **Rank Lookup** | $O(1)$ HashMap get | $O(\log N)$ Binary Search |
| **Memory Footprint**| Slightly higher (HashMap entry objects)| Lower (Primitive arrays only) |
| **Speed** | Fast | Fast |

## 14. How to Recognize This in Questions
* **"Range queries / Fenwick Tree updates with values up to 10^9"** $\rightarrow$ Coordinate Compression ($O(N \log N)$).
* **"Replace elements with their rank order in the array"** $\rightarrow$ Coordinate Compression.

## 15. Frequently Asked Interview Questions
* **Q: Does Coordinate Compression change the mathematical answer for range queries?**  
  *A:* No, provided the query depends on relative ordering ($A < B$) or point counts rather than absolute distances between value magnitudes.
* **Q: How do you invert coordinate compression to get original values back?**  
  *A:* Store the unique sorted elements in an array `sortedUnique[]`. To get the original value of rank $R$, access `sortedUnique[R]` in $O(1)$ time!

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: COORDINATE COMPRESSION                                |
+-----------------------------------------------------------------------+
| • Goal: Map large/negative values [-10⁹, 10⁹] to dense ranks [0..N-1] |
| • Preserves Relative Order: A < B in original => rank(A) < rank(B)   |
| • 3 Steps: Clone & Sort -> Map unique values to ranks -> Replace      |
| • Enables Fenwick Trees & Segment Trees on 10⁹ value ranges           |
| • Reverse Lookup: Original value of rank R = sortedUnique[R]          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain why Coordinate Compression is necessary for Fenwick Trees.
- [ ] I can write the 3-step compression pipeline in under 3 minutes.
- [ ] I know how to handle duplicate elements so they receive identical ranks.
- [ ] I can perform reverse rank lookup to get original values back in $O(1)$.
- [ ] I can solve LeetCode 1331 (Rank Transform of an Array).
