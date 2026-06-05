---
id: Q0401
title: How do you harden a CI/CD pipeline against supply chain attacks?
difficulty: expert
week: 04
topics: [cicd, security, devsecops, github-actions]
tags: [cicd, supply-chain, sast, secrets, oidc, sbom]
author: JulietChinenyeDuru
reviewed: false
---

## Short Answer
CI/CD pipelines are high-value attack surfaces compromising one can push malicious code to production. Hardening requires pinning dependencies, federating secrets via OIDC, enforcing least-privilege runners, signing artefacts, and scanning at every stage.

## Deep Dive

**1. Pin actions and dependencies to commit SHAs, not tags:**
```yaml
# Bad — tag can be moved
uses: actions/checkout@v4

# Good — immutable
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

**2. Replace stored secrets with OIDC federation:**
GitHub Actions to AWS/GCP/Azure using OIDC means zero long-lived credentials stored in GitHub Secrets.

**3. Least-privilege runners:**
- Use ephemeral, single-job runners (never reuse runner state)
- Never run privileged Docker containers in CI unless absolutely required
- Restrict runner network egress to known registries only

**4. Sign and verify artefacts:**
```bash
# Sign with cosign (Sigstore)
cosign sign --key cosign.key ghcr.io/myorg/myimage:sha256-abc123

# Verify before deploy
cosign verify --key cosign.pub ghcr.io/myorg/myimage:sha256-abc123
```

**5. Generate and attest SBOMs:**
```bash
syft packages ghcr.io/myorg/myimage -o spdx-json > sbom.json
cosign attest --predicate sbom.json --type spdxjson myimage
```

**6. Scan at every gate:**
- SAST: Semgrep, CodeQL
- Container scanning: Trivy, Grype
- Secret scanning: Gitleaks, Trufflehog (pre-commit + CI)
- Dependency audit: npm audit, pip-audit, trivy fs

## Pitfalls
- Trusting third-party GitHub Actions without reviewing their source or pinning to SHAs
- Printing secrets in logs — even masked secrets can leak via encoding tricks
- Using `pull_request_target` without understanding it runs in the context of the base branch with write permissions — a common RCE vector
- Not rotating OIDC trust policies when team members leave — audit `sts:AssumeRoleWithWebIdentity` conditions regularly

## References
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://slsa.dev/spec/v1.0/
- https://www.sigstore.dev/
- https://owasp.org/www-project-devsecops-guideline/