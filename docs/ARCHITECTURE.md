# TagMap Architecture

This document describes the internal architecture of TagMap, including data structures, algorithms, and design decisions.

---

## Overview

TagMap is a hybrid Python/C++ library that provides a high-performance data structure for managing tagged data. The architecture follows these key principles:

- **Performance**: Critical operations implemented in C++
- **Usability**: Pythonic API with familiar dictionary-like interface
- **Flexibility**: Efficient support for both AND and OR query operations
- **Simplicity**: Clean separation between Python bindings and C++ implementation

---

## Project Structure

```
tagmap.py/
├── tagmap_pybind.cc          # C++ implementation + pybind11 bindings
├── setup.py                  # Build configuration
├── pyproject.toml            # Project metadata
├── tagmap.py                 # Demo/example usage
├── test_tagmap.py            # Test suite
├── tagmap_bench.py           # Performance benchmarks
├── docs/
│   ├── API.md               # API reference
│   ├── EXAMPLES.md          # Usage examples
│   └── ARCHITECTURE.md      # This file
├── CONTRIBUTING.md          # Contribution guidelines
├── README.md                # Project overview
└── Makefile                 # Build commands
```

---

## C++ Implementation Details

### Core Data Structures

The TagMap uses three main data structures in C++:

#### 1. Main Index: `std::unordered_map<std::string, std::unordered_set<std::string>>`
- Maps keys to sets of tags
- Provides O(1) average lookup by key
- Each entry's tags are stored as a set for O(1) tag membership checks

```cpp
std::unordered_map<std::string, std::unordered_set<std::string>> data;
```

#### 2. Inverted Index: `std::unordered_map<std::string, std::unordered_set<std::string>>`
- Maps each tag to the set of keys that have that tag
- Enables fast query operations (finding all keys with a tag)
- Maintained in parallel with main index

```cpp
std::unordered_map<std::string, std::unordered_set<std::string>> tag_index;
```

#### 3. Tag Set: `std::unordered_set<std::string>`
- Stores all unique tags in the map
- Used for the `tags()` method
- Maintained in parallel

```cpp
std::unordered_set<std::string> all_tags;
```

### Time Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `m[key] = tags` | O(n) | n = number of tags assigned |
| `m[key]` | O(1) | Lookup is O(1) |
| `add_tag(key, tag)` | O(1) | Average case |
| `remove_tag(key, tag)` | O(1) | Average case |
| `has_tag(key, tag)` | O(1) | Set membership test |
| `query(*tags)` | O(k * m) | k = result size, m = avg tags per key |
| `query_any(*tags)` | O(n) | n = sum of keys for all tags |
| `count(tags)` | O(k) | k = intersection size |
| `erase_where(tags)` | O(k * n) | k = keys to remove, n = tags per key |

---

## Query Algorithm

### AND Query (query, find, count)

The AND operation finds keys that have **all** specified tags.

**Algorithm**:
1. For the first tag, get all keys with that tag from inverted index
2. For each subsequent tag, retain only keys that also have that tag
3. Return the intersection

**Example**:
```
Keys with "dev": {alice, bob, carol}
Keys with "python": {alice, dave}
Intersection: {alice}
```

**Implementation**:
```cpp
std::vector<std::string> query(const std::vector<std::string>& tags) {
    std::unordered_set<std::string> result;
    bool first = true;
    
    for (const auto& tag : tags) {
        if (tag_index.find(tag) == tag_index.end()) {
            return {};  // Tag not found, empty result
        }
        
        const auto& keys_with_tag = tag_index.at(tag);
        if (first) {
            result = keys_with_tag;
            first = false;
        } else {
            // Intersect with result
            std::unordered_set<std::string> new_result;
            for (const auto& key : result) {
                if (keys_with_tag.count(key)) {
                    new_result.insert(key);
                }
            }
            result = new_result;
        }
    }
    
    return std::vector<std::string>(result.begin(), result.end());
}
```

### OR Query (query_any, find_any, count_any)

The OR operation finds keys that have **any** of the specified tags.

**Algorithm**:
1. For each tag, get all keys with that tag
2. Union all the key sets
3. Return the union

**Example**:
```
Keys with "dev": {alice, bob, carol}
Keys with "ops": {dave, eve}
Union: {alice, bob, carol, dave, eve}
```

---

## Memory Management

### String Storage
- All strings (keys and tags) are stored as `std::string`
- C++ standard library handles memory automatically
- Python bindings convert to/from Python strings transparently

### Set Allocation
- Sets are allocated with `std::unordered_set`
- Dynamic resizing happens automatically
- Memory is freed when entries are removed

### No External Memory Management
- No raw pointers or manual `new`/`delete`
- pybind11 handles Python object lifecycle
- Reference counting by Python GC and C++ standards library

---

## Python Bindings (pybind11)

The C++ class is exposed to Python using pybind11:

```cpp
PYBIND11_MODULE(tagmap, m) {
    m.doc() = "TagMap: efficient tag management data structure";
    
    py::class_<TagMap>(m, "TagMap")
        .def(py::init<>())
        .def("__getitem__", &TagMap::get)
        .def("__setitem__", &TagMap::set)
        .def("query", &TagMap::query)
        // ... more methods ...
}
```

### Type Conversion
- Python `str` ↔ C++ `std::string`
- Python `list`/`set` ↔ C++ `std::vector`/`std::unordered_set`
- pybind11 handles automatic conversion

---

## Optimization Techniques

### 1. Hash-Based Lookups
- Uses `std::unordered_map` and `std::unordered_set` for O(1) operations
- Provides fast membership checks and lookups

### 2. Inverted Index
- Enables fast queries without scanning all entries
- Trade-off: ~2x memory usage but much faster queries
- Especially beneficial for large datasets or many tags

### 3. Set Operations
- Intersection: Only iterate through one set
- Union: Add all elements from multiple sets
- Efficient small-set operations

### 4. Compilation Flags
```bash
# -Ofast: Aggressive optimizations
# -std=c++20: Modern C++ features for better performance
```

---

## Design Decisions

### Why C++?
- **Performance**: 10-100x faster than pure Python for large datasets
- **Memory efficiency**: Compact representation of sets and maps
- **Scalability**: Efficiently handles thousands of entries with hundreds of tags

### Why Inverted Index?
- **Query speed**: Can find all matching keys without full scan
- **Scalability**: O(k) instead of O(n) for most queries
- **Trade-off**: Uses ~2x memory but queries are much faster

### Why Hash Tables?
- **Average O(1)**: Fast lookups regardless of data size
- **Collision handling**: `std::unordered_set/map` are battle-tested
- **Simple**: No need to maintain order

### Why pybind11?
- **Minimal boilerplate**: Simple and readable bindings
- **Automatic type conversion**: Handles Python ↔ C++ seamlessly
- **Performance**: Zero-copy bindings for many operations
- **Maintenance**: Well-maintained and widely used

---

## Evolution & Future Improvements

### Potential Optimizations
1. **Memory pooling**: Pre-allocate memory for bulk operations
2. **Multi-threading**: Thread-safe version for concurrent access
3. **Serialization**: Binary format for faster save/load
4. **Bloom filters**: Probabilistic early termination for large datasets

### Possible Features
1. **Weighted tags**: Support importance/frequency scores
2. **Tag relationships**: Hierarchies or synonyms
3. **Transactions**: Atomic multi-operation changes
4. **Persistence**: Built-in database integration

---

## Performance Characteristics

### Benchmark Results (approximate)

For a typical dataset with:
- 10,000 entries
- 100 unique tags
- 5-10 tags per entry

| Operation | Time | Throughput |
|-----------|------|-----------|
| Single tag addition | < 1 µs | 1M ops/sec |
| Query with 2 tags | < 100 µs | 10k queries/sec |
| Query with 5 tags | < 200 µs | 5k queries/sec |
| Add 1000 entries | < 10 ms | |

*Note: Actual performance depends on hardware, tag distribution, and entry size*

Run `python tagmap_bench.py` for current benchmark results on your system.

---

## Thread Safety

**Current**: TagMap is NOT thread-safe. For multi-threaded use:
- Use external locks (threading.Lock)
- Create separate instances per thread
- Use thread-safe wrapper if needed

```python
import threading

lock = threading.Lock()
m = tagmap.TagMap()

with lock:
    m.add_tag("alice", "dev")
```

---

## Debugging & Profiling

### Python Profiling
```python
import cProfile
import pstats

cProfile.run('tagmap_bench.py', 'tagmap.prof')
stats = pstats.Stats('tagmap.prof')
stats.sort_stats('cumulative').print_stats(10)
```

### C++ Debugging
```bash
# Compile with debug symbols
CFLAGS=-g python setup.py build_ext --inplace

# Run under gdb (macOS/Linux)
gdb python
(gdb) run test_tagmap.py
```

---

## References

- [pybind11 Documentation](https://pybind11.readthedocs.io/)
- [C++ Standard Library Reference](https://en.cppreference.com/)
- [Inverted Index Wikipedia](https://en.wikipedia.org/wiki/Inverted_index)
