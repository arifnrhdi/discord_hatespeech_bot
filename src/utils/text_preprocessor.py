import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def normalize_alay(text: str, alay_dictionary: dict):
    if not alay_dictionary:
        return text
    words = text.split()
    normalized_words = [alay_dictionary.get(word, word) for word in words]
    return " ".join(normalized_words)

def preprocess_text(text: str, alay_dict: dict = None, custom_stopwords: set = None, perform_stemming: bool = True):
    if not isinstance(text, str):
        return ""
    text = str(text).lower()

    if alay_dict:
        text = normalize_alay(text, alay_dict)

    text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', ' ', text)
    text = re.sub(r'@[^\s]+', ' ', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    text = re.sub(r'\brt\b', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(user|pengguna|url)\b', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\b(?:[a-z])\b', '', text)
    text = re.sub(r'\b(?:x|f|xf|fx|ff|xx)+\b', '', text)

    if custom_stopwords:
        words = text.split()
        filtered_words = [word for word in words if word not in custom_stopwords]
        text = " ".join(filtered_words)
    
    if perform_stemming and stemmer:
        text = stemmer.stem(text)

    text = re.sub(r'\s+', ' ', text).strip()
    return text