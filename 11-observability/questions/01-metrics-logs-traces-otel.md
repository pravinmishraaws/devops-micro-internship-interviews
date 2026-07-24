---
id: 1
title: Metrics vs Logs vs Traces — how they work together
difficulty: entry
week: 11
topics: [observability]
tags: [metrics, logs, traces, otel]
author: pravinmishraaws
reviewed: false
---

## Question
Explain the three pillars and a minimal OTEL setup.

## References
- OpenTelemetry Docs

## From the Project

The Petclinic Platform implements all three pillars with OpenTelemetry as the instrumentation layer:

- **Metrics:** Spring Boot services emit metrics via Micrometer → exported to `/actuator/prometheus` → scraped by Prometheus → visualised in Grafana
- **Logs:** FluentBit DaemonSet tails container logs from all eight services → shipped to Loki → queried in Grafana Explore
- **Traces:** OpenTelemetry SDK in each Spring Boot service → spans exported to Zipkin. A single user request through the API Gateway generates spans across api-gateway → customers-service → vets-service

All three are accessible from one Grafana instance — switch between metric dashboards and Loki log queries without leaving the tool.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
