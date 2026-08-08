# 06. Fast Input / Output in Java for DSA

## 1. Introduction
High-speed Input/Output (I/O) processing is critical in technical coding interviews and competitive programming environments. When an online judge (LeetCode, HackerRank, Codeforces) tests your code with large input streams ($N \ge 10^5$ to $10^6$ integers or strings), standard I/O mechanisms like `java.util.Scanner` cause **Time Limit Exceeded (TLE)** failures due to regex overhead and buffer synchronization locks.

> **Important:** Standard `java.util.Scanner` takes $\approx 2.5$ to $3.0$ seconds to read $10^6$ integers, whereas `BufferedReader` with `StringTokenizer` processes the same input in under $0.25$ seconds—over **10x faster**!

## 2. Core Concepts
* **`java.util.Scanner` (Slow I/O)**: Uses heavy regular expression parsing under the hood for every `nextInt()` or `next()` call. Performs internal buffer synchronization and character-by-character checks.
* **`java.io.BufferedReader` (Fast I/O)**: Reads large chunks of character data into an internal 8KB buffer memory block in a single system read call ($O(1)$ amortized per line).
* **`java.util.StringTokenizer` (Fast Tokenizer)**: Breaks a string line into space-separated tokens using basic character array iteration, avoiding regex engine overhead.
* **`java.io.PrintWriter` / `BufferedWriter` (Fast Output)**: Buffers output characters in memory and writes to standard output (`System.out`) in batches, eliminating repeated expensive I/O system calls (`System.out.println()`).

> **Memory Trick:** **"Buffer the Input, Tokenize the Line, Flush the Output"**. Combine `BufferedReader` + `StringTokenizer` for reading and `PrintWriter` for writing.

## 3. Characteristics / Properties
* **I/O Performance Comparison Matrix**:

```
I/O Mechanism            Parsing Overhead     Buffer Size      Time for 10⁶ Integers
-------------------------------------------------------------------------------------
Scanner                  Heavy (Regex Engine) 1 KB             ~2.80 seconds (RISK TLE!)
BufferedReader + Tokens  Minimal (Char Loop)  8 KB             ~0.22 seconds (PASS ⚡)
Custom Byte FastReader   Zero (Raw Byte Stream) 32 KB / 64 KB   ~0.08 seconds (LIGHTNING 🚀)
```

* **Scanner Newline Pitfall**: Calling `scanner.nextLine()` immediately after `scanner.nextInt()` reads the leftover newline character `\n` instead of the next text line!
* **Auto-Flushing**: `System.out.println()` flushes the output stream on every call, executing a kernel context switch. `PrintWriter.print()` buffers data until `pw.flush()` is called explicitly.

## 4. Internal Working
Memory buffer mechanism comparison between `Scanner` and `BufferedReader`:

```
[ Scanner Execution Flow (Slow Regex Bottleneck) ]
System.in ---> [ 1KB Buffer ] ---> [ Regex Engine Pattern Matcher ] ---> Return int (Slow!)

[ BufferedReader Execution Flow (Fast Chunking) ]
System.in ---> [ 8KB Chunk Buffer ] ---> Read Line String ---> [ StringTokenizer ] ---> Return Token (Fast!)

[ PrintWriter Execution Flow (Fast Batch Output) ]
Code Output ---> [ Output Buffer ] ---> Single Batch System Call on flush() ---> Console / File
```

## 5. Visual Diagram
The Scanner Newline Bug Visualized:

```
Input Stream Buffer:   [ 4 2 ] [ \n ] [ H e l l o ] [ \n ]
                          ^      ^
                      nextInt()  nextLine() consumes THIS empty \n!
                                 (Fails to read "Hello"!)

Correct Fix:
int n = Integer.parseInt(br.readLine()); // Reads line "42" completely
String text = br.readLine();             // Reads line "Hello" cleanly
```

## 6. Operations / Algorithms
Constructing the Production-Grade FastReader Class:
1. Initialize `BufferedReader` wrapping `InputStreamReader(System.in)`.
2. Maintain a `StringTokenizer` reference.
3. Check `tokenizer.hasMoreTokens()`; if false, read next line via `br.readLine()`.
4. Parse primitives (`Integer.parseInt()`, `Long.parseLong()`).

> **Quick Syntax:**
```java
// Fast Reader Template for Coding Interviews
static class FastReader {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st;

    String next() {
        while (st == null || !st.hasMoreElements()) {
            try {
                String line = br.readLine();
                if (line == null) return null;
                st = new StringTokenizer(line);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return st.nextToken();
    }

    int nextInt() { return Integer.parseInt(next()); }
    long nextLong() { return Long.parseLong(next()); }
    double nextDouble() { return Double.parseDouble(next()); }
    String nextLine() {
        String str = "";
        try {
            if (st != null && st.hasMoreTokens()) {
                str = st.nextToken("\n");
            } else {
                str = br.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return str;
    }
}
```

## 7. Examples
* **Matrix Input Processing**: Reading an $R \times C$ matrix where $R, C \le 1000$ ($10^6$ elements).
* **Graph Adjacency List Parsing**: Reading $V$ vertices and $E$ edges ($E \ge 10^5$).
* **Large String Manipulations**: Reading multi-line inputs with custom space delimiters.

## 8. Java Code
Complete interview-ready Fast I/O suite with custom `FastReader` and `PrintWriter`:

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class FastIODemo {

    // FastReader Utility Class
    static class FastScanner {
        private final BufferedReader br;
        private StringTokenizer st;

        public FastScanner() {
            br = new BufferedReader(new InputStreamReader(System.in));
        }

        public String next() {
            while (st == null || !st.hasMoreTokens()) {
                try {
                    String line = br.readLine();
                    if (line == null) return null;
                    st = new StringTokenizer(line);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return st.nextToken();
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

        public long nextLong() {
            return Long.parseLong(next());
        }

        public String nextLine() {
            try {
                return br.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

    public static void main(String[] args) {
        // Instantiate Fast Reader and Fast Writer
        FastScanner in = new FastScanner();
        PrintWriter out = new PrintWriter(System.out);

        // Simulation: Processing large array input
        // Suppose input contains N followed by N integers
        /*
        int n = in.nextInt();
        long sum = 0;
        for (int i = 0; i < n; i++) {
            sum += in.nextInt();
        }
        out.println("Sum of " + n + " elements: " + sum);
        */

        out.println("Fast I/O System Ready! Always call out.flush() at the end.");
        
        // MANDATORY: Flush output buffer before exiting program
        out.flush();
        out.close();
    }
}
```

## 9. Complexity Analysis
| Input Mechanism | Time per $10^6$ Ints | Memory Footprint | Regex Overhead |
| :--- | :--- | :--- | :--- |
| **`Scanner`** | $\approx 2800$ ms | $1$ KB buffer | Heavy Regex Engine |
| **`BufferedReader` + `StringTokenizer`** | $\approx 220$ ms | $8$ KB buffer | Minimal String Tokenizing |
| **Custom Byte Stream (`DataInputStream`)**| $\approx 80$ ms | $32$ KB buffer | Zero (Raw Byte Shifts) |

## 10. Edge Cases
* **Missing `out.flush()`**: If using `PrintWriter` or `BufferedWriter`, forgetting `out.flush()` or `out.close()` leaves data sitting in the output buffer, resulting in **Empty Output / Wrong Answer** on online judges!
* **Empty Lines in Input**: `StringTokenizer` skips empty lines automatically; `br.readLine()` returns empty string `""` or `null` at EOF (End Of File).
* **EOF Exception**: Reading past End Of File returns `null` from `readLine()`. Always check `line != null`.

## 11. Common Mistakes
* Mixing `Scanner` and `BufferedReader` on `System.in` in the same program (causes buffer desynchronization and skipped input tokens).
* Using `System.out.println()` inside a loop that executes $10^5$ times (causes TLE due to $10^5$ individual console flushes).
* Forgetting to call `out.flush()` when using `PrintWriter`.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** On platforms like LeetCode, methods receive pre-parsed objects (`int[]`, `String`), so custom Fast I/O is not required. However, on platforms like HackerRank, Codeforces, and Google Code Jam where input is passed via standard input stream (`System.in`), using `FastScanner` and `PrintWriter` is MANDATORY to prevent TLE!

> **Memory Trick:** **"Always flush your PrintWriter"**:
> `out.flush(); out.close();` (Put at the very last line of `main()`).

## 13. Comparisons
| Feature | `Scanner` | `BufferedReader` + `StringTokenizer` |
| :--- | :--- | :--- |
| **Ease of Use** | High (`scanner.nextInt()`) | Medium (Requires template class) |
| **Speed** | Slow ($\approx 2.8$s for $10^6$ ints) | Fast ($\approx 0.22$s for $10^6$ ints) |
| **Thread Safety** | Synchronized | Unsynchronized (Faster) |
| **Buffer Size** | 1 KB | 8 KB |

## 14. How to Recognize This in Questions
* **"Input file contains $N = 10^6$ lines"** $\rightarrow$ Instantiate `FastScanner` immediately.
* **"Code passes 80% test cases but fails remaining with Time Limit Exceeded"** $\rightarrow$ Replace `Scanner` / `System.out.println()` with `FastScanner` and `PrintWriter`.

## 15. Frequently Asked Interview Questions
* **Q: Why is `Scanner` significantly slower than `BufferedReader`?**  
  *A:* `Scanner` uses regular expressions to parse data types (`nextInt()`, `nextDouble()`), performs pattern matching on every token, uses a tiny 1KB buffer, and synchronizes input reads. `BufferedReader` simply reads large 8KB character blocks into memory without regex overhead.
* **Q: What happens if you forget to call `out.flush()` on a `PrintWriter`?**  
  *A:* The buffered output stored in memory is never written to standard output (`System.out`), resulting in an empty or incomplete response being submitted to the judge system.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FAST INPUT / OUTPUT IN JAVA                           |
+-----------------------------------------------------------------------+
| • Scanner is slow due to heavy Regex parsing (Risk TLE on N >= 10^5)  |
| • Fast Pattern: BufferedReader + StringTokenizer (10x faster)         |
| • Fast Output: PrintWriter (Batch output buffer)                      |
| • Mandatory Rule: Always call `out.flush()` at the end of main()      |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can explain why `Scanner` is slow compared to `BufferedReader`.
- [ ] I can write the `FastScanner` template class from memory.
- [ ] I know how to use `PrintWriter` for fast batched output.
- [ ] I understand the `Scanner.nextLine()` newline consumption bug.
- [ ] I remember to include `out.flush()` before method completion.
