# 02. Memory Model & Garbage Collection in Java

## 1. Introduction
Understanding the Java Virtual Machine (JVM) Memory Model is essential for analyzing space complexity, memory leaks, and object lifecycle overhead. In technical interviews, explaining how variables are stored across Stack Memory vs Heap Memory, along with Garbage Collection (GC) behavior, distinguishes senior candidates.

> **Important:** Auxiliary space analysis must account for JVM internal allocation costs: local variables and call frames sit on the **Stack**, while instantiated objects and arrays reside on the **Heap**.

## 2. Core Concepts
* **Stack Memory**: Fast, thread-private execution memory. Holds local variables, primitive data values, and object reference addresses. Allocated and freed automatically via LIFO stack frames.
* **Heap Memory**: Shared runtime memory. Holds all instantiated Objects, Arrays, and Instance Variables. Managed by Garbage Collection.
* **JVM Object Layout**: Every object on the heap incurs a **12 to 16-byte Object Header** (Mark Word + Klass Word) plus padding to 8-byte boundaries.
* **Garbage Collection (GC)**: Automatic memory management process that frees unreachable heap objects (objects with zero active references from Stack roots).

> **Memory Trick:** **"Stack = Scope (Local & Temporary), Heap = Objects (Dynamic & Shared)"**.

## 3. Characteristics / Properties
* **Stack Frame Lifecycle**: Pushed when a method is invoked; popped instantly when method returns. Zero GC overhead.
* **Heap Memory Regions (Generational GC)**:
  * **Young Generation**: Eden Space + Survivor Spaces ($S_0, S_1$). Where short-lived objects are instantiated.
  * **Old Generation (Tenured)**: Long-surviving objects promoted from Young Generation.
* **Object Memory Footprint in 64-bit JVM**:
  * Bare `java.lang.Object`: 16 bytes.
  * `java.lang.Integer`: 24 bytes ($16\text{B header} + 4\text{B int} + 4\text{B padding}$).
  * `int[100]` primitive array: $\approx 416$ bytes ($16\text{B header} + 4\text{B length} + 400\text{B data}$).

## 4. Internal Working
JVM Memory Architecture diagram:

```
+-------------------------------------------------------------------+
|                           JVM MEMORY                              |
+------------------------------------+------------------------------+
|            STACK MEMORY            |         HEAP MEMORY          |
|  (Thread Private, Fast LIFO)       |   (Shared across Threads)    |
|                                    |                              |
|  [main() Stack Frame]              |   [Eden / Young Gen]         |
|   - int x = 10                     |   - new int[]{10, 20, 30}    |
|   - Node ptr -------------------------> Node Object {val=5}       |
|                                    |                              |
|  [foo() Stack Frame]               |   [Tenured / Old Gen]        |
|   - double rate                    |   - Long-lived caches        |
+------------------------------------+------------------------------+
```

## 5. Visual Diagram
Stack Reference Pointing to Heap Object:

```
  STACK (Frame: solve())                     HEAP (Runtime Space)
+-------------------------+               +----------------------------+
| primitive val = 42      |               | int[] array (400 bytes)    |
|                         |               | [ 10 | 20 | 30 | ... ]     |
| refPtr -------------------------------->+----------------------------+
+-------------------------+               | Node head (24 bytes)       |
                                          | val: 5, next: null         |
                                          +----------------------------+
```

## 6. Operations / Algorithms
Analyzing Memory Allocation in Code:
1. Primitives declared inside methods $\to$ Allocated on **Stack** ($O(1)$ space).
2. `new` keyword $\to$ Allocates memory block on **Heap** ($O(\text{size})$ space).
3. Recursive function call $\to$ Pushes new **Stack Frame** ($O(\text{Depth})$ stack space).

> **Quick Syntax:**
```java
// Memory Allocation Breakdown:
public void process() {
    int x = 5;                        // 4 bytes allocated on Stack
    int[] arr = new int[1000];        // Reference (8B) on Stack -> Array (4016B) on Heap
    TreeNode node = new TreeNode(10); // Reference (8B) on Stack -> Object (24B) on Heap
}
```

## 7. Examples
* **Stack Memory Overflow**: Deep recursion without base case $\to$ `StackOverflowError`.
* **Heap Memory Exhaustion**: Allocating massive arrays inside infinite loops $\to$ `OutOfMemoryError: Java heap space`.
* **Garbage Collection Trigger**: Assigning `node.next = null` unlinks unreachable child nodes, making them eligible for GC sweep.

## 8. Java Code
Programmatic demonstration measuring JVM Heap Memory usage in Java:

```java
public class MemoryModelDemo {

    public static void printMemoryStats(String stage) {
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
        System.out.println("[" + stage + "] Used Heap Memory: " + usedMemory + " MB");
    }

    public static void main(String[] args) {
        printMemoryStats("Baseline");

        // Allocating 1 Million Integer Wrappers (Heavy Heap Footprint)
        Integer[] heapObjects = new Integer[1_000_000];
        for (int i = 0; i < heapObjects.length; i++) {
            heapObjects[i] = i; // Wrappers incur 24 bytes each + pointer
        }
        printMemoryStats("After 1M Integer Objects");

        // Releasing references for Garbage Collection
        heapObjects = null;
        System.gc(); // Suggests GC run
        printMemoryStats("After Nullifying & System.gc()");
    }
}
```

## 9. Complexity Analysis
| Allocation Type | Memory Location | Overhead per Element | Lifetime Bound |
| :--- | :--- | :--- | :--- |
| **Local Primitive `int`** | Stack | $0$ bytes overhead ($4$B raw) | Method scope exit |
| **Primitive Array `int[N]`**| Heap | $16$B header $+ 4$B length | Until unreachable by references |
| **Wrapper `Integer`** | Heap | $16$B header $+ 4$B padding | Until unreachable by references |
| **Recursion Frame** | Stack | $\approx 32-64$ bytes per frame | Recursive return |

## 10. Edge Cases
* **`java.lang.StackOverflowError`**: Occurs when recursive call depth exceeds thread stack capacity (typically $\approx 10,000$ calls depending on `-Xss`).
* **`java.lang.OutOfMemoryError`**: Occurs when Heap space is exhausted and GC cannot reclaim sufficient memory.
* **Memory Leaks in Static Collections**: Holding objects in `static` HashMaps prevents GC from reclaiming them since static references live indefinitely.

## 11. Common Mistakes
* Assuming local primitive variables inside recursive methods consume Heap space.
* Thinking `System.gc()` forces immediate garbage collection (it is only a non-binding *hint* to the JVM!).
* Creating temporary wrapper objects (`Double`, `Integer`) inside high-frequency loops instead of primitives.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** `System.gc()` does NOT guarantee immediate garbage collection! It merely signals to the JVM that garbage collection is desirable. Never rely on `System.gc()` for deterministic memory management in production or performance benchmarks.

> **Memory Trick:** **"Stack Overflow = Deep Recursion; Out of Memory = Huge Heap Allocation"**.

## 13. Comparisons
| Characteristic | Stack Memory | Heap Memory |
| :--- | :--- | :--- |
| **Access Speed** | Ultra-Fast (L1/L2 CPU Cache) | Slightly slower (Pointer indirection) |
| **Allocation Mechanism**| Automatic (Push / Pop) | Explicit (`new` operator / GC sweep) |
| **Scope Availability** | Thread Private | Shared across all Application Threads |
| **Flexibility** | Fixed Size (LIFO) | Dynamic Resizing |

## 14. How to Recognize This in Questions
* **"Explain memory footprint of your tree node structure"** $\rightarrow$ Calculate $16\text{B header} + \text{field sizes} + \text{padding}$.
* **"Optimizing memory in high-throughput data pipeline"** $\rightarrow$ Replace Object wrappers with primitive arrays to avoid GC pressure.

## 15. Frequently Asked Interview Questions
* **Q: Where are object instance variables stored in Java?**  
  *A:* Instance variables (fields of an object) are stored on the **Heap** inside the object's memory block, even if the fields are primitive types!
* **Q: What is compressed OOPs (Ordinary Object Pointers) in 64-bit JVM?**  
  *A:* Compressed OOPs enables 64-bit JVMs to encode object pointers as 32-bit offsets (if heap size is $<32\text{GB}$), reducing reference pointer memory footprint from 8 bytes to 4 bytes.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA MEMORY MODEL                                    |
+-----------------------------------------------------------------------+
| • Stack: Fast, LIFO, Method Scope, Local Primitives & Reference ptrs  |
| • Heap: Shared, Objects, Arrays, Instance Fields, Managed by GC        |
| • Integer Object Footprint = 24 Bytes (Header 16B + Val 4B + Pad 4B)   |
| • System.gc() is a non-binding request, NOT a guaranteed command      |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain the difference between Stack Memory and Heap Memory.
- [ ] I know the memory footprint breakdown of a Java object (Header + Fields + Padding).
- [ ] I understand why local variables live on the Stack while instance variables live on the Heap.
- [ ] I can distinguish between `StackOverflowError` and `OutOfMemoryError`.
- [ ] I know why `System.gc()` is non-binding.
