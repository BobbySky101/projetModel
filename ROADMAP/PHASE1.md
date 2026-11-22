# Phase 1 – Prepare the Old Computer
## Home AI Infrastructure Project

## 1. Project Objective

Reuse an old Windows 10 computer by installing Linux and transforming it into a dedicated local AI server.

The computer will eventually:

- Host local language models using Ollama.
- Provide an API accessible from the current computer.
- Run lightweight AI tasks such as classification, extraction, and summarization.
- Participate in a distributed AI architecture with a more powerful model running on the current computer.
- Support experimentation with Python, AI agents, web scraping, and data analysis.

This phase focuses on:

- Hardware assessment.
- Linux distribution selection.
- AI hardware feasibility.
- Storage organization.
- Network architecture and security planning.
- Windows pre-installation checks.
- Ubuntu installation preparation.

---

## 2. Hardware Assessment

The old computer has the following specifications.

### 2.1 Processor

| Parameter | Value |
|---|---|
| Model | Intel Core i7-8700 |
| Architecture | 64-bit |
| Physical cores | 6 |
| Logical processors | 12 |
| Base frequency | 3.20 GHz |

### 2.2 Memory

| Parameter | Value |
|---|---|
| Installed RAM | Approximately 16 GB |
| Exact reported value | 17,123,528,704 bytes |
| Approximate capacity | 15.95 GiB |

### 2.3 Graphics Card

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

The GTX 1070 is compatible with Ollama in principle, provided a sufficiently recent NVIDIA driver is installed.

**Important:** Ollama's NVIDIA requirements indicate that Pascal GPUs require driver version 570 or newer. The existing Windows driver (560.94) is below this requirement.

A compatible Linux NVIDIA driver must be installed and verified after Ubuntu installation.

I updated the driver to 582.78

### 2.4 Storage

The computer has three physical drives:

| Drive | Capacity | Type | Intended use |
|---|---:|---|---|
| Kingston SSD | 240 GB | SSD | Ubuntu operating system |
| Western Digital SSD | 1 TB | SSD | AI models and application data |
| Seagate HDD | 1 TB | HDD | Backups and archived datasets |

**Total storage:** Approximately 2.24 TB.

---

## 3. Linux Distribution Selection

Four Linux distributions were considered:

- Ubuntu Server 26.04 LTS.
- Ubuntu Server 24.04 LTS.
- Debian 13.
- Rocky Linux 10.

### 3.1 Distribution Comparison

| Criteria | Ubuntu 26.04 | Ubuntu 24.04 | Debian 13 | Rocky Linux 10 |
|---|---|---|---|---|
| Stability | High | Very high | Very high | Very high |
| Resource consumption | Low | Low | Low | Low |
| AI ecosystem | Excellent | Excellent | Excellent | Good |
| Documentation | Excellent | Excellent | Very good | Good |
| Beginner friendliness | Excellent | Excellent | Moderate | Moderate |
| Software freshness | Newer | Older | Conservative | Conservative |
| Server suitability | Excellent | Excellent | Excellent | Excellent |

### 3.2 Selected Distribution

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

Ubuntu 24.04 LTS remains a fallback option if a specific hardware or NVIDIA driver compatibility issue occurs.

Debian 13 is another good alternative, particularly for a more conservative server environment.

**Release verification:** Confirm the availability of the selected Ubuntu release and its maintenance dates before downloading the installation ISO.

### 3.3 Why Ubuntu Server Instead of Ubuntu Desktop?

The computer will function as a dedicated server.

A graphical desktop environment is unnecessary because administration will happen remotely through SSH and Visual Studio Code Remote SSH.

Ubuntu Server provides:

- Lower background resource consumption.
- More available RAM for AI inference.
- Less CPU overhead.
- A simpler server environment.

---

## 4. AI Hardware Expectations

The combination of an Intel i7-8700, 16 GB RAM, and GTX 1070 is suitable for experimenting with local AI models.

The GTX 1070 has 8 GB of VRAM and can accelerate compatible AI inference workloads.

### 4.1 Expected Model Feasibility

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

### 4.2 Initial AI Model

Start with:

**Llama 3.2 3B**

Ollama command:

```bash
ollama pull llama3.2
```

Test smaller models first if GPU compatibility or memory becomes an issue.

---

## 5. Storage Organization

The three physical drives will have separate responsibilities.

### 5.1 Kingston 240 GB SSD

**Purpose:** Operating system.

Contains:

- Ubuntu Server.
- System files.
- Installed applications.
- Logs and configuration.

### 5.2 Western Digital 1 TB SSD

**Purpose:** AI and application storage.

Contains:

- Ollama models.
- Python applications.
- Application databases.
- Processed datasets.
- Temporary processing files.

### 5.3 Seagate 1 TB HDD

**Purpose:** Backups and archives.

Contains:

- Application backups.
- Archived datasets.
- Historical scraping results.
- Configuration backups.

### 5.4 Installation Precaution

Before installing Ubuntu:

- Back up important files.
- Identify all three physical drives.
- Disconnect the two 1 TB drives if practical.
- Install Ubuntu only on the 240 GB Kingston SSD.

This reduces the risk of accidentally formatting the wrong drive.

The other two drives will be configured after Ubuntu is operational.

## 6. Network Architecture and Security

### 6.1 Project Requirements

The old computer will become a dedicated AI server.

The objectives are to:

- Allow the current computer to communicate with the old computer.
- Allow SSH connections from the current computer.
- Allow API requests to Ollama from the current computer.
- Prevent the old computer from accessing the public internet by default.
- Prevent external internet connections from reaching the AI server.

Both computers will remain connected to the same home network.

### 6.2 Existing Network Infrastructure

The home network uses a:

**Fizz Hitron CODA-4680 modem/router.**

The current computer and old computer will connect to the same local network.

Ethernet is recommended for the AI server because it provides a more stable connection than Wi-Fi.

### 6.3 Intended Network Architecture

```text
Current computer
(Development workstation)
       |
       | Internet access allowed
       |
Fizz Hitron CODA-4680
       |
       | Local network
       |
Ubuntu AI server
       |
       | Local communication allowed
       |
       X
    Internet blocked
```

### 6.4 Proposed Network Configuration

The following addresses are examples only. Actual addresses and the subnet must be verified before configuring the firewall.

| Device | Example IP |
|---|---|
| Fizz router | 192.168.0.1 |
| Current computer | 192.168.0.100 |
| AI server | 192.168.0.120 |

Proposed server hostname:

`ai-server`

A DHCP reservation for the AI server is recommended.

This will provide a consistent local IP address without requiring a manually configured static IP during initial installation.

### 6.5 Ethernet Connectivity Verification

Before installing Ubuntu, verify the following in Windows:

1. Connect the old computer to the router using Ethernet.
2. Open Network Connections using `ncpa.cpl`.
3. Verify that the Ethernet adapter is enabled and connected.
4. Run `ipconfig` in PowerShell.
5. Identify the IPv4 address, subnet mask, and default gateway.
6. Test communication with the router using `ping`.
7. Test external connectivity using `ping 1.1.1.1`.
8. Test DNS resolution using `nslookup ubuntu.com`.

Identify the Ethernet adapter:

```powershell
Get-NetAdapter |
    Format-Table Name, InterfaceDescription, Status, LinkSpeed
```

Record the Ethernet adapter model to verify Linux driver compatibility.

### 6.6 Fizz Hitron CODA-4680 Router Investigation

The available router security features were investigated.

#### A. Device Filter

Available options:

- Allow All.
- Allow Listed.
- Block Listed.
- Managed Devices.
- Scheduled access restrictions.

**Decision:** Do not use Device Filter for the AI server.

It may block access to the local network as well as internet access.

#### B. Firewall

Available security levels:

- Minimum Security (Low).
- Typical Security (Medium).
- Maximum Security (High).
- Custom Security.

Important observations:

- Minimum allows all LAN-to-WAN traffic.
- Typical blocks selected peer-to-peer applications.
- Maximum allows a predefined set of outgoing services, including HTTP, HTTPS, and DNS.
- Custom provides additional firewall controls.

**Decision:** Do not change the global firewall level to isolate the AI server.

Maximum Security does not guarantee that the server cannot access the internet, and router-wide changes could affect other household devices.

#### C. Port Blocking

The CODA-4680 offers:

- Managed Services.
- Protocol selection.
- Port ranges.
- Scheduled restrictions.
- Trusted PC List.

The documentation indicates that Port Blocking can restrict specified outbound traffic from computers on the internal network.

However, it is designed around selected ports and services, not a straightforward per-device rule blocking all internet access.

**Decision:** Do not rely on Port Blocking as the primary internet isolation mechanism.

#### D. Other Router Settings

The following tabs were identified:

- Firewall.
- IPv6 Inbound.
- Port Blocking.
- VPN Passthrough.

No router configuration changes have been made.

### 6.7 Final Router Decision

Keep the Fizz router in its normal configuration.

Implement the primary outbound internet restrictions directly on Ubuntu using `nftables`.

For stronger isolation in the future, consider a dedicated network firewall/router.

### 6.8 Ubuntu Network Security Configuration

The proposed Linux firewall is `nftables`.

Its objectives are to:

- Allow DHCP when necessary.
- Allow necessary local network communication.
- Allow SSH from the current computer.
- Allow Ollama API access from the current computer.
- Block outbound IPv4 internet connections.
- Block outbound IPv6 internet connections.
- Restrict incoming connections.
- Make firewall rules persistent across reboots.

**Important security considerations:**

- The firewall must distinguish between trusted local network traffic and external internet traffic.
- IPv6 must be considered in addition to IPv4.
- Additional network interfaces must be considered.
- DNS and DHCP requirements must be accounted for.
- Firewall rules must not accidentally prevent SSH administration.
- Local communication must remain functional after internet restrictions are applied.

Do not apply firewall rules until the actual IP addresses and network subnet are known.

Test SSH and Ollama connectivity after configuring the firewall.

Host-level firewall restrictions provide useful protection but are not equivalent to a separate network firewall. A process with administrator privileges could potentially modify the rules.

---

## 7. Remote Access Architecture

The current computer will be used to administer and communicate with the Ubuntu AI server.

### 7.1 SSH

Example connection:

```bash
ssh your_username@192.168.0.120
```

SSH will be restricted to the current computer or trusted local network.

SSH key authentication is recommended.

Remote administration will eventually be performed through:

- SSH.
- Visual Studio Code Remote SSH.

### 7.2 Ollama API

The intended local API endpoint is:

```text
http://192.168.0.120:11434
```

Ollama should listen on the LAN interface, with firewall access restricted to the current computer.

Never expose Ollama directly to the public internet.

---

## 8. Windows Pre-Installation Checks

Before replacing Windows 10 with Ubuntu Server, collect the necessary system information.

These checks help prevent:

- Accidental data loss.
- Hardware compatibility issues.
- Network connectivity problems.
- BIOS/UEFI configuration problems.
- Loss of software licenses or credentials.

### 8.1 Record Windows Activation

Open PowerShell as Administrator.

Execute:

```powershell
slmgr /xpr
```

This tells you whether Windows is permanently activated.

**Recorded result:**

Windows(R), Core edition: The Machine is permanently activated.

This information may be useful if Windows ever needs to be reinstalled.

### 8.2 Record BIOS/UEFI Configuration

Execute:

```powershell
msinfo32
```

Look for:

- BIOS Mode: UEFI or Legacy.
- BIOS Version/Date.
- Secure Boot State.

**Recorded result:** Screenshot taken.

This information will help configure the Ubuntu installation USB correctly.

### 8.3 Record Network Configuration

Execute:

```powershell
ipconfig /all
```

Record:

- Ethernet adapter model.
- Wi-Fi adapter model.
- MAC address.
- Current IP configuration.

**Recorded result:** Screenshot taken.

This information is useful if network driver issues occur with Ubuntu.

### 8.4 Check Disk Configuration

Open PowerShell:

```powershell
Get-Disk |
    Format-Table Number, FriendlyName, PartitionStyle, OperationalStatus, Size
```

Then:

```powershell
Get-Partition |
    Format-Table DiskNumber, PartitionNumber, DriveLetter, Type, Size
```

Identify:

- Which physical disk contains Windows.
- Which disks contain personal data.
- Whether any disks use BitLocker.
- Whether disks use GPT or MBR partitioning.

**Recorded result:** Screenshot taken.

### 8.5 Check BitLocker

Execute:

```powershell
manage-bde -status
```

If any drive is encrypted, make sure you have its recovery key before changing the system.

**Recorded result:** Screenshot taken.

### 8.6 Final Windows Information Collection

The following commands can be used to retrieve the important information again before installation:

```powershell
# 1. BIOS and Secure Boot
Get-ComputerInfo |
    Select-Object BiosFirmwareType, BiosVersion

# 2. Secure Boot status
Confirm-SecureBootUEFI

# 3. Disk layout
Get-Disk |
    Format-Table Number, FriendlyName, PartitionStyle, Size

# 4. BitLocker
manage-bde -status

# 5. Ethernet adapter
Get-NetAdapter |
    Format-Table Name, InterfaceDescription, Status, LinkSpeed

# 6. Processor virtualization capabilities
Get-CimInstance Win32_Processor |
    Select-Object Name,
                  VirtualizationFirmwareEnabled,
                  VMMonitorModeExtensions,
                  SecondLevelAddressTranslationExtensions
```

Send these results for review before proceeding.

The objective is to determine the safest installation configuration, particularly regarding:

- UEFI.
- Secure Boot.
- Disk partitioning.
- BitLocker.
- Ethernet compatibility.
- Virtualization.
- Storage drive selection.

---

## 9. BIOS and Virtualization Configuration

The Intel Core i7-8700 supports:

- Intel VT-x.
- Intel VT-d.

These technologies are useful for future experimentation with:

- Virtual machines.
- KVM/QEMU.
- Hardware passthrough.
- Isolated development environments.

They are not required for Ollama or Docker containers running directly on Linux.

### 9.1 BIOS Settings

Restart the computer and enter BIOS/UEFI, usually by pressing DEL or F2 during startup.

Check the following settings:

| Setting | Recommendation |
|---|---|
| Boot mode | UEFI |
| SATA mode | AHCI, if already configured that way |
| Secure Boot | Keep enabled initially if supported |
| Intel Virtualization Technology (VT-x) | Enabled |
| Intel VT-d | Enabled if available |
| Primary graphics | PCIe / PEG |
| Wake on LAN | Optional |

**Important:** Do not change SATA mode blindly.

Switching between RAID/RST and AHCI can cause Windows boot problems. Evaluate the existing configuration first.

Also, do not update the BIOS just for the sake of updating it. A BIOS update has some risk and is not necessary if the machine is working correctly.

### 9.2 Verify Virtualization in Windows

Open Task Manager:

1. Press Ctrl + Shift + Esc.
2. Select Performance.
3. Select CPU.
4. Look for Virtualization.

Expected result:

`Virtualization: Enabled`

Alternatively, run:

```powershell
Get-CimInstance Win32_Processor |
    Select-Object Name,
                  VirtualizationFirmwareEnabled,
                  VMMonitorModeExtensions,
                  SecondLevelAddressTranslationExtensions
```

If VT-x is disabled, enable Intel Virtualization Technology in BIOS/UEFI.

Enable Intel VT-d if available.

Do not change unrelated BIOS settings.

**Status:** Virtualization is Enabled

---

## 10. Software, Licenses, and Credentials

Before removing Windows, check whether you have:

- Paid software requiring license deactivation.
- Password managers or browser profiles.
- SSH keys.
- Git credentials.
- VPN configurations.
- Important certificates.
- Wi-Fi passwords.

For the future AI project, particularly preserve SSH keys and Git configuration if already available.

Back up important files before proceeding with the installation.

---

## 11. Physical Computer Preparation

A little maintenance is worthwhile before turning the computer into a server.

Recommended actions:

- Remove accumulated dust from the case.
- Check that CPU and GPU fans rotate freely.
- Check that the three storage drives are securely connected.
- Verify that the Ethernet port works.
- Check that the computer has adequate ventilation.

The GTX 1070 is an older graphics card, so checking its cooling system is worthwhile.

Do not disassemble the GPU unless you are comfortable doing so.
```

## 12. Ubuntu Installation Media Preparation

### 12.1 Download Ubuntu Server

Official download:

https://ubuntu.com/download/server

Download the 64-bit Server ISO.

Selected version:

Ubuntu Server 26.04.1 LTS.

### 12.2 Download Rufus

Official website:

https://rufus.ie/

Rufus will be used to create the bootable USB installation drive.

### 12.3 Prepare the USB Drive

A new USB drive will be purchased.

Requirements:

- USB drive with at least 8 GB capacity.
- Windows computer.
- Downloaded Ubuntu Server ISO.

Recommendation:

- 16 GB USB drive.
- USB 3.0 or newer.
- Reputable manufacturer.

Suggested manufacturers:

- SanDisk.
- Kingston.
- Samsung.

The USB drive will be erased during the process.

### 12.4 Configure Rufus

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

## 13. Planned Ubuntu Installation Configuration

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

### 13.1 Initial Network Configuration

The computer will be connected to the home network using Ethernet if possible.

After installation:

- Identify its local IP address.
- Configure a DHCP reservation on the router.
- Enable SSH.
- Configure a restrictive firewall.
- Access the server remotely from the current computer.

### 13.2 Installation Precautions

Before installing Ubuntu:

1. Back up important files.
2. Record Windows activation information.
3. Record BIOS/UEFI settings.
4. Check BitLocker status.
5. Identify the three physical drives.
6. Verify Ethernet connectivity.
7. Verify virtualization settings.
8. Download the Ubuntu ISO.
9. Create the bootable USB.
10. Disconnect the two 1 TB drives if practical.

Install Ubuntu only on the Kingston 240 GB SSD.

Do not erase Windows until you have successfully booted the Ubuntu USB and confirmed that the installer detects:

- Your network adapter.
- Your Kingston SSD.
- Your graphics card.

This is a useful final compatibility check before committing to the migration.

---

## 14. NVIDIA Driver Compatibility and Verification

The existing Windows NVIDIA driver is:

    560.94

The GTX 1070 uses Pascal architecture with CUDA compute capability 6.1.

According to Ollama's NVIDIA requirements, Pascal GPUs require driver version 570 or newer.

Therefore, after installing Ubuntu:

1. Identify the available NVIDIA driver packages.
2. Verify compatibility with the selected Ubuntu release.
3. Install a compatible driver version.
4. Reboot the computer.
5. Verify GPU detection using `nvidia-smi`.
6. Install Ollama.
7. Verify that Ollama recognizes the GPU.
8. Test local model inference.

**Important:** The CUDA version reported by `nvidia-smi` indicates the CUDA compatibility level of the driver. It does not necessarily mean that the CUDA Toolkit is installed.

Useful documentation:

- Ollama hardware requirements: https://docs.ollama.com/gpu
- NVIDIA drivers: https://www.nvidia.com/en-us/drivers/
- Ubuntu NVIDIA driver documentation: https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/

---

## 15. Consolidated Project Decisions

The following decisions have already been made.

### 15.1 Hardware and Operating System

| Topic | Decision |
|---|---|
| Processor | Intel Core i7-8700 |
| RAM | 16 GB |
| GPU | NVIDIA GTX 1070 |
| GPU VRAM | 8 GB |
| Operating system | Ubuntu Server 26.04.1 LTS |
| Fallback OS | Ubuntu Server 24.04 LTS |
| Desktop environment | No graphical desktop |
| NVIDIA driver target | Version 570 or newer, subject to Ubuntu compatibility verification |

### 15.2 Storage

| Topic | Decision |
|---|---|
| Installation disk | Kingston 240 GB SSD |
| AI storage | Western Digital 1 TB SSD |
| Backup storage | Seagate 1 TB HDD |
| Installation precaution | Disconnect the two 1 TB drives if practical |

### 15.3 Network and Security

| Topic | Decision |
|---|---|
| Network | Ethernet |
| Router | Fizz Hitron CODA-4680 |
| Network architecture | Both computers on the same LAN |
| Server hostname | ai-server |
| Internet restriction | Ubuntu nftables firewall |
| Remote administration | SSH |
| Ollama API | Local network access only |

Additional security decisions:

- Keep the Fizz router in its normal configuration.
- Do not use router Device Filter to isolate the AI server.
- Do not change the global router firewall level.
- Do not rely on router Port Blocking as the primary isolation mechanism.
- Implement outbound internet restrictions using Ubuntu `nftables`.
- Allow local SSH and Ollama API communication from the current computer.
- Account for IPv4 and IPv6.
- Never expose Ollama directly to the public internet.

### 15.4 AI Software

| Topic | Decision |
|---|---|
| AI runtime | Ollama |
| Initial model | Llama 3.2 3B |
| Model storage | Western Digital 1 TB SSD |
| Remote API access | Current computer over LAN |

---

## 16. Consolidated Project Checklist

### 16.1 Hardware Assessment

- [x] Identify processor.
- [x] Identify RAM capacity.
- [x] Identify graphics card.
- [x] Identify NVIDIA driver version.
- [x] Identify storage devices.
- [x] Confirm 64-bit architecture.

### 16.2 Linux Selection

- [x] Compare Ubuntu and alternative distributions.
- [x] Select Ubuntu Server 26.04.1 LTS.
- [x] Define Ubuntu 24.04 as a fallback option.
- [x] Decide against installing a graphical desktop environment.

### 16.3 Windows Preparation

- [x] Check Windows activation.
- [x] Record BIOS mode and Secure Boot status.
- [x] Record BIOS version.
- [x] Record Ethernet and Wi-Fi adapters.
- [x] Check disk partition layout.
- [x] Check BitLocker status.
- [x] Verify BitLocker recovery keys if applicable.
- [x] Save SSH keys, credentials, and software licenses.

### 16.4 Hardware Preparation

- [skipped] Clean the computer and check fans.
- [skipped] Check SSD and HDD connections.
- [x] Verify Ethernet connectivity.
- [x] Verify Intel VT-x status.
- [x] Verify Intel VT-d availability.
- [x] Confirm BIOS configuration.

### 16.5 Network Preparation

- [ ] Identify current computer IPv4 address.
- [ ] Identify subnet mask.
- [ ] Identify default gateway.
- [ ] Identify actual LAN subnet.
- [ ] Record Ethernet adapter model.
- [ ] Decide on AI server IP address.
- [ ] Prepare DHCP reservation.

### 16.6 Installation Preparation

- [ ] Back up important data.
- [ ] Confirm the selected Ubuntu release is available.
- [ ] Download Ubuntu Server ISO.
- [ ] Purchase a 16 GB USB drive.
- [ ] Download Rufus.
- [ ] Create bootable USB.
- [ ] Verify UEFI/BIOS boot configuration.
- [ ] Identify the Kingston 240 GB SSD.
- [ ] Disconnect or protect the two 1 TB drives.
- [ ] Connect monitor, keyboard, and Ethernet.
- [ ] Boot Ubuntu USB.
- [ ] Verify hardware detection.

---

## 17. Next Steps – Phase 2

After completing Phase 1, proceed with the following installation and configuration tasks:

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
11. Verify local network communication.
12. Verify internet isolation.
13. Install Ollama.
14. Download and test the first local AI model.

Once the Linux server is operational, proceed to the next objective:

**Install Ollama and run the first local AI model.**

---

## 18. Reference Documentation

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

## 19. Current Project Status and Next Session Instructions

**Project:** Home AI Infrastructure

**Current phase:** Phase 1 – Prepare the Old Computer

**Current status:** Pre-installation preparation.

**Selected operating system:** Ubuntu Server 26.04.1 LTS

**Hardware:** Intel i7-8700 / 16 GB RAM / NVIDIA GTX 1070 / 2.24 TB storage

**Network:** Fizz Hitron CODA-4680 / Ethernet / Local network

The hardware has been assessed, the Linux distribution selected, and the network architecture designed.

The Fizz router has been investigated. No router settings have been changed.

### 19.1 Next Session Objective

Resume with:

**Final Windows checks and Ubuntu installation preparation.**

Start by reviewing the remaining checklist and collecting:

1. BIOS/UEFI information.
2. Secure Boot status.
3. Disk layout.
4. BitLocker status.
5. Ethernet adapter information.
6. Current computer IP address, subnet mask, and gateway.
7. Intel VT-x and VT-d status.

Then:

1. Prepare the USB installation media.
2. Verify the Ubuntu USB boots successfully.
3. Confirm hardware detection.
4. Disconnect the two 1 TB drives if practical.
5. Proceed with Ubuntu installation on the Kingston 240 GB SSD.

### 19.2 Important Instructions for the Next Session

Continue the project from the existing decisions.

Do not repeat the hardware assessment or router investigation unless new information requires it.

Prioritize:

1. Safe installation.
2. Preservation of the two 1 TB drives.
3. Correct Ethernet configuration.
4. GPU driver compatibility.
5. Internet isolation before installing AI software.

**Long-term objective:** Build a restricted local AI server that can be accessed from the main development computer without having unrestricted internet access.