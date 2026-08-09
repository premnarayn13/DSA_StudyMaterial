# 02. Hash Functions, Bitwise Bit-Spreading & Polynomial Rolling Hash Mechanics

## 1. Introduction
A **Hash Function** $h(k)$ is a deterministic mathematical mapping that transforms an arbitrary input key $k$ (string, integer, complex object) into a 32-bit signed integer hash code. Designing robust hash functions—such as **Polynomial Rolling Hashing**, **Java 8 Supplemental XOR Bit-Spreading (`h ^ (h >>> 16)`)**, and **Multiplicative Knuth Hashing**—is essential for achieving uniform bucket distribution, eliminating systematic collision clustering, and maintaining **$O(1)$ constant time Hash Map performance**.

> **Important:** In Java 8 `HashMap`, why is the supplemental hash function **`h ^ (h >>> 16)`** applied to a key's `hashCode()`?
> For power-of-2 table capacities ($C = 2^k$), index calculation uses bitwise masking: `idx = (capacity - 1) & h`.
> Without bit-spreading, ONLY the lowest $k$ bits of `h` participate in index selection, causing massive collisions if higher bits vary!
> XORing the higher 16 bits into the lower 16 bits (`h ^ (h >>> 16)`) spreads top-bit entropy into lower bits! ⚡

```
Java 8 Supplemental Hash Bit-Spreading (`h ^ (h >>> 16)`):
32-Bit Hash Code h : [ High 16 Bits (Entropy) ] | [ Low 16 Bits ]
h >>> 16           : [ 0000000000000000 ] | [ High 16 Bits (Shifted) ]
h ^ (h >>> 16)     : Mixed High & Low Entropy in Lower 16 Bits! ⚡
```

---

## 2. Core Concepts & Hash Function Taxonomy

### 2.1 The 4 Primary Hash Function Families
1. **Division Method**: $h(k) = k \bmod M$. Simple, but vulnerable to clustering if $M$ shares common factors with keys. Best when $M$ is a **Prime Number**.
2. **Multiplicative Method (Knuth)**: $h(k) = \lfloor M (k \cdot A \bmod 1) \rfloor$, where $A = (\sqrt{5} - 1) / 2 \approx 0.6180339887$ (Golden Ratio).
3. **Polynomial Rolling Hash (Strings)**: Computes hash of string $S = s_0 s_1 \dots s_{n-1}$ using base prime $P$ and modulo $M$:
   $$h(S) = \sum_{i=0}^{n-1} s_i \cdot P^{n-1-i} \bmod M$$
4. **Bitwise Bit-Spreading (Java HashMap)**: Applies bitwise right shifts and XORs (`h ^ (h >>> 16)`) to randomize hash distributions across power-of-2 bucket arrays.

```
Hash Function Characteristics Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Hash Family           | Computation Speed | Collision Uniform | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| Division (Prime M)    | Fast              | Moderate          | Basic Integer Hash|
| Knuth Multiplicative  | **Fast ⚡**       | **High ⚡**       | Power-of-2 Arrays |
| Polynomial String     | Moderate          | **High ⚡**       | Strings / Substrings|
| MurmurHash3 / CityHash| High-Speed        | **Optimal ⚡**    | Production Databases|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Polynomial String Hash uses prime multiplier 31! Java HashMap uses h ^ (h >>> 16) to spread high-bit entropy!"**

---

## 3. Characteristics & String Polynomial Hash Code Mechanics

### 3.1 Why Java String Uses Multiplier 31 (`s[0]*31^(n-1) + s[1]*31^(n-2) + ...`)
In Java's `String.hashCode()` implementation:

$$h(S) = s[0] \cdot 31^{n-1} + s[1] \cdot 31^{n-2} + \dots + s[n-1]$$

#### Why Prime 31?
1. **Prime Multiplier**: Primes prevent common factor cancellation during modulo arithmetic, yielding superior uniform distribution.
2. **CPU Bit-Shift Optimization**: $31 \times i$ can be replaced by CPU bitwise shift and subtraction:
   $$31 \cdot i = (i \ll 5) - i$$
   Modern compilers auto-optimize $31 \cdot i$ into 1 CPU clock cycle!

```java
// Production Java String hashCode() Logic
public static int computeStringHashCode(String s) {
    int h = 0;
    for (int i = 0; i < s.length(); i++) {
        h = 31 * h + s.charAt(i); // 31 * h == (h << 5) - h
    }
    return h;
}
```

---

## 4. Internal Working Mechanics
Tracing Polynomial String Hash Computation on $S = \text{"cat"}$:

```
Characters: 'c' (ASCII 99), 'a' (ASCII 97), 't' (ASCII 116)
Init: h = 0

Char 1 ('c'): h = 31 * 0 + 99 = 99.
Char 2 ('a'): h = 31 * 99 + 97 = 3069 + 97 = 3166.
Char 3 ('t'): h = 31 * 3166 + 116 = 98146 + 116 = 98262.

Final Hash Code for "cat" = 98262 ✅ (Executed in O(N) Time!)
```

---

## 5. Visual Diagram
Java Supplemental Hash Bitwise XOR Bit-Spreading Topography:

```
Original Hash Code h : 1111 0000 1010 0101   0000 1111 1100 0011
h >>> 16             : 0000 0000 0000 0000   1111 0000 1010 0101
                      ------------------------------------------
h ^ (h >>> 16)       : 1111 0000 1010 0101   1111 1111 0110 0110
                                             ^^^^^^^^^^^^^^^^^^^^
                                     High 16-bit entropy mixed into lower bits! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Polynomial String Hashing, Knuth Multiplicative Hashing, and Java 8 Supplemental Bit-Spreading:

```java
import java.util.*;

public class HashFunctionsMaster {

    // 1. Production Polynomial String Hash (Base 31) O(N) Time
    public static int polyStringHash(String s) {
        if (s == null) return 0;
        int h = 0;
        for (int i = 0; i < s.length(); i++) {
            h = 31 * h + s.charAt(i); // (h << 5) - h
        }
        return h;
    }

    // 2. Java 8 HashMap Supplemental Bit-Spreading Function
    public static int java8SupplementalHash(Object key) {
        if (key == null) return 0;
        int h = key.hashCode();
        return h ^ (h >>> 16); // Mixes top 16 bits into lower 16 bits
    }

    // 3. Knuth Multiplicative Hash (Golden Ratio A = 2654435769L)
    public static int knuthMultiplicativeHash(int key, int capacityPowerOfTwo) {
        // Golden Ratio constant 2654435769L = (2^32 * (sqrt(5) - 1) / 2)
        long knuthConstant = 2654435769L;
        long hash = (key * knuthConstant) & 0xFFFFFFFFL;
        int shift = 32 - Integer.numberOfTrailingZeros(capacityPowerOfTwo);
        return (int) (hash >>> shift);
    }

    // 4. Custom Object hashCode() and equals() Implementation
    public static class PersonKey {
        private final int id;
        private final String name;

        public PersonKey(int id, String name) {
            this.id = id;
            this.name = (name == null) ? "" : name;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            PersonKey personKey = (PersonKey) o;
            return id == personKey.id && Objects.equals(name, personKey.name);
        }

        @Override
        public int hashCode() {
            // Combine fields using prime 31
            int result = Integer.hashCode(id);
            result = 31 * result + name.hashCode();
            return result;
        }

        @Override
        public String toString() {
            return "PersonKey{id=" + id + ", name='" + name + "'}";
        }
    }
}
```

> **Quick Syntax:**
```java
// Combining Hash Codes for Multiple Fields
int result = Integer.hashCode(field1);
result = 31 * result + Objects.hashCode(field2);
```

---

## 7. Concrete Problem Examples
* **Rabin-Karp String Matching Algorithm**: Polynomial rolling hash.
* **Java 8 `java.util.HashMap`**: `h ^ (h >>> 16)` supplemental hashing.
* **MurmurHash3 / CityHash**: Non-cryptographic fast hash tables in C++/Rust.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing Polynomial Hashing, Supplemental Bit-Spreading, and Custom Object Hash Codes:

```java
public class HashFunctionsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Polynomial String Hash (\"cat\") ===");
        int strHash = HashFunctionsMaster.polyStringHash("cat");
        System.out.println("Hash Code for \"cat\": " + strHash); // Output: 98262

        System.out.println("\n=== 2. Java 8 Supplemental Bit-Spreading ===");
        int rawHash = 0b11110000101001010000111111000011;
        int spreadHash = HashFunctionsMaster.java8SupplementalHash(rawHash);
        System.out.println("Raw Hash:    " + Integer.toBinaryString(rawHash));
        System.out.println("Spread Hash: " + Integer.toBinaryString(spreadHash));

        System.out.println("\n=== 3. Custom PersonKey Hash Contract ===");
        HashFunctionsMaster.PersonKey p1 = new HashFunctionsMaster.PersonKey(101, "Alice");
        HashFunctionsMaster.PersonKey p2 = new HashFunctionsMaster.PersonKey(101, "Alice");
        System.out.println("p1.equals(p2): " + p1.equals(p2));                // true
        System.out.println("p1.hashCode(): " + p1.hashCode());              // Same hash code!
        System.out.println("p2.hashCode(): " + p2.hashCode());              // Same hash code!
    }
}
```

---

## 9. Complexity Analysis

| Hash Function Variant | Time Complexity | Bitwise Operations | Quality Factor |
| :--- | :--- | :--- | :--- |
| **Polynomial String (31)** | **$O(N)$ Linear ⚡** | `(h << 5) - h` (1 Shift) | High Uniformity |
| **Supplemental `h ^ (h>>>16)`**| **$O(1)$ Constant ⚡**| 1 Shift + 1 XOR | Eliminates Low-bit Bias |
| **Knuth Multiplicative** | **$O(1)$ Constant ⚡**| 1 Mult + 1 Shift | High Power-of-2 Quality |

---

## 10. Edge Cases & Boundary Handling
* **Negative Integer Hash Codes**: Hash codes in Java can be negative. Always convert to positive index: `Math.abs(hash) % capacity` or `hash & 0x7FFFFFFF`.
* **Null Key Hashing**: Handled via `if (key == null) return 0;`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Math.abs(Integer.MIN_VALUE)` for Index Math**:
  - `Math.abs(Integer.MIN_VALUE)` returns `Integer.MIN_VALUE` (still negative!), causing `ArrayIndexOutOfBoundsException`!
  - **Use `(hash & 0x7FFFFFFF) % capacity` to clear the 32-bit sign bit reliably**.
* **Using Non-Prime Multipliers in Polynomial String Hashing**:
  - Using even multipliers (like 2, 4, 8) causes bit shifts that discard higher character bits over long strings!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** How to Clear the Sign Bit Safely in Java:
> `Integer.MIN_VALUE` is `-2147483648` (`0x80000000`). Calling `Math.abs(Integer.MIN_VALUE)` overflows back to `-2147483648`!
> To reliably clear the negative sign bit in 32-bit integers:
> **`int positiveHash = hash & 0x7FFFFFFF;`**
> This binary AND forces the 31st sign bit to `0` guaranteed!

> **Memory Trick:** **"Always use (hash & 0x7FFFFFFF) % capacity to clear sign bits safely!"**

---

## 13. System & Implementation Comparisons

| Feature | `(hash & 0x7FFFFFFF) % C` | `Math.abs(hash) % C` |
| :--- | :--- | :--- |
| **Safety on `Integer.MIN_VALUE`** | **100% Safe (Returns positive) ⚡**| Fails (Returns negative index!) |
| **CPU Instruction Cost** | **1 Bitwise AND Instruction ⚡**| Branching Condition |
| **Code Footprint** | Idiomatic Bitwise Mask | Standard Library Function |

---

## 14. How to Recognize This in Questions
* **"Design a custom hashCode() for multi-field class"** $\rightarrow$ Combine fields using prime 31 multiplier.
* **"Explain why Java 8 HashMap uses h ^ (h >>> 16)"** $\rightarrow$ Bitwise XOR bit-spreading to mix high-bit entropy into lower bits.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java 8 HashMap use `(capacity - 1) & hash` instead of `hash % capacity`?**  
  *A:* When capacity is a power of 2 ($2^k$), `(capacity - 1) & hash` evaluates in **1 CPU clock cycle** (Bitwise AND), compared to 15–30 CPU cycles for integer modulo division (`%`).
* **Q: What is Hash Flooding / Hash DoS Attack?**  
  *A:* An attacker crafts thousands of keys that produce the exact same `hashCode()`, degrading a web application's `HashMap` lookup time from $O(1)$ down to $O(N)$ linear time, causing CPU exhaustion.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASH FUNCTIONS & BIT-SPREADING                       |
+-----------------------------------------------------------------------+
| • Java String Multiplier: Prime 31 -> 31 * h == (h << 5) - h          |
| • Java 8 Bit-Spreading: h ^ (h >>> 16) mixes high bits into low bits   |
| • Power of 2 Index Mask: idx = (capacity - 1) & hash                  |
| • Sign Bit Removal: Use (hash & 0x7FFFFFFF) to prevent negative MIN_VAL|
| • Hash Contract: Equal objects MUST produce equal hash codes!          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a polynomial string hash function using prime 31.
- [ ] I can explain why Java 8 uses `h ^ (h >>> 16)` bit-spreading.
- [ ] I know why `Math.abs(Integer.MIN_VALUE)` fails and how `& 0x7FFFFFFF` fixes it.
- [ ] I can write a custom `hashCode()` and `equals()` method for a multi-field class.
- [ ] I know why power-of-2 bitwise AND masking is faster than modulo.
