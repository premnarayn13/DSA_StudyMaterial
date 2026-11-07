# 01. Sliding Window Foundations, Window Taxonomy & State Loop Invariants

## 1. Introduction
The **Sliding Window Pattern** is an essential algorithmic paradigm designed to optimize subarray or substring computations over linear sequences. By maintaining a dynamic sub-segment defined by two boundary pointers—a **Right Expanding Pointer (`right`)** and a **Left Shrinking Pointer (`left`)**—the Sliding Window pattern reuses overlapping calculations, reducing brute-force $O(N \cdot K)$ or $O(N^2)$ nested loop operations down to **$O(N)$ linear time and $O(1)$ constant auxiliary space**.

> **Important:** The core advantage of Sliding Window is **Incremental State Maintenance**. Instead of re-evaluating an entire sub-segment of size $K$ from scratch on every step ($K$ additions), sliding the window removes the outgoing element (`arr[left]`) and adds the incoming element (`arr[right]`) in **$O(1)$ constant time**!

```
Brute-Force vs Sliding Window Compute Spectrum:
+-----------------------------------------------------------------------------------+
| Brute-Force Re-computation: Recalculates sum of K elements at each index -> O(N * K)|
| Sliding Window Maintenance: sum = sum - arr[left] + arr[right]           -> O(N) ⚡ |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Window Taxonomy

### 2.1 The 3 Primary Sliding Window Categories
1. **Fixed-Size Window ($K$ is Fixed)**:
   - The window length is constrained to an exact constant size $K$.
   - The window slides right by incrementing both `left` and `right` in tandem (`right++`, `left++`).
   - Ideal for **Maximum Sum Subarray of Size K**, **Find All Anagrams in a String (LeetCode 438)**, and **Permutation in String (LeetCode 567)**.
2. **Variable-Size Shrinkable Window (Find Longest / Shortest)**:
   - The window expands dynamically by advancing `right` to include elements.
   - When a validity constraint is violated (or met), the window shrinks by advancing `left`.
   - Ideal for **Longest Substring Without Repeating Characters (LeetCode 3)** and **Minimum Size Subarray Sum (LeetCode 209)**.
3. **Monotonic Deque Window (Sliding Window Maximum)**:
   - Uses a `Deque` to maintain monotonic ordering of elements within a sliding window of size $K$.
   - Ideal for **Sliding Window Maximum (LeetCode 239)** ($O(N)$ time).

```
Sliding Window Classification Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Window Family         | Window Size       | Pointer Movement  | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| Fixed-Size Window     | Fixed Constant $K$| Both move together| Exact Size K Sum  |
| Variable-Size Window  | Dynamic Shrinkable| `right++`, `left++`| Longest/Shortest  |
| Monotonic Deque Window| Fixed Constant $K$| Monotonic Queue   | Sliding Max/Min   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fixed Window: Both pointers move together! Variable Window: Expand right, shrink left while condition invalid!"**

---

## 3. Characteristics & The Variable Window Expansion-Shrink Loop

### 3.1 The Canonical Variable Window Template
The universal 2-pointer loop structure for variable-size sliding window problems:

```java
int left = 0;
for (int right = 0; right < n; right++) {
    // 1. Expand Window: Add arr[right] to window state
    updateState(arr[right]);

    // 2. Shrink Window: While window condition is invalid (or met)
    while (isInvalidState()) {
        removeState(arr[left]);
        left++; // Shrink left boundary
    }

    // 3. Update Answer: Record best window size (right - left + 1)
    maxLen = Math.max(maxLen, right - left + 1);
}
```

* **Window Length Invariant**: At any moment during iteration, the current window length is:

$$\text{Window Size} = \text{right} - \text{left} + 1$$

---

## 4. Internal Working Mechanics
Tracing Fixed Window of size $K = 3$ on `[2, 1, 5, 1, 3, 2]`:

```
Init: k = 3. Compute initial sum for first 3 elements [2, 1, 5] -> currentSum = 8. maxSum = 8.

Step 1 (right = 3, val 1, left = 0, val 2):
  - Slide window: currentSum = currentSum - arr[0] + arr[3] = 8 - 2 + 1 = 7.
  - maxSum = max(8, 7) = 8.

Step 2 (right = 4, val 3, left = 1, val 1):
  - Slide window: currentSum = currentSum - arr[1] + arr[4] = 7 - 1 + 3 = 9.
  - maxSum = max(8, 9) = 9.

Step 3 (right = 5, val 2, left = 2, val 5):
  - Slide window: currentSum = currentSum - arr[2] + arr[5] = 9 - 5 + 2 = 6.
  - maxSum = max(9, 6) = 9.

Final Maximum Subarray Sum = 9 ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Sliding Window Expansion & Sliding Motion Topography:

```
Initial Window (K=3):   [ 2,   1,   5 ]  1,   3,   2   (Sum = 8)
                          ^         ^
                        left      right

Slid Window (K=3):        2, [ 1,   5,   1 ]  3,   2   (Sum = 8 - 2 + 1 = 7)
                               ^         ^
                             left      right
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Fixed Window Maximum Sum (Size $K$) and Variable Window Longest Substring Without Repeating Characters (LeetCode 3):

```java
import java.util.*;

public class SlidingWindowFoundationsMaster {

    // 1. Fixed-Size Window: Max Sum Subarray of Size K O(N) Time, O(1) Space
    public static int maxSubarraySumFixed(int[] arr, int k) {
        if (arr == null || arr.length < k || k <= 0) return 0;

        int currentSum = 0;
        // Compute sum of first window of size K
        for (int i = 0; i < k; i++) {
            currentSum += arr[i];
        }

        int maxSum = currentSum;

        // Slide window across remaining array
        for (int right = k; right < arr.length; right++) {
            currentSum += arr[right] - arr[right - k]; // Add incoming, remove outgoing
            maxSum = Math.max(maxSum, currentSum);
        }

        return maxSum;
    }

    // 2. Variable-Size Window: Longest Substring Without Repeating Characters (LeetCode 3) O(N) Time, O(1) Space
    public static int lengthOfLongestSubstring(String s) {
        if (s == null || s.length() == 0) return 0;

        int[] charMap = new int[128]; // Frequency map for ASCII characters
        Arrays.fill(charMap, -1);     // Store last seen index of each character

        int left = 0;
        int maxLen = 0;

        for (int right = 0; right < s.length(); right++) {
            char currChar = s.charAt(right);

            // If character was seen inside current window, jump left pointer
            if (charMap[currChar] >= left) {
                left = charMap[currChar] + 1;
            }

            charMap[currChar] = right; // Update last seen index
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}
```

> **Quick Syntax:**
```java
// Fixed Window Sliding Formula
currentSum += arr[right] - arr[right - k];
```

---

## 7. Concrete Problem Examples
* **Maximum Sum Subarray of Size K**: Fixed-size window sliding sum.
* **LeetCode 3 - Longest Substring Without Repeating Characters**: Variable-size shrinkable window.
* **LeetCode 209 - Minimum Size Subarray Sum**: Variable window minimum length search.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Fixed Window Max Sum and Longest Substring Without Repeats:

```java
public class SlidingWindowFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Max Sum Subarray of Size K (K = 3) ===");
        int[] arr = {2, 1, 5, 1, 3, 2};
        int maxSum = SlidingWindowFoundationsMaster.maxSubarraySumFixed(arr, 3);
        System.out.println("Max Subarray Sum (K=3): " + maxSum); // Output: 9 ([5, 1, 3])

        System.out.println("\n=== 2. Longest Substring Without Repeats (LeetCode 3) ===");
        String s = "abcabcbb";
        int longest = SlidingWindowFoundationsMaster.lengthOfLongestSubstring(s);
        System.out.println("Longest Substring Length: " + longest); // Output: 3 ("abc")
    }
}
```

---

## 9. Complexity Analysis

| Window Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Fixed Window ($K$)** | **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| `sum += arr[right] - arr[right-k]` |
| **Variable Window (3)** | **$O(N)$ Linear ⚡** | **$O(1)$ Aux Array ⚡**| `left` jumps to `charMap[c] + 1` |

---

## 10. Edge Cases & Boundary Handling
* **$K > N$ (Window Size Larger Than Array)**: Handled cleanly; returns `0`.
* **Empty String Input (`s == ""`)**: Returns `0` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Re-Summing Window Elements from Scratch ($O(N \cdot K)$ Penalty)**:
  - Writing an inner loop `for (int i = left; i <= right; i++) sum += arr[i]` at every step degrades performance to $O(N \cdot K)$!
  - **Use `currentSum += incoming - outgoing` for $O(1)$ state updates**.
* **Forgetting `right - left + 1` Formula**: Writing `right - left` off-by-one undercounts window length by 1.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Variable Window Runs in $O(N)$ Linear Time:
> Even though there is a `while` loop inside the `for` loop, both `right` and `left` pointers move strictly LEFT-TO-RIGHT.
> The `right` pointer increments $N$ times, and the `left` pointer increments at most $N$ times $\implies$ Total operations $\le 2N = \mathbf{O(N)\text{ Linear Time}}$!

> **Memory Trick:** **"Both left and right pointers only move FORWARD! Total work <= 2N steps = O(N) Time!"**

---

## 13. System & Implementation Comparisons

| Feature | Sliding Window Technique | Brute-Force Re-computation |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \cdot K)$ or $O(N^2)$ |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(1)$ |
| **State Reusability**| 100% Incremental | 0% (Recomputed) |

---

## 14. How to Recognize This in Questions
* **"Find max/min sum of contiguous subarray of fixed size K"** $\rightarrow$ Fixed-Size Window.
* **"Find longest/shortest contiguous subarray/substring satisfying condition"** $\rightarrow$ Variable-Size Window.

---

## 15. Frequently Asked Interview Questions
* **Q: How does Sliding Window guarantee $O(1)$ update time for fixed window sum?**  
  *A:* By subtracting the element leaving the window at index `right - K` and adding the element entering the window at index `right`.
* **Q: Why does character last-seen index mapping allow $O(N)$ single-pass execution in LeetCode 3?**  
  *A:* Storing `charMap[c] = index` enables the `left` pointer to jump directly past the previous occurrence of a repeating character in $O(1)$ time, skipping individual step-by-step increments.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SLIDING WINDOW FOUNDATIONS & TAXONOMY                 |
+-----------------------------------------------------------------------+
| • Fixed Window Formula: sum = sum - arr[right - k] + arr[right]       |
| • Variable Window Template: Expand right, shrink left while invalid   |
| • Window Length Formula: len = right - left + 1                       |
| • LeetCode 3 Index Jump: left = max(left, charMap[currChar] + 1)      |
| • Time Invariant: Both pointers move forward -> O(N) Linear Time ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Fixed-Size Window Max Sum in under 2 minutes.
- [ ] I know why Sliding Window reduces $O(N \cdot K)$ to $O(N)$ time.
- [ ] I can write Longest Substring Without Repeats (LeetCode 3) with index jumps.
- [ ] I can state the window length formula `right - left + 1`.
- [ ] I know why the variable window `while` loop takes at most $N$ total steps.
