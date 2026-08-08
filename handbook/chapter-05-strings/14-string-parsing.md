# 14. String Parsing, Tokenization & Expression Evaluation

## 1. Introduction
String parsing involves extracting structured values, tokenizing character streams, and evaluating mathematical expressions from unformatted string inputs. In technical coding interviews, problems such as Basic Calculator (LeetCode 224 / 227 / 772), Decode String (LeetCode 394), and String Compression (LeetCode 443) test a candidate's mastery of **Stack-based Parsing**, Operator Precedence (Shunting-Yard Algorithm), and Character Stream Tokenization.

> **Important:** String expression parsing problems require managing 4 core elements: **Current Number (`num`)**, **Current Sign (`sign`)**, **Operation Stack**, and **Parentheses Frames**.

## 2. Core Concepts
* **Digit Accumulation Pattern**: Converting digit characters to integer values during stream parsing:
  $$\text{num} = \text{num} \cdot 10 + (\text{ch} - \text{'0'})$$
* **Stack-Based Expression Evaluation**: Pushing numbers and signs onto stacks to handle operator precedence (`*`, `/` evaluated before `+`, `-`) and nested parentheses `(...)`.
* **String Expansion / Decoding (LeetCode 394)**: Using two stacks—one for repeat counts `countStack` and one for string prefixes `stringStack`—to process nested bracket expansions like `"3[a2[c]]"`.
* **Run-Length String Compression**: Overwriting duplicate adjacent characters in-place using Write Pointers and converting frequencies to character digits.

> **Memory Trick:** **"Accumulate digit via num = num * 10 + (ch - '0'). Push to stack on operator or closing bracket!"**

## 3. Characteristics / Properties
* **Operator Precedence Handling**:
  * For `+` and `-`: Perform operation or push signed number `+num` or `-num` onto Stack.
  * For `*` and `/`: Immediately pop top element, apply operation with `num`, and push result back onto Stack!
* **Parentheses Resets**: Encountering `(` pushes current state onto Stack and resets `num = 0, sign = '+'`. Encountering `)` evaluates inner sub-expression.

```
Parsing Pattern Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Parsing Category      | Core Data Struct  | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| Basic Calculator II   | Single ArrayDeque | O(N) Linear       | O(N) Stack        |
| Decode String (3[a2[c]])| Dual Stacks     | O(N * MaxRepeat)  | O(N) Stack        |
| String Compression    | Write Pointer     | O(N) Linear       | O(1) Constant ⚡   |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Basic Calculator II (`"3 + 2 * 2"`) using Operator Stack:

```
Initialization: stack = [], num = 0, sign = '+'

Char '3': num = 3
Char '+': Apply sign '+' to num 3 -> stack.push(3), reset num = 0, sign = '+'
Char '2': num = 2
Char '*': Apply sign '+' to num 2 -> stack.push(2), reset num = 0, sign = '*'
Char '2': num = 2
End of string: Apply sign '*' to num 2 -> pop 2, calculate 2 * 2 = 4 -> stack.push(4)

Final Stack Contents: [3, 4]
Sum elements in Stack: 3 + 4 = 7 ✅ (Correct!)
```

## 5. Visual Diagram
Nested Bracket Stack Frame Pushing (`3[a2[c]]`):

```
Read "3[":   countStack = [3],   stringStack = [""]
Read "a":    currentString = "a"
Read "2[":   countStack = [3, 2], stringStack = ["", "a"], currentString = ""
Read "c":    currentString = "c"
Read "]":    pop count=2, prev="a" -> currentString = "a" + "c"*2 = "acc"
Read "]":    pop count=3, prev=""  -> currentString = "" + "acc"*3 = "accaccacc" ✅
```

## 6. Operations / Algorithms
LeetCode 227 Basic Calculator II Implementation:

```java
public int calculate(String s) {
    if (s == null || s.length() == 0) return 0;

    Deque<Integer> stack = new ArrayDeque<>();
    int num = 0;
    char sign = '+';
    int n = s.length();

    for (int i = 0; i < n; i++) {
        char c = s.charAt(i);

        if (Character.isDigit(c)) {
            num = num * 10 + (c - '0');
        }

        // If char is operator OR end of string (ignore spaces)
        if ((!Character.isDigit(c) && c != ' ') || i == n - 1) {
            if (sign == '+') {
                stack.push(num);
            } else if (sign == '-') {
                stack.push(-num);
            } else if (sign == '*') {
                stack.push(stack.pop() * num);
            } else if (sign == '/') {
                stack.push(stack.pop() / num);
            }
            sign = c;
            num = 0;
        }
    }

    int result = 0;
    for (int val : stack) {
        result += val;
    }
    return result;
}
```

> **Quick Syntax:**
```java
// String Digit Accumulation Idiom
if (Character.isDigit(c)) {
    num = num * 10 + (c - '0');
}
```

## 7. Examples
* **LeetCode 227 - Basic Calculator II**: Evaluating expressions with `+`, `-`, `*`, `/`.
* **LeetCode 394 - Decode String**: Expanding nested bracket strings like `"3[a2[c]]"`.
* **LeetCode 443 - String Compression**: In-place run-length encoding.

## 8. Java Code
Complete interview-ready Java suite implementing Basic Calculator II, Decode String, and In-Place String Compression:

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class StringParsingMaster {

    // 1. Basic Calculator II (LeetCode 227) O(N) Time, O(N) Space
    public static int calculate(String s) {
        if (s == null || s.isEmpty()) return 0;

        Deque<Integer> stack = new ArrayDeque<>();
        int num = 0;
        char sign = '+';
        int n = s.length();

        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);

            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            }

            if ((!Character.isDigit(c) && c != ' ') || i == n - 1) {
                if (sign == '+') stack.push(num);
                else if (sign == '-') stack.push(-num);
                else if (sign == '*') stack.push(stack.pop() * num);
                else if (sign == '/') stack.push(stack.pop() / num);

                sign = c;
                num = 0;
            }
        }

        int result = 0;
        while (!stack.isEmpty()) {
            result += stack.pop();
        }
        return result;
    }

    // 2. Decode String (LeetCode 394) O(N * MaxK) Time, O(N) Space
    public static String decodeString(String s) {
        Deque<Integer> countStack = new ArrayDeque<>();
        Deque<StringBuilder> stringStack = new ArrayDeque<>();
        StringBuilder currString = new StringBuilder();
        int k = 0;

        for (char ch : s.toCharArray()) {
            if (Character.isDigit(ch)) {
                k = k * 10 + (ch - '0');
            } else if (ch == '[') {
                countStack.push(k);
                stringStack.push(currString);
                currString = new StringBuilder();
                k = 0;
            } else if (ch == ']') {
                StringBuilder decodedString = stringStack.pop();
                int count = countStack.pop();
                for (int i = 0; i < count; i++) {
                    decodedString.append(currString);
                }
                currString = decodedString;
            } else {
                currString.append(ch);
            }
        }

        return currString.toString();
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Calculator
        String expr = "3 + 2 * 2";
        System.out.println("Evaluate '" + expr + "': " + calculate(expr)); // Output: 7

        // Test Decode String
        String encoded = "3[a2[c]]";
        System.out.println("Decode '" + encoded + "': " + decodeString(encoded)); // Output: accaccacc
    }
}
```

## 9. Complexity Analysis
| Algorithm / Pattern | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Basic Calculator II** | **$O(N)$ Linear** | $O(N)$ Stack | Evaluates `*` and `/` immediately |
| **Decode String** | $O(N \cdot \text{maxK})$ | $O(N)$ Stack | Dual stacks for count & string frames |
| **String Compression** | **$O(N)$ Linear** | **$O(1)$ Constant** | Write pointer in-place overwrite |

## 10. Edge Cases
* **Leading / Trailing Spaces in Expression**: Guard checking `c != ' '` skips whitespace cleanly.
* **Multi-Digit Numbers**: Multi-digit parsing `num = num * 10 + (c - '0')` handles numbers like `123`.
* **Single Digit Output in Compression**: Frequencies of 1 (e.g., `"a"`) should NOT append `'1'` (write char `'a'`, skip digit count).

## 11. Common Mistakes
* Evaluating `+` and `-` immediately without storing them on Stack (violates operator precedence for `*` and `/`!).
* Using `java.util.Stack` (synchronized, legacy) instead of **`java.util.ArrayDeque`** (fast, unsynchronized).
* Forgetting to process the last number when `i == n - 1` is reached.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Always use `ArrayDeque` instead of `Stack` in Java parsing code:
> `Deque<Integer> stack = new ArrayDeque<>();`
> * `stack.push(val)` $\implies$ Pushes onto top.
> * `stack.pop()` $\implies$ Pops from top.

> **Memory Trick:** **"Multiply & Divide immediately on stack; Add & Subtract at the end!"**

## 13. Comparisons
| Metric | `java.util.Stack` (Legacy) | `java.util.ArrayDeque` (Modern) |
| :--- | :--- | :--- |
| **Thread Safety** | Synchronized (Lock overhead) | Unsynchronized (Fast!) |
| **Data Structure** | Extends `Vector` | Resizable Array Buffer |
| **Interview Recommendation** | AVOID | **MANDATORY PREFERRED** |

## 14. How to Recognize This in Questions
* **"Evaluate string arithmetic expression with +, -, *, /"** $\rightarrow$ Stack-Based Parsing ($O(N)$ time).
* **"Decode nested bracket string like 3[a2[c]]"** $\rightarrow$ Dual Stack Parsing.

## 15. Frequently Asked Interview Questions
* **Q: How does Basic Calculator handle operator precedence using a single Stack?**  
  *A:* When encountering `*` or `/`, the top element is popped from the stack immediately, multiplied or divided by `num`, and the result is pushed back onto the stack. When all characters are processed, the stack contains only numbers that need to be added together!
* **Q: Why is `ArrayDeque` preferred over `Stack` in Java?**  
  *A:* `java.util.Stack` inherits from `Vector` and synchronizes all operations, introducing locking overhead. `ArrayDeque` is unsynchronized, faster, and consumes less memory per node.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING PARSING & EXPRESSION EVALUATION                |
+-----------------------------------------------------------------------+
| • Digit Accumulation: num = num * 10 + (c - '0')                      |
| • Calculator Rule: Push +num / -num to stack; Pop & compute for *, /  |
| • End Trigger: Process current num when (!isDigit && c!=' ') || i==N-1|
| • Decode String: Use countStack & stringStack for nested brackets     |
| • Always use Deque<Integer> stack = new ArrayDeque<>()                |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the digit accumulation loop `num = num * 10 + (c - '0')`.
- [ ] I can implement Basic Calculator II using `ArrayDeque`.
- [ ] I can implement Decode String (LeetCode 394) using dual stacks.
- [ ] I know why `ArrayDeque` is preferred over legacy `Stack`.
- [ ] I know how to process operator precedence (`*` and `/` vs `+` and `-`).
