# 15. Array Problem Recognition Patterns

## 1. Introduction
Solving array problems under interview conditions requires rapid pattern recognition. Rather than memorizing individual solutions, top candidates recognize structural problem cues (phrasing, constraints, query types) and instantly map them to canonical array patterns: Two Pointers, Sliding Window, Prefix Sum, Difference Array, Kadane's Algorithm, Frequency Array, or Staircase Matrix Search.

> **Important:** In technical interviews, identifying the optimal pattern within the first 60 seconds of reading a problem statement determines whether you deliver an $O(N)$ solution or waste time on an $O(N^2)$ brute force.

## 2. Core Concepts
* **Pattern 1: Two Pointers (Opposite Direction)**: Triggered by sorted arrays, pair sum targets, or in-place range reversals.
* **Pattern 2: Two Pointers (Same Direction / Fast-Slow)**: Triggered by in-place array filtering (`Remove Duplicates`, `Move Zeroes`, cycle detection).
* **Pattern 3: Sliding Window**: Triggered by contiguous subarray / substring optimization problems ("Find longest/shortest subarray satisfying condition $C$").
* **Pattern 4: Prefix Sum + HashMap**: Triggered by subarray sum queries where **negative numbers are present**.
* **Pattern 5: Difference Array**: Triggered by batch range update operations $[L, R, V]$.
* **Pattern 6: Kadane's Algorithm**: Triggered by "Maximum contiguous subarray sum".
* **Pattern 7: Cyclic Sort**: Triggered by arrays containing numbers in range $1 \dots N$ ("Find missing / duplicate number").

> **Memory Trick:** **"Sorted Array -> Two Pointers; Subarray Range Sum -> Prefix Sum; Subarray Window -> Sliding Window; Max Subarray -> Kadane"**.

## 3. Characteristics / Properties
* **Pattern Recognition Decision Matrix**:

```
Problem Phrasing / Signal                      Optimal Array Pattern        Target Complexity
---------------------------------------------------------------------------------------------
Sorted array, find pair summing to Target       Two Pointers (Opposite)      O(N) Time, O(1) Space
Filter / Remove elements in-place               Two Pointers (Fast / Slow)   O(N) Time, O(1) Space
Longest / Shortest contiguous subarray (Positive) Sliding Window              O(N) Time, O(1) Space
Subarray sum equals K (Negative numbers present) Prefix Sum + HashMap        O(N) Time, O(N) Space
Apply Q range additions [L, R, V]               Difference Array             O(N + Q) Time, O(N) Space
Find contiguous subarray with maximum sum        Kadane's Algorithm           O(N) Time, O(1) Space
Array values in range 1..N, find missing/dup     Cyclic Sort                  O(N) Time, O(1) Space
Search in row/col sorted matrix                 Staircase Search (Top-Right) O(R + C) Time, O(1) Space
```

## 4. Internal Working
Decision Tree for Selecting Array Patterns:

```
                      [ Array Problem ]
                              |
               +--------------+--------------+
               |                             |
      [ Subarray / Window ]               [ Element Pair / Order ]
               |                             |
       +-------+-------+             +-------+-------+
       |               |             |               |
 [Range Sum / Count] [Max Sum Window] [Sorted Array] [Values 1..N]
       |               |             |               |
+------+------+   ( Kadane )   ( Two Pointers ) ( Cyclic Sort )
|             |
[Negatives?]  [No Negatives?]
|             |
(Prefix+Map) (Sliding Window)
```

## 5. Visual Diagram
Cyclic Sort Pattern Visualized (Values $1 \dots N$):

```
Values 1..N belong at index (val - 1).

Initial Array:  [ 3,  5,  2,  1,  4 ]
Index:            0   1   2   3   4

Step 1: Swap 3 to index 2 (3-1=2)  -> [ 2, 5, 3, 1, 4 ]
Step 2: Swap 2 to index 1 (2-1=1)  -> [ 5, 2, 3, 1, 4 ]
Step 3: Swap 5 to index 4 (5-1=4)  -> [ 4, 2, 3, 1, 5 ]
Step 4: Swap 4 to index 3 (4-1=3)  -> [ 1, 2, 3, 4, 5 ] (SORTED IN O(N) TIME!)
```

## 6. Operations / Algorithms
Cyclic Sort Pattern Implementation (LeetCode 268 / 448):

```java
// Cyclic Sort Template for numbers in range 1..N
public static void cyclicSort(int[] nums) {
    int i = 0;
    while (i < nums.length) {
        int correctIndex = nums[i] - 1; // For 1..N range
        if (nums[i] > 0 && nums[i] <= nums.length && nums[i] != nums[correctIndex]) {
            // Swap to correct index
            int temp = nums[i];
            nums[i] = nums[correctIndex];
            nums[correctIndex] = temp;
        } else {
            i++;
        }
    }
}
```

> **Quick Syntax:**
```java
// Cyclic Sort Correct Index Formula
int correctIndex = nums[i] - 1; // 1-based values (1..N)
int correctIndex0 = nums[i];     // 0-based values (0..N-1)
```

## 7. Examples
* **LeetCode 268 - Missing Number**: Cyclic Sort or XOR Bit Manipulation.
* **LeetCode 448 - Find All Numbers Disappeared in an Array**: Cyclic Sort or Negation Index Marking in $O(N)$ time and $O(1)$ space.
* **LeetCode 41 - First Missing Positive**: Hard problem solved trivially using Cyclic Sort in $O(N)$ time and $O(1)$ space.

## 8. Java Code
Complete interview-ready Java implementation demonstrating Cyclic Sort for finding missing numbers and duplicates in $O(N)$ time and $O(1)$ space:

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ArrayPatternRecognitionMaster {

    // 1. Cyclic Sort: Find Missing Number in range 0..N (LeetCode 268) O(N) Time, O(1) Space
    public static int missingNumber(int[] nums) {
        int i = 0;
        int n = nums.length;

        while (i < n) {
            int correctIndex = nums[i];
            if (nums[i] < n && nums[i] != nums[correctIndex]) {
                // Swap nums[i] to its correct index
                int temp = nums[i];
                nums[i] = nums[correctIndex];
                nums[correctIndex] = temp;
            } else {
                i++;
            }
        }

        // Find first index where index != nums[index]
        for (int j = 0; j < n; j++) {
            if (nums[j] != j) return j;
        }

        return n; // If 0..N-1 present, N is missing
    }

    // 2. Cyclic Sort: Find All Numbers Disappeared in Array 1..N (LeetCode 448) O(N) Time, O(1) Space
    public static List<Integer> findDisappearedNumbers(int[] nums) {
        int i = 0;
        while (i < nums.length) {
            int correctIndex = nums[i] - 1;
            if (nums[i] != nums[correctIndex]) {
                int temp = nums[i];
                nums[i] = nums[correctIndex];
                nums[correctIndex] = temp;
            } else {
                i++;
            }
        }

        List<Integer> result = new ArrayList<>();
        for (int j = 0; j < nums.length; j++) {
            if (nums[j] != j + 1) {
                result.add(j + 1);
            }
        }

        return result;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] nums1 = {3, 0, 1};
        System.out.println("Missing Number in {3, 0, 1}: " + missingNumber(nums1)); // Output: 2

        int[] nums2 = {4, 3, 2, 7, 8, 2, 3, 1};
        System.out.println("Disappeared Numbers in {4,3,2,7,8,2,3,1}: " + findDisappearedNumbers(nums2));
        // Output: [5, 6]
    }
}
```

## 9. Complexity Analysis
| Pattern | Time Complexity | Auxiliary Space | Key Triggers |
| :--- | :--- | :--- | :--- |
| **Cyclic Sort** | **$O(N)$** | **$O(1)$** | Values in range $1 \dots N$ or $0 \dots N$ |
| **Negation Index Marking** | **$O(N)$** | **$O(1)$** | Values in range $1 \dots N$, modifies array sign |
| **Two Pointers (Opposite)** | **$O(N)$** | **$O(1)$** | Sorted array pair searching |
| **Sliding Window** | **$O(N)$** | **$O(1)$** | Contiguous subarray with non-negative values |

## 10. Edge Cases
* **Cyclic Sort Infinite Loop**: If `nums[i] == nums[correctIndex]`, attempting to swap creates an infinite `while` loop! Guard: `if (nums[i] != nums[correctIndex]) swap; else i++;`.
* **Out of Range Values in Cyclic Sort**: For First Missing Positive (LeetCode 41), ignore values $\le 0$ or $> N$.
* **Array Length 1**: Ensure boundary checks handle $N = 1$ cleanly.

## 11. Common Mistakes
* Trying to use standard sorting ($O(N \log N)$) when Cyclic Sort can solve $1 \dots N$ range problems in linear $O(N)$ time.
* Forgetting `i++` in the `else` branch of Cyclic Sort (causes infinite while loop).
* Using Sliding Window for subarray sum problems when negative numbers exist in the array.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Whenever a problem mentions **"An array of size N containing numbers from 1 to N"**, think **CYCLIC SORT** or **NEGATION INDEX MARKING** immediately! You can solve missing, duplicate, or corrupted number problems in $O(N)$ time and $O(1)$ space.

> **Memory Trick:** **"Numbers 1 to N? Place element V at index V - 1!"**

## 13. Comparisons
| Technique | Sorting ($O(N \log N)$) | HashSet ($O(N)$ Space) | Cyclic Sort ($O(N)$ Space $O(1)$) |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(N \log N)$ | $O(N)$ | **$O(N)$ (Optimal)** |
| **Space Complexity**| $O(1)$ or $O(N)$ | $O(N)$ (Allocates map) | **$O(1)$ (In-Place Optimal)** |
| **Input Constraint** | Any values | Any values | **Values in range $1 \dots N$** |

## 14. How to Recognize This in Questions
* **"Find missing / duplicate number in range 1..N"** $\rightarrow$ Cyclic Sort ($O(N)$ time, $O(1)$ space).
* **"Find maximum sum subarray"** $\rightarrow$ Kadane's Algorithm ($O(N)$ time).
* **"Count subarrays summing to K with negative values"** $\rightarrow$ Prefix Sum + HashMap ($O(N)$ time).

## 15. Frequently Asked Interview Questions
* **Q: Why is Cyclic Sort $O(N)$ time despite having a nested while loop structure?**  
  *A:* Because each swap places at least one element into its correct final index position. Since there are $N$ elements, at most $N-1$ total swaps can occur across the entire algorithm execution $\implies O(N)$ time overall.
* **Q: What is Negation Index Marking?**  
  *A:* Negation Index Marking uses element values as indices and negates the value at that target index (`nums[Math.abs(val) - 1] *= -1`). If an index is already negative, a duplicate has been encountered.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ARRAY PROBLEM RECOGNITION PATTERNS                    |
+-----------------------------------------------------------------------+
| • Range 1..N Signal -> Cyclic Sort (Place num at index num - 1)       |
| • Subarray Sum + Negative Numbers -> Prefix Sum + HashMap             |
| • Subarray Sum + Positive Numbers Only -> Sliding Window              |
| • Range Updates [L, R, V] -> Difference Array (D[L]+=V, D[R+1]-=V)    |
| • Maximum Subarray Sum -> Kadane's Algorithm                          |
| • Sorted Array Pair Search -> Two Pointers Opposite Direction          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the Cyclic Sort template from memory in 2 minutes.
- [ ] I know how to avoid infinite loops in Cyclic Sort when duplicates exist.
- [ ] I can select between Sliding Window and Prefix Sum + HashMap based on negative numbers.
- [ ] I can solve LeetCode 268 (Missing Number) using Cyclic Sort.
- [ ] I can solve LeetCode 448 (Disappeared Numbers) in $O(N)$ time and $O(1)$ space.
