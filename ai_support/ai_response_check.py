import json
import os
import re
from openai import OpenAI


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_learning_topic(title, current_level='', target_level=''):

    prompt = (
        'Please generates a training task based on the following <User Input> and <Creation Rules>.'
        '<User Input>'
        f'Title:{title}'
        f'Current level:{current_level}'
        f'Target level:{target_level}'
        '<Creation Rurles>'
        '1. Divide the plan into main topics and subtopics, as shown in the example.'
        '2. Each subtopic should take ~30–60 minutes of study.'
        '3. Current level and target level are optional but should be considered if provided.'
        '4. If optional inputs are empty, create the most standard learning path.'
        '5. Output must be valid JSON (no extra text).'
        '6. Output language should match the input language.'
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
        max_tokens=1000,
        temperature=0.7
    )

    raw_content = response.choices[0].message.content.strip()
    raw_content = raw_content.replace('```json', '').replace('```', '').strip()

    if not raw_content:
        print('The AI returned an empty response.')
        return []
    
    try:
        generated_learning_topic = json.loads(raw_content)
    except json.JSONDecodeError:
        json_match = re.search(r'\[.*]', raw_content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            generated_learning_topic = json.loads(json_str)
        else:
            print('No JSON data was found.')
            generated_learning_topic = []

    print(f'generated_learning_topic: {generated_learning_topic}')

    return generated_learning_topic



title = 'Python株価予測'
current_level = 'Python基礎構文は習得済み'
target_level = '株価予測プログラムを作成して、株価取引に使用したい'
generate_learning_topic(title, current_level, target_level)