# This file contains the code to select representative sentences from each cluster.

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

def get_labels(sentences, embeddings, cluster_labels):
    representative_sentences = {}
    for cluster_id in set(cluster_labels):
        cluster_indices = np.where(cluster_labels == cluster_id)[0]
        cluster_embeddings = embeddings[cluster_indices]
        centroid = cluster_embeddings.mean(axis=0)
        closest_idx = np.argmax(cosine_similarity([centroid], cluster_embeddings))
        representative_sentences[cluster_id] = sentences[cluster_indices[closest_idx]].strip()
    return representative_sentences
