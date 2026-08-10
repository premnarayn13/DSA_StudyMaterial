# 04. 1D DP Problems: Linear Sequences, State Transitions & Space Reduction

## 1. Introduction
**1D Dynamic Programming** forms the primary gateway to mastering sequence-based optimization, counting, and decision problems. In 1D DP, the state space is indexed by a single integer parameter $i$ ($0 \le i \le N$), where $DP[i]$ represents the optimal answer, total combinations, or validity for the subproblem defined over the prefix or suffix of length $i$. 1D DP encompasses classical benchmark patterns such as **Fibonacci / Linear Recurrences** ($DP[i] = DP[i-1] + DP[i-2]$), **Non-Adjacent Choice Patterns** (House Robber $DP[i] = \max(\text{val}_i + DP[i-2], DP[i-1])$), **Partitioning Strings** (Decode Ways & Word Break), and **Maximum Contiguous Subarrays** (Kadane's Algorithm). 1D DP problems execute in **$O(N)$ Time Complexity** and can frequently be compressed down to **$O(1)$ Constant Auxiliary Space**.

> **Important:** Core Structural Invariants of 1D DP Problems:
> 1. **State Index Invariant ($DP[i]$)**:
>    - $DP[i]$ summarizes the subproblem outcome considering elements from index $0$ to $i$ (or suffix $i$ to $N-1$).
> 2. **Fixed Constant Dependency Rule**:
>    - If $DP[i]$ depends only on a fixed number $K$ of previous entries (e.g. $DP[i-1]$ and $DP[i-2]$), memory can be compressed from $O(N)$ to $O(1)$ variables!
> 3. **Variable Scope Dependency Rule**:
>    - If $DP[i]$ depends on ALL previous entries $0 \dots i-1$ (e.g. Longest Increasing Subsequence or Word Break), the 1D DP table MUST be retained in full ($O(N)$ space), executing in $O(N^2)$ or $O(N \cdot L)$ time.
> 4. **Boundary Base Case Invariant**:
>    - Base cases $DP[0]$ and $DP[1]$ handle initial array prefixes before loop iteration begins. ⚡

```
1D DP Classification Taxonomy:

1D DP Patterns:
├── 1. Fixed-Window Recurrence   ──► dp[i] depends on dp[i-1], dp[i-2]  (e.g., House Robber, Stairs) -> O(1) Space ⚡
├── 2. Decision String Split     ──► dp[i] depends on valid prefix substring (e.g., Decode Ways, Word Break) -> O(N) Space
└── 3. Contiguous Accumulation  ──► dp[i] depends on max(num[i], dp[i-1] + num[i]) (Kadane's DP) -> O(1) Space ⚡
```

---

## 2. Core Concepts & 1D DP Pattern Strategy Matrix

### 2.1 1D DP Pattern Comparison Matrix
```
1D DP Pattern Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | State Definition  | Transition Recurrence| Time Complexity| Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **House Robber I**    | Max loot up to $i$| $DP[i] = \max(v_i + DP[i-2], DP[i-1])$| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Decode Ways**       | Valid decodes $0..i$| $DP[i] = DP[i-1] + (valid ? DP[i-2] : 0)$| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Word Break**        | Can segment $0..i$| $DP[i] = \lor_{j=0}^{i-1} (DP[j] \land S[j..i] \in Dict)$| $O(N^2)$ / $O(N \cdot L)$| $O(N)$ DP Array   |
| **Kadane's Subarray** | Max sum ending $i$| $DP[i] = \max(A[i], A[i] + DP[i-1])$| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"House Robber = max(v_i + prev2, prev1); Decode Ways = prev1 + (valid_pair ? prev2 : 0); Kadane = max(v_i, v_i + prev)!"**

---

## 3. Characteristics & Mathematical Recurrence Formulations

### 3.1 Mathematical Derivation of LeetCode 91 (Decode Ways)
* A message containing digits from `'0'`..`'9'` is mapped to letters `'A'`..`'Z'` (`'1'` $\to$ `'A'` ... `'26'` $\to$ `'Z'`).
* Let $DP[i]$ be total valid decodings for prefix of length $i$.
* **State Transition Logic**:
  1. **Single Digit Case**: If $S[i-1] \neq '0'$, digit $S[i-1]$ forms a valid single letter mapping $\implies$ Add $DP[i-1]$ to $DP[i]$.
  2. **Double Digit Case**: If 2-digit substring $S[i-2 \dots i-1]$ forms a valid integer in range $[10 \dots 26]$ $\implies$ Add $DP[i-2]$ to $DP[i]$.
* Recurrence Equation:
  $$DP[i] = \left( S[i-1] \neq '0' ? DP[i-1] : 0 \right) + \left( 10 \le S[i-2 \dots i-1] \le 26 ? DP[i-2] : 0 \right)$$
* Base Cases: $DP[0] = 1$, $DP[1] = (S[0] \neq '0' ? 1 : 0)$.
* Space Compression: Since $DP[i]$ depends only on $DP[i-1]$ and $DP[i-2]$, space is compressed to **$O(1)$ Memory**! ⚡

---

## 4. Internal Working Mechanics: Word Break Substring Matching

Tracing LeetCode 139 (Word Break) for $S = \text{"leetcode"}$, $Dict = \{\text{"leet"}, \text{"code"}\}$:

```
DP Definition: dp[i] = true if substring S[0 ... i-1] can be segmented into dictionary words.
Base Case: dp[0] = true (empty string is valid).

State Evolution:
- i = 1..3 ("l", "le", "lee"): No matching word in dict -> dp[1..3] = false.
- i = 4 ("leet"): j = 0 -> dp[0] is true AND S[0..4] "leet" in dict -> dp[4] = true! ⚡

- i = 5..7 ("leetc", "leetco", "leetcod"): No match -> dp[5..7] = false.
- i = 8 ("leetcode"): j = 4 -> dp[4] is true AND S[4..8] "code" in dict -> dp[8] = true! ⚡

Final Result: dp[8] = true! String successfully segmented! ✅
```

---

## 5. Visual Diagram: Kadane's Algorithm DP State Flow

```
Kadane's DP Transition Topology for A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]:

Index i      :  0   1   2   3   4   5   6   7   8
Array A[i]   : -2   1  -3   4  -1   2   1  -5   4
DP[i] (Ending): -2   1  -2   4   3   5   6   1   5
                     ▲       ▲           ▲
                     │       │           └─ Max Subarray Sum = 6! ⚡
                     │       └─ Restart new subarray at A[3]=4!
                     └─ Restart new subarray at A[1]=1!
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing 1D DP Benchmark Problems: Decode Ways (LeetCode 91), Word Break (LeetCode 139), Kadane's DP (LeetCode 53), and House Robber I & II (LeetCode 198 & 213).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing 1D Dynamic Programming Benchmark Problems,
 * State Transitions, String Partitioning, and Space Optimization.
 */
public class OneDDPProblemsMaster {

    // =========================================================================
    // 1. LEETCODE 91: DECODE WAYS (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Calculates total ways to decode a digit string into letters A-Z.
     *
     * @param s input digit string
     * @return total valid decodings count
     */
    public int numDecodings(String s) {
        if (s == null || s.length() == 0 || s.charAt(0) == '0') return 0;

        int n = s.length();
        int prev2 = 1; // Base case: dp[0] = 1
        int prev1 = 1; // Base case: dp[1] = 1 (since s[0] != '0')

        for (int i = 2; i <= n; i++) {
            int curr = 0;

            // Single digit decoding S[i-1]
            int singleDigit = s.charAt(i - 1) - '0';
            if (singleDigit >= 1 && singleDigit <= 9) {
                curr += prev1;
            }

            // Double digit decoding S[i-2 ... i-1]
            int doubleDigit = Integer.parseInt(s.substring(i - 2, i));
            if (doubleDigit >= 10 && doubleDigit <= 26) {
                curr += prev2;
            }

            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // =========================================================================
    // 2. LEETCODE 139: WORD BREAK (O(N^2) Time, O(N) Space)
    // =========================================================================
    /**
     * Checks if string S can be segmented into dictionary words.
     */
    public boolean wordBreak(String s, List<String> wordDict) {
        if (s == null || s.length() == 0) return false;

        Set<String> dict = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true; // Base case: empty string is valid

        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break; // Substring valid -> Move to next i! ⚡
                }
            }
        }

        return dp[n];
    }

    // =========================================================================
    // 3. LEETCODE 53: MAXIMUM SUBARRAY SUM (KADANE'S DP O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves Maximum Subarray Sum using Kadane's 1D DP State Transition.
     * State Transition: dp[i] = max(nums[i], dp[i-1] + nums[i]).
     */
    public int maxSubArray(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int currentMax = nums[0];
        int globalMax = nums[0];

        for (int i = 1; i < nums.length; i++) {
            // Choice: Extend existing subarray or start fresh from nums[i]
            currentMax = Math.max(nums[i], currentMax + nums[i]);
            globalMax = Math.max(globalMax, currentMax);
        }

        return globalMax;
    }

    // =========================================================================
    // 4. LEETCODE 198: HOUSE ROBBER (O(N) Time, O(1) Space)
    // =========================================================================
    public int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int prev2 = 0, prev1 = 0;

        for (int num : nums) {
            int curr = Math.max(num + prev2, prev1);
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
}
```

> **Quick Syntax:**
```java
// Kadane's 1D DP State Line
currentMax = Math.max(nums[i], currentMax + nums[i]); globalMax = Math.max(globalMax, currentMax);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 91 - Decode Ways**:
   - String digit partitioning benchmark solved in $O(N)$ time and $O(1)$ space.

2. **LeetCode 139 - Word Break**:
   - Dictionary prefix segmentation solved in $O(N^2)$ time and $O(N)$ space.

3. **LeetCode 53 - Maximum Subarray (Kadane's DP)**:
   - Maximum contiguous profit subarray solved in $O(N)$ time and $O(1)$ space.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class OneDDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   1D DYNAMIC PROGRAMMING BENCHMARK DEMO         ");
        System.out.println("=================================================\n");

        OneDDPProblemsMaster master = new OneDDPProblemsMaster();

        // 1. Decode Ways Test (LeetCode 91)
        String s1 = "226";
        int decodes = master.numDecodings(s1);
        System.out.println("1. LeetCode 91 Decode Ways for String \"" + s1 + "\":");
        System.out.println("   Total Valid Decodings: " + decodes + " Ways (\"BZ\", \"VF\", \"BBF\")");
        System.out.println("-------------------------------------------------");

        // 2. Word Break Test (LeetCode 139)
        String s2 = "leetcode";
        List<String> dict = List.of("leet", "code");
        boolean canSegment = master.wordBreak(s2, dict);
        System.out.println("2. LeetCode 139 Word Break for \"" + s2 + "\" with Dict " + dict + ":");
        System.out.println("   Can Segment: " + canSegment + " (Optimal)");
        System.out.println("-------------------------------------------------");

        // 3. Kadane's Max Subarray Test (LeetCode 53)
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        int maxSub = master.maxSubArray(nums);
        System.out.println("3. LeetCode 53 Maximum Subarray Sum for Array:");
        System.out.println("   Max Subarray Sum (Kadane's DP): " + maxSub + " (Subarray [4, -1, 2, 1])");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| 1D DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Decode Ways (LC 91)** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Single/Double digit transitions |
| **Word Break (LC 139)** | $O(N^2)$ / $O(N \cdot L)$| $O(N)$ DP Array | Dictionary Set lookup |
| **Kadane's DP (LC 53)** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| `max(nums[i], curr + nums[i])` |
| **House Robber (LC 198)**| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| `max(num + prev2, prev1)` |

---

## 10. Edge Cases & Boundary Handling

1. **Leading Zeros in Decode Ways (`"06"`)**:
   - Returns `0` decodings immediately.

2. **All Negative Numbers in Kadane's Subarray (`[-5, -2, -8]`)**:
   - `maxSubArray` correctly picks the single maximum negative element (`-2`).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Integer Bound Range for 2-Digit Decode Ways**:
  - Checking `doubleDigit <= 26` without checking `doubleDigit >= 10` allows invalid numbers like `"06"` to be counted as double digits. ALWAYS check `doubleDigit >= 10 && doubleDigit <= 26`!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Identifying $O(1)$ Space Candidates in 1D DP:
> If the state transition formula $DP[i]$ accesses ONLY a fixed constant offset of previous entries (e.g., $i-1, i-2$), the 1D DP problem can ALWAYS be compressed down to **$O(1)$ Constant Auxiliary Space**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Decode Ways (LC 91) | Word Break (LC 139) | Kadane's DP (LC 53) |
| :--- | :--- | :--- | :--- |
| **State Output** | Total Combinations Count | Boolean Possibility | Maximum Numerical Sum |
| **Transition Range** | Fixed 2 Steps ($i-1, i-2$) | Variable Range ($0 \dots i-1$) | Single Step ($i-1$) |
| **Space Complexity** | **$O(1)$ Memory ⚡** | $O(N)$ Array | **$O(1)$ Memory ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count total valid decodings of digit string"** $\rightarrow$ Decode Ways (LeetCode 91).
* **"Find maximum sum contiguous subarray"** $\rightarrow$ Kadane's DP (LeetCode 53).

---

## 15. Frequently Asked Interview Questions

* **Q: Why can Decode Ways be space-optimized to $O(1)$ memory?**  
  *A:* Because state $DP[i]$ depends only on the previous two entries $DP[i-1]$ and $DP[i-2]$, allowing us to store state using two primitive variables (`prev1`, `prev2`).

* **Q: How does Kadane's Algorithm represent Dynamic Programming?**  
  *A:* Kadane's algorithm maintains the 1D DP state $DP[i] = \max(\text{nums}[i], \text{nums}[i] + DP[i-1])$, representing the maximum subarray sum ending at index $i$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 1D DP PROBLEMS                                        |
+-----------------------------------------------------------------------+
| • Decode Ways : dp[i] = (s[i-1]!='0'?dp[i-1]:0) + (10<=val<=26?dp[i-2]:0)|
| • Word Break  : dp[i] = true if dp[j] && s[j..i] in dict (O(N^2) Time) |
| • Kadane DP   : currMax = max(nums[i], currMax + nums[i]) -> O(N) Time|
| • House Robber: curr = max(num + prev2, prev1) -> O(1) Space ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 91 (`Decode Ways`) in $O(N)$ time and $O(1)$ space.
- [ ] I can write LeetCode 139 (`Word Break`) in $O(N^2)$ time.
- [ ] I can write Kadane's 1D DP Maximum Subarray (LeetCode 53) in $O(1)$ space.
- [ ] I can write House Robber I & II (LeetCode 198 & 213).
- [ ] I can state the condition required to compress a 1D DP array to $O(1)$ space.
