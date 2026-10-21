"""
paths_init.py - Initialize paths for Windshield Dehazing models
Add to beginning of each test script imports to fix path issues
"""

import os
import sys
from pathlib import Path

def init_paths():
    """Initialize Python paths for model imports"""
    
    # Find project root (where run_model.py is)
    current = Path(__file__).parent
    while current != current.parent:
        if (current / "run_model.py").exists():
            project_root = current
            break
        current = current.parent
    else:
        # Fallback
        project_root = Path.cwd()
    
    # Find src directory
    src_dir = None
    for candidate in project_root.rglob('src'):
        if (candidate / 'ka_net').exists() or (candidate / 'nighttime').exists():
            src_dir = candidate
            break
    
    if not src_dir:
        print(f"Warning: Could not find src directory")
        return project_root
    
    # Add all relevant paths
    paths_to_add = [
        str(project_root),
        str(src_dir),
        str(src_dir / 'ka_net' / 'testcode'),
        str(src_dir / 'nighttime'),
        str(src_dir / 'orama'),
        str(src_dir / 'daclip'),
    ]
    
    for p in paths_to_add:
        if p not in sys.path:
            sys.path.insert(0, p)
    
    # Set working directory to project root
    os.chdir(project_root)
    
    return project_root

# Initialize on import
_project_root = init_paths()
