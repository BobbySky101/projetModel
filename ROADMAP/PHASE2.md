
# Home AI Infrastructure Project

# Phase 2 – Initial Ubuntu Server Configuration

**Project status:** In progress.

---

## 1. Phase 2 Objectives

The objective of Phase 2 is to transform the Ubuntu installation into a properly configured server ready to host local AI workloads.

This phase will focus on:

- Verifying the Ubuntu installation.
- Updating and preparing the operating system.
- Configuring the additional storage drives.
- Establishing reliable network connectivity.
- Preparing NVIDIA GPU support.
- Configuring network security.
- Installing Ollama.
- Testing local AI inference.

Hardware specifications, installation history and initial network architecture are documented in the Phase 1 document.

**Important:** Preserve the existing data on both additional storage drives throughout this phase.

---

## 2. Initial Ubuntu Server Configuration

### 2.1 Verify the Installation

Confirm that Ubuntu is operating correctly.

Check:

- Ubuntu version and release.
- Linux kernel version.
- Hostname.
- System time and timezone.
- Available memory and storage.
- Network interfaces.

Useful commands:

```bash
lsb_release -a
uname -r
hostnamectl
free -h
df -h
ip -br addr
```

### 2.2 Verify Remote Access

Confirm that SSH remains operational.

```bash
sudo systemctl status ssh.socket
```

Test remote access from the development workstation.

Retain the existing SSH socket activation configuration.

### 2.3 Update Ubuntu

Update the operating system and install basic administration utilities.

```bash
sudo apt update
sudo apt upgrade -y
```

Install useful tools:

```bash
sudo apt install -y \
    curl \
    wget \
    git \
    htop \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    smartmontools \
    nvme-cli \
    nftables
```

Reboot if necessary and verify that SSH access still works.

Documentation:

https://documentation.ubuntu.com/server/

---

## 3. Storage Configuration

The objective is to configure the two additional drives for AI applications and backups.

### 3.1 Identify Storage Devices

Identify the three physical drives and their existing partitions.

```bash
lsblk -o NAME,SIZE,MODEL,SERIAL,FSTYPE,MOUNTPOINTS
```

Inspect partition information:

```bash
sudo fdisk -l
sudo blkid
```

### 3.2 Verify Existing Data

Confirm that:

- The WDC SSD is correctly identified.
- The Seagate HDD is correctly identified.
- Existing partitions and filesystems are preserved.
- Existing data is accessible.
- Both drives are in reasonable health.

Do not format either drive without explicitly verifying its contents and intended use.

### 3.3 Configure Mount Points

Proposed storage organization:

| Drive | Mount point | Purpose |
|---|---|---|
| Kingston SSD | `/` | Ubuntu operating system |
| WDC SSD | `/mnt/ai-data` | AI models and application data |
| Seagate HDD | `/mnt/ai-backups` | Backups and archives |

Configure persistent mounts using filesystem UUIDs in `/etc/fstab`.

Verify that both drives mount correctly after reboot.

### 3.4 Organize Storage

Create a basic directory structure:

```text
/mnt/ai-data/
├── ollama/
├── applications/
├── databases/
├── datasets/
└── temporary/

/mnt/ai-backups/
├── system/
├── applications/
├── databases/
└── datasets/
```

---

## 4. Network Configuration

### 4.1 Verify Network Settings

Confirm:

- Ethernet interface.
- MAC address.
- Current IPv4 address.
- IPv6 configuration.
- Default gateway.
- DNS configuration.

The current network architecture and previously identified IP addresses are documented in Phase 1.

### 4.2 Configure DHCP Reservation

Configure a DHCP reservation on the Fizz Hitron CODA-4680 router for the AI server.

Use the verified Ethernet MAC address.

The objective is to maintain a consistent server IP address without manually configuring a static address in Ubuntu.

### 4.3 Verify Local Connectivity

Confirm communication between:

- Development workstation.
- Ubuntu AI server.
- Home router.

Verify that SSH remains accessible after network configuration.

### 4.4 Network Architecture

The intended architecture remains:

```text
              Internet
                  |
             Home Router
                  |
             Local Network
                  |
          +-------+-------+
          |               |
     Development       Ubuntu AI
     Workstation       Server
          |               |
          +-------+-------+
                  |
           Local communication
```

---

## 5. NVIDIA GPU Configuration

The objective is to make the GTX 1070 available for local AI inference.

### 5.1 Verify GPU Detection

Identify the GPU:

```bash
lspci | grep -i nvidia
```

Check available NVIDIA driver packages:

```bash
ubuntu-drivers devices
```

### 5.2 Install a Compatible Driver

Verify compatibility between:

- Ubuntu release.
- Linux kernel.
- NVIDIA driver.
- GTX 1070 Pascal architecture.

The project previously identified NVIDIA driver version 570 or newer as the target requirement for Ollama's Pascal GPU support.

However, confirm package availability and compatibility with the installed Ubuntu release before installation.

### 5.3 Verify GPU Operation

After installing the driver and rebooting:

```bash
nvidia-smi
```

Confirm that:

- The GTX 1070 is detected.
- The driver loads correctly.
- Available VRAM is reported.
- No significant driver errors are present.

Documentation:

https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/

https://docs.ollama.com/gpu

---

## 6. Network Security Configuration

The objective is to restrict unnecessary network access while preserving communication with the development workstation.

### 6.1 Firewall Technology

Use `nftables` as the primary firewall.

The intended configuration should:

- Allow SSH from the development workstation.
- Allow Ollama API access from the development workstation.
- Allow necessary DHCP communication.
- Restrict incoming connections.
- Block outbound internet access from the AI server.
- Account for IPv4 and IPv6.
- Preserve local network communication.

### 6.2 Security Considerations

Before applying firewall rules:

- Verify the actual network interfaces.
- Confirm the trusted local subnet.
- Account for IPv6.
- Preserve SSH access.
- Avoid accidentally blocking required network services.

Test the configuration before making it persistent.

Keep an existing SSH session available during firewall configuration.

### 6.3 Final Network Security Objective

The intended configuration is:

| Communication | Policy |
|---|---|
| Development workstation → AI server | Allowed |
| SSH | Allowed |
| Ollama API | Allowed |
| AI server → Local network | Restricted to necessary communication |
| AI server → Public internet | Blocked |
| Public internet → AI server | Blocked |

Never expose Ollama directly to the public internet.

Documentation:

https://netfilter.org/projects/nftables/

---

## 7. Ollama Installation and Configuration

Once the operating system, GPU and network configuration are verified, install Ollama.

### 7.1 Install Ollama

Official installation:

https://ollama.com/

Installation command:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify:

```bash
ollama --version
```

### 7.2 Configure Model Storage

Configure Ollama to store its models on the WDC SSD rather than the operating system drive.

Proposed location:

```text
/mnt/ai-data/ollama/models
```

Verify that Ollama can access the directory and that model files are stored on the intended drive.

### 7.3 Download the Initial Model

The initial model selected for experimentation is:

**Llama 3.2 3B**

```bash
ollama pull llama3.2
```

If performance or memory becomes an issue, test a smaller model.

### 7.4 Test Local Inference

Run:

```bash
ollama run llama3.2
```

Test with a simple prompt.

Monitor resource consumption:

```bash
htop
```

Also monitor GPU usage:

```bash
nvidia-smi
```

Confirm whether inference uses the GPU as expected.

Documentation:

https://docs.ollama.com/

---

## 8. Ollama API and Remote Access

The objective is to make Ollama accessible from the development workstation.

### 8.1 Local API

Ollama exposes its API on port:

```text
11434
```

Test the local API on the server:

```bash
curl http://localhost:11434/api/tags
```

### 8.2 Remote API Access

Configure Ollama to listen on the intended local network interface.

Restrict access through `nftables` so that only the development workstation can access the API.

Intended endpoint:

```text
http://192.168.0.178:11434
```

The address must be updated if the server receives a different DHCP reservation.

### 8.3 Remote Verification

From the development workstation, test:

```powershell
curl.exe http://192.168.0.178:11434/api/tags
```

Confirm that the model list is returned successfully.

Do not expose port 11434 through router port forwarding.

---

## 9. Phase 2 Completion Criteria

Phase 2 will be considered complete when the following objectives have been achieved.

### Ubuntu Configuration

- [ ] Ubuntu version verified.
- [ ] Hostname verified.
- [ ] System updated.
- [ ] Basic utilities installed.
- [ ] SSH access verified.

### Storage

- [ ] WDC SSD identified.
- [ ] Seagate HDD identified.
- [ ] Existing data verified.
- [ ] Persistent mounts configured.
- [ ] Storage directory structure created.
- [ ] Mounts verified after reboot.

### Network

- [ ] Ethernet configuration verified.
- [ ] DHCP reservation configured.
- [ ] Local connectivity verified.
- [ ] IPv4 configuration verified.
- [ ] IPv6 configuration reviewed.

### NVIDIA

- [ ] GTX 1070 detected.
- [ ] Compatible NVIDIA driver installed.
- [ ] `nvidia-smi` operational.
- [ ] GPU availability verified.

### Security

- [ ] `nftables` configured.
- [ ] SSH access restricted appropriately.
- [ ] Ollama API access restricted appropriately.
- [ ] Outbound internet access blocked.
- [ ] IPv4 and IPv6 restrictions verified.
- [ ] Firewall rules persistent after reboot.
- [ ] Local communication remains functional.

### Ollama

- [ ] Ollama installed.
- [ ] Model storage configured on WDC SSD.
- [ ] Initial model downloaded.
- [ ] Local inference tested.
- [ ] GPU utilization verified.
- [ ] API accessible from development workstation.

---

## 10. Transition to Phase 3

After completing Phase 2, the Ubuntu AI server should be operational as a restricted local AI inference server.

The next phase will focus on developing the Python application on the main development workstation.

Proposed objectives:

1. Create the Python project structure.
2. Configure a virtual environment.
3. Connect Python to the Ollama API.
4. Implement the local AI agent.
5. Integrate a more powerful AI model.
6. Implement basic model routing.
7. Establish application logging and configuration.
8. Prepare the architecture for future AI agents.

The long-term objective remains a distributed AI environment where the Ubuntu server handles lightweight local inference while the development workstation coordinates more complex AI workloads.
