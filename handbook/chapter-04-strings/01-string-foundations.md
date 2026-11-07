# 01. String Foundations & Memory Mechanics

## 1. Introduction
A **String** is a sequence of characters stored sequentially in memory. In Java, `java.lang.String` is an immutable, final class that wraps an underlying byte/character array. In technical coding interviews, string manipulation problems evaluate a candidate's understanding of string immutability, the **String Constant Pool (SCP)**, memory efficiency, and $O(1)$ character indexing vs $O(N)$ string copying operations.

> **Important:** In Java, Strings are **immutable**. Any operation that appears to alter a string (such as concatenation `s += "a"` or `.substring()`) actually creates a brand-new String object on the JVM Heap!

## 2. Core Concepts
* **String Immutability**: Once created, a `String` object's content cannot be changed in memory. Immutability ensures thread safety, security (for network/file paths), and enables the String Constant Pool.
* **String Constant Pool (SCP)**: A special memory region inside the JVM Heap that caches literal String instances to save memory. Identical string literals share the exact same pool reference address.
* **Compact Strings (JDK 9+)**: Java 9+ optimizes string memory by storing characters in a `byte[]` array instead of `char[]`. Standard ASCII/Latin-1 strings take **1 byte per char** (LATIN1), while UTF-16 strings take **2 bytes per char** (UTF16).
* **Heap vs SCP Allocation**:
  * `String s1 = "hello";` $\to$ Allocates or reuses `"hello"` in the SCP.
  * `String s2 = new String("hello");` $\to$ Explicitly creates a NEW `String` object on the general Heap (referencing `"hello"` in the SCP).

> **Memory Trick:** **"Literals share SCP space; `new String()` creates duplicate Heap objects!"**

## 3. Characteristics / Properties
* **Immutability Performance Impact**:
  * Concatenating strings inside a loop using `+` takes $O(N^2)$ total time because each iteration copies all characters into a new string!
  * Using `StringBuilder` buffers character modifications in a dynamic byte array, taking **Amortized $O(N)$ time**.
* **Reference Equality (`==`) vs Value Equality (`.equals()`)**:
  * `==` checks if two reference variables point to the exact same RAM memory address.
  * `.equals()` compares the character sequence content cell by cell.

```
String Memory Allocation Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Instantiation Method  | Storage Location  | Duplicate Check   | Memory Overhead   |
+-----------------------+-------------------+-------------------+-------------------+
| Literal `"abc"`       | String Pool (SCP) | Shared (Pooled)   | Minimal           |
| `new String("abc")`   | General Heap      | Forces New Object | Object Header + SCP|
| `s.intern()`          | String Pool (SCP) | Returns Pooled Ref| Zero if exists    |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing JVM Memory Layout for String Allocations:

```java
String s1 = "java";                  // SCP allocation at 0x100
String s2 = "java";                  // Reuses 0x100 from SCP (s1 == s2 is TRUE!)
String s3 = new String("java");      // New Heap object at 0x500 (s1 == s3 is FALSE!)
String s4 = s3.intern();             // Returns 0x100 from SCP (s1 == s4 is TRUE!)
```

```
JVM Memory Layout Diagram:

   STACK (References)               HEAP MEMORY
+---------------------+          +--------------------------------------------+
| s1 = Addr 0x100 ----|--------->| [ String Constant Pool (SCP) ]             |
| s2 = Addr 0x100 ----|          |   0x100: String "java" {byte[] = [j,a,v,a]}|
|                     |          +--------------------------------------------+
| s3 = Addr 0x500 ----|--------->| [ General Heap Space ]                     |
| s4 = Addr 0x100 ----|          |   0x500: String Object -> points to 0x100   |
+---------------------+          +--------------------------------------------+
```

## 5. Visual Diagram
String Concatenation Loop Overhead ($O(N^2)$ Trap):

```
Loop Iteration 1: "a" + "b"       -> Allocates "ab"   (Copy 2 chars)
Loop Iteration 2: "ab" + "c"      -> Allocates "abc"  (Copy 3 chars)
Loop Iteration 3: "abc" + "d"     -> Allocates "abcd" (Copy 4 chars)
...
Total Characters Copied = 2 + 3 + 4 + ... + N = O(N²) Time Complexity! 🐢

StringBuilder Optimization:
Single dynamic byte[] buffer -> Appends in-place -> Final toString() takes O(N) Time! ⚡
```

## 6. Operations / Algorithms
Core String Operations and Java Syntax:

### 1. Character Access & Conversion
```java
String s = "leetcode";
int len = s.length();             // O(1) Length query
char first = s.charAt(0);          // O(1) Index access
char[] charArr = s.toCharArray();  // O(N) Conversion to char array
```

### 2. StringBuilder Dynamic Construction Idiom
```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    sb.append(arr[i]); // Amortized O(1) append
}
String result = sb.toString(); // O(N) final string creation
```

> **Quick Syntax:**
```java
// String Interning Trick
String pooledRef = unpooledString.intern(); // Guarantees SCP reference
```

## 7. Examples
* **LeetCode 125 - Valid Palindrome**: Checking string palindrome after stripping non-alphanumeric characters.
* **LeetCode 14 - Longest Common Prefix**: Horizontal / vertical character scanning.
* **LeetCode 151 - Reverse Words in a String**: Tokenizing and reversing string word order.

## 8. Java Code
Complete interview-ready Java suite demonstrating String Pool comparisons, `StringBuilder` performance, and string immutability mechanics:

```java
public class StringFoundationsMaster {

    // 1. String Pool & Reference Comparison Demo
    public static void demonstrateStringPool() {
        String s1 = "hello";
        String s2 = "hello";
        String s3 = new String("hello");
        String s4 = s3.intern();

        System.out.println("s1 == s2 (Both SCP): " + (s1 == s2));           // true
        System.out.println("s1 == s3 (SCP vs Heap): " + (s1 == s3));       // false
        System.out.println("s1.equals(s3) (Value check): " + s1.equals(s3)); // true
        System.out.println("s1 == s4 (s3.intern()): " + (s1 == s4));       // true
    }

    // 2. StringBuilder vs String Concatenation Benchmark Demonstration
    public static void compareConcatenationPerformance(int iterations) {
        // String Concatenation O(N^2)
        long start1 = System.nanoTime();
        String str = "";
        for (int i = 0; i < iterations; i++) {
            str += "a"; // Creates new String object on every iteration!
        }
        long duration1 = (System.nanoTime() - start1) / 1_000_000;

        // StringBuilder O(N)
        long start2 = System.nanoTime();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < iterations; i++) {
            sb.append("a"); // Appends in-place to dynamic buffer
        }
        String result = sb.toString();
        long duration2 = (System.nanoTime() - start2) / 1_000_000;

        System.out.println("Iterations: " + iterations);
        System.out.println("String Concatenation ('+'): " + duration1 + " ms (SLOW O(N^2))");
        System.out.println("StringBuilder ('append'): " + duration2 + " ms (FAST O(N))");
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        System.out.println("--- 1. String Pool Memory Checks ---");
        demonstrateStringPool();

        System.out.println("\n--- 2. Performance Comparison Benchmark ---");
        compareConcatenationPerformance(50000); // 50,000 concatenations
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **`s.length()`** | **$O(1)$** | $O(1)$ | Stored length property |
| **`s.charAt(i)`** | **$O(1)$** | $O(1)$ | Direct array offset lookup |
| **`s.toCharArray()`** | $O(N)$ | $O(N)$ | Allocates new `char[]` array |
| **`s1 + s2` (Concatenation)**| $O(N_1 + N_2)$ | $O(N_1 + N_2)$ | Allocates new combined String |
| **`StringBuilder.append()`**| **Amortized $O(1)$**| $O(1)$ | Dynamic array expansion ($2\times$) |
| **`s.substring(start, end)`**| $O(K)$ | $O(K)$ | Copies $K$ characters in JDK 7+ |

## 10. Edge Cases
* **Null String Reference**: Calling methods on `String s = null` (e.g., `s.length()`) throws `NullPointerException`. Guard with `if (s == null || s.isEmpty())`.
* **String Substring Out of Bounds**: `s.substring(start, end)` where `start < 0` or `end > s.length()` or `start > end` throws `StringIndexOutOfBoundsException`.
* **JDK 7+ Substring Copying**: In Java 7+, `substring()` creates a complete copy of the character range, taking $O(K)$ time and space (eliminating old memory leak issues from JDK 6).

## 11. Common Mistakes
* Using `==` to compare string contents instead of `.equals()`.
* Using String `+` concatenation inside loops instead of `StringBuilder`.
* Forgetting that `String` objects are immutable (e.g., calling `s.replace('a', 'b')` without assigning the result `s = s.replace('a', 'b')`).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why was `String.substring()` changed in JDK 7?
> In JDK 6, `substring()` shared the main string's internal character array, using offsets. If you created a tiny substring from a 10MB string, the entire 10MB array remained pinned in RAM (Memory Leak!). JDK 7+ changed `substring()` to copy only the target characters ($O(K)$ time/space), freeing the original string for GC.

> **Memory Trick:** **"Always assign string method return values: `s = s.toUpperCase();`"** (Original string is never modified!).

## 13. Comparisons
| Feature | `java.lang.String` | `java.lang.StringBuilder` | `java.lang.StringBuffer` |
| :--- | :--- | :--- | :--- |
| **Mutability** | Immutable | **Mutable** | **Mutable** |
| **Thread Safety** | Thread-Safe (Immutable) | **Unsynchronized (Fast)** | Synchronized (Slow) |
| **Performance** | Slow for loops | **Fastest for single thread**| Slightly slower |
| **Use Case** | Constants & Keys | **DSA Algorithms & Loops** | Multi-threaded code |

## 14. How to Recognize This in Questions
* **"Construct a string dynamically from loop iterations"** $\rightarrow$ Use `StringBuilder`.
* **"Check if two strings are identical in character content"** $\rightarrow$ Use `s1.equals(s2)`.

## 15. Frequently Asked Interview Questions
* **Q: Why are Strings immutable in Java?**  
  *A:* Immutability provides: (1) **Security** for network sockets/file paths, (2) **Thread Safety** without synchronization, (3) **Caching** via the String Constant Pool, and (4) **HashCode Caching** (computed once and cached).
* **Q: What is the difference between `StringBuilder` and `StringBuffer`?**  
  *A:* `StringBuilder` is unsynchronized and faster, making it ideal for single-threaded DSA interview code. `StringBuffer` is synchronized and thread-safe, incurring locking overhead.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING FOUNDATIONS & MEMORY MECHANICS                 |
+-----------------------------------------------------------------------+
| • String is Immutable: s.replace() returns NEW string!                |
| • String Pool (SCP): Literals share memory; `new` forces new Heap obj |
| • Loop Concatenation Trap: s += "a" is O(N²) -> Use StringBuilder O(N)|
| • JDK 9+ Compact Strings: Stores ASCII as byte[] (1B per char)        |
| • JDK 7+ Substring: s.substring(l, r) takes O(K) time and space       |
| • Use StringBuilder (Fast, Unsynchronized) over StringBuffer            |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain the String Constant Pool (SCP) memory architecture.
- [ ] I know why `str += "a"` inside a loop causes $O(N^2)$ TLE slowdown.
- [ ] I know why `s.equals(t)` must be used instead of `s == t`.
- [ ] I understand the difference between `StringBuilder` and `StringBuffer`.
- [ ] I can write the `StringBuilder` dynamic string construction idiom.
