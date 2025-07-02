import joblib
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from utils.data_loader import load_alay_dictionary, load_stopwords
from utils.text_preprocessor import preprocess_text
from bot.config import MODEL_PATH, VECTORIZER_PATH, ALAY_DICT_PATH, STOPWORD_PATH

class HateSpeechPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.alay_dict = None
        self.stopwords = None
        self.is_ready = False
        self._hate_speech_class_index = None

        try:
            self.alay_dict = load_alay_dictionary(ALAY_DICT_PATH)
            self.stopwords = load_stopwords(STOPWORD_PATH)

            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            
            self._hate_speech_class_index = list(self.model.classes_).index(1)
            self.is_ready = True
        except Exception as e:
            print(f"Error saat inisialisasi Predictor: {e}")

    def predict(self, text: str):
        if not self.is_ready:
            return 0, 0.0

        cleaned_text = preprocess_text(
            text, 
            alay_dict=self.alay_dict, 
            custom_stopwords=self.stopwords,
            perform_stemming=True
        )

        if not cleaned_text.strip():
            return 0, 0.0

        text_tfidf = self.vectorizer.transform([cleaned_text])
        prediction = self.model.predict(text_tfidf)
        prediction_proba = self.model.predict_proba(text_tfidf)

        hate_speech_probability = prediction_proba[0][self._hate_speech_class_index]
        
        return prediction[0], hate_speech_probability