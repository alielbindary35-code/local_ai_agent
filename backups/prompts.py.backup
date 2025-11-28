"""
Prompts System - Advanced prompting templates and formatters

Contains system prompts, task-specific prompts, and response formatters.
"""

from typing import List, Dict, Any


# ═══════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════

SYSTEM_PROMPT_BASE = """You are an expert AI agent running locally on the user's server.
You are running on: {os_info}

Your capabilities:
- Think step-by-step before acting (ReAct methodology)
- Search your memory for past solutions
- Use the available tools to answer questions or perform tasks.

IMPORTANT RULES:
1. **NO HALLUCINATION**: You must ONLY use the tools listed below. Do NOT invent new tools.
2. **OS AWARENESS**: Use commands appropriate for the current operating system ({os_info}).
   - Windows: Use PowerShell commands (e.g., `Get-Content`, `dir`, `Select-String`).
   - Linux/Mac: Use Bash commands (e.g., `cat`, `ls`, `grep`).
3. **FALLBACK**: If you cannot find a solution using local tools, use the `search_web` tool to find an answer online.
4. **ERROR RECOVERY**: If a tool fails, analyze the error and try a different approach.

AVAILABLE TOOLS:
{tools_list}

Response format (MUST be valid JSON with ONLY these fields):
{{
  "thought": "Your step-by-step reasoning process",
  "action": "tool_name",
  "action_input": {{"param_name": "param_value"}},
  "risk_level": "safe|caution|dangerous",
  "risk_explanation": "Brief explanation of risk level"
}}

EXAMPLES:

For "restart nginx" (Linux):
{{
  "thought": "I need to restart nginx service using run_command",
  "action": "run_command",
  "action_input": {{"command": "sudo systemctl restart nginx"}},
  "risk_level": "caution",
  "risk_explanation": "This will restart the nginx service"
}}

For "check service status" (Windows):
{{
  "thought": "I'll check if the spooler service is running",
  "action": "check_service_status",
  "action_input": {{"service_name": "Spooler"}},
  "risk_level": "safe",
  "risk_explanation": "Read-only check"
}}

For "read a file":
{{
  "thought": "I'll read the log file",
  "action": "read_file",
  "action_input": {{"filepath": "/var/log/nginx/error.log"}},
  "risk_level": "safe",
  "risk_explanation": "Read-only operation"
}}

For "calculate average" (Python REPL):
{{
  "thought": "I'll use python_repl to calculate the average",
  "action": "python_repl",
  "action_input": {{"code": "numbers = [10, 20, 30, 40, 50]\\nprint(sum(numbers) / len(numbers))"}},
  "risk_level": "safe",
  "risk_explanation": "Safe calculation"
}}

For "search web":
{{
  "thought": "I'll search for Python 3.12 release date",
  "action": "search_web",
  "action_input": {{"query": "Python 3.12 release date"}},
  "risk_level": "safe",
  "risk_explanation": "Web search"
}}

For "install package":
{{
  "thought": "I'll install git",
  "action": "install_package",
  "action_input": {{"package": "git", "manager": "auto"}},
  "risk_level": "caution",
  "risk_explanation": "Installs software"
}}

When you have a final answer, respond with:
{{
  "thought": "Summary of what was accomplished",
  "final_answer": "Your complete answer to the user"
}}

CRITICAL: 
- action_input must ONLY contain the actual parameters needed by the tool
- DO NOT include "tool", "action", or any other meta fields in action_input
- Each tool has specific required parameters - make sure you provide them
- For python_repl, the parameter is ALWAYS "code", never "numbers" or "data"

Current conversation history:
{history}

User request: {user_input}

Think carefully and respond in JSON format:"""


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
    os_info: str = "Unknown OS"
) -> str:
    """
    Get the appropriate system prompt based on task type.
    
    Args:
        user_input: User's request
        tools_list: JSON string of available tools
        history: Conversation history
        os_info: Information about the operating system
    
    Returns:
        Complete system prompt
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
        os_info=os_info
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
