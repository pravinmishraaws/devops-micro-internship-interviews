---
id: Q0402
title: IAM Access Managment
difficulty: easy
week: 04
topics: [aws, iam]
tags: [aws, iam, security]
author: Nchedo Nnaji
reviewed: false
---

## Question
In a multi-account in AWS environment, how would you securely allow a DevOps Engineer from one account to access s3 buckets in another account without using long-term access keys?

## Short Answer
Use AWS IAM role-based cross-account access by creating a role in the bucket’s account and allowing the DevOps engineer’s account to assume it using Security Token Service, instead of static access keys.

## Deep Dive
Secure Steps:
1. Create an IAM role in the S3 bucket’s account with a trust policy allowing the DevOps account to assume it.
2. Attach a permissions policy to that role granting `s3:ListBucket`, `s3:GetObject`, etc., on specific bucket resources.
3. In the DevOps account, the user runs:
   ```bash
   aws sts assume-role --role-arn arn:aws:iam::<BucketAccountID>:role/S3AccessRole --role-session-name devops-access
    This generates temporary credentials.
4. Optionally, use AWS Resource Access Manager (RAM) for resource sharing across accounts.
5. Implement least privilege: grant only needed bucket actions and apply bucket policies to validate access source.
Benefits:
- No need to share long-term credentials.
- Access is auditable via CloudTrail.
- Access duration can be limited via session policies.

##Pitfalls
- Forgetting to add the external account in the role trust policy.
- Using wildcard (*) in the bucket policy, violating least privilege.
- Not using CloudTrail or IAM Access Analyzer to audit access.

## References
- AWS IAM docs - https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html
- AWS Security Token Service docs - https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html
- Security best practices for Amazon S3 - https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
