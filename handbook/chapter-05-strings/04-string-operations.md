# 04. Fundamental String Operations

## 1. Introduction
Fundamental string operations—Substring Extraction, Reversal, Case Conversion, Trimming, Splitting, and Formatting—form the building blocks for string algorithms in technical coding interviews. Understanding the precise time and space complexity bounds of built-in Java string API methods prevents unexpected $O(N^2)$ hidden performance bottlenecks.

> **Important:** Methods like `String.split()`, `String.replaceAll()`, and `String.toLowerCase()` allocate new objects and execute in **$O(N)$ time and space**. Chaining these methods in a loop can accidentally degrade algorithm execution speed from $O(N)$ to $O(N^2)$!

## 2. Core Concepts
* **Substring Extraction (`s.substring(l, r)`)**: Extracts characters from start index `l` (inclusive) to end index `r` (exclusive) in $O(r - l)$ time and space.
* **In-Place Character Array Reversal**: Converting a String to `char[]` and reversing using Two Pointers (`left`, `right`) in $O(N)$ time.
* **String Splitting (`s.split(regex)`)**: Tokenizing a string using regular expressions into a `String[]` array.
* **String Join (`String.join(delimiter, elements)`)**: Concatenating an array/iterable of strings using a delimiter in $O(N)$ time.

> **Memory Trick:** **"Substring end index is EXCLUSIVE: `s.substring(0, 3)` extracts indices 0, 1, 2 (3 characters total!)"**.

## 3. Characteristics / Properties
* **Length Invariant in Substring**: Number of characters in `s.substring(start, end)` is strictly **`end - start`**.
* **Regex Performance Cost**: `s.split(" ")` uses simple character matching, but `s.split("\\s+")` invokes the full Java Regex Engine, adding noticeable runtime overhead.

```
Core String API Operations Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation / Method    | Time Complexity   | Auxiliary Space   | Key Detail        |
+-----------------------+-------------------+-------------------+-------------------+
| `s.length()`          | O(1)              | O(1)              | Direct field access|
| `s.charAt(i)`         | O(1)              | O(1)              | Direct array lookup|
| `s.substring(l, r)`   | O(r - l)          | O(r - l)          | Copies character subrange|
| `s.indexOf(target)`   | O(N * M)          | O(1)              | Brute force substring search|
| `s.split(regex)`      | O(N)              | O(N)              | Token array allocation|
| `String.join(delim)`  | O(N)              | O(N)              | Single StringBuilder pass|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Word Reversal (LeetCode 151) using Two-Pointer & Split:

```
Input String: "  the sky  is blue  "

Step 1: Trim leading/trailing spaces -> "the sky  is blue"
Step 2: Split by regex "\\s+" -> Tokens: ["the", "sky", "is", "blue"]
Step 3: Reverse token array using Two Pointers -> ["blue", "is", "sky", "the"]
Step 4: Join tokens with single space -> "blue is sky the" ✅
```

## 5. Visual Diagram
Substring Index Boundary Visualized:

```
String s = "L E E T C O D E"
Index:     0 1 2 3 4 5 6 7

  s.substring(2, 6)
             ^       ^
             |       |
           start    end
        (inclusive)(exclusive)

Extracted Characters: 'E', 'E', 'T', 'C' -> Length = 6 - 2 = 4!
```

## 6. Operations / Algorithms
Essential String Operations Code Snippets:

### 1. Reversing Words in a String (LeetCode 151)
```java
public String reverseWords(String s) {
    // Trim and split by one or more spaces
    String[] words = s.trim().split("\\s+");
    StringBuilder sb = new StringBuilder();
    
    // Iterate backward over words
    for (int i = words.length - 1; i >= 0; i--) {
        sb.append(words[i]);
        if (i > 0) sb.append(" ");
    }
    return sb.toString();
}
```

### 2. Manual Substring Comparison (`s.startsWith()`)
```java
// O(M) time prefix match helper
public boolean hasPrefix(String str, int startIndex, String prefix) {
    if (startIndex + prefix.length() > str.length()) return false;
    for (int i = 0; i < prefix.length(); i++) {
        if (str.charAt(startIndex + i) != prefix.charAt(i)) return false;
    }
    return true;
}
```

> **Quick Syntax:**
```java
// Fast Word Reversal via String.join and List reverse
String[] words = s.trim().split("\\s+");
List<String> list = Arrays.asList(words);
Collections.reverse(list);
String reversed = String.join(" ", list);
```

## 7. Examples
* **LeetCode 151 - Reverse Words in a String**: Tokenizing, reversing, and trimming strings.
* **LeetCode 387 - First Unique Character in String**: Utilizing `s.indexOf(ch) == s.lastIndexOf(ch)` for rapid checks.
* **LeetCode 14 - Longest Common Prefix**: Substring manipulation across an array of strings.

## 8. Java Code
Complete interview-ready Java suite demonstrating Word Reversal, Manual Character Array Reversal, Substring Extraction, and String Joining:

```java
import java.util.Arrays;

public class StringOperationsMaster {

    // 1. Reverse Words in a String (LeetCode 151) O(N) Time, O(N) Space
    public static String reverseWords(String s) {
        if (s == null || s.isEmpty()) return "";

        // Trim leading/trailing whitespace & split by contiguous spaces
        String[] words = s.trim().split("\\s+");
        StringBuilder sb = new StringBuilder();

        // Append words in reverse order
        for (int i = words.length - 1; i >= 0; i--) {
            sb.append(words[i]);
            if (i > 0) {
                sb.append(" ");
            }
        }

        return sb.toString();
    }

    // 2. In-Place Character Array Reversal O(N) Time, O(N) Space for array allocation
    public static String reverseString(String s) {
        if (s == null) return null;
        char[] chars = s.toCharArray();
        int left = 0, right = chars.length - 1;

        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }

        return new String(chars);
    }

    // 3. Find Longest Common Prefix across Array of Strings O(S) Time where S is total chars
    public static String longestCommonPrefix(String[] strs) {
        if (strs == null || strs.length == 0) return "";

        String prefix = strs[0];
        for (int i = 1; i < strs.length; i++) {
            while (strs[i].indexOf(prefix) != 0) {
                prefix = prefix.substring(0, prefix.length() - 1);
                if (prefix.isEmpty()) return "";
            }
        }

        return prefix;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Word Reversal
        String sampleStr = "  the sky  is blue  ";
        System.out.println("Original: \"" + sampleStr + "\"");
        System.out.println("Reversed Words: \"" + reverseWords(sampleStr) + "\""); // "blue is sky the"

        // Test Char Reversal
        System.out.println("Reversed Char String: " + reverseString("leetcode")); // "edocteel"

        // Test Longest Common Prefix
        String[] strs = {"flower", "flow", "flight"};
        System.out.println("Longest Common Prefix: \"" + longestCommonPrefix(strs) + "\""); // "fl"
    }
}
```

## 9. Complexity Analysis
| Operation / Method | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **`s.trim()`** | $O(N)$ | $O(N)$ | Strips leading/trailing whitespace |
| **`s.split("\\s+")`** | $O(N)$ | $O(N)$ | Regex split into `String[]` array |
| **`String.join(" ", arr)`**| $O(N)$ | $O(N)$ | Single StringBuilder pass |
| **`reverseWords(s)`** | $O(N)$ | $O(N)$ | Optimal linear pass |

## 10. Edge Cases
* **Multiple Consecutive Spaces**: `s = "a   b"` split by `" "` produces empty string tokens `""`. **Fix**: Split using regex `s.split("\\s+")`.
* **String Consisting Only of Spaces**: `s = "    "`. `s.trim()` produces empty string `""`.
* **Empty Input Array in `longestCommonPrefix`**: Guard with `if (strs == null || strs.length == 0) return "";`.

## 11. Common Mistakes
* Using `s.split(" ")` instead of `s.split("\\s+")` when strings contain multiple spaces (leaves empty tokens in array!).
* Forgetting that `s.substring(start, end)` is exclusive of `end` index (extracting 1 character less than intended).
* Calling `s.indexOf()` inside a nested loop, creating an unexpected $O(N \cdot M)$ or $O(N^2)$ algorithm bottleneck.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** To split a string by whitespace handling multiple spaces and leading/trailing blanks cleanly:
> Use: **`String[] words = s.trim().split("\\s+");`**
> * `\\s` matches any whitespace character (space, tab, newline).
> * `+` matches one or more occurrences.

> **Memory Trick:** **"s.substring(l, r) length is always (r - l)!"**

## 13. Comparisons
| Method | `s.split(" ")` | `s.split("\\s+")` |
| :--- | :--- | :--- |
| **Whitespace Handling**| Splitting by single space only | **Handles single/multiple spaces, tabs, newlines** |
| **Empty Tokens** | Creates empty `""` tokens for `"  "` | **Suppresses empty tokens** |
| **Regex Overhead** | Minimal | Standard Regex Engine |
| **Interview Score** | Error-prone | **PREFERRED & SAFE** |

## 14. How to Recognize This in Questions
* **"Reverse words in a string while preserving single spaces"** $\rightarrow$ `trim().split("\\s+")` + Backward Loop.
* **"Find common prefix across multiple strings"** $\rightarrow$ Shrinking prefix `substring(0, len-1)`.

## 15. Frequently Asked Interview Questions
* **Q: Why does `s.substring(start, end)` take $O(K)$ time and space in modern Java?**  
  *A:* In JDK 7+, `substring()` creates a new `String` object and copies $K = \text{end} - \text{start}$ characters into a new underlying array to prevent memory leaks from holding reference to the original large parent array.
* **Q: How do you perform in-place string modifications in Java?**  
  *A:* `java.lang.String` cannot be modified in-place due to immutability. You MUST convert to `char[]` (`s.toCharArray()`) or use `StringBuilder`, perform modifications, and convert back to String.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FUNDAMENTAL STRING OPERATIONS                        |
+-----------------------------------------------------------------------+
| • Substring: s.substring(start, end) -> Length = end - start          |
| • Clean Word Split: s.trim().split("\\s+") (Handles multiple spaces)  |
| • Reverse Words: Split -> Iterate backward over words -> Join         |
| • In-Place Edit Trick: Convert to char[] -> Modify -> new String(chars)|
| • Common Prefix: Shrink prefix via substring while indexOf != 0       |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `s.split("\\s+")` is preferred over `s.split(" ")`.
- [ ] I can implement Word Reversal (LeetCode 151) in $O(N)$ time.
- [ ] I can implement Longest Common Prefix using shrinking substrings.
- [ ] I understand why `s.substring(start, end)` is $O(K)$ time/space in JDK 7+.
- [ ] I can perform character array reversals using Two Pointers.
