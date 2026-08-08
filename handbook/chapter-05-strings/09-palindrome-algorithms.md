# 09. Palindrome Algorithms & Expand Around Center

## 1. Introduction
A **Palindrome** is a string that reads identically forward and backward (e.g., `"racecar"`, `"aba"`). In technical coding interviews, palindrome problems evaluate a candidate's mastery of Two Pointers, dynamic programming, and center expansion techniques. The **Expand Around Center** approach finds the Longest Palindromic Substring in **$O(N^2)$ time and $O(1)$ auxiliary space**, outperforming naive $O(N^3)$ substring checks and eliminating the $O(N^2)$ space memory overhead of DP matrices.

> **Important:** In Expand Around Center, an odd-length palindrome expands from a single center character `(i, i)`, while an even-length palindrome expands from a double center pair `(i, i + 1)`. There are **$2N - 1$ total potential centers** in a string of length $N$!

## 2. Core Concepts
* **Two-Pointer Palindrome Validation**: Checking if string $S$ is a palindrome by placing `left = 0` and `right = N-1` and advancing inward ($O(N)$ time, $O(1)$ space).
* **Expand Around Center Paradigm**: Expanding outward from each potential center index as long as `S[left] == S[right]`.
* **$2N - 1$ Centers**:
  * $N$ Odd-length centers: `(0,0), (1,1), (2,2), ..., (N-1, N-1)`
  * $N - 1$ Even-length centers: `(0,1), (1,2), (2,3), ..., (N-2, N-1)`
* **Palindromic Substrings Count**: Counting total palindromic substrings by adding the expansion distance `(right - left + 1) / 2` at each center.

> **Memory Trick:** **"Expand outward while S[left] == S[right]. Check both odd center (i, i) and even center (i, i + 1)!"**

## 3. Characteristics / Properties
* **In-Place Memory Efficiency**: Expand Around Center runs in **$O(1)$ auxiliary space**, avoiding $O(N^2)$ 2D DP boolean table allocations (`dp[i][j]`).
* **Max Substring Length Formula**: If expansion terminates at indices `(left, right)` where `S[left] != S[right]`, the valid palindrome length is **`right - left - 1`**.

```
Palindrome Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Strategy / Algorithm  | Time Complexity   | Auxiliary Space   | Key Advantage     |
+-----------------------+-------------------+-------------------+-------------------+
| Naive Substring Check | O(N³)             | O(N)              | TLE on large N    |
| 2D Dynamic Programming| O(N²)             | O(N²) Matrix      | High memory usage |
| Expand Around Center  | O(N²)             | O(1) Constant     | OPTIMAL & CLEAN ⚡|
| Manacher's Algorithm  | O(N) Linear       | O(N)              | Fastest theoretical|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Expand Around Center for `s = "babad"` ($N = 5$):

```
Center i = 0 (Odd center 'b'):
Expand (0, 0): 'b' == 'b' -> Len 1 ("b")

Center i = 0 (Even center 'b','a'):
Expand (0, 1): 'b' != 'a' -> Stop

Center i = 1 (Odd center 'a'):
Expand (1, 1): 'a' == 'a' -> Len 1
Expand (0, 2): 'b' == 'b' -> Len 3 ("bab") 🎉 (MAX SO FAR!)
Expand (-1, 3): Out of bounds -> Stop

Center i = 1 (Even center 'a','b'):
Expand (1, 2): 'a' != 'b' -> Stop

Center i = 2 (Odd center 'b'):
Expand (2, 2): 'b' == 'b' -> Len 1
Expand (1, 3): 'a' == 'a' -> Len 3 ("aba")
Expand (0, 4): 'b' != 'd' -> Stop

Longest Palindromic Substring Result: "bab" (or "aba") ✅
```

## 5. Visual Diagram
Odd vs Even Expansion Centers Visualized:

```
Odd Length Palindrome ("aba"):
Index:      0   1   2
Chars:      a   b   a
            ^   ^   ^
          left center right  (Center = index 1)

Even Length Palindrome ("abba"):
Index:      0   1   2   3
Chars:      a   b   b   a
                ^   ^
            left     right   (Center = index 1 and 2 pair)
```

## 6. Operations / Algorithms
LeetCode 5 Longest Palindromic Substring Implementation:

```java
public String longestPalindrome(String s) {
    if (s == null || s.length() < 1) return "";
    int start = 0, maxLen = 0;

    for (int i = 0; i < s.length(); i++) {
        // 1. Expand around odd-length center (i, i)
        int len1 = expandFromCenter(s, i, i);
        // 2. Expand around even-length center (i, i + 1)
        int len2 = expandFromCenter(s, i, i + 1);

        int len = Math.max(len1, len2);
        if (len > maxLen) {
            maxLen = len;
            // Calculate starting index of longest palindrome
            start = i - (len - 1) / 2;
        }
    }

    return s.substring(start, start + maxLen);
}

private int expandFromCenter(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return right - left - 1; // Length of valid palindrome
}
```

> **Quick Syntax:**
```java
// Length Formula after expansion loop exits:
int validLen = right - left - 1;

// Starting Index Formula:
int start = i - (len - 1) / 2;
```

## 7. Examples
* **LeetCode 5 - Longest Palindromic Substring**: Expand Around Center in $O(N^2)$ time and $O(1)$ space.
* **LeetCode 647 - Palindromic Substrings**: Counting total palindromic substrings.
* **LeetCode 125 - Valid Palindrome**: Checking two-pointer palindrome with alphanumeric filtering.

## 8. Java Code
Complete interview-ready Java suite implementing Longest Palindromic Substring, Palindromic Substring Counter, and Valid Palindrome:

```java
public class PalindromeAlgorithmsMaster {

    // 1. Longest Palindromic Substring (LeetCode 5) O(N^2) Time, O(1) Space
    public static String longestPalindrome(String s) {
        if (s == null || s.length() < 1) return "";
        int start = 0, maxLen = 0;

        for (int i = 0; i < s.length(); i++) {
            int len1 = expand(s, i, i);     // Odd center
            int len2 = expand(s, i, i + 1); // Even center
            int len = Math.max(len1, len2);

            if (len > maxLen) {
                maxLen = len;
                start = i - (len - 1) / 2;
            }
        }

        return s.substring(start, start + maxLen);
    }

    // 2. Count Palindromic Substrings (LeetCode 647) O(N^2) Time, O(1) Space
    public static int countSubstrings(String s) {
        if (s == null || s.length() == 0) return 0;
        int count = 0;

        for (int i = 0; i < s.length(); i++) {
            count += countPalindromes(s, i, i);     // Odd center count
            count += countPalindromes(s, i, i + 1); // Even center count
        }

        return count;
    }

    // Helper: Expand and return max palindrome length
    private static int expand(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }

    // Helper: Expand and return total count of valid palindromes
    private static int countPalindromes(String s, int left, int right) {
        int count = 0;
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            count++;
            left--;
            right++;
        }
        return count;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String sample = "babad";
        System.out.println("Input String: " + sample);
        System.out.println("Longest Palindromic Substring: \"" + longestPalindrome(sample) + "\""); // "bab"
        System.out.println("Total Palindromic Substrings Count: " + countSubstrings(sample));     // 7 ("b","a","b","a","d","bab","aba")
    }
}
```

## 9. Complexity Analysis
| Algorithm Variant | Time Complexity | Auxiliary Space | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Expand Around Center** | **$O(N^2)$** | **$O(1)$ Constant** | Zero memory allocation ⚡ |
| **2D Dynamic Programming** | $O(N^2)$ | $O(N^2)$ Matrix | Allocates boolean DP matrix |
| **Naive Substring Search** | $O(N^3)$ | $O(N)$ | Substring checks inside loops |

## 10. Edge Cases
* **Single Character String (`length == 1`)**: Returns original string immediately.
* **String with All Same Characters** (e.g., `"aaaaa"`): Expands to full string length $N$ on center $(N/2)$.
* **No Multi-Character Palindrome** (e.g., `"abcde"`): Returns first character `"a"` as max length 1.

## 11. Common Mistakes
* Testing ONLY odd centers `(i, i)` and forgetting even centers `(i, i + 1)` (misses even palindromes like `"abba"`!).
* Writing `validLen = right - left + 1` instead of **`right - left - 1`** after expansion loop terminates (the loop exits AFTER `left` and `right` step past the valid boundary!).
* Calculating start index as `start = i - len / 2` instead of **`start = i - (len - 1) / 2`** (causes off-by-one errors for even-length palindromes).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is `validLen = right - left - 1` after `while` loop exits?
> When `while (left >= 0 && right < N && S[left] == S[right])` exits, `left` has stepped 1 position too far to the left, and `right` has stepped 1 position too far to the right! The true boundaries are `left + 1` to `right - 1`.
> True length = `(right - 1) - (left + 1) + 1 = right - left - 1`.

> **Memory Trick:** **"Expand loop exits -> Length = right - left - 1; Start = i - (len - 1) / 2"**.

## 13. Comparisons
| Feature | Expand Around Center | 2D Dynamic Programming |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N^2)$ | $O(N^2)$ |
| **Space Complexity**| **$O(1)$ (In-Place)** | $O(N^2)$ (DP Matrix) |
| **Code Length** | Short ($\approx 20$ lines) | Longer ($\approx 35$ lines) |
| **Interview Recommendation** | **PREFERRED** | Secondary |

## 14. How to Recognize This in Questions
* **"Find longest palindromic substring"** $\rightarrow$ Expand Around Center ($O(N^2)$ time, $O(1)$ space).
* **"Count total palindromic substrings"** $\rightarrow$ Expand Around Center.

## 15. Frequently Asked Interview Questions
* **Q: Why are there $2N - 1$ centers for expansion in a string of length $N$?**  
  *A:* There are $N$ single character centers for odd-length palindromes, and $N - 1$ adjacent character pair centers for even-length palindromes $\implies N + (N - 1) = 2N - 1$ total expansion centers.
* **Q: How does `start = i - (len - 1) / 2` work for both odd and even length palindromes?**  
  *A:* For odd `len = 3` at `i = 1`: `start = 1 - (3-1)/2 = 0`. For even `len = 4` at `i = 1`: `start = 1 - (4-1)/2 = 1 - 1 = 0`. Integer division handles both cases perfectly!

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PALINDROME ALGORITHMS & EXPAND AROUND CENTER          |
+-----------------------------------------------------------------------+
| • Total Centers: 2N - 1 (N odd centers (i,i) + N-1 even centers (i,i+1))|
| • Expansion Condition: while (left>=0 && right<N && S[left]==S[right])|
| • Length Post-Expansion: len = right - left - 1                       |
| • Substring Start Index: start = i - (len - 1) / 2                    |
| • Complexity: O(N²) Time | O(1) Auxiliary Space (Optimal!)           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why there are $2N - 1$ expansion centers.
- [ ] I can derive the `right - left - 1` valid length formula.
- [ ] I can derive the `i - (len - 1) / 2` starting index formula.
- [ ] I can implement Longest Palindromic Substring in $O(1)$ space.
- [ ] I can count total palindromic substrings in $O(1)$ space.
