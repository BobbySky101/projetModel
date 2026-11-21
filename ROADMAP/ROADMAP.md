
# Home AI Infrastructure – Personal Project Plan

## 1. Project Overview

### Objective

Reuse an old computer by installing Linux and turning it into a dedicated local AI server.

The objective is to build a distributed AI environment where:

- The old computer hosts a lightweight local language model.
- The current computer acts as the primary development workstation.
- A more powerful AI model runs on the current computer or through an external API.
- A Python application coordinates the different models.
- AI agents help with application development, web scraping, data processing and analysis.

### Architecture

```text
CURRENT COMPUTER
- Python application
- Agent orchestration
- Advanced AI model
- Development environment
- Data analysis
        |
        | Local Network (SSH / HTTP)
        |
OLD COMPUTER (AI SERVER)
- Ubuntu Server
- Ollama
- Lightweight AI model
- Local inference API
        |
        | Internet
        |
EXTERNAL DATA SOURCES
- Websites
- Public APIs
- Documents
- Datasets
```

## 2. Recommended Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| OS | Ubuntu Server 24.04 LTS | Linux server |
| AI inference | Ollama | Run local models |
| Lightweight model | Llama 3.2 1B | Basic AI tasks |
| Programming | Python | Application development |
| Agent framework | LangGraph | Agent orchestration |
| IDE | Visual Studio Code | Development |
| Remote access | SSH | Remote administration |
| Web scraping | BeautifulSoup / Scrapy | Collect information |
| Data processing | Pandas | Data manipulation |
| Database | SQLite | Store information |

Documentation:

- Ubuntu: https://ubuntu.com/download/server
- Ollama: https://ollama.com/
- Ollama docs: https://docs.ollama.com/
- Python: https://docs.python.org/3/
- LangGraph: https://docs.langchain.com/oss/python/langgraph/overview
- VS Code Remote SSH: https://code.visualstudio.com/docs/remote/ssh

## 3. AI Models

The old computer has 8 GB RAM. Initially, assume CPU-only inference.

### Llama 3.2 1B

Lightweight model for basic classification, extraction and text processing.

```bash
ollama pull llama3.2:1b
```

### Gemma 2 2B

Useful for text processing and experimentation.

```bash
ollama pull gemma2:2b
```

### Llama 3.2 3B

A more capable alternative, worth testing if sufficient memory is available.

```bash
ollama pull llama3.2
```

Model sizes are approximate download sizes. Runtime memory requirements are higher.

**Recommendation:** Start with Llama 3.2 1B.

## 4. Implementation Roadmap

### Phase 1 – Prepare the Old Computer

Retrieve hardware information using Windows PowerShell:

```powershell
Get-CimInstance Win32_Processor |
  Select-Object Name

Get-CimInstance Win32_ComputerSystem |
  Select-Object TotalPhysicalMemory

Get-CimInstance Win32_DiskDrive |
  Select-Object Model, MediaType, Size

Get-CimInstance Win32_VideoController |
  Select-Object Name
```

Record:

- Processor model and generation.
- RAM.
- Disk capacity and type (SSD/HDD).
- Graphics card.
- 64-bit compatibility.

Download Ubuntu Server:

https://ubuntu.com/download/server

Create a bootable USB using Rufus:

https://rufus.ie/

Recommended installation settings:

| Setting | Value |
|---|---|
| Operating system | Ubuntu Server 24.04 LTS |
| Operating system (better) | Ubuntu Server 26.04 LTS |
| Hostname | ai-server |
| Network | Ethernet preferred |
| Installation | Clean installation |
| SSH server | Enabled |
| Additional packages | None initially |

Back up important data before installing Linux.

### Phase 2 – Configure Ubuntu Server

Update the system:

```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

Install useful utilities:

```bash
sudo apt install -y \
  curl \
  git \
  htop \
  build-essential \
  python3 \
  python3-pip \
  python3-venv \
  ufw
```

Retrieve the IP address:

```bash
hostname -I
```

Example:

```text
192.168.1.120
```

Configure a DHCP reservation on the router.

#### Configure the firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

Only SSH should be accessible initially.

### Phase 3 – Configure Remote Access

From Windows PowerShell:

```powershell
ssh your_username@192.168.1.120
```

Replace the username and IP address with your actual values.

Install Visual Studio Code and its Remote SSH extension:

https://code.visualstudio.com/docs/remote/ssh

Configure SSH key authentication.

Documentation:

https://ubuntu.com/server/docs/how-to/security/openssh-server/

### Phase 4 – Install Ollama

Install Ollama on Ubuntu:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Check installation:

```bash
ollama --version
```

Download the model:

```bash
ollama pull llama3.2:1b
```

Run it:

```bash
ollama run llama3.2:1b
```

Test with:

```text
You are a data analyst.
Explain the difference between structured
and unstructured data.
```

#### Test the local API

Ollama exposes an API on:

```text
http://localhost:11434
```

Test:

```bash
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Explain what a Python function is.",
    "stream": false
  }'
```

#### Configure secure remote access

Keep Ollama bound to localhost.

On Windows PowerShell:

```powershell
ssh -L 11434:127.0.0.1:11434 your_username@192.168.1.120
```

Keep the SSH session open.

In another PowerShell window:

```powershell
curl.exe http://localhost:11434/api/tags
```

The SSH tunnel forwards requests securely to Ollama.

### Phase 5 – Build the Python Application

On the current computer:

```powershell
mkdir home-ai-project
cd home-ai-project

python -m venv .venv
.venv\Scripts\activate

pip install requests python-dotenv
```

Recommended structure:

```text
home-ai-project/
│
├── .env
├── main.py
│
├── agents/
│   ├── __init__.py
│   ├── local_agent.py
│   └── advanced_agent.py
│
├── scrapers/
│   ├── __init__.py
│   └── web_scraper.py
│
└── data/
    ├── raw/
    └── processed/
```

#### Configure environment variables

Create `.env`:

```env
LOCAL_AI_URL=http://localhost:11434
LOCAL_AI_MODEL=llama3.2:1b
```

The localhost address works through the SSH tunnel.

#### Implement the local AI agent

Create `agents/local_agent.py`:

```python
import requests
import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("LOCAL_AI_URL")
MODEL = os.getenv("LOCAL_AI_MODEL")


def ask_local_model(prompt: str) -> str:

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()["message"]["content"]


if __name__ == "__main__":

    result = ask_local_model(
        "Give me three ideas for a Python project."
    )

    print(result)
```

#### Create main.py

```python
from agents.local_agent import ask_local_model

answer = ask_local_model(
    "Explain what an AI agent is in simple terms."
)

print(answer)
```

Run:

```powershell
python main.py
```

#### Add the advanced model

Create `agents/advanced_agent.py`:

```python
def ask_advanced_model(prompt: str) -> str:

    # Connect to a more powerful local model
    # or an external AI provider API.

    pass
```

#### Implement basic model routing

```python
def route_task(task_type, prompt):

    if task_type == "simple_analysis":
        return ask_local_model(prompt)

    if task_type == "complex_reasoning":
        return ask_advanced_model(prompt)

    if task_type == "code_generation":
        return ask_advanced_model(prompt)

    raise ValueError("Unknown task type")
```

Initially, use manually defined task types. Later, implement intelligent routing.

### Phase 6 – Introduce Web Scraping and AI Agents

The application should contain four main responsibilities.

#### 1. Web Scraper

Collect information from websites and APIs.

Recommended libraries:

- Requests
- BeautifulSoup
- Scrapy

#### 2. Data Processor

Clean, normalize and structure information.

Recommended libraries:

- Pandas
- SQLite

#### 3. Local AI Agent

Use the lightweight model for:

- Text classification.
- Entity extraction.
- Initial summarization.
- Metadata generation.
- Simple information extraction.

#### 4. Advanced AI Agent

Use the more powerful model for:

- Comparing information across sources.
- Identifying patterns.
- Generating code.
- Complex reasoning.
- Producing analytical reports.

#### Example workflow

Imagine collecting information about technology companies.

1. Scrape company information from websites.
2. Extract company names, descriptions, products and industries.
3. Send the extracted content to the lightweight local model.
4. Ask the model to categorize companies.
5. Store structured results in SQLite.
6. Send the dataset to the advanced model.
7. Ask the advanced model to identify trends and produce a report.

#### Security considerations

Treat all scraped content as untrusted data.

- Never allow scraped text to execute commands.
- Don't give AI agents unrestricted terminal access.
- Never expose passwords or API keys in prompts.
- Separate information extraction from privileged actions.
- Require human approval before executing generated code or making external changes.
- Respect website terms, robots.txt and applicable privacy rules.

Initially, the local model should only receive text and return text. Add tools progressively.

## 5. Future Improvements

### Agent Orchestration

Introduce LangGraph to coordinate multiple agents and workflows.

https://docs.langchain.com/oss/python/langgraph/overview

### Knowledge Base

Store processed information and introduce semantic search.

Potential technologies:

- ChromaDB
- FAISS
- SQLite
- Embedding models

### Data Analysis

Use the advanced model to analyze collected information and generate reports.

### Automation

Introduce scheduled tasks and background processing once the basic system is stable.

### Monitoring

Consider:

- htop for resource monitoring.
- System logs.
- Ollama model performance.
- CPU and RAM consumption.

## 6. Hardware Considerations

The old computer currently has 8 GB RAM.

| Configuration | Expected usage |
|---|---|
| 8 GB RAM | Small models and experimentation |
| 16 GB RAM | More comfortable local inference |
| 32 GB RAM | More flexibility with larger models |

An SSD is strongly recommended.

Before upgrading, identify processor, motherboard compatibility and available storage.

CPU-only inference is possible, but generation speed may be limited.

## 7. Development Milestones

| Milestone | Deliverable |
|---|---|
| 1 | Linux AI server operational |
| 2 | Ollama and local model operational |
| 3 | Remote SSH connection working |
| 4 | Python application calling the local model |
| 5 | Advanced model integrated |
| 6 | Model routing implemented |
| 7 | Web scraping pipeline operational |
| 8 | Data processing and storage implemented |
| 9 | Multiple AI agents coordinated |
| 10 | Knowledge base and analytical reports |

## 8. Initial Priorities

1. Retrieve hardware specifications.
2. Verify CPU architecture and storage.
3. Check whether RAM can be upgraded to 16 GB.
4. Download Ubuntu Server.
5. Install Linux.
6. Configure SSH and the firewall.
7. Install Ollama.
8. Run Llama 3.2 1B.
9. Connect from the current computer.
10. Build the first Python application.

**Important:** Complete and test each milestone before moving to the next one.

The goal is to build a secure, modular and expandable home AI infrastructure that can eventually support multiple models, specialized agents, web scraping and advanced data analysis.