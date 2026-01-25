# Installation Guide

This guide covers different methods to install TagMap on various platforms.

---

## Quick Install (Recommended)

### Using pip

The easiest way to install TagMap is using pip:

```bash
pip install tagmap
```

Or with uv:
```bash
uv pip install tagmap
```

This installs pre-built wheels for supported platforms (Linux, macOS, Windows).

---

## Platform-Specific Instructions

### macOS

#### Prerequisites
- Python 3.8 or later
- Xcode Command Line Tools (for building from source)

#### Install Xcode Tools (if needed)
```bash
xcode-select --install
```

#### Install TagMap
```bash
pip install tagmap
```

#### From Source
```bash
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py
pip install -e .
```

---

### Linux (Ubuntu/Debian)

#### Prerequisites
```bash
sudo apt-get install python3-dev python3-pip build-essential
```

#### Install TagMap
```bash
pip install tagmap
```

#### From Source
```bash
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py
pip install -e .
```

#### Other Distributions
For other Linux distributions, ensure you have:
- Python 3.8+ development headers
- C++20 compatible compiler (GCC 10+, Clang 11+)
- pip or package manager

---

### Windows

#### Prerequisites
- Python 3.8 or later ([download](https://www.python.org/downloads/))
- Microsoft Visual Studio Build Tools or Visual Studio with C++ support
  - [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
  - Ensure "Desktop development with C++" workload is selected

#### Install TagMap
```bash
pip install tagmap
```

#### From Source (PowerShell)
```powershell
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py
pip install -e .
```

---

## Development Installation

For contributing or local development:

### 1. Clone the Repository
```bash
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Or using uv (faster)
uv venv
```

### 3. Install with Development Dependencies
```bash
pip install -e .
pip install pytest pybind11
```

### 4. Build Locally
```bash
make clean
make
```

Or with pip:
```bash
pip install -e . --force-reinstall --no-cache-dir
```

### 5. Verify Installation
```bash
python -c "import tagmap; print(tagmap.TagMap())"
```

---

## Python Version Support

TagMap supports Python 3.8 and later:

| Version | Status | Notes |
|---------|--------|-------|
| 3.8     | ✅ Supported | Older but stable |
| 3.9     | ✅ Supported | Recommended |
| 3.10    | ✅ Supported | |
| 3.11    | ✅ Supported | |
| 3.12    | ✅ Supported | |
| 3.13    | ✅ Supported | Latest |
| 3.14    | ✅ Supported | |

### Check Your Python Version
```bash
python --version
```

### Using Specific Python Version
```bash
# Install with specific version
python3.11 -m pip install tagmap

# Or specify in virtual environment
python3.11 -m venv venv
```

---

## Troubleshooting

### "No module named 'tagmap'"

**Problem**: Python can't find the TagMap module

**Solutions**:
```bash
# Make sure pip installed it correctly
pip list | grep tagmap

# Try reinstalling
pip install --force-reinstall tagmap

# Check Python path
python -c "import sys; print(sys.path)"
```

### "ImportError: cannot import name 'TagMap'"

**Problem**: The C++ extension failed to build or load

**Solutions**:
```bash
# Check if .so (Linux/macOS) or .pyd (Windows) file exists
python -c "import tagmap; print(tagmap.__file__)"

# Try rebuilding from source
pip install --force-reinstall --no-cache-dir tagmap

# Check compiler warnings
pip install --verbose tagmap 2>&1 | head -50
```

### Build Fails on macOS

**Problem**: Compilation errors with clang

**Solutions**:
```bash
# Update Xcode Command Line Tools
xcode-select --install

# Or specify a compiler
CC=clang CXX=clang++ pip install -e .
```

### Build Fails on Linux

**Problem**: Missing development headers

**Solutions**:
```bash
# Install Python development headers
sudo apt-get install python3-dev  # Debian/Ubuntu
sudo yum install python3-devel    # RHEL/CentOS

# Try with pip verbose mode
pip install -v tagmap
```

### Build Fails on Windows

**Problem**: Visual Studio build tools not found or C++ compilation errors

**Solutions**:
1. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Select "Desktop development with C++"
3. Restart command prompt
4. Retry: `pip install tagmap`

**For C++ Standard Library Errors**:

If you see errors like `error C2039: 'optional': is not a member of 'std'`:
- The setup.py now automatically uses `/std:c++latest` on MSVC
- Ensure you have the latest Visual Studio updates
- If still failing, try upgrading setuptools: `pip install --upgrade setuptools`

**Using MinGW** (alternative):
```bash
# Requires MinGW-w64 installation
pip install tagmap
```

### "pybind11 not found"

**Problem**: pybind11 is not installed

**Solutions**:
```bash
# Install pybind11
pip install pybind11

# Then build TagMap
pip install -e .
```

### Test Failures

**Problem**: Tests fail after installation

**Solutions**:
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest test_tagmap.py -v

# Detailed output
pytest test_tagmap.py -vv -s
```

---

## Upgrading TagMap

### Upgrade via pip
```bash
pip install --upgrade tagmap
```

### Check Current Version
```bash
pip show tagmap

# Or in Python
import tagmap
print(tagmap.__version__)  # if available
```

---

## Uninstalling TagMap

```bash
pip uninstall tagmap
```

---

## Virtual Environment Setup

### Using venv (Built-in)
```bash
# Create
python -m venv tagmap_env

# Activate
source tagmap_env/bin/activate  # macOS/Linux
tagmap_env\Scripts\activate  # Windows (cmd)
source tagmap_env/Scripts/activate  # Windows (PowerShell)

# Install TagMap
pip install tagmap

# Deactivate
deactivate
```

### Using uv (Faster)
```bash
# Create and activate
uv venv tagmap_env
source tagmap_env/bin/activate  # macOS/Linux

# Install TagMap
uv pip install tagmap
```

### Using conda
```bash
# Create environment
conda create -n tagmap python=3.11

# Activate
conda activate tagmap

# Install TagMap
pip install tagmap
```

---

## Docker Setup

For containerized environments:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install TagMap
RUN pip install tagmap

COPY . .

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t tagmap-app .
docker run tagmap-app
```

---

## System Requirements

### Minimum
- Python 3.8
- 50 MB disk space
- 128 MB RAM (recommended)

### Recommended
- Python 3.10+
- Modern processor
- 512 MB RAM for large datasets

### Build Requirements
- C++20 compatible compiler
- 500 MB for build artifacts
- 2GB RAM for compilation

---

## Getting Help

If installation fails:

1. Check the [troubleshooting section](#troubleshooting) above
2. Review [GitHub Issues](https://github.com/originalsouth/tagmap.py/issues)
3. Check platform-specific notes
4. Run with verbose output: `pip install -v tagmap`
5. [Report an issue](https://github.com/originalsouth/tagmap.py/issues/new)

Include in bug reports:
- Output of `pip install -v tagmap`
- Python version: `python --version`
- Operating system and version
- Compiler version: `gcc --version` or `clang --version`
