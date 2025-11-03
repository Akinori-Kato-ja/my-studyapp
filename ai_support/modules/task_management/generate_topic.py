import json
import os
import re
from openai import OpenAI
from ai_support.ai_client import get_client


client = get_client()


def generate_learning_topic(title, current_level='', target_level=''):
    prompt = (
        'Please generates a training task based on the following <User Input> and <Creation Rules>.\n'
        '<User Input>\n'
        f'Title:{title}\n'
        f'Current level:{current_level}\n'
        f'Target level:{target_level}\n'
        '<Creation Rurles>\n'
        '1. Divide the plan into main topics and sub_topics, as shown in the example.\n'
        '2. Each sub_topic should take ~30-60 minutes of study.\n'
        '3. Current level and target level are optional but should be considered if provided.\n'
        '4. If optional inputs are empty, create the most standard learning path.\n'
        '5. Output must be valid JSON (no extra text).\n'
        '6. Output language should match the input language.\n'
        '<Example Output>\n'
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
