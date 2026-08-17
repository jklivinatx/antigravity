from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS

# Initialize FastMCP Server
mcp = FastMCP("duckduckgo-search")

@mcp.tool()
def search(query: str, max_results: int = 5) -> str:
    """Search DuckDuckGo for real-time web results without requiring any API key."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "No results found."
            formatted = []
            for r in results:
                title = r.get("title", "")
                link = r.get("href", "")
                snippet = r.get("body", "")
                formatted.append(f"### [{title}]({link})\n{snippet}\n")
            return "\n".join(formatted)
    except Exception as e:
        return f"Error performing DuckDuckGo search: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
