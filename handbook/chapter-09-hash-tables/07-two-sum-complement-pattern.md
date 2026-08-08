# 07. Two-Sum & Complement Indexing Patterns

## 1. Introduction
The **Two-Sum Complement Pattern** is the foundational algorithmic problem that introduces candidate engineers to the power of hash-based lookups in technical coding interviews (LeetCode 1 - Two Sum). Given an array of integers `nums` and a target value `target`, the goal is to find two numbers that sum up to `target`. While a naive brute-force nested loop evaluates all pairs in $O(N^2)$ time, utilizing a **Hash Map for Instant Complement Lookup (`complement = target - nums[i]`)** reduces the time complexity to **$O(N)$ linear time**.

> **Important:** The single-pass Hash Map approach inserts elements into the map AFTER checking if their complement already exists. This guarantees that an element cannot be paired with ITSELF (avoiding index reuse errors) in a single clean pass!

```
Two-Sum Complexity Transformation:
+-----------------------------------------------------------------------------------+
| Brute Force Pair Scanning    : Evaluate all N*(N-1)/2 pairs  -> O(N²) Time        |
| Sorting + Two Pointers       : Sort O(N log N) + Two Pointers -> O(N log N) Time  |
| Hash Map Complement Lookup   : Single Pass Hash Complement   -> O(N) Linear Time ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Algebra

### 2.1 The Algebraic Complement Identity
For any two numbers $a$ and $b$ at indices $i$ and $j$ ($i \neq j$) satisfying:

$$a + b = \text{target} \implies b = \text{target} - a$$

Where $b$ is the **Algebraic Complement** of $a$.

### 2.2 Brute Force vs Sorting vs Hash Map
1. **Brute Force ($O(N^2)$ Time, $O(1)$ Space)**:
   Compare every pair `(nums[i], nums[j])` for $0 \le i < j < N$. Requires $\frac{N(N-1)}{2}$ comparisons.
2. **Sort + Two Pointers ($O(N \log N)$ Time, $O(N)$ Space)**:
   Sort elements while preserving original indices. Use left and right pointers moving inward.
3. **Hash Map Single-Pass Lookup ($O(N)$ Time, $O(N)$ Space)**:
   As we iterate through `nums` at index $i$ with value `curr = nums[i]`:
   - Compute `complement = target - curr`.
   - Check if `map.containsKey(complement)`.
   - If YES: Solution found! Return `new int[]{map.get(complement), i}`.
   - If NO: Store current element and index into map `map.put(curr, i)` and continue.

```
Two-Sum Algorithmic Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Strategy              | Time Complexity   | Space Complexity  | Preserves Indices?|
+-----------------------+-------------------+-------------------+-------------------+
| Brute Force           | O(N²)             | O(1) Constant     | YES               |
| Sort + Two Pointers   | O(N log N)        | O(N) Pair Array   | Requires Wrapper  |
| Hash Map Complement   | O(N) Linear ⚡    | O(N) Hash Space   | YES (Instant) ⚡  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Complement = Target - nums[i]! Check map FIRST, then map.put(nums[i], i)!"**

---

## 3. Generalizing to Variations (Two-Sum Data Structure, 3Sum, 4Sum, K-Sum)

### 3.1 Two-Sum III - Data Structure Design (LeetCode 170)
* **`add(val)`**: Store numbers in a frequency map `map.put(val, map.getOrDefault(val, 0) + 1)`.
* **`find(value)`**: Iterate over map keys. For key $k$, check `complement = value - k`.
  * If $k \neq \text{complement}$, return true if `map.containsKey(complement)`.
  * If $k == \text{complement}$, return true if `map.get(k) >= 2` (handles duplicate requirement).

### 3.2 3Sum & 4Sum Reduction
Hash Map complement lookup can be extended to 3Sum ($a + b + c = 0$) and 4Sum ($a + b + c + d = \text{target}$). However, for 3Sum and 4Sum where returning **unique value triplets/quadruplets** is required, **Sorting + Two Pointers** is usually preferred over Hash Maps because skip-logic for duplicate values is cleaner without Hash Set overhead.

---

## 4. Internal Working Mechanics
Tracing Single-Pass Two-Sum on `nums = [2, 7, 11, 15], target = 9`:

```
Init: map = {} (Value -> Index)

i = 0: curr = 2. complement = 9 - 2 = 7.
       Check map.containsKey(7) -> false.
       map.put(2, 0) | Map: {2: 0}

i = 1: curr = 7. complement = 9 - 7 = 2.
       Check map.containsKey(2) -> TRUE!
       Match found at map.get(2) = index 0.

Result: return new int[]{0, 1} ✅ (1 Iteration, Linear O(N) Time!)
```

---

## 5. Visual Diagram
Single-Pass Complement Lookup State Flow:

```
Array: [ 3,  2,  4 ]   Target = 6

Step 1 (i=0, val=3): Complement = 6 - 3 = 3
                     Map check 3 -> Not Found
                     Map put: {3 -> 0}

Step 2 (i=1, val=2): Complement = 6 - 2 = 4
                     Map check 4 -> Not Found
                     Map put: {3 -> 0, 2 -> 1}

Step 3 (i=2, val=4): Complement = 6 - 4 = 2
                     Map check 2 -> FOUND at Index 1!
                     Return [1, 2] ✅
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite covering Two Sum (LeetCode 1), Two Sum II Sorted Array (LeetCode 167), Two Sum III Data Structure (LeetCode 170), and 4Sum II (LeetCode 454):

```java
import java.util.*;

public class TwoSumPatternMaster {

    // 1. Two Sum (LeetCode 1) O(N) Time, O(N) Space - Single Pass Hash Map
    public static int[] twoSum(int[] nums, int target) {
        if (nums == null || nums.length < 2) return new int[0];

        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];

            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }

            map.put(nums[i], i);
        }

        return new int[0]; // No solution found
    }

    // 2. Two Sum II - Input Array Is Sorted (LeetCode 167) O(N) Time, O(1) Space
    public static int[] twoSumSorted(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];

            if (sum == target) {
                return new int[]{left + 1, right + 1}; // 1-indexed output
            } else if (sum < target) {
                left++;
            } else {
                right--;
            }
        }

        return new int[0];
    }

    // 3. Two Sum III - Data Structure Design (LeetCode 170)
    public static class TwoSumDS {
        private final Map<Integer, Integer> freqMap = new HashMap<>();

        public void add(int number) {
            freqMap.put(number, freqMap.getOrDefault(number, 0) + 1);
        }

        public boolean find(int value) {
            for (int key : freqMap.keySet()) {
                int complement = value - key;

                if (complement == key) {
                    if (freqMap.get(key) >= 2) return true;
                } else {
                    if (freqMap.containsKey(complement)) return true;
                }
            }
            return false;
        }
    }

    // 4. 4Sum II (LeetCode 454) O(N²) Time, O(N²) Space
    public static int fourSumCount(int[] nums1, int[] nums2, int[] nums3, int[] nums4) {
        Map<Integer, Integer> sumMap = new HashMap<>();

        // Store all pairwise sums of nums1 and nums2
        for (int a : nums1) {
            for (int b : nums2) {
                int sum = a + b;
                sumMap.put(sum, sumMap.getOrDefault(sum, 0) + 1);
            }
        }

        int count = 0;

        // Search for negative complement -(c + d) in sumMap
        for (int c : nums3) {
            for (int d : nums4) {
                int targetComplement = -(c + d);
                count += sumMap.getOrDefault(targetComplement, 0);
            }
        }

        return count;
    }
}
```

> **Quick Syntax:**
```java
// Single Pass Check-First Pattern
int complement = target - nums[i];
if (map.containsKey(complement)) return new int[]{map.get(complement), i};
map.put(nums[i], i);
```

---

## 7. Concrete Problem Examples
* **LeetCode 1 - Two Sum**: Standard Single-Pass Hash Map complement lookup.
* **LeetCode 167 - Two Sum II**: Two pointers on sorted array in $O(1)$ space.
* **LeetCode 454 - 4Sum II**: Dividing 4 arrays into two pairs of $O(N^2)$ hash lookups ($A+B = -(C+D)$).

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Two Sum variants and 4Sum II:

```java
import java.util.Arrays;

public class TwoSumPatternDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Standard Two Sum ===");
        int[] nums = {2, 7, 11, 15};
        int target = 9;
        System.out.println("Input: " + Arrays.toString(nums) + ", Target: " + target);
        System.out.println("Result Indices: " + Arrays.toString(TwoSumPatternMaster.twoSum(nums, target)));

        System.out.println("\n=== 2. Two Sum III Data Structure ===");
        TwoSumPatternMaster.TwoSumDS ds = new TwoSumPatternMaster.TwoSumDS();
        ds.add(1);
        ds.add(3);
        ds.add(5);
        System.out.println("Find 4 (1+3): " + ds.find(4)); // true
        System.out.println("Find 7: "       + ds.find(7)); // false

        System.out.println("\n=== 3. 4Sum II Pair Counting ===");
        int[] A = {1, 2}, B = {-2, -1}, C = {-1, 2}, D = {0, 2};
        System.out.println("4Sum II Count: " + TwoSumPatternMaster.fourSumCount(A, B, C, D)); // Output: 2
    }
}
```

---

## 9. Complexity Analysis

| Algorithm / Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Two Sum (Hash Map)** | **$O(N)$ Linear ⚡** | **$O(N)$ Space** | Single Pass Complement Lookup |
| **Two Sum II (Sorted Pointers)**| **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Input Array Sorted |
| **Two Sum III (`find`)** | **$O(N)$ Search** | $O(N)$ Frequency Map | Map Key Iteration |
| **4Sum II ($N^2$ Hash Grouping)**| **$O(N^2)$ Time ⚡** | **$O(N^2)$ Space** | Split 4 arrays into 2 pairs ($A+B = -(C+D)$) |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Element Values (e.g. `nums = [3, 3], target = 6`)**:
  - Two-Pass Map approach (`map.put` all first) overwrites key `3`'s index `0` with index `1`!
  - Single-Pass approach handles this cleanly: At $i = 1$, `nums[1] = 3`, `complement = 3`. `map.containsKey(3)` evaluates `true` for index `0`, returning `[0, 1]` correctly!
* **No Solution Exists**: Return empty array `new int[0]`.
* **Integer Overflow in Sums**: When $a + b$ exceeds `Integer.MAX_VALUE`, use `long` sums.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Two-Pass Hash Map without Self-Pair Guard**: Doing `map.put()` for all items first, then checking `map.containsKey(target - nums[i])` without checking `map.get(complement) != i`. For `nums = [3, 2, 4], target = 6`, checking `nums[0] = 3` finds index `0` itself, incorrectly returning `[0, 0]`!
* **Using Hash Map for Two Sum II when Input Array is Already Sorted**: Wastes $O(N)$ auxiliary space! Use Two Pointers for $O(1)$ space.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Single-Pass Hash Map Beats Two-Pass:
> Single-pass checks `map.containsKey(complement)` BEFORE adding `nums[i]` to `map`.
> This guarantees that:
> 1. Elements cannot pair with themselves.
> 2. Duplicate numbers (e.g. `[3, 3]`) match their earlier twin without map overwrite bugs.
> 3. Execution terminates immediately on finding the first valid pair!

> **Memory Trick:** **"Check complement BEFORE map.put() to avoid self-pairing and duplicate map overwrite bugs!"**

---

## 13. System & Implementation Comparisons

| Feature | Single-Pass Hash Map | Two-Pointer (Sorted) |
| :--- | :--- | :--- |
| **Array Pre-requisite** | Unsorted Array | Must be Sorted Array |
| **Time Complexity** | **$O(N)$ Linear ⚡** | $O(N \log N)$ if sorting needed |
| **Space Complexity** | $O(N)$ Hash Map | **$O(1)$ Constant ⚡** |
| **Index Output** | Returns original indices | Destroys original indices unless wrapped |

---

## 14. How to Recognize This in Questions
* **"Find two numbers that add up to a target in an unsorted array"** $\rightarrow$ Single-Pass Hash Map (`target - nums[i]`).
* **"Count tuples (i, j, k, l) across 4 arrays such that A[i] + B[j] + C[k] + D[l] = 0"** $\rightarrow$ 4Sum II ($A+B = -(C+D)$ Hash Map).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does 4Sum II (LeetCode 454) run in $O(N^2)$ time instead of $O(N^4)$?**  
  *A:* By splitting 4 arrays into two halves of 2 arrays each. Compute all $N^2$ pairwise sums of $A$ and $B$ and store frequencies in a Hash Map ($O(N^2)$ time). Then compute all $N^2$ pairwise sums of $C$ and $D$, looking up negative complements $-(C[k] + D[l])$ in the map in $O(1)$ time $\implies \mathbf{O(N^2)\text{ Total Time}}$.
* **Q: How to adapt Two Sum if multiple valid pairs exist and we need all unique pairs?**  
  *A:* Sort the array first, then use Two Pointers with explicit skip loops (`while (left < right && nums[left] == nums[left+1]) left++;`) to skip duplicate values without set overhead.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TWO SUM & COMPLEMENT INDEXING                         |
+-----------------------------------------------------------------------+
| • Algebraic Complement: complement = target - nums[i]                 |
| • Single Pass Pattern: Check map.containsKey(complement) FIRST,       |
|   then map.put(nums[i], i). Prevents self-pairing & duplicate overwrites|
| • Two Sum II (Sorted): Left & Right pointers in O(1) space            |
| • 4Sum II (454): Group A+B into Map (O(N²)), lookup -(C+D) in Map     |
| • Complexity: Two Sum O(N) Time, O(N) Space | Two Sum II O(N) Time, O(1) Space|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write single-pass Two Sum in under 2 minutes.
- [ ] I know why single-pass prevents self-pairing bugs.
- [ ] I can explain why 4Sum II runs in $O(N^2)$ time.
- [ ] I know when to choose Hash Map vs Two Pointers for Two Sum variations.
- [ ] I can handle duplicate element edge cases cleanly.
