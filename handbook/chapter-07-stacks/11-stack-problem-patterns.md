# 11. Stack Problem Recognition Patterns

## 1. Introduction
Stack algorithmic problems follow highly recognizable problem phrasing signals in technical coding interviews. Key problem indicators—such as finding the next greater or smaller element, parsing mathematical expressions, matching parentheses, parsing nested brackets, or computing histogram areas—dictate the optimal stack pattern: Monotonic Decreasing Stack, Monotonic Increasing Stack, Multi-Stack State Framing, Base-Index Stacking, or Dual-Stack Lazy Transfer.

> **Important:** Recognizing whether a problem requires **Index Stacking** (storing `i` on stack for distance calculations) vs **Value Stacking** (storing raw values) is the single most crucial design decision in stack problem solving!

## 2. Core Concepts
* **Pattern 1: Matching / Expected Bracket Stacking**: Triggered by "Valid parentheses", "Simplify POSIX path". Push expected closing character or path directory onto stack.
* **Pattern 2: Monotonic Decreasing Stack**: Triggered by "Next Greater Element", "Daily Temperatures", "Next Warmer Day". Pop while `arr[i] > arr[stack.peek()]`.
* **Pattern 3: Monotonic Increasing Stack**: Triggered by "Next Smaller Element", "Largest Rectangle in Histogram". Pop while `arr[i] < arr[stack.peek()]`.
* **Pattern 4: Base Index Stacking (`stack.push(-1)`)**: Triggered by "Longest Valid Parentheses". Pre-push `-1` to track valid substring left boundaries (`i - stack.peek()`).
* **Pattern 5: Multi-Stack State Framing**: Triggered by "Decode nested string `3[a2[c]]`", "Parse chemical formula `K4(ON(SO3)2)2`". Use `countStack` + `stringStack`.
* **Pattern 6: Dual-Stack Lazy Transfer**: Triggered by "Implement Queue using Stacks". Transfer `inStack` to `outStack` ONLY when `outStack.isEmpty()`.

> **Memory Trick:** **"Next Greater? Monotonic Decreasing! Histogram Area? Monotonic Increasing + Dummy Sentinel 0! Decode String? Dual Stacks!"**

## 3. Characteristics / Properties
* **Pattern Recognition Decision Matrix**:

```
Problem Phrasing / Signal                      Optimal Stack Pattern        Target Complexity
---------------------------------------------------------------------------------------------
Validate matching parentheses                   Expected Bracket Push        O(N) Time, O(N) Space
Min add to make parentheses valid              2 Counters (open/needed)     O(N) Time, O(1) Space ⚡
Longest valid parentheses                       Stack w/ Base Index -1       O(N) Time, O(N) Space
Next greater element / Daily temperatures      Monotonic Decreasing Stack   O(N) Time, O(N) Space
Largest rectangle in histogram                 Monotonic Increasing + Dummy O(N) Time, O(N) Space
Evaluate Postfix / Reverse Polish Notation     Operand Stack                O(N) Time, O(N) Space
Basic Calculator with parentheses               Result + Sign Frame Stack    O(N) Time, O(N) Space
Decode nested string `3[a2[c]]`                Dual Stacks (count + string) O(N*maxK), O(N) Space
Implement Queue using Stacks                   Dual-Stack Lazy Transfer     Amortized O(1) Time ⚡
```

## 4. Internal Working
Decision Tree for Selecting Stack Patterns:

```
                      [ Stack Problem ]
                              |
           +------------------+------------------+
           |                                     |
    [ Element Scanning ]                 [ State Framing ]
           |                                     |
   +-------+-------+                     +-------+-------+
   |               |                     |               |
[Range Queries]  [Bracket Pairs]       [Expression Eval]  [String Expansion]
   |               |                     |               |
(Monotonic Stack) (Base Index -1)       (Operand Stack)   (Dual Stacks)
```

## 5. Visual Diagram
Stack Pattern Classification Summary:

```
[ MONOTONIC DECREASING STACK ]
Top is Smallest: [ 75, 72, 69 ] <- Pop 69, 72 when current is 74 (Next Greater!)

[ MONOTONIC INCREASING STACK ]
Top is Largest:  [ 1, 2, 5, 6 ]  <- Pop 6, 5 when current is 2 (Histogram Width!)

[ BASE INDEX ANCHOR STACK ]
Bottom Anchor:   [ -1 ]          <- Valid Substring Length = i - stack.peek()
```

## 6. Operations / Algorithms
Master Pattern Code Snippets:

```java
// Pattern 1: Monotonic Decreasing Stack (Next Greater Element)
Deque<Integer> stack = new ArrayDeque<>();
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {
        int poppedIdx = stack.pop();
        ans[poppedIdx] = i - poppedIdx;
    }
    stack.push(i);
}

// Pattern 2: Dual-Stack String Decoding (Opening Bracket Frame)
countStack.push(k);
stringStack.push(currString);
currString = new StringBuilder();
k = 0;

// Pattern 3: Dual-Stack Queue Transfer
if (outStack.isEmpty()) {
    while (!inStack.isEmpty()) {
        outStack.push(inStack.pop());
    }
}
```

> **Quick Syntax:**
```java
// Monotonic Stack Index Push
stack.push(i);
```

## 7. Examples
* **LeetCode 739 - Daily Temperatures**: Monotonic Decreasing Stack.
* **LeetCode 84 - Largest Rectangle in Histogram**: Monotonic Increasing Stack + Dummy Sentinel 0.
* **LeetCode 394 - Decode String**: Dual Stack Frame Parsing.

## 8. Java Code
Complete interview-ready Java suite demonstrating pattern selection across major stack interview problems:

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

public class StackPatternRecognitionMaster {

    // Pattern 1: Next Greater Element I (LeetCode 496) O(N) Time, O(N) Space
    public static int[] nextGreaterElement(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        Deque<Integer> stack = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[i] > nums[stack.peek()]) {
                result[stack.pop()] = nums[i];
            }
            stack.push(i);
        }

        return result;
    }

    // Pattern 2: Simplify Path (LeetCode 71) O(N) Time, O(N) Space
    public static String simplifyPath(String path) {
        Deque<String> stack = new ArrayDeque<>();
        String[] parts = path.split("/");

        for (String part : parts) {
            if (part.equals("..")) {
                if (!stack.isEmpty()) stack.pop();
            } else if (!part.isEmpty() && !part.equals(".")) {
                stack.push(part);
            }
        }

        StringBuilder sb = new StringBuilder();
        // ArrayDeque iteration is top-to-bottom; use descendingIterator for bottom-to-top path!
        var it = stack.descendingIterator();
        while (it.hasNext()) {
            sb.append("/").append(it.next());
        }

        return sb.length() == 0 ? "/" : sb.toString();
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums = {2, 1, 2, 43, 3};
        System.out.println("Next Greater Elements: " + Arrays.toString(nextGreaterElement(nums)));
        // Output: [43, 2, 43, -1, -1]

        String path = "/a/./b/../../c/";
        System.out.println("Simplified Path: '" + simplifyPath(path) + "'"); // Output: '/c'
    }
}
```

## 9. Complexity Analysis
| Stack Pattern | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Monotonic Stack** | **$O(N)$ Amortized** | $O(N)$ Stack | Reduces $O(N^2)$ loops to linear time ⚡ |
| **Base Index Stacking** | **$O(N)$ Linear** | $O(N)$ Stack | Computes substring lengths in $O(1)$ |
| **Dual Stack Queue** | **Amortized $O(1)$**| $O(N)$ Space | Lazy dual-stack FIFO conversion |

## 10. Edge Cases
* **No Next Greater Element**: Result defaults to `-1` for elements remaining on stack when loop finishes.
* **Root Directory Path (`"/../"`)**: Popping from empty stack in `simplifyPath` is safely ignored.
* **Empty Input Strings**: Return empty string or `/` cleanly.

## 11. Common Mistakes
* Storing raw values instead of **ARRAY INDICES** when distance calculations (`i - poppedIdx`) are required.
* Iterating `ArrayDeque` stack directly for path strings without using `descendingIterator()` (reverses POSIX directory order!).
* Using `java.util.Stack` instead of `java.util.ArrayDeque`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `ArrayDeque` Iteration Order Warning:
> `stack.iterator()` traverses from TOP to BOTTOM (LIFO order).
> If you need to print elements in original insertion order (BOTTOM to TOP, FIFO order), use:
> **`Iterator<T> it = stack.descendingIterator();`**

> **Memory Trick:** **"Need bottom-to-top order from ArrayDeque? Use stack.descendingIterator()!"**

## 13. Comparisons
| Problem Signal | Sub-Optimal Approach | Optimal Stack Pattern |
| :--- | :--- | :--- |
| **Next Greater Element** | $O(N^2)$ Nested Loops | **Monotonic Decreasing Stack ($O(N)$)** |
| **Histogram Max Area** | $O(N^2)$ Span Search | **Monotonic Increasing Stack ($O(N)$)** |
| **Min Add Parentheses** | $O(N)$ Stack Allocation | **2 Counters ($O(1)$ Space)** |

## 14. How to Recognize This in Questions
* **"Find next warmer temperature / next greater element"** $\rightarrow$ Monotonic Decreasing Stack.
* **"Find largest rectangle in bar chart"** $\rightarrow$ Monotonic Increasing Stack + Dummy Sentinel 0.
* **"Expand nested bracket string like 3[a2[c]]"** $\rightarrow$ Dual Stack Parsing (`countStack` + `stringStack`).

## 15. Frequently Asked Interview Questions
* **Q: How do you choose between Monotonic Decreasing vs Monotonic Increasing Stack?**  
  *A:* Use **Monotonic Decreasing** when looking for the **Next Greater** element (popping smaller elements when a larger element arrives). Use **Monotonic Increasing** when looking for the **Next Smaller** element or computing histogram width boundaries (popping larger elements when a smaller element arrives).
* **Q: Why is `stack.descendingIterator()` used in LeetCode 71 (Simplify Path)?**  
  *A:* `ArrayDeque.iterator()` iterates top-to-bottom (newest directories first). Using `descendingIterator()` iterates bottom-to-top (root directory first), allowing straightforward POSIX path construction (`/a/b/c`).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STACK PROBLEM RECOGNITION PATTERNS                    |
+-----------------------------------------------------------------------+
| • Next Greater Element: Monotonic Decreasing Stack (arr[i] > arr[peek])|
| • Histogram Max Area: Monotonic Increasing Stack + Dummy Sentinel 0   |
| • Longest Valid Parentheses: Pre-push stack.push(-1) base index       |
| • Decode String: Dual Stacks (countStack & stringStack)               |
| • Simplify Path: Use stack.descendingIterator() for root-first path   |
| • Modern Java Standard: Deque<Integer> stack = new ArrayDeque<>()     |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can select the optimal stack pattern within 60 seconds of reading a problem prompt.
- [ ] I know when to store array indices vs raw values on a stack.
- [ ] I know why `stack.descendingIterator()` is used for path construction.
- [ ] I can implement Monotonic Decreasing and Increasing stacks from memory.
- [ ] I can implement Simplify Path (LeetCode 71) in under 5 minutes.
