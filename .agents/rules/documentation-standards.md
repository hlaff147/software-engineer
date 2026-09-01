# 📝 Documentation Standards Rule

This rule defines the required structure and quality standards for all documentation files across this repository.

---

## 🏗️ Standard Subproject README Structure

Every subproject directory must contain a `README.md` containing at minimum:

1. **Title & Badge Header**: Clear title and relevant technology badges.
2. **Overview & Business Problem**: What this project solves and why it matters.
3. **Architecture / System Design**: ASCII diagram, mermaid flowchart, or table showing component interactions.
4. **Key Features & Design Patterns**: Bullet points and tables detailing applied design patterns.
5. **Tech Stack**: List of language versions, frameworks, and build tools.
6. **How to Run / Quick Start**:
   - Prerequisites (e.g. Java 17+, Python 3.11+, Docker).
   - Build command (`mvn clean install`, `./gradlew build`, `poetry install`, etc.).
   - Execution command (`mvn spring-boot:run`, `python main.py`, etc.).
   - Test command (`mvn test`, `pytest`, etc.).
   - Curl / HTTP request examples with expected responses (for APIs).

---

## 🎨 Root `README.md` Showcase Format

When featuring a project in the root [README.md](../../README.md), use the two-column table pattern:

```markdown
### [Project Name](./project-folder)

Short one-line description of the project.

<table>
<tr>
<td width="50%">

**🏗️ Architecture / System Design**
\`\`\`
[ASCII Diagram]
\`\`\`

</td>
<td width="50%">

**✨ Features / Highlights**
| Feature | Description |
|---------|-------------|
| ... | ... |

</td>
</tr>
</table>

**Tech Stack:** `Tech1` `Tech2` `Tech3`
```

---

## 🔗 Link Integrity Rules

- Always use **relative paths** starting with `./` or `../` for local links.
- Test links to ensure target files exist before committing changes.
- Do not link to non-existent license files, missing folders, or dummy references.
