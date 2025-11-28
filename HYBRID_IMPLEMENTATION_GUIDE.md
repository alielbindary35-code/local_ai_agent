# Hybrid Agent - Quick Implementation Guide

## What We Need to Do:

### 1. Add Internet Detection (SIMPLE VERSION)

Instead of modifying the complex `expert_agent.py`, let's create a **wrapper** that adds the functionality:

**File**: `src/utils/connection_checker.py` (NEW)

```python
import requests
from rich.console import Console

console = Console()

class ConnectionChecker:
    """Simple internet connection checker"""
    
    @staticmethod
    def check_internet() -> bool:
        """Check if internet is available"""
        try:
            response = requests.get("https://www.google.com", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_status_message(online: bool) -> str:
        """Get status message"""
        if online:
            return "[green]🌐 Online Mode[/green]"
        else:
            return "[yellow]📴 Offline Mode[/yellow]"
```

### 2. Update ExpertTools with Cache Fallback

**File**: `src/tools/expert_tools.py`

Add at the beginning of each online method:

```python
def search_documentation(self, technology: str, query: str):
    # Check if online
    from src.utils.connection_checker import ConnectionChecker
    online = ConnectionChecker.check_internet()
    
    if online:
        try:
            # Do web search
            results = self._web_search(f"{technology} {query}")
            # Save to cache
            self._save_cache(technology, results)
            return results
        except:
            console.print("[yellow]⚠️ Search failed, using cache...[/yellow]")
    
    # Use cache
    return self._read_cache(technology)
```

### 3. Simplify Prompts

**File**: `src/core/prompts.py`

Change the prompt to be more direct:

```python
SYSTEM_PROMPT_BASE = """You are a smart AI agent.

RULES:
1. For SIMPLE tasks (create file, calculator): Execute DIRECTLY
2. For COMPLEX tasks (new technology): Learn first (if needed)
3. ALWAYS generate VALID code with proper syntax

Examples:

SIMPLE (Direct):
User: "Create calculator.py"
Action: write_file("calculator.py", "def add(a, b):\\n    return a + b...")

COMPLEX (Learn first - optional):
User: "Create Docker container"
Action: search_documentation("docker", "container basics")  # Only if online
Then: write_file("Dockerfile", "FROM python:3.9...")

User: {user_input}
"""
```

## SIMPLER APPROACH:

Since the codebase is complex, let's do **MINIMAL changes**:

### Option A: Just Fix the Prompts (EASIEST)

1. Update `src/core/prompts.py` - make it more direct
2. Remove `fast_learner` references
3. Done!

### Option B: Add Connection Check (MEDIUM)

1. Create `src/utils/connection_checker.py`
2. Update tools to check connection before web search
3. Fall back to cache if offline

### Option C: Full Hybrid (COMPLEX - what we planned)

1. All of the above
2. Plus code validation
3. Plus auto-caching
4. Plus intelligent fallback

## RECOMMENDATION:

Let's start with **Option A** (simplest):
- Fix prompts to be more direct
- Remove broken references
- Test it

Then if needed, add **Option B** (connection check).

What do you think?
