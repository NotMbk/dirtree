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

# Try to import ignore patterns, fallback to basic set if not available
try:
    from ignore_patterns import (
        DEFAULT_IGNORE_PATTERNS,
        MINIMAL_PATTERNS,
        AGGRESSIVE_PATTERNS,
        get_patterns_by_category,
        get_language_patterns
    )
except ImportError:
    # Fallback patterns if ignore_patterns.py is not available
    DEFAULT_IGNORE_PATTERNS = {
        'node_modules', '__pycache__', '.venv', 'venv', '.git',
        'dist', 'build', '.next', '.idea', '.vscode', '*.log'
    }
    MINIMAL_PATTERNS = {'node_modules', '__pycache__', '.git'}
    AGGRESSIVE_PATTERNS = DEFAULT_IGNORE_PATTERNS
    
    def get_patterns_by_category(categories=None):
        return DEFAULT_IGNORE_PATTERNS
    
    def get_language_patterns(language):
        return set()

class DirectoryTreeGenerator:
    """Main class for generating directory trees with advanced features."""
    
    def __init__(self, ignore_patterns: Optional[Set[str]] = None, 
                 show_hidden: bool = False, max_depth: Optional[int] = None,
                 use_default_ignores: bool = True, pattern_mode: str = 'default'):
        """
        Initialize the tree generator.
        
        Args:
            ignore_patterns: Custom patterns to ignore
            show_hidden: Show hidden files/directories
            max_depth: Maximum depth to traverse
            use_default_ignores: Whether to use default ignore patterns
            pattern_mode: Which default patterns to use ('default', 'minimal', 'aggressive')
        """
        self.ignore_patterns = ignore_patterns or set()
        self.show_hidden = show_hidden
        self.max_depth = max_depth
        
        if use_default_ignores:
            if pattern_mode == 'minimal':
                self.ignore_patterns.update(MINIMAL_PATTERNS)
            elif pattern_mode == 'aggressive':
                self.ignore_patterns.update(AGGRESSIVE_PATTERNS)
            else:  # default
                self.ignore_patterns.update(DEFAULT_IGNORE_PATTERNS)
        
    def add_language_patterns(self, language: str) -> None:
        """Add language-specific ignore patterns."""
        patterns = get_language_patterns(language)
        self.ignore_patterns.update(patterns)
    
    def add_category_patterns(self, categories: List[str]) -> None:
        """Add patterns from specific categories."""
        patterns = get_patterns_by_category(categories)
        self.ignore_patterns.update(patterns)
    
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
    pattern_mode = 'default'
    custom_ignore_patterns = set()
    ignore_file = None
    output_file = None
    language = None
    categories = None
    
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
        elif arg.startswith("--pattern-mode="):
            pattern_mode = arg.split("=")[1]
            if pattern_mode not in ['default', 'minimal', 'aggressive']:
                print("Error: pattern-mode must be 'default', 'minimal', or 'aggressive'")
                return
        elif arg.startswith("--language="):
            language = arg.split("=")[1]
        elif arg.startswith("--categories="):
            categories = arg.split("=")[1].split(",")
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
        use_default_ignores=use_default_ignores,
        pattern_mode=pattern_mode
    )
    
    # Add language-specific patterns if specified
    if language:
        generator.add_language_patterns(language)
    
    # Add category-specific patterns if specified
    if categories:
        generator.add_category_patterns(categories)
    
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
dirtree - Directory Tree Generator v2.0

USAGE:
    python dirtree.py [DIRECTORY] [OPTIONS]

ARGUMENTS:
    DIRECTORY            Target directory path (default: current directory)

OPTIONS:
    -h, --help          Show this help message
    --depth=N           Limit tree depth to N levels
    --show-hidden       Show hidden files and directories
    --no-default-ignores Disable default ignore patterns
    --pattern-mode=MODE Pattern mode: 'default', 'minimal', or 'aggressive'
    --language=LANG     Add language-specific patterns (python, javascript, etc.)
    --categories=LIST   Add specific categories (deps,build,vcs,ide,os,temp,logs)
    --ignore=PATTERNS   Comma-separated list of patterns to ignore
    --ignore-file=FILE  Use custom ignore file
    --output=FILE       Save output to file instead of displaying
    --create-ignore     Create a default .dirtreeignore file

PATTERN MODES:
    default    - Standard ignore patterns (recommended)
    minimal    - Only ignore dependencies, VCS, and OS files
    aggressive - Ignore everything including minified files, assets

EXAMPLES:
    python dirtree.py
    python dirtree.py /path/to/project
    python dirtree.py . --depth=3 --pattern-mode=minimal
    python dirtree.py . --language=python --categories=deps,build
    python dirtree.py . --ignore=*.pyc,temp* --output=structure.md
"""
    print(help_text)

if __name__ == "__main__":
    main()