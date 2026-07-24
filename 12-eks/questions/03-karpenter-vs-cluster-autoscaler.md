---
id: 3
title: What is Karpenter and how does it differ from Cluster Autoscaler?
difficulty: medium
week: 12
topics: [eks, karpenter, autoscaling, nodes, cost]
tags: [karpenter, cluster-autoscaler, nodepool, ec2nodeclass, spot, graviton, cost-optimization]
author: pravinmishraaws
reviewed: true
---

## Question
What is Karpenter and why would you use it instead of Cluster Autoscaler?

## Short Answer
Karpenter provisions nodes directly via the EC2 API — no node groups required. When pods are pending, Karpenter calculates exactly what instance type fits them and launches it within seconds. Cluster Autoscaler scales pre-defined node groups up and down; Karpenter picks the right instance type for each workload.

## Deep Dive
**Cluster Autoscaler approach:**
- You pre-define node groups in the AWS console or Terraform
- Cluster Autoscaler watches for pending pods and increments the node group's desired count
- Every node in the group is the same instance type — you decide the type upfront
- Scale-down is slow: Cluster Autoscaler waits 10 minutes after a node becomes idle before terminating it

**Karpenter approach:**
- You define `NodePool` (constraints) and `EC2NodeClass` (AWS-specific config) — not node groups
- Karpenter watches for pending pods and computes the best instance type from a configurable list
- It calls `ec2:RunInstances` directly to launch the node
- Node comes online in ~60 seconds (vs several minutes for CA)
- Spot interruption handling: Karpenter watches EventBridge for spot interruption notices and proactively drains and replaces affected nodes

```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["t4g.small", "t4g.medium", "t4g.large"]
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64"]
  limits:
    cpu: "100"
  disruption:
    consolidationPolicy: WhenUnderutilized
    consolidateAfter: 30s
```

**Consolidation:** Karpenter can bin-pack existing workloads onto fewer nodes and terminate the now-empty ones. Cluster Autoscaler can only scale down empty nodes.

## Pitfalls
- Not configuring spot interruption handling — SQS queue + EventBridge rule + Karpenter's `EC2NodeClass` must be wired together
- Using a single instance type in the NodePool — spot availability varies by instance type; diversification avoids "no capacity" errors
- Forgetting the IRSA role — Karpenter needs `ec2:RunInstances`, `ec2:TerminateInstances`, SQS permissions
- Mixing Cluster Autoscaler and Karpenter on the same cluster — they will fight over the same nodes

## References
- [Karpenter Docs — Getting Started with Karpenter](https://karpenter.sh/docs/getting-started/)
- [Karpenter Docs — NodePool](https://karpenter.sh/docs/concepts/nodepools/)
- [Karpenter Docs — Disruption](https://karpenter.sh/docs/concepts/disruption/)

## From the Project

The Petclinic Platform uses Karpenter for node scaling in both dev and prod. The `terraform/modules/karpenter/` module provisions:

- The `petclinic-karpenter-role` IAM role (via IRSA) with `ec2:RunInstances`, `ec2:TerminateInstances`, and SQS permissions
- An SQS queue that receives EC2 spot interruption notices from EventBridge
- The EventBridge rules that route `EC2 Spot Instance Interruption Warning` and `EC2 Instance State-change Notification` events to the queue

The `NodePool` is configured to use `t4g.small`, `t4g.medium`, and `t4g.large` ARM/Graviton instances — all on spot — with on-demand as fallback. Consolidation is enabled so idle nodes are terminated within 30 seconds of becoming empty.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
