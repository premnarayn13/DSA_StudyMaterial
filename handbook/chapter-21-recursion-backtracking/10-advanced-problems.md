# 10. Advanced Backtracking Problems: Expression Evaluation & $K$-Partitioning

## 1. Introduction
**Advanced Backtracking Problems** push constraint satisfaction algorithms into complex expression evaluation, precedence tracking, and multi-set equal partitioning. Hard-level problems like **Expression Add Operators (LeetCode 282)** and **Matchsticks to Square (LeetCode 473)** require tracking running evaluation totals alongside previous operand values (`prevOperand`) to respect mathematical multiplication precedence ($+$, $-$, $*$) in **$O(4^N)$ Time** and **$O(N)$ Space**.

> **Important:** Core Invariants of Expression Add Operators (LeetCode 282):
> 1. **Multiplication Precedence Tracking (`prevOperand`)**:
>    - Addition $+ val$: `eval + val`, `prevOperand = val`.
>    - Subtraction $- val$: `eval - val`, `prevOperand = -val`.
>    - Multiplication $* val$: Undo previous operation and apply multiplication:
>      $$\text{newEval} = (\text{eval} - \text{prevOperand}) + (\text{prevOperand} \cdot val)$$
>      $$\text{newPrevOperand} = \text{prevOperand} \cdot val$$
> 2. **Leading Zero Invariant**:
>    - If current substring starts with `'0'` (e.g., `"05"`), ONLY process single digit `'0'` and `break` loop immediately to prevent invalid multi-digit leading zero numbers! ⚡

```
Expression Add Operators Multiplication Precedence Topology (Target = 6, String "123"):
Path "1+2*3":
- After "1+2": eval = 3, prevOperand = +2.
- Process "*3": Undo prev (+2): (3 - 2) + (2 * 3) = 1 + 6 = 7! (Evaluates 1 + (2 * 3) correctly!). ⚡
```

---

## 2. Core Concepts & LeetCode 282 vs 473 Strategy Matrix

### 2.1 Advanced Backtracking Strategy Matrix
```
Advanced Backtracking Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | State Tracking    | Time Complexity   | Primary Target    |
+-----------------------+-------------------+-------------------+-------------------+
| **Add Operators (282)**| `(eval, prev)`    | **$O(4^N)$ Time ⚡**| Target Value Math |
| **Matchsticks (473)** | `sides[4]` Array  | **$O(4^N)$ Time ⚡**| 4 Equal Perimeter |
| **Phone Combo (17)**  | Mapping Array     | **$O(4^N)$ Time ⚡**| Keypad Combinations|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 282 Multiplication: (eval - prev) + (prev * val)! Prune leading zeros if (i > start && num[start] == '0')!"**

---

## 3. Characteristics & $O(4^N)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(4^N)$ Complexity
* For a string of length $N$, there are $N - 1$ slot positions between digits.
* In LeetCode 282, each slot has 4 options: NO operator (concat), $+$, $-$, $*$.
* Total branching factor: $4^{N-1}$.
* Total Time Complexity: $\mathbf{O(4^N) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 282 on `num = "123"`, `target = 6`:

```
Call backtrack(start = 0, eval = 0, prev = 0):
- Substring "1":
  - First num: eval = 1, prev = 1, path = "1".
  - Recurse start = 1:
    - Substring "2":
      - Try '+': eval = 1 + 2 = 3, prev = 2, path = "1+2".
        - Recurse start = 2:
          - Substring "3":
            - Try '*': eval = (3 - 2) + (2 * 3) = 1 + 6 = 7 != 6.
            - Try '+': eval = 3 + 3 = 6 == target! Match "1+2+3"!
            - Try '*': eval = (3 - 2) + (2 * 3) = 7 != 6.
      - Try '*': eval = (1 - 1) + (1 * 2) = 2, prev = 2, path = "1*2".
        - Recurse start = 2:
          - Substring "3":
            - Try '*': eval = (2 - 2) + (2 * 3) = 6 == target! Match "1*2*3"!

Total Matches Found: ["1+2+3", "1*2*3"]! ✅ (O(4^N) Time!)
```

---

## 5. Visual Diagram
Expression Multiplication Undo Topography:

```
State before *: eval = 3, prev = +2, current value = 3
Apply *:        (3 - 2) + (2 * 3) = 1 + 6 = 7!  (Correctly evaluates 1 + (2 * 3) = 7) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 282 (Expression Add Operators) and LeetCode 473 (Matchsticks to Square):

```java
import java.util.*;

// LeetCode 282 & 473: Advanced Backtracking Master Class
public class AdvancedBacktrackingMaster {

    // 1. LeetCode 282: Expression Add Operators O(4^N) Time
    public List<String> addOperators(String num, int target) {
        List<String> result = new ArrayList<>();
        if (num == null || num.length() == 0) return result;

        backtrackOperators(num, target, 0, 0, 0, new StringBuilder(), result);
        return result;
    }

    private void backtrackOperators(String num, int target, int start, 
                                   long eval, long prevOperand, 
                                   StringBuilder path, List<String> result) {
        // Base Case: Processed all digits in string!
        if (start == num.length()) {
            if (eval == target) {
                result.add(path.toString()); // Target expression found!
            }
            return;
        }

        for (int i = start; i < num.length(); i++) {
            // Leading Zero Guard: "05" is invalid, but single "0" is valid
            if (i > start && num.charAt(start) == '0') {
                break;
            }

            String currentStr = num.substring(start, i + 1);
            long val = Long.parseLong(currentStr);
            int len = path.length();

            if (start == 0) {
                // First operand in expression (No operator prefix)
                path.append(currentStr);
                backtrackOperators(num, target, i + 1, val, val, path, result);
                path.setLength(len); // Backtrack
            } else {
                // Option 1: Addition '+'
                path.append('+').append(currentStr);
                backtrackOperators(num, target, i + 1, eval + val, val, path, result);
                path.setLength(len);

                // Option 2: Subtraction '-'
                path.append('-').append(currentStr);
                backtrackOperators(num, target, i + 1, eval - val, -val, path, result);
                path.setLength(len);

                // Option 3: Multiplication '*' (Precedence Undo Step!)
                path.append('*').append(currentStr);
                long newEval = (eval - prevOperand) + (prevOperand * val);
                long newPrev = prevOperand * val;
                backtrackOperators(num, target, i + 1, newEval, newPrev, path, result);
                path.setLength(len);
            }
        }
    }

    // 2. LeetCode 473: Matchsticks to Square O(4^N) Time
    public boolean makesquare(int[] matchsticks) {
        if (matchsticks == null || matchsticks.length < 4) return false;

        long sum = 0;
        for (int m : matchsticks) sum += m;
        if (sum % 4 != 0) return false; // Total perimeter must be divisible by 4!

        int targetSide = (int) (sum / 4);

        // Sort descending to fail fast during backtracking!
        Arrays.sort(matchsticks);
        int[] reversed = new int[matchsticks.length];
        for (int i = 0; i < matchsticks.length; i++) {
            reversed[i] = matchsticks[matchsticks.length - 1 - i];
        }

        int[] sides = new int[4];
        return backtrackSquare(reversed, 0, sides, targetSide);
    }

    private boolean backtrackSquare(int[] matchsticks, int index, int[] sides, int target) {
        if (index == matchsticks.length) {
            return sides[0] == target && sides[1] == target && 
                   sides[2] == target && sides[3] == target;
        }

        int currLength = matchsticks[index];

        for (int i = 0; i < 4; i++) {
            if (sides[i] + currLength <= target) {
                sides[i] += currLength;

                if (backtrackSquare(matchsticks, index + 1, sides, target)) {
                    return true;
                }

                sides[i] -= currLength; // Backtrack
            }

            // Pruning Guard: If side is 0, subsequent empty sides will yield identical subtrees
            if (sides[i] == 0) break;
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Multiplication Undo Line (LeetCode 282)
long newEval = (eval - prevOperand) + (prevOperand * val);
```

---

## 7. Concrete Problem Examples
* **LeetCode 282 - Expression Add Operators**: Target value precedence math.
* **LeetCode 473 - Matchsticks to Square**: $K$-partition equal sum.
* **LeetCode 17 - Letter Combinations of a Phone Number**: Keypad combinations.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 282 `addOperators`:

```java
public class AdvancedBacktrackingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 282 Expression Add Operators Test ===");
        AdvancedBacktrackingMaster solver = new AdvancedBacktrackingMaster();

        String num = "123";
        int target = 6;

        List<String> expressions = solver.addOperators(num, target);
        System.out.println("Expressions evaluating to 6: " + expressions);
        // Output: ["1+2+3", "1*2*3"] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Add Operators (282)** | **$O(4^N)$ Exponential ⚡**| **$O(N)$ Call Stack Memory**| Precedence undo `(eval - prev) + (prev * val)` |
| **Matchsticks (473)**   | **$O(4^N)$ Exponential ⚡**| **$O(N)$ Call Stack Memory**| Descending sort + `sides[i] == 0` break |

---

## 10. Edge Cases & Boundary Handling
* **Leading Zeros in String (`"105"`)**: Substring `"05"` pruned immediately by `if (i > start && num.charAt(start) == '0') break`.
* **64-Bit Integer Overflow**: Uses `long` type for `eval`, `prevOperand`, and `val`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `int` Types Instead of `long` for Expression Evaluation**:
  - String numbers like `"105234234"` easily exceed 32-bit `Integer.MAX_VALUE` during intermediate multiplication steps.
  - **ALWAYS use `long` for evaluation totals in LeetCode 282**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Descending Order Speeds Up LeetCode 473 Matchsticks:
> Sorting matchstick lengths in descending order places large elements first.
> Large elements fail capacity checks (`sides[i] + val <= target`) early in the decision tree, cutting off thousands of invalid subtrees near the top of the search space! ⚡

> **Memory Trick:** **"Sort matchsticks descending to fail capacity checks near the top of the backtracking tree!"**

---

## 13. System & Implementation Comparisons

| Feature | Expression Evaluation Backtracking | Postfix Expression Stack |
| :--- | :--- | :--- |
| **Search Goal** | Generate All Matching Expressions | Evaluate Fixed Expression |
| **Precedence Mechanism**| **Undo Previous Step `(eval - prev)` ⚡**| Operator Precedence Stack |
| **Time Complexity** | $O(4^N)$ Exponential | **$O(N)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Insert +, -, * operators between digits to match target value"** $\rightarrow$ LeetCode 282 (Expression Add Operators).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `(eval - prevOperand) + (prevOperand * val)` handle multiplication precedence?**  
  *A:* It subtracts `prevOperand` from `eval` to undo the previous addition/subtraction, then adds the true multiplied value `(prevOperand * val)`.
* **Q: Why does `if (i > start && num.charAt(start) == '0') break;` prevent leading zero bugs?**  
  *A:* If the number starts with `'0'`, single digit `"0"` is valid, but multi-digit substrings starting with `'0'` (e.g. `"05"`) are illegal, so we `break` immediately.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED BACKTRACKING (LEETCODE 282)                  |
+-----------------------------------------------------------------------+
| • Multiplication Undo: newEval = (eval - prevOperand) + (prevOperand * val);|
| • Leading Zero Guard : if (i > start && num.charAt(start) == '0') break;|
| • Path Backtrack     : path.setLength(len);                           |
| • Matchsticks (473)  : Sort descending + check sum % 4 == 0            |
| • Performance        : O(4^N) Exponential Time | O(N) Stack Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 282 (`Expression Add Operators`) in Java.
- [ ] I can write LeetCode 473 (`Matchsticks to Square`).
- [ ] I know why `(eval - prev) + (prev * val)` handles multiplication precedence.
- [ ] I know why leading zeros are pruned.
- [ ] I can trace expression evaluation backtracking step by step.
