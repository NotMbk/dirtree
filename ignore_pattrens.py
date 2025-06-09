"""
Default ignore patterns for directory tree generation.
Organized by category for easy maintenance and customization.
"""

# Development Dependencies
DEPENDENCIES = {
    'node_modules',           # Node.js
    '__pycache__',           # Python
    '.venv', 'venv', 'env',  # Python virtual environments
    'vendor',                # PHP Composer, Go modules
    'bower_components',      # Bower (legacy)
    '.yarn',                 # Yarn v2+
    '.pnpm-store',          # PNPM
    'Packages',             # Unity
    'node_modules.nosync',  # Node.js with iCloud
}

# Build Outputs and Compiled Assets
BUILD_OUTPUTS = {
    'dist',                 # General distribution
    'build',               # General build output
    'out',                 # Next.js, general output
    '.next',               # Next.js
    '.nuxt',               # Nuxt.js
    '.docusaurus',         # Docusaurus
    'target',              # Rust, Maven, Scala
    'bin',                 # General binaries
    'obj',                 # .NET, C++
    'Debug', 'Release',    # Visual Studio
    '.output',             # Nitro
}

# Version Control Systems
VERSION_CONTROL = {
    '.git',
    '.svn',
    '.hg',                 # Mercurial
    '.bzr',                # Bazaar
    'CVS',                 # CVS (legacy)
}

# IDE and Editor Files
IDE_EDITOR = {
    '.vscode',             # Visual Studio Code
    '.idea',               # JetBrains IDEs
    '*.swp', '*.swo',      # Vim
    '*~',                  # Emacs, Vim
    '.project',            # Eclipse
    '.classpath',          # Eclipse
    '.settings',           # Eclipse
    '*.iml',               # IntelliJ
    '.vs',                 # Visual Studio
    '*.suo', '*.user',     # Visual Studio
}

# Operating System Files
OS_FILES = {
    '.DS_Store',           # macOS
    '.DS_Store?',          # macOS
    '._*',                 # macOS
    '.Spotlight-V100',     # macOS
    '.Trashes',            # macOS
    'ehthumbs.db',         # Windows
    'Thumbs.db',           # Windows
    'desktop.ini',         # Windows
    '$RECYCLE.BIN',        # Windows
}

# Temporary and Cache Files
TEMP_CACHE = {
    '*.tmp', '*.temp',     # General temporary
    '.cache',              # General cache
    'tmp', 'temp',         # Temp directories
    '.sass-cache',         # Sass
    '.eslintcache',        # ESLint
    '.parcel-cache',       # Parcel
    '.webpack',            # Webpack
    '.turbo',              # Turborepo
}

# Log Files
LOGS = {
    '*.log',
    'logs',
    'npm-debug.log*',
    'yarn-debug.log*',
    'yarn-error.log*',
    'lerna-debug.log*',
    '.pnpm-debug.log*',
}

# Testing and Coverage
TESTING_COVERAGE = {
    'coverage',
    '.coverage',
    '.coverage.*',
    '.nyc_output',
    'htmlcov',
    '.pytest_cache',
    '.tox',
    'junit.xml',
    '.karma',
    '__snapshots__',
}

# Database Files
DATABASES = {
    '*.sqlite',
    '*.sqlite3',
    '*.db',
    '*.sqlite-journal',
}

# Compiled Files and Archives
COMPILED = {
    '*.pyc', '*.pyo',      # Python
    '*.class',             # Java
    '*.o', '*.obj',        # C/C++
    '*.so', '*.dll',       # Libraries
    '*.jar', '*.war', '*.ear',  # Java archives
    '*.exe',               # Executables
}

# Environment and Configuration
ENVIRONMENT = {
    '.env',
    '.env.local',
    '.env.development.local',
    '.env.test.local',
    '.env.production.local',
    '.env.*.local',
    'config.json',         # Sometimes contains secrets
    'secrets.json',
    '.secrets',
}

# Documentation Build Outputs
DOCS = {
    'docs/_build',
    'site',                # MkDocs
    '_site',               # Jekyll
    '.docz',              # Docz
}

# Package Manager Lock Files (optional - some people want to see these)
LOCK_FILES = {
    # Uncomment if you want to hide lock files
    # 'package-lock.json',
    # 'yarn.lock',
    # 'pnpm-lock.yaml',
    # 'Pipfile.lock',
    # 'poetry.lock',
    # 'Gemfile.lock',
}

# Combine all patterns
DEFAULT_IGNORE_PATTERNS = (
    DEPENDENCIES |
    BUILD_OUTPUTS |
    VERSION_CONTROL |
    IDE_EDITOR |
    OS_FILES |
    TEMP_CACHE |
    LOGS |
    TESTING_COVERAGE |
    DATABASES |
    COMPILED |
    ENVIRONMENT |
    DOCS |
    LOCK_FILES
)

# Alternative pattern sets for different use cases
MINIMAL_PATTERNS = DEPENDENCIES | VERSION_CONTROL | OS_FILES
AGGRESSIVE_PATTERNS = DEFAULT_IGNORE_PATTERNS | {
    '*.min.js',           # Minified files
    '*.min.css',
    '*.map',              # Source maps
    'public/assets',      # Static assets
}

# Language-specific patterns
PYTHON_PATTERNS = {
    '__pycache__', '*.pyc', '*.pyo', '.venv', 'venv', 'env',
    '.pytest_cache', '.tox', '.coverage', 'htmlcov',
    'dist', 'build', '*.egg-info',
}

JAVASCRIPT_PATTERNS = {
    'node_modules', '.next', '.nuxt', 'dist', 'build',
    '.eslintcache', '.parcel-cache', 'coverage',
    '*.log', '.env.local',
}

def get_patterns_by_category(categories=None):
    """Get patterns by specific categories."""
    if not categories:
        return DEFAULT_IGNORE_PATTERNS
    
    result = set()
    category_map = {
        'deps': DEPENDENCIES,
        'build': BUILD_OUTPUTS,
        'vcs': VERSION_CONTROL,
        'ide': IDE_EDITOR,
        'os': OS_FILES,
        'temp': TEMP_CACHE,
        'logs': LOGS,
        'test': TESTING_COVERAGE,
        'db': DATABASES,
        'compiled': COMPILED,
        'env': ENVIRONMENT,
        'docs': DOCS,
    }
    
    for category in categories:
        if category in category_map:
            result.update(category_map[category])
    
    return result

def get_language_patterns(language):
    """Get patterns specific to a programming language/framework."""
    language_map = {
        'python': PYTHON_PATTERNS,
        'javascript': JAVASCRIPT_PATTERNS,
        'js': JAVASCRIPT_PATTERNS,
        'node': JAVASCRIPT_PATTERNS,
    }
    
    return language_map.get(language.lower(), set())