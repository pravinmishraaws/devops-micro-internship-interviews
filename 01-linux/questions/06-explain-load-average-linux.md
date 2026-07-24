---
id: 6
title: "What does load average mean in Linux?"
difficulty: easy
week: 01
topics: [linux, performance, monitoring]
tags: [load-average, performance-monitoring, system-metrics]
author: nkydigitech
reviewed: false
---

## Question
Explain load average in Linux. What do the three numbers represent, and what's considered "high"?

## Short Answer
- The three numbers represent the average number of processes waiting for CPU time over the last 1, 5, and 15 minutes, showing short-term, medium-term, and long-term load trends.
- A "high" load depends on your CPU count—a load of 1.0 per core means full utilization, so 4.0 on a 4-core system is at capacity, while 8.0 means processes are queuing.
- If the 1-minute load is high but 15-minute is low, it's a temporary spike; if all three are consistently high, you have a sustained performance problem that needs investigation.

## Deep Dive

**Understanding Load Average:**

Load average represents the number of processes in a runnable or uninterruptible state. This includes:
- Processes actively using the CPU
- Processes waiting for CPU time
- Processes waiting for I/O operations (disk, network)

**The Three Numbers:**

When you run `uptime` or `top`, you see three load average numbers:
```bash

## From the Project

On the Petclinic Platform's t4g.small EKS nodes (2 vCPU each), load average is a meaningful signal:

- Load average above 2.0 on a 2-vCPU node means the run queue is backed up — pods start experiencing latency
- Karpenter monitors pending pods (not load average directly), but sustained high CPU on existing nodes is often what causes pods to become unschedulable in the first place
- `kubectl top nodes` shows CPU usage percentage; Grafana shows the underlying trend over time

In practice: if a node consistently runs above 80% CPU, Karpenter provisions a new node and the scheduler redistributes pending pods automatically.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
