# AI & Crypto Job Finder 🤖

A Python-based job aggregator that scrapes and summarizes AI and cryptocurrency job listings from multiple sources. The tool automatically collects job postings, generates detailed summaries, and can share updates via Discord webhooks.

## Features ✨

- **Multi-Source Job Scraping**
  - [cryptojobslist.com](https://cryptojobslist.com/)
  - [web3.career](https://web3.career/)
  - (More sources coming soon!)

- **Comprehensive Job Information**
  - Job title and company
  - Location and salary details
  - Posted date and tags
  - Full job descriptions
  - Direct links to job postings

- **Multiple Output Formats**
  - JSON file with complete job data
  - Markdown summary for easy reading
  - Discord webhook integration for instant updates

- **Smart Features**
  - HTML cleaning for readable descriptions
  - Automatic job deduplication
  - Source-specific data extraction
  - Error handling and logging

## Prerequisites 📋

- Python 3.7 or higher
- pip (Python package installer)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-crypto-job-summary.git
cd ai-crypto-job-summary
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Discord webhook:
   - Go to your Discord server
   - Select a channel
   - Click the gear icon (Edit Channel)
   - Go to Integrations
   - Click "Create Webhook"
   - Give it a name (e.g., "AI & Crypto Jobs")
   - Copy the webhook URL
   - Set it as an environment variable:
     ```bash
     export DISCORD_WEBHOOK_URL="your-webhook-url-here"
     ```

## Usage 💡

1. Run the scraper:
```bash
python3 scraper.py
```

2. The script will:
   - Scrape jobs from all configured sources
   - Save complete job data to a JSON file (`jobs_YYYYMMDD_HHMMSS.json`)
   - Generate a markdown summary (`jobs_summary_YYYYMMDD_HHMMSS.md`)
   - Send updates to Discord (if webhook URL is configured)

## Output Files 📁

### JSON Output (`jobs_YYYYMMDD_HHMMSS.json`)
Contains complete job data in structured format:
```json
{
  "title": "Job Title",
  "company": "Company Name",
  "location": "Job Location",
  "salary": "Salary Range",
  "posted": "Posted Date",
  "tags": ["tag1", "tag2"],
  "description": "Job Description",
  "link": "Job URL",
  "source": "Source Website",
  "scraped_at": "Timestamp"
}
```

### Markdown Summary (`jobs_summary_YYYYMMDD_HHMMSS.md`)
A human-readable summary including:
- Total job count
- Jobs by source
- Detailed job listings with descriptions
- Direct links to job postings

## Discord Integration 💬

When configured with a webhook URL, the script sends:
- Total job count
- Breakdown by source
- Top 5 jobs from each source
- Links to full job postings
- Timestamp of the update

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to [cryptojobslist.com](https://cryptojobslist.com/) and [web3.career](https://web3.career/) for providing job listings
- Built with Python and various open-source libraries

## Support 💪

If you encounter any issues or have suggestions, please open an issue in the GitHub repository. 