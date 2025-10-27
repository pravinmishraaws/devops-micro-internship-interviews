---
id: Q0513
title: EpicBook Clustered Platform Migration
difficulty: entry
week: 5
topics: [azure, architecture, management]
tags: [azure, cluster, self-healing]
author: WhitneyKataka

reviewed: false
---

## Question
Hey there! So we've got EpicBook running on a single Azure server right now, and it works... most of the time. But every time we need to update the app, we have to take it offline, and users aren't happy about that. I've heard about this thing called "clustered, self-healing setups" in Azure. How would moving to that kind of setup help us roll out updates without disrupting our users? What's the actual benefit of having multiple servers working together?

## Short Answer
Moving to a clustered setup helps us run EpicBook on multiple servers at once. When we need to update the app, we can do it gradually across these servers without any downtime. If something goes wrong with one server, the others keep the app running while Azure fixes the problem. This makes our deployments much safer and faster.

## Deep Dive
When we set up clustering in Azure, we'll probably use Azure Kubernetes Service (AKS). It's like having a smart system that spreads out our users across different servers. The cool thing is that it watches these servers 24/7 - if one starts acting up, it'll automatically move users to healthy servers and try to fix or replace the problematic one.

The real game-changer is how we can update EpicBook. Instead of taking down the whole app, we update one or two servers at a time. If the new version works well, great! If not, Azure quickly switches everyone back to the old version before users notice any issues. We can automate this whole process using Azure's deployment pipelines, which means fewer late-night manual updates and fewer mistakes.

## Pitfalls
- Wrong health probes can cause the load balancer to remove healthy nodes.  
- Not versioning containers properly may lead to rollbacks failing.  
- Cluster misconfiguration can increase cost if resources are over-provisioned.  
- Ignoring monitoring makes failures harder to detect.

## References
- https://learn.microsoft.com/en-us/azure/aks/concepts-clusters-workloads
- https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling
