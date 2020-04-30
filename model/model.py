from pathlib import Path

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from data import generate_dataset
from tooling import (
    ModelAttributes,
    predict,
)

model_attributes = ModelAttributes()

model_path = Path(__file__).resolve().parent
dataset = generate_dataset(model_path / 'data' / 'dataset.csv')
questions, labels = zip(*dataset)

train_size = int(len(questions) * model_attributes.training_portion)
train_questions = questions[0: train_size]
train_labels = labels[0: train_size]

validation_questions = questions[train_size:]
validation_labels = labels[train_size:]

tokenizer = Tokenizer(
    num_words=model_attributes.vocab_size, oov_token=model_attributes.oov_tok)
tokenizer.fit_on_texts(train_questions)
word_index = tokenizer.word_index

train_sequences = tokenizer.texts_to_sequences(train_questions)
validation_sequences = tokenizer.texts_to_sequences(validation_questions)

train_padded = pad_sequences(
    train_sequences,
    maxlen=model_attributes.max_length,
    padding=model_attributes.padding_type,
    truncating=model_attributes.trunc_type,
)
validation_padded = pad_sequences(
    validation_sequences,
    maxlen=model_attributes.max_length,
    padding=model_attributes.padding_type,
    truncating=model_attributes.trunc_type,
)

label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(labels)

training_label_seq = np.array(label_tokenizer.texts_to_sequences(train_labels))
validation_label_seq = np.array(label_tokenizer.texts_to_sequences(validation_labels))

model = tf.keras.Sequential([
    # Add an Embedding layer expecting input vocab of size 5000, and output embedding dimension of size 64 we set at the top
    tf.keras.layers.Embedding(model_attributes.vocab_size, model_attributes.embedding_dim),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(model_attributes.embedding_dim)),
    # tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    # use ReLU in place of tanh function since they are very good alternatives of each other.
    tf.keras.layers.Dense(model_attributes.embedding_dim, activation='relu'),
    # Add a Dense layer with 6 units and softmax activation.
    # When we have multiple outputs, softmax convert outputs layers into a probability distribution.
    tf.keras.layers.Dense(6, activation='softmax')
])
model.summary()

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 5 is just fine sounds like
num_epochs = 5
history = model.fit(train_padded, training_label_seq, epochs=num_epochs, validation_data=(validation_padded, validation_label_seq), verbose=2)

"""
from visualization import plot_graphs
plot_graphs(history, 'accuracy')
plot_graphs(history, 'loss')
"""
