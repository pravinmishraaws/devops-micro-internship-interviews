---
id: 2
title: What are the three pillars of observability?
difficulty: easy
week: 11
topics: [observability, metrics, logs, traces]
tags: [observability, prometheus, grafana, logs, tracing, opentelemetry]
author: pravinmishraaws
reviewed: true
---

## Question
What are the three pillars of observability and what tool covers each?

## Short Answer
Metrics, logs, and traces. Metrics tell you what is happening right now. Logs tell you what happened. Traces tell you where the time went across multiple services.

## Deep Dive
Each pillar answers a different question during an incident:

| Pillar | Question answered | Tool |
|---|---|---|
| Metrics | Is the system healthy right now? What are the trends? | Prometheus + Grafana |
| Logs | What exactly happened at 14:23:07? | FluentBit → Loki, Grafana Explore |
| Traces | Which service caused the 3-second latency spike? | OpenTelemetry → Zipkin |

**Metrics:** Prometheus scrapes `/actuator/prometheus` from each Spring Boot service. Grafana queries Prometheus and displays dashboards and alerts.

**Logs:** FluentBit runs as a DaemonSet on each EKS node, collects container logs, and ships them to Loki. Grafana Explore queries Loki — same tool as metrics, one pane of glass.

**Traces:** The application emits OpenTelemetry spans. Zipkin receives them and reconstructs the full request path across services — you can see the waterfall and identify which service took the most time.

**The investigation sequence:** When an alert fires, start with metrics (which service, what metric, what trend), move to logs (what happened at that timestamp), then traces (if it is a latency issue, which call chain is slow). Metrics → Logs → Traces.

## Pitfalls
- Having metrics but no logs — you know something is broken but cannot see what happened
- Having logs but no structured format — searching free-text logs at 2am during an incident is painful
- Missing traces — distributed systems without tracing make latency bugs nearly impossible to diagnose

## References
- [OpenTelemetry — Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [Grafana Docs — Loki](https://grafana.com/docs/loki/latest/)

## From the Project

The Petclinic Platform implements all three pillars in production:

- **Metrics:** Prometheus scrapes `/actuator/prometheus` from five services (api-gateway, customers, visits, vets, genai). Grafana renders per-service dashboards with request rate, error rate, and JVM memory.
- **Logs:** FluentBit DaemonSet tails container logs from all eight services and ships to Loki. Grafana Explore filters by service, pod, or log level.
- **Traces:** OpenTelemetry exporter in each Spring Boot service sends spans to Zipkin. A slow API call shows exactly which downstream service added the latency.

The investigation sequence in production: metrics tell you *something is wrong*, logs tell you *what happened*, traces tell you *where the time went*.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
