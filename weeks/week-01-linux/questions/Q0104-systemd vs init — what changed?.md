id: Q0104
title: systemd vs init — what changed?
difficulty: medium
week: 02
topics: [linux, boot, services]
tags: [systemd, init, services]
author: supuni
reviewed: false

Question

Compare init and systemd. How does systemd improve service management?

Short Answer

systemd is parallel, event-driven, dependency-aware.

Replaces SysV init’s linear startup scripts.

Deep Dive

Uses unit files (.service, .target) instead of rc scripts.

Faster boot; unified logging via journald.

Pitfalls

Misconfigured dependencies (After, Requires) cause boot issues.

References

systemctl, journalctl
