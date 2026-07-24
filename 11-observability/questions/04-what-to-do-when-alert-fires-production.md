---
id: 4
title: What do you do when an alert fires in production?
difficulty: medium
week: 11
topics: [observability, incident-response, prometheus, grafana, loki]
tags: [alerting, incident-response, grafana, prometheus, loki, zipkin, on-call]
author: pravinmishraaws
reviewed: true
---

## Question
An alert fires in production at 2am. Walk me through what you do.

## Short Answer
Metrics first, then logs, then traces. Check Grafana to identify which service and what metric is affected. Check Loki for logs from that service around the time of the alert. Check Zipkin for trace-level detail if it is a latency issue. Fix with the right tool — Git revert for a bad release, ArgoCD sync for drift, `kubectl describe` for a pod-level problem.

## Deep Dive
**Step 1 — Metrics (Grafana):** Which service triggered the alert? What metric? What does the trend look like over the last hour? Is this a sudden spike or a slow degradation? Compare against the last deployment time.

**Step 2 — Logs (Loki via Grafana Explore):** Filter logs for the affected service around the timestamp of the alert. Look for stack traces, error messages, connection timeouts. LogQL query:
```
{namespace="petclinic-prod", app="api-gateway"} |= "ERROR" | json
```

**Step 3 — Traces (Zipkin):** If the issue is latency — a slow endpoint, a timeout — traces show you the full call chain. You can see which downstream service took the most time and whether the slowness is in your code or in a dependency (RDS, external API).

**Step 4 — Fix with the right tool:**
| Cause | Fix |
|---|---|
| Bad release | `git revert` the image tag commit → ArgoCD redeploys previous version |
| Cluster drift | ArgoCD manual sync to restore desired state |
| OOMKilled pod | `kubectl describe pod` → adjust memory limits in values file → PR |
| RDS connection exhaustion | `kubectl exec` into a debug pod → check connection pool settings |

**What makes this answer strong:** Having all three pillars in place is what lets you go from alert to root cause in minutes instead of hours. Most teams have metrics. Fewer have correlated logs and traces. Showing you have all three — and know when to use each — is the signal interviewers are looking for.

## Pitfalls
- Starting with logs before checking metrics — logs are verbose, metrics give you the fastest signal on what is broken
- Not having runbooks — at 2am, documented steps matter more than memory
- Fixing in the cluster directly without updating Git — the fix gets overwritten by the next ArgoCD sync

## References
- [Grafana Docs — Explore](https://grafana.com/docs/grafana/latest/explore/)
- [Zipkin Docs — Architecture](https://zipkin.io/pages/architecture.html)

## From the Project

On the Petclinic Platform, the response when an alert fires:

1. **Grafana** → alerting dashboard: which service, which metric, is it a spike or a sustained trend?
2. **Loki** → Grafana Explore → filter logs for that service in the 10 minutes around the alert. Look for stack traces, connection errors, timeout messages.
3. **Zipkin** → if the metric is latency-related, pull a trace from around the alert time. Find the slow span — is it the service itself, the database query, or a downstream call?

**Fix options in order:**
- Bad release → `git revert <commit>` on the image tag commit in `helm-values/`. ArgoCD re-deploys the previous image automatically.
- Configuration drift → ArgoCD manual sync restores the desired state
- Pod crash → `kubectl describe pod` + `kubectl logs --previous` to see the exit reason

Metrics → logs → traces. In that order, every time.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
