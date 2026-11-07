# 04. Open Addressing Mechanics, Linear/Quadratic Probing & Double Hashing

## 1. Introduction
**Open Addressing** is a primary collision resolution technique where all key-value entries are stored directly inside the primary bucket array itself, eliminating external linked list nodes. When a collision occurs ($h(k) \bmod M$ is occupied), Open Addressing probes alternative array slots sequentially using a **Probe Sequence** $h(k, i)$ for $i = 0, 1, 2 \dots M-1$. Probing schemes—including **Linear Probing**, **Quadratic Probing**, and **Double Hashing**—achieve **$O(1)$ Average Constant Time** with **Maximum CPU Cache Line Performance**.

> **Important:** In Open Addressing, deleting a key CANNOT simply set array slots to `null`! Setting a slot to `null` breaks probe sequences for subsequent elements that collided at the same initial index. Open Addressing MUST use a sentinel marker **`TOMBSTONE / DELETED`** to preserve lookup continuity!

```
Open Addressing Probing Sequence Topography:
Linear Probing    : h(k, i) = (h(k) + i) mod M            (Step size 1)
Quadratic Probing : h(k, i) = (h(k) + c1*i + c2*i^2) mod M (Accelerating step size)
Double Hashing    : h(k, i) = (h1(k) + i * h2(k)) mod M   (Custom step size per key) ⚡
```

---

## 2. Core Concepts & Probing Taxonomy

### 2.1 The 3 Primary Probing Schemes
1. **Linear Probing**: $h(k, i) = (h(k) + i) \bmod M$.
   - **Pros**: Exceptional CPU L1/L2 cache locality (pre-fetches contiguous memory blocks).
   - **Cons**: Severe **Primary Clustering** (long contiguous blocks of occupied slots build up, causing probe sequences to grow rapidly).
2. **Quadratic Probing**: $h(k, i) = (h(k) + c_1 i + c_2 i^2) \bmod M$.
   - **Pros**: Eliminates primary clustering by accelerating probe step size.
   - **Cons**: Vulnerable to **Secondary Clustering** (keys with identical initial hash codes follow identical probe paths).
3. **Double Hashing**: $h(k, i) = (h_1(k) + i \cdot h_2(k)) \bmod M$.
   - Uses two independent hash functions $h_1(k)$ and $h_2(k)$ (where $h_2(k) \ne 0$).
   - **Pros**: Completely eliminates primary AND secondary clustering! Each key follows a unique probe sequence determined by $h_2(k)$.

```
Probing Scheme Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Probing Scheme        | CPU Cache Hit Rate| Primary Cluster   | Secondary Cluster |
+-----------------------+-------------------+-------------------+-------------------+
| Linear Probing        | **Optimal ⚡**    | Severe            | High              |
| Quadratic Probing     | Moderate          | **Eliminated ⚡** | Moderate          |
| Double Hashing        | Low               | **Eliminated ⚡** | **Eliminated ⚡** |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Linear Probing: Best cache, worst clustering! Double Hashing: Worst cache, zero clustering!"**

---

## 3. Characteristics & Tombstone Deletion Mechanics

### 3.1 The Tombstone Marker Protocol
When deleting a key $K$ in Open Addressing:
* Setting `array[slot] = null` creates a "hole" that terminates future `get()` probe loops prematurely, causing existing keys inserted later in the probe sequence to become UNREACHABLE!
* **Protocol**: Mark deleted slots with a static sentinel object **`DELETED / TOMBSTONE`**:
  - `get()` treats `DELETED` as an occupied slot and **CONTINUES PROBING**.
  - `put()` treats `DELETED` as an empty slot and **OVERWRITES IT**.

```
Tombstone Deletion Continuity Topology:
Array Slots: [ Key A ] | [ DELETED ] | [ Key C (Collided with A) ]
                           ^
Search Key C: Hits A -> Hits DELETED (Continuation Signal!) -> Finds Key C at Index 2! ✅
```

---

## 4. Internal Working Mechanics
Tracing Double Hashing ($M = 7, h_1(k) = k \bmod 7, h_2(k) = 1 + (k \bmod 5)$):

```
Insert Key 14: h1(14) = 0. Index 0 is empty -> Insert 14 at Slot 0.
Insert Key 21: h1(21) = 0 (Collision at Slot 0!).
  - Compute step size: h2(21) = 1 + (21 % 5) = 2.
  - Probe 1 (i=1): (0 + 1*2) % 7 = 2. Slot 2 is empty -> Insert 21 at Slot 2.

Insert Key 28: h1(28) = 0 (Collision at Slot 0!).
  - Compute step size: h2(28) = 1 + (28 % 5) = 4.
  - Probe 1 (i=1): (0 + 1*4) % 7 = 4. Slot 4 is empty -> Insert 28 at Slot 4.

Keys 14, 21, 28 all collided at Slot 0, but followed UNIQUE step sizes (2 vs 4)! Zero Clustering! ✅
```

---

## 5. Visual Diagram
Linear vs Double Hashing Probe Sequence Distribution Topography:

```
Linear Probing (Step Size = 1):
[ Key A ] -> [ Key B ] -> [ Key C ] -> [ Key D ] (Primary Clustering Block!)

Double Hashing (Custom Step Size per Key):
[ Key A ] -------> [ Key B (Step 2) ] -------> [ Key C (Step 3) ] (Uniformly Distributed!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Double Hashing Open Addressing with Tombstone Deletions:

```java
import java.util.*;

public class OpenAddressingMaster {

    // Double Hashing Open Addressing Engine with Tombstone Markers
    public static class DoubleHashingHashMap<K, V> {
        private static class Entry<K, V> {
            K key;
            V value;

            Entry(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }

        @SuppressWarnings("unchecked")
        private final Entry<K, V> DELETED = new Entry<>(null, null); // Tombstone Sentinel

        private Entry<K, V>[] table;
        private int capacity;
        private int size;

        @SuppressWarnings("unchecked")
        public DoubleHashingHashMap(int capacity) {
            this.capacity = capacity;
            this.table = new Entry[capacity];
            this.size = 0;
        }

        // O(1) Average Put with Tombstone Reuse
        public boolean put(K key, V value) {
            if (key == null) return false;
            if (size >= capacity * 0.7) {
                resize(capacity * 2); // Resize at 70% load factor
            }

            int h1 = hash1(key);
            int h2 = hash2(key);
            int firstDeletedIndex = -1;

            for (int i = 0; i < capacity; i++) {
                int index = (h1 + i * h2) % capacity;

                if (table[index] == null) {
                    // Empty slot found! Insert at first deleted slot if available
                    int targetIndex = (firstDeletedIndex != -1) ? firstDeletedIndex : index;
                    table[targetIndex] = new Entry<>(key, value);
                    size++;
                    return true;
                } else if (table[index] == DELETED) {
                    if (firstDeletedIndex == -1) {
                        firstDeletedIndex = index; // Record first tombstone slot for reuse
                    }
                } else if (table[index].key.equals(key)) {
                    // Update existing key
                    table[index].value = value;
                    return true;
                }
            }

            return false; // Table full
        }

        // O(1) Average Get (Continues Probing Past Tombstones!)
        public V get(K key) {
            if (key == null) return null;

            int h1 = hash1(key);
            int h2 = hash2(key);

            for (int i = 0; i < capacity; i++) {
                int index = (h1 + i * h2) % capacity;

                if (table[index] == null) {
                    return null; // Search hit null -> Key not in table
                } else if (table[index] != DELETED && table[index].key.equals(key)) {
                    return table[index].value;
                }
            }

            return null;
        }

        // O(1) Average Tombstone Deletion
        public boolean remove(K key) {
            if (key == null) return false;

            int h1 = hash1(key);
            int h2 = hash2(key);

            for (int i = 0; i < capacity; i++) {
                int index = (h1 + i * h2) % capacity;

                if (table[index] == null) {
                    return false; // Key not found
                } else if (table[index] != DELETED && table[index].key.equals(key)) {
                    table[index] = DELETED; // Mark slot as TOMBSTONE
                    size--;
                    return true;
                }
            }

            return false;
        }

        private int hash1(K key) {
            return Math.abs(key.hashCode()) % capacity;
        }

        private int hash2(K key) {
            // Secondary hash MUST be non-zero and relatively prime to capacity
            int hash = Math.abs(key.hashCode() * 31 + 17) % (capacity - 1);
            return hash + 1;
        }

        @SuppressWarnings("unchecked")
        private void resize(int newCapacity) {
            Entry<K, V>[] oldTable = table;
            this.capacity = newCapacity;
            this.table = new Entry[newCapacity];
            this.size = 0;

            for (Entry<K, V> entry : oldTable) {
                if (entry != null && entry != DELETED) {
                    put(entry.key, entry.value);
                }
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Double Hashing Index Formula (h2 MUST be > 0!)
int index = (hash1(key) + i * hash2(key)) % capacity;
```

---

## 7. Concrete Problem Examples
* **High-Performance Embedded C/C++ Systems**: Open Addressing Linear Probing (maximum cache hits).
* **Python Dictionary (`dict`) Implementation**: Open Addressing with Pseudo-Random Probing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `DoubleHashingHashMap` and Tombstone Reuse:

```java
public class OpenAddressingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Double Hashing Open Addressing Demonstration ===");
        OpenAddressingMaster.DoubleHashingHashMap<String, Integer> map = 
            new OpenAddressingMaster.DoubleHashingHashMap<>(7);

        map.put("Key1", 100);
        map.put("Key2", 200);
        map.put("Key3", 300);

        System.out.println("Get Key2: " + map.get("Key2")); // Output: 200
        System.out.println("Removing Key2...");
        map.remove("Key2"); // Inserts TOMBSTONE marker

        System.out.println("Get Key3 (Probes past Tombstone): " + map.get("Key3")); // Output: 300
        System.out.println("Re-inserting Key4 (Reuses Tombstone slot)...");
        map.put("Key4", 400);
        System.out.println("Get Key4: " + map.get("Key4")); // Output: 400
    }
}
```

---

## 9. Complexity Analysis

| Probing Technique | Average Search Time | Worst Search Time | CPU Cache Locality | Primary Clustering |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Probing** | **$O(1)$ Constant ⚡** | $O(N)$ (High Cluster) | **Optimal ⚡** | Severe |
| **Quadratic Probing**| **$O(1)$ Constant ⚡** | $O(N)$ | Moderate | **Eliminated ⚡** |
| **Double Hashing** | **$O(1)$ Constant ⚡** | $O(N)$ | Low | **Eliminated ⚡** |

---

## 10. Edge Cases & Boundary Handling
* **$h_2(k) == 0$ in Double Hashing**: If $h_2(k) = 0$, step size becomes 0, resulting in an infinite loop! $h_2(k)$ MUST return a value $\ge 1$.
* **Relative Primality of $h_2(k)$ and Capacity $M$**: If $h_2(k)$ shares a common factor with $M$, probing skips bucket slots. Capacity $M$ should be a **Prime Number**.

---

## 11. Common Mistakes & Anti-Patterns
* **Setting Deleted Slots to `null`**:
  - Setting `table[index] = null` breaks probe sequence continuity, causing future `get()` queries to return `null` for valid keys!
  - **Always mark deleted slots with a `DELETED` Tombstone sentinel**.
* **Allowing $h_2(k) = 0$ in Double Hashing**:
  - If secondary hash yields 0, probing stalls at initial index forever.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Requirements for Double Hashing $h_2(k)$:
> 1. $h_2(k)$ MUST NEVER return 0 ($h_2(k) \ge 1$).
> 2. $h_2(k)$ MUST be relatively prime to capacity $M$ (guarantees probing visits every single array slot).
> 3. Standard Formula: $h_2(k) = R - (k \bmod R)$, where $R$ is a prime number $< M$.

> **Memory Trick:** **"Secondary Hash h2(k) MUST NEVER equal 0! Use h2(k) = 1 + (hash % (M - 1))!"**

---

## 13. System & Implementation Comparisons

| Feature | Open Addressing | Separate Chaining |
| :--- | :--- | :--- |
| **CPU Cache Locality** | **Optimal (Contiguous Array) ⚡**| Poor (Heap Pointers) |
| **Deletion Mechanics** | Requires `DELETED` Tombstones | Simple Node Pointer Removal |
| **Memory Efficiency** | **No Node Object Overhead ⚡**| 24 Bytes Node Overhead per Elem |

---

## 14. How to Recognize This in Questions
* **"Design a Hash Map without external linked list nodes"** $\rightarrow$ Open Addressing.
* **"Eliminate primary clustering while maintaining open addressing"** $\rightarrow$ Double Hashing.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Linear Probing suffer from Primary Clustering?**  
  *A:* Because any key that hashes to ANY slot within an existing contiguous cluster of occupied cells will be forced to append to the end of that cluster, causing contiguous blocks of filled slots to grow longer exponentially.
* **Q: How are Tombstones cleaned up in Open Addressing?**  
  *A:* During table rehashing (when capacity doubles), `DELETED` Tombstones are discarded, and only valid key-value entries are re-inserted into the new table.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: OPEN ADDRESSING & DOUBLE HASHING                      |
+-----------------------------------------------------------------------+
| • Linear Probing Formula: h(k, i) = (h1(k) + i) % M                   |
| • Double Hashing Formula: h(k, i) = (h1(k) + i * h2(k)) % M           |
| • Secondary Hash Constraint: h2(k) MUST NEVER equal 0!                |
| • Tombstone Rule: Mark deletions with DELETED sentinel to preserve probes|
| • Tombstone Reuse: put() overwrites DELETED slots; get() probes past  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement Double Hashing Open Addressing from scratch.
- [ ] I know why `DELETED` Tombstones are required for deletions.
- [ ] I know why secondary hash $h_2(k)$ must never return 0.
- [ ] I can explain Primary vs Secondary Clustering.
- [ ] I know how Tombstones are purged during table rehashing.
