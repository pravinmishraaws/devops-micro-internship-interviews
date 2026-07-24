---
id: 3
title: Resource requests and limits — what they mean and how to set them
difficulty: medium
week: 10
topics: [kubernetes, resources, scheduling, qos]
tags: [requests, limits, cpu, memory, qos, oom, scheduling]
author: pravinmishraaws
reviewed: true
---

## Question
What is the difference between resource requests and limits in Kubernetes? How do requests affect scheduling, and what happens when a pod exceeds its memory limit?

## Short Answer
Requests are what the scheduler uses to find a node — a pod is only placed on a node that has at least that much free capacity. Limits are the ceiling — CPU is throttled when a container exceeds its limit, and the container is killed (OOMKilled) if it exceeds its memory limit.

## Deep Dive
**Requests — scheduling guarantee:**
- The scheduler sums up the requests of all pods on a node and only places a new pod where the remaining capacity meets the request
- The actual CPU/memory used at runtime can be higher or lower than the request
- Setting no request means the scheduler sees the pod as zero-cost — it can be placed anywhere, even on a node with no real capacity

**Limits — runtime ceiling:**
- CPU: throttled at the limit — the process slows down but is not killed
- Memory: if a container allocates more memory than its limit, the Linux kernel OOM killer terminates the container process — Kubernetes shows `OOMKilled` in `kubectl describe pod`
- Setting no limit means the container can consume all available memory on the node, starving other pods

**QoS classes (Kubernetes assigns automatically):**
| Class | Rule | Eviction Priority |
|---|---|---|
| Guaranteed | request == limit for CPU and memory | Evicted last |
| Burstable | request < limit, or only one is set | Middle |
| BestEffort | No requests or limits set | Evicted first |

Under node memory pressure, Kubernetes evicts BestEffort pods first, then Burstable, then Guaranteed.

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

**Vertical Pod Autoscaler (VPA)** can observe actual usage over time and recommend or automatically adjust requests and limits — useful when you do not know the right values at deployment time.

## Pitfalls
- Setting limits without requests — Kubernetes defaults the request to the limit, making the pod Guaranteed class. The scheduler is more conservative than it needs to be.
- Setting memory limits too low — JVM services resize their heap at startup based on available memory; a 256Mi limit can cause constant OOMKills before the app serves a single request
- Setting no limits at all — one misbehaving pod can consume all node memory and evict everything else
- Confusing `m` (millicores) for CPU and `Mi` (mebibytes) for memory — `500m` CPU is 0.5 cores; `500M` memory is 500 megabytes, not mebibytes

## References
- [Kubernetes Docs — Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes Docs — Quality of Service for Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)

## From the Project

The Petclinic microservices run on `t4g.small` ARM/Graviton nodes — 2 vCPU and 2 GiB memory per node. With eight services plus system pods, resource sizing has to be precise.

Each Spring Boot service in the Petclinic Platform is configured with:
- **Memory limit: 512Mi** — matches the `eclipse-temurin:17` Docker image memory constraint set in `docker/Dockerfile`. The JVM is configured to not exceed this boundary.
- **Dev environment:** single replica per service, lower requests to fit more services per node
- **Prod environment:** 2+ replicas with slightly higher requests to guarantee scheduling stability

The `k8s/overlays/dev/` and `k8s/overlays/prod/` directories override the base resource values using Kustomize patches — dev and prod have different resource profiles from the same base manifests.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
