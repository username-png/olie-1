from tensorflow.keras.preprocessing.sequence import pad_sequences

from .model import (
    model_attributes,
    model,
    tokenizer,
    tags,
)


def predict(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=model_attributes.max_length)
    pred = model.predict(padded)
    tag_indexes = [
        i for i, accuracy in enumerate(pred[0])
        if accuracy > 0.2
    ]
    return sorted(zip(
        [tags[i] for i in tag_indexes],
        [pred[0][i] for i in tag_indexes],
    ), key=lambda v: v[1], reverse=True)
