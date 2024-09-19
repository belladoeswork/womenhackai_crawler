# from stadler_scraper import StadlerScraper
# from thales_scraper import ThalesScraper
# from hitachi_scraper import HitachiScraper
# from alstom_scraper import AlstomScraper

# def main():
#     scrapers = [
#         # StadlerScraper(),
#         # ThalesScraper(),
#         # HitachiScraper(),
#         AlstomScraper()
#     ]

#     all_jobs = []

#     for scraper in scrapers:
#         scraper.scrape_jobs()
#         all_jobs.extend(scraper.jobs)

#     print(f"Total jobs scraped: {len(all_jobs)}")

#     # Example of using the search function
#     query = "rail signaling engineer"
#     results = []
#     for scraper in scrapers:
#         results.extend(scraper.search_jobs(query))

#     results.sort(key=lambda x: x[1], reverse=True)
#     print(f"\nTop 5 results for '{query}':")
#     for job, similarity in results[:5]:
#         print(f"{job['title']} - {job['company']} (Similarity: {similarity:.2f})")

# if __name__ == "__main__":
#     main()
    
    
    
    
from alstom_scraper import AlstomScraper

def main():
    scraper = AlstomScraper()
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