# 06. Java HashSet, LinkedHashMap & Access-Order Cache Architecture

## 1. Introduction
Java's **`java.util.HashSet`** and **`java.util.LinkedHashMap`** are primary collections built directly on top of Java's `HashMap` engine. In technical coding interviews and enterprise Java systems design, understanding how `HashSet` delegates all operations to an internal backing `HashMap` (using a dummy `PRESENT` sentinel value), and how `LinkedHashMap` extends `HashMap.Node` with doubly linked pointers (`before` and `after`) to enable **Predictable Insertion-Order Iteration** and **Access-Order LRU Cache Eviction** (`removeEldestEntry()`), is an essential core competency.

> **Important:** `LinkedHashMap` combines the **$O(1)$ lookup performance of a Hash Table** with the **$O(1)$ sequential ordering of a Doubly Linked List**. Setting `accessOrder = true` transforms `LinkedHashMap` into an automatic **Least Recently Used (LRU) Cache**!

```
Java Collection Delegation Architecture:
+-----------------------------------------------------------------------------------+
| HashSet          : Wraps HashMap<E, Object> using dummy static final PRESENT value|
| LinkedHashMap    : Extends HashMap with Node.before and Node.after doubly pointers|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & JDK Class Architecture

### 2.1 How `HashSet<E>` Backing Works
`java.util.HashSet` does NOT implement a unique set data structure from scratch. Instead, it maintains a private backing `HashMap<E, Object>` instance:

```java
public class HashSet<E> AbstractSet<E> implements Set<E>, Cloneable, java.io.Serializable {
    private transient HashMap<E,Object> map;
    private static final Object PRESENT = new Object(); // Dummy value sentinel

    public HashSet() {
        map = new HashMap<>();
    }

    public boolean add(E e) {
        return map.put(e, PRESENT) == null; // Returns true if key was new
    }

    public boolean contains(Object o) {
        return map.containsKey(o); // Delegates to HashMap.containsKey()
    }

    public boolean remove(Object o) {
        return map.remove(o) == PRESENT; // Returns true if removed
    }
}
```

### 2.2 How `LinkedHashMap<K,V>` Extends `HashMap`
`LinkedHashMap` inherits all hashing, bucket indexing, and collision resolution logic from `HashMap`. However, it overrides `newNode()` to instantiate `Entry<K,V>` objects containing two additional pointer fields: `before` and `after`:

```java
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after; // Doubly linked pointers for global iteration order
    Entry(int hash, K key, V value, Node<K,V> next) {
        super(hash, key, value, next);
    }
}
```

### 2.3 Insertion-Order vs Access-Order Modes
* **Insertion Order (`accessOrder = false`, Default)**: Iterating over `LinkedHashMap` returns elements in the exact order they were inserted.
* **Access Order (`accessOrder = true`)**: Accessing an entry via `get(key)` or `put(key, val)` automatically moves that entry to the **tail of the doubly linked list** (marking it as Most Recently Used). The head of the list (`head`) is ALWAYS the **Least Recently Used (LRU) Entry**!

> **Memory Trick:** **"HashSet is a HashMap with dummy PRESENT values! LinkedHashMap adds before/after pointers to HashMap Nodes for O(1) LRU ordering!"**

---

## 3. Characteristics & LRU Cache Mechanics (`removeEldestEntry`)

### 3.1 `LinkedHashMap` Dual Pointer Mesh
Each node in a `LinkedHashMap` belongs to TWO independent structural graphs simultaneously:
1. **Hash Table Bucket Chain**: Uses `Node.next` (and Red-Black tree pointers) to resolve collisions within a bucket slot.
2. **Global Doubly Linked List**: Uses `Entry.before` and `Entry.after` to link ALL map entries globally across all buckets.

```
LinkedHashMap Dual Data Structure Graph:
+-----------------------------------------------------------------------------------+
| Hash Bucket Grid (next pointers)   : Slot 1 -> [Node A] -> [Node B]              |
| Global LRU List (before/after)    : [Head: Node B] <===> [Node A] <===> [Tail]   |
+-----------------------------------------------------------------------------------+
```

### 3.2 Overriding `removeEldestEntry()` for Automatic Eviction
By overriding `protected boolean removeEldestEntry(Map.Entry<K,V> eldest)` in a subclass of `LinkedHashMap`, developers can create a production-grade LRU Cache in **under 10 lines of code**:

```java
public class SimpleLRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int maxCapacity;

    public SimpleLRUCache(int maxCapacity) {
        super(maxCapacity, 0.75f, true); // accessOrder = true for LRU!
        this.maxCapacity = maxCapacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > maxCapacity; // Evicts LRU head entry when capacity exceeded!
    }
}
```

---

## 4. Internal Working Mechanics
Tracing `LinkedHashMap.get(key)` with `accessOrder = true`:

```
INITIAL LRU LIST: [Head: Key 1] <===> [Key 2] <===> [Key 3: Tail] (Capacity = 3)
Call: map.get(1)

Step 1: Hash bucket lookup locates Node for Key 1 in O(1) time.
Step 2: Retrieve Value for Key 1.
Step 3: Trigger recordAccess() callback:
        - Unlink Key 1 from Head: Set head = Key 2.
        - Relink Key 1 to Tail: Set Key 3.after = Key 1, Key 1.before = Key 3, Key 1.after = null.
        - Set tail = Key 1.

UPDATED LRU LIST: [Head: Key 2] <===> [Key 3] <===> [Key 1: Tail] (Key 1 moved to Tail!) ✅
```

---

## 5. Visual Diagram
`LinkedHashMap` Memory Topology showing Bucket Chains overlaid with Global Iteration Pointers:

```
                  Global Head (LRU - Eldest)
                             |
                             v
                 +-----------------------+
                 | Entry Key: "A" (Val:1)| <---+
                 +-----------------------+     |
                 | hash, key, val, next  |     | (before / after)
                 | before: null          |     |
                 | after: ----+          |     |
                 +------------|----------+     |
                              |                |
                              v                |
                 +-----------------------+     |
                 | Entry Key: "B" (Val:2)| <---+
                 +-----------------------+
                 | hash, key, val, next  |
                 | before: ----+         |
                 | after: null           |
                 +-----------------------+
                             ^
                             |
                  Global Tail (MRU - Newest)
```

---

## 6. Operations & Complete Java Implementation
Production-grade implementation of custom `HashSet` and custom `LinkedHashMap` with LRU access-ordering:

```java
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Objects;

// 1. Custom HashSet Delegation Implementation
public class CustomHashSet<E> implements Iterable<E> {
    private final CustomJDKHashMap<E, Object> map;
    private static final Object PRESENT = new Object();

    public CustomHashSet() {
        this.map = new CustomJDKHashMap<>();
    }

    public boolean add(E element) {
        return map.put(element, PRESENT) == null;
    }

    public boolean contains(E element) {
        return map.get(element) != null;
    }

    public int size() {
        return map.size();
    }

    @Override
    public Iterator<E> iterator() {
        throw new UnsupportedOperationException("Key iteration via HashMap");
    }
}
```

```java
// 2. Custom Production-Grade LinkedHashMap with Access-Order LRU Eviction
public class CustomLinkedHashMap<K, V> {

    static class Entry<K, V> {
        final int hash;
        final K key;
        V value;
        Entry<K, V> next;   // Hash bucket chain pointer
        Entry<K, V> before; // Global doubly list prev
        Entry<K, V> after;  // Global doubly list next

        Entry(int hash, K key, V value, Entry<K, V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    private Entry<K, V>[] table;
    private int size;
    private int capacity;
    private final boolean accessOrder;
    private final int maxCapacity;

    private Entry<K, V> head; // Eldest entry (LRU target)
    private Entry<K, V> tail; // Newest entry (MRU target)

    @SuppressWarnings("unchecked")
    public CustomLinkedHashMap(int capacity, boolean accessOrder, int maxCapacity) {
        this.capacity = capacity;
        this.table = (Entry<K, V>[]) new Entry[capacity];
        this.accessOrder = accessOrder;
        this.maxCapacity = maxCapacity;
        this.size = 0;
    }

    static final int spreadHash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }

    public V get(K key) {
        int h = spreadHash(key);
        int idx = h & (capacity - 1);
        Entry<K, V> e = table[idx];

        while (e != null) {
            if (e.hash == h && Objects.equals(e.key, key)) {
                if (accessOrder) {
                    afterNodeAccess(e); // Move accessed entry to tail!
                }
                return e.value;
            }
            e = e.next;
        }
        return null;
    }

    public void put(K key, V value) {
        int h = spreadHash(key);
        int idx = h & (capacity - 1);
        Entry<K, V> first = table[idx];

        Entry<K, V> e = first;
        while (e != null) {
            if (e.hash == h && Objects.equals(e.key, key)) {
                e.value = value;
                if (accessOrder) {
                    afterNodeAccess(e);
                }
                return;
            }
            e = e.next;
        }

        // Insert new Entry
        Entry<K, V> newEntry = new Entry<>(h, key, value, first);
        table[idx] = newEntry;
        linkNodeAtEnd(newEntry);
        size++;

        // Automatic LRU Eviction check
        if (size > maxCapacity) {
            removeEldestEntry();
        }
    }

    private void linkNodeAtEnd(Entry<K, V> p) {
        Entry<K, V> last = tail;
        tail = p;
        if (last == null) {
            head = p;
        } else {
            p.before = last;
            last.after = p;
        }
    }

    private void afterNodeAccess(Entry<K, V> e) {
        Entry<K, V> last = tail;
        if (accessOrder && last != e) {
            Entry<K, V> p = e, b = p.before, a = p.after;
            p.after = null;
            if (b == null) head = a;
            else b.after = a;

            if (a != null) a.before = b;
            else last = b;

            if (last == null) head = p;
            else { p.before = last; last.after = p; }
            tail = p;
        }
    }

    private void removeEldestEntry() {
        Entry<K, V> eldest = head;
        if (eldest != null) {
            remove(eldest.key);
        }
    }

    public void remove(K key) {
        int h = spreadHash(key);
        int idx = h & (capacity - 1);
        Entry<K, V> prev = null;
        Entry<K, V> curr = table[idx];

        while (curr != null) {
            if (curr.hash == h && Objects.equals(curr.key, key)) {
                if (prev == null) table[idx] = curr.next;
                else prev.next = curr.next;

                // Unlink from global doubly list
                unlinkNode(curr);
                size--;
                return;
            }
            prev = curr;
            curr = curr.next;
        }
    }

    private void unlinkNode(Entry<K, V> e) {
        Entry<K, V> b = e.before, a = e.after;
        if (b == null) head = a;
        else b.after = a;

        if (a == null) tail = b;
        else a.before = b;
    }

    public void printLRUOrder() {
        System.out.print("LRU Order (Head -> Tail): ");
        Entry<K, V> curr = head;
        while (curr != null) {
            System.out.print("[" + curr.key + ":" + curr.value + "] ");
            curr = curr.after;
        }
        System.out.println();
    }

    public int size() { return size; }
}
```

> **Quick Syntax:**
```java
// LRU Eviction Subclass Pattern
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    public LRUCache(int cap) { super(cap, 0.75f, true); }
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > cap;
    }
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 146 - LRU Cache**: Overriding `LinkedHashMap.removeEldestEntry()` or custom Map + DLL implementation.
* **LeetCode 380 - Insert Delete GetRandom O(1)**: Combining a Hash Map for index lookups with an ArrayList for $O(1)$ random access.
* **LeetCode 350 - Intersection of Two Arrays II**: Utilizing `HashSet` / `HashMap` for element counting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `HashSet` duplicate rejection and `LinkedHashMap` access-order LRU eviction:

```java
public class HashSetLinkedHashMapDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing HashSet Backing Mechanism ===");
        CustomHashSet<String> set = new CustomHashSet<>();
        System.out.println("Add 'Apple':  " + set.add("Apple")); // true
        System.out.println("Add 'Banana': " + set.add("Banana")); // true
        System.out.println("Add 'Apple' Duplicate: " + set.add("Apple")); // false!
        System.out.println("Contains 'Banana': " + set.contains("Banana")); // true

        System.out.println("\n=== 2. Testing LinkedHashMap LRU Access-Order Eviction ===");
        CustomLinkedHashMap<Integer, String> lruCache = 
            new CustomLinkedHashMap<>(4, true, 3); // Max Capacity = 3

        lruCache.put(1, "One");
        lruCache.put(2, "Two");
        lruCache.put(3, "Three");
        lruCache.printLRUOrder(); // Expected: [1:One] [2:Two] [3:Three]

        System.out.println("\nAccessing Key 1 (Moves Key 1 to Tail):");
        lruCache.get(1);
        lruCache.printLRUOrder(); // Expected: [2:Two] [3:Three] [1:One]

        System.out.println("\nInserting Key 4 (Triggers Eviction of Eldest Head Key 2):");
        lruCache.put(4, "Four");
        lruCache.printLRUOrder(); // Expected: [3:Three] [1:One] [4:Four]
    }
}
```

---

## 9. Complexity Analysis

| Collection | `get` / `contains` Time | `add` / `put` Time | `remove` Time | Iteration Order Guarantee | Memory Overhead |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`HashSet<E>`** | **Average $O(1)$** | **Amortized $O(1)$**| **Average $O(1)$**| Unordered | 32B Node + Dummy Val |
| **`LinkedHashMap`**| **Average $O(1)$** | **Amortized $O(1)$**| **Average $O(1)$**| **Insertion or Access Order ⚡**| 40B Node (Extra Pointers)|
| **`TreeSet<E>`** | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | Sorted Key Order | Red-Black Tree Nodes |

---

## 10. Edge Cases & Boundary Handling
* **`HashSet` Dummy Value Overhead**: Every `HashSet.add()` passes the static final `PRESENT` object. Because `PRESENT` is static, only ONE dummy object exists in memory across all `HashSet` instances!
* **Concurrent Modification during LRU Access**: Calling `LinkedHashMap.get()` with `accessOrder = true` mutates the internal doubly linked list! Therefore, calling `get()` while iterating over a `LinkedHashMap` throws `ConcurrentModificationException`.

---

## 11. Common Mistakes & Anti-Patterns
* **Assuming `HashSet` Maintains Insertion Order**: Standard `HashSet` iteration order is completely non-deterministic! Use **`LinkedHashSet`** if insertion-order iteration is required.
* **Forgetting `accessOrder = true` in LRU Cache**: Passing `super(capacity, 0.75f, false)` creates an Insertion-Order cache, NOT an Access-Order LRU cache! Accessing entries will fail to refresh their LRU status.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Three Key Java Map Iteration Guarantees:
> 1. **`HashMap`**: **NO Guarantee** (Unordered, order changes on resize).
> 2. **`LinkedHashMap`**: **Strict Guarantee** (Insertion Order OR Access Order).
> 3. **`TreeMap`**: **Sorted Key Guarantee** (Natural `Comparable` order or custom `Comparator`).

> **Memory Trick:** **"HashSet = Dummy Map! LinkedHashSet = Insertion Order Set! LinkedHashMap(cap, 0.75f, true) = LRU Cache!"**

---

## 13. System & Implementation Comparisons

| Metric | `HashMap` | `LinkedHashMap` (Insertion) | `LinkedHashMap` (Access LRU) |
| :--- | :--- | :--- | :--- |
| **Pointers per Node** | `next` (1 Pointer) | `next`, `before`, `after` (3) | `next`, `before`, `after` (3) |
| **`get()` Side-Effects** | Zero Read Mutation | Zero Read Mutation | **Mutates Doubly Linked List!** |
| **Iteration Order** | Random Bucket Order | Chronological Insertion Order | Least Recently Used $\to$ Most Recently Used |

---

## 14. How to Recognize This in Questions
* **"Design an LRU Cache with O(1) ops using standard Java collections"** $\rightarrow$ Extend `LinkedHashMap` with `accessOrder = true` and `removeEldestEntry()`.
* **"Remove duplicates while preserving original order"** $\rightarrow$ `LinkedHashSet`.

---

## 15. Frequently Asked Interview Questions
* **Q: How does `HashSet` check if an element already exists?**  
  *A:* `HashSet.add(e)` calls internal `map.put(e, PRESENT)`. `HashMap.put()` computes `hash(e)` and index, checks bucket chain equality via `e.hashCode()` and `e.equals()`. If key exists, `put()` returns `PRESENT` (causing `add()` to return `false`).
* **Q: Why does `LinkedHashMap.get()` throw `ConcurrentModificationException` when `accessOrder = true`?**  
  *A:* Because `get()` calls `afterNodeAccess()`, which unlinks and moves the node to the tail of the doubly linked list, modifying `modCount` (structural modification).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASHSET, LINKEDHASHMAP & ACCESS-ORDER LRU             |
+-----------------------------------------------------------------------+
| • HashSet Mechanics: Backed by HashMap<E, Object> with dummy PRESENT  |
| • LinkedHashMap Node: Extends Node with Node.before and Node.after    |
| • Dual Structure: Hash Bucket Chain (next) + Global Doubly List (b/a) |
| • LRU Cache Setup: super(capacity, 0.75f, true) [accessOrder = true]  |
| • LRU Eviction: Override removeEldestEntry() -> return size() > cap   |
| • LinkedHashMap get() Side Effect: Mutates doubly list! (modCount++)  |
| • Order Comparison: HashMap (Random), LinkedHashMap (Order), TreeMap (Sorted)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can explain how `HashSet` delegates to `HashMap` using static `PRESENT`.
- [ ] I can write the 10-line `LinkedHashMap` LRU Cache subclass pattern.
- [ ] I know why `LinkedHashMap.get()` mutates `modCount` when `accessOrder = true`.
- [ ] I can explain the dual pointer structure (`next` vs `before`/`after`).
- [ ] I know when to choose between `HashSet`, `LinkedHashSet`, and `TreeSet`.
