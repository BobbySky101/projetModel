# Hardware Configuration

**Project:** Home AI Infrastructure  
**System name:** ai-server  
**Last updated:** 2026-11-24

---

# 1. System Overview

| Component | Value |
|----------|---------|
| Hostname | ai-server |
| Purpose | Dedicated local AI inference server |
| Operating System | Ubuntu Server 26.04.1 LTS |
| Architecture | x86_64 |
| Form Factor | Repurposed desktop computer |

---

# 2. Processor

| Parameter | Value |
|------------|---------|
| Model | Intel Core i7-8700 |
| Architecture | x86_64 |
| Physical Cores | 6 |
| Logical Processors | 12 |
| Base Clock | 3.20 GHz |
| Virtualization Support | Intel VT-x |
| IOMMU Support | Intel VT-d |

## Notes

- Virtualization verified as enabled.
- Suitable for Docker, KVM and AI inference workloads.
- Primary AI acceleration is provided by the NVIDIA GPU.

---

# 3. Memory

| Parameter | Value |
|------------|---------|
| Installed RAM | 16 GB |
| Approximate Capacity | 15.95 GiB |
| Swap | 4 GB |

## Notes

- Adequate for lightweight local AI inference.
- Larger models may require CPU offloading.

---

# 4. Graphics Processing Unit

| Parameter | Value |
|------------|---------|
| GPU | NVIDIA GeForce GTX 1070 |
| Architecture | Pascal |
| Compute Capability | 6.1 |
| VRAM | 8 GB |
| Driver Version | 580.178.04 |
| CUDA Compatibility Reported by Driver | 13.0 |
| Secure Boot | Disabled |

## Validation

Verified using:

```bash
nvidia-smi
```

Results:

- GTX 1070 detected
- NVIDIA driver loaded
- 8192 MiB VRAM available
- GPU available for Ollama inference

## Notes

- CUDA Toolkit is not currently installed.
- GPU is intended for inference rather than training.
- Practical target model sizes:
  - 3B models: comfortable
  - 7B models: feasible with quantization
  - Larger models may require CPU offloading

---

# 5. Storage Devices

## 5.1 Kingston SSD

| Parameter | Value |
|------------|---------|
| Role | Operating System |
| Capacity | 240 GB |
| Filesystem | ext4 |
| Mount Point | / |

### Partitions

| Mount Point | Filesystem | Purpose |
|-------------|------------|---------|
| /boot/efi | FAT32 | UEFI boot |
| / | ext4 | Ubuntu filesystem |

---

## 5.2 Western Digital SSD

| Parameter | Value |
|------------|---------|
| Role | AI Storage |
| Capacity | 1 TB |
| Label | ai-ssd |
| Filesystem | ext4 |
| Mount Point | /mnt/ai-ssd |

### Intended Usage

- Ollama models
- Applications
- Databases
- Datasets
- Temporary processing data

---

## 5.3 Seagate HDD

| Parameter | Value |
|------------|---------|
| Role | Backup Storage |
| Capacity | 1 TB |
| Label | backup |
| Filesystem | ext4 |
| Mount Point | /mnt/backup |

### Intended Usage

- System backups
- Application backups
- Archived datasets
- Historical data

---

# 6. Current Storage Layout

```text
/
├── Ubuntu Server
│
├── /mnt/ai-ssd
│   ├── ollama
│   ├── applications
│   ├── databases
│   ├── datasets
│   └── temporary
│
└── /mnt/backup
    ├── system
    ├── applications
    ├── databases
    └── datasets
```

---

# 7. Network Hardware

| Parameter | Value |
|------------|---------|
| Primary Interface | enp8s0 |
| Connection Type | Ethernet |
| Link Speed | 1 Gbps |
| DHCP Reservation | Configured |

## Notes

- Server is intended to operate permanently on Ethernet.
- Wi-Fi is not used for normal operation.

---

# 8. Cooling and Physical Condition

| Item | Status |
|--------|--------|
| CPU Cooling | Operational |
| GPU Cooling | Operational |
| Dust Cleaning | Not yet performed |
| Fan Inspection | Pending |
| Drive Connection Inspection | Pending |

---

# 9. Hardware Capability Summary

| Capability | Status |
|-------------|---------|
| Ubuntu Server | Verified |
| SSH Administration | Verified |
| NVIDIA Acceleration | Verified |
| Ollama GPU Inference | Verified |
| Docker Support | Supported |
| Virtualization Support | Verified |
| AI Workloads | Verified |
| Backup Storage Available | Yes |

---

# 10. Hardware Constraints

- Limited to 16 GB system RAM.
- Limited to 8 GB GPU VRAM.
- GTX 1070 is a Pascal-generation GPU.
- Not suitable for training modern large language models.
- Best suited for local inference and AI utility services.

---

# 11. Upgrade Opportunities

## Medium Priority

- Increase RAM to 32 GB.
- Add larger SSD for model storage.
- Clean cooling system and fans.

## Long-Term

- Replace GTX 1070 with a newer NVIDIA GPU.
- Add dedicated UPS power protection.
- Add automated backup storage.