---
id: 6
title: How does FluentBit collect and forward logs from pods in EKS?
difficulty: medium
week: 11
topics: [observability, logging, fluentbit, cloudwatch, eks]
tags: [fluentbit, logs, daemonset, cloudwatch, eks, log-aggregation, stdout]
author: pravinmishraaws
reviewed: true
---

## Question
How do you collect logs from all pods across a Kubernetes cluster and send them to a central destination? Walk me through how FluentBit works in EKS.

## Short Answer
FluentBit runs as a DaemonSet — one pod per node. It tails the container log files on the node's filesystem (which are just the stdout/stderr of every container), parses them, and forwards them to CloudWatch Logs or another destination. The application writes to stdout; FluentBit handles the rest.

## Deep Dive
**Why stdout?** Kubernetes captures everything a container writes to stdout and stderr and saves it to `/var/log/containers/<pod>_<namespace>_<container>-<id>.log` on the node. FluentBit tails these files — no changes to the application code required.

**DaemonSet design:**
- One FluentBit pod per node — every pod's logs are on the same node's filesystem
- Mounts `/var/log/containers/` as a `hostPath` volume
- Uses the Kubernetes filter to enrich log records with pod name, namespace, labels from the Kubernetes API

**FluentBit config (simplified):**
```ini
[INPUT]
    Name              tail
    Tag               kube.*
    Path              /var/log/containers/*.log
    Parser            cri
    DB                /var/log/flb_kube.db
    Mem_Buf_Limit     5MB
    Skip_Long_Lines   On

[FILTER]
    Name              kubernetes
    Match             kube.*
    Kube_URL          https://kubernetes.default.svc:443
    Merge_Log         On
    Keep_Log          Off

[OUTPUT]
    Name              cloudwatch_logs
    Match             kube.*
    region            eu-central-1
    log_group_name    /eks/petclinic
    log_stream_prefix petclinic-
    auto_create_group On
```

**CloudWatch Logs structure:**
- One log group per cluster: `/eks/petclinic`
- One log stream per pod: `petclinic-customers-service-abc123`
- Log Insights for querying across all streams

**IRSA for FluentBit:** FluentBit needs `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` to write to CloudWatch. Attach these permissions to a role via IRSA — do not use the EC2 instance profile.

## Pitfalls
- Logs written to files inside the container instead of stdout — FluentBit cannot see them; the application must write to stdout/stderr
- No `DB` parameter in the INPUT config — FluentBit loses its read position on restart and re-ships all old logs, creating duplicates in CloudWatch
- `Mem_Buf_Limit` too low on a busy node — FluentBit drops logs instead of buffering them when a pod is logging at high volume
- Not setting IRSA for FluentBit — it falls back to the instance profile, which may have broader permissions than needed

## References
- [FluentBit Docs — Kubernetes Filter](https://docs.fluentbit.io/manual/pipeline/filters/kubernetes)
- [FluentBit Docs — CloudWatch Output](https://docs.fluentbit.io/manual/pipeline/outputs/cloudwatch)
- [AWS Docs — Set up FluentBit on EKS](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-logs-FluentBit.html)

## From the Project

The `terraform/modules/observability/` module deploys FluentBit as a DaemonSet using the `aws-for-fluent-bit` Helm chart. Configuration:

- **Input:** tails `/var/log/containers/*.log` — picks up stdout from all eight Petclinic services automatically
- **Filter:** enriches each log record with the pod name, namespace, and service labels from the Kubernetes API
- **Output:** CloudWatch Logs group `/eks/petclinic` in `eu-central-1` — one log stream per pod

FluentBit uses IRSA via the `petclinic-fluentbit-role` IAM role scoped to CloudWatch Logs write permissions. No credentials are stored in the cluster.

The Spring Boot services log in structured JSON (configured in `logback-spring.xml`) — FluentBit ships the raw JSON, and CloudWatch Logs Insights can query specific fields like `level`, `service`, `traceId`, and `message` directly.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
