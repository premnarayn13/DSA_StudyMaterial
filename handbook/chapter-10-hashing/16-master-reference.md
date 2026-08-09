# 16. Master Reference — Hashing

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 10: Hashing**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh `hashCode()` and `equals()` contracts, Java 8 bit-spreading `h ^ (h >>> 16)`, treeification constants (8, 6, 64), high/low bit split `(e.hash & oldCap) == 0`, load factor 0.75 pre-sizing formula `(N / 0.75) + 1`, Cuckoo hashing worst-case $O(1)$ search, Prefix Sum `currSum - K` maps, Top K frequency bucket sort, and Consistent Hashing virtual nodes!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Contract Between `equals()` and `hashCode()`**:
  - `a.equals(b) == true \implies a.hashCode() == b.hashCode()`. Overriding `equals()` REQUIRES overriding `hashCode()`.
* **Java 8 Supplemental Hash Bit-Spreading**:
  - `h = key.hashCode(); hash = h ^ (h >>> 16)`.
* **Power-of-2 Array Bucket Indexing**:
  - `index = (capacity - 1) & hash`.
* **Safe Positive Sign Bit Removal**:
  - `positiveHash = hash & 0x7FFFFFFF`.
* **Load Factor & Threshold Equation**:
  - $\alpha = N / M = 0.75$. $\text{Threshold} = \text{Capacity} \times 0.75$.
* **Pre-Sizing Capacity Equation for $N$ Items**:
  - $\text{Initial Capacity} = \lceil N / 0.75 \rceil + 1$.
* **Java 8 High/Low Bit Transfer Condition**:
  - If `(e.hash & oldCap) == 0` $\rightarrow$ Stays at `index`.
  - If `(e.hash & oldCap) != 0` $\rightarrow$ Moves to `index + oldCap`.
* **Java 8 Treeification Threshold Constants**:
  - `TREEIFY_THRESHOLD = 8`, `UNTREEIFY_THRESHOLD = 6`, `MIN_TREEIFY_CAPACITY = 64`.
* **Subarray Sum Prefix Match Equation**:
  - $\text{SubarraySum}(i \dots j) = P[j] - P[i-1] = K \implies P[i-1] = P[j] - K$.
* **Positive Remainder Normalization Formula**:
  - $\text{remainder} = ((currSum \bmod K) + K) \bmod K$.
* **Rolling Hash $O(1)$ Window Update Equation**:
  - $H_{\text{new}} = (((H_{\text{old}} - s[i-1] \cdot P^{L-1}) \bmod M + M) \bmod M \cdot P + s[i+L-1]) \bmod M$.
* **Bloom Filter Bit Array & Hash Functions Equations**:
  - $M = -\frac{N \ln p}{(\ln 2)^2}$, $K = \frac{M}{N} \ln 2$.

```
Hashing Invariants & Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Hashing Variant                   | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Java 8 Supplemental Hash          | hash = h ^ (h >>> 16)                             |
| Bucket Indexing (Power of 2)      | index = (capacity - 1) & hash                     |
| High/Low Bit Split Resizing       | (e.hash & oldCap) == 0 -> index vs index + oldCap |
| HashMap Pre-sizing Formula        | initialCapacity = (expectedEntries / 0.75f) + 1   |
| Treeify Constants                 | Treeify at 8 nodes if capacity >= 64; Untreeify 6 |
| Subarray Sum Prefix Match         | Check prefixMap.containsKey(currSum - K)          |
| Positive Modulo Normalization     | remainder = ((currSum % K) + K) % K               |
| Consecutive Sequence Start        | Explore ONLY IF !set.contains(num - 1)            |
| Group Anagrams Frequency Key      | Key = "#1#0#2...#0" using '#' delimiters          |
| HashSet Map Backing               | return map.put(element, PRESENT) == null          |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`HashMap.get() / put()`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(\log N)$ (Treeified)**| $O(N)$ Space | Direct array indexing + BST |
| **Polynomial String Hash**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(1)$ Space | Multiplier prime 31 `(h<<5)-h` |
| **Cuckoo Hashing Search** | **$O(1)$ Guaranteed ⚡**| **$O(1)$ Guaranteed ⚡**| **$O(1)$ Guaranteed ⚡**| $O(N)$ Space | 2 Tables, 2 Hash functions |
| **Open Address Probing** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(N)$ (High Load) | **$O(N)$ In-Place** | Maximum CPU cache locality |
| **High/Low Rehashing** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(2N)$ Array | Zero hash re-computations |
| **HashSet `add() / contains()`**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡** | **$O(\log N)$ (Treeified)**| $O(N)$ Space | `HashMap<E, Object>` backing |
| **First Unique Char (387)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Array Space**| Fixed `int[26]` frequency array |
| **Top K Bucket Sort (347)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Bucket Space| Bucket index = frequency |
| **Min Window Substring (76)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(U)$ Map Space | Sliding window + frequency map |
| **Subarray Sum Equals K (560)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Prefix sum `prefixMap.put(0,1)` |
| **Divisible by K (974)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(K)$ Map Space | Positive remainder `((S%K)+K)%K`|
| **Contiguous Array (525)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Convert 0 to -1 + prefix index |
| **Group Anagrams (49)** | **$O(N \cdot K)$ ⚡** | **$O(N \cdot K)$ ⚡** | **$O(N \cdot K)$ ⚡** | $O(N \cdot K)$ Space| Frequency key `#1#0#2...` |
| **Isomorphic Strings (205)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Array Space**| Dual 1-based index arrays |
| **Longest Consecutive (128)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Set Space | Skip if `set.contains(n - 1)` |
| **Rabin-Karp Search (28)**| **$O(N + M)$ Average ⚡**| **$O(N + M)$ Average ⚡**| $O(N \cdot M)$ Collide | **$O(1)$ Space** | $O(1)$ rolling hash update |
| **Consistent Hash Lookup**| **$O(\log(N \cdot V))$ ⚡**| **$O(\log(N \cdot V))$ ⚡**| **$O(\log(N \cdot V))$ ⚡**| $O(N \cdot V)$ Space| TreeMap `ceilingKey()` |
| **Bloom Filter Lookup** | **$O(K)$ Constant ⚡** | **$O(K)$ Constant ⚡** | **$O(K)$ Constant ⚡** | **$O(M)$ Bit Array**| Zero false negatives! |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Hash Table Implementations                                   |
+-----------------------------------------------------------------------------------+
| JDK HashMap Node<K,V>               : 32 Bytes per Entry (Object Header + Pointers)|
| Open Addressing Entry Array         : Contiguous Array (Best CPU Cache Hit Rate) ⚡ |
| Bloom Filter BitSet                 : ~10 Bits per Element (99% Space Reduction!) ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. HashMap Frequency Counter Pattern
map.put(key, map.getOrDefault(key, 0) + 1);

// 2. Subarray Sum Prefix Match Pattern
prefixMap.put(0, 1);
if (prefixMap.containsKey(currSum - k)) count += prefixMap.get(currSum - k);

// 3. Longest Consecutive Sequence Boundary Exploration Pattern
if (!numSet.contains(num - 1)) {
    while (numSet.contains(curr + 1)) { curr++; streak++; }
}

// 4. Group Anagrams Frequency String Key Pattern
int[] count = new int[26];
for (char c : s.toCharArray()) count[c - 'a']++;
StringBuilder sb = new StringBuilder();
for (int c : count) sb.append('#').append(c);

// 5. Pre-sizing HashMap Capacity for N Elements
int capacity = (int) Math.ceil(expectedEntries / 0.75f) + 1;
Map<K, V> map = new HashMap<>(capacity);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Overriding `equals()` Without `hashCode()`**: Equal objects hash to different buckets, returning `null` on `get()`.
* **Pitfall 2: Mutating Keys After Insertion**: Changes `hashCode()`, causing the key to become unreachable in future `get()` calls.
* **Pitfall 3: Forgetting `prefixMap.put(0, 1)` Base Sentinel**: Misses valid sub-arrays starting at index 0 whose sum equals $K$.
* **Pitfall 4: Negative Remainder in Modulo Math (`-2 % 5 = -2`)**: Always normalize remainders: `((currSum % K) + K) % K`.
* **Pitfall 5: Using `==` on Integer Object Values in Maps**: Values outside `-128 ... 127` fail `==`. Always use `.equals()`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 10 (HASHING)                     |
+-----------------------------------------------------------------------+
| 1. Hash Contract: Equal objects MUST produce equal hash codes!        |
| 2. Bit-Spreading: hash = h ^ (h >>> 16) mixes high-bit entropy        |
| 3. Index Formula: (capacity - 1) & hash for power-of-2 capacities     |
| 4. Treeify Constants: Treeify at 8 nodes if cap >= 64; Untreeify at 6 |
| 5. High/Low Rehash: (e.hash & oldCap) == 0 splits low/high bins       |
| 6. Pre-sizing Rule: capacity = (expectedEntries / 0.75f) + 1          |
| 7. Cuckoo Search: Checks 2 tables -> Guaranteed O(1) worst-case search|
| 8. Open Addressing Tombstones: Mark deletions with DELETED sentinel   |
| 9. Subarray Sum (560): prefixMap.put(0, 1); check currSum - K          |
| 10. Top K Bucket Sort (347): Bucket index = frequency; scan N down to 1|
| 11. Consecutive Sequence (128): Explore ONLY if !set.contains(n - 1)  |
| 12. Group Anagrams (49): Frequency key "#1#0#2" for O(N*K) time       |
| 13. Rolling Hash (28): H_new = (((H - out*power)%M + M)%M * P + in) % M|
| 14. Bloom Filter: Zero false negatives! False = 100% NOT present      |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write a custom Chaining HashMap from scratch.
- [ ] I can trace `putVal()` control flow in JDK HashMap.
- [ ] I can write Cuckoo Hashing with 2 tables for guaranteed $O(1)$ search.
- [ ] I can write Double Hashing Open Addressing with Tombstones.
- [ ] I can write Subarray Sum Equals K (LeetCode 560) using prefix maps.
- [ ] I can write Subarray Sums Divisible by K (LeetCode 974).
- [ ] I can write Contiguous Array (LeetCode 525) by converting 0 to -1.
- [ ] I can write Top K Frequent Elements (LeetCode 347) using Bucket Sort.
- [ ] I can write Group Anagrams (LeetCode 49) using frequency keys.
- [ ] I can write Isomorphic Strings (LeetCode 205) using dual index arrays.
- [ ] I can write Longest Consecutive Sequence (LeetCode 128) in $O(N)$ time.
- [ ] I can write Rabin-Karp Substring Search (LeetCode 28) rolling hash.
- [ ] I can write Repeated DNA Sequences (LeetCode 187) 20-bit bitmask.
- [ ] I can write a Consistent Hashing Ring with Virtual Nodes.
- [ ] I can write a Bloom Filter using `BitSet`.
