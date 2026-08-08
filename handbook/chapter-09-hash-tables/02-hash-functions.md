# 02. Hash Functions, Polynomial Rolling Hash & Hash Spreading Mechanics

## 1. Introduction
A **Hash Function** $h(k)$ is a mathematical function that maps a key $k$ from a large universe of keys $U$ to a fixed range of array indices $[0 \dots m - 1]$. In technical coding interviews and distributed systems architecture, designing an optimal Hash Function is the single most important factor determining Hash Table performance. A well-designed hash function distributes keys uniformly across all available bucket slots, minimizing collisions and guaranteeing **Average $O(1)$ constant time complexity** for hash map operations.

> **Important:** The fundamental ideal of hashing is the **Simple Uniform Hashing Assumption**: Any given key $k$ is equally likely to hash into any of the $m$ slots, independently of where any other key has hashed.

```
Hash Function Construction Goals:
+-----------------------------------------------------------------------------------+
| 1. Uniformity : Distribute keys evenly across slots 0..m-1                        |
| 2. Speed      : Execute in O(1) time using fast CPU bitwise operations            |
| 3. Determinism: Same input key MUST ALWAYS yield exact same hash output           |
| 4. Spreading  : A 1-bit change in key changes ~50% of hash output bits (Avalanche)|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Methods

### 2.1 The Division Method
In the **Division Method**, the hash function maps a non-negative integer key $k$ to one of $m$ slots by taking the remainder of $k$ divided by $m$:

$$h(k) = k \pmod m$$

* **Advantage**: Fast computation (single modulo division instruction).
* **Pitfall with Powers of Two**: If $m = 2^p$, then $h(k)$ is simply the $p$ lowest-order bits of $k$. Higher-order bits are completely ignored, causing severe collisions if keys share low-order patterns!
* **Optimal Choice for $m$**: When using the Division Method, $m$ should be a **Prime Number** not close to any power of 2 or 10 (e.g. $m = 701$ or $m = 9973$).

### 2.2 The Multiplication Method
The **Multiplication Method** operates in two steps:
1. Multiply the key $k$ by a constant real number $A$ in the range $0 < A < 1$, and extract the fractional part of $k \cdot A$:
   $$\text{fractional}(k \cdot A) = (k \cdot A) \pmod 1 = (k \cdot A) - \lfloor k \cdot A \rfloor$$
2. Multiply this fractional value by $m$ and take the floor of the result:

$$h(k) = \lfloor m \cdot ((k \cdot A) \pmod 1) \rfloor$$

* **Advantage**: The choice of table size $m$ is not critical! $m$ can be chosen as a power of two ($m = 2^p$) for fast bitwise implementation.
* **Knuth's Golden Ratio Constant**: Donald Knuth recommended the inverse of the Golden Ratio:
  $$A = \frac{\sqrt{5} - 1}{2} \approx 0.6180339887\dots$$

### 2.3 Universal Hashing
To prevent malicious adversaries from intentionally crafting keys that all hash to the same bucket (causing a Denial of Service attack via $O(N)$ worst-case slowdown), **Universal Hashing** selects a hash function at random at runtime from a carefully designed family of hash functions $\mathcal{H}$.

Let $p$ be a prime number larger than any key universe value $U$. Let $\mathbb{Z}_p = \{0, 1, \dots, p - 1\}$ and $\mathbb{Z}_p^* = \{1, 2, \dots, p - 1\}$.
For any chosen $a \in \mathbb{Z}_p^*$ and $b \in \mathbb{Z}_p$, define the hash function $h_{a,b}(k)$:

$$h_{a,b}(k) = ((a \cdot k + b) \pmod p) \pmod m$$

The family of all such functions is $\mathcal{H}_{p,m}$:

$$\mathcal{H}_{p,m} = \{ h_{a,b} \mid a \in \mathbb{Z}_p^* \quad \text{and} \quad b \in \mathbb{Z}_p \}$$

* **Theorem**: The family $\mathcal{H}_{p,m}$ is **universal**. For any distinct keys $k_1 \neq k_2 \in U$, the probability of a collision is at most $1/m$:

$$P_{h \in \mathcal{H}}(h(k_1) = h(k_2)) \le \frac{1}{m}$$

> **Memory Trick:** **"Division Method wants Prime m! Multiplication Method uses Golden Ratio A ≈ 0.618! Universal Hashing picks random (a*k + b) % p % m!"**

---

## 3. String Hashing & Polynomial Rolling Hash

### 3.1 Polynomial Rolling Hash Mechanics
For a string $S = s_0 s_1 s_2 \dots s_{n-1}$ of length $n$, treating the string as a base-$P$ polynomial yields the **Polynomial Rolling Hash**:

$$\text{Hash}(S) = \left( \sum_{i=0}^{n-1} s_i \cdot P^{n - 1 - i} \right) \pmod{MOD}$$

Or evaluated using Horner's Method:

$$\text{Hash}(S) = (s_0 \cdot P^{n-1} + s_1 \cdot P^{n-2} + \dots + s_{n-1} \cdot P^0) \pmod{MOD}$$

* **Prime Base $P$**: Typically $P = 31$ (for lowercase English) or $P = 53$ (for mixed uppercase/lowercase).
* **Prime Modulus $MOD$**: Typically $MOD = 10^9 + 7$ or $MOD = 10^9 + 9$.

### 3.2 Java's String `hashCode()` Algorithm
Java's `java.lang.String` implements a 32-bit version of Polynomial Rolling Hash using $P = 31$ without explicit modulo division (relying on 32-bit signed integer overflow arithmetic):

$$h(s) = \sum_{i=0}^{n-1} s[i] \cdot 31^{n - 1 - i} = s[0] \cdot 31^{n-1} + s[1] \cdot 31^{n-2} + \dots + s[n-1]$$

Evaluating efficiently using **Horner's Rule**:

$$h(s) = (\dots ((s[0] \cdot 31 + s[1]) \cdot 31 + s[2]) \dots \cdot 31 + s[n-1])$$

#### Why 31?
1. **Prime Multiplier**: 31 is a prime number, reducing hash collisions when hashing strings with common character prefixes/suffixes.
2. **CPU Hardware Optimization**: $31 \cdot i$ can be calculated using a fast bitwise shift and subtraction:
   $$31 \cdot i = (i \ll 5) - i$$
   Modern CPU execution units execute `(i << 5) - i` in a single clock cycle!

```
Polynomial Hash Calculation Trace for "cat":
'c' = 99, 'a' = 97, 't' = 116

Step 1: h = 0
Step 2: h = (0 * 31) + 99 = 99
Step 3: h = (99 * 31) + 97 = 3069 + 97 = 3166
Step 4: h = (3166 * 31) + 116 = 98146 + 116 = 98262

Result: "cat".hashCode() = 98262 ✅
```

---

## 4. Hash Spreading & Bitwise Avalanche Effect

### 4.1 The Avalanche Effect
A hash function exhibits the **Avalanche Effect** if a tiny change in the input (e.g. flipping a single bit) causes approximately 50% of the output bits to flip randomly.

### 4.2 Java 8 `HashMap` Supplemental Hash Spreading
In Java 8's `HashMap`, array capacity $m$ is always a power of two ($2^k$). Index compression uses `hash & (m - 1)`, which inspects ONLY the lowest $k$ bits of the hash code.
If a key object's `hashCode()` differs only in high-order bits, all those keys will map to the exact same bucket!

To solve this, Java applies a **Supplemental Hash Spreading Function**:

```java
static final int hash(Object key) {
    int h;
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

* **XOR Bitwise Mixing (`h ^ (h >>> 16)`)**: Shifts the higher 16 bits of the 32-bit hash code right by 16 bits (`h >>> 16`), and XORs them with the lower 16 bits.
* **Impact**: Ensures that high-bit variations participate in the final index computation `hash & (m - 1)`, drastically reducing collisions for table sizes $m < 65536$!

```
XOR Hash Spreading Mechanics:
Original 32-bit Hash (h)   : 1101 0101 1010 1100  0011 1100 1010 0110
Shifted Right 16 (h >>> 16): 0000 0000 0000 0000  1101 0101 1010 1100
----------------------------------------------------------------------
Mixed Spreading Hash Result: 1101 0101 1010 1100  1110 1001 0000 1010
                                                  ^^^^^^^^^^^^^^^^^^
                                       Lower 16 bits now contain High-Bit Data!
```

---

## 5. Visual Diagram
Java String `hashCode()` Horner Evaluation & Bitwise Index Spreading:

```
String Key: "data"  [ 'd'=100, 'a'=97, 't'=116, 'a'=97 ]

[ HORNER EVALUATION LOOP ]
h = 0
h = (0 * 31) + 100  = 100
h = (100 * 31) + 97 = 3197
h = (3197 * 31) + 116 = 99223
h = (99223 * 31) + 97 = 3076010

Raw Hash Code: 3076010 (Binary: 0000 0000 0010 1110 1111 0011 1010 1010)
                                |------------|-------------|
                                   High 16       Low 16
                                      |             |
                                      v             v
                              [ h ^ (h >>> 16) XOR Spreading ]
                                            |
                                            v
                                 [ Index Mask & (16 - 1) ]
                                            |
                                            v
                                     Bucket Index: 10
```

---

## 6. Operations & Complete Java Implementation
Custom Implementation of Custom Hash Functions for Objects, Strings, and Arrays:

```java
import java.util.Objects;

public class HashFunctionMaster {

    // 1. Custom String Polynomial Rolling Hash (Base 31)
    public static int computeStringHash(String s) {
        if (s == null) return 0;
        int h = 0;
        for (int i = 0; i < s.length(); i++) {
            // Equivalent to h = h * 31 + s.charAt(i) using fast bitwise shift
            h = ((h << 5) - h) + s.charAt(i);
        }
        return h;
    }

    // 2. Supplemental Hash Spreading (Java 8 HashMap Style)
    public static int spreadHash(int hashCode) {
        return hashCode ^ (hashCode >>> 16);
    }

    // 3. Power-of-Two Index Compression
    public static int compressIndex(int spreadHash, int capacity) {
        // Assumes capacity is a power of 2 (e.g. 16, 32, 64)
        return spreadHash & (capacity - 1);
    }

    // 4. Universal Hash Function Implementation h_{a,b}(k) = ((a*k + b) % p) % m
    public static class UniversalHash {
        private final long a;
        private final long b;
        private final long primeP;
        private final int mCapacity;

        public UniversalHash(long a, long b, long primeP, int mCapacity) {
            this.a = a;
            this.b = b;
            this.primeP = primeP;
            this.mCapacity = mCapacity;
        }

        public int hash(int key) {
            long k = key & 0xFFFFFFFFL; // Convert signed int to unsigned long
            long hashedVal = ((a * k + b) % primeP) % mCapacity;
            return (int) hashedVal;
        }
    }

    // 5. Multi-Field Class hashCode Construction (Best Practice)
    public static class Student {
        private final int id;
        private final String name;
        private final double gpa;

        public Student(int id, String name, double gpa) {
            this.id = id;
            this.name = name;
            this.gpa = gpa;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Student student = (Student) o;
            return id == student.id &&
                   Double.compare(student.gpa, gpa) == 0 &&
                   Objects.equals(name, student.name);
        }

        @Override
        public int hashCode() {
            // Objects.hash uses 31 * result + element.hashCode() internally!
            return Objects.hash(id, name, gpa);
        }
    }
}
```

> **Quick Syntax:**
```java
// Hardware Bitwise Shift Equivalent to h * 31
h = ((h << 5) - h) + c;
```

---

## 7. Concrete Problem Examples
* **LeetCode 187 - Repeated DNA Sequences**: Using Polynomial Rolling Hash ($P = 4$ for A, C, G, T) to find 10-letter DNA sequences in $O(N)$ time.
* **LeetCode 28 - Find the Index of the First Occurrence in a String**: Implementing Rabin-Karp algorithm with Polynomial Rolling Hash in $O(N + M)$ time.
* **LeetCode 706 - Design HashMap**: Implementing custom hash function and bucket index compression.

---

## 8. Java Code Demonstration & Dry Run
Complete interview-ready demonstration inspecting Hash Spreading, String Hash distribution, and Avalanche Effect:

```java
public class HashFunctionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. String hashCode() Comparison ===");
        String s1 = "cat";
        String s2 = "tac";
        System.out.println("hashCode('cat'): " + s1.hashCode() + " (Custom: " + HashFunctionMaster.computeStringHash(s1) + ")");
        System.out.println("hashCode('tac'): " + s2.hashCode() + " (Custom: " + HashFunctionMaster.computeStringHash(s2) + ")");

        System.out.println("\n=== 2. Avalanche Effect Demonstration ===");
        String inputA = "Hello World 1";
        String inputB = "Hello World 2"; // Flipped 1 bit at end

        int hashA = HashFunctionMaster.spreadHash(inputA.hashCode());
        int hashB = HashFunctionMaster.spreadHash(inputB.hashCode());

        System.out.println("Hash A Binary: " + String.format("%32s", Integer.toBinaryString(hashA)).replace(' ', '0'));
        System.out.println("Hash B Binary: " + String.format("%32s", Integer.toBinaryString(hashB)).replace(' ', '0'));

        int flippedBits = Integer.bitCount(hashA ^ hashB);
        System.out.println("Flipped Bits Count: " + flippedBits + " / 32 bits (" + (flippedBits * 100 / 32) + "% Avalanche Flipping)");

        System.out.println("\n=== 3. Testing Power-of-Two Compression ===");
        int cap = 16;
        for (String word : new String[]{"apple", "banana", "cherry", "date", "elderberry"}) {
            int rawHash = word.hashCode();
            int spread = HashFunctionMaster.spreadHash(rawHash);
            int idx = HashFunctionMaster.compressIndex(spread, cap);
            System.out.printf("Key: %-10s | Raw Hash: %-11d | Spread: %-11d | Index (cap 16): %d%n", word, rawHash, spread, idx);
        }
    }
}
```

---

## 9. Complexity Analysis

| Hash Function Type | Computational Time | Space Overhead | Collision Resistance Quality |
| :--- | :--- | :--- | :--- |
| **Division Method (`k % m`)** | **$O(1)$ (1 Division)** | $O(1)$ Constant | Poor if $m$ is power of 2 |
| **Multiplication Method** | **$O(1)$ (Multiplication)** | $O(1)$ Constant | High (Knuth Golden Ratio) |
| **Polynomial Rolling Hash** | **$O(L)$ ($L$ string len)** | $O(1)$ Constant | **High (Base 31 Prime)** |
| **Universal Hashing** | **$O(1)$** | $O(1)$ Constant | **Maximum (Guaranteed $1/m$)** |
| **MurmurHash3 / xxHash** | **$O(L)$ (Ultra-Fast)** | $O(1)$ Constant | **Maximum (Cryptographic Grade)**|

---

## 10. Edge Cases & Boundary Handling
* **String Hash Collision Pairs**: Strings `"Aa"` and `"BB"` produce the exact same Java `hashCode()` of `2112`!
  * `'A'*31 + 'a' = 65*31 + 97 = 2015 + 97 = 2112`
  * `'B'*31 + 'B' = 66*31 + 66 = 2046 + 66 = 2112`
  * Always handle hash collisions gracefully; never assume distinct strings yield distinct hash codes!
* **Integer Overflows in Polynomial Hash**: In 32-bit signed arithmetic, large strings overflow integer boundaries into negative numbers. This is harmless if index compression uses `hash & (m - 1)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Math.abs(key.hashCode()) % capacity`**: `Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE` (still negative!), causing `ArrayIndexOutOfBoundsException`!
* **Using Non-Prime Multipliers**: Using an even number (like 30 or 32) as polynomial multiplier loses information because multiplication by an even number shifts bits left, dropping high bits!
* **Ignoring High-Order Bits**: Forgetting bitwise XOR spreading (`h ^ (h >>> 16)`) when using power-of-two array capacities.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `Math.abs(key.hashCode()) % m` is a Bug:
> In Java, `Math.abs(Integer.MIN_VALUE)` is **`-2147483648`** (because positive `2147483648` overflows 32-bit signed int!).
> Taking `-2147483648 % m` returns a **negative array index**, throwing `ArrayIndexOutOfBoundsException`!
> **Fix**: Use `(hashCode & 0x7FFFFFFF) % m` OR power-of-two bitwise mask `spreadHash & (m - 1)`.

> **Memory Trick:** **"Math.abs(Integer.MIN_VALUE) is still NEGATIVE! Use (hash & 0x7FFFFFFF) or hash & (m - 1)!"**

---

## 13. System & Implementation Comparisons

| Feature | Java String `hashCode()` | MurmurHash3 | CityHash / xxHash |
| :--- | :--- | :--- | :--- |
| **Primary Use Case** | Java In-Memory Hash Maps | Redis, Cassandra, RocksDB | High-Throughput Databases |
| **Bitwise Avalanche** | Moderate | **Near Perfect 100%** | **Near Perfect 100%** |
| **Execution Speed** | Moderate ($O(L)$ Horner) | **Extremely Fast** | **Fastest (SIMD Vectorized)** |
| **Output Size** | 32-bit Signed Int | 32-bit / 128-bit | 64-bit / 128-bit |

---

## 14. How to Recognize This in Questions
* **"Find substring patterns in linear time"** $\rightarrow$ Rabin-Karp with Polynomial Rolling Hash.
* **"Design a custom hash map for objects"** $\rightarrow$ Implement `hashCode()` using `Objects.hash()` and XOR spreading.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java 8 `HashMap` use `(h = key.hashCode()) ^ (h >>> 16)`?**  
  *A:* Because `HashMap` uses capacity $m = 2^k$ and index mask `h & (m - 1)`, which reads only the lowest $k$ bits. XORing the top 16 bits into the bottom 16 bits ensures that variations in high-order bits participate in index calculation, preventing collisions when lower bits are identical.
* **Q: Why is 31 used as the multiplier in String `hashCode()`?**  
  *A:* (1) 31 is an odd prime, reducing hash collisions. (2) $31 \cdot i = (i \ll 5) - i$, allowing CPUs to compute multiplication using a single fast bitwise shift and subtraction.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASH FUNCTIONS & ROLLING HASH                         |
+-----------------------------------------------------------------------+
| • Simple Uniform Hashing: Keys distribute evenly across 0..m-1        |
| • Polynomial Rolling Hash: Hash(S) = sum(s[i] * P^(n-1-i))            |
| • Java String hashCode: Uses multiplier 31 -> (h << 5) - h + char     |
| • Why 31? Prime number + fast bitwise hardware shift (i << 5) - i     |
| • XOR Spreading (Java 8): h ^ (h >>> 16) mixes high 16 bits into low  |
| • Power-of-Two Index Mask: index = spreadHash & (capacity - 1)        |
| • Math.abs Bug: Math.abs(Integer.MIN_VALUE) is NEGATIVE!              |
|   Always use (hash & 0x7FFFFFFF) % m OR hash & (m - 1)                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Polynomial Rolling Hash formula and Horner's rule.
- [ ] I know why 31 is used in Java's String `hashCode()` (`(i << 5) - i`).
- [ ] I can write Java 8's hash spreading function `h ^ (h >>> 16)`.
- [ ] I know why `Math.abs(Integer.MIN_VALUE)` fails and how to fix it.
- [ ] I can implement a Universal Hash Function `((a * k + b) % p) % m`.
- [ ] I know why strings `"Aa"` and `"BB"` produce identical hash code `2112`.
