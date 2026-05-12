# Windows Port Restrictions

## Reserved Port Ranges

Windows reserves certain port ranges for system services. User applications cannot bind to these ports.

### Dynamic Port Range (Ephemeral Ports)

Default range varies by Windows version:
- **Windows 10/11**: 49152-65535 (IANA standard)
- **Windows Server 2008+**: 49152-65535
- **Older Windows**: 1025-5000

Check current range:
```powershell
netsh int ipv4 show dynamicport tcp
netsh int ipv4 show dynamicport udp
```

### Hyper-V Reserved Ports

When Hyper-V or WSL2 is enabled, Windows reserves additional port ranges for NAT and virtual networking.

Check excluded ranges:
```powershell
netsh int ipv4 show excludedportrange protocol=tcp
```

Example output:
```
Protocol tcp Port Exclusion Ranges

Start Port    End Port
----------    --------
      1430        1430      *
      5357        5357
     50000       50059      *
```

Ports marked with `*` are reserved by Hyper-V and **cannot be used** by user applications.

## Common Error Messages

### "An attempt was made to access a socket in a way forbidden by its access permissions"

**Cause**: Port is in a reserved range or excluded by Hyper-V.

**Fix**: Use a different port (8000-9000 is usually safe).

### "Only one usage of each socket address is normally permitted"

**Cause**: Another process is already using the port.

**Diagnosis**:
```powershell
netstat -ano | findstr :PORT
Get-Process -Id PID
```

**Fix**: Kill the process or use a different port.

## Safe Port Ranges

Recommended port ranges for local AI services:

- **8000-8999**: HTTP services (Ollama default: 11434, but 8000-8999 safer)
- **9000-9999**: Alternative HTTP services
- **3000-3999**: Development servers (Next.js, React, etc.)
- **5000-5999**: Flask, FastAPI (but check for conflicts)

**Avoid**:
- **1-1023**: Well-known ports (require admin privileges)
- **1024-5000**: Often used by Windows services
- **49152-65535**: Dynamic port range (ephemeral)
- **Any port in `netsh excludedportrange` output**

## Troubleshooting Workflow

1. **Check if port is in use**:
   ```powershell
   netstat -ano | findstr :PORT
   ```

2. **Check if port is reserved**:
   ```powershell
   netsh int ipv4 show excludedportrange protocol=tcp
   ```

3. **If reserved by Hyper-V**: Use a different port (don't try to unreserve)

4. **If used by another process**:
   - Identify: `Get-Process -Id PID`
   - If it's your service: kill and restart
   - If it's `svchost` or system service: use a different port

5. **If still failing**: Try running PowerShell as Administrator (some ports require elevated privileges)

## WSL2-Specific Notes

WSL2 uses Hyper-V networking, which reserves additional ports. The reserved ranges can change after Windows updates or reboots.

**Best practice**: Always check `excludedportrange` before choosing a port for services that need WSL2 access.

## Example: enowxai Port Conflict

**Scenario**: enowxai tries to bind to port 1430 but crashes with "access forbidden" error.

**Diagnosis**:
```powershell
PS> netstat -ano | findstr :1430
  TCP    127.0.0.1:1430    ...    ESTABLISHED    4636

PS> Get-Process -Id 4636
Name      Id
----      --
svchost   4636

PS> netsh int ipv4 show excludedportrange protocol=tcp
Start Port    End Port
----------    --------
      1430        1430      *
```

**Conclusion**: Port 1430 is reserved by Hyper-V (indicated by `*`). Cannot be used.

**Solution**: Use port 8430 instead:
```powershell
enowxai start --port 8430 --dashboard-port 8431
```

**Verify**:
```powershell
PS> netstat -ano | findstr :8430
  TCP    0.0.0.0:8430    ...    LISTENING    5678

# From WSL2
$ curl http://$(ip route show default | awk '{print $3}'):8430/v1/models
```
