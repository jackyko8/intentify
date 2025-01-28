# This file contains the code to preprocess the sentences before clustering.

import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Pre-requisite: Run these in a Python shell once before running any code that uses the NLTK library
# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt_tab')

def preprocess_sentences(sentences):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    preprocessed = []
    for sentence in sentences:
        sentence = re.sub(r'[^\w\s]', '', sentence.lower())  # Remove punctuation
        tokens = sentence.split()
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        preprocessed.append(" ".join(tokens))
    return preprocessed
