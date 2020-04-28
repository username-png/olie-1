import functools
import json
import logging
import operator

import requests

from bs4 import BeautifulSoup as BS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

search_url = 'https://celulares.mercadolivre.com.br/iphone/linea-iphone/'

product_title_class = (
    'item-title__primary',
    'ui-pdp-title',
)
product_price_class = (
    'price-tag-fraction',
)
questions_class = 'questions__group'
question_class = 'questions__item--question'
answer_class = 'questions__item--answer'
qa_content_class = 'questions__content'


def generate_pages(search_url):
    since = 0
    while 1:
        yield search_url if since == 0 else f'{search_url}_Desde_{since}'
        since += 50


def fetch_products(search_url):
    response = requests.get(search_url)
    parsed_response = BS(response.text, features='lxml')

    for product in parsed_response.find_all('a', {'class': 'item__info-title'}):
        product_href = product['href']
        logger.info(f'Fetching {product_href}')
        yield BS(requests.get(product['href']).text, features='lxml')


def search_class_variants(container, class_names):
    for class_name in class_names:
        if elements := container.find_all(attrs={'class': class_name}):
            return elements[0]


next_page = next(generate_pages(search_url))
logger.info(f'Starting with {next_page}')
products = fetch_products(next_page)

for product in products:
    title = search_class_variants(product, product_title_class).text
    price = search_class_variants(product, product_price_class).text
    try:
        questions = product.find_all(attrs={'class': questions_class})
    except Exception as exc:
        logging.warning(f'No questions found for {title}')
        continue

    parsed_questions = []
    for question in questions:
        question_container = question.find_all(attrs={'class': question_class})[0]
        question_content = question_container.find_all(attrs={'class': qa_content_class})[0].text
        answer_container = question.find_all(attrs={'class': answer_class})[0]
        answer_content = answer_container.find_all(attrs={'class': qa_content_class})[0].text
        parsed_questions.append((question_content, answer_content))

    try:
        with open('questions.json', 'r') as questions_f:
            stored_questions = json.load(question_f)
    except FileNotFoundError:
        stored_questions = []

    for (question, answer) in parsed_questions:
        stored_questions.append({
            'product': title,
            'price': price,
            'question': question,
            'answer': answer,
        })

    with open('questions.json', 'w') as questions_f:
        json.dump(stored_questions, questions_f)
