---
id: 2
title: How does the ALB Ingress Controller work in EKS?
difficulty: medium
week: 12
topics: [eks, ingress, alb, networking, aws]
tags: [alb, ingress, load-balancer, eks, irsa, aws-load-balancer-controller]
author: pravinmishraaws
reviewed: true
---

## Question
How does the AWS Load Balancer Controller work in EKS? What is the relationship between a Kubernetes Ingress resource and an AWS Application Load Balancer?

## Short Answer
The AWS Load Balancer Controller watches Kubernetes Ingress resources and automatically creates and configures an Application Load Balancer in AWS to match. When you apply an Ingress manifest with the right annotations, the controller provisions the ALB, target groups, and listener rules — no manual AWS console work required.

## Deep Dive
The controller runs as a pod in the `kube-system` namespace and uses IRSA to call the AWS API. The flow:

1. You apply an `Ingress` resource with `kubernetes.io/ingress.class: alb`
2. The controller detects the new Ingress
3. It calls the EC2 API to create an ALB in the VPC
4. It creates target groups — one per service backend
5. It creates listener rules — HTTP/HTTPS routing from the ALB to the target groups
6. ALB → target group → pod (traffic bypasses kube-proxy and goes directly to the pod IP)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: petclinic-ingress
  namespace: petclinic-dev
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:eu-central-1:123456789:certificate/abc
spec:
  rules:
    - host: dev.petclinic.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-gateway
                port:
                  number: 8080
```

**`target-type: ip`** — traffic goes directly to the pod IP, not to the node IP first. This is more efficient and avoids double-hop routing through kube-proxy.

**IRSA requirement:** the controller's service account must be annotated with an IAM role that has permissions to create and manage ALBs, target groups, security groups, and listeners. Without IRSA, the controller cannot call the AWS API.

## Pitfalls
- Not creating the OIDC provider — the controller's IRSA role cannot be assumed without it
- Forgetting the `alb.ingress.kubernetes.io/scheme: internet-facing` annotation — ALB defaults to internal, unreachable from the internet
- Using `target-type: instance` (the default) instead of `ip` — requires NodePort services and routes traffic through kube-proxy, adding unnecessary latency
- Not attaching the ACM certificate ARN — HTTPS listeners require the annotation even if Route 53 is already configured

## References
- [AWS Docs — AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
- [AWS Load Balancer Controller — Ingress Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/)

## From the Project

The Petclinic Platform uses the AWS Load Balancer Controller as the single entry point for all external traffic. The Ingress resource in `k8s/base/ingress/` routes everything through the API Gateway service — the API Gateway pod then routes to the individual microservices internally via Kubernetes service discovery.

The ALB terminates TLS using an ACM certificate provisioned via the `dns` Terraform module. Route 53 has an A record (alias) pointing to the ALB DNS name — `dev.petclinic.example.com` resolves to the ALB, which forwards to the `api-gateway` pods.

The controller uses IRSA via the `petclinic-alb-role` IAM role scoped to ALB and target group management — not full EC2 admin permissions.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
