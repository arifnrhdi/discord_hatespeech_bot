import pandas as pd
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from bot.config import CLEANED_DATASET_PATH, VECTORIZER_PATH, MODEL_PATH, SAVED_MODELS_DIR

def train_and_evaluate():
    os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

    df = pd.read_csv(CLEANED_DATASET_PATH)

    df.dropna(subset=['Tweet_bersih'], inplace=True)
    df['HS'] = pd.to_numeric(df['HS'], errors='coerce').fillna(0).astype(int)
    df['Abusive'] = pd.to_numeric(df['Abusive'], errors='coerce').fillna(0).astype(int)
    
    df['is_hate_speech'] = ((df['HS'] == 1) | (df['Abusive'] == 1)).astype(int)

    X = df['Tweet_bersih']
    y = df['is_hate_speech']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    vectorizer = TfidfVectorizer(max_features=5000, min_df=2, ngram_range=(1,1))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_tfidf, y_train)
    joblib.dump(model, MODEL_PATH)

    y_pred = model.predict(X_test_tfidf)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

    print(f"Akurasi Keseluruhan: {accuracy:.4f}")
    print(f"Presisi (kelas hate speech): {precision:.4f}")
    print(f"Recall (kelas hate speech): {recall:.4f}")
    print(f"F1-Score (kelas hate speech): {f1:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Bukan Hate Speech', 'Hate Speech'], zero_division=0))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"[[TN FP]\n [FN TP]] = [[{cm[0][0]} {cm[0][1]}]\n [{cm[1][0]} {cm[1][1]}]]")

if __name__ == '__main__':
    train_and_evaluate()