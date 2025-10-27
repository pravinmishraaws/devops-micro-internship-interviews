---
id: Q1901
title: "How do you debug a container that cannot reach the internet?"
difficulty: medium
week: 01
topics: [docker, networking, containers]
tags: [troubleshooting, docker-networking, connectivity, containers]
author: nkydigitech
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
