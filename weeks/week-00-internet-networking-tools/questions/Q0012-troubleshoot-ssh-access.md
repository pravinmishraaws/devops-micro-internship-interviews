---
id: Q0012
title: Troubleshooting SSH Access Issues
difficulty: entry
week: 00
topics: [networking, ssh, troubleshooting]
tags: [ssh, networking, linux, troubleshooting]
author: "[Hajixhayjhay](https://github.com/Hajixhayjhay)"
reviewed: false
---

## Question
How do you troubleshoot when you can’t SSH into a server?

## Short Answer
Check the basics first — **network reachability, credentials, and SSH configuration**.  
Most SSH issues come from:
1. Wrong key or username  
2. Security group or firewall blocking port 22  
3. Server SSH service not running  
4. Network path issues or misconfigured routing/NAT

## Deep Dive

### 🔹 1. Network Reachability
- **Ping** the server:  
  ```bash
  ping <server-ip>
If no response, the server may be down or blocked by a firewall.

Check SSH port (22) using telnet or nc:

bash
Copy code
nc -zv <server-ip> 22
🔹 2. Security Groups & Firewalls
On AWS: confirm your Security Group allows inbound traffic on port 22 from your IP.

On Azure: verify the Network Security Group (NSG) rules permit port 22.

Locally, check if any firewall (e.g., Windows Defender or ufw) blocks SSH.

🔹 3. SSH Key or Authentication
Ensure you’re using the right private key:

```bash

ssh -i <my-key.pem> ubuntu@<server-ip>

```
Confirm correct user (e.g., ubuntu, ec2-user, centos).

Check permissions:

```bash

chmod 400 <my-key.pem>

```

## Pitfalls
- Using a .pem key with incorrect permissions (should be 400)
- Forgetting to open port 22 in your security group
- Copying keys with line breaks or spaces
- Trying to log in with the wrong user for your OS

## References

- [AWS SSH Troubleshooting Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html)
- [Azure SSH Access Documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/linux/troubleshoot-ssh-connection)
- [DigitalOcean SSH Overview](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
