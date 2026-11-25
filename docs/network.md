# Network Configuration

**Project:** Home AI Infrastructure  
**System:** ai-server  
**Last updated:** 2026-11-24

---

# 1. Network Overview

## Purpose

The Ubuntu AI server operates as a local inference server accessible from the development workstation over the home network.

The server:

- Accepts SSH connections from the development workstation.
- Accepts Ollama API requests from the development workstation.
- Is not exposed to the public Internet through port forwarding.
- Uses nftables to restrict inbound access.

---

# 2. Physical Connectivity

## Development Workstation

| Parameter | Value |
|------------|---------|
| Role | Main development workstation |
| Connection | Wi-Fi |
| Operating System | Windows |
| IPv4 Address | 192.168.0.87 |

---

## AI Server

| Parameter | Value |
|------------|---------|
| Hostname | ai-server |
| Role | Local AI inference server |
| Connection | Ethernet |
| Interface | enp8s0 |
| Link Speed | 1 Gbps |
| IPv4 Address | 192.168.0.178 |

---

## Router

| Parameter | Value |
|------------|---------|
| Device | Fizz Hitron CODA-4680 |
| Address | 192.168.0.1 |
| Function | Gateway, DHCP, DNS |

---

# 3. Current Addressing

## IPv4

| Device | Address |
|----------|---------|
| Router | 192.168.0.1 |
| Development Workstation | 192.168.0.87 |
| AI Server | 192.168.0.178 |

---

## Network Parameters

| Parameter | Value |
|------------|---------|
| Network | 192.168.0.0/24 |
| Subnet Mask | 255.255.255.0 |
| Gateway | 192.168.0.1 |
| Address Assignment | DHCP Reservation |

---

## DHCP Reservation

| Parameter | Value |
|------------|---------|
| Status | Configured |
| Reserved Address | 192.168.0.178 |
| Device | ai-server |

The router reserves the AI server's IP address using the Ethernet adapter MAC address.

---

# 4. IPv6 Configuration

## Status

IPv6 is enabled.

The server receives IPv6 configuration automatically from the router.

---

## Verification Status

| Item | Status |
|---------|---------|
| IPv6 Address Assigned | Verified |
| Default Route Present | Verified |
| External Connectivity | Verified |

---

## Notes

No static IPv6 configuration is currently required.

---

# 5. Network Topology

```text
                Internet
                    |
                    |
        +-----------------------+
        |  Fizz CODA-4680       |
        |  192.168.0.1          |
        +-----------+-----------+
                    |
            Home LAN Switch
                    |
        +-----------+-----------+
        |                       |
        |                       |
Development Workstation     AI Server
192.168.0.87               192.168.0.178
Wi-Fi                      Ethernet
```

---

# 6. Network Services

## Services Running on AI Server

| Service | Port | Protocol | Purpose |
|-----------|------|-----------|---------|
| SSH | 22 | TCP | Server administration |
| Ollama API | 11434 | TCP | Local model inference |

---

## Public Exposure

| Service | Internet Accessible |
|-----------|--------------------|
| SSH | No |
| Ollama API | No |

No router port forwarding is configured.

---

# 7. Access Policy

## Allowed

| Source | Destination | Port |
|-----------|------------|------|
| Development Workstation | SSH | 22 |
| Development Workstation | Ollama | 11434 |
| Established Connections | Any | Existing Sessions |

---

## Blocked

| Source | Destination |
|-----------|------------|
| Phone | AI Server |
| Other LAN Devices | AI Server |
| Internet | AI Server |

---

# 8. Firewall Policy

## Firewall System

```text
nftables
```

---

## Firewall Objectives

- Allow SSH from the development workstation.
- Allow Ollama API access from the development workstation.
- Allow established and related traffic.
- Block unauthorized inbound connections.
- Preserve IPv4 and IPv6 connectivity.
- Persist across reboot.

---

## Default Policies

| Chain | Policy |
|---------|---------|
| Input | Drop |
| Forward | Drop |
| Output | Accept |

---

# 9. DNS Configuration

## Current Configuration

DNS services are supplied by the router.

```text
192.168.0.1
```

The router forwards requests to its configured upstream DNS providers.

---

# 10. Connectivity Verification

## Local Connectivity

| Test | Status |
|---------|---------|
| Server ↔ Router | Verified |
| Workstation ↔ Server | Verified |
| SSH Access | Verified |
| Ollama API Access | Verified |

---

## Internet Connectivity

| Test | Status |
|---------|---------|
| IPv4 Connectivity | Verified |
| IPv6 Connectivity | Verified |
| Package Downloads | Verified |

---

# 11. Security Decisions

## Confirmed Decisions

- Use nftables as the primary firewall.
- No SSH exposure to the Internet.
- No Ollama exposure to the Internet.
- No UPnP dependency.
- No router port forwarding.
- Development workstation acts as the primary client.
- Future phone access should pass through the workstation rather than directly accessing the AI server.

---

# 12. Future Enhancements

## Possible Improvements

- Create local DNS hostname resolution.
- Deploy Tailscale for secure remote administration.
- Separate AI devices into a dedicated VLAN.
- Implement centralized monitoring.
- Add network intrusion logging.

---

# 13. Quick Reference

## SSH

```powershell
ssh USERNAME@192.168.0.178
```

---

## Ollama API

```text
http://192.168.0.178:11434
```

---

## Important Addresses

| Item | Address |
|---------|---------|
| Router | 192.168.0.1 |
| Development Workstation | 192.168.0.87 |
| AI Server | 192.168.0.178 |