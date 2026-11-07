# 05. Array Rotation & Reversal Algorithms

## 1. Introduction
Array rotation involves shifting every element in an array circularly by $K$ positions to the left or right. In technical coding interviews, array rotation (such as LeetCode 189 "Rotate Array") tests an applicant's ability to transition from naive $O(n \cdot k)$ or $O(n)$ extra space solutions to optimal **$O(n)$ time and $O(1)$ auxiliary space** in-place algorithms using reversal tricks or cyclic replacements.

> **Important:** Always normalize the rotation count using **`k = k % n`**. Rotating an array of size $n$ by $k$ steps is identical to rotating it by $k \pmod n$ steps because rotating $n$ times returns the array to its original state!

## 2. Core Concepts
* **Right Rotation by $K$**: Shifting elements clockwise so that the last $K$ elements wrap around to become the first $K$ elements of the array.
* **Left Rotation by $K$**: Shifting elements counter-clockwise so that the first $K$ elements wrap around to become the last $K$ elements of the array.
* **The Reversal Algorithm**: An ingenious 3-step range reversal technique that rotates an array in-place in $O(n)$ time and $O(1)$ space.
* **Juggling Algorithm (GCD Cycles)**: Rotating elements in cyclic sets based on $\gcd(n, k)$ to achieve $O(n)$ time and $O(1)$ space with minimal writes.

> **Memory Trick for Right Rotation:** **"Split at k -> Reverse Part 1 -> Reverse Part 2 -> Reverse All"**.
> 1. `reverse(0, k - 1)`
> 2. `reverse(k, n - 1)`
> 3. `reverse(0, n - 1)`

## 3. Characteristics / Properties
* **Rotation Equivalent Property**: Left rotation by $K$ is mathematically equivalent to Right rotation by $n - K$.
* **In-Place Optimality**: The reversal algorithm performs exactly $N$ total swaps, achieving optimal $O(n)$ execution time with zero auxiliary heap memory.

```
Array Rotation Method Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Rotation Method       | Time Complexity   | Space Complexity  | Notes / Trade-off |
+-----------------------+-------------------+-------------------+-------------------+
| Brute Force (k times) | O(n * k)          | O(1)              | TLE on large k    |
| Temporary Extra Array | O(n)              | O(n)              | Violates O(1) space|
| Reversal Algorithm    | O(n)              | O(1)              | OPTIMAL & PREFERRED|
| Juggling (GCD Cyclic) | O(n)              | O(1)              | Complex code math |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing 3-Step Reversal Algorithm for **Right Rotation** by $K = 3$ on `arr = [1, 2, 3, 4, 5, 6, 7]` ($n = 7$):

### Step 0: Normalize $K$
$$K = 3 \pmod 7 = 3$$

### Step 1: Reverse First $n - K$ Elements (index $0 \dots 3$)
Reverse `[1, 2, 3, 4]` $\to$ `[4, 3, 2, 1]`  
Array state: `[4, 3, 2, 1, 5, 6, 7]`

### Step 2: Reverse Last $K$ Elements (index $4 \dots 6$)
Reverse `[5, 6, 7]` $\to$ `[7, 6, 5]`  
Array state: `[4, 3, 2, 1, 7, 6, 5]`

### Step 3: Reverse the Entire Array (index $0 \dots 6$)
Reverse `[4, 3, 2, 1, 7, 6, 5]` $\to$ `[5, 6, 7, 1, 2, 3, 4]`  
Final Right Rotated Result: **`[5, 6, 7, 1, 2, 3, 4]`** ✅

## 5. Visual Diagram
Right Rotation Reversal Mechanics Visualized:

```
Original Array:    [ 1 ][ 2 ][ 3 ][ 4 ]  |  [ 5 ][ 6 ][ 7 ]   (k = 3)
                   <--- Part 1 ------->  |  <--- Part 2 -->

Step 1 (Rev Pt 1): [ 4 ][ 3 ][ 2 ][ 1 ]  |  [ 5 ][ 6 ][ 7 ]
Step 2 (Rev Pt 2): [ 4 ][ 3 ][ 2 ][ 1 ]  |  [ 7 ][ 6 ][ 5 ]
Step 3 (Rev All):  [ 5 ][ 6 ][ 7 ][ 1 ][ 2 ][ 3 ][ 4 ]  (ROTATED!)
```

## 6. Operations / Algorithms
Code Templates for Right and Left Array Rotation:

### 1. In-Place Right Rotation by $K$ Steps (LeetCode 189)
```java
public void rotateRight(int[] nums, int k) {
    int n = nums.length;
    if (n == 0) return;
    k = k % n; // Step 0: Normalize k
    
    // Step 1: Reverse first n - k elements
    reverse(nums, 0, n - k - 1);
    // Step 2: Reverse last k elements
    reverse(nums, n - k, n - 1);
    // Step 3: Reverse entire array
    reverse(nums, 0, n - 1);
}
```

### 2. In-Place Left Rotation by $K$ Steps
```java
public void rotateLeft(int[] nums, int k) {
    int n = nums.length;
    if (n == 0) return;
    k = k % n; // Step 0: Normalize k
    
    // Step 1: Reverse first k elements
    reverse(nums, 0, k - 1);
    // Step 2: Reverse remaining n - k elements
    reverse(nums, k, n - 1);
    // Step 3: Reverse entire array
    reverse(nums, 0, n - 1);
}
```

> **Quick Syntax:**
```java
// Subrange Array Reversal Helper
private void reverse(int[] nums, int start, int end) {
    while (start < end) {
        int temp = nums[start];
        nums[start] = nums[end];
        nums[end] = temp;
        start++;
        end--;
    }
}
```

## 7. Examples
* **LeetCode 189 - Rotate Array**: Rotate array right by $k$ steps in-place.
* **Rotate String / Check Cyclic Shift**: Verifying if string $S_2$ is a rotated version of $S_1$ via `(S1 + S1).contains(S2)`.
* **Search in Rotated Sorted Array (LeetCode 33)**: Modified binary search on a rotated array structure.

## 8. Java Code
Complete interview-ready Java implementation demonstrating Right Rotation, Left Rotation, and Verification dry runs:

```java
import java.util.Arrays;

public class ArrayRotationMaster {

    // Main 3-Step Reversal Right Rotation Method O(n) Time, O(1) Space
    public static void rotateRight(int[] nums, int k) {
        if (nums == null || nums.length <= 1) return;

        int n = nums.length;
        k = k % n; // Normalize k to handle k >= n
        if (k == 0) return;

        // 1. Reverse first n - k elements (0 to n - k - 1)
        reverseRange(nums, 0, n - k - 1);
        // 2. Reverse last k elements (n - k to n - 1)
        reverseRange(nums, n - k, n - 1);
        // 3. Reverse entire array (0 to n - 1)
        reverseRange(nums, 0, n - 1);
    }

    // Main 3-Step Reversal Left Rotation Method O(n) Time, O(1) Space
    public static void rotateLeft(int[] nums, int k) {
        if (nums == null || nums.length <= 1) return;

        int n = nums.length;
        k = k % n;
        if (k == 0) return;

        // 1. Reverse first k elements (0 to k - 1)
        reverseRange(nums, 0, k - 1);
        // 2. Reverse remaining elements (k to n - 1)
        reverseRange(nums, k, n - 1);
        // 3. Reverse entire array (0 to n - 1)
        reverseRange(nums, 0, n - 1);
    }

    // Helper method for subrange reversal
    private static void reverseRange(int[] arr, int start, int end) {
        while (start < end) {
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            start++;
            end--;
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        int[] arr1 = {1, 2, 3, 4, 5, 6, 7};
        int k1 = 3;

        System.out.println("Original: " + Arrays.toString(arr1));
        rotateRight(arr1, k1);
        System.out.println("Rotated Right by " + k1 + ": " + Arrays.toString(arr1));
        // Output: [5, 6, 7, 1, 2, 3, 4]

        int[] arr2 = {1, 2, 3, 4, 5, 6, 7};
        int k2 = 2;
        rotateLeft(arr2, k2);
        System.out.println("Rotated Left by " + k2 + ": " + Arrays.toString(arr2));
        // Output: [3, 4, 5, 6, 7, 1, 2]
    }
}
```

## 9. Complexity Analysis
| Rotation Algorithm | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **3-Step Reversal** | $O(n)$ | $O(1)$ | Performs exactly $N$ total element swaps |
| **Extra Array Strategy**| $O(n)$ | $O(n)$ | Allocates `new int[n]` copy array |
| **Juggling (GCD Cycles)**| $O(n)$ | $O(1)$ | Moves elements directly to destination index |
| **Brute Force (k loops)**| $O(n \cdot k)$ | $O(1)$ | Shifts elements by 1 position $K$ times (TLE) |

## 10. Edge Cases
* **$K \ge N$**: If $K = 10$ and $N = 7$, rotating by $10$ is identical to rotating by $10 \pmod 7 = 3$. Skipping `k = k % n` causes `ArrayIndexOutOfBoundsException`!
* **$K = 0$ or $K \% N == 0$**: No rotation needed; return immediately.
* **Single Element Array ($N = 1$)**: Return immediately.

## 11. Common Mistakes
* Forgetting `k = k % n` normalization before reversing ranges.
* Confusing Left Rotation range bounds with Right Rotation range bounds.
* Using an extra array `int[] temp = new int[n]` when the interviewer explicitly requested an $O(1)$ in-place memory solution.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Memory cheat code for Right vs Left Rotation bounds:
> * **Right Rotate by K**: Reverse `[0 ... n-k-1]`, Reverse `[n-k ... n-1]`, Reverse `[0 ... n-1]`.
> * **Left Rotate by K**: Reverse `[0 ... k-1]`, Reverse `[k ... n-1]`, Reverse `[0 ... n-1]`.

> **Memory Trick:** **"Always normalize k = k % n first!"**

## 13. Comparisons
| Feature | Extra Array Strategy | Reversal Algorithm |
| :--- | :--- | :--- |
| **Time Complexity** | $O(n)$ | $O(n)$ |
| **Space Complexity**| $O(n)$ (Allocates copy array) | **$O(1)$ (In-Place)** |
| **Implementation Ease**| High (`copy[ (i + k) % n ] = nums[i]`) | High (3 line helper method) |
| **Interview Score** | Acceptable for naive pass | **EXCELLENT (Passes optimal tier)** |

## 14. How to Recognize This in Questions
* **"Rotate array by K steps in-place"** $\rightarrow$ 3-Step Reversal Algorithm.
* **"Search element in a rotated sorted array"** $\rightarrow$ Modified Binary Search.

## 15. Frequently Asked Interview Questions
* **Q: Why does the 3-Step Reversal algorithm work for array rotation?**  
  *A:* Array rotation splits the array into two contiguous blocks $A$ and $B$. A right rotation converts sequence $AB$ into $BA$. Reversing $A$ to $A^R$ and $B$ to $B^R$ produces $A^R B^R$. Reversing the entire combined array $(A^R B^R)^R$ yields $(B^R)^R (A^R)^R = BA$, which is the exact rotated arrangement!
* **Q: How do you handle negative values of $K$ (e.g., $K = -2$)?**  
  *A:* Normalize negative values by converting them to positive right rotation steps: `k = (k % n + n) % n`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ARRAY ROTATION & REVERSAL                            |
+-----------------------------------------------------------------------+
| • Step 0: Mandatory k = k % n normalization                           |
| • Right Rotate by K: Reverse(0, n-k-1) -> Reverse(n-k, n-1)           |
|                      -> Reverse(0, n-1)                               |
| • Left Rotate by K:  Reverse(0, k-1)   -> Reverse(k, n-1)             |
|                      -> Reverse(0, n-1)                               |
| • Proof: (A^R B^R)^R = BA                                             |
| • Optimal Complexity: O(n) Time, O(1) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can state why `k = k % n` normalization is mandatory.
- [ ] I can implement the 3-Step Reversal Right Rotation from memory.
- [ ] I can implement the 3-Step Reversal Left Rotation from memory.
- [ ] I can prove why $(A^R B^R)^R = BA$ yields the rotated arrangement.
- [ ] I know how to convert negative $K$ values to valid positive rotation counts.
