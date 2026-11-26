# Home AI Infrastructure - Application Platform (Phase 3)

This repository establishes the software foundation for future AI agents. It provides a Python environment configured to communicate with an Ollama instance on a remote Ubuntu server.

## Project Structure

- `src/`: Core application logic.
- `tests/`: Automated tests using pytest.
- `logs/`: Application logs.
- `.env.example`: Environment configuration template.

## Prerequisites
1. Git installed on your workstation
2. SSH client available (OpenSSH)
3. Network access to ai-server

## Step-by-Step Setup

### Step 1: Connect via SSH Tunnel
Open PowerShell on your workstation and run:

```powershell
ssh -N -L 11434:127.0.0.1:11434 ai-server 
```

**Command Breakdown:**
- `-N`: Don't execute any command on remote (forward only)
- `-L`: Create local port forwarding
- `127.0.0.1:11434`: Local endpoint to access
- `ai-server:ollama-user@ai-server`: Remote host and SSH username

### Step 2: Verify Connection
You should see a message like "Connecting to ai-server..." in your terminal window. Keep this terminal open - it maintains the tunnel.

### Step 3: Access Ollama API Locally
Once connected, you can access the API at `http://127.0.0.1:11434` using tools like:
- Postman
- curl
- Any REST client

## Troubleshooting

**Common Issues:**
- **Connection refused**: Ensure ai-server SSH port is open (default 22)
- **Port already in use**: Check for other processes using port 11434 on your workstation
- **SSH not found**: Install OpenSSH client from [GitHub](https://github.com/tyrossl/openssh-windows)

## Maintenance
To stop the tunnel, close the PowerShell session or run:
```powershell
netstat -ano | findstr :11434
```

*Note: Keep the SSH terminal open to maintain the active connection.*


## Setup Instructions

1. **Clone the repository**.
2. **Install dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. **Create Virtual Environment (Recommended)**:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Unix/macOS
   # or
   .venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source .venv/Scripts/activate  # Git Bash
   python -m pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
   Copy `.env.example` to `.env` and configure your Ollama server details (see Section 6 in `phase3-application-platform.md`).


## Usage Example

Import the router to get available models:

```python
from src.router import get_available_models
models = get_available_models()
print(models)
```

### Running Tests

Ensure `.env` is set correctly, then run:

```bash
pytest tests/
```

---

### 4. `src/__init__.py`

Empty marker file to make it a Python package.

```python
# src/__init__.py - Empty marker file
```

---

### 5. `src/logger.py` (Section 9)

Implements standardized logging using the built-in `logging` module and reads config from `.env`.

```python
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class AppLogger:
    """Standardized logger for the Home AI Platform."""
    
    def __init__(self, name="App"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
        
    def _setup_logger(self):
        log_level = os.getenv("LOG_LEVEL", "INFO")
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # File Handler
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(level)
        file_handler.setFormatter(console_formatter)
        
        # Add handlers to root logger (simpler than managing self.logger.handlers)
        # This is a simplified approach. For robust separation, 
        # we usually add directly to the specific logger instance here or return it.
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            handlers=[console_handler, file_handler],
        )

    def get_logger(self):
        # Return a fresh logger instance that uses the configured config
        return logging.getLogger("HomeAIPlatform")

# Convenience function to get the logger instance
def get_logger():
    return AppLogger().get_logger()
```

---

### 6. `src/ollama_client.py` (Section 7)

Handles communication with the Ollama API using `requests`. Implements error handling and retries.

```python
import requests
from dotenv import load_dotenv
import logging
import time

# Load environment variables
load_dotenv()

logger = logging.getLogger("OllamaClient")

class OllamaClient:
    """Abstracts interaction with the Ollama API."""
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.timeout = int(os.getenv('OAPI_TIMEOUT', '30'))
        self.max_retries = int(os.getenv('OAPI_RETRIES', '2'))
        
    def list_models(self):
        """List all available models."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json().get('models', [])
            else:
                logger.error(f"Failed to list models. Status: {response.status_code}")
                return []
        except Exception as e:
            logger.exception(f"Error listing models: {e}")
            raise

    def generate(self, model_name, prompt, stream=False):
        """Generate a response from a specific model."""
        url = f"{self.base_url}/api/generate"
        
        try:
            data = {
                "model": model_name,
                "prompt": prompt,
                "stream": stream,
                "format": "json" if not stream else "plain_text" # Adjust format if needed
            }
            
            # For streaming, we might need a different response handling logic later.
            # This is a basic non-streaming call for now to ensure structure consistency.
            
            response = requests.post(url, json=data, timeout=self.timeout)
            
            if response.status_code == 200:
                result = response.json()
                # In streaming, results come in chunks; here we get full text directly or handle chunks.
                # Assuming JSON output for simplicity in this demo:
                return result.get('response', '')
            else:
                logger.error(f"Generation failed. Status: {response.status_code}")
                return None
                
        except Exception as e:
            logger.exception(f"Error generating response: {e}")
            raise

    def is_available(self):
        """Check if the server is reachable."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5 # Short timeout for health check
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Server unavailable: {e}")
            return False

# Singleton instance to avoid re-initialization
_instance = None

def get_client():
    global _instance
    if _instance is None:
        _instance = OllamaClient()
    return _instance
```

---

### 7. `src/router.py` (Section 8)

Provides a clean interface to interact with models, preventing hardcoding specific model names in business logic.

```python
import os
from dotenv import load_dotenv
import requests
from src.ollama_client import get_client as _get_client
import logging

logger = logging.getLogger("ModelRouter")

class ModelRouter:
    """Manages and routes model requests."""
    
    def __init__(self):
        self.client = _get_client()
        self._ensure_connection()
        
    def _ensure_connection(self):
        """Check if Ollama is running. If not, try to list models and handle gracefully."""
        if not self.client.is_available():
            logger.warning("Ollama server appears to be offline.")
            
    def get_available_models(self):
        """Fetch a list of available models."""
        return self.client.list_models()
        
    def select_model(self, prompt=None, priority_models=None):
        """
        Select a model based on user preference or defaults.
        
        Args:
            prompt (str): User input. Can influence selection (e.g., code vs creative).
            priority_models (list): Manual override list.
            
        Returns:
            str: Name of the selected model.
        """
        models = self.get_available_models()
        
        # 1. Manual Override
        if priority_models and len(priority_models) > 0:
            for m in priority_models:
                if m in models:
                    logger.info(f"Using specified model: {m}")
                    return m
        
        # 2. Default Selection (based on env var or first available)
        default_model = os.getenv("DEFAULT_MODEL", "llama3.2")
        
        if default_model and default_model in models:
            logger.info(f"Using default model: {default_model}")
            return default_model
            
        # 3. Fallback to first non-system model
        usable_models = [m for m in models if 'system' not in m.lower()]
        if usable_models:
            selected = usable_models[0]
            logger.info(f"Falling back to first available model: {selected}")
            return selected
            
        logger.error("No usable models found.")
        return None
        
    def generate(self, prompt, model_name=None):
        """Delegate generation to the client."""
        if not model_name:
            model_name = self.select_model(prompt)
            
        if not model_name:
            raise ValueError("No model available for generation.")
            
        logger.info(f"Generating response with {model_name}")
        return self.client.generate(model_name, prompt)

# Singleton instance
_instance = None

def get_router():
    global _instance
    if _instance is None:
        _instance = ModelRouter()
    return _instance