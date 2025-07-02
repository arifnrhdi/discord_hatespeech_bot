import os
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Config
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("DISCORD_BOT_PREFIX", "!")
MODERATOR_CHANNEL_ID = int(os.getenv("MODERATOR_CHANNEL_ID")) if os.getenv("MODERATOR_CHANNEL_ID") else None

# Path Direktori
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
SAVED_MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

# Path File
DELETED_MESSAGES_LOG_PATH = os.path.join(LOGS_DIR, 'deleted_messages.log')
DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
CLEANED_DATASET_PATH = os.path.join(DATA_DIR, 'cleaned_dataset.csv')
ALAY_DICT_PATH = os.path.join(DATA_DIR, 'new_kamusalay.csv')
ABUSIVE_WORDS_PATH = os.path.join(DATA_DIR, 'abusive.csv')
STOPWORD_PATH = os.path.join(DATA_DIR, 'stopwordbahasa.csv')

# Path Model
MODEL_PATH = os.path.join(SAVED_MODELS_DIR, 'hate_speech_model.pkl')
VECTORIZER_PATH = os.path.join(SAVED_MODELS_DIR, 'tfidf_vectorizer.pkl')

# Threshold
DETECTION_THRESHOLD = 0.75