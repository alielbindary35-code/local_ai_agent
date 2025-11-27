"""
Script to organize project files into proper directory structure
"""
import os
import shutil
from pathlib import Path

# Define source and destination mappings
ORGANIZATION = {
    'agents': {
        'src': ['agent.py', 'expert_agent.py', 'simple_agent.py'],
        'dest': 'src/agents'
    },
    'tools': {
        'src': ['tools.py', 'expert_tools.py', 'extended_tools.py'],
        'dest': 'src/tools'
    },
    'core': {
        'src': ['memory.py', 'prompts.py', 'simple_prompts.py', 
                'trainer.py', 'automated_trainer.py', 'monitor_training.py',
                'train_agent.py', 'clean_memory.py'],
        'dest': 'src/core'
    },
    'scripts': {
        'src': ['*.bat', '*.sh'],
        'dest': 'scripts'
    },
    'docs': {
        'src': ['*.md', 'documentation.html'],
        'dest': 'docs'
    },
    'tests': {
        'src': ['test_*.py', 'verify_agent.py', 'test_*.txt', 'test_output.txt'],
        'dest': 'tests'
    },
    'data': {
        'src': ['agent_log.txt', 'agent_memory.db', 'training_report.txt'],
        'dest': 'data'
    },
    'examples': {
        'src': ['learn_docker.py', 'force_create_n8n.py', 'interactive_session.py'],
        'dest': 'examples'
    }
}

def organize_files():
    """Organize project files into proper directories"""
    base_path = Path('.').resolve()
    print(f"Working directory: {base_path}")
    
    # Create directories
    for org in ORGANIZATION.values():
        dest_path = base_path / org['dest']
        dest_path.mkdir(parents=True, exist_ok=True)
        print(f"Created/Verified directory: {dest_path}")
    
    # Move files
    for category, config in ORGANIZATION.items():
        dest_path = base_path / config['dest']
        print(f"\nProcessing {category}...")
        
        for pattern in config['src']:
            if '*' in pattern:
                # Handle glob patterns
                import glob
                files = glob.glob(pattern)
                print(f"  Found {len(files)} files matching {pattern}")
                for file in files:
                    src_file = base_path / file
                    if src_file.exists():
                        dest_file = dest_path / file
                        try:
                            shutil.move(str(src_file), str(dest_file))
                            print(f"  ✓ Moved {file} -> {dest_file}")
                        except Exception as e:
                            print(f"  ✗ Error moving {file}: {e}")
            else:
                # Handle specific files
                src_file = base_path / pattern
                if src_file.exists():
                    dest_file = dest_path / pattern
                    try:
                        shutil.move(str(src_file), str(dest_file))
                        print(f"  ✓ Moved {pattern} -> {dest_file}")
                    except Exception as e:
                        print(f"  ✗ Error moving {pattern}: {e}")
                else:
                    print(f"  - File not found: {pattern}")
    
    # Move logs directory
    logs_src = base_path / 'logs'
    if logs_src.exists():
        logs_dest = base_path / 'data' / 'logs_backup'
        if logs_dest.exists():
            shutil.rmtree(str(logs_dest))
        shutil.move(str(logs_src), str(logs_dest))
        print(f"\n✓ Moved logs -> {logs_dest}")
    
    # Move knowledge_base
    kb_src = base_path / 'knowledge_base'
    if kb_src.exists():
        kb_dest = base_path / 'data' / 'knowledge_base'
        if kb_dest.exists():
            shutil.rmtree(str(kb_dest))
        shutil.move(str(kb_src), str(kb_dest))
        print(f"✓ Moved knowledge_base -> {kb_dest}")
    
    print("\n✅ Project organization complete!")

if __name__ == '__main__':
    organize_files()

