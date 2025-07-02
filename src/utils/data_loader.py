import pandas as pd

def load_main_dataset(file_path: str):
    df = pd.read_csv(file_path, encoding='latin-1')
    return df

def load_alay_dictionary(file_path: str):
    df = pd.read_csv(file_path, names=['alay', 'baku'], header=0, encoding='latin-1')
    alay_dict = df.set_index('alay')['baku'].to_dict()
    return alay_dict

def load_abusive_words(file_path: str):
    df = pd.read_csv(file_path, header=None)
    abusive_set = set(df[0].str.strip().str.lower())
    return abusive_set

def load_stopwords(file_path: str):
    df = pd.read_csv(file_path, header=None, names=['stopword'])
    stopwords = set(df['stopword'].str.strip().str.lower())
    return stopwords