# 12. Master Reference — Two Pointers

## 1. Introduction
This Master Reference consolidates all mathematical proofs, pointer invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 7: Two Pointers**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Opposite Direction converging search (`left++` / `right--`), Same Direction Read-Write $K$-Duplicate Truncation (`nums[read] != nums[write - K]`), Dutch National Flag 3-pointer rules (`low, mid, high`), 3Sum 3-tier duplicate skipping, Trapping Rain Water 2-pointer boundaries, Generalized $K$-Sum 64-bit `long` casting, and Interval Sweeping earlier-end advancement!

---

## 2. Master Mathematical & Pointer Formula Cheat Sheet
* **Monotonicity Search Reduction**: On a sorted array, comparing `nums[left] + nums[right]` against `target` discards an entire row/column of $N$ candidate pairs in $O(1)$ constant time, reducing $O(N^2)$ brute-force search down to **$O(N)$ Linear Time**.
* **Generalized $K$-Duplicate Truncation Invariant**:
  - `if (nums[read] != nums[write - K]) nums[write++] = nums[read];`
  - Valid for any sorted array truncation (LeetCode 26 for $K=1$, LeetCode 80 for $K=2$).
* **Dutch National Flag 3-Way Invariant**:
  - `[0 ... low - 1]`: All 0s
  - `[low ... mid - 1]`: All 1s
  - `[mid ... high]`: Unprocessed region
  - `[high + 1 ... N - 1]`: All 2s
  - Case 2 (`nums[mid] == 2`): `swap(nums, mid, high); high--;` (**DO NOT `mid++`**).
* **Generalized $K$-Sum Time Complexity**: $O(N^{K-1})$ Time across all $K \ge 2$.
* **Valid Triangle Inequality Count**: If `nums[i] + nums[j] > nums[k]` (where $a \le b \le c$), add **`count += (j - i)`** in $O(1)$ time!
* **Interval Overlap Calculation**: `start = max(f[i][0], s[j][0])`, `end = min(f[i][1], s[j][1])`. Valid overlap iff `start <= end`. Advance pointer with `min(f[i][1], s[j][1])`.

```
Two Pointers Invariants & Structures Summary:
+-----------------------------------+---------------------------------------------------+
| Two Pointers Variant              | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Converging 2Sum                   | Sorted array; if sum < target left++ else right-- |
| K-Duplicate Truncation            | nums[read] != nums[write - K]                     |
| Container Water Greedy            | Always move pointer at shorter vertical height    |
| Dutch National Flag               | Case 0: swap(low++, mid++); Case 2: swap(mid, high--)|
| 3Sum Unique Triplets              | Skip duplicate anchor i AND inner left/right      |
| K-Sum Overflow Guard              | Cast sub-target & sum additions to (long)         |
| Interval Sweeping                 | Advance pointer with EARLIER END TIME!            |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Two Sum II (167)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Converging two pointers on sorted array |
| **Remove Duplicates (26)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Read-Write pointer `nums[write - 1]` |
| **Remove Duplicates II (80)**| **$O(N)$ Linear ⚡**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Read-Write pointer `nums[write - 2]` |
| **Move Zeroes (283)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Swap non-zeroes to `write` pointer |
| **Container Water (11)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Move shorter height pointer |
| **Trapping Water (42)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| 2-Pointer max elevation boundary |
| **Valid Palindrome (125)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Converging alphanumeric matching |
| **3Sum (15)** | **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(1)$ Strict In-Place ⚡**| 1 Anchor + 2Sum; 3-tier duplicate skip |
| **3Sum Closest (16)** | **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(1)$ Strict In-Place ⚡**| Track `abs(sum - target)` |
| **4Sum (18)** | **$O(N^3)$ Cubic ⚡** | **$O(N^3)$ Cubic ⚡** | **$O(N^3)$ Cubic ⚡** | **$O(1)$ Auxiliary ⚡**| 2 Anchors + 2Sum; `long` target cast |
| **Generalized K-Sum** | **$O(N^{K-1})$ ⚡** | **$O(N^{K-1})$ ⚡** | **$O(N^{K-1})$ ⚡** | $O(K)$ Call Stack | (K-2) Anchors + 2Sum base case |
| **Sort Colors DNF (75)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| 3-Way partition `low, mid, high` |
| **Triangle Number (611)**| **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(N^2)$ Quadratic⚡**| **$O(1)$ Strict In-Place ⚡**| Fix largest side $c$; `count += j - i` |
| **Interval Overlap (986)**| **$O(M + N)$ Linear ⚡**| **$O(M + N)$ Linear ⚡**| **$O(M + N)$ Linear ⚡**| **$O(1)$ Auxiliary ⚡**| Advance pointer with earlier end time |
| **Mountain Array (845)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Peak check + `i = right` slope skip |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Two-Pointer Array Operations                                 |
+-----------------------------------------------------------------------------------+
| In-Place Mutation (26, 80, 283, 75) : 0 Bytes Auxiliary Memory (In-Place Array Ops)⚡ |
| Output Array Operations (977, 2149) : 4N Bytes Primitive Array Output             |
| Hash Map Comparison                 : 32 Bytes per Map Entry (High Memory Footprint)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Opposite Converging Two-Pointer Loop
int left = 0, right = nums.length - 1;
while (left < right) {
    int sum = nums[left] + nums[right];
    if (sum == target) return new int[]{left + 1, right + 1};
    else if (sum < target) left++;
    else right--;
}

// 2. Generalized K-Duplicate Truncation
int write = k;
for (int read = k; read < nums.length; read++) {
    if (nums[read] != nums[write - k]) nums[write++] = nums[read];
}

// 3. Dutch National Flag 3-Way Partitioning
while (mid <= high) {
    if (nums[mid] == 0) swap(nums, low++, mid++);
    else if (nums[mid] == 1) mid++;
    else swap(nums, mid, high--); // DO NOT mid++!
}

// 4. Container With Most Water Greedy Move
if (height[left] < height[right]) left++;
else right--;

// 5. Interval Overlap Advancement
if (firstList[i][1] < secondList[j][1]) i++;
else j++;
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: 32-Bit Integer Overflow in 4Sum**: Adding 4 large integers exceeds `Integer.MAX_VALUE`. Always cast sum additions and remaining targets to `long`.
* **Pitfall 2: Incrementing `mid` on Case 2 in Dutch National Flag (`nums[mid] == 2`)**: Swapping with `high` brings an UNPROCESSED element into `mid`. Incrementing `mid++` skips checking this element!
* **Pitfall 3: Moving Taller Pointer in Container With Most Water**: Moving the taller line reduces width without increasing height, guaranteeing smaller areas. Always move the **shorter line pointer**.
* **Pitfall 4: Advancing Interval Pointer by Start Time Instead of End Time**: Advancing by start time skips valid overlaps with longer intervals. Always advance the pointer pointing to the **earlier end time**.
* **Pitfall 5: Forgetting Inner Duplicate Skipping in 3Sum**: Omitting `while (left < right && nums[left] == nums[left+1]) left++` produces duplicate output triplets.
* **Pitfall 6: Not Skipping Descending Slope in Longest Mountain (845)**: Incrementing `i++` after mountain expansion causes $O(N^2)$ time. Set **`i = right`** to skip the descending slope in $O(N)$ time.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 7 (TWO POINTERS)                 |
+-----------------------------------------------------------------------+
| 1. Monotonicity Search: Discards 1 row/col per step; O(N^2) -> O(N) ⚡  |
| 2. K-Duplicate Rule: nums[read] != nums[write - K] for any K >= 1     |
| 3. Move Zeroes (283): Swap non-zeroes to write pointer in-place       |
| 4. Container Water (11): Always move pointer at shorter height        |
| 5. Trapping Water (42): Process smaller boundary height; O(1) space ⚡ |
| 6. DNF 3-Way (75): Case 2 (val==2) swap(mid, high) & high-- ONLY      |
| 7. 3Sum (15): Skip duplicate anchor i AND inner left/right pointers    |
| 8. 4Sum (18): Cast sums to long! Use generalized kSum(K-1, target-nums[i])|
| 9. Triangle Number (611): Fix largest side c; count += (j - i)        |
| 10. Interval Sweeping (986): Advance pointer with EARLIER END TIME!   |
| 11. Happy Number (202): slow = f(slow), fast = f(f(fast)) in O(1) space|
| 12. Mountain Array (845): Check peak & set i = right for O(N) time    |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Two Sum II (LeetCode 167) in under 2 minutes.
- [ ] I can state the generalized $K$-duplicate invariant `nums[write - K]`.
- [ ] I can write Move Zeroes (LeetCode 283) in-place.
- [ ] I can prove why moving the shorter line pointer in Container Water (LeetCode 11) is optimal.
- [ ] I can solve Trapping Rain Water (LeetCode 42) in $O(1)$ space using 2 pointers.
- [ ] I can write Dutch National Flag Sort Colors (LeetCode 75) in a single pass.
- [ ] I know why `mid` is not incremented on case 2 in DNF.
- [ ] I can write 3Sum (LeetCode 15) with 3-tier duplicate skipping in $O(1)$ space.
- [ ] I can write 64-bit safe 4Sum (LeetCode 18) and Generalized $K$-Sum.
- [ ] I can solve Valid Triangle Number (LeetCode 611) using `count += j - i`.
- [ ] I can write Interval List Intersections (LeetCode 986) in $O(M + N)$ time.
- [ ] I can solve Longest Mountain in Array (LeetCode 845) in $O(N)$ time.
