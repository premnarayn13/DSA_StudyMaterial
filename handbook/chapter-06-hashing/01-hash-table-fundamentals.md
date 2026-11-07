# 01. Hash Table Fundamentals, Key-Value Associative Mapping & Constant-Time Invariants

## 1. Introduction
A **Hash Table** (or **Hash Map**) is an essential associative data structure designed to map arbitrary keys to corresponding values. By applying a mathematical **Hash Function** $h(k)$ to map keys into array bucket indices, Hash Tables achieve **$O(1)$ Average-Case Constant Time** for search (`get`), insertion (`put`), and deletion (`remove`) operations.

> **Important:** The key architectural trade-off of Hash Tables is **Trading Memory for Time**. By allocating an array of bucket slots and converting keys into integer hash codes, Hash Tables transform $O(N)$ linear search into **$O(1)$ Average Constant-Time Lookup**, making them the backbone of database indexing, caches, and high-frequency key-value storage!

```
Hash Table Key-Value Mapping Topology:
Key ("Alice")  ---> [ Hash Function h(k) ] ---> Bucket Index 4 ---> Value ("555-0199")
Key ("Bob")    ---> [ Hash Function h(k) ] ---> Bucket Index 1 ---> Value ("555-0142")
+------------------------------------------------------------------------------------+
| Average Time Complexity: O(1) Get | O(1) Put | O(1) Remove ⚡                      |
+------------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Hash Table Operational Contract

### 2.1 The 4 Core Hash Table Operations
1. **`put(K key, V value)`**: Computes $h(\text{key})$, resolves collisions if necessary, and stores the key-value pair. Average Time Complexity: **$O(1)$ Constant**.
2. **`get(K key)`**: Computes $h(\text{key})$ and returns the associated value. Returns `null` if key is not found. Average Time Complexity: **$O(1)$ Constant**.
3. **`remove(K key)`**: Computes $h(\text{key})$ and deletes the key-value entry. Average Time Complexity: **$O(1)$ Constant**.
4. **`containsKey(K key)`**: Checks if the key exists in the table. Average Time Complexity: **$O(1)$ Constant**.

```
Hash Table Performance & Complexity Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Intent      | Average Case Time | Worst Case Time   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| `put(key, value)`     | **$O(1)$ Constant ⚡**| $O(N)$ (All collide)| $O(N)$ Table Size |
| `get(key)`            | **$O(1)$ Constant ⚡**| $O(N)$ (All collide)| $O(N)$ Table Size |
| `remove(key)`         | **$O(1)$ Constant ⚡**| $O(N)$ (All collide)| $O(N)$ Table Size |
| `containsKey(key)`    | **$O(1)$ Constant ⚡**| $O(N)$ (All collide)| $O(N)$ Table Size |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Hash Tables achieve O(1) average lookup by mapping keys into array indices via hash functions!"**

---

## 3. Characteristics & The 3 Invariants of Effective Hash Tables

### 3.1 The 3 Invariants of Effective Hash Tables
1. **Deterministic Output**: For any key $k$, evaluating $h(k)$ multiple times MUST return the exact same integer hash value throughout the application's lifecycle.
2. **Uniform Distribution (High Entropy)**: The hash function must distribute keys evenly across all array bucket slots, minimizing collision clustering.
3. **Fast Computation**: Evaluating $h(k)$ must take **$O(1)$ constant time**, involving simple bitwise or arithmetic operations.

```
Deterministic & Uniformity Proof:
If key1 == key2 (according to equals()), then hashCode(key1) MUST equal hashCode(key2)!
Violating this contract causes HashMap.get(key) to search the WRONG bucket slot, returning null for existing keys! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Hash Table Insertion and Retrieval:

```
Init: Capacity = 8 (Bucket Array size 8, indices 0..7).

put("John", 95):
  1. Hash Code: "John".hashCode() = 2314521.
  2. Bucket Index: 2314521 % 8 = index 1.
  3. Store Entry("John", 95) at Bucket[1].

put("Mary", 88):
  1. Hash Code: "Mary".hashCode() = 2390112.
  2. Bucket Index: 2390112 % 8 = index 0.
  3. Store Entry("Mary", 88) at Bucket[0].

get("John"):
  1. Hash Code: "John".hashCode() = 2314521.
  2. Index: 2314521 % 8 = index 1.
  3. Inspect Bucket[1] -> Matches key "John"! Returns 95. ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
Associative Key-Value Array Index Bucket Mapping Topography:

```
Keys               Hash Function h(k)           Bucket Array (Indices 0..7)
"Mary"    --->  [ h("Mary") % 8 = 0 ]  --->  [0]: Entry("Mary", 88)
"John"    --->  [ h("John") % 8 = 1 ]  --->  [1]: Entry("John", 95)
                                             [2]: null
"Alex"    --->  [ h("Alex") % 8 = 3 ]  --->  [3]: Entry("Alex", 92)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a basic Fixed-Capacity Chaining Hash Map (`SimpleHashMap`):

```java
import java.util.*;

public class HashTableFundamentalsMaster {

    // Production-Grade Basic Hash Map Implementation (Separate Chaining)
    public static class SimpleHashMap<K, V> {
        private static class Entry<K, V> {
            final K key;
            V value;
            Entry<K, V> next;

            Entry(K key, V value, Entry<K, V> next) {
                this.key = key;
                this.value = value;
                this.next = next;
            }
        }

        private Entry<K, V>[] buckets;
        private int capacity;
        private int size;

        @SuppressWarnings("unchecked")
        public SimpleHashMap(int capacity) {
            this.capacity = capacity;
            this.buckets = new Entry[capacity];
            this.size = 0;
        }

        // O(1) Average Put Operation
        public void put(K key, V value) {
            if (key == null) return;

            int index = getBucketIndex(key);
            Entry<K, V> head = buckets[index];

            // Update value if key already exists
            while (head != null) {
                if (head.key.equals(key)) {
                    head.value = value;
                    return;
                }
                head = head.next;
            }

            // Insert new entry at head of chain (O(1) prepending)
            Entry<K, V> newEntry = new Entry<>(key, value, buckets[index]);
            buckets[index] = newEntry;
            size++;
        }

        // O(1) Average Get Operation
        public V get(K key) {
            if (key == null) return null;

            int index = getBucketIndex(key);
            Entry<K, V> head = buckets[index];

            while (head != null) {
                if (head.key.equals(key)) {
                    return head.value;
                }
                head = head.next;
            }

            return null; // Key not found
        }

        // O(1) Average Remove Operation
        public boolean remove(K key) {
            if (key == null) return false;

            int index = getBucketIndex(key);
            Entry<K, V> curr = buckets[index];
            Entry<K, V> prev = null;

            while (curr != null) {
                if (curr.key.equals(key)) {
                    if (prev != null) {
                        prev.next = curr.next;
                    } else {
                        buckets[index] = curr.next;
                    }
                    size--;
                    return true;
                }
                prev = curr;
                curr = curr.next;
            }

            return false;
        }

        public boolean containsKey(K key) {
            return get(key) != null;
        }

        public int size() {
            return size;
        }

        private int getBucketIndex(K key) {
            int hashCode = key.hashCode();
            // Spread hash bits and map to positive bucket index
            return Math.abs(hashCode) % capacity;
        }
    }
}
```

> **Quick Syntax:**
```java
// Standard Java HashMap Usage
Map<String, Integer> map = new HashMap<>();
map.put("John", 95);
int score = map.getOrDefault("John", 0);
boolean exists = map.containsKey("John");
```

---

## 7. Concrete Problem Examples
* **Two Sum (LeetCode 1)**: $O(1)$ complement key lookup.
* **Group Anagrams (LeetCode 49)**: Frequency key hash table grouping.
* **Database Indexing & In-Memory Caches (Redis)**: $O(1)$ key-value record storage.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing custom `SimpleHashMap` and `java.util.HashMap`:

```java
public class HashTableFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Custom SimpleHashMap Demonstration ===");
        HashTableFundamentalsMaster.SimpleHashMap<String, Integer> map = 
            new HashTableFundamentalsMaster.SimpleHashMap<>(8);

        map.put("John", 95);
        map.put("Mary", 88);
        map.put("Alex", 92);

        System.out.println("John's Score: " + map.get("John"));   // Output: 95
        System.out.println("Contains Mary? " + map.containsKey("Mary")); // Output: true
        map.remove("Mary");
        System.out.println("Contains Mary after remove? " + map.containsKey("Mary")); // Output: false

        System.out.println("\n=== 2. Standard Java HashMap Demonstration ===");
        Map<String, String> capitalMap = new HashMap<>();
        capitalMap.put("USA", "Washington D.C.");
        capitalMap.put("France", "Paris");
        System.out.println("Capital of France: " + capitalMap.get("France")); // Output: Paris
    }
}
```

---

## 9. Complexity Analysis

| Hash Table Operation | Average Case Time | Worst Case Time | Space Complexity |
| :--- | :--- | :--- | :--- |
| **`put(key, value)`** | **$O(1)$ Constant ⚡** | $O(N)$ (Degenerate Hash) | $O(N)$ Storage Memory |
| **`get(key)`** | **$O(1)$ Constant ⚡** | $O(N)$ (Degenerate Hash) | $O(N)$ Storage Memory |
| **`remove(key)`** | **$O(1)$ Constant ⚡** | $O(N)$ (Degenerate Hash) | $O(N)$ Storage Memory |

---

## 10. Edge Cases & Boundary Handling
* **Null Key Handling**: Standard Java `HashMap` permits 1 `null` key (mapped to bucket 0).
* **Hash Collisions**: Multiple keys producing identical bucket index `getBucketIndex(k)` are chained sequentially.

---

## 11. Common Mistakes & Anti-Patterns
* **Violating `hashCode()` and `equals()` Contract**:
  - Overriding `equals()` without overriding `hashCode()` causes equal objects to produce different hash codes, resulting in `get()` returning `null` for existing keys!
  - **Always override BOTH `equals()` and `hashCode()` together**.
* **Mutating Key Objects After Insertion**:
  - Mutating a key's fields alters its `hashCode()`, placing future `get()` queries in a different bucket and making the entry unreachable (Memory Leak).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The Contract Between `equals()` and `hashCode()`:
> 1. If `a.equals(b) == true`, then `a.hashCode() == b.hashCode()` MUST be `true`!
> 2. If `a.hashCode() == b.hashCode()`, `a.equals(b)` is NOT required to be `true` (Collision case).
> 3. Overriding `equals()` REQUIRES overriding `hashCode()`.

> **Memory Trick:** **"Equal objects MUST have equal hash codes! Unequal hash codes guarantee unequal objects!"**

---

## 13. System & Implementation Comparisons

| Feature | Hash Table (`HashMap`) | Balanced Search Tree (`TreeMap`) |
| :--- | :--- | :--- |
| **Average Time Complexity** | **$O(1)$ Constant ⚡** | $O(\log N)$ Logarithmic |
| **Element Ordering** | Unordered | Sorted Order (Natural / Comparator) |
| **Range Queries** | Unsupported | Supported (`subMap`, `firstKey`) |

---

## 14. How to Recognize This in Questions
* **"Find item in O(1) lookup time"** $\rightarrow$ Hash Table (`HashMap`).
* **"Check set membership or track frequencies"** $\rightarrow$ Hash Set (`HashSet`) / Hash Map.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `HashMap` achieve $O(1)$ average time complexity?**  
  *A:* By converting keys to bucket indices using a hash function, direct array indexing locates the target bucket in $O(1)$ time. If collision chains are short, scanning the bucket takes $O(1)$ time.
* **Q: What happens if all keys produce the exact same `hashCode()`?**  
  *A:* All key-value entries collide in a single bucket chain, degrading `HashMap` operations from $O(1)$ constant time down to **$O(N)$ linear time**.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASH TABLE FUNDAMENTALS                               |
+-----------------------------------------------------------------------+
| • Core Contract: Average O(1) Time for get(), put(), remove() ⚡       |
| • Bucket Index Formula: idx = Math.abs(key.hashCode()) % capacity     |
| • Equals/HashCode Rule: Equal objects MUST have equal hash codes!     |
| • Key Mutability: NEVER mutate key fields after inserting into map!   |
| • Storage Trade-off: Trades array memory to eliminate search latency  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement a basic Chaining Hash Map from scratch.
- [ ] I can state the contract between `equals()` and `hashCode()`.
- [ ] I know why mutating a key object breaks `HashMap.get()`.
- [ ] I can explain why Hash Tables achieve $O(1)$ average time.
- [ ] I know when to choose `HashMap` vs `TreeMap`.
