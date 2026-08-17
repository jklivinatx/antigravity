import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("readwise-mcp")

def get_headers():
    token = os.environ.get("READWISE_TOKEN", "").strip()
    if not token:
        raise ValueError("READWISE_TOKEN environment variable is not set. Get your token from https://readwise.io/access_token")
    return {"Authorization": f"Token {token}"}

@mcp.tool()
def get_books(category: str = "") -> str:
    """List books, articles, podcasts, or tweets saved in your Readwise library.
    Optional category: 'books', 'articles', 'tweets', 'podcasts'."""
    try:
        url = "https://readwise.io/api/v2/books/"
        params = {}
        if category:
            params["category"] = category
        r = requests.get(url, headers=get_headers(), params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if not results:
            return "No books/articles found in Readwise."
        
        output = []
        for b in results[:20]:
            output.append(f"- **{b.get('title')}** by *{b.get('author', 'Unknown')}* ({b.get('num_highlights')} highlights) - ID: {b.get('id')}")
        return "\n".join(output)
    except Exception as e:
        return f"Error querying Readwise books: {str(e)}"

@mcp.tool()
def get_highlights(book_id: int = 0, query: str = "") -> str:
    """Fetch highlights from Readwise. Optionally filter by book_id or search query."""
    try:
        url = "https://readwise.io/api/v2/highlights/"
        params = {}
        if book_id > 0:
            params["book_id"] = book_id
        r = requests.get(url, headers=get_headers(), params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if not results:
            return "No highlights found."
        
        output = []
        for h in results:
            text = h.get("text", "")
            if query and query.lower() not in text.lower():
                continue
            output.append(f"> {text}\n*Note: {h.get('note', '')} | Highlighted on: {h.get('highlighted_at', '')}*\n")
            if len(output) >= 15:
                break
        return "\n".join(output) if output else f"No highlights matching '{query}' found."
    except Exception as e:
        return f"Error querying Readwise highlights: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
