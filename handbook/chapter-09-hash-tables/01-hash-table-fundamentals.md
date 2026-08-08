# 01. Hash Table Fundamentals, Key-Value Mapping & Direct Addressing

## 1. Introduction
A **Hash Table** (or Hash Map) is an associative data structure that maps keys to values, enabling **Average $O(1)$ constant time complexity** for insertion, deletion, lookup, and search operations. In computer science and technical software engineering interviews, Hash Tables represent the single most versatile data structure. They underpin database indexing engines (MySQL InnoDB Hash Indexes, Redis Key-Value Store), memory caching systems (Memcached), compiler symbol tables, and high-throughput network routing tables.

> **Important:** While a Direct Address Table achieves strict $O(1)$ time by using key values directly as array indices, it requires an array size equal to the size of the key universe $U$. A Hash Table solves this memory explosion by applying a mathematical **Hash Function $h(k)$** to map a massive key universe $U$ down to a compact array slot range $0 \dots m - 1$.

```
Key Mapping Paradigm Evolution:
+-----------------------------------------------------------------------------------+
| Direct Address Table  : Index = Key                  -> Requires Array of Size |U||
| Compact Hash Table    : Index = h(Key) mod m         -> Requires Array of Size m |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts
### 2.1 The Key-Value Associative Abstraction
A Hash Table models an abstract dictionary storing unique Key-Value pairs $(K, V)$. The key $K$ serves as an immutable lookup identifier, while value $V$ stores the associated data payload.

### 2.2 Direct Addressing vs Hashing
If the universe of keys $U$ is small (e.g. $U = \{0, 1, \dots, 99\}$), we can allocate a Direct Address Array `V T[100]` where slot `T[k]` directly stores the value for key $k$.
* **Advantage**: Strict $O(1)$ time for `search`, `insert`, and `delete`. Zero collision handling logic required.
* **Disadvantage**: If keys are 64-bit integers ($|U| = 2^{64} \approx 1.84 \times 10^{19}$), allocating a Direct Address Table requires **exabytes of memory**, which is physically impossible.

### 2.3 The Hash Mapping Pipeline
To map a large key universe $|U|$ to a table of size $m$ (where $m \ll |U|$), Hashing executes a two-stage mathematical pipeline:
1. **Hash Code Generation**: Convert an arbitrary key object $K$ into a 32-bit signed integer hash code:
   $$\text{hashCode}(K) \in [-2^{31}, 2^{31}-1]$$
2. **Compression Function**: Map the 32-bit hash code to a valid array index $i \in [0, m - 1]$:
   $$i = \text{compress}(\text{hashCode}(K), m)$$
   In Java's `HashMap`, when table size $m = 2^k$ is a power of two, compression uses bitwise AND:
   $$i = \text{hashCode}(K) \ \& \ (m - 1)$$

### 2.4 Load Factor ($\alpha$)
The **Load Factor ($\alpha$)** measures how densely populated the Hash Table array is:
$$\alpha = \frac{n}{m}$$
where $n$ is the number of stored key-value pairs, and $m$ is the current array capacity.
* In Java's `HashMap`, the default initial capacity is $m = 16$ and the default load factor threshold is $\alpha = 0.75$.
* When $n > m \cdot \alpha$ (i.e. when $n > 12$ for capacity $16$), the table automatically triggers a **Rehash Operation**, doubling table capacity ($m \to 2m$) and redistributing all elements.

> **Memory Trick:** **"Direct Addressing = Index is Key (Needs Huge RAM)! Hashing = Index is h(Key) & (m - 1) (Needs Small RAM)!"**

---

## 3. Characteristics & Mathematical Foundations

### 3.1 The Pigeonhole Principle & Mandatory Collisions
The **Pigeonhole Principle** states that if $n$ items are put into $m$ containers, with $n > m$, then at least one container must contain more than one item.

$$\text{Since } |U| > m, \quad \exists \ k_1, k_2 \in U \ (k_1 \neq k_2) \quad \text{such that} \quad h(k_1) = h(k_2)$$

This mathematical certainty proves that **Hash Collisions are completely unavoidable** for any hash function mapping a larger key space to a smaller table capacity.

### 3.2 The Birthday Paradox & Collision Probability
The **Birthday Paradox** demonstrates how quickly collisions occur even when table capacity seems large. In a room of $N$ people, the probability $P(N)$ that at least two people share the same birthday (out of $D = 365$ possible days) is:

$$P(N) = 1 - \frac{D!}{(D - N)! \cdot D^N} = 1 - \prod_{i=0}^{N-1} \left(1 - \frac{i}{D}\right)$$

Using the Taylor series approximation $e^{-x} \approx 1 - x$:

$$P(N) \approx 1 - \prod_{i=0}^{N-1} e^{-i/D} = 1 - e^{-\sum_{i=0}^{N-1} i / D} = 1 - e^{-\frac{N(N-1)}{2D}}$$

Setting $P(N) = 0.5$ (50% collision probability):

$$e^{-\frac{N^2}{2D}} \approx 0.5 \implies \frac{N^2}{2D} = \ln 2 \approx 0.693 \implies N \approx \sqrt{2 \ln 2 \cdot D} \approx 1.177 \sqrt{D}$$

* **Takeaway**: For a Hash Table of size $m = 1,000,000$, a 50% chance of collision occurs after inserting only $N \approx 1.177 \sqrt{10^6} \approx \mathbf{1,177 \text{ keys}}$! This proves that a Hash Table MUST implement robust Collision Resolution strategies from day one.

```
Pigeonhole Principle vs Birthday Paradox:
+-----------------------+-------------------+-------------------+-------------------+
| Mathematical Rule     | Threshold Key Count| Collision Odds   | Insight           |
+-----------------------+-------------------+-------------------+-------------------+
| Pigeonhole Principle  | N = m + 1         | 100% Guaranteed   | Theoretical Limit |
| Birthday Paradox      | N ≈ 1.177 √m      | 50% Probability   | Real-World Shock! |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Key Insertion, Index Computation, and Retrieval in a Hash Table:

```
[ INPUT KEY ] : String "apple", Value 100
      |
      v
[ STAGE 1: HASH CODE GENERATION ]
"apple".hashCode() -> 93029210 (32-bit Signed Integer)
      |
      v
[ STAGE 2: HASH SPREADING / MIXING ]
hash = h ^ (h >>> 16) -> Spreads higher bits down to lower bits
      |
      v
[ STAGE 3: INDEX COMPRESSION ]
tableSize m = 16 (m - 1 = 15 = 0x0F)
index = hash & 15 -> Index 10
      |
      v
[ STAGE 4: BUCKET SLOTS ACCESS ]
Array[10] -> Stores Node("apple", 100, next=null)
```

```
Step-by-Step Retrieval Trace for "apple":
1. Compute hashCode("apple") -> 93029210.
2. Mix hash: hash = h ^ (h >>> 16).
3. Compute Index: index = hash & (16 - 1) = 10.
4. Access Array[10].
5. Traversal Bucket Chain: Compare key.equals("apple"). Matches! Return Value 100 in O(1) time.
```

---

## 5. Visual Diagram
Direct Addressing vs Hash Function Index Compression Layout:

```
[ DIRECT ADDRESS TABLE ] (Huge Memory Leak)
Key 0     ---> Slot 0
Key 1000  ---> Slot 1000
Key 99999 ---> Slot 99999  (Allocates 100,000 array elements for 3 keys!)


[ HASH TABLE WITH COMPRESSION ] (Memory Efficient)
Key "Alice" ---> hashCode()=78129  ---\
Key "Bob"   ---> hashCode()=81920   -----> [ Compression: h & (m - 1) ]
Key "Carl"  ---> hashCode()=19283  ---/
                                               |
                                               v
                                    Array Capacity m = 4
                                    +--------------------+
                                    | Slot 0: "Bob"      |
                                    | Slot 1: "Alice"    |
                                    | Slot 2: Empty      |
                                    | Slot 3: "Carl"     |
                                    +--------------------+
```

---

## 6. Operations & Core Algorithms
Implementation of a Custom Direct Address Table vs Elementary Separated-Chain Hash Table:

```java
// 1. Direct Address Table for Small Universe U = 0..999
public class DirectAddressTable {
    private final Integer[] table;

    public DirectAddressTable(int universeSize) {
        this.table = new Integer[universeSize];
    }

    public void insert(int key, int value) {
        table[key] = value; // Strict O(1)
    }

    public Integer search(int key) {
        return table[key]; // Strict O(1)
    }

    public void delete(int key) {
        table[key] = null; // Strict O(1)
    }
}
```

```java
// 2. Custom Fundamental Hash Table (Chaining with Simple Linked Lists)
public class SimpleHashTable<K, V> {
    
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

    private Entry<K, V>[] table;
    private int capacity;
    private int size;
    private static final float LOAD_FACTOR = 0.75f;

    @SuppressWarnings("unchecked")
    public SimpleHashTable(int initialCapacity) {
        this.capacity = initialCapacity;
        this.table = (Entry<K, V>[]) new Entry[capacity];
        this.size = 0;
    }

    private int getIndex(K key) {
        if (key == null) return 0;
        int h = key.hashCode();
        // Bitwise XOR mixing (Supplemental Hash Function)
        h = h ^ (h >>> 16);
        return h & (capacity - 1);
    }

    public void put(K key, V value) {
        int index = getIndex(key);
        Entry<K, V> head = table[index];

        // Check if key already exists in bucket chain
        Entry<K, V> curr = head;
        while (curr != null) {
            if ((curr.key == null && key == null) || (curr.key != null && curr.key.equals(key))) {
                curr.value = value; // Update value
                return;
            }
            curr = curr.next;
        }

        // Insert new entry at head of bucket chain
        Entry<K, V> newEntry = new Entry<>(key, value, head);
        table[index] = newEntry;
        size++;

        // Trigger resize if load factor threshold exceeded
        if ((float) size / capacity >= LOAD_FACTOR) {
            resize();
        }
    }

    public V get(K key) {
        int index = getIndex(key);
        Entry<K, V> curr = table[index];

        while (curr != null) {
            if ((curr.key == null && key == null) || (curr.key != null && curr.key.equals(key))) {
                return curr.value;
            }
            curr = curr.next;
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    private void resize() {
        int oldCapacity = capacity;
        Entry<K, V>[] oldTable = table;

        capacity = oldCapacity * 2;
        table = (Entry<K, V>[]) new Entry[capacity];
        size = 0;

        for (int i = 0; i < oldCapacity; i++) {
            Entry<K, V> curr = oldTable[i];
            while (curr != null) {
                put(curr.key, curr.value);
                curr = curr.next;
            }
        }
    }

    public int size() { return size; }
}
```

> **Quick Syntax:**
```java
// Fast Index Compression Trick for Power-of-Two Table Capacity
int index = (hashCode ^ (hashCode >>> 16)) & (capacity - 1);
```

---

## 7. Concrete Problem Examples
* **LeetCode 1 - Two Sum**: Storing visited numbers into a Hash Map to find complement values in $O(N)$ linear time.
* **LeetCode 217 - Contains Duplicate**: Storing visited keys into a Hash Set to detect duplicates in $O(N)$ time.
* **LeetCode 146 - LRU Cache**: Combining a Hash Map for $O(1)$ key lookups with a Doubly Linked List for $O(1)$ recency ordering.

---

## 8. Java Code Demonstration & Dry Run
Complete interview-ready demonstration comparing Direct Addressing vs Hashing performance and collision distribution:

```java
import java.util.HashMap;
import java.util.Map;

public class HashTableFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Direct Address Table ===");
        DirectAddressTable directTable = new DirectAddressTable(100);
        directTable.insert(42, 9999);
        System.out.println("Direct Lookup Key 42: " + directTable.search(42));

        System.out.println("\n=== 2. Testing Custom Hash Table ===");
        SimpleHashTable<String, Integer> studentGrades = new SimpleHashTable<>(8);
        studentGrades.put("Alice", 95);
        studentGrades.put("Bob", 87);
        studentGrades.put("Charlie", 92);
        studentGrades.put("David", 78);

        System.out.println("Alice Grade: " + studentGrades.get("Alice"));
        System.out.println("Bob Grade:   " + studentGrades.get("Bob"));

        // Overwrite existing key
        studentGrades.put("Alice", 98);
        System.out.println("Alice Updated Grade: " + studentGrades.get("Alice"));

        System.out.println("\n=== 3. Birthday Paradox Simulation ===");
        simulateBirthdayParadox(365, 10000);
    }

    // Birthday Paradox Simulation
    private static void simulateBirthdayParadox(int daysInYear, int trials) {
        int collisionCount = 0;
        int people = 23; // 23 people give ~50.7% chance of birthday collision!

        for (int t = 0; t < trials; t++) {
            boolean[] birthdays = new boolean[daysInYear];
            boolean hasCollision = false;
            for (int p = 0; p < people; p++) {
                int day = (int) (Math.random() * daysInYear);
                if (birthdays[day]) {
                    hasCollision = true;
                    break;
                }
                birthdays[day] = true;
            }
            if (hasCollision) collisionCount++;
        }

        double probability = (double) collisionCount / trials * 100;
        System.out.println("Simulation with " + people + " people over " + trials + " trials:");
        System.out.println("Empirical Collision Probability: " + String.format("%.2f", probability) + "% (Expected ~50.7%)");
    }
}
```

---

## 9. Complexity Analysis

| Operation / Feature | Direct Address Table | Hash Table (Average Case) | Hash Table (Worst Case - All Collide) |
| :--- | :--- | :--- | :--- |
| **Search / `get(k)`** | **Strict $O(1)$** | **Average $O(1)$ ⚡** | $O(N)$ (Linear Bucket Scan) |
| **Insertion / `put(k, v)`**| **Strict $O(1)$** | **Amortized $O(1)$ ⚡**| $O(N)$ (Resize or Long Bucket) |
| **Deletion / `remove(k)`** | **Strict $O(1)$** | **Average $O(1)$ ⚡** | $O(N)$ (Linear Bucket Scan) |
| **Space Complexity** | $O(|U|)$ (Huge Space!) | **$O(N + m)$ (Compact)**| $O(N + m)$ |

### Why Worst Case is $O(N)$
If an adversary crafted $N$ distinct keys that all produce the exact same bucket index (e.g. `hashCode() % m == 3`), all $N$ elements end up in a single linked list bucket chain. Searching for a key requires traversing $N$ nodes $\implies \mathbf{O(N)\text{ Worst Case}}$.
* Java 8+ mitigates this attack by automatically converting long linked list buckets ($\ge 8$ nodes) into **Red-Black Balanced BSTs**, improving worst-case search time from $O(N)$ to **$O(\log N)$**!

---

## 10. Edge Cases & Boundary Handling
* **Null Keys**: Java `HashMap` permits a single `null` key, which is forcibly assigned to bucket index `0`.
* **Mutable Objects as Keys**: If an object's fields are modified AFTER inserting it into a Hash Map, its `hashCode()` changes! Subsequent lookups compute a different bucket index, making the object **permanently lost** inside the map.
* **Negative Hash Codes**: In Java, `hashCode()` can return negative integers (e.g. `-2147483648`). Simply taking `hash % capacity` yields a negative index! Use `(hash & 0x7FFFFFFF) % capacity` or Java's power-of-two mask `hash & (capacity - 1)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Overriding `equals()` without Overriding `hashCode()`**: Violates Java's contract! Two equal objects (`a.equals(b) == true`) MUST return identical hash codes (`a.hashCode() == b.hashCode()`). Otherwise, equal objects end up in different buckets, breaking map lookups.
* **Modifying Key Objects In-Place**: Mutating fields used in `hashCode()` after key insertion.
* **Using Modulo `%` with Non-Power-of-Two Capacities and Bad Hash Codes**: Leads to severe bucket clustering.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Java's Contract for `equals()` and `hashCode()`:
> 1. If `a.equals(b) == true`, then **`a.hashCode() == b.hashCode()` MUST be true**.
> 2. If `a.hashCode() == b.hashCode()` is true, `a.equals(b)` **is NOT required to be true** (Hash Collision!).
> 3. Always use **immutable objects** (e.g. `String`, `Integer`, custom `record` / `final` class) as Hash Map keys!

> **Memory Trick:** **"Equal objects MUST have equal hash codes! Equal hash codes MAY collide!"**

---

## 13. System & Implementation Comparisons

| Metric | Direct Addressing | Separate Chaining (Java HashMap) | Open Addressing (Linear Probing) |
| :--- | :--- | :--- | :--- |
| **Array Capacity Required**| Universe size $|U|$ | Bounded capacity $m \approx N$ | Bounded capacity $m > N$ |
| **Collision Resolution** | N/A (Impossible) | External Linked Lists / Trees | Probing internal open array slots |
| **Cache Locality** | High | Low (Node pointer dereferencing)| **High (Contiguous array scan)** |
| **Load Factor Tolerance** | N/A | Can exceed $\alpha > 1.0$ | Strict bound $\alpha < 1.0$ (Max 0.7) |

---

## 14. How to Recognize This in Questions
* **"Find two elements in an array that sum to Target in O(N) time"** $\rightarrow$ Store visited numbers in a Hash Map (`val -> index`).
* **"Check if two strings are anagrams in O(N) time"** $\rightarrow$ Character Frequency Hash Table (`int[26]`).
* **"Find longest consecutive sequence of numbers in O(N) time"** $\rightarrow$ Store array numbers in a Hash Set for $O(1)$ lookup.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java's `HashMap` require capacity $m$ to be a power of two ($2^k$)?**  
  *A:* When $m = 2^k$, index compression `hash % m` is mathematically equivalent to the bitwise AND operation `hash & (m - 1)`. Bitwise AND executes in a single CPU clock cycle, whereas integer division `%` takes ~15–30 CPU cycles!
* **Q: What happens if two distinct keys return the same hash code?**  
  *A:* A **Hash Collision** occurs. Both key-value pairs are stored in the same bucket slot using a collision resolution technique (such as Separate Chaining in Java `HashMap`). When searching for a key, the hash table computes the bucket index, then traverses the bucket list comparing key equality via `.equals()`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASH TABLE FUNDAMENTALS & KEY MAPPING                 |
+-----------------------------------------------------------------------+
| • Direct Addressing: Index = Key (Strict O(1), requires huge RAM)     |
| • Hashing Pipeline: Key -> hashCode() [32-bit int] -> Index & (m - 1) |
| • Compression Formula: index = (h ^ (h >>> 16)) & (capacity - 1)      |
| • Pigeonhole & Birthday Paradox: Collisions are 100% mathematically   |
|   guaranteed! (50% collision odds with just ~1,177 keys for m=1,000,000)|
| • Java Load Factor: Default capacity = 16, load factor = 0.75         |
| • Equals & HashCode Rule: Equal objects MUST have equal hash codes!   |
| • Worst Case Complexity: O(N) linear if all keys collide into 1 chain |
| • Java 8+ Optimization: Converts bucket chain to Red-Black Tree >= 8  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can explain the difference between Direct Addressing and Hashing.
- [ ] I can derive why collisions are inevitable using the Pigeonhole Principle.
- [ ] I know why $P(\text{collision}) \approx 50\%$ occurs at $N \approx 1.177 \sqrt{m}$ (Birthday Paradox).
- [ ] I can write `(h ^ (h >>> 16)) & (capacity - 1)` index compression code.
- [ ] I know Java's mandatory contract between `equals()` and `hashCode()`.
- [ ] I know why mutable objects make dangerous Hash Map keys.
- [ ] I can implement a basic Separate-Chaining Hash Table from scratch in Java.
