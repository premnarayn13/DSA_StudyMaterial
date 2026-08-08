# 11. Binary Search on Arrays

## 1. Introduction
**Binary Search** is an optimal search paradigm that finds the index of a target value in a sorted array by repeatedly dividing the search space in half. Operating in **$O(\log n)$ time and $O(1)$ auxiliary space**, Binary Search is one of the most essential algorithms tested in technical coding interviews. Beyond simple target lookup, Binary Search extends to finding Lower/Upper bounds, searching in rotated arrays, and solving **Binary Search on Answer Space** problems.

> **Important:** Binary Search requires monotonic search space properties (e.g., sorted array order or monotonic boolean conditions `false ... false true ... true`).

## 2. Core Concepts
* **Halving the Search Space**: In each step, compare `target` with midpoint element `arr[mid]`. Eliminate half the search space based on the comparison.
* **Overflow-Safe Midpoint**: Calculating `mid` as **`int mid = left + (right - left) / 2`** to prevent signed 32-bit integer overflow when `left + right > Integer.MAX_VALUE`.
* **Lower Bound (First Occurrence / Insertion Point)**: Smallest index `i` such that `arr[i] >= target`.
* **Upper Bound**: Smallest index `i` such that `arr[i] > target`.
* **Search Space Boundaries (`while (left <= right)` vs `while (left < right)`)**:
  * `while (left <= right)`: Standard target search where `right = mid - 1` and `left = mid + 1`.
  * `while (left < right)`: Boundary search (Lower/Upper bound) where search space narrows down to a single index `left == right`.

> **Memory Trick:** **"Never write (left + right) / 2! Always write left + (right - left) / 2"**.

## 3. Characteristics / Properties
* **Logarithmic Efficiency**: Reduces search space exponentially: $N \to N/2 \to N/4 \dots \to 1$ in $\log_2 N$ steps. For $N = 10^9$ elements, binary search takes at most **30 comparisons**!
* **Monotonic Condition**: Does NOT strictly require a sorted array—it requires any property that partitions the array into two distinct halves (`true` side and `false` side).

```
Search Paradigm Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Search Paradigm       | Best Case         | Average Case      | Worst Case        |
+-----------------------+-------------------+-------------------+-------------------+
| Linear Search         | Ω(1)              | Θ(n)              | O(n)              |
| Binary Search         | Ω(1) (Hits mid)   | Θ(log n)          | O(log n) (OPTIMAL)|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Lower Bound Binary Search for `target = 4` on `arr = [1, 2, 4, 4, 4, 6, 7]` ($N = 7$):

```
Goal: Find first occurrence index of target 4

Step 1: left = 0, right = 6 -> mid = 0 + (6-0)/2 = 3 (val 4)
        arr[mid] >= target (4 >= 4) -> Save candidate index 3, search left: right = 2

Step 2: left = 0, right = 2 -> mid = 0 + (2-0)/2 = 1 (val 2)
        arr[mid] < target (2 < 4) -> Search right: left = 2

Step 3: left = 2, right = 2 -> mid = 2 + (2-2)/2 = 2 (val 4)
        arr[mid] >= target (4 >= 4) -> Save candidate index 2, search left: right = 1

Loop terminates because left (2) > right (1).
First Occurrence (Lower Bound Index): 2 ✅ (Correct!)
```

## 5. Visual Diagram
Binary Search Halving Visualized:

```
Step 1: [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ][ 60 ][ 70 ]  (left=0, right=6, mid=3, val=40)
                                                    Target = 60 > 40 -> Eliminate Left!
Step 2:                         [ 50 ][ 60 ][ 70 ]  (left=4, right=6, mid=5, val=60)
                                                    Target = 60 == 60 -> FOUND AT INDEX 5! ⚡
```

## 6. Operations / Algorithms
Binary Search Master Templates:

### 1. Standard Target Lookup (`while (left <= right)`)
```java
public int binarySearch(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1; // Target not found
}
```

### 2. Lower Bound / First Occurrence (`while (left <= right)`)
```java
public int lowerBound(int[] nums, int target) {
    int left = 0, right = nums.length - 1;
    int ans = -1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
            ans = mid;    // Record candidate index
            right = mid - 1; // Try to find earlier occurrence on the left
        } else {
            left = mid + 1;
        }
    }
    return ans;
}
```

> **Quick Syntax:**
```java
// Java Built-in Binary Search
int index = Arrays.binarySearch(sortedArr, target);
// If index >= 0: Target found at returned index
// If index < 0: Target missing; insertion point = -(index + 1)
```

## 7. Examples
* **LeetCode 704 - Binary Search**: Standard target lookup on sorted array.
* **LeetCode 34 - Find First and Last Position of Element in Sorted Array**: Lower Bound and Upper Bound binary search.
* **LeetCode 33 - Search in Rotated Sorted Array**: Binary search with pivot condition identification.
* **LeetCode 875 - Koko Eating Bananas**: Binary Search on Answer Space ($O(N \log (\text{Range}))$).

## 8. Java Code
Complete interview-ready Java suite implementing Standard Binary Search, Lower/Upper Bound, and First/Last Occurrence:

```java
import java.util.Arrays;

public class BinarySearchMaster {

    // 1. Standard Binary Search: O(log n) Time, O(1) Space
    public static int search(int[] nums, int target) {
        if (nums == null || nums.length == 0) return -1;

        int left = 0, right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2; // Prevents overflow

            if (nums[mid] == target) return mid;
            if (nums[mid] < target) left = mid + 1;
            else right = mid - 1;
        }

        return -1;
    }

    // 2. Lower Bound (First Occurrence) O(log n)
    public static int findFirstOccurrence(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int firstIndex = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                firstIndex = mid;
                right = mid - 1; // Continue searching left half
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return firstIndex;
    }

    // 3. Upper Bound (Last Occurrence) O(log n)
    public static int findLastOccurrence(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        int lastIndex = -1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                lastIndex = mid;
                left = mid + 1; // Continue searching right half
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return lastIndex;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] sorted = {10, 20, 30, 40, 50, 60, 70};
        System.out.println("Search 50: Index " + search(sorted, 50)); // Output: 4
        System.out.println("Search 99: Index " + search(sorted, 99)); // Output: -1

        int[] duplicates = {1, 2, 4, 4, 4, 5, 6};
        int target = 4;
        int first = findFirstOccurrence(duplicates, target);
        int last = findLastOccurrence(duplicates, target);
        System.out.println("Target 4 Range: [" + first + " ... " + last + "]"); // Output: [2 ... 4]
        System.out.println("Total Frequency of 4: " + (last - first + 1));      // Output: 3
    }
}
```

## 9. Complexity Analysis
| Algorithm Variant | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Iterative Binary Search** | **$O(\log n)$** | **$O(1)$** | Halves search space each step |
| **Recursive Binary Search** | $O(\log n)$ | $O(\log n)$ call stack | Stack frames equal tree height |
| **Lower / Upper Bound** | $O(\log n)$ | $O(1)$ | Continues search after match |
| **Search in Rotated Array** | $O(\log n)$ | $O(1)$ | Identifies which half is sorted |

## 10. Edge Cases
* **Integer Overflow in Midpoint**: Using `(left + right) / 2` overflows when `left + right > 2^31 - 1`. **Always use `left + (right - left) / 2`**.
* **Target Smaller than Minimum / Larger than Maximum**: Binary search terminates cleanly with `left > right`, returning `-1` or insertion index `left`.
* **Array with All Duplicate Values**: E.g., `[4, 4, 4, 4]`. First occurrence logic narrows down to index 0 cleanly.

## 11. Common Mistakes
* Writing `(left + right) / 2` instead of `left + (right - left) / 2`.
* Creating an infinite loop in `while (left < right)` by forgetting `left = mid + 1` or setting `right = mid` incorrectly.
* Using Binary Search on an **unsorted** array without sorting it first!

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `Arrays.binarySearch(arr, key)` in Java returns:
> * Index $\ge 0$ if key is found.
> * Negative value `-(insertionPoint + 1)` if key is NOT found.
> To extract the insertion point when key is missing: **`int insertPos = -(index + 1);`**.

> **Memory Trick:** **"Mid = Left + (Right - Left) / 2"**.

## 13. Comparisons
| Metric | Iterative Binary Search | Recursive Binary Search |
| :--- | :--- | :--- |
| **Time Complexity** | $O(\log n)$ | $O(\log n)$ |
| **Space Complexity**| **$O(1)$ (Optimal)** | $O(\log n)$ (Recursion stack space) |
| **Stack Overflow Risk**| Zero | Slight risk if call depth is huge |
| **Interview Recommendation** | **PREFERRED** | Acceptable |

## 14. How to Recognize This in Questions
* **"Search in a sorted array"** $\rightarrow$ Binary Search ($O(\log n)$).
* **"Find first / last occurrence of target"** $\rightarrow$ Lower / Upper Bound Binary Search.
* **"Minimize the maximum / Maximize the minimum"** $\rightarrow$ **Binary Search on Answer Space**.

## 15. Frequently Asked Interview Questions
* **Q: How many comparisons does Binary Search execute for an array of size $1,000,000$?**  
  *A:* At most $\lceil\log_2(1,000,000)\rceil = 20$ comparisons.
* **Q: How do you find the count of a target value in a sorted array in $O(\log n)$ time?**  
  *A:* Find the first occurrence index `first` and last occurrence index `last` using Lower and Upper Bound binary search. Total count is **`last - first + 1`**.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY SEARCH ON ARRAYS                               |
+-----------------------------------------------------------------------+
| • Mid Calculation: int mid = left + (right - left) / 2 (Overflow Safe)|
| • Standard Search: while (left <= right) -> left=mid+1 or right=mid-1  |
| • First Occurrence: Record index when nums[mid]==target, right=mid-1  |
| • Last Occurrence:  Record index when nums[mid]==target, left=mid+1   |
| • Target Count in Sorted Array = lastIndex - firstIndex + 1           |
| • Java built-in missing insertion point = -(Arrays.binarySearch + 1)  |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write overflow-safe midpoint calculation `left + (right - left) / 2`.
- [ ] I can write iterative Binary Search from memory in 2 minutes.
- [ ] I can implement First and Last occurrence binary search.
- [ ] I know how to calculate element frequency in a sorted array in $O(\log n)$.
- [ ] I know how to extract `Arrays.binarySearch()` insertion points.
