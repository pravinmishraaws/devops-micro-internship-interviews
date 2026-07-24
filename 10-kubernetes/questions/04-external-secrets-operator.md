---
id: 4
title: How do you manage secrets in Kubernetes without storing them in Git?
difficulty: medium
week: 10
topics: [kubernetes, secrets, external-secrets, security]
tags: [secrets, external-secrets-operator, secrets-manager, irsa, security]
author: pravinmishraaws
reviewed: true
---

## Question
How do you manage secrets in Kubernetes without storing them in Git or hardcoding them in manifests?

## Short Answer
External Secrets Operator (ESO) syncs secrets from AWS Secrets Manager into Kubernetes Secret objects automatically. The operator authenticates to AWS using IRSA — no credentials in the cluster, no secrets in Git, and Secrets Manager handles rotation.

## Deep Dive
The flow has three components:

**1. AWS Secrets Manager** — holds the actual secret value. Only the ESO pod has permission to read it (via IRSA).

**2. External Secrets Operator** — runs as a pod in the cluster. Watches `ExternalSecret` CRDs and calls the Secrets Manager API to fetch values. Creates and updates Kubernetes `Secret` objects automatically.

**3. ExternalSecret CRD** — declarative config that says "fetch this key from Secrets Manager and write it to this Kubernetes Secret."

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: petclinic-db-credentials
  namespace: petclinic-dev
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: petclinic-db-credentials
  data:
    - secretKey: username
      remoteRef:
        key: petclinic/dev/db-credentials
        property: username
    - secretKey: password
      remoteRef:
        key: petclinic/dev/db-credentials
        property: password
```

The Kubernetes `Secret` named `petclinic-db-credentials` is created and kept in sync. The application pod references it as an environment variable — the Spring Boot service never knows the secret came from Secrets Manager.

**Why not use Kubernetes Secrets directly?** Base64-encoded Kubernetes Secrets are not encrypted at rest by default. Anyone with `kubectl get secret` access in the namespace can read them. Committing them to Git (even base64) is a common security failure.

**Secret rotation:** when the secret value changes in Secrets Manager, ESO re-fetches it at the `refreshInterval` and updates the Kubernetes Secret. Pods pick up the new value on the next restart or via volume mounts that are updated automatically.

## Pitfalls
- Forgetting to create the OIDC provider — ESO's IRSA role cannot be assumed without it
- Setting `refreshInterval` too long — a rotated DB password will not reach the pods until the next refresh cycle
- Giving ESO's IAM role access to all secrets with `secretsmanager:GetSecretValue:*` — scope it to specific secret ARNs or path prefixes
- Not enabling secret versioning in Secrets Manager — without it you cannot roll back a bad secret value

## References
- [External Secrets Operator — Getting Started](https://external-secrets.io/latest/introduction/getting-started/)
- [External Secrets Operator — AWS Secrets Manager Provider](https://external-secrets.io/latest/provider/aws-secrets-manager/)
- [AWS Docs — Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

## From the Project

The Petclinic Platform stores three secrets in AWS Secrets Manager:

| Secret Path | Contents | Used By |
|---|---|---|
| `petclinic/dev/db-credentials` | MySQL username and password | customers-service, visits-service, vets-service |
| `petclinic/dev/openai-api-key` | OpenAI API key | genai-service |
| `petclinic/dev/config-server-git` | Git credentials for Config Server | config-server (if private repo) |

The External Secrets Operator runs in the `external-secrets` namespace and authenticates to AWS using IRSA. The `petclinic-eso-role` IAM role is scoped to only `secretsmanager:GetSecretValue` on the petclinic-prefixed paths — not every secret in the account.

`ExternalSecret` CRDs live in `k8s/base/external-secrets/` and are applied alongside the service manifests. ArgoCD manages them as part of the GitOps deployment — no manual `kubectl apply` required.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
