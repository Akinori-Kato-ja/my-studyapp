import os
import json

from openai import OpenAI


def generate_learning_topic(title, current_level='', target_level=''):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = (
        'Please generates a training task based on the following <User Input> and <Creation Rules>.'
        '<User Input>'
        f'Title:{title}'
        f'Current level:{current_level}'
        f'Target level:{target_level}'
        '<Creation Rurles>'
        '1.As shown in the <Example Output>, please divide the tasks into main topics and subtopics. Please generate the data in JSON format.'
        '2.Please break each subtopic down as much as possible. The recommended study time for each subtopic is about 30 minutes to an hour.'
        '3.<User Input> requires only a title, other inputs are optional.'
        'If there are optional inputs, the most optimal task must be generated taking all inputs into account.'
        'If no optional fields are entered, generate the most orthodox task that matches the title.'
        "4.Please generate tasks in the same language as the user's input."
        '<Example Output>'
        """
[
    {{
        "main_topic": "Python basic grammar",
        "sub_topics": [
            {{
                "sub_topic": "Variable"
            }},
            {{
                "sub_topic": "Data Types"
            }},
            ....
        ]
    }},
    ....
    {{
        "main_topic": "Data Science",
        "sub_topics": [
            {{
                "sub_topic": "Library"
            }},
            ....
        ]
    }},
]
"""
    )

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are an AI assistant that generates optimal study plans based on the learning goals set by the user.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=2000,
        temperature=0.7
    )
    print(response)


title = 'Python株価予測'
current_level = 'Python基礎構文は習得済み'
target_level = '株価予測プログラムを作成して、株価取引に使用したい'
generate_learning_topic(title, current_level, target_level)
