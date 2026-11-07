# 12. Pattern Recognition & Searching Triggers: Identifying Algorithmic Archetypes

## 1. Introduction
High-speed problem-solving in technical coding interviews requires rapid **Searching Pattern Recognition**. Rather than analyzing every searching problem from scratch, experienced engineers map problem descriptions directly to one of six universal **Searching Master Archetypes**: **Template 1 Exact Search**, **Template 2 Boundary Search (Lower/Upper Bound)**, **Slope Predicate Peak Search**, **Rotated Sorted Array Search**, **Binary Search on Answer (Feasibility Optimization)**, and **2D Matrix Searching (Virtual 1D / Staircase Scan)**. Recognizing structural key phrases in problem specifications enables instant selection of optimal loop invariants, mid-pointer formulas, and subproblem elimination directions.

> **Important:** The 6 Universal Searching Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Exact Match Binary Search**: Trigger = *"Search target in sorted array"*. Loop = `while (low <= high)`. Code = `high = mid - 1` / `low = mid + 1`. Time = $O(\log N)$.
> 2. **Pattern 2: Boundary Search (Lower / Upper Bound)**: Trigger = *"Find first/last occurrence, insertion position, or frequency count"*. Loop = `while (low < high)`. Code = `high = mid`. Time = $O(\log N)$.
> 3. **Pattern 3: Slope Predicate Search**: Trigger = *"Find local peak or single non-duplicate in unsorted/partially-sorted array"*. Predicate = `nums[mid] < nums[mid + 1]`. Time = $O(\log N)$.
> 4. **Pattern 4: Rotated Array Search**: Trigger = *"Search in array shifted around a pivot point"*. Invariant = Identify sorted half `nums[low] <= nums[mid]`. Time = $O(\log N)$.
> 5. **Pattern 5: Binary Search on Answer**: Trigger = *"Find minimum speed/capacity or maximize minimum distance to satisfy condition"*. Helper = `isPossible(mid)`. Time = $O(N \log (\text{Range}))$.
> 6. **Pattern 6: 2D Matrix Search**: Trigger = *"Search in 2D sorted grid"*. Virtual 1D = `mid / cols, mid % cols` or Staircase = Top-Right Corner `(0, cols - 1)`. Time = $O(\log(M \cdot N))$ or $O(M + N)$. ⚡

```
Searching Master Archetype Decision Tree Topography:
Problem Description Trigger Signal:
├── "Search target in 1D sorted array?" ──────────────────> Pattern 1: Exact Match BS
├── "Find first/last position or insertion index?" ────────> Pattern 2: Boundary (Lower/Upper Bound)
├── "Find local peak / single element?" ──────────────────> Pattern 3: Slope Predicate Search
├── "Search in array shifted around pivot?" ──────────────> Pattern 4: Rotated Array Search
├── "Find min capacity / max min distance for condition?" -> Pattern 5: Binary Search on Answer
└── "Search target in 2D grid matrix?" ───────────────────> Pattern 6: 2D Matrix Searching ⚡
```

---

## 2. Core Concepts & Master Pattern Strategy Matrix

### 2.1 Searching Master Pattern Recognition Matrix
```
Master Searching Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Mid Invariant     | Primary Mechanism |
+-----------------------+-------------------+-------------------+-------------------+
| **1. Exact Match**    | "Search target"   | `low <= high`     | `high = mid - 1`  |
| **2. Boundary Search**| "First / Last pos"| `low < high`      | `high = mid`      |
| **3. Slope Predicate**| "Find local peak" | `nums[mid] < right`| Follow higher slope|
| **4. Rotated Search** | "Shifted pivot"   | `nums[low]<=mid`  | Check sorted half |
| **5. Search on Answer**| "Min capacity"   | `isPossible(mid)` | Feasibility helper|
| **6. 2D Matrix Search**| "Sorted 2D grid" | `mid / cols`      | Virtual 1D / Stairs|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Search target = Exact BS; First/Last = Lower Bound; Min capacity = Search on Answer!"**

---

## 3. Deep Dive into the 6 Searching Archetypes

### 3.1 Archetype 1: Exact Match Binary Search
* **Trigger Words**: *"Find index of target in sorted array..."*, *"Binary search exact key..."*
* **Template**: `while (low <= high)` with `mid = low + (high - low) / 2`.
* **Invariants**: If `nums[mid] == target` return `mid`. If `<` shift `low = mid + 1`, if `>` shift `high = mid - 1`.

### 3.2 Archetype 2: Boundary Search (Lower / Upper Bound)
* **Trigger Words**: *"Search insert position..."*, *"Find first and last occurrence..."*, *"Count frequency in O(log N)..."*
* **Template**: `while (low < high)` with `high = arr.length`.
* **Invariants**: Lower bound `if (arr[mid] >= target) high = mid; else low = mid + 1;`. Upper bound `if (arr[mid] > target) high = mid; else low = mid + 1;`.

### 3.3 Archetype 5: Binary Search on Answer
* **Trigger Words**: *"Find minimum speed K..."*, *"Capacity to ship within D days..."*, *"Maximize minimum distance..."*
* **Template**: Search range $[low, high]$ over candidate answers. Helper `isPossible(mid)`.
* **Invariants**: Minimize Maximum $\implies$ Search FIRST `TRUE` (`high = mid - 1`). Maximize Minimum $\implies$ Search LAST `TRUE` (`low = mid + 1`).

---

## 4. Internal Working Mechanics: Matching LeetCode Problems to Archetypes

```
Problem Match Audits:

LeetCode 704 (Binary Search)                  ---> Match Archetype 1: Exact Match BS
LeetCode 35 (Search Insert Position)         ---> Match Archetype 2: Lower Bound (First >= Target)
LeetCode 34 (First and Last Position)         ---> Match Archetype 2: Lower Bound & Upper Bound
LeetCode 162 (Find Peak Element)              ---> Match Archetype 3: Slope Predicate Search
LeetCode 33 (Search in Rotated Sorted Array)  ---> Match Archetype 4: Rotated Sorted Half Check
LeetCode 875 (Koko Eating Bananas)            ---> Match Archetype 5: Binary Search on Answer
LeetCode 74 (Search a 2D Matrix I)            ---> Match Archetype 6: Virtual 1D Matrix Search
```

---

## 5. Visual Diagram: Pattern Selector Flowchart

```
                          [ New Searching Problem ]
                                     │
                         Is it a 2D Matrix / Grid?
                             /                \
                         (Yes)                (No)
                          /                      \
              [ Pattern 6: Matrix Search ]    Is search domain over CANDIDATE ANSWERS?
                                                 /                  \
                                             (Yes)                  (No)
                                              /                        \
                            [ Pattern 5: BS on Answer ]    Is array shifted / rotated around pivot?
                                                                   /                 \
                                                               (Yes)                 (No)
                                                                /                       \
                                                    [ Pattern 4: Rotated BS ]    Are we finding BOUNDARIES (First/Last)?
                                                                                    /                    \
                                                                                (Yes)                    (No)
                                                                                 /                          \
                                                                 [ Pattern 2: Lower/Upper Bound ]  [ Pattern 1: Exact BS ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across all 6 Searching Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating the 6 Searching Algorithmic Archetypes.
 */
public class SearchingPatternRecognitionMaster {

    // =========================================================================
    // PATTERN 1: EXACT MATCH BINARY SEARCH (LeetCode 704 O(log N))
    // =========================================================================
    public int pattern1_ExactMatchBS(int[] arr, int target) {
        if (arr == null || arr.length == 0) return -1;
        int low = 0, high = arr.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }

    // =========================================================================
    // PATTERN 2: BOUNDARY SEARCH (Lower Bound / Search Insert LeetCode 35 O(log N))
    // =========================================================================
    public int pattern2_LowerBound(int[] arr, int target) {
        if (arr == null || arr.length == 0) return 0;
        int low = 0, high = arr.length; // Range [0 ... N]

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] >= target) high = mid;
            else low = mid + 1;
        }
        return low;
    }

    // =========================================================================
    // PATTERN 3: SLOPE PREDICATE SEARCH (Peak Element LeetCode 162 O(log N))
    // =========================================================================
    public int pattern3_SlopePredicatePeak(int[] nums) {
        if (nums == null || nums.length == 0) return -1;
        int low = 0, high = nums.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] < nums[mid + 1]) low = mid + 1; // Slope increasing -> Move right
            else high = mid;                             // Slope decreasing -> Move left
        }
        return low;
    }

    // =========================================================================
    // PATTERN 4: ROTATED ARRAY SEARCH (LeetCode 33 O(log N))
    // =========================================================================
    public int pattern4_RotatedArraySearch(int[] nums, int target) {
        if (nums == null || nums.length == 0) return -1;
        int low = 0, high = nums.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;

            if (nums[low] <= nums[mid]) { // Left half sorted
                if (nums[low] <= target && target < nums[mid]) high = mid - 1;
                else low = mid + 1;
            } else { // Right half sorted
                if (nums[mid] < target && target <= nums[high]) low = mid + 1;
                else high = mid - 1;
            }
        }
        return -1;
    }

    // =========================================================================
    // PATTERN 5: BINARY SEARCH ON ANSWER (Koko Bananas LeetCode 875 O(N log Range))
    // =========================================================================
    public int pattern5_BinarySearchOnAnswer(int[] piles, int h) {
        int low = 1, high = 0;
        for (int p : piles) high = Math.max(high, p);
        int ans = high;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canFinish(piles, mid, h)) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return ans;
    }

    private boolean canFinish(int[] piles, int speed, int h) {
        long hours = 0;
        for (int p : piles) hours += (p + speed - 1) / speed;
        return hours <= h;
    }

    // =========================================================================
    // PATTERN 6: 2D MATRIX SEARCH (LeetCode 74 Virtual 1D BS O(log(M * N)))
    // =========================================================================
    public boolean pattern6_VirtualMatrixSearch(int[][] matrix, int target) {
        if (matrix == null || matrix.length == 0) return false;
        int rows = matrix.length, cols = matrix[0].length;
        int low = 0, high = rows * cols - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int val = matrix[mid / cols][mid % cols]; // Virtual 2D Mapping
            if (val == target) return true;
            else if (val < target) low = mid + 1;
            else high = mid - 1;
        }
        return false;
    }
}
```

> **Quick Syntax:**
```java
// Pattern Recognition Quick Identifier Template
// Trigger: "Search target" -> Pattern 1: Exact Match BS
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Exact Match)**: LeetCode 704 (Binary Search), LeetCode 374 (Guess Number Higher or Lower).
* **Pattern 2 (Boundary Search)**: LeetCode 35 (Search Insert Position), LeetCode 34 (First/Last Position).
* **Pattern 3 (Slope Predicate)**: LeetCode 162 (Find Peak Element), LeetCode 540 (Single Element in Sorted Array).
* **Pattern 4 (Rotated Array)**: LeetCode 33 (Rotated Array I), LeetCode 81 (Rotated Array II), LeetCode 153 (Find Min).
* **Pattern 5 (BS on Answer)**: LeetCode 875 (Koko Bananas), LeetCode 1011 (Ship Packages), LeetCode 1552 (Magnetic Force).
* **Pattern 6 (2D Matrix Search)**: LeetCode 74 (Search 2D Matrix I), LeetCode 240 (Search 2D Matrix II).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class SearchingPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SEARCHING PATTERN RECOGNITION DEMONSTRATION   ");
        System.out.println("=================================================\n");

        SearchingPatternRecognitionMaster master = new SearchingPatternRecognitionMaster();

        // 1. Pattern 1 Test (Exact BS)
        int[] sorted = {2, 5, 8, 12, 16, 23, 38};
        int t1 = 23;
        int idx1 = master.pattern1_ExactMatchBS(sorted, t1);
        System.out.println("1. Pattern 1 (Exact BS) Search Target " + t1 + ": Index = " + idx1);
        System.out.println("-------------------------------------------------");

        // 2. Pattern 2 Test (Lower Bound / Search Insert)
        int t2 = 10;
        int insertIdx = master.pattern2_LowerBound(sorted, t2);
        System.out.println("2. Pattern 2 (Lower Bound) Search Insert for " + t2 + ": Index = " + insertIdx);
        System.out.println("-------------------------------------------------");

        // 3. Pattern 4 Test (Rotated Array Search)
        int[] rotated = {4, 5, 6, 7, 0, 1, 2};
        int t4 = 0;
        int rotIdx = master.pattern4_RotatedArraySearch(rotated, t4);
        System.out.println("3. Pattern 4 (Rotated Search) Target " + t4 + " in " + Arrays.toString(rotated) + ": Index = " + rotIdx);
        System.out.println("-------------------------------------------------");

        // 4. Pattern 5 Test (BS on Answer Koko Bananas)
        int[] piles = {3, 6, 7, 11};
        int h = 8;
        int minSpeed = master.pattern5_BinarySearchOnAnswer(piles, h);
        System.out.println("4. Pattern 5 (BS on Answer) Min Speed for Piles " + Arrays.toString(piles) + ": Speed = " + minSpeed);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Master Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Exact Match** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | "Search target in sorted array" |
| **2. Boundary Search**| $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | "First/last position or insert index" |
| **3. Slope Predicate**| $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | "Find local peak / single element" |
| **4. Rotated Search** | $\mathbf{O(\log N)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | "Array shifted around pivot" |
| **5. BS on Answer**   | $\mathbf{O(N \log (\text{Range}))}$| $\mathbf{O(1)}$ Constant ⚡ | "Find min capacity / max min distance" |
| **6. 2D Matrix Search**| $\mathbf{O(\log(M \cdot N))}$ ⚡| $\mathbf{O(1)}$ Constant ⚡ | "Search in sorted 2D grid" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Pattern 1 (Exact Match) and Pattern 2 (Boundary Search)**:
   - If array contains **unique values** and problem asks for exact match $\implies$ Use Pattern 1 (`while (low <= high)`).
   - If array contains **duplicates** or problem asks for first/last occurrence / insert position $\implies$ Use Pattern 2 (`while (low < high)`).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Pattern 1 to Range Boundary Search Problems**:
  - Using Pattern 1 (`while (low <= high)`) for finding the first occurrence of a duplicate target requires extra linear scanning after finding a match, ruining $O(\log N)$ performance.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Searching Pattern Selector:
> 1. Check array structure: Rotated? $\to$ Pattern 4; 2D Grid? $\to$ Pattern 6; Unsorted Slope? $\to$ Pattern 3.
> 2. Check search domain: Searching candidate answer values $[low, high]$? $\to$ Pattern 5 (BS on Answer).
> 3. Check output requirements: First/Last occurrence? $\to$ Pattern 2 (Lower Bound). Exact match? $\to$ Pattern 1. ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Search Domain | Midpoint Strategy | Loop Condition |
| :--- | :--- | :--- | :--- |
| **Pattern 1 (Exact Match)** | 1D Sorted Array | Subtraction Offset | `while (low <= high)` |
| **Pattern 2 (Boundary Search)**| 1D Sorted Array | Subtraction Offset | `while (low < high)` |
| **Pattern 5 (BS on Answer)** | Candidate Values Range | Range Midpoint | `while (low <= high)` + Helper |

---

## 14. How to Recognize This in Questions

* **"Search target in sorted array"** $\rightarrow$ Pattern 1 (Exact BS).
* **"Search insert position"** $\rightarrow$ Pattern 2 (Lower Bound).
* **"Find minimum capacity to complete task"** $\rightarrow$ Pattern 5 (BS on Answer).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Pattern 2 (Boundary Search) initialize `high = arr.length` instead of `arr.length - 1`?**  
  *A:* To allow the algorithm to return index $N$ when the target is larger than all elements, serving as a valid insertion index at the end of the array.

* **Q: Why does Pattern 5 (Binary Search on Answer) operate on unsorted arrays?**  
  *A:* Because the search space is NOT the input array! The search space is the candidate answer range $[low, high]$, which is strictly monotonic.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEARCHING PATTERN RECOGNITION                         |
+-----------------------------------------------------------------------+
| • Pattern 1: Exact Match BS      -> "Search target" (low <= high)     |
| • Pattern 2: Lower / Upper Bound -> "First/last position" (low < high)|
| • Pattern 3: Slope Predicate     -> "Find local peak" (nums[mid]<right)|
| • Pattern 4: Rotated Array Search-> "Shifted pivot" (nums[low]<=mid)  |
| • Pattern 5: BS on Answer        -> "Min capacity / Max min distance" |
| • Pattern 6: 2D Matrix Search    -> "Virtual 1D mid / cols, mid % cols"⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any searching problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I know when to use Pattern 1 (Exact Match) vs Pattern 2 (Boundary Search).
- [ ] I can identify Binary Search on Answer problems by checking if the candidate answer range is monotonic.
- [ ] I can write Pattern 4 Rotated Sorted Array search in Java.
- [ ] I can write Pattern 6 2D Matrix Virtual Binary Search.
