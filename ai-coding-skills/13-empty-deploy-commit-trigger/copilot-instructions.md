# Empty Deploy Commit Trigger for GitHub Copilot

When the user asks to trigger a deployment without code changes ("commit no content", "commit vazio", "trigger deploy", "deploy uat"):

1. Create an empty commit without staged files:
   `git commit --allow-empty -m "ci: #deployuat #auto"`

2. Immediately push to current branch:
   `git push origin $(git branch --show-current)`

3. Rules:
   - Message must be strictly `"ci: #deployuat #auto"`.
   - Never stage or alter files during this command.
   - Always push immediately to trigger the CI/CD pipeline.
