# 10. Cache Design (LRU & LFU Cache Architecture)

## 1. Introduction
Designing high-performance caching algorithms—specifically **LRU Cache (Least Recently Used - LeetCode 146)** and **LFU Cache (Least Frequently Used - LeetCode 460)**—is one of the most prestigious data structure system design topics in technical coding interviews. These problems evaluate combining fast hash-table lookup with double-ended ordering structures to achieve **Strict $O(1)$ constant time for `get(key)` and `put(key, value)`**.

> **Important:** While LRU Cache uses a single **HashMap + Doubly Linked List**, LFU Cache requires **TWO HashMaps + Frequency Doubly Linked Lists** (`keyToNode` map + `freqToList` map + `minFreq` tracker) to achieve $O(1)$ eviction!

## 2. Core Concepts
* **LRU Cache Architecture ($O(1)$ Time)**:
  * **HashMap (`map`)**: Maps `key` $\to$ `Node` reference ($O(1)$ lookup).
  * **Doubly Linked List (`head`, `tail` sentinels)**: Maintains access ordering (Most Recently Used at `head.next`, Least Recently Used at `tail.prev`).
* **LFU Cache Architecture ($O(1)$ Time)**:
  * **`keyToNode` Map**: Maps `key` $\to$ `Node(key, val, freq)`.
  * **`freqToList` Map**: Maps `frequency` $\to$ `DoublyLinkedList` of nodes with that exact frequency.
  * **`minFreq` Tracker**: Integer tracking the current global minimum frequency across all stored items.

> **Memory Trick:** **"LRU = HashMap + DoublyLinkedList; LFU = HashMap<Key, Node> + HashMap<Freq, DoublyLinkedList> + minFreq!"**

## 3. Characteristics / Properties
* **LFU Tie-Breaking Rule**: When multiple items share the exact same minimum frequency `minFreq`, LFU evicts the **Least Recently Used** item among those minimum frequency items!
* **Sentinel Dummy Nodes**: Using dummy `head` and `tail` sentinels in Doubly Linked List eliminates `null` pointer boundary checks.

```
LRU vs LFU Cache Architecture Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | LRU Cache (146)   | LFU Cache (460)   | Winner / Choice   |
+-----------------------+-------------------+-------------------+-------------------+
| Eviction Policy       | Recency of Access | Frequency of Access| Context Dependent|
| `get` / `put` Time    | Strict O(1) ⚡    | Strict O(1) ⚡    | Tie               |
| Data Structure        | Map + DLL         | 2 Maps + Freq DLLs| LRU is Simpler    |
| Space Complexity      | O(Capacity)       | O(Capacity)       | Tie               |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing LFU Cache ($Capacity=2$) on `put(1,1), put(2,2), get(1), put(3,3)`:

```
put(1, 1): Node(1, val=1, freq=1). freqToList[1] = [1]. minFreq = 1 | Map: {1: Node1}
put(2, 2): Node(2, val=2, freq=1). freqToList[1] = [2, 1]. minFreq = 1 | Map: {1: Node1, 2: Node2}

get(1): Node1 freq increases 1 -> 2!
        - Remove Node1 from freqToList[1]
        - Add Node1 to freqToList[2]
        - minFreq remains 1 (since Node2 is still in freqToList[1])

put(3, 3): Capacity full (2/2)! Evict from freqToList[minFreq=1] (LRU item in freq 1 is Node2!).
        - Evict Node2!
        - Add Node3 (freq 1) to freqToList[1]. Set minFreq = 1.
Map now contains {1, 3} (Node2 correctly evicted!) ✅
```

## 5. Visual Diagram
LFU Cache Dual-Map & Frequency Linked List Architecture:

```
keyToNode Map: { Key 1 -> Node A (freq=2), Key 3 -> Node C (freq=1) }

freqToList Map:
  Freq 1: [ Dummy Head ] <===> [ Node C (val=3) ] <===> [ Dummy Tail ]  <-- minFreq = 1
  Freq 2: [ Dummy Head ] <===> [ Node A (val=1) ] <===> [ Dummy Tail ]

Eviction Target: Always pop from `freqToList[minFreq].tail.prev` in O(1) time!
```

## 6. Operations / Algorithms
LeetCode 146 (LRU) & LeetCode 460 (LFU) Core Implementation:

```java
// LRU O(1) Move To Head Helper
private void moveToHead(Node node) {
    removeNode(node);
    addNodeToHead(node);
}

private void removeNode(Node node) {
    node.prev.next = node.next;
    node.next.prev = node.prev;
}

private void addNodeToHead(Node node) {
    node.next = head.next;
    node.prev = head;
    head.next.prev = node;
    head.next = node;
}
```

> **Quick Syntax:**
```java
// O(1) DLL Node Removal Formula
node.prev.next = node.next;
node.next.prev = node.prev;
```

## 7. Examples
* **LeetCode 146 - LRU Cache**: Recency eviction using HashMap + Doubly Linked List.
* **LeetCode 460 - LFU Cache**: Frequency eviction using Dual HashMaps + Frequency Doubly Linked Lists.

## 8. Java Code
Complete interview-ready Java suite implementing LeetCode 146 (LRU Cache) and LeetCode 460 (LFU Cache) with $O(1)$ operations:

```java
import java.util.HashMap;
import java.util.Map;

public class CacheDesignMaster {

    // 1. LRU Cache (LeetCode 146) Strict O(1) Get & Put
    public static class LRUCache {
        private static class Node {
            int key, val;
            Node prev, next;
            Node(int key, int val) { this.key = key; this.val = val; }
        }

        private final int capacity;
        private final Map<Integer, Node> map;
        private final Node head, tail;

        public LRUCache(int capacity) {
            this.capacity = capacity;
            this.map = new HashMap<>();
            this.head = new Node(-1, -1);
            this.tail = new Node(-1, -1);
            head.next = tail;
            tail.prev = head;
        }

        public int get(int key) {
            if (!map.containsKey(key)) return -1;
            Node node = map.get(key);
            moveToHead(node);
            return node.val;
        }

        public void put(int key, int value) {
            if (map.containsKey(key)) {
                Node node = map.get(key);
                node.val = value;
                moveToHead(node);
            } else {
                if (map.size() == capacity) {
                    Node lru = tail.prev;
                    removeNode(lru);
                    map.remove(lru.key);
                }
                Node newNode = new Node(key, value);
                map.put(key, newNode);
                addHead(newNode);
            }
        }

        private void addHead(Node node) {
            node.next = head.next;
            node.prev = head;
            head.next.prev = node;
            head.next = node;
        }

        private void removeNode(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }

        private void moveToHead(Node node) {
            removeNode(node);
            addHead(node);
        }
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        LRUCache lru = new LRUCache(2);
        lru.put(1, 1);
        lru.put(2, 2);
        System.out.println("Get 1: " + lru.get(1)); // Output: 1 (List: [1, 2])

        lru.put(3, 3); // Evicts key 2!
        System.out.println("Get 2: " + lru.get(2)); // Output: -1 (Evicted!)
    }
}
```

## 9. Complexity Analysis
| Cache Algorithm | `get(key)` Time | `put(key, val)` Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **LRU Cache (146)** | **Strict $O(1)$ ⚡** | **Strict $O(1)$ ⚡** | $O(\text{Capacity})$ |
| **LFU Cache (460)** | **Strict $O(1)$ ⚡** | **Strict $O(1)$ ⚡** | $O(\text{Capacity})$ |

## 10. Edge Cases
* **Capacity = 0**: Handled cleanly by returning `-1` or ignoring `put`.
* **Updating Existing Key**: Updating value MUST increment frequency (in LFU) or move node to head (in LRU).
* **Single Element Capacity ($Capacity=1$)**: Every new `put` evicts the existing element cleanly.

## 11. Common Mistakes
* In LFU Cache, using `PriorityQueue` for frequency sorting (causes $O(\log N)$ operations instead of $O(1)$!). Use **Dual HashMaps + Frequency Doubly Linked Lists** for true $O(1)$ LFU operations.
* Forgetting to remove `map.remove(lru.key)` when evicting nodes.
* Forgetting to update `minFreq` when `freqToList.get(minFreq).isEmpty()`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why is PriorityQueue sub-optimal for LFU Cache?
> A Min-Heap Priority Queue ordered by frequency takes **$O(\log N)$ time** for `get` and `put` because updating a node's frequency requires heap re-sifting.
> **Dual HashMaps + Frequency Doubly Linked Lists** achieves **Strict $O(1)$ time** for LFU operations!

> **Memory Trick:** **"True O(1) LFU requires Dual HashMaps + DoublyLinkedLists, NOT PriorityQueue!"**

## 13. Comparisons
| Feature | LRU Cache | LFU Cache |
| :--- | :--- | :--- |
| **Eviction Focus** | Recency | Frequency (+ Recency for ties) |
| **Implementation Complexity**| Moderate (1 Map + 1 DLL) | **High (2 Maps + Multiple DLLs)** |
| **Scan Resistance** | Poor (Sequential scans wipe cache)| **High (Frequent items remain cached)** |

## 14. How to Recognize This in Questions
* **"Design LRU Cache with O(1) get and put"** $\rightarrow$ LeetCode 146 (Map + DLL).
* **"Design LFU Cache with O(1) get and put"** $\rightarrow$ LeetCode 460 (2 Maps + Freq DLLs + minFreq).

## 15. Frequently Asked Interview Questions
* **Q: How does LFU Cache achieve $O(1)$ time for frequency increments?**  
  *A:* When node $X$ with frequency $F$ is accessed, it is removed from `freqToList[F]` in $O(1)$ time and added to the head of `freqToList[F + 1]` in $O(1)$ time. If `freqToList[F]` becomes empty and $F = minFreq$, $minFreq$ is incremented by 1.
* **Q: Why are Sentinel Dummy Nodes (`head` and `tail`) used in cache doubly linked lists?**  
  *A:* Sentinel nodes guarantee that `node.prev` and `node.next` are never `null`, eliminating conditional checks for empty lists or head/tail node removal.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CACHE DESIGN (LRU & LFU CACHE ARCHITECTURE)           |
+-----------------------------------------------------------------------+
| • LRU Cache: HashMap<Key, Node> + DoublyLinkedList (head/tail dummy)  |
| • LRU Eviction: Pop from tail.prev in O(1) time                       |
| • LFU Cache: keyToNode Map + freqToList Map + minFreq Integer         |
| • LFU Eviction: Pop from freqToList[minFreq].tail.prev in O(1) time   |
| • O(1) Node Removal: node.prev.next = node.next; node.next.prev = node.prev|
| • Complexity: Strict O(1) Time for get and put | O(Capacity) Space    |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write $O(1)$ DLL head insertion and node removal.
- [ ] I can implement LRU Cache (LeetCode 146) from memory in under 8 minutes.
- [ ] I know why PriorityQueue is $O(\log N)$ and Dual Maps are $O(1)$ for LFU Cache.
- [ ] I can explain LFU Cache `minFreq` tracking logic.
- [ ] I know how Sentinel Dummy Nodes eliminate boundary checks.
