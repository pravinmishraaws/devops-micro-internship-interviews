---
id: 2
title: Readiness, liveness, and startup probes — what they do and when each fires
difficulty: medium
week: 10
topics: [kubernetes, probes, health-checks, deployments]
tags: [readiness, liveness, startup, probes, actuator, health]
author: pravinmishraaws
reviewed: true
---

## Question
What is the difference between readiness, liveness, and startup probes in Kubernetes? When does each one fire, and what happens when each one fails?

## Short Answer
Readiness controls traffic: a pod that fails its readiness probe is removed from the Service endpoint — it stays running but receives no requests. Liveness controls restarts: a pod that fails its liveness probe is killed and restarted. Startup probes protect slow-starting containers — liveness and readiness are paused until the startup probe passes.

## Deep Dive
Three probes, three jobs:

**Readiness probe** — "Is this pod ready to serve traffic?"
- Checked continuously throughout the pod's lifetime
- Failure: pod is removed from the Service's endpoint list — no new requests reach it
- Recovery: pod is re-added when the probe passes again
- Use case: a pod that is temporarily overloaded, doing a long DB migration, or waiting for a dependency

**Liveness probe** — "Is this pod still alive?"
- Checked continuously throughout the pod's lifetime
- Failure: pod is killed and restarted (respects `restartPolicy`)
- Use case: detect deadlocks, hung threads, or states the process cannot recover from on its own

**Startup probe** — "Has this pod finished starting?"
- Checked only during startup
- While the startup probe is pending, both liveness and readiness probes are suspended
- Failure: pod is killed and restarted — same as liveness
- Use case: slow-starting applications (JVM warm-up, large schema migrations) where a liveness probe would kill the pod before it finishes booting

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  initialDelaySeconds: 60
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8081
  initialDelaySeconds: 30
  periodSeconds: 5
  failureThreshold: 3
```

**What happens during a rolling update without readiness probes?** Kubernetes sends traffic to the new pod immediately after it starts, before the JVM is ready to serve requests. Users get connection errors. Readiness probes are what make rolling updates safe.

## Pitfalls
- Setting `initialDelaySeconds` too low for JVM services — the liveness probe kills the pod during startup before it has warmed up
- Pointing liveness at a dependency (database, external API) — if the DB goes down, Kubernetes restarts every pod in a loop, making the outage worse
- Not setting a readiness probe at all — traffic hits pods that are still initializing, causing 502 errors during deploys
- Using the same endpoint for liveness and readiness when they should behave differently

## References
- [Kubernetes Docs — Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Spring Boot Actuator — Health Groups](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.health.groups)

## From the Project

All eight Petclinic microservices expose Spring Boot Actuator health endpoints:

- `/actuator/health/readiness` — checks if the service is ready to accept traffic (DB connections, config loaded)
- `/actuator/health/liveness` — checks if the service process is alive and not deadlocked

The Kubernetes manifests in `k8s/base/<service>/deployment.yaml` configure both probes for every service. Spring Boot 2.3+ splits the `/actuator/health` endpoint into readiness and liveness groups automatically — no custom code required.

The JVM services take 30–60 seconds to start. Setting `initialDelaySeconds: 60` on the liveness probe ensures the container is not killed during JVM warm-up. The readiness probe uses a shorter `initialDelaySeconds` so traffic is only sent once the application context is fully loaded.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
