# 14. System Applications: Consistent Hashing, Bloom Filters & Distributed Hash Tables

## 1. Introduction
In large-scale distributed systems and database architectures, Advanced Hashing Algorithms manage distributed data partitioning, load balancing, fast membership testing, and rate limiting. Key industrial architectures include **Consistent Hashing with Virtual Nodes** (used in Apache Cassandra, Amazon DynamoDB, and Akamai CDNs), **Bloom Filters** (probabilistic constant-time set membership in RocksDB and Google Chrome), and **Distributed Hash Tables (DHTs / Kademlia)**.

> **Important:** Why does Traditional Modulo Partitioning ($\text{Node} = h(\text{key}) \bmod N$) fail in distributed systems?
> When a single cache server node is added or removed ($N \to N + 1$ or $N \to N - 1$), **OVER 99% OF ALL KEYS MAP TO DIFFERENT NODES**, causing a catastrophic cache stampede!
> **Consistent Hashing** ensures that adding or removing a node re-maps ONLY $1/N$-th of the keys! ⚡

```
Consistent Hashing Ring & Virtual Node Architecture:
Ring Space: 0 --------------------------------------------------> 2^32 - 1
Node A_v1 (Idx 1000) ---> Node B_v1 (Idx 5000) ---> Node A_v2 (Idx 9000)
                              ^
Key "User123" (Hash 3500) ----+  (Clockwise routing maps Key to Node B_v1!) ⚡
```

---

## 2. Core Concepts & Consistent Hashing Ring Topology

### 2.1 Consistent Hashing with Virtual Nodes
* **Hash Ring Space**: Key space is mapped to a circular integer range $[0 \dots 2^{32} - 1]$.
* **Node Placement**: Server nodes are hashed onto the ring using their IP or ID: $h(\text{node\_ip})$.
* **Clockwise Key Routing**: A data key is mapped to $h(\text{key})$ and routed **Clockwise** to the first server node whose ring position is $\ge h(\text{key})$.
* **Virtual Nodes (`vnodes`)**: Each physical server is assigned $V$ virtual replica positions on the ring (e.g. `NodeA_v1`, `NodeA_v2`).
  - **Benefit**: Virtual nodes guarantee uniform load distribution and prevent "hotspots" where 1 physical node receives disproportionate traffic!

```
Consistent Hashing vs Traditional Modulo Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature Metrics       | Traditional Modulo| Consistent Hashing| VNode Consistent  |
+-----------------------+-------------------+-------------------+-------------------+
| Keys Moved on Resize  | ~100% (Catastrophic)| $1/N$ (Minimal)   | **$1/N$ Uniform ⚡**|
| Load Uniformity       | High              | Poor (Hotspots)   | **Optimal ⚡**    |
| Lookup Complexity     | $O(1)$ Direct     | $O(\log N)$ Ring  | **$O(\log(N \cdot V))$ ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Consistent Hashing re-maps ONLY 1/N keys on server failure! Virtual nodes eliminate hotspots!"**

---

## 3. Characteristics & Bloom Filter Probabilistic Set Membership

### 3.1 Bloom Filters (Zero False Negatives, Controlled False Positives)
A **Bloom Filter** is a space-efficient probabilistic data structure that tests whether an element is a member of a set:
* **Guarantees**:
  - **NO False Negatives**: If Bloom Filter returns `false` ("Not Present"), the element is **DEFINITELY NOT** in the set!
  - **Possible False Positives**: If Bloom Filter returns `true` ("Present"), the element is **PROBABLY** in the set (requires disk lookup to confirm).
* **Architecture**: Bit Array $B$ of size $M$ + $K$ independent hash functions ($h_1, h_2 \dots h_k$).
* **Insertion**: For key $x$, set bits $B[h_1(x)], B[h_2(x)] \dots B[h_k(x)] = 1$.
* **Lookup**: Check if all bits $B[h_i(x)] == 1$. If ANY bit is 0, return `false` guaranteed!

```
Optimal Hash Functions Formula for False Positive Rate $p$:
$$K = \frac{M}{N} \ln 2 \approx 0.7 \times \frac{M}{N}$$
```

---

## 4. Internal Working Mechanics
Tracing Consistent Hashing Ring Lookup using `TreeMap` in Java:

```
Nodes Added: ServerA (vnodes: A_v1@100, A_v2@700), ServerB (vnodes: B_v1@400)
TreeMap Ring Keys: {100: "ServerA", 400: "ServerB", 700: "ServerA"}

Lookup Key "DataKey":
1. Compute Hash: h("DataKey") = 350.
2. Query TreeMap tailMap: ring.ceilingKey(350) -> Returns 400 ("ServerB").
3. Route Key to ServerB!

If 350 > max ring key (700):
Wrap around! Take ring.firstKey() -> 100 ("ServerA").

Routing completes in O(log(N * V)) Logarithmic Time! ✅
```

---

## 5. Visual Diagram
Bloom Filter Bit Array Insertion & Verification Topography:

```
Bit Array (M = 8): [ 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 ]
                         ^       ^           ^
                     h1("Key") h2("Key")  h3("Key")

Lookup "Key" : Bits 1, 3, 6 are ALL 1 -> Returns TRUE (Probably Present).
Lookup "Key2": Bit 0 is 0           -> Returns FALSE (DEFINITELY NOT PRESENT!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementations of Consistent Hashing with Virtual Nodes and a BitSet-based Bloom Filter:

```java
import java.util.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class SystemApplicationsHashingMaster {

    // 1. Production Consistent Hashing Engine with Virtual Nodes O(log(N*V))
    public static class ConsistentHashRing {
        private final NavigableMap<Long, String> ring = new TreeMap<>();
        private final int virtualNodesPerServer;

        public ConsistentHashRing(int virtualNodesPerServer) {
            this.virtualNodesPerServer = virtualNodesPerServer;
        }

        public void addServer(String serverIp) {
            for (int i = 0; i < virtualNodesPerServer; i++) {
                String vNodeName = serverIp + "#VN" + i;
                long hash = hash(vNodeName);
                ring.put(hash, serverIp);
            }
        }

        public void removeServer(String serverIp) {
            for (int i = 0; i < virtualNodesPerServer; i++) {
                String vNodeName = serverIp + "#VN" + i;
                long hash = hash(vNodeName);
                ring.remove(hash);
            }
        }

        // Clockwise Routing to Nearest Node
        public String getServer(String key) {
            if (ring.isEmpty()) return null;

            long hash = hash(key);
            // Find first node with ring position >= key hash
            Long targetHash = ring.ceilingKey(hash);

            // Wrap around ring if key hash exceeds largest node position
            if (targetHash == null) {
                targetHash = ring.firstKey();
            }

            return ring.get(targetHash);
        }

        // 64-Bit MD5 Hash Function for Ring Uniformity
        private long hash(String input) {
            try {
                MessageDigest md = MessageDigest.getInstance("MD5");
                byte[] bytes = md.digest(input.getBytes());
                return ((long) (bytes[3] & 0xFF) << 24) |
                       ((long) (bytes[2] & 0xFF) << 16) |
                       ((long) (bytes[1] & 0xFF) << 8)  |
                       ((long) (bytes[0] & 0xFF));
            } catch (NoSuchAlgorithmException e) {
                return input.hashCode() & 0xFFFFFFFFL;
            }
        }
    }

    // 2. Production Bloom Filter (Zero False Negatives) O(K) Time
    public static class BloomFilter<T> {
        private final BitSet bitSet;
        private final int bitSetSize;
        private final int numHashFunctions;

        public BloomFilter(int expectedElements, float falsePositiveRate) {
            // M = - (N * ln(p)) / (ln(2)^2)
            this.bitSetSize = (int) (-expectedElements * Math.log(falsePositiveRate) / (Math.log(2) * Math.log(2)));
            // K = (M / N) * ln(2)
            this.numHashFunctions = Math.max(1, (int) ((bitSetSize / (double) expectedElements) * Math.log(2)));
            this.bitSet = new BitSet(bitSetSize);
        }

        public void add(T element) {
            int[] hashes = getHashes(element.toString());
            for (int hash : hashes) {
                bitSet.set(Math.abs(hash % bitSetSize), true);
            }
        }

        public boolean mightContain(T element) {
            int[] hashes = getHashes(element.toString());
            for (int hash : hashes) {
                if (!bitSet.get(Math.abs(hash % bitSetSize))) {
                    return false; // Zero False Negatives! Definitely NOT present!
                }
            }
            return true; // Probably present (Subject to false positive rate)
        }

        // Kirsch-Mitzenmacher Optimization: Generate K hashes using 2 hash functions
        private int[] getHashes(String data) {
            int[] result = new int[numHashFunctions];
            int h1 = data.hashCode();
            int h2 = h1 ^ (h1 >>> 16);
            for (int i = 0; i < numHashFunctions; i++) {
                result[i] = h1 + i * h2; // gi(x) = h1(x) + i * h2(x)
            }
            return result;
        }
    }
}
```

> **Quick Syntax:**
```java
// Clockwise Ring Routing Line
Long targetHash = ring.ceilingKey(keyHash);
if (targetHash == null) targetHash = ring.firstKey(); // Wrap around
```

---

## 7. Concrete Problem Examples
* **Apache Cassandra / Amazon DynamoDB**: Consistent Hashing key partition routing.
* **RocksDB / Google Chrome**: Bloom Filter fast disk lookup skip.
* **Distributed Hash Tables (Kademlia / BitTorrent)**: Peer-to-peer node lookup.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `ConsistentHashRing` and `BloomFilter`:

```java
public class SystemApplicationsHashingDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Consistent Hashing Ring Test ===");
        SystemApplicationsHashingMaster.ConsistentHashRing ring = 
            new SystemApplicationsHashingMaster.ConsistentHashRing(10); // 10 vnodes

        ring.addServer("192.168.1.10");
        ring.addServer("192.168.1.20");

        System.out.println("Key 'User123' Routed to: " + ring.getServer("User123"));
        System.out.println("Key 'User456' Routed to: " + ring.getServer("User456"));

        System.out.println("\n=== 2. Bloom Filter Test ===");
        SystemApplicationsHashingMaster.BloomFilter<String> bloom = 
            new SystemApplicationsHashingMaster.BloomFilter<>(1000, 0.01f); // 1% false positive

        bloom.add("https://malicious-site.com");
        System.out.println("Might Contain 'malicious-site.com'? " + 
            bloom.mightContain("https://malicious-site.com")); // true

        System.out.println("Might Contain 'google.com'? " + 
            bloom.mightContain("https://google.com")); // false (Zero False Negatives!)
    }
}
```

---

## 9. Complexity Analysis

| System Architecture | Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Consistent Hashing**| Node Lookup | **$O(\log(N \cdot V))$ ⚡**| $O(N \cdot V)$ Ring Space | TreeMap `ceilingKey()` |
| **Bloom Filter** | `add()` / `mightContain()`| **$O(K)$ Constant ⚡**| **$O(M)$ Bit Array ⚡**| $K$ bitwise hash checks |

---

## 10. Edge Cases & Boundary Handling
* **Key Hash Exceeds Largest Ring Position**: Clockwise wraparound takes `ring.firstKey()`.
* **BitSet Overflow in Bloom Filter**: Bit array size $M$ calculated via optimal formula based on expected elements $N$ and false positive rate $p$.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Consistent Hashing Without Virtual Nodes**:
  - Without virtual nodes, physical servers hash unevenly across the ring, causing severe load imbalance and hotspots.
  - **Always assign $V = 100 \dots 250$ virtual nodes per server**.
* **Misunderstanding Bloom Filter Guarantees**:
  - Assuming `mightContain() == true` means the element is 100% present. It only means "probably present"; secondary storage verification is required.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Bloom Filter Golden Rules:
> 1. If Bloom Filter returns `false` $\rightarrow$ Element is **100% DEFINITELY NOT IN SET** (Skip expensive disk reads!).
> 2. If Bloom Filter returns `true` $\rightarrow$ Element is **PROBABLY IN SET** (Perform disk read to verify).
> 3. Elements CANNOT be deleted from a standard Bloom Filter (deleting a bit affects other keys). Use a **Counting Bloom Filter** for deletions!

> **Memory Trick:** **"Bloom Filter false = Definitely NOT present! True = Probably present!"**

---

## 13. System & Implementation Comparisons

| Feature | Consistent Hashing | Modulo Hashing ($h(k) \bmod N$) |
| :--- | :--- | :--- |
| **Keys Moved on Rescaling**| **$1/N$-th of total keys ⚡** | ~100% of all keys (Cache Stampede) |
| **Hotspot Prevention** | **Virtual Nodes ($V$) ⚡** | N/A |
| **Lookup Engine** | TreeMap $O(\log(N \cdot V))$ | Direct $O(1)$ Array Index |

---

## 14. How to Recognize This in Questions
* **"Design distributed cache partition routing when servers join/leave"** $\rightarrow$ Consistent Hashing with Virtual Nodes.
* **"Skip expensive database disk reads for non-existent keys in O(1) space"** $\rightarrow$ Bloom Filter.

---

## 15. Frequently Asked Interview Questions
* **Q: Why are Virtual Nodes necessary in Consistent Hashing?**  
  *A:* Virtual nodes assign multiple hash positions on the ring to each physical server. This ensures uniform data distribution across all physical nodes and prevents single-node hotspots when servers are added or removed.
* **Q: What is the Kirsch-Mitzenmacher Optimization in Bloom Filters?**  
  *A:* It proves that $K$ independent hash functions can be generated using ONLY 2 hash functions via the formula $g_i(x) = h_1(x) + i \cdot h_2(x) \bmod M$, reducing CPU hashing overhead by 80%.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SYSTEM APPLICATIONS OF HASHING                        |
+-----------------------------------------------------------------------+
| • Consistent Hashing: Re-maps ONLY 1/N keys on server change          |
| • Virtual Nodes: Prevents hotspots; maps 1 server to V ring positions |
| • Ring Routing: NavigableMap ceilingKey() with wrap to firstKey()     |
| • Bloom Filter: Zero false negatives! False = 100% not present        |
| • Kirsch-Mitzenmacher: gi(x) = h1(x) + i * h2(x) generates K hashes   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a Consistent Hashing Ring with Virtual Nodes using `TreeMap`.
- [ ] I can write a Bloom Filter using `BitSet`.
- [ ] I know why false = 100% not present in Bloom Filters.
- [ ] I can explain why traditional modulo hashing causes cache stampedes.
- [ ] I know how Kirsch-Mitzenmacher generates $K$ hashes from 2 hash functions.
