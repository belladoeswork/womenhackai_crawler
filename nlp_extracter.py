
# import json
# import spacy
# from collections import Counter
# import pandas as pd
# import matplotlib.pyplot as plt
# from langdetect import detect
# import os

# # Language models
# nlp_models = {
#     'en': spacy.load("en_core_web_sm"),
#     'fr': spacy.load("fr_core_news_sm"),
#     'de': spacy.load("de_core_news_sm"),
#     'it': spacy.load("it_core_news_sm"),
#     'es': spacy.load("es_core_news_sm")
# }

# def load_data(json_file_path):
#     with open(json_file_path, 'r', encoding='utf-8') as file:
#         return json.load(file)
    
# def detect_language(text):
#     try:
#         return detect(text)
#     except:
#         return 'en'

# def process_text(text):
#     lang = detect_language(text)
#     nlp = nlp_models.get(lang, nlp_models['en'])  # Default to English
#     doc = nlp(text)
#     return [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha and len(token) > 1]

# def extract_keywords(data, n=20):
#     all_words = []
#     for job in data:
#         all_words.extend(process_text(job['description']))
    
#     word_freq = Counter(all_words)
#     return word_freq.most_common(n)

# def visualize_keywords(keywords, output_dir):
#     df = pd.DataFrame(keywords, columns=['Word', 'Frequency'])
#     plt.figure(figsize=(12, 6))
#     plt.bar(df['Word'], df['Frequency'])
#     plt.title('Top Keywords in Job Descriptions')
#     plt.xlabel('Words')
#     plt.ylabel('Frequency')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, 'keyword_frequency.png'))
#     plt.close()

# def main(json_file_path, output_dir):
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Load data
#     data = load_data(json_file_path)
    
#     # Extract keywords
#     keywords = extract_keywords(data)
    
#     # Print top keywords
#     print("Top 20 keywords:")
#     for word, freq in keywords:
#         print(f"{word}: {freq}")
    
#     # to file
#     with open(os.path.join(output_dir, 'top_keywords.txt'), 'w', encoding='utf-8') as f:
#         f.write("Top 20 keywords:\n")
#         for word, freq in keywords:
#             f.write(f"{word}: {freq}\n")
    
#     # Viz
#     visualize_keywords(keywords, output_dir)
    
#     # Additional NLP tasks
#     with open(os.path.join(output_dir, 'named_entities.txt'), 'w', encoding='utf-8') as f:
#         for job in data:  
#             lang = detect_language(job['description'])
#             nlp = nlp_models.get(lang, nlp_models['en'])
#             doc = nlp(job['description'])
#             f.write(f"\nJob Title: {job['title']}\n")
#             f.write("Named Entities:\n")
#             for ent in doc.ents:
#                 f.write(f"- {ent.text} ({ent.label_})\n")

#     print(f"Analysis complete. Results saved in {output_dir}")

# if __name__ == "__main__":
#     json_file = 'alstom_jobs_20240919_170036.json'
#     output_dir = 'nlp_results'
#     main(json_file, output_dir)


import json
import spacy
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from langdetect import detect
import os

# Language models
nlp_models = {
    'en': spacy.load("en_core_web_sm"),
    'fr': spacy.load("fr_core_news_sm"),
    'de': spacy.load("de_core_news_sm"),
    'it': spacy.load("it_core_news_sm"),
    'es': spacy.load("es_core_news_sm")
}

# to exclude 
common_words = set(['de', 'et', 'la', 'les', 'à', 'en', 'le', 'und', 'der', 'die', 'das', 'il', 'e', 'a', 'i', 'o', 'y', 'el', 'los', 'las', 'un', 'una', 'the', 'and', 'of', 'to', 'in', 'for', 'with', 'on', 'at', 'from', 'by', 'day','work', 'team'])

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
    nlp = nlp_models.get(lang, nlp_models['en'])  # tokenization, then to English
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha and len(token) > 2 and token.lemma_.lower() not in common_words]

def extract_keywords(data, n=20):
    all_words = []
    for job in data:
        all_words.extend(process_text(job['description']))
    
    word_freq = Counter(all_words)
    return word_freq.most_common(n)

def visualize_keywords(keywords, output_dir):
    df = pd.DataFrame(keywords, columns=['Word', 'Frequency'])
    plt.figure(figsize=(12, 6))
    plt.bar(df['Word'], df['Frequency'])
    plt.title('Top Keywords in Job Descriptions')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'keyword_frequency.png'))
    plt.savefig(output_dir)
    print(f"Saved plot to {output_dir}")
    plt.close()

def main(json_file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    data = load_data(json_file_path)
    
    # Extract keywords
    keywords = extract_keywords(data)
    
    # Print top keywords
    print("Top 20 keywords:")
    for word, freq in keywords:
        print(f"{word}: {freq}")
    
    # Save keywords to file
    with open(os.path.join(output_dir, 'top_keywords.txt'), 'w', encoding='utf-8') as f:
        f.write("Top 20 keywords:\n")
        for word, freq in keywords:
            f.write(f"{word}: {freq}\n")
    
    # Visualize keywords
    visualize_keywords(keywords, output_dir)
    
    # ent recogn
    with open(os.path.join(output_dir, 'named_entities.txt'), 'w', encoding='utf-8') as f:
        for job in data:  
            lang = detect_language(job['description'])
            nlp = nlp_models.get(lang, nlp_models['en'])
            doc = nlp(job['description'])
            f.write(f"\nJob Title: {job['title']}\n")
            f.write("Named Entities:\n")
            for ent in doc.ents:
                f.write(f"- {ent.text} ({ent.label_})\n")

    print(f"Analysis complete. Results saved in {output_dir}")

if __name__ == "__main__":
    json_file = 'alstom_jobs_20240919_170036.json'
    output_dir = 'nlp_results'
    main(json_file, output_dir)