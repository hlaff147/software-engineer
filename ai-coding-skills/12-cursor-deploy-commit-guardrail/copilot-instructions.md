# Deploy Commit Guardrail for GitHub Copilot

Whenever generating git commit messages or running terminal commit commands:

1. **Pre-Commit Interactive Question**:
   Before proposing or executing `git commit`, always ask the user:
   "Deseja acionar o deploy (UAT) com este commit? (Sim / Não)"

2. **Commit Message Format on 'Yes'**:
   Append `#deployuat #auto` preceded by an empty line:
   ```
   <type>(<scope>): <short imperative description>

   <optional detailed body>

   #deployuat #auto
   ```

3. **Commit Message Format on 'No'**:
   Proceed with standard Conventional Commits without the deploy hashtags.

4. **Rules**:
   - The hashtags `#deployuat #auto` are mandatory triggers for CI/CD.
   - Do not change their spelling, casing, or order.
   - Always keep them separated from previous paragraphs by a blank line.
