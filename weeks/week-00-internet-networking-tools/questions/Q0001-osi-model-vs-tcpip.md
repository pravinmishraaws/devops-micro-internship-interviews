---
id: Q0001
title: OSI vs TCP/IP — what’s the practical difference?
difficulty: entry
week: 00
topics: [networking, models]
tags: [networking, osi, tcpip]
author: pravinmishraaws
reviewed: false
---

## Question
Compare OSI and TCP/IP models and explain how they map to real-world troubleshooting.

## Short Answer
- OSI is a teaching model (7 layers); TCP/IP is pragmatic (4–5 layers) used on the Internet.
- Map examples: DNS (app), TCP/UDP (transport), IP (network), Ethernet/Wi‑Fi (link).
- Troubleshoot top→down or bottom→up; verify each layer (DNS, TCP handshake, routing, link).

## Deep Dive
- Mapping table, typical tools: `ping`, `traceroute`, `dig`, `curl`, `tcpdump`.

## Pitfalls
- Confusing DNS failures (app) with network reachability (IP/route).

## References
- https://datatracker.ietf.org/doc/html/rfc1122
