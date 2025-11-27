"""
Project Organization Script
سكريبت تنظيم المشروع
==========================

Organizes project files into proper directory structure using centralized paths.
"""

import os
import shutil
import glob
from pathlib import Path
from typing import List, Dict, Tuple

# Import centralized paths system
try:
    from src.core.paths import (
        get_project_root,
        get_data_dir,
        get_scripts_dir,
        get_examples_dir,
        get_docs_dir,
        get_tests_dir,
        ensure_dir
    )
    USE_PATHS_SYSTEM = True
except ImportError:
    # Fallback if paths system not available
    USE_PATHS_SYSTEM = False
    print("Warning: Paths system not available, using relative paths")


def get_base_path():
    """Get project base path"""
    if USE_PATHS_SYSTEM:
        return get_project_root()
    return Path('.').resolve()


def get_dest_path(dest: str):
    """Get destination path"""
    if USE_PATHS_SYSTEM:
        if dest == 'scripts':
            return get_scripts_dir()
        elif dest == 'examples':
            return get_examples_dir()
        elif dest == 'docs':
            return get_docs_dir()
        elif dest == 'tests':
            return get_tests_dir()
        elif dest == 'data':
            return get_data_dir()
    base = get_base_path()
    return base / dest


# Files that should stay in root
ROOT_FILES = {
    'README.md',
    'requirements.txt',
    '.gitignore',
    'config.py',
    'organize_project.py',
    'reorganize.py',
    'generate_colab_notebook.py',
    'GUIDE_ARABIC.md',  # Keep main guide in root
}

# PowerShell scripts should stay in root
ROOT_SCRIPTS = {
    'merge_colab_results.ps1',
    'run_auto_learning.ps1',
    'setup_github.ps1',
    'verify_knowledge_base.ps1',
}

# Organization rules
ORGANIZATION_RULES = [
    # Test files -> tests/
    {
        'pattern': 'test_*.py',
        'dest': 'tests',
        'description': 'Test Python files'
    },
    
    # Example scripts -> examples/
    {
        'pattern': ['learn_*.py', 'fast_learn_*.py', 'colab_complete_learning.py'],
        'dest': 'examples',
        'description': 'Example and learning scripts'
    },
    
    # Documentation files -> docs/ (except README.md)
    {
        'pattern': ['*_GUIDE.md', '*_PLAN.md', '*_STEPS.md', '*_FIX.md', 
                    'HOW_TO_*.md', 'PATH_*.md', 'TOOLS_*.md', 'COLAB_*.md',
                    'DEPLOYMENT_*.md', 'QUICK_*.md', 'NEXT_*.md', 'MIGRATION_*.md'],
        'dest': 'docs',
        'description': 'Documentation files',
        'exclude': ['README.md']
    },
    
    # Data files -> data/
    {
        'pattern': ['agent_memory.db', '*.db', '1.txt'],
        'dest': 'data',
        'description': 'Data and database files'
    },
]


def should_keep_in_root(filename: str) -> bool:
    """Check if file should stay in root directory"""
    if filename in ROOT_FILES:
        return True
    if filename in ROOT_SCRIPTS:
        return True
    if filename == 'README.md':
        return True
    return False


def organize_files(dry_run: bool = False) -> Dict[str, List[Tuple[str, str]]]:
    """
    Organize project files into proper directories.
    
    Args:
        dry_run: If True, only show what would be moved without actually moving
    
    Returns:
        Dictionary with organization results
    """
    base_path = get_base_path()
    results = {
        'moved': [],
        'skipped': [],
        'errors': []
    }
    
    print("=" * 60)
    print("Project Organization Script")
    print("=" * 60)
    print(f"Working directory: {base_path}")
    print(f"Dry run: {dry_run}")
    print()
    
    # Ensure all directories exist
    directories = ['scripts', 'examples', 'docs', 'tests', 'data']
    for dir_name in directories:
        dest_path = get_dest_path(dir_name)
        if not dry_run:
            ensure_dir(dest_path)
        print(f"✓ Directory ready: {dest_path}")
    
    print()
    
    # Track processed files to avoid duplicates
    processed_files = set()
    
    # Process organization rules
    for rule in ORGANIZATION_RULES:
        patterns = rule['pattern'] if isinstance(rule['pattern'], list) else [rule['pattern']]
        dest = rule['dest']
        description = rule.get('description', dest)
        exclude = rule.get('exclude', [])
        
        print(f"\n📁 Processing {description} -> {dest}/")
        print("-" * 60)
        
        dest_path = get_dest_path(dest)
        
        for pattern in patterns:
            # Find matching files
            matches = list(base_path.glob(pattern))
            
            for src_file in matches:
                filename = src_file.name
                file_key = str(src_file.resolve())
                
                # Skip if already processed
                if file_key in processed_files:
                    continue
                processed_files.add(file_key)
                
                # Skip if should stay in root
                if should_keep_in_root(filename):
                    results['skipped'].append((str(src_file), 'Keep in root'))
                    print(f"  ⊘ Skipped (root file): {filename}")
                    continue
                
                # Skip if in exclude list
                if filename in exclude:
                    results['skipped'].append((str(src_file), 'Excluded'))
                    print(f"  ⊘ Skipped (excluded): {filename}")
                    continue
                
                # Skip if already in destination
                if src_file.parent == dest_path:
                    results['skipped'].append((str(src_file), 'Already in destination'))
                    print(f"  ⊘ Skipped (already there): {filename}")
                    continue
                
                # Skip if file doesn't exist (shouldn't happen, but safety check)
                if not src_file.exists():
                    continue
                
                # Move file
                dest_file = dest_path / filename
                
                try:
                    if not dry_run:
                        # If destination exists, add suffix
                        if dest_file.exists():
                            counter = 1
                            while dest_file.exists():
                                stem = src_file.stem
                                suffix = src_file.suffix
                                new_name = f"{stem}_{counter}{suffix}"
                                dest_file = dest_path / new_name
                                counter += 1
                        
                        shutil.move(str(src_file), str(dest_file))
                        results['moved'].append((str(src_file), str(dest_file)))
                        print(f"  ✓ Moved: {filename} -> {dest_file.name}")
                    else:
                        results['moved'].append((str(src_file), str(dest_file)))
                        print(f"  → Would move: {filename} -> {dest_file.name}")
                        
                except Exception as e:
                    error_msg = f"Error moving {filename}: {e}"
                    results['errors'].append((str(src_file), error_msg))
                    print(f"  ✗ {error_msg}")
    
    # Clean up unwanted files/folders in root
    print("\n📁 Cleaning up unwanted files/folders...")
    print("-" * 60)
    
    unwanted_items = [
        '-p',  # Empty folder
        '__pycache__',  # Python cache
    ]
    
    for item_name in unwanted_items:
        item_path = base_path / item_name
        if item_path.exists():
            try:
                if not dry_run:
                    if item_path.is_dir():
                        shutil.rmtree(str(item_path))
                        print(f"  ✓ Removed directory: {item_name}")
                    else:
                        item_path.unlink()
                        print(f"  ✓ Removed file: {item_name}")
                else:
                    print(f"  → Would remove: {item_name}")
            except Exception as e:
                print(f"  ✗ Error removing {item_name}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Organization Summary")
    print("=" * 60)
    print(f"✓ Moved: {len(results['moved'])} files")
    print(f"⊘ Skipped: {len(results['skipped'])} files")
    print(f"✗ Errors: {len(results['errors'])} files")
    
    if results['errors']:
        print("\nErrors:")
        for src, error in results['errors']:
            print(f"  - {Path(src).name}: {error}")
    
    if not dry_run:
        print("\n✅ Project organization complete!")
    else:
        print("\n💡 This was a dry run. Run without --dry-run to actually move files.")
    
    return results


def main():
    """Main function"""
    import sys
    
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN MODE - No files will be moved\n")
    
    results = organize_files(dry_run=dry_run)
    
    # Show what would be moved
    if results['moved']:
        print("\n📋 Files that would be/were moved:")
        for src, dest in results['moved'][:10]:  # Show first 10
            print(f"  {Path(src).name} -> {Path(dest).parent.name}/{Path(dest).name}")
        if len(results['moved']) > 10:
            print(f"  ... and {len(results['moved']) - 10} more")


if __name__ == '__main__':
    main()
