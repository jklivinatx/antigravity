import os
import glob
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("obsidian-mcp")

VAULT_DIR = os.environ.get("OBSIDIAN_VAULT_PATH", r"C:\Users\cary\iCloudDrive\iCloud~md~obsidian\Wobsidian")

@mcp.tool()
def search_vault_notes(query: str, max_results: int = 10) -> str:
    """Search all Markdown notes in your Obsidian vault for text or keywords."""
    if not os.path.exists(VAULT_DIR):
        return f"Obsidian vault directory not found: {VAULT_DIR}"
    
    matches = []
    query_lower = query.lower()
    
    for root, _, files in os.walk(VAULT_DIR):
        for f in files:
            if f.endswith(".md"):
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, VAULT_DIR)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        if query_lower in content.lower() or query_lower in f.lower():
                            # Find matching snippet
                            lines = content.splitlines()
                            snippet = ""
                            for line in lines:
                                if query_lower in line.lower():
                                    snippet = line.strip()
                                    break
                            matches.append(f"📄 **[[{rel_path[:-3]}]]** (`{rel_path}`)\n> {snippet[:200]}")
                            if len(matches) >= max_results:
                                break
                except Exception:
                    continue
        if len(matches) >= max_results:
            break
            
    return "\n\n".join(matches) if matches else f"No notes found matching '{query}'."

@mcp.tool()
def read_vault_note(note_name: str) -> str:
    """Read the full content of a note from your Obsidian vault by title or filename."""
    if not note_name.endswith(".md"):
        note_name += ".md"
    
    target_path = os.path.join(VAULT_DIR, note_name)
    if not os.path.exists(target_path):
        # Search recursively
        for root, _, files in os.walk(VAULT_DIR):
            if note_name.lower() in [f.lower() for f in files]:
                target_path = os.path.join(root, note_name)
                break
                
    if not os.path.exists(target_path):
        return f"Note '{note_name}' not found in vault."
        
    try:
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"Error reading note '{note_name}': {str(e)}"

@mcp.tool()
def create_or_append_note(title: str, content: str, folder: str = "", append: bool = False) -> str:
    """Create a new note or append content to an existing note in the Obsidian vault."""
    filename = title if title.endswith(".md") else f"{title}.md"
    target_dir = os.path.join(VAULT_DIR, folder) if folder else VAULT_DIR
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    
    mode = "a" if append and os.path.exists(target_path) else "w"
    try:
        with open(target_path, mode, encoding="utf-8") as f:
            if mode == "a":
                f.write(f"\n\n{content}")
            else:
                f.write(content)
        action = "Appended to" if mode == "a" else "Created"
        return f"Successfully {action.lower()} note: `{target_path}`"
    except Exception as e:
        return f"Error modifying note '{title}': {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
