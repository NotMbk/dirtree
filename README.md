# dirtree

Python script to generate directory tree structures. Does what `tree` command does but with better ignore patterns and cross-platform support.

## Installation

```bash
git clone https://github.com/yourusername/dirtree.git
cd dirtree
```

No dependencies. Just Python 3.6+.

## Files

- `dirtree.py` - Main script
- `ignore_patterns.py` - All the ignore patterns, organized by category
- `.dirtreeignore` - Example ignore file (like .gitignore)

## Usage

```bash
# Basic usage
python dirtree.py

# Specific directory
python dirtree.py /path/to/project

# Common options
python dirtree.py . --depth=3
python dirtree.py . --ignore=logs,temp
python dirtree.py . --output=structure.md
```

## Pattern modes

```bash
# Different levels of filtering
python dirtree.py . --pattern-mode=minimal     # Only essential ignores
python dirtree.py . --pattern-mode=default     # Standard (recommended)
python dirtree.py . --pattern-mode=aggressive  # Hide everything possible
```

## Language-specific patterns

```bash
# Add patterns for specific languages/frameworks
python dirtree.py . --language=python
python dirtree.py . --language=javascript
```

## Category-specific patterns

```bash
# Pick what to ignore by category
python dirtree.py . --categories=deps,build,vcs
python dirtree.py . --categories=ide,temp,logs
```

Available categories: `deps`, `build`, `vcs`, `ide`, `os`, `temp`, `logs`, `test`, `db`, `compiled`, `env`, `docs`

## What it ignores by default

Check `ignore_patterns.py` for the full organized list. Main categories:

- **Dependencies**: `node_modules`, `__pycache__`, `.venv`, `vendor`
- **Build outputs**: `dist`, `build`, `.next`, `target`
- **Version control**: `.git`, `.svn`, `.hg`
- **IDE files**: `.vscode`, `.idea`, `*.swp`
- **OS files**: `.DS_Store`, `Thumbs.db`
- **Temp/logs**: `*.log`, `*.tmp`, `.cache`

## Options

```
python dirtree.py [directory] [options]

--depth=N              Only go N levels deep
--show-hidden          Show hidden files (starting with .)
--pattern-mode=MODE    minimal/default/aggressive
--language=LANG        Add language-specific patterns
--categories=LIST      Add specific categories (comma-separated)
--ignore=a,b,c         Ignore these patterns (comma-separated)
--ignore-file=file     Use custom ignore file
--output=file          Save to file instead of printing
--no-default-ignores   Don't ignore the default stuff
--create-ignore        Create a .dirtreeignore template
```

## Ignore files

Create `.dirtreeignore` in your project root:

```
# One pattern per line
node_modules
*.log
temp*
my-secret-stuff
```

Supports glob patterns like `*.txt`, `build-*`, etc.

## Example output

```
my-project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── requirements.txt
└── README.md
```

## Customizing ignore patterns

Edit `ignore_patterns.py` to add/remove patterns by category. The modular structure makes it easy to maintain and customize for your needs.

## Why not just use `tree`?

- `tree` isn't available on Windows by default
- This has better ignore patterns for modern dev projects
- Modular and customizable
- Cross-platform
- Can output to files

That's it. It works.

## License

MIT