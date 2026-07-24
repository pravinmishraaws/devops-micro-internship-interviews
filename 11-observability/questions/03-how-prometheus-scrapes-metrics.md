---
id: 3
title: How does Prometheus scrape metrics from your services?
difficulty: medium
week: 11
topics: [prometheus, metrics, scraping, kubernetes]
tags: [prometheus, scraping, actuator, micrometer, kubernetes, annotations]
author: pravinmishraaws
reviewed: true
---

## Question
How does Prometheus scrape metrics from your services? Walk me through the mechanism.

## Short Answer
Services expose a `/metrics` endpoint (or `/actuator/prometheus` for Spring Boot via Micrometer). Prometheus is configured with scrape targets — either static or via Kubernetes service discovery — and pulls metrics from those endpoints on a regular interval.

## Deep Dive
For Spring Boot microservices using Micrometer, the scrape flow is:

1. **Application** — Micrometer auto-configures a `/actuator/prometheus` endpoint that exposes metrics in Prometheus text format (JVM memory, HTTP request counts, latency histograms, custom metrics)
2. **Kubernetes annotations** — services are annotated to tell Prometheus to scrape them:
   ```yaml
   annotations:
     prometheus.io/scrape: "true"
     prometheus.io/port: "8081"
     prometheus.io/path: "/actuator/prometheus"
   ```
3. **Prometheus service discovery** — Prometheus uses the Kubernetes API to discover pods with these annotations and automatically adds them as scrape targets
4. **Scrape interval** — Prometheus pulls from each target every 15–30 seconds and stores the time-series data

**Which services to scrape:** Not every service needs Micrometer metrics. In a petclinic-style platform, you scrape the services that handle user traffic: api-gateway, customers-service, visits-service, vets-service, genai-service. Config Server and Discovery Server are infrastructure services — they do not emit meaningful business metrics.

**What to say in the interview:** "We intentionally excluded Config Server and Discovery Server because they do not expose Micrometer metrics. Knowing what to exclude shows you understand your platform, not just that you followed steps."

## Pitfalls
- Scraping every service including infrastructure services that emit no useful metrics — wastes storage and creates noise
- Not setting resource limits on Prometheus — high-cardinality metrics can consume significant memory
- Using `latest` tag on Prometheus image in production — breaking changes can silently change scrape behaviour

## References
- [Prometheus Docs — Kubernetes Service Discovery](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)
- [Micrometer Docs — Prometheus Registry](https://micrometer.io/docs/registry/prometheus)

## From the Project

Five of the eight Petclinic services are scraped by Prometheus:

| Service | Key metrics |
|---|---|
| api-gateway | Request throughput, circuit breaker state, latency |
| customers-service | JVM metrics, HTTP request rate |
| visits-service | JVM metrics, HTTP request rate |
| vets-service | Caffeine cache hit rate, JVM metrics |
| genai-service | AI model call latency, token usage |

The three excluded services — config-server, discovery-server, admin-server — do not expose a Micrometer metrics endpoint. Prometheus is configured not to scrape them. Saying "we intentionally excluded three services because they do not expose Micrometer metrics" in an interview signals real hands-on knowledge.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
