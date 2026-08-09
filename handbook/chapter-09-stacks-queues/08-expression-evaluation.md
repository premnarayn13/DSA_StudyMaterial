# 08. Expression Evaluation, Postfix Shunting-Yard & Calculator Parsing Engines

## 1. Introduction
**Expression Evaluation and Parsing Engines** represent one of the most critical industrial applications of Stacks in compiler design, database query engines, and mathematical evaluation systems. By transforming Infix expressions (`A + B`) into Postfix / Reverse Polish Notation (`A B +`) via Dijkstra's **Shunting-Yard Algorithm**, or processing operator precedence dynamically using operand and operator stacks, problems like **Evaluate Reverse Polish Notation (LeetCode 150)**, **Basic Calculator (LeetCode 224)**, and **Basic Calculator II (LeetCode 227)** execute in **$O(N)$ linear time and $O(N)$ space**.

> **Important:** In **Reverse Polish Notation (RPN)**, operators follow their operands (`3 4 +`). Postfix evaluation NEVER requires parenthesis handling or operator precedence checking! Popping two operands on every operator and pushing the intermediate result evaluates any expression in a **SINGLE PASS**!

```
Infix vs Postfix (RPN) Expression Spectrum:
+-----------------------------------------------------------------------------------+
| Infix (Human Notation)   : (3 + 4) * 5  -> Requires Parentheses & Precedence Rules|
| Postfix / RPN Notation   : 3 4 + 5 *    -> ZERO Parentheses! Evaluated via Stack ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Postfix RPN Stack Mechanics (LeetCode 150)

### 2.1 Evaluate Reverse Polish Notation (LeetCode 150)
Given an array of string tokens representing an arithmetic expression in RPN, evaluate and return the integer result:
1. Maintain operand stack `Deque<Integer> stack = new ArrayDeque<>()`.
2. For each token in `tokens`:
   - If token is an operator (`"+"`, `"-"`, `"*"` , `"/"`):
     - Pop second operand: `b = stack.pop()`.
     - Pop first operand: `a = stack.pop()`.
     - Compute `result = evaluate(a, b, token)` and push `result` back onto stack!
   - Else (token is a number):
     - Push `Integer.parseInt(token)` onto stack.
3. Return `stack.pop()`.

```
RPN Evaluation Operand Order Invariant:
When popping operands for operator op:
b = stack.pop()  (Second Operand)
a = stack.pop()  (First Operand)
Result = a op b  (Note: Subtraction and Division are NON-COMMUTATIVE! Order matters: a / b, NOT b / a!) ⚡
```

### 2.2 Basic Calculator II (LeetCode 227 - Operator Precedence)
Evaluate an infix string `s` containing non-negative integers and operators `+`, `-`, `*`, `/`:
* **Single Stack Precedence Strategy**:
  1. Maintain `stack` storing numbers to be summed at the end.
  2. `currentNumber = 0`, `lastOperator = '+'`.
  3. Iterate characters in `s`:
     - If digit: `currentNumber = currentNumber * 10 + (c - '0')`.
     - If character is operator or last character in `s`:
       - If `lastOperator == '+'`: `stack.push(currentNumber)`.
       - If `lastOperator == '-'`: `stack.push(-currentNumber)`.
       - If `lastOperator == '*'`: `stack.push(stack.pop() * currentNumber)` (Immediate Evaluation!).
       - If `lastOperator == '/'`: `stack.push(stack.pop() / currentNumber)` (Immediate Evaluation!).
       - Update `lastOperator = c`, `currentNumber = 0`.
  4. Sum all elements in `stack` to get final result!

> **Memory Trick:** **"Basic Calculator II: Multiply and Divide evaluate IMMEDIATELY on stack.pop()! Add and Subtract push signed values!"**

---

## 3. Characteristics & Basic Calculator with Parentheses (LeetCode 224)

### 3.1 Basic Calculator (LeetCode 224 - Parentheses & Sign Stack)
Evaluate expression string `s` containing `+`, `-`, `(`, `)` and spaces:
1. Maintain `stack` storing `(result, sign)` context state across nested parentheses.
2. `result = 0`, `sign = 1`, `currentNumber = 0`.
3. For `i = 0` to $N - 1$:
   - `c = s.charAt(i)`.
   - If digit: `currentNumber = currentNumber * 10 + (c - '0')`.
   - If `c == '+'`: `result += sign * currentNumber; currentNumber = 0; sign = 1;`
   - If `c == '-'`: `result += sign * currentNumber; currentNumber = 0; sign = -1;`
   - If `c == '('`:
     - Save current context: `stack.push(result)`, `stack.push(sign)`.
     - Reset context: `result = 0`, `sign = 1`.
   - If `c == ')'`:
     - `result += sign * currentNumber; currentNumber = 0;`
     - `prevSign = stack.pop()`, `prevResult = stack.pop()`.
     - `result = prevResult + prevSign * result`.
4. Return `result + (sign * currentNumber)`.

---

## 4. Internal Working Mechanics
Tracing Evaluate RPN (LeetCode 150) on `tokens = ["2", "1", "+", "3", "*"]`:

```
token = "2": Push 2. stack = [2]
token = "1": Push 1. stack = [1, 2]
token = "+": Pop b = 1, Pop a = 2. Compute 2 + 1 = 3. Push 3. stack = [3]
token = "3": Push 3. stack = [3, 3]
token = "*": Pop b = 3, Pop a = 3. Compute 3 * 3 = 9. Push 9. stack = [9]

Final Expression Result = 9 ✅ (O(N) Time, O(N) Auxiliary Space!)
```

---

## 5. Visual Diagram
Shunting-Yard Infix to Postfix Operator Stack Routing Topography:

```
Infix Token Stream: 3  +  4  *  2
                    |  |  |  |  |
Output Queue      : 3     4  2     *  +
Operator Stack    :    +     * -> (Higher precedence '*' outputted before '+')
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Evaluate RPN (LeetCode 150), Basic Calculator II (LeetCode 227), and Basic Calculator (LeetCode 224):

```java
import java.util.*;

public class ExpressionEvaluationMaster {

    // 1. Evaluate Reverse Polish Notation (LeetCode 150) O(N) Time, O(N) Space
    public static int evalRPN(String[] tokens) {
        if (tokens == null || tokens.length == 0) return 0;

        Deque<Integer> stack = new ArrayDeque<>();
        for (String token : tokens) {
            if (token.equals("+")) {
                stack.push(stack.pop() + stack.pop());
            } else if (token.equals("-")) {
                int b = stack.pop();
                int a = stack.pop();
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

    // 2. Basic Calculator II (+, -, *, / without parentheses) (LeetCode 227) O(N) Time, O(N) Space
    public static int calculate2(String s) {
        if (s == null || s.length() == 0) return 0;

        Deque<Integer> stack = new ArrayDeque<>();
        int currentNumber = 0;
        char lastOperator = '+';
        int n = s.length();

        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);

            if (Character.isDigit(c)) {
                currentNumber = currentNumber * 10 + (c - '0');
            }

            if ((!Character.isDigit(c) && c != ' ') || i == n - 1) {
                if (lastOperator == '+') {
                    stack.push(currentNumber);
                } else if (lastOperator == '-') {
                    stack.push(-currentNumber);
                } else if (lastOperator == '*') {
                    stack.push(stack.pop() * currentNumber); // Immediate evaluation
                } else if (lastOperator == '/') {
                    stack.push(stack.pop() / currentNumber); // Immediate evaluation
                }

                lastOperator = c;
                currentNumber = 0;
            }
        }

        int result = 0;
        for (int val : stack) {
            result += val;
        }

        return result;
    }

    // 3. Basic Calculator (+, -, parentheses) (LeetCode 224) O(N) Time, O(N) Space
    public static int calculate1(String s) {
        if (s == null || s.length() == 0) return 0;

        Deque<Integer> stack = new ArrayDeque<>();
        int result = 0;
        int currentNumber = 0;
        int sign = 1;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);

            if (Character.isDigit(c)) {
                currentNumber = currentNumber * 10 + (c - '0');
            } else if (c == '+') {
                result += sign * currentNumber;
                currentNumber = 0;
                sign = 1;
            } else if (c == '-') {
                result += sign * currentNumber;
                currentNumber = 0;
                sign = -1;
            } else if (c == '(') {
                stack.push(result);
                stack.push(sign);
                result = 0;
                sign = 1;
            } else if (c == ')') {
                result += sign * currentNumber;
                currentNumber = 0;
                int prevSign = stack.pop();
                int prevResult = stack.pop();
                result = prevResult + prevSign * result;
            }
        }

        return result + (sign * currentNumber);
    }
}
```

> **Quick Syntax:**
```java
// Immediate Higher-Precedence Evaluation Syntax
if (lastOperator == '*') stack.push(stack.pop() * currentNumber);
if (lastOperator == '/') stack.push(stack.pop() / currentNumber);
```

---

## 7. Concrete Problem Examples
* **LeetCode 150 - Evaluate Reverse Polish Notation**: Postfix evaluation stack.
* **LeetCode 227 - Basic Calculator II**: Operator precedence stack.
* **LeetCode 224 - Basic Calculator**: Sign and result context stack for parentheses.
* **LeetCode 772 - Basic Calculator III**: Full calculator supporting `+`, `-`, `*`, `/` and parentheses.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Evaluate RPN, Basic Calculator II, and Basic Calculator:

```java
public class ExpressionEvaluationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Evaluate RPN (LeetCode 150) ===");
        String[] tokens = {"2", "1", "+", "3", "*"};
        int rpnRes = ExpressionEvaluationMaster.evalRPN(tokens);
        System.out.println("RPN Result: " + rpnRes); // Output: 9

        System.out.println("\n=== 2. Basic Calculator II (LeetCode 227) ===");
        String expr2 = "3+2*2";
        int calc2 = ExpressionEvaluationMaster.calculate2(expr2);
        System.out.println("Calculator II Result: " + calc2); // Output: 7

        System.out.println("\n=== 3. Basic Calculator I (LeetCode 224) ===");
        String expr1 = "(1+(4+5+2)-3)+(6+8)";
        int calc1 = ExpressionEvaluationMaster.calculate1(expr1);
        System.out.println("Calculator I Result: " + calc1); // Output: 23
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Evaluate RPN (150)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Single pass over token stream |
| **Calculator II (227)** | **$O(N)$ Linear ⚡** | $O(N)$ Stack Space | Immediate `*` and `/` evaluation |
| **Calculator I (224)** | **$O(N)$ Linear ⚡** | $O(N)$ Context Stack| Save `(result, sign)` on `(` |

---

## 10. Edge Cases & Boundary Handling
* **Non-Commutative Subtraction & Division**: `b = stack.pop()`, `a = stack.pop()`; result is `a - b` or `a / b` (NOT `b - a`).
* **Multi-Digit Numbers (`"123"`)**: Accumulated via `currentNumber = currentNumber * 10 + (c - '0')`.

---

## 11. Common Mistakes & Anti-Patterns
* **Reversing Operand Order During Subtraction / Division**:
  - Writing `stack.pop() - stack.pop()` evaluates `b - a` instead of `a - b`!
  - **Explicitly assign `int b = stack.pop()`, `int a = stack.pop()` and compute `a - b`**.
* **Forgetting Final Number Addition at End of Loop**:
  - In string calculators, the loop finishes while `currentNumber` contains the last parsed digits.
  - **Always execute `result + (sign * currentNumber)` at return time**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Postfix (RPN) is Preferred by Hardware Compilers:
> Infix notation (`(A + B) * C`) requires checking operator precedence and parsing nested parentheses.
> Postfix notation (`A B + C *`) processes operators sequentially in exact execution order using a single stack, eliminating precedence tables and recursive call overhead!

> **Memory Trick:** **"RPN operand order: b = pop(), a = pop(), calculate a op b!"**

---

## 13. System & Implementation Comparisons

| Feature | Single Stack Infix Parser | Postfix (RPN) Parser |
| :--- | :--- | :--- |
| **Parentheses Support** | Requires Sign Context Stack | **Zero Parentheses Needed ⚡** |
| **Precedence Handling** | Delayed Stack Evaluation | **Immediate Sequential Execution ⚡**|
| **Code Footprint** | ~35 Lines | ~20 Lines |

---

## 14. How to Recognize This in Questions
* **"Evaluate mathematical expression in Reverse Polish Notation"** $\rightarrow$ LeetCode 150 (Postfix Stack).
* **"Evaluate string containing +, -, *, / with precedence"** $\rightarrow$ LeetCode 227 (Immediate `*` and `/` stack evaluation).

---

## 15. Frequently Asked Interview Questions
* **Q: How does Basic Calculator II (LeetCode 227) solve `*` and `/` operator precedence without two stacks?**  
  *A:* By evaluating `*` and `/` IMMEDIATELY against the top element of the stack (`stack.push(stack.pop() * currentNumber)`), higher-precedence operations are collapsed before lower-precedence `+` and `-` values are summed at the end.
* **Q: What does Dijkstra's Shunting-Yard Algorithm accomplish?**  
  *A:* Shunting-Yard parses infix math expressions into postfix (RPN) token sequences using an operator stack and output queue.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: EXPRESSION EVALUATION & CALCULATOR ENGINES             |
+-----------------------------------------------------------------------+
| • RPN Operand Order: b = stack.pop(); a = stack.pop(); push(a op b)   |
| • Non-Commutative Rule: Compute a - b and a / b (b is second pop!)    |
| • Calculator II (227): Immediate evaluation for * and / on stack top  |
| • Calculator I (224): Push (result, sign) onto stack on '('           |
| • Digit Accumulation: currentNumber = currentNumber * 10 + (c - '0')  |
| • Time Complexity: O(N) Linear Time | O(N) Space ⚡                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Evaluate Reverse Polish Notation (LeetCode 150).
- [ ] I know why operand pop order matters for subtraction and division.
- [ ] I can write Basic Calculator II (LeetCode 227) with operator precedence.
- [ ] I can write Basic Calculator (LeetCode 224) supporting parentheses.
- [ ] I can explain Dijkstra's Shunting-Yard Algorithm.
