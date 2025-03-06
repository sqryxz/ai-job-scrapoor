from scraper import scrape_cryptojobslist, scrape_web3career, generate_markdown_summary
import json
from datetime import datetime

def main():
    # Scrape jobs from both sources
    print("Scraping jobs from cryptojobslist.com...")
    crypto_jobs = scrape_cryptojobslist()
    print(f"Found {len(crypto_jobs)} jobs from cryptojobslist.com")
    
    print("\nScraping jobs from web3.career...")
    web3_jobs = scrape_web3career()
    print(f"Found {len(web3_jobs)} jobs from web3.career")
    
    # Combine all jobs
    all_jobs = crypto_jobs + web3_jobs
    print(f"\nTotal jobs found: {len(all_jobs)}")
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"jobs_{timestamp}.json"
    
    with open(json_filename, 'w') as f:
        json.dump(all_jobs, f, indent=2)
    print(f"\nJobs saved to {json_filename}")
    
    # Generate markdown summary
    generate_markdown_summary(all_jobs)
    print(f"Markdown summary generated as jobs_summary_{timestamp}.md")
    
    # Print a sample job
    if all_jobs:
        print("\nSample job listing:")
        sample_job = all_jobs[0]
        print(f"Title: {sample_job['title']}")
        print(f"Company: {sample_job['company']}")
        print(f"Location: {sample_job['location']}")
        print(f"Source: {sample_job['source']}")
        print(f"Link: {sample_job['job_link']}")
        print("\nDescription preview:")
        print(sample_job['description'][:200] + "...")

if __name__ == "__main__":
    main() 