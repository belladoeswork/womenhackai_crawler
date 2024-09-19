from alstom_scraper import AlstomScraper

def main():
    scraper = AlstomScraper() # this can change based on how many websites you scrape . don't forget to import the class
    scraper.scrape_jobs()

    print(f"Total jobs scraped: {len(scraper.jobs)}")

    query = "rail signaling engineer"
    results = scraper.search_jobs(query)

    print(f"\nTop 5 results for '{query}':")
    for job, similarity in results[:5]:
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"Function: {job['function']}")
        print(f"Experience: {job['experience']}")
        print(f"Date Posted: {job['date_posted']}")
        print(f"URL: {job['url']}")
        print(f"Similarity: {similarity:.2f}\n")

if __name__ == "__main__":
    main()