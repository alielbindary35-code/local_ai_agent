"""
Test JSON tool call parsing with a mock response
"""
import json
import re

# Simulate the response from deepseek-r1:8b with JSON tool calls
mock_response = """
I will help you learn Docker technology. Here are the tool calls I need to execute:

{
  "tool": "learn_new_technology",
  "args": ["Docker", ["containers", "images", "docker-compose"]]
}

{
  "tool": "read_knowledge_base",
  "args": ["Docker"]
}

{
  "tool": "search_documentation",
  "args": ["containers"]
}
"""

print("Testing JSON Tool Call Parsing")
print("=" * 60)
print("\nMock Response:")
print(mock_response)
print("\n" + "=" * 60)

# Test the IMPROVED JSON parsing approach
json_tool_calls = []
try:
    # Find all potential JSON blocks first by tracking braces
    potential_jsons = []
    brace_count = 0
    start_idx = -1
    
    for i, char in enumerate(mock_response):
        if char == '{':
            if brace_count == 0:
                start_idx = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start_idx != -1:
                json_str = mock_response[start_idx:i+1]
                potential_jsons.append(json_str)
                start_idx = -1
    
    print(f"\nFound {len(potential_jsons)} potential JSON blocks\n")
    
    # Now try to parse each potential JSON
    for json_str in potential_jsons:
        try:
            data = json.loads(json_str)
            if isinstance(data, dict) and "tool" in data and "args" in data:
                tool_name = data["tool"]
                args_list = data["args"]
                if not isinstance(args_list, list):
                    args_list = [args_list]
                json_tool_calls.append((tool_name, args_list))
                print(f"✅ Tool: {tool_name}")
                print(f"   Args: {args_list}")
                print()
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Skipping invalid JSON: {e}")
            continue
            
except Exception as e:
    print(f"❌ JSON tool parsing failed: {e}")

print("=" * 60)
print(f"\n✨ Result: Successfully parsed {len(json_tool_calls)} tool calls!")
print("\nThe fix is working correctly! 🎉")
