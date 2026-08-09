# 09. Next Greater Element Variants, Circular Array Sweeping & Digit Permutation Algorithms

## 1. Introduction
The **Next Greater Element (NGE) Problem Suite** represents a major domain of Monotonic Stack applications. From simple linear arrays to circular array traversals (**Next Greater Element II - LeetCode 503**) and lexicographical digit permutations (**Next Greater Element III - LeetCode 556**), Monotonic Stacks solve nearest-greater-value search problems in **$O(N)$ linear time and $O(N)$ auxiliary space**.

> **Important:** In **Next Greater Element II (LeetCode 503)**, the array is circular (the element after `nums[N-1]` wraps around to `nums[0]`). By simulating a doubled array of size $2N$ via index mapping **`nums[i % N]`** and traversing from `i = 2N - 1` down to `0`, a Monotonic Stack finds the Next Greater Element across circular array boundaries in $O(N)$ linear time!

```
Circular Array Virtual Doubling Topology (LeetCode 503):
Virtual Array Indices: 0    1    2    3    4    5  (Size 2N = 6)
Array Values         : [ 1,   2,   1,   1,   2,   1 ] (Modulo Index: i % N)
                       ^-------------^  ^-------------^
                       Original Array    Virtual Copy
Traverse from i = 2N-1 (5) down to 0! Monotonic Stack handles circular bounds! ⚡
```

---

## 2. Core Concepts & Circular Array Sweeping (LeetCode 503)

### 2.1 Next Greater Element II (LeetCode 503 - Circular Array)
Given a circular integer array `nums`, return the next greater number for every element in `nums`:

#### Algorithmic Strategy ($O(N)$ Time, $O(N)$ Auxiliary Space):
1. `N = nums.length`.
2. Create result array `int[] result = new int[N]`.
3. Initialize empty stack `Deque<Integer> stack = new ArrayDeque<>()`.
4. Traverse virtual array from **`i = 2 * N - 1` down to `0`**:
   - `currVal = nums[i % N]`.
   - **Purge Smaller Elements**: While `!stack.isEmpty() && stack.peek() <= currVal`, `stack.pop()`.
   - **Record Answer** (ONLY when `i < N`):
     - `result[i] = stack.isEmpty() ? -1 : stack.peek()`.
   - **Push Current Value**: `stack.push(currVal)`.
5. Return `result`.

```
Why Virtual 2N Virtual Loop Works:
The first N iterations (i = 2N-1 down to N) populate the stack with elements from the right end.
The next N iterations (i = N-1 down to 0) compute the actual answers for indices 0...N-1,
allowing elements near index N-1 to find next greater candidates near index 0! ⚡
```

> **Memory Trick:** **"Circular Array Next Greater: Loop 2N-1 down to 0! Use nums[i % N] and record result ONLY when i < N!"**

---

## 3. Characteristics & Next Greater Element III (LeetCode 556)

### 3.1 Next Greater Element III (LeetCode 556 - Next Lexicographical Permutation)
Given a positive 32-bit integer $N$, find the smallest integer which has the exact same digits as $N$ and is strictly greater than $N$:

#### 4-Step Next Permutation Algorithm ($O(D)$ Time, $O(D)$ Space):
1. Convert integer $N$ to character digit array `char[] a = String.valueOf(n).toCharArray()`.
2. **Step 1 (Find Pivot)**: Scan right-to-left to find first index $i$ where **`a[i] < a[i + 1]`**. If no such $i$ exists, return `-1`.
3. **Step 2 (Find Successor)**: Scan right-to-left to find first index $j$ where **`a[j] > a[i]`**.
4. **Step 3 (Swap Pivot & Successor)**: Swap `a[i]` and `a[j]`.
5. **Step 4 (Reverse Descending Tail)**: Reverse digits from index `i + 1` to end of array to get the smallest lexicographical arrangement!
6. Parse digit array to `long val`. Return `val > Integer.MAX_VALUE ? -1 : (int) val`.

```
Next Permutation 4-Step Visual (n = 124651):
1. Find Pivot     : i = 2 (val 4, because 4 < 6).
2. Find Successor : j = 4 (val 5, because 5 > 4).
3. Swap           : Swap 4 and 5 -> 1 2 5 6 4 1.
4. Reverse Tail   : Reverse 6 4 1 -> 1 4 6.
Result: 1 2 5 1 4 6 ✅ (Smallest Next Greater Integer!)
```

---

## 4. Internal Working Mechanics
Tracing Next Greater Element II (LeetCode 503) on `nums = [1, 2, 1]` ($N = 3, 2N = 6$):

```
Virtual Loop i = 5 down to 0 (nums[i % 3]):

i = 5 (val 1): stack = [1]
i = 4 (val 2): purge 1 <= 2. stack = [2]
i = 3 (val 1): stack = [1, 2]

--- Actual Result Recording Phase (i < 3) ---
i = 2 (val 1): purge 1 <= 1. stack.peek() = 2 -> result[2] = 2. push(1). stack = [1, 2]
i = 1 (val 2): purge 1 <= 2. stack.peek() empty -> result[1] = -1. push(2). stack = [2]
i = 0 (val 1): 2 > 1 -> result[0] = 2. push(1). stack = [1, 2]

Final Circular Result: [2, -1, 2] ✅ (O(N) Time, O(N) Space!)
```

---

## 5. Visual Diagram
Next Greater Element III 4-Step Digit Permutation Topography:

```
Digit Array:   1    2    4    6    5    1
                         ^         ^
                       Pivot i  Successor j
                       (Swap 4 and 5)
               ------------------------------
Result     :   1    2    5    1    4    6
                              ^^^^^^^^^
                        (Reversed Tail 6 4 1 -> 1 4 6)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Next Greater Element II (LeetCode 503) and Next Greater Element III (LeetCode 556):

```java
import java.util.*;

public class NextGreaterVariantsMaster {

    // 1. Next Greater Element II (LeetCode 503 - Circular Array) O(N) Time, O(N) Space
    public static int[] nextGreaterElementsCircular(int[] nums) {
        if (nums == null || nums.length == 0) return new int[0];

        int n = nums.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();

        // Loop virtual 2N indices from 2N-1 down to 0
        for (int i = 2 * n - 1; i >= 0; i--) {
            int currVal = nums[i % n];

            // Purge elements <= current value
            while (!stack.isEmpty() && stack.peek() <= currVal) {
                stack.pop();
            }

            // Record answer for original array indices
            if (i < n) {
                result[i] = stack.isEmpty() ? -1 : stack.peek();
            }

            stack.push(currVal);
        }

        return result;
    }

    // 2. Next Greater Element III (LeetCode 556 - Next Digit Permutation) O(D) Time, O(D) Space
    public static int nextGreaterElement3(int n) {
        char[] a = String.valueOf(n).toCharArray();
        int len = a.length;

        // Step 1: Find first decreasing digit from right (Pivot)
        int i = len - 2;
        while (i >= 0 && a[i] >= a[i + 1]) {
            i--;
        }

        if (i < 0) return -1; // Digits are in complete descending order (no greater permutation)

        // Step 2: Find smallest digit greater than pivot from right (Successor)
        int j = len - 1;
        while (a[j] <= a[i]) {
            j--;
        }

        // Step 3: Swap pivot and successor
        swap(a, i, j);

        // Step 4: Reverse tail from i + 1 to len - 1
        reverse(a, i + 1, len - 1);

        try {
            long val = Long.parseLong(new String(a));
            return val > Integer.MAX_VALUE ? -1 : (int) val;
        } catch (NumberFormatException e) {
            return -1;
        }
    }

    private static void swap(char[] a, int i, int j) {
        char temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }

    private static void reverse(char[] a, int start, int end) {
        while (start < end) {
            swap(a, start, end);
            start++;
            end--;
        }
    }
}
```

> **Quick Syntax:**
```java
// 2N Circular Modulo Virtual Pass Syntax
for (int i = 2 * n - 1; i >= 0; i--) {
    int val = nums[i % n];
    ...
    if (i < n) result[i] = stack.isEmpty() ? -1 : stack.peek();
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 503 - Next Greater Element II**: Circular array monotonic stack.
* **LeetCode 556 - Next Greater Element III**: Lexicographical next permutation.
* **LeetCode 31 - Next Permutation**: Core 4-step permutation algorithm.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Next Greater Element II and Next Greater Element III:

```java
public class NextGreaterVariantsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Next Greater Element II Circular (LeetCode 503) ===");
        int[] nums1 = {1, 2, 1};
        int[] resCirc = NextGreaterVariantsMaster.nextGreaterElementsCircular(nums1);
        System.out.println("Circular Next Greater: " + Arrays.toString(resCirc)); // Output: [2, -1, 2]

        System.out.println("\n=== 2. Next Greater Element III (LeetCode 556) ===");
        int n = 124651;
        int nextGreaterVal = NextGreaterVariantsMaster.nextGreaterElement3(n);
        System.out.println("Next Greater Permutation of " + n + ": " + nextGreaterVal); // Output: 125146
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Circular NGE II (503)**| **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Virtual 2N loop with modulo `i % N` |
| **Digit Permutation III (556)**| **$O(D)$ Linear ⚡** | $O(D)$ Digit Array | 4-step next permutation algorithm |

---

## 10. Edge Cases & Boundary Handling
* **32-Bit Integer Overflow in LeetCode 556**: `Long.parseLong(new String(a)) > Integer.MAX_VALUE` returns `-1`.
* **Decreasing Digit Permutation (`54321`)**: Pivot search `i` fails (`i < 0`), returns `-1` cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Creating Actual Doubled Array ($2N$ Space Penalty) in LeetCode 503**:
  - Allocating a physical array `int[] doubled = new int[2*N]` consumes extra heap memory.
  - **Use modulo virtual indexing `nums[i % N]` on loop `2N-1` down to `0`**.
* **Forgetting to Reverse Descending Tail in LeetCode 556**:
  - Swapping pivot and successor without reversing digits from `i+1` to `N-1` produces a valid greater integer, but NOT the SMALLEST next greater integer!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The 4-Step Next Permutation Pattern:
> 1. Find pivot `a[i] < a[i+1]` from right.
> 2. Find successor `a[j] > a[i]` from right.
> 3. Swap `a[i]` and `a[j]`.
> 4. Reverse array tail from `i+1` to end.
> This single 4-step template solves both **Next Permutation (LeetCode 31)** and **Next Greater Element III (LeetCode 556)**!

> **Memory Trick:** **"Next Permutation: 1. Pivot (a[i]<a[i+1]) -> 2. Successor (a[j]>a[i]) -> 3. Swap -> 4. Reverse Tail!"**

---

## 13. System & Implementation Comparisons

| Feature | Virtual Modulo Loop `i % N` | Physical Array Doubling |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(N)$ Stack Only ⚡** | $O(2N)$ Doubled Array Memory |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N)$ Linear |
| **Code Footprint** | Concise | Allocation Overhead |

---

## 14. How to Recognize This in Questions
* **"Find next greater element in a CIRCULAR array"** $\rightarrow$ LeetCode 503 (Virtual $2N$ modulo loop).
* **"Find smallest integer greater than N with same digits"** $\rightarrow$ LeetCode 556 (4-step Next Permutation algorithm).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does iterating $2N-1$ down to $0$ correctly populate circular Next Greater Elements?**  
  *A:* The first $N$ iterations ($2N-1 \dots N$) fill the stack with right-side circular candidates. The second $N$ iterations ($N-1 \dots 0$) compute the answers for original indices, allowing elements near the array end to inspect wrapped candidates near the array start.
* **Q: Why is reversing the tail required in Next Permutation (Step 4)?**  
  *A:* After swapping the pivot with the successor, the tail digits from `i+1` to end are in strictly DESCENDING order (largest possible arrangement). Reversing them converts the tail into strictly ASCENDING order (smallest possible arrangement), yielding the minimum next greater value.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: NEXT GREATER ELEMENT VARIANTS                         |
+-----------------------------------------------------------------------+
| • Circular Array Rule (503): Virtual loop 2N-1 down to 0 using i % N  |
| • Record Condition (503): Record result[i] ONLY when i < N            |
| • Next Permutation (556): Find pivot (a[i]<a[i+1]), find succ (a[j]>a[i])|
| • Swap & Reverse: Swap pivot & successor; reverse tail i+1 to end     |
| • Overflow Protection: Return -1 if parsed long > Integer.MAX_VALUE   |
| • Time Complexity: O(N) Linear Time | O(N) Auxiliary Space ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Next Greater Element II (LeetCode 503) using $2N$ modulo loop.
- [ ] I know why physical array doubling is unnecessary in circular arrays.
- [ ] I can write Next Greater Element III (LeetCode 556) in $O(D)$ time.
- [ ] I can state the 4 steps of the Next Permutation algorithm.
- [ ] I know how to check for 32-bit integer overflow in digit permutations.
