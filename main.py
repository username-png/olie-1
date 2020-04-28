import json
import csv

with open('deduped_questions.json', 'r') as deduped_question_f:
    data = json.load(deduped_question_f)

with open('output.csv', 'w') as output_f:
    writer = csv.writer(output_f)
    for question in data:
        writer.writerow([
            question['id'],
            question['product'],
            question['price'],
            question['question'],
            question['answer'],
        ])
