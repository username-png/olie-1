import json
import logging


def clean_text(text):
    text = text.strip()
    text = text.replace('\n', '')
    text = text.replace('Denunciar', '')
    return text

with open('assets/questions.json', 'r') as questions_f:
    data = json.load(questions_f)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

questions_set = set()
deduped_questions = []

logging.info(f'Processing {len(data)}')

global_id = 1
for question in data:
    question_text = clean_text(question['question'])
    answer_text = clean_text(question['answer'])
    product = clean_text(question['product'])
    price = clean_text(question['price'])

    if question_text in questions_set:
        continue

    questions_set.add(question_text)
    question['id'] = global_id
    question['question'] = question_text
    question['answer'] = answer_text
    question['product'] = product
    question['price'] = price
    deduped_questions.append(question)
    global_id += 1

logging.info(f'Finished deduping {len(deduped_questions)}')

with open('assets/deduped_questions.json', 'w') as deduped_questions_f:
    json.dump(deduped_questions, deduped_questions_f)
