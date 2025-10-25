---
id: Q0105
title: How does SSH authentication work?
difficulty: easy
week: 04
topics: [linux, ssh, security]
tags: [ssh, rsa, authentication, keys]
author: supuni
reviewed: false

---

## Question
- Explain how public-key authentication works in SSH

## Short Answer
- Client proves identity using private key; server verifies using public key.

## Deep Dive
- Keys stored in ~/.ssh/id_rsa and ~/.ssh/authorized_keys.
- Uses asymmetric encryption (RSA/ECDSA/ED25519).
- Secure, passwordless automation (used in Ansible/Terraform).
## Pitfalls
- Wrong file permissions on ~/.ssh cause “Permission denied”.

## References
- systemctl, journalctl
