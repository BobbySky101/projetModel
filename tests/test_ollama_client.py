import pytest
from projet_model.clients.ollama_client import get_client, OllamaClient
import os
# Optional: Set a fake env if real connection fails for local testing
# os.environ['OLLAMA_HOST'] = 'http://localhost:11434' 

def test_get_client():
    """Test that client instance is created."""
    client = get_client()
    assert isinstance(client, OllamaClient)

def test_list_models_structure():
    """Verify the return type of list_models (if connection succeeds)."""
    client = get_client()
    
    # If this fails, it's likely a network issue or missing config.
    # It is expected to raise an exception if server is unreachable.
    try:
        models = client.list_models()
        assert isinstance(models, list)
    except Exception as e:
        pytest.fail(f"Client failed to connect or process response: {e}")

def test_generate_response():
    """Test generation with a known model (if available)."""
    router = __import__('projet_model.routing.router', fromlist=['get_router']).get_router()
    # Use a known stable model if possible, otherwise first available
    models = router.get_available_models()
    
    test_prompt = "Hello, this is a Phase 3 test."
    
    # Pick one model to test against