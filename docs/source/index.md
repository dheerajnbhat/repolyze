# repolyze

repolyze is a lightweight tool for analyzing source code repositories and
extracting useful statistics about their structure, contents, and overall
health. It can be used both as a Python library and as a command-line tool.

The goal of repolyze is to provide fast, filesystem-based insights without
parsing source code or relying on language-specific tooling.

## Features

- Repository structure analysis (file and directory counts, depth)
- File size statistics and distributions
- File type and language inference based on extensions
- Time-based insights such as recent modifications and file age
- Repository hygiene indicators (empty files, large files, temp files)
- Detection of common project metadata files
- Human-readable directory tree summary

## Installation

```bash
pip install repolyze
````

## Quick Usage

### Python

```python
import repolyze

stats = repolyze.analyze(".")
print(stats.structure.total_files)
```

### Command Line

```bash
repolyze .
```

## Documentation

This documentation covers both stable and development versions of repolyze.
The stable version reflects the latest released package, while the development
version tracks the current state of the main branch.

For usage guides, CLI reference, and API details, use the navigation menu.

## License

repolyze is released under the Apache 2.0 License.
