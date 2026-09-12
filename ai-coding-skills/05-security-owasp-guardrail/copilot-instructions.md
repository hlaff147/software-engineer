<🎯 Title>
Security OWASP Guardrail

## Rules
- ZERO SQL string concatenation — ALWAYS use parameterized queries, ORM expressions, or prepared statements
- NEVER store secrets (API keys, tokens, passwords, connection strings) in source code — use environment variables or secret managers
- Ban `eval()`, `exec()`, `os.system()`, `Runtime.exec()` with user-controlled input — use safe alternatives with allowlists
- Input validation on ALL external boundaries: HTTP params, headers, request bodies, file uploads
- Output encoding/escaping for HTML, JavaScript, URL, and SQL contexts
- Password hashing: ONLY Argon2id or BCrypt with cost factor ≥ 12 — NEVER MD5, SHA1, or SHA256 for passwords
- CORS: explicit origin allowlist — NEVER use `Access-Control-Allow-Origin: *` in production
- CSRF tokens for state-changing operations in server-rendered apps
- Rate limiting on authentication endpoints
- Secure headers: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Strict-Transport-Security`
- File uploads: validate MIME type AND file extension, scan content, store outside webroot
- NEVER log sensitive data (passwords, tokens, PII) — use structured logging with PII redaction
- HTTPS everywhere — NEVER allow mixed content
- JWT: validate signature, expiration, issuer, audience — NEVER trust unsigned tokens

## Verification
- `grep -rn 'eval\|exec\|os.system' src/`
- `grep -rn 'password.*=.*"' src/`
- dependency audit (`npm audit`, `pip audit`, `mvn dependency-check:check`)
