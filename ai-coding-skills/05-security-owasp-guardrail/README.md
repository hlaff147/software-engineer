# Security OWASP Guardrail

## 🎯 Problem
Insecure coding practices expose applications to serious vulnerabilities, often stemming from improper handling of user input, lack of access control, or insecure configurations.

**Bad Examples:**

1. SQL Injection:
```javascript
// BAD: String concatenation makes it vulnerable to SQL Injection
const query = `SELECT * FROM users WHERE username = '${req.body.username}'`;
db.execute(query);
```

2. Hardcoded Secrets:
```python
# BAD: Storing secrets in source code
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE" 
```

3. `eval()` Usage:
```javascript
// BAD: Evaluating user input directly
const result = eval(req.body.expression);
```

4. Weak Cryptography:
```python
import hashlib
# BAD: Using MD5 for passwords
hashed = hashlib.md5(password.encode()).hexdigest()
```

## ✅ Solution
Adopt defensive coding practices aligned with OWASP Top 10. 

**Good Examples:**

1. Parameterized Queries:
```javascript
// GOOD: Using parameterized queries
const query = `SELECT * FROM users WHERE username = ?`;
db.execute(query, [req.body.username]);
```

2. Externalizing Secrets:
```python
import os
# GOOD: Using environment variables
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
```

3. Safe Parsing:
```javascript
// GOOD: Safe parsing instead of eval
const result = JSON.parse(req.body.data);
```

4. Strong Hashing:
```python
import bcrypt
# GOOD: Using BCrypt for password hashing
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

## 📐 Anatomy of the skill
The skill targets common OWASP vulnerabilities:
- Injection flaws are mitigated by banning string concatenation in queries and using parameterized alternatives.
- Cryptographic failures are addressed by enforcing strong hashing algorithms and external secret storage.
- Insecure execution is prevented by banning functions like `eval()` or `os.system()`.

## 🔧 How to install
- **Gemini/Antigravity**: Place `SKILL.md` in your AI coding skills directory.
- **Cursor**: Copy `.cursorrules` into the root of your project.
- **GitHub Copilot**: Save `copilot-instructions.md` as `.github/copilot-instructions.md`.

## 📊 Expected impact
- Significant reduction in severe security vulnerabilities (e.g., SQLi, RCE).
- Compliance with industry security standards like the OWASP Top 10.
- Safer credential and secret management.

## 🔗 References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- `references/owasp-top10-cheatsheet.md`
