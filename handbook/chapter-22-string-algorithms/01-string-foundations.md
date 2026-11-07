# 01. String Foundations: Representations, Memory Layouts & Invariants

## 1. Introduction
**String Processing** forms the core of textual data manipulation, pattern matching, natural language processing, compilers, and network protocol parsers. Mathematically, a **String $S$** is an ordered sequence of characters $S = s_0 s_1 s_2 \dots s_{N-1}$ drawn from a finite alphabet $\Sigma$ of size $|\Sigma|$ (e.g., ASCII $|\Sigma|=128/256$, Lowercase English $|\Sigma|=26$, Binary $|\Sigma|=2$). In Java, strings are represented as immutable objects backed by byte arrays (`byte[]` with Compact Strings in JDK 9+), enforcing **String Constant Pool Interning**, **Immutable Hash Code Caching**, and $O(1)$ length access while requiring mutable structures like `StringBuilder` for high-speed string modifications.

> **Important:** The 4 Structural Invariants of String Representation:
> 1. **Java Compact String Memory Layout (JDK 9+)**:
>    - Strings store characters as `byte[] coder` using LATIN1 (1 byte per char) if all characters fit in ASCII/Latin1 ($0 \dots 255$), or UTF-16 (2 bytes per char) if Unicode characters exist.
> 2. **String Immutability & Hash Caching**:
>    - Strings are immutable. The 32-bit hash code `int hash` is calculated lazily on the first `.hashCode()` call and cached permanently.
> 3. **Substrings, Prefixes & Suffixes**:
>    - A **Prefix** is a substring starting at index 0 ($S[0 \dots k]$).
>    - A **Suffix** is a substring ending at index $N-1$ ($S[k \dots N-1]$).
>    - A string of length $N$ has $N+1$ prefixes, $N+1$ suffixes, and $\frac{N(N+1)}{2}$ non-empty substrings.
> 4. **String Pool Invariant**: Literal strings `"hello"` are stored in the heap's String Constant Pool to save memory via object deduplication. ⚡

```
String Memory Representation Topology:
String s = "DSA" -> Heap Object:
┌─────────────────────────────────────────┐
│ Object Header (12 Bytes)                │
│ hash: 67891 (Cached 32-bit Hash)        │
│ coder: 0 (LATIN1: 1 byte per char)      │
│ value: [ 'D', 'S', 'A' ] (byte[])      │
└─────────────────────────────────────────┘

Compact String saves 50% memory footprint compared to UTF-16 char[]! ⚡
```

---

## 2. Core Concepts & String Data Structures Matrix

### 2.1 String Mechanics Strategy Matrix
```
String Data Structure Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Component / Structure | Mutability        | Thread Safety     | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+
| **java.lang.String**  | **Immutable ⚡**  | **Thread-Safe ⚡**| Hash Caching / Pool|
| **StringBuilder**     | **Mutable ⚡**    | Non-Thread-Safe   | Fast Appends $O(1)$|
| **StringBuffer**      | **Mutable ⚡**    | **Thread-Safe (Sync)**| Concurrent Edit  |
| **char[] Array**      | **Mutable ⚡**    | Non-Thread-Safe   | In-Place Mutation |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"String is immutable with cached hash code; StringBuilder is mutable for fast append O(1) loops!"**

---

## 3. Characteristics & Java Polynomial Rolling Hash Formula Proof

### 3.1 Mathematical Proof of Java String Hash Code Formula
* Java's `String.hashCode()` computes a polynomial rolling hash over characters $s_0, s_1 \dots s_{N-1}$ using base prime $P = 31$:
  $$H(S) = \sum_{i=0}^{N-1} s_i \cdot 31^{N - 1 - i} = s_0 \cdot 31^{N-1} + s_1 \cdot 31^{N-2} + \dots + s_{N-1}$$
* Computed using **Horner's Method** in $O(N)$ time:
  $$H_0 = 0, \quad H_{i+1} = 31 \cdot H_i + s_i$$
* Base $31$ is chosen because $31 \cdot x = (x \ll 5) - x$, allowing modern compilers to replace integer multiplication with a 1-cycle bitwise shift and subtraction! ⚡

---

## 4. Internal Working Mechanics: String Concatenation Bottleneck vs StringBuilder

Why string concatenation (`s += ch`) inside a loop is an $O(N^2)$ anti-pattern:

```
String Loop Concatenation Anti-Pattern (N Iterations):

Loop i = 0: s = "" + 'a'     -> Allocates new String size 1  (Copy 1 char)
Loop i = 1: s = "a" + 'b'    -> Allocates new String size 2  (Copy 2 chars)
Loop i = 2: s = "ab" + 'c'   -> Allocates new String size 3  (Copy 3 chars)
...
Total Characters Copied: 1 + 2 + 3 + ... + N = N(N+1)/2 = O(N^2) Time! ❌

StringBuilder Amortized Append (N Iterations):
Resizable array doubles capacity when full.
Total Amortized Time: O(1) per append -> O(N) Total Time! ✅
```

---

## 5. Visual Diagram: Prefix vs Proper Prefix vs Suffix Topography

```
String S = "ABAC":

Prefixes:          "", "A", "AB", "ABA", "ABAC"
Proper Prefixes:   "", "A", "AB", "ABA"  (Excludes full string "ABAC")

Suffixes:          "", "C", "AC", "BAC", "ABAC"
Proper Suffixes:   "", "C", "AC", "BAC"  (Excludes full string "ABAC")

Border (Prefix == Suffix): Longest Proper Prefix that is also a Proper Suffix! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing custom Polynomial Rolling Hash evaluation, String Substring Generators, and In-Place Character Reversal utilities.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing String Foundations,
 * Polynomial Rolling Hash Engines, and Substring Analytics.
 */
public class StringFoundationsMaster {

    // =========================================================================
    // 1. POLYNOMIAL ROLLING HASH EVALUATOR (Horner's Rule Base 31)
    // =========================================================================
    /**
     * Computes Java string hash code manually using Horner's Method:
     * H = 31 * H + s[i]
     *
     * @param s input string
     * @return 32-bit integer hash code
     */
    public int computeJavaHashCode(String s) {
        if (s == null || s.length() == 0) return 0;

        int h = 0;
        for (int i = 0; i < s.length(); i++) {
            h = 31 * h + s.charAt(i); // Equivalent to (h << 5) - h + charAt(i)
        }

        return h;
    }

    // =========================================================================
    // 2. PREFIX & SUFFIX GENERATOR ENGINES
    // =========================================================================
    /**
     * Generates all proper prefixes of a string.
     */
    public List<String> getProperPrefixes(String s) {
        List<String> prefixes = new ArrayList<>();
        if (s == null || s.length() <= 1) return prefixes;

        for (int i = 1; i < s.length(); i++) {
            prefixes.add(s.substring(0, i));
        }

        return prefixes;
    }

    /**
     * Generates all proper suffixes of a string.
     */
    public List<String> getProperSuffixes(String s) {
        List<String> suffixes = new ArrayList<>();
        if (s == null || s.length() <= 1) return suffixes;

        for (int i = 1; i < s.length(); i++) {
            suffixes.add(s.substring(i));
        }

        return suffixes;
    }

    // =========================================================================
    // 3. IN-PLACE CHAR ARRAY STRING REVERSAL (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Reverses a char array in-place without auxiliary memory.
     */
    public void reverseCharArray(char[] s) {
        if (s == null || s.length <= 1) return;

        int left = 0;
        int right = s.length - 1;

        while (left < right) {
            char temp = s[left];
            s[left] = s[right];
            s[right] = temp;
            left++;
            right--;
        }
    }
}
```

> **Quick Syntax:**
```java
// Horner's Polynomial Hash Line
h = 31 * h + s.charAt(i);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 344 - Reverse String**:
   - In-place two-pointer character array reversal ($O(N)$ time, $O(1)$ space).

2. **LeetCode 28 - Find the Index of the First Occurrence in a String**:
   - Fundamental substring search paradigm.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class StringFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     STRING FOUNDATIONS & HASHING DEMO           ");
        System.out.println("=================================================\n");

        StringFoundationsMaster master = new StringFoundationsMaster();

        // 1. Hash Code Verification Test
        String str = "Antigravity";
        int manualHash = master.computeJavaHashCode(str);
        int nativeHash = str.hashCode();
        System.out.println("1. String: \"" + str + "\"");
        System.out.println("   Manual Base-31 Hash: " + manualHash);
        System.out.println("   Native s.hashCode() : " + nativeHash);
        System.out.println("   Hashes Match        : " + (manualHash == nativeHash));
        System.out.println("-------------------------------------------------");

        // 2. Prefixes and Suffixes Test
        String target = "ABAC";
        System.out.println("2. String: \"" + target + "\"");
        System.out.println("   Proper Prefixes: " + master.getProperPrefixes(target));
        System.out.println("   Proper Suffixes: " + master.getProperSuffixes(target));
        System.out.println("-------------------------------------------------");

        // 3. In-Place Char Array Reversal Test
        char[] charArr = {'h', 'e', 'l', 'l', 'o'};
        System.out.println("3. Original Char Array: " + Arrays.toString(charArr));
        master.reverseCharArray(charArr);
        System.out.println("   Reversed Char Array: " + Arrays.toString(charArr));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| String Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`s.length()` Access**| $\mathbf{O(1)}$ Constant ⚡| $\mathbf{O(1)}$ Memory ⚡| Cached field |
| **`s.charAt(i)` Access**| $\mathbf{O(1)}$ Constant ⚡| $\mathbf{O(1)}$ Memory ⚡| Direct array indexing |
| **`s.hashCode()`**    | $\mathbf{O(N)}$ First Call | $\mathbf{O(1)}$ Space ⚡| Cached permanently after |
| **`s.substring(i, j)`**| $\mathbf{O(j - i)}$ Linear | $O(j - i)$ Memory | Creates new byte[] copy |
| **`s += ch` (In Loop)**| $O(N^2)$ Anti-Pattern ❌| $O(N^2)$ Memory Heap | Repeated allocations |
| **`sb.append(ch)`**   | $\mathbf{O(1)}$ Amortized ⚡| $O(N)$ Buffer Space | Resizable array |

---

## 10. Edge Cases & Boundary Handling

1. **Null or Empty Strings (`""`)**:
   - `s.length() == 0` returns hash 0 without array operations.

2. **Surrogate Pair Unicode Characters (e.g. Emoji `😀`)**:
   - Consists of 2 `char` units (High and Low surrogates). Standard `s.length()` returns 2. Use `s.codePointCount(0, s.length())` for true Unicode character count.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Concatenating Strings with `+` Inside Loops**:
  - Creates $O(N^2)$ temporary garbage objects. Always use **`StringBuilder`** for loop concatenations.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Base 31 is Used in Java HashCode:
> 1. **31 is Prime**: Minimizes hash collisions across ASCII character distributions.
> 2. **Compiler Optimization**: $31 \cdot x = (x \ll 5) - x$ runs in 1 clock cycle! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | java.lang.String | StringBuilder | char[] Array |
| :--- | :--- | :--- | :--- |
| **Mutability** | Immutable | **Mutable ⚡** | **Mutable ⚡** |
| **Thread Safety** | **Thread-Safe ⚡** | Non-Thread-Safe | Non-Thread-Safe |
| **Hash Caching** | **Cached ⚡** | None | None |

---

## 14. How to Recognize This in Questions

* **"Construct string result through N iterations efficiently"** $\rightarrow$ StringBuilder ($O(N)$ time).
* **"Find longest proper prefix that is also a proper suffix"** $\rightarrow$ String Border Invariant (KMP Prefix Table).

---

## 15. Frequently Asked Interview Questions

* **Q: Why are Java Strings immutable?**  
  *A:* For security (URL/File parameters), String Constant Pool sharing (memory savings), thread safety (no synchronization required), and permanent hash code caching.

* **Q: How does JDK 9 Compact Strings reduce memory footprint?**  
  *A:* By storing characters in a `byte[]` instead of `char[]`. If all characters fit in Latin-1 ($0 \dots 255$), each char takes 1 byte instead of 2 bytes, cutting string memory usage by 50%.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING FOUNDATIONS                                    |
+-----------------------------------------------------------------------+
| • Java Storage  : Compact Strings byte[] (Latin-1 1 byte, UTF-16 2 B) |
| • Hash Formula  : H = 31 * H + s.charAt(i) (Horner's Method)          |
| • Shift Optim   : 31 * x = (x << 5) - x (1 CPU clock cycle)           |
| • Substring Count: N * (N + 1) / 2 Non-empty Substrings                |
| • Loop Concats  : NEVER use s += ch; ALWAYS use StringBuilder! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can explain Java Compact Strings memory layout (`byte[] coder`).
- [ ] I can write manual string hash code calculation using base 31 Horner's rule.
- [ ] I can state why string loop concatenation with `+` is an $O(N^2)$ anti-pattern.
- [ ] I can write in-place char array reversal.
- [ ] I can state the number of non-empty substrings for a string of length $N$.
