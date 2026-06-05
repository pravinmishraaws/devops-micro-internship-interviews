---
id: Q0101
title: IAM role vs IAM user — when and why does it matter at scale?
difficulty: hard
week: 01
topics: [aws, iam, security]
tags: [aws, iam, least-privilege, security]
author: JulietChinenyeDuru
reviewed: false
---

## Short Answer
IAM users are long-lived identities with static credentials; IAM roles issue short-lived, auto-rotating tokens assumed by services, humans, or cross-account principals. At scale, users become a credential management liability — roles are the secure default.

## Deep Dive
IAM roles use STS (Security Token Service) to issue temporary credentials (15 min–12 hrs). This eliminates the risk of leaked long-term access keys.

Key patterns:

**EC2 instance profiles** — attach a role to an EC2 instance; applications call the metadata endpoint (`169.254.169.254`) for credentials automatically.

**EKS IRSA** (IAM Roles for Service Accounts) — binds a Kubernetes service account to an IAM role via OIDC, giving pods fine-grained AWS access without node-level permissions.

**Cross-account roles** — a central tooling account assumes roles in spoke accounts, enabling centralised CI/CD pipelines without distributing credentials.

Auditing: CloudTrail logs `AssumeRole` events with the full chain of assumed principals, making forensics far cleaner than shared IAM user keys.

```bash
# Check what credentials your environment is using
aws sts get-caller-identity

# Assume a role manually
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name debug-session
```

## Pitfalls
- Creating IAM users for CI/CD pipelines instead of using OIDC federation (GitHub Actions → AWS via OIDC needs zero stored secrets)
- Over-broad trust policies on roles (`"Principal": "*"`) — anyone can assume them
- Forgetting that role session duration limits affect long-running jobs (default 1hr, max 12hrs)
- Using `AdministratorAccess` for convenience — enforce least privilege with IAM Access Analyzer

## References
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html
- https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
- https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html