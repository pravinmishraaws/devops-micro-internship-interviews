---
id: Q0102
title: Your web server suddenly goes down, but you can still SSH into the machine. What steps would you take to identify and fix the issue?
difficulty: easy
week: 01
topics: [linux]
tags: [linux, troubleshooting, webserver]
author: amaramercy
reviewed: false
---

## Question
Your web server suddenly goes down, but you can still SSH into the machine.  
What steps would you take to identify and fix the issue?

## Short Answer
Check if the web service is running, inspect logs for errors, verify ports and firewall rules, then restart or reconfigure the service as needed.

## Deep Dive
1. **Check service status**
   ```bash
   sudo systemctl status nginx
   # or
   sudo systemctl status apache2

Look for “active (running)” or failure messages.

Restart the service

sudo systemctl restart nginx


Verify port usage

sudo ss -tulnp | grep 80


Ensures the web server is actually listening on port 80 or 443.

Check logs

/var/log/nginx/error.log

/var/log/apache2/error.log

journalctl -u nginx

Check firewall and security rules

sudo ufw status


Confirm that inbound traffic on ports 80/443 is allowed.

Check resource usage

df -h   # Disk usage
free -h # Memory usage
top     # CPU usage


Validate configuration

sudo nginx -t


or

apachectl configtest


Fix syntax errors before restarting.

Recent changes
Review recent deployments, config edits, or package updates that could have broken the service.

Pitfalls

Restarting services blindly without checking logs.

Ignoring port/firewall settings.

Not validating configuration before restarting.

Overlooking full disk or low memory.
