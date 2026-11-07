# 02. Opposite Direction Pointers, Converging Search & Water Container Trapping

## 1. Introduction
The **Opposite Direction Two Pointers Pattern** (also called **Converging Pointers**) places one pointer at the start (`left = 0`) and one pointer at the end (`right = N - 1`) of a sequence. The pointers move towards each other (`left++` or `right--`) until they meet. This technique powers **Two Sum II (LeetCode 167)**, **Container With Most Water (LeetCode 11)**, **Trapping Rain Water (LeetCode 42)**, and **Valid Palindrome (LeetCode 125)**, solving complex geometric and search problems in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** In Container With Most Water (LeetCode 11), why is moving the pointer pointing to the **SHORTER height** mathematically optimal?
> The container area is bounded by `width * min(height[left], height[right])`.
> Decreasing width by moving the taller line can NEVER increase area because area remains bottlenecked by the shorter line!
> Thus, the ONLY chance to find a larger area is moving the pointer at the **Shorter Line**!

```
Converging Pointers Topology:
+-----------------------------------------------------------------------------------+
| Pointer Left  : Starts at Index 0      -> Moves Right (left++)                    |
| Pointer Right : Starts at Index N - 1  -> Moves Left (right--)                    |
| Termination   : Loop ends when left >= right                                      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Algorithmic Mechanics

### 2.1 Container With Most Water (LeetCode 11)
Given an array `height` representing vertical lines at index $i$:
1. Initialize `left = 0`, `right = N - 1`, `maxArea = 0`.
2. While `left < right`:
   - `width = right - left`
   - `currentArea = width * Math.min(height[left], height[right])`
   - `maxArea = Math.max(maxArea, currentArea)`
   - **Greedy Move Rule**:
     - `if (height[left] < height[right]) left++;`
     - `else right--;`
3. Return `maxArea`.

```
Container With Most Water Greedy Proof:
Area = (right - left) * min(h[left], h[right])
If h[left] < h[right]:
   Holding 'left' and decrementing 'right' reduces width to (right-1-left).
   The new min height is <= h[left].
   New Area <= (width - 1) * h[left] < Current Area!
Therefore, all pairs (left, right-1), (left, right-2)... are strictly SMALLER!
We safely eliminate 'left' in O(1) time! ⚡
```

### 2.2 Trapping Rain Water (LeetCode 42 - 2-Pointer $O(1)$ Space Strategy)
Given an array `height` representing elevation map:
* Water trapped at index $i$ is bounded by:

$$\text{Water}[i] = \max(0, \min(\text{maxLeft}, \text{maxRight}) - \text{height}[i])$$

* **2-Pointer Algorithm**:
  1. `left = 0`, `right = N - 1`, `leftMax = 0`, `rightMax = 0`, `totalWater = 0`.
  2. While `left < right`:
     - If `height[left] < height[right]`:
       - If `height[left] >= leftMax`: `leftMax = height[left]`.
       - Else: `totalWater += leftMax - height[left]`.
       - `left++`.
     - Else:
       - If `height[right] >= rightMax`: `rightMax = height[right]`.
       - Else: `totalWater += rightMax - height[right]`.
       - `right--`.

```
Trapping Rain Water 2-Pointer Optimization:
Because height[left] < height[right], we KNOW that leftMax < rightMax!
Therefore, water at 'left' is strictly bottlenecked by leftMax!
We don't need to know the exact rightMax value! ⚡ (O(N) Time, O(1) Space!)
```

> **Memory Trick:** **"Container Water: Move shorter line pointer! Trapping Rain Water: Move pointer with smaller height, trap (leftMax - h[left])!"**

---

## 3. Characteristics & Valid Palindrome Mechanics (LeetCode 125)

### 3.1 Valid Palindrome (LeetCode 125)
Given a string `s`, check if it is a palindrome considering only alphanumeric characters and ignoring cases:
1. `left = 0`, `right = s.length() - 1`.
2. While `left < right`:
   - Advance `left++` while `left < right` and `!Character.isLetterOrDigit(s.charAt(left))`.
   - Decrement `right--` while `left < right` and `!Character.isLetterOrDigit(s.charAt(right))`.
   - Compare `Character.toLowerCase(s.charAt(left))` vs `Character.toLowerCase(s.charAt(right))`.
   - If mismatch, return `false`.
   - `left++`, `right--`.
3. Return `true`.

---

## 4. Internal Working Mechanics
Tracing Container With Most Water (LeetCode 11) on `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`:

```
Init: left = 0 (h=1), right = 8 (h=7), maxArea = 0

Step 1: width = 8, h = min(1, 7) = 1 -> area = 8. maxArea = 8.
        h[left] (1) < h[right] (7) -> left++ (left = 1, h=8).

Step 2: width = 7, h = min(8, 7) = 7 -> area = 49. maxArea = 49.
        h[right] (7) < h[left] (8) -> right-- (right = 7, h=3).

Step 3: width = 6, h = min(8, 3) = 3 -> area = 18. maxArea = 49.
        h[right] (3) < h[left] (8) -> right-- (right = 6, h=8).

Step 4: width = 5, h = min(8, 8) = 8 -> area = 40. maxArea = 49.
        h[left] == h[right] -> right-- (right = 5, h=4).

Max Area Found: 49 ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Trapping Rain Water 2-Pointer Elevation Boundary Topography:

```
        leftMax                                      rightMax
          ||                                            ||
          ||                   (Water)                  ||
     +----+----+             +~~~~~~~~~+             +----+----+
     | H: 3    |             | H: 1    |             | H: 4    |
     +----+----+             +----+----+             +----+----+
        left                                            right
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Container With Most Water (LeetCode 11), Trapping Rain Water (LeetCode 42), Valid Palindrome (LeetCode 125), and Reverse String (LeetCode 344):

```java
import java.util.*;

public class OppositeDirectionMaster {

    // 1. Container With Most Water (LeetCode 11) O(N) Time, O(1) Space
    public static int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int maxWater = 0;

        while (left < right) {
            int width = right - left;
            int currentWater = width * Math.min(height[left], height[right]);
            maxWater = Math.max(maxWater, currentWater);

            // Move the pointer at the shorter vertical line
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }

        return maxWater;
    }

    // 2. Trapping Rain Water 2-Pointer (LeetCode 42) O(N) Time, O(1) Auxiliary Space
    public static int trap(int[] height) {
        if (height == null || height.length == 0) return 0;

        int left = 0;
        int right = height.length - 1;
        int leftMax = 0;
        int rightMax = 0;
        int totalWater = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    totalWater += leftMax - height[left];
                }
                left++;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    totalWater += rightMax - height[right];
                }
                right--;
            }
        }

        return totalWater;
    }

    // 3. Valid Palindrome (LeetCode 125) O(N) Time, O(1) Auxiliary Space
    public static boolean isPalindrome(String s) {
        if (s == null || s.length() == 0) return true;

        int left = 0;
        int right = s.length() - 1;

        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }

            char c1 = Character.toLowerCase(s.charAt(left));
            char c2 = Character.toLowerCase(s.charAt(right));

            if (c1 != c2) return false;

            left++;
            right--;
        }

        return true;
    }

    // 4. Reverse String (LeetCode 344) O(N) Time, O(1) Space
    public static void reverseString(char[] s) {
        int left = 0;
        int right = s.length - 1;

        while (left < right) {
            char temp = s[left];
            s[left] = s[right];
            s[right] = temp;
            left++;
            right--;
        }
    }
}
```

> **Quick Syntax:**
```java
// Container With Most Water Greedy Pointer Syntax
int width = right - left;
maxWater = Math.max(maxWater, width * Math.min(height[left], height[right]));
if (height[left] < height[right]) left++;
else right--;
```

---

## 7. Concrete Problem Examples
* **LeetCode 11 - Container With Most Water**: Greedy shorter-line pointer movement.
* **LeetCode 42 - Trapping Rain Water**: 2-pointer height boundary trap.
* **LeetCode 125 - Valid Palindrome**: Converging alphanumeric character matching.
* **LeetCode 344 - Reverse String**: In-place character swap.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Container With Most Water, Trapping Rain Water, and Valid Palindrome:

```java
public class OppositeDirectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Container With Most Water (LeetCode 11) ===");
        int[] heights = {1, 8, 6, 2, 5, 4, 8, 3, 7};
        int waterArea = OppositeDirectionMaster.maxArea(heights);
        System.out.println("Max Water Area: " + waterArea); // Output: 49

        System.out.println("\n=== 2. Trapping Rain Water (LeetCode 42) ===");
        int[] elevation = {0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
        int trappedWater = OppositeDirectionMaster.trap(elevation);
        System.out.println("Total Trapped Water: " + trappedWater); // Output: 6

        System.out.println("\n=== 3. Valid Palindrome (LeetCode 125) ===");
        String s = "A man, a plan, a canal: Panama";
        System.out.println("Is Palindrome? " + OppositeDirectionMaster.isPalindrome(s)); // Output: true
    }
}
```

---

## 9. Complexity Analysis

| Operation / Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Container Water (11)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Move pointer at shorter height |
| **Trapping Water (42)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| 2-Pointer max boundary tracking |
| **Valid Palindrome (125)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Alphanumeric filter + case fold |

---

## 10. Edge Cases & Boundary Handling
* **All Zero Height Array**: Returns `0` water area cleanly.
* **String With No Alphanumeric Characters**: `left < right` loop terminates cleanly, returns `true`.

---

## 11. Common Mistakes & Anti-Patterns
* **Moving the Taller Pointer in Container With Most Water**:
  - Moving the pointer at the taller line can NEVER increase area (since area is bottlenecked by shorter height).
  - **Always move the pointer pointing to the SHORTER line**.
* **Allocating Dynamic Arrays in Trapping Rain Water ($O(N)$ Space)**:
  - Using `leftMax[]` and `rightMax[]` arrays takes $O(N)$ auxiliary memory.
  - **Use 2-pointer `left` and `right` with `leftMax` and `rightMax` variables for $O(1)$ space**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why 2-Pointer Trapping Rain Water Works in $O(1)$ Space:
> When `height[left] < height[right]`, we know `leftMax < rightMax` (or at least `rightMax >= height[right] > height[left]`).
> Therefore, water trapped at `left` depends ONLY on `leftMax - height[left]`. We don't need to compute the full `rightMax` array!

> **Memory Trick:** **"If h[left] < h[right], water at left is bottlenecked ONLY by leftMax!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Pointer Trapping Water | Dynamic Programming Arrays |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Auxiliary Arrays |
| **Time Complexity** | **$O(N)$ Single Pass ⚡** | $O(N)$ 3 Passes |
| **Code Footprint** | 20 Lines | 25 Lines |

---

## 14. How to Recognize This in Questions
* **"Find two lines that together with x-axis form container with max water"** $\rightarrow$ LeetCode 11 (Converging shorter line pointer).
* **"Compute how much water terrain can trap after raining in O(1) space"** $\rightarrow$ LeetCode 42 (2-pointer elevation boundaries).
* **"Check if string is palindrome ignoring non-alphanumeric characters"** $\rightarrow$ LeetCode 125 (Converging character matching).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does moving the shorter pointer in LeetCode 11 guarantee we don't miss the optimal container area?**  
  *A:* Because holding the shorter line while moving the taller line reduces width without increasing height, producing strictly smaller areas for all eliminated pairs.
* **Q: How does Trapping Rain Water eliminate the need for `rightMax[]` array?**  
  *A:* By maintaining `left` and `right` pointers, whenever `height[left] < height[right]`, `height[right]` acts as a guaranteed right boundary wall higher than `leftMax`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: OPPOSITE DIRECTION POINTERS & WATER TRAPPING          |
+-----------------------------------------------------------------------+
| • Opposite Pointers: left=0, right=N-1; while (left < right)          |
| • Container Water (11): maxWater = max(maxWater, (right-left) * min(h[l], h[r]))|
| • Greedy Rule (11): if (h[l] < h[r]) left++ else right--              |
| • Trapping Water (42): if (h[l] < h[r]) process left; else process right|
| • Water Formula: totalWater += leftMax - height[left]                 |
| • Valid Palindrome (125): Skip non-alphanumeric; compare toLowerCase   |
| • Space Invariant: All converging pointer algorithms run in O(1) Space ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Container With Most Water (LeetCode 11) in under 3 minutes.
- [ ] I can prove why moving the shorter line pointer in LeetCode 11 is optimal.
- [ ] I can write Trapping Rain Water (LeetCode 42) in $O(1)$ space using 2 pointers.
- [ ] I can write Valid Palindrome (LeetCode 125) skipping non-alphanumeric chars.
- [ ] I know how 2 pointers eliminate the $O(N)$ space array requirement in LeetCode 42.
