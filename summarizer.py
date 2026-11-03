import re
from collections import Counter


def summarize_text(text, sentence_count=5):

    # Remove unnecessary spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Divide text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Remove very short sentences
    sentences = [
        sentence for sentence in sentences
        if len(sentence.split()) > 4
    ]

    if not sentences:
        return "Not enough readable content to summarize."

    # Common words that should not affect importance
    stop_words = {
        "the", "is", "are", "was", "were", "a", "an",
        "and", "or", "but", "in", "on", "at", "to",
        "of", "for", "with", "by", "from", "as",
        "it", "this", "that", "these", "those",
        "be", "been", "being", "has", "have", "had"
    }

    # Calculate word frequency
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    word_frequency = Counter(filtered_words)

    # Calculate sentence importance
    sentence_scores = {}

    for sentence in sentences:

        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b',
            sentence.lower()
        )

        score = sum(
            word_frequency[word]
            for word in sentence_words
            if word not in stop_words
        )

        sentence_scores[sentence] = (
            score / max(len(sentence_words), 1)
        )

    # Select important sentences
    important_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:sentence_count]

    # Maintain original sentence order
    summary = [
        sentence for sentence in sentences
        if sentence in important_sentences
    ]

    return " ".join(summary)
