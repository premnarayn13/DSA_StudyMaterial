# 08. HashSet Architecture, Map-Backing Wrappers & Set Algebra Operations

## 1. Introduction
A **Hash Set (`HashSet`)** is an unordered collection of unique elements designed to support set membership testing, insertion, and deletion in **$O(1)$ Average Constant Time**. Rather than re-implementing hashing mechanics from scratch, Java's `java.util.HashSet` is built entirely as a lightweight **Adapter Pattern Wrapper** around an internal **`HashMap<E, Object>`**, storing set elements as map keys and pairing them with a single static dummy value **`PRESENT = new Object()`**.

> **Important:** Why does Java `HashSet` reuse `HashMap` internally instead of maintaining a custom bucket array?
> Reusing `HashMap` eliminates code duplication! `HashSet` delegates all hashing, collision handling, treeification, and dynamic rehashing directly to `HashMap`, guaranteeing identical high performance with minimal code footprint!

```
HashSet Map-Backing Architecture Topology:
HashSet<E> Object  --->  Internal Private HashMap<E, Object> map
                               |
                   +-----------+-----------+
                   | Keys (Set Elements)   | Values (Static Dummy Object PRESENT)
                   +-----------------------+------------------------------------+
                   | "Alice"               | static final Object PRESENT = new Object();
                   | "Bob"                 | static final Object PRESENT;
                   +-----------------------+------------------------------------+
```

---

## 2. Core Concepts & Set Implementation Taxonomy

### 2.1 The 3 Primary Java Set Implementations
1. **`HashSet`**: Backed by `HashMap`. Unordered, permits 1 `null` element, **$O(1)$ Average Time**.
2. **`LinkedHashSet`**: Backed by `LinkedHashMap`. Preserves **Insertion Order** via a doubly linked list running through all entries. **$O(1)$ Average Time**.
3. **`TreeSet`**: Backed by `NavigableMap` (`TreeMap` Red-Black Tree). Maintained in **Sorted Order** (Natural or custom `Comparator`). **$O(\log N)$ Logarithmic Time**.

```
Java Set Family Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Set Implementation    | Underlying Map    | Element Ordering  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| `HashSet`             | `HashMap`         | Unordered         | **$O(1)$ Average ⚡**|
| `LinkedHashSet`       | `LinkedHashMap`   | Insertion Order   | **$O(1)$ Average ⚡**|
| `TreeSet`             | `TreeMap` (BST)   | Sorted Order      | $O(\log N)$ Log   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"HashSet is unordered O(1); LinkedHashSet preserves insertion order O(1); TreeSet is sorted O(log N)!"**

---

## 3. Characteristics & Mathematical Set Algebra Operations

### 3.1 Fast Set Algebra via `HashSet`
1. **Union ($A \cup B$)**: Combines all elements from Set $A$ and Set $B$:
   `Set<T> union = new HashSet<>(setA); union.addAll(setB);` -> Time: $O(|A| + |B|)$.
2. **Intersection ($A \cap B$)**: Retains ONLY elements present in BOTH Set $A$ and Set $B$:
   `Set<T> intersect = new HashSet<>(setA); intersect.retainAll(setB);` -> Time: $O(|A|)$.
3. **Difference ($A \setminus B$)**: Removes all elements of Set $B$ from Set $A$:
   `Set<T> diff = new HashSet<>(setA); diff.removeAll(setB);` -> Time: $O(|A|)$.

```
Set Algebra Complexity & Operations Summary:
+-----------------------+-------------------+-------------------+-------------------+
| Set Algebra Method    | Java Collection   | Operation Intent  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| Union ($A \cup B$)    | `setA.addAll(B)`  | All unique elements| $O(|A| + |B|)$    |
| Intersection ($A \cap B$)| `setA.retainAll(B)`| Common elements   | $O(|A|)$          |
| Difference ($A \setminus B$)| `setA.removeAll(B)`| Elements only in A| $O(|A|)$         |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing `HashSet.add("Alice")`:

```
Call set.add("Alice"):
1. Internally delegates to: map.put("Alice", PRESENT).
2. If "Alice" did NOT exist in map:
   - map.put() inserts Key "Alice" with Value PRESENT and returns null.
   - set.add() checks: return map.put("Alice", PRESENT) == null -> Returns true! ✅
3. If "Alice" ALREADY existed in map:
   - map.put() overwrites value and returns previous value PRESENT.
   - set.add() checks: return map.put("Alice", PRESENT) == null -> Returns false! ✅

Uniqueness and O(1) membership guaranteed! ✅
```

---

## 5. Visual Diagram
HashSet Dummy Object `PRESENT` Shared Reference Topography:

```
HashSet Entries:
Key "Alice"  --->  Value  \
Key "Bob"    --->  Value  ----> [ Single Shared Object Dummy: PRESENT = new Object() ]
Key "Charlie"--->  Value  /
(Zero extra heap allocations for map values!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a custom `HashSet` (`SimpleHashSet`) replicating JDK Map-Backing architecture:

```java
import java.util.*;

public class HashSetImplementationMaster {

    // Complete Replica of JDK HashSet (HashMap Adapter Pattern Wrapper)
    public static class CustomHashSet<E> implements Iterable<E> {
        private final Map<E, Object> map;
        // Static dummy object used as constant value in backing HashMap
        private static final Object PRESENT = new Object();

        public CustomHashSet() {
            this.map = new HashMap<>();
        }

        public CustomHashSet(int initialCapacity) {
            this.map = new HashMap<>(initialCapacity);
        }

        // O(1) Average Add (Returns true if set changed)
        public boolean add(E element) {
            return map.put(element, PRESENT) == null;
        }

        // O(1) Average Remove
        public boolean remove(E element) {
            return map.remove(element) == PRESENT;
        }

        // O(1) Average Membership Test
        public boolean contains(E element) {
            return map.containsKey(element);
        }

        public int size() {
            return map.size();
        }

        public boolean isEmpty() {
            return map.isEmpty();
        }

        public void clear() {
            map.clear();
        }

        @Override
        public Iterator<E> iterator() {
            return map.keySet().iterator();
        }

        // --- Set Algebra Operations ---

        // Union: A u B
        public CustomHashSet<E> union(CustomHashSet<E> other) {
            CustomHashSet<E> result = new CustomHashSet<>(this.size() + other.size());
            for (E item : this) result.add(item);
            for (E item : other) result.add(item);
            return result;
        }

        // Intersection: A n B
        public CustomHashSet<E> intersection(CustomHashSet<E> other) {
            CustomHashSet<E> result = new CustomHashSet<>();
            for (E item : this) {
                if (other.contains(item)) {
                    result.add(item);
                }
            }
            return result;
        }

        // Difference: A \ B
        public CustomHashSet<E> difference(CustomHashSet<E> other) {
            CustomHashSet<E> result = new CustomHashSet<>();
            for (E item : this) {
                if (!other.contains(item)) {
                    result.add(item);
                }
            }
            return result;
        }
    }
}
```

> **Quick Syntax:**
```java
// Idiomatic HashSet Set Membership Check
Set<Integer> seen = new HashSet<>();
if (!seen.add(num)) {
    // Duplicate detected!
}
```

---

## 7. Concrete Problem Examples
* **Contains Duplicate (LeetCode 217)**: $O(1)$ set insertion uniqueness check.
* **Intersection of Two Arrays (LeetCode 349)**: Set intersection algebra.
* **Longest Consecutive Sequence (LeetCode 128)**: $O(1)$ set lookup for sequence bounds.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing custom `CustomHashSet` and Set Algebra:

```java
public class HashSetImplementationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Custom HashSet Basic Operations ===");
        HashSetImplementationMaster.CustomHashSet<String> set = 
            new HashSetImplementationMaster.CustomHashSet<>();

        System.out.println("Add \"Alice\": " + set.add("Alice")); // true
        System.out.println("Add \"Bob\":   " + set.add("Bob"));   // true
        System.out.println("Add Duplicate \"Alice\": " + set.add("Alice")); // false!

        System.out.println("Contains \"Alice\"? " + set.contains("Alice")); // true

        System.out.println("\n=== 2. Set Algebra Operations ===");
        HashSetImplementationMaster.CustomHashSet<Integer> setA = new HashSetImplementationMaster.CustomHashSet<>();
        HashSetImplementationMaster.CustomHashSet<Integer> setB = new HashSetImplementationMaster.CustomHashSet<>();

        setA.add(1); setA.add(2); setA.add(3);
        setB.add(2); setB.add(3); setB.add(4);

        System.out.print("Set A: [1, 2, 3], Set B: [2, 3, 4]\n");
        System.out.print("Intersection (A n B): ");
        for (int x : setA.intersection(setB)) System.out.print(x + " "); // Output: 2 3
        System.out.println();

        System.out.print("Difference (A \\ B): ");
        for (int x : setA.difference(setB)) System.out.print(x + " ");   // Output: 1
        System.out.println();
    }
}
```

---

## 9. Complexity Analysis

| Set Operation | HashSet Time | LinkedHashSet Time | TreeSet Time |
| :--- | :--- | :--- | :--- |
| **`add(element)`** | **$O(1)$ Average ⚡** | **$O(1)$ Average ⚡** | $O(\log N)$ Logarithmic |
| **`contains(element)`**| **$O(1)$ Average ⚡** | **$O(1)$ Average ⚡** | $O(\log N)$ Logarithmic |
| **`remove(element)`** | **$O(1)$ Average ⚡** | **$O(1)$ Average ⚡** | $O(\log N)$ Logarithmic |

---

## 10. Edge Cases & Boundary Handling
* **Null Elements**: `HashSet` permits 1 `null` element (stored at bucket 0). `TreeSet` throws `NullPointerException` (unless custom Comparator handles nulls).
* **Element Mutability**: Mutating an object inside a `HashSet` changes its hash code, corrupting set lookup.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `TreeSet` When Ordering is Unnecessary**:
  - `TreeSet` incurs an $O(\log N)$ time penalty per operation compared to $O(1)$ `HashSet`.
  - **Use `HashSet` unless elements MUST be maintained in sorted order**.
* **Mutating Set Elements After Insertion**:
  - Modifying an element's fields after adding it to a `HashSet` causes `contains()` to return `false` for an existing item!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `HashSet.add()` returns `boolean`:
> `map.put(key, PRESENT)` returns `null` if the key was NEW, or the previous value (`PRESENT`) if the key already existed.
> `HashSet.add(element)` evaluates:
> **`return map.put(element, PRESENT) == null;`**
> Returning `true` signals that the element was newly added; returning `false` signals that it was a duplicate!

> **Memory Trick:** **"HashSet.add() returns map.put(key, PRESENT) == null!"**

---

## 13. System & Implementation Comparisons

| Feature | `HashSet` | `TreeSet` |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(1)$ Average ⚡** | $O(\log N)$ Logarithmic |
| **Ordering** | Unordered | **Sorted (Natural / Comparator) ⚡** |
| **Null Support** | Permits 1 `null` | Throws `NullPointerException` |

---

## 14. How to Recognize This in Questions
* **"Check if element has been seen before in O(1) time"** $\rightarrow$ `HashSet`.
* **"Find elements unique to Set A or common to Set A and B"** $\rightarrow$ Set Algebra (`HashSet`).

---

## 15. Frequently Asked Interview Questions
* **Q: How does `HashSet` enforce element uniqueness?**  
  *A:* By delegating to `HashMap.put(key, PRESENT)`. `HashMap` evaluates `hashCode()` and `equals()` to prevent duplicate key entries.
* **Q: Why is a single static `PRESENT` object shared across all `HashSet` instances?**  
  *A:* Sharing a single `static final Object PRESENT = new Object();` eliminates allocating a new dummy value object for every set element, reducing memory consumption.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: HASHSET ARCHITECTURE & MAP BACKING                    |
+-----------------------------------------------------------------------+
| • Adapter Pattern: HashSet wraps an internal HashMap<E, Object>        |
| • Dummy Sentinel: Uses a static final Object PRESENT for all values   |
| • Add Formula: return map.put(element, PRESENT) == null               |
| • HashSet (O(1) Unordered) | LinkedHashSet (O(1) Order) | TreeSet (O(logN) Sorted)|
| • Set Algebra: addAll() = Union, retainAll() = Intersect, removeAll() = Diff|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can implement a custom `HashSet` wrapper around `HashMap`.
- [ ] I know why `HashSet` uses a static dummy `PRESENT` object.
- [ ] I can write Set Algebra methods (Union, Intersection, Difference).
- [ ] I know when to use `HashSet` vs `LinkedHashSet` vs `TreeSet`.
- [ ] I know why mutating set elements causes bugs.
