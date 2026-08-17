import requests
import urllib.parse
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("job-search-mcp")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

@mcp.tool()
def search_linkedin_jobs(keywords: str, location: str = "United States", count: int = 10) -> str:
    """Search LinkedIn Jobs for free without requiring any account login or API key.
    Uses LinkedIn's public guest search endpoint."""
    try:
        kw_encoded = urllib.parse.quote(keywords)
        loc_encoded = urllib.parse.quote(location)
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={kw_encoded}&location={loc_encoded}"
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="base-search-card")
        
        if not cards:
            return f"No LinkedIn jobs found for '{keywords}' in '{location}'."
            
        results = []
        for card in cards[:count]:
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            loc_tag = card.find("span", class_="job-search-card__location")
            link_tag = card.find("a", class_="base-card__full-link")
            time_tag = card.find("time")
            
            title = title_tag.text.strip() if title_tag else "Job Title"
            company = company_tag.text.strip() if company_tag else "Company"
            loc = loc_tag.text.strip() if loc_tag else location
            link = link_tag.get("href", "").split("?")[0] if link_tag else "#"
            date_posted = time_tag.text.strip() if time_tag else ""
            
            results.append(f"### [{title}]({link})\n- **Company:** {company}\n- **Location:** {loc}\n- **Posted:** {date_posted}\n")
            
        return "\n".join(results)
    except Exception as e:
        return f"Error searching LinkedIn jobs: {str(e)}"

@mcp.tool()
def search_indeed_jobs(keywords: str, location: str = "United States", count: int = 10) -> str:
    """Search Indeed for current job postings and opening links."""
    try:
        query = f"site:indeed.com/viewjob {keywords} {location}"
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=count))
            
        if not raw_results:
            return f"No Indeed job postings found for '{keywords}' in '{location}'."
            
        results = []
        for r in raw_results:
            title = r.get("title", "Job Posting").replace(" - Indeed.com", "").replace(" - Indeed", "")
            link = r.get("href", "")
            snippet = r.get("body", "")
            results.append(f"### [{title}]({link})\n- **Source:** Indeed\n- **Summary:** {snippet}\n")
            
        return "\n".join(results)
    except Exception as e:
        return f"Error searching Indeed jobs: {str(e)}"

@mcp.tool()
def search_google_jobs(keywords: str, location: str = "United States", count: int = 10) -> str:
    """Search Google Jobs and major careers boards across the web."""
    try:
        query = f"{keywords} jobs in {location} careers apply"
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(query, max_results=count))
            
        if not raw_results:
            return f"No jobs found for '{keywords}' in '{location}'."
            
        results = []
        for r in raw_results:
            title = r.get("title", "Job Opening")
            link = r.get("href", "")
            snippet = r.get("body", "")
            results.append(f"### [{title}]({link})\n- **Details:** {snippet}\n")
            
        return "\n".join(results)
    except Exception as e:
        return f"Error searching Google Jobs: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
