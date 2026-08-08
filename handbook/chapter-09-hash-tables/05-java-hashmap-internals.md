# 05. Java HashMap Internals, JDK Source Code & Bitwise Resizing

## 1. Introduction
Java's **`java.util.HashMap`** is one of the most sophisticated, high-performance data structures in the Java Standard Library. In technical coding interviews and senior software engineering architecture rounds, deep familiarity with Java's internal `HashMap` source code—including the 64-bit object memory layout of `Node<K,V>`, bitwise power-of-two index calculations, load factor thresholds, the **`resize()` Bit-Transfer Optimization** (which splits bucket chains without recalculating modulo remainder), and thread-safety invariants—distinguishes top 1% Java developers.

> **Important:** In Java 7 and earlier, multi-threaded `HashMap.put()` resizing caused an **Infinite Loop CPU 100% Hang** due to head-insertion list reversals during resizing. Java 8 fixed this by using **Tail Insertion** during resizing, preserving node insertion order!

```
Java HashMap JDK Evolution:
+-----------------------------------------------------------------------------------+
| Java 7 HashMap : Entry<K,V>[] table -> Head Insertion -> Resize Infinite Loop Bug|
| Java 8+ HashMap: Node<K,V>[] table  -> Tail Insertion -> Treeification at >=8    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & JDK Source Code Constants

### 2.1 Key JDK Source Code Constants
From `java.util.HashMap` JDK source code:

```java
static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // 16 (Must be power of 2!)
static final int MAXIMUM_CAPACITY = 1 << 30;       // 1,073,741,824
static final float DEFAULT_LOAD_FACTOR = 0.75f;    // 75% load factor threshold
static final int TREEIFY_THRESHOLD = 8;            // Convert list to tree
static final int UNTREEIFY_THRESHOLD = 6;          // Convert tree back to list
static final int MIN_TREEIFY_CAPACITY = 64;        // Min capacity for treeify
```

### 2.2 The `Node<K,V>` Internal Class
Each key-value pair is stored as an instance of `HashMap.Node<K,V>`:

```java
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;  // Cached 32-bit spread hash code
    final K key;     // Key object reference
    V value;         // Value object reference
    Node<K,V> next;  // Reference to next node in bucket chain
}
```

### 2.3 64-Bit JVM Node Memory Footprint
In a 64-bit JVM with Compressed OOPs (`-XX:+UseCompressedOops`, active by default for heaps $< 32\text{GB}$):
* **Mark Word**: 8 Bytes (Header lock/age metadata)
* **Klass Word**: 4 Bytes (Compressed class pointer)
* **`int hash`**: 4 Bytes (Cached hash value)
* **`K key` Ref**: 4 Bytes (Compressed OOP reference)
* **`V value` Ref**: 4 Bytes (Compressed OOP reference)
* **`Node next` Ref**: 4 Bytes (Compressed OOP reference)
* **Padding**: 4 Bytes (Aligns to 8-byte boundary)
* **Total Memory Footprint**: **32 Bytes per Node object!** (Excluding key and value object payloads).

> **Memory Trick:** **"1 HashMap Node = 32 Bytes of RAM! Default capacity is 16, Default load factor is 0.75!"**

---

## 3. Characteristics & Bitwise Resizing Optimization

### 3.1 The Bitwise Mask Index Trick
Because table capacity $m$ is constrained to a power of two ($m = 2^k$), computing bucket index avoids expensive integer division:

$$\text{index} = \text{hash} \ \& \ (m - 1)$$

### 3.2 Java 8 Bit-Transfer Resizing Optimization ($O(N)$ Time)
When `HashMap` doubles its capacity from $m$ to $2m$, every element in bucket $i$ will either:
1. Stay at the **exact same index $i$** in the new table, OR
2. Move to **index $i + m$** (old index plus old capacity) in the new table!

#### How Java 8 Determines Node Position WITHOUT Recalculating Hash/Modulo:
Java inspects the single bit corresponding to `oldCap` in the element's hash:

$$\text{bitCheck} = \text{hash} \ \& \ \text{oldCap}$$

* **If `(hash & oldCap) == 0`**: The element stays at index $i$ in the new table (**`loHead` chain**).
* **If `(hash & oldCap) != 0`**: The element moves to index $i + \text{oldCap}$ in the new table (**`hiHead` chain**).

This elegant bitwise check allows Java 8 to split a bucket chain into two pristine sub-chains (`loHead` and `hiHead`) in a single pass without re-executing `hashCode()` or modulo division!

```
Bit-Transfer Resizing Example (oldCap = 16 = 0x10):
Element A: hash = 0010 1101 (45) -> 45 & 16 (0001 0000) = 0001 0000 (Non-Zero!) -> Moves to index 13 + 16 = 29!
Element B: hash = 0000 1101 (13) -> 13 & 16 (0001 0000) = 0000 0000 (Zero!)     -> Stays at index 13!
```

---

## 4. Internal Working Mechanics
Tracing Java 8 `HashMap.put()` Source Code Flow:

```
[ HashMap.put(key, value) ]
           |
           v
[ Compute spread hash: h = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16) ]
           |
           v
[ Is table empty/null? ] ---> YES ---> [ Call resize() to allocate 16 slots ]
           | NO
           v
[ Compute index: i = (n - 1) & h ]
           |
           v
[ Is table[i] empty? ] ---> YES ---> [ Create new Node(h, key, value, null) at table[i] ]
           | NO
           v
[ Collision Handling ]
           |-- Key matches table[i] key? ---> Overwrite Value
           |-- table[i] is TreeNode?    ---> Put into Red-Black Tree
           |-- table[i] is LinkedList Node:
                   Traverse chain. Append new Node at Tail.
                   Count binCount. If binCount >= 7 (8th node) ---> Call treeifyBin(i)
           |
           v
[ Increment size. Does size > threshold (n * loadFactor)? ] ---> YES ---> [ Call resize() ]
```

---

## 5. Visual Diagram
Java 8 Bit-Transfer Bucket Splitting During Resizing ($16 \to 32$):

```
OLD TABLE (Capacity 16, Mask = 15 = 0x0F)
Index 13: [ Node A (hash=13) ] ---> [ Node B (hash=45) ] ---> [ Node C (hash=29) ]
             (13 & 16 == 0)           (45 & 16 != 0)           (29 & 16 != 0)

                               |
                               v  RESIZE TO CAPACITY 32
NEW TABLE (Capacity 32, Mask = 31 = 0x1F)
Index 13 (loHead): [ Node A (hash=13) ] ---> null
Index 29 (hiHead): [ Node B (hash=45) ] ---> [ Node C (hash=29) ] ---> null

Notice: Zero modulo recomputations! Chain split into low and high chains using (hash & oldCap)!
```

---

## 6. Operations & Deep JDK-Style Source Implementation
Complete production-grade implementation mirroring Java 8's exact `HashMap` bitwise resizing, low/high chain splitting, and `putVal()` logic:

```java
import java.util.Objects;

public class CustomJDKHashMap<K, V> {

    static final int DEFAULT_INITIAL_CAPACITY = 16;
    static final int MAXIMUM_CAPACITY = 1 << 30;
    static final float DEFAULT_LOAD_FACTOR = 0.75f;

    static class Node<K, V> {
        final int hash;
        final K key;
        V value;
        Node<K, V> next;

        Node(int hash, K key, V value, Node<K, V> next) {
            this.hash = hash;
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    private Node<K, V>[] table;
    private int size;
    private int threshold;
    private final float loadFactor;

    public CustomJDKHashMap() {
        this.loadFactor = DEFAULT_LOAD_FACTOR;
        this.threshold = (int) (DEFAULT_INITIAL_CAPACITY * DEFAULT_LOAD_FACTOR);
    }

    static final int hash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }

    public V get(K key) {
        Node<K, V> e = getNode(hash(key), key);
        return e == null ? null : e.value;
    }

    final Node<K, V> getNode(int hash, Object key) {
        Node<K, V>[] tab = table;
        int n;
        if (tab != null && (n = tab.length) > 0) {
            Node<K, V> first = tab[(n - 1) & hash];
            if (first != null) {
                if (first.hash == hash && Objects.equals(first.key, key)) {
                    return first;
                }
                Node<K, V> e = first.next;
                if (e != null) {
                    do {
                        if (e.hash == hash && Objects.equals(e.key, key)) {
                            return e;
                        }
                    } while ((e = e.next) != null);
                }
            }
        }
        return null;
    }

    public V put(K key, V value) {
        return putVal(hash(key), key, value);
    }

    @SuppressWarnings("unchecked")
    final V putVal(int hash, K key, V value) {
        Node<K, V>[] tab = table;
        int n;
        if (tab == null || (n = tab.length) == 0) {
            tab = resize();
            n = tab.length;
        }

        int i = (n - 1) & hash;
        Node<K, V> p = tab[i];

        if (p == null) {
            tab[i] = new Node<>(hash, key, value, null);
        } else {
            Node<K, V> e = null;
            if (p.hash == hash && Objects.equals(p.key, key)) {
                e = p;
            } else {
                Node<K, V> curr = p;
                while (true) {
                    if (curr.hash == hash && Objects.equals(curr.key, key)) {
                        e = curr;
                        break;
                    }
                    if (curr.next == null) {
                        curr.next = new Node<>(hash, key, value, null);
                        break;
                    }
                    curr = curr.next;
                }
            }

            if (e != null) { // Existing key found
                V oldValue = e.value;
                e.value = value;
                return oldValue;
            }
        }

        if (++size > threshold) {
            resize();
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    final Node<K, V>[] resize() {
        Node<K, V>[] oldTab = table;
        int oldCap = (oldTab == null) ? 0 : oldTab.length;
        int oldThr = threshold;
        int newCap, newThr = 0;

        if (oldCap > 0) {
            if (oldCap >= MAXIMUM_CAPACITY) {
                threshold = Integer.MAX_VALUE;
                return oldTab;
            } else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY && oldCap >= DEFAULT_INITIAL_CAPACITY) {
                newThr = oldThr << 1; // Double threshold
            }
        } else { // Initial capacity
            newCap = DEFAULT_INITIAL_CAPACITY;
            newThr = (int) (DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
        }

        threshold = newThr;
        Node<K, V>[] newTab = (Node<K, V>[]) new Node[newCap];
        table = newTab;

        if (oldTab != null) {
            for (int j = 0; j < oldCap; ++j) {
                Node<K, V> e = oldTab[j];
                if (e != null) {
                    oldTab[j] = null; // Clear old table reference for GC
                    if (e.next == null) {
                        newTab[e.hash & (newCap - 1)] = e;
                    } else { // Preserving Tail Insertion Order (Bit-Transfer Optimization!)
                        Node<K, V> loHead = null, loTail = null;
                        Node<K, V> hiHead = null, hiTail = null;
                        Node<K, V> next;
                        do {
                            next = e.next;
                            // Check bit at oldCap offset
                            if ((e.hash & oldCap) == 0) {
                                if (loTail == null) loHead = e;
                                else loTail.next = e;
                                loTail = e;
                            } else {
                                if (hiTail == null) hiHead = e;
                                else hiTail.next = e;
                                hiTail = e;
                            }
                        } while ((e = next) != null);

                        if (loTail != null) {
                            loTail.next = null;
                            newTab[j] = loHead; // Stays at same index j
                        }
                        if (hiTail != null) {
                            hiTail.next = null;
                            newTab[j + oldCap] = hiHead; // Moves to index j + oldCap
                        }
                    }
                }
            }
        }
        return newTab;
    }

    public int size() { return size; }
    public int capacity() { return table == null ? 0 : table.length; }
}
```

> **Quick Syntax:**
```java
// Java 8 Bit-Transfer Resizing Check
if ((e.hash & oldCap) == 0) {
    // Append to loHead chain -> Stays at index j
} else {
    // Append to hiHead chain -> Moves to index j + oldCap
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 1 - Two Sum**: Utilizing Java `HashMap` for $O(1)$ complement indexing.
* **LeetCode 560 - Subarray Sum Equals K**: Utilizing Prefix Sums + `HashMap` frequency tracking in $O(N)$ time.
* **LeetCode 138 - Copy List with Random Pointer**: Utilizing `HashMap<Node, Node>` mapping in $O(N)$ time.

---

## 8. Java Code Demonstration & Dry Run
Demonstration inspecting initial capacity allocation, automatic bit-transfer resizing, and index splitting:

```java
public class JDKHashMapInternalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing JDK-Style HashMap Resizing ===");
        CustomJDKHashMap<Integer, String> map = new CustomJDKHashMap<>();

        System.out.println("Initial Capacity: " + map.capacity());

        // Insert 12 elements (12 is threshold for cap 16 at 0.75 load factor)
        for (int i = 1; i <= 12; i++) {
            map.put(i, "Value-" + i);
        }
        System.out.println("Size: " + map.size() + ", Capacity after 12 puts: " + map.capacity());

        // 13th element triggers resize (16 -> 32)
        map.put(13, "Value-13");
        System.out.println("Size: " + map.size() + ", Capacity after 13th put: " + map.capacity() + " (DOUBLED!)");

        // Verify retrieval of all elements
        System.out.println("\n=== 2. Verifying Key Lookups ===");
        System.out.println("Key 5:  " + map.get(5));
        System.out.println("Key 13: " + map.get(13));
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Space Complexity | JDK Mechanism |
| :--- | :--- | :--- | :--- |
| **`get(key)`** | **Average $O(1)$** | $O(1)$ | Bitwise mask `hash & (n - 1)` |
| **`put(key, val)`** | **Amortized $O(1)$**| $O(1)$ | Tail insertion + `(hash & oldCap)` split |
| **`resize()` (Capacity $m \to 2m$)**| **$O(N)$ Linear** | $O(2m)$ Array | Single pass bit-transfer splitting |
| **Space Overhead** | $O(N + m)$ | **32 Bytes / Node**| Header + Hash + Key + Val + Next |

---

## 10. Edge Cases & Boundary Handling
* **Java 7 Multi-Threaded Infinite Loop Bug**: In Java 7, `transfer()` used Head Insertion. If Thread 1 and Thread 2 resized concurrently, pointer references in a bucket list became inverted into a cycle (`A.next = B` and `B.next = A`). Subsequent `get()` calls on that bucket resulted in an **infinite loop spinning CPU at 100%**! Java 8 fixed this by using **Tail Insertion** (`loTail`, `hiTail`) during `resize()`, preserving insertion order.
* **ConcurrentModificationException**: Modifying a `HashMap` structurally while iterating over it via an `Iterator` throws `ConcurrentModificationException` (via `modCount` check).

---

## 11. Common Mistakes & Anti-Patterns
* **Using `HashMap` in Multi-Threaded Environments**: `HashMap` is NOT thread-safe! Concurrent writes corrupt array state or drop entries. Use **`ConcurrentHashMap`** for thread-safe applications.
* **Initializing `HashMap` without Capacity Planning**: Creating a `HashMap` that will hold 1,000,000 items with default initial capacity 16 causes **16 expensive resize passes** ($16 \to 32 \to 64 \dots \to 2,097,152$), copying 1 million objects 16 times!
  * **Fix**: Pass initial capacity: `new HashMap<>((int) (targetSize / 0.75f) + 1);`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Initial Capacity Formula for Large Datasets:
> If you know your map will store $N$ elements, initialize it with capacity:
> **`int initialCapacity = (int) Math.ceil(N / 0.75f);`**
> This avoids expensive dynamic array allocation and bit-transfer rehashing during bulk insertions!

> **Memory Trick:** **"Java 7 Head Insertion = Infinite Loop Resizing Bug! Java 8 Tail Insertion = Order Preserved!"**

---

## 13. System & Implementation Comparisons

| Feature | Java 7 HashMap | Java 8+ HashMap | `ConcurrentHashMap` |
| :--- | :--- | :--- | :--- |
| **Resizing Order** | Head Insertion (Reverses list) | **Tail Insertion (Preserves order)**| Tail Insertion |
| **Thread Safety** | Unsafe (CPU 100% Loop Bug) | Unsafe (Data Loss / Corruption) | **100% Thread-Safe (CAS + Locks)** |
| **Bucket Structure** | Singly Linked List Only | **Hybrid List $\to$ Red-Black Tree**| Hybrid List $\to$ Red-Black Tree |
| **Multi-Thread Lock** | None | None | **Segment Locks / CAS Synchronized**|

---

## 14. How to Recognize This in Questions
* **"Explain Java 8 HashMap resizing optimization"** $\rightarrow$ `(hash & oldCap)` splits bucket chain into `loHead` and `hiHead` without hash recalculation.
* **"Explain why Java 7 HashMap caused CPU 100% infinite loops"** $\rightarrow$ Concurrent head-insertion resizing created reference cycles.

---

## 15. Frequently Asked Interview Questions
* **Q: How does `(e.hash & oldCap) == 0` split bucket chains during `resize()`?**  
  *A:* Because capacity doubles from $m = 2^k$ to $2m = 2^{k+1}$, the new mask $2^{k+1} - 1$ includes one additional bit (the bit at position $2^k = \text{oldCap}$). If an element's hash has a `0` at that bit position, its index is unchanged ($i$). If it has a `1`, its new index is $i + \text{oldCap}$.
* **Q: Why is default load factor 0.75 chosen in Java's HashMap?**  
  *A:* 0.75 offers the optimal trade-off between spatial overhead and computational time. Higher load factors ($\alpha > 0.8$) reduce memory footprint but increase collision frequency and search times. Lower load factors ($\alpha < 0.5$) waste significant array memory.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JAVA HASHMAP INTERNALS & BITWISE RESIZING             |
+-----------------------------------------------------------------------+
| • Default Capacity = 16 (1 << 4), Load Factor = 0.75, Max Cap = 1 << 30|
| • 64-bit JVM Node Memory: 32 Bytes per Node object                    |
| • Index Mask: index = hash & (capacity - 1)                           |
| • Bit-Transfer Resizing (Java 8): if ((hash & oldCap) == 0)           |
|   -> Stays at index j (loHead chain)                                  |
|   -> Else moves to index j + oldCap (hiHead chain)                    |
| • Zero Hash Recomputation: Splits bucket chains in 1 pass via bit-test|
| • Java 7 Bug Fixed: Java 8 uses Tail Insertion to prevent loop cycles |
| • Capacity Formula: Set initialCapacity = (N / 0.75f) + 1 to avoid resize|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can state the 6 JDK HashMap constants and their default values.
- [ ] I can write the 32-byte memory breakdown for a 64-bit JVM `Node<K,V>`.
- [ ] I can derive why `(hash & oldCap) == 0` splits bucket chains into `loHead` and `hiHead`.
- [ ] I know why Java 7 caused CPU 100% infinite loop hangs during concurrent resizing.
- [ ] I know how Java 8 Tail Insertion solved the concurrent resizing loop bug.
- [ ] I can calculate the optimal `initialCapacity` for a dataset of size $N$.
