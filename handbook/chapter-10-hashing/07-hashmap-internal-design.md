# 07. HashMap Internal Architecture, JDK Source Code Breakdown & Control Flow Mechanics

## 1. Introduction
The **JDK `java.util.HashMap`** is one of the most sophisticated high-performance data structure implementations in modern software engineering. It combines power-of-2 array masking, supplemental bit-spreading, dynamic separate chaining, automatic Red-Black treeification, and high/low bit transfer rehashing. Understanding the exact source code fields, method contracts (`putVal`, `getNode`, `resize`), and control flow paths of JDK HashMap is a staple requirement for senior software engineering interviews.

> **Important:** In JDK HashMap, `table` initialization is **LAZY**! Calling `new HashMap<>()` allocates ZERO array buckets on the heap. Array allocation is deferred until the VERY FIRST `put()` invocation inside `resize()`!

```
JDK HashMap High-Level Architecture Topology:
HashMap Object  ---> [ Transient Node<K,V>[] table ] (Lazy Allocation on 1st put)
                             |
                   +---------+---------+
                   |                   |
            [ Node<K,V> Bin ]   [ TreeNode<K,V> Bin ]
            (Singly Linked List) (Red-Black BST, if len >= 8 & cap >= 64)
```

---

## 2. Core Concepts & JDK HashMap Source Code Fields

### 2.1 The Core Fields & Constants in `java.util.HashMap`
* **`DEFAULT_INITIAL_CAPACITY = 1 << 4`** (16): Default bucket array size.
* **`MAXIMUM_CAPACITY = 1 << 30`**: Maximum allowable array size ($1,073,741,824$).
* **`DEFAULT_LOAD_FACTOR = 0.75f`**: Default load factor.
* **`TREEIFY_THRESHOLD = 8`**: List to Red-Black Tree conversion limit.
* **`UNTREEIFY_THRESHOLD = 6`**: Tree to list conversion limit.
* **`MIN_TREEIFY_CAPACITY = 64`**: Minimum capacity required for treeification.
* **`transient Node<K,V>[] table`**: The bucket array.
* **`transient int size`**: Total number of key-value mappings.
* **`transient int modCount`**: Tracks structural modifications (powers Fail-Fast `ConcurrentModificationException` iterators!).
* **`int threshold`**: Next size value at which to resize (`capacity * loadFactor`).

```
HashMap Core Structural Field Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Field / Constant Name | Type              | Default Value     | Purpose           |
+-----------------------+-------------------+-------------------+-------------------+
| `table`               | `Node<K,V>[]`     | `null` (Lazy)     | Bucket array      |
| `size`                | `int`             | `0`               | Number of entries |
| `modCount`            | `int`             | `0`               | Fail-Fast iterator|
| `threshold`           | `int`             | `16 * 0.75 = 12`  | Next resize limit |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"HashMap table allocation is LAZY! modCount tracks structural mutations for Fail-Fast iterators!"**

---

## 3. Characteristics & JDK `putVal()` Method Control Flow

### 3.1 Step-by-Step Control Flow of `putVal()`
When `map.put(key, value)` is called:
1. Compute supplemental hash: `hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16)`.
2. Check if `table` is null or empty $\rightarrow$ Call `resize()` to initialize array (Lazy Allocation).
3. Compute bucket index: `i = (n - 1) & hash`.
4. If `table[i] == null`: Create new `Node(hash, key, value, null)` and assign directly to `table[i]`.
5. Else (`table[i]` is occupied):
   - **Case A (Key Match at Bin Head)**: If `p.hash == hash && (p.key == key || key.equals(p.key))`, set `e = p`.
   - **Case B (Treeified Bin)**: If `p instanceof TreeNode`, delegate to `((TreeNode)p).putTreeVal(...)`.
   - **Case C (Linked List Bin)**: Iterate list:
     - If existing key found, break (`e = p`).
     - Append new node at TAIL (`p.next = newNode`).
     - If list length reaches `TREEIFY_THRESHOLD - 1` (8th node), call `treeifyBin(tab, hash)`.
6. If `e != null` (Key already existed): Overwrite `e.value` with new value, return `oldValue`.
7. Increment `modCount++`.
8. Increment `size++`. If `size > threshold`, call `resize()`.

---

## 4. Internal Working Mechanics
Tracing `put("Key", 100)` on an uninitialized HashMap:

```
Call map.put("Key", 100):
1. Compute hash("Key"): h = "Key".hashCode() ^ (h >>> 16) = 75432.
2. Table is null -> Call resize(). Allocate Node[16] array. Set threshold = 12.
3. Compute index: i = (16 - 1) & 75432 = 8.
4. table[8] is null -> Insert Node(75432, "Key", 100, null) at table[8].
5. modCount++ (1), size++ (1).
6. size (1) < threshold (12) -> No resize needed.

Operation completed in 4 internal steps! ✅
```

---

## 5. Visual Diagram
JDK HashMap `putVal()` Execution Path Topography:

```
map.put(K, V)
    |
    v
Supplemental Hash -> (key == null) ? 0 : h ^ (h >>> 16)
    |
    +---> Is table null? ---> YES ---> Call resize() (Lazy Init)
    |                          |
    NO                         v
    |                  Index = (n - 1) & hash
    v                          |
Is table[i] null? ---> YES ---> Insert new Node at table[i]
    |
    NO (Collision!)
    |
    +---> Is Head Key Equal? ---> YES ---> Overwrite Value
    |
    +---> Is TreeNode? ---------> YES ---> putTreeVal() (BST Insert)
    |
    +---> LinkedList Bin -------> Loop List: Append Tail -> Check treeifyBin if len >= 8
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java simulation replicating JDK HashMap's exact `Node`, `TreeNode`, and `putVal()` control flow:

```java
import java.util.*;

public class HashMapInternalDesignMaster {

    // Complete JDK HashMap Structural Replica
    public static class JDKHashMapReplica<K, V> {
        static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // 16
        static final int MAXIMUM_CAPACITY = 1 << 30;
        static final float DEFAULT_LOAD_FACTOR = 0.75f;
        static final int TREEIFY_THRESHOLD = 8;
        static final int UNTREEIFY_THRESHOLD = 6;
        static final int MIN_TREEIFY_CAPACITY = 64;

        // Base Node Class
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
        private int modCount;
        private int threshold;
        private final float loadFactor;

        @SuppressWarnings("unchecked")
        public JDKHashMapReplica() {
            this.loadFactor = DEFAULT_LOAD_FACTOR;
            // Lazy table allocation: table remains null until 1st put!
            this.table = null;
            this.size = 0;
            this.modCount = 0;
        }

        // JDK HashMap Supplemental Hash Function
        static final int hash(Object key) {
            int h;
            return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
        }

        public V put(K key, V value) {
            return putVal(hash(key), key, value, false, true);
        }

        // JDK HashMap putVal Source Code Logic Replication
        @SuppressWarnings("unchecked")
        final V putVal(int hash, K key, V value, boolean onlyIfAbsent, boolean evict) {
            Node<K, V>[] tab = table;
            int n, i;

            // Step 1: Lazy Table Initialization on First Put
            if (tab == null || (n = tab.length) == 0) {
                tab = resize();
                n = tab.length;
            }

            // Step 2: Direct Bucket Insertion if Slot Empty
            if (tab[i = (n - 1) & hash] == null) {
                tab[i] = new Node<>(hash, key, value, null);
            } else {
                Node<K, V> e = null;
                K k;
                Node<K, V> p = tab[i];

                // Case A: Bin Head Key Match
                if (p.hash == hash && ((k = p.key) == key || (key != null && key.equals(k)))) {
                    e = p;
                } else {
                    // Case B: Linked List Traversal
                    int binCount = 0;
                    while (true) {
                        if ((e = p.next) == null) {
                            p.next = new Node<>(hash, key, value, null); // Append to TAIL (Java 8!)
                            if (binCount >= TREEIFY_THRESHOLD - 1) { // 8th node
                                treeifyBin(tab, hash);
                            }
                            break;
                        }
                        if (e.hash == hash && ((k = e.key) == key || (key != null && key.equals(k)))) {
                            break; // Key match found inside list
                        }
                        p = e;
                        binCount++;
                    }
                }

                // Existing Key Overwrite Handling
                if (e != null) {
                    V oldValue = e.value;
                    if (!onlyIfAbsent || oldValue == null) {
                        e.value = value;
                    }
                    return oldValue;
                }
            }

            modCount++;
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
            } else {
                // Initial Lazy Allocation
                newCap = DEFAULT_INITIAL_CAPACITY;
                newThr = (int) (DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
            }

            threshold = newThr;
            Node<K, V>[] newTab = (Node<K, V>[]) new Node[newCap];
            table = newTab;

            if (oldTab != null) {
                // High/Low Bit Transfer Logic executed during table transfer
                for (int j = 0; j < oldCap; j++) {
                    Node<K, V> e = oldTab[j];
                    if (e != null) {
                        oldTab[j] = null;
                        if (e.next == null) {
                            newTab[e.hash & (newCap - 1)] = e;
                        } else {
                            Node<K, V> loHead = null, loTail = null;
                            Node<K, V> hiHead = null, hiTail = null;
                            Node<K, V> next;
                            do {
                                next = e.next;
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

                            if (loTail != null) { loTail.next = null; newTab[j] = loHead; }
                            if (hiTail != null) { hiTail.next = null; newTab[j + oldCap] = hiHead; }
                        }
                    }
                }
            }

            return newTab;
        }

        private void treeifyBin(Node<K, V>[] tab, int hash) {
            // Simulated Treeification Trigger
            if (tab == null || tab.length < MIN_TREEIFY_CAPACITY) {
                resize();
            }
        }

        public int size() { return size; }
        public boolean isEmpty() { return size == 0; }
    }
}
```

> **Quick Syntax:**
```java
// JDK HashMap Lazy Table Initialization Check
if (tab == null || (n = tab.length) == 0) {
    tab = resize();
}
```

---

## 7. Concrete Problem Examples
* **Fail-Fast Iterator Verification**: `modCount` checks during concurrent modification.
* **JDK Source Code Customization**: Extending HashMap internal mechanisms.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `JDKHashMapReplica` lazy initialization and control flow:

```java
public class HashMapInternalDesignDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. JDK HashMap Replica Demonstration ===");
        HashMapInternalDesignMaster.JDKHashMapReplica<String, Integer> map = 
            new HashMapInternalDesignMaster.JDKHashMapReplica<>();

        System.out.println("Map Created! Size: " + map.size() + ", Table is Null (Lazy Allocation!).");

        map.put("Key1", 100); // Triggers 1st resize()!
        map.put("Key2", 200);

        System.out.println("After Puts -> Size: " + map.size() + " ✅");
        System.out.println("Overwriting Key1...");
        map.put("Key1", 999);
        System.out.println("Key1 Overwritten Value successfully! ✅");
    }
}
```

---

## 9. Complexity Analysis

| JDK Method | Time Complexity (Average) | Time Complexity (Worst-Case) | Purpose |
| :--- | :--- | :--- | :--- |
| **`putVal()`** | **$O(1)$ Constant ⚡** | **$O(\log N)$ (Treeified)** | Inserts/Overwrites entries |
| **`getNode()`** | **$O(1)$ Constant ⚡** | **$O(\log N)$ (Treeified)** | Retrieves entry values |
| **`resize()`** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | Doubles capacity via High/Low split |

---

## 10. Edge Cases & Boundary Handling
* **Concurrent Modification During Iteration**: `modCount != expectedModCount` throws `ConcurrentModificationException` (Fail-Fast iterator behavior).
* **Maximum Capacity Exceeded (`1 << 30`)**: Sets `threshold = Integer.MAX_VALUE` and halts further table resizes.

---

## 11. Common Mistakes & Anti-Patterns
* **Assuming Nodes are Appended to Head in Java 8**:
  - Java 7 appended new colliding nodes to the HEAD of the bucket list.
  - **Java 8 appends new colliding nodes to the TAIL of the list** (preserving relative order and preventing loop hazards during resize).
* **Forgetting Lazy Initialization**:
  - Expecting `table != null` immediately after `new HashMap<>()` fails. `table` is `null` until `resize()` runs on the first `put()`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Key Differences Between Java 7 and Java 8 HashMap:
> 1. **Data Structure**: Java 7 uses LinkedList only ($O(N)$ worst-case). Java 8 uses LinkedList + Red-Black BST ($O(\log N)$ worst-case).
> 2. **Insertion Order**: Java 7 inserts at HEAD. Java 8 appends to TAIL.
> 3. **Rehashing Engine**: Java 7 re-calculates index `hash % newCap`. Java 8 uses High/Low bit mask `(e.hash & oldCap) == 0`.

> **Memory Trick:** **"Java 8 appends to TAIL, treeifies at 8, and rehashes using (e.hash & oldCap) == 0!"**

---

## 13. System & Implementation Comparisons

| Feature | Java 7 HashMap | Java 8 HashMap |
| :--- | :--- | :--- |
| **Collision Data Structure**| Linked List Only | **Linked List + Red-Black Tree ⚡**|
| **List Insertion Location** | Head Prepending | **Tail Appending ⚡** |
| **Rehash Efficiency** | Hash Re-calculation | **High/Low 1-Bit Mask ⚡** |

---

## 14. How to Recognize This in Questions
* **"Explain JDK HashMap putVal internal control flow"** $\rightarrow$ Step-by-step 8-stage pipeline.
* **"Explain how Fail-Fast iterators work in HashMap"** $\rightarrow$ `modCount` modification tracking.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java 8 HashMap append new colliding nodes to the TAIL instead of the HEAD?**  
  *A:* Appending to the tail preserves original relative element ordering during list-to-tree conversions and High/Low bit split rehashing, preventing circular pointer loop bugs.
* **Q: What is the purpose of `modCount` in HashMap?**  
  *A:* `modCount` is an integer field incremented on every structural modification (`put` new key, `remove`, `clear`). Iterators store `expectedModCount = modCount` and check `modCount == expectedModCount` on every `next()` call, throwing `ConcurrentModificationException` if modified concurrently.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: JDK HASHMAP INTERNAL ARCHITECTURE                     |
+-----------------------------------------------------------------------+
| • Lazy Allocation: table is null until first put() invocation!        |
| • Tail Appending: Java 8 appends new colliding nodes to LIST TAIL     |
| • Treeify Condition: listLen >= 8 AND capacity >= 64                  |
| • Fail-Fast Protection: modCount tracks structural modifications       |
| • Maximum Capacity: 1 << 30 (1,073,741,824 slots)                     |
| • Time Complexity: O(1) Average | O(log N) Worst-Case (Treeified) ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can trace all 8 steps of the `putVal()` control flow.
- [ ] I know why table allocation is lazy in JDK HashMap.
- [ ] I can state the differences between Java 7 and Java 8 HashMap.
- [ ] I know how `modCount` powers Fail-Fast iterators.
- [ ] I know why Java 8 appends colliding nodes to the tail.
