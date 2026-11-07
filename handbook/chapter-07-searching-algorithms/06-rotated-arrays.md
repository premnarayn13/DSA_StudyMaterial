# 06. Rotated Sorted Arrays: Sorted Half Invariants & Duplicate Degradation

## 1. Introduction
**Rotated Sorted Array Search** is one of the most critical binary search domains in technical interview evaluations. A rotated sorted array is formed by shifting a strictly ascending array around a pivot point (e.g. $[0, 1, 2, 4, 5, 6, 7] \to [4, 5, 6, 7, 0, 1, 2]$). Benchmark problems include **Search in Rotated Sorted Array I (LeetCode 33)**, **Search in Rotated Sorted Array II with Duplicates (LeetCode 81)**, and **Find Minimum in Rotated Sorted Array (LeetCode 153/154)**. By exploiting the **Sorted Half Invariant** (at least one half $[low \dots mid]$ or $[mid \dots high]$ MUST be strictly sorted), rotated array search executes in **$O(\log N)$ Time** and **$O(1)$ Space**.

> **Important:** Core Invariants of Rotated Array Search:
> 1. **Sorted Half Identification Invariant**:
>    - If `nums[low] <= nums[mid]`: The **LEFT HALF $[low \dots mid]$ is strictly sorted**!
>    - Otherwise (`nums[low] > nums[mid]`): The **RIGHT HALF $[mid \dots high]$ is strictly sorted**!
> 2. **Target Range Containment Check**:
>    - Once the sorted half is identified, check if `target` lies within the bounds of that sorted half:
>      - If YES: Narrow search to that sorted half.
>      - If NO: Search the opposite rotated half!
> 3. **Duplicate Degradation (LeetCode 81 & 154)**:
>    - When `nums[low] == nums[mid] == nums[high]`, duplicate values prevent identifying which half is sorted. Shrink boundary `low++` / `high--`, degrading worst-case time to **$O(N)$**. ⚡

```
Rotated Array Sorted Half Topology (nums = [4, 5, 6, 7, 0, 1, 2], Target = 0):
Low = 0 (val 4), Mid = 3 (val 7), High = 6 (val 2)

Check Sorted Half:  nums[low] (4) <= nums[mid] (7) ---> LEFT HALF [4, 5, 6, 7] is SORTED!
Check Target 0:     Is 0 in range [4 ... 7]? NO!
Decision:           Target MUST lie in Right Half [0, 1, 2] -> Set low = mid + 1 (4)!

Target 0 Found at Index 4 in O(log N) Steps! ⚡
```

---

## 2. Core Concepts & Rotated Array Problem Matrix

### 2.1 Rotated Array Strategy Matrix
```
Rotated Array Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Key Invariant     | Duplicate Handling| Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Search Rotated I(33)**| Sorted Half Check| Distinct values   | **$O(\log N)$ Log ⚡**|
| **Search Rotated II(81)**| Sorted Half Check| `low++ / high--`  | **$O(\log N)$ Avg / $O(N)$ Worst**|
| **Find Minimum (153)**| `nums[mid] > nums[high]`| Shift right `low = mid + 1`| **$O(\log N)$ Log ⚡**|
| **Find Min II (154)** | `nums[mid] == nums[high]`| `high--`         | **$O(\log N)$ Avg / $O(N)$ Worst**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Check nums[low] <= nums[mid] to find sorted half! If duplicates make low == mid == high -> shrink bounds!"**

---

## 3. Characteristics & Duplicate Time Complexity Degradation Proof

### 3.1 Mathematical Proof of $O(N)$ Duplicate Degradation
* In LeetCode 81 / 154 with duplicates (e.g. `[1, 1, 1, 1, 1, 2, 1, 1]`), `nums[low] == nums[mid] == nums[high] = 1`.
* It is impossible to determine whether the rotation pivot lies to the left or right of `mid`.
* The algorithm can only shrink the search space linearly by 1 element per step:
  $$T(N) = T(N - 1) + O(1) \implies \mathbf{O(N) \text{ Worst-Case Time Complexity}}$$
* For unique elements (LeetCode 33 / 153), every step halves the search space: $\mathbf{O(\log N) \text{ Strict Logarithmic Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Find Minimum in Rotated Array

Tracing LeetCode 153 (Find Minimum in Rotated Sorted Array) on `nums = [4, 5, 6, 7, 0, 1, 2]`:

```
Goal: Find the rotation pivot / minimum element.

Init: low = 0 (val 4), high = 6 (val 2).

Step 1: mid = 3 (val = 7).
        Compare nums[mid] (7) with nums[high] (2):
        7 > 2 ---> Minimum MUST lie to the RIGHT of mid!
        Set low = mid + 1 (4). Search range: [4 ... 6].

Step 2: low = 4 (val 0), high = 6 (val 2).
        mid = 5 (val = 1).
        Compare nums[mid] (1) with nums[high] (2):
        1 <= 2 ---> Minimum lies at mid or to the LEFT!
        Set high = mid (5). Search range: [4 ... 5].

Step 3: low = 4 (val 0), high = 5 (val 1).
        mid = 4 (val = 0).
        Compare nums[mid] (0) with nums[high] (1):
        0 <= 1 ---> Set high = mid (4). Search range: [4 ... 4].

Loop terminates (low == high == 4).
Minimum Element = nums[4] = 0! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram: Rotated Array Structural Topography

```
Rotated Array Elevation Profile:

Value
  7 |        /|
  6 |       / |
  5 |      /  |
  4 |     /   |
  1 |    /    |          /
  0 |   /     |_________/ (Pivot / Minimum Element)
    +-----------------------
        Left Half     Right Half
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 33 (Search in Rotated Sorted Array), LeetCode 81 (With Duplicates), LeetCode 153 (Find Minimum), and LeetCode 154 (Find Minimum with Duplicates).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Rotated Array Searching Algorithms,
 * Sorted Half Invariants, and Duplicate Handling Mechanics.
 */
public class RotatedArraysMaster {

    // =========================================================================
    // 1. SEARCH IN ROTATED SORTED ARRAY I (LeetCode 33 Unique Elements O(log N))
    // =========================================================================
    /**
     * Searches target in rotated sorted array with unique elements.
     * LeetCode 33 Solution.
     *
     * @param nums rotated sorted array
     * @param target search key
     * @return index of target or -1 if absent
     */
    public int search(int[] nums, int target) {
        if (nums == null || nums.length == 0) return -1;

        int low = 0;
        int high = nums.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (nums[mid] == target) {
                return mid; // Found target!
            }

            // Step 1: Identify which half is strictly sorted
            if (nums[low] <= nums[mid]) {
                // LEFT HALF [low ... mid] is strictly sorted!
                if (nums[low] <= target && target < nums[mid]) {
                    high = mid - 1; // Target lies within sorted left half
                } else {
                    low = mid + 1;  // Target lies in right half
                }
            } else {
                // RIGHT HALF [mid ... high] is strictly sorted!
                if (nums[mid] < target && target <= nums[high]) {
                    low = mid + 1;  // Target lies within sorted right half
                } else {
                    high = mid - 1; // Target lies in left half
                }
            }
        }

        return -1;
    }

    // =========================================================================
    // 2. SEARCH IN ROTATED SORTED ARRAY II (LeetCode 81 With Duplicates O(log N) Avg)
    // =========================================================================
    /**
     * Searches target in rotated sorted array with duplicate elements.
     * LeetCode 81 Solution. Handles low == mid == high duplicate ambiguity.
     */
    public boolean searchWithDuplicates(int[] nums, int target) {
        if (nums == null || nums.length == 0) return false;

        int low = 0;
        int high = nums.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (nums[mid] == target) return true;

            // Duplicate Ambiguity Resolution: Shrink bounds when low == mid == high
            if (nums[low] == nums[mid] && nums[mid] == nums[high]) {
                low++;
                high--;
            } else if (nums[low] <= nums[mid]) {
                // Left half sorted
                if (nums[low] <= target && target < nums[mid]) {
                    high = mid - 1;
                } else {
                    low = mid + 1;
                }
            } else {
                // Right half sorted
                if (nums[mid] < target && target <= nums[high]) {
                    low = mid + 1;
                } else {
                    high = mid - 1;
                }
            }
        }

        return false;
    }

    // =========================================================================
    // 3. FIND MINIMUM IN ROTATED SORTED ARRAY (LeetCode 153 O(log N))
    // =========================================================================
    /**
     * Finds minimum element in rotated sorted array of unique values.
     * LeetCode 153 Solution.
     */
    public int findMin(int[] nums) {
        if (nums == null || nums.length == 0) return -1;

        int low = 0;
        int high = nums.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;

            // Compare mid with high to determine minimum side
            if (nums[mid] > nums[high]) {
                low = mid + 1; // Minimum lies to the right of mid
            } else {
                high = mid; // Minimum lies at mid or to the left
            }
        }

        return nums[low];
    }
}
```

> **Quick Syntax:**
```java
// Sorted Half Check Line
if (nums[low] <= nums[mid]) { /* Left Sorted */ } else { /* Right Sorted */ }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 33 - Search in Rotated Sorted Array**:
   - Primary rotated searching benchmark ($O(\log N)$).

2. **LeetCode 81 - Search in Rotated Sorted Array II**:
   - Duplicate-tolerant rotated searching ($O(\log N)$ avg / $O(N)$ worst).

3. **LeetCode 153 / 154 - Find Minimum in Rotated Array**:
   - Locating rotation pivot offset in high-speed circular buffers.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class RotatedArraysDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ROTATED SORTED ARRAY SEARCH DEMONSTRATION     ");
        System.out.println("=================================================\n");

        RotatedArraysMaster master = new RotatedArraysMaster();

        // 1. Search Unique Rotated Array (LeetCode 33)
        int[] nums1 = {4, 5, 6, 7, 0, 1, 2};
        int target1 = 0;
        int idx1 = master.search(nums1, target1);
        System.out.println("1. Search Target " + target1 + " in Rotated Array " + Arrays.toString(nums1) + ":");
        System.out.println("   Target Index: " + idx1 + " (Value = " + nums1[idx1] + ")");
        System.out.println("-------------------------------------------------");

        // 2. Search With Duplicates (LeetCode 81)
        int[] nums2 = {2, 5, 6, 0, 0, 1, 2};
        int target2 = 0;
        boolean exists = master.searchWithDuplicates(nums2, target2);
        System.out.println("2. Search Target " + target2 + " with Duplicates " + Arrays.toString(nums2) + ":");
        System.out.println("   Target Exists: " + exists);
        System.out.println("-------------------------------------------------");

        // 3. Find Minimum Element (LeetCode 153)
        int minVal = master.findMin(nums1);
        System.out.println("3. Minimum Element in " + Arrays.toString(nums1) + ": " + minVal);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Rotated Variant | Time (Unique) | Time (Duplicates) | Auxiliary Space | Key Identification Check |
| :--- | :--- | :--- | :--- | :--- |
| **Search Target (33/81)**| **$O(\log N)$ Log ⚡**| $O(N)$ Worst Case | **$O(1)$ Constant Space ⚡**| `nums[low] <= nums[mid]` |
| **Find Minimum (153/154)**| **$O(\log N)$ Log ⚡**| $O(N)$ Worst Case | **$O(1)$ Constant Space ⚡**| `nums[mid] > nums[high]` |

---

## 10. Edge Cases & Boundary Handling

1. **Un-rotated Array (`[1, 2, 3, 4, 5]`)**:
   - `nums[low] <= nums[mid]` holds true. Target range check operates normally as standard binary search.

2. **Array of Size 1 or 2**:
   - Single-element arrays (`[1]`) terminate immediately at `low == high`.

3. **All Duplicate Elements (`[1, 1, 1, 1]`)**:
   - Handled safely by `low++` and `high--` shrinking without index exceptions.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Comparing `nums[mid]` with `nums[low]` in Find Minimum**:
  - In Find Minimum (LeetCode 153), comparing `nums[mid]` with `nums[low]` fails on un-rotated arrays like `[1, 2, 3]`.
  - **ALWAYS compare `nums[mid]` with `nums[high]` for Find Minimum**.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Rules of Rotated Binary Search:
> 1. **Rule 1 (Search Target)**: Compare `nums[low]` with `nums[mid]` to find which half is sorted.
> 2. **Rule 2 (Find Minimum)**: Compare `nums[mid]` with `nums[high]` to determine if minimum lies left or right of `mid`. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Rotated Binary Search | Linear Scan Search |
| :--- | :--- | :--- |
| **Time Complexity (Unique)** | **$O(\log N)$ Logarithmic ⚡** | $O(N)$ Linear |
| **Time Complexity (Duplicates)**| $O(N)$ Worst Case | $O(N)$ Worst Case |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| **$O(1)$ Constant Space ⚡** |

---

## 14. How to Recognize This in Questions

* **"Search element in sorted array that was shifted around a pivot"** $\rightarrow$ LeetCode 33 / 81.
* **"Find minimum element / pivot in rotated sorted array"** $\rightarrow$ LeetCode 153 / 154.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does `nums[low] <= nums[mid]` guarantee the left half is sorted?**  
  *A:* Because a rotated sorted array consists of two sorted sub-sequences. If `nums[low] <= nums[mid]`, no rotation pivot can exist between `low` and `mid`, proving the left half is unbroken and strictly sorted.

* **Q: Why do duplicates cause worst-case time complexity to degrade to $O(N)$?**  
  *A:* When `nums[low] == nums[mid] == nums[high]`, it is impossible to determine whether the rotation pivot lies to the left or right, forcing $O(1)$ incremental boundary steps (`low++` / `high--`).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: ROTATED SORTED ARRAYS                                 |
+-----------------------------------------------------------------------+
| • Sorted Half Check : if (nums[low] <= nums[mid]) -> Left is Sorted!  |
| • Target Range Check: Check if target lies in sorted half bounds      |
| • Find Min Check    : if (nums[mid] > nums[high]) low = mid + 1        |
| • Duplicate Guard   : if (low == mid == high) low++; high--;          |
| • Performance       : O(log N) Time for unique values! ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 33 (`Search in Rotated Sorted Array`) in $O(\log N)$ time.
- [ ] I can write LeetCode 81 (`Search in Rotated Array II`) with duplicate handling.
- [ ] I can write LeetCode 153 (`Find Minimum in Rotated Sorted Array`).
- [ ] I know why `nums[mid]` is compared with `nums[high]` for Find Minimum.
- [ ] I can trace sorted half identification step by step.
