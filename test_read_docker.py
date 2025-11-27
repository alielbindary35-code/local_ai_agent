"""Test reading Docker knowledge base"""
from src.tools.expert_tools import ExpertTools

tools = ExpertTools()
result = tools.read_knowledge_base("Docker")
print(result)

