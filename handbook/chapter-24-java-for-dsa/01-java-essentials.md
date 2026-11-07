# 01. Java Essentials for DSA

## 1. Introduction
Java is a strongly-typed, object-oriented language that runs on the Java Virtual Machine (JVM). In technical interviews, mastery over Java's primitive types, reference wrappers, array mechanisms, and string immutability is mandatory for writing bug-free, high-performance algorithms.

> **Important:** Understanding how Java handles primitives vs object references, pass-by-value semantics, and memory allocations prevents common runtime bugs during coding interviews.

## 2. Core Concepts
* **Primitive Types vs Wrappers**:
  * Primitives (`int`, `long`, `double`, `boolean`, `char`, `byte`, `short`, `float`) store raw values directly on the stack.
  * Wrapper Objects (`Integer`, `Long`, `Double`, `Boolean`, `Character`) wrap primitives into heap objects, incurring a 16-byte object overhead.
* **Pass-By-Value Semantics**: Java is **strictly pass-by-value**. When passing an object reference to a method, Java passes a copy of the reference address value (NOT the object itself).
* **String Immutability**: `String` objects are immutable in Java. Any modification creates a new string in memory.

> **Memory Trick:** **"Primitives live on Stack, Objects live on Heap"**. Primitives have zero object headers and offer faster access due to CPU cache alignment.

## 3. Characteristics / Properties
* **Primitive Data Sizes**:
  * `byte`: 8 bits ($-128$ to $127$)
  * `short`: 16 bits ($-32,768$ to $32,767$)
  * `int`: 32 bits ($-2 \times 10^9$ to $2 \times 10^9$ / Integer.MIN_VALUE to Integer.MAX_VALUE)
  * `long`: 64 bits ($-9 \times 10^{18}$ to $9 \times 10^{18}$)
  * `char`: 16 bits (Unicode $0$ to $65,535$)
* **Auto-boxing and Unboxing**:
  * Auto-boxing: Automatic conversion of primitive to wrapper (`int` $\to$ `Integer`).
  * Unboxing: Automatic conversion of wrapper to primitive (`Integer` $\to$ `int`).
  * **Warning**: Unboxing a `null` wrapper throws a `NullPointerException`!

## 4. Internal Working
Memory layout comparing primitive array vs object array:

```
Primitive Array (int[] arr = new int[3]):
+------------------------------------------+
| Header (16B) | 10 (4B) | 20 (4B) | 30(4B)|  <-- Single Contiguous Memory Block
+------------------------------------------+

Object Array (Integer[] arr = new Integer[3]):
+------------------------------------------+
| Header (16B) | Ref1 (8B) | Ref2 (8B)... |  <-- Array of Pointers
+--------------------+-----------+---------+
                     |           |
                     v           v
                 [Integer 10] [Integer 20]     <-- Scattered Heap Objects
```

## 5. Visual Diagram
Pass-By-Value Mechanism for References:

```
 Caller Method                      Called Method
+------------------+               +------------------+
| refA = Addr 0x500| --- copy ---> | param = Addr 0x500|
+------------------+               +------------------+
         |                                  |
         v                                  v
+-----------------------------------------------------+
| Heap Object Node { val = 10, next = null } (0x500)  |
+-----------------------------------------------------+
Modifying param.val = 20 mutates the underlying heap object!
Reassigning param = new Node() does NOT change refA in caller!
```

## 6. Operations / Algorithms
Essential Java Idioms for Interviews:
1. **Array Instantiation**: `int[] arr = new int[n];` (initialized to `0`).
2. **String to Char Array**: `char[] chars = s.toCharArray();` (enables $O(1)$ index access).
3. **StringBuilder Usage**: Always use `StringBuilder` for loop string construction to guarantee $O(n)$ time complexity.
4. **Arrays Utility Functions**: `Arrays.sort()`, `Arrays.fill()`, `Arrays.copyOf()`.

> **Quick Syntax:**
```java
// String to Char Array & StringBuilder Construction
String s = "leetcode";
char[] arr = s.toCharArray(); // O(N) conversion

StringBuilder sb = new StringBuilder();
for (char c : arr) {
    sb.append(c); // O(1) amortized append
}
String result = sb.toString(); // O(N) final string creation
```

## 7. Examples
* **Fast Array Initialization**: `Arrays.fill(dp, -1);` (Sets all elements of 1D array to -1).
* **2D Array Matrix Initialization**: `int[][] matrix = new int[R][C];`.
* **String Comparison**: Always use `s1.equals(s2)`, NEVER `s1 == s2` (`==` compares memory addresses, not string contents!).

## 8. Java Code
Interview-ready Java code demonstrating essential syntax, array utilities, and reference manipulation:

```java
import java.util.Arrays;

public class JavaEssentialsDemo {

    // Demonstrates reference mutation vs reference reassignment
    public static void modifyArray(int[] arr) {
        if (arr != null && arr.length > 0) {
            arr[0] = 999; // Mutates heap object -> visible to caller!
        }
        arr = new int[]{1, 2, 3}; // Reassigns local copy -> NOT visible to caller!
    }

    public static void main(String[] args) {
        int[] nums = {10, 20, 30};
        modifyArray(nums);
        System.out.println("nums[0] after method call: " + nums[0]); // Prints 999

        // Fast Array Operations
        int[] data = {5, 2, 8, 1, 9};
        Arrays.sort(data); // Dual-Pivot Quicksort: O(n log n)
        System.out.println("Sorted: " + Arrays.toString(data));

        // Binary Search on sorted array
        int index = Arrays.binarySearch(data, 8);
        System.out.println("Index of 8: " + index);
    }
}
```

## 9. Complexity Analysis
| Java Operation | Time Complexity | Auxiliary Space | Key Gotcha |
| :--- | :--- | :--- | :--- |
| **`s.length()` / `arr.length`** | $O(1)$ | $O(1)$ | Stored property lookup |
| **`s.charAt(i)`** | $O(1)$ | $O(1)$ | Direct character indexing |
| **`s.toCharArray()`** | $O(n)$ | $O(n)$ | Allocates new `char[]` copy |
| **`Arrays.sort(primitive[])`**| $O(n \log n)$ | $O(\log n)$ | Dual-Pivot Quicksort (unstable) |
| **`Arrays.sort(Object[])`** | $O(n \log n)$ | $O(n)$ | Timsort (stable) |
| **`String1 + String2` in loop**| $O(n^2)$ | $O(n^2)$ | Creates new string allocation every loop |

## 10. Edge Cases
* **Integer Wrapper Cache (`-128` to `127`)**: `Integer a = 100, b = 100; a == b` is `true` (cached). `Integer a = 500, b = 500; a == b` is `false`! ALWAYS use `.equals()` for wrappers.
* **Array Index Out of Bounds**: Accessing `arr[arr.length]` throws `ArrayIndexOutOfBoundsException`.
* **Null Pointer Exception on Unboxing**: `Integer val = null; int x = val;` throws `NullPointerException` during unboxing.

## 11. Common Mistakes
* Using `==` to compare Object wrappers or Strings.
* Using `String` concatenation `+` inside a loop instead of `StringBuilder`.
* Instantiating new objects inside inner loops, causing high garbage collection (GC) pressure.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `Integer` cache ranges from `-128` to `127`. Comparing `Integer a = 127` and `Integer b = 127` with `==` returns `true`, but `Integer a = 128` and `Integer b = 128` with `==` returns `false`! ALWAYS compare wrapper objects using `a.equals(b)`.

> **Memory Trick:** **"Arrays.sort() is Dual-Pivot Quicksort for primitives, Timsort for objects"**.

## 13. Comparisons
| Feature | `int[]` (Primitive Array) | `ArrayList<Integer>` (Collection) |
| :--- | :--- | :--- |
| **Memory Layout** | Contiguous raw ints | Array of pointers to Integer objects |
| **Memory Footprint** | $4$ bytes per element | $\approx 24$ bytes per element (Object header overhead) |
| **Resizing** | Fixed size | Dynamic auto-resizing ($1.5\times$) |
| **Performance** | Maximum CPU cache locality | Slight pointer indirection overhead |

## 14. How to Recognize This in Questions
* **"Manipulate characters in a string repeatedly"** $\rightarrow$ Convert to `char[]` array or `StringBuilder`.
* **"Frequent lookup and frequency count"** $\rightarrow$ Use primitive `int[26]` frequency array for lowercase English letters instead of `HashMap<Character, Integer>`.

## 15. Frequently Asked Interview Questions
* **Q: Is Java Pass-By-Value or Pass-By-Reference?**  
  *A:* Java is **100% Pass-By-Value**. For object references, the value passed into the method is a copy of the reference address itself.
* **Q: Why should `int[26]` be preferred over `HashMap<Character, Integer>` for character counting?**  
  *A:* `int[26]` avoids object allocation, auto-boxing overhead, hashing computation, and memory fragmentation, operating in $O(1)$ space with zero GC overhead.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA ESSENTIALS FOR DSA                              |
+-----------------------------------------------------------------------+
| • Java is 100% Pass-By-Value (Copies reference address for objects)   |
| • Integer Cache (-128 to 127): Always use .equals() for Integer       |
| • Character Counting: Prefer int[26] over HashMap<Character, Integer> |
| • String loop concatenation: Use StringBuilder (O(n) vs O(n²))        |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain Java's pass-by-value mechanics for object references.
- [ ] I know why `.equals()` must be used instead of `==` for object wrappers.
- [ ] I understand the memory overhead differences between `int[]` and `ArrayList<Integer>`.
- [ ] I know how to use `Arrays.sort()`, `Arrays.fill()`, and `Arrays.binarySearch()`.
- [ ] I can use `StringBuilder` to build strings in $O(n)$ time.
