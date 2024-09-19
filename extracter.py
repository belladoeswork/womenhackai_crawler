import json
import spacy
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect
import os
from nltk.corpus import stopwords
import nltk

# Download NLTK stop words
try:
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"Error downloading stopwords: {e}")

# Language models
nlp_models = {
    'en': spacy.load("en_core_web_sm"),
    'fr': spacy.load("fr_core_news_sm"),
    'de': spacy.load("de_core_news_sm"),
    'it': spacy.load("it_core_news_sm"),
    'es': spacy.load("es_core_news_sm")
}

# Use NLTK's stop words and extend them
stop_words = {
    'en': set(stopwords.words('english')),
    'fr': set(stopwords.words('french')),
    'de': set(stopwords.words('german')),
    'it': set(stopwords.words('italian')),
    'es': set(stopwords.words('spanish'))
}

# Add custom stop words
for lang in stop_words:
    stop_words[lang].update(['alstom', 'company', 'job', 'work', 'role', 'position', 'candidate'])

# Category words
category_words = {
    'Rail Infrastructure': {
        'ATC': 5, 'Interlocking': 5, 'ERTMS': 5, 'ETCS': 5, 'CBTC': 5,
        'Telecommunications': 4, 'PIS': 4
    },
    'Technology': {
        'etcs': 4, 'on-board': 3, 'ato': 4, 'driverless': 4, 'onboard': 3,
        'auriga': 3, 'quasar': 3, 'e-highway': 3, 'ehighway': 3, 'rfid': 3,
        'lte': 3, 'goa2': 4, 'goa4': 4, 'bim': 3, 'iot': 3, 'automatic train operation': 5,
        'radio-frequency identification': 4, 'long term evolution': 4,
        'grade of automation': 4, 'building information modeling': 4,
        'internet of things': 4
    },
    'Mass Transit': {
        'rail': 3, 'train': 3, 'metro': 4, 'LRT': 4, 'light rail': 4,
        'cybersecurity': 3, '5G': 3, 'resignaling': 4, 'resignalling': 4,
        'digital': 3, 'project': 2, 'award': 2, 'onboard': 3
    },
    'Rolling Stock': {
        'high-speed train': 5, 'EMU': 4, 'DMU': 4, 'electric train': 4,
        'diesel train': 4, 'passenger coach': 3, 'LRV': 4, 'tram': 4,
        'monorail': 4, 'locomotive': 4, 'high-speed rail': 5, 'inter-city train': 4,
        'battery-operated train': 4, 'hybrid train': 4, 'electric vehicle': 3,
        'diesel vehicle': 3, 'passenger vehicle': 3, 'public transport': 3,
        'streetcar': 3, 'low-floor': 2, 'high-floor': 2, 'mass transit': 4,
        'rapid transit': 4, 'skytrain': 3, 'automated guideway transit': 4
    },
    'Business': {
        'innovation': 3, 'award': 2, 'contract': 3, 'strategy': 3,
        'strategic': 3, 'order': 3, 'funding': 3, 'acquire': 3,
        'acquisition': 3, 'agreement': 3
    }
}

def load_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'en'

def process_text(text):
    lang = detect_language(text)
    nlp = nlp_models.get(lang, nlp_models['en'])
    doc = nlp(text)
    
    lang_stop_words = stop_words.get(lang, stop_words['en'])
    
    return [token.lemma_.lower() for token in doc 
            if not token.is_stop 
            and not token.is_punct 
            and token.is_alpha 
            and len(token) > 2 
            and token.lemma_.lower() not in lang_stop_words]

def score_word(word):
    score = 0
    for category, words in category_words.items():
        if word in words:
            score += words[word]
        else:
            # Check for multi-word matches
            for key, value in words.items():
                if ' ' in key and word in key.split():
                    score += value / len(key.split()) 
    return score

def extract_keywords(data, n=20):
    word_scores = Counter()
    for job in data:
        words = process_text(job['description'])
        for word in words:
            word_scores[word] += score_word(word)
    
    return word_scores.most_common(n)

def visualize_keywords(keywords, output_dir):
    df = pd.DataFrame(keywords, columns=['Word', 'Score'])
    plt.figure(figsize=(12, 6))
    plt.bar(df['Word'], df['Score'])
    plt.title('Top Keywords in Job Descriptions')
    plt.xlabel('Words')
    plt.ylabel('Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'keyword_scores.png'))
    plt.close()

def main(json_file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    data = load_data(json_file_path)
    keywords = extract_keywords(data)
    
    print("Top 20 keywords:")
    for word, score in keywords:
        print(f"{word}: {score}")
    
    with open(os.path.join(output_dir, 'top_keywords.txt'), 'w', encoding='utf-8') as f:
        f.write("Top 20 keywords:\n")
        for word, score in keywords:
            f.write(f"{word}: {score}\n")
    
    visualize_keywords(keywords, output_dir)
    
    print(f"Analysis complete. Results saved in {output_dir}")

if __name__ == "__main__":
    json_file = 'alstom_jobs_20240919_170036.json'
    output_dir = 'nlp_results'
    main(json_file, output_dir)