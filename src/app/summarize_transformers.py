from transformers import pipeline

# Load a summarization pipeline
model = "t5-small"
summarizer = pipeline("summarization", model=model)

def get_summary(sentence):
    # Generate title phrase
    title = summarizer(sentence, max_length=10, min_length=5, do_sample=False)
    return title[0]['summary_text']
