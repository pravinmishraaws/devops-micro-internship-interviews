---
id: 7
title: How do you structure Terraform modules for a production platform?
difficulty: medium
week: 06
topics: [terraform, modules, structure, best-practices]
tags: [terraform, modules, environments, reuse, root-module, child-module]
author: pravinmishraaws
reviewed: true
---

## Question
How do you structure Terraform code for a platform that has multiple environments and multiple infrastructure components?

## Short Answer
Separate root modules per environment, shared child modules per component. The `environments/dev/` directory is the root module for dev — it calls the child modules (vpc, eks, ecr, rds) with dev-specific variables. The `environments/prod/` does the same with prod values. Child modules live in `modules/` and contain no environment-specific logic.

## Deep Dive
**The pattern:**

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf       ← calls child modules with dev vars
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── backend.tf    ← dev state key
│   └── prod/
│       ├── main.tf       ← same structure, prod vars
│       ├── variables.tf
│       ├── outputs.tf
│       └── backend.tf    ← prod state key
└── modules/
    ├── vpc/
    ├── eks/
    ├── ecr/
    ├── rds/
    └── secrets/
```

**Root module** (environment directory): calls child modules, passes environment-specific values, holds the backend config. You `cd` into this directory to run `terraform init`, `plan`, `apply`.

**Child module** (component directory): contains reusable logic. No hardcoded environment values. Accepts variables for anything that differs between environments (instance size, replica count, CIDR blocks).

```hcl
# environments/dev/main.tf
module "eks" {
  source         = "../../modules/eks"
  cluster_name   = "petclinic-dev"
  instance_type  = "t4g.small"
  desired_nodes  = 2
  subnet_ids     = module.vpc.private_subnet_ids
}
```

**What not to do:** a single `main.tf` with `count` or `for_each` conditionals branching on an `environment` variable. It works at small scale but becomes impossible to reason about and dangerous — a mistake in the condition logic can apply dev changes to prod.

## Pitfalls
- Calling child modules with hardcoded values instead of variables — the module cannot be reused for a second environment without editing the module itself
- Nesting modules too deeply — one level of abstraction (root → child) is usually enough; deeper nesting makes `terraform graph` unreadable and plan output confusing
- Not pinning module versions when using public registry modules — an upstream breaking change can fail your next `terraform init`
- Putting provider configuration inside child modules — providers belong in the root module only; child modules should inherit them

## References
- [Terraform Docs — Module Structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)
- [Terraform Docs — Root Module](https://developer.hashicorp.com/terraform/language/modules#the-root-module)
- [Terraform Best Practices — Module Composition](https://developer.hashicorp.com/terraform/language/modules/develop/composition)

## From the Project

The Petclinic Platform uses this exact structure. The `terraform/` directory has:

- `environments/dev/` — root module for dev. State key: `petclinic/dev/terraform.tfstate`
- `environments/prod/` — root module for prod. State key: `petclinic/prod/terraform.tfstate`
- `modules/` — eight child modules: `vpc`, `eks`, `ecr`, `rds`, `dns`, `secrets`, `observability`, `karpenter`

Each child module accepts the variables that differ per environment (cluster name, instance type, node count, CIDR range) and outputs the values the next module needs (VPC ID, subnet IDs, cluster endpoint). Modules are wired together through outputs — `module.vpc.subnet_ids` flows into `module.eks.subnet_ids`, and so on.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
