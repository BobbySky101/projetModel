# Phase 2 - Initial Server Configuration

**Project:** Home AI Infrastructure

**Status:** Completed

**Completion Date:** 2026-11-24

---

# 1. Objective

The objective of Phase 2 was to transform the freshly installed Ubuntu system into a functional AI server by configuring:

- Operating system updates
- Storage
- Networking
- NVIDIA GPU support
- Firewall security
- Ollama
- Remote AI API access

System inventory and permanent configuration are documented separately:

- hardware.md
- network.md
- storage.md
- security.md
- services.md

---

# 2. Initial System Verification

The newly installed system was inspected to verify that Ubuntu had been installed correctly.

Verification included:

- Ubuntu release
- Kernel version
- Hostname
- Time configuration
- Memory
- Storage
- Networking

---

## Results

| Item | Result |
|--------|--------|
| Ubuntu Version | 26.04.1 LTS |
| Kernel | 7.0.0-44-generic |
| Hostname | ai-server |
| Architecture | x86_64 |
| Time Synchronization | Working |
| NTP | Working |
| SSH Access | Working |

---

# 3. System Updates

The server received all available operating system updates.

Commands executed:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Administration Utilities

The following packages were installed:

```text
curl
wget
git
htop
build-essential
python3
python3-pip
python3-venv
smartmontools
nvme-cli
nftables
```

---

## Outcome

- Package repositories updated.
- System upgraded successfully.
- No update-related issues observed.

---

# 4. Storage Configuration

The additional storage devices were reviewed.

The project owner explicitly approved reusing both drives.

---

## Actions Performed

### WDC SSD

Configured as:

```text
Label: ai-ssd
Filesystem: ext4
Mount Point: /mnt/ai-ssd
```

Purpose:

- AI models
- Applications
- Databases
- Datasets

---

### Seagate HDD

Configured as:

```text
Label: backup
Filesystem: ext4
Mount Point: /mnt/backup
```

Purpose:

- Backups
- Archives
- Historical data

---

## Persistence

Mounts were configured in:

```text
/etc/fstab
```

Verification after reboot succeeded.

---

## Outcome

✅ Storage successfully configured.

---

# 5. Network Configuration

The Ethernet interface was verified.

The server was assigned a reserved address through DHCP.

---

## Results

| Item | Value |
|--------|--------|
| Interface | enp8s0 |
| IPv4 Address | 192.168.0.178 |
| Gateway | 192.168.0.1 |
| Link Speed | 1 Gbps |
| DHCP Reservation | Configured |

---

## IPv6

IPv6 functionality was reviewed.

Results:

- Global IPv6 addresses assigned.
- Default route present.
- External IPv6 connectivity verified.

---

## Outcome

✅ Network configuration validated.

---

# 6. NVIDIA GPU Configuration

The NVIDIA GTX 1070 was prepared for AI inference workloads.

---

## Driver Installation

Installed driver:

```text
NVIDIA 580.178.04
```

Installation method:

```bash
sudo ubuntu-drivers install nvidia:580
```

---

## Verification

Commands:

```bash
nvidia-smi
lspci -k
```

Results:

| Item | Result |
|--------|--------|
| GTX 1070 Detected | Yes |
| Proprietary Driver Loaded | Yes |
| VRAM Available | 8192 MiB |
| NVIDIA Modules Loaded | Yes |
| CUDA Compatibility Reported | 13.0 |

---

## Outcome

✅ GPU available for inference workloads.

---

# 7. Security Configuration

Firewall deployment was completed using nftables.

Detailed policy is maintained in:

```text
security.md
```

---

## Objectives

Permit:

- SSH from development workstation
- Ollama API access from development workstation

Block:

- Unauthorized inbound connections

---

## Validation

Verified:

- Rule syntax
- Rule persistence
- IPv4 connectivity
- IPv6 connectivity
- SSH access
- Unauthorized-device testing

---

## Outcome

✅ Firewall operational.

---

# 8. Ollama Installation

Ollama was installed as the primary inference engine.

Installation:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## Storage Configuration

Model storage relocated to:

```text
/mnt/ai-ssd/ollama
```

---

## Initial Model

Downloaded:

```text
Llama 3.2
```

---

## Local Verification

Inference test completed successfully.

Verified:

- Model loading
- Prompt execution
- Response generation

---

## GPU Verification

GPU acceleration confirmed through monitoring.

Observed using:

```bash
nvidia-smi
```

---

## Outcome

✅ Ollama functioning correctly.

---

# 9. Remote API Configuration

The Ollama API was made available to the development workstation.

Endpoint:

```text
http://192.168.0.178:11434
```

---

## Access Policy

Allowed:

```text
192.168.0.87
```

Blocked:

```text
All other devices
```

---

## Verification

API queries completed successfully from the workstation.

---

## Outcome

✅ Remote inference available.

---

# 10. Problems Encountered

## No Critical Issues

No major installation failures occurred during Phase 2.

Minor configuration adjustments included:

- Timezone correction.
- Driver compatibility verification.
- Firewall validation before activation.

No rollback actions were required.

---

# 11. Deliverables

| Deliverable | Status |
|-------------|---------|
| System Updated | ✅ |
| Utilities Installed | ✅ |
| Storage Configured | ✅ |
| Persistent Mounts Configured | ✅ |
| DHCP Reservation Configured | ✅ |
| NVIDIA Driver Installed | ✅ |
| GPU Operational | ✅ |
| nftables Configured | ✅ |
| Firewall Tested | ✅ |
| Ollama Installed | ✅ |
| Local Inference Tested | ✅ |
| Remote API Tested | ✅ |

---

# 12. Lessons Learned

## GPT Architecture Was Effective

Separating:

- OS disk
- AI storage
- Backup storage

simplified future capacity planning.

---

## DHCP Reservation Is Preferable

Using reservation at the router maintains stable addressing without requiring static IP configuration on Ubuntu.

---

## Firewall Testing Is Critical

Maintaining an active SSH session during testing avoided accidental lockout.

---

## Pascal GPUs Remain Useful

The GTX 1070 remains capable of serving as an inference accelerator for smaller quantized models.

---

# 13. Final Outcome

Phase 2 successfully transformed the Ubuntu installation into an operational local AI server.

The resulting platform provides:

- Updated Ubuntu Server
- Remote management
- Dedicated AI storage
- Dedicated backup storage
- NVIDIA GPU acceleration
- nftables firewall protection
- Ollama local inference
- Remote API access

The server is now ready to support application development and AI automation workloads.

---

# 14. Exit Criteria Verification

| Requirement | Status |
|-------------|---------|
| Ubuntu Verified | ✅ |
| System Updated | ✅ |
| SSH Verified | ✅ |
| Storage Configured | ✅ |
| DHCP Reservation Complete | ✅ |
| NVIDIA Driver Installed | ✅ |
| GPU Verified | ✅ |
| Firewall Operational | ✅ |
| Ollama Installed | ✅ |
| GPU Inference Verified | ✅ |
| Remote API Verified | ✅ |

---

# 15. Next Phase

Proceed to:

```text
Phase 3 - Application Platform Development
```

Primary goals:

- Python project structure
- Virtual environments
- Ollama integration
- Agent architecture
- Model routing
- Logging
- Configuration management
- Future multi-agent support