---
id: Q0102
title: Recover deleted /etc/nginx/nginx.conf quickly
difficulty: easy
week: 01
topics: [linux, nginx, troubleshooting]
tags: [nginx, configuration, recovery, linux]
author: amaramercy
reviewed: false
---

## Question
Someone accidentally deleted `/etc/nginx/nginx.conf`. What can you do to recover quickly?

## Short Answer
- If Nginx is still running, **copy the configuration from memory or the process**:
  ```bash
  ps -ef | grep nginx
  cat /proc/<nginx-master-pid>/cmdline
  nginx -T > /etc/nginx/nginx.conf.recovered
Otherwise, restore from a backup, package default, or version control.

Finally, test and reload:

bash
Copy code
nginx -t && systemctl reload nginx
Deep Dive
If Nginx is still running:

Dump the active config:

bash
Copy code
nginx -T > /etc/nginx/nginx.conf.recovered
Confirm paths:

bash
Copy code
ps aux | grep nginx
Validate:

bash
Copy code
nginx -t
If Nginx is not running:

Check package defaults:

Debian/Ubuntu: /usr/share/nginx/

CentOS/RHEL: /etc/nginx/nginx.conf.default

Reinstall config templates:

bash
Copy code
sudo apt reinstall nginx
Or recover from Git if configs are versioned.

Prevent recurrence:

Manage /etc/nginx/ under version control.

Restrict write/delete permissions.

Keep nightly backups.

Pitfalls / Gotchas
Restarting Nginx before recovery loses the in-memory config.

Forgetting to test with nginx -t can cause downtime.

Reinstalling may overwrite other custom configs.

