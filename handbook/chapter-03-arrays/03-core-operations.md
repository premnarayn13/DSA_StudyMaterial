# 03. Core Array Operations

## 1. Introduction
Core array operations—Traversal, Searching, Reversal, Swapping, and In-place Transformations—form the foundation of array manipulation in technical interviews. Mastering these basic building blocks enables solving complex algorithmic problems (such as Two Pointers, Sliding Window, and Kadane's Algorithm) with optimal time and space bounds.

> **Important:** Array manipulation in technical interviews heavily emphasizes **In-Place Operations** ($O(1)$ auxiliary space) to optimize memory efficiency and eliminate heap allocations.

## 2. Core Concepts
* **Linear Traversal**: Visiting every element from index `0` to `n-1` sequentially ($O(n)$ time).
* **Two-Pointer Traversal**: Utilizing dual index variables (e.g., `left` starting at `0`, `right` starting at `n-1`) moving inward to process elements in $O(n)$ time.
* **Element Swapping**: Exchanging values between indices `i` and `j` using a temporary variable or XOR bitwise trick in $O(1)$ time.
* **In-Place Reversal**: Reversing array elements between index `left` and `right` by repeatedly swapping `arr[left]` and `arr[right]` until pointers meet.

> **Memory Trick:** **"Opposite Pointers for Reversal & Pairs; Same Direction Pointers for Fast/Slow Partitioning"**.

## 3. Characteristics / Properties
* **In-Place Transformation**: Modifying input array values without allocating auxiliary arrays ($O(1)$ auxiliary space).
* **Index Bounds Safety**: Pointer operations must preserve invariant $0 \le \text{index} < n$.
* **Symmetry Property in Reversal**: Element at index `i` maps to index `n - 1 - i` after array reversal.

```
Array Core Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation             | Best Case         | Average Case      | Worst Case        |
+-----------------------+-------------------+-------------------+-------------------+
| Linear Traversal      | Ω(n)              | Θ(n)              | O(n)              |
| In-Place Reversal     | Ω(n/2) = Ω(n)     | Θ(n)              | O(n)              |
| Element Swap          | Ω(1)              | Θ(1)              | O(1)              |
| Unsorted Linear Search| Ω(1)              | Θ(n)              | O(n)              |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing In-Place Array Reversal using Two-Pointer Swapping:

```
Initial Array: [ 10, 20, 30, 40, 50 ]
Pointer init:  left = 0 (val 10), right = 4 (val 50)

Step 1: Swap(arr[0], arr[4]) -> Array becomes [ 50, 20, 30, 40, 10 ]
        Increment left=1, Decrement right=3

Step 2: Swap(arr[1], arr[3]) -> Array becomes [ 50, 40, 30, 20, 10 ]
        Increment left=2, Decrement right=2

Step 3: Loop terminates because left >= right (left == right == 2).
Final Reversed Array: [ 50, 40, 30, 20, 10 ]
```

## 5. Visual Diagram
Two-Pointer In-Place Reversal Execution:

```
Index:    0      1      2      3      4
Val:    [ 10 ][ 20 ][ 30 ][ 40 ][ 50 ]
          ^                      ^
         left                  right

  Swap(10, 50)  -->  left++, right--

Val:    [ 50 ][ 20 ][ 30 ][ 40 ][ 10 ]
                 ^        ^
                left    right

  Swap(20, 40)  -->  left++, right--

Val:    [ 50 ][ 40 ][ 30 ][ 20 ][ 10 ]
                        ^
                  left == right (STOP!)
```

## 6. Operations / Algorithms
Essential Array Building Block Algorithms:

### 1. In-Place Element Swap (`swap(arr, i, j)`)
```java
// Temp Variable Swap (Standard & Preferred)
int temp = arr[i];
arr[i] = arr[j];
arr[j] = temp;

// XOR Bitwise Swap Trick (Zero Auxiliary Space)
// WARNING: Fails if i == j (sets arr[i] to 0!)
arr[i] = arr[i] ^ arr[j];
arr[j] = arr[i] ^ arr[j];
arr[i] = arr[i] ^ arr[j];
```

### 2. In-Place Array Subrange Reversal (`reverse(arr, start, end)`)
```java
public static void reverse(int[] arr, int start, int end) {
    while (start < end) {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}
```

> **Quick Syntax:**
```java
// Two-Pointer Opposite Direction Traversal Idiom
int left = 0, right = arr.length - 1;
while (left < right) {
    // Process arr[left] and arr[right]
    left++;
    right--;
}
```

## 7. Examples
* **Array Rotation**: Rotating array by $K$ steps using triple reversal (`reverse(0, K-1)`, `reverse(K, N-1)`, `reverse(0, N-1)`).
* **Palindrome Check**: Validating if array reads identical forward and backward using Two Pointers.
* **Dutch National Flag / Partitioning**: Segregating 0s, 1s, and 2s in $O(n)$ time.

## 8. Java Code
Interview-ready suite of core array operations (traversal, reversal, find min/max, two-pointer swap, and dry run validation):

```java
public class CoreArrayOperations {

    // 1. In-Place Element Swap
    public static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // 2. In-Place Range Reversal: Sub-array arr[left...right]
    public static void reverseRange(int[] arr, int left, int right) {
        if (arr == null || left >= right) return;
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }

    // 3. Single-Pass Min and Max Finder O(n) Time, O(1) Space
    public static int[] findMinAndMax(int[] arr) {
        if (arr == null || arr.length == 0) return new int[]{};

        int min = arr[0];
        int max = arr[0];

        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < min) min = arr[i];
            if (arr[i] > max) max = arr[i];
        }

        return new int[]{min, max}; // Returns [min, max]
    }

    // 4. Check if Array is Palindromic
    public static boolean isPalindrome(int[] arr) {
        if (arr == null) return false;
        int left = 0, right = arr.length - 1;
        while (left < right) {
            if (arr[left] != arr[right]) return false;
            left++;
            right--;
        }
        return true;
    }

    // Dry Run
    public static void main(String[] args) {
        int[] data = {12, 34, 56, 78, 90};

        System.out.println("Original: " + java.util.Arrays.toString(data));

        // Test Range Reversal
        reverseRange(data, 0, data.length - 1);
        System.out.println("Reversed: " + java.util.Arrays.toString(data)); // [90, 78, 56, 34, 12]

        // Test Min and Max
        int[] minMax = findMinAndMax(data);
        System.out.println("Min: " + minMax[0] + ", Max: " + minMax[1]); // Min: 12, Max: 90

        // Test Palindrome
        int[] palindromeArr = {1, 2, 3, 2, 1};
        System.out.println("Is {1,2,3,2,1} Palindrome? " + isPalindrome(palindromeArr)); // true
    }
}
```

## 9. Complexity Analysis
| Core Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **In-Place Range Reversal** | $O(n)$ | $O(1)$ | Performs $\lfloor n/2 \rfloor$ swaps |
| **Find Min and Max** | $O(n)$ | $O(1)$ | Single pass ($n-1$ comparisons) |
| **Array Palindrome Check** | $O(n)$ | $O(1)$ | Early exit on mismatch |
| **XOR Bitwise Swap** | $O(1)$ | $O(1)$ | Fails if `i == j` |

## 10. Edge Cases
* **XOR Swap Same Index Bug**: Executing `arr[i] = arr[i] ^ arr[i]` when `i == j` sets `arr[i]` to `0`! Always use temp variable or guard `if (i != j)`.
* **Null or Empty Array**: Guard methods against `arr == null` or `arr.length == 0`.
* **Single Element Array (`length == 1`)**: Reversal or Palindrome check returns immediately without swaps.

## 11. Common Mistakes
* Using XOR swap without checking `i != j` (zeroes out the element at index `i`).
* Forgetting to update pointer variables (`left++`, `right--`) inside the `while` loop (causes infinite loop!).
* Allocating a new array `int[] reversed = new int[n]` for array reversal when an in-place $O(1)$ space reversal was requested.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never use XOR bitwise swap `a ^= b ^= a ^= b` in production or interviews unless explicitly requested! Standard temporary variable swap is cleaner, faster (due to CPU register optimization), and immune to the `i == j` zeroing bug.

> **Memory Trick:** **"Reversal Trick for Rotation"**:
> To rotate array right by $K$ steps:
> 1. `reverse(0, K - 1)`
> 2. `reverse(K, N - 1)`
> 3. `reverse(0, N - 1)`

## 13. Comparisons
| Feature | Temporary Variable Swap | XOR Bitwise Swap |
| :--- | :--- | :--- |
| **Code Syntax** | `temp = a; a = b; b = temp;` | `a ^= b; b ^= a; a ^= b;` |
| **Safety** | 100% Safe | **Unsafe if `a` and `b` reference same location** |
| **Readability** | High | Low |
| **Recommendation** | **PREFERRED** | **AVOID** |

## 14. How to Recognize This in Questions
* **"Reverse array in-place"** $\rightarrow$ Two Pointers (`left = 0`, `right = n-1`).
* **"Rotate array by K positions"** $\rightarrow$ Three-step Subrange Reversal.

## 15. Frequently Asked Interview Questions
* **Q: How many comparisons are required to find both minimum and maximum in an array?**  
  *A:* Naive approach takes $2n - 2$ comparisons. Pairwise comparison optimization finds both in $\frac{3}{2}n - 2$ comparisons by comparing pairs first before updating min/max.
* **Q: Why does two-pointer array reversal run in $O(n)$ time?**  
  *A:* The loop executes $\lfloor n/2 \rfloor$ iterations, performing constant $O(1)$ operations per iteration, which simplifies to $O(n)$ linear time complexity.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CORE ARRAY OPERATIONS                                 |
+-----------------------------------------------------------------------+
| • Reversal: Two Pointers (left=0, right=n-1) -> Swap until left >= right|
| • Rotation Trick (Right by K): Reverse(0, K-1) -> Reverse(K, N-1)     |
|                                -> Reverse(0, N-1)                     |
| • Temp Swap is safer than XOR Swap (XOR zeroes element if i == j)     |
| • Min & Max: Single pass O(n) time, O(1) space                        |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write in-place array range reversal from memory.
- [ ] I know why XOR swap fails when `i == j`.
- [ ] I can derive the 3-step reversal algorithm for array rotation.
- [ ] I can implement single-pass min/max search.
- [ ] I know how to use opposite-direction two pointers safely.
