import pytest
from unittest.mock import Mock, patch
import sys
import os

# Now we can import from the module directly
from src.router import ModelRouter, get_router


@pytest.fixture
def mock_client():
    """Create a mock OllamaClient with sample models."""
    mock_client = Mock()
    # Simulate available models
    mock_client.list_models.return_value = ["qwen3.5", "phi3", "system_model"]
    mock_client.generate.return_value = {"content": "This is a test response.", "done": True}
    
    return mock_client


class TestModelRouter:
    
    def test_get_available_models(self, mock_client):
        """Test fetching available models."""
        with patch('src.router._get_client', return_value=mock_client):
            router = ModelRouter()
            
            # Verify the client's list_models method was called
            assert mock_client.list_models.called
            
            # Get a fresh instance for each test to ensure clean state
            router2 = ModelRouter()
            models = router2.get_available_models()
            
            assert isinstance(models, list)
            assert len(models) == 3  # Based on mock
            assert "qwen3.5" in models
            
    def test_select_model_priority(self, mock_client):
        """Test selecting a specific model via priority_models argument."""
        with patch('src.router._get_client', return_value=mock_client):
            router = ModelRouter()
            
            priority_models = ["phi3", "qwen3.5"]
            result = router.select_model(priority_models=priority_models)
            
            assert result == "phi3"
    
    def test_select_model_default(self, mock_client):
        """Test selecting the default model from environment."""
        # Set up environment variable for test
        os.environ["DEFAULT_MODEL"] = "qwen3.5"
        
        try:
            with patch('src.router._get_client', return_value=mock_client):
                router = ModelRouter()
                result = router.select_model(prompt="Hello")
                
                assert result == "qwen3.5"
        finally:
            # Clean up environment variable after test
            del os.environ["DEFAULT_MODEL"]
    
    def test_select_model_fallback(self, mock_client):
        """Test selecting the first usable model when defaults fail."""
        with patch('src.router._get_client', return_value=mock_client):
            router = ModelRouter()
            
            # Ensure DEFAULT_MODEL is not set in environment
            if "DEFAULT_MODEL" in os.environ:
                del os.environ["DEFAULT_MODEL"]
                
            result = router.select_model(prompt="Hello")
            
            assert result == "phi3"  # First non-system model
            
    def test_generate_with_prompt(self, mock_client):
        """Test the generate method."""
        with patch('src.router._get_client', return_value=mock_client):
            router = ModelRouter()
            
            response = router.generate("Explain quantum physics")
            
            # Verify the client's generate method was called with correct args
            mock_client.generate.assert_called_once_with("qwen3.5", "Explain quantum physics")
            assert isinstance(response, str)
            assert "This is a test response." in response


def test_get_router_singleton():
    """Test the singleton pattern."""
    # First call should create instance
    router1 = get_router()
    
    # Second call should return same instance
    with patch('src.router.ModelRouter') as MockModelRouter:
        mock_instance = Mock(ModelRouter)
        MockModelRouter.return_value = mock_instance
        
        router2 = get_router()
        
        # The actual ModelRouter.__init__ was only called once due to singleton check
        assert MockModelRouter.call_count == 1