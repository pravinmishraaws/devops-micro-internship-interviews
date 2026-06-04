---
id: Q0001
title: OSI vs TCP/IP — what's the practical difference?
difficulty: hard
week: 00
topics: [networking, models]
tags: [networking, osi, tcpip]
author: JulietChinenyeDuru
reviewed: false
---

## Short Answer
The OSI model is a 7-layer conceptual framework used for teaching and troubleshooting, while TCP/IP is the 4-layer practical model that actually governs internet communication. In real-world DevOps, you debug at TCP/IP layers but reason about problems using OSI terminology.

## Deep Dive
OSI layers (Physical → Data Link → Network → Transport → Session → Presentation → Application) give you a precise language for isolating faults — e.g. "is this a Layer 3 routing issue or a Layer 4 connection issue?" TCP/IP collapses these into Network Access, Internet, Transport, and Application.

Practically:
- `ping` operates at Layer 3 (ICMP/Network)
- `telnet host 443` tests Layer 4 connectivity
- `curl -v` reveals Layer 7 (HTTP/Application) behaviour
- Tools like Wireshark let you inspect all layers simultaneously

In Kubernetes networking, CNI plugins (Calico, Flannel) operate at Layer 3/4, while Ingress controllers operate at Layer 7. Misidentifying the layer wastes hours of debugging.

## Pitfalls
- Assuming TCP/IP and OSI are interchangeable models — OSI is conceptual, TCP/IP is implemented
- Forgetting that TLS sits between Layer 4 and 7 (sometimes called Layer 5/6 in OSI terms), causing confusion when debugging mTLS issues in service meshes
- Using `ping` to confirm a service is up — it only confirms Layer 3 reachability, not that the application is healthy

## References
- https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/
- https://datatracker.ietf.org/doc/html/rfc1122s
