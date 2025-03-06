import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import re
from bs4 import BeautifulSoup as bs
import os

def clean_html(html_content):
    """Convert HTML to plain text while preserving basic formatting."""
    if not html_content:
        return ""
    soup = bs(html_content, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    # Get text and preserve line breaks
    text = soup.get_text(separator='\n', strip=True)
    # Clean up extra whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

def generate_markdown_summary(jobs):
    """Generate a markdown summary of the jobs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"jobs_summary_{timestamp}.md"
    
    # Group jobs by source
    jobs_by_source = {}
    for job in jobs:
        source = job.get('source', 'Unknown Source')
        if source not in jobs_by_source:
            jobs_by_source[source] = []
        jobs_by_source[source].append(job)
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"# AI & Crypto Jobs Summary\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Write summary statistics
        f.write("## Summary Statistics\n")
        f.write(f"- Total Jobs: {len(jobs)}\n")
        for source, source_jobs in jobs_by_source.items():
            f.write(f"- {source}: {len(source_jobs)} jobs\n")
        f.write("\n")
        
        # Write jobs by source
        for source, source_jobs in jobs_by_source.items():
            f.write(f"## {source}\n\n")
            
            for job in source_jobs:
                f.write(f"### {job['title']}\n")
                f.write(f"**Company:** {job['company']}\n")
                f.write(f"**Location:** {job['location']}\n")
                
                # Add salary if available
                if job.get('salary'):
                    f.write(f"**Salary:** {job['salary']}\n")
                
                # Add posted date if available
                if job.get('posted'):
                    f.write(f"**Posted:** {job['posted']}\n")
                
                # Add tags if available
                if job.get('tags'):
                    f.write("**Tags:** " + ", ".join(job['tags']) + "\n")
                
                # Add description if available
                if job.get('description'):
                    f.write("\n**Description:**\n")
                    # Clean HTML and format description
                    clean_desc = clean_html(job['description'])
                    # Limit description length and add ellipsis
                    if len(clean_desc) > 500:
                        clean_desc = clean_desc[:497] + "..."
                    f.write(clean_desc + "\n")
                
                f.write(f"\n**Link:** {job['link']}\n")
                f.write("---\n\n")
    
    print(f"\nGenerated markdown summary: {filename}")

def extract_jobs_from_json_ld(html_content):
    jobs = []
    
    # Find all JSON-LD script tags
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script', type='application/ld+json')
    print(f"\nFound {len(script_tags)} JSON-LD script tags")
    
    for i, script in enumerate(script_tags):
        try:
            print(f"\nProcessing script tag {i + 1}:")
            data = json.loads(script.string)
            
            # Handle @graph structure
            if isinstance(data, dict) and '@graph' in data:
                items = data['@graph']
            else:
                items = [data]
            
            print(f"Number of items to process: {len(items)}")
            
            for item in items:
                if item.get('@type') == 'JobPosting':
                    job_data = {
                        "title": item.get('title', 'No title found'),
                        "company": item.get('hiringOrganization', {}).get('name', 'No company found'),
                        "location": item.get('jobLocation', {}).get('address', {}).get('addressLocality', 'Remote'),
                        "description": item.get('description', 'No description available'),
                        "link": item.get('url', '#'),
                        "source": "cryptojobslist.com",
                        "scraped_at": datetime.now().isoformat()
                    }
                    jobs.append(job_data)
                    print(f"\nFound job: {job_data['title']} at {job_data['company']}")
        except Exception as e:
            print(f"Error processing JSON-LD data: {e}")
            continue
    
    return jobs

def scrape_web3career():
    url = "https://web3.career/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        print(f"\nFetching {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = []
        
        # Find the job listings table
        job_rows = soup.find_all('tr')
        print(f"\nFound {len(job_rows)} potential job rows")
        
        for row in job_rows[1:]:  # Skip header row
            try:
                # Extract job details from the row
                cells = row.find_all('td')
                if len(cells) >= 5:  # Ensure we have enough cells
                    title_cell = cells[0]
                    company_cell = cells[1]
                    posted_cell = cells[2]
                    location_cell = cells[3]
                    salary_cell = cells[4]
                    
                    # Extract title and link
                    title_link = title_cell.find('a')
                    title = title_link.text.strip() if title_link else "No title found"
                    link = f"https://web3.career{title_link['href']}" if title_link and title_link.get('href') else "#"
                    
                    # Extract company
                    company = company_cell.text.strip() if company_cell else "No company found"
                    
                    # Extract location
                    location = location_cell.text.strip() if location_cell else "Remote"
                    
                    # Extract salary
                    salary = salary_cell.text.strip() if salary_cell else "Not specified"
                    
                    # Extract tags
                    tags = []
                    tag_links = cells[5].find_all('a') if len(cells) > 5 else []
                    for tag in tag_links:
                        tags.append(tag.text.strip())
                    
                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "posted": posted_cell.text.strip() if posted_cell else "Unknown",
                        "tags": tags,
                        "link": link,
                        "source": "web3.career",
                        "scraped_at": datetime.now().isoformat()
                    }
                    jobs.append(job_data)
                    print(f"\nFound job: {job_data['title']} at {job_data['company']}")
            
            except Exception as e:
                print(f"Error processing job row: {e}")
                continue
        
        return jobs[:10]  # Limit to first 10 jobs
    
    except Exception as e:
        print(f"Error scraping web3.career: {e}")
        return []

def scrape_cryptojobslist():
    url = "https://cryptojobslist.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        
        # Extract jobs from JSON-LD data
        jobs = extract_jobs_from_json_ld(response.text)
        
        # Limit to first 10 jobs
        return jobs[:10]
    
    except Exception as e:
        print(f"Error scraping cryptojobslist.com: {e}")
        return []

def save_jobs_to_json(jobs):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"jobs_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(jobs)} jobs to {filename}")

def send_to_discord(jobs, webhook_url):
    """Send job summary to Discord via webhook."""
    try:
        # Group jobs by source
        jobs_by_source = {}
        for job in jobs:
            source = job.get('source', 'Unknown Source')
            if source not in jobs_by_source:
                jobs_by_source[source] = []
            jobs_by_source[source].append(job)
        
        # Create Discord message
        message = {
            "embeds": [{
                "title": "🤖 AI & Crypto Jobs Summary",
                "description": f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "color": 0x00ff00,  # Green color
                "fields": [
                    {
                        "name": "📊 Summary Statistics",
                        "value": f"Total Jobs: {len(jobs)}\n" + 
                                "\n".join(f"- {source}: {len(source_jobs)} jobs" 
                                        for source, source_jobs in jobs_by_source.items()),
                        "inline": False
                    }
                ]
            }]
        }
        
        # Add fields for each source
        for source, source_jobs in jobs_by_source.items():
            jobs_text = ""
            for job in source_jobs[:5]:  # Limit to 5 jobs per source in Discord
                jobs_text += f"**{job['title']}**\n"
                jobs_text += f"Company: {job['company']}\n"
                jobs_text += f"Location: {job['location']}\n"
                if job.get('salary'):
                    jobs_text += f"Salary: {job['salary']}\n"
                if job.get('posted'):
                    jobs_text += f"Posted: {job['posted']}\n"
                jobs_text += f"Link: {job['link']}\n\n"
            
            if len(source_jobs) > 5:
                jobs_text += f"... and {len(source_jobs) - 5} more jobs"
            
            message["embeds"][0]["fields"].append({
                "name": f"🎯 {source}",
                "value": jobs_text,
                "inline": False
            })
        
        # Send to Discord
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print(f"\nSuccessfully sent summary to Discord")
        
    except Exception as e:
        print(f"Error sending to Discord: {e}")

def main():
    print("Starting job scraping...")
    
    # Scrape from both sources
    crypto_jobs = scrape_cryptojobslist()
    web3_jobs = scrape_web3career()
    
    # Combine all jobs
    all_jobs = crypto_jobs + web3_jobs
    
    # Save JSON results
    save_jobs_to_json(all_jobs)
    
    # Generate markdown summary
    generate_markdown_summary(all_jobs)
    
    # Send to Discord if webhook URL is provided
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook_url:
        send_to_discord(all_jobs, webhook_url)
    
    print("Scraping completed!")

if __name__ == "__main__":
    main() 