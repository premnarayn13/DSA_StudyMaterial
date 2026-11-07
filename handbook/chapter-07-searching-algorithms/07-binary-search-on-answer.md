# 07. Binary Search on Answer: Feasibility Functions & Search Space Optimization

## 1. Introduction
**Binary Search on Answer** is an advanced problem-solving paradigm used when an optimal answer (e.g. minimum capacity, maximum minimum distance, or minimum speed) cannot be computed directly, but candidate answers can be verified efficiently using a boolean **Feasibility Function `isPossible(mid)`**. By framing the search space over the continuous or discrete range of candidate answers $[minVal, maxVal]$, Binary Search evaluates whether a candidate value `mid` is feasible. If `isPossible(mid)` is **Monotonic** (e.g. `[false, false, ..., true, true]`), Binary Search pinpoints the exact optimal boundary in **$O(N \log (\text{Range}))$ Time** and **$O(1)$ Space**.

> **Important:** The 3 Pillars of Binary Search on Answer:
> 1. **Answer Range Definition $[low, high]$**: Determine the lower bound `low` (minimum possible candidate value) and upper bound `high` (maximum possible candidate value).
> 2. **Feasibility Function `isPossible(candidate)`**: A deterministic $O(N)$ helper function that checks if a given `candidate` parameter satisfies all problem constraints.
> 3. **Monotonic Feasibility Property**:
>    - **Minimize Maximum Problem** (e.g., Koko Eating Bananas LeetCode 875): Feasibility array looks like `[false, ..., false, true, ..., true]`. Search for **FIRST TRUE**!
>    - **Maximize Minimum Problem** (e.g., Aggressive Cows / LeetCode 1552): Feasibility array looks like `[true, ..., true, false, ..., false]`. Search for **LAST TRUE**! ⚡

```
Binary Search on Answer Feasibility Topology (Koko Eating Bananas LeetCode 875):
Candidate Speed K:     [ 1,   2,   3,   4,   5,   6,   7,   8 ]
Feasibility (H = 8):   [ F,   F,   F,   T,   T,   T,   T,   T ]
                                        ^
                              Minimum Speed K = 4! ⚡
```

---

## 2. Core Concepts & Problem Pattern Strategy Matrix

### 2.1 Binary Search on Answer Strategy Matrix
```
Binary Search on Answer Problem Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Goal / Objective  | Monotonic Array   | Binary Search Shift|
+-----------------------+-------------------+-------------------+-------------------+
| **Koko Bananas (875)**| Minimized Speed $K$| `[F, F, T, T, T]` | `high = mid - 1`  |
| **Ship Packages(1011)**| Minimized Capacity| `[F, F, T, T, T]` | `high = mid - 1`  |
| **Aggressive Cows(1552)**| Maximized Min Dist| `[T, T, T, F, F]` | `low = mid + 1`   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Minimize Max -> First TRUE (high = mid - 1); Maximize Min -> Last TRUE (low = mid + 1)!"**

---

## 3. Characteristics & $O(N \log (\text{Range}))$ Complexity Proof

### 3.1 Mathematical Proof of $O(N \log (\text{Range}))$ Time Complexity
* Let $R = high - low + 1$ be the search range size of candidate answers.
* Binary search performs $\lfloor \log_2 R \rfloor + 1$ iterations.
* In each iteration, evaluating `isPossible(mid)` takes $O(N)$ time by scanning the input array of size $N$.
* Total Time Complexity: $\mathbf{O(N \log (high - low)) \text{ Time Complexity}}$. Auxiliary Space: $\mathbf{O(1) \text{ Constant Space}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Koko Eating Bananas (LeetCode 875)

Tracing LeetCode 875 on `piles = [3, 6, 7, 11]`, `h = 8` Hours:

```
Goal: Find minimum eating speed K (piles/hour) to finish all bananas within 8 hours.

Range: low = 1, high = max(piles) = 11.

Feasibility Function isPossible(k):
Hours needed = sum( ceil(pile / k) )

Step 1: mid = 6.
        Hours = ceil(3/6) + ceil(6/6) + ceil(7/6) + ceil(11/6) = 1 + 1 + 2 + 2 = 6 <= 8 (TRUE!).
        k = 6 is feasible! Record ans = 6, try smaller speed: high = mid - 1 = 5.

Step 2: low = 1, high = 5. mid = 3.
        Hours = ceil(3/3) + ceil(6/3) + ceil(7/3) + ceil(11/3) = 1 + 2 + 3 + 4 = 10 > 8 (FALSE!).
        k = 3 is too slow! Must increase speed: low = mid + 1 = 4.

Step 3: low = 4, high = 5. mid = 4.
        Hours = ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4) = 1 + 2 + 2 + 3 = 8 <= 8 (TRUE!).
        k = 4 is feasible! Record ans = 4, try smaller speed: high = mid - 1 = 3.

Loop terminates (low = 4, high = 3).
Minimum Speed K = 4 Bananas/Hour! ✅ (O(N log(MaxPile)) Time!)
```

---

## 5. Visual Diagram: Feasibility Function Monotonicity Mapping

```
1. Minimize Maximum Candidate Search (First TRUE):
Speed Range:       [ 1 ... 3 ] | [ 4 ... 11 ]
Feasibility:       [  FALSE  ] | [  TRUE   ]
                                   ^
                              Optimal Answer (low / ans = 4)! ⚡

2. Maximize Minimum Distance Search (Last TRUE):
Dist Range:        [ 1 ... 5 ] | [ 6 ... 10 ]
Feasibility:       [  TRUE   ] | [  FALSE  ]
                       ^
                Optimal Answer (ans = 5)! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 875 (Koko Eating Bananas), LeetCode 1011 (Capacity To Ship Packages Within D Days), and LeetCode 1552 (Magnetic Force Between Two Balls / Aggressive Cows).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Binary Search on Answer Algorithms:
 * Feasibility Functions, Minimized Maximum, and Maximized Minimum Optimization.
 */
public class BinarySearchOnAnswerMaster {

    // =========================================================================
    // 1. KOKO EATING BANANAS (LeetCode 875 O(N log(MaxPile)))
    // =========================================================================
    /**
     * Finds minimum integer speed K to eat all bananas within H hours.
     * LeetCode 875 Solution.
     *
     * @param piles array of banana counts per pile
     * @param h available hours
     * @return minimum speed K
     */
    public int minEatingSpeed(int[] piles, int h) {
        if (piles == null || piles.length == 0 || h <= 0) return 0;

        int low = 1;
        int high = 0;
        for (int p : piles) high = Math.max(high, p);

        int ans = high;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canFinishBananas(piles, mid, h)) {
                ans = mid;        // Feasible speed, try searching smaller speed
                high = mid - 1;
            } else {
                low = mid + 1;    // Speed too slow, must increase
            }
        }

        return ans;
    }

    private boolean canFinishBananas(int[] piles, int speed, int maxHours) {
        long totalHours = 0;
        for (int p : piles) {
            // Integer ceiling division: (p + speed - 1) / speed
            totalHours += (p + speed - 1) / speed;
        }
        return totalHours <= maxHours;
    }

    // =========================================================================
    // 2. CAPACITY TO SHIP PACKAGES WITHIN D DAYS (LeetCode 1011 O(N log(Sum)))
    // =========================================================================
    /**
     * Finds minimum ship capacity to convey all packages within D days.
     * LeetCode 1011 Solution.
     */
    public int shipWithinDays(int[] weights, int days) {
        if (weights == null || weights.length == 0) return 0;

        int low = 0;
        int high = 0;
        for (int w : weights) {
            low = Math.max(low, w); // Capacity must at least fit heaviest single package!
            high += w;              // Capacity at most fits all packages in 1 day
        }

        int ans = high;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canShip(weights, mid, days)) {
                ans = mid;        // Feasible capacity, try searching smaller capacity
                high = mid - 1;
            } else {
                low = mid + 1;    // Capacity too small, must increase
            }
        }

        return ans;
    }

    private boolean canShip(int[] weights, int capacity, int maxDays) {
        int requiredDays = 1;
        int currentLoad = 0;

        for (int w : weights) {
            if (currentLoad + w > capacity) {
                requiredDays++;
                currentLoad = w;
            } else {
                currentLoad += w;
            }
        }

        return requiredDays <= maxDays;
    }

    // =========================================================================
    // 3. MAGNETIC FORCE BETWEEN TWO BALLS / AGGRESSIVE COWS (LeetCode 1552)
    // =========================================================================
    /**
     * Maximizes minimum distance between M balls placed in sorted basket positions.
     * LeetCode 1552 Solution (Maximized Minimum Problem).
     */
    public int maxDistance(int[] position, int m) {
        if (position == null || position.length < m) return 0;

        Arrays.sort(position); // Sort positions for distance feasibility checking!

        int low = 1; // Minimum possible distance
        int high = position[position.length - 1] - position[0]; // Maximum possible distance
        int ans = 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canPlaceBalls(position, mid, m)) {
                ans = mid;       // Feasible distance, try searching LARGER distance!
                low = mid + 1;
            } else {
                high = mid - 1;  // Distance too large, must decrease
            }
        }

        return ans;
    }

    private boolean canPlaceBalls(int[] position, int dist, int m) {
        int count = 1; // Place 1st ball at position[0]
        int lastPos = position[0];

        for (int i = 1; i < position.length; i++) {
            if (position[i] - lastPos >= dist) {
                count++;
                lastPos = position[i];
                if (count == m) return true;
            }
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Integer Ceiling Division Line
long hours = (pile + speed - 1) / speed;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 875 - Koko Eating Bananas**:
   - Minimized Maximum Rate Search ($O(N \log (\text{Max}))$.

2. **LeetCode 1011 - Capacity To Ship Packages Within D Days**:
   - Minimized Maximum Weight Capacity.

3. **LeetCode 1552 - Magnetic Force Between Two Balls**:
   - Maximized Minimum Distance (Aggressive Cows).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class BinarySearchOnAnswerDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BINARY SEARCH ON ANSWER DEMONSTRATION         ");
        System.out.println("=================================================\n");

        BinarySearchOnAnswerMaster master = new BinarySearchOnAnswerMaster();

        // 1. Koko Eating Bananas Test
        int[] piles = {3, 6, 7, 11};
        int h = 8;
        int minSpeed = master.minEatingSpeed(piles, h);
        System.out.println("1. Koko Eating Bananas " + Arrays.toString(piles) + ", H = " + h + ":");
        System.out.println("   Minimum Speed K: " + minSpeed + " Bananas/Hour");
        System.out.println("-------------------------------------------------");

        // 2. Ship Within Days Test
        int[] weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int days = 5;
        int minCap = master.shipWithinDays(weights, days);
        System.out.println("2. Ship Within " + days + " Days " + Arrays.toString(weights) + ":");
        System.out.println("   Minimum Ship Capacity: " + minCap);
        System.out.println("-------------------------------------------------");

        // 3. Magnetic Force / Aggressive Cows Test
        int[] position = {1, 2, 8, 4, 9};
        int m = 3;
        int maxMinDist = master.maxDistance(position, m);
        System.out.println("3. Maximize Min Distance (m = " + m + " balls) in " + Arrays.toString(position) + ":");
        System.out.println("   Maximized Minimum Distance: " + maxMinDist);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Answer Paradigm | Goal | Range $[low, high]$ | Time Complexity | Feasibility Function |
| :--- | :--- | :--- | :--- | :--- |
| **Koko Bananas (875)** | Minimize Speed | $[1 \dots \max(piles)]$ | $\mathbf{O(N \log (\max P))}$ | Hour Sum Check |
| **Ship Packages (1011)**| Minimize Capacity | $[\max(W) \dots \sum W]$ | $\mathbf{O(N \log (\sum W))}$| Day Count Check |
| **Magnetic Force (1552)**| Maximize Distance| $[1 \dots (pos[N-1] - pos[0])]$| $\mathbf{O(N \log (\text{Range}))}$| Ball Count Check |

---

## 10. Edge Cases & Boundary Handling

1. **Search Range Initialization for Ship Capacity**:
   - `low` MUST be initialized to $\max(weights)$ (the heaviest single package). If `low < max(weights)`, the ship capacity cannot even carry a single heavy package, causing infinite loops!

2. **Long Integer Hours Calculation**:
   - Summing hours `(p + speed - 1) / speed` over large piles can exceed 32-bit `Integer.MAX_VALUE`. Use `long totalHours`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Floating-Point Division in Integer Ceiling Calculation**:
  ```java
  // BAD: Double conversion causes precision loss for large numbers!
  int hours = (int) Math.ceil((double) p / speed);
  
  // GOOD: Overflow-safe integer ceiling formula!
  long hours = (p + speed - 1L) / speed; ⚡
  ```

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** How to Distinguish "Minimize Max" from "Maximize Min":
> * **Minimize Maximum** (e.g. min speed, min capacity): Find FIRST `TRUE` in `[F, F, T, T, T]`.
>   When feasible: `ans = mid; high = mid - 1;`
> * **Maximize Minimum** (e.g. max distance): Find LAST `TRUE` in `[T, T, T, F, F]`.
>   When feasible: `ans = mid; low = mid + 1;` ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Binary Search on Answer | Linear Scanning Candidate Range |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N \log (\text{Range}))$ Logarithmic ⚡** | $O(N \cdot \text{Range})$ Linear |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| **$O(1)$ Constant Space ⚡** |
| **Large Range Scale**| **Instant ($30$ Iterations for $10^9$) ⚡**| Crashes (1 Billion Scans) |

---

## 14. How to Recognize This in Questions

* **"Find minimum speed/capacity to finish task within D days"** $\rightarrow$ Binary Search on Answer (Minimize Max).
* **"Distribute M items to maximize the minimum distance between items"** $\rightarrow$ Binary Search on Answer (Maximize Min).

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Binary Search on Answer applicable when the input array is unsorted?**  
  *A:* Because the search space is NOT the input array! The search space is the RANGE OF CANDIDATE ANSWERS $[low, high]$, which is strictly monotonic.

* **Q: How does `(p + speed - 1) / speed` perform integer ceiling division?**  
  *A:* Adding `speed - 1` offsets exact multiples, effectively rounding any non-zero remainder up to the next integer without floating-point conversion.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY SEARCH ON ANSWER                               |
+-----------------------------------------------------------------------+
| • Paradigm    : Binary search over candidate answer range [low, high] |
| • Minimize Max: Find FIRST TRUE in [F, F, T, T] -> high = mid - 1     |
| • Maximize Min: Find LAST TRUE in [T, T, T, F]  -> low = mid + 1      |
| • Ceiling Div : (val + speed - 1) / speed                             |
| • Performance : O(N * log(Range)) Time | O(1) Auxiliary Space ⚡       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 875 (`Koko Eating Bananas`) in $O(N \log (\text{Max}))$ time.
- [ ] I can write LeetCode 1011 (`Capacity To Ship Packages`).
- [ ] I can write LeetCode 1552 (`Magnetic Force Between Two Balls / Aggressive Cows`).
- [ ] I know why `low` for ship capacity MUST be $\max(weights)$.
- [ ] I can perform integer ceiling division `(p + speed - 1) / speed`.
