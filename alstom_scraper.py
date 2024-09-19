from base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import json

class AlstomScraper(BaseScraper):
    def __init__(self):
        super().__init__('https://jobsearch.alstom.com/search/')
        self.keywords = ['rail', 'signal', 'engineer', 'ETCS', 'ERTMS', 'CBTC']  

    def scrape_jobs(self):
        for page in range(1, 6):  
            url = f"{self.base_url}?startrow={25 * (page - 1)}"
            soup = self.get_soup(url)
            job_listings = soup.find_all('tr', class_='data-row')
            
            if not job_listings:
                break  

            for job in job_listings:
                title_elem = job.find('a', class_='jobTitle-link')
                title = self.extract_text(title_elem)
                job_url = 'https://jobsearch.alstom.com' + title_elem['href']
                location = self.extract_text(job.find('span', class_='jobLocation'))
                function = self.extract_text(job.find('span', class_='jobDepartment'))
                experience = self.extract_text(job.find('span', class_='jobShift'))
                date = self.extract_text(job.find('span', class_='jobDate'))

                #  job description
                job_soup = self.get_soup(job_url)
                description = self.extract_text(job_soup.find('div', class_='job'))

                # job contains any of the keywords?
                if any(keyword.lower() in description.lower() for keyword in self.keywords):
                    self.jobs.append({
                        'company': 'Alstom',
                        'title': title,
                        'location': location,
                        'function': function,
                        'experience': experience,
                        'description': self.normalize_text(description),
                        'url': job_url,
                        'date_posted': date,
                        'date_scraped': datetime.now().isoformat()
                    })

            print(f"Scraped page {page}")
            time.sleep(2)  

        if self.jobs:
            self.save_jobs()
            print(f"Scraped {len(self.jobs)} jobs from Alstom")
        else:
            print("No jobs matching the keywords were found")

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def save_jobs(self):
        filename = f'alstom_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=4)
        print(f"Saved {len(self.jobs)} jobs to {filename}")