# This file contains the code to cluster the embeddings of the sentences using the Agglomerative Clustering algorithm.

from sklearn.cluster import AgglomerativeClustering

def cluster_sentences(embeddings, granularity=16):
    clustering_model = AgglomerativeClustering(
        n_clusters=None,  # Automatically determine the number of clusters
        metric='cosine',
        linkage='average',
        distance_threshold=1 - granularity / 100  # Convert similarity to distance
    )
    cluster_labels = clustering_model.fit_predict(embeddings)
    return cluster_labels
