# SSH Service

## Server

| Property | Value |
|-----------|---------|
| Service | OpenSSH |
| Port | 22 |
| Authentication | SSH Key |
| Socket Activation | Enabled |

## Administrative Connection

Primary connection method:

```bash
ssh ai-server
```

Client SSH configuration:

```sshconfig
Host ai-server
    HostName 192.168.0.178
    User maddodvapeur
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

## Notes

- Host alias simplifies administration.
- Ed25519 key is used for authentication.
- Password authentication remains available for recovery.
- VS Code Remote SSH uses this configuration.