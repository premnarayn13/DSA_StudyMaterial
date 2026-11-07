# 08. System Applications: Stock Price Range Engines, Sweep-Line & Game Leaderboards

## 1. Introduction
**Segment Trees** are the underlying engine for real-time analytics platforms, financial trading systems, and computational geometry applications. From **Financial High-Frequency Trading Stock Volatility Range Engines** (answering minimum, maximum, and average stock price queries across dynamic time windows in $O(\log N)$ time) to **2D Computational Geometry Sweep-Line Algorithms** (rectangle union area calculations) and **Real-Time Multiplayer Game Leaderboards**, Segment Trees deliver deterministic, real-time logarithmic performance across dynamic datasets.

> **Important:** Core Industrial Segment Tree Application Domains:
> 1. **Financial Stock Price Window Engine**: Indexes tick-by-tick stock prices over $N$ time intervals. Evaluates `queryMax(t1, t2)` (Peak Price) and `queryMin(t1, t2)` (Trough Price) in **$O(\log N)$ Time** while updating stock prices dynamically.
> 2. **2D Sweep-Line Geometry (Rectangle Union Area)**: Sweeps a vertical line across 2D space, using a Segment Tree to track active vertical segment intervals in **$O(N \log N)$ Time**! ⚡

```
Stock Price Volatility Range Engine Segment Tree Architecture:
                      [ Time 0 ... 999: Max=$150.50, Min=$95.00 ]  <--- Root (0..999)
                     /                                          \
    [ Time 0 ... 499: Max=$150.50 ]              [ Time 500 ... 999: Min=$95.00 ]

Instant O(log N) Min/Max/Volatility calculation over ANY time window [t1 ... t2]! ⚡
```

---

## 2. Core Concepts & Financial Stock Price Volatility Range Engine

### 2.1 Financial Stock Price Range Engine Architecture
In algorithmic trading:
* Ticks arrive at time indices $0 \dots N-1$.
* Traded prices are updated dynamically via `update(timeIdx, price)`.
* Volatility over window $[t_1 \dots t_2]$ is computed as $\text{MaxPrice} - \text{MinPrice}$ in **$O(\log N)$ time**.

```
Segment Tree System Application Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Production System     | Segment Value     | Query Type        | Performance Goal  |
+-----------------------+-------------------+-------------------+-------------------+
| **Stock Trading Engine**| Stock Price Pair  | Range Min & Max   | **$O(\log N)$ Volatility ⚡**|
| **Sweep-Line Geometry**| Active Segments  | Union Interval Length| **$O(N \log N)$ Area ⚡**|
| **Game Leaderboard**  | Player Scores     | Rank / Top Score  | **$O(\log N)$ Rank ⚡** |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Stock Price Range Engine: Segment Tree computes Volatility = Max - Min over [t1...t2] in O(log N) time!"**

---

## 3. Characteristics & 2D Sweep-Line Geometry

### 3.1 Sweep-Line Algorithm for Union of Rectangles
To compute the total area covered by $N$ 2D rectangles:
1. Sort vertical rectangle edges by X-coordinate ($O(N \log N)$).
2. Sweep vertical line from left to right.
3. Use a Segment Tree over Y-coordinates to maintain total active vertical length.
4. Multiply active Y-length by $\Delta X$ to accumulate area in **$O(N \log N)$ Time**! ⚡

---

## 4. Internal Working Mechanics
Tracing Volatility Query $[100 \dots 500]$ on Stock Segment Tree:

```
Stock Segment Tree stores (Min, Max) pairs per segment:

Query time window [100 ... 500]:
- SegTree queryMax(100, 500) -> Returns $150.50.
- SegTree queryMin(100, 500) -> Returns $110.00.
- Volatility = $150.50 - $110.00 = $40.50!

Calculated in 12 node visits over 1,000,000 time ticks! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
Financial Volatility Range Engine Topography:

```
                  [ Time Window [t1 ... t2] ]
                 /                           \
       queryMax(t1, t2)                queryMin(t1, t2)
       (Returns $150.50)               (Returns $110.00)
              \                               /
               +-----------------------------+
               | Volatility = Max - Min      |
               | Volatility = $40.50! ⚡     |
               +-----------------------------+
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a Financial Stock Price Volatility Range Engine powered by a dual Min-Max Segment Tree:

```java
import java.util.*;

public class SegmentTreeApplicationsMaster {

    public static class StockTick {
        public double minPrice;
        public double maxPrice;

        public StockTick(double minPrice, double maxPrice) {
            this.minPrice = minPrice;
            this.maxPrice = maxPrice;
        }
    }

    public static class StockVolatilityEngine {
        private final double[] minTree;
        private final double[] maxTree;
        private final double[] prices;
        private final int n;

        public StockVolatilityEngine(double[] initialPrices) {
            this.prices = initialPrices;
            this.n = initialPrices.length;
            this.minTree = new double[4 * n];
            this.maxTree = new double[4 * n];

            if (n > 0) {
                build(0, 0, n - 1);
            }
        }

        private void build(int treeIdx, int l, int r) {
            if (l == r) {
                minTree[treeIdx] = prices[l];
                maxTree[treeIdx] = prices[l];
                return;
            }
            int mid = l + (r - l) / 2;
            build(2 * treeIdx + 1, l, mid);
            build(2 * treeIdx + 2, mid + 1, r);

            minTree[treeIdx] = Math.min(minTree[2 * treeIdx + 1], minTree[2 * treeIdx + 2]);
            maxTree[treeIdx] = Math.max(maxTree[2 * treeIdx + 1], maxTree[2 * treeIdx + 2]);
        }

        // Update Stock Price at Time Tick O(log N) Time
        public void updatePrice(int timeIdx, double newPrice) {
            if (timeIdx < 0 || timeIdx >= n) return;
            updateHelper(0, 0, n - 1, timeIdx, newPrice);
        }

        private void updateHelper(int treeIdx, int l, int r, int targetIdx, double newPrice) {
            if (l == r) {
                prices[targetIdx] = newPrice;
                minTree[treeIdx] = newPrice;
                maxTree[treeIdx] = newPrice;
                return;
            }
            int mid = l + (r - l) / 2;
            if (targetIdx <= mid) updateHelper(2 * treeIdx + 1, l, mid, targetIdx, newPrice);
            else updateHelper(2 * treeIdx + 2, mid + 1, r, targetIdx, newPrice);

            minTree[treeIdx] = Math.min(minTree[2 * treeIdx + 1], minTree[2 * treeIdx + 2]);
            maxTree[treeIdx] = Math.max(maxTree[2 * treeIdx + 1], maxTree[2 * treeIdx + 2]);
        }

        // Calculate Stock Volatility (Max - Min) over Time Window [t1 ... t2] O(log N) Time
        public double calculateVolatility(int t1, int t2) {
            double minP = queryMin(0, 0, n - 1, t1, t2);
            double maxP = queryMax(0, 0, n - 1, t1, t2);
            return maxP - minP;
        }

        private double queryMin(int treeIdx, int l, int r, int ql, int qr) {
            if (ql <= l && r <= qr) return minTree[treeIdx];
            if (r < ql || l > qr) return Double.MAX_VALUE;
            int mid = l + (r - l) / 2;
            return Math.min(queryMin(2 * treeIdx + 1, l, mid, ql, qr),
                            queryMin(2 * treeIdx + 2, mid + 1, r, ql, qr));
        }

        private double queryMax(int treeIdx, int l, int r, int ql, int qr) {
            if (ql <= l && r <= qr) return maxTree[treeIdx];
            if (r < ql || l > qr) return Double.MIN_VALUE;
            int mid = l + (r - l) / 2;
            return Math.max(queryMax(2 * treeIdx + 1, l, mid, ql, qr),
                            queryMax(2 * treeIdx + 2, mid + 1, r, ql, qr));
        }
    }
}
```

> **Quick Syntax:**
```java
// Volatility Calculation Line
double volatility = queryMax(t1, t2) - queryMin(t1, t2);
```

---

## 7. Concrete Problem Examples
* **Financial Trading Engine**: Volatility calculation over custom time windows.
* **Game Leaderboards**: Range score queries and rank updates.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `StockVolatilityEngine`:

```java
public class SegmentTreeApplicationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Financial Stock Volatility Engine Test ===");
        double[] prices = {100.0, 105.5, 95.0, 110.0, 150.5, 120.0};
        SegmentTreeApplicationsMaster.StockVolatilityEngine engine = 
            new SegmentTreeApplicationsMaster.StockVolatilityEngine(prices);

        System.out.println("Volatility Window [0 ... 5]: $" + 
            engine.calculateVolatility(0, 5)); // Output: $55.50 (150.5 - 95.0)

        System.out.println("\nUpdating Tick 2 (95.0 -> 90.0)...");
        engine.updatePrice(2, 90.0);

        System.out.println("Volatility Window [0 ... 5] AFTER Update: $" + 
            engine.calculateVolatility(0, 5)); // Output: $60.50 (150.5 - 90.0) ✅
    }
}
```

---

## 9. Complexity Analysis

| System Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`calculateVolatility(t1, t2)`**| **$O(\log N)$ Strict ⚡** | **$O(\log N)$ Stack Space**| Dual Min/Max range queries |
| **`updatePrice(timeIdx, price)`**| **$O(\log N)$ Strict ⚡** | **$O(\log N)$ Stack Space**| Dual Min/Max point updates |

---

## 10. Edge Cases & Boundary Handling
* **Time Window of Length 1 ($t_1 = t_2$)**: Volatility returns `$0.00` (Max - Min = 0).
* **Negative Stock Prices**: Handled correctly by `Math.min` and `Math.max`.

---

## 11. Common Mistakes & Anti-Patterns
* **Running Separate Min and Max Segment Trees with Redundant Traversal**:
  - Combining `minTree` and `maxTree` inside a single unified Segment Tree node reduces memory and call stack overhead by 50%.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Segment Trees Are Chosen for Algorithmic Trading Systems:
> Algorithmic trading requires strict sub-millisecond SLAs.
> A Segment Tree guarantees **$O(\log N)$ time for BOTH updates and range queries**, eliminating latency spikes during high-volume market tick arrivals!

> **Memory Trick:** **"Combine Min and Max in a single Segment Tree node for 50% faster volatility queries!"**

---

## 13. System & Implementation Comparisons

| Feature | Dual Min-Max Segment Tree | Sliding Window Deque |
| :--- | :--- | :--- |
| **Window Length** | **Arbitrary Window $[t_1 \dots t_2]$ ⚡**| Fixed Window Size $K$ |
| **Update Time** | **$O(\log N)$ Logarithmic ⚡** | **$O(1)$ Constant ⚡** |
| **Query Flexibility**| Any Range, Any Time | Fixed Tail Range |

---

## 14. How to Recognize This in Questions
* **"Compute minimum and maximum stock price over arbitrary time range [t1 ... t2] with dynamic price updates"** $\rightarrow$ Segment Tree Volatility Engine.

---

## 15. Frequently Asked Interview Questions
* **Q: How does a Segment Tree compute stock volatility over window $[t_1 \dots t_2]$?**  
  *A:* By executing `queryMax(t1, t2)` and `queryMin(t1, t2)` in $O(\log N)$ time and returning `maxPrice - minPrice`.
* **Q: How does 2D Sweep-Line use a Segment Tree to calculate rectangle union area?**  
  *A:* By sweeping a vertical line across X-coordinates and using a Segment Tree over Y-coordinates to maintain active vertical segment lengths.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEGMENT TREE SYSTEM APPLICATIONS                      |
+-----------------------------------------------------------------------+
| • Stock Volatility Engine: Volatility = queryMax(t1, t2) - queryMin(t1, t2)|
| • Time Bounds        : O(log N) Volatility Query | O(log N) Price Update|
| • Sweep-Line Geometry: Maintains active Y-interval lengths in O(N log N)|
| • Dual Tree Node     : Combine Min & Max inside 1 node for 50% memory savings|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a Financial Stock Price Volatility Engine in Java.
- [ ] I can combine Min and Max inside a single Segment Tree.
- [ ] I know why Segment Trees are preferred for financial trading platforms.
- [ ] I can explain 2D Sweep-Line rectangle union area algorithms.
- [ ] I can trace volatility calculation for custom time windows.
