# Research Options for Indexing Codebase (GitHub Copilot)

This doc explains how to index your repo so GitHub Copilot can find and reason over your code and docs.

---

## Quick Reference
- **Solo / private repo?** Use **Local Workspace Index**.
- **Team / Copilot Enterprise?** Use **Remote Workspace Index** for a shared cloud index.

---

## 1) Local Workspace Index (Recommended for private or unpublished code)

**What it is**
- Builds a **local-only** index of the repo open in VS Code.
- Makes files (code + Markdown) searchable for Copilot Chat commands like `/explain`, `/tests`, `/fix`, etc.
- The index **stays on your machine**; teammates must build their own.

**Requirements**
- VS Code with GitHub Copilot Chat extension enabled.
- Repo open in VS Code (folder/workspace).

**How to build**
1. Open the repo in VS Code.
2. Press `Ctrl/Cmd + Shift + P` → **GitHub Copilot: Build Local Workspace Index**.
3. Wait for the confirmation toast (index completed).

**Good for**
- Private/unpublished code.
- Fast personal iteration.

**Limitations**
- Not shared; each dev must build it locally.
- Rebuild after large refactors or major file moves.

---

## 2) Remote Workspace Index (Copilot Enterprise – Team Shared)

**What it is**
- Creates a **cloud-based** index for a GitHub-hosted repo.
- **Shared** across your org (access controlled by GitHub/Repo permissions).
- Available in GitHub.com (Copilot Chat) and VS Code.

**Requirements**
- Repo hosted on **GitHub**.
- **GitHub Copilot Enterprise** (org feature).
- You have access to the repo.

**How to build**
1. Open the repo (VS Code or GitHub).
2. Command Palette → **GitHub Copilot: Build Remote Workspace Index**.
3. The index becomes available to teammates who can access the repo.

**Good for**
- Cross-team collaboration, consistent shared context.
- Onboarding (new devs benefit immediately).

**Limitations**
- Requires Copilot **Enterprise**.
- Index lives in GitHub.

---



