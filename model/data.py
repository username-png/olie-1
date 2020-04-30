import csv
import re

import unidecode
import pandas as pd
from nltk.corpus import stopwords

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('portuguese'))

model_labels = set(['cor', 'pagamento', 'contato', 'frete'])

def clean(text):
    text = unidecode.unidecode(text)
    text = text.lower()
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = [
        token
        for token in text.split(' ')
        if token and token not in STOPWORDS
    ]
    return text


def generate_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df.drop(df[~df['Class'].isin(model_labels)].index, inplace=True)
    df['Question'] = df['Question'].apply(clean)
    return df
