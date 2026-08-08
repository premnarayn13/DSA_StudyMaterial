# 04. Monotonic Stack Pattern & Range Query Optimization

## 1. Introduction
The **Monotonic Stack** is one of the most powerful and frequently tested algorithmic patterns in advanced technical coding interviews. A Monotonic Stack maintains its elements in strictly increasing or decreasing order. In problems such as Next Greater Element (LeetCode 496 / 503), Daily Temperatures (LeetCode 739), Largest Rectangle in Histogram (LeetCode 84), and Trapping Rain Water (LeetCode 42), the Monotonic Stack reduces brute-force $O(N^2)$ search loops down to **$O(N)$ linear time**.

> **Important:** Monotonic Stack works because each array element is **pushed to the stack exactly once** and **popped from the stack at most once**. Even with nested loops, total operations are bounded by $2N \implies \mathbf{O(N)\text{ Linear Time}}$!

## 2. Core Concepts
* **Monotonic Decreasing Stack** (Top element is smallest $\to$ Bottom is largest):
  * **Use Case**: Used to find the **Next Greater Element** to the right.
  * **Mechanism**: Before pushing `curr`, pop all elements $\le \text{curr}$. The popped elements have found `curr` as their Next Greater Element!
* **Monotonic Increasing Stack** (Top element is largest $\to$ Bottom is smallest):
  * **Use Case**: Used to find the **Next Smaller Element** to the right.
  * **Mechanism**: Before pushing `curr`, pop all elements $\ge \text{curr}$.
* **Index Stacking**: In almost all advanced problems (e.g. Daily Temperatures, Histogram), store **ARRAY INDICES** on the stack rather than raw values (`stack.push(i)`), allowing calculation of index distances (`i - poppedIndex`).

> **Memory Trick:** **"Next Greater Element? Use Monotonic DECREASING Stack! Pop while stack.peek() <= curr!"**

## 3. Characteristics / Properties
* **Element Lifecycle Guarantee**: Every index enters the stack once and leaves once $\implies O(N)$ Amortized Time Complexity.
* **Stack State Invariant**: At any point, elements inside a Monotonic Decreasing Stack represent a sequence of elements for which no greater element to their right has been discovered yet.

```
Monotonic Stack Variants Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variant               | Stack Order (Top) | Pop Condition     | Solves Problem    |
+-----------------------+-------------------+-------------------+-------------------+
| Monotonic Decreasing  | Smallest at Top   | `arr[stack.peek()] <= curr` | Next Greater Element ⚡|
| Monotonic Increasing  | Largest at Top    | `arr[stack.peek()] >= curr` | Next Smaller Element ⚡|
| Index Stacking        | Stores Indices `i`| Compare `arr[i]`  | Distance calculation|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Next Greater Element on `[73, 74, 75, 71, 69, 72, 76]` (Daily Temperatures LeetCode 739):

```
Init: ans = [0,0,0,0,0,0,0], stack = []

i=0 (73): stack.push(0)  | stack: [0]
i=1 (74): 74 > arr[0](73) -> pop 0! ans[0] = 1-0 = 1. stack.push(1) | stack: [1]
i=2 (75): 75 > arr[1](74) -> pop 1! ans[1] = 2-1 = 1. stack.push(2) | stack: [2]
i=3 (71): 71 < 75 -> stack.push(3) | stack: [2, 3]
i=4 (69): 69 < 71 -> stack.push(4) | stack: [2, 3, 4]
i=5 (72):
  - 72 > arr[4](69) -> pop 4! ans[4] = 5-4 = 1
  - 72 > arr[3](71) -> pop 3! ans[3] = 5-3 = 2
  - 72 < arr[2](75) -> stop popping. stack.push(5) | stack: [2, 5]
i=6 (76): 76 > all -> pop 5 (ans[5]=1), pop 2 (ans[2]=4). push(6)

Final Result Days: [1, 1, 4, 2, 1, 1, 0] ✅ (Linear O(N) Time!)
```

## 5. Visual Diagram
Monotonic Decreasing Stack Popping Mechanics:

```
Current Array Element: [ 72 ] at index 5

Stack before push: [ 75(idx 2), 71(idx 3), 69(idx 4) ]  <-- Top is 69

1. Compare 72 > 69 -> POP idx 4! Days[4] = 5 - 4 = 1 day wait
2. Compare 72 > 71 -> POP idx 3! Days[3] = 5 - 3 = 2 days wait
3. Compare 72 < 75 -> STOP POPPING!

Stack after push:  [ 75(idx 2), 72(idx 5) ]  <-- Top is 72
```

## 6. Operations / Algorithms
LeetCode 739 Daily Temperatures Master Implementation:

```java
// LeetCode 739: Daily Temperatures O(N) Time, O(N) Space
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>(); // Stores INDICES

    for (int i = 0; i < n; i++) {
        // While current temperature is warmer than top of stack
        while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
            int prevIdx = stack.pop();
            answer[prevIdx] = i - prevIdx; // Calculate day gap
        }
        stack.push(i); // Push current index
    }

    return answer;
}
```

> **Quick Syntax:**
```java
// Monotonic Stack Loop Template
while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {
    int poppedIdx = stack.pop();
    result[poppedIdx] = i - poppedIdx;
}
stack.push(i);
```

## 7. Examples
* **LeetCode 739 - Daily Temperatures**: Next warmer temperature distance.
* **LeetCode 496 / 503 - Next Greater Element I & II**: Next greater element array search (with circular array wrapping).
* **LeetCode 84 - Largest Rectangle in Histogram**: Monotonic Increasing Stack area calculation.

## 8. Java Code
Complete interview-ready Java suite implementing Daily Temperatures (LeetCode 739) and Next Greater Element II Circular Array (LeetCode 503):

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class MonotonicStackMaster {

    // 1. Daily Temperatures (LeetCode 739) O(N) Time, O(N) Space
    public static int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && temperatures[i] > temperatures[stack.peek()]) {
                int prevIdx = stack.pop();
                answer[prevIdx] = i - prevIdx;
            }
            stack.push(i);
        }

        return answer;
    }

    // 2. Next Greater Element II Circular Array (LeetCode 503) O(N) Time, O(N) Space
    public static int[] nextGreaterElementsCircular(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        Deque<Integer> stack = new ArrayDeque<>();

        // Simulate 2N iterations for circular array wrapping
        for (int i = 0; i < 2 * n; i++) {
            int num = nums[i % n];
            while (!stack.isEmpty() && nums[stack.peek()] < num) {
                result[stack.pop()] = num;
            }
            if (i < n) {
                stack.push(i);
            }
        }

        return result;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] temps = {73, 74, 75, 71, 69, 72, 76};
        System.out.println("Daily Temps Wait Days: " + Arrays.toString(dailyTemperatures(temps)));
        // Output: [1, 1, 4, 2, 1, 1, 0]

        int[] circularNums = {1, 2, 1};
        System.out.println("Circular Next Greater: " + Arrays.toString(nextGreaterElementsCircular(circularNums)));
        // Output: [2, -1, 2]
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Reason |
| :--- | :--- | :--- | :--- |
| **Daily Temperatures** | **$O(N)$ Amortized** | $O(N)$ Stack Space | Each index pushed/popped at most once |
| **Next Greater Element II**| **$O(N)$ Amortized** | $O(N)$ Stack Space | 2Pass loop $2N$ iteration |
| **Histogram Rectangle** | **$O(N)$ Amortized** | $O(N)$ Stack Space | Computes max area in linear time |

## 10. Edge Cases
* **No Greater Element Found**: Elements remaining in stack when loop finishes have no next greater element. Result array defaults to `0` or `-1`.
* **Circular Array Wrapping (LeetCode 503)**: Iterating $2 \times N$ times using index modulo `i % n` simulates circular list traversal cleanly.
* **Duplicate Array Values**: When values are equal (`temperatures[i] == temperatures[stack.peek()]`), choose strict `>` vs `>=` depending on problem specifications.

## 11. Common Mistakes
* Pushing element values (`nums[i]`) onto stack instead of array **INDICES (`i`)** (prevents distance calculations `i - poppedIdx`!).
* Confusing strictly increasing vs strictly decreasing monotonic condition.
* Assuming the nested `while` loop makes the algorithm $O(N^2)$ (it is strictly $O(N)$ amortized because no element is popped more than once!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Store INDICES, Not Values!
> Always store **array indices `i`** on the Monotonic Stack: `stack.push(i)`.
> * Access value via **`arr[stack.peek()]`**.
> * Access distance/gap via **`i - poppedIdx`**!

> **Memory Trick:** **"Always store INDICES on Monotonic Stack to get distance i - poppedIdx!"**

## 13. Comparisons
| Feature | Brute Force Double Loop | Monotonic Stack Pattern |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N^2)$ Quadratic | **$O(N)$ Amortized Linear ⚡** |
| **Auxiliary Space** | $O(1)$ | $O(N)$ Stack Memory |
| **Interview Recommendation** | TLE (Time Limit Exceeded) | **OPTIMAL EXPECTED ANSWER** |

## 14. How to Recognize This in Questions
* **"Find next warmer temperature / next greater element"** $\rightarrow$ Monotonic Decreasing Stack.
* **"Find nearest smaller element / largest rectangle area"** $\rightarrow$ Monotonic Increasing Stack.
* **"Calculate water trapped between bars"** $\rightarrow$ Monotonic Stack (LeetCode 42).

## 15. Frequently Asked Interview Questions
* **Q: Why is Monotonic Stack $O(N)$ time despite having a `while` loop inside a `for` loop?**  
  *A:* Because across the entire execution of the algorithm, each array index is pushed onto the stack exactly once and popped from the stack at most once. The total number of `while` loop executions across all iterations cannot exceed $N$, yielding an amortized time complexity of $O(N)$.
* **Q: How does Monotonic Stack handle circular arrays (LeetCode 503)?**  
  *A:* Iterate loop index $i$ from $0$ to $2N - 1$, accessing array values using `nums[i % n]`. Only push indices during the first pass ($i < n$), allowing the second pass to resolve next greater elements for elements near the end of the array.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MONOTONIC STACK PATTERN                               |
+-----------------------------------------------------------------------+
| • Rule: Store INDICES on stack (stack.push(i))                        |
| • Next Greater Element: Pop while (!stack.isEmpty() && arr[i] > arr[top])|
| • Distance Calculation: gap = i - poppedIndex                         |
| • Circular Array Trick: Loop 0 to 2N-1 with arr[i % n]; push if i < n |
| • Time Complexity: Amortized O(N) Linear Time                         |
| • Auxiliary Space: O(N) Stack Space                                   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why Monotonic Stack runs in $O(N)$ time despite nested `while` loops.
- [ ] I always store array indices `i` on the Monotonic Stack.
- [ ] I can write Daily Temperatures (LeetCode 739) in under 3 minutes.
- [ ] I can solve circular array problems (LeetCode 503) using $2N$ iteration.
- [ ] I can select between Monotonic Decreasing vs Increasing stack configurations.
