# Lab 3.1: Pull Request Suggestions for Security Vulnerabilities in Multi-Service Repos

### Objectives:
    - Learn to use GitHub Copilot Chat to detect potential security vulnerabilities in a codebase.
    - Practice generating a Pull Request draft that fixes the identified issues.
    - Use contextual prompts to ensure PR descriptions follow your enterprise’s contribution guidelines.
    - Leverage Copilot’s access to multi-file context for version-aware security fixes.

### Scenario:
Your organization has a `user-service` microservice in a large monorepo. A recent code review flagged that passwords are stored in plain text in the database — a critical security flaw.

You must:
1. Detect the issue using Copilot Chat’s contextual search capabilities.
2. Implement a fix using secure password hashing (e.g., bcrypt).
3. Create a PR draft with:
   - Clear title
   - Detailed description of changes
   - References to the security standard (e.g., OWASP Top 10)

### Instructions:

Part 1 — Detecting the Vulnerability
1. Search for instances of `password` handling across the `user-service` folder using Copilot Chat.
2. Identify functions or classes where plain-text passwords are being stored.

Part 2 — Implementing the Fix
1. Update the affected code to:
   - Use a secure password hashing algorithm.
   - Never store passwords in plain text.
2. Ensure backward compatibility for existing user logins by implementing a migration strategy.

Part 3 — Creating a PR Draft with Copilot
1. Use Copilot Chat in GitHub’s PR view to:
   - Auto-generate the PR title and description.
   - Include “Before” and “After” code snippets in the PR description.
   - Reference the security ticket ID from your internal tracker.

#### Starter Code Snippet:
```python
def create_user(username, password):
    # TODO: Replace plain text storage with secure hashing
    db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    return {"status": "success", "user": username}
