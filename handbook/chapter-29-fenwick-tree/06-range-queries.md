# 06. Fenwick Tree Range Queries, Prefix Subtraction Invariant & Limitations

## 1. Introduction
A **Range Query** on a **Fenwick Tree (Binary Indexed Tree)** computes the cumulative sum of elements over an arbitrary 0-based range $[\text{left} \dots \text{right}]$ in **$O(\log N)$ Logarithmic Time**. Because a Fenwick Tree natively computes prefix sums from index 1 up to $K$, an arbitrary range query is executed using the fundamental **Prefix Subtraction Invariant**: subtract the prefix sum up to $\text{left} - 1$ from the prefix sum up to $\text{right}$, executing **2 Prefix Queries** in **$O(\log N)$ Time**.

> **Important:** The Prefix Subtraction Invariant for Range Sums:
> For any 0-based range $[\text{left} \dots \text{right}]$:
> $$\text{RangeSum}(\text{left}, \text{right}) = \text{PrefixSum}(0 \dots \text{right}) - \text{PrefixSum}(0 \dots \text{left} - 1)$$
> 1. In 1-based indexing: `query(right + 1) - query(left)`.
> 2. **Operational Constraint**: Prefix subtraction requires the merge operator to have an **INVERSE OPERATOR** (e.g. addition $+$ has inverse subtraction $-$).
> 3. **Range Min/Max Limitation**: Non-invertible operators like $\min$ and $\max$ CANNOT be queried over arbitrary ranges using prefix subtraction! Segment Trees are required for Range Min/Max! ⚡

```
Prefix Subtraction Invariant Topology (Querying Range [2 ... 5]):
PrefixSum(0 ... 5): [0] + [1] + [2] + [3] + [4] + [5]
PrefixSum(0 ... 1): [0] + [1]
-----------------------------------------------------------------
Subtraction:                   [2] + [3] + [4] + [5] = RangeSum(2, 5)! ⚡
```

---

## 2. Core Concepts & Prefix Subtraction Invariant

### 2.1 The Prefix Subtraction Equation
For 0-based input array indices $0 \le \text{left} \le \text{right} < N$:
* **1-Based Conversion**:
  - $\text{right} \to \text{1basedRight} = \text{right} + 1$.
  - $\text{left} - 1 \to \text{1basedLeftMinus1} = (\text{left} - 1) + 1 = \text{left}$.
* **Final Range Formula**:
  $$\text{sumRange}(\text{left}, \text{right}) = \text{query}(\text{right} + 1) - \text{query}(\text{left})$$

```
Range Query Operator Compatibility Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Query Operator        | Has Inverse?      | Fenwick Range Query| Alternative DS   |
+-----------------------+-------------------+-------------------+-------------------+
| **Range Sum Query**   | YES ($+ \to -$)   | **$O(\log N)$ ⚡**| Fenwick Tree      |
| **Range XOR Query**   | YES ($\oplus \to \oplus$)| **$O(\log N)$ ⚡**| Fenwick Tree      |
| **Range Minimum (RMQ)**| NO (No inverse)  | Complex / Limited | **Segment Tree ⚡**|
| **Range Maximum**     | NO (No inverse)   | Complex / Limited | **Segment Tree ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Range Sum Formula: query(right + 1) - query(left)! Requires inverse subtraction operator!"**

---

## 3. Characteristics & $O(\log N)$ Range Query Bounds

### 3.1 Time Complexity Bounds
* Executing `sumRange(left, right)` calls `query(right + 1)` and `query(left)`.
* Each `query()` call takes at most $\lceil \log_2 N \rceil$ downward hops.
* Total Time Complexity: $2 \times O(\log N) = \mathbf{O(\log N) \text{ Logarithmic Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Range Sum `sumRange(left = 2, right = 5)` on Array `[3, 2, -1, 6, 5, 4]` ($N=6$):

```
Input Array nums = [3, 2, -1, 6, 5, 4]. Target range [2..5] elements: -1 + 6 + 5 + 4 = 14.

Call sumRange(2, 5):
1. Call query(right + 1 = 6):
   - 1-based index 6: sum = 3 + 2 + -1 + 6 + 5 + 4 = 19.

2. Call query(left = 2):
   - 1-based index 2: sum = 3 + 2 = 5.

3. Subtract:
   - sumRange(2, 5) = query(6) - query(2) = 19 - 5 = 14!

Exact range sum calculated in 2 prefix queries! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Prefix Subtraction Range Sum Topography:

```
PrefixSum(6): |====== 19 ======| (Elements 0, 1, 2, 3, 4, 5)
PrefixSum(2): |== 5 ==|          (Elements 0, 1)
              ------------------
RangeSum(2,5):        |== 14 ==| (Elements 2, 3, 4, 5) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Range Sum and Range XOR queries via Fenwick Tree:

```java
import java.util.*;

// LeetCode 307: Range Queries via Fenwick Tree
public class FenwickTreeRangeQueriesMaster {

    private final int[] tree;
    private final int[] nums;
    private final int n;

    public FenwickTreeRangeQueriesMaster(int[] nums) {
        this.nums = nums.clone();
        this.n = nums.length;
        this.tree = new int[n + 1];

        // Optimal O(N) Linear Construction
        for (int i = 0; i < n; i++) tree[i + 1] = nums[i];
        for (int i = 1; i <= n; i++) {
            int parent = i + (i & -i);
            if (parent <= n) tree[parent] += tree[i];
        }
    }

    // Downward Prefix Query [1 ... i] O(log N) Time
    private int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= (i & -i);
        }
        return sum;
    }

    // Range Sum Query [left ... right] (0-based) O(log N) Time
    public int sumRange(int left, int right) {
        if (left < 0 || right >= n || left > right) return 0;
        return query(right + 1) - query(left); // Prefix Subtraction Invariant
    }

    // Value Replacement Update LeetCode 307 O(log N) Time
    public void update(int index, int val) {
        if (index < 0 || index >= n) return;
        int delta = val - nums[index];
        nums[index] = val;

        int i = index + 1;
        while (i <= n) {
            tree[i] += delta;
            i += (i & -i);
        }
    }
}
```

> **Quick Syntax:**
```java
// Range Sum Line: return query(right + 1) - query(left);
```

---

## 7. Concrete Problem Examples
* **LeetCode 307 - Range Sum Query - Mutable**: Core range sum problem.
* **Range Bitwise XOR Queries**: $X \oplus X = 0$ allows range XOR queries `queryXOR(right + 1) ^ queryXOR(left)`.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `sumRange(left, right)`:

```java
public class FenwickTreeRangeQueriesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Fenwick Tree Range Query Test ===");
        int[] nums = {3, 2, -1, 6, 5, 4};
        FenwickTreeRangeQueriesMaster bit = new FenwickTreeRangeQueriesMaster(nums);

        System.out.println("Range Sum [2 ... 5] (-1+6+5+4): " + 
            bit.sumRange(2, 5)); // Output: 14

        System.out.println("Range Sum [0 ... 2] (3+2+-1):   " + 
            bit.sumRange(0, 2)); // Output: 4

        System.out.println("\nUpdating Index 2 from -1 to 9...");
        bit.update(2, 9); // Array becomes [3, 2, 9, 6, 5, 4]

        System.out.println("Range Sum [2 ... 5] AFTER Update: " + 
            bit.sumRange(2, 5)); // Output: 24 (9+6+5+4) ✅
    }
}
```

---

## 9. Complexity Analysis

| Range Query Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`sumRange(left, right)`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Auxiliary Space**|

---

## 10. Edge Cases & Boundary Handling
* **Single Element Range (`left == right`)**: Returns `nums[left]`. `query(left + 1) - query(left) = nums[left]`.
* **Full Array Range (`0 ... N - 1`)**: Returns `query(N) - query(0) = query(N)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `query(right) - query(left)` Instead of `query(right + 1) - query(left)`**:
  - Subtracting `query(left)` from `query(right)` subtracts `nums[left]`, excluding `nums[left]` from the result range!
  - **ALWAYS use `query(right + 1) - query(left)` to include `nums[left]`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Fenwick Trees Struggle with Range Minimum / Maximum (RMQ):
> Computing Range Sum uses subtraction (the inverse of addition): $\text{RangeSum}(L, R) = S_R - S_{L-1}$.
> Minimum and Maximum operations do NOT have inverse functions (you cannot "subtract" a minimum value to recover the previous minimum).
> Therefore, while Range Sum is trivial in Fenwick Trees, **Range Min/Max queries require Segment Trees**! ⚡

> **Memory Trick:** **"Range Sum = Fenwick Tree! Range Min/Max = Segment Tree!"**

---

## 13. System & Implementation Comparisons

| Feature | Fenwick Tree Range Query | Segment Tree Range Query |
| :--- | :--- | :--- |
| **Operator Requirement** | Must be Invertible ($+$ or $\oplus$) | Any Associative Monoid (Sum, Min, Max, GCD) |
| **Implementation** | **1-Line Subtraction ⚡** | 15-Line 3-Case Recursion |
| **Time Complexity** | **$O(\log N)$ Logarithmic ⚡** | **$O(\log N)$ Logarithmic ⚡** |

---

## 14. How to Recognize This in Questions
* **"Perform Range Sum Query over dynamic array with dynamic element updates"** $\rightarrow$ Fenwick Tree Range Query.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is the formula for 0-based range sum `query(right + 1) - query(left)`?**  
  *A:* Because `query(right + 1)` calculates sum $0 \dots \text{right}$, and `query(left)` calculates sum $0 \dots \text{left} - 1$. Subtracting them isolates range $\text{left} \dots \text{right}$.
* **Q: Can Fenwick Trees support Range XOR queries?**  
  *A:* Yes! Because $X \oplus X = 0$ (XOR is its own inverse), `queryXOR(right + 1) ^ queryXOR(left)` computes range XOR.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FENWICK TREE RANGE QUERIES                            |
+-----------------------------------------------------------------------+
| • Range Sum Formula: sumRange(left, right) = query(right + 1) - query(left)|
| • Invariant Rule   : Prefix subtraction requires invertible operator (+) |
| • Limitation       : Range Min/Max queries CANNOT use prefix subtraction|
| • Time Bounds      : O(log N) Logarithmic Time (2 prefix queries) ⚡    |
| • Code Simplicity  : 1 line of subtraction! ⚡                         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `sumRange(left, right)` in Java in 1 line.
- [ ] I can explain the Prefix Subtraction Invariant.
- [ ] I know why `query(left)` is subtracted (not `query(left - 1)`).
- [ ] I know why Segment Trees are needed for Range Min/Max queries.
- [ ] I can trace range subtraction for Range $[2 \dots 5]$.
