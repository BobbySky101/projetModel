
# Home AI Infrastructure Project

# Phase 1 – Prepare the Old Computer

**Project status:** Phase 1 completed. Ubuntu Server successfully installed and initial remote SSH access verified.

---

## 1. Project Objective

Reuse an old Windows 10 computer by installing Linux and transforming it into a dedicated local AI server.

The computer will eventually:

- Host local language models using Ollama.
- Provide an API accessible from the current computer.
- Run lightweight AI tasks such as classification, extraction, and summarization.
- Participate in a distributed AI architecture with a more powerful model running on the current computer.
- Support experimentation with Python, AI agents, web scraping, and data analysis.

The project focuses on:

- Hardware assessment.
- Linux distribution selection.
- AI hardware feasibility.
- Storage organization.
- Network architecture and security planning.
- Windows pre-installation checks.
- Ubuntu installation.
- Initial remote administration.

**Phase 1 is now complete.** Ubuntu Server has been installed successfully, and remote SSH access from the development workstation has been tested successfully.

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
| Previous Windows driver | 560.94 |
| Updated Windows driver | 582.78 |
| GPU temperature (previously observed) | 35°C |
| GPU utilization (previously observed) | 2% |

The GTX 1070 is compatible with Ollama in principle, provided a sufficiently recent NVIDIA driver is installed.

**Important:** Ollama's NVIDIA requirements indicate that Pascal GPUs require driver version 570 or newer.

The Windows NVIDIA driver was updated to version 582.78 before Linux installation.

A compatible Linux NVIDIA driver must still be installed and verified.

### 2.4 Storage

The computer has three physical drives:

| Drive | Capacity | Type | Intended use |
|---|---:|---|---|
| Kingston SSD | 240 GB | SSD | Ubuntu operating system |
| Western Digital SSD (WDC) | 1 TB | SSD | AI models and application data |
| Seagate HDD (ST) | 1 TB | HDD | Backups and archived datasets |

**Total storage:** Approximately 2.24 TB.

The Kingston SSD is identified by the Ubuntu installer as approximately 223.570 GiB.

The two additional drives were kept connected during installation. Their existing partitions were preserved and were not selected for formatting or mounting.

---

## 3. Linux Distribution Selection

Four Linux distributions were considered:

- Ubuntu Server 26.04.1 LTS.
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

### 3.3 Why Ubuntu Server Instead of Ubuntu Desktop?

The computer will function as a dedicated server.

A graphical desktop environment is unnecessary because administration will happen remotely through SSH and Visual Studio Code Remote SSH.

Ubuntu Server provides:

- Lower background resource consumption.
- More available RAM for AI inference.
- Less CPU overhead.
- A simpler server environment.

### 3.4 Installation Result

Ubuntu Server was successfully installed on the Kingston 240 GB SSD.

The installer completed without reported errors.

The computer successfully rebooted into the installed operating system.

The first login encountered a username identification issue. The correct Linux username was subsequently identified, and successful local login was achieved.

The installation did not need to be repeated.

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

Ollama has not yet been installed.

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

Will contain:

- Ollama models.
- Python applications.
- Application databases.
- Processed datasets.
- Temporary processing files.

### 5.3 Seagate 1 TB HDD

**Purpose:** Backups and archives.

Will contain:

- Application backups.
- Archived datasets.
- Historical scraping results.
- Configuration backups.

### 5.4 Installation Result and Partition Configuration

The Ubuntu installer successfully identified all three physical drives.

The Kingston SSD was selected for the operating system.

The installer initially displayed five existing partitions on the Kingston SSD, corresponding to the previous Windows installation.

A custom storage layout was configured.

Final Kingston partition configuration:

| Partition | Format | Mount point | Purpose |
|---|---|---|---|
| 1 | FAT32 | `/boot/efi` | UEFI boot partition |
| 2 | ext4 | `/` | Ubuntu root filesystem |

The EFI partition was approximately 1 GiB.

The remaining Kingston capacity was allocated to the root filesystem.

The two additional drives remained unchanged.

| Drive | Installation result |
|---|---|
| Kingston | Reformatted and used for Ubuntu |
| WDC 1 TB | Existing partitions preserved |
| ST 1 TB | Existing partitions preserved |

**Important:** The two 1 TB drives were not disconnected during installation. This was acceptable because the installer clearly identified the physical drives and showed no pending changes to either ST or WDC.

Both drives must still be inspected after installation to confirm their filesystems and data are intact.

They will be configured and mounted in Ubuntu during Phase 2.

---

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

The current computer and old computer are connected to the same local network.

Ethernet is used for the AI server because it provides a more stable connection than Wi-Fi.

### 6.3 Confirmed Network Configuration

#### A. Current Computer – Development Workstation

| Parameter | Value |
|---|---|
| IPv4 address | `192.168.0.87` |
| Processor | AMD Ryzen 7 9700F |
| Role | Main development workstation |
| Network connection | Wi-Fi |
| Internet access | Allowed |

#### B. Old Computer – Ubuntu AI Server

| Parameter | Value |
|---|---|
| IPv4 address before installation | `192.168.0.176` |
| IPv4 address after installation | `192.168.0.178` |
| Processor | Intel Core i7-8700 |
| Role | Ubuntu AI server |
| Network connection | Ethernet |
| Internet access | To be restricted |

The server's IP address changed during installation.

The currently verified address is:

`192.168.0.178`

#### C. Shared Network Configuration

| Parameter | Verified value |
|---|---|
| Subnet | `192.168.0.0/24` |
| Subnet mask | `255.255.255.0` |
| IPv4 gateway | `192.168.0.1` |
| IPv6 gateway | `fe80::90aa:c3ff:fe36:c691%10` |
| Router | Fizz Hitron CODA-4680 |

Both computers are connected to the same IPv4 subnet and can communicate locally.

### 6.4 Proposed Network Architecture

A DHCP reservation for `192.168.0.178` is recommended, provided the router supports reservations based on the Ethernet adapter's MAC address.

This will provide a consistent local IP address without requiring a manually configured static IP on Ubuntu.

```text
                 Internet
                    |
                    |
          Fizz Hitron CODA-4680
             192.168.0.1
                    |
              Local network
                    |
          +---------+---------+
          |                   |
          |                   |
   Development             Ubuntu AI
   Workstation             Server
   192.168.0.87            192.168.0.178
   Wi-Fi                   Ethernet
          |                   |
          |                   |
   Internet allowed     Internet to be
   Local access         restricted
                        SSH: 22
                        Ollama: 11434
```

### 6.5 Fizz Hitron CODA-4680 Router Investigation

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

### 6.6 Final Router Decision

Keep the Fizz router in its normal configuration.

Implement the primary outbound internet restrictions directly on Ubuntu using `nftables`.

For stronger isolation in the future, consider a dedicated network firewall/router.

### 6.7 Ubuntu Network Security Configuration

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

Do not apply firewall rules until the actual network configuration has been verified.

Test SSH and Ollama connectivity after configuring the firewall.

Host-level firewall restrictions provide useful protection but are not equivalent to a separate network firewall. A process with administrator privileges could potentially modify the rules.

---

## 7. Remote Access Architecture

The current computer will be used to administer and communicate with the Ubuntu AI server.

### 7.1 SSH

OpenSSH Server was selected during Ubuntu installation.

It was successfully installed.

The SSH socket activation mechanism was retained rather than explicitly configuring SSH as a permanently running service.

The initial status of `ssh.service` showed:

```text
Active: inactive (dead)
TriggeredBy: ssh.socket
```

This was expected because systemd socket activation was configured.

The SSH socket was subsequently verified as listening on TCP port 22.

A successful SSH connection from the development workstation activated the SSH service.

The service was then observed in the following state:

```text
Active: active (running)
```

This is consistent with the socket activation configuration.

**Project decision:** Retain SSH socket activation.

There is no need to force `ssh.service` to run continuously.

### 7.2 Successful Remote Connection

The first remote SSH connection was successfully established from the development workstation.

Example connection command:

```powershell
ssh YOUR_USERNAME@192.168.0.178
```

Replace `YOUR_USERNAME` with the actual Linux account username.

The connection was tested using password authentication.

**Verification result:** Successful.

The SSH session was subsequently closed successfully using:

```bash
exit
```

### 7.3 SSH Architecture

The intended configuration is:

```text
Development workstation
192.168.0.87
       |
       | SSH / TCP 22
       |
       v
Ubuntu AI server
192.168.0.178
       |
       | systemd socket activation
       |
       v
ssh.socket
       |
       v
ssh.service
```

SSH will eventually be restricted to the development workstation or trusted local network.

SSH key authentication is recommended for future configuration.

### 7.4 Ollama API

The intended local API endpoint is:

```text
http://192.168.0.178:11434
```

Ollama should listen on the LAN interface, with firewall access restricted to the development workstation.

Never expose Ollama directly to the public internet.

Ollama has not yet been installed.



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

This information was collected before installation and used to guide the USB boot configuration.

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

The Kingston SSD was identified as the Windows installation disk.

The two additional drives were identified as the WDC 1 TB SSD and ST 1 TB HDD.

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

### 8.7 Windows Preparation Result

The necessary Windows pre-installation information was collected.

The following items were verified or recorded:

- Windows activation.
- BIOS/UEFI information.
- Network adapter information.
- Disk configuration.
- BitLocker status.
- Virtualization capabilities.

The old Windows installation was subsequently replaced by Ubuntu Server on the Kingston SSD.

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

The following settings were checked or considered:

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

**Recorded result:** Virtualization is Enabled.

Intel VT-d availability was also checked.

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

**Status:** Important pre-installation data was backed up before replacing Windows.

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

**Recorded result:** Physical maintenance tasks were skipped.

The computer was nevertheless operational and successfully completed the Ubuntu installation.

These maintenance tasks can be performed later if necessary.

---

## 12. Ubuntu Installation Media Preparation

### 12.1 Download Ubuntu Server

Official download:

https://ubuntu.com/download/server

Download the 64-bit Server ISO.

Selected version:

**Ubuntu Server 26.04.1 LTS**

### 12.2 Download Rufus

Official website:

https://rufus.ie/

Rufus was selected to create the bootable USB installation drive.

### 12.3 Prepare the USB Drive

A 16 GB USB drive was selected.

Requirements:

- USB drive with at least 8 GB capacity.
- Windows computer.
- Downloaded Ubuntu Server ISO.
- Rufus.

Recommended specifications:

- 16 GB USB drive.
- USB 3.0 or newer.
- Reputable manufacturer.

The USB drive was erased during the bootable media creation process.

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

### 12.5 USB Creation and Boot Verification

The bootable USB was successfully created using Rufus.

The USB was connected to the old computer.

The computer successfully booted from the USB installation media.

The Ubuntu Server installer appeared without errors or unusual messages.

The language selection screen was reached successfully.

**Verification result:** USB installation media works correctly.

---


## 13. Ubuntu Installation Configuration

The following settings were used during installation.

| Setting | Selected configuration |
|---|---|
| Distribution | Ubuntu Server 26.04.1 LTS |
| Installation disk | Kingston 240 GB SSD |
| Hostname | ai-server |
| Network | Ethernet |
| Installation type | Custom storage layout |
| SSH server | Enabled |
| Additional packages | None initially |
| Ubuntu Pro | Skipped |

### 13.1 Storage Configuration

The three physical drives were identified in the Ubuntu installer.

The Kingston SSD appeared as approximately 223.570 GiB.

The two additional drives were:

- ST: Seagate 1 TB HDD.
- WDC: Western Digital 1 TB SSD.

The Kingston initially contained five existing Windows partitions:

| Partition | Original filesystem | Approximate size |
|---|---|---:|
| 1 | NTFS | 450 MB |
| 2 | FAT32 / ESP | 99 MB |
| 3 | Unused | 16 MB |
| 4 | NTFS | 222.514 GB |
| 5 | NTFS | 514 MB |

The installer initially displayed the USB installation drive under Used Devices. Its approximately 57.734 GB capacity confirmed that it was the USB drive rather than the Kingston SSD.

The Kingston was then selected for the installation.

### 13.2 Custom Partition Layout

The custom storage layout was selected.

The Kingston SSD was configured with two new partitions:

| Partition | Format | Mount point | Purpose |
|---|---|---|---|
| 1 | FAT32 | `/boot/efi` | UEFI boot partition |
| 2 | ext4 | `/` | Ubuntu root filesystem |

The EFI partition was configured with approximately 1 GiB.

The remaining available Kingston capacity was allocated to the root partition.

The Kingston was subsequently displayed under Used Devices with both new partitions.

### 13.3 Protection of the Two Additional Drives

The ST and WDC drives remained connected throughout installation.

The installer showed their existing partitions as available devices.

No partitions were selected for formatting or mounting.

Before confirming the storage configuration, the pending changes were reviewed.

**Verification result:**

- Kingston: New EFI and root partitions.
- ST: No pending changes.
- WDC: No pending changes.

Only the Kingston had pending formatting and partition operations.

The installation was therefore approved.

**Important:** The ST and WDC drives were not disconnected during installation. Their data was preserved by leaving their existing partitions untouched.

Their contents and filesystems must still be verified from the installed Ubuntu system.

### 13.4 Ubuntu Pro

When prompted to enable Ubuntu Pro, the option to skip it was selected.

Ubuntu Pro is optional and can be enabled later.

This decision does not prevent the installation or use of Ubuntu Server, Ollama, Docker, Python, or NVIDIA drivers.

### 13.5 SSH Configuration

During installation, the option to install OpenSSH Server was selected.

This was necessary because the server will be administered remotely from the development workstation.

The SSH server was successfully installed.

Password authentication was used for the initial remote connection.

SSH key authentication will be configured later.

### 13.6 Featured Server Snaps

The installer displayed a list of optional featured server snaps.

No additional packages were selected.

This was intentional.

The project will install and configure the necessary software manually after verifying the base Ubuntu installation.

Planned software includes:

- NVIDIA drivers.
- Ollama.
- Docker.
- Python.
- Git.
- nftables.

### 13.7 Installation Completion

Ubuntu Server installation completed successfully.

The computer rebooted from the Kingston SSD.

The installation USB was no longer needed after the successful first boot.

The initial login encountered a username identification issue.

The username entered during installation was not correctly remembered.

Ubuntu Recovery Mode was accessed using the GRUB advanced boot options.

Two recovery kernel entries were displayed:

- Linux 7.0.0-44-generic.
- Linux 7.0.0-30-generic.

The newer recovery entry was selected.

The recovery menu displayed:

- resume
- clean
- dpkg
- fsck
- grub
- network
- root
- system-summary

The root recovery shell was used to inspect the local user accounts.

The following command was used:

```bash
awk -F: '$3 >= 1000 && $3 < 60000 {print $1, $6}' /etc/passwd
```

This identified the actual Linux username.

The username was subsequently used to log in successfully.

**Important:** The issue was caused by incorrect username identification, not a failed Ubuntu installation.

No reinstallation was necessary.

---

## 14. First Boot and Initial Installation Verification

After successfully logging in, the first system checks were performed.

### 14.1 Local Login

**Status:** Successful.

The correct Linux username was identified and used.

The Ubuntu account password was accepted.

### 14.2 Sudo Authentication

The `sudo` command initially returned an authentication failure.

This was resolved, and administrative commands could subsequently be executed successfully.

The account password is used for local `sudo` authentication.

The same account password was used for the initial SSH password authentication.

### 14.3 SSH Service Verification

The following command was executed:

```bash
sudo systemctl status ssh
```

The initial output showed:

```text
ssh.service - OpenBSD Secure Shell server

Loaded: loaded (/usr/lib/systemd/system/ssh.service; disable; preset: enabled)

Active: inactive (dead)

TriggeredBy: ssh.socket
```

This was investigated.

The SSH service was configured for systemd socket activation.

The socket was subsequently verified as listening on TCP port 22.

There was no need to force the SSH service to run continuously.

After a successful remote connection, the SSH service was observed as:

```text
Active: active (running)
```

This is expected behavior when a connection activates the service.

**Project decision:** Retain socket activation.

### 14.4 Successful Remote SSH Connection

The development workstation successfully connected to the Ubuntu server.

The server's original IP address changed during installation.

The previously recorded address was:

`192.168.0.176`

The new address was identified as:

`192.168.0.178`

The successful connection was made using:

```powershell
ssh YOUR_USERNAME@192.168.0.178
```

The actual Linux username was used.

The first connection required accepting the server's SSH host key.

Password authentication was then successful.

The SSH session was closed using:

```bash
exit
```

**Verification result:** Remote SSH access works successfully.

### 14.5 SSH Socket Verification

The SSH socket was verified as listening on port 22.

The following command can be used to inspect its status:

```bash
sudo systemctl status ssh.socket
```

Expected result:

```text
Active: active (listening)
```

The listening port can also be inspected using:

```bash
sudo ss -ltnp | grep ':22'
```

### 14.6 Important SSH Management Decision

The SSH service will remain configured for socket activation.

Do not automatically execute:

```bash
sudo systemctl enable --now ssh
```

This would explicitly enable and start the SSH service rather than retaining the intended socket-activated arrangement.

The current configuration is suitable for this project.

---

## 15. Installation Results Summary

The following installation objectives have been achieved:

| Objective | Result |
|---|---|
| Create bootable USB | Successful |
| Boot old computer from USB | Successful |
| Reach Ubuntu Server installer | Successful |
| Identify Kingston SSD | Successful |
| Identify ST and WDC drives | Successful |
| Configure EFI partition | Successful |
| Configure Ubuntu root partition | Successful |
| Preserve two additional drives during installation | Successful, pending post-installation data verification |
| Complete Ubuntu installation | Successful |
| Boot from Kingston SSD | Successful |
| Complete first local login | Successful |
| Install OpenSSH Server | Successful |
| Verify SSH socket on port 22 | Successful |
| Establish remote SSH connection | Successful |

### 15.1 Remaining Verification

The following items still need to be checked:

- Actual Ubuntu version and release.
- Hostname.
- Current Ethernet interface and IP configuration.
- Physical disk identification from Linux.
- Filesystem integrity and data preservation on ST and WDC.
- NVIDIA GPU detection.
- Linux NVIDIA driver compatibility.
- DHCP reservation for the server's current IP address.

These checks will be completed during Phase 2.

---

## 16. Phase 1 Completion

The original objective of Phase 1 was to prepare the old computer and install Ubuntu Server safely.

This objective has been achieved.

The following decisions and actions are now confirmed:

- Ubuntu Server successfully installed on the Kingston 240 GB SSD.
- UEFI boot partition configured.
- Root filesystem configured as ext4.
- Both 1 TB drives left untouched during installation.
- OpenSSH Server installed.
- SSH socket activation retained.
- Successful remote SSH access from the development workstation.
- Current server IP address identified as `192.168.0.178`.

The computer is now operational as an Ubuntu Server installation.

The next phase will focus on system verification, networking, storage configuration, security and AI software preparation.

---

## 17. Transition to Phase 2

The next phase will begin with:

**Phase 2 – Initial Ubuntu Server Configuration**

The objectives are:

1. Verify the installed Ubuntu version.
2. Verify the hostname.
3. Inspect the network interfaces and current IP address.
4. Confirm the SSH socket configuration.
5. Verify the two additional storage drives.
6. Configure a DHCP reservation.
7. Update Ubuntu.
8. Prepare NVIDIA driver installation.
9. Configure the network firewall.
10. Install Ollama.
11. Test local AI inference.

The priority remains:

- Preserve existing data on both 1 TB drives.
- Maintain reliable remote SSH access.
- Verify NVIDIA compatibility.
- Establish controlled local network communication.
- Restrict unnecessary internet access before deploying AI services.



# Part 3 – Project Status, Consolidated Decisions and Next Steps

## 18. Consolidated Project Decisions

The following decisions have been made throughout Phase 1.

### 18.1 Hardware and Operating System

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

### 18.2 Storage

| Topic | Decision |
|---|---|
| Installation disk | Kingston 240 GB SSD |
| AI storage | Western Digital 1 TB SSD |
| Backup storage | Seagate 1 TB HDD |
| Installation precaution | Both additional drives left untouched during installation |

### 18.3 Network and Security

| Topic | Decision |
|---|---|
| Network | Ethernet |
| Router | Fizz Hitron CODA-4680 |
| Network architecture | Both computers on the same LAN |
| Server hostname | ai-server (planned; verification pending) |
| Server IP address | 192.168.0.178 (currently observed) |
| Internet restriction | Ubuntu nftables firewall |
| Remote administration | SSH |
| SSH activation | systemd socket activation |
| SSH port | 22 |
| Ollama API | Local network access only, port 11434 |

Additional security decisions:

- Keep the Fizz router in its normal configuration.
- Do not use router Device Filter to isolate the AI server.
- Do not change the global router firewall level.
- Do not rely on router Port Blocking as the primary internet isolation mechanism.
- Implement outbound internet restrictions using Ubuntu `nftables`.
- Allow local SSH and Ollama API communication from the development workstation.
- Account for IPv4 and IPv6.
- Never expose Ollama directly to the public internet.

### 18.4 AI Software

| Topic | Decision |
|---|---|
| AI runtime | Ollama |
| Initial model | Llama 3.2 3B |
| Model storage | Western Digital 1 TB SSD |
| Remote API access | Development workstation over LAN |
| Development environment | Current Windows workstation |
| Remote administration | SSH / VS Code Remote SSH |

---

## 19. Consolidated Project Checklist

### 19.1 Hardware Assessment

- [x] Identify processor.
- [x] Identify RAM capacity.
- [x] Identify graphics card.
- [x] Identify NVIDIA driver version.
- [x] Identify storage devices.
- [x] Confirm 64-bit architecture.

### 19.2 Linux Selection

- [x] Compare Ubuntu and alternative distributions.
- [x] Select Ubuntu Server 26.04.1 LTS.
- [x] Define Ubuntu 24.04 as a fallback option.
- [x] Decide against installing a graphical desktop environment.

### 19.3 Windows Preparation

- [x] Check Windows activation.
- [x] Record BIOS mode and Secure Boot status.
- [x] Record BIOS version.
- [x] Record Ethernet and Wi-Fi adapters.
- [x] Check disk partition layout.
- [x] Check BitLocker status.
- [x] Verify BitLocker recovery keys if applicable.
- [x] Save important data and credentials.

### 19.4 Hardware Preparation

- [x] Verify Ethernet connectivity.
- [x] Verify Intel VT-x status.
- [x] Verify Intel VT-d availability.
- [x] Confirm BIOS configuration.
- [ ] Clean the computer and check fans.
- [ ] Check SSD and HDD physical connections.

Physical maintenance was skipped before installation. It can be performed later.

### 19.5 Network Preparation

- [x] Identify current computer IPv4 address.
- [x] Identify subnet mask.
- [x] Identify default gateway.
- [x] Identify actual LAN subnet.
- [x] Record Ethernet adapter model.
- [x] Identify the server's post-installation IP address.
- [ ] Prepare DHCP reservation for the server.
- [ ] Verify the server's current IPv4 and IPv6 configuration.

### 19.6 Installation Preparation

- [x] Back up important data.
- [x] Confirm selected Ubuntu release availability.
- [x] Download Ubuntu Server ISO.
- [x] Purchase a 16 GB USB drive.
- [x] Download Rufus.
- [x] Create bootable USB.
- [x] Verify USB boots successfully.
- [x] Identify the Kingston 240 GB SSD.
- [x] Identify the two additional storage drives.
- [x] Configure Kingston EFI partition.
- [x] Configure Kingston root partition.
- [x] Preserve ST and WDC partitions during installation.
- [x] Install Ubuntu Server.
- [x] Successfully boot Ubuntu from Kingston SSD.

### 19.7 Initial Ubuntu Access

- [x] Complete initial local login.
- [x] Identify the correct Linux username.
- [x] Resolve initial sudo authentication issue.
- [x] Install OpenSSH Server.
- [x] Verify SSH socket listening on port 22.
- [x] Retain SSH socket activation.
- [x] Successfully connect remotely from the development workstation.
- [x] Verify that SSH session can be closed using `exit`.

### 19.8 Remaining Ubuntu Configuration

- [ ] Verify Ubuntu version and release.
- [ ] Verify hostname.
- [ ] Verify Ethernet interface configuration.
- [ ] Verify current server IP address.
- [ ] Verify SSH socket activation after reboot.
- [ ] Verify both additional drives and their existing data.
- [ ] Configure persistent storage mount points.
- [ ] Configure DHCP reservation.
- [ ] Update Ubuntu.
- [ ] Verify NVIDIA GPU detection.
- [ ] Install compatible NVIDIA driver.
- [ ] Verify NVIDIA driver operation.
- [ ] Configure `nftables`.
- [ ] Verify IPv4 internet restrictions.
- [ ] Verify IPv6 internet restrictions.
- [ ] Verify local SSH access after firewall configuration.
- [ ] Verify local Ollama API access after installation.
- [ ] Install Ollama.
- [ ] Configure Ollama model storage.
- [ ] Download initial AI model.
- [ ] Test local inference.

---

## 20. Current Project Status

**Project:** Home AI Infrastructure

**Phase 1:** Prepare the Old Computer

<badge color="success">Completed</badge>

**Phase 2:** Initial Ubuntu Server Configuration

<badge color="info">Next phase</badge>

### 20.1 Current Hardware

| Component | Configuration |
|---|---|
| CPU | Intel Core i7-8700 |
| RAM | 16 GB |
| GPU | NVIDIA GTX 1070 |
| GPU VRAM | 8 GB |
| OS disk | Kingston 240 GB SSD |
| AI storage | WDC 1 TB SSD |
| Backup storage | ST 1 TB HDD |

### 20.2 Current Software Status

| Component | Status |
|---|---|
| Ubuntu Server | Installed |
| OpenSSH Server | Installed |
| SSH socket activation | Verified |
| SSH remote connection | Tested successfully |
| NVIDIA Linux driver | Not yet installed |
| Ollama | Not yet installed |
| Docker | Not yet installed |
| Python development environment | Not yet configured |
| nftables firewall | Not yet configured |

### 20.3 Current Network Configuration

| Device | IP address | Connection |
|---|---|---|
| Development workstation | `192.168.0.87` | Wi-Fi |
| Ubuntu AI server | `192.168.0.178` | Ethernet |
| Router | `192.168.0.1` | Gateway |

Subnet:

`192.168.0.0/24`

The server's IP address changed from `192.168.0.176` to `192.168.0.178` during installation.

A DHCP reservation should be configured once the Ethernet MAC address has been verified.

### 20.4 Current Access Information

The Linux account username is the username entered during Ubuntu installation, which was initially misidentified.

The correct username was subsequently identified using the recovery environment.

The account password is used for local login, sudo authentication and initial SSH password authentication.

The SSH connection is:

```powershell
ssh YOUR_USERNAME@192.168.0.178
```

Replace `YOUR_USERNAME` with the actual Linux username.

The SSH session can be terminated using:

```bash
exit
```

**Security note:** Never store the actual account password in this project documentation.

---

## 21. Next Steps – Phase 2

After completing Phase 1, proceed with the following installation and configuration tasks.

### 21.1 Initial Ubuntu Verification

1. Verify the Ubuntu version.
2. Verify the hostname.
3. Verify the current network configuration.
4. Verify the SSH socket activation mechanism.
5. Identify the physical storage devices.
6. Confirm that the two additional drives still contain their expected data.

### 21.2 Storage Configuration

1. Identify the WDC 1 TB SSD.
2. Identify the ST 1 TB HDD.
3. Verify their existing partition tables and filesystems.
4. Mount the WDC SSD for AI models and application data.
5. Mount the ST HDD for backups and archives.
6. Configure persistent mounts using `/etc/fstab`.
7. Verify that both drives mount correctly after reboot.

Do not format either drive before verifying its existing contents.

### 21.3 Network Configuration

1. Identify the Ethernet MAC address.
2. Configure a DHCP reservation for `192.168.0.178`, if available.
3. Verify the server's IPv4 configuration.
4. Inspect IPv6 configuration.
5. Verify local communication between both computers.
6. Confirm SSH access remains functional.

### 21.4 System Updates

Update the Ubuntu installation and verify that the system is operating correctly.

### 21.5 NVIDIA Configuration

1. Identify the available NVIDIA driver packages.
2. Verify compatibility with the installed Ubuntu release.
3. Install a compatible driver.
4. Reboot the server.
5. Verify GPU detection using `nvidia-smi`.
6. Confirm that the GTX 1070 is available for AI workloads.

### 21.6 Network Security

Configure `nftables` to:

- Allow necessary local network communication.
- Allow SSH from the development workstation.
- Allow Ollama API access from the development workstation.
- Allow DHCP where necessary.
- Restrict incoming connections.
- Block outbound internet access.
- Account for IPv4 and IPv6.
- Preserve access after reboot.

Test firewall behavior carefully before considering internet isolation complete.

### 21.7 AI Software Installation

1. Install Ollama.
2. Configure Ollama to store models on the WDC SSD.
3. Verify that Ollama recognizes the NVIDIA GPU.
4. Download Llama 3.2 3B.
5. Run the first inference test.
6. Verify API access from the development workstation.

---

## 22. Important Reference Documentation

| Resource | URL |
|---|---|
| Ubuntu Server downloads | https://ubuntu.com/download/server |
| Ubuntu Server documentation | https://documentation.ubuntu.com/server/ |
| Ubuntu NVIDIA drivers | https://documentation.ubuntu.com/server/how-to/graphics/install-nvidia-drivers/ |
| NVIDIA driver downloads | https://www.nvidia.com/en-us/drivers/ |
| Ollama | https://ollama.com/ |
| Ollama documentation | https://docs.ollama.com/ |
| Ollama GPU requirements | https://docs.ollama.com/gpu |
| Rufus | https://rufus.ie/ |
| VS Code Remote SSH | https://code.visualstudio.com/docs/remote/ssh |

---

## 23. Final Project Summary

Phase 1 successfully transformed the old Windows 10 computer into an operational Ubuntu Server installation.

The machine has:

- Ubuntu Server installed on the Kingston 240 GB SSD.
- A working local Linux account.
- OpenSSH Server installed.
- SSH socket activation configured.
- Successful remote access from the main development workstation.
- Both additional storage drives preserved during installation.

The next objective is to configure the server as a secure, remotely accessible infrastructure platform.

The long-term architecture remains:

```text
                Internet
                    |
                    |
              Home Router
             192.168.0.1
                    |
              Local Network
                    |
          +---------+---------+
          |                   |
          |                   |
   Development             Ubuntu AI
   Workstation             Server
   192.168.0.87            192.168.0.178
          |                   |
          |                   |
   Main AI workloads      Ollama
   Development            Local models
   Orchestration          AI API
          |                   |
          +---------+---------+
                    |
              Local communication
```

**Long-term objective:** Build a restricted local AI server that can be accessed from the main development computer without having unrestricted internet access.

The next working document will be:

**Phase 2 – Initial Ubuntu Server Configuration.**
