# 03. Expression Evaluation & Shunting-Yard Algorithm

## 1. Introduction
Evaluating mathematical expressions represented as strings is a high-frequency topic in technical coding interviews. Problems such as Evaluate Reverse Polish Notation (LeetCode 150 - Postfix evaluation), Basic Calculator (LeetCode 224 - with parentheses), and Basic Calculator II (LeetCode 227 - with precedence `*` and `/`) require converting between **Infix** ($A + B$), **Prefix** ($+ A B$), and **Postfix** ($A B +$) notations using **Dijkstra's Shunting-Yard Algorithm** and stack-based operand processing in **$O(N)$ linear time**.

> **Important:** In Infix notation (`3 + 2 * 2`), operators are placed between operands, requiring operator precedence rules. In Postfix / Reverse Polish Notation (`3 2 2 * +`), operator precedence is **built directly into token order**, eliminating parentheses and operator precedence ambiguity during stack evaluation!

## 2. Core Concepts
* **Expression Notations**:
  * **Infix**: Human readable (`(A + B) * C`). Requires precedence rules and parentheses handling.
  * **Postfix (Reverse Polish Notation - RPN)**: Machine optimal (`A B + C *`). Operands appear first, followed by operators.
  * **Prefix (Polish Notation)**: (`* + A B C`). Operators precede operands.
* **Postfix Evaluation Algorithm**: Iterate through tokens. If token is a number, push to stack. If token is an operator, pop top 2 operands (`b = pop(), a = pop()`), perform `a op b`, and push result back to stack!
* **Dijkstra's Shunting-Yard Algorithm**: Converts Infix string expressions to Postfix tokens using an operator stack and precedence weights (`*` & `/` precedence 2, `+` & `-` precedence 1).

> **Memory Trick for RPN:** **"Operand -> Push to stack; Operator -> Pop b, Pop a, compute (a op b), Push result!"**

## 3. Characteristics / Properties
* **Operand Order Precedence in Division/Subtraction**: When popping two operands for `-` or `/`, the FIRST popped element is $B$ (right operand) and the SECOND popped element is $A$ (left operand). The operation MUST be evaluated as **`A - B`** or **`A / B`**!

```
Expression Notation Conversion & Evaluation Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Notation              | Stack Structure   | Time Complexity   | Key Advantage     |
+-----------------------+-------------------+-------------------+-------------------+
| Reverse Polish (RPN)  | Operand Stack     | O(N) Linear ⚡   | Zero Parentheses  |
| Basic Calculator II   | Operand Stack     | O(N) Linear ⚡   | Priority *, / Ops |
| Infix -> Postfix      | Operator Stack    | O(N) Linear ⚡   | Shunting-Yard     |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Evaluate Reverse Polish Notation (LeetCode 150) on `["2", "1", "+", "3", "*"]`:

```
Read "2": Operand -> stack.push(2)     | Stack: [2]
Read "1": Operand -> stack.push(1)     | Stack: [2, 1]
Read "+": Operator -> b=1, a=2         | Compute 2 + 1 = 3 -> stack.push(3) | Stack: [3]
Read "3": Operand -> stack.push(3)     | Stack: [3, 3]
Read "*": Operator -> b=3, a=3         | Compute 3 * 3 = 9 -> stack.push(9) | Stack: [9]

End of tokens. Pop final answer = 9 ✅
```

## 5. Visual Diagram
Dijkstra's Shunting-Yard Infix to Postfix Train Yard Analogy:

```
Infix Input: 3 + 4 * 2 / ( 1 - 5 )

         [ Train Tracks ]
Input Tokens ---------------> Output Postfix Queue (3 4 2 * 1 5 - / +)
                                   ^
                                   | Push/Pop based on Precedence
                             [ Operator Stack ] (+ * /)
```

## 6. Operations / Algorithms
LeetCode 150 & LeetCode 227 Master Implementation:

```java
// 1. Evaluate Reverse Polish Notation (LeetCode 150) O(N) Time, O(N) Space
public int evalRPN(String[] tokens) {
    Deque<Integer> stack = new ArrayDeque<>();

    for (String token : tokens) {
        if (token.equals("+")) {
            stack.push(stack.pop() + stack.pop());
        } else if (token.equals("-")) {
            int b = stack.pop(); // Right operand first!
            int a = stack.pop(); // Left operand second!
            stack.push(a - b);
        } else if (token.equals("*")) {
            stack.push(stack.pop() * stack.pop());
        } else if (token.equals("/")) {
            int b = stack.pop();
            int a = stack.pop();
            stack.push(a / b);
        } else {
            stack.push(Integer.parseInt(token));
        }
    }

    return stack.pop();
}
```

> **Quick Syntax:**
```java
// Operand Pop Order for Non-Commutative Ops (-, /)
int b = stack.pop(); // Right operand
int a = stack.pop(); // Left operand
stack.push(a / b);   // Left / Right
```

## 7. Examples
* **LeetCode 150 - Evaluate Reverse Polish Notation**: Postfix evaluation using single operand stack.
* **LeetCode 227 - Basic Calculator II**: Infix evaluation with `+`, `-`, `*`, `/` operator precedence.
* **LeetCode 224 - Basic Calculator**: Infix evaluation with parentheses `(` and `)` handling.

## 8. Java Code
Complete interview-ready Java suite implementing Evaluate RPN (LeetCode 150) and Infix Expression Evaluation with Parentheses (LeetCode 224):

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class ExpressionEvaluationMaster {

    // 1. Evaluate Reverse Polish Notation (LeetCode 150) O(N) Time, O(N) Space
    public static int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();

        for (String token : tokens) {
            switch (token) {
                case "+":
                    stack.push(stack.pop() + stack.pop());
                    break;
                case "-": {
                    int b = stack.pop(), a = stack.pop();
                    stack.push(a - b);
                    break;
                }
                case "*":
                    stack.push(stack.pop() * stack.pop());
                    break;
                case "/": {
                    int b = stack.pop(), a = stack.pop();
                    stack.push(a / b);
                    break;
                }
                default:
                    stack.push(Integer.parseInt(token));
                    break;
            }
        }

        return stack.pop();
    }

    // 2. Basic Calculator with Parentheses (LeetCode 224) O(N) Time, O(N) Space
    public static int calculateWithParentheses(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        int res = 0;
        int num = 0;
        int sign = 1; // 1 for +, -1 for -

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);

            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '+') {
                res += sign * num;
                num = 0;
                sign = 1;
            } else if (c == '-') {
                res += sign * num;
                num = 0;
                sign = -1;
            } else if (c == '(') {
                // Save current result and sign frame onto stack
                stack.push(res);
                stack.push(sign);
                res = 0;
                sign = 1;
            } else if (c == ')') {
                res += sign * num;
                num = 0;
                res *= stack.pop(); // Pop saved sign
                res += stack.pop(); // Pop saved result before bracket
            }
        }

        return res + (sign * num);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String[] rpn = {"4", "13", "5", "/", "+"}; // 4 + (13 / 5) = 6
        System.out.println("Eval RPN: " + evalRPN(rpn)); // Output: 6

        String expr = "(1+(4+5+2)-3)+(6+8)";
        System.out.println("Eval Expression with Parentheses: " + calculateWithParentheses(expr)); // Output: 23
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Triggers |
| :--- | :--- | :--- | :--- |
| **Evaluate RPN (Postfix)** | **$O(N)$ Linear** | $O(N)$ Operand Stack | Machine optimal token scanning |
| **Basic Calculator II** | **$O(N)$ Linear** | $O(N)$ Stack | Evaluates `*` and `/` immediately |
| **Shunting-Yard (Infix $\to$ Postfix)**| **$O(N)$ Linear** | $O(N)$ Operator Stack | Standard compiler parser pass |

## 10. Edge Cases
* **Subtraction and Division Operand Order**: Reversing operand order (`b - a` instead of `a - b`) produces wrong answers! First pop is $B$, second pop is $A$.
* **Negative Numbers in Strings**: Multi-digit and negative numbers handling in string tokens.
* **Nested Parentheses `((1 + 2))`**: Bracket stack frame pushing saves previous result and sign seamlessly.

## 11. Common Mistakes
* Evaluating non-commutative operations as `stack.pop() - stack.pop()` (evaluates `b - a` instead of `a - b`!).
* Using `==` string equality for token strings (`token == "+"` fails in Java!). Always use **`token.equals("+")`** or `switch (token)`.
* Forgetting to flush remaining `sign * num` at the end of string expression parsing loops.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Operator Stack Order Rule for Subtraction and Division:
> When popping operands for `-` or `/`:
> **`int b = stack.pop();`** (Right operand)
> **`int a = stack.pop();`** (Left operand)
> Compute: **`a - b`** or **`a / b`**!

> **Memory Trick:** **"b = pop() FIRST, a = pop() SECOND! Result is (a - b) or (a / b)"**.

## 13. Comparisons
| Feature | Infix Notation | Postfix Notation (RPN) |
| :--- | :--- | :--- |
| **Syntax** | `(A + B) * C` | `A B + C *` |
| **Parentheses Required**| YES | **NO (Zero Parentheses Required)** |
| **Parsing Complexity** | Complex (Operator Precedence) | **Simple Linear Stack Scan** |
| **Machine Execution** | Requires conversion first | **Native Stack Machine Execution** |

## 14. How to Recognize This in Questions
* **"Evaluate expression in Reverse Polish Notation"** $\rightarrow$ Stack Postfix Evaluation (LeetCode 150).
* **"Evaluate string math expression with +, -, *, /, (, )"** $\rightarrow$ Basic Calculator with Stack (LeetCode 224 / 227).

## 15. Frequently Asked Interview Questions
* **Q: Why is Reverse Polish Notation (RPN) preferred for computer calculation?**  
  *A:* RPN eliminates the need for parentheses and operator precedence parsing. Tokens can be processed strictly left-to-right using a single operand stack, executing in $O(N)$ linear time with zero backtrack.
* **Q: How does Shunting-Yard algorithm handle operator precedence?**  
  *A:* Shunting-Yard assigns precedence weights to operators (e.g. `*`=2, `+`=1). When reading a new operator, any operators on the stack with $\ge$ precedence are popped to output first, ensuring higher-precedence operations appear earlier in the Postfix stream.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: EXPRESSION EVALUATION & SHUNTING-YARD                 |
+-----------------------------------------------------------------------+
| • Postfix Evaluation: Number -> Push; Operator -> Pop b, Pop a, Push (a op b)|
| • Non-Commutative Rule: b = stack.pop() FIRST, a = stack.pop() SECOND!|
| • Subtraction/Division: Compute (a - b) and (a / b)                   |
| • String Comparison: Use token.equals("+") or switch(token)           |
| • Parentheses Frame Push: Push previous (res, sign) on '('             |
| • Complexity: O(N) Linear Time | O(N) Auxiliary Stack Space           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can evaluate Postfix / RPN tokens using an operand stack.
- [ ] I know why `b = pop()` is right operand and `a = pop()` is left operand.
- [ ] I can handle operator precedence (`*` and `/` vs `+` and `-`).
- [ ] I can write Basic Calculator with parentheses (LeetCode 224).
- [ ] I know why `token.equals()` is required over `==` in Java.
