# 08. Palindrome Partitioning, DP Table Acceleration & Substring Backtracking

## 1. Introduction
**Palindrome Partitioning I** (LeetCode 131) and **Palindrome Partitioning II** (LeetCode 132) represent classic string decomposition backtracking problems. The objective is to partition a string $S$ into all possible combinations of substrings such that **EVERY SUBSTRING IN THE PARTITION IS A PALINDROME**. By accelerating palindrome validity checks using a **Precomputed 2D DP Table (`boolean[][] dp`)** or 2-pointer validation, Palindrome Partitioning explores substring combinations in **$O(N \cdot 2^N)$ Time** and **$O(N^2)$ Space**.

> **Important:** Core Invariants of Palindrome Partitioning:
> 1. **Substring Backtracking Loop**:
>    - Loop end index $e$ from $start$ to $N - 1$.
>    - Check if substring $S[start \dots e]$ is a palindrome!
>    - If YES: Include substring $S[start \dots e]$ in `currentList`, recurse to `e + 1`, then **BACKTRACK (Remove substring)**!
> 2. **Precomputed DP Table Optimization**:
>    - Precompute `dp[i][j]` where `dp[i][j] == true` if substring $S[i \dots j]$ is a palindrome:
>      $$\text{dp}[i][j] = (S[i] == S[j]) \text{ and } (j - i \le 2 \text{ or } \text{dp}[i+1][j-1])$$
>    - Reduces palindrome check time from $O(N)$ to **$O(1)$ Instant Lookup**! ⚡

```
Palindrome Partitioning Decision Tree Topology for s = "aab":
                                    "aab"
                             /                 \
                 "a" + "ab"                       "aa" + "b"
                  /      \                         |
           "a"+"a"+"b"   "a"+"ab" (Not Palindrome!) "aa"+"b" (Valid!)

Valid Partitions Generated: [["a", "a", "b"], ["aa", "b"]]! ⚡
```

---

## 2. Core Concepts & LeetCode 131 vs 132 Strategy Matrix

### 2.1 Palindrome Partitioning Strategy Matrix
```
Palindrome Partitioning Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Goal              | Primary Algorithm | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Partitioning I (131)**| All Palindrome Sets| Backtracking + DP | **$O(N \cdot 2^N)$ ⚡**|
| **Partitioning II (132)**| Minimum Cuts   | Dynamic Program   | **$O(N^2)$ Quadratic ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Palindrome Partitioning: Loop end index e = start..N-1! If substring[start..e] is palindrome -> Recurse e + 1!"**

---

## 3. Characteristics & $O(N \cdot 2^N)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(N \cdot 2^N)$ Complexity
* A string of length $N$ has $N - 1$ possible cut positions $\implies 2^{N-1}$ total possible partitions.
* For each partition, copying $O(N)$ character substrings into the list takes $O(N)$ time.
* Total Time Complexity: $\mathbf{O(N \cdot 2^N) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 131 on String `s = "aab"` with DP Table Acceleration:

```
DP Table for "aab":
dp[0][0] = T ("a")
dp[1][1] = T ("a")
dp[2][2] = T ("b")
dp[0][1] = T ("aa")
dp[1][2] = F ("ab")

Call backtrack(start = 0):
- Loop e = 0: dp[0][0] is T ("a") -> Add "a". Recurse backtrack(start = 1):
  - Loop e = 1: dp[1][1] is T ("a") -> Add "a". Recurse backtrack(start = 2):
    - Loop e = 2: dp[2][2] is T ("b") -> Add "b". Recurse backtrack(start = 3):
      - Base Case (start == 3): Add ["a", "a", "b"] to result! Return.
    - Pop "b".
  - Pop "a".
  - Loop e = 2: dp[1][2] is F ("ab") -> Skip!
- Pop "a".
- Loop e = 1: dp[0][1] is T ("aa") -> Add "aa". Recurse backtrack(start = 2):
  - Loop e = 2: dp[2][2] is T ("b") -> Add "b". Recurse backtrack(start = 3):
    - Base Case (start == 3): Add ["aa", "b"] to result! Return.
  - Pop "b".
- Pop "aa".

Extracted Partitions: [["a", "a", "b"], ["aa", "b"]]! ✅ (O(N * 2^N) Time!)
```

---

## 5. Visual Diagram
Palindrome Decision Tree Partition Topography:

```
Level 0 (start = 0):                      s = "aab"
                                  /                       \
Level 1 (start = 1, 2):     "a" | "ab"                 "aa" | "b"
                           /        \                     |
Level 2 (start = 3):   "a"|"a"|"b"  "a"|"ab" (F!)      "aa"|"b"  (Valid!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 131 (Palindrome Partitioning I with Precomputed DP Acceleration):

```java
import java.util.*;

// LeetCode 131: Palindrome Partitioning I Master Class
public class PalindromePartitioningMaster {

    // LeetCode 131 Solution O(N * 2^N) Time, O(N^2) Space
    public List<List<String>> partition(String s) {
        List<List<String>> result = new ArrayList<>();
        if (s == null || s.length() == 0) return result;

        int n = s.length();

        // Step 1: Precompute 2D Palindrome DP Table O(N^2) Time
        boolean[][] dp = new boolean[n][n];
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s.charAt(i) == s.charAt(j)) {
                    if (j - i <= 2 || dp[i + 1][j - 1]) {
                        dp[i][j] = true;
                    }
                }
            }
        }

        // Step 2: Backtracking Search using O(1) DP Palindrome Checks
        backtrackPartition(s, 0, dp, new ArrayList<>(), result);

        return result;
    }

    private void backtrackPartition(String s, int start, boolean[][] dp, 
                                    List<String> current, List<List<String>> result) {
        // Base Case: Processed entire string up to length N!
        if (start == s.length()) {
            result.add(new ArrayList<>(current)); // Found valid partition!
            return;
        }

        for (int end = start; end < s.length(); end++) {
            // O(1) DP Check: Is substring s[start ... end] a valid palindrome?
            if (dp[start][end]) {
                String substring = s.substring(start, end + 1);

                current.add(substring);                                   // Step 1: Choose
                backtrackPartition(s, end + 1, dp, current, result);      // Step 2: Recurse
                current.remove(current.size() - 1);                       // Step 3: BACKTRACK
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Palindrome Substring Loop Line
if (dp[start][end]) { current.add(s.substring(start, end + 1)); backtrack(end + 1); current.remove(...); }
```

---

## 7. Concrete Problem Examples
* **LeetCode 131 - Palindrome Partitioning I**: All palindrome partition lists.
* **LeetCode 132 - Palindrome Partitioning II**: Minimum cut optimization.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 131 `partition`:

```java
public class PalindromePartitioningDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 131 Palindrome Partitioning Test ===");
        PalindromePartitioningMaster solver = new PalindromePartitioningMaster();

        String s = "aab";
        List<List<String>> result = solver.partition(s);

        System.out.println("All Palindrome Partitions of 'aab':");
        for (List<String> part : result) {
            System.out.println(part);
        }
        // Output: [["a", "a", "b"], ["aa", "b"]] ✅
    }
}
```

---

## 9. Complexity Analysis

| Algorithm Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Partitioning + DP Table**| **$O(N \cdot 2^N)$ Optimal ⚡**| **$O(N^2)$ DP Matrix** | Precomputed $O(1)$ palindrome check |
| **Naive Partitioning**   | $O(N^2 \cdot 2^N)$ Slower | $O(N)$ Call Stack Memory | $O(N)$ 2-pointer check per subproblem |

---

## 10. Edge Cases & Boundary Handling
* **Single Character String (`"a"`)**: Returns `[["a"]]`.
* **String of All Same Characters (`"aaaa"`)**: Generates all integer partitions of $N$.

---

## 11. Common Mistakes & Anti-Patterns
* **Performing $O(N)$ 2-Pointer Palindrome Check Inside the Backtracking Loop**:
  - Running a 2-pointer `isPalindrome()` loop inside the recursive backtracking function adds an extra $O(N)$ multiplier to every branch, degrading performance to $O(N^2 \cdot 2^N)$.
  - **ALWAYS precompute a 2D `boolean[][] dp` table for $O(1)$ instant palindrome checks**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Precomputing 2D DP Table Accelerates Backtracking:
> The subproblem `isPalindrome(s, i, j)` is evaluated thousands of times across different backtracking paths.
> Precomputing `dp[i][j]` in $O(N^2)$ time upfront allows the backtracking loop to check `if (dp[start][end])` in **$O(1)$ time**, eliminating redundant character comparisons! ⚡

> **Memory Trick:** **"Precompute boolean[][] dp table upfront for O(1) palindrome checks in backtracking!"**

---

## 13. System & Implementation Comparisons

| Feature | Palindrome Partitioning I (131) | Palindrome Partitioning II (132) |
| :--- | :--- | :--- |
| **Primary Goal** | Generate All Partitions | Find Minimum Number of Cuts |
| **Algorithm Type** | **Backtracking + DP ⚡** | Pure Dynamic Programming |
| **Time Complexity** | $O(N \cdot 2^N)$ Exponential | **$O(N^2)$ Quadratic ⚡** |

---

## 14. How to Recognize This in Questions
* **"Partition string such that every substring in the partition is a palindrome"** $\rightarrow$ LeetCode 131 (Palindrome Partitioning).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `dp[i][j] = (s[i] == s[j]) && (j - i <= 2 || dp[i+1][j-1])` build the DP table?**  
  *A:* If boundary characters match, a substring of length $\le 3$ ($j - i \le 2$) is automatically a palindrome; longer substrings depend on inner substring `dp[i+1][j-1]`.
* **Q: Why does `backtrackPartition` pass `end + 1` as the next start index?**  
  *A:* Because `end` is the inclusive last character of the current palindrome substring, so the next substring MUST begin at index `end + 1`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PALINDROME PARTITIONING (LEETCODE 131)                |
+-----------------------------------------------------------------------+
| • Step 1: Precompute boolean[][] dp table: dp[i][j] in O(N^2) time    |
| • Step 2: Loop end = start to N-1:                                    |
|           if (dp[start][end]) {                                       |
|               current.add(s.substring(start, end + 1));              |
|               backtrack(end + 1);                                     |
|               current.remove(current.size() - 1);                     |
|           }                                                           |
| • Performance: O(N * 2^N) Time | O(N^2) DP Table Auxiliary Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 131 (`Palindrome Partitioning I`) in Java.
- [ ] I can write the 2D DP table precomputation loop.
- [ ] I know why $O(1)$ DP check accelerates backtracking.
- [ ] I can contrast LeetCode 131 with LeetCode 132.
- [ ] I can trace palindrome partitioning step by step.
