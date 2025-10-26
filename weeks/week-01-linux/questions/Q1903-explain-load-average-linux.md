---
id: Q1903
title: "What does load average mean in Linux?"
difficulty: easy
week: 01
topics: [linux, performance, monitoring]
tags: [load-average, performance-monitoring, system-metrics]
author: nkydigitech
reviewed: false
---

## Question
Explain load average in Linux. What do the three numbers represent, and what's considered "high"?

## Short Answer
- The three numbers represent the average number of processes waiting for CPU time over the last 1, 5, and 15 minutes, showing short-term, medium-term, and long-term load trends.
- A "high" load depends on your CPU count—a load of 1.0 per core means full utilization, so 4.0 on a 4-core system is at capacity, while 8.0 means processes are queuing.
- If the 1-minute load is high but 15-minute is low, it's a temporary spike; if all three are consistently high, you have a sustained performance problem that needs investigation.

## Deep Dive

**Understanding Load Average:**

Load average represents the number of processes in a runnable or uninterruptible state. This includes:
- Processes actively using the CPU
- Processes waiting for CPU time
- Processes waiting for I/O operations (disk, network)

**The Three Numbers:**

When you run `uptime` or `top`, you see three load average numbers:
```bash
