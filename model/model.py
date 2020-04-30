import logging
from pathlib import Path

import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from data import generate_dataset
from tooling import (
    model_attributes,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_path = Path(__file__).resolve().parent
dataset = generate_dataset(model_path / 'data' / 'dataset.csv')
dataset = dataset.sort_values(by=['Class'])

tokenizer = Tokenizer(
    num_words=model_attributes.vocab_size,
    filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~',
    lower=True,
)
tokenizer.fit_on_texts(dataset['Question'].values)
labels = dataset['Class'].unique()

X = tokenizer.texts_to_sequences(dataset['Question'].values)
X = pad_sequences(X, maxlen=model_attributes.max_length)
Y = pd.get_dummies(dataset['Class']).values

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.10,
    random_state=42,
)

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(
        model_attributes.vocab_size,
        model_attributes.embedding_dim,
        input_length=X.shape[1]
    ),
    tf.keras.layers.SpatialDropout1D(0.2),
    tf.keras.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2),
    tf.keras.layers.Dense(len(labels), activation='softmax'),
])
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'],
)

epochs = 6
batch_size = 64

history = model.fit(
    X_train,
    Y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_split=0.1,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,
            min_delta=0.0001,
        )
    ]
)


def predict(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=model_attributes.max_length)
    return labels[np.argmax(model.predict(padded))]
