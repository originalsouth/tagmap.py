# TagMap

Fast dictionary-like data structure for managing tags and metadata. Built with C++ and pybind11.

## What is This?

TagMap is a specialized data structure optimized for managing multiple tags per key with efficient query support. Think of it as a dict where each key has a set of tags, and you can query for all keys matching specific tag combinations.

## Features

- Fast tag queries: intersection (all-of) and union (any-of) operations
- O(1) add/remove/check, O(n) queries
- Efficient tag storage with optimized inverted index
- Built on high-performance C++
- Python bindings with pybind11
- Handles metadata management, feature flags, classification systems

## Install

```bash
pip install tagmap
```

Or with uv:
```bash
uv pip install tagmap
```

## Usage

```python
import tagmap

m = tagmap.TagMap()

# Add keys with tags
m["alice"] = {"dev", "python"}
m["bob"] = {"dev", "cpp"}
m["carol"] = ["design", "python"]

# Query: keys with both "dev" AND "python"
m.query("dev", "python")          # ['alice']

# Query: keys with "python" OR "ops"
m.query_any("python", "ops")      # ['alice', 'carol']

# Check if key has tag
m.has_tag("alice", "python")      # True

# Modify tags
m.add_tag("alice", "ml")
m.remove_tag("bob", "dev")
```

## Docs

- [Installation](docs/INSTALLATION.md) - Setup for all platforms
- [API Reference](docs/API.md) - Method signatures and behavior
- [Examples](docs/EXAMPLES.md) - Real usage patterns
- [Architecture](docs/ARCHITECTURE.md) - Design and performance details
- [Contributing](CONTRIBUTING.md) - How to contribute

## Examples

### Skills Tracking

```python
team = tagmap.TagMap({
    "alice": ["python", "typescript", "backend"],
    "bob": ["cpp", "rust", "backend"],
    "carol": ["ux", "ui", "design"],
})

team.query("python")              # ['alice']
team.query("backend")             # ['alice', 'bob']
team.query("python", "backend")   # ['alice']
```

## Performance

Query: O(n) where n = result count. Tag ops: O(1) average. Uses optimized inverted index. Handles thousands of entries with hundreds of tags. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

## Building

```bash
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py

python -m venv venv
source venv/bin/activate

pip install pybind11 pytest
pip install -e .
# or: make

pytest test_tagmap.py -v
```

Requires: Python 3.8+, C++20 compiler, pybind11

Both build methods use: `-Ofast -march=native -flto=auto`

See [INSTALLATION.md](docs/INSTALLATION.md) for platform details.

## License

MIT. See [LICENSE](LICENSE).

## Author

originalsouth

## Changelog

See [GitHub Releases](https://github.com/originalsouth/tagmap.py/releases).

## Links

- Docs: [docs/](docs/)
- Issues: https://github.com/originalsouth/tagmap.py/issues
- Discussions: https://github.com/originalsouth/tagmap.py/discussions
