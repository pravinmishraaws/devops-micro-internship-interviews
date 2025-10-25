---
id: Q0602
title: Terraform remote state, backends
difficulty: medium
week: 06
topics: [terraform, state]
tags: [terraform, state, backend]
author: bhupendrabhati (https://github.com/bhupendrabhati/dmi-interview-repo)
reviewed: false
---

## Question
When we run terraform init command, backend get initializa. Where we can see that backend in our local machine.

## Short Answer
- When we run terraform init, Terraform initializes the backend, which is where it stores the state file.
- We can see which backend is configured in our Terraform configuration file typically in the backend block inside the terraform section of a .tf file (like main.tf).

## Deep Dive Answer
- When you execute terraform init, Terraform does the following for the backend:

- Reads the configuration: It looks in your .tf files for a terraform block with a backend definition.

- Initializes the backend plugin: Depending on the type (e.g., local, s3, azurerm, gcs), Terraform downloads and configures the appropriate backend plugin.

- Verifies or creates the remote storage: For example, if it’s an S3 backend, Terraform checks access to the bucket and key.
If it’s local, it simply creates or uses the local terraform.tfstate file.

- Writes backend metadata locally: Terraform stores backend-related data inside a hidden directory called .terraform/

## Pitfalls/Gotchas 
- Backend config is not always visible

- We can’t “see” the backend directly from terraform init output unless we configured it in your .tf files.

- Terraform stores backend metadata inside .terraform/ directory, not printed to console.


## References
- Terraform Docs — Backends
