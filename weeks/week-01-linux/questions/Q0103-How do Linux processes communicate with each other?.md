---
id: Q0103
title: How do Linux processes communicate with each other?
difficulty: medium
week: 02
topics: [linux, processes, ipc]
tags: [ipc, signals, sockets, pipes]
author: supuni
reviewed: false
---

## Question
- Explain different Inter-Process Communication (IPC) mechanisms in Linux.

## Short Answer
- Pipes, FIFOs, Shared Memory, Message Queues, Sockets, Signals.

## Deep Dive
- Use pipes/FIFOs for simple parent-child communication.
- Shared memory + semaphores for speed.
- Sockets for network-based IPC (used in microservices).

## Pitfalls
- Race conditions when synchronizing access to shared memory.

## References
- man ipc, ipcs, ipcrm
