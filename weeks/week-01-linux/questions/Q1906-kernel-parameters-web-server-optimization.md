---
id: Q1906
title: "How do you optimize kernel parameters for a high-traffic web server?"
difficulty: hard
week: 01
topics: [linux, performance, networking, sysctl]
tags: [kernel-tuning, performance-optimization, sysctl, web-server]
author: nkydigitech
reviewed: false
---

## Question
How would you use kernel parameters (sysctl) to optimize a web server for high traffic?

## Short Answer
- Increase `net.core.somaxconn` (to 4096+) and `net.ipv4.tcp_max_syn_backlog` (to 8192+) to allow the server to queue more incoming connections without dropping them.
- Enable `net.ipv4.tcp_tw_reuse=1` to recycle TIME_WAIT sockets faster, expand `net.ipv4.ip_local_port_range` to provide more available ports, and reduce `net.ipv4.tcp_fin_timeout` to 15-30 seconds.
- Raise `fs.file-max` (to 500000+) for more file descriptors and tune TCP buffer sizes with `net.ipv4.tcp_rmem` and `net.ipv4.tcp_wmem`, then apply with `sysctl -w` and persist in `/etc/sysctl.conf`.

## Deep Dive

**Understanding sysctl:**

Sysctl is used to modify kernel parameters at runtime without rebooting. For web servers handling high traffic, proper kernel tuning is crucial.

**Viewing and Setting Parameters:**
```bash
# View current value
sysctl net.core.somaxconn

# Set temporarily (lost on reboot)
sudo sysctl -w net.core.somaxconn=4096

# Set permanently in /etc/sysctl.conf or /etc/sysctl.d/99-custom.conf
echo "net.core.somaxconn=4096" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p

# View all parameters
sysctl -a
```

**Critical Parameters for High-Traffic Web Servers:**

**1. Connection Queue Limits:**
```bash
# Maximum queue length of pending connections
net.core.somaxconn = 4096

# Maximum number of SYN packets queued
net.ipv4.tcp_max_syn_backlog = 8192

# Maximum number of packets queued on interface
net.core.netdev_max_backlog = 5000
```

**Why:** Prevents connection drops during traffic spikes. Default values (128-512) are too low for busy servers.

**2. TCP Connection Handling:**
```bash
# Reuse sockets in TIME_WAIT state for new connections
net.ipv4.tcp_tw_reuse = 1

# Reduce TIME_WAIT timeout (default 60s)
net.ipv4.tcp_fin_timeout = 30

# Enable TCP fast open (reduces handshake latency)
net.ipv4.tcp_fastopen = 3

# Disable slow start after idle
net.ipv4.tcp_slow_start_after_idle = 0
```

**Why:** Faster socket recycling means more connections can be handled without exhausting ports.

**3. Port Range:**
```bash
# Expand ephemeral port range for outbound connections
net.ipv4.ip_local_port_range = 10000 65535
```

**Why:** Default range (32768-60999) provides ~28k ports. Expanding gives ~55k ports for outbound connections.

**4. File Descriptor Limits:**
```bash
# System-wide file descriptor limit
fs.file-max = 500000

# Per-process limits (also set in /etc/security/limits.conf)
# * soft nofile 100000
# * hard nofile 100000
```

**Why:** Each connection uses a file descriptor. Default limits (1024-4096) are insufficient for high-traffic servers.

**5. TCP Memory and Buffer Sizes:**
```bash
# TCP receive buffer: min, default, max (in bytes)
net.ipv4.tcp_rmem = 4096 87380 16777216

# TCP send buffer: min, default, max (in bytes)
net.ipv4.tcp_wmem = 4096 65536 16777216

# Maximum TCP buffer size
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216

# TCP memory allocation (pages): min, pressure, max
net.ipv4.tcp_mem = 65536 131072 262144
```

**Why:** Larger buffers improve throughput, especially for high-bandwidth connections.

**6. Connection Tracking:**
```bash
# Maximum number of tracked connections (for firewalls/NAT)
net.netfilter.nf_conntrack_max = 262144

# Connection timeout values
net.netfilter.nf_conntrack_tcp_timeout_established = 600
```

**Why:** Important if using iptables/netfilter. Default limits can cause "table full, dropping packet" errors.

**7. Security and Protection:**
```bash
# SYN flood protection
net.ipv4.tcp_syncookies = 1

# Number of SYN retries
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_synack_retries = 2

# Disable ICMP redirects (security)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
```

**Complete Example Configuration:**

Create `/etc/sysctl.d/99-webserver-tuning.conf`:
```bash
# Connection handling
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 8192
net.core.netdev_max_backlog = 5000

# TCP tuning
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_slow_start_after_idle = 0

# Port range
net.ipv4.ip_local_port_range = 10000 65535

# File descriptors
fs.file-max = 500000

# Buffer sizes
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216

# Security
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_syn_retries = 2

# Apply with:
# sudo sysctl -p /etc/sysctl.d/99-webserver-tuning.conf
```

**Monitoring Impact:**
```bash
# Check connection states
ss -s

# Monitor dropped connections
netstat -s | grep -i drop

# Watch socket usage
watch -n 1 'cat /proc/net/sockstat'

# Monitor file descriptor usage
lsof | wc -l
cat /proc/sys/fs/file-nr
```

## Pitfalls / Gotchas

- **Setting values too high without enough RAM**: Large TCP buffers consume memory—on a system with limited RAM, excessively large buffers can cause OOM (Out of Memory) kills.
- **Enabling tcp_tw_recycle**: **Never use `net.ipv4.tcp_tw_recycle=1`** as it breaks connections behind NAT and was removed in Linux 4.12—use `tcp_tw_reuse` instead.
- **Not testing changes under load**: Always test kernel parameter changes under realistic load conditions—what works in testing might behave differently in production.
- **Forgetting application-level limits**: Kernel tuning is useless if your web server (nginx, Apache) has its own connection limits—ensure application configs match kernel settings.
- **Ignoring monitoring**: After tuning, monitor metrics like connection drops, retransmits, and TIME_WAIT sockets to verify improvements—use `netstat -s` and application logs.
- **One-size-fits-all approach**: Optimal values depend on your workload, hardware, and traffic patterns—start conservative and tune based on monitoring data.

## References
- https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt
- https://www.brendangregg.com/blog/2021-09-06/system-performance-tuning.html
- https://www.nginx.com/blog/tuning-nginx/
- https://man7.org/linux/man-pages/man8/sysctl.8.html
