# OWASP Top 10 2021 Cheatsheet

Mapping OWASP Top 10 categories to concrete coding rules:

- **A01:2021 Broken Access Control** → ALWAYS implement server-side authorization checks. Do NOT rely on client-side state or hidden fields.
- **A02:2021 Cryptographic Failures** → ONLY use Argon2id or BCrypt for hashing. Encrypt data in transit using TLS. NEVER store secrets in source code.
- **A03:2021 Injection** → ALWAYS use parameterized queries or ORMs. Validate and sanitize user input.
- **A04:2021 Insecure Design** → Follow threat modeling checklists. Ensure secure architecture from the start.
- **A05:2021 Security Misconfiguration** → Use secure defaults. Disable unused features and services. 
- **A06:2021 Vulnerable Components** → Perform regular dependency scanning (e.g., `npm audit`, `pip audit`).
- **A07:2021 Auth Failures** → Enforce strong password policies and MFA. Implement rate limiting on authentication endpoints.
- **A08:2021 Software/Data Integrity** → Ensure signed updates. Implement CI/CD pipeline security. Verify software signatures.
- **A09:2021 Logging Failures** → Implement audit logging. NEVER log sensitive data (PII, passwords).
- **A10:2021 SSRF (Server-Side Request Forgery)** → Implement URL allowlists and network segmentation. Do not blindly fetch URLs provided by users.
