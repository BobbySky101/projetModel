
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
timedatectl
```

**Results:**

- Ubuntu 26.04.1 LTS (Resolute).
- Kernel: 7.0.0-44-generic.
- Hostname: `ai-server`.
- Architecture: x86-64.
- RAM: 16 GB.
- System drive: Kingston 240 GB SSD.
- Timezone corrected from UTC to Eastern Time.
- System clock synchronized using NTP.
- Ethernet interface: `enp8s0`.

### 2.2 Verify Remote Access

Confirm that SSH remains operational.

```bash
sudo systemctl status ssh.socket
```

Test remote access from the development workstation.

Retain the existing SSH socket activation configuration.

**Results:** SSH works.

SSH socket is enabled and listening on port 22.

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

**Results:**

- Ubuntu updated successfully.
- Basic administration utilities were addressed.
- No reboot was initially required after updates.

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

### 3.2 Verify and Prepare Storage

The contents of both additional drives were reviewed.

The user explicitly approved permanently erasing both drives.

Both drives were repartitioned and formatted using ext4.

Current storage configuration:

| Drive | Filesystem | Label | Purpose |
|---|---|---|---|
| Kingston SSD | ext4 | - | Ubuntu operating system |
| WDC SSD | ext4 | ai-ssd | AI models and application data |
| Seagate HDD | ext4 | backup | Backups and archives |

### 3.3 Configure Mount Points

Current storage organization:

| Drive | Mount point | Purpose |
|---|---|---|
| Kingston SSD | `/` | Ubuntu operating system |
| WDC SSD | `/mnt/ai-ssd` | AI models and application data |
| Seagate HDD | `/mnt/backup` | Backups and archives |

Persistent mounts are configured using filesystem UUIDs in `/etc/fstab`.

Current entries:

```fstab
UUID=3e08dcda-25fa-44ce-92d7-f94394f2e97c /mnt/ai-ssd ext4 defaults,nofail 0 2
UUID=56bdda1b-966e-417d-8c44-4f839e043152 /mnt/backup ext4 defaults,nofail 0 2
```

Verify mounts using:

```bash
findmnt /mnt/ai-ssd
findmnt /mnt/backup
```

Both mounts were successfully verified after reboot.

### 3.4 Organize Storage

Proposed directory structure:

```text
/mnt/ai-ssd/
├── ollama/
├── applications/
├── databases/
├── datasets/
└── temporary/

/mnt/backup/
├── system/
├── applications/
├── databases/
└── datasets/
```

Directory organization remains to be completed.

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

Current configuration:

- Interface: `enp8s0`.
- IPv4 address: `192.168.0.178`.
- Gateway: `192.168.0.1`.
- Ethernet speed: 1 Gbps.
- DNS: Router-provided DNS servers.

### 4.2 Configure DHCP Reservation

Configure a DHCP reservation on the Fizz Hitron CODA-4680 router for the AI server.

Use the verified Ethernet MAC address.

**Results:** DHCP reservation completed.

The server retains its reserved IPv4 address.

### 4.3 Verify Local Connectivity

Confirm communication between:

- Development workstation.
- Ubuntu AI server.
- Home router.

Verify that SSH remains accessible after network configuration.

### 4.4 IPv6 Configuration

IPv6 is currently enabled and automatically configured through router advertisements and DHCPv6.

Verification commands:

```bash
ip -6 addr show enp8s0
ip -6 route
ping -6 -c 4 google.com
```

**Results:**

- Global IPv6 addresses assigned.
- IPv6 default route available.
- External IPv6 connectivity successfully tested.

No static IPv6 configuration is currently required.

### 4.5 Network Architecture

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

**Results:**

- GPU: NVIDIA GeForce GTX 1070.
- Architecture: Pascal.
- Compute capability: 6.1.
- VRAM: 8 GB.

### 5.2 Install a Compatible Driver

Verify compatibility between:

- Ubuntu release.
- Linux kernel.
- NVIDIA driver.
- GTX 1070 Pascal architecture.

The project identified NVIDIA driver version 570 or newer as the target requirement for Ollama's Pascal GPU support.

Installed driver:

**NVIDIA 580.178.04**

Secure Boot is disabled.

Installation was performed using:

```bash
sudo apt update
sudo ubuntu-drivers install nvidia:580
```

### 5.3 Verify GPU Operation

After installing the driver and rebooting:

```bash
nvidia-smi
lspci -k -s 01:00.0
lsmod | grep nvidia
```

**Results:**

- GTX 1070 detected successfully.
- Proprietary NVIDIA driver loaded.
- Kernel driver in use: `nvidia`.
- NVIDIA kernel modules loaded.
- VRAM detected: 8192 MiB.
- GPU temperature at idle: approximately 36°C.
- Driver version: 580.178.04.
- Driver reports CUDA 13.0 compatibility.

Note: CUDA Toolkit is not yet installed. The CUDA version reported by `nvidia-smi` does not mean the CUDA Toolkit is installed.

### 5.4 Hardware Specifications Summary

The following hardware has been verified:

| Component | Specification |
|---|---|
| CPU | Intel Core i7-8700 @ 3.20 GHz |
| Architecture | x86_64 |
| Physical cores | 6 |
| Threads | 12 |
| RAM | 16 GB |
| Swap | 4 GB |
| GPU | NVIDIA GeForce GTX 1070 |
| GPU VRAM | 8 GB |

The server will primarily use the NVIDIA GPU for local LLM inference.

Model selection should take available VRAM and system memory into consideration.

### 5.5 GPU Inference Preparation

The primary objective is local LLM inference, not model training.

Important hardware constraints:

- Pascal architecture (compute capability 6.1).
- 8 GB VRAM.
- 16 GB system RAM.

Start with quantized 3B–4B models and evaluate 7B–8B models using 4-bit quantization.

Some models may require CPU offloading.

Ollama is the planned inference engine.

Documentation:

https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/

https://docs.ollama.com/gpu

https://developer.nvidia.com/cuda-gpus

---

## 6. Network Security Configuration

The objective is to protect the Ubuntu AI server while allowing controlled communication with the development workstation.

The development workstation will act as the primary interface between users (including the phone in the future) and the Ubuntu AI server.

The phone will not communicate directly with the Ubuntu server.

### 6.1 Firewall Configuration

Use `nftables` as the primary firewall.

The intended configuration should:

- Allow SSH connections from the development workstation.
- Allow Ollama API access from the development workstation.
- Block incoming connections from other devices.
- Allow necessary outbound internet connections.
- Allow established and related connections.
- Account for both IPv4 and IPv6.
- Preserve necessary network services such as DHCP and DNS.

### 6.2 Network Access Policy

| Communication | Policy |
|---|---|
| Development workstation → SSH (port 22) | Allowed |
| Development workstation → Ollama API (port 11434) | Allowed |
| Phone → Ubuntu server | Blocked |
| Other home devices → Ubuntu server | Blocked |
| Ubuntu server → Internet | Allowed |
| Established connections | Allowed |
| Other unsolicited incoming connections | Blocked |

The development workstation will be responsible for handling future phone access and forwarding requests to the AI server when necessary.

### 6.3 Security Considerations

Before applying firewall rules:

- Verify the development workstation's IP address.
- Verify the AI server's reserved IP address.
- Confirm the trusted local subnet.
- Account for IPv4 and IPv6.
- Preserve SSH access during configuration.
- Avoid blocking necessary outbound connections.

Keep an existing SSH session available while testing firewall changes.

Do not expose SSH or the Ollama API through router port forwarding.

### 6.4 Firewall Verification

After configuration, verify that:

- SSH remains accessible from the development workstation.
- Ollama API access works from the development workstation.
- Other devices cannot access the server's SSH or Ollama API.
- IPv4 and IPv6 restrictions work as expected.
- Outbound internet access remains functional.
- Firewall rules persist after reboot.

### 6.5 Documentation

https://documentation.ubuntu.com/server/how-to/security/firewalls/

https://netfilter.org/projects/nftables/

https://docs.ollama.com/

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
/mnt/ai-ssd/ollama/models
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

- [x] Ubuntu version verified.
- [x] Hostname verified.
- [x] System updated.
- [x] Basic utilities addressed.
- [x] SSH access verified.
- [x] Timezone configured.

### Storage

- [x] WDC SSD identified.
- [x] Seagate HDD identified.
- [x] Existing data reviewed and deletion explicitly approved.
- [x] Both drives reformatted as ext4.
- [x] Persistent mounts configured.
- [x] Mounts verified after reboot.
- [x] Storage directory structure created.

### Network

- [x] Ethernet configuration verified.
- [x] DHCP reservation configured.
- [x] Local connectivity verified.
- [x] IPv4 configuration verified.
- [x] IPv6 configuration reviewed.
- [x] IPv6 external connectivity tested.

### NVIDIA

- [x] GTX 1070 detected.
- [x] NVIDIA 580 driver installed.
- [x] `nvidia-smi` operational.
- [x] NVIDIA kernel modules loaded.
- [ ] GPU inference verified using Ollama.

### Security

### Security

- [x] nftables installed.
- [x] Existing configuration backed up.
- [x] Firewall rules configured.
- [x] Configuration syntax validated.
- [x] SSH access restricted to development workstation.
- [x] Ollama API access restricted to development workstation.
- [x] Default incoming policy set to DROP.
- [x] Default forwarding policy set to DROP.
- [x] Outgoing connections permitted.
- [x] IPv4 connectivity verified.
- [x] IPv6 connectivity verified.
- [x] Firewall enabled at startup.
- [x] SSH access verified after firewall activation.
- [x] Unauthorized device access tested.
- [x] Firewall persistence verified after reboot.

### Ollama

- [x] Ollama installed.
- [x] Model storage configured on WDC SSD.
- [x] Initial model downloaded.
- [x] Local inference tested.
- [x] GPU utilization verified.
- [x] API accessible from development workstation.

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
