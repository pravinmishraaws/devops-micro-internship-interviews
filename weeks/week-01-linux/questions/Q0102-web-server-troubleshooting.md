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
Check if the service is running, view logs, verify ports/firewall, and restart or fix configuration issues.

## Deep Dive
1. **Check service status**
   ```bash
   sudo systemctl status nginx || sudo systemctl status apache2
   sudo systemctl restart nginx
Verify port and firewall

bash
Copy code
sudo ss -tulnp | grep 80
sudo ufw status
Check logs

bash
Copy code
sudo tail -n 20 /var/log/nginx/error.log
journalctl -u nginx
Validate configuration

bash
Copy code
sudo nginx -t || apachectl configtest
Check system health

bash
Copy code
df -h; free -h; top
Pitfalls
Restarting without checking logs

Ignoring port/firewall issues

Not validating configs or system resources


