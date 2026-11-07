# 05. Monotonic Stack Mechanics, Next Greater Element & Range Invariant Traversal

## 1. Introduction
The **Monotonic Stack Pattern** is one of the most vital algorithmic techniques for linear search problems. By maintaining elements inside a stack in a strictly **Monotonic Ordering** (either strictly increasing or strictly decreasing), a Monotonic Stack finds the **Next Greater Element**, **Next Smaller Element**, **Previous Greater Element**, or **Previous Smaller Element** for every item in an array in **$O(N)$ linear time and $O(N)$ auxiliary space**.

> **Important:** Why does a Monotonic Stack achieve $O(N)$ linear time instead of $O(N^2)$ brute-force searching?
> Even though there is a `while` loop popping elements inside the array iteration, **EVERY ARRAY INDEX IS PUSHED EXACTLY ONCE AND POPPED AT MOST ONCE**!
> Total stack operations across the entire algorithm $\le 2N \implies \mathbf{O(N)\text{ Amortized Linear Time}}$!

```
Monotonic Stack Classification Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Monotonic Stack Variant| Stack Property   | Purge Condition   | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| Monotonic Decreasing  | Elements decrease | `stack.peek() <= current` | Next Greater Element |
| Monotonic Increasing  | Elements increase | `stack.peek() >= current` | Next Smaller Element |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 2. Core Concepts & Next Greater Element Mechanics

### 2.1 Next Greater Element Algorithm (LeetCode 496 / 739)
Given an array `nums`, find the next element to the right that is strictly greater than `nums[i]` for every index $i$:

#### Standard Right-to-Left Traversal Template:
1. Initialize an empty stack `Deque<Integer> stack = new ArrayDeque<>()`.
2. Create result array `int[] result = new int[N]`.
3. Traverse array from **Right to Left (`i = N - 1` down to `0`)**:
   - **Purge Smaller Elements**: While `!stack.isEmpty() && stack.peek() <= nums[i]`, `stack.pop()`.
   - **Record Answer**: `result[i] = stack.isEmpty() ? -1 : stack.peek()`.
   - **Push Current Element**: `stack.push(nums[i])`.
4. Return `result`.

```
Why Right-to-Left Traversal Works:
Traversing right-to-left ensures that the stack contains ONLY candidates residing to the RIGHT of index i.
Popping smaller elements eliminates values that can NEVER be the Next Greater Element for index i or ANY index to the left! ⚡
```

### 2.2 Daily Temperatures (LeetCode 739)
Given an array of integers `temperatures`, return an array `answer` where `answer[i]` is the number of days you have to wait after the $i$-th day to get a warmer temperature:
* **Index Storage Strategy**: Instead of storing values in the stack, **Store Array Indices**!
* `daysToWait = stack.isEmpty() ? 0 : stack.peek() - i`.

> **Memory Trick:** **"Next Greater Element: Monotonic Decreasing Stack! Traverse Right-to-Left; purge stack.peek() <= val!"**

---

## 3. Characteristics & Online Stock Span Mechanics (LeetCode 901)

### 3.1 Online Stock Span (LeetCode 901 - Monotonic Stack Stream)
Design an algorithm that collects daily price quotes for a stock and returns the **span** of that stock's price for the current day (the maximum number of consecutive days for which the price was $\le$ current price):

```java
public class StockSpanner {
    private Deque<int[]> stack; // Stores pairs: [price, span]

    public StockSpanner() {
        stack = new ArrayDeque<>();
    }

    public int next(int price) {
        int span = 1;
        while (!stack.isEmpty() && stack.peek()[0] <= price) {
            span += stack.pop()[1]; // Accumulate previous spans!
        }
        stack.push(new int[]{price, span});
        return span;
    }
}
```

---

## 4. Internal Working Mechanics
Tracing Daily Temperatures (LeetCode 739) on `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`:

```
Traverse Right-to-Left (i = 7 down to 0):

i = 7 (val 73): stack empty -> result[7] = 0. push(7). stack = [7(73)]
i = 6 (val 76): purge 7(73) <= 76. stack empty -> result[6] = 0. push(6). stack = [6(76)]
i = 5 (val 72): 76 > 72 -> result[5] = 6 - 5 = 1. push(5). stack = [5(72), 6(76)]
i = 4 (val 69): 72 > 69 -> result[4] = 5 - 4 = 1. push(4). stack = [4(69), 5(72), 6(76)]
i = 3 (val 71): purge 4(69) <= 71. 72 > 71 -> result[3] = 5 - 3 = 2. push(3). stack = [3(71), 5(72), 6(76)]
i = 2 (val 75): purge 3(71), 5(72) <= 75. 76 > 75 -> result[2] = 6 - 2 = 4. push(2). stack = [2(75), 6(76)]
i = 1 (val 74): 75 > 74 -> result[1] = 2 - 1 = 1. push(1). stack = [1(74), 2(75), 6(76)]
i = 0 (val 73): 74 > 73 -> result[0] = 1 - 0 = 1. push(0). stack = [0(73), 1(74), ...]

Final Days to Wait Array: [1, 1, 4, 2, 1, 1, 0, 0] ✅ (O(N) Time, O(N) Space!)
```

---

## 5. Visual Diagram
Monotonic Decreasing Stack Purge & Push Topology:

```
Incoming val 75 at i=2:
Stack Top -> [ Index 3 (Val 71), Index 5 (Val 72), Index 6 (Val 76) ] <- Stack Bottom
                |                 |
                v                 v
             PURGE (71 <= 75)   PURGE (72 <= 75)   (76 > 75 KEEP!)

New Stack Top -> [ Index 2 (Val 75), Index 6 (Val 76) ] <- Stack Bottom
Next Greater Element for i=2 is at Index 6! (Wait = 6 - 2 = 4 days)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Next Greater Element I (LeetCode 496), Daily Temperatures (LeetCode 739), and Online Stock Span (LeetCode 901):

```java
import java.util.*;

public class MonotonicStackMaster {

    // 1. Daily Temperatures (LeetCode 739) O(N) Time, O(N) Space
    public static int[] dailyTemperatures(int[] temperatures) {
        if (temperatures == null || temperatures.length == 0) return new int[0];

        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>(); // Stores array indices

        for (int i = n - 1; i >= 0; i--) {
            // Purge indices with temperatures <= current temperature
            while (!stack.isEmpty() && temperatures[stack.peek()] <= temperatures[i]) {
                stack.pop();
            }

            // Record days to wait
            result[i] = stack.isEmpty() ? 0 : stack.peek() - i;

            // Push current index
            stack.push(i);
        }

        return result;
    }

    // 2. Next Greater Element I (LeetCode 496) O(N + M) Time, O(N) Space
    public static int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();

        // Process nums2 from right to left
        for (int i = nums2.length - 1; i >= 0; i--) {
            int val = nums2[i];
            while (!stack.isEmpty() && stack.peek() <= val) {
                stack.pop();
            }

            nextGreaterMap.put(val, stack.isEmpty() ? -1 : stack.peek());
            stack.push(val);
        }

        // Map results for nums1
        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            result[i] = nextGreaterMap.get(nums1[i]);
        }

        return result;
    }

    // 3. Online Stock Span (LeetCode 901) O(1) Amortized Time per next() Call
    public static class StockSpanner {
        private Deque<int[]> stack; // Stores pairs [price, span]

        public StockSpanner() {
            stack = new ArrayDeque<>();
        }

        public int next(int price) {
            int span = 1;
            while (!stack.isEmpty() && stack.peek()[0] <= price) {
                span += stack.pop()[1];
            }
            stack.push(new int[]{price, span});
            return span;
        }
    }
}
```

> **Quick Syntax:**
```java
// Right-to-Left Monotonic Stack Purge Pattern
while (!stack.isEmpty() && arr[stack.peek()] <= arr[i]) {
    stack.pop();
}
result[i] = stack.isEmpty() ? -1 : stack.peek();
stack.push(i);
```

---

## 7. Concrete Problem Examples
* **LeetCode 739 - Daily Temperatures**: Next Greater Element index distance.
* **LeetCode 496 - Next Greater Element I**: Sub-array next greater element mapping.
* **LeetCode 901 - Online Stock Span**: Monotonic stack stream span accumulation.
* **LeetCode 503 - Next Greater Element II**: Circular array monotonic stack.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Daily Temperatures and Online Stock Span:

```java
public class MonotonicStackDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Daily Temperatures (LeetCode 739) ===");
        int[] temps = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] days = MonotonicStackMaster.dailyTemperatures(temps);
        System.out.println("Days to Wait: " + Arrays.toString(days));
        // Output: [1, 1, 4, 2, 1, 1, 0, 0]

        System.out.println("\n=== 2. Online Stock Span (LeetCode 901) ===");
        MonotonicStackMaster.StockSpanner spanner = new MonotonicStackMaster.StockSpanner();
        int[] prices = {100, 80, 60, 70, 60, 75, 85};
        System.out.print("Spans: ");
        for (int p : prices) {
            System.out.print(spanner.next(p) + " ");
        }
        // Output: 1 1 1 2 1 4 6
        System.out.println();
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Daily Temps (739)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Push and pop each index at most once |
| **Next Greater I (496)** | **$O(N + M)$ Linear ⚡**| $O(N)$ Map Space | Single pass over `nums2` |
| **Stock Span (901)** | **$O(1)$ Amortized ⚡**| $O(N)$ Stack Space | Accumulated span pair stack |

---

## 10. Edge Cases & Boundary Handling
* **Strictly Decreasing Array (`[9, 8, 7, 6]`)**: No next greater element exists; all results are `0` or `-1`.
* **Strictly Increasing Array (`[1, 2, 3, 4]`)**: Each element pops the previous element immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Using $O(N^2)$ Nested Loops for Next Greater Search**:
  - Writing an inner loop `for (int j = i + 1; j < N; j++)` causes TLE on large arrays ($N = 10^5$).
  - **Use a Monotonic Stack for $O(N)$ linear time**.
* **Storing Values Instead of Array Indices**:
  - Storing values in Daily Temperatures prevents calculating index distance (`stack.peek() - i`).
  - **Always store ARRAY INDICES in the stack**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Monotonic Stack Direction Rules:
> * **Next Greater Element**: Traverse **Right-to-Left**, Purge `stack.peek() <= val`.
> * **Next Smaller Element**: Traverse **Right-to-Left**, Purge `stack.peek() >= val`.
> * **Previous Greater Element**: Traverse **Left-to-Right**, Purge `stack.peek() <= val`.
> * **Previous Smaller Element**: Traverse **Left-to-Right**, Purge `stack.peek() >= val`.

> **Memory Trick:** **"Next = Right-to-Left traversal! Greater = Purge <= val! Smaller = Purge >= val!"**

---

## 13. System & Implementation Comparisons

| Feature | Monotonic Stack Approach | Brute-Force Nested Loops |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N^2)$ Quadratic |
| **Auxiliary Memory** | $O(N)$ Stack Space | **$O(1)$ Constant** |
| **Execution Steps** | $\le 2N$ Total Operations | $N(N-1)/2$ Operations |

---

## 14. How to Recognize This in Questions
* **"Find next element to the right greater/smaller than current"** $\rightarrow$ Monotonic Stack (Right-to-Left).
* **"Find number of days until warmer temperature"** $\rightarrow$ Monotonic Stack storing indices (LeetCode 739).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Monotonic Stack achieve $O(N)$ amortized time despite the inner `while` loop?**  
  *A:* Because every element is pushed onto the stack exactly once and popped at most once across the entire algorithm loop.
* **Q: How to handle circular arrays in Next Greater Element II (LeetCode 503)?**  
  *A:* Simulate a doubled array by looping index `i` from `2N - 1` down to `0`, accessing elements via `nums[i % N]`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MONOTONIC STACK MECHANICS                             |
+-----------------------------------------------------------------------+
| • Next Greater Rule: Right-to-Left pass; while (peek() <= val) pop() |
| • Days to Wait Formula: answer[i] = stack.isEmpty() ? 0 : stack.peek() - i|
| • Index Storage Rule: Store ARRAY INDICES in stack for distance queries|
| • Stock Span (901): Store [price, span]; sum popped spans on push     |
| • Circular Array (503): Loop 2N-1 down to 0 using nums[i % N]          |
| • Time Complexity: O(N) Amortized Linear Time | O(N) Space ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Daily Temperatures (LeetCode 739) in $O(N)$ time.
- [ ] I know why storing indices is required for distance calculations.
- [ ] I can solve Next Greater Element I (LeetCode 496).
- [ ] I can write Online Stock Span (LeetCode 901) using pair stack.
- [ ] I can solve Next Greater Element II (LeetCode 503) for circular arrays.
