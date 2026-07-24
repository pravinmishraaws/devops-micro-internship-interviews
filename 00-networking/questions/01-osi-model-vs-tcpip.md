---
id: 1
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

## From the Project

The Petclinic Platform runs inside a custom AWS VPC, where every layer of the OSI model plays a role:

- **Application layer:** Route 53 resolves the public domain to the ALB; Spring Boot services communicate via HTTP on internal ports
- **Transport layer:** The ALB terminates TLS (port 443) and forwards HTTP to pods on port 8080
- **Network layer:** VPC routing tables and security groups control east-west traffic between EKS pods and RDS
- **Link layer:** AWS manages the underlying Ethernet fabric across Availability Zones

When debugging pod connectivity issues on EKS, the same top-down approach applies — start at DNS, verify the service endpoint resolves, then check the TCP handshake to the target pod.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
