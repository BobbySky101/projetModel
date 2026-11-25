# AI Server Tunnel Setup Guide

## Overview
This setup creates a secure tunnel between your workstation and the AI server, allowing you to access the Ollama API locally.

## Prerequisites
1. Git installed on your workstation
2. SSH client available (OpenSSH)
3. Network access to ai-server

## Step-by-Step Setup

### Step 1: Connect via SSH Tunnel
Open PowerShell on your workstation and run:

```powershell
ssh -N -L 127.0.0.1:11434:ai-server ollama-user@ai-server
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