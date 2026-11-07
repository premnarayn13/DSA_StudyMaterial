# 05. Java Collections Framework Overview for DSA

## 1. Introduction
The Java Collections Framework (JCF) provides standard data structure implementations optimized for production and technical interviews. Choosing the correct collection (`ArrayList`, `LinkedList`, `ArrayDeque`, `HashMap`, `TreeMap`, `HashSet`, `TreeSet`, `PriorityQueue`) based on query bounds is a primary evaluation metric in DSA interviews.

> **Important:** Master the complexity trade-offs between array-backed collections (`ArrayList`, `ArrayDeque`), hash-backed collections (`HashMap`, `HashSet`), and tree-backed collections (`TreeMap`, `TreeSet`, `PriorityQueue`).

## 2. Core Concepts
* **List Interface**: Ordered collection maintaining insertion order (`ArrayList`, `LinkedList`).
* **Set Interface**: Collection containing NO duplicate elements (`HashSet`, `LinkedHashSet`, `TreeSet`).
* **Queue / Deque Interface**: Double-ended collection for FIFO / LIFO operations (`ArrayDeque`, `LinkedList`).
* **Map Interface**: Key-value pair mapping (`HashMap`, `LinkedHashMap`, `TreeMap`).
* **PriorityQueue**: Binary Min-Heap / Max-Heap structure for $O(1)$ top element access.

> **Memory Trick:** **"Use ArrayDeque over Stack and LinkedList for Stacks/Queues!"** Java's legacy `java.util.Stack` class is synchronized and slow; `LinkedList` incurs pointer overhead. `ArrayDeque` is faster and cache-friendly.

## 3. Characteristics / Properties
* **Hierarchy Map**:

```
                  Collection Interface
                           |
       +-------------------+-------------------+
       |                   |                   |
 List Interface      Set Interface      Queue / Deque Interface
   - ArrayList         - HashSet          - ArrayDeque
   - LinkedList        - LinkedHashSet    - PriorityQueue
                       - TreeSet          - LinkedList
```

* **Map Hierarchy (Standalone Interface)**:
  * `HashMap`: $O(1)$ avg time, unsorted keys.
  * `LinkedHashMap`: $O(1)$ avg time, preserves insertion order (Ideal for LRU Cache!).
  * `TreeMap`: $O(\log N)$ time, keys sorted via Red-Black Tree.

## 4. Internal Working
Collection Underlying Data Structure Map:

```
Collection Type      Underlying Implementation              Key Property
-----------------------------------------------------------------------------------
ArrayList            Dynamic Resizing Array (1.5x)          O(1) Random Access
LinkedList           Doubly Linked List                     O(1) Head/Tail Insert
ArrayDeque           Circular Resizing Array                O(1) Stack & Queue ops
HashMap              Hash Table (Array + List/RB Tree)      O(1) Avg Key Lookup
TreeMap              Red-Black Self-Balancing BST           O(log N) Sorted Keys
HashSet              Backed internally by a HashMap         O(1) Unique Elements
TreeSet              Backed internally by a TreeMap         O(log N) Sorted Unique
PriorityQueue        Binary Heap (Array-backed)             O(log N) Insert/Poll
```

## 5. Visual Diagram
ArrayDeque Circular Buffer Execution:

```
 ArrayDeque (Backing Array):
+------+------+------+------+------+------+------+------+
|  30  |  40  | null | null | null | null |  10  |  20  |
+------+------+------+------+------+------+------+------+
                 ^                    ^
               Tail                 Head

PushFirst(5)  -> Decrements Head pointer counter (wraps circularly).
PushLast(50)  -> Increments Tail pointer counter.
```

## 6. Operations / Algorithms
Essential Java Collection Instantiations:
1. **Min-Heap (Default)**: `PriorityQueue<Integer> minHeap = new PriorityQueue<>();`
2. **Max-Heap**: `PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));`
3. **Double-Ended Queue / Stack**: `Deque<Integer> stack = new ArrayDeque<>();`
4. **Sorted Map with Custom Comparator**: `TreeMap<Integer, Integer> map = new TreeMap<>(Collections.reverseOrder());`

> **Quick Syntax:**
```java
// PriorityQueue Max-Heap Syntax Reminders
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));

// ArrayDeque as Stack (LIFO) Idiom
Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);  // Adds to head
int val = stack.pop(); // Removes from head
```

## 7. Examples
* **Stack Operations**: Use `Deque<Integer> stack = new ArrayDeque<>();` (`push()`, `pop()`, `peek()`).
* **Queue Operations**: Use `Queue<Integer> queue = new ArrayDeque<>();` (`offer()`, `poll()`, `peek()`).
* **Top K Elements**: Use `PriorityQueue<Integer> minHeap` of size $K$.

## 8. Java Code
Interview-ready code demonstrating JCF collection selection across common DSA problems:

```java
import java.util.*;

public class CollectionsOverviewDemo {

    public static void demonstrateCollections() {
        // 1. ArrayDeque as Stack (LIFO)
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(10);
        stack.push(20);
        System.out.println("Stack Pop: " + stack.pop()); // 20

        // 2. PriorityQueue as Max-Heap
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
        maxHeap.offer(5);
        maxHeap.offer(50);
        maxHeap.offer(25);
        System.out.println("Max-Heap Top: " + maxHeap.poll()); // 50

        // 3. TreeMap for Range Queries & Sorted Keys
        TreeMap<Integer, String> treeMap = new TreeMap<>();
        treeMap.put(100, "Score A");
        treeMap.put(50, "Score B");
        treeMap.put(200, "Score C");
        System.out.println("Floor Key for 150: " + treeMap.floorKey(150)); // 100
        System.out.println("Ceiling Key for 150: " + treeMap.ceilingKey(150)); // 200
    }

    public static void main(String[] args) {
        demonstrateCollections();
    }
}
```

## 9. Complexity Analysis
| Collection | Access | Search | Insertion | Deletion | Space |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ArrayList** | $O(1)$ | $O(N)$ | $O(1)$ amortized end | $O(N)$ middle | $O(N)$ |
| **LinkedList** | $O(N)$ | $O(N)$ | $O(1)$ head/tail | $O(1)$ head/tail | $O(N)$ |
| **ArrayDeque** | $O(1)$ head/tail | $O(N)$ | $O(1)$ head/tail | $O(1)$ head/tail | $O(N)$ |
| **HashMap** | N/A | $O(1)$ avg | $O(1)$ avg | $O(1)$ avg | $O(N)$ |
| **TreeMap** | N/A | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(N)$ |
| **PriorityQueue**| $O(1)$ top | $O(N)$ contains | $O(\log N)$ offer | $O(\log N)$ poll | $O(N)$ |

## 10. Edge Cases
* **`java.util.Stack` Deprecation**: Never use `Stack` class in interviews! It extends `Vector` and synchronizes all methods, making it slow and obsolete. Use `ArrayDeque`.
* **ArrayDeque Null Restriction**: `ArrayDeque` does NOT allow `null` elements (`NullPointerException` thrown on `add(null)`).
* **`PriorityQueue.remove(Object)` is $O(N)$**: Deleting an arbitrary non-top element from a PriorityQueue requires linear scan $O(N)$ time!

## 11. Common Mistakes
* Using `LinkedList` as a Queue or Stack when `ArrayDeque` is faster and uses less memory.
* Assuming `PriorityQueue.contains()` or `remove()` takes $O(\log N)$ time (they take $O(N)$ time!).
* Using `(a, b) -> a - b` instead of `Integer.compare(a, b)` for PriorityQueue comparators.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Always use `ArrayDeque` instead of `Stack` or `LinkedList` for Stacks and Queues! `ArrayDeque` is backed by a circular array, providing better CPU cache locality, zero pointer allocation overhead, and faster speed.

> **Memory Trick:** **"TreeMap & TreeSet = Red-Black Tree = O(log N); HashMap & HashSet = Hash Table = O(1)"**.

## 13. Comparisons
| Requirement | Recommended Collection | Key Advantage |
| :--- | :--- | :--- |
| **LIFO Stack** | `ArrayDeque<T>` | Fast, no synchronization overhead |
| **FIFO Queue** | `ArrayDeque<T>` | Fast circular array buffer |
| **Top K / Min / Max** | `PriorityQueue<T>` | $O(1)$ peek, $O(\log N)$ poll |
| **Range Queries / Floor / Ceiling**| `TreeMap<K, V>` / `TreeSet<T>` | $O(\log N)$ self-balancing tree operations |
| **LRU Cache Base** | `LinkedHashMap<K, V>` | Maintains key insertion / access order |

## 14. How to Recognize This in Questions
* **"Find Floor / Ceiling / Nearest Element"** $\rightarrow$ Use `TreeSet` (`floor()`, `ceiling()`).
* **"Maintain dynamic median of stream"** $\rightarrow$ Dual PriorityQueue (Min-Heap + Max-Heap).

## 15. Frequently Asked Interview Questions
* **Q: Why does `ArrayDeque` prohibit `null` elements?**  
  *A:* `ArrayDeque` methods like `poll()` return `null` to signal that the queue is empty. Permitting `null` elements would introduce ambiguity.
* **Q: What is the time complexity of `TreeMap.floorKey(k)`?**  
  *A:* $O(\log N)$ time because `TreeMap` is implemented using a self-balancing Red-Black Binary Search Tree.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA COLLECTIONS FRAMEWORK OVERVIEW                  |
+-----------------------------------------------------------------------+
| • Stack & Queue: Use ArrayDeque (Faster & cache-friendly)             |
| • Max-Heap: PriorityQueue<Integer>((a,b) -> Integer.compare(b, a))    |
| • PriorityQueue.remove(x) is O(N) linear search, NOT O(log N)!        |
| • TreeMap / TreeSet: O(log N) operations with floorKey / ceilingKey   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I know why `ArrayDeque` is preferred over `Stack` and `LinkedList`.
- [ ] I can write the syntax for Min-Heap and Max-Heap `PriorityQueue`.
- [ ] I understand the $O(\log N)$ bounds for `TreeMap` and `TreeSet`.
- [ ] I know how `TreeMap.floorKey()` and `ceilingKey()` work.
- [ ] I know that `PriorityQueue.remove(obj)` takes $O(N)$ time.
