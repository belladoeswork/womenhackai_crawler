import requests
from bs4 import BeautifulSoup
import spacy
import json
from datetime import datetime

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.jobs = []
        self.nlp = spacy.load("en_core_web_sm")

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.content, 'html.parser')

    def extract_text(self, element):
        return element.get_text(strip=True) if element else ''

    def normalize_text(self, text):
        doc = self.nlp(text.lower())
        return ' '.join([token.lemma_ for token in doc if not token.is_stop and token.is_alpha])

    def search_jobs(self, query):
        query_doc = self.nlp(query.lower())
        results = []
        for job in self.jobs:
            job_doc = self.nlp(job['description'].lower())
            similarity = query_doc.similarity(job_doc)
            if similarity > 0.5:  # Adjust this threshold as needed
                results.append((job, similarity))
        return sorted(results, key=lambda x: x[1], reverse=True)

    def save_jobs(self):
        with open(f'{self.__class__.__name__}_jobs.json', 'w') as f:
            json.dump(self.jobs, f, indent=2)

    def scrape_jobs(self):
        raise NotImplementedError("This method should be implemented by subclasses")