"""
Prompts System - Advanced prompting templates and formatters

Contains system prompts, task-specific prompts, and response formatters.
"""

from typing import List, Dict, Any


# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT_BASE = """You are a smart AI agent running locally on {os_info}.

RULES:
1. For SIMPLE tasks (create file, calculator, simple query): Execute DIRECTLY.
2. For COMPLEX tasks (new technology, research): Learn first (if online) or check cache.
3. ALWAYS generate VALID code with proper syntax. Check parentheses, brackets, and quotes are balanced.
4. NO HALLUCINATION: Use ONLY available tools. Use EXACT service names as mentioned by user.
5. ONLINE STATUS: {online_status}

TOOL SELECTION GUIDE:
- get_system_info: For OS, CPU, RAM, disk info (general system information)
- monitor_resources: For CURRENT CPU/RAM usage percentages and real-time monitoring
- list_dir: For listing directory contents (all files/folders)
- search_files: For finding files matching a pattern (e.g., *.py, *.txt)
- read_file: For reading file contents
- write_file: For creating/writing files
- check_service_status: Use EXACT service name from user (e.g., "Ollama" not "Apache")
- search_web: For internet searches - use specific, technical queries (e.g., "Python 3.12 release date" not "latest Python version")
- python_repl: For calculations - use simple, valid Python code (e.g., "print(sum([10,20,30,40,50])/5)")

AVAILABLE TOOLS:
{tools_list}

Response format (MUST be valid JSON):
{{
  "thought": "Step-by-step reasoning",
  "action": "tool_name",
  "action_input": {{"param": "value"}}
}}

EXAMPLES:

SIMPLE (Direct):
User: "Create calculator.py"
Action: write_file("calculator.py", "def add(a, b):\\n    return a + b...")

User: "What is CPU usage?"
Action: monitor_resources()  # NOT get_system_info

User: "Find Python files"
Action: search_files({{"pattern": "*.py", "directory": "."}})  # NOT list_dir

User: "Check if Ollama is running"
Action: check_service_status({{"service_name": "Ollama"}})  # Use EXACT name from user

User: "Calculate average of 10, 20, 30, 40, 50"
Action: python_repl({{"code": "numbers = [10, 20, 30, 40, 50]\\nprint(sum(numbers) / len(numbers))"}})

COMPLEX (Learn first):
User: "Create Docker container"
Action: search_documentation("docker", "container basics")  # Only if online
Then: write_file("Dockerfile", "FROM python:3.9...")

OFFLINE (Cache):
User: "How to use n8n?"
Action: read_knowledge_base("n8n")

User request: {user_input}
"""


SECURITY_TASK_PROMPT = """
🔒 SECURITY TASK DETECTED

Additional guidelines for security tasks:
- Check current security status FIRST before making changes
- Propose least-invasive solutions
- Explain security implications clearly
- Suggest backup before making changes
- Verify changes after execution
- Consider compliance and best practices
"""


DATA_ANALYSIS_PROMPT = """
📊 DATA ANALYSIS TASK DETECTED

Guidelines for data analysis:
- Use pandas for Excel/CSV files
- Generate summary statistics
- Identify patterns and anomalies
- Create visualizations if helpful
- Provide actionable insights
- Explain methodology clearly
"""


DEPLOYMENT_PROMPT = """
🚀 DEPLOYMENT TASK DETECTED

Guidelines for deployment:
- Check system requirements first
- Verify dependencies
- Use staging environment if available
- Plan rollback strategy
- Monitor after deployment
- Document changes
"""


DEBUGGING_PROMPT = """
🐛 DEBUGGING TASK DETECTED

Guidelines for debugging:
- Gather error information first
- Check logs and stack traces
- Isolate the problem
- Test hypotheses systematically
- Verify fix works
- Document root cause
"""


# ═══════════════════════════════════════════════════════════
# CLARIFICATION TEMPLATES
# ═══════════════════════════════════════════════════════════

CLARIFICATION_TEMPLATE = """
I need clarification on your request to provide the best solution.

Your request: "{user_input}"

Please clarify:
{questions}
Once I have this information, I can proceed with confidence.
"""


# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

def get_system_prompt(
    user_input: str,
    tools_list: str,
    history: List[Dict[str, Any]] = None,
    os_info: str = "Unknown OS",
    online: bool = True
) -> str:
    """
    Get the appropriate system prompt based on task type.
    
    Args:
        user_input: User's request
        tools_list: JSON string of available tools
        history: Conversation history
        os_info: Information about the operating system
        online: Whether internet is available
    """
    # Format history
    history_str = ""
    if history:
        for i, item in enumerate(history[-5:]):  # Last 5 items
            history_str += f"\nStep {i+1}:\n"
            history_str += f"  Thought: {item.get('thought', 'N/A')}\n"
            history_str += f"  Action: {item.get('action', 'N/A')}\n"
            history_str += f"  Observation: {str(item.get('observation', 'N/A'))[:500]}...\n"
    else:
        history_str = "No previous steps in this task."
    
    # Build base prompt
    prompt = SYSTEM_PROMPT_BASE.format(
        tools_list=tools_list,
        history=history_str,
        user_input=user_input,
        os_info=os_info,
        online_status="ONLINE" if online else "OFFLINE"
    )
    
    # Add task-specific prompts
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ['security', 'ssl', 'certificate', 'firewall', 'vulnerability']):
        prompt += "\n" + SECURITY_TASK_PROMPT
    
    if any(word in user_lower for word in ['analyze', 'analysis', 'data', 'excel', 'csv', 'statistics']):
        prompt += "\n" + DATA_ANALYSIS_PROMPT
    
    if any(word in user_lower for word in ['deploy', 'deployment', 'release', 'production']):
        prompt += "\n" + DEPLOYMENT_PROMPT
    
    if any(word in user_lower for word in ['debug', 'error', 'bug', 'fix', 'issue', 'problem']):
        prompt += "\n" + DEBUGGING_PROMPT
    
    return prompt


def format_tool_response(tool_name: str, result: Any) -> str:
    """
    Format tool execution result for display.
    
    Args:
        tool_name: Name of the tool
        result: Tool execution result
    
    Returns:
        Formatted string
    """
    if isinstance(result, dict):
        if 'error' in result:
            return f"❌ Error in {tool_name}: {result['error']}"
        elif 'stdout' in result:
            return f"✓ {tool_name} output:\n{result['stdout']}"
        else:
            import json
            return f"✓ {tool_name} result:\n{json.dumps(result, indent=2)}"
    elif isinstance(result, list):
        return f"✓ {tool_name} returned {len(result)} items"
    else:
        return f"✓ {tool_name}: {str(result)}"


def generate_clarification_questions(user_input: str, ambiguities: List[str]) -> str:
    """
    Generate clarification questions for ambiguous requests.
    
    Args:
        user_input: User's request
        ambiguities: List of ambiguous aspects
    
    Returns:
        Formatted clarification request
    """
    questions = "\n".join([f"{i+1}. {q}" for i, q in enumerate(ambiguities)])
    
    return CLARIFICATION_TEMPLATE.format(
        user_input=user_input,
        questions=questions
    )


def format_risk_explanation(risk_level: str, action: str, details: str) -> str:
    """
    Format risk explanation for user.
    
    Args:
        risk_level: 'safe', 'caution', or 'dangerous'
        action: Action being taken
        details: Risk details
    
    Returns:
        Formatted risk explanation
    """
    emojis = {
        'safe': '🟢',
        'caution': '🟡',
        'dangerous': '🔴'
    }
    
    emoji = emojis.get(risk_level, '⚪')
    
    return f"""
{emoji} RISK LEVEL: {risk_level.upper()}

Action: {action}

{details}

Please review carefully before approving.
"""


# ═══════════════════════════════════════════════════════════
# MULTI-SOLUTION TEMPLATES
# ═══════════════════════════════════════════════════════════

def format_multiple_solutions(solutions: List[Dict[str, str]]) -> str:
    """
    Format multiple solution options for user.
    
    Args:
        solutions: List of solution dicts with 'approach', 'pros', 'cons'
    
    Returns:
        Formatted solutions
    """
    output = "I found multiple approaches to solve this:\n\n"
    
    for i, sol in enumerate(solutions, 1):
        output += f"**Option {i}: {sol['approach']}**\n"
        output += f"✅ Pros: {sol['pros']}\n"
        output += f"❌ Cons: {sol['cons']}\n\n"
    
    output += "Which approach would you prefer?"
    
    return output


# ═══════════════════════════════════════════════════════════
# EDUCATIONAL CONTEXT
# ═══════════════════════════════════════════════════════════

def add_educational_context(solution: str, explanation: str) -> str:
    """
    Add educational context to a solution.
    
    Args:
        solution: The solution
        explanation: Why this solution works
    
    Returns:
        Solution with educational context
    """
    return f"""
{solution}

💡 **Why this works:**
{explanation}

This will help you understand the solution better and apply similar approaches in the future.
"""
