---
id: 7
title: How do you set up alerting with Prometheus and Alertmanager?
difficulty: medium
week: 11
topics: [observability, prometheus, alertmanager, alerting, sre]
tags: [prometheus, alertmanager, alertrule, prometheusrule, pagerduty, slack, sre, slo]
author: pravinmishraaws
reviewed: true
---

## Question
How do you configure alerts in Prometheus? Walk me through the flow from defining a rule to an engineer receiving a notification.

## Short Answer
You define a `PrometheusRule` CRD with an alerting expression in PromQL. Prometheus evaluates it on a schedule and fires the alert to Alertmanager when the condition is true. Alertmanager routes the alert to the right receiver — Slack, PagerDuty, email — based on labels.

## Deep Dive
**Three components:**
1. **PrometheusRule** — defines what to alert on (PromQL expression + threshold)
2. **Prometheus** — evaluates the rule every `evaluationInterval` and sends fired alerts to Alertmanager
3. **Alertmanager** — receives alerts, deduplicates, groups, and routes to receivers

**Step 1 — Define the rule:**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: petclinic-alerts
  namespace: petclinic-prod
  labels:
    release: kube-prometheus-stack
spec:
  groups:
    - name: petclinic.availability
      rules:
        - alert: ServiceDown
          expr: up{namespace="petclinic-prod"} == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "{{ $labels.job }} is down"
            description: "No healthy pods for {{ $labels.job }} in petclinic-prod for over 1 minute"

        - alert: HighErrorRate
          expr: |
            rate(http_server_requests_seconds_count{namespace="petclinic-prod",status=~"5.."}[5m])
            /
            rate(http_server_requests_seconds_count{namespace="petclinic-prod"}[5m]) > 0.05
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: "High 5xx rate on {{ $labels.job }}"
```

**`for: 1m`** — the condition must be true continuously for 1 minute before the alert fires. Prevents flapping on transient issues.

**Step 2 — Alertmanager routing:**
```yaml
route:
  group_by: ['alertname', 'namespace']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'slack-prod'
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

receivers:
  - name: 'slack-prod'
    slack_configs:
      - api_url: '<webhook-url>'
        channel: '#petclinic-alerts'
  - name: 'pagerduty'
    pagerduty_configs:
      - routing_key: '<key>'
```

**Silences and inhibitions:** Alertmanager supports temporary silences (mute an alert during maintenance) and inhibitions (suppress warnings when a critical alert is already firing for the same service).

## Pitfalls
- Missing the `release: kube-prometheus-stack` label on `PrometheusRule` — the Prometheus Operator uses label selectors to find rules; without the right label, rules are ignored silently
- Setting `for: 0m` — the alert fires on the first failing scrape, causing constant noise from transient glitches
- Not testing PromQL in the Prometheus UI before deploying — a syntax error in the expression is silent at deployment time but the rule never fires
- Alertmanager not configured with a `repeat_interval` — a firing alert repeats every 15 seconds by default, flooding the channel

## References
- [Prometheus Docs — Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Alertmanager Docs — Routing](https://prometheus.io/docs/alerting/latest/configuration/#route)
- [Prometheus Operator — PrometheusRule](https://prometheus-operator.dev/docs/user-guides/alerting/)

## From the Project

The Petclinic Platform defines `PrometheusRule` resources in `k8s/base/` alongside the service manifests. Each rule file contains two categories of alerts:

- **Availability alerts** — `up == 0` for 1 minute → critical → PagerDuty
- **SLO alerts** — 5xx rate above 5% over a 5-minute window → warning → Slack `#petclinic-alerts`

Alertmanager is deployed as part of the `kube-prometheus-stack` Helm release in `terraform/modules/observability/`. The Alertmanager config is stored as a Kubernetes Secret (managed by the Helm chart) and never committed to Git in plaintext — the Slack webhook URL and PagerDuty routing key are injected from AWS Secrets Manager via the External Secrets Operator.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
