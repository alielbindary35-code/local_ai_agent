# Implementation Plan - Agent Reliability & Intelligence Enhancements

## Goal Description
The goal is to fix the "stupid" behavior of the local AI agent where it hallucinates tools (e.g., `check_os_version`) and fails to recover from errors. We will make the agent robust, capable of self-correction, and able to use online search when local knowledge fails.

## User Review Required
> [!IMPORTANT]
> I will be modifying the core `agent.py` loop to inject specific error messages when tools fail. This changes the internal logic of the agent.

## Proposed Changes

### Local AI Agent

#### [MODIFY] [prompts.py](file:///c:/Users/engha/Music/New%20folder1/local_ai_agent/prompts.py)
- **Update `SYSTEM_PROMPT_BASE`**:
    - Add strict "NO HALLUCINATION" rules.
    - Explicitly list available tools in the prompt instructions (not just the JSON).
    - Add a "Fallback Strategy": If you don't know, search online.
    - Add OS-awareness instructions: "You are running on {os} {version}. Use appropriate commands (e.g., PowerShell for Windows, bash for Linux)."

#### [MODIFY] [agent.py](file:///c:/Users/engha/Music/New%20folder1/local_ai_agent/agent.py)
- **Enhance Error Handling**:
    - Detect "Tool not found" errors.
    - If a tool is not found, feed back a system message listing the *actual* available tools.
    - If `run_command` fails, suggest searching online.
- **Inject OS Context**:
    - Pass `platform.system()` and `platform.release()` to `get_system_prompt`.

#### [MODIFY] [trainer.py](file:///c:/Users/engha/Music/New%20folder1/local_ai_agent/trainer.py)
- **Session Logging**:
    - Create a log file (e.g., `logs/training_session_{timestamp}.txt`).
    - Log every user query, agent thought, tool output, and final answer.
    - Ensure the log is readable and structured.

#### [MODIFY] [tools.py](file:///c:/Users/engha/Music/New%20folder1/local_ai_agent/tools.py)
- **Robustness**:
    - Ensure `run_command` handles Windows/Linux differences gracefully where possible.
    - (Optional) Add aliases if the model persistently gets it wrong, but prompt engineering is preferred.

## Verification Plan

### Automated Verification
- None (LLM reasoning is hard to unit test deterministically without a complex eval harness).

### Manual Verification
1. **Run Trainer**: `python local_ai_agent/trainer.py`
2. **Test Case 1 (OS Version)**:
    - Input: "What is the OS version?"
    - Expected: Agent uses `get_system_info` (not `check_os`) and returns the Windows version.
3. **Test Case 2 (Search)**:
    - Input: "What is the latest version of Python?"
    - Expected: Agent uses `search_web` and returns the answer.
4. **Test Case 3 (Error Recovery)**:
    - Input: "Check system info using check_os_version tool" (forcing a hallucination if possible, or just seeing if it avoids it).
    - Expected: Agent corrects itself or refuses to use the non-existent tool.

## COMPLETED CHANGES

✅ **prompts.py** - Added OS awareness and strict tool usage rules
✅ **tools.py** - Improved tool descriptions with parameter info, added `get_os_identifier()`
✅ **agent.py** - Injected OS context into prompts, added "Tool not found" error recovery
✅ **trainer.py** - Added session logging to `logs/training_session_{date}.txt`

## HOW TO TEST

Run the trainer manually in your terminal:
```powershell
cd "c:\Users\engha\Music\New folder1"
python local_ai_agent/trainer.py
```

Then ask: "What is the OS version?"

The agent should now:
1. Know it's running on Windows
2. Use `get_system_info` tool (not hallucinate `check_os_version`)
3. Return the correct Windows version
4. Log everything to `logs/training_session_2025-11-27.txt`
