# 04. Java Generics in Data Structures

## 1. Introduction
Java Generics provide compile-time type safety, allowing classes and algorithms to operate on specified data types without raw type casting. In technical coding interviews, generics enable constructing reusable, type-safe data structures like generic `Pair<K, V>`, `Node<T>`, `Stack<T>`, and custom Graph structures.

> **Important:** Java Generics operate via **Type Erasure** at compile time. The JVM converts generic type parameters (`<T>`) to `Object` (or bounded types), meaning generic type information is erased at runtime!

## 2. Core Concepts
* **Type Erasure**: Compiler feature where generic types (`List<String>`) are replaced with raw types (`List`) or bounds (`Object`) during compilation. Bytecode contains zero generic type parameters.
* **Primitive Restriction**: Generic type parameters MUST be Reference/Object types (`List<Integer>`), NOT primitives (`List<int>` is invalid Java syntax!).
* **Wildcards (`?`)**:
  * `? extends T` (Upper Bounded): Accepts `T` or any subclass of `T` (Read-only / Producer `Extends`).
  * `? super T` (Lower Bounded): Accepts `T` or any superclass of `T` (Write-only / Consumer `Super`).
* **PECS Principle**: **Producer `Extends`, Consumer `Super`**.

> **Memory Trick:** **"PECS: Producer Extends, Consumer Super"**. Use `? extends T` when reading items FROM a collection; use `? super T` when writing items INTO a collection.

## 3. Characteristics / Properties
* **Cannot Instantiate Generic Arrays**: `new T[10]` is **illegal** in Java due to type erasure! You must allocate an `Object[]` array and cast: `(T[]) new Object[capacity]`.
* **Cannot Instantiate Generic Types directly**: `new T()` is illegal without Reflection.
* **Static Generic Methods**: Static methods cannot access class-level generic types; they must declare their own generic parameters: `public static <T> void swap(T[] arr, int i, int j)`.

## 4. Internal Working
Type Erasure Transformation during Java Compilation:

```
[ Developer Java Code ]
public class Stack<T> {
    private T[] data;
    public void push(T item) { ... }
    public T pop() { ... }
}

[ Compiled Bytecode (Type Erasure applied) ]
public class Stack {
    private Object[] data;
    public void push(Object item) { ... }
    public Object pop() { ... }
}
```

## 5. Visual Diagram
PECS Wildcard Data Flow:

```
Producer Extends (? extends Number):
[ Source Collection ] ---> READ items out as Number ---> (Consumer Code)
  (You CANNOT add elements into a ? extends Collection!)

Consumer Super (? super Integer):
(Producer Code) ---> WRITE Integers into ---> [ Target Collection ]
  (You CANNOT safely read specific types out of a ? super Collection!)
```

## 6. Operations / Algorithms
Creating Generic Classes & Methods in Java:
1. Declare generic class: `public class MyContainer<T>`.
2. Allocate backing storage: `this.storage = (T[]) new Object[capacity];`.
3. Use `@SuppressWarnings("unchecked")` to handle compiler cast warnings cleanly.

> **Quick Syntax:**
```java
// Generic Pair Class Idiom for DSA
class Pair<K, V> {
    public final K key;
    public final V val;
    public Pair(K key, V val) {
        this.key = key;
        this.val = val;
    }
}
```

## 7. Examples
* **Generic Min-Heap PriorityQueue**: `PriorityQueue<T>` where `T extends Comparable<T>`.
* **Generic Tuple / Triple Class**: Storing `Pair<Integer, String>` in graph algorithms.
* **Generic Array Swap Helper**: `public static <T> void swap(T[] arr, int i, int j)`.

## 8. Java Code
Complete interview-ready generic Stack implementation handling type erasure and array allocation:

```java
import java.util.EmptyStackException;

public class GenericStackDemo {

    // Interview-ready Generic Stack Implementation
    static class CustomStack<T> {
        private Object[] data;
        private int size;
        private static final int DEFAULT_CAPACITY = 10;

        @SuppressWarnings("unchecked")
        public CustomStack() {
            this.data = new Object[DEFAULT_CAPACITY];
            this.size = 0;
        }

        public void push(T element) {
            if (size == data.length) {
                resize();
            }
            data[size++] = element;
        }

        @SuppressWarnings("unchecked")
        public T pop() {
            if (isEmpty()) {
                throw new EmptyStackException();
            }
            T item = (T) data[--size]; // Cast Object back to generic T
            data[size] = null; // Prevent memory leak / loitering
            return item;
        }

        @SuppressWarnings("unchecked")
        public T peek() {
            if (isEmpty()) throw new EmptyStackException();
            return (T) data[size - 1];
        }

        public boolean isEmpty() {
            return size == 0;
        }

        private void resize() {
            Object[] newArr = new Object[data.length * 2];
            System.arraycopy(data, 0, newArr, 0, size);
            data = newArr;
        }
    }

    public static void main(String[] args) {
        CustomStack<String> stringStack = new CustomStack<>();
        stringStack.push("Alpha");
        stringStack.push("Beta");
        System.out.println("Popped: " + stringStack.pop()); // Beta

        CustomStack<Integer> intStack = new CustomStack<>();
        intStack.push(100);
        intStack.push(200);
        System.out.println("Peek: " + intStack.peek()); // 200
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Generic Casting `(T) obj`** | $O(1)$ | $O(1)$ | Zero runtime overhead (Compile-time check) |
| **Generic Method Invocation** | $O(1)$ | $O(1)$ | Same bytecode execution speed |
| **Generic Array Allocation** | $O(1)$ | $O(N)$ heap space | Requires `(T[]) new Object[N]` cast |

## 10. Edge Cases
* **`new T[size]` Compile Error**: Attempting to allocate generic arrays directly causes a compilation error `Cannot create a generic array of T`.
* **Loitering / Memory Leak**: Forgetting to set `data[size] = null` when popping elements from a custom array-backed stack retains unreachable heap object references, preventing Garbage Collection.

## 11. Common Mistakes
* Attempting to use primitive types as generic arguments (`List<int>` instead of `List<Integer>`).
* Expecting generic type information to be accessible at runtime (e.g., `if (obj instanceof T)` is **illegal** due to type erasure!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Remember **PECS**: **Producer Extends, Consumer Super**. If your method accepts a collection that produces data to be read, use `<? extends T>`. If your method accepts a collection that consumes data to be written, use `<? super T>`.

> **Memory Trick:** **"Type Erasure turns <T> into Object"**. Generics exist purely for the Java compiler; at the bytecode level, everything is raw `Object` references and casts.

## 13. Comparisons
| Feature | Primitive Collection Strategy (`int[]`) | Generic Collection (`List<Integer>`) |
| :--- | :--- | :--- |
| **Type Safety** | Checked at compile time | Checked at compile time |
| **Genericity** | Fixed type only | Operates on any Object type |
| **Memory Efficiency** | $O(1)$ zero wrapper overhead | 16-24 bytes wrapper overhead per item |
| **Runtime Performance**| Fast (Direct CPU cache) | Slight unboxing overhead |

## 14. How to Recognize This in Questions
* **"Design a generic Data Structure (Stack/Queue/LRU)"** $\rightarrow$ Implement generic `<T>` type parameters and handle array allocation via `(T[]) new Object[N]`.

## 15. Frequently Asked Interview Questions
* **Q: Why does Java prohibit primitive type parameters in Generics (e.g., `ArrayList<int>`)?**  
  *A:* Because Java Generics rely on Type Erasure, replacing `<T>` with `Object`. Primitive types do not inherit from `java.lang.Object`, so they cannot be erased to `Object`.
* **Q: What is Memory Loitering in custom stack implementations?**  
  *A:* Memory loitering occurs when an array-backed data structure retains references to popped/deleted elements (e.g., failing to set `data[top] = null`), preventing the JVM Garbage Collector from freeing the memory.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA GENERICS                                         |
+-----------------------------------------------------------------------+
| • Type Erasure: Generics erased to Object at compile time             |
| • PECS Rule: Producer Extends, Consumer Super                         |
| • Array Allocation Fix: (T[]) new Object[capacity]                    |
| • Memory Loitering: Always set popped array indices to null          |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain Java Type Erasure and its impact on bytecode.
- [ ] I know the PECS rule (`? extends T` vs `? super T`).
- [ ] I can write the legal syntax for allocating generic arrays in Java.
- [ ] I understand why primitives cannot be used as generic type arguments.
- [ ] I know how to prevent memory loitering in custom collection classes.
