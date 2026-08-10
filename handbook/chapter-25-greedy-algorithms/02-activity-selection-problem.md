# 02. Activity Selection Problem: Finish Time Greedy Invariants & Mathematical Proofs

## 1. Introduction
The **Activity Selection Problem** (also known as **Interval Scheduling Maximization**) is the foundational classic benchmark problem in greedy algorithmic theory. Given a set of $N$ activities $A = \{a_1, a_2 \dots a_N\}$, where each activity $a_i$ has a start time $s_i$ and a finish time $f_i$ ($s_i < f_i$), the goal is to select the **Maximum Number of Mutually Compatible Activities** that can be performed by a single resource (e.g. a meeting room or CPU execution thread). Two activities $a_i$ and $a_j$ are compatible if their execution intervals do NOT overlap ($s_j \ge f_i$ or $s_i \ge f_j$). The optimal Greedy strategy sorts activities by **Earliest Finish Time ($f_i$)** in ascending order, achieving **$O(N \log N)$ Time Complexity** and **$O(1)$ Auxiliary Space**.

> **Important:** Core Invariants of the Activity Selection Problem:
> 1. **Earliest Finish Time Choice Invariant**:
>    - Always select the unselected compatible activity with the **Earliest Finish Time ($f_i$)**.
>    - Why? Finishing early leaves the MAXIMUM remaining time available for subsequent activities!
> 2. **Flawed Greedy Choices Audit**:
>    - Sort by Start Time ($s_i$): FAILS (An activity starting early could run for 1,000 hours!).
>    - Sort by Shortest Duration ($f_i - s_i$): FAILS (Short activity in middle blocks two non-overlapping long activities!).
>    - Sort by Fewest Overlaps: FAILS (Complex counter-examples exist).
> 3. **Exchange Argument Proof Invariant**:
>    - Proves that picking the activity with the earliest finish time can always be substituted into any optimal solution without reducing the total activity count. ⚡

```
Activity Selection Topology (Sorted by Finish Time):

Activity 1: [ s1 ====== f1 ]
Activity 2:          [ s2 ======= f2 ]
Activity 3:                     [ s3 ========= f3 ]

Greedy Rule: Pick Activity 1 (Finishes First).
Next Compatible: Activity 2 starts at s2 >= f1 -> PICK Activity 2!
Next Compatible: Activity 3 starts at s3 >= f2 -> PICK Activity 3!

Maximizes count of non-overlapping meetings scheduled! ⚡
```

---

## 2. Core Concepts & Interval Strategy Matrix

### 2.1 Interval Greedy Sorting Rules Comparison Matrix
```
Interval Sorting Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Sorting Criterion     | Strategy Outcome  | Correctness       | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Earliest Finish**   | $f_1 \le f_2 \le \dots$| **OPTIMAL ✅**    | **$O(N \log N)$ ⚡**|
| **Earliest Start**    | $s_1 \le s_2 \le \dots$| **FAILS ❌**      | $O(N \log N)$     |
| **Shortest Duration** | $(f-s)_1 \le (f-s)_2$| **FAILS ❌**      | $O(N \log N)$     |
| **Fewest Overlaps**   | $\text{deg}_1 \le \text{deg}_2$| **FAILS ❌**   | $O(N^2)$          |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Always sort intervals by EARLIEST FINISH TIME f_i! Finishing early leaves max room for future tasks!"**

---

## 3. Characteristics & Exchange Argument Mathematical Proof

### 3.1 Mathematical Proof of Optimality via Exchange Argument
* **Theorem**: Sorting activities by earliest finish time $f_i$ yields an optimal maximum subset of mutually compatible activities.
* **Proof**:
  1. Let $A = \{1, 2 \dots N\}$ be activities sorted such that $f_1 \le f_2 \le \dots \le f_N$.
  2. Let $G = \{g_1, g_2 \dots g_k\}$ be the greedy solution, and $O = \{o_1, o_2 \dots o_m\}$ be an optimal solution.
  3. We want to prove $k = m$ (Greedy selects the same maximum number of activities as optimal).
  4. Compare first choices $g_1$ and $o_1$:
     - By greedy choice, $g_1$ has the earliest finish time among all activities, so $f_{g_1} \le f_{o_1}$.
     - If $g_1 = o_1$, they match.
     - If $g_1 \neq o_1$, substitute $g_1$ for $o_1$ in $O$, forming $O' = \{g_1, o_2 \dots o_m\}$.
     - Since $f_{g_1} \le f_{o_1}$, activity $g_1$ finishes no later than $o_1$. Thus, $g_1$ does NOT overlap with $o_2, o_3 \dots o_m$.
     - Therefore, $O'$ is a valid compatible solution of size $m$.
  5. By mathematical induction, we can replace every element $o_i$ with $g_i$ without breaking compatibility.
  6. Thus, $k = m$, proving that the Greedy solution $G$ is globally optimal! ⚡

---

## 4. Internal Working Mechanics: Counter-Examples to Flawed Choices

Why sorting by Start Time or Duration fails:

```
Counter-Example 1: Sorting by Earliest Start Time (FAILS ❌):
Activity A: [ 0 ============================= 100 ]
Activity B:    [ 1 == 2 ]
Activity C:              [ 3 == 4 ]

- Sort by Start Time: Picks Activity A (Starts at 0). Takes 1 activity total.
- OPTIMAL Solution: Picks Activity B + Activity C. Takes 2 activities! ❌

Counter-Example 2: Sorting by Shortest Duration (FAILS ❌):
Activity A: [ 0 ====== 5 ]
Activity B:        [ 4 = 6 ] (Shortest Duration = 2)
Activity C:            [ 5 ====== 10 ]

- Sort by Duration: Picks Activity B (Duration 2). Blocks A and C! Total = 1.
- OPTIMAL Solution: Picks Activity A + Activity C. Total = 2 activities! ❌
```

---

## 5. Visual Diagram: Greedy Activity Selection Pipeline

```
Activities Array (Sorted by Finish Time f_i):

Index 0:  [ s0 === f0 ]   ──► SELECTED (Last Finish Time = f0)
Index 1:    [ s1 === f1 ] ──► OVERLAPS (s1 < f0) -> REJECT!
Index 2:       [ s2 === f2 ] ──► COMPATIBLE (s2 >= f0) -> SELECTED (Last Finish Time = f2)
Index 3:          [ s3 = f3 ] ──► OVERLAPS (s3 < f2) -> REJECT!

Selected Count = 2 Activities! Linear Scan in O(N) after sorting! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Activity Selection, LeetCode 435 (Non-Overlapping Intervals), and LeetCode 452 (Minimum Arrows to Burst Balloons).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Activity Selection Problem,
 * Earliest Finish Time Greedy Sorting, and Interval Scheduling Variants.
 */
public class ActivitySelectionMaster {

    public static class Activity {
        public final int id;
        public final int start;
        public final int finish;

        public Activity(int id, int start, int finish) {
            this.id = id;
            this.start = start;
            this.finish = finish;
        }

        @Override
        public String toString() {
            return "Activity" + id + "[" + start + "->" + finish + "]";
        }
    }

    // =========================================================================
    // 1. STANDARD ACTIVITY SELECTION (O(N log N) Time, O(1) Auxiliary Space)
    // =========================================================================
    /**
     * Selects maximum count of non-overlapping activities.
     *
     * @param activities list of input activities
     * @return list of selected optimal activities
     */
    public List<Activity> selectMaxActivities(List<Activity> activities) {
        List<Activity> selected = new ArrayList<>();
        if (activities == null || activities.isEmpty()) return selected;

        // Step 1: Sort activities by EARLIEST FINISH TIME (f_i) ascending
        List<Activity> sorted = new ArrayList<>(activities);
        sorted.sort(Comparator.comparingInt(a -> a.finish));

        // Step 2: Pick first activity (earliest finish time)
        Activity lastSelected = sorted.get(0);
        selected.add(lastSelected);

        // Step 3: Iterate through remaining activities
        for (int i = 1; i < sorted.size(); i++) {
            Activity curr = sorted.get(i);
            // Check compatibility: current start >= last finish
            if (curr.start >= lastSelected.finish) {
                selected.add(curr);
                lastSelected = curr; // Update last finish time! ⚡
            }
        }

        return selected;
    }

    // =========================================================================
    // 2. LEETCODE 435: NON-OVERLAPPING INTERVALS (O(N log N) Time)
    // =========================================================================
    /**
     * Calculates MINIMUM number of intervals to remove to make remaining intervals non-overlapping.
     * Theorem: Min Removes = Total Intervals - Max Selected Non-Overlapping Activities.
     */
    public int eraseOverlapIntervals(int[][] intervals) {
        if (intervals == null || intervals.length <= 1) return 0;

        // Sort by end time ascending
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));

        int countKept = 1;
        int lastEnd = intervals[0][1];

        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= lastEnd) {
                countKept++;
                lastEnd = intervals[i][1];
            }
        }

        return intervals.length - countKept; // Min removals formula ⚡
    }

    // =========================================================================
    // 3. LEETCODE 452: MINIMUM ARROWS TO BURST BALLOONS (O(N log N) Time)
    // =========================================================================
    /**
     * Finds minimum arrows needed to burst all balloons represented by overlapping intervals.
     */
    public int findMinArrowShots(int[][] points) {
        if (points == null || points.length == 0) return 0;

        // Sort by end coordinate ascending (handling integer overflow safely!)
        Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));

        int arrows = 1;
        int lastArrowPos = points[0][1];

        for (int i = 1; i < points.length; i++) {
            if (points[i][0] > lastArrowPos) {
                arrows++;
                lastArrowPos = points[i][1];
            }
        }

        return arrows;
    }
}
```

> **Quick Syntax:**
```java
// Activity Selection Finish Time Sorting Line
sorted.sort(Comparator.comparingInt(a -> a.finish));
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 435 - Non-Overlapping Intervals**:
   - Equivalent to Activity Selection: $\text{Min Removals} = N - \text{Max Kept}$.

2. **LeetCode 452 - Minimum Number of Arrows to Burst Balloons**:
   - Greedy interval intersection problem ($O(N \log N)$ time).

3. **CPU Single-Core Task Scheduling & Room Booking**:
   - Maximizing total non-overlapping meetings hosted in a single conference room.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class ActivitySelectionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ACTIVITY SELECTION GREEDY ALGORITHM DEMO      ");
        System.out.println("=================================================\n");

        ActivitySelectionMaster master = new ActivitySelectionMaster();

        // 1. Standard Activity Selection Test
        List<ActivitySelectionMaster.Activity> activities = List.of(
            new ActivitySelectionMaster.Activity(1, 5, 9),
            new ActivitySelectionMaster.Activity(2, 1, 2),
            new ActivitySelectionMaster.Activity(3, 3, 4),
            new ActivitySelectionMaster.Activity(4, 0, 6),
            new ActivitySelectionMaster.Activity(5, 5, 7),
            new ActivitySelectionMaster.Activity(6, 8, 9)
        );

        List<ActivitySelectionMaster.Activity> selected = master.selectMaxActivities(activities);
        System.out.println("1. Input Activities: " + activities);
        System.out.println("   Max Non-Overlapping Selected (" + selected.size() + " Total): " + selected);
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 435 Non-Overlapping Intervals Test
        int[][] intervals = {{1, 2}, {2, 3}, {3, 4}, {1, 3}};
        int minRemovals = master.eraseOverlapIntervals(intervals);
        System.out.println("2. LeetCode 435 Min Removals for [[1,2],[2,3],[3,4],[1,3]]: " + minRemovals + " Removals");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Activity Selection Subroutine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Finish Time Sort** | $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Sorting Space | Sort by $f_i$ ascending |
| **Greedy Scan**      | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Check $s_i \ge f_{\text{last}}$ |
| **Overall Algorithm**| $\mathbf{O(N \log N)}$ ⚡| $O(N)$ Space | Optimal Greedy Strategy |

---

## 10. Edge Cases & Boundary Handling

1. **Integer Overflow in Sorting (`b[1] - a[1]`)**:
   - Using `(a, b) -> a[1] - b[1]` causes integer underflow/overflow if intervals have negative bounds near `Integer.MIN_VALUE`.
   - **Guard**: Always use `Comparator.comparingInt(a -> a[1])` or `Integer.compare(a[1], b[1])`!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Sorting Intervals by Start Time $s_i$**:
  - Sorting by start time fails when an early-starting interval has a massive duration that blocks all future intervals. **ALWAYS sort by FINISH TIME $f_i$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Sorting by Finish Time Works:
> Picking the activity that finishes earliest leaves the **MAXIMUM possible remaining time window** for scheduling all subsequent activities, proving optimality via Exchange Arguments! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Activity Selection | Weighted Interval Scheduling | Interval Merging |
| :--- | :--- | :--- | :--- |
| **Objective** | **Maximize Count ⚡** | Maximize Total Weight | Merge Overlaps |
| **Algorithm** | **Greedy (Earliest Finish)⚡**| Dynamic Programming + BS| Greedy (Start Time Sort) |
| **Time Complexity**| **$O(N \log N)$ ⚡** | $O(N \log N)$ | $O(N \log N)$ |

---

## 14. How to Recognize This in Questions

* **"Select maximum number of non-overlapping intervals"** $\rightarrow$ Activity Selection (Sort by Finish Time).
* **"Minimum intervals to remove to make rest non-overlapping"** $\rightarrow$ LeetCode 435 ($N - \text{Selected}$).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does sorting by finish time yield an optimal greedy choice?**  
  *A:* Because finishing an activity as early as possible frees up the resource for the maximum number of remaining available activities.

* **Q: How does Activity Selection differ from Weighted Interval Scheduling?**  
  *A:* Activity Selection assigns equal weight ($1$) to each activity and is solved in $O(N \log N)$ greedy time. Weighted Interval Scheduling assigns arbitrary values $v_i$ to activities and requires Dynamic Programming ($O(N \log N)$ time).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: ACTIVITY SELECTION PROBLEM                            |
+-----------------------------------------------------------------------+
| • Greedy Choice : Sort activities by EARLIEST FINISH TIME (f_i)       |
| • Compatibility : Select activity if start >= lastSelected.finish     |
| • Flawed Choices: Start time sort FAILS! Duration sort FAILS!         |
| • Min Removals  : Min Intervals Removed = Total - Count(Selected)     |
| • Performance   : O(N log N) Sorting Time | O(1) Auxiliary Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state why Activity Selection MUST sort by finish time $f_i$ (not start time or duration).
- [ ] I can write standard Activity Selection in Java.
- [ ] I can solve LeetCode 435 (`Non-Overlapping Intervals`).
- [ ] I can solve LeetCode 452 (`Minimum Arrows to Burst Balloons`).
- [ ] I can prove Activity Selection optimality using an Exchange Argument.
