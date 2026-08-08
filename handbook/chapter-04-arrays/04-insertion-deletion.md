# 04. Insertion & Deletion in Arrays

## 1. Introduction
Insertion and deletion operations in arrays require careful index pointer management and element shifting due to contiguous memory allocation. In technical coding interviews, mastering array insertion and deletion—including static array shifting, dynamic array resizing, in-place element removal (`Remove Element`, `Remove Duplicates`), and two-pointer compaction—is a foundational requirement.

> **Important:** Array insertion at index $K$ requires **Right-Shifting** elements from $N-1$ down to $K$. Array deletion at index $K$ requires **Left-Shifting** elements from $K+1$ up to $N-1$.

## 2. Core Concepts
* **Insertion at Index $K$**: Inserting a new value into an array by shifting all existing elements from index $K$ onward one slot to the right.
* **Deletion at Index $K$**: Removing an element at index $K$ by shifting all subsequent elements from index $K+1$ onward one slot to the left.
* **Two-Pointer Compaction (In-Place Filter)**: Using a `readPointer` to scan the array and a `writePointer` to overwrite valid elements in-place in $O(n)$ time and $O(1)$ space.
* **Dynamic Array Growth**: Allocating a new backing array when capacity is reached and copying elements over.

> **Memory Trick:** **"Write Pointer stays behind Read Pointer"**. In two-pointer in-place deletion/compaction problems, `writePointer` tracks the end of the clean modified array while `readPointer` scans the input.

## 3. Characteristics / Properties
* **Position-Dependent Complexity**:
  * Insert/Delete at End: $O(1)$ constant time (if capacity exists).
  * Insert/Delete at Beginning: $O(n)$ worst case (must shift ALL $n$ elements).
  * Insert/Delete at Index $K$: $O(n - K)$ time (shifts $n - K$ elements).
* **In-Place Compaction Strategy**: Avoids allocating new arrays by overwriting duplicate or unwanted elements directly in the input array.

```
Insertion & Deletion Position Complexity:
+-----------------------+-------------------+-------------------+
| Operation Position    | Time Complexity   | Elements Shifted  |
+-----------------------+-------------------+-------------------+
| Beginning (Index 0)   | O(n)              | n elements        |
| Middle (Index n/2)    | O(n)              | n/2 elements      |
| End (Index n - 1)     | O(1)              | 0 elements        |
+-----------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Two-Pointer In-Place Element Removal (`removeElement(arr, val = 3)`):

```
Initial Array: [ 3, 2, 2, 3, 4 ], Target to remove: val = 3
Pointers: write = 0, read = 0

Read 0 (val 3): Match! Skip read.                 [ 3, 2, 2, 3, 4 ] (write=0, read=0)
Read 1 (val 2): Keep! arr[write++] = 2.           [ 2, 2, 2, 3, 4 ] (write=1, read=1)
Read 2 (val 2): Keep! arr[write++] = 2.           [ 2, 2, 2, 3, 4 ] (write=2, read=2)
Read 3 (val 3): Match! Skip read.                 [ 2, 2, 2, 3, 4 ] (write=2, read=3)
Read 4 (val 4): Keep! arr[write++] = 4.           [ 2, 2, 4, 3, 4 ] (write=3, read=4)

Result: New length = write = 3. Compacted Array Prefix: [ 2, 2, 4 ]
```

## 5. Visual Diagram
Shifting Mechanics vs Two-Pointer Compaction:

```
[ INSERTION AT INDEX 1: Right Shift ]
Initial:   [ 10 ][ 20 ][ 30 ][ 40 ][ _ ]
Shift 40:  [ 10 ][ 20 ][ 30 ][ 40 ][ 40 ] (Shift right from end!)
Shift 30:  [ 10 ][ 20 ][ 30 ][ 30 ][ 40 ]
Shift 20:  [ 10 ][ 20 ][ 20 ][ 30 ][ 40 ]
Insert 99: [ 10 ][ 99 ][ 20 ][ 30 ][ 40 ]

[ DELETION AT INDEX 1: Left Shift ]
Initial:   [ 10 ][ 99 ][ 20 ][ 30 ][ 40 ]
Shift 20:  [ 10 ][ 20 ][ 20 ][ 30 ][ 40 ] (Shift left from index + 1!)
Shift 30:  [ 10 ][ 20 ][ 30 ][ 30 ][ 40 ]
Shift 40:  [ 10 ][ 20 ][ 30 ][ 40 ][ 40 ]
Clear Last:[ 10 ][ 20 ][ 30 ][ 40 ][ 0  ]
```

## 6. Operations / Algorithms
In-Place Array Compaction Algorithms:

### 1. Remove Target Element In-Place (LeetCode 27)
```java
public int removeElement(int[] nums, int val) {
    int write = 0;
    for (int read = 0; read < nums.length; read++) {
        if (nums[read] != val) {
            nums[write++] = nums[read];
        }
    }
    return write; // Returns new length
}
```

### 2. Remove Duplicates from Sorted Array (LeetCode 26)
```java
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int write = 1;
    for (int read = 1; read < nums.length; read++) {
        if (nums[read] != nums[read - 1]) {
            nums[write++] = nums[read];
        }
    }
    return write; // Returns length of unique prefix
}
```

> **Quick Syntax:**
```java
// Overwriting target element using Write-Pointer
int write = 0;
for (int read = 0; read < arr.length; read++) {
    if (shouldKeep(arr[read])) {
        arr[write++] = arr[read];
    }
}
```

## 7. Examples
* **Move Zeroes to End (LeetCode 283)**: Using write-pointer to compact non-zero elements, then filling remaining indices with zeros.
* **Remove Duplicates from Sorted Array II**: Allowing elements to appear at most twice by checking `nums[read] != nums[write - 2]`.
* **Insert into Sorted Array**: Finding insertion index via Binary Search, then right-shifting elements.

## 8. Java Code
Complete, interview-ready Java suite demonstrating dynamic array resizing, in-place element removal, and duplicate stripping:

```java
import java.util.Arrays;

public class InsertionDeletionMaster {

    // 1. In-Place Remove Element (LeetCode 27)
    public static int removeElement(int[] nums, int val) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != val) {
                nums[write++] = nums[read];
            }
        }
        return write;
    }

    // 2. In-Place Remove Duplicates from Sorted Array (LeetCode 26)
    public static int removeDuplicates(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int write = 1;
        for (int read = 1; read < nums.length; read++) {
            if (nums[read] != nums[read - 1]) {
                nums[write++] = nums[read];
            }
        }
        return write;
    }

    // 3. Move Zeroes to End (LeetCode 283)
    public static void moveZeroes(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != 0) {
                nums[write++] = nums[read];
            }
        }
        // Fill remaining trailing slots with zeroes
        while (write < nums.length) {
            nums[write++] = 0;
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Remove Element
        int[] arr1 = {3, 2, 2, 3, 4, 3, 5};
        int len1 = removeElement(arr1, 3);
        System.out.println("After removing 3: " + Arrays.toString(Arrays.copyOf(arr1, len1))); // [2, 2, 4, 5]

        // Test Remove Duplicates from Sorted Array
        int[] sortedArr = {1, 1, 2, 2, 3, 4, 4, 5};
        int len2 = removeDuplicates(sortedArr);
        System.out.println("After removing duplicates: " + Arrays.toString(Arrays.copyOf(sortedArr, len2))); // [1, 2, 3, 4, 5]

        // Test Move Zeroes
        int[] zeroesArr = {0, 1, 0, 3, 12};
        moveZeroes(zeroesArr);
        System.out.println("After moving zeroes: " + Arrays.toString(zeroesArr)); // [1, 3, 12, 0, 0]
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **`removeElement()`** | $O(n)$ | $O(1)$ | Single pass write-pointer compaction |
| **`removeDuplicates()`**| $O(n)$ | $O(1)$ | Single pass adjacent check |
| **`moveZeroes()`** | $O(n)$ | $O(1)$ | Write non-zeros then fill remaining zeros |
| **Static Insertion** | $O(n)$ | $O(1)$ | Right shift elements from $N-1$ down |
| **Static Deletion** | $O(n)$ | $O(1)$ | Left shift elements from $K+1$ up |

## 10. Edge Cases
* **Empty Input Array (`nums.length == 0`)**: Return 0 immediately.
* **All Elements Match Target**: E.g., `removeElement([3, 3, 3], 3)` returns `newLength = 0`.
* **No Elements Match Target**: E.g., `removeElement([1, 2, 4], 3)` returns original length without mutations.

## 11. Common Mistakes
* Shifting left-to-right during static array insertion (overwrites subsequent values!).
* Creating a new array `new int[n]` when an **in-place** modification was requested.
* Forgetting to zero out or fill remaining trailing indices when moving zeroes or removing elements.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** When solving "Remove Duplicates" or "Remove Element" on LeetCode, DO NOT allocate a new array! The problem expects an in-place modification of the original array, returning the new valid prefix length `k`. The caller checks indices `0` through `k-1`.

> **Memory Trick:** **"Write-Pointer Compaction Pattern"**:
> `int write = 0; for (int read = 0; read < N; read++) if (keep(arr[read])) arr[write++] = arr[read]; return write;`

## 13. Comparisons
| Feature | Element Shifting (Static Array) | Two-Pointer Compaction (In-Place Filter) |
| :--- | :--- | :--- |
| **Shifting Direction** | Right (Insert) / Left (Delete) | Direct overwriting via write-pointer |
| **Single Operation Time**| $O(n)$ | $O(1)$ per step ($O(n)$ total pass) |
| **Auxiliary Space** | $O(1)$ | $O(1)$ |
| **Use Case** | Single element update | Batch filtering / Duplicate removal |

## 14. How to Recognize This in Questions
* **"Remove element in-place and return new length"** $\rightarrow$ Two-Pointer Read/Write Compaction.
* **"Move elements matching condition to end"** $\rightarrow$ Two-Pointer Compaction + Zero Fill.

## 15. Frequently Asked Interview Questions
* **Q: How does `removeDuplicates` work in $O(n)$ time and $O(1)$ space for a sorted array?**  
  *A:* Since the array is sorted, duplicates are adjacent. A `read` pointer scans every element while a `write` pointer only advances and writes when `arr[read] != arr[read - 1]`.
* **Q: Why is inserting at the beginning of an ArrayList $O(n)$?**  
  *A:* Because every existing element in the backing array must be shifted right by one index position to make room at index 0.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: INSERTION & DELETION IN ARRAYS                        |
+-----------------------------------------------------------------------+
| • Insertion Shifting: Right-to-Left (i = size-1 down to index)         |
| • Deletion Shifting: Left-to-Right (i = index up to size-2)           |
| • In-Place Removal: Write pointer tracks valid prefix                 |
| • Move Zeroes: Write non-zeros first, fill trailing indices with 0s   |
| • Space Constraint: In-Place operations MUST use O(1) auxiliary space|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can implement in-place element removal (`removeElement`) in $O(1)$ space.
- [ ] I can implement duplicate removal from sorted arrays (`removeDuplicates`).
- [ ] I know how to move zeroes to the end of an array using two pointers.
- [ ] I understand why static insertion requires right-to-left shifting.
- [ ] I understand why static deletion requires left-to-right shifting.
