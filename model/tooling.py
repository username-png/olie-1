from dataclasses import dataclass

from tensorflow.keras.preprocessing.sequence import pad_sequences


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


def predict(model, tokenizer, tags, text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=model_attributes.max_length)
    pred = model.predict(padded)
    tag_indexes = [
        i for i, accuracy in enumerate(pred[0])
        if accuracy > 0.2
    ]
    return (
        [tags[i] for i in tag_indexes],
        tags,
        [pred[0][i] for i in tag_indexes],
    )
