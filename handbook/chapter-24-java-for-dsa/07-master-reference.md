# 07. Master Reference — Java for DSA

## 1. Introduction
This Master Reference acts as a rapid-scanning summary for **Chapter 3: Java for DSA**. It consolidates JVM memory mechanics, pass-by-value rules, generic type erasure, collections selection, and fast I/O idioms into a concentrated, high-yield interview cheat sheet.

> **Important:** Review this master reference 15 minutes before an interview to lock in Java-specific memory rules, comparator tricks, and collection choices.

## 2. Core Concepts Cheat Sheet
* **Primitives vs Wrappers**: Primitives (`int`, `long`) live on the Stack with zero header overhead. Objects (`Integer`, `Long`) live on the Heap with a 16-byte object header.
* **Pass-By-Value Rules**: Java passes copies of reference addresses. Mutating an object's fields mutates the underlying heap state; reassigning the parameter variable does NOT affect the caller.
* **Equals & HashCode**: Overriding `.equals()` REQUIRES overriding `.hashCode()`.
* **Collection Strategy**:
  * Use `ArrayDeque` for Stacks and Queues (Avoid legacy `Stack` and pointer-heavy `LinkedList`).
  * Use `PriorityQueue` for Min/Max Heaps (Always use `Integer.compare(a, b)` in Comparators).
  * Use `int[26]` frequency arrays for lowercase character counts instead of `HashMap<Character, Integer>`.

> **Memory Trick:** **"Pass-By-Value, Equals-HashCode, ArrayDeque for Stack, Integer.compare for PQ"**.

## 3. Collections Selection Matrix
```
+-----------------------------------------------------------------------------------------+
| DSA Need                      | Recommended Java Structure    | Underlying Structure    |
+-----------------------------------------------------------------------------------------+
| Dynamic Array / Random Access | ArrayList<T>                  | Dynamic Resizing Array  |
| LIFO Stack / FIFO Queue       | ArrayDeque<T>                 | Circular Array Buffer   |
| Top-K / Priority Min/Max      | PriorityQueue<T>              | Binary Heap             |
| Constant Key Lookup           | HashMap<K, V> / HashSet<T>    | Hash Table + RB Tree    |
| Sorted Keys / Range Queries   | TreeMap<K, V> / TreeSet<T>    | Red-Black Tree          |
| Fast Character Count          | int[26]                       | Primitive Array         |
+-----------------------------------------------------------------------------------------+
```

## 4. Hardware & Memory Footprint Table
| Structure | Object Header | Pointer Overhead | Element Size | Total Footprint (100 elements) |
| :--- | :--- | :--- | :--- | :--- |
| `int[100]` | $16$ bytes | $0$ (Contiguous) | $4$ bytes | $\approx 416$ bytes (Cache Friendly) |
| `Integer[100]` | $16$ bytes | $8$ bytes/ref | $24$ bytes/Integer | $\approx 3,216$ bytes (Cache Misses) |
| `ArrayList<Integer>` (100) | $24$ bytes | $8$ bytes/ref | $24$ bytes/Integer | $\approx 3,240$ bytes |
| `LinkedList<Integer>` (100)| $24$ bytes | $24$ bytes/Node | $24$ bytes/Integer | $\approx 4,824$ bytes |

## 5. Java Syntax Reminders & Snippets

> **Quick Syntax:**
```java
// 1. Min-Heap & Max-Heap PriorityQueue
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));

// 2. ArrayDeque Stack & Queue Idioms
Deque<Integer> stack = new ArrayDeque<>();
stack.push(10); 
int val = stack.pop();

Queue<Integer> queue = new ArrayDeque<>();
queue.offer(10); 
int nextVal = queue.poll();

// 3. String to Char Array & StringBuilder
char[] chars = str.toCharArray();
StringBuilder sb = new StringBuilder();
sb.append('a');
String result = sb.toString();

// 4. Safe Comparator Subtraction (Avoids Underflow)
Comparator<int[]> comp = (a, b) -> Integer.compare(a[0], b[0]);
```

## 6. Mandatory Edge Case & Trap Audit
* **Trap 1: `Integer` Cache (`-128` to `127`)**: `Integer a = 128, b = 128; a == b` evaluates to `false`! Always use `a.equals(b)`.
* **Trap 2: `PriorityQueue.remove(obj)`**: Deleting non-top items takes $O(N)$ time, NOT $O(\log N)$!
* **Trap 3: Comparator Underflow**: Writing `(a, b) -> a - b` underflows on `Integer.MIN_VALUE`. Always write `(a, b) -> Integer.compare(a, b)`.
* **Trap 4: `Scanner` Regex Bottleneck**: Using `Scanner` on $N \ge 10^5$ inputs causes TLE. Use `BufferedReader` + `StringTokenizer`.
* **Trap 5: Missing `out.flush()`**: Forgetting to flush `PrintWriter` results in empty submission outputs.

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 3                               |
+-----------------------------------------------------------------------+
| 1. Stack = Fast Scope Memory; Heap = Shared Object Storage             |
| 2. Java Generics = Type Erasure to Object at compile time             |
| 3. Always use ArrayDeque over Stack or LinkedList                      |
| 4. Comparators: Integer.compare(a, b) [Never a - b]                    |
| 5. Fast I/O: BufferedReader + StringTokenizer + PrintWriter.flush()   |
+-----------------------------------------------------------------------+
```

## 8. Final Practice Checklist
- [ ] I can explain Java's pass-by-value reference copy behavior.
- [ ] I know why `.equals()` and `.hashCode()` must both be overridden.
- [ ] I know how to write overflow-safe Comparators using `Integer.compare()`.
- [ ] I can instantiate `ArrayDeque` for Stacks and Queues.
- [ ] I can write the `FastScanner` template for competitive programming.
