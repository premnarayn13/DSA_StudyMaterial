# 03. Same Direction Pointers, Read-Write Mutators & In-Place Duplicate Truncation

## 1. Introduction
The **Same Direction Two Pointers Pattern** (also called **Catch-Up** or **Read-Write Pointer Technique**) moves both pointer references from left to right along a sequence. One pointer—the **Read Pointer (`read`)**—scans every element sequentially, while the second pointer—the **Write Pointer (`write`)**—maintains the boundary of valid output elements. This pattern powers **Remove Duplicates from Sorted Array II (LeetCode 80)**, **Sort Array by Parity (LeetCode 905)**, and **String Compression (LeetCode 443)** in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** Same-direction read-write pointers allow in-place array transformations without allocating dynamic target buffers. In **Remove Duplicates II (LeetCode 80)**, comparing `nums[read]` against **`nums[write - 2]`** guarantees that no element appears more than $K = 2$ times!

```
Same-Direction Read-Write Topology:
+-----------------------------------------------------------------------------------+
| Write Pointer (Slow) : Stores destination index for valid processed elements      |
| Read Pointer (Fast)  : Scans input array sequentially from 0 to N - 1            |
| General Rule K-Duplicates: if (read element != nums[write - K]) nums[write++] = val|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Generalized $K$-Duplicate Removal Mechanics

### 2.1 Generalized $K$-Duplicate Truncation (LeetCode 80 for $K = 2$)
Given a sorted array `nums`, remove duplicates in-place such that each unique element appears at most $K$ times:

#### The `nums[write - K]` Invariant:
1. If array length $N \le K$, return $N$ immediately.
2. Initialize `write = K`.
3. Iterate `read` from index $K$ to $N - 1$:
   - Compare `nums[read]` against the element $K$ positions behind `write`: **`nums[write - K]`**.
   - If `nums[read] != nums[write - K]`:
     - Assign `nums[write] = nums[read]`.
     - Increment `write++`.
4. Return `write` as the new length of valid elements.

```
Why nums[write - K] Works:
Since the array is sorted, if nums[read] == nums[write - K], it means we ALREADY have
K copies of that exact element in the valid sub-array nums[0 ... write-1]!
Discarding nums[read] prevents inserting a (K+1)-th copy! ⚡
```

### 2.2 Partitioning by Parity (LeetCode 905 - Sort Array by Parity)
Given an integer array `nums`, move all even integers to the front followed by all odd integers:
1. `write = 0`.
2. Iterate `read` from `0` to $N - 1$:
   - If `nums[read] % 2 == 0`:
     - Swap `nums[write]` and `nums[read]`.
     - `write++`.

```
Parity Read-Write Pointer Tracing [ 3, 1, 2, 4 ]:
read 0 (val 3): Odd -> Skip. write = 0.
read 1 (val 1): Odd -> Skip. write = 0.
read 2 (val 2): Even -> Swap nums[0](3) & nums[2](2) -> [ 2, 1, 3, 4 ]. write = 1.
read 3 (val 4): Even -> Swap nums[1](1) & nums[3](4) -> [ 2, 4, 3, 1 ]. write = 2.

Result: [ 2, 4, 3, 1 ] ✅ (Even numbers at front, O(N) Time, O(1) Space!)
```

> **Memory Trick:** **"To allow at most K duplicates in sorted array: compare nums[read] with nums[write - K]!"**

---

## 3. Characteristics & String Compression Mechanics (LeetCode 443)

### 3.1 In-Place String Compression (LeetCode 443)
Given an array of characters `chars`, compress it in-place using the following algorithm:
1. Initialize `write = 0`, `read = 0`.
2. While `read < chars.length`:
   - Identify run-length group: `groupStart = read`.
   - Advance `read` while `read < chars.length && chars[read] == chars[groupStart]`.
   - Write character: `chars[write++] = chars[groupStart]`.
   - Compute count: `count = read - groupStart`.
   - If `count > 1`: Convert `count` to string digits and write each digit into `chars[write++]`.
3. Return `write` as the compressed length.

```
String Compression Tracing [ 'a', 'a', 'b', 'b', 'c', 'c', 'c' ]:
Group 'a': count = 2 -> Write 'a', Write '2'. write = 2.
Group 'b': count = 2 -> Write 'b', Write '2'. write = 4.
Group 'c': count = 3 -> Write 'c', Write '3'. write = 6.

Compressed Array: [ 'a', '2', 'b', '2', 'c', '3' ] ✅
```

---

## 4. Internal Working Mechanics
Tracing Remove Duplicates II ($K = 2$) on `[1, 1, 1, 2, 2, 3]`:

```
Init: K = 2, write = 2 (Valid sub-array initially [1, 1])

read = 2 (val 1): nums[2] vs nums[write-2] (nums[0] = 1). 1 == 1 -> Skip (3rd copy!).
read = 3 (val 2): nums[3] vs nums[write-2] (nums[0] = 1). 2 != 1 -> Assign nums[2]=2, write=3. Array: [1, 1, 2, 2, 2, 3]
read = 4 (val 2): nums[4] vs nums[write-2] (nums[1] = 1). 2 != 1 -> Assign nums[3]=2, write=4. Array: [1, 1, 2, 2, 2, 3]
read = 5 (val 3): nums[5] vs nums[write-2] (nums[2] = 2). 3 != 2 -> Assign nums[4]=3, write=5. Array: [1, 1, 2, 2, 3, 3]

New Length = write = 5. Array: [1, 1, 2, 2, 3] ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Same-Direction $K$-Duplicate Truncation Pointer Topology:

```
Array:     [ 1,   1,   1,   2,   2,   3 ]
             ^         ^
          write-2     read  (nums[read] == nums[write-2] -> Skip 3rd duplicate!)

Array:     [ 1,   1,   2,   2,   3,   3 ]
                  ^         ^
               write-2     read  (nums[read] != nums[write-2] -> nums[write++] = nums[read])
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Remove Duplicates II (LeetCode 80), Sort Array by Parity (LeetCode 905), and String Compression (LeetCode 443):

```java
import java.util.*;

public class SameDirectionMaster {

    // 1. Remove Duplicates from Sorted Array II (LeetCode 80 - At Most 2 Copies) O(N) Time, O(1) Space
    public static int removeDuplicates2(int[] nums) {
        return removeDuplicatesK(nums, 2);
    }

    // Generalized Function: Allow At Most K Duplicates in Sorted Array
    public static int removeDuplicatesK(int[] nums, int k) {
        if (nums == null) return 0;
        if (nums.length <= k) return nums.length;

        int write = k;
        for (int read = k; read < nums.length; read++) {
            // Compare current element against element K positions behind write pointer
            if (nums[read] != nums[write - k]) {
                nums[write] = nums[read];
                write++;
            }
        }

        return write;
    }

    // 2. Sort Array by Parity (LeetCode 905) O(N) Time, O(1) Auxiliary Space
    public static int[] sortArrayByParity(int[] nums) {
        if (nums == null || nums.length <= 1) return nums;

        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] % 2 == 0) {
                int temp = nums[write];
                nums[write] = nums[read];
                nums[read] = temp;
                write++;
            }
        }

        return nums;
    }

    // 3. String Compression (LeetCode 443) O(N) Time, O(1) Auxiliary Space
    public static int compress(char[] chars) {
        if (chars == null || chars.length == 0) return 0;

        int write = 0;
        int read = 0;

        while (read < chars.length) {
            char currentChar = chars[read];
            int groupStart = read;

            // Find end of current character group
            while (read < chars.length && chars[read] == currentChar) {
                read++;
            }

            // Write character
            chars[write++] = currentChar;
            int count = read - groupStart;

            // Write count digits if count > 1
            if (count > 1) {
                String countStr = String.valueOf(count);
                for (char c : countStr.toCharArray()) {
                    chars[write++] = c;
                }
            }
        }

        return write;
    }
}
```

> **Quick Syntax:**
```java
// Generalized K-Duplicates Invariant Syntax
if (nums[read] != nums[write - k]) {
    nums[write++] = nums[read];
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 80 - Remove Duplicates from Sorted Array II**: At most 2 duplicates allowed.
* **LeetCode 905 - Sort Array by Parity**: Partitioning evens before odds in-place.
* **LeetCode 443 - String Compression**: In-place run-length encoding.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Remove Duplicates II, Sort Array by Parity, and String Compression:

```java
public class SameDirectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Remove Duplicates II (LeetCode 80, K=2) ===");
        int[] nums1 = {1, 1, 1, 2, 2, 3};
        int newLen = SameDirectionMaster.removeDuplicates2(nums1);
        System.out.println("New Length: " + newLen); // Output: 5
        System.out.println("Resulting Sub-array: " + Arrays.toString(Arrays.copyOf(nums1, newLen))); // [1, 1, 2, 2, 3]

        System.out.println("\n=== 2. Sort Array by Parity (LeetCode 905) ===");
        int[] nums2 = {3, 1, 2, 4};
        SameDirectionMaster.sortArrayByParity(nums2);
        System.out.println("Parity Sorted: " + Arrays.toString(nums2)); // Output: [2, 4, 3, 1]

        System.out.println("\n=== 3. String Compression (LeetCode 443) ===");
        char[] chars = {'a', 'a', 'b', 'b', 'c', 'c', 'c'};
        int compLen = SameDirectionMaster.compress(chars);
        System.out.println("Compressed Length: " + compLen); // Output: 6
        System.out.println("Compressed Chars: " + Arrays.toString(Arrays.copyOf(chars, compLen))); // ['a', '2', 'b', '2', 'c', '3']
    }
}
```

---

## 9. Complexity Analysis

| Operation / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Remove Duplicates II (80)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `nums[read] != nums[write - K]` check |
| **Sort by Parity (905)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Swap evens to `write` pointer |
| **String Compression (443)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Single-pass run-length encoding |

---

## 10. Edge Cases & Boundary Handling
* **$N \le K$ Array**: Returns $N$ immediately without loop execution.
* **Count $> 9$ in String Compression**: Integer `count` digits are converted to character array and written sequentially into `chars[write++]`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Extra Frequency Maps for LeetCode 80 ($O(N)$ Space)**:
  - Using a `HashMap<Integer, Integer>` to track frequencies consumes $O(N)$ memory and loses sorted order.
  - **Use `nums[read] != nums[write - K]` for $O(1)$ space**.
* **Overwriting Unread Elements in String Compression**:
  - Writing `countStr` ahead of `read` pointer can corrupt data if `write` overtakes `read`.
  - In String Compression, `write` is GUARANTEED to be $\le$ `read` at all times.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The Power of `nums[write - K]` Invariant:
> This single template solves:
> * **At most 1 copy (LeetCode 26)**: `k = 1` $\implies$ `nums[read] != nums[write - 1]`.
> * **At most 2 copies (LeetCode 80)**: `k = 2` $\implies$ `nums[read] != nums[write - 2]`.
> * **At most $K$ copies**: `nums[read] != nums[write - K]`.

> **Memory Trick:** **"nums[read] != nums[write - K] solves ALL K-duplicate array truncation problems!"**

---

## 13. System & Implementation Comparisons

| Feature | `nums[write - K]` Template | Frequency Counting Map |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Hash Table |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(N)$ 2 Passes |
| **Generality** | Handles any $K$ instantly | Requires map lookup |

---

## 14. How to Recognize This in Questions
* **"Remove duplicates from sorted array such that elements appear at most K times"** $\rightarrow$ LeetCode 80 (`nums[read] != nums[write - K]`).
* **"Rearrange elements in-place based on condition (even/odd)"** $\rightarrow$ Read-Write swap pointer.
* **"Compress character array in-place"** $\rightarrow$ LeetCode 443.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `nums[read] != nums[write - K]` work only when the array is sorted?**  
  *A:* Because in a sorted array, identical elements are contiguous. Comparing `nums[read]` against `nums[write - K]` guarantees that if they match, all intermediate elements `nums[write - K ... write - 1]` are identical, meaning $K$ copies have ALREADY been stored.
* **Q: Why is `write` guaranteed to be $\le$ `read` in same-direction mutation algorithms?**  
  *A:* Because `read` advances on every single iteration step (`read++`), while `write` advances ONLY when a valid element is accepted (`write++`). Thus `write` never exceeds `read`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SAME DIRECTION READ-WRITE POINTER PATTERN              |
+-----------------------------------------------------------------------+
| • Generalized K-Duplicates (80): write = K; for read = K..N-1         |
|   if (nums[read] != nums[write - K]) nums[write++] = nums[read]       |
| • Sort by Parity (905): write = 0; if (val % 2 == 0) swap(write++, read)|
| • String Compression (443): Run-length encoding; write char & count   |
| • Invariant Rule: write <= read at all times (Prevents overwriting!)   |
| • Space Invariant: All same-direction mutators run in O(1) Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Remove Duplicates II (LeetCode 80) in 6 lines using `write - 2`.
- [ ] I can state the generalized $K$-duplicate invariant `nums[write - K]`.
- [ ] I can write Sort Array by Parity (LeetCode 905) in $O(N)$ time.
- [ ] I can write String Compression (LeetCode 443) in $O(1)$ space.
- [ ] I know why `write` is guaranteed to be $\le$ `read` in same-direction mutation.
