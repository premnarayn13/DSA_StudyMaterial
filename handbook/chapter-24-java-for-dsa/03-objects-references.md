# 03. Objects, References & Custom Classes in Java

## 1. Introduction
In Java, custom objects and reference variables form the core building blocks for pointer-based data structures such as Linked Lists, Binary Trees, N-ary Trees, and Graphs. In technical interviews, writing clean `ListNode`, `TreeNode`, or custom pair/comparator objects requires a strong understanding of object lifecycle, memory reference aliases, `equals()` and `hashCode()` contracts, and reference mutation semantics.

> **Important:** A reference variable in Java is NOT the object itself; it is a 64-bit (or 32-bit compressed) memory pointer pointing to an object residing on the Heap.

## 2. Core Concepts
* **Reference Variable**: Variable stored on the stack containing the memory address of an object on the heap.
* **Aliasing**: When two or more reference variables point to the exact same heap memory location (e.g., `Node a = b;`). Modifying state via `a` mutates the object visible through `b`.
* **Null Reference**: A reference pointing to memory address `0x0`. Dereferencing a `null` reference (`null.val`) throws a `NullPointerException`.
* **The `equals()` and `hashCode()` Contract**:
  1. If `a.equals(b)` is `true`, then `a.hashCode()` MUST equal `b.hashCode()`.
  2. If two objects have the same `hashCode()`, they are NOT required to be equal (Hash Collision).
  3. Overriding `equals()` REQUIRES overriding `hashCode()` (Mandatory for HashMap / HashSet keys!).

> **Memory Trick:** **"Same equals = Same hashCode; Same hashCode != Same equals"**.

## 3. Characteristics / Properties
* **Default Class Methods**: Every Java class inherits `toString()`, `equals()`, `hashCode()`, and `clone()` from `java.lang.Object`.
* **Default Object Comparisons**: `==` compares reference memory addresses. `.equals()` compares logical content equivalence.
* **Custom Inner Classes**:
  * `static class Node`: Independent nested class; cannot access outer instance fields (Preferred for DSA node definitions).
  * `class Node`: Non-static inner class; holds an implicit reference to the outer class instance (incurs extra 8-byte pointer overhead).

## 4. Internal Working
HashMap Bucket Lookup violating `equals()` / `hashCode()` contract:

```
[ Correct Contract Implementation ]
Key: Person("Alice", 25)  --> hashCode() = 8592 --> Bucket 4 --> equals() == true  --> [ FOUND ]

[ Broken Contract: Overrode equals() without hashCode() ]
Key Put:   Person("Alice", 25) --> Default System.identityHashCode() = 9912 --> Bucket 7
Key Get:   Person("Alice", 25) --> Default System.identityHashCode() = 1204 --> Bucket 2 --> [ NOT FOUND / NULL! ]
```

## 5. Visual Diagram
Reference Aliasing vs Object Mutation:

```
Stack Frame                         Heap Memory
+-----------------------+          +-----------------------------------+
| Node p1 = 0x800       | -------->| Node Object @ 0x800               |
|                       |          | val: 10                           |
| Node p2 = p1 (0x800)  | -------->| next: null                        |
+-----------------------+          +-----------------------------------+

Executing `p2.val = 50` updates the object at 0x800.
Now `p1.val` ALSO evaluates to 50 because both pointers reference 0x800!
```

## 6. Operations / Algorithms
Creating Custom Data Classes for Coding Interviews:
1. Declare static nested class for DSA nodes (`TreeNode`, `ListNode`, `Pair`).
2. Implement custom `Comparable<T>` interface for custom sorting in `PriorityQueue`.
3. Override `equals()` and `hashCode()` when using custom objects as `HashMap` keys or `HashSet` elements.

> **Quick Syntax:**
```java
// Standard Interview ListNode & TreeNode Definitions
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}
```

## 7. Examples
* **Custom Pair Class**: Storing `(row, col, distance)` tuples in BFS / Dijkstra graph algorithms.
* **Custom PriorityQueue Comparator**: Sorting custom `Job` objects by `priority` descending.
* **Dummy Head Node Trick**: Using `ListNode dummy = new ListNode(-1)` to eliminate edge-case pointer null checks when building or reversing linked lists.

## 8. Java Code
Complete interview-ready implementation of custom pair objects with `Comparable` and proper `equals()` / `hashCode()` overrides:

```java
import java.util.HashSet;
import java.util.PriorityQueue;
import java.util.Set;

public class CustomClassDemo {

    // Interview-ready Custom Pair Class implementing Comparable
    static class Point implements Comparable<Point> {
        int x, y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        // Min-Heap sorting based on x coordinate first, then y coordinate
        @Override
        public int compareTo(Point other) {
            if (this.x != other.x) {
                return Integer.compare(this.x, other.x);
            }
            return Integer.compare(this.y, other.y);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Point point = (Point) o;
            return this.x == point.x && this.y == point.y;
        }

        @Override
        public int hashCode() {
            return 31 * x + y; // Standard hash polynomial combination
        }
    }

    public static void main(String[] args) {
        // PriorityQueue using custom Comparable
        PriorityQueue<Point> pq = new PriorityQueue<>();
        pq.add(new Point(3, 5));
        pq.add(new Point(1, 9));
        pq.add(new Point(1, 2));

        System.out.println("Top of Min-Heap: (" + pq.peek().x + ", " + pq.peek().y + ")"); // (1, 2)

        // HashSet using custom equals() and hashCode()
        Set<Point> visited = new HashSet<>();
        visited.add(new Point(4, 4));
        System.out.println("Contains Point(4, 4)? " + visited.contains(new Point(4, 4))); // true
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity | Space Overhead | Key Note |
| :--- | :--- | :--- | :--- |
| **Object Instantiation (`new`)**| $O(1)$ | $16$B header $+ \text{fields}$ | Allocates heap memory block |
| **Reference Copy (`Node a = b`)**| $O(1)$ | $0$ heap allocation | Copies 64-bit pointer address on stack |
| **`equals()` Execution** | $O(1)$ | $O(1)$ | Compares field values |
| **`hashCode()` Execution** | $O(1)$ | $O(1)$ | Computes 32-bit integer hash code |

## 10. Edge Cases
* **Forgetting `static` on Inner Classes**: Non-static inner classes hold a hidden reference to the outer class instance, preventing outer class GC collection and causing subtle memory leaks.
* **Mutating Object Fields while inside HashSet**: Mutating fields of a key object ALREADY inserted in a `HashSet` changes its `hashCode()`, making it impossible to find or remove from the set!
* **Comparing Reference Equality instead of Value**: Using `p1 == p2` for custom node comparisons checks address identity, returning `false` for identical value objects.

## 11. Common Mistakes
* Overriding `equals()` but omitting `hashCode()` override (causes `HashSet.contains()` to return `false` for identical objects!).
* Modifying an object's state while it serves as a key inside a `HashMap` or `HashSet`.
* Creating custom `Comparator` returning `a.val - b.val` without checking for **integer overflow** when values can be negative (`Integer.MIN_VALUE`). Use `Integer.compare(a.val, b.val)` instead!

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never use `(a, b) -> a.val - b.val` for custom comparators if values can be negative! If `a.val = Integer.MIN_VALUE` and `b.val = 1`, subtraction `a.val - b.val` causes integer underflow, returning a POSITIVE number and reversing your sort order! Always use **`Integer.compare(a.val, b.val)`**.

> **Memory Trick:** **"Static Inner Node Classes save memory and prevent outer pointer references"**.

## 13. Comparisons
| Approach | `a.val - b.val` | `Integer.compare(a.val, b.val)` |
| :--- | :--- | :--- |
| **Underflow / Overflow Safe?**| **NO** (Fails on `MIN_VALUE` / `MAX_VALUE` subtraction) | **YES** (100% Safe across full integer range) |
| **Code Style** | Fragile | Standard Professional Java |
| **Interview Recommendation** | **AVOID** | **MANDATORY BEST PRACTICE** |

## 14. How to Recognize This in Questions
* **"Design a LRU / LFU Cache"** $\rightarrow$ Build custom `Node` class with `prev`, `next`, `key`, `val`.
* **"Top K Frequent Elements / Dijkstra Shortest Path"** $\rightarrow$ Build custom class with `Comparable<T>` for `PriorityQueue`.

## 15. Frequently Asked Interview Questions
* **Q: Why must nested node classes in trees/linked lists be declared `static`?**  
  *A:* Declaring nested classes as `static` prevents the JVM from attaching a synthetic outer class reference (`this$0`), saving 8 bytes of pointer memory per node and preventing memory leaks.
* **Q: What is the purpose of a dummy head node in LinkedList algorithms?**  
  *A:* A dummy head node eliminates special-case conditional logic when inserting into or deleting from the head of a linked list, simplifying code structure.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: OBJECTS, REFERENCES & CUSTOM CLASSES                  |
+-----------------------------------------------------------------------+
| • Reference = Pointer Address (64-bit on Stack) -> Object (on Heap)   |
| • Equals & HashCode Contract: Override BOTH or HashSet/Map breaks!     |
| • Comparator Trick: Use Integer.compare(a, b), NEVER (a - b)         |
| • Node Inner Classes: Always declare as `static class Node`           |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know how to write custom `equals()` and `hashCode()` methods.
- [ ] I know why `Integer.compare(a, b)` must be used instead of `a - b` in comparators.
- [ ] I understand the difference between `static` and non-static inner node classes.
- [ ] I know how to use dummy head nodes in LinkedList manipulation.
- [ ] I can implement `Comparable<T>` for custom `PriorityQueue` elements.
