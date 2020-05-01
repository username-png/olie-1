import csv
import json
from pathlib import Path

import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from .data import generate_dataset
from .tooling import (
    model_attributes,
)

from app.questions.models import Question


def generate_csv():
    dataset_path = 'model/data/dataset.csv'
    with open(dataset_path, 'w') as dataset_f:
        writer = csv.writer(dataset_f)
        writer.writerow(['Question', 'Tag'])
        for question in Question.objects.select_related('tag').iterator():
            if question.tag is not None:
                writer.writerow([question.text, question.tag.slug])
    return dataset_path


def get_train_data():
    dataset_path = generate_csv()

    dataset = generate_dataset(dataset_path)
    dataset = dataset.sort_values(by=['Tag'])

    tokenizer = Tokenizer(
        num_words=model_attributes.vocab_size,
        filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~',
        lower=True,
    )
    tokenizer.fit_on_texts(dataset['Question'].values)
    tags = dataset['Tag'].unique()

    X = tokenizer.texts_to_sequences(dataset['Question'].values)
    X = pad_sequences(X, maxlen=model_attributes.max_length)
    Y = pd.get_dummies(dataset['Tag']).values

    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.10,
        random_state=42,
    )
    return X, Y, X_train, X_test, Y_train, Y_test, tokenizer, tags


def fit_model(model, X_train, Y_train):
    epochs = 10
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
    return history


def get_model_structure(X, tags):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Embedding(
            model_attributes.vocab_size,
            model_attributes.embedding_dim,
            input_length=X.shape[1]
        ),
        tf.keras.layers.SpatialDropout1D(0.2),
        tf.keras.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2),
        tf.keras.layers.Dense(len(tags), activation='softmax'),
    ])
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy'],
    )
    return model


def load_from_cache(model_cache, model_weights, tokenizer_cache, tags_cache):
    with open(model_cache, 'r') as model_f:
        model = model_from_json(json.load(model_f))
    model.load_weights(str(model_weights))

    with open(tokenizer_cache, 'r') as tokenizer_cache_f:
        tokenizer = json.load(tokenizer_cache_f)

    with open(tags_cache, 'r') as tags_cache_f:
        tags = json.load(tags_cache_f)

    return model, tokenizer, tags


def serialize_model(
    model, tokenizer, tags, model_cache, model_weights,
    tokenizer_cache, tags_cache
):
    with open(model_cache, 'w') as model_cache_f:
        json.dump(model.to_json(), model_cache_f)
    model.save_weights(str(model_weights))

    with open(tokenizer_cache, 'w') as tokenizer_cache_f:
        json.dump(tokenizer.to_json(), tokenizer_cache_f)

    with open(tags_cache, 'w') as tags_cache_f:
        json.dump(tags, tags_cache_f)


def load_model():
    model_cache_path = Path('model/data')
    model_cache = model_cache_path / 'model.json' 
    model_weights = model_cache_path / 'model.h5' 
    tokenizer_cache = model_cache_path / 'tokenizer.json'
    tags_cache = model_cache_path / 'tags.json'

    if (
        model_cache.is_file()
        and model_weights.is_file()
        and tokenizer_cache.is_file()
        and tags_cache.is_file()
    ):
        return load_from_cache(
            model_cache,
            model_weights,
            tokenizer_cache,
            tags_cache)

    (
        X,
        Y,
        X_train,
        X_test,
        Y_train,
        Y_test,
        tokenizer,
        tags,
    ) = get_train_data()
    model = get_model_structure(X, tags)
    history = fit_model(model, X_train, Y_train)
    serialize_model(model, tokenizer, tags, model_cache, model_weights)
    return model, tokenizer, tags
