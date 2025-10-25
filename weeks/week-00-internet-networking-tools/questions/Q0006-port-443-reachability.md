---
id: Q0006
title: Checking Port 443 Reachability — TCP vs TLS vs HTTPS
difficulty: intermediate
week: 00
topics: [internet, networking, tools]
tags: [tcp, tls, https, troubleshooting]
author: RanbirKaur11
reviewed: false
---

## Question
When troubleshooting a service on a remote host running on port 443, which commands can you use to check if the port is open and reachable, and how are the commands different?

## Short Answer
- `nc` / `Test-NetConnection` → checks **can we reach port 443 at all?**
- `openssl s_client` → checks **is SSL working and is the certificate okay?**
- `curl` → checks **is the website actually loading over HTTPS?**
- `nmap` → checks **is the port open or blocked by firewall?**
 

## Deep Dive
1. **TCP Reachability (Basic network test)**
   - This checks if the server is listening on port 443.
   - If this fails → firewall or service is down.
   - **Example:**
     - Linux/macOS: `nc -vz example.com 443`
     - Windows: `Test-NetConnection example.com -Port 443`

2. **TLS Handshake (SSL check)**
   - This checks if HTTPS security works and if certificate is valid.
   - If this fails → certificate issue or missing SNI.
   - **Example:**
     - `openssl s_client -connect example.com:443 -servername example.com`

3. **HTTPS Response (Web application check)**
   - Confirms the actual website is loading over HTTPS.
   - If this fails → app issue (backend, gateway, or configuration).
   - **Example:**
     - `curl -vk https://example.com/`

4. **Port Scan (Firewall / filtering check)**
   - Shows whether port 443 is open, closed, or filtered.
   - If `filtered` → blocked by firewall/WAF.
   - **Example:**
     - `nmap -p 443 example.com`

## Pitfalls
- TCP success ≠ HTTPS success. TCP success does **not** mean the website is working — HTTPS can still fail.
- If **SNI** is missing, the server may show the **wrong certificate**. SNI (Server Name Indication) tells the server which website’s SSL certificate it should show when many websites share the same IP.
- `curl` errors may indicate **application problems**, not network issues.

## References
- IANA (Port 443 - HTTPS): https://www.iana.org/assignments/service-names-port-numbers/
- Test-NetConnection (Microsoft Docs): https://learn.microsoft.com/powershell/module/nettcpip/test-netconnection
- OpenSSL s_client: https://www.openssl.org/docs/
- curl HTTPS usage: https://curl.se/docs/https/
- nmap basics: https://nmap.org/book/