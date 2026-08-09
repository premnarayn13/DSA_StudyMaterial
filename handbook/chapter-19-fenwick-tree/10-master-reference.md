# 10. Master Reference — Fenwick Trees (Binary Indexed Trees)

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 19: Fenwick Trees (Binary Indexed Trees)**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for dynamic range query algorithms, bit manipulation tricks, and technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh the LSB extraction formula `i & (-i)`, 1-based indexing requirement, $O(N)$ Optimal Linear Build loop (`tree[parent] += tree[i]`), Upward Additive Update (`i += i & (-i)`), Downward Prefix Query (`i -= i & (-i)`), Value Replacement Delta Calculation (`delta = val - nums[idx]`), 1-Line Range Sum Formula (`query(right + 1) - query(left)`), Dual BIT Range Updates ($B_1, B_2$), 2D Fenwick Trees (LeetCode 308), and Frequency BIT for LeetCode 315!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Least Significant Bit (LSB) Extraction Formula**:
  - `int lsb = i & (-i);` (Isolates lowest set bit of $i$ in Two's Complement arithmetic).
* **Upward Update Hop Formula**:
  - `i += i & (-i);` (Navigates up to parent ancestors responsible for index $i$).
* **Downward Query Hop Formula**:
  - `i -= i & (-i);` (Navigates down through disjoint subsegment ranges to index 0).
* **Optimal $O(N)$ Linear Construction Loop**:
  - `for (int i = 1; i <= n; i++) { int parent = i + (i & -i); if (parent <= n) tree[parent] += tree[i]; }`
* **0-Based Range Sum Formula**:
  - `sumRange(left, right) = query(right + 1) - query(left);`
* **Dual BIT Prefix Sum Equation**:
  - $\text{PrefixSum}(k) = k \cdot B_1.\text{query}(k) - B_2.\text{query}(k)$
* **2D Inclusion-Exclusion Submatrix Formula**:
  - `submatrixSum = Q(r2+1, c2+1) - Q(r1, c2+1) - Q(r2+1, c1) + Q(r1, c1);`

```
Fenwick Trees Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Space Allocation                  | new int[n + 1] (Saves 75% memory vs Segment Tree) |
| Least Significant Bit (LSB)       | LSB(i) = i & (-i)                                 |
| Upward Point Update Loop          | for (int i = idx; i <= n; i += i & -i) tree[i] += d;|
| Downward Prefix Query Loop        | for (int i = idx; i > 0;  i -= i & -i) sum += tree[i];|
| Optimal Linear Build Time         | O(N) Linear Time (Cascades to immediate parent) ⚡ |
| Range Sum Formula                 | query(right + 1) - query(left)                    |
| Dual BIT Range Query              | k * B1.query(k) - B2.query(k)                      |
| 2D Submatrix Query (LeetCode 308) | Q(r2+1, c2+1) - Q(r1, c2+1) - Q(r2+1, c1) + Q(r1, c1)|
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`lsb(i)` Extraction**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(1)$ Space | Bitwise `i & (-i)` |
| **Optimal $O(N)$ Build**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$N + 1$ Integers ⚡**| Immediate parent push |
| **Additive Update `add`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Stack Space ⚡**| Upward `i += i & (-i)` loop |
| **Value Update (307)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Stack Space ⚡**| Delta calculation `val - old` |
| **Prefix Query `query`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Stack Space ⚡**| Downward `i -= i & (-i)` loop |
| **Range Sum `sumRange`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Stack Space ⚡**| 1-line prefix subtraction |
| **Dual BIT Range Query**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(N)$ Space ($B_1, B_2$) | $k \cdot B_1(k) - B_2(k)$ |
| **2D Matrix Query (308)**| **$O(1)$ Constant ⚡** | **$O(\log M \log N)$ ⚡**| **$O(\log M \log N)$ ⚡**| $O(M \cdot N)$ Matrix Space| 2D Inclusion-Exclusion |
| **Smaller After (315)**| **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | $O(N)$ BIT Space | Compression + Frequency BIT |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Fenwick Trees                                                |
+-----------------------------------------------------------------------------------+
| Standard 1D `tree[]` Array           : 4 Bytes per $N$ elements ($N + 1$ Integers)     |
| Total Memory for $N = 100,000$       : 400 KB Total Memory (Fits inside L1/L2 Cache!)⚡ |
| Memory Savings vs Segment Tree       : 75% Memory Savings (400 KB vs 1.6 MB!)           |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. LSB Calculation Line
int lsb = i & (-i);

// 2. Upward Additive Point Update Loop
public void add(int i, int delta) { while (i <= n) { tree[i] += delta; i += (i & -i); } }

// 3. Downward Prefix Sum Query Loop
public int query(int i) { int sum = 0; while (i > 0) { sum += tree[i]; i -= (i & -i); } return sum; }

// 4. Value Replacement Update with Delta Calculation
public void update(int index, int val) { int delta = val - nums[index]; nums[index] = val; add(index + 1, delta); }

// 5. 1-Line Range Sum Subtraction
public int sumRange(int left, int right) { return query(right + 1) - query(left); }

// 6. Optimal O(N) Linear Build Loop
for (int i = 1; i <= n; i++) { int parent = i + (i & -i); if (parent <= n) tree[parent] += tree[i]; }

// 7. Dual BIT Prefix Sum Equation
public int prefixSum(int k) { return k * query(b1, k) - query(b2, k); }
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Using 0-Based Indexing for `tree[]` Array Access**: Accessing `tree[0]` causes `i & (-i) = 0`, crashing in an infinite loop. Always pass 1-based index `idx + 1` into BIT methods!
* **Pitfall 2: Confusing Upward vs Downward Loops**: Adding LSB during query navigates UP to ancestors, missing lower subsegments. Remember: UPDATE goes UP (`+=`), QUERY goes DOWN (`-=`).
* **Pitfall 3: Passing New Value `val` Directly to `add(idx, val)`**: Passing `val` instead of `delta = val - nums[idx]` adds new value on top of old value. Always compute `delta` first!
* **Pitfall 4: Using Fenwick Trees for Range Minimum / Maximum Queries**: Non-invertible operators like $\min$ and $\max$ cannot use prefix subtraction. Use Segment Trees for Range Min/Max!
* **Pitfall 5: Using `query(right) - query(left)`**: Subtracting `query(left)` excludes element `nums[left]`. Always use `query(right + 1) - query(left)`!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 19 (FENWICK TREES)               |
+-----------------------------------------------------------------------+
| 1. Space Allocation: ALWAYS allocate (N + 1) space (75% Memory Saved!)|
| 2. LSB Bit Formula : LSB(i) = i & (-i)                                |
| 3. Additive Update : while (i <= n) { tree[i] += delta; i += (i & -i); }|
| 4. Prefix Query    : while (i > 0)  { sum += tree[i];  i -= (i & -i); }|
| 5. Range Sum       : query(right + 1) - query(left)                   |
| 6. Value Update    : delta = val - nums[idx]; add(idx + 1, delta);    |
| 7. Optimal Build   : tree[parent] += tree[i] in O(N) linear time ⚡      |
| 8. LeetCode 315    : Compress ranks -> Backward traversal -> Query BIT|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write `add(i, delta)` and `query(i)` in Java in 6 lines of code.
- [ ] I can write the optimal $O(N)$ linear construction loop in Java.
- [ ] I can write `update(index, val)` with delta calculation for LeetCode 307.
- [ ] I can write 1-line `sumRange(left, right)`.
- [ ] I can write Dual BIT Range Updates ($B_1, B_2$).
- [ ] I can write LeetCode 308 (`Range Sum Query 2D - Mutable`).
- [ ] I can write LeetCode 315 (`Count of Smaller Numbers After Self`) using Frequency BIT.
- [ ] I know why Fenwick Trees use 75% less memory than Segment Trees.
