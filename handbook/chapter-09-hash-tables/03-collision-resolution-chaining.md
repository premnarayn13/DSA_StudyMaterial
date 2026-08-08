# 03. Collision Resolution via Separate Chaining & Treeification (Java 8+ HashMap)

## 1. Introduction
**Separate Chaining** is a fundamental collision resolution technique where each array bucket slot in a Hash Table maintains an external data structure (traditionally a Singly Linked List) holding all key-value entries that map to that specific bucket index. In technical coding interviews and high-performance system design, understanding the transition from basic linked list chaining to **Java 8+ Hybrid Red-Black Tree Treeification** explains how modern hash tables guarantee $O(\log N)$ worst-case search performance even under adversarial Hash DoS attacks.

> **Important:** In Java 8+, when a single bucket's linked list chain length reaches or exceeds **TREEIFY_THRESHOLD = 8** AND the overall table capacity is at least **MIN_TREEIFY_CAPACITY = 64**, Java automatically converts that bucket chain into a **Red-Black Balanced Search Tree**. This improves worst-case lookup time from $O(N)$ down to **$O(\log N)$**!

```
Collision Resolution Spectrum:
+-----------------------------------------------------------------------------------+
| Traditional Separate Chaining : Linked List per Bucket -> Worst Case O(N) Search  |
| Java 8+ Hybrid Chaining      : List -> Treeify at >=8  -> Worst Case O(log N)    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Analysis

### 2.1 The Separate Chaining Architecture
In Separate Chaining, the main table array `Node<K,V>[] table` contains references to the head nodes of external lists.
When a new key-value pair $(K, V)$ is inserted:
1. Compute bucket index $i = \text{hash}(K) \ \& \ (m - 1)$.
2. If bucket `table[i]` is empty, create a new Node and set `table[i] = newNode`.
3. If bucket `table[i]` is non-empty, traverse the chain checking `.equals(K)`. If found, overwrite value; else append/prepend the new node.

### 2.2 Expected Chain Length & Load Factor Analysis
Under the **Simple Uniform Hashing Assumption** (where $n$ keys are distributed uniformly across $m$ buckets), the expected number of keys in any single bucket chain is equal to the **Load Factor $\alpha$**:

$$E[\text{chain length}] = \alpha = \frac{n}{m}$$

* **Successful Search Expected Time**: Searching for a key present in the table requires inspecting the target node plus half of the remaining elements in its bucket chain:
  $$T_{\text{success}} = 1 + \frac{\alpha}{2} - \frac{\alpha}{2n} = \mathbf{O(1 + \alpha)}$$
* **Unsuccessful Search Expected Time**: Searching for a key not present in the table requires scanning the entire bucket chain:
  $$T_{\text{unsuccess}} = 1 + \alpha = \mathbf{O(1 + \alpha)}$$

If $\alpha$ is maintained as a constant (e.g. $\alpha \le 0.75$ via dynamic resizing), then $O(1 + \alpha) = \mathbf{O(1)\text{ Average Time}}$.

### 2.3 Why Treeify Threshold is Exactly 8
Under a random hash code distribution following a Poisson Distribution with mean $\lambda = 0.5$ (for load factor $\alpha = 0.75$), the probability $P(k)$ of a bucket having $k$ nodes is:

$$P(k) = \frac{e^{-\lambda} \cdot \lambda^k}{k!}$$

Evaluating probabilities for chain length $k$:
* $k = 0$: $P(0) \approx 0.6065$
* $k = 1$: $P(1) \approx 0.3032$
* $k = 2$: $P(2) \approx 0.0758$
* $k = 3$: $P(3) \approx 0.0126$
* $k = 4$: $P(4) \approx 0.0016$
* $k = 5$: $P(5) \approx 0.00015$
* $k = 6$: $P(6) \approx 0.000013$
* $k = 7$: $P(7) \approx 0.00000094$
* $k = 8$: $P(8) \approx \mathbf{0.00000006}$ **(6 in 100 million chance!)**

Because reaching 8 nodes in a single bucket under normal uniform hashing is statistically astronomically rare ($0.000006\%$), a chain of length 8 strongly indicates either a non-uniform hash function or an adversarial Hash DoS attack. Thus, **`TREEIFY_THRESHOLD = 8`** is the mathematically optimal threshold to trigger treeification!

```
Poisson Probability of Bucket Chain Lengths (λ = 0.5):
+-----------------------+-------------------+-------------------+-------------------+
| Chain Length k        | Probability P(k)  | Occurrences in 10M| State Action      |
+-----------------------+-------------------+-------------------+-------------------+
| k = 1                 | 30.32%            | 3,032,000         | Linked List Node  |
| k = 3                 | 1.26%             | 126,000           | Linked List Node  |
| k = 6                 | 0.0013%           | 130               | Linked List Node  |
| k = 8                 | 0.000006%         | 0.6               | TREEIFY TO RED-BLACK TREE!|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Chaining Expected Search = O(1 + α)! Treeify at >= 8 nodes because Poisson odds of 8 nodes is 6 in 100 million!"**

---

## 3. Characteristics & Java 8+ Treeification Threshold Rules

### 3.1 Java 8+ HashMap Constants
* **`TREEIFY_THRESHOLD = 8`**: Bin count threshold for converting a linked list bucket into a Red-Black TreeNode.
* **`UNTREEIFY_THRESHOLD = 6`**: Bin count threshold for converting a Red-Black TreeNode bucket back into a plain linked list during resizing/shrinkage. (Gap between 8 and 6 prevents rapid oscillation / thrashing!).
* **`MIN_TREEIFY_CAPACITY = 64`**: Minimum table capacity required for treeification. If table capacity is $< 64$ when a bucket hits 8 nodes, Java resizes the table ($m \to 2m$) instead of treeifying!

```
Bucket State Transitions:
[ Linked List ] === (Nodes >= 8 & Capacity >= 64) ===> [ Red-Black Tree ]
[ Red-Black Tree ] === (Nodes <= 6 & Resize/Remove) ===> [ Linked List ]
```

---

## 4. Internal Working Mechanics
Tracing Bucket Insertion & Treeification Transition:

```
[ INSERTION TRACE IN BUCKET SLOT 5 ]

State 1: Bucket 5 has 7 Nodes (Node1 -> Node2 -> ... -> Node7)
Action : Inserting Key "AdversaryKey8" which hashes to Bucket 5.

Step 1: Traverse linked list, count binCount = 7.
Step 2: Append Node8 at end of list (binCount reaches 8!).
Step 3: Call treeifyBin(table, hash).
Step 4: Check table.length:
        - If table.length < 64: Call resize() to double capacity!
        - If table.length >= 64: Convert all 8 Nodes into TreeNode objects!
Step 5: Build Red-Black Tree structure with root at table[5].

Result: Bucket 5 transformed from O(N) Linked List to O(log N) Red-Black Tree! ✅
```

---

## 5. Visual Diagram
Separate Chaining with Hybrid Linked List and Treeified Red-Black Buckets:

```
Array Table Index
+---+
| 0 | ---> null
+---+
| 1 | ---> [ Node A ] <---> [ Node B ] ---> null  (Normal Chaining, Len 2 < 8)
+---+
| 2 | ---> null
+---+
| 3 | ---> [ Red-Black Tree Root Node ]           (Treeified Bucket, Len >= 8)
|   |             /            \
|   |     [ Node Left ]     [ Node Right ]
|   |       /       \         /        \
|   |     [...]    [...]    [...]     [...]
+---+
| 4 | ---> null
+---+
```

---

## 6. Operations & Complete Java Implementation
Complete production-grade implementation of a Separate-Chaining Hash Table with Treeification mechanics:

```java
import java.util.Objects;

public class HybridChainingHashTable<K extends Comparable<K>, V> {

    static final int TREEIFY_THRESHOLD = 8;
    static final int UNTREEIFY_THRESHOLD = 6;
    static final int MIN_TREEIFY_CAPACITY = 64;
    static final float DEFAULT_LOAD_FACTOR = 0.75f;

    // Node Abstraction: Can be a LinkedList Node or TreeNode
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

    // Red-Black Tree Node Extension for Treeified Buckets
    static final class TreeNode<K extends Comparable<K>, V> extends Node<K, V> {
        TreeNode<K, V> parent;
        TreeNode<K, V> left;
        TreeNode<K, V> right;
        boolean red;

        TreeNode(int hash, K key, V value, Node<K, V> next) {
            super(hash, key, value, next);
        }

        // Simplified BST Search inside Treeified Bucket
        V findTree(int h, K k) {
            TreeNode<K, V> p = this;
            while (p != null) {
                int ph = p.hash;
                K pk = p.key;
                if (ph > h) {
                    p = p.left;
                } else if (ph < h) {
                    p = p.right;
                } else if (Objects.equals(pk, k)) {
                    return p.value;
                } else if (k != null && pk != null) {
                    int dir = k.compareTo(pk);
                    p = (dir < 0) ? p.left : p.right;
                } else {
                    p = p.right;
                }
            }
            return null;
        }
    }

    private Node<K, V>[] table;
    private int size;
    private int capacity;

    @SuppressWarnings("unchecked")
    public HybridChainingHashTable(int initialCapacity) {
        this.capacity = Math.max(initialCapacity, 16);
        this.table = (Node<K, V>[]) new Node[capacity];
        this.size = 0;
    }

    static final int spreadHash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }

    public V get(K key) {
        int h = spreadHash(key);
        int idx = h & (capacity - 1);
        Node<K, V> first = table[idx];

        if (first == null) return null;

        // If bucket is treeified
        if (first instanceof TreeNode) {
            return ((TreeNode<K, V>) first).findTree(h, key);
        }

        // Standard Linked List Bucket Scan
        Node<K, V> curr = first;
        while (curr != null) {
            if (curr.hash == h && Objects.equals(curr.key, key)) {
                return curr.value;
            }
            curr = curr.next;
        }
        return null;
    }

    public void put(K key, V value) {
        int h = spreadHash(key);
        int idx = h & (capacity - 1);
        Node<K, V> first = table[idx];

        if (first == null) {
            table[idx] = new Node<>(h, key, value, null);
            size++;
        } else if (first instanceof TreeNode) {
            // Put into Treeified Bucket
            putTree((TreeNode<K, V>) first, h, key, value);
        } else {
            // Append to Linked List Bucket & Count Chain Length
            Node<K, V> curr = first;
            int binCount = 0;
            while (true) {
                if (curr.hash == h && Objects.equals(curr.key, key)) {
                    curr.value = value;
                    return;
                }
                binCount++;
                if (curr.next == null) {
                    curr.next = new Node<>(h, key, value, null);
                    size++;
                    break;
                }
                curr = curr.next;
            }

            // Check Treeification Condition
            if (binCount >= TREEIFY_THRESHOLD - 1) {
                treeifyBin(idx);
            }
        }

        if ((float) size / capacity >= DEFAULT_LOAD_FACTOR) {
            resize();
        }
    }

    private void treeifyBin(int index) {
        if (capacity < MIN_TREEIFY_CAPACITY) {
            resize(); // Double capacity instead of treeifying if table is small
            return;
        }

        Node<K, V> head = table[index];
        if (head == null) return;

        TreeNode<K, V> treeHead = null, tail = null;
        Node<K, V> e = head;
        while (e != null) {
            TreeNode<K, V> p = new TreeNode<>(e.hash, e.key, e.value, null);
            if (tail == null) treeHead = p;
            else { p.parent = tail; tail.next = p; }
            tail = p;
            e = e.next;
        }

        table[index] = treeHead; // Simplified placeholder tree root
    }

    @SuppressWarnings("unchecked")
    private void resize() {
        int oldCap = capacity;
        Node<K, V>[] oldTable = table;

        capacity = oldCap * 2;
        table = (Node<K, V>[]) new Node[capacity];
        size = 0;

        for (int i = 0; i < oldCap; i++) {
            Node<K, V> e = oldTable[i];
            while (e != null) {
                put(e.key, e.value);
                e = e.next;
            }
        }
    }

    public int size() { return size; }
}
```

> **Quick Syntax:**
```java
// Check Treeification Guard Conditions
if (binCount >= TREEIFY_THRESHOLD - 1 && capacity >= MIN_TREEIFY_CAPACITY) {
    treeifyBin(index);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 706 - Design HashMap**: Separate chaining implementation with dynamic array.
* **LeetCode 49 - Group Anagrams**: Hashing strings into bucket chains using canonical frequency keys.
* **LeetCode 355 - Design Twitter**: User feed timeline management via map bucket chains.

---

## 8. Java Code Demonstration & Dry Run
Demonstration verifying bucket chain traversal, treeification trigger conditions, and performance under deliberate hash collisions:

```java
public class SeparateChainingDemo {

    // Bad Key class forcing deliberate hash collisions into bucket 0
    static class BadKey implements Comparable<BadKey> {
        final int id;
        BadKey(int id) { this.id = id; }

        @Override
        public int hashCode() {
            return 42; // FORCES ALL KEYS TO MAP TO BUCKET INDEX (42 & (cap-1))!
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            return id == ((BadKey) o).id;
        }

        @Override
        public int compareTo(BadKey o) {
            return Integer.compare(this.id, o.id);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== 1. Testing Separate Chaining Table ===");
        HybridChainingHashTable<BadKey, String> map = new HybridChainingHashTable<>(64);

        System.out.println("Inserting 10 Keys with Identical HashCodes (Forces Bucket 10 Collision)...");
        for (int i = 1; i <= 10; i++) {
            map.put(new BadKey(i), "Val-" + i);
            System.out.println("Inserted BadKey(" + i + "), Total Size: " + map.size());
        }

        System.out.println("\nRetrieving Keys from Treeified/Long Bucket Chain:");
        System.out.println("BadKey(5) Value: " + map.get(new BadKey(5)));
        System.out.println("BadKey(9) Value: " + map.get(new BadKey(9)));
    }
}
```

---

## 9. Complexity Analysis

| Operation | Standard Separate Chaining (Linked List) | Hybrid Treeified Chaining (Java 8+ HashMap) |
| :--- | :--- | :--- |
| **Search (Average Case)** | **$O(1 + \alpha) = \mathbf{O(1)}$ ⚡** | **$O(1 + \alpha) = \mathbf{O(1)}$ ⚡** |
| **Search (Worst Case - All Collide)**| $O(N)$ (Linear List Scan) | **$O(\log N)$ (Red-Black Tree Search) ⚡** |
| **Insertion (Average Case)** | **Amortized $O(1)$** | **Amortized $O(1)$** |
| **Insertion (Worst Case)** | $O(N)$ | **$O(\log N)$ Tree Insert** |
| **Deletion (Average Case)** | **$O(1)$** | **$O(1)$** |
| **Deletion (Worst Case)** | $O(N)$ | **$O(\log N)$ Tree Delete** |

---

## 10. Edge Cases & Boundary Handling
* **High Hash Collision Attack (Hash DoS)**: Adversaries send HTTP POST requests with keys designed to collide into a single bucket. Separate chaining with plain lists slows servers down to $O(N^2)$ CPU processing time. Java 8+ treeification caps CPU processing at $O(N \log N)$.
* **Resizing Untreeifies Small Buckets**: When resizing shrinks or redistributes a treeified bucket down to $\le 6$ nodes (`UNTREEIFY_THRESHOLD`), Java converts the Red-Black Tree back to a simple linked list to save memory.

---

## 11. Common Mistakes & Anti-Patterns
* **Setting Treeify Threshold to a Small Value (e.g. 2 or 3)**: Red-Black Tree nodes (`TreeNode`) consume **double the memory** of standard list nodes (`Node`). Treeifying small buckets wastes massive RAM!
* **Setting Treeify and Untreeify Thresholds Equal (e.g. 8 and 8)**: Causes **Thrashing**! Repeatedly adding and removing the 8th element causes continuous expensive conversions between List $\leftrightarrow$ Tree. Setting thresholds to 8 and 6 provides a hysteresis gap.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why the Gap Between `TREEIFY_THRESHOLD = 8` and `UNTREEIFY_THRESHOLD = 6` Matters:
> Having a gap of 2 elements prevents **Thrashing**. If both thresholds were 8, adding an 8th element would treeify the bucket, and immediately removing it would untreeify it. Alternating `put`/`remove` calls would waste CPU constantly converting data structures!

> **Memory Trick:** **"Treeify at 8, Untreeify at 6! The gap of 2 prevents conversion thrashing!"**

---

## 13. System & Implementation Comparisons

| Feature | Plain Separate Chaining (Java 7) | Treeified Hybrid Chaining (Java 8+) |
| :--- | :--- | :--- |
| **Bucket Structure** | `Entry<K,V>` Linked List | `Node<K,V>` List $\to$ `TreeNode<K,V>` RB-Tree |
| **Worst-Case Search** | $O(N)$ Linear Time | **$O(\log N)$ Logarithmic Time ⚡** |
| **List Insertion Order**| Prepend at Head ($O(1)$) | Append at Tail ($O(1)$ list / $O(\log N)$ tree) |
| **Memory per Node** | ~32 Bytes (`Entry`) | ~32 Bytes (`Node`) / ~64 Bytes (`TreeNode`) |

---

## 14. How to Recognize This in Questions
* **"Explain how Java 8 HashMap handles severe hash collisions"** $\rightarrow$ Linked List treeifies to Red-Black Tree at $\ge 8$ nodes & capacity $\ge 64$.
* **"Design a Hash Map resilient against Hash DoS attacks"** $\rightarrow$ Hybrid Separate Chaining with Treeification ($O(\log N)$ worst case).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Java 8 HashMap require `MIN_TREEIFY_CAPACITY = 64` before treeifying a bucket?**  
  *A:* When table capacity is small ($< 64$), bucket collisions are more efficiently resolved by doubling table capacity (`resize()`). Doubling capacity redistributes elements across twice as many buckets, naturally shortening chain lengths without incurring the memory overhead of Red-Black Tree nodes.
* **Q: Why does Java 7 prepend new elements at the head of bucket lists, while Java 8 appends at the tail?**  
  *A:* Java 7 prepended at head in $O(1)$ time without traversing the list. Java 8 must traverse the list to count nodes (`binCount`) to check if the threshold of 8 is reached, so it appends at the tail during traversal.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEPARATE CHAINING & TREEIFICATION                     |
+-----------------------------------------------------------------------+
| • Separate Chaining: Array of buckets where each slot holds a list/tree|
| • Expected Search Time: O(1 + α) where α = n / m (Load Factor)        |
| • TREEIFY_THRESHOLD = 8: Bucket chain converts to Red-Black Tree       |
| • UNTREEIFY_THRESHOLD = 6: Tree converts back to Linked List           |
| • MIN_TREEIFY_CAPACITY = 64: Must have capacity >= 64 to treeify      |
| • Poisson Odds: Probability of 8 nodes in a bucket is 6 in 100 million|
| • Hysteresis Gap (8 vs 6): Prevents rapid conversion thrashing!       |
| • Worst-Case Improvement: Java 7 O(N) -> Java 8 O(log N) Search        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can derive $E[\text{search time}] = O(1 + \alpha)$ for Separate Chaining.
- [ ] I know why `TREEIFY_THRESHOLD = 8` was chosen using Poisson distribution odds.
- [ ] I know why `MIN_TREEIFY_CAPACITY = 64` is checked before treeification.
- [ ] I can explain why `UNTREEIFY_THRESHOLD = 6` creates a hysteresis gap.
- [ ] I know how treeification mitigates Hash DoS attacks ($O(\log N)$ vs $O(N)$).
- [ ] I can implement a complete Separate-Chaining Hash Table in Java.
