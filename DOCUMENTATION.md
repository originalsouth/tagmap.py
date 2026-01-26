# TagMap Documentation

Overview of all docs for the TagMap project.

## Core Docs

### [README.md](README.md)
Start here. Project overview, quick start, basic usage, and common cases.

### [docs/INSTALLATION.md](docs/INSTALLATION.md)
How to get it installed:
- pip install tagmap
- Platform-specific notes (macOS, Linux, Windows)
- Development setup
- Python version requirements
- Troubleshooting

### [docs/API.md](docs/API.md)
API reference. Every method, constructor, return types, everything.
- Constructor options
- Item access
- Tag operations (add, remove, check)
- Query operations (AND/OR)
- Count operations
- Dictionary methods
- Erase and retain operations
- Type hints

### [docs/EXAMPLES.md](docs/EXAMPLES.md)
Working examples:
- Team skills management
- Content tagging
- Feature flags and deployments
- Document classification
- Filtering
- Tag updates
- Bulk operations
- Analytics
- Performance tuning

### [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
How it works under the hood:
- Data structures and algorithms
- Time complexity
- Query algorithms
- Memory layout
- Python bindings (pybind11)
- Optimization details
- Design decisions
- Performance metrics
- Thread safety
- Profiling

### [CONTRIBUTING.md](CONTRIBUTING.md)
Contributing guidelines:
- Development setup
- Code style
- Testing
- Docs standards
- Common tasks
- Pull request process
- Bug reporting

## Quick Navigation

| Need | See |
|---|---|
| Install | [INSTALLATION.md](docs/INSTALLATION.md) |
| Learn usage | [README.md](README.md) + [EXAMPLES.md](docs/EXAMPLES.md) |
| API reference | [API.md](docs/API.md) |
| Technical details | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |

## File Structure

```
tagmap.py/
├── README.md                 # Start here
├── DOCUMENTATION.md          # This file
├── CONTRIBUTING.md           # How to contribute
├── LICENSE                   # MIT
├── docs/
│   ├── INSTALLATION.md      # Install instructions
│   ├── API.md               # API reference
│   ├── EXAMPLES.md          # Usage examples
│   └── ARCHITECTURE.md      # Technical details
└── [source]
```

## Links

- Install: `pip install tagmap`
- GitHub: https://github.com/originalsouth/tagmap.py
- Issues: https://github.com/originalsouth/tagmap.py/issues
- Releases: https://github.com/originalsouth/tagmap.py/releases

## Getting Started

1. Read [README.md](README.md)
2. `pip install tagmap`
3. Check [EXAMPLES.md](docs/EXAMPLES.md) for code samples

## Development Setup

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Follow [INSTALLATION.md#development-installation](docs/INSTALLATION.md#development-installation)
3. Run: `pytest test_tagmap.py -v`

## Finding Things

- How do I install? → [INSTALLATION.md](docs/INSTALLATION.md)
- How do I use it? → [README.md](README.md)
- What methods exist? → [API.md](docs/API.md)
- Got an example? → [EXAMPLES.md](docs/EXAMPLES.md)
- Performance questions? → [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Want to contribute? → [CONTRIBUTING.md](CONTRIBUTING.md)
- Build problems? → [INSTALLATION.md#troubleshooting](docs/INSTALLATION.md#troubleshooting)

## Documentation Coverage

- Quick start in README
- Installation for all platforms
- Full API reference
- Working examples
- Architecture docs
- Contribution guidelines
- Performance specs
- Troubleshooting

## Keeping Docs Current

When making changes:
- Update README.md for features
- Update docs/API.md for method changes
- Add examples to docs/EXAMPLES.md
- Update docs/ARCHITECTURE.md for internals
- Update docs/INSTALLATION.md for setup changes
- Keep CONTRIBUTING.md current

---

Last Updated: 2026-01-26

Latest docs: https://github.com/originalsouth/tagmap.py
