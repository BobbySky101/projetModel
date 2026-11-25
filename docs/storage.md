# Storage Configuration

**Project:** Home AI Infrastructure  
**System:** ai-server  
**Last updated:** 2026-11-24

---

# 1. Storage Overview

The server contains three physical drives.

Each drive has a dedicated responsibility:

| Drive | Role |
|---------|---------|
| Kingston SSD | Operating system |
| WDC SSD | AI models and application data |
| Seagate HDD | Backups and archives |

Total available storage:

| Device | Capacity |
|----------|----------:|
| Kingston SSD | 240 GB |
| WDC SSD | 1 TB |
| Seagate HDD | 1 TB |
| Total | ~2.24 TB |

---

# 2. Physical Drive Inventory

## 2.1 Kingston SSD

| Parameter | Value |
|------------|---------|
| Purpose | Operating System |
| Capacity | 240 GB |
| Filesystem | ext4 |
| Mount Point | / |

### Current Usage

- Ubuntu Server
- System packages
- Logs
- Configuration files
- System services

---

## 2.2 Western Digital SSD

| Parameter | Value |
|------------|---------|
| Purpose | AI Storage |
| Capacity | 1 TB |
| Label | ai-ssd |
| Filesystem | ext4 |
| Mount Point | /mnt/ai-ssd |

### Current Usage

- Ollama models
- Python applications
- Databases
- Datasets
- Temporary processing data

---

## 2.3 Seagate HDD

| Parameter | Value |
|------------|---------|
| Purpose | Backup Storage |
| Capacity | 1 TB |
| Label | backup |
| Filesystem | ext4 |
| Mount Point | /mnt/backup |

### Current Usage

- System backups
- Application backups
- Archived datasets
- Archived model data

---

# 3. Filesystem Layout

## Operating System Drive

```text
/
├── boot
├── etc
├── home
├── usr
├── var
└── ...
```

---

## AI Storage Drive

```text
/mnt/ai-ssd
├── ollama
├── applications
├── databases
├── datasets
└── temporary
```

---

## Backup Drive

```text
/mnt/backup
├── system
├── applications
├── databases
└── datasets
```

---

# 4. Mount Configuration

Persistent mounts are configured using filesystem UUIDs.

Current fstab entries:

```fstab
UUID=3e08dcda-25fa-44ce-92d7-f94394f2e97c /mnt/ai-ssd ext4 defaults,nofail 0 2
UUID=56bdda1b-966e-417d-8c44-4f839e043152 /mnt/backup ext4 defaults,nofail 0 2
```

---

# 5. Mount Verification

Verify mounted storage:

```bash
findmnt
```

Verify individual mount points:

```bash
findmnt /mnt/ai-ssd
findmnt /mnt/backup
```

Verify available space:

```bash
df -h
```

---

# 6. Disk Information Commands

## List Block Devices

```bash
lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINTS
```

---

## List UUIDs

```bash
sudo blkid
```

---

## Display Detailed Partition Information

```bash
sudo fdisk -l
```

---

# 7. Data Placement Policy

## Operating System Drive

Allowed:

- Ubuntu operating system
- System packages
- Logs
- Service configuration
- Temporary administrative files

Avoid storing:

- AI models
- Large datasets
- Application databases
- Long-term backups

---

## AI Storage Drive

Store:

- Ollama models
- Python projects
- Application data
- AI datasets
- Cache data
- Temporary processing files

---

## Backup Drive

Store:

- Backups
- Snapshots
- Exported databases
- Archived datasets
- Historical project data

Do not run active applications from this drive.

---

# 8. Ollama Storage

## Model Location

Planned location:

```text
/mnt/ai-ssd/ollama/models
```

---

## Purpose

Store:

- Downloaded models
- Model manifests
- Quantized model files
- Future custom models

Examples:

```text
/mnt/ai-ssd/ollama/models
├── llama3.2
├── qwen
├── mistral
└── ...
```

---

# 9. Backup Strategy

## Objectives

Protect:

- System configuration
- Application code
- Databases
- Custom AI assets

---

## Backup Target

```text
/mnt/backup
```

---

## Proposed Layout

```text
/mnt/backup
├── system
│   ├── etc
│   ├── nftables
│   └── ssh
│
├── applications
│
├── databases
│
└── datasets
```

---

# 10. Capacity Monitoring

## Check Free Space

```bash
df -h
```

---

## Largest Directories

```bash
sudo du -xh /mnt/ai-ssd --max-depth=1 | sort -h
```

---

## Monitor Storage Growth

```bash
sudo du -sh /mnt/ai-ssd/*
```

---

# 11. Recovery Notes

## Recreate Mount Points

```bash
sudo mkdir -p /mnt/ai-ssd
sudo mkdir -p /mnt/backup
```

---

## Test fstab

After modifying:

```bash
sudo mount -a
```

A successful execution with no errors indicates that the entries are valid.

---

# 12. Current Storage Status

| Item | Status |
|---------|---------|
| Kingston SSD operational | Yes |
| WDC SSD operational | Yes |
| Seagate HDD operational | Yes |
| Filesystems verified | Yes |
| Persistent mounts configured | Yes |
| Mounts verified after reboot | Yes |
| AI storage ready | Yes |
| Backup storage ready | Yes |

---

# 13. Future Improvements

## Medium Priority

- Automated backups
- Scheduled filesystem health checks
- SMART monitoring alerts
- Compression of archived datasets

## Long-Term

- Larger SSD for model storage
- External backup destination
- Off-site backup strategy
- Snapshot-based backup system