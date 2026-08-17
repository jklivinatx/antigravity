import urllib.request
import re
import json
from html import unescape
import os

JOBVITE_BASE = "https://jobs.jobvite.com"
JOBS_PAGE_URL = "https://jobs.jobvite.com/nyrr"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_html(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def get_job_openings():
    print("Fetching NYRR jobs page...")
    html = fetch_html(JOBS_PAGE_URL)
    
    # Split by department headings <h3 class="h2">Category Name</h3>
    # Or find all categories and job tables
    categories_data = []
    
    # Pattern to match <h3 class="h2">Category</h3> followed by <table class="jv-job-list">...</table>
    cat_blocks = re.split(r'<h3 class="h2">(.*?)</h3>', html)
    
    # cat_blocks[0] is preamble before first category
    # cat_blocks[1] is 1st cat name, cat_blocks[2] is 1st cat table html...
    for i in range(1, len(cat_blocks), 2):
        category_name = unescape(cat_blocks[i].strip())
        block_html = cat_blocks[i+1]
        
        # Extract rows <tr> <td class="jv-job-list-name"> <a href="/nyrr/job/JOB_ID">Job Title</a> </td> <td class="jv-job-list-location"> Location </td> </tr>
        job_matches = re.findall(
            r'<td class="jv-job-list-name">\s*<a href="([^"]+)">(.*?)</a>\s*</td>\s*<td class="jv-job-list-location">\s*(.*?)\s*</td>',
            block_html,
            re.DOTALL
        )
        
        jobs_in_cat = []
        for href, title, location in job_matches:
            clean_title = unescape(re.sub(r'<[^>]+>', '', title)).strip()
            clean_loc = unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', location))).strip()
            full_url = JOBVITE_BASE + href if href.startswith('/') else href
            job_id = href.split('/')[-1] if '/job/' in href else ''
            
            jobs_in_cat.append({
                "id": job_id,
                "title": clean_title,
                "location": clean_loc,
                "url": full_url,
                "category": category_name
            })
            
        if jobs_in_cat:
            categories_data.append({
                "category": category_name,
                "jobs": jobs_in_cat
            })
            
    return categories_data

def enrich_job_details(job):
    try:
        print(f"Fetching details for: {job['title']} ({job['url']})...")
        job_html = fetch_html(job['url'])
        
        # Look for JSON-LD JobPosting schema
        json_ld_match = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', job_html, re.DOTALL)
        if json_ld_match:
            data = json.loads(json_ld_match.group(1))
            job['date_posted'] = data.get('datePosted', '')
            job['employment_type'] = data.get('employmentType', '')
            
            # Extract description text summary
            desc_html = data.get('description', '')
            # Try to extract compensation rate if mentioned
            rate_match = re.search(r'(Hourly Rate|Salary|Pay Rate)\s*:?\s*(\$[\d\.\,\s\-]+(?:\s*per\s*hour|\s*\/hr)?)', desc_html, re.IGNORECASE)
            if rate_match:
                job['compensation'] = rate_match.group(2).strip()
            else:
                # check plain text search in desc_html
                rate_match_2 = re.search(r'\$[\d\.]+(?:\s*\-\s*\$[\d\.]+)?\s*(?:per hour|\/hr|\/hour)', desc_html, re.IGNORECASE)
                if rate_match_2:
                    job['compensation'] = rate_match_2.group(0).strip()
                else:
                    job['compensation'] = ''
        else:
            job['date_posted'] = ''
            job['employment_type'] = ''
            job['compensation'] = ''
    except Exception as e:
        print(f"Error enriching {job['title']}: {e}")
        job['date_posted'] = ''
        job['employment_type'] = ''
        job['compensation'] = ''
        
def generate_markdown(categories_data, output_filepath):
    total_jobs = sum(len(cat['jobs']) for cat in categories_data)
    
    md_lines = []
    md_lines.append("# New York Road Runners (NYRR) Job Openings")
    md_lines.append("")
    md_lines.append(f"> **Total Active Openings:** {total_jobs} positions  ")
    md_lines.append(f"> **Source Portal:** [NYRR Jobvite Careers](https://jobs.jobvite.com/nyrr)  ")
    md_lines.append(f"> **Last Updated:** August 10, 2026  ")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Table of contents
    md_lines.append("## Categories")
    for cat in categories_data:
        cat_anchor = cat['category'].lower().replace(' ', '-').replace('&', '').replace('--', '-')
        md_lines.append(f"- [{cat['category']} ({len(cat['jobs'])} roles)](#{cat_anchor})")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Category sections
    for cat in categories_data:
        md_lines.append(f"## {cat['category']}")
        md_lines.append("")
        for job in cat['jobs']:
            md_lines.append(f"### [{job['title']}]({job['url']})")
            md_lines.append(f"- **Location:** {job['location']}")
            if job.get('employment_type'):
                md_lines.append(f"- **Type:** {job['employment_type']}")
            if job.get('compensation'):
                md_lines.append(f"- **Compensation:** {job['compensation']}")
            if job.get('date_posted'):
                md_lines.append(f"- **Posted Date:** {job['date_posted']}")
            md_lines.append(f"- **Apply Link:** [View & Apply on Jobvite]({job['url']})")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
    md_lines.append("## General Application")
    md_lines.append("If you do not see a role matching your profile, NYRR accepts general applications:")
    md_lines.append("- [NYRR General Application Link](https://jobs.jobvite.com/nyrr/apply)")
    md_lines.append("")
    
    content = "\n".join(md_lines)
    
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated markdown file at: {output_filepath}")

if __name__ == "__main__":
    jobs_data = get_job_openings()
    for cat in jobs_data:
        for job in cat['jobs']:
            enrich_job_details(job)
            
    output_path = os.path.join(os.getcwd(), "nyrr_job_openings.md")
    generate_markdown(jobs_data, output_path)
