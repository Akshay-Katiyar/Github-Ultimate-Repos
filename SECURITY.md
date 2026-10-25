# Security Policy

## Supported Versions

We prioritize the security and integrity of the **Github Ultimate Repos** ecosystem, its registry schemas, automated validation tools, and distributed workflows.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take all security vulnerabilities seriously. If you discover a security flaw, credential leakage, or unsafe execution path within any script or registry component:

1. **Do NOT open a public GitHub Issue.**
2. Send an advisory report via private email to: `security@akshaykatiyar.dev` (or directly via [GitHub Security Advisories](https://github.com/Akshay-Katiyar/Github-Ultimate-Repos/security/advisories/new)).
3. Include the following details in your report:
   - Type of vulnerability (e.g., path traversal, command injection, secret leakage, malicious external dependency).
   - Step-by-step reproduction instructions or a minimal Proof of Concept (PoC).
   - Affected scripts, schemas, or workflows.
   - Potential impact and suggested remediation.

### Response Timelines
- **Initial Acknowledgement**: Within 24 hours.
- **Triage & Impact Assessment**: Within 48 hours.
- **Remediation & Patch Deployment**: Within 7 business days for high/critical vulnerabilities.

---

## Safe Execution & Zero-Trust Mandate

1. **Untrusted Code Isolation**: Repositories cataloged within this directory are third-party open-source projects. Never execute third-party scripts or clone arbitrary binaries directly into production host environments without containerization (e.g., Docker, Microsoft MXC, or microVM sandboxes).
2. **Least Privilege by Default**: All automated workflows in `.github/workflows/` run with strictly scoped, read-only permissions (`contents: read`).
3. **Zero Secret Storage**: No API keys, credentials, or private access tokens may ever be committed to this repository. All validation tooling enforces strict pre-commit entropy and regex scanning.
