# 14. Master Reference — Bit Manipulation Algorithms & Paradigms

## 1. Introduction
This Master Reference consolidates all mathematical formulas, operational complexities, structural invariants, decision trees, design patterns, and interview traps for **Chapter 29: Bit Manipulation**. It serves as an ultra-dense, rapid-scanning interview cheat sheet covering Binary Representation, Two's Complement (-x = ~x + 1), Bitwise Operators (&, |, ^, ~, <<, >>, >>>), Bit Masks, Common Bit Hacks (Power of 2, 3, 4, Fast Modulo, ASCII Case Switching), XOR Algorithms (Single Number I, II, III, Missing Number), Bit Counting (Brian Kernighan, SWAR, LeetCode 338 DP), Gray Code (LeetCode 89), Bitmask Enumeration (Sub-mask loop `sub = (sub - 1) & mask`, Gosper's Hack), Bitmask DP (Held-Karp TSP, LeetCode 1125), Systems Applications (Bloom Filters, CIDR Subnetting, POSIX Permissions), Advanced Optimizations (Branchless `abs`, `min`, `max`, 64-bit Bitsets), and the 6 Master Bit Manipulation Archetypes.

> **Important:** Review this master reference 15 minutes before an interview to refresh Two's Complement Negation (`-x = ~x + 1`), Check bit `((x & (1 << k)) != 0)`, Set bit `x | (1 << k)`, Clear bit `x & ~(1 << k)`, Clear lowest bit `x & (x - 1)`, Isolate lowest bit `x & (-x)`, Power of Two `(n > 0) && ((n & (n - 1)) == 0)`, Power of Three `(n > 0) && (1162261467 % n == 0)`, Power of Four `(n > 0) && isPow2 && ((n & 0x55555555) != 0)`, Single Number III partition `diff & (-diff)`, Counting Bits Range DP (`DP[i >> 1] + (i & 1)`), Gray Code (`i ^ (i >> 1)`), Sub-mask loop (`sub = (sub - 1) & mask`), Gosper's Hack, Bloom Filter `BitSet`, Subnet IP (`ip & mask`), and Branchless `abs(x) = (x + mask) ^ mask`!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Two's Complement Negation**:
  - $-x = \sim x + 1$ (Invert all bits and add 1).
* **Arithmetic vs Logical Shift Rules**:
  - `x >> k`: Arithmetic Right Shift (Preserves sign bit by shifting in `1`s for negative numbers).
  - `x >>> k`: Logical Right Shift (Fills vacant left bits with `0`s regardless of sign).
* **The 6 Master Bit Masking Formulas**:
  1. Check Bit $k$: `((x & (1 << k)) != 0)`
  2. Set Bit $k$: `x | (1 << k)`
  3. Clear Bit $k$: `x & ~(1 << k)`
  4. Toggle Bit $k$: `x ^ (1 << k)`
  5. Clear Lowest Set Bit: `x & (x - 1)` (Brian Kernighan's Algorithm)
  6. Isolate Lowest Set Bit: `x & (-x)` (Fenwick Tree Extractor)
* **Common Bit Tricks Formulas**:
  - Fast Parity: `(x & 1) == 0` (Even) | `(x & 1) != 0` (Odd).
  - Fast Modulo by $2^k$: `x & (2^k - 1)`.
  - In-Place XOR Swap: `a ^= b; b ^= a; a ^= b;`
  - ASCII Lowercase: `ch | ' '` (Sets bit 5).
  - ASCII Uppercase: `ch & '_'` (Clears bit 5).
  - ASCII Toggle Case: `ch ^ ' '` (Flips bit 5).
* **Power Verification Formulas**:
  - Power of 2 (LC 231): `(n > 0) && ((n & (n - 1)) == 0)`.
  - Power of 3 (LC 326): `(n > 0) && (1162261467 % n == 0)` ($3^{19} = 1,162,261,467$).
  - Power of 4 (LC 342): `(n > 0) && ((n & (n - 1)) == 0) && ((n & 0x55555555) != 0)`.
* **Single Number III Partitioning Invariant (LC 260)**:
  - $\text{diff} = X \oplus Y \implies \text{isolatedBit} = \text{diff} \& (-\text{diff})$. Partition by `(num & isolatedBit) != 0`.
* **Counting Bits Range DP Recurrence (LC 338)**:
  - $DP[i] = DP[i \gg 1] + (i \;\&\; 1)$ in $O(N)$ linear time.
* **Gray Code Conversions (LC 89)**:
  - Binary to Gray: $G = B \oplus (B \gg 1)$.
  - Sequence Generation: $\text{res.add}(i \oplus (i \gg 1))$ for $i = 0 \dots 2^N - 1$.
* **Sub-mask & Gosper's Hack Formulas**:
  - Sub-mask Iteration Loop: `for (int sub = mask; sub > 0; sub = (sub - 1) & mask)`.
  - Gosper's Hack: `c = mask & -mask; r = mask + c; mask = (((r ^ mask) >> 2) / c) | r;`.
* **Network Subnetting & System Bitmasks**:
  - Network Base IP: `network = ip & mask`.
  - Broadcast IP: `broadcast = ip | (~mask)`.
  - POSIX Permission Mask: `(owner << 6) | (group << 3) | others`.
* **Branchless Bitwise Optimization Idioms**:
  - Branchless `abs(x)`: `mask = x >> 31; return (x + mask) ^ mask;`.
  - Branchless `min(a, b)`: `diff = a - b; return b + (diff & (diff >> 31));`.
  - Branchless `max(a, b)`: `diff = a - b; return a - (diff & (diff >> 31));`.
  - Compact BitSet: `words[i >> 6] |= (1L << (i & 63))` ($8\times$ data density!).

```
Master Bit Manipulation Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Bitwise Archetype     | Core Formula      | Primary Hardware  | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Binary & Two's Comp**| `-x = ~x + 1`    | Arithmetic ALU    | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Bit Masking**       | `x & (x - 1)` / `x & (-x)`| Bitwise AND/XOR| **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **XOR Algorithms**    | `diff & (-diff)`  | Bitwise XOR       | **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **Bit Counting (338)**| `DP[i>>1] + (i&1)`| Shift Adder       | **$O(N)$ Linear ⚡**| **$O(N)$ Array ⚡**|
| **Power Verifier (231)**| `(n & (n-1))==0`| Single Set Bit    | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Gray Code (89)**    | `i ^ (i >> 1)`    | Reflected Shift   | **$O(2^N)$ Linear ⚡**| **$O(2^N)$ Array ⚡**|
| **Sub-mask Loop**     | `sub = (sub-1)&mask`| Binomial Expansion| **$O(3^N)$ Total ⚡**| **$O(1)$ Memory ⚡**|
| **Bitmask DP (TSP)**  | $DP[\text{mask}][u]$| Compressed Mask  | **$O(N^2 \cdot 2^N)$ ⚡**| **$O(N \cdot 2^N)$ ⚡**|
| **Systems Subnetting**| `ip & mask`       | Mask Extractor    | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
| **Branchless `abs`**  | `(x + mask)^mask` | Zero Mispredicts  | **$O(1)$ Instant ⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Bit Manipulation Topic | Primary Formula | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Two's Complement** | `-x = ~x + 1` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Sign bit MSB 31 |
| **Bitwise AND (`&`)** | `x & y` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Bit extraction & masking |
| **Bitwise OR (`|`)** | `x | y` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Setting bit flags |
| **Bitwise XOR (`^`)** | `x ^ y` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Toggling & $A \oplus A = 0$ |
| **Clear Lowest Bit** | `x & (x - 1)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Brian Kernighan bit count |
| **Isolate Lowest Bit**| `x & (-x)` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Fenwick Tree index update |
| **Single Number I (136)**| Cumulative XOR sum | $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Pair cancellation |
| **Single Number III (260)**| `diff & (-diff)` | $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(1)}$ Memory ⚡| Bit group partitioning |
| **Counting Bits (338)**| `DP[i >> 1] + (i & 1)`| $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(N)}$ Array Space| Range $0 \dots N$ DP |
| **Power of Two (231)**| `(n > 0) && (n & (n-1))==0`| $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Single set 1-bit |
| **Power of Three (326)**| `(n > 0) && (1162261467 % n == 0)`| $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| $3^{19} = 1,162,261,467$ |
| **Power of Four (342)**| `n & 0x55555555` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Odd position mask |
| **Gray Code Gen (89)**| `res.add(i ^ (i >>> 1))`| $\mathbf{O(2^N)}$ Strict Linear⚡| $\mathbf{O(2^N)}$ Array Space| Single-bit transition |
| **Sub-mask Iteration** | `sub = (sub - 1) & mask`| $\mathbf{O(3^N)}$ Total Binomial⚡| $\mathbf{O(1)}$ Memory ⚡| All sub-masks of all masks |
| **Gosper's Hack** | `mask = (((r^mask)>>2)/c)|r`| $\mathbf{O(1)}$ per State ⚡| $\mathbf{O(1)}$ Memory ⚡| Fixed $K$ set bits |
| **Held-Karp TSP** | $DP[\text{mask}][u]$ | $\mathbf{O(N^2 \cdot 2^N)}$ Exponential⚡| $\mathbf{O(N \cdot 2^N)}$ DP Table| $N \le 20$ Cities |
| **Bloom Filter** | `bitSet.set(h(x))` | $\mathbf{O(K)}$ Hashes ⚡| $\mathbf{O(M)}$ BitSet | >99% RAM Compression |
| **CIDR Subnetting** | `network = ip & mask` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| IPv4 Base & Broadcast |
| **Branchless `abs(x)`**| `(x + mask) ^ mask` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Zero CPU mispredicts |

---

## 4. Architectural System & Production Use Cases
```
+-----------------------------------------------------------------------------------+
| Production System Bit Manipulation Architectures                                  |
+-----------------------------------------------------------------------------------+
| Database Bitmap Indexes & Query Filtering      : Fast Bitset Bitwise AND / OR     |
| Production Bloom Filters (Redis, Chrome, RocksDB): Probabilistic Set Membership BitSet|
| Network Subnet Routers & Firewall CIDR Filters : IPv4 Bitmask Operations (ip & mask)|
| Industrial Machine Vision & Rotary Encoders    : Gray Code Glitch-Free Transitions|
| High-Frequency Trading & Physics Engines       : Branchless Arithmetic (abs/min/max)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
> ```java
> // 1. Two's Complement Negation & Shifts
> int negX = ~x + 1; int arithmetic = num >> shift; int logical = num >>> shift;
> 
> // 2. The 6 Master Bit Masking Formulas
> boolean isSet = ((x & (1 << k)) != 0); int setB = x | (1 << k); int clearB = x & ~(1 << k);
> int toggleB = x ^ (1 << k); int clearLowest = x & (x - 1); int isolateLowest = x & (-x);
> 
> // 3. Common Bit Hacks
> boolean isEven = (x & 1) == 0; int modPow2 = x & (powerOfTwo - 1);
> char lower = (char)(ch | ' '); char upper = (char)(ch & '_'); char toggle = (char)(ch ^ ' ');
> 
> // 4. Power Verification Formulas
> boolean isPow2 = (n > 0 && (n & (n - 1)) == 0);
> boolean isPow3 = (n > 0 && 1162261467 % n == 0);
> boolean isPow4 = (n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0);
> 
> // 5. Single Number III Bit Partitioning (LC 260)
> int diff = 0; for (int num : nums) diff ^= num;
> int isolatedBit = diff & (-diff);
> if ((num & isolatedBit) != 0) x ^= num; else y ^= num;
> 
> // 6. Counting Bits Range DP (LC 338)
> for (int i = 1; i <= n; i++) dp[i] = dp[i >> 1] + (i & 1);
> 
> // 7. Gray Code Sequence (LC 89)
> for (int i = 0; i < (1 << n); i++) res.add(i ^ (i >>> 1));
> 
> // 8. Sub-mask Iteration Loop & Gosper's Hack
> for (int sub = mask; sub > 0; sub = (sub - 1) & mask) ...
> int c = mask & -mask, r = mask + c; mask = (((r ^ mask) >> 2) / c) | r;
> 
> // 9. Branchless Arithmetic & 64-bit BitSet
> int absVal = (x + (x >> 31)) ^ (x >> 31); words[i >> 6] |= (1L << (i & 63));
> ```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Omitting Parentheses Around Bitwise Operations**: Writing `if (x & 1 == 0)` evaluates `1 == 0` first due to precedence, producing a logical bug. **ALWAYS write `if ((x & 1) == 0)`**!
* **Pitfall 2: Shifting by $\ge 32$ Bits on 32-bit `int` Types**: In Java, `1 << 32` evaluates to `1 << 0 = 1`. **ALWAYS use `1L << k` with `long` primitive type for $k \ge 32$**!
* **Pitfall 3: Using `>>` Instead of `>>>` for Unsigned Bit Scanning**: Using arithmetic right shift `>>` on negative integers shifts in `1`s, creating an infinite loop. **ALWAYS use `>>>` for unsigned bit scanning**!
* **Pitfall 4: Omitting Positivity Check `n > 0` in Power Verification**: Writing `(n & (n - 1)) == 0` without `n > 0` evaluates to `true` for `n = 0`. **ALWAYS check `n > 0 && ((n & (n - 1)) == 0)`**!
* **Pitfall 5: Applying Bitmask DP when $N > 22$**: Allocating `new int[1 << 30]` crashes JVM with memory overflow. **Bitmask DP is strictly for $N \le 20$**!
* **Pitfall 6: Using `boolean[]` Arrays for Large Flag Vectors**: `boolean[]` wastes 7 out of 8 bits per element in RAM. **ALWAYS use `long[]` BitSet for 8x memory density and L1 cache locality**!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 29 (BIT MANIPULATION)            |
+-----------------------------------------------------------------------+
| 1. Two's Complement: -x = ~x + 1 | Logical shift >>> fills 0s         |
| 2. Check Bit k     : ((x & (1 << k)) != 0) (Double Parentheses!)      |
| 3. Clear Lowest Bit: x & (x - 1) (Brian Kernighan O(SetBits) Count)   |
| 4. Isolate Lowest  : x & (-x) (Fenwick Tree Index Extractor)          |
| 5. Power of 2 (231): (n > 0) && ((n & (n - 1)) == 0)                  |
| 6. Power of 3 (326): (n > 0) && (1162261467 % n == 0)                 |
| 7. Power of 4 (342): (n > 0) && isPow2 && ((n & 0x55555555) != 0)     |
| 8. Single Num III  : diff = X^Y -> isolatedBit = diff & -diff         |
| 9. Counting Bits   : DP[i] = DP[i >> 1] + (i & 1) (LeetCode 338 O(N))  |
| 10. Gray Code (89) : res.add(i ^ (i >>> 1))                           |
| 11. Sub-mask Loop  : for (int sub = mask; sub > 0; sub = (sub - 1) & mask)|
| 12. Bitmask DP     : State DP[mask][u] strictly for N <= 20           |
| 13. Subnet Base    : networkIP = ip & mask; broadcastIP = ip | (~mask)|
| 14. Branchless Abs : mask = x >> 31; return (x + mask) ^ mask;        |
| 15. 64-bit BitSet  : words[i >> 6] |= (1L << (i & 63)) (8x Density!)  |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Two's Complement negation `-x = ~x + 1` in Java.
- [ ] I can explain the difference between arithmetic `>>` and logical `>>>` shifts.
- [ ] I can write all 6 master bit masking formulas in Java.
- [ ] I can state why parentheses are mandatory around `((x & mask) == 0)`.
- [ ] I can write Brian Kernighan's set bit counter in Java.
- [ ] I can write LeetCode 136 (`Single Number I`) and LeetCode 260 (`Single Number III`) in Java.
- [ ] I can write LeetCode 338 (`Counting Bits`) DP array generator in $O(N)$ time.
- [ ] I can write all 3 Power Verification formulas (LeetCode 231, 326, 342) in $O(1)$ time.
- [ ] I can write LeetCode 89 (`Gray Code Sequence`) in $O(2^N)$ time.
- [ ] I can write the sub-mask iteration loop `sub = (sub - 1) & mask`.
- [ ] I can state why Bitmask DP is limited to $N \le 20$.
- [ ] I can write IPv4 network and broadcast address calculators.
- [ ] I can write branchless `abs(x)`, `min(a, b)`, and `max(a, b)` in Java.
- [ ] I can write a 64-bit word BitSet allocator in Java.
- [ ] I can match any bit manipulation question to one of the 6 Master Archetypes in under 10 seconds.
