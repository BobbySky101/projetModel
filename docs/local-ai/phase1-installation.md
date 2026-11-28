# Phase 1 - Ubuntu Server Installation

**Project:** Home AI Infrastructure

**Status:** Completed

**Completion Date:** 2026-11-24

---

# 1. Objective

The objective of Phase 1 was to transform an unused Windows 10 desktop computer into a functional Ubuntu Server system suitable for future AI development and local inference workloads.

The installation needed to:

- Replace Windows 10.
- Preserve the two existing 1 TB data drives.
- Install Ubuntu Server.
- Enable remote administration.
- Verify successful remote access.

Detailed hardware information is maintained in:

- hardware.md
- storage.md
- network.md

---

# 2. Initial Situation

System state before work began:

| Item | State |
|--------|--------|
| Operating System | Windows 10 |
| Primary Disk | Kingston SSD |
| Additional Disk #1 | WDC SSD |
| Additional Disk #2 | Seagate HDD |
| Remote Access | Not configured |
| Linux Installed | No |

---

# 3. Pre-Installation Preparation

## Tasks Completed

- Verified Windows activation.
- Recorded BIOS and UEFI information.
- Recorded network information.
- Recorded disk configuration.
- Verified virtualization support.
- Verified BitLocker status.
- Backed up important data.

---

# 4. Operating System Selection

The following operating systems were evaluated:

- Ubuntu Server 26.04.1 LTS
- Ubuntu Server 24.04 LTS
- Debian 13
- Rocky Linux 10

Selected operating system:

```text
Ubuntu Server 26.04.1 LTS
```

Reasoning:

- Strong AI ecosystem.
- Excellent community support.
- Good NVIDIA compatibility.
- Well-supported by Ollama.
- Familiar administration model.

---

# 5. Installation Media

## Installation USB

| Tool | Purpose |
|---------|---------|
| Rufus | Create bootable USB |
| Ubuntu Server ISO | Operating system installation |

Results:

- Bootable USB created successfully.
- USB boot verified successfully.

---

# 6. Installation Procedure

## Disk Selection

The Kingston SSD was selected for installation.

The WDC SSD and Seagate HDD remained connected but were not modified.

---

## Partition Configuration

The Kingston SSD was repartitioned.

Resulting layout:

| Mount Point | Filesystem |
|------------|------------|
| /boot/efi | FAT32 |
| / | ext4 |

---

## Operating System Installation

Ubuntu Server installation completed successfully.

No installation errors were reported.

---

# 7. SSH Installation

OpenSSH Server was installed during setup.

Remote administration was required for the project architecture.

SSH installation completed successfully.

---

# 8. First Boot

The system rebooted successfully after installation.

Ubuntu booted from the Kingston SSD.

Result:

✅ Successful

---

# 9. Issue Encountered

## Username Identification

### Problem

The username configured during installation was not remembered correctly.

Login initially failed because the incorrect username was used.

---

### Investigation

Recovery mode was opened through GRUB.

A root shell was used to inspect local accounts.

Command used:

```bash
awk -F: '$3 >= 1000 && $3 < 60000 {print $1, $6}' /etc/passwd
```

---

### Resolution

The correct username was identified.

Login then succeeded immediately.

---

### Impact

No reinstallation was required.

No data loss occurred.

Issue resolved successfully.

---

# 10. SSH Verification

Initial verification showed:

```text
ssh.service inactive (dead)
ssh.socket active (listening)
```

Investigation confirmed that Ubuntu was using systemd socket activation.

This behavior was normal.

---

## Decision

Retain socket activation.

Do not force ssh.service to run continuously.

---

# 11. Remote Access Validation

A remote SSH connection was established successfully from the development workstation.

Example:

```powershell
ssh USERNAME@192.168.0.178
```

Results:

- Host key accepted.
- Password authentication successful.
- Shell access confirmed.
- Session terminated successfully.

---

# 12. Phase 1 Deliverables

Completed deliverables:

| Deliverable | Result |
|-------------|---------|
| Ubuntu Server installed | Complete |
| Kingston SSD migrated to Linux | Complete |
| EFI partition created | Complete |
| Root filesystem created | Complete |
| Additional drives preserved | Complete |
| OpenSSH installed | Complete |
| Local login verified | Complete |
| SSH access verified | Complete |
| Remote administration verified | Complete |

---

# 13. Lessons Learned

## Recovery Mode Can Prevent Reinstallation

The username issue initially appeared serious.

Using recovery mode quickly identified the actual cause.

This avoided an unnecessary reinstall.

---

## Socket-Activated SSH Is Normal

Ubuntu's socket-activated SSH configuration differs from many traditional Linux installations.

An inactive ssh.service does not necessarily indicate a problem.

---

## Installing with Additional Drives Connected Is Safe

Careful review of installer actions prevented accidental modification of the 1 TB drives.

The installer clearly separated physical devices and pending changes.

---

# 14. Final Outcome

Phase 1 successfully converted the former Windows 10 computer into a functioning Ubuntu Server.

The resulting system provides:

- Ubuntu Server 26.04.1 LTS
- Remote SSH administration
- Preserved secondary storage
- Stable network connectivity
- Foundation for future AI workloads

---

# 15. Exit Criteria Verification

| Requirement | Status |
|-------------|---------|
| Ubuntu Installed | ✅ |
| System Boots Successfully | ✅ |
| Data Drives Preserved | ✅ |
| Local Login Works | ✅ |
| SSH Installed | ✅ |
| Remote SSH Access Works | ✅ |

---

# 16. Next Phase

Proceed to:

```text
Phase 2 - Initial Server Configuration
```

Primary objectives:

- System updates
- Storage configuration
- Network configuration
- NVIDIA setup
- Firewall deployment
- Ollama installation