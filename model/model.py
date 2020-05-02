import csv
import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.text import (
    tokenizer_from_json,
    Tokenizer,
)
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

from app.questions.models import Question

from .data import generate_dataset


@dataclass
class ModelAttributes:
    vocab_size: int = 50000
    embedding_dim: int = 100
    max_length: int = 250
    trunc_type: str = 'post'
    padding_type: str = 'post'
    oov_tok: str = '<OOV>'
    training_portion: float = .8
    filters: str = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'


model_attributes = ModelAttributes()


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
        filters=model_attributes.filters,
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
        tokenizer = tokenizer_from_json(json.load(tokenizer_cache_f))

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
        json.dump(list(tags), tags_cache_f)


def load_model(force_retrain=False):
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
        and not force_retrain
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
    fit_model(model, X_train, Y_train)

    serialize_model(
        model,
        tokenizer,
        tags,
        model_cache,
        model_weights,
        tokenizer_cache,
        tags_cache,
    )
    return model, tokenizer, tags


model, tokenizer, tags = load_model()
