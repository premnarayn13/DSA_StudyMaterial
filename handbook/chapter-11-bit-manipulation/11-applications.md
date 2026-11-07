# 11. Systems & Applications: Bloom Filters, CIDR Subnetting & POSIX Permission Bitmasks

## 1. Introduction
**Bit Manipulation** is not merely an abstract interview topic; it forms the backbone of real-world low-level systems engineering, database engines, networking protocols, operating system kernels, and high-frequency trading platforms. Operating directly on primitive bit vectors allows computer systems to achieve maximum space compression and execution speed. Key production applications include:
1. **Bloom Filters**: Probabilistic data structures that test set membership using $K$ hash functions mapped onto a single $M$-bit vector, achieving over **99% memory savings** compared to standard HashSets.
2. **Network CIDR Subnetting**: Calculating IPv4 network addresses (`ip & mask`), broadcast addresses (`ip | ~mask`), and host ranges in $O(1)$ bitwise operations.
3. **POSIX File System Permissions**: Managing Read/Write/Execute (`rwx`) flags using 9-bit permission masks (`0755` = `rwxr-xr-x`).
4. **Memory-Mapped I/O (MMIO) Driver Control**: Toggling hardware register control flags in embedded operating systems.

> **Important:** Core Systems Bitmask Formulas:
> 1. **Network Subnetting Formulas**:
>    - Network Base Address: $\text{networkIP} = \text{ipAddress} \;\&\; \text{subnetMask}$
>    - Broadcast Address: $\text{broadcastIP} = \text{ipAddress} \mid (\sim\text{subnetMask})$
> 2. **POSIX Permission Bitmasks**:
>    - Read Bit (4): `0b100`, Write Bit (2): `0b010`, Execute Bit (1): `0b001`.
>    - User, Group, Others packed into 9-bit mask: `(Owner << 6) | (Group << 3) | Others`.
> 3. **Bloom Filter Bit Set Rule**:
>    - For item $X$, set bits at indices $h_1(X) \pmod M \dots h_K(X) \pmod M$:
>      $$\text{bitSet.set}(h_i(X) \pmod M)$$ ⚡

```
Production Bitmask Architecture Topology:

POSIX 9-Bit File Permissions Layout:
  Owner (rwx)      Group (r-x)     Others (r-x)
┌───────────────┬───────────────┬───────────────┐
│ 1   1   1     │ 1   0   1     │ 1   0   1     │  = Octal 0755 (rwxr-xr-x)
└───────────────┴───────────────┴───────────────┘
  r   w   x       r   w   x       r   w   x

Single 16-bit Short stores full permission mask for User, Group, and Others! ⚡
```

---

## 2. Core Concepts & Production Bitmask Systems Strategy Matrix

### 2.1 Production Bitmask Systems Strategy Matrix
```
Production Bitmask Systems Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Production System     | Bitmask Structure | Core Bit Operation| Memory Savings    | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Bloom Filter**      | $M$-bit `BitSet`  | `bitSet.set(h(x))`| **> 99% Compression⚡**| **$O(K)$ Hashes ⚡**|
| **CIDR Subnetting**   | 32-bit Integer IP | `ip & mask`       | **$O(1)$ Memory ⚡**| **$O(1)$ Single Op ⚡**|
| **POSIX File System** | 9-bit Permission  | `mask & READ_BIT` | **Compact Integer ⚡**| **$O(1)$ Single Op ⚡**|
| **Hardware Driver**   | 32-bit MMIO Reg   | `reg |= (1 << k)` | Hardware Direct   | **$O(1)$ Clock Cycle⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Bloom Filters use BitSet for 99% memory savings; Subnet IP = ip & mask; Broadcast IP = ip | ~mask!"**

---

## 3. Characteristics & Bloom Filter False Positive Math

### 3.1 Mathematical Derivation of Bloom Filter False Positive Probability
* Let $M$ be the bit array size in bits, $N$ be the number of inserted elements, and $K$ be the number of hash functions.
* Probability that a specific bit is NOT set by a single hash function:
  $$P(\text{not set}) = 1 - \frac{1}{M}$$
* Probability that a bit is NOT set after $N$ elements (using $K$ hash functions):
  $$P(\text{still zero}) = \left(1 - \frac{1}{M}\right)^{KN} \approx e^{-\frac{KN}{M}}$$
* **False Positive Rate $P_{fp}$**:
  - A false positive occurs when all $K$ hash positions for an uninserted item happen to be 1:
    $$P_{fp} = (1 - P(\text{still zero}))^K \approx \left(1 - e^{-\frac{KN}{M}}\right)^K$$
* **Optimal Number of Hash Functions $K_{\text{opt}}$**:
  $$K_{\text{opt}} = \frac{M}{N} \ln 2 \approx 0.7 \times \frac{M}{N}$$
* Provides deterministic, controllable false positive rates in minimal RAM! ⚡

---

## 4. Internal Working Mechanics: IPv4 Subnet Masking Calculation

Tracing IPv4 Address `192.168.1.10` with CIDR `/24` (`255.255.255.0`):

```
IP Address:  192.168.1.10   (11000000 10101000 00000001 00001010_2)
Subnet Mask: 255.255.255.0  (11111111 11111111 11111111 00000000_2)

1. Network Base Address (IP & Mask):
   11000000 10101000 00000001 00001010 (IP)
 & 11111111 11111111 11111111 00000000 (Mask)
 ─────────────────────────────────────
   11000000 10101000 00000001 00000000 ──► 192.168.1.0 ✅ ⚡

2. Broadcast Address (IP | ~Mask):
   ~Mask = 00000000 00000000 00000000 11111111
   11000000 10101000 00000001 00001010 (IP)
 | 00000000 00000000 00000000 11111111 (~Mask)
 ─────────────────────────────────────
   11000000 10101000 00000001 11111111 ──► 192.168.1.255 ✅ ⚡
```

---

## 5. Visual Diagram: Bloom Filter Membership Insertion

```
Bloom Filter Bit Array (M = 12 Bits):

Bit Index:  0  1  2  3  4  5  6  7  8  9  10 11
Bit Array: [0  1  0  0  1  0  0  1  0  0  1  0]
               ▲        ▲        ▲        ▲
               │        │        │        │
           h1("cat") h2("cat") h1("dog") h2("dog")

Item "cat" hashes to bits {1, 4} ──► Bits 1 and 4 set to 1!
Item "dog" hashes to bits {7, 10} ──► Bits 7 and 10 set to 1!
Check "fox" -> Hashes to {1, 8} -> Bit 8 is 0 ──► "fox" DEFINITELY NOT IN SET! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing a Production Bloom Filter, IPv4 CIDR Subnet Calculator, and POSIX File Permission System.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Systems Bitmask Applications:
 * Bloom Filter, IPv4 CIDR Subnet Calculator, and POSIX Permission System.
 */
public class SystemsBitmaskMaster {

    // =========================================================================
    // 1. PRODUCTION BLOOM FILTER (PROBABILISTIC BITSET)
    // =========================================================================
    public static class BloomFilter<T> {
        private final BitSet bitSet;
        private final int bitSetSize;
        private final int numHashFunctions;

        public BloomFilter(int bitSetSize, int numHashFunctions) {
            this.bitSetSize = bitSetSize;
            this.numHashFunctions = numHashFunctions;
            this.bitSet = new BitSet(bitSetSize);
        }

        public void add(T item) {
            int[] hashes = getHashes(item);
            for (int h : hashes) {
                bitSet.set(Math.abs(h % bitSetSize)); // Set bit in BitSet ⚡
            }
        }

        public boolean mightContain(T item) {
            int[] hashes = getHashes(item);
            for (int h : hashes) {
                if (!bitSet.get(Math.abs(h % bitSetSize))) {
                    return false; // DEFINITELY NOT IN SET! ⚡
                }
            }
            return true; // PROBABLY IN SET!
        }

        private int[] getHashes(T item) {
            int[] hashes = new int[numHashFunctions];
            int h1 = item.hashCode();
            int h2 = Integer.rotateLeft(h1, 13);
            for (int i = 0; i < numHashFunctions; i++) {
                hashes[i] = h1 + i * h2; // Double hashing technique ⚡
            }
            return hashes;
        }
    }

    // =========================================================================
    // 2. IPV4 CIDR SUBNET CALCULATOR
    // =========================================================================
    public static class SubnetInfo {
        public final String networkIP;
        public final String broadcastIP;
        public final int hostCount;

        public SubnetInfo(String networkIP, String broadcastIP, int hostCount) {
            this.networkIP = networkIP;
            this.broadcastIP = broadcastIP;
            this.hostCount = hostCount;
        }
    }

    public SubnetInfo calculateSubnet(String ipAddress, int prefixLength) {
        int ip = parseIP(ipAddress);
        int mask = (prefixLength == 0) ? 0 : (0xFFFFFFFF << (32 - prefixLength));

        int network = ip & mask;      // Network Base IP (IP & Mask) ⚡
        int broadcast = ip | (~mask); // Broadcast IP (IP | ~Mask) ⚡
        int hostCount = (prefixLength >= 31) ? 0 : (1 << (32 - prefixLength)) - 2;

        return new SubnetInfo(formatIP(network), formatIP(broadcast), hostCount);
    }

    private int parseIP(String ipStr) {
        String[] parts = ipStr.split("\\.");
        int ip = 0;
        for (int i = 0; i < 4; i++) {
            ip |= (Integer.parseInt(parts[i]) << (24 - i * 8));
        }
        return ip;
    }

    private String formatIP(int ip) {
        return String.format("%d.%d.%d.%d",
            (ip >>> 24) & 0xFF,
            (ip >>> 16) & 0xFF,
            (ip >>> 8) & 0xFF,
            ip & 0xFF
        );
    }

    // =========================================================================
    // 3. POSIX FILE PERMISSION BITMASK ENGINE
    // =========================================================================
    public static final int READ = 4;    // 100_2
    public static final int WRITE = 2;   // 010_2
    public static final int EXECUTE = 1; // 001_2

    public int createPermissionMask(int owner, int group, int others) {
        return (owner << 6) | (group << 3) | others; // Pack into 9-bit integer ⚡
    }

    public boolean canOwnerWrite(int modeMask) {
        return ((modeMask >>> 6) & WRITE) != 0;
    }
}
```

> **Quick Syntax:**
```java
// Production Systems Bitmask Lines
int networkIP = ip & mask; int broadcastIP = ip | (~mask); int permMask = (owner << 6) | (group << 3) | others;
```

---

## 7. Concrete Problem Examples & Applications

1. **Production Bloom Filters (Redis, Cassandra, Chrome)**:
   - Eliminating unnecessary disk/network reads by testing key presence.

2. **IPv4 CIDR Subnet Calculators**:
   - Network routing table lookups ($O(1)$ time).

3. **POSIX File System Permissions (`chmod`)**:
   - Compact file access control bits.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class SystemsBitmaskDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SYSTEMS BITMASK APPLICATIONS DEMO             ");
        System.out.println("=================================================\n");

        SystemsBitmaskMaster master = new SystemsBitmaskMaster();

        // 1. Bloom Filter Test
        SystemsBitmaskMaster.BloomFilter<String> bloom = new SystemsBitmaskMaster.BloomFilter<>(1000, 3);
        bloom.add("user_101");
        bloom.add("user_202");

        System.out.println("1. Bloom Filter Set Membership Test:");
        System.out.println("   Might Contain 'user_101': " + bloom.mightContain("user_101") + " (Optimal = true)");
        System.out.println("   Might Contain 'user_999': " + bloom.mightContain("user_999") + " (Optimal = false)");
        System.out.println("-------------------------------------------------");

        // 2. IPv4 CIDR Subnet Test
        String ip = "192.168.1.10";
        int prefix = 24;
        SystemsBitmaskMaster.SubnetInfo subnet = master.calculateSubnet(ip, prefix);

        System.out.println("2. IPv4 CIDR Subnet Calculator for " + ip + "/" + prefix + ":");
        System.out.println("   Network Base Address : " + subnet.networkIP);
        System.out.println("   Broadcast Address    : " + subnet.broadcastIP);
        System.out.println("   Usable Hosts Count   : " + subnet.hostCount);
        System.out.println("-------------------------------------------------");

        // 3. POSIX Permission Test
        int mode = master.createPermissionMask(7, 5, 5); // 0755
        System.out.println("3. POSIX Permission Bitmask Test (0755 rwxr-xr-x):");
        System.out.println("   Can Owner Write: " + master.canOwnerWrite(mode) + " (Optimal = true)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Production System | Bitwise Operation | Time Complexity | Memory Savings |
| :--- | :--- | :--- | :--- |
| **Bloom Filter** | `bitSet.set(h(x))` | $\mathbf{O(K)}$ Hashes ⚡| **> 99% Compression ⚡**|
| **CIDR Subnetting** | `ip & mask` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory |
| **POSIX Permission** | `(owner << 6) | (group << 3) | others`| $\mathbf{O(1)}$ Single CPU Cycle⚡| Compact 9-bit Int |

---

## 10. Edge Cases & Boundary Handling

1. **Subnet Prefix `/32` (Single Host)**:
   - Subnet mask is `0xFFFFFFFF`, usable host count is 0.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Assuming a Bloom Filter Can Return False Negatives**:
  - Bloom filters NEVER produce false negatives (`mightContain` returning `false` guarantees item is 100% NOT in set). They can only produce false positives!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Bloom Filter Guarantee Rule:
> * If Bloom Filter returns **`false`**, the item is **100% GUARANTEED NOT IN SET** (No False Negatives!).
> * If Bloom Filter returns **`true`**, the item is **PROBABLY IN SET** (Subject to controlled False Positive Rate). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | HashSet | Bloom Filter |
| :--- | :--- | :--- |
| **Memory Footprint** | Large Pointer Overhead | **Tiny Bit Array (>99% Savings) ⚡** |
| **False Negatives** | None | **None (100% Guaranteed) ⚡** |
| **False Positives** | None | Low (Controllable $P_{fp}$) |

---

## 14. How to Recognize This in Questions

* **"Design space-efficient probabilistic set checker for 1 billion keys"** $\rightarrow$ Bloom Filter.

---

## 15. Frequently Asked Interview Questions

* **Q: Why are Bloom Filters preferred in distributed databases like Cassandra and HBase?**  
  *A:* Because testing a Bloom Filter in RAM takes microseconds and avoids expensive disk I/O reads for keys that do not exist on disk.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SYSTEMS BITMASK APPLICATIONS                          |
+-----------------------------------------------------------------------+
| • Bloom Filter : BitSet(M) + K Hashes -> NO FALSE NEGATIVES! ⚡        |
| • Subnet Base  : networkIP = ip & mask                                |
| • Broadcast IP : broadcastIP = ip | (~mask)                           |
| • POSIX Mode   : (owner << 6) | (group << 3) | others (Octal 0755)   |
| • Performance  : Executes in O(1) single CPU clock cycles! ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write a Bloom Filter using Java's `BitSet`.
- [ ] I can write IPv4 network and broadcast address calculators.
- [ ] I can explain why Bloom Filters have zero false negatives.
- [ ] I can write a POSIX permission bitmask packer and unpacker.
- [ ] I can calculate optimal hash functions count for a Bloom Filter.
