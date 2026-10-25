# Security Architecture & Policies

Security is paramount in Github Ultimate Repos. See also [SECURITY.md](../SECURITY.md) for vulnerability disclosure guidelines.

## Threat Model & Safeguards

1. **Untrusted Data Isolation**:
   All 11,730 repository descriptions, URLs, and owner names are treated as untrusted strings. The CLI and ingestion scripts utilize parameterized SQL queries (`?`) exclusively, preventing SQL injection vulnerabilities.

2. **Zero Arbitrary Execution**:
   The catalog is purely informational and index-driven. No code from external repositories is fetched, downloaded, or executed automatically.

3. **Secret Protection**:
   The repository is verified free of hardcoded API tokens, private keys, or credentials. Automated secret scanning runs on every push.

4. **Minimal Permissions in CI**:
   GitHub Actions workflows are configured with strict `contents: read` permissions.
