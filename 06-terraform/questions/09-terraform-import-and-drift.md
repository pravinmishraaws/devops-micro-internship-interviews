---
id: 9
title: What is Terraform drift, and how do you detect and fix it?
difficulty: medium
week: 06
topics: [terraform, state, drift, import, debugging]
tags: [terraform, drift, plan, refresh, import, state-sync]
author: pravinmishraaws
reviewed: true
---

## Question
What is configuration drift in Terraform and how do you handle it? What do you do when the real infrastructure differs from what Terraform's state says it should be?

## Short Answer
Drift is when the actual infrastructure in AWS differs from what Terraform's state file tracks — someone made a manual change in the console, a resource was modified outside Terraform, or the state file is stale. `terraform plan` detects it. Fix it by either reconciling the code to match reality, or running `terraform apply` to force reality back to what the code says.

## Deep Dive
**What causes drift:**
- Manual changes in the AWS console or CLI (the most common cause)
- AWS auto-modifying resources (e.g., EKS updating security group rules automatically)
- Someone running `terraform apply` on a different machine with a different version of the code
- The state file getting corrupted or manually edited

**Detecting drift:**
```bash
# Refresh the state against actual AWS resources, then show the diff
terraform plan -refresh-only

# Or: just run plan (it always refreshes before computing the diff)
terraform plan
```

`terraform plan` output shows:
- `~` (update in place) — Terraform will change an existing resource
- `+` (add) — Terraform will create a new resource
- `-` (destroy) — Terraform will delete a resource
- `-/+` (destroy and recreate) — requires replacement

**Fixing drift — two options:**

Option A — force infrastructure back to code (recommended):
```bash
terraform apply
```
Applies the code as the source of truth. Manual changes are overwritten.

Option B — update the state to match reality (when the manual change was intentional):
```bash
# Import an existing resource into state
terraform import aws_security_group.eks sg-0abc1234

# Or: use terraform refresh to sync state with current AWS values
terraform apply -refresh-only
```

**`terraform import`** — used when a resource exists in AWS but not in Terraform state. After import, write the corresponding `resource` block in your `.tf` files or Terraform will try to destroy it on the next plan.

## Pitfalls
- Accepting plan output without reading it — a drift-correcting `terraform apply` can destroy resources that were manually created for a good reason
- Using `terraform refresh` (deprecated in TF 1.x) instead of `terraform apply -refresh-only` — the old refresh command modified state without confirmation
- Not using state locking — two engineers running `terraform apply` simultaneously can corrupt the state file and create drift
- Ignoring drift in prod — small manual changes accumulate and eventually the Terraform code cannot apply cleanly without destroying things

## References
- [Terraform Docs — Plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform Docs — Import](https://developer.hashicorp.com/terraform/cli/commands/import)
- [Terraform Docs — Refresh-Only Mode](https://developer.hashicorp.com/terraform/cli/commands/plan#planning-modes)

## From the Project

The Petclinic Platform's `docs/runbook.md` includes a drift detection runbook. The standard check before any infrastructure change:

```bash
cd terraform/environments/prod
terraform plan -out=tfplan
```

The plan output is reviewed before `terraform apply tfplan` is run. If the plan shows unexpected changes (resources being replaced, rules being removed), the apply is stopped and the unexpected changes are investigated before proceeding.

DynamoDB state locking (`petclinic-tfstate-lock` table) prevents concurrent applies — a second engineer running `terraform apply` while the first is running gets a lock error immediately instead of corrupting the state file.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
