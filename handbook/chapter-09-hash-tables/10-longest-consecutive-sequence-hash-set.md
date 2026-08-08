# 10. Longest Consecutive Sequence & Set Boundary Scanning

## 1. Introduction
Finding the **Longest Consecutive Sequence** in an unsorted array of integers (LeetCode 128) is a benchmark hard-level technical coding interview question that tests optimal algorithm design. Given an unsorted array `nums`, we must find the length of the longest sequence of consecutive elements (e.g. `[1, 2, 3, 4]`) without requiring elements to be contiguous in the original array. While sorting the array takes $O(N \log N)$ time, leveraging a **Hash Set Sequence Boundary Start Filter (`!set.contains(num - 1)`)** solves this problem in **Strict $O(N)$ linear time and $O(N)$ space**.

> **Important:** The key to achieving $O(N)$ time is skipping inner expansion loops for elements that are NOT sequence starting points. We ONLY expand a sequence if **`num - 1` is NOT present in the Hash Set**!

```
Longest Consecutive Sequence Strategy Matrix:
+-----------------------------------------------------------------------------------+
| Sort Array & Scan    : Sort O(N log N) + Scan -> O(N log N) Time, Modifies Array |
| Set Boundary Scan    : Hash Set + (!set.contains(n-1)) -> O(N) Linear Time ⚡    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Amortized $O(N)$ Time Proof

### 2.1 The Sequence Starting Point Invariant
A number $x$ in a set $S$ is the **Beginning / Start of a Consecutive Sequence** if and only if:

$$x - 1 \notin S$$

* If $x - 1 \in S$, then $x$ is NOT the start of the sequence (it is a middle or end element of a sequence starting at some smaller value $y < x$).
* By enforcing `if (!set.contains(num - 1))`, we guarantee that each consecutive sequence is expanded **EXACTLY ONCE** from its minimum starting boundary element!

### 2.2 Amortized $O(N)$ Linear Time Proof
Critics often assume that having a `while` loop inside a `for` loop produces $O(N^2)$ quadratic time.
Here is the mathematical proof that the nested loops run in **Strict $O(N)$ Time**:
1. Inserting all $N$ elements into `HashSet` takes $O(N)$ time.
2. The outer loop iterates over each number in `set` exactly once ($N$ iterations).
3. The `while (set.contains(currentNum + 1))` loop executes ONLY when `num - 1` is absent.
4. Each number in the array belongs to exactly ONE consecutive sequence. Therefore, every element $x$ is visited inside the `while` loop at most ONCE across the entire execution of the algorithm!
5. Total inner `while` iterations summed across all sequences $\le N \implies \mathbf{O(N) + O(N) = O(N)\text{ Linear Time}}$.

```
Amortized Analysis Breakdown:
Outer iterations: N steps
Inner while loops: Sum of all sequence lengths = N steps
Total Operations = N + N = 2N -> O(N) Linear Time Complexity!
```

> **Memory Trick:** **"Only expand sequence if (!set.contains(num - 1))! Each number visited at most twice total!"**

---

## 3. Characteristics & Problem Variations

### 3.1 Hash Set vs Union-Find (Disjoint Set Union)
While Hash Set boundary scanning is the standard $O(N)$ approach, the problem can also be solved using **Union-Find**:
* For each number $x$, union $x$ with $x + 1$ if $x + 1$ exists in the set.
* The maximum component size in Union-Find represents the longest consecutive sequence.
* Time Complexity: $O(N \cdot \alpha(N))$ using path compression.

---

## 4. Internal Working Mechanics
Tracing Longest Consecutive Sequence (LeetCode 128) on `nums = [100, 4, 200, 1, 3, 2]`:

```
Step 1: Build HashSet = {100, 4, 200, 1, 3, 2}

Iterate over HashSet:
- num = 100: Check contains(99) -> FALSE! 100 IS A START!
             Expand: 101 in set? No. Length = 1. maxLen = max(0, 1) = 1.

- num = 4  : Check contains(3) -> TRUE! 4 is NOT a start. SKIP!

- num = 200: Check contains(199) -> FALSE! 200 IS A START!
             Expand: 201 in set? No. Length = 1. maxLen = max(1, 1) = 1.

- num = 1  : Check contains(0) -> FALSE! 1 IS A START!
             Expand:
               - 2 in set? YES -> curr=2, len=2
               - 3 in set? YES -> curr=3, len=3
               - 4 in set? YES -> curr=4, len=4
               - 5 in set? NO.
             Length = 4. maxLen = max(1, 4) = 4.

- num = 3  : Check contains(2) -> TRUE! 3 is NOT a start. SKIP!
- num = 2  : Check contains(1) -> TRUE! 2 is NOT a start. SKIP!

Final Result: maxLen = 4 (Sequence: [1, 2, 3, 4]) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
Set Boundary Skipping vs Sequence Expansion Topology:

```
HashSet Elements: { 100,  4,  200,  1,  3,  2 }

Check (x - 1):
  100 - 1 = 99  (Not in set) ---> START! Expand [100] -> Length 1
    4 - 1 = 3   (In set)    ---> SKIP! (Not a start)
  200 - 1 = 199 (Not in set) ---> START! Expand [200] -> Length 1
    1 - 1 = 0   (Not in set) ---> START! Expand [1, 2, 3, 4] -> Length 4 ⚡
    3 - 1 = 2   (In set)    ---> SKIP! (Not a start)
    2 - 1 = 1   (In set)    ---> SKIP! (Not a start)

Notice: Inner while loop executes ONLY ONCE for sequence starting at 1!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Longest Consecutive Sequence (LeetCode 128) using Hash Set and Union-Find:

```java
import java.util.*;

public class LongestConsecutiveMaster {

    // 1. Hash Set Boundary Scan O(N) Time, O(N) Space - OPTIMAL
    public static int longestConsecutive(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        Set<Integer> numSet = new HashSet<>();
        for (int num : nums) {
            numSet.add(num);
        }

        int maxLength = 0;

        for (int num : numSet) {
            // ONLY start expanding if num is the minimum element of a sequence!
            if (!numSet.contains(num - 1)) {
                int currentNum = num;
                int currentStreak = 1;

                while (numSet.contains(currentNum + 1)) {
                    currentNum += 1;
                    currentStreak += 1;
                }

                maxLength = Math.max(maxLength, currentStreak);
            }
        }

        return maxLength;
    }

    // 2. Alternative Union-Find Solution O(N * α(N)) Time, O(N) Space
    public static class UnionFindSolution {
        static class DisjointSet {
            private final Map<Integer, Integer> parent = new HashMap<>();
            private final Map<Integer, Integer> size = new HashMap<>();

            public void add(int x) {
                if (!parent.containsKey(x)) {
                    parent.put(x, x);
                    size.put(x, 1);
                }
            }

            public int find(int i) {
                if (parent.get(i) == i) return i;
                int root = find(parent.get(i));
                parent.put(i, root); // Path compression
                return root;
            }

            public void union(int i, int j) {
                int rootI = find(i);
                int rootJ = find(j);
                if (rootI != rootJ) {
                    parent.put(rootI, rootJ);
                    size.put(rootJ, size.get(rootJ) + size.get(rootI));
                }
            }

            public int getMaxSize() {
                int max = 0;
                for (int s : size.values()) {
                    max = Math.max(max, s);
                }
                return max;
            }

            public boolean contains(int x) {
                return parent.containsKey(x);
            }
        }

        public static int longestConsecutiveUF(int[] nums) {
            if (nums == null || nums.length == 0) return 0;

            DisjointSet uf = new DisjointSet();
            for (int num : nums) uf.add(num);

            for (int num : nums) {
                if (uf.contains(num + 1)) {
                    uf.union(num, num + 1);
                }
            }

            return uf.getMaxSize();
        }
    }
}
```

> **Quick Syntax:**
```java
// Boundary Start Check Filter
if (!numSet.contains(num - 1)) {
    while (numSet.contains(curr + 1)) { curr++; streak++; }
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 128 - Longest Consecutive Sequence**: Hash Set sequence boundary scanning.
* **LeetCode 298 - Binary Tree Longest Consecutive Sequence**: Tree traversal consecutive sequence.
* **LeetCode 674 - Longest Continuous Increasing Subarray**: Sliding window on contiguous indices.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Hash Set boundary scanning and Union-Find algorithms:

```java
public class LongestConsecutiveDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Hash Set Boundary Scan ===");
        int[] nums1 = {100, 4, 200, 1, 3, 2};
        System.out.println("Input: " + Arrays.toString(nums1));
        System.out.println("Longest Streak: " + LongestConsecutiveMaster.longestConsecutive(nums1)); // Output: 4 ([1, 2, 3, 4])

        int[] nums2 = {0, 3, 7, 2, 5, 8, 4, 6, 0, 1};
        System.out.println("\nInput: " + Arrays.toString(nums2));
        System.out.println("Longest Streak: " + LongestConsecutiveMaster.longestConsecutive(nums2)); // Output: 9 ([0..8])

        System.out.println("\n=== 2. Union-Find Solution ===");
        System.out.println("Longest Streak (UF): " + LongestConsecutiveMaster.UnionFindSolution.longestConsecutiveUF(nums1)); // Output: 4
    }
}
```

---

## 9. Complexity Analysis

| Strategy | Time Complexity | Auxiliary Space | Key Mechanism |
| :--- | :--- | :--- | :--- |
| **Set Boundary Filter** | **$O(N)$ Linear ⚡** | **$O(N)$ Hash Set** | Skip if `set.contains(n - 1)` |
| **Sorting Array** | $O(N \log N)$ | $O(1)$ or $O(N)$ | Sort array, scan adjacent items |
| **Union-Find (DSU)** | **$O(N \cdot \alpha(N))$ ⚡**| $O(N)$ Parent Map | Union $x$ with $x + 1$ |

---

## 10. Edge Cases & Boundary Handling
* **Empty Array (`nums = []`)**: Return 0 immediately.
* **Array with Duplicates (`nums = [1, 2, 0, 1]`)**: HashSet deduplicates numbers automatically, producing set `{0, 1, 2}` and returning correct length 3.
* **Negative Numbers (`nums = [-5, -4, -3, 0, 1]`)**: `HashSet` lookup handles negative integer arithmetic cleanly.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting the `!numSet.contains(num - 1)` Start Check**: Expanding from EVERY number in the set degrades time complexity to $O(N^2)$ on sequences like `[1, 2, 3, 4, 5]`!
* **Iterating over Array `nums` instead of `numSet`**: Iterating over `nums` processes duplicates multiple times. Always iterate over `numSet`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `!numSet.contains(num - 1)` Guarantees $O(N)$ Time:
> If an array has a sequence of length 1,000 (e.g. `1..1000`), iterating over numbers 2 through 1000 will fail the `!contains(n-1)` check and instantly skip!
> The inner `while` loop runs ONLY for number 1, scanning 1,000 steps once.
> Total operations across all elements = $N + N = 2N \implies \mathbf{O(N)\text{ Linear Time}}$.

> **Memory Trick:** **"Check (n - 1) absent to find START of sequence! Never expand from middle elements!"**

---

## 13. System & Implementation Comparisons

| Feature | Sorting Approach | Hash Set Boundary Approach |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log N)$ | **$O(N)$ Linear Time ⚡** |
| **Auxiliary Space** | $O(1)$ In-Place | $O(N)$ Hash Set |
| **Modifies Input Array**| YES (Sorts array) | **NO (Read-Only Input)** |

---

## 14. How to Recognize This in Questions
* **"Find longest sequence of consecutive elements in an unsorted array in O(N) time"** $\rightarrow$ LeetCode 128 (Hash Set Boundary Filter `!set.contains(n - 1)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does iterating over `numSet` with a `while` loop inside not take $O(N^2)$ time?**  
  *A:* Because the `while` loop executes ONLY when `num - 1` is absent (at the sequence start). Every sequence is traversed exactly once. Across all sequences, each element is visited at most twice (once in outer loop, once in inner `while` loop), guaranteeing $O(N)$ time.
* **Q: How to handle duplicate numbers in the array?**  
  *A:* Inserting elements into `Set<Integer> numSet` automatically removes all duplicate entries, ensuring sequences are evaluated over unique values.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LONGEST CONSECUTIVE SEQUENCE                          |
+-----------------------------------------------------------------------+
| • Core Condition: Start sequence ONLY if (!set.contains(num - 1))     |
| • Sequence Expansion: while (set.contains(curr + 1)) { curr++; streak++; }|
| • Mathematical Time Proof: Outer N + Inner N = 2N total operations -> O(N)|
| • Deduplication: Set handles duplicate values automatically            |
| • Edge Cases: Empty array -> return 0; Handles negative numbers cleanly|
| • Complexity: O(N) Linear Time | O(N) Auxiliary Set Space             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the `!set.contains(num - 1)` sequence start filter.
- [ ] I can prove why nested loops execute in $O(N)$ amortized time.
- [ ] I can implement LeetCode 128 in under 4 minutes.
- [ ] I know why HashSet automatically handles duplicate values.
- [ ] I can explain the Union-Find alternative approach.
