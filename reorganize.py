#!/usr/bin/env python3
"""
Simple script to reorganize project files
Run this from the project root directory
"""
import os
import shutil
import glob

# Create directories
dirs = [
    'src/agents',
    'src/tools', 
    'src/core',
    'scripts',
    'docs',
    'tests',
    'data',
    'examples'
]

print("Creating directories...")
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"  ✓ {d}")

# Move agent files
print("\nMoving agent files...")
agents = ['agent.py', 'expert_agent.py', 'simple_agent.py']
for f in agents:
    if os.path.exists(f):
        shutil.move(f, f'src/agents/{f}')
        print(f"  ✓ {f} -> src/agents/")

# Move tool files
print("\nMoving tool files...")
tools = ['tools.py', 'expert_tools.py', 'extended_tools.py']
for f in tools:
    if os.path.exists(f):
        shutil.move(f, f'src/tools/{f}')
        print(f"  ✓ {f} -> src/tools/")

# Move core files
print("\nMoving core files...")
core = ['memory.py', 'prompts.py', 'simple_prompts.py', 
        'trainer.py', 'automated_trainer.py', 'monitor_training.py',
        'train_agent.py', 'clean_memory.py']
for f in core:
    if os.path.exists(f):
        shutil.move(f, f'src/core/{f}')
        print(f"  ✓ {f} -> src/core/")

# Move scripts
print("\nMoving scripts...")
for f in glob.glob('*.bat') + glob.glob('*.sh'):
    if os.path.exists(f):
        shutil.move(f, f'scripts/{f}')
        print(f"  ✓ {f} -> scripts/")

# Move documentation
print("\nMoving documentation...")
for f in glob.glob('*.md'):
    if f != 'README.md':  # Keep README in root
        if os.path.exists(f):
            shutil.move(f, f'docs/{f}')
            print(f"  ✓ {f} -> docs/")
if os.path.exists('documentation.html'):
    shutil.move('documentation.html', 'docs/documentation.html')
    print(f"  ✓ documentation.html -> docs/")

# Move tests
print("\nMoving test files...")
for f in glob.glob('test_*.py') + glob.glob('test_*.txt'):
    if os.path.exists(f):
        shutil.move(f, f'tests/{f}')
        print(f"  ✓ {f} -> tests/")
if os.path.exists('verify_agent.py'):
    shutil.move('verify_agent.py', 'tests/verify_agent.py')
    print(f"  ✓ verify_agent.py -> tests/")
if os.path.exists('test_output.txt'):
    shutil.move('test_output.txt', 'tests/test_output.txt')
    print(f"  ✓ test_output.txt -> tests/")

# Move data files
print("\nMoving data files...")
data_files = ['agent_log.txt', 'agent_memory.db', 'training_report.txt']
for f in data_files:
    if os.path.exists(f):
        shutil.move(f, f'data/{f}')
        print(f"  ✓ {f} -> data/")

# Move logs
if os.path.exists('logs'):
    if os.path.exists('data/logs_backup'):
        shutil.rmtree('data/logs_backup')
    shutil.move('logs', 'data/logs_backup')
    print(f"  ✓ logs -> data/logs_backup")

# Move knowledge_base
if os.path.exists('knowledge_base'):
    if os.path.exists('data/knowledge_base'):
        shutil.rmtree('data/knowledge_base')
    shutil.move('knowledge_base', 'data/knowledge_base')
    print(f"  ✓ knowledge_base -> data/knowledge_base")

# Move examples
print("\nMoving example files...")
examples = ['learn_docker.py', 'force_create_n8n.py', 'interactive_session.py']
for f in examples:
    if os.path.exists(f):
        shutil.move(f, f'examples/{f}')
        print(f"  ✓ {f} -> examples/")

print("\n✅ Project reorganization complete!")
print("\nNext steps:")
print("1. Update import statements in Python files")
print("2. Update script paths in batch/shell files")
print("3. Test that everything works")

