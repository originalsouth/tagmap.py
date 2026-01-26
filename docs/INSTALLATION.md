# Installation Guide

Installation instructions for TagMap on supported platforms.

## Quick Start

Install the latest version from PyPI:

```bash
pip install tagmap
```

Requires Python 3.8 or later. Pre-built wheels are available for Linux, macOS, and Windows.

## Platform-Specific Setup

### macOS

Requirements: Python 3.8+, Xcode Command Line Tools

Install command-line tools if needed:
```bash
xcode-select --install
```

Then install TagMap:
```bash
pip install tagmap
```

### Linux (Ubuntu/Debian)

Install development packages:
```bash
sudo apt-get install python3-dev python3-pip build-essential
pip install tagmap
```

For other distributions, ensure Python 3.8+ development headers and a C++20 compiler are installed.

### Windows

Requirements: Python 3.8+, Visual Studio Build Tools with C++ support

Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) and select "Desktop development with C++" workload.

Then install TagMap:
```bash
pip install tagmap
```

## Building from Source

For development or when pre-built wheels are not available:

```bash
git clone https://github.com/originalsouth/tagmap.py.git
cd tagmap.py

python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

pip install pybind11 pytest
pip install -e .
```

Verify the installation:
```bash
python -c "import tagmap; print(tagmap.TagMap())"
```

### Build Requirements

- C++20 compatible compiler (GCC 10+, Clang 11+, MSVC 16.11+)
- pybind11 2.6.0+
- 500 MB disk space for build artifacts

## Python Version Support

Supported Python versions: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

Check your version:
```bash
python --version
```

Use a specific version:
```bash
python3.11 -m pip install tagmap
```

## Troubleshooting

### Import Error

If `import tagmap` fails:

```bash
# Verify installation
pip list | grep tagmap

# Reinstall
pip install --force-reinstall tagmap

# Check Python path
python -c "import sys; print(sys.path)"
```

### Compilation Error on macOS

If the build fails with clang errors:

```bash
# Update Xcode tools
xcode-select --install

# Or specify compiler
CC=clang CXX=clang++ pip install -e .
```

### Compilation Error on Linux

If build fails with missing headers:

```bash
# Install Python development headers
sudo apt-get install python3-dev      # Debian/Ubuntu
sudo yum install python3-devel        # RHEL/CentOS

# Rebuild with verbose output
pip install -v tagmap
```

### Compilation Error on Windows

If Visual Studio build tools are not found:

1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Select "Desktop development with C++" workload
3. Restart command prompt
4. Retry: `pip install tagmap`

For C++ standard library errors, ensure Visual Studio is up to date: `pip install --upgrade setuptools`

### Test Failures

Run tests with verbose output:

```bash
pip install pytest
pytest test_tagmap.py -v
```

## Upgrading and Uninstalling

Upgrade to the latest version:
```bash
pip install --upgrade tagmap
```

Uninstall:
```bash
pip uninstall tagmap
```

## Virtual Environments

### Using venv

```bash
python -m venv tagmap_env
source tagmap_env/bin/activate     # macOS/Linux
# or: tagmap_env\Scripts\activate  # Windows

pip install tagmap
deactivate
```

### Using conda

```bash
conda create -n tagmap python=3.11
conda activate tagmap
pip install tagmap
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install tagmap

COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t tagmap-app .
docker run tagmap-app
```

## System Requirements

**Minimum**
- Python 3.8
- 50 MB disk space

**Recommended**
- Python 3.10+
- 512 MB RAM for large datasets

**Build Requirements**
- C++20 compatible compiler
- 500 MB for build artifacts
- 2 GB RAM for compilation

## Support

For installation help, review the [Troubleshooting](#troubleshooting) section above.

For other issues:
- Check [GitHub Issues](https://github.com/originalsouth/tagmap.py/issues)
- [Report a new issue](https://github.com/originalsouth/tagmap.py/issues/new)

When reporting issues, include:
- Output of `pip install -v tagmap`
- Python version: `python --version`
- Operating system and version
- Compiler version: `gcc --version` or `clang --version`
