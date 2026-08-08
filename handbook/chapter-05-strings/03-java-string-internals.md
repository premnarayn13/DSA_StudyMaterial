# 03. Java String Internals & Memory Optimization

## 1. Introduction
Deep technical understanding of Java String internals is a hallmark of senior engineering candidates. In Java, the evolution of string memory storage—from JDK 6 shared array references, to JDK 7+ Heap-based String Constant Pools, to JDK 9 Compact Strings, and JDK 11 String Deduplication—has fundamentally altered time and space complexity characteristics for string operations in coding interviews.

> **Important:** In JDK 9+, Java introduced **Compact Strings**, changing `String`'s internal storage from `char[]` (2 bytes per character) to `byte[]` plus an 8-bit `coder` flag. If a string contains only LATIN1 characters, it consumes **1 byte per char**, saving 50% memory!

## 2. Core Concepts
* **Internal Representation (JDK 9+)**:
  ```java
  public final class String {
      private final byte[] value; // Stores characters as bytes
      private final byte coder;   // 0 = LATIN1 (1 byte), 1 = UTF16 (2 bytes)
      private int hash;           // Caching computed hashCode (0 by default)
  }
  ```
* **HashCode Caching**: String hashCode is computed lazily upon first call to `.hashCode()` and stored in the `hash` instance field. Subsequent calls return `hash` instantly in **$O(1)$ constant time**.
* **String Deduplication (G1 Garbage Collector)**: A JVM feature that inspects `byte[]` values of distinct `String` objects on the heap and unifies duplicate byte arrays to point to a single shared heap array.
* **String Deduplication vs String Interning**:
  * **Interning (`s.intern()`)**: Manually places or retrieves string references from the String Constant Pool (SCP).
  * **G1 String Deduplication**: Automatic background GC process that unifies identical underlying `byte[]` arrays without changing String object identities.

> **Memory Trick:** **"LATIN1 = 1 Byte, UTF16 = 2 Bytes. HashCode is calculated once and cached!"**

## 3. Characteristics / Properties
* **Memory Footprint Evolution**:

```
JDK Version     Internal Array Type     ASCII Char Size      Object Overhead
-----------------------------------------------------------------------------------
JDK 6           char[]                  2 Bytes / char       24 Bytes + shared offset
JDK 7 / 8       char[]                  2 Bytes / char       24 Bytes + char[] header
JDK 9+          byte[] (Compact)        1 Byte / char        24 Bytes + byte[] header
```

* **HashCode Calculation Invariant**: If `hash == 0`, `.hashCode()` computes $\sum_{i=0}^{n-1} s[i] \cdot 31^{n-1-i}$. If result is 0, it recomputes, but for all non-zero values, it caches the result!

## 4. Internal Working
Tracing JVM Compact String Encoding & Hash Caching:

```
String s = "DSA"; // Contains LATIN1 characters ('D'=68, 'S'=83, 'A'=65)

Memory Block Allocation:
- byte[] value = [68, 83, 65] (3 Bytes total)
- byte coder   = 0 (LATIN1 Flag)
- int hash     = 0 (Uncomputed)

First call: s.hashCode()
Calculates: (68 * 31² + 83 * 31¹ + 65 * 31⁰) = 67888
Updates:    hash = 67888

Second call: s.hashCode() -> Returns cached 67888 instantly in O(1) time! ⚡
```

## 5. Visual Diagram
G1 GC String Deduplication Mechanics:

```
Before Garbage Collection Deduplication:
Heap Object A: String { byte[] -> [0x500: 'j', 'a', 'v', 'a'] }
Heap Object B: String { byte[] -> [0x820: 'j', 'a', 'v', 'a'] } (DUPLICATE MEMORY!)

After G1 GC String Deduplication Sweep:
Heap Object A: String { byte[] -------------> [0x500: 'j', 'a', 'v', 'a'] }
Heap Object B: String { byte[] ------------/  (Array 0x820 FREED by GC! ⚡)
```

## 6. Operations / Algorithms
String Internals & Hashcode Caching Idioms:

```java
// Demonstrating HashCode Caching Mechanics
String key = "very_long_string_identifier";

// First call: O(N) linear computation of polynomial hash
int h1 = key.hashCode(); 

// Second call: O(1) instant return of cached hash field!
int h2 = key.hashCode(); 
```

> **Quick Syntax:**
```java
// String Reflection Inspection (Educational/Debugging Concept)
java.lang.reflect.Field valueField = String.class.getDeclaredField("value");
valueField.setAccessible(true);
byte[] bytes = (byte[]) valueField.get("hello"); // Reads byte[] array in JDK 9+
```

## 7. Examples
* **HashMap Key Lookup Performance**: Strings make optimal HashMap keys because their hashCode is cached ($O(1)$ hash retrieval on all queries after insertion).
* **High-Throughput Web Services**: Enabling `-XX:+UseStringDeduplication` under G1 GC to reduce heap footprint by 15-20% in string-heavy applications.
* **String Multi-Threading**: Thread safety without locks because string state cannot be mutated by rival threads.

## 8. Java Code
Complete interview-ready Java benchmark inspecting string hashCode caching and demonstrating string deduplication concepts:

```java
public class StringInternalsMaster {

    // Demonstrates HashCode Caching Efficiency
    public static void testHashCodeCaching() {
        // Construct a large string
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000000; i++) {
            sb.append("a");
        }
        String largeString = sb.toString();

        // Measure First Call to hashCode() -> Computes polynomial O(N)
        long start1 = System.nanoTime();
        int hash1 = largeString.hashCode();
        long duration1 = System.nanoTime() - start1;

        // Measure Second Call to hashCode() -> Returns cached field O(1)
        long start2 = System.nanoTime();
        int hash2 = largeString.hashCode();
        long duration2 = System.nanoTime() - start2;

        System.out.println("First hashCode() call time:  " + duration1 + " ns (Computes O(N))");
        System.out.println("Second hashCode() call time: " + duration2 + " ns (Cached O(1) ⚡)");
        System.out.println("Hashes Match? " + (hash1 == hash2));
    }

    // Demonstrates Memory Overhead of Compact Strings (LATIN1 vs UTF-16)
    public static void inspectStringEncoding(String str) {
        System.out.println("String: \"" + str + "\" | Length: " + str.length());
        boolean isLatin1 = true;
        for (char c : str.toCharArray()) {
            if (c > 0xFF) { // Character outside LATIN1 (0..255)
                isLatin1 = false;
                break;
            }
        }
        System.out.println("Encoding Mode: " + (isLatin1 ? "LATIN1 (1 Byte/char ⚡)" : "UTF-16 (2 Bytes/char)"));
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        System.out.println("--- 1. HashCode Caching Benchmark ---");
        testHashCodeCaching();

        System.out.println("\n--- 2. Compact String Encoding Checks ---");
        inspectStringEncoding("Hello World"); // LATIN1
        inspectStringEncoding("Hello World 😀"); // UTF-16 due to Emoji
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity (1st Call) | Time Complexity (2nd Call) | Memory Footprint |
| :--- | :--- | :--- | :--- |
| **`s.hashCode()`** | $O(N)$ polynomial calculation | **$O(1)$ cached field return** | $4$ bytes cached `hash` field |
| **LATIN1 Storage** | N/A | N/A | **$1$ Byte per char** |
| **UTF-16 Storage** | N/A | N/A | **$2$ Bytes per char** |
| **`s.intern()`** | $O(N)$ string lookup in SCP | **$O(1)$ reference return** | Pointer in SCP Table |

## 10. Edge Cases
* **HashCode Zero Collision**: If a string's calculated polynomial hashCode evaluates to exactly `0`, Java does NOT cache it! It will recalculate $O(N)$ on every `.hashCode()` call. (Extremely rare edge case!).
* **Emoji Characters in Compact Strings**: Including a single Emoji (e.g., `"Hello 😀"`) forces the JVM to switch the ENTIRE string encoding from LATIN1 to UTF-16 (doubling byte storage for all characters in that string).

## 11. Common Mistakes
* Assuming `.hashCode()` calculates string hash in $O(N)$ time on every call (forgetting the cached `hash` field optimization).
* Believing string interning (`s.intern()`) should be called on millions of unique dynamic strings (bloats the native SCP StringTable, degrading JVM performance!).
* Expecting `String` characters to be stored in `char[]` in modern Java (JDK 9+ uses `byte[]`).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why are Strings the most popular key type for `HashMap` in Java?
> 1. **Immutability**: Guaranteed that the key's state will never change while inside the map.
> 2. **HashCode Caching**: First call computes hash; subsequent HashMap lookups execute in **$O(1)$ time** because the cached `hash` field is returned instantly without re-scanning characters!

> **Memory Trick:** **"Strings cache their HashCode — 1st call O(N), subsequent calls O(1)!"**

## 13. Comparisons
| Metric | `s.intern()` (Manual Interning) | `-XX:+UseStringDeduplication` (G1 GC) |
| :--- | :--- | :--- |
| **Trigger** | Manual code call in Java | Automatic background GC pass |
| **Target Storage** | String Constant Pool (SCP) | General Heap (`byte[]` array sharing) |
| **Reference Equality (`==`)**| Returns identical String reference | Keeps distinct String references (shares underlying bytes) |
| **Overhead** | Risk of SCP table bloat | Zero code overhead |

## 14. How to Recognize This in Questions
* **"Explain why String is preferred over custom objects as HashMap keys"** $\rightarrow$ Highlight Immutability + HashCode Caching ($O(1)$ lookup).
* **"Explain memory optimizations introduced in Java 9 for Strings"** $\rightarrow$ Compact Strings (`byte[]` array + `coder` flag).

## 15. Frequently Asked Interview Questions
* **Q: How does JDK 9+ Compact Strings optimize memory?**  
  *A:* Pre-JDK 9 stored all strings as `char[]` consuming 2 bytes per char. JDK 9+ checks if characters fit in LATIN1 (0..255). If so, it stores them in `byte[]` consuming 1 byte per char, cutting string memory consumption by 50%.
* **Q: What is the polynomial constant used in Java's String `.hashCode()`?**  
  *A:* Java uses multiplier **31** because: (1) It is an odd prime (reduces hash collisions), and (2) $31 \cdot i$ can be optimized by CPU compilers to bit shift `(i << 5) - i`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA STRING INTERNALS & MEMORY OPTIMIZATION          |
+-----------------------------------------------------------------------+
| • Compact Strings (JDK 9+): Stored as byte[] (1B/char LATIN1 vs 2B UTF16)|
| • HashCode Caching: Calculated once on 1st call O(N), cached for O(1) |
| • Hash Multiplier: Uses prime 31 (Compiler optimizes to (i << 5) - i) |
| • HashMap Advantage: Cached hash field makes String lookups ultra-fast |
| • G1 String Deduplication: Unifies duplicate byte[] arrays in background|
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain JDK 9+ Compact Strings (`byte[]` + `coder` flag).
- [ ] I know why `.hashCode()` execution is $O(1)$ after the first call.
- [ ] I can explain why 31 is chosen as the hash polynomial multiplier.
- [ ] I understand why Strings are the optimal key type for Java HashMaps.
- [ ] I know the difference between String Interning and G1 String Deduplication.
