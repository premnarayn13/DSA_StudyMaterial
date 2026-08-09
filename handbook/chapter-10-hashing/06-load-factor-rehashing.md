# 06. Load Factor & Rehashing, High/Low Bit Transfer & Array Doubling Mechanics

## 1. Introduction
The **Load Factor ($\alpha$)** of a Hash Table measures the ratio of stored key-value entries $N$ to total array bucket capacity $M$:

$$\alpha = \frac{N}{M}$$

Maintaining an optimal load factor threshold via **Rehashing** (dynamically allocating a new array of $2\times$ capacity and re-distributing existing entries) prevents search performance degradation. This section explores the mathematics of load factors, why Java defaults to $\alpha = 0.75$, and Java 8's revolutionary **High/Low Bit Transfer Optimization (`(e.hash & oldCap) == 0`)** that eliminates expensive modulo re-computations during rehashing!

> **Important:** In Java 8 `HashMap`, when doubling table capacity ($M \to 2M$), an entry's new index can ONLY stay at its original index **`idx`** OR move to **`idx + oldCap`**!
> Evaluating a single bitwise AND test **`(e.hash & oldCap) == 0`**:
> * If `0`: Entry stays at index `idx` in lower bin.
> * If non-zero: Entry moves to index `idx + oldCap` in higher bin.
> Re-calculating hash codes or modulo operations during rehashing is completely eliminated! ⚡

```
Java 8 High/Low Bin Split Optimization during Rehashing (oldCap = 16):
Test: (e.hash & 16) == 0
+- If True  (0 Bit) ----> Low  Bin: New Index = idx (Unchanged) ⚡
+- If False (16 Bit) ---> High Bin: New Index = idx + 16 (Offset by oldCap) ⚡
```

---

## 2. Core Concepts & The Load Factor Trade-off

### 2.1 The Mathematics of $\alpha = 0.75$ Default Load Factor
The choice of Default Load Factor $\alpha = 0.75$ balances **Time Complexity** and **Space Overhead**:

$$\text{Threshold} = \text{Capacity} \times \text{Load Factor} = M \times \alpha$$

* **If Load Factor is too high ($\alpha = 1.0$)**: Saves heap space, but collision frequency increases sharply, lengthening bucket chains and degrading search time.
* **If Load Factor is too low ($\alpha = 0.5$)**: Reduces collisions, but triggers frequent rehashing resizes and wastes 50% of allocated array space.
* **$\alpha = 0.75$ Golden Ratio**: According to Poisson distribution analysis, $\alpha = 0.75$ offers an optimal trade-off: **near-zero collision clustering with 75% memory efficiency**!

```
Load Factor Performance Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Load Factor $\alpha$  | Average Search    | Memory Utilization| Rehashing Frequency|
+-----------------------+-------------------+-------------------+-------------------+
| $\alpha = 0.50$       | Ultra-Fast        | 50% Wasted Space  | High (Frequent)   |
| **$\alpha = 0.75$**   | **Optimal ⚡**    | **75% Efficient ⚡**| **Optimal ⚡**    |
| $\alpha = 1.00$       | Slow (Collisions) | 100% Full         | Rare              |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Default Load Factor 0.75 strikes the golden balance between O(1) speed and memory utilization!"**

---

## 3. Characteristics & Java 8 High/Low Bit Split Mechanics

### 3.1 Mathematical Proof of High/Low Bit Bin Splitting
When array capacity doubles from $M = 2^k$ to $2M = 2^{k+1}$:
* Old Index Mask: $M - 1 = 2^k - 1$ (Selects lower $k$ bits).
* New Index Mask: $2M - 1 = 2^{k+1} - 1$ (Selects lower $k+1$ bits).
* The new mask includes EXACTLY ONE NEW BIT at position $2^k$ (`oldCap`):

```
Old Cap = 16 (00010000_2). Old Mask = 15 (00001111_2). New Mask = 31 (00011111_2).
If hash bit at position 16 (00010000_2) is 0: New Index == Old Index!
If hash bit at position 16 (00010000_2) is 1: New Index == Old Index + 16!
```

---

## 4. Internal Working Mechanics
Tracing Java 8 Rehashing for Bucket 3 (`oldCap = 16`):

```
Bucket 3 contains entries with hashes: H1 = 3 (00000011_2), H2 = 19 (00010011_2)

Both H1 and H2 mapped to Index 3 in Old Table (hash & 15 = 3).

Rehashing Test: (hash & oldCap) == (hash & 16):
- For H1 (3) : (3 & 16) == 0   -> Goes to Low Head (New Index 3).
- For H2 (19): (19 & 16) == 16 -> Goes to High Head (New Index 3 + 16 = 19).

Bucket 3 splits perfectly into Index 3 and Index 19 in O(N) single-pass without hash re-computation! ✅
```

---

## 5. Visual Diagram
Java 8 High/Low Head and Tail Bin Splitting Topography:

```
Old Bucket[3] List: [ Node H1 (hash 3) ] ---> [ Node H2 (hash 19) ]
                             |                         |
               (3 & 16) == 0 |                         | (19 & 16) != 0
                             v                         v
New Table:               [ Index 3 ]               [ Index 19 ]
                     (Low Head / Tail)         (High Head / Tail)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java simulation implementing Java 8 High/Low Bit Transfer Rehashing Engine:

```java
import java.util.*;

public class LoadFactorRehashingMaster {

    // Java 8 Optimized HashMap Rehashing Engine
    public static class HighLowRehashingHashMap<K, V> {
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
        private int capacity;
        private int size;
        private final float loadFactor;
        private int threshold;

        @SuppressWarnings("unchecked")
        public HighLowRehashingHashMap(int initialCapacity, float loadFactor) {
            this.capacity = getPowerOfTwoCapacity(initialCapacity);
            this.loadFactor = loadFactor;
            this.threshold = (int) (this.capacity * loadFactor);
            this.table = new Node[this.capacity];
            this.size = 0;
        }

        public void put(K key, V value) {
            if (key == null) return;
            int hash = hash(key);
            int idx = (capacity - 1) & hash;

            Node<K, V> head = table[idx];
            while (head != null) {
                if (head.hash == hash && head.key.equals(key)) {
                    head.value = value;
                    return;
                }
                head = head.next;
            }

            table[idx] = new Node<>(hash, key, value, table[idx]);
            size++;

            // Rehash check against threshold
            if (size >= threshold) {
                resize();
            }
        }

        // Java 8 High/Low Bit Transfer Rehashing Engine (Zero Hash Re-computation!)
        @SuppressWarnings("unchecked")
        private void resize() {
            Node<K, V>[] oldTable = table;
            int oldCap = capacity;
            int newCap = oldCap * 2;
            Node<K, V>[] newTable = new Node[newCap];

            for (int j = 0; j < oldCap; j++) {
                Node<K, V> e = oldTable[j];
                if (e != null) {
                    oldTable[j] = null; // Clear old reference

                    if (e.next == null) {
                        // Single node in bin: Direct index placement
                        newTable[e.hash & (newCap - 1)] = e;
                    } else {
                        // Preserve original relative order using Low and High heads/tails!
                        Node<K, V> loHead = null, loTail = null;
                        Node<K, V> hiHead = null, hiTail = null;
                        Node<K, V> next;

                        do {
                            next = e.next;
                            // Test single bit at position oldCap
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

                        // Attach Low Bin to index j
                        if (loTail != null) {
                            loTail.next = null;
                            newTable[j] = loHead;
                        }
                        // Attach High Bin to index j + oldCap
                        if (hiTail != null) {
                            hiTail.next = null;
                            newTable[j + oldCap] = hiHead;
                        }
                    }
                }
            }

            this.table = newTable;
            this.capacity = newCap;
            this.threshold = (int) (newCap * loadFactor);
        }

        private int hash(K key) {
            int h = key.hashCode();
            return h ^ (h >>> 16);
        }

        private int getPowerOfTwoCapacity(int cap) {
            int n = cap - 1;
            n |= n >>> 1; n |= n >>> 2; n |= n >>> 4; n |= n >>> 8; n |= n >>> 16;
            return (n < 0) ? 1 : n + 1;
        }
    }
}
```

> **Quick Syntax:**
```java
// High/Low Bit Split Condition (Java 8 HashMap resize line)
if ((e.hash & oldCap) == 0) {
    // Stays at newTable[j]
} else {
    // Moves to newTable[j + oldCap]
}
```

---

## 7. Concrete Problem Examples
* **Java 8 `java.util.HashMap`**: High/Low bit transfer resizing.
* **High-Concurrency ConcurrentHashMap**: Transfer bin resizing.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `HighLowRehashingHashMap` table expansion:

```java
public class LoadFactorRehashingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. High/Low Bit Transfer Rehashing Test ===");
        // Capacity 4, Load Factor 0.75 -> Threshold = 3
        HighLowRehashingHashMap<Integer, String> map = 
            new HighLowRehashingHashMap<>(4, 0.75f);

        map.put(1, "A");
        map.put(2, "B");
        map.put(3, "C"); // Triggers resize to capacity 8!

        System.out.println("Inserted 3 items into capacity 4 map. Threshold triggered resize to 8!");
        System.out.println("High/Low Bit Split successfully split bins without hash re-computation! ✅");
    }
}
```

---

## 9. Complexity Analysis

| Operation Stage | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Standard Insertion** | **$O(1)$ Average ⚡** | $O(N)$ Storage Memory | Threshold check `size >= threshold` |
| **Rehashing Resize** | **$O(N)$ Linear ⚡** | **$O(2N)$ New Array** | High/low bit split `(hash & oldCap) == 0` |

---

## 10. Edge Cases & Boundary Handling
* **Custom Initial Capacity Not a Power of 2**: Converted to next power of 2 using bit-shifting (`getPowerOfTwoCapacity`).
* **Preserving Relative Node Order (Java 8 Improvement)**: High/Low head/tail pointers preserve original list order, preventing infinite loops during concurrent writes.

---

## 11. Common Mistakes & Anti-Patterns
* **Re-computing `hashCode()` or Modulo During Rehashing**:
  - Re-evaluating `key.hashCode()` or `Math.abs(h) % newCap` during resize incurs heavy CPU overhead.
  - **Use `(e.hash & oldCap) == 0` for 1-bit index determination**.
* **Pre-sizing HashMap Too Small**:
  - Instantiating `new HashMap<>()` default capacity 16 for $1,000,000$ elements triggers 16 resize operations ($O(N)$ reallocations).
  - **Initialize capacity: `initialCapacity = (expectedEntries / 0.75f) + 1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** How to Pre-size a Java HashMap for $N$ Items:
> To store $N$ elements without triggering ANY rehashing resize:
> $$\text{Initial Capacity} = \left\lceil \frac{N}{0.75} \right\rceil + 1$$
> For $N = 1000$: $1000 / 0.75 + 1 = 1334 \implies$ Next power of 2 is **$2048$**!

> **Memory Trick:** **"Always pre-size HashMaps with (expectedItems / 0.75) + 1 to avoid resize overhead!"**

---

## 13. System & Implementation Comparisons

| Feature | Java 7 Rehashing | Java 8 Rehashing |
| :--- | :--- | :--- |
| **Index Calculation** | `e.hash % newCap` (Slower) | **`(e.hash & oldCap) == 0` (Fastest) ⚡** |
| **Node Order** | Reverses Node Order | **Preserves Relative Node Order ⚡** |
| **Concurrency Hazard**| Infinite Loop Hazard | Safe Traversal |

---

## 14. How to Recognize This in Questions
* **"Explain how Java 8 HashMap doubles capacity without recalculating hash codes"** $\rightarrow$ High/Low Bit Transfer (`(e.hash & oldCap) == 0`).
* **"Pre-size a HashMap for N items"** $\rightarrow$ `(N / 0.75f) + 1`.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java 8 HashMap preserve original node ordering during rehashing?**  
  *A:* Java 7 prepended transferred nodes to new bucket heads, reversing list order. Under concurrent writes, head prepending could create circular pointer loops (`nodeA.next = nodeB; nodeB.next = nodeA`), causing infinite CPU loops on `get()`. Java 8's High/Low tail pointers preserve original node order, eliminating this hazard.
* **Q: What is the relationship between `threshold`, `capacity`, and `loadFactor`?**  
  *A:* `threshold = (int)(capacity * loadFactor)`. When `size` reaches `threshold`, capacity doubles.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: LOAD FACTOR & REHASHING MECHANICS                     |
+-----------------------------------------------------------------------+
| • Default Load Factor: 0.75 balances O(1) speed and 75% memory use    |
| • Threshold Formula: threshold = capacity * loadFactor                |
| • High/Low Bit Split: (e.hash & oldCap) == 0 stays at index idx       |
| • High Bin Offset: If (e.hash & oldCap) != 0 moves to idx + oldCap    |
| • Pre-sizing Formula: initialCapacity = (expectedEntries / 0.75f) + 1 |
| • Rehash Complexity: O(N) Linear Time (Zero hash re-computations!) ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Java 8 High/Low bit split rehashing logic from memory.
- [ ] I know why default load factor is 0.75.
- [ ] I can calculate the pre-sized initial capacity for $N$ items.
- [ ] I know how `(e.hash & oldCap) == 0` determines new bucket index.
- [ ] I can explain why Java 8 preserves relative node order during resize.
