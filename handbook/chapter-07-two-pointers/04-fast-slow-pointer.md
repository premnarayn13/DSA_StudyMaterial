# 04. Fast & Slow Pointers (Tortoise & Hare), Digit Cycles & Circular Array Loops

## 1. Introduction
The **Fast & Slow Pointer Pattern** (also known as the **Tortoise and Hare Algorithm**) employs two pointer references advancing through a sequence at different speeds—typically `slow` moving 1 step per iteration and `fast` moving 2 steps per iteration. Beyond linked list applications, this pattern solves cycle detection problems in implicit functional state graphs, such as **Happy Number (LeetCode 202)** and **Circular Array Loop (LeetCode 457)**, in **$O(N)$ linear time and $O(1)$ constant auxiliary space**.

> **Important:** Fast & Slow pointers eliminate the need for an external `HashSet` to track visited states in cycle detection problems! By proving mathematically that two pointers moving at different speeds inside a finite state graph WILL eventually overlap (`slow == fast`), cycle detection is achieved in **$O(1)$ space**!

```
Fast & Slow Pointer State Cycle Topology:
+-----------------------------------------------------------------------------------+
| Hash Set Strategy : Set<Integer> visited -> O(N) Time, O(N) Space (High Memory)   |
| Fast & Slow Pointer: slow (1 step) & fast (2 steps) -> O(N) Time, O(1) Space ⚡   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Happy Number Cycle Mechanics (LeetCode 202)

### 2.1 Happy Number Problem (LeetCode 202)
A **Happy Number** is defined by replacing a number with the sum of the squares of its digits, and repeating until the number equals `1` (happy) or loops endlessly in a cycle (unhappy):

#### Digit Sum Function $f(n)$:
For $n = 19$:

$$f(19) = 1^2 + 9^2 = 1 + 81 = 82$$

$$f(82) = 8^2 + 2^2 = 64 + 4 = 68$$

$$f(68) = 6^2 + 8^2 = 36 + 64 = 100$$

$$f(100) = 1^2 + 0^2 + 0^2 = 1 \text{ (Happy!)}$$

#### Unhappy Cycle Example ($n = 2$):
$2 \to 4 \to 16 \to 37 \to 58 \to 89 \to 145 \to 42 \to 20 \to 4 \dots$ (Enters cycle containing 4!).

#### Fast & Slow Pointer Algorithm:
1. `slow = n`, `fast = getNext(n)`.
2. While `fast != 1 && slow != fast`:
   - `slow = getNext(slow)` (1 step).
   - `fast = getNext(getNext(fast))` (2 steps).
3. Return `fast == 1`!

```
Happy Number Fast & Slow Pointer Execution:
Start: slow = 19, fast = 82 (f(19))

Step 1: slow = 82, fast = 68 (f(f(82)))
Step 2: slow = 68, fast = 1 (f(f(68))) -> fast reaches 1!

Loop terminates. fast == 1 -> Returns TRUE! ✅ (O(1) Auxiliary Space!)
```

> **Memory Trick:** **"Happy Number Cycle Detection: slow = getNext(slow), fast = getNext(getNext(fast))! If fast == 1 return true!"**

---

## 3. Characteristics & Circular Array Loop (LeetCode 457)

### 3.1 Circular Array Loop (LeetCode 457)
Given a circular array `nums` of positive and negative integers:
* A movement step from index $i$ lands at index **$(i + \text{nums}[i]) \bmod N$** (handling negative modulo correctly).
* A cycle MUST meet 3 strict rules:
  1. **Uniform Direction**: All elements in the cycle MUST move in the SAME direction (all positive or all negative).
  2. **Cycle Length $> 1$**: A self-loop node pointing to itself (`nums[i] % N == 0`) is NOT a valid cycle.
  3. **Space Complexity**: Must be solved in **$O(1)$ constant auxiliary space**.

#### Algorithmic Strategy:
* Iterate each index $i$ as a candidate starting node.
* Use `slow` and `fast` pointers to traverse index jumps.
* Validate direction: `isForward = nums[i] > 0`. If any jump changes direction, abort cycle search for that candidate!

```
Correct Modulo Pointer Jump Equation in Java:
int nextIdx = (curr + nums[curr]) % N;
if (nextIdx < 0) nextIdx += N; // Wrap negative modulo!
```

---

## 4. Internal Working Mechanics
Tracing Happy Number (LeetCode 202) on $N = 2$ (Unhappy Number):

```
Init: slow = 2, fast = getNext(2) = 4

Pass 1: slow = getNext(2) = 4
        fast = getNext(getNext(4)) = getNext(16) = 37

Pass 2: slow = 16, fast = 89
Pass 3: slow = 37, fast = 42
Pass 4: slow = 58, fast = 4  ===> slow == fast == 4! (Meeting Point)

Loop terminates. fast != 1 -> Returns FALSE! ✅ (O(1) Auxiliary Space!)
```

---

## 5. Visual Diagram
Happy Number Digit Transition State Graph Topography:

```
UNHAPPY CYCLE (n = 2):
( 2 ) ---> ( 4 ) ---> ( 16 ) ---> ( 37 ) ---> ( 58 )
             ^                                   |
             |                                   v
          ( 20 ) <--- ( 42 ) <--- ( 145 ) <--- ( 89 )
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Happy Number (LeetCode 202) and Circular Array Loop (LeetCode 457):

```java
import java.util.*;

public class FastSlowPointerMaster {

    // 1. Happy Number (LeetCode 202) O(log N) Time, O(1) Auxiliary Space
    public static boolean isHappy(int n) {
        int slow = n;
        int fast = getNextDigitSum(n);

        while (fast != 1 && slow != fast) {
            slow = getNextDigitSum(slow);
            fast = getNextDigitSum(getNextDigitSum(fast));
        }

        return fast == 1;
    }

    // Helper: Compute Sum of Squares of Digits
    public static int getNextDigitSum(int n) {
        int sum = 0;
        while (n > 0) {
            int digit = n % 10;
            sum += digit * digit;
            n /= 10;
        }
        return sum;
    }

    // 2. Circular Array Loop (LeetCode 457) O(N) Time, O(1) Auxiliary Space
    public static boolean circularArrayLoop(int[] nums) {
        if (nums == null || nums.length <= 1) return false;
        int n = nums.length;

        for (int i = 0; i < n; i++) {
            if (nums[i] == 0) continue; // Already marked invalid

            int slow = i;
            int fast = i;
            boolean isForward = nums[i] > 0;

            while (true) {
                slow = getNextIndex(nums, isForward, slow);
                fast = getNextIndex(nums, isForward, fast);
                if (fast != -1) {
                    fast = getNextIndex(nums, isForward, fast);
                }

                if (slow == -1 || fast == -1) break; // Invalid direction or self-loop

                if (slow == fast) {
                    return true; // Valid cycle found!
                }
            }

            // Mark visited path as 0 to prevent re-processing
            int curr = i;
            while (nums[curr] != 0 && (nums[curr] > 0) == isForward) {
                int next = getNextIndex(nums, isForward, curr);
                nums[curr] = 0;
                if (next == -1) break;
                curr = next;
            }
        }

        return false;
    }

    private static int getNextIndex(int[] nums, boolean isForward, int curr) {
        int n = nums.length;
        boolean direction = nums[curr] > 0;

        // Rule 1: Direction must match
        if (direction != isForward) return -1;

        int nextIdx = (curr + nums[curr]) % n;
        if (nextIdx < 0) nextIdx += n; // Wrap negative modulo

        // Rule 2: Cycle length must be > 1 (No self-loops!)
        if (nextIdx == curr) return -1;

        return nextIdx;
    }
}
```

> **Quick Syntax:**
```java
// Wrapped Modulo Calculation for Circular Array Moves
int nextIdx = (curr + nums[curr]) % n;
if (nextIdx < 0) nextIdx += n;
```

---

## 7. Concrete Problem Examples
* **LeetCode 202 - Happy Number**: Digit sum cycle detection.
* **LeetCode 457 - Circular Array Loop**: Array index jump cycle detection.
* **LeetCode 287 - Find the Duplicate Number**: Array functional graph cycle detection.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Happy Number and Circular Array Loop:

```java
public class FastSlowPointerDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Happy Number Check (LeetCode 202) ===");
        System.out.println("Is 19 Happy? (Expected true):  " + FastSlowPointerMaster.isHappy(19)); // true
        System.out.println("Is 2 Happy?  (Expected false): " + FastSlowPointerMaster.isHappy(2));  // false

        System.out.println("\n=== 2. Circular Array Loop (LeetCode 457) ===");
        int[] nums1 = {2, -1, 1, 2, 2};
        System.out.println("Has Circular Loop? (Expected true): " + FastSlowPointerMaster.circularArrayLoop(nums1)); // true

        int[] nums2 = {-1, 2};
        System.out.println("Has Circular Loop? (Expected false): " + FastSlowPointerMaster.circularArrayLoop(nums2)); // false
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Happy Number (202)** | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Strict In-Place ⚡**| Digit sum function bounds state space |
| **Circular Array Loop (457)**| **$O(N)$ Linear ⚡** | **$O(1)$ Strict In-Place ⚡**| Zeroing visited invalid paths |

---

## 10. Edge Cases & Boundary Handling
* **Self-Loop Jumps (`nums[i] % N == 0`)**: Invalidated by `nextIdx == curr` check in LeetCode 457.
* **Negative Modulo Wrapping**: Handled cleanly via `if (nextIdx < 0) nextIdx += n;`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `HashSet` for Happy Number ($O(N)$ Space)**:
  - Using a `Set<Integer>` to store visited numbers consumes $O(N)$ auxiliary memory.
  - **Use Fast & Slow pointers for $O(1)$ constant memory**.
* **Ignoring Negative Modulo in Circular Array Movement**:
  - `(curr + nums[curr]) % N` can yield negative values in Java!
  - **Always add `N` if `nextIdx < 0`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Correct Java Negative Modulo Arithmetic Rule:
> In Java, `-1 % 5` evaluates to `-1` (NOT `4`!).
> To convert a negative modulo result to a valid array index:
> `int idx = (curr + step) % N; if (idx < 0) idx += N;`

> **Memory Trick:** **"Java modulo can be negative! Always add N if nextIdx < 0!"**

---

## 13. System & Implementation Comparisons

| Feature | Fast & Slow Pointer Approach | Hash Set Visited Tracking |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Constant ⚡** | $O(N)$ Hash Table |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N)$ Linear |
| **Garbage Collection**| Zero Heap Objects | High Object Churn |

---

## 14. How to Recognize This in Questions
* **"Determine if process enters endless cycle of digit operations"** $\rightarrow$ LeetCode 202 (Fast & Slow digit sum).
* **"Find continuous direction cycle in circular array"** $\rightarrow$ LeetCode 457 (Fast & Slow index jumps).

---

## 15. Frequently Asked Interview Questions
* **Q: Why is the state space of Happy Number digit sums small and bounded?**  
  *A:* For any 32-bit integer $N \le 2 \times 10^9$, the largest number is $1,999,999,999$. Its digit sum is $1^2 + 9 \times 9^2 = 1 + 729 = 730$. Thus, digit sums rapidly shrink below $730$, bounding the state space to a small finite graph!
* **Q: Why are self-loops disallowed in LeetCode 457 (Circular Array Loop)?**  
  *A:* A self-loop occurs when an element points to itself (`nums[i] % N == 0`). LeetCode 457 explicitly defines a valid cycle as having length $> 1$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FAST & SLOW POINTERS IN DIGIT & ARRAY CYCLES          |
+-----------------------------------------------------------------------+
| • Happy Number (202): slow = f(slow), fast = f(f(fast))               |
| • Happy Condition: Loop ends when fast == 1 (Happy) or slow == fast (Cycle)|
| • Negative Modulo Rule: idx = (curr + nums[curr]) % N; if (idx < 0) idx += N|
| • Circular Array Rules (457): Uniform direction AND cycle length > 1  |
| • Path Cleaning: Set nums[curr] = 0 for invalid paths to achieve O(N) time|
| • Space Invariant: Strictly O(1) Auxiliary Memory ⚡                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Happy Number (LeetCode 202) using Fast & Slow pointers in $O(1)$ space.
- [ ] I can write the `getNextDigitSum` helper function in 5 lines.
- [ ] I know why Java negative modulo requires `if (idx < 0) idx += N`.
- [ ] I can solve Circular Array Loop (LeetCode 457) respecting direction & length rules.
- [ ] I know why Happy Number digit sums are bounded below 730.
