---
id: 5
title: How does Prometheus scrape metrics from pods in EKS?
difficulty: medium
week: 11
topics: [observability, prometheus, kubernetes, metrics, eks]
tags: [prometheus, scraping, servicemonitor, actuator, micrometer, annotations, eks]
author: pravinmishraaws
reviewed: true
---

## Question
How does Prometheus know which pods to scrape for metrics in a Kubernetes cluster? What does a pod need to expose to be scraped?

## Short Answer
Prometheus discovers pods using Kubernetes service discovery — it reads the cluster's API to find pods and services with the right annotations or `ServiceMonitor` CRDs. The pod exposes metrics at a `/metrics` endpoint (HTTP GET), and Prometheus pulls from it on a configurable interval.

## Deep Dive
**Two ways to configure scraping:**

**1. Pod annotations (simple):**
```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/actuator/prometheus"
    prometheus.io/port: "8081"
```
Prometheus is configured with a `kubernetes_sd_config` job that relabels pods with these annotations and scrapes them automatically.

**2. ServiceMonitor CRD (kube-prometheus-stack):**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: customers-service
  namespace: petclinic-dev
spec:
  selector:
    matchLabels:
      app: customers-service
  endpoints:
    - port: http
      path: /actuator/prometheus
      interval: 15s
```
The Prometheus Operator watches `ServiceMonitor` CRDs and generates the scrape config automatically. This is the preferred approach in production — declarative, namespace-scoped, and version-controlled in Git.

**What the pod needs:**
- An HTTP endpoint that returns metrics in Prometheus exposition format (plain text, one metric per line)
- A port exposed on the Service that Prometheus can reach
- Spring Boot with Micrometer + `spring-boot-starter-actuator` exposes `/actuator/prometheus` automatically when the `prometheus` dependency is on the classpath

**Scrape flow:**
1. Prometheus polls the Kubernetes API for matching pods/services every `resync_period`
2. For each target, Prometheus sends `GET /actuator/prometheus` every `interval` (15s default)
3. Prometheus parses the response and stores the time series in its TSDB
4. Grafana queries Prometheus via PromQL to render dashboards

## Pitfalls
- Pods not in the right namespace for the `ServiceMonitor` — the `ServiceMonitor` and the service must be in the same namespace, or RBAC must explicitly allow cross-namespace scraping
- Port name mismatch — `ServiceMonitor.endpoints.port` must match the port **name** in the Service spec, not the number
- Missing the Micrometer Prometheus dependency — Spring Boot exposes `/actuator/health` by default but not `/actuator/prometheus` without `micrometer-registry-prometheus` on the classpath
- Firewalls blocking port 8080+ on EKS node security groups — Prometheus runs in the cluster and goes pod-to-pod, but if your node SG restricts intra-cluster traffic, scraping fails

## References
- [Prometheus Docs — Kubernetes Service Discovery](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)
- [Prometheus Operator — ServiceMonitor](https://prometheus-operator.dev/docs/user-guides/getting-started/)
- [Spring Boot Docs — Actuator Metrics](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics)

## From the Project

All eight Petclinic services expose `/actuator/prometheus` via Spring Boot Actuator and Micrometer. The dependency in each service's `pom.xml`:

```xml
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

The `terraform/modules/observability/` module deploys the `kube-prometheus-stack` Helm chart — this gives you Prometheus, the Prometheus Operator, Grafana, and a set of default Kubernetes dashboards in one install.

`ServiceMonitor` CRDs in `k8s/base/` tell the Prometheus Operator which services to scrape, which path (`/actuator/prometheus`), and at what interval. Every service gets its own `ServiceMonitor` — scoped to its port and path so Prometheus only scrapes what each service exposes.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
