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


def predict(model, tokenizer, texts):
    seq = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(seq, maxlen=model_attributes.max_length)
    return model.predict(padded)
