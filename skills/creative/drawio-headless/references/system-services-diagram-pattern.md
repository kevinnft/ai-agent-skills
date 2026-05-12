# System Services Diagram Pattern

Pattern for mapping running services to comprehensive architecture diagrams.

## Data Collection Commands

```bash
# List all active systemd services
systemctl list-units --type=service --state=running --no-pager

# List all processes sorted by memory
ps aux --sort=-%mem

# List listening ports with process info
sudo ss -tulpn

# List systemd timers
systemctl list-timers --no-pager

# Check screen sessions
screen -ls

# Check cron jobs
crontab -l
```

## Diagram Structure

### Layer 1: User Services
- User-level processes (non-root)
- Screen/tmux sessions
- User systemd instance
- SSH sessions

### Layer 2: System Services
Group by function:
- **Core System**: systemd, journald, udevd, logind
- **Network**: networkd, resolved, sshd, chrony, dispatcher
- **Utilities**: snapd, dbus, polkit, rsyslog, cron, unattended-upgrades
- **Hardware**: udisks, ModemManager, upower, getty, at-spi

### Layer 3: Listening Ports
Map ports to services with arrows showing relationships.

## Color Coding

- **Red (#f8cecc)**: Primary user services (high memory)
- **Yellow (#fff2cc)**: Secondary services, API proxies
- **Green (#d5e8d4)**: Active/healthy services
- **Blue (#dae8fc)**: System services
- **Orange (#ffe6cc)**: Utilities, background services
- **Purple (#e1d5e7)**: Child processes, details

## Key Information to Include

For each service:
- Full name (not just binary name)
- PID
- Memory usage (MB + %)
- CPU usage (%)
- Start time / uptime
- Parent process (PPID)
- Command line
- Listening ports (if applicable)
- Status (running, sleeping, etc.)

## Example: enowxai Daemon Entry

```
enowxai Daemon
PID: 115828
Memory: 143 MB (7.2%)
CPU: 0.6%
Started: May 01 00:17:40
Runtime: 2 days 12 hours
Parent: systemd --user (PID 3240)
Status: Running (Ssl)
Ports: 1430 (API), 1431 (Dashboard)
Purpose: AI API proxy with credential pooling
```

## Snap Confinement Note

When working with snap-installed services (like draw.io), remember:
- Snap processes may have restricted file access
- Use home directory for diagram generation
- Snap services show as `/snap/<name>/current/...` in process list
