from rake_nltk import Rake

# Initialize RAKE
rake = Rake()

def get_summary(sentence):
    # Extract keywords
    rake.extract_keywords_from_text(sentence)
    keywords = rake.get_ranked_phrases()
    return " ".join(keywords[:2])  # Combine top keywords
