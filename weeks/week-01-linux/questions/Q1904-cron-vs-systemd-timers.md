---
id: Q1904
title: "What's the difference between cron and systemd timers?"
difficulty: medium
week: 01
topics: [linux, scheduling, automation]
tags: [cron, systemd, timers, task-scheduling]
author: nkydigitech
reviewed: false
---

## Question
What's the difference between cron and systemd timers? When would you choose one over the other?

## Short Answer
- Cron is simpler with straightforward time-based scheduling (`* * * * *` syntax) and works well for basic periodic tasks, but offers limited logging and no dependency management.
- Systemd timers provide advanced features like monotonic scheduling (run after boot), automatic logging to journald, and the ability to depend on other services, making them better for complex system tasks.
- Choose cron for simple scheduled scripts like backups or log rotation; use systemd timers when you need service dependencies, boot-relative timing, or centralized logging.

## Deep Dive

**Cron Overview:**

Cron has been the traditional Unix/Linux task scheduler for decades. It's simple, well-understood, and widely supported.

**Cron syntax:**
```bash
# Edit user crontab
crontab -e

# Format: minute hour day month weekday command
# Example: Run backup daily at 2:30 AM
30 2 * * * /usr/local/bin/backup.sh

# Common patterns:
0 * * * *     # Every hour
*/15 * * * *  # Every 15 minutes
0 0 * * 0     # Weekly on Sunday at midnight
0 2 1 * *     # Monthly on 1st at 2 AM
```

**Systemd Timers Overview:**

Systemd timers are the modern approach, integrated with systemd's service management.

**Basic systemd timer setup:**

1. Create a service unit (`/etc/systemd/system/backup.service`):
```ini
[Unit]
Description=Daily Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
```

2. Create a timer unit (`/etc/systemd/system/backup.timer`):
```ini
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=02:30
Persistent=true

[Install]
WantedBy=timers.target
```

3. Enable and start:
```bash
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
```

**Key Differences:**

| Feature | Cron | Systemd Timers |
|---------|------|----------------|
| Syntax | Traditional (`* * * * *`) | Calendar expressions |
| Logging | Limited (mail/syslog) | Integrated with journald |
| Dependencies | None | Can depend on services |
| Missed runs | Skipped if system down | Can catch up with `Persistent=true` |
| Resource control | None | Full systemd controls (CPU, memory limits) |
| Boot-relative timing | No | Yes (`OnBootSec`, `OnStartupSec`) |

**Advanced Systemd Timer Features:**
```ini
# Run 5 minutes after boot
OnBootSec=5min

# Run 10 minutes after service last ran
OnUnitActiveSec=10min

# Randomize start time (useful for load distribution)
RandomizedDelaySec=30min

# Run only if AC power available
ConditionACPower=true
```

**Viewing and Managing:**
```bash
# Cron
crontab -l                    # List user cron jobs
sudo crontab -u user -l       # List another user's jobs
grep CRON /var/log/syslog     # View cron logs

# Systemd timers
systemctl list-timers         # List all timers
systemctl status backup.timer # Check timer status
journalctl -u backup.service  # View service logs
systemctl cat backup.timer    # View timer configuration
```

**When to Use Cron:**
- Simple time-based scheduling
- Legacy systems without systemd
- User-level tasks (in user crontabs)
- Quick and simple automation
- When team is more familiar with cron syntax

**When to Use Systemd Timers:**
- Need service dependencies (run after network is up)
- Want integrated logging
- Need resource control (CPU/memory limits)
- Boot-relative scheduling required
- System-level services on modern Linux
- Want better failure handling and retries

## Pitfalls / Gotchas

- **Cron environment differs from shell**: Cron runs with minimal environment variables—always use full paths and set PATH explicitly in crontab or scripts.
- **Forgetting to enable timer**: Creating a systemd timer unit isn't enough—you must `systemctl enable` and `start` it, unlike cron which auto-loads from crontab.
- **Systemd timer/service name mismatch**: Timer file must match service name (`backup.timer` controls `backup.service`)—mismatched names won't work.
- **Persistent flag confusion**: `Persistent=true` in systemd timers runs missed jobs after downtime, which can cause unexpected behavior if the job shouldn't run multiple times.
- **Cron logging gaps**: By default, cron only logs job starts, not output—redirect output to files or use logger for debugging: `command >> /var/log/myjob.log 2>&1`

## References
- https://man7.org/linux/man-pages/man5/crontab.5.html
- https://www.freedesktop.org/software/systemd/man/systemd.timer.html
- https://wiki.archlinux.org/title/Systemd/Timers
- https://crontab.guru/ (Cron expression tester)
