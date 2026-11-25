# src/router.py

"""
Model Router module for Home AI Platform.

This module provides a clean interface to interact with models, 
preventing hardcoding specific model names in business logic.
It manages the routing of requests between different available LLMs.
"""

import os
from dotenv import load_dotenv
import logging

# Import the OllamaClient from this project's structure
try:
    # If running within the virtual environment defined in README.md Step 3
    from src.ollama_client import get_client as _get_client
except ImportError:
    # Fallback for direct import (though README.md expects src.ollama_client)
    from ollama_client import get_client as _get_client

logger = logging.getLogger("ModelRouter")


class ModelRouter:
    """Manages and routes model requests to the Ollama API."""
    
    def __init__(self):
        """Initialize the router with the Ollama client."""
        self.client = _get_client()
        
        # Ensure connection is valid before proceeding
        self._ensure_connection()
    
    def _ensure_connection(self):
        """
        Check if Ollama server is running.
        Logs a warning but does not prevent initialization.
        """
        try:
            if not self.client.is_available():
                logger.warning("Ollama server appears to be offline.")
        except Exception as e:
            logger.error(f"Failed to verify connection: {e}")
    
    def get_available_models(self) -> list:
        """
        Fetch a list of all available models from Ollama.
        
        Returns:
            list: A list of model names (strings).
        """
        try:
            return self.client.list_models()
        except Exception as e:
            logger.exception(f"Error listing models: {e}")
            return []
    
    def select_model(self, prompt=None, priority_models=None) -> str | None:
        """
        Select a model based on user preference or defaults.
        
        Args:
            prompt (str, optional): User input. Can influence selection logic if implemented.
            priority_models (list[str], optional): Manual override list of models to try first.
            
        Returns:
            str | None: Name of the selected model, or None if no suitable model found.
        """
        models = self.get_available_models()
        
        # 1. Manual Override Check
        if priority_models and len(priority_models) > 0:
            for m in priority_models:
                if m in models:
                    logger.info(f"Using specified model: {m}")
                    return m
        
        # 2. Default Selection (from environment variable or standard fallback)
        default_model = os.getenv("DEFAULT_MODEL", "qwen3.5")
        
        if default_model and default_model in models:
            logger.info(f"Using default model from env var: {default_model}")
            return default_model
            
        # 3. Fallback to first non-system model
        usable_models = [m for m in models if 'system' not in m.lower()]
        if usable_models:
            selected = usable_models[0]
            logger.info(f"Falling back to first available model: {selected}")
            return selected
            
        logger.error("No usable models found.")
        return None
    
    def generate(self, prompt: str, model_name: str | None = None) -> str:
        """
        Generate a response from the Ollama API.
        
        Args:
            prompt (str): The text to generate a response for.
            model_name (str | None): The name of the model to use. 
                                   If None, the router will select a default model.
        
        Returns:
            str: The generated response text.
            
        Raises:
            ValueError: If no model is available for generation.
        """
        # Select model if not explicitly provided
        if not model_name:
            model_name = self.select_model(prompt)
            
            if not model_name:
                raise ValueError("No model available for generation.")
            
            logger.info(f"Selected model for generation: {model_name}")
        
        logger.info(f"Generating response with model '{model_name}'")
        
        try:
            # Delegate the actual API call to the client
            result = self.client.generate(model_name, prompt)
            
            if result is None:
                raise ValueError("Model returned empty or invalid response.")
                
            return str(result)
            
        except Exception as e:
            logger.exception(f"Error generating response: {e}")
            raise


# Singleton instance management
_instance = None

def get_router() -> ModelRouter:
    """
    Get the singleton instance of ModelRouter.
    
    Returns:
        ModelRouter: The global router instance.
    """
    global _instance
    if _instance is None:
        # Lazy initialization to avoid issues if Ollama is not yet running
        logger.info("Initializing ModelRouter singleton.")
        _instance = ModelRouter()
    return _instance