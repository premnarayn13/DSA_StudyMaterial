# 14. System Applications: LRU Cache, Task Schedulers & Work-Stealing Deques

## 1. Introduction
In computer systems engineering, Stacks and Queues are the foundational building blocks for memory management, operating system scheduling, database caching, and concurrent runtime systems. High-performance production structures—such as the **LRU Cache (Least Recently Used Cache - LeetCode 146)**, **Task Scheduler (LeetCode 621)**, and **Work-Stealing Deques (Java ForkJoinPool)**—combine Stacks, Queues, Hash Maps, and Doubly Linked Lists to achieve **$O(1)$ constant time cache hits, evictions, and work distribution**.

> **Important:** In **LRU Cache (LeetCode 146)**, pairing a **Hash Map (`HashMap<Integer, Node>`)** with a **Doubly Linked List (`head` and `tail` sentinels)** enables both key lookup AND node promotion/eviction in **$O(1)$ Constant Time**!

```
LRU Cache Hybrid Architecture:
HashMap <Key, Node>  --->  [ Head Sentinel ] <---> [ Node A ] <---> [ Node B ] <---> [ Tail Sentinel ]
(O(1) Key Lookup)          (Most Recently Used)                              (Least Recently Used - Evict!)
```

---

## 2. Core Concepts & LRU Cache Architecture (LeetCode 146)

### 2.1 LRU Cache Design (LeetCode 146)
Design a data structure that follows the constraints of a **Least Recently Used (LRU) Cache**:

#### Operational Contracts:
1. **`get(key)`**:
   - If `key` exists in map: Move node to front (`head`) of Doubly Linked List. Return `node.value`.
   - Else: Return `-1`. Time Complexity: **$O(1)$ Constant**.
2. **`put(key, value)`**:
   - If `key` exists in map: Update value and move node to front (`head`).
   - If `key` does not exist:
     - If capacity is full: Remove least recently used node from rear (`tail.prev`) from both list and map!
     - Create new node, insert at front (`head`), and record in map. Time Complexity: **$O(1)$ Constant**.

```
LRU Cache Node Manipulation Invariants:
1. Move to Head (Promotion): removeNode(node) -> addHead(node)
2. Evict LRU Element        : evictNode = tail.prev -> removeNode(evictNode) -> map.remove(evictNode.key)
3. Add New Element          : node = new Node(k, v) -> addHead(node) -> map.put(k, node)
```

> **Memory Trick:** **"LRU Cache = HashMap + Doubly LinkedList! Most Recently Used at Head, Least Recently Used at Tail!"**

---

## 3. Characteristics & Task Scheduler Mechanics (LeetCode 621)

### 3.1 Task Scheduler (LeetCode 621 - Priority Queue + Cooldown Queue)
Given a characters array `tasks` and non-negative integer `n` representing CPU cooldown interval between identical tasks, return the minimum number of CPU units required:

#### Algorithmic Strategy ($O(N)$ Time, $O(1)$ Space):
1. Count character task frequencies using `int[26]`.
2. Push all non-zero frequencies into a **Max Heap / PriorityQueue**.
3. Maintain a **Cooldown Queue** storing pairs `[freq, availableTime]`.
4. `time = 0`.
5. While PriorityQueue OR Cooldown Queue is not empty:
   - `time++`.
   - If PriorityQueue is not empty:
     - Pop max frequency task: `freq = maxHeap.poll() - 1`.
     - If `freq > 0`, offer to cooldown queue: `cooldownQueue.offer(new int[]{freq, time + n})`.
   - If `!cooldownQueue.isEmpty() && cooldownQueue.peek()[1] == time`:
     - Re-insert task into PriorityQueue: `maxHeap.offer(cooldownQueue.poll()[0])`.
6. Return `time`.

---

## 4. Internal Working Mechanics
Tracing LRU Cache (LeetCode 146) on Capacity 2:

```
put(1, 1): Map: {1: Node(1,1)}. List: Head <-> Node(1,1) <-> Tail
put(2, 2): Map: {1: Node(1,1), 2: Node(2,2)}. List: Head <-> Node(2,2) <-> Node(1,1) <-> Tail

get(1)   : Node(1,1) accessed! Promote to Head.
           Map: {1: Node(1,1), 2: Node(2,2)}. List: Head <-> Node(1,1) <-> Node(2,2) <-> Tail
           Returns 1. ✅

put(3, 3): Capacity full (2)! Evict LRU element at tail.prev (Node(2,2)).
           Remove Node(2,2) from list and map.
           Insert Node(3,3) at Head.
           Map: {1: Node(1,1), 3: Node(3,3)}. List: Head <-> Node(3,3) <-> Node(1,1) <-> Tail

get(2)   : Not in map -> Returns -1. ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
LRU Cache Node Promotion & Sentinel List Manipulation Topography:

```
BEFORE Accessing Key 1:
Head Sentinel <---> Node(2) <---> Node(1) <---> Tail Sentinel
                                   ^
                           (Target to Promote)

AFTER Accessing Key 1 (Promoted to Head):
Head Sentinel <---> Node(1) <---> Node(2) <---> Tail Sentinel
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementations of LRU Cache (LeetCode 146) and Task Scheduler (LeetCode 621):

```java
import java.util.*;

public class SystemApplicationsMaster {

    // 1. LRU Cache Implementation (LeetCode 146) O(1) Get and Put
    public static class LRUCache {
        private static class Node {
            int key;
            int value;
            Node prev;
            Node next;

            Node(int key, int value) {
                this.key = key;
                this.value = value;
            }
        }

        private final int capacity;
        private final Map<Integer, Node> map;
        private final Node head;
        private final Node tail;

        public LRUCache(int capacity) {
            this.capacity = capacity;
            this.map = new HashMap<>();
            this.head = new Node(-1, -1);
            this.tail = new Node(-1, -1);
            head.next = tail;
            tail.prev = head;
        }

        public int get(int key) {
            if (!map.containsKey(key)) {
                return -1;
            }
            Node node = map.get(key);
            moveToHead(node);
            return node.value;
        }

        public void put(int key, int value) {
            if (map.containsKey(key)) {
                Node node = map.get(key);
                node.value = value;
                moveToHead(node);
            } else {
                if (map.size() == capacity) {
                    // Evict Least Recently Used element (tail.prev)
                    Node lru = tail.prev;
                    removeNode(lru);
                    map.remove(lru.key);
                }
                Node newNode = new Node(key, value);
                addHead(newNode);
                map.put(key, newNode);
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

    // 2. Task Scheduler (LeetCode 621) O(N) Time, O(1) Auxiliary Space
    public static int leastInterval(char[] tasks, int n) {
        if (tasks == null || tasks.length == 0) return 0;
        if (n == 0) return tasks.length;

        int[] frequencies = new int[26];
        for (char task : tasks) {
            frequencies[task - 'A']++;
        }

        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int freq : frequencies) {
            if (freq > 0) maxHeap.offer(freq);
        }

        Queue<int[]> cooldownQueue = new ArrayDeque<>(); // Stores [freq, availableTime]
        int time = 0;

        while (!maxHeap.isEmpty() || !cooldownQueue.isEmpty()) {
            time++;

            if (!maxHeap.isEmpty()) {
                int freq = maxHeap.poll() - 1;
                if (freq > 0) {
                    cooldownQueue.offer(new int[]{freq, time + n});
                }
            }

            if (!cooldownQueue.isEmpty() && cooldownQueue.peek()[1] == time) {
                maxHeap.offer(cooldownQueue.poll()[0]);
            }
        }

        return time;
    }
}
```

> **Quick Syntax:**
```java
// Doubly Linked List Sentinel Insertion Line
node.next = head.next;
node.prev = head;
head.next.prev = node;
head.next = node;
```

---

## 7. Concrete Problem Examples
* **LeetCode 146 - LRU Cache**: Doubly Linked List + HashMap.
* **LeetCode 460 - LFU Cache**: HashMap + Frequency Buckets Doubly Linked List.
* **LeetCode 621 - Task Scheduler**: PriorityQueue + Cooldown Queue.
* **Java ForkJoinPool**: Work-Stealing Deque runtime worker threads.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `LRUCache` and `leastInterval`:

```java
public class SystemApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LRU Cache Demonstration (LeetCode 146) ===");
        SystemApplicationsMaster.LRUCache cache = new SystemApplicationsMaster.LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println("Get Key 1: " + cache.get(1)); // Output: 1 (Promoted)
        cache.put(3, 3); // Evicts Key 2!
        System.out.println("Get Key 2 (Evicted): " + cache.get(2)); // Output: -1
        System.out.println("Get Key 3: " + cache.get(3)); // Output: 3

        System.out.println("\n=== 2. Task Scheduler Demonstration (LeetCode 621) ===");
        char[] tasks = {'A', 'A', 'A', 'B', 'B', 'B'};
        int minUnits = SystemApplicationsMaster.leastInterval(tasks, 2);
        System.out.println("Min CPU Execution Time (n=2): " + minUnits); // Output: 8 (A -> B -> idle -> A -> B -> idle -> A -> B)
    }
}
```

---

## 9. Complexity Analysis

| System Application | Get / Read Time | Put / Write Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **LRU Cache (146)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(\text{Capacity})$ Memory |
| **LFU Cache (460)** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(\text{Capacity})$ Memory |
| **Task Scheduler (621)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(1)$ Space ($26$ Freq Map) |

---

## 10. Edge Cases & Boundary Handling
* **LRU Capacity $= 1$**: Every `put()` of a new key evicts the existing single node cleanly.
* **Task Cooldown $n = 0$**: `leastInterval` returns total task count `tasks.length` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Singly Linked List for LRU Cache ($O(N)$ Removal Overhead)**:
  - Deleting a node from a Singly Linked List requires searching for its predecessor node in $O(N)$ time.
  - **Use a Doubly Linked List with `prev` pointers for $O(1)$ deletion**.
* **Forgetting Head and Tail Sentinel Nodes**:
  - Managing null checks for list head and tail introduces verbose edge case bugs.
  - **Initialize dummy `head` and `tail` sentinel nodes**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Sentinels Simplify Doubly Linked Lists:
> Dummy `head` and `tail` sentinel nodes eliminate null pointer checks!
> * Adding to head is ALWAYS `addHead(node)` between `head` and `head.next`.
> * Evicting from tail is ALWAYS `removeNode(tail.prev)`.
> No special cases exist for empty lists or single-element lists!

> **Memory Trick:** **"Always use dummy head and tail sentinel nodes in LRU Cache to eliminate null checks!"**

---

## 13. System & Implementation Comparisons

| Feature | Custom HashMap + Doubly LinkedList | Java `LinkedHashMap` Override |
| :--- | :--- | :--- |
| **Interview Value** | **100% Expected Implementation ⚡**| Minimal (Library call) |
| **Control** | Full Pointer Optimization | Delegates to internal map |
| **Time Complexity** | $O(1)$ Get and Put | $O(1)$ Get and Put |

---

## 14. How to Recognize This in Questions
* **"Design a Least Recently Used (LRU) Cache supporting O(1) get and put"** $\rightarrow$ LeetCode 146 (HashMap + Doubly Linked List).
* **"Schedule CPU tasks with cooldown intervals"** $\rightarrow$ LeetCode 621 (PriorityQueue + Cooldown Queue).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does LRU Cache require a Doubly Linked List instead of a Queue?**  
  *A:* Because `get(key)` requires promoting an arbitrary node from the MIDDLE of the structure to the front. A standard Queue only allows removals from the front ($O(1)$), requiring $O(N)$ search time to remove middle items. A Doubly Linked List allows $O(1)$ node removal from any position.
* **Q: What is a Work-Stealing Deque in multi-threaded runtime environments?**  
  *A:* In systems like Java `ForkJoinPool`, each worker thread owns a local Deque. The owner thread pushes and pops tasks from the TAIL (LIFO stack behavior for cache locality), while idle worker threads steal tasks from the FRONT (FIFO queue behavior) to minimize contention.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SYSTEM APPLICATIONS OF STACKS AND QUEUES              |
+-----------------------------------------------------------------------+
| • LRU Cache (146): HashMap<Key, Node> + Doubly Linked List            |
| • Sentinel Strategy: Dummy head and tail nodes eliminate null checks  |
| • Node Promotion: removeNode(node) -> addHead(node)                   |
| • LRU Eviction: Node lru = tail.prev; removeNode(lru); map.remove(lru)|
| • Task Scheduler (621): PriorityQueue (Max Heap) + Cooldown Queue     |
| • Work-Stealing Deque: Owner acts as LIFO stack; thieves steal FIFO   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LRU Cache (LeetCode 146) from scratch using HashMap + Doubly LinkedList.
- [ ] I know why dummy sentinel nodes simplify list mutations.
- [ ] I can write Task Scheduler (LeetCode 621) using PriorityQueue and Queue.
- [ ] I can explain Work-Stealing Deque architecture in ForkJoinPool.
- [ ] I know why Singly Linked Lists fail $O(1)$ LRU node removal.
