---
id: Q0101
title: How do you diagnose a slow server using Linux commands?
difficulty: medium
week: 01
topics: [Linux, System Administration, Performance]
tags: [troubleshooting, diadnosics, performance-monitoring]
author: nkydigitech
reviewed: false
---

## Question
A server is running slowly. Walk me through your systematic approach to diagnose the issue using Linux commands.

## Short Answer
- Start with `top` or `htop` to check CPU and memory usage, identifying which processes are consuming the most resources.
- Run `iostat -x 1` to see if disk I/O is the bottleneck, looking for high %util values or long await times.
- Check system logs with `dmesg | tail` and `journalctl -xe` for errors, verify disk space with `df -h`, and confirm swap usage isn't excessive using `free -h`.

## Deep Dive

**Initial Resource Assessment:**

When a server runs slowly, start with a top-down approach. The `top` or `htop` commands provide real-time views of CPU usage, memory consumption, and running processes. Look for processes with high %CPU or %MEM values—these are your primary suspects.

**Disk I/O Investigation:**

Disk bottlenecks are common culprits for slow performance. Use `iostat -x 1` to monitor disk statistics every second. Key metrics include:
- `%util`: Percentage of time the disk was busy (>80% indicates saturation)
- `await`: Average wait time for I/O requests (high values mean slow disk)
- `r/s` and `w/s`: Read and write operations per second

For more detailed process-level I/O analysis, use `iotop` to see which processes are generating disk activity.

**Network and Connection Analysis:**

Check for network-related slowness with `netstat -tulpn` or the more modern `ss -tulpn` to view active connections. Use `ss -s` for summary statistics. If you see an unusual number of connections in TIME_WAIT or ESTABLISHED states, you might have a networking issue or application problem.

**System Logs and Health:**

Review system logs for hardware errors, kernel issues, or service failures:
- `dmesg | tail`: Recent kernel messages (hardware errors, driver issues)
- `journalctl -xe`: Systemd service logs with recent errors
- `/var/log/syslog` or `/var/log/messages`: General system logs

**Additional Diagnostics:**

- `vmstat 1`: Virtual memory statistics, showing CPU, memory, and I/O stats
- `free -h`: Memory usage including swap (high swap usage indicates memory pressure)
- `df -h`: Disk space usage (full disks cause major performance issues)
- `uptime`: Shows load average and how long the system has been running

## Pitfalls

- **Snapshot vs. Trend**: Running commands once gives you a snapshot; for intermittent issues, use monitoring tools or run commands in a loop to catch patterns over time.
- **Ignoring Load Average Context**: A load of 5.0 means different things on a 2-core vs. 16-core system—always compare load to available CPU cores.
- **Overlooking Swap Thrashing**: If swap usage is high and constantly changing, the system is thrashing (swapping pages in/out rapidly), which severely degrades performance—add more RAM or reduce memory usage.
- **Missing the Obvious**: Always check `df -h` first—a full disk (especially root partition) causes cascading failures and slow performance across the entire system.
- **Not Checking Historical Data**: If available, review historical metrics (sar, monitoring tools) to see if this is a new issue or recurring pattern.

## References

- [Linux Performance Analysis in 60 Seconds](https://netflixtechblog.com/linux-performance-analysis-in-60-000-milliseconds-accc10403c55)
- [htop Documentation](https://htop.dev/)
- [iostat Man Page](https://man7.org/linux/man-pages/man1/iostat.1.html)
- [Brendan Gregg's Linux Performance Tools](https://www.brendangregg.com/linuxperf.html)

File name: Q0801-diagnose-slow-server-linux.md

Save location: weeks/8/questions/Q0801-diagnose-slow-server-linux.md

Ready for Question 2?


