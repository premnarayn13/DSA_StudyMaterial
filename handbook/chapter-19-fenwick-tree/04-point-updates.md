# 04. Fenwick Tree Point Updates, Delta Computation & Upward Bit Traversal

## 1. Introduction
A **Point Update** on a **Fenwick Tree (Binary Indexed Tree)** modifies an element at array index `index` and propagates the change to all ancestor subsegment nodes in **$O(\log N)$ Logarithmic Time**. Because a Fenwick Tree `update(idx, delta)` fundamentally performs **Additive Delta Propagation**, updating a target value directly (e.g. replacing `nums[index]` with `val` in **LeetCode 307**) requires computing the difference $\text{delta} = \text{val} - \text{nums}[\text{index}]$ before adding `delta` to all parent ancestors via `i += i & (-i)`.

> **Important:** The 2 Operational Variations of Fenwick Tree Point Updates:
> 1. **Additive Update (`add(idx, delta)`)**: Adds `delta` directly to all ancestor nodes responsible for `idx`:
>    ```java
>    for (int i = idx + 1; i <= n; i += (i & -i)) tree[i] += delta;
>    ```
> 2. **Replacement Update (`update(idx, val)` LeetCode 307)**:
>    - Compute difference: `int delta = val - nums[idx]`.
>    - Update stored array value: `nums[idx] = val`.
>    - Propagate `delta` up the tree: `add(idx, delta)`. ⚡

```
Fenwick Tree Point Additive Update Pipeline Topology:
Adding delta = +5 to 0-based Index 1 (1-based Index 2 = 0010):
Step 1: i = 2 (0010) ---> tree[2] += 5. Next i = 2 + LSB(2) = 2 + 2 = 4 (0100)
Step 2: i = 4 (0100) ---> tree[4] += 5. Next i = 4 + LSB(4) = 4 + 4 = 8 (1000)
Step 3: i = 8 (1000) ---> tree[8] += 5. Next i = 8 + LSB(8) = 16 (> N). Loop terminates! ⚡
```

---

## 2. Core Concepts & Value Replacement vs Additive Update

### 2.1 Point Update Strategy Matrix
```
Point Update Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Variant     | Delta Calculation | Index Conversion  | Upward Loop       |
+-----------------------+-------------------+-------------------+-------------------+
| **Additive Update**   | Passed as `delta` | `i = 0based + 1`  | `i += i & (-i)`   |
| **Value Replacement** | `val - nums[idx]` | `i = 0based + 1`  | `i += i & (-i)`   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Replacement Update: Compute delta = val - nums[idx] -> Loop i += i & -i to add delta to ancestors!"**

---

## 3. Characteristics & $O(\log N)$ Upward Traversal Bounds

### 3.1 Mathematical Proof of $O(\log N)$ Point Update Complexity
* Adding $\text{LSB}(i) = i \mathbin{\&} (-i)$ to index $i$ flips the rightmost `1` bit to `0` and carries `1` to the next higher bit position.
* Each addition strictly increases the value of $i$ while clearing or shifting set bits.
* For an array of size $N$, the loop `while (i <= n)` visits at most $\lceil \log_2 N \rceil$ ancestor nodes.
* Total Time Complexity: $\mathbf{O(\log N) \text{ Logarithmic Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Replacement Update `update(index=1, val=7)` on Array `[3, 2, -1, 6]` ($N=4$):

```
Initial Array: nums = [3, 2, -1, 6]. Initial tree = [0, 3, 5, -1, 10].

Call update(index=1, val=7):
1. Compute delta = 7 - nums[1] = 7 - 2 = +5.
2. Update stored array: nums[1] = 7.
3. 1-Based Index i = 1 + 1 = 2.

Upward Loop (i += i & -i):
- i = 2 (0010): tree[2] += 5 -> tree[2] = 5 + 5 = 10. Next i = 2 + 2 = 4.
- i = 4 (0100): tree[4] += 5 -> tree[4] = 10 + 5 = 15. Next i = 4 + 4 = 8 (> 4). Loop ends.

Resulting tree = [0, 3, 10, -1, 15]! All ancestors updated in 2 hops! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Fenwick Tree Upward Point Update Path Topography:

```
                  [ tree[8] += 5 ] (Index 8)
                         ^
                         | (i += LSB(4) = 8)
                  [ tree[4] += 5 ] (Index 4)
                         ^
                         | (i += LSB(2) = 4)
                  [ tree[2] += 5 ] (Target Index 2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Additive and Replacement Point Updates for Fenwick Trees (LeetCode 307):

```java
import java.util.*;

// LeetCode 307: Point Updates via Fenwick Tree
public class FenwickTreeUpdatesMaster {

    private final int[] tree;
    private final int[] nums;
    private final int n;

    public FenwickTreeUpdatesMaster(int[] nums) {
        this.nums = nums.clone();
        this.n = nums.length;
        this.tree = new int[n + 1];

        // Build Fenwick Tree using point additions O(N log N) or O(N)
        for (int i = 0; i < n; i++) {
            add(i + 1, nums[i]);
        }
    }

    // 1. Additive Point Update O(log N) Time
    public void add(int i, int delta) {
        while (i <= n) {
            tree[i] += delta;
            i += (i & -i); // Navigate upward to parent ancestor
        }
    }

    // 2. Value Replacement Update LeetCode 307 O(log N) Time
    public void update(int index, int val) {
        if (index < 0 || index >= n) return;

        int delta = val - nums[index]; // Step 1: Compute difference
        nums[index] = val;              // Step 2: Update stored array

        add(index + 1, delta);         // Step 3: Propagate delta to 1-based index
    }

    // Helper Prefix Sum Query O(log N) Time
    public int query(int i) {
        int sum = 0;
        while (i > 0) {
            sum += tree[i];
            i -= (i & -i);
        }
        return sum;
    }

    public int sumRange(int left, int right) {
        return query(right + 1) - query(left);
    }
}
```

> **Quick Syntax:**
```java
// Fenwick Tree Additive Update Loop Line
public void add(int i, int delta) { while (i <= n) { tree[i] += delta; i += (i & -i); } }
```

---

## 7. Concrete Problem Examples
* **LeetCode 307 - Range Sum Query - Mutable**: Point value updates.
* **Frequency Array Updates**: Incrementing item occurrence counts.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `update(index, val)` and `sumRange(l, r)`:

```java
public class FenwickTreeUpdatesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Fenwick Tree Point Update Test ===");
        int[] nums = {1, 3, 5};
        FenwickTreeUpdatesMaster bit = new FenwickTreeUpdatesMaster(nums);

        System.out.println("Sum Range [0 ... 2]: " + bit.sumRange(0, 2)); // Output: 9 (1+3+5)

        System.out.println("\nUpdating Index 1 to Value 2...");
        bit.update(1, 2); // Array becomes [1, 2, 5]

        System.out.println("Sum Range [0 ... 2] AFTER Update: " + 
            bit.sumRange(0, 2)); // Output: 8 (1+2+5) ✅
    }
}
```

---

## 9. Complexity Analysis

| Point Update Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`add(idx, delta)`**  | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Auxiliary Space**|
| **`update(idx, val)`** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Auxiliary Space**|

---

## 10. Edge Cases & Boundary Handling
* **Updating First Index (`index = 0`)**: Converts to 1-based index 1, updating ancestors $1, 2, 4, 8 \dots$.
* **Updating Last Index (`index = N - 1`)**: Converts to 1-based index $N$, updating ancestor $N$.

---

## 11. Common Mistakes & Anti-Patterns
* **Passing Target Value `val` Directly Into `add(idx, val)`**:
  - Passing `val` directly instead of `delta = val - nums[idx]` adds the new value on top of the old value, corrupting prefix sums!
  - **ALWAYS compute `delta = val - nums[idx]` before calling `add`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Fenwick Tree Point Updates Require Delta Calculation:
> A Fenwick Tree `tree[i]` stores cumulative additive sums.
> To change an element from $X$ to $Y$, we must add the differential change $(Y - X)$ to all ancestor nodes that incorporate element $X$ in their subsegment ranges! ⚡

> **Memory Trick:** **"Fenwick Tree updates are additive! Compute delta = new - old first!"**

---

## 13. System & Implementation Comparisons

| Feature | Fenwick Tree Point Update | Segment Tree Point Update |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(\log N)$ Logarithmic ⚡** | **$O(\log N)$ Logarithmic ⚡** |
| **Code Implementation**| **3 Lines Iterative Loop ⚡** | 15 Lines Recursive Method |
| **Auxiliary Memory** | **$O(1)$ Zero Call Stack ⚡**| $O(\log N)$ Call Stack Memory |

---

## 14. How to Recognize This in Questions
* **"Update a single element at index i and query range sums in minimum code"** $\rightarrow$ Fenwick Tree Point Update.

---

## 15. Frequently Asked Interview Questions
* **Q: How does `i += i & (-i)` navigate upward to ancestor nodes?**  
  *A:* Adding the LSB to $i$ carries the lowest set bit to the next higher binary position, matching the 1-based index of the parent subsegment node.
* **Q: Why does replacement update require storing original array values `nums[]`?**  
  *A:* To compute `delta = val - nums[index]` when `update(index, val)` is called.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FENWICK TREE POINT UPDATES                            |
+-----------------------------------------------------------------------+
| • Additive Update: void add(i, delta) { while (i <= n) { tree[i] += delta; i += (i & -i); } }|
| • Replacement   : delta = val - nums[index]; nums[index] = val; add(index + 1, delta);|
| • Direction     : Upward hop (i += i & -i)                            |
| • Time Bounds   : O(log N) Logarithmic Time (Zero stack memory!) ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `add(i, delta)` in Java in 3 lines.
- [ ] I can write `update(index, val)` with delta calculation.
- [ ] I know why delta calculation `val - nums[idx]` is mandatory.
- [ ] I can trace upward update hops for Index 2.
- [ ] I can state the space complexity ($O(1)$ auxiliary memory).
