# 11. Two Pointers Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Recognizing two-pointer problem patterns instantly during a technical coding interview allows solving search, partitioning, and sequence mutation problems in **$O(N)$ linear time and $O(1)$ constant space**. Two-pointer problems fit into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal pointer strategies, along with copy-paste production Java templates.

> **Important:** Master the primary two-pointer selection invariants:
> 1. **Opposite Direction (Converging)**: Use when sequence is sorted or contains mountain peaks (`left = 0, right = N - 1`).
> 2. **Same Direction (Read-Write)**: Use for in-place array transformations (`write = 0`, scan `read`).
> 3. **Fast & Slow**: Use for cycle detection and middle finding.

---

## 2. Master Two Pointers Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER TWO POINTERS PROBLEM DECISION MATRIX                                                      |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Find pair/triplet in sorted array matching sum"  | Opposite Direction    | `left++` or `right--` |
| "Container water / trapping rain water in O(1) mem"| Converging Water Boundary| Move shorter height|
| "Remove duplicates in-place (allow at most K)"    | Read-Write Truncation | `nums[write - K]`     |
| "Happy number digit sum cycle / circular loop"    | Fast & Slow Pointers  | `slow 1x, fast 2x`    |
| "Sort 0s, 1s, 2s in single pass (Sort Colors)"    | Dutch National Flag   | 3 Pointers (`low,mid,high`)|
| "Find overlapping intervals in sorted lists"      | Interval Sweeping     | Advance earlier end   |
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Opposite Direction Pair/Triplet Search Template
* **Signal**: Sorted array target sum search (167, 15).

```java
public static int[] twoSumSortedTemplate(int[] numbers, int target) {
    int left = 0;
    int right = numbers.length - 1;

    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return new int[]{left + 1, right + 1};
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }

    return new int[]{-1, -1};
}
```

---

## 4. Pattern 2: Same Direction $K$-Duplicate Truncation Template
* **Signal**: In-place duplicate truncation allowing at most $K$ duplicates (26, 80).

```java
public static int removeDuplicatesKTemplate(int[] nums, int k) {
    if (nums == null || nums.length <= k) return nums == null ? 0 : nums.length;

    int write = k;
    for (int read = k; read < nums.length; read++) {
        if (nums[read] != nums[write - k]) {
            nums[write++] = nums[read];
        }
    }

    return write;
}
```

---

## 5. Pattern 3: Dutch National Flag 3-Way Partitioning Template
* **Signal**: Sorting 3 distinct elements/colors in-place in a single pass (75).

```java
public static void sortColorsTemplate(int[] nums) {
    int low = 0, mid = 0, high = nums.length - 1;

    while (mid <= high) {
        if (nums[mid] == 0) {
            int temp = nums[low]; nums[low] = nums[mid]; nums[mid] = temp;
            low++; mid++;
        } else if (nums[mid] == 1) {
            mid++;
        } else {
            int temp = nums[mid]; nums[mid] = nums[high]; nums[high] = temp;
            high--; // DO NOT mid++!
        }
    }
}
```

---

## 6. Pattern 4: Generalized $K$-Sum Recursive Engine Template
* **Signal**: Finding all unique $K$-element combinations summing to target (18).

```java
public static List<List<Integer>> kSumTemplate(int[] nums, long target, int k, int start) {
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;
    if (start >= n) return result;

    if (k == 2) {
        int left = start, right = n - 1;
        while (left < right) {
            long sum = (long) nums[left] + nums[right];
            if (sum == target) {
                result.add(Arrays.asList(nums[left], nums[right]));
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++; right--;
            } else if (sum < target) left++;
            else right--;
        }
        return result;
    }

    for (int i = start; i < n - k + 1; i++) {
        if (i > start && nums[i] == nums[i - 1]) continue;
        if ((long) nums[i] * k > target) break;
        if ((long) nums[i] + (long) (k - 1) * nums[n - 1] < target) continue;

        List<List<Integer>> sub = kSumTemplate(nums, target - nums[i], k - 1, i + 1);
        for (List<Integer> list : sub) {
            List<Integer> quad = new ArrayList<>();
            quad.add(nums[i]);
            quad.addAll(list);
            result.add(quad);
        }
    }

    return result;
}
```

---

## 7. Pattern 5: Converging Water Boundary Trapping Template
* **Signal**: Max area container or trapped rain water calculation (11, 42).

```java
public static int maxAreaTemplate(int[] height) {
    int left = 0, right = height.length - 1, maxWater = 0;

    while (left < right) {
        int width = right - left;
        maxWater = Math.max(maxWater, width * Math.min(height[left], height[right]));
        if (height[left] < height[right]) left++;
        else right--;
    }

    return maxWater;
}
```

---

## 8. Pattern 6: Interval Overlap Sweeping Template
* **Signal**: Finding intersection of two sorted closed interval lists (986).

```java
public static int[][] intervalIntersectionTemplate(int[][] f, int[][] s) {
    List<int[]> res = new ArrayList<>();
    int i = 0, j = 0;

    while (i < f.length && j < s.length) {
        int start = Math.max(f[i][0], s[j][0]);
        int end = Math.min(f[i][1], s[j][1]);
        if (start <= end) res.add(new int[]{start, end});

        if (f[i][1] < s[j][1]) i++;
        else j++;
    }

    return res.toArray(new int[res.size()][]);
}
```

---

## 9. Edge Case & Trap Checklist
* **32-Bit Integer Overflow in Sums**: Always cast large sum targets to `(long)`.
* **Case 2 in Dutch National Flag (`nums[mid] == 2`)**: Only decrement `high--` (do NOT `mid++`).
* **Infinite Loops in 3Sum**: Always execute `left++` and `right--` after matching a target triplet.
* **Negative Modulo in Circular Move**: Add $N$ if `(curr + step) % N < 0`.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: TWO POINTER PATTERN RECOGNITION                      |
+-----------------------------------------------------------------------+
| 1. Opposite Direction: left=0, right=N-1; sorted array target search  |
| 2. Same Direction (K-Duplicates): nums[read] != nums[write - K]       |
| 3. Dutch National Flag: Case 2 (val==2) swap(mid, high) & high-- ONLY |
| 4. Container Water (11): Always move pointer at shorter vertical height|
| 5. Trapping Water (42): Process smaller boundary height; O(1) space ⚡ |
| 6. K-Sum (18): (K-2) anchor loops + 2Sum; cast target/sum to long!    |
| 7. Triangle Number (611): Fix largest side c; count += (j - i)        |
| 8. Interval Sweeping (986): Advance pointer with EARLIER END TIME!    |
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why `nums[write - K]` handles $K$-duplicate truncation.
- [ ] I know why `mid` is not incremented on case 2 in DNF.
- [ ] I can write 64-bit safe 4Sum (LeetCode 18).
