
---
id: 2
title: Linux optimization
difficulty: easy
week: 01
topics: [linux, optimization]
tags: [linux, optimization]
author: gasufra
reviewed: false
---

## Question
How important Linux optimization for DevOps?

## Short Answer
- Performance efficiency: Optimizing CPU usage, memory consumption, Disk I/O, Network Throughput
- Realibility and uptime: Stability preventing system crash 
- Speeds means lower cost: Optimizing means savings

## Deep Dive
- `top`(System Performance), `netstat`(Networking), `systemd`(Process Management), `ext4`(Storage) 

## Pitfalls
- Optimizing without measure. Doesn't mean fast it is stable

## References
- man `top`, `systemd`, `netstat`, `ext4`

## From the Project

The Petclinic Platform runs on AWS t4g.small ARM/Graviton EKS nodes (2 vCPU, 2 GiB RAM). With eight Spring Boot microservices sharing cluster capacity, resource efficiency matters:

- Each pod is capped at 512 MiB memory limit — the same limit set in the Docker build
- JVM heap is tuned to stay within the container memory limit, preventing OOMKill events
- Karpenter provisions nodes on demand and removes them when idle — over-provisioning at the cluster level is avoided automatically

Knowing how to read node resource usage (`kubectl top nodes`, `kubectl describe node`) is how you catch a memory-starved node before it starts evicting pods.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
