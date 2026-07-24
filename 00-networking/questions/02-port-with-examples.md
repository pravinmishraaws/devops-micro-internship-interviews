---
id: 2
title:  Understanding Ports — what they are and why they matter
difficulty: entry
week: 00
topics: [networking, transport]
tags: [tcp, udp, ports, networking]
author: Hajarat Akande
reviewed: false
---

## Question
What are ports in networking, and how do they help different applications communicate over the Internet?

## Short Answer
- A **port** identifies a specific process or service on a host.
- IP = location of the device; Port = door for a specific service.
- Example:  
  - HTTP → TCP **port 80**  
  - HTTPS → TCP **port 443**  
  - DNS → UDP **port 53**
- Together with IP and protocol, it forms a **socket** (e.g., `192.168.1.10:80`).

## Deep Dive
- Ports range from **0–65535**:
  - **Well-known (0–1023):** system services (`22=SSH`, `25=SMTP`)
  - **Registered (1024–49151):** user apps (`3306=MySQL`, `8080=Alt HTTP`)
  - **Ephemeral (49152–65535):** temporary client connections  
- Tools:  
  - `netstat -tuln` → list open ports  
  - `telnet <ip> <port>` or `nc -zv <ip> <port>` → check port access  
  - `ss -ltnp` → find which service is using a port  
- Example flow:
  - Browser → connects to `example.com:443`
  - Server → listens on TCP 443  
  - If blocked by firewall, connection fails.
## Pitfalls
- Forgetting to open ports in **security groups/firewalls**.
- Confusing **TCP vs UDP** ports (e.g., DNS uses UDP, but zone transfers use TCP).
- Assuming same port can serve multiple apps on one IP (unless using different protocols or IPs).

## References
- https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
## From the Project

Every service in the Petclinic Platform exposes a specific port — and security groups allow only those ports, nothing else:

| Service | Port | Notes |
|---|---|---|
| API Gateway | 8080 | Internal; ALB forwards 443 → 8080 |
| Config Server | 8888 | Must start first; all services depend on it |
| Discovery Server | 8761 | Eureka registry |
| Customers / Visits / Vets | 8081–8083 | Spring Boot, MySQL backend |
| RDS MySQL | 3306 | Allowed only from EKS node security group |
| Prometheus | 9090 | Scraped by Grafana inside the cluster |

Understanding which port each service uses — and why — is the difference between an engineer who deployed it and one who just read the docs.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
