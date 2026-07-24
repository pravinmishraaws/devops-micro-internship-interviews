---
id: 1
title: Roles vs Playbooks — structure and reuse
difficulty: easy
week: 07
topics: [ansible, roles]
tags: [ansible, roles, reuse, galaxy]
author: pravinmishraaws
reviewed: false

---

## Question
When to create roles? How do roles improve reuse and testing?

## References
- Ansible Docs — Roles

---

id: Q0706

title: Ansible Modules — purpose and usage

difficulty: easy

week: 07
topics: [ansible, modules]

tags: [ansible, modules, tasks, automation]

author: rukevweubioworo

reviewed: false
---

## Question 1
- what is Anible Modues?
-  How do module help  perform  configuration  tasks on managed hosts
-  how can you find or use build-in module



  
## Question 2
- What is an Ansible playbook
-  what are its main components ?
- Describe how Ansible executes a playbook from start to finish.

## Question 3
- What is the difference between running an Ansible ad-hoc command and using a playbook?
-  When would you prefer one over the other in a DevOps workflow?

## Question 4
- How can you test if a service (like Nginx or MySQL) is running or alive using Ansible?
- Which modules or playbook tasks can you use to verify and restart it if it’s down?


  








## From the Project

The Petclinic Platform uses Terraform for infrastructure provisioning — not Ansible. The role vs. playbook distinction maps directly to Terraform's module vs. root module pattern:

| Ansible | Terraform equivalent |
|---|---|
| Playbook | Root module (`environments/dev/main.tf`) |
| Role | Reusable module (`modules/vpc/`, `modules/eks/`) |
| Task | Resource block |
| Inventory | `terraform.tfvars` / backend config |

If you are asked about Ansible in an interview for a role that uses Terraform — drawing this parallel shows you understand the abstraction, not just the syntax.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
