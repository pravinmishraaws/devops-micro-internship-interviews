---
id: Q0401
title: Designing a secure VPC architecture
difficulty: easy
week: 04
topics: [aws, vpc]
tags: [networking, vpc, architecture]
author: Nchedo Nnaji
reviewed: false
---

## Question
How can one design a secure VPC architecture that allows public web servers to serve traffic, while keeping backend databases private and isolated?

## Short Answer
-By placing public web servers in public subnets and private databases in private subnets within the same VPC. Use Internet Gateway (IGW) for public access, NAT Gateway for private instances, outbound traffic, and Security Groups to strictly control inbound/outbound rules.

## Deep Dive
A secure VPC design follows a two-tier or three-tier model:
- Public Subnet: Contains Application Load Balancer (ALB) and web servers. Route table includes route to Internet Gateway (IGW) for external access.
- Private Subnet: Hosts databases or internal services. No direct route to the Internet, only route via NAT Gateway for updates/outbound requests.
- Security Controls:
  - Use Security Groups to allow traffic from ALB/web tier to database tier.
  
- Additional best practices:
  - Use Multi-AZ subnets for high availability.
  - Use VPC Endpoints to connect privately to S3 or DynamoDB.
  - Disable public IP assigned on private subnets.

## Pitfalls
- Placing databases in public subnets.
- Forgetting to enable Flow Logs for auditing.
- Allowing NAT Gateway in a single AZ (single point of failure).

## References
- AWS VPC Documentation - https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- AWS Security Best Practices - https://aws.amazon.com/architecture/security-identity-compliance/
