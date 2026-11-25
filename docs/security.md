# Security Configuration

**Project:** Home AI Infrastructure  
**System:** ai-server  
**Last updated:** 2026-11-24

---

# 1. Security Overview

The Ubuntu AI server provides local AI inference services within a home network.

The server is not intended to be publicly accessible and should only be reachable by authorized devices on the local network.

Primary security objectives:

- Protect remote administration access.
- Restrict access to AI services.
- Limit attack surface.
- Prevent accidental exposure to the Internet.
- Preserve system integrity and recoverability.
- Maintain secure operation with minimal complexity.

---

# 2. Security Principles

## Least Privilege

Only required services should be accessible.

Unnecessary services should remain disabled or uninstalled.

---

## Local-Only Access

The server is intended for use inside the home network.

No services should be exposed directly to the Internet.

---

## Defense in Depth

Security is provided through multiple layers:

- Router configuration
- Linux firewall
- Service configuration
- User authentication
- Operating system updates

---

## Recoverability

Security controls must allow safe recovery and administration of the server.

Avoid configurations that risk permanent loss of SSH access.

---

# 3. Security Objectives

| Objective | Status |
|------------|---------|
| Secure remote administration | Implemented |
| Restrict AI service access | Implemented |
| Prevent public exposure | Implemented |
| Maintain OS updates | Implemented |
| Restrict unnecessary inbound traffic | Implemented |
| Preserve administrative access | Implemented |

---

# 4. Protected Assets

## System

- Ubuntu Server installation
- Operating system configuration
- Installed software
- Firewall configuration

---

## AI Assets

- Ollama models
- Model configurations
- Local datasets
- Future agent applications

---

## Administrative Assets

- User accounts
- SSH configuration
- SSH keys
- Backup archives

---

# 5. Threat Model

## In Scope

### Unauthorized Access from Local Devices

Example:

- Infected laptop
- Guest device
- Untrusted device on Wi-Fi

Mitigation:

- Firewall restrictions
- Limited exposed services

---

### Accidental Internet Exposure

Example:

- Router misconfiguration
- Port forwarding

Mitigation:

- No port forwarding
- Regular review of router configuration

---

### Service Misconfiguration

Example:

- Ollama listening on unintended interfaces
- Overly permissive firewall rules

Mitigation:

- Explicit access controls
- Configuration verification

---

### Credential Theft

Example:

- Weak passwords
- Reused passwords

Mitigation:

- Strong passwords
- SSH key authentication

---

## Out of Scope

The server is not designed to resist:

- Nation-state adversaries
- Physical theft
- Advanced persistent threats
- Highly targeted attacks

---

# 6. Authentication

## Local Login

Authentication is required for:

- Console login
- SSH access
- Administrative tasks

---

## Sudo Access

Administrative actions require:

```bash
sudo
```

Only trusted administrative users should have sudo privileges.

---

## SSH Authentication

Current status:

| Method | Status |
|----------|---------|
| Password Authentication | Enabled |
| Public Key Authentication | Planned |
| Root Login | Disabled |

Current administrative access uses:

- Ed25519 SSH key authentication
- SSH client host alias `ai-server`
- Dedicated key specified through IdentityFile

Primary connection:

```bash
ssh ai-server
```

---

## Future Recommendation

Migrate to SSH key authentication:

```text
PasswordAuthentication no
PubkeyAuthentication yes
```

After successfully verifying key-based login.

---

# 7. Network Access Control

## Allowed Access

| Source | Destination | Port |
|----------|------------|------|
| Development Workstation | SSH | 22 |
| Development Workstation | Ollama API | 11434 |

---

## Blocked Access

| Source | Destination |
|----------|------------|
| Internet | SSH |
| Internet | Ollama |
| Other LAN Devices | SSH |
| Other LAN Devices | Ollama |

---

# 8. Firewall Configuration

## Firewall Platform

```text
nftables
```

---

## Default Policies

| Chain | Policy |
|----------|---------|
| Input | Drop |
| Forward | Drop |
| Output | Accept |

---

## Firewall Objectives

Allow:

- SSH from development workstation
- Ollama API from development workstation
- Established connections
- Required networking services

Block:

- Unauthorized inbound connections
- Unsolicited access attempts

---

## Verification

Verify firewall status:

```bash
sudo nft list ruleset
```

---

Verify service exposure:

```bash
sudo ss -ltnp
```

---

# 9. Service Exposure

## Approved Listening Services

| Service | Port |
|-----------|------|
| SSH | 22 |
| Ollama | 11434 |

---

## Verification

```bash
sudo ss -ltnp
```

Review periodically for unexpected services.

---

# 10. Router Security

## Current Policy

The router remains in its default operating mode.

No special isolation is configured on the router.

---

## Explicit Decisions

Do not use:

- Device filtering
- Port blocking for server isolation
- Public port forwarding

---

## Public Exposure Policy

The following services must never be forwarded to the Internet:

- SSH (22)
- Ollama API (11434)

---

# 11. Software Updates

## Operating System

Keep Ubuntu updated:

```bash
sudo apt update
sudo apt upgrade
```

---

## NVIDIA Driver

Maintain a supported NVIDIA driver version.

Current version:

```text
580.178.04
```

---

## Ollama

Review periodically for updates.

---

# 12. Logging and Monitoring

## System Logs

View recent logs:

```bash
journalctl -xe
```

---

## SSH Logs

```bash
journalctl -u ssh
```

---

## Firewall Logs

Review nftables logging configuration if enabled.

---

# 13. Backup Security

## Protected Data

Backup:

- Configuration files
- AI applications
- Databases
- Datasets

---

## Important Configuration Files

```text
/etc/fstab
/etc/nftables.conf
/etc/ssh/sshd_config
```

---

## Recommended Backup Target

```text
/mnt/backup
```

---

# 14. Security Verification Checklist

## Authentication

- [ ] SSH password works.
- [ ] SSH key authentication configured.
- [ ] Root login disabled.
- [ ] Administrative accounts verified.

---

## Firewall

- [ ] nftables active.
- [ ] SSH restricted correctly.
- [ ] Ollama restricted correctly.
- [ ] Configuration persists after reboot.

---

## Services

- [ ] No unexpected listening ports.
- [ ] No public exposure.
- [ ] Router port forwarding disabled.

---

## Updates

- [ ] Ubuntu updated.
- [ ] NVIDIA driver verified.
- [ ] Ollama updated.

---

# 15. Incident Recovery

## Firewall Lockout

Keep an active SSH session open while testing firewall changes.

Verify access before closing the original session.

---

## SSH Failure

Access locally through:

```text
Keyboard + Monitor
```

Or use Ubuntu recovery mode if necessary.

---

## Configuration Restore

Restore from backups:

```text
/etc/nftables.conf
/etc/ssh/sshd_config
/etc/fstab
```

---

# 16. Future Improvements

## Near-Term

- Configure SSH key authentication.
- Disable password authentication.
- Enable automatic security updates.
- Improve backup automation.

---

## Long-Term

- Dedicated management VLAN.
- Tailscale remote administration.
- Centralized monitoring.
- Intrusion detection.
- Off-site backup storage.

---

# 17. Security Status Summary

| Security Control | Status |
|------------------|---------|
| SSH Installed | Yes |
| SSH Restricted | Yes |
| Firewall Enabled | Yes |
| nftables Persistent | Yes |
| Ollama Restricted | Yes |
| Public Port Forwarding | No |
| Local-Only Architecture | Yes |
| System Updates Applied | Yes |
| SSH Key Authentication | Enabled |
| Automated Backups | Pending |