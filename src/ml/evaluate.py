import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from bot.config import CLEANED_DATASET_PATH, VECTORIZER_PATH, MODEL_PATH

def evaluate_model():
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    except FileNotFoundError:
        print(f"Model not found")
        return

    df = pd.read_csv(CLEANED_DATASET_PATH)
    if df.empty:
        print("cleaned_dataset gagal dimuat.")
        return

    df.dropna(subset=['Tweet_bersih'], inplace=True)
    df['HS'] = pd.to_numeric(df['HS'], errors='coerce').fillna(0).astype(int)
    df['Abusive'] = pd.to_numeric(df['Abusive'], errors='coerce').fillna(0).astype(int)
    df['is_hate_speech'] = ((df['HS'] == 1) | (df['Abusive'] == 1)).astype(int)

    X = df['Tweet_bersih']
    y = df['is_hate_speech']
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    print(f"Data uji: {len(X_test)} sampel.")

    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)

    print("\n--- Hasil Evaluasi Model pada Data Uji ---")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)

    print(f"Akurasi Keseluruhan: {accuracy:.4f}")
    print(f"Presisi (untuk kelas Hate Speech): {precision:.4f}")
    print(f"Recall (untuk kelas Hate Speech): {recall:.4f}")
    print(f"F1-Score (untuk kelas Hate Speech): {f1:.4f}")
    
    print(classification_report(y_test, y_pred, target_names=['Bukan Hate Speech', 'Hate Speech'], zero_division=0))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"[[TN FP]\n [FN TP]] = [[{cm[0][0]} {cm[0][1]}]\n [{cm[1][0]} {cm[1][1]}]]")

if __name__ == '__main__':
    evaluate_model()