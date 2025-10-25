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
- Client proves identity using private key; server verifies using public key.

## Short Answer
- Keys stored in ~/.ssh/id_rsa and ~/.ssh/authorized_keys.
- Uses asymmetric encryption (RSA/ECDSA/ED25519).
- Secure, passwordless automation (used in Ansible/Terraform).

## Deep Dive
- Wrong file permissions on ~/.ssh cause “Permission denied”.

## Pitfalls
- man ssh-keygen, man sshd_config


## References
- systemctl, journalctl
