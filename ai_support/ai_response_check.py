import os
import json

from openai import OpenAI


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
message = '人間の欠点は?'

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'system', 'content': 'あなたは全ての生物の頂点です。'},
        {'role': 'user', 'content': '人間のよくない点は？'},
    ],
    max_tokens=200,
    temperature=0.7,
)

print(f'response: {response}')
raw_content = response.choices[0].message.content.strip()
print('*'*20)
print(f'raw_content: {raw_content}')
