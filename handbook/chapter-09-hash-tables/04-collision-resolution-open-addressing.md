# 04. Collision Resolution via Open Addressing (Linear, Quadratic & Double Hashing)

## 1. Introduction
**Open Addressing** is a collision resolution strategy where all key-value entries are stored directly inside the main Hash Table array itself without external linked lists or nodes. When a collision occurs at bucket index $h(k)$, Open Addressing systematically probes a sequence of alternative slots within the array until an empty slot is found. In technical coding interviews and high-performance systems engineering (Python's `dict`, C++ `std::unordered_map` implementations like Google's Abseil `flat_hash_map`, Linux kernel hash tables), Open Addressing achieves superior CPU L1/L2 cache locality by eliminating pointer dereferencing.

> **Important:** In Open Addressing, the Load Factor $\alpha = n / m$ CANNOT exceed 1.0 ($\alpha < 1.0$). If $\alpha \to 1.0$, probing performance degrades severely! Resizing MUST be triggered at $\alpha \approx 0.5 \dots 0.7$.

```
Open Addressing Probing Sequence Spectrum:
+-----------------------------------------------------------------------------------+
| Linear Probing    : h(k, i) = (h'(k) + i) mod m           -> Primary Clustering   |
| Quadratic Probing : h(k, i) = (h'(k) + c1*i + c2*i²) mod m -> Secondary Clustering |
| Double Hashing    : h(k, i) = (h1(k) + i * h2(k)) mod m   -> Optimal Uniform Probe|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Probing Projections

### 2.1 Probing Sequence Formulation
A probe sequence $\langle h(k, 0), h(k, 1), \dots, h(k, m-1) \rangle$ is a permutation of the array indices $\{0, 1, \dots, m-1\}$ for a key $k$, where $i$ represents the probe attempt number ($i = 0, 1, 2 \dots$).

### 2.2 Linear Probing
Linear Probing uses a linear function of the probe number $i$:

$$h(k, i) = (h'(k) + i) \pmod m$$

* **Mechanism**: If index $h'(k)$ is occupied, check $h'(k) + 1$, then $h'(k) + 2$, then $h'(k) + 3$, wrapping around modulo $m$.
* **Advantage**: **Maximum CPU L1/L2 Cache Locality**! Scanning adjacent array memory slots pre-fetches contiguous cache lines.
* **Flaw (Primary Clustering)**: Long contiguous blocks of occupied slots build up over time. Any key that hashes into a cluster increases the cluster size, making future insertions even longer $\implies$ **Primary Clustering Phenomenon**.

### 2.3 Quadratic Probing
Quadratic Probing uses a quadratic polynomial of the probe number $i$:

$$h(k, i) = (h'(k) + c_1 \cdot i + c_2 \cdot i^2) \pmod m$$

where $c_1, c_2 \neq 0$ are auxiliary constants.
* **Advantage**: Eliminates Primary Clustering by stepping quadratically ($+1, +4, +9, +16 \dots$).
* **Flaw (Secondary Clustering)**: If two keys have the same initial hash $h'(k_1) = h'(k_2)$, they trace the **exact same probe sequence** $\implies$ **Secondary Clustering**.
* **Full Table Coverage Guard**: To guarantee probing visits all $m$ slots, capacity $m$ must be prime and $c_1 = c_2 = 0.5$, or $m = 2^p$ with $c_1 = c_2 = 0.5$.

### 2.4 Double Hashing
Double Hashing applies two independent auxiliary hash functions $h_1(k)$ and $h_2(k)$:

$$h(k, i) = (h_1(k) + i \cdot h_2(k)) \pmod m$$

* **Mechanism**: $h_1(k)$ determines the initial slot index, while $h_2(k)$ determines the probe step size!
* **Constraint**: $h_2(k)$ must be **relatively prime to $m$** for all keys $k$ so the probe sequence visits every slot in the table.
  * Easy setup: Set $m = 2^p$ and force $h_2(k)$ to always return an **odd integer**.
  * Alternative setup: Set $m$ as a prime number and set $h_2(k) = 1 + (k \pmod{m - 1})$.
* **Advantage**: **Eliminates both Primary and Secondary Clustering**! Provides $m^2$ distinct probe sequences, closest approximation to Uniform Hashing.

### 2.5 Expected Probe Count Analysis
Under Uniform Hashing with Load Factor $\alpha = n / m < 1$:

* **Unsuccessful Search / Insertion Expected Probes**:
  $$E[\text{probes}] = \frac{1}{1 - \alpha}$$
* **Successful Search Expected Probes**:
  $$E[\text{probes}] = \frac{1}{\alpha} \ln \left(\frac{1}{1 - \alpha}\right)$$

```
Expected Probes vs Load Factor (α):
+-----------------------+-------------------+-------------------+-------------------+
| Load Factor α         | Unsuccessful (1/(1-α))| Successful ((1/α) ln(1/(1-α))) | Impact |
+-----------------------+-------------------+-------------------+-------------------+
| α = 0.50 (50% Full)   | 2.00 Probes       | 1.39 Probes       | Ultra Fast ⚡     |
| α = 0.75 (75% Full)   | 4.00 Probes       | 1.85 Probes       | Good Threshold    |
| α = 0.90 (90% Full)   | 10.00 Probes      | 2.56 Probes       | Severe Degradation|
| α = 0.99 (99% Full)   | 100.00 Probes     | 4.65 Probes       | Complete Collapse |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Linear = +i (Cache Fast, Primary Cluster)! Quadratic = +i² (No Primary Cluster)! Double Hashing = +i*h2(k) (Optimal)!"**

---

## 3. Tombstone Deletion Mechanics (`DELETED` Marker)

In Open Addressing, simply setting a deleted slot to `null` **corrupts future search probes**!
If Key A probes through slot $S$ to reach slot $S+1$, deleting Key at slot $S$ by setting `table[S] = null` causes a search for Key A to stop at slot $S$, incorrectly reporting Key A as missing!

### The Tombstone Protocol (`TOMBSTONE`)
1. **Deletion**: Replace deleted entry with a special sentinel object: **`DELETED` / Tombstone**.
2. **Search**: Continue probing through `DELETED` slots; stop ONLY when an actual `null` slot is encountered.
3. **Insertion**: Can overwrite a `DELETED` slot when inserting a new key!
4. **Rehash Garbage Collection**: During dynamic table resizing, all `DELETED` tombstones are purged, reclaiming table slots.

```
Tombstone Deletion Lifecycle:
[ Slot 1: Key A ] -> [ Slot 2: Key B ] -> [ Slot 3: Key C ]
Action: Delete Key B

INCORRECT: [ Slot 1: Key A ] -> [ Slot 2: null ] -> [ Slot 3: Key C ]  (Search Key C STOPS at Slot 2 -> BUG!)
CORRECT  : [ Slot 1: Key A ] -> [ Slot 2: TOMBSTONE ] -> [ Slot 3: Key C ] (Search Key C PASSES Slot 2!)
```

---

## 4. Internal Working Mechanics
Tracing Double Hashing Insertion & Tombstone Overwriting:

```
Table Capacity m = 7 (Prime), h1(k) = k % 7, h2(k) = 1 + (k % 5)

Insert Key 14: h1(14) = 0. Slot 0 empty -> Place 14 at Slot 0.
Insert Key 21: h1(21) = 0 (Collision!). h2(21) = 1 + (21 % 5) = 2.
               Probe 1: (0 + 1 * 2) % 7 = Slot 2. Slot 2 empty -> Place 21 at Slot 2.

Delete Key 14: Mark Slot 0 as TOMBSTONE.

Search Key 21:
- Check Slot 0: TOMBSTONE (Not null!). Continue probing!
- Probe 1 (Slot 2): Key 21 matches! Found in 2 probes. ✅

Insert Key 35: h1(35) = 0. Slot 0 is TOMBSTONE -> Can overwrite Slot 0! Place 35 at Slot 0. ✅
```

---

## 5. Visual Diagram
Linear Probing Primary Clustering vs Double Hashing Distribution:

```
[ LINEAR PROBING PRIMARY CLUSTERING ]
+---+---+---+---+---+---+---+---+---+
| X | X | X | X | X |   |   |   |   |  <- Massive contiguous cluster!
+---+---+---+---+---+---+---+---+---+
  0   1   2   3   4   5   6   7   8
Any key hashing to 0, 1, 2, 3, or 4 MUST probe all the way to slot 5!


[ DOUBLE HASHING UNIFORM PROBING ]
Key A (step 2): Slot 0 -> Slot 2 -> Slot 4 -> Slot 6
Key B (step 3): Slot 0 -> Slot 3 -> Slot 6 -> Slot 2
Keys with identical h1(k) take completely different step sizes, avoiding clusters!
```

---

## 6. Operations & Complete Java Implementation
Production-grade implementation of an Open Addressing Hash Table supporting Linear Probing, Double Hashing, and Tombstone Deletion:

```java
import java.util.Objects;

public class OpenAddressingHashTable<K, V> {

    // Sentinel Tombstone Object to mark deleted slots
    @SuppressWarnings("rawtypes")
    private static final Entry TOMBSTONE = new Entry<>(null, null);

    private static class Entry<K, V> {
        K key;
        V value;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }

    public enum ProbeType { LINEAR, DOUBLE_HASHING }

    private Entry<K, V>[] table;
    private int capacity;
    private int size;
    private int tombstoneCount;
    private final ProbeType probeType;
    private static final float DEFAULT_MAX_LOAD_FACTOR = 0.60f;

    @SuppressWarnings("unchecked")
    public OpenAddressingHashTable(int initialCapacity, ProbeType probeType) {
        this.capacity = getNextPrime(initialCapacity);
        this.table = (Entry<K, V>[]) new Entry[capacity];
        this.size = 0;
        this.tombstoneCount = 0;
        this.probeType = probeType;
    }

    private int h1(K key) {
        if (key == null) return 0;
        return (key.hashCode() & 0x7FFFFFFF) % capacity;
    }

    private int h2(K key) {
        if (key == null) return 1;
        // Primary prime step size helper
        int hash = (key.hashCode() & 0x7FFFFFFF);
        return 1 + (hash % (capacity - 1));
    }

    private int getProbeIndex(K key, int i) {
        if (probeType == ProbeType.LINEAR) {
            return (h1(key) + i) % capacity;
        } else { // DOUBLE_HASHING
            return (int) ((h1(key) + (long) i * h2(key)) % capacity);
        }
    }

    public V get(K key) {
        for (int i = 0; i < capacity; i++) {
            int idx = getProbeIndex(key, i);
            Entry<K, V> entry = table[idx];

            if (entry == null) {
                return null; // Key does not exist
            }

            if (entry != TOMBSTONE && Objects.equals(entry.key, key)) {
                return entry.value; // Key found!
            }
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    public void put(K key, V value) {
        if ((float) (size + tombstoneCount + 1) / capacity >= DEFAULT_MAX_LOAD_FACTOR) {
            resize();
        }

        int firstTombstoneIdx = -1;

        for (int i = 0; i < capacity; i++) {
            int idx = getProbeIndex(key, i);
            Entry<K, V> entry = table[idx];

            if (entry == null) {
                // Insert at first tombstone if encountered, else at empty slot
                int targetIdx = (firstTombstoneIdx != -1) ? firstTombstoneIdx : idx;
                table[targetIdx] = new Entry<>(key, value);
                if (firstTombstoneIdx != -1) tombstoneCount--;
                size++;
                return;
            }

            if (entry == TOMBSTONE) {
                if (firstTombstoneIdx == -1) {
                    firstTombstoneIdx = idx; // Remember first tombstone spot
                }
            } else if (Objects.equals(entry.key, key)) {
                entry.value = value; // Key already exists -> Update value
                return;
            }
        }

        throw new IllegalStateException("Hash Table Full");
    }

    @SuppressWarnings("unchecked")
    public V remove(K key) {
        for (int i = 0; i < capacity; i++) {
            int idx = getProbeIndex(key, i);
            Entry<K, V> entry = table[idx];

            if (entry == null) return null; // Key not found

            if (entry != TOMBSTONE && Objects.equals(entry.key, key)) {
                V oldVal = entry.value;
                table[idx] = (Entry<K, V>) TOMBSTONE; // Replace with TOMBSTONE
                size--;
                tombstoneCount++;
                return oldVal;
            }
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    private void resize() {
        int oldCap = capacity;
        Entry<K, V>[] oldTable = table;

        capacity = getNextPrime(oldCap * 2);
        table = (Entry<K, V>[]) new Entry[capacity];
        size = 0;
        tombstoneCount = 0;

        for (int i = 0; i < oldCap; i++) {
            Entry<K, V> entry = oldTable[i];
            if (entry != null && entry != TOMBSTONE) {
                put(entry.key, entry.value);
            }
        }
    }

    private static int getNextPrime(int n) {
        while (!isPrime(n)) n++;
        return n;
    }

    private static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    public int size() { return size; }
}
```

> **Quick Syntax:**
```java
// Double Hashing Probe Calculation Formula
int probeIdx = (int) ((h1(key) + (long) i * h2(key)) % capacity);
```

---

## 7. Concrete Problem Examples
* **LeetCode 705 - Design HashSet**: Open Addressing Boolean Array implementation.
* **Python `dict` Implementation**: Uses Open Addressing with pseudo-random probing to maximize cache locality.
* **Google Abseil `flat_hash_map`**: Open Addressing with SIMD vector instruction metadata probing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration comparing Linear Probing vs Double Hashing under dense load factors:

```java
public class OpenAddressingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Open Addressing (Linear Probing) ===");
        OpenAddressingHashTable<String, Integer> linearMap = 
            new OpenAddressingHashTable<>(7, OpenAddressingHashTable.ProbeType.LINEAR);

        linearMap.put("Alpha", 100);
        linearMap.put("Beta", 200);
        linearMap.put("Gamma", 300);

        System.out.println("Alpha Val: " + linearMap.get("Alpha"));
        System.out.println("Removing Beta: " + linearMap.remove("Beta"));
        System.out.println("Beta Val after Removal (Tombstone test): " + linearMap.get("Beta"));
        System.out.println("Gamma Val (Passes Tombstone): " + linearMap.get("Gamma"));

        System.out.println("\n=== 2. Testing Double Hashing ===");
        OpenAddressingHashTable<String, Integer> doubleHashMap = 
            new OpenAddressingHashTable<>(7, OpenAddressingHashTable.ProbeType.DOUBLE_HASHING);

        doubleHashMap.put("Apple", 1);
        doubleHashMap.put("Banana", 2);
        doubleHashMap.put("Cherry", 3);

        System.out.println("Cherry Val: " + doubleHashMap.get("Cherry"));
    }
}
```

---

## 9. Complexity Analysis

| Probing Method | Primary Clustering? | Secondary Clustering? | Cache Locality | Expected Probes ($\alpha = 0.5$) |
| :--- | :--- | :--- | :--- | :--- |
| **Linear Probing** | **YES (High)** | YES | **Maximum (L1 Hits ⚡)** | ~2.5 Probes |
| **Quadratic Probing** | NO | YES | Moderate | ~2.0 Probes |
| **Double Hashing** | **NO (Zero)** | **NO (Zero)** | Lower (Scattered) | **~1.39 Probes (Optimal ⚡)** |

---

## 10. Edge Cases & Boundary Handling
* **Infinite Probing Loops**: Occurs if step size $h_2(k)$ shares a common factor with table capacity $m$. Solved by ensuring $m$ is Prime or $h_2(k)$ is always Odd for $m = 2^p$.
* **Tombstone Accumulation**: If many elements are deleted without resizing, table fills with `DELETED` tombstones, causing searches to probe through dead slots. Resizing purges tombstones completely.

---

## 11. Common Mistakes & Anti-Patterns
* Setting deleted slots to `null` instead of `TOMBSTONE` (breaks search chains!).
* Allowing Load Factor $\alpha > 0.75$ (causes probing collapse $1 / (1 - \alpha)$).
* In Double Hashing, allowing $h_2(k) = 0$ (causes infinite loop probing the exact same slot!). Always ensure $h_2(k) \ge 1$.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Tombstones Are Mandatory in Open Addressing:
> Setting a deleted slot to `null` breaks the probing chain for keys inserted AFTER the deleted item.
> Searches stop at the first `null` slot, incorrectly reporting existing keys as missing!
> **Rule**: Replace deleted items with `TOMBSTONE`. Stop probing ONLY on `null`.

> **Memory Trick:** **"Null stops search! Tombstone continues search! Insert overwrites Tombstone!"**

---

## 13. System & Implementation Comparisons

| Metric | Separate Chaining (Java HashMap) | Open Addressing (Double Hashing) |
| :--- | :--- | :--- |
| **Max Load Factor $\alpha$** | $\alpha > 1.0$ allowed (e.g. 1.5) | Strict $\alpha < 0.7$ (Max 0.75) |
| **Memory Pointer Overhead**| Extra `Node` pointers per item | **Zero Pointer Overhead (Flat Array) ⚡**|
| **Cache Line Performance**| Low (Node dereferencing) | **High (Flat Array Storage) ⚡** |
| **Deletion Mechanism** | Simple node unlinking | **Requires `TOMBSTONE` markers** |

---

## 14. How to Recognize This in Questions
* **"Design a Hash Table without using external linked lists or node allocations"** $\rightarrow$ Open Addressing (Linear or Double Hashing).
* **"Explain why Python's dict is faster than Java's HashMap for small keys"** $\rightarrow$ Flat array Open Addressing cache locality.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Open Addressing require a lower Load Factor threshold ($\alpha \approx 0.5 \dots 0.6$) than Separate Chaining ($\alpha = 0.75$)?**  
  *A:* Because in Open Addressing, all elements compete for slots in the same array. As $\alpha \to 1$, the expected probes for an unsuccessful search scales as $1 / (1 - \alpha)$. At $\alpha = 0.9$, average probes jump to 10 per search, causing severe performance degradation.
* **Q: How does Double Hashing eliminate Primary and Secondary Clustering?**  
  *A:* $h_1(k)$ determines starting position and $h_2(k)$ determines step size. Two keys colliding at $h_1(k_1) = h_1(k_2)$ will have different $h_2(k_1) \neq h_2(k_2)$ step sizes, causing their probing paths to diverge immediately.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: OPEN ADDRESSING & PROBING MECHANICS                   |
+-----------------------------------------------------------------------+
| • Open Addressing: All elements stored directly in main array         |
| • Linear Probing: h(k, i) = (h1(k) + i) % m -> Max Cache, High Cluster |
| • Quadratic Probing: h(k, i) = (h1(k) + c1*i + c2*i²) % m             |
| • Double Hashing: h(k, i) = (h1(k) + i * h2(k)) % m -> Zero Cluster!   |
| • Tombstone Rule: Setting deleted slot to null breaks searches!       |
|   Use TOMBSTONE marker; search continues; insert overwrites TOMBSTONE.|
| • Load Factor Limit: Must keep α < 0.7 (Expected Probes = 1 / (1 - α))|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can derive the expected probe formula $E[\text{probes}] = \frac{1}{1 - \alpha}$.
- [ ] I can write the Double Hashing probe formula `(h1(k) + i * h2(k)) % m`.
- [ ] I know why `TOMBSTONE` sentinels are mandatory for deletions.
- [ ] I know how Primary and Secondary Clustering differ.
- [ ] I can implement an Open Addressing Hash Table from scratch in Java.
- [ ] I know why $h_2(k)$ must never return 0 in Double Hashing.
