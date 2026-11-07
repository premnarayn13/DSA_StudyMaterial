# 01. Two Pointers Fundamentals, Monotonicity & In-Place Array Mutation

## 1. Introduction
The **Two Pointers Pattern** is an essential algorithmic paradigm in computer science for searching, partitioning, and mutating linear data structures (arrays, strings, linked lists) in **$O(N)$ linear time and $O(1)$ constant space**. By leveraging array order or sorted monotonicity, two pointer references iterate through a structure concurrently, pruning quadratic $O(N^2)$ search spaces down to optimal $O(N)$ single-pass execution.

> **Important:** The fundamental precondition for two-pointer search optimization is **Monotonicity (Sorted Order)** or **Structural State Reduction**. When an array is sorted, comparing elements at two pointers (`left` and `right`) allows discarding an entire row or column of candidate pairs in $O(1)$ constant time, bypassing brute-force nested loops!

```
Brute-Force vs Two Pointers Search Space Spectrum:
+-----------------------------------------------------------------------------------+
| Brute-Force Nested Loops : O(N^2) Quadratic Time -> Checks all N*(N-1)/2 pairs ❌  |
| Two Pointers Optimization: O(N) Linear Time    -> Prunes 1 row/col per step! ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Pointer Taxonomy

### 2.1 The 3 Primary Two-Pointer Families
1. **Opposite Direction Pointers (Converging Pointers)**:
   - `left` initialized at index `0`, `right` initialized at index `N - 1`.
   - Move towards each other: `left++` or `right--`.
   - Ideal for **Two Sum II (LeetCode 167)**, **Container With Most Water (LeetCode 11)**, and **Valid Palindrome (LeetCode 125)**.
2. **Same Direction Pointers (Catch-Up / Read-Write Pointers)**:
   - `write` (slow) pointer tracks destination index for valid elements; `read` (fast) pointer scans input array.
   - Ideal for **In-Place Array Mutation**: **Remove Duplicates from Sorted Array (LeetCode 26)** and **Move Zeroes (LeetCode 283)**.
3. **Fast & Slow Pointers (Cycle Detection & Middle Finding)**:
   - `slow` advances 1 step (`slow++`), `fast` advances 2 steps (`fast += 2`).
   - Ideal for Linked List Middle Finding (LeetCode 876) and Floyd's Cycle Detection (LeetCode 141).

```
Two Pointers Classification Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Pointer Family        | Initial Positions | Pointer Movement  | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| Opposite Direction    | `0` and `N - 1`   | `left++`, `right--`| Pair/Triplet Search|
| Same Direction        | `0` and `0`       | `read++`, `write++`| In-place Mutation|
| Fast & Slow           | `0` and `0`       | `slow+1`, `fast+2` | Cycle & Middle    |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Opposite pointers prune sorted search space! Same direction read/write pointers mutate arrays in O(1) space!"**

---

## 3. Characteristics & In-Place Array Mutation Mechanics

### 3.1 In-Place Array Mutation (LeetCode 26 & LeetCode 283)
In production software engineering and technical interviews, array mutation operations MUST be executed **in-place** ($O(1)$ auxiliary space) without allocating new arrays.

* **Remove Duplicates from Sorted Array (LeetCode 26)**:
  1. `write = 0`.
  2. Iterate `read` from index `1` to `N - 1`:
     - If `nums[read] != nums[write]`: Advance `write++` and assign **`nums[write] = nums[read]`**.
  3. Return `write + 1` as the new length of unique elements.

* **Move Zeroes to End (LeetCode 283)**:
  1. `write = 0`.
  2. Iterate `read` from `0` to `N - 1`:
     - If `nums[read] != 0`: Swap `nums[write]` and `nums[read]`, then advance `write++`.

```
Move Zeroes Read-Write Pointer Tracing [ 0, 1, 0, 3, 12 ]:
Read 0 (val 0)  : Skip. write = 0.
Read 1 (val 1)  : Swap nums[0] & nums[1] -> [ 1, 0, 0, 3, 12 ]. write = 1.
Read 2 (val 0)  : Skip. write = 1.
Read 3 (val 3)  : Swap nums[1] & nums[3] -> [ 1, 3, 0, 0, 12 ]. write = 2.
Read 4 (val 12) : Swap nums[2] & nums[4] -> [ 1, 3, 12, 0, 0 ]. write = 3.

Result: [ 1, 3, 12, 0, 0 ] ✅ (In-Place O(N) Time, O(1) Space!)
```

---

## 4. Internal Working Mechanics
Tracing Remove Duplicates (LeetCode 26) on `[1, 1, 2, 3, 3, 4]`:

```
Init: write = 0 (val 1)

read = 1 (val 1): nums[1] == nums[0] -> Skip.
read = 2 (val 2): nums[2] != nums[0] -> write++ (1), nums[1] = 2. Array: [1, 2, 2, 3, 3, 4]
read = 3 (val 3): nums[3] != nums[1] -> write++ (2), nums[2] = 3. Array: [1, 2, 3, 3, 3, 4]
read = 4 (val 3): nums[4] == nums[2] -> Skip.
read = 5 (val 4): nums[5] != nums[2] -> write++ (3), nums[3] = 4. Array: [1, 2, 3, 4, 3, 4]

New Length = write + 1 = 4. Unique Sub-array: [1, 2, 3, 4] ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Same-Direction Read-Write Pointer Topology:

```
Array:   [ 1,   1,   2,   3,   3,   4 ]
           ^    ^
        write  read  (nums[read] == nums[write] -> Skip read)

Array:   [ 1,   2,   2,   3,   3,   4 ]
                ^    ^
             write  read  (nums[read] != nums[write] -> write++, nums[write] = nums[read])
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Remove Duplicates (LeetCode 26), Move Zeroes (LeetCode 283), Remove Element (LeetCode 27), and Two Sum II Sorted (LeetCode 167):

```java
import java.util.*;

public class TwoPointersFundamentalsMaster {

    // 1. Remove Duplicates from Sorted Array (LeetCode 26) O(N) Time, O(1) Space
    public static int removeDuplicates(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int write = 0;
        for (int read = 1; read < nums.length; read++) {
            if (nums[read] != nums[write]) {
                write++;
                nums[write] = nums[read];
            }
        }

        return write + 1; // Length of unique elements
    }

    // 2. Move Zeroes to End (LeetCode 283) O(N) Time, O(1) Auxiliary Space
    public static void moveZeroes(int[] nums) {
        if (nums == null || nums.length <= 1) return;

        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != 0) {
                if (read != write) {
                    int temp = nums[write];
                    nums[write] = nums[read];
                    nums[read] = temp;
                }
                write++;
            }
        }
    }

    // 3. Remove Element in-place (LeetCode 27) O(N) Time, O(1) Space
    public static int removeElement(int[] nums, int val) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != val) {
                nums[write] = nums[read];
                write++;
            }
        }
        return write;
    }

    // 4. Two Sum II - Input Array Is Sorted (LeetCode 167) O(N) Time, O(1) Space
    public static int[] twoSumSorted(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if (sum == target) {
                return new int[]{left + 1, right + 1}; // 1-indexed
            } else if (sum < target) {
                left++;  // Sum too small -> Increase left pointer!
            } else {
                right--; // Sum too large -> Decrease right pointer!
            }
        }

        return new int[]{-1, -1};
    }
}
```

> **Quick Syntax:**
```java
// Same-Direction Read-Write Pattern
int write = 0;
for (int read = 0; read < nums.length; read++) {
    if (condition) {
        nums[write++] = nums[read];
    }
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 26 - Remove Duplicates from Sorted Array**: Same direction read-write pointers.
* **LeetCode 283 - Move Zeroes**: Same direction swap read-write pointers.
* **LeetCode 167 - Two Sum II**: Opposite direction sorted two pointers.

---

## 8. Java Code Demonstration & Dry Run
Demonstration removing duplicates and moving zeroes in-place:

```java
public class TwoPointersFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Remove Duplicates (LeetCode 26) ===");
        int[] nums1 = {1, 1, 2, 3, 3, 4};
        int newLen = TwoPointersFundamentalsMaster.removeDuplicates(nums1);
        System.out.println("New Length: " + newLen); // Output: 4
        System.out.println("Unique Sub-array: " + Arrays.toString(Arrays.copyOf(nums1, newLen))); // [1, 2, 3, 4]

        System.out.println("\n=== 2. Move Zeroes (LeetCode 283) ===");
        int[] nums2 = {0, 1, 0, 3, 12};
        TwoPointersFundamentalsMaster.moveZeroes(nums2);
        System.out.println("Moved Zeroes: " + Arrays.toString(nums2)); // Output: [1, 3, 12, 0, 0]
    }
}
```

---

## 9. Complexity Analysis

| Operation / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Remove Duplicates (26)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Read pointer scans once |
| **Move Zeroes (283)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Swap non-zeroes to `write` |
| **Two Sum II (167)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Sorted array monotonicity |

---

## 10. Edge Cases & Boundary Handling
* **Empty or Single-Element Array (`nums.length <= 1`)**: Handled cleanly; returns `nums.length`.
* **Array With No Targets / All Targets**: Read pointer scans entire array without index out-of-bounds errors.

---

## 11. Common Mistakes & Anti-Patterns
* **Allocating Extra Auxiliary Arrays ($O(N)$ Space Penalty)**:
  - Creating a new array `int[] temp = new int[N]` violates the $O(1)$ space constraint required by in-place array mutation problems.
  - **Use same-direction read-write pointers (`write` and `read`)**.
* **Off-By-One Errors in Return Length**: Returning `write` instead of `write + 1` in LeetCode 26 truncates the last unique element.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Two Pointers Works on Sorted Arrays (Monotonicity):
> On a sorted array `nums`, if `nums[left] + nums[right] > target`, incrementing `left` will only INCREASE the sum further.
> Therefore, the current `right` element CANNOT pair with ANY element to the right of `left` $\implies$ We can SAFELY discard `right` by executing `right--`!
> This prunes $N$ candidate pairs in a single step!

> **Memory Trick:** **"If sum > target, right--! If sum < target, left++! Discards 1 row/col per step!"**

---

## 13. System & Implementation Comparisons

| Feature | Two Pointers Approach | Brute-Force Nested Loops |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(1)$ |
| **Pruning Mechanism**| State Elimination | None |

---

## 14. How to Recognize This in Questions
* **"Modify array in-place with O(1) extra memory"** $\rightarrow$ Read-Write Same Direction Pointers.
* **"Find pair/triplet in a sorted array matching target sum"** $\rightarrow$ Opposite Direction Pointers.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does the Read-Write pointer pattern preserve original relative order of elements in LeetCode 283?**  
  *A:* Because both `read` and `write` pointers iterate strictly left-to-right. Non-zero elements encountered by `read` are written to `write` sequentially, preserving their original input ordering.
* **Q: Can Two Pointers solve Two Sum on an UNSORTED array in $O(N)$ time?**  
  *A:* No! Unsorted Two Sum requires a **Hash Map (`Map<Integer, Integer>`)** for $O(N)$ time. Sorting an unsorted array takes $O(N \log N)$ time first before two pointers can be applied.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO POINTERS FUNDAMENTALS & IN-PLACE MUTATION         |
+-----------------------------------------------------------------------+
| • Opposite Direction: left=0, right=N-1; left++ or right--            |
| • Same Direction (Read-Write): write=0; for read=0..N-1 write++       |
| • Monotonicity: Sorted order enables discarding 1 row/col per step    |
| • Remove Duplicates (26): if (nums[read] != nums[write]) nums[++write] = nums[read]|
| • Move Zeroes (283): Swap nums[write] and nums[read] when val != 0    |
| • Space Invariant: All two-pointer algorithms run in O(1) Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Remove Duplicates (LeetCode 26) in under 2 minutes.
- [ ] I can write Move Zeroes (LeetCode 283) in-place.
- [ ] I can write Two Sum II Sorted (LeetCode 167) in $O(N)$ time.
- [ ] I know why sorted monotonicity enables $O(N)$ time complexity.
- [ ] I know when to use Hash Map vs Two Pointers for Two Sum.
