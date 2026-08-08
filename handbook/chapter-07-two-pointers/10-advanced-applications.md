# 10. Advanced Applications: Array Mountains, Domino Physics Simulation & Sign Rearrangement

## 1. Introduction
Advanced applications of the Two Pointers pattern combine multiple structural constraints—such as bidirectional peak expansion, physics forces simulation, and alternating sign index assignment—into high-performance algorithms. Problems like **Longest Mountain in Array (LeetCode 845)**, **Push Dominoes (LeetCode 838)**, and **Rearrange Array Elements by Sign (LeetCode 2149)** demonstrate how two pointers maintain state invariants across complex linear sequences in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** In **Push Dominoes (LeetCode 838)**, simulating falling domino forces between two adjacent non-standing boundary markers (`L` and `R`) allows processing segments independently! By maintaining `left` and `right` boundary pointers, domino orientation across intermediate standing dominoes (`.`) is calculated in **$O(1)$ constant time per segment**!

```
Domino Physics 2-Pointer Boundary States:
+-----------------------+---------------------------------------------------+
| Boundary Pattern      | Resulting Domino Forces Between Boundaries        |
+-----------------------+---------------------------------------------------+
| L ... L               | All intermediate dominoes fall LEFT: L L L L L    |
| R ... R               | All intermediate dominoes fall RIGHT: R R R R R   |
| L ... R               | No forces meet in middle: L . . . R (Unchanged)   |
| R ... L               | Forces collide in middle: R R R . L L L           |
+-----------------------+---------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Push Dominoes Physics Simulation (LeetCode 838)
Given a string `dominoes` representing initial states (`L`, `R`, `.`), determine the final standing state after forces propagate:
1. Pad string with imaginary boundaries: `S = "L" + dominoes + "R"`.
2. Maintain `left = 0`, `right = 1`.
3. Iterate `right` across $S$:
   - If `S[right] == '.'`, continue.
   - Process segment between `left` and `right`:
     - If `S[left] == S[right]`: Fill all intermediate `.` with `S[left]`.
     - Else if `S[left] == 'R' && S[right] == 'L'`: Fill first half with `R`, second half with `L`, and middle `.` (if odd length) remains `.`.
     - Else (`S[left] == 'L' && S[right] == 'R'`): Leave intermediate `.` unchanged.
   - Advance `left = right`.

### 2.2 Longest Mountain in Array (LeetCode 845 - Bidirectional Expansion)
A mountain is defined as a contiguous subarray of length $\ge 3$ where elements strictly increase to a single peak node and then strictly decrease.
* **Algorithm**:
  1. `i = 1`, `maxMountain = 0`.
  2. While `i < N - 1`:
     - Check if `i` is a valid peak: **`nums[i - 1] < nums[i] && nums[i] > nums[i + 1]`**.
     - If `i` is a peak:
       - Expand left pointer `left = i - 1` while `left > 0 && nums[left - 1] < nums[left]`.
       - Expand right pointer `right = i + 1` while `right < N - 1 && nums[right] > nums[right + 1]`.
       - Calculate mountain length: `mountainLen = right - left + 1`.
       - `maxMountain = Math.max(maxMountain, mountainLen)`.
       - Advance `i = right` (Skip already processed descending slope!).
     - Else: `i++`.

> **Memory Trick:** **"Mountain Peak: Check nums[i-1] < nums[i] > nums[i+1]! Expand left and right pointers outward!"**

---

## 3. Characteristics & Rearrange Array Elements by Sign (LeetCode 2149)

### 3.1 Rearrange Array Elements by Sign (LeetCode 2149)
Given an array `nums` of even length containing equal numbers of positive and negative integers:
* Rearrange elements such that every consecutive pair has opposite signs, starting with a positive integer, while preserving original relative order.
* **Two Pointers Placement Algorithm**:
  1. `posIdx = 0` (for even indices $0, 2, 4 \dots$).
  2. `negIdx = 1` (for odd indices $1, 3, 5 \dots$).
  3. Create result array `int[] result = new int[N]`.
  4. Iterate `num` in `nums`:
     - If `num > 0`: `result[posIdx] = num; posIdx += 2;`
     - Else: `result[negIdx] = num; negIdx += 2;`
  5. Return `result`.

```
Sign Rearrangement Index Progression:
Positive Numbers -> Placed at posIdx = 0, 2, 4, 6 ...
Negative Numbers -> Placed at negIdx = 1, 3, 5, 7 ...
Preserves original relative order in a SINGLE pass! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Push Dominoes (LeetCode 838) on `.L.R...LR..`:

```
Padded String: L . L . R . . . L R . . R
Indices      : 0 1 2 3 4 5 6 7 8 9 10 11 12

Segment 1 (left=0 'L', right=2 'L'): Same sign 'L' -> Fill index 1 with 'L'.
Segment 2 (left=2 'L', right=4 'R'): L...R -> Intermediate index 3 stays '.'.
Segment 3 (left=4 'R', right=8 'L'): R...L -> Intermediates 5,6,7 -> Fill 5 with 'R', 6 with '.', 7 with 'L'.
Segment 4 (left=8 'L', right=9 'R'): L...R -> Unchanged.
Segment 5 (left=9 'R', right=12 'R'): Same sign 'R' -> Fill 10,11 with 'R'.

Final Result: "LL.RR.LLRRRR" ✅ (O(N) Time, O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Longest Mountain Array Bidirectional Pointer Expansion Topography:

```
                      ( Peak Node: 5 )
                         /        \
                        /          \
                       3            4
                      /              \
         ( left ) -> 1                2 <- ( right )
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Push Dominoes (LeetCode 838), Longest Mountain in Array (LeetCode 845), and Rearrange Array Elements by Sign (LeetCode 2149):

```java
import java.util.*;

public class AdvancedApplicationsMaster {

    // 1. Push Dominoes Physics Simulation (LeetCode 838) O(N) Time, O(N) Space
    public static String pushDominoes(String dominoes) {
        if (dominoes == null || dominoes.length() <= 1) return dominoes;

        String S = "L" + dominoes + "R";
        int n = S.length();
        char[] result = S.toCharArray();

        int left = 0;
        for (int right = 1; right < n; right++) {
            if (result[right] == '.') continue;

            int span = right - left - 1;
            if (span > 0) {
                if (result[left] == result[right]) {
                    // Both boundaries are same sign: Fill all intermediate dominoes
                    for (int k = left + 1; k < right; k++) {
                        result[k] = result[left];
                    }
                } else if (result[left] == 'R' && result[right] == 'L') {
                    // Opposite boundaries R...L: Forces collide in middle
                    for (int k = 1; k <= span / 2; k++) {
                        result[left + k] = 'R';
                        result[right - k] = 'L';
                    }
                }
                // Case L...R: Unchanged (forces pull away)
            }

            left = right; // Advance left boundary
        }

        return new String(result, 1, dominoes.length());
    }

    // 2. Longest Mountain in Array (LeetCode 845) O(N) Time, O(1) Auxiliary Space
    public static int longestMountain(int[] arr) {
        if (arr == null || arr.length < 3) return 0;

        int n = arr.length;
        int maxMountain = 0;
        int i = 1;

        while (i < n - 1) {
            // Check if i is a valid peak
            boolean isPeak = arr[i - 1] < arr[i] && arr[i] > arr[i + 1];

            if (isPeak) {
                // Expand left pointer
                int left = i - 1;
                while (left > 0 && arr[left - 1] < arr[left]) {
                    left--;
                }

                // Expand right pointer
                int right = i + 1;
                while (right < n - 1 && arr[right] > arr[right + 1]) {
                    right++;
                }

                int currentLen = right - left + 1;
                maxMountain = Math.max(maxMountain, currentLen);

                // Advance i to right (Skip descending slope!)
                i = right;
            } else {
                i++;
            }
        }

        return maxMountain;
    }

    // 3. Rearrange Array Elements by Sign (LeetCode 2149) O(N) Time, O(N) Space
    public static int[] rearrangeArray(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        int posIdx = 0; // Even indices for positive numbers
        int negIdx = 1; // Odd indices for negative numbers

        for (int num : nums) {
            if (num > 0) {
                result[posIdx] = num;
                posIdx += 2;
            } else {
                result[negIdx] = num;
                negIdx += 2;
            }
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// Peak Check and Skip Descending Slope Optimization
if (arr[i - 1] < arr[i] && arr[i] > arr[i + 1]) {
    ... // Expand left and right
    i = right; // Skip descending slope!
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 838 - Push Dominoes**: Physics force boundary simulation.
* **LeetCode 845 - Longest Mountain in Array**: Peak detection + bidirectional expansion.
* **LeetCode 2149 - Rearrange Array Elements by Sign**: Dual pointer index placement.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Push Dominoes, Longest Mountain, and Rearrange Array by Sign:

```java
public class AdvancedApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Push Dominoes Simulation (LeetCode 838) ===");
        String dominoes = ".L.R...LR..";
        String finalState = AdvancedApplicationsMaster.pushDominoes(dominoes);
        System.out.println("Final State: " + finalState); // Output: "LL.RR.LLRRRR"

        System.out.println("\n=== 2. Longest Mountain in Array (LeetCode 845) ===");
        int[] mountainArr = {2, 1, 4, 7, 3, 2, 5};
        int longestMtn = AdvancedApplicationsMaster.longestMountain(mountainArr);
        System.out.println("Longest Mountain Length: " + longestMtn); // Output: 5 ([1, 4, 7, 3, 2])

        System.out.println("\n=== 3. Rearrange Array by Sign (LeetCode 2149) ===");
        int[] nums = {3, 1, -2, -5, 2, -4};
        int[] rearranged = AdvancedApplicationsMaster.rearrangeArray(nums);
        System.out.println("Rearranged Array: " + Arrays.toString(rearranged));
        // Output: [3, -2, 1, -5, 2, -4]
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Push Dominoes (838)** | **$O(N)$ Linear ⚡** | $O(N)$ Result String | 2-Pointer segment boundary filling |
| **Longest Mountain (845)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `i = right` skips descending slope |
| **Rearrange Sign (2149)** | **$O(N)$ Single Pass ⚡**| $O(N)$ Result Array | Dual pointer `posIdx` & `negIdx` |

---

## 10. Edge Cases & Boundary Handling
* **No Mountain Exists**: Arrays without peak `arr[i-1] < arr[i] > arr[i+1]` return `0` cleanly.
* **Dominoes With No Forces (`"......."`)**: Remained unchanged as `"......."`.

---

## 11. Common Mistakes & Anti-Patterns
* **Not Skipping Descending Slope in Longest Mountain ($O(N^2)$ Degraded Time)**:
  - If `i` is incremented by 1 (`i++`) after processing a peak, elements on the descending slope are re-inspected multiple times.
  - **Execute `i = right` to skip the descending slope instantaneously**.
* **Modifying Input Array In-Place in LeetCode 2149**: Overwriting elements in-place corrupts unread values. Use a separate `result` array.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Longest Mountain (LeetCode 845) Runs in $O(N)$ Linear Time:
> Even though inner `while` loops expand `left` and `right` outward, setting **`i = right`** after processing a mountain ensures that each array index is visited at most **2 times** across the entire algorithm!

> **Memory Trick:** **"Set i = right after mountain expansion to guarantee linear O(N) time!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Mountain Expansion | DP Prefix/Suffix Array Approach |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Prefix/Suffix Arrays |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(N)$ 3 Passes |
| **Code Footprint** | 15 Lines | 25 Lines |

---

## 14. How to Recognize This in Questions
* **"Find longest mountain subarray that strictly increases then decreases"** $\rightarrow$ LeetCode 845 (Peak check + `i = right`).
* **"Simulate falling dominoes with left and right forces"** $\rightarrow$ LeetCode 838 (Padded string boundary pointers).
* **"Rearrange elements by alternating positive and negative signs"** $\rightarrow$ LeetCode 2149 (`posIdx += 2`, `negIdx += 2`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why are imaginary boundaries `"L"` and `"R"` padded onto the string in Push Dominoes?**  
  *A:* Padding `"L"` at index 0 and `"R"` at index $N+1$ guarantees that the first and last unprocessed domino segments have valid non-null boundary pointers, eliminating special head/tail edge case logic.
* **Q: Can Rearrange Array by Sign (LeetCode 2149) be solved in $O(1)$ space while preserving order?**  
  *A:* No! Preserving original relative order while modifying signs in-place without extra space requires $O(N^2)$ block rotation (similar to insertion sort). The $O(N)$ time solution requires an $O(N)$ output array.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED TWO POINTER APPLICATIONS                     |
+-----------------------------------------------------------------------+
| • Push Dominoes (838): Pad "L" + S + "R"; fill between left & right   |
| • Mountain Array (845): Check peak arr[i-1] < arr[i] > arr[i+1]       |
| • Mountain Skip Rule: Set i = right to skip descending slope in O(N)! |
| • Sign Rearrange (2149): posIdx = 0, negIdx = 1; increment by +2      |
| • Space Complexity: O(1) Space for 845; O(N) Output for 838 & 2149    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can solve Push Dominoes (LeetCode 838) using 2-pointer boundaries.
- [ ] I can write Longest Mountain in Array (LeetCode 845) in $O(N)$ time & $O(1)$ space.
- [ ] I know why `i = right` guarantees linear execution time in LeetCode 845.
- [ ] I can solve Rearrange Array Elements by Sign (LeetCode 2149).
- [ ] I know why padding `"L"` and `"R"` simplifies Push Dominoes.
