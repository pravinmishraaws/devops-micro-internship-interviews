---
id: Q0013
title: EC2 Cannot Access S3 — Missing Networking Component
difficulty: entry
week: 00
topics: networking, aws, vpc, s3]
tags: [ec2, s3, networking, vpc, troubleshooting]
author: "[Hajixhayjhay](https://github.com/Hajixhayjhay)"
reviewed: false
---

## Question
- Your EC2 instance cannot access an S3 bucket. What networking component could be missing?

## Short Answer
- Most likely a **VPC Endpoint** (Gateway Endpoint for S3) is missing, or the EC2 instance has no **Internet Gateway/NAT Gateway** for public S3 access.  


## Deep Dive
- **VPC Endpoint for S3:**  
  - Allows private communication between EC2 and S3 without going over the public internet.  
  - Check if a Gateway Endpoint exists for the correct route table.  

- **Internet or NAT Gateway:**  
  - If the EC2 is in a private subnet, it needs a NAT Gateway to access S3 over the internet.  
  - Public subnet EC2s need an Internet Gateway attached to the VPC.

- **Security Groups & NACLs:**  
  - Ensure outbound rules allow traffic to S3 endpoints or the internet.

- **Testing:**  
```bash
curl https://<bucket-name>.s3.amazonaws.com

```
If it fails, verify subnet routing and endpoint configuration.

## Pitfalls
- Confusing security groups with network connectivity issues.
- Assuming S3 access always requires public internet.
- Forgetting route table associations with the VPC Endpoint.

## References
- [AWS VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
- [S3 Access from VPC](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html)
- [AWS NAT Gateway Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)

