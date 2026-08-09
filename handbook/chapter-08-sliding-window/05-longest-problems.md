# 05. Longest Window Problems, Distinct Character Constraints & Subarray Expansion

## 1. Introduction
The **Longest Window Sub-category** of Sliding Window algorithms focuses on expanding a window as far as possible while maintaining structural validity constraints. Problems like **Longest Substring with At Most K Distinct Characters (LeetCode 340)**, **Longest Substring with At Most Two Distinct Characters (LeetCode 159)**, and **Fruit Into Baskets (LeetCode 904)** require maximizing the window size $(right - left + 1)$ in **$O(N)$ linear time and $O(1)$ constant space**.

> **Important:** In Longest Window problems, the answer is recorded **AFTER the shrink loop finishes** (when the window state becomes valid again). The window expands aggressively via `right++`, and whenever the constraint is violated (e.g. `distinctCount > K`), `left` is advanced until the window is valid once more!

```
Longest Window Expansion-Shrink Protocol:
+-----------------------------------------------------------------------------------+
| 1. Expand Window : Advance right, update character frequency map / state          |
| 2. Shrink Window : While distinctCount > K -> decrement map[s[left]], left++     |
| 3. Record Answer : maxLen = max(maxLen, right - left + 1) (Valid Window State) ⚡ |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & At Most $K$ Distinct Characters Mechanics

### 2.1 Longest Substring with At Most $K$ Distinct Characters (LeetCode 340)
Given a string `s` and integer $K$, find the length of the longest substring that contains at most $K$ distinct characters:

1. If $K == 0$ or `s` is empty, return `0`.
2. Maintain frequency map `int[] count = new int[128]` and a `distinctCount` counter.
3. `left = 0`, `maxLen = 0`.
4. For `right = 0` to $N - 1$:
   - `inChar = s.charAt(right)`.
   - If `count[inChar] == 0`, `distinctCount++` (New unique character entered window!).
   - `count[inChar]++`.
   - **Shrink Window While Invalid (`distinctCount > K`)**:
     - `outChar = s.charAt(left)`.
     - `count[outChar]--`.
     - If `count[outChar] == 0`, `distinctCount--` (Character completely removed from window!).
     - `left++`.
   - **Record Answer**: `maxLen = Math.max(maxLen, right - left + 1)`.
5. Return `maxLen`.

```
Distinct Character Counting Rule:
- When adding char: if (count[char] == 0) distinctCount++; count[char]++;
- When removing char: count[char]--; if (count[char] == 0) distinctCount--;
This maintains distinctCount in O(1) time without iterating the map! ⚡
```

### 2.2 Fruit Into Baskets (LeetCode 904 - Isomorphic to At Most 2 Distinct Characters)
Given an array `fruits` where `fruits[i]` represents the type of fruit on tree $i$:
* You have 2 baskets, and each basket can hold only ONE single type of fruit.
* Find the maximum number of fruits you can collect in a continuous sequence.
* **Isomorphic Equivalence**: This problem is EXACTLY identical to **Longest Subarray with At Most 2 Distinct Elements (LeetCode 159)**!

> **Memory Trick:** **"Fruit Into Baskets IS LeetCode 159 (At Most 2 Distinct Characters)! Record maxLen AFTER the shrink loop!"**

---

## 3. Characteristics & Non-Decreasing Window Optimization ($O(N)$ Space-Optimal)

### 3.1 Non-Decreasing Window Trick ($O(N)$ Single-Pass Optimization)
Instead of shrinking the window back down when invalid using a `while` loop, we can prevent the window size from ever shrinking!
* If a window of length `L` was previously valid, we NEVER need to test windows of length $< L$.
* Change `while (distinctCount > K)` to a single `if (distinctCount > K)`:
  - If invalid, simply shift the entire window right by 1 step (`left++`).
  - At the end of the loop, the final window size `right - left` is GUARANTEED to be the maximum valid length!

```java
// Non-Decreasing Window Optimization (No Math.max needed at the end!)
for (int right = 0; right < s.length(); right++) {
    if (count[s.charAt(right)]++ == 0) distinctCount++;
    if (distinctCount > k) {
        if (--count[s.charAt(left++)] == 0) distinctCount--;
    }
}
return s.length() - left; // Maximum valid window size!
```

---

## 4. Internal Working Mechanics
Tracing Longest Substring with At Most $K = 2$ Distinct Characters (LeetCode 159) on `s = "eceba"`:

```
Init: left = 0, distinctCount = 0, maxLen = 0, count[128] = 0

right = 0 ('e'): count['e']=1, distinctCount=1 <= 2. maxLen = 1 ("e").
right = 1 ('c'): count['c']=1, distinctCount=2 <= 2. maxLen = 2 ("ec").
right = 2 ('e'): count['e']=2, distinctCount=2 <= 2. maxLen = 3 ("ece").
right = 3 ('b'): count['b']=1, distinctCount=3 > 2 -> INVALID!
  - Shrink loop: outChar = 'e' (left=0). count['e']=1. left=1.
  - distinctCount still 3 ('c', 'e', 'b').
  - Next shrink: outChar = 'c' (left=1). count['c']=0. distinctCount=2 ('e', 'b'). left=2.
  - Window valid ("eb", len 2). maxLen remains 3.

right = 4 ('a'): count['a']=1, distinctCount=3 > 2 -> INVALID!
  - Shrink loop: outChar = 'e' (left=2). count['e']=0. distinctCount=2 ('b', 'a'). left=3.
  - Window valid ("ba", len 2). maxLen remains 3.

Result: 3 ("ece") ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Longest Substring At Most 2 Distinct Characters Window Traversal Topography:

```
s = " e  c  e  b  a "
    [=======]             right = 2: Window "ece" (2 distinct: 'e', 'c', Len 3) -> maxLen = 3 ✅
       [=======]          right = 3: Window "ceb" (3 distinct) -> Shrinks to "eb" (Len 2)
          [=======]       right = 4: Window "eba" (3 distinct) -> Shrinks to "ba" (Len 2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Longest Substring with At Most K Distinct Characters (LeetCode 340), Fruit Into Baskets (LeetCode 904), and Non-Decreasing Window Optimization:

```java
import java.util.*;

public class LongestProblemsMaster {

    // 1. Longest Substring with At Most K Distinct Characters (LeetCode 340) O(N) Time, O(1) Space
    public static int lengthOfLongestSubstringKDistinct(String s, int k) {
        if (s == null || s.length() == 0 || k <= 0) return 0;

        int[] count = new int[128];
        int left = 0;
        int distinctCount = 0;
        int maxLen = 0;

        for (int right = 0; right < s.length(); right++) {
            char inChar = s.charAt(right);
            if (count[inChar] == 0) {
                distinctCount++;
            }
            count[inChar]++;

            // Shrink window while distinctCount > k
            while (distinctCount > k) {
                char outChar = s.charAt(left);
                count[outChar]--;
                if (count[outChar] == 0) {
                    distinctCount--;
                }
                left++;
            }

            // Record max length for valid window
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }

    // 2. Fruit Into Baskets (LeetCode 904 / LeetCode 159) O(N) Time, O(1) Auxiliary Space
    public static int totalFruit(int[] fruits) {
        if (fruits == null || fruits.length == 0) return 0;

        Map<Integer, Integer> basket = new HashMap<>();
        int left = 0;
        int maxFruits = 0;

        for (int right = 0; right < fruits.length; right++) {
            int fruitType = fruits[right];
            basket.put(fruitType, basket.getOrDefault(fruitType, 0) + 1);

            // Shrink window while basket has more than 2 fruit types
            while (basket.size() > 2) {
                int outFruit = fruits[left];
                basket.put(outFruit, basket.get(outFruit) - 1);
                if (basket.get(outFruit) == 0) {
                    basket.remove(outFruit);
                }
                left++;
            }

            maxFruits = Math.max(maxFruits, right - left + 1);
        }

        return maxFruits;
    }

    // 3. Non-Decreasing Window Optimization (LeetCode 340) O(N) Single-Pass
    public static int lengthOfLongestSubstringKDistinctNonDecreasing(String s, int k) {
        if (s == null || s.length() == 0 || k <= 0) return 0;

        int[] count = new int[128];
        int left = 0;
        int distinctCount = 0;

        for (int right = 0; right < s.length(); right++) {
            if (count[s.charAt(right)]++ == 0) {
                distinctCount++;
            }

            // If invalid, shift window right without shrinking size!
            if (distinctCount > k) {
                if (--count[s.charAt(left++)] == 0) {
                    distinctCount--;
                }
            }
        }

        return s.length() - left; // Final maximum window size
    }
}
```

> **Quick Syntax:**
```java
// Distinct Count Update Pattern
if (count[inChar] == 0) distinctCount++;
count[inChar]++;
```

---

## 7. Concrete Problem Examples
* **LeetCode 340 - Longest Substring with At Most K Distinct Characters**: Generic $K$ distinct window.
* **LeetCode 159 - Longest Substring with At Most Two Distinct Characters**: $K = 2$ special case.
* **LeetCode 904 - Fruit Into Baskets**: Isomorphic 2-basket fruit collection.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing K-Distinct Substring, Fruit Into Baskets, and Non-Decreasing Window Optimization:

```java
public class LongestProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Longest Substring At Most K Distinct (LeetCode 340, K=2) ===");
        String s = "eceba";
        int len1 = LongestProblemsMaster.lengthOfLongestSubstringKDistinct(s, 2);
        System.out.println("Max Substring Length (K=2): " + len1); // Output: 3 ("ece")

        System.out.println("\n=== 2. Fruit Into Baskets (LeetCode 904) ===");
        int[] fruits = {1, 2, 3, 2, 2};
        int maxFruit = LongestProblemsMaster.totalFruit(fruits);
        System.out.println("Max Fruits Collected: " + maxFruit); // Output: 4 ([2, 3, 2, 2])

        System.out.println("\n=== 3. Non-Decreasing Window (LeetCode 340) ===");
        int lenOpt = LongestProblemsMaster.lengthOfLongestSubstringKDistinctNonDecreasing("aa", 1);
        System.out.println("Non-Decreasing Result: " + lenOpt); // Output: 2 ("aa")
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **K-Distinct Substring (340)**| **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `distinctCount` variable tracking |
| **Fruit Into Baskets (904)** | **$O(N)$ Linear ⚡** | **$O(1)$ Map (Size $\le 3$) ⚡**| Basket size $\le 2$ invariant |
| **Non-Decreasing Window** | **$O(N)$ Single Pass ⚡**| **$O(1)$ Aux Array ⚡**| `if` instead of `while` shrink loop |

---

## 10. Edge Cases & Boundary Handling
* **$K = 0$ Input**: Returns `0` immediately.
* **String With Fewer Unique Characters Than $K$**: `distinctCount > K` is never triggered; returns `s.length()`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `count[outChar] == 0` Check when Decrementing**:
  - Decrementing `count[outChar]--` without checking if it hit 0 fails to decrement `distinctCount`.
  - **Execute `distinctCount--` ONLY when `count[outChar] == 0`**.
* **Recording Answer Inside Shrink Loop for Longest Window Problems**:
  - Recording `maxLen` inside the `while (distinctCount > K)` loop records invalid intermediate windows.
  - **Record `maxLen` AFTER the shrink loop when window is valid**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Fruit Into Baskets (904) is Isomorphic to LeetCode 159:
> Fruit types are integers representing array values, and 2 baskets represent $K = 2$ distinct allowed values.
> Therefore, LeetCode 904 is EXACTLY the "Longest Subarray with At Most 2 Distinct Elements"!

> **Memory Trick:** **"Fruit Into Baskets = Longest Subarray with At Most 2 Unique Numbers!"**

---

## 13. System & Implementation Comparisons

| Feature | `while` Shrink Loop Strategy | Non-Decreasing `if` Shift Strategy |
| :--- | :--- | :--- |
| **Window Motion** | Expands & Shrinks | Expands & Shifts Right |
| **Answer Calculation**| `Math.max(maxLen, r - l + 1)` | `s.length() - left` |
| **Code Length** | Standard (Easier to read) | Ultra-compact |

---

## 14. How to Recognize This in Questions
* **"Find longest substring containing at most K distinct characters"** $\rightarrow$ LeetCode 340.
* **"Collect maximum fruits in 2 baskets"** $\rightarrow$ LeetCode 904 ($K = 2$ distinct numbers).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `distinctCount` track unique characters in $O(1)$ time?**  
  *A:* Increment `distinctCount` only when a character's frequency increases from 0 to 1 (`count[c] == 0`). Decrement `distinctCount` only when a character's frequency decreases from 1 to 0 (`count[c] == 0`).
* **Q: Why does the Non-Decreasing Window optimization work for finding the maximum window size?**  
  *A:* When the window becomes invalid, replacing `while` with `if` shifts both `left` and `right` by 1 step. This freezes the window size at its historical maximum until a larger valid window is found.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LONGEST SLIDING WINDOW PROBLEMS                       |
+-----------------------------------------------------------------------+
| • K-Distinct Rule (340): if (count[c]++ == 0) distinctCount++         |
| • Shrink Condition: while (distinctCount > k) if (--count[l] == 0) distinct--|
| • Longest Record Rule: maxLen = max(maxLen, right - left + 1) AFTER shrink|
| • Fruit Into Baskets (904): Identical to At Most 2 Distinct Numbers!  |
| • Non-Decreasing Optimization: Use if (distinctCount > k) and return N-left|
| • Time Complexity: O(N) Linear Time | O(1) Auxiliary Space ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Longest Substring with At Most K Distinct Characters (LeetCode 340).
- [ ] I know why `distinctCount` updates only when count crosses 0.
- [ ] I can solve Fruit Into Baskets (LeetCode 904).
- [ ] I know where to record the answer for longest window search.
- [ ] I can explain the Non-Decreasing Window optimization.
