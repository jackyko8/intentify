# This file contains the code to classify sentences into intents.

from get_data import get_sentences
from preprocess import preprocess_sentences
from embeddings import get_embeddings
from labeling import get_labels
from cluster import cluster_sentences

# from summarize_transformers import get_summary
from summarize_rake import get_summary

granularity = 16
raw_output = True

# Test stubs
show_some = 0

def classify_sentences(sentences, granularity=granularity):
    if not sentences:
        return {}

    # Preprocess sentences
    preprocessed = preprocess_sentences(sentences)
    # Test stub
    if show_some:
        print(f"\nPreprocessed: {len(preprocessed)} sentences; showing {show_some}")
        for ii in range(show_some):
            print(preprocessed[ii])

    # Get embeddings
    embeddings = get_embeddings(preprocessed)
    # Test stub
    if show_some:
        print(f"\nEmbeddings: {len(embeddings)}; showing {show_some}")
        for ii in range(show_some):
            print(embeddings[ii])

    # # Perform clustering
    cluster_labels = cluster_sentences(embeddings, granularity)
    # Test stub
    if show_some:
        print(f"\nCluster labels: {len(cluster_labels)}; showing {show_some}")
        for ii in range(show_some):
            print(cluster_labels[ii])

    # Get representative sentences
    representatives = get_labels(sentences, embeddings, cluster_labels)
    # Test stub
    if show_some:
        print(f"\nRepresentatives: {len(representatives)}; showing {show_some}")
        for ii in range(show_some):
            print(representatives[ii])

    # Group sentences by cluster
    clusters = {label: [] for label in set(cluster_labels)}
    for i, label in enumerate(cluster_labels):
        # print(f"i: {i}; label: {label}; sentence: {sentences[i].strip()}")
        clusters[label].append(sentences[i])
    # Test stub
    if show_some:
        print(f"\nClusters: {len(clusters)}; showing {show_some}")
        for ii in range(show_some):
            print(clusters[ii])

    # Test stub
    if show_some:
        return [], []

    # return clusters, representatives
    intents = {}
    for label, group in clusters.items():
        representative_sentence = representatives.get(label, "No representative sentence")
        summary = get_summary(representative_sentence)
        intents[summary] = group

    return intents


if __name__ == "__main__":
    sentences, lines = get_sentences()
    # sentences = [sentence.strip() for sentence in get_sentences()]
    # print(f"Sentences: {len(sentences)}")
    # for sentence in sentences:
    #     print(sentence)

    # clusters, representatives = classify_sentences(sentences)
    # if not clusters or not representatives:
    intents = classify_sentences(sentences)
    if not intents:
        print("No intents found.")
        exit()


    # print(f"\nClusters:")
    # for label, group in clusters.items():
    #     print(f"Cluster {label} ({len(group)}): {group}")

    # print("\nRepresentative Sentences:")
    # for label, sentence in representatives.items():
    #     print(f"Cluster {label}: {sentence}")

    # print("\nClusters with Representative Sentences:")
    # for label, group in clusters.items():
    #     representative_sentence = representatives.get(label, "No representative sentence")
    #     print(f"- Cluster {label} ({len(group)} sentences):")
    #     print(f"  - Representative Sentence: {representative_sentence}")
    #     print(f"  - Sentences:")
    #     for sentence in group:
    #         print(f"    - {sentence}")
    #     print()

    # intents = {}
    # for label, group in clusters.items():
    #     representative_sentence = representatives.get(label, "No representative sentence")
    #     summary = get_summary(representative_sentence)
    #     intents[summary] = group

    if raw_output:
        print({
            "metadata": {
                "granularity": granularity,
                "lines": len(lines),
                "sentences": len(sentences),
                "intents": len(intents),
            },
            "intents": intents,
        })
    else:
        print(f"\nFound {len(intents)} intents from {len(lines)} input lines, containing {len(sentences)} unique sentences, using a granularity of {granularity}.")
        print(f"\nIntents ({len(intents)}):\n")
        for intent in intents:
            print(intent)

        print(f"\nClusters with sentences:\n")
        for intent in intents:
            print(f"- {intent}")
            for sentence in intents[intent]:
                print(f"  - {sentence}")
            print()
