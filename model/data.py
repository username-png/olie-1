import csv

from nltk.corpus import stopwords


model_labels = set(['cor', 'pagamento', 'contato', 'frete'])
portuguese_stopwords = set(stopwords.words('portuguese'))


def generate_dataset(dataset_path):
    with open(dataset_path, 'r') as dataset_f:
        reader = csv.reader(dataset_f, delimiter=',')
        next(reader)

        for row in reader:
            _, _, _, question, _, label, _ = row
            if not label or label not in model_labels:
                continue

            for word in portuguese_stopwords:
                token = ' ' + word + ' '
                question = question.replace(token, ' ')
                question = question.replace(' ', ' ')

            yield question, label
