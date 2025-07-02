import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from utils.data_loader import load_main_dataset, load_alay_dictionary, load_stopwords
from utils.text_preprocessor import preprocess_text
from bot.config import DATASET_PATH, ALAY_DICT_PATH, STOPWORD_PATH, CLEANED_DATASET_PATH, DATA_DIR

def clean_and_save_dataset():
    df = load_main_dataset(DATASET_PATH)
    alay_dict = load_alay_dictionary(ALAY_DICT_PATH)
    custom_stopwords = load_stopwords(STOPWORD_PATH)

    df['Tweet_bersih'] = df['Tweet'].apply(
        lambda x: preprocess_text(
            text=x,
            alay_dict=alay_dict,
            custom_stopwords=custom_stopwords,
            perform_stemming=True
        )
    )
    
    df = df[['Tweet_bersih', 'HS', 'Abusive']]

    os.makedirs(DATA_DIR, exist_ok=True)
    
    try:
        df.to_csv(CLEANED_DATASET_PATH, index=False, encoding='utf-8')
        print("cleaned dataset success")
    except Exception as e:
        print(f"failed saving cleaned dataset: {e}")

if __name__ == '__main__':
    clean_and_save_dataset()