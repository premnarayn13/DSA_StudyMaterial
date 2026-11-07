# 08. Two-Pointer Partitioning Schemes, Dutch National Flag & Hoare vs Lomuto Mechanics

## 1. Introduction
**Two-Pointer Partitioning** is a core algorithmic technique for reordering array elements around a pivot value or condition in **$O(N)$ linear time and $O(1)$ constant space**. Partitioning underpins **Quicksort (Hoare & Lomuto schemes)**, **Quickselect (LeetCode 215)**, and the famous **Dutch National Flag Problem (LeetCode 75 - Sort Colors)**.

> **Important:** In **Sort Colors (LeetCode 75)**, Dijkstra's **3-Way Dutch National Flag Partitioning** partitions an array of 3 distinct values (`0`, `1`, `2`) in a SINGLE pass using 3 pointers (`low`, `mid`, `high`)! Elements are partitioned into 3 regions: `[0 ... low-1]` (all 0s), `[low ... high]` (all 1s), and `[high+1 ... N-1]` (all 2s)!

```
Dutch National Flag 3-Way Array Topology:
+-----------------------------------------------------------------------------------+
| 0s Region       | 1s Region       | Unprocessed Region | 2s Region                |
| 0 ... low - 1   | low ... mid - 1 | mid ... high       | high + 1 ... N - 1       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Dutch National Flag 3-Way Partitioning (LeetCode 75)
Given an array `nums` with $N$ objects colored red (`0`), white (`1`), or blue (`2`), sort them in-place so that objects of the same color are adjacent:

1. Initialize `low = 0`, `mid = 0`, `high = N - 1`.
2. While `mid <= high`:
   - If `nums[mid] == 0`:
     - Swap `nums[low]` and `nums[mid]`.
     - `low++; mid++;`
   - Else if `nums[mid] == 1`:
     - `mid++;` (Element is already in correct 1s region!).
   - Else (`nums[mid] == 2`):
     - Swap `nums[mid]` and `nums[high]`.
     - **`high--;`** (Crucial: Do NOT increment `mid` here, because the swapped element from `high` has NOT been processed yet!).

```
Dutch National Flag Swap Rules:
Case 0 (val == 0): swap(nums[low], nums[mid]) -> low++, mid++
Case 1 (val == 1): mid++
Case 2 (val == 2): swap(nums[mid], nums[high]) -> high-- (DO NOT mid++)!
```

### 2.2 Hoare vs Lomuto Partitioning Schemes in Quicksort
* **Lomuto Partition Scheme (Single Direction)**:
  - Uses `pivot = nums[high]`, `i = low`.
  - Scans `j` from `low` to `high - 1`.
  - If `nums[j] < pivot`: Swap `nums[i]` and `nums[j]`, `i++`.
  - Swaps `nums[i]` with `nums[high]` at the end. Performs $\approx 3 \times$ more swaps than Hoare!
* **Hoare Partition Scheme (Two Converging Pointers)**:
  - Uses `pivot = nums[low]`, two pointers `i = low - 1`, `j = high + 1`.
  - Advance `i++` while `nums[i] < pivot`; decrement `j--` while `nums[j] > pivot`.
  - If `i < j`: Swap `nums[i]` and `nums[j]`.
  - Executes **3x fewer swaps** than Lomuto and handles duplicate elements gracefully!

> **Memory Trick:** **"Dutch National Flag: Swap 0s to low (low++, mid++), skip 1s (mid++), swap 2s to high (high-- ONLY, do not mid++)!"**

---

## 3. Characteristics & Partition Array Around Pivot (LeetCode 2161)

### 3.1 Partition Array According to Given Pivot (LeetCode 2161)
Given an array `nums` and pivot `pivot`, reorder `nums` such that:
1. Every element $< \text{pivot}$ appears before every element $= \text{pivot}$.
2. Every element $= \text{pivot}$ appears before every element $> \text{pivot}$.
3. Relative order of elements $< \text{pivot}$ and $> \text{pivot}$ is PRESERVED (Stable Partition!).

```java
public static int[] pivotArray(int[] nums, int pivot) {
    int n = nums.length;
    int[] result = new int[n];
    int left = 0;
    int right = n - 1;

    // Pass 1: Fill elements < pivot from left and > pivot from right
    for (int i = 0, j = n - 1; i < n; i++, j--) {
        if (nums[i] < pivot) {
            result[left++] = nums[i];
        }
        if (nums[j] > pivot) {
            result[right--] = nums[j];
        }
    }

    // Pass 2: Fill remaining middle slots with pivot
    while (left <= right) {
        result[left++] = pivot;
    }

    return result;
}
```

---

## 4. Internal Working Mechanics
Tracing Dutch National Flag (LeetCode 75) on `nums = [2, 0, 2, 1, 1, 0]`:

```
Init: low = 0, mid = 0, high = 5

Step 1: mid=0 (val 2) -> Swap nums[0] & nums[5] -> [0, 0, 2, 1, 1, 2]. high=4. (mid stays 0)
Step 2: mid=0 (val 0) -> Swap nums[0] & nums[0] -> [0, 0, 2, 1, 1, 2]. low=1, mid=1.
Step 3: mid=1 (val 0) -> Swap nums[1] & nums[1] -> [0, 0, 2, 1, 1, 2]. low=2, mid=2.
Step 4: mid=2 (val 2) -> Swap nums[2] & nums[4] -> [0, 0, 1, 1, 2, 2]. high=3. (mid stays 2)
Step 5: mid=2 (val 1) -> Element is 1 -> mid=3.
Step 6: mid=3 (val 1) -> Element is 1 -> mid=4. Loop terminates (mid > high).

Sorted Result: [0, 0, 1, 1, 2, 2] ✅ (Single Pass O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Dutch National Flag 3-Pointer Invariant State Topography:

```
Array:   [ 0,  0 | 1,  1 | 2,  0,  1 | 2,  2 ]
                   ^       ^       ^
                  low     mid     high
                  |       |       |
                 (0s)    (1s)  (Unprocessed) (2s)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Sort Colors DNF (LeetCode 75), Hoare's Partition Scheme, Lomuto's Partition Scheme, and Partition Array Around Pivot (LeetCode 2161):

```java
import java.util.*;

public class PartitioningMaster {

    // 1. Dutch National Flag 3-Way Partitioning (LeetCode 75) O(N) Time, O(1) Space
    public static void sortColors(int[] nums) {
        if (nums == null || nums.length <= 1) return;

        int low = 0;
        int mid = 0;
        int high = nums.length - 1;

        while (mid <= high) {
            if (nums[mid] == 0) {
                swap(nums, low, mid);
                low++;
                mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else { // nums[mid] == 2
                swap(nums, mid, high);
                high--; // DO NOT increment mid!
            }
        }
    }

    // 2. Hoare's Partition Scheme (Two Converging Pointers) O(N) Time, O(1) Space
    public static int hoarePartition(int[] nums, int low, int high) {
        int pivot = nums[low];
        int i = low - 1;
        int j = high + 1;

        while (true) {
            do { i++; } while (nums[i] < pivot);
            do { j--; } while (nums[j] > pivot);

            if (i >= j) return j;

            swap(nums, i, j);
        }
    }

    // 3. Lomuto's Partition Scheme (Single Direction) O(N) Time, O(1) Space
    public static int lomutoPartition(int[] nums, int low, int high) {
        int pivot = nums[high];
        int i = low;

        for (int j = low; j < high; j++) {
            if (nums[j] < pivot) {
                swap(nums, i, j);
                i++;
            }
        }

        swap(nums, i, high);
        return i; // Final pivot position
    }

    // 4. Stable Pivot Partitioning (LeetCode 2161) O(N) Time, O(N) Space
    public static int[] pivotArray(int[] nums, int pivot) {
        int n = nums.length;
        int[] result = new int[n];
        int left = 0;
        int right = n - 1;

        for (int i = 0, j = n - 1; i < n; i++, j--) {
            if (nums[i] < pivot) {
                result[left++] = nums[i];
            }
            if (nums[j] > pivot) {
                result[right--] = nums[j];
            }
        }

        while (left <= right) {
            result[left++] = pivot;
        }

        return result;
    }

    private static void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

> **Quick Syntax:**
```java
// Dutch National Flag 3-Way Pointer Loop
while (mid <= high) {
    if (nums[mid] == 0) swap(nums, low++, mid++);
    else if (nums[mid] == 1) mid++;
    else swap(nums, mid, high--);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 75 - Sort Colors**: Dutch National Flag 3-way partition.
* **LeetCode 215 - Kth Largest Element in an Array**: Quickselect partitioning.
* **LeetCode 2161 - Partition Array According to Given Pivot**: Stable 2-pass pivot partition.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Dutch National Flag, Hoare Partitioning, and Stable Pivot Partitioning:

```java
public class PartitioningDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Dutch National Flag (LeetCode 75) ===");
        int[] colors = {2, 0, 2, 1, 1, 0};
        PartitioningMaster.sortColors(colors);
        System.out.println("Sorted Colors: " + Arrays.toString(colors)); // Output: [0, 0, 1, 1, 2, 2]

        System.out.println("\n=== 2. Hoare Partition Scheme ===");
        int[] arr1 = {4, 1, 3, 9, 7};
        int pivotIdx = PartitioningMaster.hoarePartition(arr1, 0, arr1.length - 1);
        System.out.println("Partitioned Array: " + Arrays.toString(arr1) + " | Split Index: " + pivotIdx);

        System.out.println("\n=== 3. Stable Pivot Partition (LeetCode 2161, Pivot=10) ===");
        int[] arr2 = {9, 12, 5, 10, 14, 3, 10};
        int[] partitioned = PartitioningMaster.pivotArray(arr2, 10);
        System.out.println("Stable Partitioned: " + Arrays.toString(partitioned));
        // Output: [9, 5, 3, 10, 10, 14, 12]
    }
}
```

---

## 9. Complexity Analysis

| Partition Scheme | Time Complexity | Auxiliary Space | Swaps Footprint |
| :--- | :--- | :--- | :--- |
| **Dutch National Flag (75)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Minimized (Single Pass) |
| **Hoare Partition** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| **3x Fewer Swaps than Lomuto ⚡**|
| **Lomuto Partition** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| High Swaps |
| **Stable Pivot (2161)** | **$O(N)$ Linear ⚡** | $O(N)$ Output Array | Zero Swaps (Direct Placement) |

---

## 10. Edge Cases & Boundary Handling
* **Array With Only 1 Color (`[0, 0, 0]`)**: `mid` increments cleanly to $N$, loop terminates.
* **All Elements Equal Pivot in Hoare Scheme**: Converging pointers handle equal elements cleanly without infinite loops.

---

## 11. Common Mistakes & Anti-Patterns
* **Incrementing `mid` When Swapping Case 2 (`nums[mid] == 2`) in DNF**:
  - Writing `swap(nums, mid, high); mid++; high--;` causes bug!
  - The element swapped from `high` into `mid` position has NOT been inspected yet and could be a `0` or `2`!
  - **Only decrement `high--` without incrementing `mid` when processing case 2**.
* **Using Counting Sort for In-Place Sort Colors**:
  - Counting frequency of 0s, 1s, 2s and overwriting array requires 2 full passes.
  - **DNF sorts the array in a SINGLE pass**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `mid` is NOT Incremented on Case 2 in DNF:
> When `nums[mid] == 2`, we swap `nums[mid]` with `nums[high]`.
> The new value now sitting at `nums[mid]` came from an **UNPROCESSED** region (`high`).
> If we increment `mid++`, we bypass checking this newly swapped element, potentially leaving a `0` or `2` in the 1s region!

> **Memory Trick:** **"When nums[mid] == 2, swap with high and ONLY decrement high--! Leave mid unchanged to inspect swapped element!"**

---

## 13. System & Implementation Comparisons

| Feature | Hoare's Partition Scheme | Lomuto's Partition Scheme |
| :--- | :--- | :--- |
| **Pointer Direction** | **Converging (Left & Right) ⚡**| Single Direction (Left-to-Right) |
| **Average Swaps** | **$N / 6$ Swaps (Minimal) ⚡** | $N / 2$ Swaps |
| **Duplicate Handling** | Handles duplicates efficiently | Degrades to $O(N^2)$ if all equal |

---

## 14. How to Recognize This in Questions
* **"Sort array of 0s, 1s, 2s in-place in a single pass"** $\rightarrow$ LeetCode 75 (Dutch National Flag 3-way partition).
* **"Rearrange elements relative to pivot preserving relative order"** $\rightarrow$ LeetCode 2161 (Stable pivot array).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is Hoare's partition scheme preferred over Lomuto's in production C++ `std::sort` / Java sorting libraries?**  
  *A:* Hoare's scheme uses two converging pointers, resulting in roughly $3 \times$ fewer element swaps than Lomuto's scheme. Furthermore, Hoare handles arrays with identical duplicate elements gracefully without degrading partition balance.
* **Q: What is the spatial invariant maintained by the 3 pointers in DNF?**  
  *A:* `nums[0 ... low-1]` contains all 0s, `nums[low ... mid-1]` contains all 1s, `nums[mid ... high]` is unprocessed, and `nums[high+1 ... N-1]` contains all 2s.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO-POINTER PARTITIONING SCHEMES                      |
+-----------------------------------------------------------------------+
| • DNF Invariant: [0..low-1]=0 | [low..mid-1]=1 | [high+1..N-1]=2        |
| • Case 0 (val==0): swap(low, mid) -> low++, mid++                     |
| • Case 1 (val==1): mid++                                              |
| • Case 2 (val==2): swap(mid, high) -> high-- ONLY (DO NOT mid++)!      |
| • Hoare Scheme: Converging pointers (i++, j--); 3x fewer swaps than Lomuto|
| • Stable Pivot (2161): Fill < pivot from left & > pivot from right    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Dutch National Flag Sort Colors (LeetCode 75) in under 3 minutes.
- [ ] I know why `mid` is NOT incremented when swapping case 2 (`nums[mid] == 2`).
- [ ] I can write Hoare's Partitioning scheme with converging pointers.
- [ ] I can solve Partition Array According to Given Pivot (LeetCode 2161).
- [ ] I know why Hoare performs fewer swaps than Lomuto.
