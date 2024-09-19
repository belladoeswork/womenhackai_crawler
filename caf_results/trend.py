import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import seaborn as sns
from wordcloud import WordCloud
import json

class JobPostingAnalyzer:
    def __init__(self, excel_file_path):
        self.data = self.load_data(excel_file_path)

    def load_data(self, excel_file_path):
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        df['extraction_date'] = pd.to_datetime(df['extraction_date'], infer_datetime_format=True, errors='coerce')
        return df

    def location_analysis(self):
        loc_counts = self.data['location'].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        loc_counts.plot(kind='bar')
        plt.title('Top 10 Job Locations')
        plt.xlabel('Location')
        plt.ylabel('Number of Job Postings')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('top_locations.png')
        plt.close()
        return loc_counts.to_dict()

    def time_series_analysis(self):
        daily_counts = self.data['extraction_date'].value_counts().sort_index()
        plt.figure(figsize=(12, 6))
        daily_counts.plot(kind='line')
        plt.title('Job Postings Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Job Postings')
        plt.tight_layout()
        plt.savefig('job_postings_timeline.png')
        plt.close()
        return daily_counts.to_dict()

    def keyword_analysis(self):
        all_titles = ' '.join(self.data['title'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Common Words in Job Titles')
        plt.tight_layout()
        plt.savefig('job_titles_wordcloud.png')
        plt.close()
        
        word_freq = Counter(all_titles.split())
        return dict(word_freq.most_common(20))

    def generate_report(self):
        report = {
            "Top Job Locations": self.location_analysis(),
            "Job Postings Timeline": self.time_series_analysis(),
            "Common Job Title Keywords": self.keyword_analysis()
        }
        return report

def main():
    analyzer = JobPostingAnalyzer('CAF_Job_Table.xlsx')
    report = analyzer.generate_report()

    # Convert Timestamps to strings before dumping to JSON
    report = {k: {str(kk): vv for kk, vv in v.items()} if isinstance(v, dict) else v for k, v in report.items()}

    with open('job_market_insights_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    print("Analysis complete. Results saved in job_market_insights_report.json")
    print("Visualizations saved as PNG files in the current directory.")

if __name__ == "__main__":
    main()