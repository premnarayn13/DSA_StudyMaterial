# 05. Production DSU Class Blueprint, Path Compression + Union by Rank/Size Master Suite

## 1. Introduction
Combining **Path Compression** with **Union by Rank** or **Union by Size** produces the complete production-grade **Disjoint Set Union (DSU)** blueprint used in high-performance software systems and competitive programming. This hybrid implementation achieves **$\alpha(N) \approx O(1)$ Amortized Near-Constant Time** per operation. Furthermore, extending DSU with generic map indexing enables handling arbitrary non-integer objects (such as `String` usernames or `IPAddress` objects) seamlessly.

> **Important:** The Complete Production DSU Blueprint Invariants:
> 1. **Path Compression Invariant**: `parent[i] = find(parent[i])` flattens tree depth during every `find()` query!
> 2. **Union by Size Invariant**: Attaches smaller sets under larger sets (`parent[smaller] = larger`), accumulating sizes `size[larger] += size[smaller]`!
> 3. **Component Count Invariant**: Tracks total active disjoint sets in $O(1)$ time (`count--` on valid union)! ⚡

```
Production DSU Class Structural Architecture:
+-----------------------------------------------------------------------+
| DisjointSetUnion<T> Class Structure                                   |
+-----------------------------------------------------------------------+
| • parent: int[]       (Pointer to parent node / root)                |
| • size:   int[]       (Component size tracking)                       |
| • count:  int         (Active component counter)                      |
| • map:    Map<T, Int> (Generic Object to 0-indexed ID mapper)         |
+-----------------------------------------------------------------------+
| Operations: find(x), union(x, y), connected(x, y), getComponentSize(x)|
+-----------------------------------------------------------------------+
```

---

## 2. Core Concepts & Generic Mapping Architecture

### 2.1 Generic Object DSU Mapping Pattern
To support generic elements (e.g. `String` accounts in LeetCode 721 Accounts Merge):
* Maintain a `Map<T, Integer> map` mapping each unique object `T` to a 0-indexed integer ID $0 \dots N-1$.
* Perform all DSU operations (`find`, `union`) on integer IDs internally in **$\alpha(N) \approx O(1)$ time**.

```
Production DSU Operational Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Operation / Query     | Method Signature  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **`find(x)`**         | `int find(int i)` | **$\alpha(N) \approx O(1)$ ⚡**| $O(N)$ Path Stack |
| **`union(x, y)`**     | `boolean union(x, y)`| **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary  |
| **`connected(x, y)`** | `boolean connected(x, y)`| **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary |
| **`getComponentSize(x)`**| `int getSize(x)`| **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary |
| **`getComponentCount()`**| `int getCount()`| **$O(1)$ Constant ⚡**| $O(1)$ Auxiliary |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Production DSU: Combine Path Compression + Union by Size + Object Map for ultimate O(1) performance!"**

---

## 3. Characteristics & Combined $\alpha(N)$ Complexity Proof

### 3.1 Proof of Near-Constant Amortized Time $\alpha(N)$
* Tarjan (1975) proved that combining Path Compression and Union by Rank/Size bounds the total time for $M$ DSU operations on $N$ elements to:
  $$O(M \cdot \alpha(N))$$
* Since $\alpha(N) \le 4$ for all physical values of $N$, average cost per operation is **$\alpha(N) \approx O(1)$ Amortized Near-Constant Time**! ⚡

---

## 4. Internal Working Mechanics
Tracing Production Generic DSU on `String` items `["alice", "bob", "charlie"]`:

```
Add items to Map: "alice" -> 0, "bob" -> 1, "charlie" -> 2.
parent = [0, 1, 2], size = [1, 1, 1], count = 3.

Call union("alice", "bob"):
- find("alice") = 0, find("bob") = 1.
- size[0] (1) == size[1] (1) -> Attach 1 under 0: parent[1] = 0. size[0] = 2. count = 2.

Call union("bob", "charlie"):
- find("bob") = 0 (Path Compressed!), find("charlie") = 2.
- size[0] (2) > size[2] (1) -> Attach 2 under 0: parent[2] = 0. size[0] = 3. count = 1.

All 3 users connected in 1 single component of size 3! ✅
```

---

## 5. Visual Diagram
Generic Object Mapping & Parent Forest Topography:

```
Map Indexing:                 DSU Parent Forest:
"alice"   ---> ID 0                 (0) (size = 3, root)
"bob"     ---> ID 1                /   \
"charlie" ---> ID 2              (1)   (2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a thread-safe, generic object DSU master class:

```java
import java.util.*;

// Complete Production-Grade DSU Master Blueprint
public class ProductionDSUMaster<T> {

    private final int[] parent;
    private final int[] size;
    private int count;

    private final Map<T, Integer> objectToId;
    private final List<T> idToObject;

    // 1. Primitive Integer DSU Constructor
    public ProductionDSUMaster(int n) {
        this.count = n;
        this.parent = new int[n];
        this.size = new int[n];
        this.objectToId = null;
        this.idToObject = null;

        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }

    // 2. Generic Object DSU Constructor
    public ProductionDSUMaster(Collection<T> objects) {
        int n = objects.size();
        this.count = n;
        this.parent = new int[n];
        this.size = new int[n];
        this.objectToId = new HashMap<>();
        this.idToObject = new ArrayList<>();

        int id = 0;
        for (T obj : objects) {
            if (!objectToId.containsKey(obj)) {
                objectToId.put(obj, id);
                idToObject.add(obj);
                parent[id] = id;
                size[id] = 1;
                id++;
            }
        }
    }

    // Core Find with Recursive Path Compression O(alpha(N)) Time
    public int find(int i) {
        if (i == parent[i]) {
            return i;
        }
        return parent[i] = find(parent[i]); // Path Compression Assignment
    }

    // Generic Object Find
    public int find(T obj) {
        Integer id = objectToId.get(obj);
        if (id == null) throw new IllegalArgumentException("Object not found in DSU");
        return find(id);
    }

    // Core Union by Size O(alpha(N)) Time
    public boolean union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX == rootY) {
            return false; // Already in same component!
        }

        // Attach smaller set under larger set
        if (size[rootX] < size[rootY]) {
            parent[rootX] = rootY;
            size[rootY] += size[rootX];
        } else {
            parent[rootY] = rootX;
            size[rootX] += size[rootY];
        }

        count--; // Decrement active component count
        return true; // Successfully merged!
    }

    // Generic Object Union
    public boolean union(T obj1, T obj2) {
        return union(find(obj1), find(obj2));
    }

    // Check Connectivity O(alpha(N)) Time
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }

    public boolean connected(T obj1, T obj2) {
        return find(obj1) == find(obj2);
    }

    // Component Size Query O(alpha(N)) Time
    public int getComponentSize(int i) {
        return size[find(i)];
    }

    public int getComponentSize(T obj) {
        return getComponentSize(find(obj));
    }

    public int getComponentCount() {
        return count;
    }
}
```

> **Quick Syntax:**
```java
// Production DSU Union Return Line
if (rootX == rootY) return false;
if (size[rootX] < size[rootY]) { parent[rootX] = rootY; size[rootY] += size[rootX]; }
else { parent[rootY] = rootX; size[rootX] += size[rootY]; }
count--; return true;
```

---

## 7. Concrete Problem Examples
* **LeetCode 721 - Accounts Merge**: Generic DSU for merging email accounts.
* **LeetCode 128 - Longest Consecutive Sequence**: DSU grouping consecutive numbers.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `ProductionDSUMaster` with generic `String` objects:

```java
public class ProductionDSUDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Production Generic DSU Master Test ===");
        List<String> users = Arrays.asList("alice", "bob", "charlie", "david");
        ProductionDSUMaster<String> dsu = new ProductionDSUMaster<>(users);

        System.out.println("Initial Component Count: " + dsu.getComponentCount()); // Output: 4

        dsu.union("alice", "bob");
        dsu.union("bob", "charlie");

        System.out.println("Is 'alice' connected to 'charlie'? " + 
            dsu.connected("alice", "charlie")); // Output: true

        System.out.println("Component Size of 'alice': " + 
            dsu.getComponentSize("alice")); // Output: 3

        System.out.println("Component Size of 'david': " + 
            dsu.getComponentSize("david")); // Output: 1

        System.out.println("Final Component Count: " + 
            dsu.getComponentCount()); // Output: 2 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`find(x)`** | **$\alpha(N) \approx O(1)$ ⚡**| $O(N)$ Path Stack | Recursive Path Compression |
| **`union(x, y)`** | **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary | Union by Size balancing |
| **`connected(x, y)`**| **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary | Root comparison |
| **`getComponentSize()`**| **$\alpha(N) \approx O(1)$ ⚡**| $O(1)$ Auxiliary | Accumulated `size[]` lookup |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Objects Added to Constructor**: Handled safely by `Map` deduplication.
* **Unregistered Object Query**: Throws clean `IllegalArgumentException`.

---

## 11. Common Mistakes & Anti-Patterns
* **Returning `void` from `union()` Instead of `boolean`**:
  - Returning `boolean` (`true` if merged, `false` if already connected) simplifies cycle detection and Kruskal MST algorithms significantly!
  - **ALWAYS return `boolean` from `union(x, y)`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `boolean union(x, y)` is Superior:
> If `union(x, y)` returns `false`, it signals that $x$ and $y$ were ALREADY connected in the same set!
> In graph algorithms, an edge connecting two already-connected nodes forms a **CYCLE**!
> Returning `boolean` allows Cycle Detection and Kruskal MST to be implemented in 3 lines of code! ⚡

> **Memory Trick:** **"Return boolean from union(x, y): false means cycle detected!"**

---

## 13. System & Implementation Comparisons

| Feature | Production Generic DSU Class | Basic Array DSU |
| :--- | :--- | :--- |
| **Type Support** | **Universal Objects (`T`) ⚡** | Integer IDs Only |
| **Union Return** | **`boolean` (Cycle Signal) ⚡**| `void` |
| **Metadata Tracking**| Component Count & Size | Parent Array Only |

---

## 14. How to Recognize This in Questions
* **"Merge non-integer elements (strings/objects) into connected sets"** $\rightarrow$ Production Generic DSU.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does `union(x, y)` return `false` when `rootX == rootY`?**  
  *A:* Because $x$ and $y$ are already part of the same set, meaning no merge operation occurred.
* **Q: How does the generic constructor map non-integer objects to DSU IDs?**  
  *A:* By populating a `Map<T, Integer>` mapping each unique object to a 0-indexed integer ID $0 \dots N-1$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRODUCTION DSU MASTER BLUEPRINT                       |
+-----------------------------------------------------------------------+
| • Hybrid Setup : Path Compression + Union by Size + Generic Object Map|
| • find(i)      : return parent[i] = find(parent[i]);                  |
| • union(x, y)  : boolean return (false signals cycle!) ⚡              |
| • Size Track   : size[larger] += size[smaller]                        |
| • Performance  : $\alpha(N) \approx O(1)$ Amortized Constant Time! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Production DSU Master Class in Java.
- [ ] I can implement generic object mapping using `Map<T, Integer>`.
- [ ] I know why `union(x, y)` should return `boolean`.
- [ ] I can state the combined amortized complexity $\alpha(N)$.
- [ ] I can trace generic object unions step by step.
