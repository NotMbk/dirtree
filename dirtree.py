#!/usr/bin/env python3
"""
Directory Tree Generator
Traverses a directory and displays its structure in a tree format with advanced features.
Supports ignore patterns, configuration files, and various output options.

Usage: python dirtree.py [directory_path] [options]
If no path is provided, uses current directory.
"""

import os
import sys
import json
import fnmatch
from pathlib import Path
from typing import List, Set, Optional

# Default ignore patterns - common directories/files to ignore
DEFAULT_IGNORE_PATTERNS = {
    # Dependencies
    'node_modules',
    '__pycache__',
    '.venv',
    'venv',
    'env',
    'vendor',
    'bower_components',
    
    # Build outputs
    'dist',
    'build',
    'out',
    '.next',
    '.nuxt',
    'target',
    'bin',
    'obj',
    
    # Version control
    '.git',
    '.svn',
    '.hg',
    
    # IDE/Editor files
    '.vscode',
    '.idea',
    '*.swp',
    '*.swo',
    '*~',
    
    # OS files
    '.DS_Store',
    'Thumbs.db',
    'desktop.ini',
    
    # Temporary files
    '*.tmp',
    '*.temp',
    '.cache',
    'tmp',
    'temp',
    
    # Logs
    '*.log',
    'logs',
    
    # Coverage/Test outputs
    'coverage',
    '.coverage',
    '.nyc_output',
    'htmlcov',
    '.pytest_cache',
    '.tox',
}

class DirectoryTreeGenerator:
    """Main class for generating directory trees with advanced features."""
    
    def __init__(self, ignore_patterns: Optional[Set[str]] = None, 
                 show_hidden: bool = False, max_depth: Optional[int] = None,
                 use_default_ignores: bool = True):
        self.ignore_patterns = ignore_patterns or set()
        if use_default_ignores:
            self.ignore_patterns.update(DEFAULT_IGNORE_PATTERNS)
        self.show_hidden = show_hidden
        self.max_depth = max_depth
        
    def load_ignore_file(self, ignore_file_path: str) -> None:
        """Load ignore patterns from a file (similar to .gitignore format)."""
        try:
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        self.ignore_patterns.add(line)
        except FileNotFoundError:
            pass  # Ignore file doesn't exist, which is fine
        except Exception as e:
            print(f"Warning: Could not read ignore file '{ignore_file_path}': {e}")
    
    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored based on patterns."""
        name = path.name
        
        # Check if hidden file/directory should be ignored
        if not self.show_hidden and name.startswith('.'):
            return True
            
        # Check against ignore patterns
        for pattern in self.ignore_patterns:
            # Support glob patterns
            if fnmatch.fnmatch(name, pattern):
                return True
            # Support exact matches
            if name == pattern:
                return True
            # Support path patterns (e.g., "src/__pycache__")
            if fnmatch.fnmatch(str(path), pattern):
                return True
                
        return False
    def generate_tree(self, directory, prefix="", is_last=True, current_depth=0):
        """
        Generate a tree structure for the given directory.
        
        Args:
            directory: Path object or string path to directory
            prefix: Current prefix for tree formatting
            is_last: Boolean indicating if this is the last item in current level
            current_depth: Current depth level
        """
        if self.max_depth is not None and current_depth >= self.max_depth:
            return
        
        directory = Path(directory)
        
        if not directory.exists():
            print(f"Error: Directory '{directory}' does not exist.")
            return
        
        if not directory.is_dir():
            print(f"Error: '{directory}' is not a directory.")
            return
        
        # Print current directory name (except for root call)
        if current_depth > 0:
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{directory.name}/")
            prefix += "    " if is_last else "│   "
        else:
            # Print root directory
            print(f"{directory.name}/")
        
        try:
            # Get all items in directory
            items = list(directory.iterdir())
            
            # Filter out ignored items
            items = [item for item in items if not self.should_ignore(item)]
            
            # Sort: directories first, then files, both alphabetically
            items.sort(key=lambda x: (x.is_file(), x.name.lower()))
            
            for i, item in enumerate(items):
                is_last_item = i == len(items) - 1
                
                if item.is_dir():
                    # Recursively process subdirectories
                    self.generate_tree(item, prefix, is_last_item, current_depth + 1)
                else:
                    # Print files
                    connector = "└── " if is_last_item else "├── "
                    print(f"{prefix}{connector}{item.name}")
                    
        except PermissionError:
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}[Permission Denied]")

def create_default_ignore_file(path: str = ".dirtreeignore") -> None:
    """Create a default ignore file with common patterns."""
    ignore_content = """# Directory Tree Generator Ignore File
# Lines starting with # are comments
# Supports glob patterns like *.log, temp*, etc.

# Dependencies
node_modules
__pycache__
.venv
venv
env
vendor
bower_components

# Build outputs
dist
build
out
.next
.nuxt
target
bin
obj

# Version control
.git
.svn
.hg

# IDE/Editor files
.vscode
.idea
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
*.tmp
*.temp
.cache
tmp
temp

# Logs
*.log
logs

# Coverage/Test outputs
coverage
.coverage
.nyc_output
htmlcov
.pytest_cache
.tox
"""
    
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(ignore_content)
        print(f"Created default ignore file: {path}")
    except Exception as e:
        print(f"Error creating ignore file: {e}")

def save_tree_to_file(directory: str, output_file: str, generator: DirectoryTreeGenerator) -> None:
    """Save the tree output to a file."""
    import io
    import contextlib
    
    # Capture stdout
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        generator.generate_tree(directory)
    
    tree_output = f.getvalue()
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"# Directory Tree\n\n```\n{tree_output}```\n")
        print(f"Tree saved to: {output_file}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def main():
    """Main function to handle command line arguments and run the tree generator."""
    
    # Default values
    target_dir = "."
    max_depth = None
    show_hidden = False
    use_default_ignores = True
    custom_ignore_patterns = set()
    ignore_file = None
    output_file = None
    
    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg in ["-h", "--help"]:
            print_help()
            return
        elif arg == "--create-ignore":
            create_default_ignore_file()
            return
        elif arg.startswith("--depth="):
            try:
                max_depth = int(arg.split("=")[1])
            except ValueError:
                print("Error: Invalid depth value. Use --depth=NUMBER")
                return
        elif arg == "--show-hidden":
            show_hidden = True
        elif arg == "--no-default-ignores":
            use_default_ignores = False
        elif arg.startswith("--ignore="):
            patterns = arg.split("=")[1].split(",")
            custom_ignore_patterns.update(patterns)
        elif arg.startswith("--ignore-file="):
            ignore_file = arg.split("=")[1]
        elif arg.startswith("--output="):
            output_file = arg.split("=")[1]
        elif not arg.startswith("-"):
            target_dir = arg
        else:
            print(f"Unknown option: {arg}")
            print("Use --help for usage information")
            return
        
        i += 1
    
    # Create generator instance
    generator = DirectoryTreeGenerator(
        ignore_patterns=custom_ignore_patterns,
        show_hidden=show_hidden,
        max_depth=max_depth,
        use_default_ignores=use_default_ignores
    )
    
    # Load ignore file if specified or look for default ones
    ignore_files_to_check = []
    if ignore_file:
        ignore_files_to_check.append(ignore_file)
    else:
        # Check for common ignore file names
        ignore_files_to_check.extend([
            ".dirtreeignore",
            ".treeignore", 
            "dirtree.ignore"
        ])
    
    for ignore_path in ignore_files_to_check:
        if Path(ignore_path).exists():
            generator.load_ignore_file(ignore_path)
            break
    
    target_path = Path(target_dir).resolve()
    
    if not output_file:
        print(f"Directory structure for: {target_path}")
        print("-" * 50)
        generator.generate_tree(target_path)
    else:
        save_tree_to_file(target_path, output_file, generator)

def print_help():
    """Print help information."""
    help_text = """
Directory Tree Generator v2.0

A powerful command-line tool to generate directory tree structures with 
advanced filtering and customization options.

USAGE:
    python dirtree.py [DIRECTORY] [OPTIONS]

ARGUMENTS:
    DIRECTORY            Target directory path (default: current directory)

OPTIONS:
    -h, --help          Show this help message
    --depth=N           Limit tree depth to N levels
    --show-hidden       Show hidden files and directories (starting with .)
    --no-default-ignores Disable default ignore patterns
    --ignore=PATTERNS   Comma-separated list of patterns to ignore
    --ignore-file=FILE  Use custom ignore file (default: .dirtreeignore)
    --output=FILE       Save output to file instead of displaying
    --create-ignore     Create a default .dirtreeignore file

IGNORE PATTERNS:
    Supports glob patterns like:
    - node_modules      (exact match)
    - *.log            (all .log files)  
    - temp*            (files starting with 'temp')
    - **/__pycache__   (nested patterns)

IGNORE FILES:
    The tool automatically looks for ignore files in this order:
    1. Custom file specified with --ignore-file
    2. .dirtreeignore
    3. .treeignore
    4. dirtree.ignore
    
    Ignore file format (similar to .gitignore):
    - One pattern per line
    - Lines starting with # are comments
    - Empty lines are ignored

EXAMPLES:
    # Basic usage
    python dirtree.py
    python dirtree.py /path/to/project
    
    # With options
    python dirtree.py . --depth=3 --show-hidden
    python dirtree.py /project --ignore=*.pyc,temp*,logs
    python dirtree.py . --ignore-file=my_ignore.txt
    python dirtree.py /project --output=project_structure.md
    
    # Create ignore file template
    python dirtree.py --create-ignore

DEFAULT IGNORED ITEMS:
    Dependencies: node_modules, __pycache__, .venv, venv, vendor, etc.
    Build outputs: dist, build, out, .next, target, bin, obj, etc.
    Version control: .git, .svn, .hg
    IDE files: .vscode, .idea, *.swp, etc.
    OS files: .DS_Store, Thumbs.db, desktop.ini
    Temporary: *.tmp, .cache, tmp, temp, logs, etc.
    
    Use --no-default-ignores to disable these defaults.

GITHUB: https://github.com/yourusername/directory-tree-generator
"""
    print(help_text)

if __name__ == "__main__":
    main()