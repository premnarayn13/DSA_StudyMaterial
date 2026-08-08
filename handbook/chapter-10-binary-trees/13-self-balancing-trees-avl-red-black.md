# 13. Self-Balancing Trees: AVL Trees, Red-Black Trees & Java TreeMap Architecture

## 1. Introduction
Unbalanced Binary Search Trees can degenerate into $O(N)$ linear chains when keys are inserted in sorted or semi-sorted order. **Self-Balancing Binary Search Trees**—primarily **AVL Trees** and **Red-Black Trees**—solve this degeneration by performing local structural **Tree Rotations** during insertions and deletions, guaranteeing **Strict $O(\log N)$ logarithmic time complexity** for search, insertion, and deletion operations under all workload conditions. In Java's Standard Library, **`java.util.TreeMap`** and **`java.util.TreeSet`** are implemented as Red-Black Trees.

> **Important:** While AVL Trees enforce a stricter height balance constraint ($|\text{balanceFactor}| \le 1$), requiring more frequent rotations during writes, Red-Black Trees relax the balance constraint slightly, requiring at most **2 rotations per insertion** and **3 rotations per deletion**. This makes Red-Black Trees the preferred choice for general-purpose map and set libraries!

```
Self-Balancing BST Trade-Off Spectrum:
+-----------------------------------------------------------------------------------+
| Unbalanced BST   : Height H = O(N) Worst Case  -> Search/Insert/Delete O(N)       |
| AVL Tree         : Balance Factor <= 1         -> Strict H = 1.44 log N (Read Fast)|
| Red-Black Tree   : Black-Height Invariants     -> Relaxed H <= 2 log N (Write Fast)|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Rotation Mechanics

### 2.1 Tree Rotations (The Fundamental Rebalancing Building Block)
Rotations change the local structure of a tree without violating the BST property ($L < X < R$).

#### Left Rotation (`rotateLeft(X)`):
Brings node $X$'s right child $Y$ up to replace $X$, making $X$ the left child of $Y$:
```
     ( X )                      ( Y )
    /     \                    /     \
  t1      ( Y )    ===>      ( X )    t3
         /     \            /     \
       t2      t3         t1      t2
```
* **Pointer Assignments**:
  - `X.right = Y.left`
  - `Y.left = X`

#### Right Rotation (`rotateRight(Y)`):
Brings node $Y$'s left child $X$ up to replace $Y$, making $Y$ the right child of $X$:
```
        ( Y )                  ( X )
       /     \                /     \
     ( X )    t3   ===>     t1      ( Y )
    /     \                        /     \
  t1      t2                     t2      t3
```
* **Pointer Assignments**:
  - `Y.left = X.right`
  - `X.right = Y`

---

## 3. AVL Trees & The 4 Rotation Cases

### 3.1 AVL Balance Factor Invariant
For every node $X$ in an AVL Tree:

$$\text{BalanceFactor}(X) = \text{Height}(\text{left}) - \text{Height}(\text{right}) \in \{-1, 0, 1\}$$

If $|\text{BalanceFactor}(X)| > 1$, node $X$ is unbalanced!

### 3.2 The 4 Rebalancing Cases
1. **Left-Left (LL) Case**: Insertion into left subtree of left child ($\text{BF} > 1$, $\text{left.BF} \ge 0$).
   - *Fix*: Perform **Single Right Rotation** on $X$.
2. **Right-Right (RR) Case**: Insertion into right subtree of right child ($\text{BF} < -1$, $\text{right.BF} \le 0$).
   - *Fix*: Perform **Single Left Rotation** on $X$.
3. **Left-Right (LR) Case**: Insertion into right subtree of left child ($\text{BF} > 1$, $\text{left.BF} < 0$).
   - *Fix*: Perform **Left Rotation on Left Child**, then **Right Rotation on $X$**.
4. **Right-Left (RL) Case**: Insertion into left subtree of right child ($\text{BF} < -1$, $\text{right.BF} > 0$).
   - *Fix*: Perform **Right Rotation on Right Child**, then **Left Rotation on $X$**.

```
AVL 4 Rotation Cases Summary:
+-----------------------+-------------------+-------------------+-------------------+
| Unbalance Case        | Balance Factors   | Primary Cause     | Required Rotations|
+-----------------------+-------------------+-------------------+-------------------+
| Left-Left (LL)        | BF(X)>1, BF(L)>=0 | Left-Left Heavy   | Single Right(X)   |
| Right-Right (RR)      | BF(X)<-1, BF(R)<=0| Right-Right Heavy | Single Left(X)    |
| Left-Right (LR)       | BF(X)>1, BF(L)<0  | Left-Right Heavy  | Left(L) + Right(X)|
| Right-Left (RL)       | BF(X)<-1, BF(R)>0 | Right-Left Heavy  | Right(R) + Left(X)|
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Red-Black Trees & The 5 Invariants

A **Red-Black Tree** is a self-balancing BST where each node contains an extra color bit (`RED` or `BLACK`).

### 4.1 The 5 Red-Black Invariants
1. **Node Color Rule**: Every node is either `RED` or `BLACK`.
2. **Root Rule**: The Root node is ALWAYS `BLACK`.
3. **Leaf (NIL) Rule**: Every Leaf (`NIL` sentinel node) is `BLACK`.
4. **Red Parent-Child Rule**: If a node is `RED`, both of its children MUST be `BLACK` (No two adjacent `RED` nodes along any path!).
5. **Black Height Invariant**: Every path from any node to its descendant `NIL` leaves contains the **EXACT SAME NUMBER OF BLACK NODES**.

### 4.2 Height Bounding Theorem
The 5 invariants guarantee that the longest path from the root to any leaf is **at most twice as long as the shortest path**!
$$\text{Height}(H) \le 2 \log_2(N + 1) = \mathbf{O(\log N)}$$

> **Memory Trick:** **"AVL = Balance Factor <= 1 (Strict, Fast Reads)! Red-Black = Equal Black Height on all paths (Fast Writes)!"**

---

## 5. Visual Diagram
AVL Left-Right (LR) Double Rotation Mechanics:

```
Unbalanced (LR Case):         Left-Rotate Left Child (2):       Right-Rotate Root (5):
         ( 5 ) BF=+2                     ( 5 )                         ( 3 )
        /                               /                             /     \
      ( 2 ) BF=-1        ===>         ( 3 )           ===>          ( 2 )   ( 5 )
         \                           /
         ( 3 )                     ( 2 )
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing an AVL Tree with complete LL, RR, LR, and RL rotations:

```java
import java.util.*;

public class SelfBalancingTreeMaster {

    public static class AVLNode {
        public int val;
        public int height;
        public AVLNode left;
        public AVLNode right;

        public AVLNode(int val) {
            this.val = val;
            this.height = 1;
        }
    }

    public static class AVLTree {
        private AVLNode root;

        public int height(AVLNode node) {
            return node == null ? 0 : node.height;
        }

        public int getBalance(AVLNode node) {
            return node == null ? 0 : height(node.left) - height(node.right);
        }

        private void updateHeight(AVLNode node) {
            node.height = 1 + Math.max(height(node.left), height(node.right));
        }

        // 1. Single Right Rotation (LL Case)
        private AVLNode rotateRight(AVLNode y) {
            AVLNode x = y.left;
            AVLNode T2 = x.right;

            // Perform Rotation
            x.right = y;
            y.left = T2;

            // Update Heights
            updateHeight(y);
            updateHeight(x);

            return x; // New root of subtree
        }

        // 2. Single Left Rotation (RR Case)
        private AVLNode rotateLeft(AVLNode x) {
            AVLNode y = x.right;
            AVLNode T2 = y.left;

            // Perform Rotation
            y.left = x;
            x.right = T2;

            // Update Heights
            updateHeight(x);
            updateHeight(y);

            return y; // New root of subtree
        }

        // 3. Insert Node into AVL Tree O(log N) Time
        public void insert(int val) {
            root = insertHelper(root, val);
        }

        private AVLNode insertHelper(AVLNode node, int val) {
            if (node == null) return new AVLNode(val);

            if (val < node.val) {
                node.left = insertHelper(node.left, val);
            } else if (val > node.val) {
                node.right = insertHelper(node.right, val);
            } else {
                return node; // Duplicate keys not allowed in standard AVL
            }

            // Update height of ancestor node
            updateHeight(node);

            // Compute balance factor to check for unbalance
            int balance = getBalance(node);

            // Case 1: Left-Left (LL)
            if (balance > 1 && val < node.left.val) {
                return rotateRight(node);
            }

            // Case 2: Right-Right (RR)
            if (balance < -1 && val > node.right.val) {
                return rotateLeft(node);
            }

            // Case 3: Left-Right (LR)
            if (balance > 1 && val > node.left.val) {
                node.left = rotateLeft(node.left);
                return rotateRight(node);
            }

            // Case 4: Right-Left (RL)
            if (balance < -1 && val < node.right.val) {
                node.right = rotateRight(node.right);
                return rotateLeft(node);
            }

            return node;
        }

        public List<Integer> inorder() {
            List<Integer> list = new ArrayList<>();
            inorderHelper(root, list);
            return list;
        }

        private void inorderHelper(AVLNode node, List<Integer> list) {
            if (node == null) return;
            inorderHelper(node.left, list);
            list.add(node.val);
            inorderHelper(node.right, list);
        }
    }
}
```

> **Quick Syntax:**
```java
// AVL Left-Right (LR) Double Rotation
if (balance > 1 && val > node.left.val) {
    node.left = rotateLeft(node.left);
    return rotateRight(node);
}
```

---

## 7. Concrete Problem Examples
* **LeetCode 110 - Balanced Binary Tree**: Checking balance factor invariants.
* **LeetCode 108 - Convert Sorted Array to Binary Search Tree**: Building height-balanced BST in $O(N)$ time.
* **Java `TreeMap` & `TreeSet`**: Red-Black Tree implementation.

---

## 8. Java Code Demonstration & Dry Run
Demonstration inserting sorted sequence into AVL Tree and verifying height balancing:

```java
public class SelfBalancingTreeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Inserting Sorted Sequence into AVL Tree ===");
        SelfBalancingTreeMaster.AVLTree avl = new SelfBalancingTreeMaster.AVLTree();

        // Inserting 1..7 (Unbalanced BST would degrade to height 6)
        for (int i = 1; i <= 7; i++) {
            avl.insert(i);
        }

        System.out.println("In-Order Traversal: " + avl.inorder()); // Output: [1, 2, 3, 4, 5, 6, 7]
        System.out.println("Tree Height after 7 inserts: " + avl.height(avl.root) + " (Expected Logarithmic Height: 3)");
    }
}
```

---

## 9. Complexity Analysis

| Operation | Unbalanced BST | AVL Tree | Red-Black Tree (`TreeMap`) |
| :--- | :--- | :--- | :--- |
| **Search** | $O(N)$ Worst Case | **$O(\log N)$ (Faster Reads ⚡)** | **$O(\log N)$ Logarithmic** |
| **Insertion** | $O(N)$ Worst Case | **$O(\log N)$ (More Rotations)** | **$O(\log N)$ (Faster Writes ⚡)** |
| **Deletion** | $O(N)$ Worst Case | **$O(\log N)$** | **$O(\log N)$ (Max 3 Rotations)** |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Insertions**: Standard self-balancing BSTs either ignore duplicates or maintain count fields.
* **Re-balancing Single Node Trees**: Rotations executed on nodes with null subtrees update heights cleanly without null pointer crashes.

---

## 11. Common Mistakes & Anti-Patterns
* **Confusing LL/RR Rotations with LR/RL Rotations**:
  - LL case requires single Right rotation.
  - LR case requires Left rotation on child FIRST, then Right rotation on root!
* **Forgetting to Update Heights After Rotations**: Failing to call `updateHeight()` causes stale balance factor calculations.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Java `TreeMap` Uses Red-Black Trees over AVL Trees:
> AVL Trees re-balance aggressively, guaranteeing a maximum height of $\sim 1.44 \log_2 N$.
> Red-Black Trees allow slightly higher height ($\le 2 \log_2 N$), but require **fewer rotations during insertion and deletion** (at most 2 rotations for insert, 3 for delete).
> For general-purpose Java collections with frequent writes, Red-Black Trees offer superior overall throughput!

> **Memory Trick:** **"AVL = Strict Height (Fast Lookup)! Red-Black = Max 3 Rotations (Fast Mutations)!"**

---

## 13. System & Implementation Comparisons

| Feature | AVL Tree | Red-Black Tree (`TreeMap`) |
| :--- | :--- | :--- |
| **Max Height Bound** | $1.44 \log_2 N$ (Stricter) | $2 \log_2 N$ (Relaxed) |
| **Max Rotations (Insert)** | $O(\log N)$ | **At most 2 Rotations ⚡** |
| **Max Rotations (Delete)** | $O(\log N)$ | **At most 3 Rotations ⚡** |

---

## 14. How to Recognize This in Questions
* **"Design a map maintaining sorted keys with guaranteed logarithmic lookups and range queries"** $\rightarrow$ Red-Black Tree (`TreeMap` / `TreeSet`).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Red-Black Tree insertion require at most 2 rotations?**  
  *A:* Because recoloring nodes handles most invariant violations. When recoloring reaches a black uncle node, a single or double rotation restores all 5 Red-Black invariants permanently.
* **Q: How does `rotateRight(y)` maintain the BST property?**  
  *A:* `rotateRight(y)` sets `x = y.left`. It moves `x.right` to `y.left` (valid since `x.right > x` and `< y`) and sets `x.right = y`. The relative ordering of all subtrees is completely preserved.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SELF-BALANCING TREES (AVL & RED-BLACK)               |
+-----------------------------------------------------------------------+
| • Balance Factor (AVL): BF = height(left) - height(right) in {-1,0,1} |
| • LL Case: BF > 1 & val < left.val -> Single Right Rotation           |
| • RR Case: BF < -1 & val > right.val -> Single Left Rotation          |
| • LR Case: BF > 1 & val > left.val -> Left(left) then Right(root)     |
| • RL Case: BF < -1 & val < right.val -> Right(right) then Left(root)  |
| • Red-Black 5 Rules: Root is Black; Red node has Black children;      |
|   Equal Black Height on all root-to-leaf paths                         |
| • Java Choice: TreeMap uses Red-Black Trees (Max 2 insert rotations)  |
| • Complexity: Strict O(log N) Search, Insert, Delete                  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can draw single Left and Right rotations.
- [ ] I know all 4 AVL rotation cases (LL, RR, LR, RL).
- [ ] I can state the 5 Red-Black Tree invariants.
- [ ] I know why Java `TreeMap` uses Red-Black Trees over AVL Trees.
- [ ] I can implement an AVL Tree `insert()` function with height updates.
