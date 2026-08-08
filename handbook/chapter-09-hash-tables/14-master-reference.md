# 14. Master Reference — Hash Tables & Hash Maps

## 1. Introduction
This Master Reference consolidates all mathematical proofs, JDK source code constants, bitwise indexing formulas, collision resolution mechanics, hash functions, and problem recognition patterns for **Chapter 9: Hash Tables & Hash Maps**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for candidates preparing for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh `h ^ (h >>> 16)` bitwise spreading, `(hash & oldCap) == 0` bit-transfer resizing, Poisson treeification odds, `map.put(0, 1)` prefix sum rules, and `LinkedHashMap` LRU cache setups.

---

## 2. Master Mathematical & JDK Formula Cheat Sheet
* **Index Compression Mask (Power of 2)**: `index = (hash ^ (hash >>> 16)) & (capacity - 1)`
* **Positive Integer Modulo**: `index = (hashCode & 0x7FFFFFFF) % capacity`
* **Positive Remainder Modulo**: `remainder = ((runningSum % k) + k) % k`
* **Polynomial String Hash (Horner)**: `h = (h << 5) - h + char` (Multiplier 31)
* **Universal Hashing Formula**: `h_{a,b}(k) = ((a * k + b) % p) % m`
* **Expected Open Addressing Probes**: $E[\text{unsuccessful probes}] = \frac{1}{1 - \alpha}$
* **Expected Separate Chaining Search**: $E[\text{search time}] = O(1 + \alpha)$
* **Bit-Transfer Resizing Check**: `if ((hash & oldCap) == 0)` $\implies$ Stays at index $j$ (`loHead`); else moves to $j + \text{oldCap}$ (`hiHead`).
* **Sudoku 3x3 Sub-Grid Index**: `boxIndex = (r / 3) * 3 + (c / 3)`
* **2D Coordinate Linear Flattening**: `key = r * COLS + c` (Decode: `r = key / COLS, c = key % COLS`)
* **64-Bit Bitwise Coordinate Packing**: `long key = (((long) r) << 32) | (c & 0xFFFFFFFFL)`
* **Task Capacity Formula**: Set `initialCapacity = (int) Math.ceil(N / 0.75f) + 1` to prevent dynamic resizing overhead.

```
JDK HashMap Core Constants Summary:
+-----------------------------------+-------------------+------------------------------------+
| JDK Constant Name                 | Constant Value    | Architectural Significance         |
+-----------------------------------+-------------------+------------------------------------+
| DEFAULT_INITIAL_CAPACITY          | 16 (1 << 4)       | Must be power of two               |
| MAXIMUM_CAPACITY                  | 1,073,741,824     | (1 << 30)                          |
| DEFAULT_LOAD_FACTOR               | 0.75f             | Optimal time/space balance         |
| TREEIFY_THRESHOLD                 | 8                 | Convert linked list to RB-Tree     |
| UNTREEIFY_THRESHOLD               | 6                 | Convert RB-Tree back to list       |
| MIN_TREEIFY_CAPACITY              | 64                | Min table size required to treeify |
+-----------------------------------+-------------------+------------------------------------+
```

---

## 3. Master Hash Table Complexity Table

| Operation / Algorithm | Time Complexity (Average) | Time Complexity (Worst Case) | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **`HashMap.get(key)`** | **$O(1)$ Constant ⚡** | $O(\log N)$ (Java 8 Tree) | $O(N + m)$ | Bitwise mask `hash & (n-1)` |
| **`HashMap.put(k, v)`** | **Amortized $O(1)$ ⚡**| $O(\log N)$ (Java 8 Tree) | $O(N + m)$ | Tail insertion + Bit-transfer split |
| **`HashMap.remove(k)`** | **$O(1)$ Constant ⚡** | $O(\log N)$ (Java 8 Tree) | $O(N + m)$ | Node / TreeNode unlinking |
| **Linear Probing Probe** | **$O(1)$ ($\alpha < 0.5$)** | $O(N)$ (Primary Cluster)| $O(m)$ Array | High L1 Cache locality ⚡ |
| **Double Hashing Probe** | **$O(1)$ ($\alpha < 0.7$)** | $O(N)$ | $O(m)$ Array | `(h1(k) + i*h2(k)) % m` |
| **Two Sum (LeetCode 1)** | **$O(N)$ Linear ⚡** | $O(N)$ | $O(N)$ | Complement `target - nums[i]` |
| **Subarray Sum K (560)** | **$O(N)$ Linear ⚡** | $O(N)$ | $O(N)$ | Prefix Sum `P[j] - K` (map.put(0,1)) |
| **Equal 0s and 1s (525)** | **$O(N)$ Linear ⚡** | $O(N)$ | $O(N)$ | Map 0 to -1, First Index Map |
| **Group Anagrams (49)** | **$O(N \cdot L)$ Linear ⚡**| $O(N \cdot L)$ | $O(N \cdot L)$ | Canonical Key `#1#0#1...` |
| **Longest Consecutive (128)**| **$O(N)$ Linear ⚡**| $O(N)$ | $O(N)$ | Set Filter `!set.contains(n-1)` |
| **Isomorphic Strings (205)**| **$O(N)$ Linear ⚡** | $O(N)$ | **$O(1)$ Space ⚡**| Dual Array `lastSeenS[s] == lastSeenT[t]`|
| **Valid Sudoku (36)** | **$O(1)$ Constant ⚡** | $O(1)$ | $O(1)$ Stack | Bitmask Arrays `rows[r] & (1<<num)` |
| **LRU Cache (146)** | **Strict $O(1)$ ⚡** | Strict $O(1)$ | $O(\text{Cap})$ | `LinkedHashMap(cap, 0.75f, true)` |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory & Architecture Object Breakdown (64-Bit JVM with Compressed OOPs)          |
+-----------------------------------------------------------------------------------+
| Node<K,V> Memory Footprint  : 32 Bytes per Node object on Heap                    |
| TreeNode<K,V> Memory        : ~64 Bytes per Red-Black Tree Node                   |
| LinkedHashMap.Entry<K,V>    : ~40 Bytes per Entry (Adds before & after pointers)  |
| HashSet Storage Overhead    : Wraps HashMap<E, Object> using 1 static PRESENT val |
| Array Memory Allocation     : Object[] table reference array                      |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Supplemental Hash Spreading & Power of Two Mask Compression
int h = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
int index = h & (capacity - 1);

// 2. Safe Positive Modulo for Negative Remainders
int remainder = ((runningSum % k) + k) % k;

// 3. Bit-Transfer Resizing Split Check
if ((e.hash & oldCap) == 0) { /* loHead (same index j) */ }
else { /* hiHead (moves to index j + oldCap) */ }

// 4. Single-Pass Complement Lookup
int comp = target - nums[i];
if (map.containsKey(comp)) return new int[]{map.get(comp), i};
map.put(nums[i], i);

// 5. Prefix Sum Subarray Counting Base Rule
map.put(0, 1);

// 6. Set Sequence Boundary Start Filter
if (!set.contains(num - 1)) { while (set.contains(curr + 1)) { curr++; streak++; } }

// 7. Bijective 1-Based Last Seen Match
if (sSeen[s.charAt(i)] != tSeen[t.charAt(i)]) return false;
sSeen[s.charAt(i)] = i + 1; tSeen[t.charAt(i)] = i + 1;

// 8. 64-Bit Coordinate Packing
long key = (((long) r) << 32) | (c & 0xFFFFFFFFL);

// 9. LRU Cache LinkedHashMap Subclass Pattern
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    public LRUCache(int cap) { super(cap, 0.75f, true); }
    @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) { return size() > cap; }
}
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Overriding `equals()` without Overriding `hashCode()`**: Violates Java's fundamental contract! Equal objects end up in different buckets.
* **Pitfall 2: Mutating Keys In-Place**: Modifying fields used in `hashCode()` after insertion makes the object **permanently un-retrievable**.
* **Pitfall 3: `Math.abs(Integer.MIN_VALUE)` Negative Index Bug**: `Math.abs(Integer.MIN_VALUE)` is STILL negative (`-2147483648`). Always use `(hash & 0x7FFFFFFF) % m`.
* **Pitfall 4: Open Addressing Null Deletion Bug**: Setting deleted slots to `null` breaks search chains. Use `TOMBSTONE` sentinels.
* **Pitfall 5: Omitting Delimiters in Canonical Keys**: Frequency arrays without `#` cause false collisions between `[1, 11]` and `[11, 1]`.
* **Pitfall 6: Double Slope Keys (LeetCode 149)**: Floating-point precision rounding errors ruin map keys. Use GCD reduced fraction string keys `"dy/dx"`.
* **Pitfall 7: Thread-Unsafe Resizing in Java 7**: Multi-threaded `HashMap.put()` resizing caused CPU 100% infinite loops due to head-insertion list reversals. Java 8 uses tail insertion.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 9 (HASH TABLES & HASH MAPS)      |
+-----------------------------------------------------------------------+
| 1. Index Formula: (hash ^ (hash >>> 16)) & (capacity - 1)             |
| 2. Treeify Rule: List -> Red-Black Tree at >= 8 nodes & capacity >= 64|
| 3. Untreeify Rule: Tree -> List at <= 6 nodes (Hysteresis Gap!)       |
| 4. Bit-Transfer Resizing: (hash & oldCap) == 0 splits lo/hi chains    |
| 5. Two Sum Pattern: Check map.containsKey(target - nums[i]) BEFORE put|
| 6. Prefix Sum Pattern: ALWAYS map.put(0, 1)! Target = P[j] - K        |
| 7. Anagram Canonical Key: Format int[26] count as "#1#0#1..."         |
| 8. Consecutive Sequence: Expand ONLY if (!set.contains(num - 1))      |
| 9. Bijective Match: sSeen[s[i]] == tSeen[t[i]] with 1-based indices   |
| 10. LRU Cache: LinkedHashMap(cap, 0.75f, true) + removeEldestEntry()  |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write the supplemental hash function `h ^ (h >>> 16)` and explain its necessity.
- [ ] I can derive `(hash & oldCap) == 0` for bit-transfer resizing without hash recomputation.
- [ ] I can state the 6 JDK HashMap constants and their exact values.
- [ ] I can explain the 32-byte heap memory footprint of `HashMap.Node`.
- [ ] I can write single-pass Two Sum and explain why checking before `put()` prevents bugs.
- [ ] I can write Subarray Sum Equals K (LeetCode 560) and explain `map.put(0, 1)`.
- [ ] I can format 26-element canonical frequency keys with `#` delimiters.
- [ ] I can write Longest Consecutive Sequence (LeetCode 128) in $O(N)$ amortized time.
- [ ] I can write Isomorphic Strings (LeetCode 205) using dual `int[256]` last-seen arrays.
- [ ] I can implement Valid Sudoku (LeetCode 36) using bitmask arrays and box index math.
- [ ] I can create a 10-line LRU Cache extending `LinkedHashMap`.
