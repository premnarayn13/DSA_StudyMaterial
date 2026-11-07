# 12. Longest Consecutive Sequence, HashSet Boundary Exploration & $O(N)$ Invariant Proofs

## 1. Introduction
The **Longest Consecutive Sequence Problem (LeetCode 128)** is one of the most famous array interview questions. Given an unsorted array of integers `nums`, find the length of the longest consecutive elements sequence in **$O(N)$ Linear Time**. While sorting the array takes $O(N \log N)$ time, leveraging a **HashSet** to perform **Boundary Exploration** achieves optimal $O(N)$ linear execution by identifying the exact **START of each consecutive sequence**.

> **Important:** How does a HashSet achieve $O(N)$ time instead of $O(N^2)$ brute-force exploration?
> An element `num` is the **START of a sequence ONLY IF `!set.contains(num - 1)`**!
> We skip sequence exploration for any number that is NOT a sequence start!
> As a result, **EVERY ARRAY ELEMENT IS VISITED AT MOST TWICE** (once during set population, once during sequence counting) $\implies \mathbf{O(N)\text{ Amortized Linear Time}}$! ⚡

```
Sequence Start Boundary Exploration Topology:
Array   : [ 100, 4, 200, 1, 3, 2 ]
HashSet : { 1, 2, 3, 4, 100, 200 }

Inspect 100: set.contains(99) -> false  -> Sequence Start! Count: [100] (Len 1)
Inspect 4  : set.contains(3)  -> true   -> SKIP! (Not sequence start)
Inspect 200: set.contains(199)-> false  -> Sequence Start! Count: [200] (Len 1)
Inspect 1  : set.contains(0)  -> false  -> Sequence Start! Count: 1, 2, 3, 4 (Len 4!) ⚡
```

---

## 2. Core Concepts & Sequence Start Boundary Condition

### 2.1 The Sequence Start Invariant
For any integer `val` in the input array:
* If `set.contains(val - 1) == true`: `val` is an INTERNAL element of a sequence. Do NOT explore from `val`!
* If `set.contains(val - 1) == false`: `val` is the **FIRST ELEMENT (START) of a sequence**!
  - Start a `while (set.contains(curr + 1))` loop from `curr = val`.
  - Increment `curr` and `currentStreak++`.
  - Update `longestStreak = Math.max(longestStreak, currentStreak)`.

```
Sequence Boundary Elimination Decision Table:
+-----------------------+-------------------+-------------------+-------------------+
| Number under Test     | `set.contains(num - 1)` | Sequence Role     | Action Taken      |
+-----------------------+-------------------+-------------------+-------------------+
| `100`                 | `false`           | Sequence Start    | Explore 100...    |
| `4`                   | `true` (3 exists) | Internal Member   | **SKIP (O(1)) ⚡**|
| `200`                 | `false`           | Sequence Start    | Explore 200...    |
| `1`                   | `false`           | Sequence Start    | Explore 1, 2, 3, 4|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Longest Consecutive Sequence: Explore ONLY if !set.contains(num - 1)! Yields strict O(N) linear time!"**

---

## 3. Characteristics & Mathematical Proof of $O(N)$ Time

### 3.1 Mathematical Proof of Linear Time Complexity
Let $N$ be the number of elements in the array:
1. Inserting all $N$ elements into the `HashSet` takes $O(N)$ time.
2. Iterating through each element in the `HashSet` takes $N$ iterations.
3. The inner `while` loop runs ONLY for sequence starts. Across all sequence starts, the `while` loop visits each consecutive number EXACTLY ONCE.
4. Total inner loop iterations $\le N$.
5. Total Operations = $N \text{ (Set insert)} + N \text{ (Outer loop)} + N \text{ (Inner loop)} = 3N \implies \mathbf{O(N)\text{ Linear Time Complexity}}$!

---

## 4. Internal Working Mechanics
Tracing Longest Consecutive Sequence (LeetCode 128) on `nums = [100, 4, 200, 1, 3, 2]`:

```
Step 1: Set Population -> set = {1, 2, 3, 4, 100, 200}
Step 2: Iterate elements in Set:

num = 100: set.contains(99) is false -> Sequence Start!
  - Loop curr = 100: set.contains(101) false. streak = 1. maxLen = 1.

num = 4: set.contains(3) is true -> SKIP!

num = 200: set.contains(199) is false -> Sequence Start!
  - Loop curr = 200: set.contains(201) false. streak = 1. maxLen = 1.

num = 1: set.contains(0) is false -> Sequence Start!
  - curr = 1: set.contains(2) true -> curr = 2, streak = 2
  - curr = 2: set.contains(3) true -> curr = 3, streak = 3
  - curr = 3: set.contains(4) true -> curr = 4, streak = 4
  - curr = 4: set.contains(5) false -> STOP! maxLen = max(1, 4) = 4.

num = 3: set.contains(2) is true -> SKIP!
num = 2: set.contains(1) is true -> SKIP!

Final Longest Consecutive Sequence Length = 4 ([1, 2, 3, 4]) ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
HashSet Boundary Exploration Sequence Topography:

```
Sequence 1: [ 100 ]                      (Len 1)
Sequence 2: [ 200 ]                      (Len 1)
Sequence 3: [ 1 ] -> [ 2 ] -> [ 3 ] -> [ 4 ] (Len 4 - MAX!) ✅
             ^
       (Sequence Start: !set.contains(0))
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Longest Consecutive Sequence (LeetCode 128) using HashSet Boundary Exploration and Union-Find Disjoint Set alternative:

```java
import java.util.*;

public class LongestConsecutiveSequenceMaster {

    // 1. HashSet Boundary Exploration Strategy (LeetCode 128) O(N) Time, O(N) Space
    public static int longestConsecutive(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        // Step 1: Add all elements to HashSet (eliminates duplicates)
        Set<Integer> numSet = new HashSet<>();
        for (int num : nums) {
            numSet.add(num);
        }

        int longestStreak = 0;

        // Step 2: Explore sequence starts only
        for (int num : numSet) {
            // Check if 'num' is the START of a sequence
            if (!numSet.contains(num - 1)) {
                int currentNum = num;
                int currentStreak = 1;

                // Expand sequence to the right
                while (numSet.contains(currentNum + 1)) {
                    currentNum += 1;
                    currentStreak += 1;
                }

                longestStreak = Math.max(longestStreak, currentStreak);
            }
        }

        return longestStreak;
    }

    // 2. Disjoint Set (Union-Find) Alternative Strategy O(N * alpha(N)) Time
    public static class UnionFindConsecutive {
        private final Map<Integer, Integer> parent = new HashMap<>();
        private final Map<Integer, Integer> size = new HashMap<>();

        public int longestConsecutiveUF(int[] nums) {
            if (nums == null || nums.length == 0) return 0;

            for (int num : nums) {
                if (parent.containsKey(num)) continue;
                parent.put(num, num);
                size.put(num, 1);

                if (parent.containsKey(num - 1)) {
                    union(num, num - 1);
                }
                if (parent.containsKey(num + 1)) {
                    union(num, num + 1);
                }
            }

            int maxSize = 0;
            for (int sz : size.values()) {
                maxSize = Math.max(maxSize, sz);
            }
            return maxSize;
        }

        private int find(int i) {
            if (parent.get(i) == i) return i;
            int root = find(parent.get(i));
            parent.put(i, root); // Path compression
            return root;
        }

        private void union(int i, int j) {
            int rootI = find(i);
            int rootJ = find(j);
            if (rootI != rootJ) {
                parent.put(rootI, rootJ);
                size.put(rootJ, size.get(rootJ) + size.get(rootI));
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Sequence Start Boundary Check
if (!numSet.contains(num - 1)) {
    while (numSet.contains(curr + 1)) { curr++; streak++; }
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 128 - Longest Consecutive Sequence**: Core $O(N)$ boundary exploration.
* **Continuous Range Analytics**: Finding uninterrupted consecutive date or transaction ranges.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Longest Consecutive Sequence via HashSet and Union-Find:

```java
public class LongestConsecutiveSequenceDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Longest Consecutive Sequence (HashSet Strategy) ===");
        int[] nums = {100, 4, 200, 1, 3, 2};
        int maxSeq = LongestConsecutiveSequenceMaster.longestConsecutive(nums);
        System.out.println("Longest Consecutive Length: " + maxSeq); // Output: 4 ([1, 2, 3, 4])

        System.out.println("\n=== 2. Longest Consecutive Sequence (Union-Find Strategy) ===");
        LongestConsecutiveSequenceMaster.UnionFindConsecutive uf = 
            new LongestConsecutiveSequenceMaster.UnionFindConsecutive();
        int maxSeqUF = uf.longestConsecutiveUF(nums);
        System.out.println("Union-Find Result: " + maxSeqUF); // Output: 4
    }
}
```

---

## 9. Complexity Analysis

| Implementation Strategy | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **HashSet Boundary Exploration**| **$O(N)$ Linear ⚡** | $O(N)$ Set Space | Skip non-start numbers (`!set.contains(num-1)`) |
| **Union-Find Disjoint Set** | **$O(N \cdot \alpha(N))$ ⚡**| $O(N)$ Map Space | Dynamic parent component union |
| **Sorting Approach** | $O(N \log N)$ Logarithmic | $O(1)$ Space | Sorting array before linear pass |

---

## 10. Edge Cases & Boundary Handling
* **Empty Input Array (`[]`)**: Returns `0` immediately.
* **Array with Duplicate Numbers (`[1, 2, 0, 1]`)**: Handled cleanly by `HashSet` population, which deduplicates elements.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting the `!set.contains(num - 1)` Check**:
  - Running the inner `while` loop for EVERY array element degrades time complexity from $O(N)$ linear to $O(N^2)$ quadratic!
  - **ALWAYS check `!set.contains(num - 1)` before initiating sequence loops**.
* **Iterating Over `nums` Array Instead of `numSet`**:
  - Iterating over `nums` processes duplicate values repeatedly.
  - **Iterate over `numSet` to process unique keys only**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** How to Explain $O(N)$ Linear Time for LeetCode 128:
> Interviewers will ask: *"You have a while loop inside a for loop; why is this O(N) instead of O(N^2)?"*
> Answer:
> *"The while loop executes ONLY when `num` is the START of a sequence (`!set.contains(num - 1)`). Since every consecutive number belongs to exactly one sequence, each number is visited by the inner while loop at most ONCE across the entire execution. Thus, total operations $\le 3N = O(N)$ time."*

> **Memory Trick:** **"The inner while loop runs ONLY for sequence starts! Every element is visited at most twice!"**

---

## 13. System & Implementation Comparisons

| Feature | HashSet Boundary Exploration | Sorting Strategy |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡** | $O(N \log N)$ Logarithmic |
| **Auxiliary Memory** | $O(N)$ Heap Memory | **$O(1)$ In-Place Space** |
| **Code Footprint** | ~15 Lines | ~10 Lines |

---

## 14. How to Recognize This in Questions
* **"Find longest consecutive sequence in UNSORTED array in O(N) time"** $\rightarrow$ LeetCode 128 (HashSet boundary condition `!set.contains(num - 1)`).

---

## 15. Frequently Asked Interview Questions
* **Q: Can Longest Consecutive Sequence be solved in $O(N)$ time using Union-Find?**  
  *A:* Yes! Iterate elements, add each to Union-Find. If `num - 1` or `num + 1` exists in the set, union `num` with its neighbor. Track connected component sizes to find the max length.
* **Q: Why is sorting the array NOT acceptable for LeetCode 128?**  
  *A:* Sorting takes $O(N \log N)$ time, violating the problem's strict $O(N)$ linear time complexity constraint.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LONGEST CONSECUTIVE SEQUENCE                          |
+-----------------------------------------------------------------------+
| • Sequence Start Rule: Explore ONLY IF !set.contains(num - 1)         |
| • Extension Loop: while (set.contains(curr + 1)) curr++; streak++;    |
| • Deduplication: Populating set deduplicates array elements automatically|
| • Linear Time Proof: Inner while loop visits each element AT MOST ONCE|
| • Time Complexity: O(N) Linear Time | O(N) Space ⚡                       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Longest Consecutive Sequence (LeetCode 128) in $O(N)$ time.
- [ ] I can explain why the `!set.contains(num - 1)` condition guarantees $O(N)$ time.
- [ ] I can write the Union-Find alternative solution.
- [ ] I know why sorting fails the $O(N)$ time constraint.
- [ ] I know how duplicates are handled by `HashSet`.
