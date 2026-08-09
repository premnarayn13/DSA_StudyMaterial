# 07. Parentheses Matching, Stack Index Tracking & Longest Valid Substring Mechanics

## 1. Introduction
**Parentheses Problems** form a canonical sub-family of Stack applications. Because nested bracket pairs follow a strict **LIFO (Last-In, First-Out) Structural Symmetry**, stacks match opening brackets with corresponding closing brackets in **$O(N)$ linear time and $O(N)$ auxiliary space**. Key problems include **Valid Parentheses (LeetCode 20)**, **Longest Valid Parentheses (LeetCode 32)**, **Minimum Remove to Make Valid Parentheses (LeetCode 1249)**, and **Generate Parentheses (LeetCode 22)**.

> **Important:** In **Longest Valid Parentheses (LeetCode 32)**, pushing **ARRAY INDICES** (rather than bracket characters) onto the stack enables computing the exact length of continuous valid parentheses substrings in **$O(N)$ linear time**! Initializing the stack with a sentinel index `-1` provides the boundary base for valid substring calculations!

```
LIFO Bracket Matching Topology:
Input String:  (  [  {  }  ]  )
Stack Action: Push Push Push -> Pop '}' matches '{' -> Pop ']' matches '[' -> Pop ')' matches '('
Stack State : [ ( ] -> [ (, [ ] -> [ (, [, { ] -> [ (, [ ] -> [ ( ] -> [ ] (Empty -> VALID! ✅)
```

---

## 2. Core Concepts & Parentheses Matching Mechanics

### 2.1 Valid Parentheses Verification (LeetCode 20)
Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['`, and `']'`:
1. Initialize an empty stack `Deque<Character> stack = new ArrayDeque<>()`.
2. For each character `c` in `s`:
   - If `c` is an opening bracket (`'('`, `'{'`, `'['`), push its corresponding closing bracket (`')'`, `'}'`, `']'`) onto the stack!
   - Else if `c` is a closing bracket:
     - If `stack.isEmpty()` OR `stack.pop() != c`, return `false`!
3. Return `stack.isEmpty()`.

```java
// Clean Map-Free Matching Syntax Trick:
if (c == '(') stack.push(')');
else if (c == '{') stack.push('}');
else if (c == '[') stack.push(']');
else if (stack.isEmpty() || stack.pop() != c) return false;
```

### 2.2 Longest Valid Parentheses (LeetCode 32 - Stack Index Boundary Strategy)
Given a string containing just `'('` and `')'`, find the length of the longest valid parentheses substring:
1. Create index stack `Deque<Integer> stack = new ArrayDeque<>()`.
2. **Sentinel Initialization**: `stack.push(-1)` (Acts as initial valid substring boundary).
3. `maxLen = 0`.
4. For `i = 0` to $N - 1$:
   - If `s.charAt(i) == '('`, push index: `stack.push(i)`.
   - Else (`s.charAt(i) == ')'`):
     - `stack.pop()` (Pop matching opening index or boundary sentinel).
     - If `stack.isEmpty()`:
       - `stack.push(i)` (Push current index as NEW invalid boundary sentinel!).
     - Else:
       - `validLen = i - stack.peek()`.
       - `maxLen = Math.max(maxLen, validLen)`.
5. Return `maxLen`.

> **Memory Trick:** **"Longest Valid Parentheses (32): Push -1 sentinel onto index stack! On ')', pop stack; if empty push i as new boundary sentinel, else maxLen = max(maxLen, i - stack.peek())!"**

---

## 3. Characteristics & Minimum Remove to Make Valid Parentheses (LeetCode 1249)

### 3.1 Minimum Remove to Make Valid Parentheses (LeetCode 1249)
Given a string `s` of `'('`, `')'` and lowercase English characters, remove the minimum number of parentheses so that the resulting string is valid:
1. Maintain stack storing indices of unmatched opening parentheses `(` and a boolean array `invalid[N]`.
2. For `i = 0` to $N - 1$:
   - `c = s.charAt(i)`.
   - If `c == '('`, `stack.push(i)`.
   - Else if `c == ')'`:
     - If `!stack.isEmpty()`, `stack.pop()`.
     - Else, mark `invalid[i] = true` (Unmatched closing bracket!).
3. Mark remaining unmatched opening bracket indices in `stack` as `invalid[idx] = true`.
4. Build result string omitting all `invalid[i] == true` characters in $O(N)$ time!

---

## 4. Internal Working Mechanics
Tracing Longest Valid Parentheses (LeetCode 32) on `s = ")()())"`:

```
Init: stack = [-1], maxLen = 0

i = 0 (')'): pop() -> stack becomes empty!
  - Push 0 as new boundary sentinel. stack = [0].

i = 1 ('('): push(1). stack = [1, 0].

i = 2 (')'): pop() -> pops 1. stack = [0] (Not empty!).
  - validLen = 2 - stack.peek(0) = 2. maxLen = max(0, 2) = 2.

i = 3 ('('): push(3). stack = [3, 0].

i = 4 (')'): pop() -> pops 3. stack = [0] (Not empty!).
  - validLen = 4 - stack.peek(0) = 4. maxLen = max(2, 4) = 4.

i = 5 (')'): pop() -> pops 0. stack becomes empty!
  - Push 5 as new boundary sentinel. stack = [5].

Final Maximum Valid Parentheses Length = 4 ("()()") ✅ (O(N) Time, O(N) Space!)
```

---

## 5. Visual Diagram
Stack Index Sentinel Boundary Advancement Topography:

```
String S:   )   (   )   (   )   )
Indices :   0   1   2   3   4   5
           ^                 ^
     Sentinel 0          Valid Substring [1..4] = "()()"
                         Length = i - stack.peek() = 4 - 0 = 4 ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Valid Parentheses (LeetCode 20), Longest Valid Parentheses (LeetCode 32), Minimum Remove to Make Valid (LeetCode 1249), and Generate Parentheses (LeetCode 22):

```java
import java.util.*;

public class ParenthesesProblemsMaster {

    // 1. Valid Parentheses (LeetCode 20) O(N) Time, O(N) Space
    public static boolean isValid(String s) {
        if (s == null || s.length() % 2 != 0) return false;

        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) return false;
        }

        return stack.isEmpty();
    }

    // 2. Longest Valid Parentheses (LeetCode 32) O(N) Time, O(N) Space
    public static int longestValidParentheses(String s) {
        if (s == null || s.length() < 2) return 0;

        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1); // Sentinel boundary initialization
        int maxLen = 0;

        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else {
                stack.pop(); // Pop match or boundary sentinel
                if (stack.isEmpty()) {
                    stack.push(i); // New invalid boundary sentinel
                } else {
                    maxLen = Math.max(maxLen, i - stack.peek());
                }
            }
        }

        return maxLen;
    }

    // 3. Minimum Remove to Make Valid Parentheses (LeetCode 1249) O(N) Time, O(N) Space
    public static String minRemoveToMakeValid(String s) {
        if (s == null || s.length() == 0) return "";

        Deque<Integer> stack = new ArrayDeque<>();
        boolean[] invalid = new boolean[s.length()];

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') {
                stack.push(i);
            } else if (c == ')') {
                if (!stack.isEmpty()) {
                    stack.pop();
                } else {
                    invalid[i] = true; // Unmatched closing parenthesis
                }
            }
        }

        // Mark remaining unmatched opening parentheses as invalid
        while (!stack.isEmpty()) {
            invalid[stack.pop()] = true;
        }

        // Reconstruct string omitting invalid characters
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            if (!invalid[i]) {
                sb.append(s.charAt(i));
            }
        }

        return sb.toString();
    }
}
```

> **Quick Syntax:**
```java
// Cleanest Bracket Match Technique
if (c == '(') stack.push(')');
else if (c == '{') stack.push('}');
else if (c == '[') stack.push(']');
else if (stack.isEmpty() || stack.pop() != c) return false;
```

---

## 7. Concrete Problem Examples
* **LeetCode 20 - Valid Parentheses**: Basic bracket matching.
* **LeetCode 32 - Longest Valid Parentheses**: Sentinel index stack length calculation.
* **LeetCode 1249 - Minimum Remove to Make Valid Parentheses**: Filter invalid index markers.
* **LeetCode 22 - Generate Parentheses**: Backtracking bracket combinations.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Valid Parentheses, Longest Valid Parentheses, and Min Remove to Make Valid:

```java
public class ParenthesesProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Valid Parentheses (LeetCode 20) ===");
        System.out.println("Is \"()[]{}\" Valid? " + ParenthesesProblemsMaster.isValid("()[]{}")); // true
        System.out.println("Is \"([)]\" Valid?   " + ParenthesesProblemsMaster.isValid("([)]"));   // false

        System.out.println("\n=== 2. Longest Valid Parentheses (LeetCode 32) ===");
        String s2 = ")()())";
        int maxLen = ParenthesesProblemsMaster.longestValidParentheses(s2);
        System.out.println("Longest Valid Length: " + maxLen); // Output: 4 ("()()")

        System.out.println("\n=== 3. Minimum Remove to Make Valid (LeetCode 1249) ===");
        String s3 = "lee(t(c)o)de)";
        String cleaned = ParenthesesProblemsMaster.minRemoveToMakeValid(s3);
        System.out.println("Cleaned String: \"" + cleaned + "\""); // Output: "lee(t(c)o)de"
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Valid Parentheses (20)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Direct closing bracket stack push |
| **Longest Valid (32)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | `-1` sentinel index initialization |
| **Min Remove Valid (1249)**| **$O(N)$ Linear ⚡** | $O(N)$ Boolean Array| Mark invalid indices in stack |

---

## 10. Edge Cases & Boundary Handling
* **Odd Length String in LeetCode 20**: Returns `false` immediately.
* **String With All Opening Brackets (`"((((("`)**: `stack.isEmpty()` returns `false` at end.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `java.util.Stack` with Unchecked `pop()`**:
  - Calling `stack.pop()` when empty throws `EmptyStackException` crash.
  - **Always check `!stack.isEmpty()` before calling `pop()`**.
* **Forgetting `-1` Sentinel Initialization in LeetCode 32**:
  - Without `-1` sentinel, calculating length `i - stack.peek()` for valid substrings starting at index 0 fails.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The "Push Closing Bracket" Trick in LeetCode 20:
> When encountering an opening bracket `'('`, instead of pushing `'('` and doing map lookups on closing brackets, **push the EXPECTED closing bracket `')'` directly onto the stack**!
> When encountering a closing bracket, simply check if `stack.pop() == c`!
> This eliminates `HashMap` allocations and reduces code to 4 clean lines!

> **Memory Trick:** **"When you see an opening bracket, push its expected CLOSING bracket onto the stack!"**

---

## 13. System & Implementation Comparisons

| Feature | Push Expected Closing Bracket | HashMap Lookup Approach |
| :--- | :--- | :--- |
| **Code Length** | **4 Lines ⚡** | 15 Lines |
| **Auxiliary Memory** | **Zero Map Memory ⚡** | $O(1)$ Hash Map Storage |
| **Execution Speed** | **Fastest (Primitive Switches) ⚡**| Slower |

---

## 14. How to Recognize This in Questions
* **"Determine if bracket pairs are correctly nested and closed"** $\rightarrow$ Valid Parentheses (LeetCode 20).
* **"Find longest contiguous valid parentheses substring"** $\rightarrow$ Longest Valid Parentheses (LeetCode 32 - Index stack with `-1` sentinel).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does pushing `-1` onto the stack in LeetCode 32 enable $O(N)$ time complexity?**  
  *A:* The `-1` sentinel represents an imaginary invalid boundary before index 0. When a valid bracket pair matching at index `i` is popped, `i - stack.peek()` evaluates the exact length of all contiguous valid pairs extended back to the last invalid boundary.
* **Q: Can Longest Valid Parentheses (LeetCode 32) be solved in $O(1)$ space?**  
  *A:* Yes! Using 2 passes (Left-to-Right and Right-to-Left) with `left` and `right` bracket counters achieves $O(N)$ time and $O(1)$ constant space.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PARENTHESES PROBLEMS & INDEX STACK MECHANICS          |
+-----------------------------------------------------------------------+
| • Push Closing Trick (20): if (c == '(') stack.push(')')              |
| • Match Verification: if (stack.isEmpty() || stack.pop() != c) false  |
| • Longest Valid (32): Push -1 sentinel; validLen = i - stack.peek()   |
| • Boundary Reset (32): If stack empty after pop, push i as sentinel   |
| • Min Remove (1249): Mark unmatched '(' and ')' indices as invalid    |
| • Time Complexity: O(N) Linear Time | O(N) Space ⚡                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Valid Parentheses (LeetCode 20) in 4 lines using the closing push trick.
- [ ] I can solve Longest Valid Parentheses (LeetCode 32) using `-1` sentinel stack.
- [ ] I can solve Minimum Remove to Make Valid Parentheses (LeetCode 1249).
- [ ] I know why `-1` sentinel initialization is required in LeetCode 32.
- [ ] I know how to handle unmatched parentheses indices.
