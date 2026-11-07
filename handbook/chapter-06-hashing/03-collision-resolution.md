# 03. Collision Resolution Taxonomy, Pigeonhole Principle & Cuckoo Hashing Mechanics

## 1. Introduction
A **Hash Collision** occurs when two distinct keys $k_1 \ne k_2$ evaluate to the exact same array bucket index ($h(k_1) \bmod M = h(k_2) \bmod M$). By the **Pigeonhole Principle**, because the universe of potential keys (e.g. all possible 64-character strings) vastly exceeds the finite number of array bucket slots $M$, collisions are mathematically UNAVOIDABLE. Collision resolution strategies—specifically **Separate Chaining**, **Open Addressing**, **Robin Hood Hashing**, and **Cuckoo Hashing**—guarantee correct retrieval in **$O(1)$ Average Constant Time**.

> **Important:** The choice of Collision Resolution Strategy dictates a Hash Table's **CPU Cache Locality**, **Memory Footprint**, and **Worst-Case Search Bounds**:
> * **Separate Chaining**: Stores colliding keys in an external linked list or Red-Black tree per bucket. Easy to implement, but suffers from cache misses.
> * **Open Addressing**: Stores ALL entries directly inside the primary bucket array. Excellent CPU cache locality, but susceptible to clustering.

```
Collision Resolution Strategy Taxonomy:
+-----------------------------------------------------------------------------------+
| 1. Separate Chaining (External Storage) : Buckets point to Linked Lists / Trees   |
| 2. Open Addressing   (Internal Probe)   : Probes alternative array slots          |
| 3. Robin Hood Hashing (Variance Minimization): Rich keys yield to poor keys       |
| 4. Cuckoo Hashing    (Worst-case O(1))  : 2 Hash Tables; kicks existing items   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Cuckoo Hashing Mechanics

### 2.1 Cuckoo Hashing ($O(1)$ Guaranteed Worst-Case Retrieval)
**Cuckoo Hashing** provides **$O(1)$ Guaranteed Worst-Case Retrieval** by employing 2 independent hash functions ($h_1(k)$ and $h_2(k)$) and 2 bucket tables ($T_1$ and $T_2$):
* **Lookup ($O(1)$ Guaranteed)**: Check $T_1[h_1(k)]$ and $T_2[h_2(k)]$. The key is in ONE of these two exact slots! Search takes at most 2 comparisons!
* **Insertion (Cuckoo Displacement)**:
  1. Try placing $k$ in $T_1[h_1(k)]$. If empty, insertion complete!
  2. If $T_1[h_1(k)]$ is occupied by key $x$: **Kick key $x$ out**! Place $k$ in $T_1[h_1(k)]$.
  3. Re-home evicted key $x$ into its alternate location $T_2[h_2(x)]$.
  4. If $T_2[h_2(x)]$ is occupied, repeat displacement recursively until an empty slot is found or a cycle limit is reached (triggering rehashing).

```
Cuckoo Hashing Displacement Topology:
Insert Key K ---> Place in T1[h1(K)] ---> (Occupied by X!)
                                                |
                                    Kick X out! Place K in T1[h1(K)]
                                                |
                                    Move X to alternate slot T2[h2(X)]
```

> **Memory Trick:** **"Cuckoo Hashing uses 2 tables! Search takes AT MOST 2 lookups! Insert kicks existing keys to alternate slots!"**

---

## 3. Characteristics & Robin Hood Hashing Mechanics

### 3.1 Robin Hood Hashing (Minimizing Search Distance Variance)
A variant of Open Addressing linear probing where keys record their **Probe Count / Distance from Initial Bucket (DIB)**:
* **The Robin Hood Invariant ("Take from the rich, give to the poor")**:
  - During insertion, if an incoming key has a **LARGER DIB** than the key currently sitting in the probed slot (meaning the incoming key is "poorer" / further from home), **SWAP THEM**!
  - Continue probing with the displaced "richer" key!
* **Benefit**: Dramatically reduces search variance, maintaining near-constant lookup times across dense tables.

---

## 4. Internal Working Mechanics
Tracing Cuckoo Hashing Insertion with 2 Tables ($T_1, T_2$ of capacity 4):

```
Insert Key A (h1(A)=1, h2(A)=2): T1[1] is empty -> Place A at T1[1].

Insert Key B (h1(B)=1, h2(B)=3):
  - T1[1] is occupied by A!
  - Kick A out! Place B at T1[1].
  - Move A to alternate slot T2[h2(A)] = T2[2].
  - T2[2] is empty -> Insertion complete!

Lookup Key A: Check T1[h1(A)=1] (holds B) -> Check T2[h2(A)=2] (holds A!).
Found in EXACTLY 2 steps! Guaranteed O(1) Worst-Case Search! ✅
```

---

## 5. Visual Diagram
Robin Hood Hashing Displacement & Swap Topography:

```
Probing Index 4:
Incoming Key: "Z" (Probe Distance DIB = 3)  ("Poorer" key)
Existing Key: "Y" (Probe Distance DIB = 1)  ("Richer" key)

Action: SWAP! Place "Z" in Index 4 (DIB = 3).
Continue probing next slot with displaced key "Y" (DIB = 2)!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Cuckoo Hashing with 2 Tables and 2 Hash Functions:

```java
import java.util.*;

public class CollisionResolutionMaster {

    // Production-Grade Cuckoo Hashing Engine (2 Tables, O(1) Guaranteed Lookup)
    public static class CuckooHashTable<K, V> {
        private static class Entry<K, V> {
            K key;
            V value;

            Entry(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }

        private final int capacity;
        private final Entry<K, V>[] table1;
        private final Entry<K, V>[] table2;
        private static final int MAX_DISPLACEMENTS = 50;

        @SuppressWarnings("unchecked")
        public CuckooHashTable(int capacity) {
            this.capacity = capacity;
            this.table1 = new Entry[capacity];
            this.table2 = new Entry[capacity];
        }

        // Guaranteed O(1) Worst-Case Search (At most 2 comparisons!)
        public V get(K key) {
            if (key == null) return null;

            int idx1 = hash1(key);
            if (table1[idx1] != null && table1[idx1].key.equals(key)) {
                return table1[idx1].value;
            }

            int idx2 = hash2(key);
            if (table2[idx2] != null && table2[idx2].key.equals(key)) {
                return table2[idx2].value;
            }

            return null; // Key not in table
        }

        // Cuckoo Displacement Insertion
        public boolean put(K key, V value) {
            if (key == null) return false;
            if (get(key) != null) {
                // Update existing key
                int idx1 = hash1(key);
                if (table1[idx1] != null && table1[idx1].key.equals(key)) {
                    table1[idx1].value = value;
                    return true;
                }
                int idx2 = hash2(key);
                table2[idx2].value = value;
                return true;
            }

            Entry<K, V> curr = new Entry<>(key, value);
            for (int count = 0; count < MAX_DISPLACEMENTS; count++) {
                // Try table 1
                int idx1 = hash1(curr.key);
                if (table1[idx1] == null) {
                    table1[idx1] = curr;
                    return true;
                }

                // Displace table 1 entry
                Entry<K, V> temp = table1[idx1];
                table1[idx1] = curr;
                curr = temp;

                // Try table 2 for displaced entry
                int idx2 = hash2(curr.key);
                if (table2[idx2] == null) {
                    table2[idx2] = curr;
                    return true;
                }

                // Displace table 2 entry
                temp = table2[idx2];
                table2[idx2] = curr;
                curr = temp;
            }

            // Cycle detected! In production, trigger rehashing here.
            return false;
        }

        private int hash1(K key) {
            return Math.abs(key.hashCode()) % capacity;
        }

        private int hash2(K key) {
            return Math.abs(key.hashCode() * 31 + 17) % capacity;
        }
    }
}
```

> **Quick Syntax:**
```java
// Cuckoo Guaranteed O(1) Search Check
int idx1 = hash1(key);
if (t1[idx1] != null && t1[idx1].key.equals(key)) return t1[idx1].val;
int idx2 = hash2(key);
if (t2[idx2] != null && t2[idx2].key.equals(key)) return t2[idx2].val;
```

---

## 7. Concrete Problem Examples
* **Hardware Network Routers (IP Route Lookup)**: Cuckoo Hashing ($O(1)$ worst-case packet routing).
* **High-Performance Memory Allocators**: Robin Hood Hashing (low variance probing).

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `CuckooHashTable`:

```java
public class CollisionResolutionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Cuckoo Hashing Demonstration (O(1) Worst-Case Search) ===");
        CollisionResolutionMaster.CuckooHashTable<String, Integer> cuckoo = 
            new CollisionResolutionMaster.CuckooHashTable<>(8);

        cuckoo.put("Alpha", 100);
        cuckoo.put("Beta", 200);
        cuckoo.put("Gamma", 300); // Displaces existing keys if collision occurs!

        System.out.println("Get Alpha: " + cuckoo.get("Alpha")); // Output: 100
        System.out.println("Get Beta:  " + cuckoo.get("Beta"));  // Output: 200
        System.out.println("Get Delta (Non-existent): " + cuckoo.get("Delta")); // Output: null
    }
}
```

---

## 9. Complexity Analysis

| Collision Resolution Strategy | Search Average | Search Worst-Case | CPU Cache Locality |
| :--- | :--- | :--- | :--- |
| **Separate Chaining** | **$O(1)$ Constant ⚡** | $O(N)$ (Tree: $O(\log N)$) | Poor (Pointer Chasing) |
| **Linear Probing** | **$O(1)$ Constant ⚡** | $O(N)$ (Primary Clusters)| **Excellent ⚡** |
| **Robin Hood Hashing** | **$O(1)$ Constant ⚡** | $O(\log N)$ Low Variance | **Excellent ⚡** |
| **Cuckoo Hashing** | **$O(1)$ Constant ⚡** | **$O(1)$ Guaranteed ⚡** | Moderate (2 Table Lookups)|

---

## 10. Edge Cases & Boundary Handling
* **Infinite Loops in Cuckoo Displacement**: Solved by setting `MAX_DISPLACEMENTS` threshold to trigger table rehashing on cycle detection.
* **High Load Factor in Open Addressing**: Degrades performance severely when load factor $\alpha > 0.7$; requires immediate rehashing.

---

## 11. Common Mistakes & Anti-Patterns
* **Assuming Hash Tables Have $O(1)$ Worst-Case Lookup**:
  - Standard Separate Chaining and Linear Probing degrade to $O(N)$ worst-case under malicious hash collision attacks!
  - **Only Cuckoo Hashing guarantees $O(1)$ worst-case search**.
* **Ignoring Primary Clustering in Linear Probing**:
  - Contiguous collision blocks grow exponentially if hash functions are poorly distributed.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Cuckoo Hashing Guarantees $O(1)$ Worst-Case Search:
> A key $K$ can ONLY reside in 2 exact locations: Table 1 at `h1(K)` or Table 2 at `h2(K)`.
> Searching requires at most 2 memory reads, guaranteeing $O(1)$ worst-case execution time regardless of table contents!

> **Memory Trick:** **"Cuckoo Hashing = At most 2 lookups for ANY key guaranteed!"**

---

## 13. System & Implementation Comparisons

| Feature | Separate Chaining | Cuckoo Hashing |
| :--- | :--- | :--- |
| **Worst-Case Search** | $O(N)$ (or $O(\log N)$ with Trees) | **$O(1)$ Guaranteed ⚡** |
| **Insertion Complexity**| $O(1)$ Prepending | $O(1)$ Amortized (Displacement) |
| **Implementation Complexity**| Low | Medium |

---

## 14. How to Recognize This in Questions
* **"Design a hash table with guaranteed O(1) worst-case search time"** $\rightarrow$ Cuckoo Hashing.
* **"Minimize search distance variance across probed slots"** $\rightarrow$ Robin Hood Hashing.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Pigeonhole Principle in Hashing?**  
  *A:* If $N$ items are placed into $M$ containers where $N > M$, at least one container MUST contain more than 1 item. Since key spaces are infinite and array buckets $M$ are finite, collisions are mathematically inevitable.
* **Q: What is Robin Hood Hashing's swap rule?**  
  *A:* During linear probing, if a probing key's Distance from Initial Bucket (DIB) is GREATER than the DIB of the key residing in the current slot, the keys are swapped, giving priority to the "poorer" (further displaced) key.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: COLLISION RESOLUTION TAXONOMY                         |
+-----------------------------------------------------------------------+
| • Pigeonhole Principle: Collisions are mathematically inevitable!     |
| • Cuckoo Hashing: 2 Tables, 2 Hash Functions -> Guaranteed O(1) Search|
| • Cuckoo Insert: Kicks existing keys to alternate slots recursively   |
| • Robin Hood Hashing: Swap key if incoming DIB > existing DIB         |
| • Performance Choice: Open Addressing wins cache; Chaining handles high load|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a Cuckoo Hash Table from scratch with 2 tables.
- [ ] I know why Cuckoo Hashing guarantees $O(1)$ worst-case search.
- [ ] I can explain the Robin Hood Hashing swap rule.
- [ ] I can state the Pigeonhole Principle.
- [ ] I know how to detect cycles during Cuckoo displacement.
