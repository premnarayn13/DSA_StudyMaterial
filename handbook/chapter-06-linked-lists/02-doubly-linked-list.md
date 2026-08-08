# 02. Doubly Linked List & Bidirectional Pointer Mechanics

## 1. Introduction
A **Doubly Linked List (DLL)** is a linear data structure composed of nodes containing two pointers: `next` (referencing the subsequent node) and `prev` (referencing the preceding node). In technical coding interviews, Doubly Linked Lists are essential for building advanced $O(1)$ data structures—such as **LRU Cache (Least Recently Used Cache - LeetCode 146)**, LFU Cache, and Deques (Double-Ended Queues)—enabling bidirectional traversal and constant-time node removal when given direct node references.

> **Important:** In a Doubly Linked List, deleting a known node given ONLY its reference takes **$O(1)$ constant time**! (In a Singly Linked List, deleting a node requires $O(N)$ traversal to find the preceding node).

## 2. Core Concepts
* **DLL Node Architecture**: A node containing value `val`, reference pointer `next`, and reference pointer `prev`:
  ```java
  class Node {
      int val;
      Node prev;
      Node next;
      Node(int val) { this.val = val; }
  }
  ```
* **Sentinel Dummy Head & Tail**: Using two dummy sentinel nodes—`head` and `tail`—initialized to point to each other (`head.next = tail; tail.prev = head;`). This eliminates boundary checks for empty list, single element, and edge insertions/deletions!
* **Bidirectional Traversal**: Ability to traverse forward from `head` to `tail` or backward from `tail` to `head`.

> **Memory Trick:** **"LRU Cache = HashMap + Doubly Linked List! Dummy head & tail make insertions/deletions 100% boundary-safe!"**

## 3. Characteristics / Properties
* **$O(1)$ Deletion with Known Node Reference**:
  ```java
  node.prev.next = node.next;
  node.next.prev = node.prev;
  ```
* **Memory Overhead**: Doubly Linked List nodes consume **50% more pointer memory** than Singly Linked List nodes (2 pointer fields `prev` and `next` per node).

```
Doubly Linked List vs Singly Linked List:
+-----------------------+-------------------+-------------------+-------------------+
| Feature / Operation   | Singly Linked List| Doubly Linked List| Winner / Impact   |
+-----------------------+-------------------+-------------------+-------------------+
| Pointer Overhead      | 1 Pointer (`next`)| 2 Pointers (`prev`,`next`)| Singly uses less RAM|
| Traversal             | Forward Only      | Forward & Backward| Doubly is Flexible|
| Delete Known Node Ref | O(N) Traversal    | O(1) Constant ⚡  | Doubly is Optimal |
| LRU Cache Foundation  | Insufficient      | Essential         | Doubly enables LRU|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing $O(1)$ Node Removal in a Doubly Linked List:

```
Initial Chain: [ Node A ] <---> [ Target Node X ] <---> [ Node B ]

Goal: Delete Target Node X given reference to X

Step 1: X.prev.next = X.next; (Node A's next now points directly to Node B)
Step 2: X.next.prev = X.prev; (Node B's prev now points directly to Node A)

Result: [ Node A ] <=================================> [ Node B ]
Node X is completely unlinked in O(1) time and reclaimed by JVM GC! ✅
```

## 5. Visual Diagram
Doubly Linked List Sentinel Dummy Head & Tail Architecture:

```
[ Dummy Head ] <===> [ Node 10 ] <===> [ Node 20 ] <===> [ Dummy Tail ]
 (prev=null)                                              (next=null)

Add to Head (Most Recently Used position):
node.next = head.next;
node.prev = head;
head.next.prev = node;
head.next = node;
```

## 6. Operations / Algorithms
Sentinel-Based Doubly Linked List Operations:

```java
public class DoublyLinkedList {
    private class Node {
        int key, val;
        Node prev, next;
        Node(int key, int val) { this.key = key; this.val = val; }
    }

    private final Node head, tail;

    public DoublyLinkedList() {
        head = new Node(-1, -1);
        tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    // O(1) Add Node Right After Head (Most Recently Used)
    public void addHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    // O(1) Remove Arbitrary Known Node
    public void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    // O(1) Pop Last Node Before Tail (Least Recently Used)
    public Node popTail() {
        if (tail.prev == head) return null; // Empty list
        Node res = tail.prev;
        remove(res);
        return res;
    }
}
```

> **Quick Syntax:**
```java
// O(1) Node Removal Formula
node.prev.next = node.next;
node.next.prev = node.prev;
```

## 7. Examples
* **LeetCode 146 - LRU Cache**: Combined `HashMap<Integer, Node>` + Doubly Linked List to achieve $O(1)$ `get` and `put`.
* **LeetCode 460 - LFU Cache**: HashMap of Frequency Keys pointing to Doubly Linked Lists.
* **Flatten a Multilevel Doubly Linked List (LeetCode 430)**: Recursive / Stack-based flattening of 2D child pointers.

## 8. Java Code
Complete interview-ready Java implementation of LeetCode 146 (LRU Cache) using HashMap and Doubly Linked List with Sentinel Dummy Head/Tail:

```java
import java.util.HashMap;
import java.util.Map;

public class LRUCacheMaster {

    private static class Node {
        int key, val;
        Node prev, next;
        Node(int key, int val) {
            this.key = key;
            this.val = val;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> map;
    private final Node head, tail; // Dummy Sentinels

    public LRUCacheMaster(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        this.head = new Node(-1, -1);
        this.tail = new Node(-1, -1);
        head.next = tail;
        tail.prev = head;
    }

    // O(1) Get Value
    public int get(int key) {
        if (!map.containsKey(key)) return -1;

        Node node = map.get(key);
        moveToHead(node); // Mark as Most Recently Used
        return node.val;
    }

    // O(1) Put Key-Value Pair
    public void put(int key, int value) {
        if (map.containsKey(key)) {
            Node node = map.get(key);
            node.val = value;
            moveToHead(node);
        } else {
            if (map.size() == capacity) {
                // Evict Least Recently Used (node before tail)
                Node lru = tail.prev;
                removeNode(lru);
                map.remove(lru.key);
            }
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addNodeToHead(newNode);
        }
    }

    // Helper: Add node immediately after dummy head
    private void addNodeToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    // Helper: Remove arbitrary node from list
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    // Helper: Move existing node to head (Most Recently Used)
    private void moveToHead(Node node) {
        removeNode(node);
        addNodeToHead(node);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        LRUCacheMaster lru = new LRUCacheMaster(2); // Capacity 2

        lru.put(1, 1); // List: [1]
        lru.put(2, 2); // List: [2, 1]
        System.out.println("Get 1: " + lru.get(1)); // Output: 1 (List: [1, 2])

        lru.put(3, 3); // Evicts key 2! List: [3, 1]
        System.out.println("Get 2: " + lru.get(2)); // Output: -1 (Evicted!)

        lru.put(4, 4); // Evicts key 1! List: [4, 3]
        System.out.println("Get 1: " + lru.get(1)); // Output: -1 (Evicted!)
        System.out.println("Get 3: " + lru.get(3)); // Output: 3
        System.out.println("Get 4: " + lru.get(4)); // Output: 4
    }
}
```

## 9. Complexity Analysis
| Operation | Singly Linked List | Doubly Linked List (with Sentinels) |
| :--- | :--- | :--- |
| **`remove(node)` (Known Node Ref)** | $O(N)$ (Must find prev node) | **$O(1)$ Constant ⚡** |
| **`addHead(node)`** | $O(1)$ Constant | **$O(1)$ Constant** |
| **`popTail()`** | $O(N)$ (Must find node before tail)| **$O(1)$ Constant ⚡** |
| **LRU Cache `get` / `put`** | $O(N)$ time | **$O(1)$ Constant ⚡** |

## 10. Edge Cases
* **List Capacity 1 in LRU Cache**: Inserting a 2nd item immediately evicts the 1st item. Handled cleanly by dummy sentinels.
* **Updating Existing Key Value in LRU Cache**: Updating value MUST move node to head as Most Recently Used.
* **4-Step Pointer Assignment for Node Insertion**: Setting `node.next`, `node.prev`, `head.next.prev`, and `head.next` in exact correct order.

## 11. Common Mistakes
* Writing `node.prev.next = node.next` without checking if `node.prev == null` (causes `NullPointerException` when sentinels are NOT used!). **Always use Sentinel Dummy Head & Tail**.
* Forgetting to update `map.remove(lru.key)` when evicting nodes in LRU Cache.
* Assigning `head.next = node` BEFORE `head.next.prev = node` during head insertion (corrupts `head.next` link!).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** 4-Step Pointer Assignment for Insertion after `head`:
> 1. `node.next = head.next;`
> 2. `node.prev = head;`
> 3. `head.next.prev = node;`
> 4. `head.next = node;`
> Order matters! Steps 1 & 2 connect the new node first before mutating `head.next`.

> **Memory Trick:** **"Connect New Node pointers FIRST (steps 1 & 2), then update existing list pointers (steps 3 & 4)!"**

## 13. Comparisons
| Feature | `java.util.LinkedList` | Custom Doubly Linked List with Sentinels |
| :--- | :--- | :--- |
| **Node Reference Removal** | Requires linear search $O(N)$ | **Direct node reference removal $O(1)$** |
| **LRU Cache Fitness** | Poor (Cannot get Node reference) | **Optimal (HashMap stores Node references)** |
| **Boundary Handling** | Manual `null` checks | Automatic via Dummy Head & Tail |

## 14. How to Recognize This in Questions
* **"Design a Least Recently Used (LRU) Cache with O(1) get and put"** $\rightarrow$ HashMap + Doubly Linked List with Dummy Head/Tail.
* **"Delete a node in O(1) time given node reference"** $\rightarrow$ Doubly Linked List `node.prev.next = node.next`.

## 15. Frequently Asked Interview Questions
* **Q: Why does LRU Cache combine a HashMap with a Doubly Linked List?**  
  *A:* The HashMap provides $O(1)$ key-to-node lookup. The Doubly Linked List maintains access ordering (Most Recently Used at head, Least Recently Used at tail) and enables $O(1)$ node removal and head insertion when given a node reference.
* **Q: Why are Dummy Head and Dummy Tail nodes crucial in LRU Cache?**  
  *A:* Dummy Head and Tail nodes guarantee that `node.prev` and `node.next` are NEVER `null` for any valid data node. This eliminates `if (node == head)` or `if (node == tail)` boundary checks, making $O(1)$ insertion and removal completely bug-free.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DOUBLY LINKED LIST & LRU CACHE                        |
+-----------------------------------------------------------------------+
| • Node Structure: int val; Node prev; Node next;                      |
| • O(1) Node Removal: node.prev.next = node.next; node.next.prev = node.prev|
| • Dummy Sentinels: head.next = tail; tail.prev = head;                |
| • Insertion Order: (1) node.next=head.next (2) node.prev=head         |
|                    (3) head.next.prev=node (4) head.next=node         |
| • LRU Architecture: HashMap<Key, Node> + DoublyLinkedList             |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the 4-step pointer assignment for DLL head insertion.
- [ ] I can write $O(1)$ node removal `node.prev.next = node.next`.
- [ ] I know why Dummy Head and Tail sentinels eliminate `null` checks.
- [ ] I can implement LRU Cache (LeetCode 146) from memory in under 10 minutes.
- [ ] I know why HashMap + DLL is required for $O(1)$ LRU `get` and `put`.
