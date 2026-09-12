# REST API Contract-First

## 🎯 Problem
Inconsistent API designs confuse clients, make SDK generation difficult, and lead to fragile integrations.

**Bad API Designs:**
- Returning a `200 OK` with `{ "error": "User not found" }`
- Naming endpoints with verbs: `/api/v1/createUser`
- Unstructured error messages that clients can't easily parse.
- Unpredictable response formats depending on server conditions.

## ✅ Solution
Adopt strict REST principles, standard pagination envelopes, and RFC 7807 for error reporting.

**Good API Designs:**
- Using standard HTTP verbs and plural nouns: `POST /api/v1/users`
- Explicit status codes: `404 Not Found`
- Structured, typed JSON responses for errors (RFC 7807).

## 📐 Anatomy of the Skill
Enforcing REST constraints at the controller/routing layer:
1. **Routing Definition**: Verifying HTTP methods match CRUD operations.
2. **Response Formatting**: Using standardized envelopes (pagination, errors).
3. **Status Codes**: Mapping business exceptions to precise HTTP codes.

### RFC 7807 Explanation
RFC 7807 standardizes error responses in HTTP APIs. It provides a standard structure (`type`, `title`, `status`, `detail`, `instance`) to convey machine-readable error details.

### Pagination Comparison
Instead of just returning an array `[{...}, {...}]`, use an envelope:
```json
{
  "items": [...],
  "page": 1,
  "pageSize": 20,
  "totalCount": 142,
  "totalPages": 8
}
```

## 🔧 How to Install

### Antigravity / Gemini
Copy `SKILL.md` to your skills directory.

### Cursor
Copy `.cursorrules` to the root of your repository.

### GitHub Copilot
Copy `copilot-instructions.md` to `.github/copilot-instructions.md`.

## 📊 Expected Impact
- Easier API documentation (Swagger/OpenAPI).
- Consistent client-side error handling.
- Better long-term API maintainability.

## 🔗 References
- GitHub Copilot Instructions repo.
- [RFC 7807 - Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807).
- Microsoft REST API Guidelines.
