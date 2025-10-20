name: "New Question"
description: "Propose a new interview question (and optional answer)"
title: "[Question] <Week> <Short title>"
labels:
  - "type:question"
body:
  - type: dropdown
    id: week
    attributes:
      label: "Week"
      options:
        - "00 Internet/Networking"
        - "01 Linux"
        - "02 Git & GitHub"
        - "03 DevOps Lifecycle"
        - "04 AWS"
        - "05 Azure"
        - "06 Terraform"
        - "07 Ansible"
        - "08 Azure DevOps CI/CD"
        - "09 Docker"
        - "10 Kubernetes"
        - "11 Observability"
    validations:
      required: true
  - type: input
    id: title
    attributes:
      label: "Title"
      placeholder: "Example: Rolling vs Blue/Green vs Canary"
    validations:
      required: true
  - type: dropdown
    id: difficulty
    attributes:
      label: "Difficulty"
      options:
        - "entry"
        - "easy"
        - "medium"
        - "hard"
        - "expert"
    validations:
      required: true
  - type: textarea
    id: outline
    attributes:
      label: "Outline or Draft Answer"
      description: "Bullet points or a draft answer"
