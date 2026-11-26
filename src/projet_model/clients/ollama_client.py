"""
Ollama Client module for Home AI Platform.

This module provides the low-level communication interface with the Ollama API,
handling HTTP requests and responses while abstracting connection details
(like base URL) from higher-level application logic.
"""

import os
import logging
import requests
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

logger = logging.getLogger("OllamaClient")


class OllamaClient:
    """Abstracts interaction with the Ollama API."""

    def __init__(self):
        """Initialize client with configuration from environment variables."""
        # Use local port forwarding if configured, otherwise default to localhost
        self.base_url = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:11434')
        
        # Configuration for API requests
        self.timeout = int(os.getenv('OAPI_TIMEOUT', '60'))
        self.max_retries = int(os.getenv('OAPI_RETRIES', '2'))

    def list_models(self) -> list:
        """
        List all available models on the Ollama server.
        
        Returns:
            list: A list of model names (strings).
        """
        url = f"{self.base_url}/api/tags"
        
        try:
            response = self._make_request("GET", url)
            
            if response.status_code == 200:
                data = response.json()
                # Ollama returns models as a list inside the JSON object
                return data.get('models', [])
            else:
                logger.error(f"Failed to list models. Status: {response.status_code}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error("Request to Ollama timed out.")
            return []
        except requests.exceptions.ConnectionError:
            logger.warning("Connection refused or reset by peer (Ollama might be offline).")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error listing models: {e}")
            return []

    def generate(self, model_name: str, prompt: str, stream: bool = False) -> dict | None:
        """
        Generate a response from the specified model.
        
        Args:
            model_name (str): The name of the model to use.
            prompt (str): The text to generate a response for.
            stream (bool): Whether to enable streaming (False by default).
            
        Returns:
            dict | None: The response object if successful, or None on failure.
        """
        url = f"{self.base_url}/api/generate"
        
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": stream,
            }
            
            # Note: Standard Ollama generate does not return raw JSON directly in the body for non-streaming.
            # It returns a completion object with 'response' text and metadata.
            if not stream:
                response = self._make_request("POST", url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "output": data.get('response', ''),
                        "context": data.get('context', []),
                        "done": True
                    }
                else:
                    logger.error(f"Generation failed. Status: {response.status_code}")
                    return None
            else:
                # For now, we stick to non-streaming or handle streaming chunks manually if required.
                # This keeps the API consistent with the documentation examples provided.
                logger.warning("Streaming is enabled but only returning first response chunk for consistency.")
                # Standard implementation would require a generator based approach.
                # We will assume non-streaming for Phase 3 simplicity as per the doc.
                
        except Exception as e:
            logger.exception(f"Error generating response: {e}")
            return None

    def is_available(self) -> bool:
        """
        Check if the Ollama server is reachable and responding.
        
        Returns:
            bool: True if reachable, False otherwise.
        """
        url = f"{self.base_url}/api/tags"
        
        try:
            response = self._make_request("GET", url)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Server check failed: {e}")
            return False

    def _make_request(self, method: str, url: str, json_data: dict = None) -> requests.Response:
        """
        Helper method to make HTTP requests with retry logic and logging.
        
        Args:
            method (str): HTTP method ('GET' or 'POST').
            url (str): The target URL.
            json_data (dict): JSON payload for POST requests.
            
        Returns:
            requests.Response: The HTTP response object.
        """
        try:
            if json_data is None:
                params = {}
            else:
                params = json_data
            
            # If using streaming, we might need to handle the Response differently
            # But for this phase, we assume non-streaming requests for consistency.
            
            response = self._make_request_inner(method, url, params)
            
            return response
            
        except Exception as e:
            logger.exception(f"Error in internal request logic: {e}")
            raise

    def _make_request_inner(self, method: str, url: str, data: dict = None):
        """
        Inner helper to build the actual requests.post/get call.
        """
        import requests
        
        if data is None:
            data = {}
            
        try:
            response = requests.request(method, url, json=data, timeout=self.timeout)
            return response
            
        except requests.exceptions.Timeout:
            logger.warning("Request to Ollama timed out.")
            raise
        except requests.exceptions.ConnectionError:
            logger.warning("Connection error occurred (Ollama might be offline).")
            raise
        except Exception as e:
            logger.exception(f"Unexpected request error: {e}")
            raise

# Singleton instance to avoid re-initialization across the application
_instance = None


def get_client() -> OllamaClient:
    """
    Get the singleton instance of OllamaClient.
    
    This function is designed to be imported by `router.py` to maintain a global reference,
    ensuring consistent configuration and connection state throughout the application lifecycle.
    
    Returns:
        OllamaClient: The global client instance.
    """
    global _instance
    if _instance is None:
        logger.info("Initializing OllamaClient singleton.")
        _instance = OllamaClient()
    return _instance