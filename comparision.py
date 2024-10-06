from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample dictionary of pre-saved OCR data
pages = {
    1: "This is the text from page one with some content",
    2: "Here is the data from page two, it contains different content",
    3: "Page three text goes here with even more different information"
}

# OCR result from camera (with errors)
ocr_camera_result = "this is page with some content and errors"

# Combine all texts
texts = list(pages.values())
texts.append(ocr_camera_result)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer().fit_transform(texts)
vectors = vectorizer.toarray()

# Cosine similarity between camera result and all pages
cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()

# Find the page with the highest similarity score
most_similar_page = cosine_similarities.argmax() + 1  # +1 for page number
similarity_score = cosine_similarities.max()

# Output result
print(f"The page is most likely: {most_similar_page} with similarity: {similarity_score:.2f}")
