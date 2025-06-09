# dirtree

Python script to generate directory tree structures. Does what `tree` command does but with better ignore patterns and cross-platform support.

## Installation

```bash
git clone https://github.com/yourusername/dirtree.git
cd dirtree
```

No dependencies. Just Python 3.6+.

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

## What it ignores by default

Stuff you probably don't want to see:
- `node_modules`, `__pycache__`, `.venv`, `venv`
- `dist`, `build`, `out`, `.next`, `target`
- `.git`, `.svn`, `.idea`, `.vscode`
- `*.log`, `*.tmp`, `.DS_Store`, `Thumbs.db`

Full list is in the code.

## Options

```
python dirtree.py [directory] [options]

--depth=N              Only go N levels deep
--show-hidden          Show hidden files (starting with .)
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

## Why not just use `tree`?

- `tree` isn't available on Windows by default
- This has better ignore patterns for modern dev projects
- Cross-platform
- Can output to files

That's it. It works.

## License

MIT