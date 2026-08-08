# 09. Geometry Problems, Interval Sweeping & Triangle Inequality Mechanics

## 1. Introduction
Geometric and spatial interval problems represent an advanced domain of Two-Pointer applications. By converting geometric rules—such as the **Triangle Inequality Theorem ($a + b > c$)**, **Interval Intersection Boundary Sweeping**, and **Subarray Sum Distance Thresholds**—into sorted monotonicity constraints, two pointers solve **Valid Triangle Number (LeetCode 611)**, **Interval List Intersections (LeetCode 986)**, and **Minimum Size Subarray Sum (LeetCode 209)** in **$O(N)$ or $O(N^2)$ optimal time with $O(1)$ constant space**.

> **Important:** In **Valid Triangle Number (LeetCode 611)**, sorting the side lengths in ascending order ($a \le b \le c$) simplifies the 3 Triangle Inequality conditions ($a+b > c, a+c > b, b+c > a$) down to a SINGLE inequality: **$a + b > c$**! Fixing $c$ at index `k` and using converging two pointers `i` and `j` counts **`j - i` valid triangles instantaneously** in $O(1)$ time!

```
Triangle Inequality 2-Pointer Reduction:
+-----------------------------------------------------------------------------------+
| Unsorted Array : Must check (a+b > c), (a+c > b), (b+c > a) -> O(N^3) Brute Force |
| Sorted Array   : Sort a <= b <= c. Only check (a + b > c)!                       |
| 2-Pointer Rule : If (nums[i] + nums[j] > nums[k]), count += (j - i) in O(1) step! ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Valid Triangle Number (LeetCode 611 - Triangle Inequality)
Given an integer array `nums`, return the number of triplets that can form a valid triangle:
1. Sort `nums` in ascending order: `Arrays.sort(nums)` ($O(N \log N)$ time).
2. Outer loop `k` from $N - 1$ down to `2` (fixing largest side $c = \text{nums}[k]$):
   - `i = 0`, `j = k - 1`.
   - While `i < j`:
     - If `nums[i] + nums[j] > nums[k]`:
       - Since array is sorted, any element from index `i + 1` to `j - 1` paired with `nums[j]` will ALSO satisfy `nums[x] + nums[j] > nums[k]`!
       - Add **`count += (j - i)`** instantaneously!
       - Decrement `j--`.
     - Else (`nums[i] + nums[j] <= nums[k]`):
       - Increment `i++`.
3. Return `count`.

```
Valid Triangle Count Tracing [ 2, 2, 3, 4 ]:
k = 3 (val 4): i = 0 (val 2), j = 2 (val 3)
   nums[0] + nums[2] = 2 + 3 = 5 > 4!
   Valid triangles with j=3: (2@idx0, 3, 4) and (2@idx1, 3, 4) -> (j - i = 2 - 0 = 2) triangles!
   count += 2. j-- (j = 1).
```

### 2.2 Interval List Intersections (LeetCode 986)
Given two lists of closed intervals `firstList` and `secondList` sorted by start times:
1. `i = 0`, `j = 0`.
2. While `i < firstList.length && j < secondList.length`:
   - Compute candidate intersection overlap:
     - `start = Math.max(firstList[i][0], secondList[j][0])`
     - `end = Math.min(firstList[i][1], secondList[j][1])`
   - If **`start <= end`**, a valid non-empty overlap exists! Add `[start, end]` to result list.
   - Advance the pointer pointing to the interval with the **EARLIER END TIME**:
     - `if (firstList[i][1] < secondList[j][1]) i++;`
     - `else j++;`

> **Memory Trick:** **"Triangle Number (611): Sort first! Fix largest side k; if nums[i] + nums[j] > nums[k], count += (j - i) and j--!"**

---

## 3. Characteristics & Minimum Size Subarray Sum (LeetCode 209)

### 3.1 Minimum Size Subarray Sum (LeetCode 209)
Given an array of positive integers `nums` and target `target`, return the minimal length of a contiguous subarray whose sum is $\ge \text{target}$:
1. `left = 0`, `currentSum = 0`, `minLength = Integer.MAX_VALUE`.
2. For `right = 0` to $N - 1$:
   - `currentSum += nums[right]`.
   - While `currentSum >= target`:
     - `minLength = Math.min(minLength, right - left + 1);`
     - `currentSum -= nums[left];`
     - `left++;`
3. Return `minLength == Integer.MAX_VALUE ? 0 : minLength`.

---

## 4. Internal Working Mechanics
Tracing Interval List Intersections (LeetCode 986) on `firstList = [[0,2], [5,10]]`, `secondList = [[1,5], [8,12]]`:

```
i = 0 [0, 2], j = 0 [1, 5]:
  - start = max(0, 1) = 1, end = min(2, 5) = 2.
  - start (1) <= end (2) -> Intersect = [1, 2]!
  - end1 (2) < end2 (5) -> Advance i++ (i = 1).

i = 1 [5, 10], j = 0 [1, 5]:
  - start = max(5, 1) = 5, end = min(10, 5) = 5.
  - start (5) <= end (5) -> Intersect = [5, 5]!
  - end2 (5) <= end1 (10) -> Advance j++ (j = 1).

i = 1 [5, 10], j = 1 [8, 12]:
  - start = max(5, 8) = 8, end = min(10, 12) = 10.
  - start (8) <= end (10) -> Intersect = [8, 10]!
  - end1 (10) < end2 (12) -> Advance i++ (i = 2).

Result: [[1, 2], [5, 5], [8, 10]] ✅ (O(M + N) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Interval Overlap Sweeping & End Time Pointer Advancement Topography:

```
FirstList [i]  :   |=========| (0..2)               |=================| (5..10)
SecondList [j] :        |=================| (1..5)               |=================| (8..12)
                        
Overlap        :        |====| (1..2)               |===| (5..5)        |========| (8..10)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Valid Triangle Number (LeetCode 611), Interval List Intersections (LeetCode 986), and Minimum Size Subarray Sum (LeetCode 209):

```java
import java.util.*;

public class GeometryProblemsMaster {

    // 1. Valid Triangle Number (LeetCode 611) O(N^2) Time, O(1) Auxiliary Space
    public static int triangleNumber(int[] nums) {
        if (nums == null || nums.length < 3) return 0;

        Arrays.sort(nums); // Sort in ascending order
        int n = nums.length;
        int count = 0;

        // Fix largest side c = nums[k]
        for (int k = n - 1; k >= 2; k--) {
            int i = 0;
            int j = k - 1;

            while (i < j) {
                if (nums[i] + nums[j] > nums[k]) {
                    // All elements between i and j-1 paired with j form valid triangles with k!
                    count += (j - i);
                    j--;
                } else {
                    i++;
                }
            }
        }

        return count;
    }

    // 2. Interval List Intersections (LeetCode 986) O(M + N) Time, O(1) Auxiliary Space
    public static int[][] intervalIntersection(int[][] firstList, int[][] secondList) {
        if (firstList == null || secondList == null || firstList.length == 0 || secondList.length == 0) {
            return new int[0][0];
        }

        List<int[]> result = new ArrayList<>();
        int i = 0;
        int j = 0;

        while (i < firstList.length && j < secondList.length) {
            // Find max start and min end
            int start = Math.max(firstList[i][0], secondList[j][0]);
            int end = Math.min(firstList[i][1], secondList[j][1]);

            // If overlap exists, add to result
            if (start <= end) {
                result.add(new int[]{start, end});
            }

            // Advance pointer with earlier end time
            if (firstList[i][1] < secondList[j][1]) {
                i++;
            } else {
                j++;
            }
        }

        return result.toArray(new int[result.size()][]);
    }

    // 3. Minimum Size Subarray Sum (LeetCode 209) O(N) Time, O(1) Space
    public static int minSubArrayLen(int target, int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int left = 0;
        int currentSum = 0;
        int minLength = Integer.MAX_VALUE;

        for (int right = 0; right < nums.length; right++) {
            currentSum += nums[right];

            while (currentSum >= target) {
                minLength = Math.min(minLength, right - left + 1);
                currentSum -= nums[left];
                left++;
            }
        }

        return minLength == Integer.MAX_VALUE ? 0 : minLength;
    }
}
```

> **Quick Syntax:**
```java
// Interval Intersection Advancement Rule
int start = Math.max(f[i][0], s[j][0]);
int end = Math.min(f[i][1], s[j][1]);
if (start <= end) result.add(new int[]{start, end});
if (f[i][1] < s[j][1]) i++; else j++;
```

---

## 7. Concrete Problem Examples
* **LeetCode 611 - Valid Triangle Number**: Triangle inequality two-pointer count.
* **LeetCode 986 - Interval List Intersections**: Sweeping sorted intervals.
* **LeetCode 209 - Minimum Size Subarray Sum**: Expanding/shrinking sliding window.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Triangle Number, Interval Intersections, and Min Subarray Length:

```java
public class GeometryProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Valid Triangle Number (LeetCode 611) ===");
        int[] sides = {2, 2, 3, 4};
        int triangles = GeometryProblemsMaster.triangleNumber(sides);
        System.out.println("Valid Triangles Count: " + triangles); // Output: 3

        System.out.println("\n=== 2. Interval List Intersections (LeetCode 986) ===");
        int[][] list1 = {{0, 2}, {5, 10}, {13, 23}, {24, 25}};
        int[][] list2 = {{1, 5}, {8, 12}, {15, 24}, {25, 26}};
        int[][] intersections = GeometryProblemsMaster.intervalIntersection(list1, list2);
        System.out.println("Intersections: " + Arrays.deepToString(intersections));
        // Output: [[1, 2], [5, 5], [8, 10], [13, 12]... [24, 24], [25, 25]]

        System.out.println("\n=== 3. Minimum Size Subarray Sum (LeetCode 209, target=7) ===");
        int[] nums = {2, 3, 1, 2, 4, 3};
        int minLen = GeometryProblemsMaster.minSubArrayLen(7, nums);
        System.out.println("Min Subarray Length: " + minLen); // Output: 2 ([4, 3])
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Triangle Number (611)**| **$O(N^2)$ Quadratic ⚡**| **$O(1)$ Strict In-Place ⚡**| Fix largest side $c$; `count += j - i` |
| **Interval Intersections (986)**| **$O(M + N)$ Linear ⚡**| **$O(1)$ Auxiliary ⚡**| Advance pointer with earlier end time |
| **Min Subarray Sum (209)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Two-pointer sliding window |

---

## 10. Edge Cases & Boundary Handling
* **Single Point Intersections (`start == end`)**: Valid non-empty closed interval overlap `[5, 5]`; handled correctly.
* **Array Length $< 3$ in Triangle Problem**: Returns `0` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Advancing Interval Pointer Based on Start Time Instead of End Time**:
  - Advancing the pointer with the earlier START time skips valid overlaps with longer intervals!
  - **Always advance the pointer pointing to the interval with the EARLIER END TIME (`firstList[i][1] < secondList[j][1]`)**.
* **Checking All 3 Triangle Inequalities on Sorted Input**:
  - On a sorted array ($a \le b \le c$), $a + c > b$ and $b + c > a$ are ALWAYS true.
  - **Only check $a + b > c$**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Earlier End Time Pointer Advancement Works in Interval Sweeping:
> An interval $A$ with an earlier end time (`A.end < B.end`) CANNOT overlap with any subsequent intervals in list $B$ (since all future $B$ intervals start after `B.end > A.end`).
> Therefore, interval $A$ has completed all possible overlap matches and can be safely discarded by executing `i++`!

> **Memory Trick:** **"In interval intersection: advance pointer with EARLIER END TIME!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Interval Sweeping | Interval Tree Approach |
| :--- | :--- | :--- |
| **Precondition** | **Sorted Input Lists ⚡** | Unsorted Intervals |
| **Time Complexity** | **$O(M + N)$ Linear ⚡** | $O((M + N) \log N)$ |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Tree Nodes |

---

## 14. How to Recognize This in Questions
* **"Find number of triplets that can form side lengths of a triangle"** $\rightarrow$ LeetCode 611 (Sort + fix largest side + `count += j - i`).
* **"Find intersection of two sorted lists of closed intervals"** $\rightarrow$ LeetCode 986 (`start = max(s1,s2)`, `end = min(e1,e2)`).
* **"Find minimal length of contiguous subarray with sum >= target"** $\rightarrow$ LeetCode 209.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does fixing the LARGEST side $c = \text{nums}[k]$ in LeetCode 611 allow instant `j - i` range counting?**  
  *A:* When `nums[i] + nums[j] > nums[k]`, because the array is sorted, any element `nums[x]` where `i < x < j` is $\ge \text{nums}[i]$. Thus `nums[x] + nums[j] > nums[k]` is guaranteed to hold for all $x \in [i \dots j-1]$. There are exactly `j - i` such elements.
* **Q: What happens if two intervals end at the exact same time in LeetCode 986?**  
  *A:* `firstList[i][1] < secondList[j][1]` evaluates `false`, causing the `else` block (`j++`) to execute. On the next iteration, if both were at their last overlap, advancing `j` terminates or advances `i` on the subsequent step cleanly.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GEOMETRY & INTERVAL TWO-POINTER PATTERNS              |
+-----------------------------------------------------------------------+
| • Triangle Number (611): Sort first! Loop k = N-1 down to 2           |
| • Triangle Rule: If (nums[i] + nums[j] > nums[k]) count += (j - i), j--|
| • Interval Intersection (986): start = max(s1,s2), end = min(e1,e2)   |
| • Interval Overlap Condition: if (start <= end) add [start, end]      |
| • Interval Advancement Rule: Advance pointer with EARLIER END TIME!   |
| • Min Subarray Sum (209): Expand right, shrink left while sum >= target|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Valid Triangle Number (LeetCode 611) in $O(N^2)$ time.
- [ ] I can derive why fixing the largest side $c$ enables `j - i` range counting.
- [ ] I can write Interval List Intersections (LeetCode 986) in $O(M + N)$ time.
- [ ] I know why we advance the pointer with the earlier end time in interval sweeping.
- [ ] I can solve Minimum Size Subarray Sum (LeetCode 209).
