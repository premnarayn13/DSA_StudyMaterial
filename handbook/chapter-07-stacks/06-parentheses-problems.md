# 06. Advanced Parentheses Matching & Validation

## 1. Introduction
Advanced parentheses and bracket string validation problems represent a dedicated category in technical coding interviews. Problems such as Minimum Add to Make Parentheses Valid (LeetCode 921), Minimum Remove to Make Valid Parentheses (LeetCode 1249), Longest Valid Parentheses (LeetCode 32), and Score of Parentheses (LeetCode 856) evaluate stack-based state tracking, index boundary matching, two-pass counting optimizations, and DP state transitions in **$O(N)$ linear time**.

> **Important:** For problems calculating **Longest Valid Parentheses**, initializing the stack with **`-1` as a dummy base index** allows instant calculation of valid substring length: **`length = i - stack.peek()`**!

## 2. Core Concepts
* **Minimum Add to Make Valid (LeetCode 921)**: Track `openCount` and `neededAdd`.
  * If `c == '('`: Increment `openCount++`.
  * If `c == ')'`: If `openCount > 0` decrement `openCount--`, else increment `neededAdd++`.
  * Result $= \text{openCount} + \text{neededAdd}$ in $O(N)$ time and **$O(1)$ space**!
* **Minimum Remove to Make Valid (LeetCode 1249)**: Use a Stack to store unmatched `'('` indices. Unmatched `')'` indices are marked immediately for deletion. Build result string using `StringBuilder`, skipping marked deletion indices.
* **Longest Valid Parentheses (LeetCode 32)**:
  * Initialize `stack.push(-1)`.
  * On `(`: Push index `i`.
  * On `)`: Pop stack. If stack becomes empty, push `i` as new base index! Else `maxLen = Math.max(maxLen, i - stack.peek())`.

> **Memory Trick:** **"Longest Valid Parentheses? Push -1 as base index! Length = i - stack.peek()"**.

## 3. Characteristics / Properties
* **Dummy Base Index `-1` Trick**: Pre-pushing `-1` onto the stack provides a valid left boundary anchor for valid substrings starting at index 0.

```
Parentheses Problems Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Variant     | Auxiliary Space   | Optimal Technique | Target Complexity |
+-----------------------+-------------------+-------------------+-------------------+
| Min Add to Make Valid | O(1) Constant ⚡  | 2 Counters        | O(N) Linear       |
| Min Remove to Valid   | O(N) Space        | Stack + Set/Bool  | O(N) Linear       |
| Longest Valid (32)    | O(N) Stack / O(1) | Stack w/ Base -1  | O(N) Linear       |
| Score of Parentheses  | O(1) Constant ⚡  | Bit Depth Shift   | O(N) Linear       |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Longest Valid Parentheses (LeetCode 32) on `") ( ( ) ( ) )"`:

```
Init: stack = [-1], maxLen = 0

i=0 ')': Pop -1. Stack empty -> Push 0 as new base index! | Stack: [0]
i=1 '(': Push 1 | Stack: [0, 1]
i=2 '(': Push 2 | Stack: [0, 1, 2]
i=3 ')': Pop 2. Stack top is 1 -> len = 3 - 1 = 2. maxLen = 2 | Stack: [0, 1]
i=4 '(': Push 4 | Stack: [0, 1, 4]
i=5 ')': Pop 4. Stack top is 1 -> len = 5 - 1 = 4. maxLen = 4 | Stack: [0, 1]
i=6 ')': Pop 1. Stack top is 0 -> len = 6 - 0 = 6. maxLen = 6 🎉 | Stack: [0]

Result: 6 ✅ (Substrings "((()))" is valid, len 6!)
```

## 5. Visual Diagram
Longest Valid Parentheses Base Index Mechanics:

```
Stack State: [ -1 (Base) ]

Read '(': Push index 0 -> Stack: [ -1, 0 ]
Read '(': Push index 1 -> Stack: [ -1, 0, 1 ]
Read ')': Pop 1        -> Stack top is 0 -> Valid Length = 2 - 0 = 2
Read ')': Pop 0        -> Stack top is -1 -> Valid Length = 3 - (-1) = 4
```

## 6. Operations / Algorithms
LeetCode 1249 & LeetCode 32 Master Implementation:

```java
// 1. Minimum Remove to Make Valid Parentheses (LeetCode 1249) O(N) Time, O(N) Space
public String minRemoveToMakeValid(String s) {
    Set<Integer> invalidIndices = new HashSet<>();
    Deque<Integer> stack = new ArrayDeque<>();

    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(') {
            stack.push(i);
        } else if (c == ')') {
            if (!stack.isEmpty()) {
                stack.pop(); // Matched valid pair!
            } else {
                invalidIndices.add(i); // Unmatched closing bracket
            }
        }
    }

    // Remaining indices in stack are unmatched opening brackets
    while (!stack.isEmpty()) {
        invalidIndices.add(stack.pop());
    }

    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < s.length(); i++) {
        if (!invalidIndices.contains(i)) {
            sb.append(s.charAt(i));
        }
    }

    return sb.toString();
}

// 2. Longest Valid Parentheses (LeetCode 32) O(N) Time, O(N) Space
public int longestValidParentheses(String s) {
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(-1); // Base boundary index
    int maxLen = 0;

    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') {
            stack.push(i);
        } else {
            stack.pop(); // Match with previous '(' or base index
            if (stack.isEmpty()) {
                stack.push(i); // Push new base boundary index
            } else {
                maxLen = Math.max(maxLen, i - stack.peek());
            }
        }
    }

    return maxLen;
}
```

> **Quick Syntax:**
```java
// Longest Valid Base Index Setup
Deque<Integer> stack = new ArrayDeque<>();
stack.push(-1); // Base index anchor
```

## 7. Examples
* **LeetCode 32 - Longest Valid Parentheses**: Stack base index `-1` method or 2-pass counter method.
* **LeetCode 1249 - Minimum Remove to Make Valid Parentheses**: Unmatched index set filtering.
* **LeetCode 921 - Minimum Add to Make Parentheses Valid**: $O(1)$ space counter approach.

## 8. Java Code
Complete interview-ready Java suite implementing Minimum Add, Minimum Remove, and Longest Valid Parentheses:

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;

public class AdvancedParenthesesMaster {

    // 1. Minimum Add to Make Valid (LeetCode 921) O(N) Time, O(1) Space
    public static int minAddToMakeValid(String s) {
        int openCount = 0;
        int neededAdd = 0;

        for (char c : s.toCharArray()) {
            if (c == '(') {
                openCount++;
            } else if (c == ')') {
                if (openCount > 0) {
                    openCount--;
                } else {
                    neededAdd++;
                }
            }
        }

        return openCount + neededAdd;
    }

    // 2. Longest Valid Parentheses (LeetCode 32) O(N) Time, O(N) Space
    public static int longestValidParentheses(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1);
        int maxLen = 0;

        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else {
                stack.pop();
                if (stack.isEmpty()) {
                    stack.push(i);
                } else {
                    maxLen = Math.max(maxLen, i - stack.peek());
                }
            }
        }

        return maxLen;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String s1 = "())";
        System.out.println("Min Add for '" + s1 + "': " + minAddToMakeValid(s1)); // Output: 1

        String s2 = ")()())";
        System.out.println("Longest Valid Parentheses for '" + s2 + "': " + longestValidParentheses(s2)); // Output: 4 ("()()")
    }
}
```

## 9. Complexity Analysis
| Problem | Time Complexity | Auxiliary Space | Key Technique |
| :--- | :--- | :--- | :--- |
| **Min Add to Make Valid** | **$O(N)$ Linear** | **$O(1)$ Constant ⚡** | Open / Needed Counters |
| **Min Remove to Make Valid**| **$O(N)$ Linear** | $O(N)$ Space | Index set filtering |
| **Longest Valid Parentheses** | **$O(N)$ Linear** | $O(N)$ Stack Space | Base Index `-1` Stacking |

## 10. Edge Cases
* **All Closing Brackets (`"))))"`)**: Stack pops `-1` and pushes new base indices continuously; `maxLen` remains `0`.
* **All Opening Brackets (`"(((("`)**: Stack grows; `maxLen` remains `0`.
* **Interleaved Letters (`"a)b(c)d"`)**: Min Remove skips non-bracket letters during index matching.

## 11. Common Mistakes
* Allocating an $O(N)$ Stack for Minimum Add when 2 simple integer counters solve it in **$O(1)$ auxiliary space**.
* Forgetting to pre-push `-1` onto the stack for Longest Valid Parentheses.
* In Minimum Remove, mutating String using `substring()` inside loops (causes $O(N^2)$ runtime!). Always use `StringBuilder`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** $O(1)$ Space Optimization for Minimum Add to Make Valid:
> Do NOT use a Stack! Maintain two counters:
> * `openCount`: Unmatched `'('` count.
> * `neededAdd`: Unmatched `')'` count.
> Total insertions needed $= \text{openCount} + \text{neededAdd}$ in **$O(N)$ time and $O(1)$ space**!

> **Memory Trick:** **"Min Add needs 2 counters (openCount & neededAdd) — NO STACK REQUIRED!"**

## 13. Comparisons
| Feature | Stack Approach (Min Add) | 2-Counter Approach (Min Add) |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ | $O(N)$ |
| **Auxiliary Space** | $O(N)$ Stack Memory | **$O(1)$ Constant Space ⚡** |
| **Code Length** | ~15 lines | ~8 lines |
| **Interview Score** | Good | **OPTIMAL & PREFERRED** |

## 14. How to Recognize This in Questions
* **"Find minimum insertions to make parentheses valid"** $\rightarrow$ 2 Counters ($O(1)$ space).
* **"Find length of longest valid parentheses substring"** $\rightarrow$ Stack with base `-1` anchor (LeetCode 32).
* **"Remove minimum invalid parentheses"** $\rightarrow$ Unmatched Index Filtering (LeetCode 1249).

## 15. Frequently Asked Interview Questions
* **Q: Why is `-1` pre-pushed onto the stack for Longest Valid Parentheses?**  
  *A:* Pre-pushing `-1` provides a dummy base index preceding position 0. When a valid substring starting at index 0 is matched (e.g. `"()"` at $i=1$), popping index 0 leaves `-1` at `stack.peek()`. The valid length is $1 - (-1) = 2$.
* **Q: How can Longest Valid Parentheses be solved in $O(1)$ space?**  
  *A:* Using two passes: (1) Left-to-right pass counting `left` and `right` parentheses, resetting when `right > left`. (2) Right-to-left pass counting `left` and `right`, resetting when `left > right`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED PARENTHESES PROBLEMS                         |
+-----------------------------------------------------------------------+
| • Min Add (O(1) Space): Track openCount & neededAdd; return open+needed|
| • Longest Valid (LeetCode 32): Pre-push stack.push(-1) base index     |
| • Longest Valid Length: len = i - stack.peek()                        |
| • Min Remove (LeetCode 1249): Push unmatched '(' indices; filter string|
| • Target Complexity: O(N) Linear Time across all variants             |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can solve Minimum Add to Make Valid in $O(1)$ auxiliary space.
- [ ] I know why `-1` is pre-pushed onto the stack in Longest Valid Parentheses.
- [ ] I can write the `len = i - stack.peek()` valid length formula.
- [ ] I can implement Minimum Remove to Make Valid Parentheses (LeetCode 1249).
- [ ] I know how to solve Longest Valid Parentheses in $O(1)$ space using 2 passes.
