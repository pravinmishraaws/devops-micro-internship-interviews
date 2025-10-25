---
id: Q1901
title: "How do you debug a container that cannot reach the internet?"
difficulty: medium
week: 1
topics: [docker, networking, containers]
tags: [troubleshooting, docker-networking, connectivity, containers]
author: YourGitHubUsername
reviewed: false
---

## Question
A container cannot reach the internet, but the host can. What steps would you take to debug this?

## Short Answer
- Test if the container can ping external IPs like `8.8.8.8` versus domain names to determine if it's a DNS or routing issue, and verify the network mode with `docker inspect`.
- Confirm IP forwarding is enabled on the host (`cat /proc/sys/net/ipv4/ip_forward` should show 1) and check if firewall rules are blocking container traffic with `iptables -L -n -v`.
- Inspect the container's network configuration with `docker network inspect bridge` to ensure it has a valid IP, gateway, and proper routing with `ip route` from inside the container.

## Deep Dive

**Understanding Container Networking:**

Docker containers typically use bridge networking by default, where the host acts as a router/NAT gateway. When a container can't reach the internet but the host can, the issue is usually in the network path between them.

**Step 1: Isolate DNS vs. Connectivity:**

First, determine if this is a DNS resolution problem or actual connectivity issue:
```bash
# Test IP connectivity (bypasses DNS)
docker exec <container_name> ping -c 4 8.8.8.8

# Test DNS resolution
docker exec <container_name> ping -c 4 google.com

# Check container's DNS settings
docker exec <container_name> cat /etc/resolv.conf
```

If IP works but DNS doesn't, the problem is DNS configuration. If neither works, it's a routing/firewall issue.

**Step 2: Verify Network Configuration:**

Check the container's network mode and settings:
```bash
# View container network details
docker inspect <container_name> | grep -A 20 NetworkSettings

# Check which network the container is using
docker inspect <container_name> | grep NetworkMode

# Inspect the bridge network
docker network inspect bridge
```

Ensure the container has a valid IP address, gateway, and is connected to the correct network.

**Step 3: Check Host IP Forwarding:**

For containers to reach the internet through the host, IP forwarding must be enabled:
```bash
# Check if IP forwarding is enabled (should return 1)
cat /proc/sys/net/ipv4/ip_forward

# If it's 0, enable it temporarily
sudo sysctl -w net.ipv4.ip_forward=1

# Make it permanent
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
```

**Step 4: Verify Firewall/iptables Rules:**

Docker creates iptables rules for NAT. Check if they're intact:
```bash
# View NAT rules
sudo iptables -t nat -L -n -v

# Check FORWARD chain
sudo iptables -L FORWARD -n -v

# Check if docker chains exist
sudo iptables -L DOCKER -n -v
```

If rules are missing, restart the Docker daemon: `sudo systemctl restart docker`

**Step 5: Test Routing from Container:**

Get inside the container and check routing:
```bash
# Enter container shell
docker exec -it <container_name> sh

# Check routing table
ip route

# Test connectivity to gateway
ping <gateway_ip>
```

**Common DNS Issues:**

If DNS is the problem, you can specify custom DNS servers:
```bash
# Run container with custom DNS
docker run --dns 8.8.8.8 --dns 8.8.4.4 <image>

# Or set in daemon.json
echo '{"dns": ["8.8.8.8", "8.8.4.4"]}' | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker
```

## Pitfalls / Gotchas

- **Assuming DNS is the problem**: Always test with IP addresses first (like `ping 8.8.8.8`) to isolate whether it's DNS or actual connectivity—many people waste time troubleshooting DNS when routing is broken.
- **Network mode confusion**: Containers using `--network=none` or `--network=host` behave differently—`none` has no network access, while `host` uses the host's network directly and shouldn't have this issue.
- **Forgetting to restart Docker after changes**: Changes to `/etc/docker/daemon.json` or iptables configuration often require restarting the Docker daemon to take effect.
- **Corporate firewalls and proxies**: In enterprise environments, the host might require a proxy to reach the internet, which needs to be configured in the container with `HTTP_PROXY` environment variables.

## References
- https://docs.docker.com/network/
- https://docs.docker.com/network/bridge/
- https://docs.docker.com/config/containers/container-networking/
