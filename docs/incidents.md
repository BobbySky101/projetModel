## Incident: Loss of Remote Access

### Symptoms

- SSH connections failed.
- Router no longer displayed the server as connected.
- The server could still be accessed locally.

### Root Cause

The Ethernet cable was not fully connected.

### Observations

- Interface enp8s0 was in the DOWN state.
- No DHCP lease was assigned.
- No IPv4 address was present.

### Resolution

The Ethernet connection was reseated.

### Lesson Learned

When SSH suddenly becomes unavailable, verify basic network connectivity before troubleshooting authentication, firewall rules, or SSH configuration.