

## From the Project

Security in the Petclinic Platform is built in at every layer:

- **No long-lived credentials:** GitHub Actions uses OIDC; pods use IRSA — access keys do not exist in this system
- **Secrets at runtime:** MySQL credentials and the OpenAI API key live in AWS Secrets Manager, injected by the External Secrets Operator — never in environment variables in the deployment YAML
- **Network isolation:** RDS has no public endpoint; port 3306 is allowed only from the EKS node security group
- **Image scanning:** ECR scan-on-push is enabled — every image is scanned for known CVEs before ArgoCD can deploy it

Security is not a section at the end. It is a decision made at every layer of the stack.

*Built as part of the [DevOps with Claude Code: Terraform, EKS, ArgoCD & Helm](https://www.udemy.com/course/devops-with-claude-code-terraform-eks-argocd-helm/?referralCode=1C5B734505D65A010FA3) course.*
