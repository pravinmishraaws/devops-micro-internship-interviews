---
id: 2
title: Azure Subscription ID
difficulty: entry
week: 05
topics: [azure, networking, management]
tags: [azure, subscription-id]
author: Tanisha Borana
reviewed: false
---

## Question
Why is a **Subscription ID** required to access or manage any resource in Microsoft Azure?

## References
- [Microsoft Azure Documentation – Understand Azure subscriptions](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/subscription)

## From the Project

The Petclinic Platform runs on AWS, where the equivalent of an Azure Subscription is an AWS Account. Key parallels:

- **Azure Subscription → AWS Account:** the billing and permission boundary
- **Subscription ID → AWS Account ID:** appears in every IAM role ARN, ECR repository URI, and S3 bucket policy

In the petclinic setup, the AWS Account ID is referenced across Terraform modules — in the ECR repository ARN, in IRSA trust policies, and in the S3 state bucket policy. Knowing your account ID is day-one knowledge for any AWS engineer.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
