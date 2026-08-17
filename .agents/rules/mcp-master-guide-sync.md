---
trigger: always_on
description: Automatically keep the Antigravity Master Guide & Cheatsheet updated in the repository and Obsidian vault whenever MCP servers or tools change.
---

# MCP & Master Guide Auto-Sync Rule

Whenever you add, modify, reconfigure, or remove any MCP server (Model Context Protocol) or custom agent tool:

1. **Update Master Guides:**
   - Update [`Antigravity Master Guide & Cheatsheet.md`](../../Antigravity%20Master%20Guide%20&%20Cheatsheet.md) in the root of the workspace.
   - Update the mirrored copy in the user's Obsidian vault at `C:\Users\cary\iCloudDrive\iCloud~md~obsidian\Wobsidian\antigravity-gemini\Antigravity Master Guide & Cheatsheet.md`.

2. **Document the Changes:**
   - Include the new server name, capabilities, configuration script path, and available tools.

3. **Sync to GitHub:**
   - Automatically stage, commit, and push the updated documentation and configuration to GitHub (`origin/main`).
