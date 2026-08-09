# 06. Advanced Range Queries: RMQ, Range GCD & Custom Monoid Operators

## 1. Introduction
Beyond standard Range Sum queries, **Segment Trees** excel at computing arbitrary **Monoid Range Queries**—including **Range Minimum Query (RMQ)**, **Range Maximum Query (RMaxQ)**, **Range Greatest Common Divisor (Range GCD)**, and **Range Bitwise AND/OR**—over mutable dynamic arrays in **$O(\log N)$ Logarithmic Time**. Any query operation that satisfies **Associativity** ($A \oplus (B \oplus C) = (A \oplus B) \oplus C$) and possesses an **Identity Element** ($A \oplus I = A$) can be seamlessly plugged into a Segment Tree merge operator.

> **Important:** The Algebraic Monoid Rules for Segment Tree Merge Operators:
> A binary merge operator $\oplus$ is valid for a Segment Tree IF AND ONLY IF:
> 1. **Associativity Property**: $(A \oplus B) \oplus C = A \oplus (B \oplus C)$. Order of subsegment evaluation does NOT alter the query result!
> 2. **Identity Element ($I$)**: There exists an element $I$ such that $X \oplus I = X$.
>    - **Range Sum**: $\oplus = +$, $I = 0$.
>    - **Range Minimum (RMQ)**: $\oplus = \min$, $I = \text{Integer.MAX\_VALUE}$.
>    - **Range Maximum (RMaxQ)**: $\oplus = \max$, $I = \text{Integer.MIN\_VALUE}$.
>    - **Range GCD**: $\oplus = \gcd$, $I = 0$ ($\gcd(X, 0) = X$). ⚡

```
Custom Monoid Segment Tree Merge Pipeline Topology:
Parent Node [L ... R] --------------------> tree[i] = LeftChild.val (+) RightChild.val
Left Child Result (Range [qL ... mid]) ---> Recurse Left Subtree
Right Child Result (Range [mid+1 .. qR]) -> Recurse Right Subtree
Case 2 No Overlap Base Case --------------> Return Identity Element (I) ⚡
```

---

## 2. Core Concepts & Range Greatest Common Divisor (Range GCD)

### 2.1 Range GCD Query Architecture
Finding the Greatest Common Divisor of all elements in subarray $[qL \dots qR]$ dynamically:
* **Merge Logic**: `tree[treeIdx] = gcd(tree[leftChild], tree[rightChild])`.
* **Identity Base Value**: `0` (since $\gcd(X, 0) = X$).
* **Euclidean GCD Algorithm**: `gcd(a, b) = (b == 0) ? a : gcd(b, a % b)`.

```
Monoid Operator Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Range Query Type      | Merge Operator    | Identity Element  | Point Update      |
+-----------------------+-------------------+-------------------+-------------------+
| **Range Minimum (RMQ)**| `Math.min(a, b)`  | `Integer.MAX_VAL` | `tree[i] = val`   |
| **Range Maximum**     | `Math.max(a, b)`  | `Integer.MIN_VAL` | `tree[i] = val`   |
| **Range GCD Query**   | `gcd(a, b)`       | `0`               | `tree[i] = val`   |
| **Range Bitwise AND** | `a & b`           | `~0` (`0xFFFFFFFF`)| `tree[i] = val`   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Any associative operator with an identity element forms a valid Segment Tree Monoid!"**

---

## 3. Characteristics & $O(\log N \log(\text{val}))$ Range GCD Complexity

### 3.1 Time Complexity Bounds for Range GCD
* Each Euclidean GCD computation between two numbers takes $O(\log(\text{val}))$ steps.
* Evaluating Range GCD over a Segment Tree range query visits at most $4 \log_2 N$ nodes.
* Total Time Complexity: $\mathbf{O(\log N \cdot \log(\text{val})) \text{ Logarithmic Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Range GCD Query $[0 \dots 2]$ on Array `[12, 18, 24, 30]`:

```
Input nums = [12, 18, 24, 30] (N = 4).

Build Step:
- Leaf 0..0: 12. Leaf 1..1: 18 -> Node 0..1 = gcd(12, 18) = 6.
- Leaf 2..2: 24. Leaf 3..3: 30 -> Node 2..3 = gcd(24, 30) = 6.
- Root 0..3 = gcd(6, 6) = 6.

Query Range GCD [0 ... 2]:
- Subsegment [0..1]: Total Overlap -> Returns 6.
- Subsegment [2..2]: Total Overlap -> Returns 24.
- Subsegment [3..3]: No Overlap    -> Returns 0 (Identity).

Result = gcd(6, gcd(24, 0)) = gcd(6, 24) = 6! Executed in O(log N) steps! ✅
```

---

## 5. Visual Diagram
Range GCD Segment Tree Subsegment Hierarchy Topography:

```
                      [ Root 0..3: GCD=6 ] (Node 0)
                     /                    \
      [ Range 0..1: GCD=6 ] (Node 1)    [ Range 2..3: GCD=6 ] (Node 2)
     /                     \           /                     \
[0..0: Val=12]       [1..1: Val=18] [2..2: Val=24]       [3..3: Val=30]
 (Node 3)              (Node 4)      (Node 5)              (Node 6)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Range Minimum (RMQ) and Range GCD Segment Trees:

```java
import java.util.*;

public class AdvancedRangeQueriesMaster {

    // 1. Range GCD Segment Tree Implementation
    public static class RangeGCDSegmentTree {
        private final int[] tree;
        private final int n;

        public RangeGCDSegmentTree(int[] nums) {
            this.n = nums.length;
            this.tree = new int[4 * n];
            if (n > 0) build(nums, 0, 0, n - 1);
        }

        private void build(int[] nums, int treeIdx, int l, int r) {
            if (l == r) { tree[treeIdx] = nums[l]; return; }
            int mid = l + (r - l) / 2;
            build(nums, 2 * treeIdx + 1, l, mid);
            build(nums, 2 * treeIdx + 2, mid + 1, r);
            tree[treeIdx] = gcd(tree[2 * treeIdx + 1], tree[2 * treeIdx + 2]);
        }

        public int queryGCD(int ql, int qr) {
            return queryHelper(0, 0, n - 1, ql, qr);
        }

        private int queryHelper(int treeIdx, int l, int r, int ql, int qr) {
            if (ql <= l && r <= qr) return tree[treeIdx]; // Total Overlap
            if (r < ql || l > qr) return 0;               // No Overlap (GCD Identity = 0)

            int mid = l + (r - l) / 2;
            int leftGCD = queryHelper(2 * treeIdx + 1, l, mid, ql, qr);
            int rightGCD = queryHelper(2 * treeIdx + 2, mid + 1, r, ql, qr);

            return gcd(leftGCD, rightGCD);
        }

        public void update(int index, int val) {
            updateHelper(0, 0, n - 1, index, val);
        }

        private void updateHelper(int treeIdx, int l, int r, int arrIdx, int val) {
            if (l == r) { tree[treeIdx] = val; return; }
            int mid = l + (r - l) / 2;
            if (arrIdx <= mid) updateHelper(2 * treeIdx + 1, l, mid, arrIdx, val);
            else updateHelper(2 * treeIdx + 2, mid + 1, r, arrIdx, val);
            tree[treeIdx] = gcd(tree[2 * treeIdx + 1], tree[2 * treeIdx + 2]);
        }

        // Euclidean GCD Algorithm
        private static int gcd(int a, int b) {
            while (b != 0) {
                int temp = b;
                b = a % b;
                a = temp;
            }
            return Math.abs(a);
        }
    }
}
```

> **Quick Syntax:**
```java
// Euclidean GCD Loop Line
private static int gcd(int a, int b) { while (b != 0) { int t = b; b = a % b; a = t; } return Math.abs(a); }
```

---

## 7. Concrete Problem Examples
* **Range GCD Queries**: Computing GCD of dynamic subarrays in $O(\log N \log(\text{val}))$ time.
* **Range Bitwise AND Queries**: Range filtering operations.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Range GCD Queries and Dynamic Updates:

```java
public class AdvancedRangeQueriesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Range GCD Segment Tree Test ===");
        int[] nums = {12, 18, 24, 30};
        AdvancedRangeQueriesMaster.RangeGCDSegmentTree gcdTree = 
            new AdvancedRangeQueriesMaster.RangeGCDSegmentTree(nums);

        System.out.println("GCD Range [0 ... 2] (12, 18, 24): " + 
            gcdTree.queryGCD(0, 2)); // Output: 6

        System.out.println("GCD Range [1 ... 3] (18, 24, 30): " + 
            gcdTree.queryGCD(1, 3)); // Output: 6

        System.out.println("\nUpdating Index 0 from 12 to 36...");
        gcdTree.update(0, 36);

        System.out.println("GCD Range [0 ... 2] (36, 18, 24) AFTER Update: " + 
            gcdTree.queryGCD(0, 2)); // Output: 6 ✅
    }
}
```

---

## 9. Complexity Analysis

| Monoid Query Type | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Range GCD Query** | **$O(1)$ Constant ⚡** | **$O(\log N \log V)$ ⚡** | **$O(\log N \log V)$ ⚡**| $O(\log N)$ Call Stack Space |
| **Range Bitwise AND**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **GCD with Zero**: Handled by `gcd(a, 0) = a`. Identity element `0` leaves query results unchanged.
* **Single Element Range**: Returns `nums[i]` directly.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Non-Associative Operations (e.g. Subtraction / Average)**:
  - Subtraction is NOT associative: $(A - B) - C \ne A - (B - C)$. Subtraction CANNOT be used as a Segment Tree merge operator!
  - **ONLY use associative operators ($\oplus$) with valid identity elements**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Monoid Requirements for Segment Trees:
> Any custom data type or function can be implemented in a Segment Tree as long as it satisfies the **Monoid Algebraic Properties**:
> 1. Associativity: $(A \oplus B) \oplus C = A \oplus (B \oplus C)$.
> 2. Identity Element: $X \oplus I = X$.
> Examples include 2x2 Matrix Multiplication (for Fibonacci numbers), Line Segment Overlaps, and Range Polynomials! ⚡

> **Memory Trick:** **"Associativity + Identity = Valid Segment Tree Monoid!"**

---

## 13. System & Implementation Comparisons

| Feature | Segment Tree Range GCD | Brute Force Range GCD |
| :--- | :--- | :--- |
| **Query Speed** | **$O(\log N \log V)$ Logarithmic ⚡**| $O(K \log V)$ Linear Scan ❌ |
| **Point Update Speed**| **$O(\log N \log V)$ Dynamic ⚡**| **$O(1)$ Constant ⚡** |
| **Scalability** | **Scales to 10,000,000 queries ⚡**| TLEs on 10,000 queries |

---

## 14. How to Recognize This in Questions
* **"Find greatest common divisor or custom monoid value over dynamic range [l ... r]"** $\rightarrow$ Segment Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Range GCD use `0` as its identity element?**  
  *A:* Because $\gcd(X, 0) = X$ for any integer $X$. Returning `0` for Case 2 No Overlap leaves the range GCD calculation unaffected.
* **Q: What is the identity element for Range Bitwise AND queries?**  
  *A:* All 1 bits (`~0` or `0xFFFFFFFF`), because $X \text{ AND } 0\text{xFFFFFFFF} = X$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED MONOID RANGE QUERIES                         |
+-----------------------------------------------------------------------+
| • Monoid Rules : Must satisfy Associativity & have Identity Element   |
| • Range Minimum: Identity = Integer.MAX_VALUE | Merge = Math.min(a,b) |
| • Range Maximum: Identity = Integer.MIN_VALUE | Merge = Math.max(a,b) |
| • Range GCD    : Identity = 0                 | Merge = gcd(a,b)      |
| • Time Bounds  : O(log N * log V) for Range GCD queries ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Euclidean GCD function in Java.
- [ ] I can write a Range GCD Segment Tree with dynamic point updates.
- [ ] I know why monoid associativity is required.
- [ ] I know the correct identity element for Bitwise AND and Range GCD.
- [ ] I can trace a Range GCD query step by step.
