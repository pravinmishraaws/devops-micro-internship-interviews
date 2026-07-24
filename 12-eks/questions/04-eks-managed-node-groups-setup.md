---
id: 4
title: How do you set up an EKS cluster with managed node groups using Terraform?
difficulty: hard
week: 12
topics: [eks, terraform, node-groups, oidc, iam]
tags: [eks, managed-node-groups, terraform, oidc, graviton, arm64, irsa]
author: pravinmishraaws
reviewed: true
---

## Question
Walk me through provisioning an EKS cluster with managed node groups in Terraform. What are the key configuration decisions and why?

## Short Answer
The cluster itself needs an IAM role with `AmazonEKSClusterPolicy`. Node groups need a separate IAM role with `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`, and `AmazonEKS_CNI_Policy`. Enable the OIDC provider on the cluster — IRSA for everything that needs AWS access will not work without it.

## Deep Dive
**Three IAM roles minimum:**

1. **Cluster role** — allows the EKS control plane to manage AWS resources (load balancers, ENIs)
2. **Node group role** — allows EC2 nodes to join the cluster and pull images from ECR
3. **Per-component IRSA roles** — ESO, ALB Controller, Karpenter each get their own role

**OIDC provider — enable it or nothing works:**
```hcl
data "tls_certificate" "eks" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.eks.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer
}
```

**Managed node group configuration decisions:**
- **Instance type:** ARM/Graviton (`t4g.*`) for cost savings; requires all images to be built for `linux/arm64`
- **AMI type:** `AL2023_ARM_64_STANDARD` for Graviton nodes
- **Scaling:** `min_size`, `max_size`, `desired_size` — with Karpenter, keep the managed node group small and let Karpenter handle burst
- **Launch template:** needed if you want custom user data, specific security groups, or EBS volume settings

```hcl
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "petclinic-ng"
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.subnet_ids

  instance_types = ["t4g.small"]
  ami_type       = "AL2023_ARM_64_STANDARD"

  scaling_config {
    desired_size = 2
    min_size     = 2
    max_size     = 4
  }
}
```

**Add-ons** — install via `aws_eks_addon` resources, not manually:
- `vpc-cni` — pod networking
- `coredns` — cluster DNS
- `kube-proxy` — iptables rules for Services
- `aws-ebs-csi-driver` — persistent volumes (if needed)

## Pitfalls
- Forgetting to attach `AmazonEKS_CNI_Policy` to the node role — pods cannot get IP addresses and stay in `Pending`
- Not enabling OIDC — IRSA roles cannot be assumed; ESO, ALB Controller, and Karpenter all fail silently
- Using x86 (amd64) instance types but pushing arm64 images — pods crash immediately with `exec format error`
- Not tagging subnets with `kubernetes.io/role/internal-elb: 1` — the ALB Controller cannot find subnets to place load balancers in

## References
- [AWS Docs — Creating a managed node group](https://docs.aws.amazon.com/eks/latest/userguide/create-managed-node-group.html)
- [AWS Docs — Enable IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html)
- [Terraform AWS Provider — aws_eks_cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eks_cluster)

## From the Project

The `terraform/modules/eks/` module provisions the entire cluster setup:

- EKS cluster with Kubernetes 1.29 in `eu-central-1`
- Two managed node groups of `t4g.small` ARM/Graviton instances (2 vCPU, 2 GiB each) — enough capacity for all eight microservices plus system pods
- OIDC provider enabled — required by ESO, ALB Controller, and Karpenter before they can call any AWS API
- All four standard add-ons provisioned via `aws_eks_addon` with the correct IAM roles where needed

Because the nodes are ARM (`t4g.small`), all eight Petclinic service images are built for `linux/arm64` in the GitHub Actions CI pipeline using `docker buildx` with the `--platform linux/arm64` flag.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
