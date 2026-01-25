# TagMap API Reference

## Constructor

### `TagMap()`
Create an empty TagMap instance.

```python
m = tagmap.TagMap()
```

### `TagMap(dict)`
Create a TagMap from a dictionary.

```python
m = tagmap.TagMap({
    "alice": {"dev", "python"},
    "bob": ["cpp", "dev"]
})
```

### `TagMap(list)`
Create a TagMap from a list of key-value pairs.

```python
m = tagmap.TagMap([
    ("alice", {"dev", "python"}),
    ("bob", ["cpp", "dev"])
])
```

### `TagMap(keys, values)`
Create a TagMap from separate lists of keys and values.

```python
m = tagmap.TagMap(
    ["alice", "bob"],
    [["dev", "python"], ["cpp", "dev"]]
)
```

---

## Item Access

### `m[key]`
Get or set tags for a key.

```python
# Get tags
tags = m["alice"]  # Returns a set-like object

# Set tags
m["alice"] = {"dev", "python"}
m["alice"] = ["dev", "python"]  # Also accepts lists
```

### `key in m`
Check if a key exists.

```python
if "alice" in m:
    print("alice is in the map")
```

---

## Tag Operations

### `add_tag(key, tag)`
Add a single tag to an entry.

```python
m.add_tag("alice", "ml")
```

### `add_tags(key, tags)`
Add multiple tags to an entry.

```python
m.add_tags("alice", ["ml", "pytorch"])
```

### `remove_tag(key, tag)`
Remove a tag from an entry. Raises `KeyError` if the tag doesn't exist.

```python
m.remove_tag("alice", "dev")
```

### `discard_tag(key, tag)`
Remove a tag from an entry. Does not raise an error if the tag doesn't exist.

```python
m.discard_tag("alice", "nonexistent")  # No error
```

### `has_tag(key, tag)`
Check if an entry has a specific tag.

```python
if m.has_tag("alice", "python"):
    print("alice has python tag")
```

---

## Query Operations

### `query(*tags)`
Query entries with **all** of the specified tags (AND operation).

```python
result = m.query("dev", "python")  # All entries with both tags
result = m.query("dev")  # All entries with 'dev' tag
result = m.query()  # All entries
```

### `find(tags)`
Query entries with all of the specified tags using a list/iterable.

```python
result = m.find(["dev", "python"])
```

### `query_any(*tags)`
Query entries with **any** of the specified tags (OR operation).

```python
result = m.query_any("dev", "ops")  # All entries with either tag
```

### `find_any(tags)`
Query entries with any of the specified tags using a list/iterable.

```python
result = m.find_any(["dev", "ops"])
```

---

## Count Operations

### `count(tags)`
Count entries with **all** of the specified tags.

```python
count = m.count(["dev", "python"])
count = m.count(["dev"])
```

### `count_any(tags)`
Count entries with **any** of the specified tags.

```python
count = m.count_any(["dev", "ops"])
```

---

## Dictionary-like Operations

### `len(m)`
Get the number of entries in the TagMap.

```python
size = len(m)
```

### `get(key, default=None)`
Get tags for a key with a default value if not found.

```python
tags = m.get("alice")  # Returns None if not found
tags = m.get("alice", {"unknown"})  # Returns default if not found
```

### `setdefault(key, default)`
Get tags for a key, or set and return a default value if not found.

```python
tags = m.setdefault("alice", {"dev"})
```

### `pop(key, default=None)`
Remove and return tags for a key. Returns default if not found.

```python
tags = m.pop("alice")  # Removes alice and returns its tags
tags = m.pop("alice", {"unknown"})  # Returns default if not found
```

### `popitem()`
Remove and return an arbitrary key-value pair.

```python
key, tags = m.popitem()
```

### `update(other)`
Update TagMap with entries from a dictionary or another TagMap.

```python
m.update({"bob": {"cpp"}})
m.update([("carol", ["design"])])
```

### `keys()` / `iter(m)`
Iterate over all keys.

```python
for key in m:
    print(key)

keys = list(m.keys())
```

### `values()` / `items()`
Iterate over values and key-value pairs.

```python
for tags in m.values():
    print(tags)

for key, tags in m.items():
    print(key, tags)
```

---

## Erase/Retain Operations

### `erase(key)`
Remove an entry by key. Raises `KeyError` if not found.

```python
m.erase("alice")
```

### `discard(key)`
Remove an entry by key. Does not raise an error if not found.

```python
m.discard("nonexistent")  # No error
```

### `erase_where(tags)`
Remove all entries with **all** of the specified tags. Returns list of removed keys.

```python
removed = m.erase_where(["dev"])  # Remove all entries with 'dev' tag
```

### `erase_where_any(tags)`
Remove all entries with **any** of the specified tags. Returns list of removed keys.

```python
removed = m.erase_where_any(["dev", "ops"])
```

### `retain_where(tags)`
Keep only entries with **all** of the specified tags. Returns list of kept keys.

```python
kept = m.retain_where(["dev"])  # Keep only entries with 'dev' tag
```

### `retain_where_any(tags)`
Keep only entries with **any** of the specified tags. Returns list of kept keys.

```python
kept = m.retain_where_any(["dev", "ops"])
```

### `clear()`
Remove all entries from the TagMap.

```python
m.clear()
```

---

## Utility Methods

### `tags()`
Get all unique tags used in the TagMap.

```python
all_tags = m.tags()  # Returns list of all unique tags
```

### `to_dict()`
Convert TagMap to a dictionary.

```python
d = m.to_dict()
```

### `from_dict(dict)` (static method)
Create a TagMap from a dictionary.

```python
m = tagmap.TagMap.from_dict({"alice": {"dev", "python"}})
```

### `from_keys_values(keys, values)` (static method)
Create a TagMap from separate key and value lists.

```python
m = tagmap.TagMap.from_keys_values(["a", "b"], [["x", "y"], ["z"]])
```

---

## Type Hints (Python 3.9+)

```python
from typing import List, Set, Dict
import tagmap

def process_entries(m: tagmap.TagMap) -> List[str]:
    """Get all developers."""
    return m.query("dev")

def filter_tags(m: tagmap.TagMap, required: Set[str]) -> Dict[str, Set[str]]:
    """Filter entries and return as dict."""
    return m.to_dict()
```

---

## Return Types

- **Tags**: Set-like objects returned by getters are compatible with set operations
- **Query results**: Lists of matching keys
- **Counts**: Integer values
- **All unique tags**: List of strings
