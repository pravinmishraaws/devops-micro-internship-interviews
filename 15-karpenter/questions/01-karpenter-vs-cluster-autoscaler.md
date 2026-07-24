---
id: 1
title: What is Karpenter and how is it different from Cluster Autoscaler?
difficulty: medium
week: 15
topics: [karpenter, autoscaling, eks, kubernetes]
tags: [karpenter, cluster-autoscaler, autoscaling, eks, spot, node-provisioning]
author: pravinmishraaws
reviewed: true
---

## Question
What is Karpenter and how is it different from Cluster Autoscaler?

## Short Answer
Karpenter is a node autoscaler for Kubernetes that calls the EC2 Fleet API directly to provision exactly the right instance type for pending pods — typically in under 60 seconds. Cluster Autoscaler scales pre-defined Auto Scaling Groups, which is slower and less flexible.

## Deep Dive
When pods cannot be scheduled because there is no available node capacity, Karpenter steps in:

1. It reads the pending pod's resource requests (CPU, memory, GPU)
2. It evaluates the NodePool configuration — which instance families, architectures, and capacity types are allowed
3. It calls the EC2 Fleet API directly and provisions the most cost-efficient instance that satisfies the pod's requirements
4. The node joins the cluster and the pod schedules — typically within 60 seconds

**Key difference from Cluster Autoscaler:**

| | Karpenter | Cluster Autoscaler |
|---|---|---|
| Provisioning | Calls EC2 Fleet API directly | Scales ASG min/max |
| Instance selection | Picks the right size for the workload | Uses whatever the ASG was configured with |
| Speed | ~60 seconds | Several minutes |
| Spot handling | Built-in diversification across families | Requires separate Spot ASGs |

**NodePool example:**
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64"]
```

For a Kubernetes platform on AWS, Karpenter is the current industry standard. Cluster Autoscaler is still used but Karpenter is replacing it for most new deployments.

## Pitfalls
- Not configuring instance diversification — relying on one instance type for Spot means mass interruptions when that type is reclaimed
- Forgetting to set resource requests on pods — Karpenter cannot size nodes correctly without them
- Not setting a `disruption` budget — Karpenter may consolidate nodes during business hours and cause brief pod restarts

## References
- [Karpenter Docs — Getting Started](https://karpenter.sh/docs/getting-started/)
- [Karpenter vs Cluster Autoscaler — AWS Blog](https://aws.amazon.com/blogs/containers/using-amazon-eks-with-karpenter-for-optimized-computing/)

## From the Project

The Petclinic Platform uses Karpenter with a NodePool that targets ARM/Graviton instances:

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: petclinic-nodes
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64"]
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["t4g.small", "t4g.medium", "t4g.large"]
```

When a Spring Boot pod cannot be scheduled because all t4g.small nodes are full, Karpenter reads the pod's resource request (256 MiB, 0.25 CPU) and provisions the cheapest ARM instance that fits — trying spot first, falling back to on-demand if no spot capacity is available. Provisioning takes under 60 seconds.

Cluster Autoscaler would have required a pre-configured ASG with a fixed instance type. Karpenter makes that decision dynamically, per workload.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
