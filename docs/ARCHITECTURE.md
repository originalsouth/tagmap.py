# TagMap Architecture

Internal architecture and implementation details of TagMap.

## Overview

TagMap uses a Python/C++ architecture where performance-critical operations are implemented in C++ and exposed via pybind11. The design emphasizes both speed and usability with a familiar dictionary-like interface.

## Project Structure

```
├── tagmap_pybind.cc     # C++ implementation + pybind11 bindings
├── setup.py             # Build configuration
├── pyproject.toml       # Project metadata
├── test_tagmap.py       # Test suite
├── docs/
│   ├── API.md           # API reference
│   ├── EXAMPLES.md      # Usage examples
│   └── ARCHITECTURE.md  # This file
└── [other files]
```

## C++ Data Structures

TagMap maintains three core data structures:

**1. Main Index**
```cpp
std::unordered_map<std::string, std::unordered_set<std::string>> data;
```
Maps keys to tag sets. Provides O(1) key lookup and O(1) tag membership checks.

**2. Inverted Index**
```cpp
std::unordered_map<std::string, std::unordered_set<std::string>> tag_index;
```
Maps each tag to the set of keys with that tag. Enables fast query operations without scanning all entries.

**3. Tag Set**
```cpp
std::unordered_set<std::string> all_tags;
```
Stores all unique tags used in the map.

## Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `m[key] = tags` | O(n) | n = number of tags assigned |
| `m[key]` | O(1) | Lookup |
| `add_tag(key, tag)` | O(1) | Average case |
| `remove_tag(key, tag)` | O(1) | Average case |
| `has_tag(key, tag)` | O(1) | Membership check |
| `query(*tags)` | O(k·m) | k = result size, m = avg tags per key |
| `query_any(*tags)` | O(n) | n = sum of keys for all tags |
| `count(tags)` | O(k) | k = intersection size |
| `erase_where(tags)` | O(k·n) | k = keys to remove, n = tags per key |

---

## Query Algorithms

### AND Query

Finds keys with **all** specified tags.

**Algorithm**:
1. Get all keys with the first tag from the inverted index
2. For each subsequent tag, intersect with the result set
3. Return the final intersection

**Example**:
```
Keys with "dev": {alice, bob, carol}
Keys with "python": {alice, dave}
Result: {alice}
```

### OR Query

Finds keys with **any** of the specified tags.

**Algorithm**:
1. Get all keys for each tag from the inverted index
2. Union all key sets
3. Return the final union

**Example**:
```
Keys with "dev": {alice, bob, carol}
Keys with "ops": {dave, eve}
Result: {alice, bob, carol, dave, eve}
```

---

## Memory Management

All memory is managed by C++ standard library and Python's reference counting. No manual memory allocation is needed.

- Strings stored as `std::string`
- Sets allocated with `std::unordered_set` with automatic resizing
- pybind11 handles Python object lifecycle

## Optimizations

**Hash-Based Lookups**: Uses `std::unordered_map` and `std::unordered_set` for O(1) operations.

**Inverted Index**: Enables fast queries without full table scans. Trade-off: approximately 2x memory usage for significantly faster queries.

**Set Operations**: Intersection and union algorithms optimized for efficiency.

**Compilation Flags**: Build uses `-Ofast -march=native -flto=auto` for aggressive optimizations.

## Design Rationale

**C++**: Provides 10-100x performance improvement over pure Python for large datasets and memory-efficient representation.

**Inverted Index**: Trades ~2x memory for O(k) queries instead of O(n) full table scans.

**Hash Tables**: Provides O(1) average lookups and simple collision handling via standard library.

**pybind11**: Minimal boilerplate, automatic type conversion, zero-copy bindings.

## Future Improvements

Potential optimizations:
- Memory pooling for bulk operations
- Multi-threaded operations
- Binary serialization format
- Bloom filters for probabilistic early termination

Possible features:
- Weighted tags with importance scores
- Tag relationships and hierarchies
- Atomic multi-operation transactions
- Database persistence layer

## Performance Characteristics

Approximate performance for a typical dataset:
- 10,000 entries
- 100 unique tags
- 5-10 tags per entry

| Operation | Time |
|-----------|------|
| Single tag add | < 1 µs |
| Query (2 tags) | < 100 µs |
| Query (5 tags) | < 200 µs |
| Add 1000 entries | < 10 ms |

Actual results depend on hardware, tag distribution, and entry characteristics. Run benchmarks on your system for accurate numbers.

## Thread Safety

**Current**: TagMap is not thread-safe. For multi-threaded use, apply external synchronization:

```python
import threading

lock = threading.Lock()
m = tagmap.TagMap()

with lock:
    m.add_tag("alice", "dev")
```

Alternatively, create separate instances per thread.
