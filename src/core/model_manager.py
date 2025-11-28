"""
Model Manager - Optimized local AI model usage
==============================================

Manages local AI models, context, and optimizes model selection
for offline operation.
"""

import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages local AI models with context optimization.
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """
        Initialize model manager.
        
        Args:
            ollama_url: Ollama server URL
        """
        self.ollama_url = ollama_url
        self.available_models: List[Dict[str, Any]] = []
        self.model_cache: Dict[str, Any] = {}
        self.context_history: Dict[str, List[Dict]] = {}
        self.max_context_length = 4096  # Default context window
        
        self._refresh_models()
    
    def _refresh_models(self):
        """Refresh list of available models."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                self.available_models = [
                    {
                        'name': m['name'],
                        'size': m.get('size', 0),
                        'modified': m.get('modified_at', '')
                    }
                    for m in models
                ]
                logger.info(f"Found {len(self.available_models)} available models")
        except Exception as e:
            logger.warning(f"Could not refresh models: {e}")
            self.available_models = []
    
    def select_best_model(
        self,
        task_complexity: str = "medium",
        task_type: Optional[str] = None,
        context_size: Optional[int] = None
    ) -> Optional[str]:
        """
        Select best model for task.
        
        Args:
            task_complexity: Task complexity (simple, medium, complex)
            task_type: Task type (coding, general, etc.)
            context_size: Required context size
        
        Returns:
            Best model name or None
        """
        if not self.available_models:
            self._refresh_models()
        
        if not self.available_models:
            return None
        
        # Model selection logic
        model_scores = {}
        
        for model in self.available_models:
            name = model['name'].lower()
            score = 0
            
            # Complexity-based scoring
            if task_complexity == "simple":
                if any(x in name for x in ['3b', '7b', '8b']):
                    score += 50
            elif task_complexity == "medium":
                if any(x in name for x in ['7b', '8b', '14b']):
                    score += 50
            elif task_complexity == "complex":
                if any(x in name for x in ['14b', '32b', '70b']):
                    score += 50
            
            # Task type scoring
            if task_type == "coding":
                if 'deepseek' in name or 'coder' in name:
                    score += 30
            elif task_type == "general":
                if 'qwen' in name or 'llama' in name or 'mistral' in name:
                    score += 30
            
            # Size-based scoring (prefer smaller for speed)
            if '3b' in name:
                score += 20
            elif '7b' in name or '8b' in name:
                score += 15
            
            model_scores[model['name']] = score
        
        if model_scores:
            best_model = max(model_scores.items(), key=lambda x: x[1])
            logger.info(f"Selected model: {best_model[0]} (score: {best_model[1]})")
            return best_model[0]
        
        return self.available_models[0]['name'] if self.available_models else None
    
    def optimize_context(
        self,
        conversation_history: List[Dict[str, str]],
        max_tokens: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Optimize conversation context to fit within limits.
        
        Args:
            conversation_history: Full conversation history
            max_tokens: Maximum tokens (defaults to max_context_length)
        
        Returns:
            Optimized context
        """
        if max_tokens is None:
            max_tokens = self.max_context_length
        
        # Simple optimization: keep most recent messages
        # In production, use token counting
        if len(conversation_history) <= 10:
            return conversation_history
        
        # Keep system message if present
        optimized = []
        if conversation_history and conversation_history[0].get('role') == 'system':
            optimized.append(conversation_history[0])
        
        # Keep most recent messages
        optimized.extend(conversation_history[-9:])
        
        return optimized
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        for model in self.available_models:
            if model['name'] == model_name:
                return model
        return None
    
    def is_model_available(self, model_name: str) -> bool:
        """Check if model is available."""
        return any(m['name'] == model_name for m in self.available_models)

