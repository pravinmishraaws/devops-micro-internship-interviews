---
id: 1
title: How do you handle per-environment differences in Helm?
difficulty: medium
week: 13
topics: [helm, environments, values, kubernetes]
tags: [helm, values, dev, prod, environments, overrides]
author: pravinmishraaws
reviewed: true
---

## Question
How do you manage differences between dev and prod environments when using Helm?

## Short Answer
One generic chart, per-service values files, and per-environment override files. The chart contains logic. The values files contain configuration. They are never mixed.

## Deep Dive
The structure that scales across many services and environments:

```
helm/
└── petclinic-service/     ← one generic chart for all 8 services
    ├── Chart.yaml
    ├── templates/
    └── values.yaml        ← defaults only

helm-values/
├── api-gateway.yaml       ← per-service: port, probes, env vars
├── customers-service.yaml
├── dev.yaml               ← per-env: replicas=1, HPA disabled
└── prod.yaml              ← per-env: replicas=2, HPA enabled
```

Deploy command layers the values in order:

```bash
helm upgrade --install api-gateway helm/petclinic-service \
  -f helm-values/api-gateway.yaml \
  -f helm-values/dev.yaml
```

Dev overrides set replicas to 1, HPA disabled, smaller resource limits.
Prod overrides set replicas to 2 or more, HPA enabled, larger resource limits, stricter probes.

**The key point for the interview:** The chart is the logic, the values are the configuration, and they are never mixed. That separation is what makes one chart reusable across all services and both environments — without duplicating templates.

## Pitfalls
- Hardcoding environment-specific values in the chart templates — breaks reusability
- Using a separate chart per environment — doubles the maintenance burden with no benefit
- Applying the wrong values file to the wrong environment — use CI/CD to enforce which files are used in which environment

## References
- [Helm Docs — Values Files](https://helm.sh/docs/chart_template_guide/values_files/)
- [Helm Docs — helm upgrade](https://helm.sh/docs/helm/helm_upgrade/)

## From the Project

The Petclinic Platform uses exactly this pattern for all eight services:

```
helm/
└── petclinic-service/        ← one generic chart for all 8 services
helm-values/
├── api-gateway/
│   ├── values.yaml           ← port, probes, env vars, resource limits
│   ├── dev.yaml              ← replicas: 1, HPA: disabled
│   └── prod.yaml             ← replicas: 2, HPA: enabled
└── customers-service/
    └── ...
```

Deploying api-gateway to dev:
`helm upgrade api-gateway ./helm/petclinic-service -f helm-values/api-gateway/values.yaml -f helm-values/api-gateway/dev.yaml`

Swap `dev.yaml` for `prod.yaml` for prod. The chart never changes. Only the values file changes.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
