import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_cryptojobslist_example():
    """
    Example of scraping cryptojobslist.com using JSON-LD structured data
    """
    url = "https://cryptojobslist.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the webpage
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all JSON-LD script tags
    script_tags = soup.find_all('script', type='application/ld+json')
    
    jobs = []
    for script in script_tags:
        try:
            # Parse the JSON-LD data
            job_data = json.loads(script.string)
            
            # Extract job details from the structured data
            job = {
                'title': job_data.get('title', ''),
                'company': job_data.get('hiringOrganization', {}).get('name', ''),
                'location': job_data.get('jobLocation', {}).get('address', {}).get('addressLocality', ''),
                'description': job_data.get('description', ''),
                'job_link': job_data.get('url', ''),
                'source': 'cryptojobslist.com',
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            jobs.append(job)
        except json.JSONDecodeError:
            continue
            
    return jobs

def scrape_web3career_example():
    """
    Example of scraping web3.career using HTML table parsing
    """
    url = "https://web3.career/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Fetch the webpage
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the jobs table
    jobs_table = soup.find('table', {'class': 'jobs-table'})
    if not jobs_table:
        return []
    
    jobs = []
    # Find all job rows
    job_rows = jobs_table.find_all('tr')[1:]  # Skip header row
    
    for row in job_rows:
        try:
            # Extract job details from table cells
            cells = row.find_all('td')
            if len(cells) >= 5:
                job = {
                    'title': cells[0].text.strip(),
                    'company': cells[1].text.strip(),
                    'location': cells[2].text.strip(),
                    'salary': cells[3].text.strip(),
                    'posted_date': cells[4].text.strip(),
                    'description': '',  # Would need to visit individual job pages
                    'job_link': cells[0].find('a')['href'] if cells[0].find('a') else '',
                    'source': 'web3.career',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                jobs.append(job)
        except Exception as e:
            print(f"Error processing job row: {e}")
            continue
            
    return jobs

def main():
    # Example usage
    print("Scraping cryptojobslist.com...")
    crypto_jobs = scrape_cryptojobslist_example()
    print(f"Found {len(crypto_jobs)} jobs from cryptojobslist.com")
    
    print("\nScraping web3.career...")
    web3_jobs = scrape_web3career_example()
    print(f"Found {len(web3_jobs)} jobs from web3.career")
    
    # Print sample jobs
    if crypto_jobs:
        print("\nSample job from cryptojobslist.com:")
        print(json.dumps(crypto_jobs[0], indent=2))
    
    if web3_jobs:
        print("\nSample job from web3.career:")
        print(json.dumps(web3_jobs[0], indent=2))

if __name__ == "__main__":
    main() 