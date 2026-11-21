# Phase 1 – Prepare the Old Computer
## Home AI Infrastructure Project

## 1. Project Objective

Reuse an old Windows 10 computer by installing Linux and transforming it into a dedicated local AI server.

The computer will eventually:

- Host local language models using Ollama.
- Provide an API accessible from the current computer.
- Run lightweight AI tasks such as classification, extraction and summarization.
- Participate in a distributed AI architecture with a more powerful model running on the current computer.
- Support experimentation with Python, AI agents, web scraping and data analysis.

This phase focuses exclusively on hardware assessment, Linux selection and installation preparation.

---

## 2. Hardware Assessment

The old computer has the following specifications.

### Processor

| Parameter | Value |
|---|---|
| Model | Intel Core i7-8700 |
| Architecture | 64-bit |
| Physical cores | 6 |
| Logical processors | 12 |
| Base frequency | 3.20 GHz |

### Memory

| Parameter | Value |
|---|---|
| Installed RAM | Approximately 16 GB |
| Exact reported value | 17,123,528,704 bytes |
| Approximate capacity | 15.95 GiB |

### Graphics Card

| Parameter | Value |
|---|---|
| GPU | NVIDIA GeForce GTX 1070 |
| Architecture | Pascal |
| Compute capability | 6.1 |
| Dedicated VRAM | 8 GB |
| Windows driver | 560.94 |
| CUDA compatibility reported | 12.6 |
| GPU temperature | 35°C |
| GPU utilization | 2% |

The GPU is compatible with Ollama in principle, provided a sufficiently recent NVIDIA driver is installed.

**Important:** Ollama currently requires NVIDIA driver 570 or newer for Pascal GPUs. The existing Windows driver (560.94) is below this requirement.

We will need to install and verify a compatible Linux NVIDIA driver.

### Storage

The computer has three physical drives:

| Drive | Capacity | Type | Intended use |
|---|---:|---|---|
| Kingston SSD | 240 GB | SSD | Ubuntu operating system |
| Western Digital SSD | 1 TB | SSD | AI models and application data |
| Seagate HDD | 1 TB | HDD | Backups and archived datasets |

Total storage: approximately 2.24 TB.

---

## 3. Linux Distribution Selection

Four Linux distributions were considered:

- Ubuntu Server 26.04 LTS
- Ubuntu Server 24.04 LTS
- Debian 13
- Rocky Linux 10

### Comparison

| Criteria | Ubuntu 26.04 | Ubuntu 24.04 | Debian 13 | Rocky Linux 10 |
|---|---|---|---|---|
| Stability | High | Very high | Very high | Very high |
| Resource consumption | Low | Low | Low | Low |
| AI ecosystem | Excellent | Excellent | Excellent | Good |
| Documentation | Excellent | Excellent | Very good | Good |
| Beginner friendliness | Excellent | Excellent | Moderate | Moderate |
| Software freshness | Newer | Older | Conservative | Conservative |
| Server suitability | Excellent | Excellent | Excellent | Excellent |

### Selected Distribution

**Ubuntu Server 26.04.1 LTS**

Official download:

https://ubuntu.com/download/server

Reasons for selecting Ubuntu Server:

1. Excellent compatibility with Python and AI development tools.
2. Extensive Ollama and Docker ecosystem.
3. Large community and documentation.
4. Long-term security maintenance.
5. No graphical desktop environment required.
6. Relatively low resource consumption.
7. Suitable for a home AI server.

Ubuntu 26.04 LTS provides standard security maintenance until May 2031.

Ubuntu 24.04 LTS remains a fallback option if we encounter a specific hardware or NVIDIA driver compatibility issue.

Debian 13 is another good alternative, particularly for a more conservative server environment.

### Why Ubuntu Server instead of Ubuntu Desktop?

The computer will function as a dedicated server.

A graphical desktop environment is unnecessary because administration will happen remotely through SSH and Visual Studio Code Remote SSH.

Ubuntu Server provides:

- Lower background resource consumption.
- More available RAM for AI inference.
- Less CPU overhead.
- A simpler server environment.

---

## 4. AI Hardware Expectations

The combination of an Intel i7-8700, 16 GB RAM and GTX 1070 is suitable for experimenting with local AI models.

The GTX 1070 has 8 GB of VRAM and can accelerate compatible AI inference workloads.

Initial model recommendations:

| Model size | Expected feasibility |
|---|---|
| 1B–2B | Very comfortable |
| 3B | Good starting point |
| 7B–8B quantized | Potentially feasible |
| 13B | Possible with CPU offloading, but potentially slow |
| 30B+ | Not practical |

These are estimates, not performance guarantees.

Actual performance will depend on:

- Model architecture.
- Quantization.
- Context length.
- GPU memory consumption.
- CPU and RAM usage.
- Ollama and NVIDIA driver compatibility.

### Initial AI Model

Start with:

**Llama 3.2 3B**

Ollama command:

```bash
ollama pull llama3.2
```

Test smaller models first if GPU compatibility or memory becomes an issue.

---

## 5. Storage Organization

The recommended storage configuration is:

### Kingston 240 GB SSD

Purpose: Operating system.

Contains:

- Ubuntu Server.
- System files.
- Installed applications.
- Logs and configuration.

### Western Digital 1 TB SSD

Purpose: AI and application storage.

Contains:

- Ollama models.
- Python applications.
- Application databases.
- Processed datasets.
- Temporary processing files.

### Seagate 1 TB HDD

Purpose: Backups and archives.

Contains:

- Application backups.
- Archived datasets.
- Historical scraping results.
- Configuration backups.

### Important Installation Precaution

Before installing Ubuntu:

- Back up important files.
- Identify all three physical drives.
- Disconnect the two 1 TB drives if practical.
- Install Ubuntu only on the 240 GB Kingston SSD.

This reduces the risk of accidentally formatting the wrong drive.

The other two drives will be configured after Ubuntu is operational.

---

## 6. NVIDIA Driver Compatibility

The existing Windows NVIDIA driver is:

```text
560.94
```

The GTX 1070 uses Pascal architecture with CUDA compute capability 6.1.

According to Ollama's NVIDIA requirements, Pascal GPUs require driver version 570 or newer.

Therefore, after installing Ubuntu:

1. Identify the available NVIDIA driver packages.
2. Install a compatible driver version.
3. Reboot the computer.
4. Verify GPU detection using `nvidia-smi`.
5. Install Ollama.
6. Verify that Ollama recognizes the GPU.
7. Test local model inference.

Useful documentation:

- Ollama hardware requirements: https://docs.ollama.com/gpu
- NVIDIA drivers: https://www.nvidia.com/en-us/drivers/
- Ubuntu NVIDIA driver documentation: https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/

**Important:** The CUDA version reported by `nvidia-smi` indicates the CUDA compatibility level of the driver. It does not necessarily mean that the CUDA Toolkit is installed.

---

## 7. Installation Preparation

### Step 1 – Download Ubuntu Server

Official download:

https://ubuntu.com/download/server

Download the 64-bit Server ISO.

Selected version:

Ubuntu Server 26.04.1 LTS.

### Step 2 – Download Rufus

Official website:

https://rufus.ie/

Rufus will be used to create the bootable USB installation drive.

### Step 3 – Prepare the USB Drive

Requirements:

- USB drive with at least 8 GB capacity.
- Windows computer.
- Downloaded Ubuntu Server ISO.

The USB drive will be erased during the process.

### Step 4 – Configure Rufus

Recommended settings, assuming UEFI boot:

| Setting | Value |
|---|---|
| Device | USB drive |
| Boot selection | Ubuntu Server ISO |
| Partition scheme | GPT |
| Target system | UEFI |
| File system | FAT32, if offered |

If the old computer uses legacy BIOS instead of UEFI, these settings may need adjustment.

---

## 8. Planned Ubuntu Installation Configuration

During installation, use the following settings:

| Setting | Recommended value |
|---|---|
| Distribution | Ubuntu Server 26.04.1 LTS |
| Installation disk | Kingston 240 GB SSD |
| Hostname | ai-server |
| Network | Ethernet preferred |
| Installation type | Clean installation |
| SSH server | Enabled |
| Additional packages | None initially |

The two 1 TB drives should remain untouched during the operating system installation.

### Initial Network Configuration

The computer will be connected to the home network using Ethernet if possible.

After installation:

- Identify its local IP address.
- Configure a DHCP reservation on the router.
- Enable SSH.
- Configure a restrictive firewall.
- Access the server remotely from the current computer.

---

## 9. Phase 1 Completion Checklist

### Hardware assessment

- [x] Identify processor.
- [x] Identify RAM capacity.
- [x] Identify graphics card.
- [x] Identify NVIDIA driver version.
- [x] Identify storage devices.
- [x] Confirm 64-bit architecture.

### Linux selection

- [x] Compare Ubuntu and alternative distributions.
- [x] Select Ubuntu Server 26.04.1 LTS.
- [x] Define Ubuntu 24.04 as a fallback option.
- [x] Decide against installing a graphical desktop environment.

### Installation preparation

- [ ] Back up important data.
- [ ] Download Ubuntu Server ISO.
- [ ] Download Rufus.
- [ ] Prepare bootable USB.
- [ ] Verify UEFI/BIOS boot configuration.
- [ ] Disconnect or protect the two 1 TB drives.
- [ ] Boot the installation USB.

---

## 10. Next Steps – Phase 2

After completing the installation preparation, proceed with:

1. Install Ubuntu Server on the Kingston 240 GB SSD.
2. Configure the hostname and user account.
3. Configure networking.
4. Install and configure OpenSSH.
5. Configure the firewall.
6. Connect remotely from the current computer.
7. Update Ubuntu.
8. Configure the two additional storage drives.
9. Install a compatible NVIDIA driver.
10. Verify GTX 1070 detection.

Once the Linux server is operational, proceed to the next phase:

**Install Ollama and run the first local AI model.**

---

## 11. Reference Documentation

| Resource | URL |
|---|---|
| Ubuntu Server downloads | https://ubuntu.com/download/server |
| Ubuntu Server documentation | https://documentation.ubuntu.com/server/ |
| Ubuntu NVIDIA drivers | https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/ |
| NVIDIA driver downloads | https://www.nvidia.com/en-us/drivers/ |
| Ollama | https://ollama.com/ |
| Ollama documentation | https://docs.ollama.com/ |
| Rufus | https://rufus.ie/ |
| VS Code Remote SSH | https://code.visualstudio.com/docs/remote/ssh |

---

**Project:** Home AI Infrastructure

**Current phase:** Phase 1 – Prepare the Old Computer

**Selected operating system:** Ubuntu Server 26.04.1 LTS

**Hardware:** Intel i7-8700 / 16 GB RAM / NVIDIA GTX 1070 / 2.24 TB storage

**Next objective:** Prepare the bootable USB and install Ubuntu Server safely.