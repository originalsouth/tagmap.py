# TagMap Documentation Index

This file provides an overview of all documentation available for the TagMap project.

## 📚 Core Documentation

### [README.md](README.md)
**Start here!** Overview of the project, quick start guide, basic usage examples, and common use cases.

### [docs/INSTALLATION.md](docs/INSTALLATION.md)
Comprehensive installation guide covering:
- Quick install via pip
- Platform-specific instructions (macOS, Linux, Windows)
- Development setup
- Python version support
- Troubleshooting common issues

### [docs/API.md](docs/API.md)
Complete API reference with:
- Constructor options
- Item access methods
- Tag operations (add, remove, check)
- Query operations (AND/OR)
- Count operations
- Dictionary-like methods
- Erase and retain operations
- Type hints and return types

### [docs/EXAMPLES.md](docs/EXAMPLES.md)
Real-world usage examples:
- Team member skills management
- Content tagging system
- Feature flags and deployment tracking
- Document classification
- Conditional filtering
- Dynamic tag updates
- Bulk operations
- Reporting and analytics
- Performance tips

### [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
Technical deep dive into:
- Data structures and algorithms
- Time complexity analysis
- Query algorithms (AND/OR)
- Memory management
- Python bindings (pybind11)
- Optimization techniques
- Design decisions
- Performance characteristics
- Thread safety
- Debugging and profiling

### [CONTRIBUTING.md](CONTRIBUTING.md)
Guide for contributing to the project:
- Development setup
- Workflow and code style
- Testing guidelines
- Documentation standards
- Common tasks (adding methods, fixing bugs)
- Pull request process
- Reporting issues

## 🎯 Use Cases

Choose documentation based on your needs:

| I want to... | Read |
|---|---|
| Install TagMap | [INSTALLATION.md](docs/INSTALLATION.md) |
| Learn how to use it | [README.md](README.md) → [EXAMPLES.md](docs/EXAMPLES.md) |
| Look up a method | [API.md](docs/API.md) |
| Understand internals | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Fix a bug or add a feature | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 📖 Documentation Structure

```
tagmap.py/
├── README.md                 # Project overview & quick start
├── DOCUMENTATION.md          # This file - documentation index
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
├── docs/
│   ├── INSTALLATION.md      # Setup instructions
│   ├── API.md               # Complete API reference
│   ├── EXAMPLES.md          # Usage examples & patterns
│   └── ARCHITECTURE.md      # Technical internals
└── [source files...]
```

## 🚀 Quick Links

- **Installation**: `pip install tagmap`
- **GitHub**: https://github.com/originalsouth/tagmap.py
- **Issue Tracker**: https://github.com/originalsouth/tagmap.py/issues
- **Release Notes**: https://github.com/originalsouth/tagmap.py/releases

## 📝 Common Tasks

### Getting Started (5 minutes)
1. Read [README.md](README.md) - Overview and quick start
2. Install: `pip install tagmap`
3. Run examples from [EXAMPLES.md](docs/EXAMPLES.md)

### For Developers (setup)
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup
2. Follow installation steps for [development](docs/INSTALLATION.md#development-installation)
3. Run tests: `pytest test_tagmap.py -v`

### API Lookup
- Go to [API.md](docs/API.md)
- Use browser search or editor Ctrl+F to find your method
- See examples right there or cross-reference [EXAMPLES.md](docs/EXAMPLES.md)

### Understanding Performance
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Performance section
- Run benchmarks: `python tagmap_bench.py`
- Review time complexity table

### Contributing Changes
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Follow development workflow
3. Add tests and documentation
4. Submit pull request

## 📚 Document Relationships

```
README.md (START HERE)
├── EXAMPLES.md (See it in action)
├── INSTALLATION.md (Set it up)
├── API.md (Learn all methods)
│   └── ARCHITECTURE.md (How it works inside)
└── CONTRIBUTING.md (Make it better)
```

## 🔍 Finding What You Need

**How do I...?**
- ...get started? → [README.md](README.md)
- ...install it? → [INSTALLATION.md](docs/INSTALLATION.md)
- ...use feature X? → [EXAMPLES.md](docs/EXAMPLES.md)
- ...call method Y? → [API.md](docs/API.md)
- ...optimize it? → [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- ...contribute? → [CONTRIBUTING.md](CONTRIBUTING.md)

**Troubleshooting:**
- Installation issues? → [INSTALLATION.md#troubleshooting](docs/INSTALLATION.md#troubleshooting)
- API questions? → [API.md](docs/API.md)
- Performance concerns? → [ARCHITECTURE.md#performance-characteristics](docs/ARCHITECTURE.md#performance-characteristics)
- Found a bug? → [CONTRIBUTING.md#reporting-issues](CONTRIBUTING.md#reporting-issues)

## 📋 Documentation Checklist

- ✅ Quick start guide in README
- ✅ Installation instructions for all platforms
- ✅ Complete API reference
- ✅ Real-world usage examples
- ✅ Architecture and design documentation
- ✅ Contribution guidelines
- ✅ Performance characteristics
- ✅ Troubleshooting guides

## 🔄 Keeping Documentation Updated

Documentation is kept up-to-date in:
- `README.md` - Core features, quick start
- `docs/API.md` - Method signatures and descriptions
- `docs/EXAMPLES.md` - Usage patterns
- `docs/ARCHITECTURE.md` - Technical details
- `docs/INSTALLATION.md` - Setup procedures
- `CONTRIBUTING.md` - Development info

When contributing:
- Update relevant docs when changing features
- Add examples for new methods
- Keep API docs in sync with code
- Update troubleshooting if you solve an issue

## ✨ Documentation Quality

All documentation includes:
- Clear, concise explanations
- Practical code examples
- Links between related docs
- Troubleshooting sections
- Index/search-friendly format

---

**Last Updated**: 2026-01-25

For the latest documentation, visit:
https://github.com/originalsouth/tagmap.py
