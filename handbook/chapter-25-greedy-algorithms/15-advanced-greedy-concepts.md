# 15. Advanced Greedy Concepts: Regret Priority Queues, Monotone Stacks & Competitive Ratios

## 1. Introduction
**Advanced Greedy Concepts** extend classical static greedy choices into dynamic online environments, regret-based decision systems, and competitive ratio analysis. While standard greedy algorithms make irrevocable choices, **Greedy Regret Algorithms** maintain a **Priority Queue of Past Choices** that can be retroactively **Undone or Exchanged** when a more beneficial opportunity arises. Key advanced greedy paradigms include:
1. **Greedy Regret / Priority Queue Undo (LeetCode 871 & LeetCode 630)**: Greedily consumes resources or accepts courses, but if a capacity/deadline constraint is violated, retroactively pops the largest past expense or duration from a Max-Heap in **$O(N \log N)$ Time Complexity**.
2. **Monotone Stack / Queue Greedy Choices (LeetCode 402 & LeetCode 316)**: Maintains a monotonic stack to greedily eliminate larger leading digits or character inversions in **$O(N)$ Strict Linear Time**.
3. **Online Algorithms & Competitive Ratios**: Analyzes algorithms processing input streams without future knowledge, comparing online performance $A(\sigma)$ against an offline adversary $OPT(\sigma)$ via the **Competitive Ratio**:
   $$\text{Competitive Ratio } c = \max_{\sigma} \frac{A(\sigma)}{OPT(\sigma)}$$

> **Important:** Core Invariants of Advanced Greedy Systems:
> 1. **Greedy Regret Invariant**:
>    - Process elements sequentially. If a constraint (e.g. tank empty, deadline exceeded) is violated, pop the LARGEST element from a Max-Heap of past choices to "regret" and restore validity in $O(\log N)$ time.
> 2. **Monotone Stack Invariant**:
>    - Pop elements from stack while `stack.peek() > currChar` and `remCount > 0` (or remaining occurrences exist), greedily ensuring leading digits/chars are as small as possible!
> 3. **Ski-Rental 2-Competitive Bound**:
>    - Online rule: Rent equipment until rental cost equals purchase price $P$, then buy! Guarantees competitive ratio $\le 2$ against any offline adversary. ⚡

```
Greedy Regret Max-Heap Topology (LeetCode 871 - Min Refueling Stops):

Current Tank: 10 miles. Reached Station A (Gas 60).
Greedy Step: Do NOT refuel yet! Push Gas 60 to Max-Heap.

Drive to Station B at mile 15: Tank drops to 10 - 15 = -5 (EMPTY!).
Regret Step: Pop LARGEST past station from Max-Heap! Pop Gas 60!
Tank increases to -5 + 60 = 55 miles! Stops Count = 1! ⚡

Retroactive Refueling without backtracking execution! ⚡
```

---

## 2. Core Concepts & Advanced Greedy Paradigm Strategy Matrix

### 2.1 Advanced Greedy Strategy Matrix
```
Advanced Greedy Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Paradigm              | Primary Mechanism | Undo Capacity?    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Greedy Regret**     | Max-Heap Backtrack| **YES (Max-Heap)⚡**| **$O(N \log N)$ ⚡**| **$O(N)$ Heap ⚡**|
| **Monotone Stack**    | Stack Inversion   | **YES (Pop Stack)⚡**| **$O(N)$ Strict ⚡**| $O(N)$ Stack      |
| **Online Ski-Rental** | Threshold Buy     | No                | **$O(1)$ Instant ⚡**| $O(1)$ Memory     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Greedy Regret pops max element from Max-Heap to undo past choices; Monotone Stack pops stack.peek() > curr to minimize leading digits!"**

---

## 3. Characteristics & Competitive Ratio Proofs

### 3.1 Mathematical Proof of Ski-Rental 2-Competitive Ratio
* **Problem**: Renting skis costs $\$1$/day; Buying skis costs $\$P$. You do not know how many days $D$ you will ski.
* **Greedy Online Strategy**: Rent for $P - 1$ days. On day $P$, buy the skis. Total Cost = $(P - 1) \cdot 1 + P = 2P - 1$.
* **Proof of 2-Competitive Ratio**:
  - Case 1 ($D < P$): Offline optimal $OPT = D$. Online cost $A = D$. Ratio $\frac{A}{OPT} = 1$.
  - Case 2 ($D \ge P$): Offline optimal buys on day 1 $\to OPT = P$. Online cost $A = 2P - 1$.
  - Competitive Ratio:
    $$\frac{A}{OPT} = \frac{2P - 1}{P} = 2 - \frac{1}{P} < 2$$
  - Proves that the online greedy rule is strictly **2-Competitive**! ⚡

---

## 4. Internal Working Mechanics: Monotone Stack Digit Elimination

Tracing LeetCode 402 (Remove K Digits) for $num = \text{"1432219"}$, $k = 3$:

```
Goal: Remove k = 3 digits to form the smallest possible integer.

Process Chars with Monotone Stack:

1. Char '1': Stack = ['1']
2. Char '4': '4' > '1' -> Push '4'. Stack = ['1', '4']
3. Char '3': '3' < Stack.peek() ('4') AND k > 0!
   - POP '4'! k = 2. Push '3'. Stack = ['1', '3']
4. Char '2': '2' < Stack.peek() ('3') AND k > 0!
   - POP '3'! k = 1. Push '2'. Stack = ['1', '2']
5. Char '2': '2' == Stack.peek() ('2') -> Push '2'. Stack = ['1', '2', '2']
6. Char '1': '1' < Stack.peek() ('2') AND k > 0!
   - POP '2'! k = 0. Push '1'. Stack = ['1', '2', '1']
7. Char '9': k = 0 -> Push '9'. Stack = ['1', '2', '1', '9']

Result String = "1219" (Smallest integer after removing 3 digits!) ✅
```

---

## 5. Visual Diagram: Greedy Regret Priority Queue Execution

```
Vehicle Traversal & Gas Station Max-Heap Flow (LeetCode 871):

Gas Stations Passed:   [ Station 1: 60 ]    [ Station 2: 30 ]    [ Station 3: 10 ]
Max-Heap Contents  :   [ 60 ] ──► Add 30 ──► [ 60, 30 ] ──► Add 10 ──► [ 60, 30, 10 ]

Tank Empty at Mile 100!
Regret Step: Pop Max-Heap Top (60)!
Refuel Count = 1, Tank Capacity Increases by 60 miles! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Greedy Regret Refueling (LeetCode 871), Monotone Stack Digit Removal (LeetCode 402), and LeetCode 630 (Course Schedule III).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced Greedy Concepts:
 * Regret Priority Queues, Monotone Stack Digit Elimination, and Course Scheduling.
 */
public class AdvancedGreedyConceptsMaster {

    // =========================================================================
    // 1. LEETCODE 871: MINIMUM NUMBER OF REFUELING STOPS (O(N log N) Time)
    // =========================================================================
    /**
     * Finds minimum refueling stops using Greedy Regret Max-Heap.
     * stations[i] = [position_i, fuel_i].
     */
    public int minRefuelStops(int target, int startFuel, int[][] stations) {
        if (startFuel >= target) return 0;

        // Max-Heap storing fuel capacity of passed stations
        PriorityQueue<Integer> maxFuelHeap = new PriorityQueue<>(Collections.reverseOrder());

        int currentFuel = startFuel;
        int stops = 0;
        int i = 0;
        int n = (stations != null) ? stations.length : 0;

        while (currentFuel < target) {
            // Push all reachable stations into Max-Heap
            while (i < n && stations[i][0] <= currentFuel) {
                maxFuelHeap.add(stations[i][1]);
                i++;
            }

            // Tank empty and no past stations to regret -> Impossible!
            if (maxFuelHeap.isEmpty()) return -1;

            // Regret Choice: Retroactively refuel at past station with MAX fuel! ⚡
            currentFuel += maxFuelHeap.poll();
            stops++;
        }

        return stops;
    }

    // =========================================================================
    // 2. LEETCODE 630: COURSE SCHEDULE III (Greedy Regret Max-Heap O(N log N))
    // =========================================================================
    /**
     * Maximizes total courses taken. courses[i] = [duration_i, lastDay_i].
     */
    public int scheduleCourse(int[][] courses) {
        if (courses == null || courses.length == 0) return 0;

        // Step 1: Sort courses by LAST DAY ascending
        Arrays.sort(courses, Comparator.comparingInt(a -> a[1]));

        // Max-Heap storing durations of taken courses
        PriorityQueue<Integer> durationMaxHeap = new PriorityQueue<>(Collections.reverseOrder());
        int totalTime = 0;

        for (int[] course : courses) {
            int duration = course[0];
            int lastDay = course[1];

            if (totalTime + duration <= lastDay) {
                // Course fits! Add to schedule
                totalTime += duration;
                durationMaxHeap.add(duration);
            } else if (!durationMaxHeap.isEmpty() && durationMaxHeap.peek() > duration) {
                // Regret Choice: Replace longest past course with shorter course! ⚡
                totalTime += duration - durationMaxHeap.poll();
                durationMaxHeap.add(duration);
            }
        }

        return durationMaxHeap.size();
    }

    // =========================================================================
    // 3. LEETCODE 402: REMOVE K DIGITS (Monotone Stack O(N) Strict Linear Time)
    // =========================================================================
    /**
     * Removes k digits from string num to form the smallest possible integer.
     */
    public String removeKdigits(String num, int k) {
        if (num == null || k >= num.length()) return "0";

        Deque<Character> stack = new ArrayDeque<>();

        for (int i = 0; i < num.length(); i++) {
            char digit = num.charAt(i);

            // Monotone Stack Inversion Swap Line
            while (!stack.isEmpty() && k > 0 && stack.peekLast() > digit) {
                stack.removeLast();
                k--;
            }

            stack.addLast(digit);
        }

        // If k > 0 remaining, pop from tail
        while (k > 0 && !stack.isEmpty()) {
            stack.removeLast();
            k--;
        }

        // Build result and strip leading zeros
        StringBuilder sb = new StringBuilder();
        while (!stack.isEmpty()) {
            sb.append(stack.removeFirst());
        }

        while (sb.length() > 1 && sb.charAt(0) == '0') {
            sb.deleteCharAt(0); // Strip leading zero
        }

        return (sb.length() == 0) ? "0" : sb.toString();
    }
}
```

> **Quick Syntax:**
```java
// Greedy Regret Duration Swap Line
if (totalTime + duration > lastDay && durationMaxHeap.peek() > duration) totalTime += duration - durationMaxHeap.poll();
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 871 - Minimum Number of Refueling Stops**:
   - Primary Greedy Regret Max-Heap application ($O(N \log N)$ time).

2. **LeetCode 630 - Course Schedule III**:
   - Retroactive course swap using Max-Heap of durations.

3. **LeetCode 402 - Remove K Digits**:
   - Monotone stack digit elimination in $O(N)$ linear time.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class AdvancedGreedyConceptsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ADVANCED GREEDY REGRET & MONOTONE STACK DEMO  ");
        System.out.println("=================================================\n");

        AdvancedGreedyConceptsMaster master = new AdvancedGreedyConceptsMaster();

        // 1. LeetCode 871 Min Refuel Stops Test
        int target = 100;
        int startFuel = 10;
        int[][] stations = {{10, 60}, {20, 30}, {30, 30}, {60, 40}};
        int minStops = master.minRefuelStops(target, startFuel, stations);

        System.out.println("1. LeetCode 871 Min Refuel Stops (Target 100, Fuel 10):");
        System.out.println("   Stations = [[10,60], [20,30], [30,30], [60,40]]");
        System.out.println("   Minimum Stops (Greedy Regret Max-Heap): " + minStops + " Stops");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 402 Remove K Digits Test
        String num = "1432219";
        int k = 3;
        String smallestNum = master.removeKdigits(num, k);

        System.out.println("2. LeetCode 402 Remove K Digits Test:");
        System.out.println("   Original Num = \"" + num + "\", k = " + k);
        System.out.println("   Smallest Result (Monotone Stack): \"" + smallestNum + "\" (O(N) Time)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Advanced Greedy Paradigm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Greedy Regret (Heap)**| $\mathbf{O(N \log N)}$ ⚡| $\mathbf{O(N)}$ Heap ⚡| Retroactive Max-Heap swap |
| **Monotone Stack**      | $\mathbf{O(N)}$ Strict ⚡| $O(N)$ Stack | Pop `stack.peek() > curr` |
| **Ski-Rental Online**   | $\mathbf{O(1)}$ Instant ⚡| $\mathbf{O(1)}$ Memory ⚡| 2-Competitive Threshold |

---

## 10. Edge Cases & Boundary Handling

1. **Leading Zeros in Remove K Digits (`"10200"`, $k=1$)**:
   - Removing `'1'` leaves `"0200"`. Stripping leading zeros produces `"200"`. Handled cleanly.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Thinking Greedy Choices Can Never Be Undone**:
  - In Greedy Regret problems, maintaining a Priority Queue allows retroactively swapping past choices when constraints are violated!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Use Greedy Regret Priority Queues:
> Use Greedy Regret when processing items sequentially where a past choice might be swapped for a better choice later (e.g. replacing a long course with a shorter course in Course Schedule III). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Greedy Regret (Heap) | Monotone Stack | Standard Greedy |
| :--- | :--- | :--- | :--- |
| **Choice Undo?** | **YES (Max-Heap Swap)⚡**| **YES (Stack Pop)⚡**| NEVER (Irrevocable) |
| **Time Complexity** | **$O(N \log N)$ ⚡** | **$O(N)$ Strict ⚡** | $O(N \log N)$ |
| **Primary Structure**| PriorityQueue | Deque / Stack | Sorted Array |

---

## 14. How to Recognize This in Questions

* **"Minimum refueling stops to reach target"** $\rightarrow$ LeetCode 871 (Greedy Regret Max-Heap).
* **"Remove K digits to make remaining integer smallest"** $\rightarrow$ LeetCode 402 (Monotone Stack).

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Greedy Regret Algorithm?**  
  *A:* An algorithm that processes choices sequentially but stores past decisions in a Priority Queue to retroactively undo/swap the worst choice if a constraint is violated.

* **Q: What is a Competitive Ratio?**  
  *A:* The maximum ratio over all input sequences of an online algorithm's cost compared to an offline optimal adversary ($c = \max \frac{A(\sigma)}{OPT(\sigma)}$).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED GREEDY CONCEPTS                              |
+-----------------------------------------------------------------------+
| • Greedy Regret: Maintain Max-Heap -> Pop max past item to undo choice |
| • Monotone Stack: Pop stack.peek() > currDigit while k > 0 -> O(N)    |
| • Ski-Rental   : Rent until cost == P, then Buy -> 2-Competitive      |
| • LC 871/630   : Greedy Regret Max-Heap in O(N log N) time ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Greedy Regret Max-Heap refueling (LeetCode 871) in Java.
- [ ] I can solve LeetCode 630 (`Course Schedule III`) using Greedy Regret.
- [ ] I can write Monotone Stack digit elimination (LeetCode 402) in Java.
- [ ] I can prove the 2-Competitive ratio for Ski-Rental.
- [ ] I can explain how Greedy Regret differs from standard Greedy.
