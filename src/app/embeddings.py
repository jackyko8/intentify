# This file contains the code to convert sentences to embeddings using Sentence-BERT.

from sentence_transformers import SentenceTransformer

# Load a pre-trained Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert sentences to embeddings
def get_embeddings(sentences):
    return model.encode(sentences)
