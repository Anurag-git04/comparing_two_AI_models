Prompt: Explain how a hash map works in about 150 words.

| Provider | Model | TTFT (s) | Latency (s) | In tok | Out tok | Total tok | Out tok/s |
|---|---|---|---|---|---|---|---|
| Groq | openai/gpt-oss-120b | 0.999 | 1.532 | 83 | 290 | 373 | 544.2 |
| Groq | openai/gpt-oss-20b | 0.197 | 0.464 | 83 | 308 | 391 | 1150.7 |
| Gemini | gemini-3.8-flash | 14.760 | 14.768 | 15 | 568 | 583 | 73399.2 |

## openai/gpt-oss-120b

A hash map (or hash table) stores key‑value pairs for fast lookup, insertion, and deletion. When you add an entry, the key is passed through a **hash function** that converts it into an integer hash code. This code is then reduced (often by modulo the table’s size) to an **index** that points to a bucket in an underlying array.

If two different keys produce the same index—a **collision**—the map must handle it. Common strategies are:

* **Separate chaining:** each bucket holds a linked list (or another dynamic container) of all entries that hash to that slot.
* **Open addressing:** the map probes other slots (linear, quadratic, or double hashing) until it finds an empty one.

When you look up a key, the same hash function calculates its index, then the bucket is examined (or the probe sequence followed) to find the matching key and return its value.  

To keep operations near O(1), the table **resizes** (usually doubling its capacity) when a load factor (entries / buckets) exceeds a threshold, re‑hashing all existing keys into the larger array. This maintains low collision rates and preserves fast average‑case performance.

## openai/gpt-oss-20b

A hash map stores key‑value pairs in an array of “buckets.” When you insert or look up a key, a hash function turns the key into an integer, which is then reduced modulo the array size to pick a bucket. If the bucket is empty, the key/value is stored there. If it’s already occupied, the map must resolve the “collision.” Two common strategies are:

1. **Chaining** – each bucket holds a small linked list (or tree) of entries; new entries are appended.
2. **Open addressing** – the map probes other buckets (linear, quadratic, or double hashing) until an empty one is found.

The map tracks a *load factor* (entries ÷ bucket count). When it exceeds a threshold, the array is resized (usually doubled) and all entries are rehashed. Average‑case lookup, insert, and delete run in O(1) time, but worst‑case can degrade to O(n) if many collisions occur. This simplicity and speed make hash maps ideal for dictionaries, caches, and associative arrays.

## gemini-3.8-flash

A hash map (or hash table) is a data structure that stores data as key-value pairs, designed for ultra-fast data retrieval. 

It works using an underlying array and a **hash function**. When you add an entry, the hash function processes the key and converts it into a numerical index. The value is then stored in the array at that specific location. 

To retrieve the value later, the map runs the key through the same hash function, instantly recalculating the index and locating the data. Because it jumps directly to the memory address rather than searching through elements one by one, operations like lookups, insertions, and deletions take constant time, or $O(1)$, on average.

When two different keys generate the same index—known as a **collision**—the hash map resolves it, typically by using **chaining** (storing multiple items in a linked list at that index) or **open addressing** (finding the next available slot).
