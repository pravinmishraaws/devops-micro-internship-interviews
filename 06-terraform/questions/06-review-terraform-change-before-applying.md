---
id: 6
title: How do you review a Terraform change before applying?
difficulty: easy
week: 06
topics: [terraform, plan, review]
tags: [terraform, plan, apply, review, safety]
author: pravinmishraaws
reviewed: true
---

## Question
How do you review a Terraform change before applying it?

## Short Answer
Run `terraform plan`. Read every line. Do not apply until you understand every addition, modification, and destruction. Save the plan with `-out` so what you reviewed is exactly what gets applied.

## Deep Dive
`terraform plan` shows you three types of changes: additions (`+`), modifications (`~`), and destructions (`-`). Destructions are the dangerous ones — a destroyed resource can mean downtime or data loss.

The professional workflow:
1. Read the technical spec before writing any Terraform
2. Run `terraform plan -out plan.out`
3. Review every line — especially anything marked for destruction
4. Apply with `terraform apply plan.out` (applies the saved plan, not a re-calculated one)

Saving with `-out` is critical. Without it, `terraform apply` recalculates the plan at apply time. If the state or variables changed between plan and apply, you apply something different from what you reviewed.

**What to say in the interview:** "I save the plan with `-out plan.out` so that what I reviewed is exactly what gets applied." This detail separates engineers who have used Terraform in production from those who followed a tutorial.

## Pitfalls
- Running `terraform apply` without a prior `plan` — the apply itself shows a plan but you are under pressure to proceed
- Not reading destruction lines carefully — Terraform will tell you it is destroying something, but it is easy to miss in a long plan output
- Applying without `-out` — the re-calculated plan can differ from what you reviewed if the state was modified by another process

## References
- [Terraform Docs — terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform Docs — terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)

## From the Project

Every infrastructure change in the Petclinic Platform follows this review discipline:

1. Read the technical spec first — understand what should exist before writing any Terraform
2. Write the module, run `terraform plan -out plan.out`
3. Read the plan line by line — every addition, modification, and destruction has a reason. An unexpected destruction of an RDS instance or EKS node group means stop and investigate.
4. Apply with `terraform apply plan.out` — the saved plan ensures exactly what you reviewed is what gets applied

The `-out` flag matters because Terraform re-calculates the plan at apply time if you do not save it. What you reviewed and what gets applied could differ if the state changed between the two commands.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
