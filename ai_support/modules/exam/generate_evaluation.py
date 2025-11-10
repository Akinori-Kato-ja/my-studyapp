import json
import re
from langchain.chains.conversation.base import ConversationChain
from ai_support.ai_chain import get_llm
from ai_support.modules.exam.exam_memory import get_summary_memory
from exam.models import ExamSession, ExamLog, ExamEvaluation
from .exam_prompts import get_mcq_evaluation_prompt
from exam.models import ExamEvaluation


def generate_mcq_evaluation(log: ExamLog) -> tuple[float, str]:  # {'score': float, 'explanation': str}
    llm = get_llm()
    memory = get_summary_memory(log.session.summary)

    prompt = get_mcq_evaluation_prompt(question=log.question, answer=log.answer)
    # Generate
    response = llm.invoke(prompt)

    print(f'response[content]: {response.content}')
    print(f'response[metadata]: {response.response_metadata}')

    try:
        generated = json.loads(response.content)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*}', response.content)
        if json_match:
            json_str = json_match.group(0)
            generated = json.loads(json_str.replace("'", '"'))
        else:
            print('No JSON data was found.')
            generated = None
            return generated
    
    # Check if a dictionary contains a required key
    required_keys = ['score', 'explanation']
    for key in required_keys:
        if key not in generated:
            raise KeyError(f'The required key({key}) is not included in the output.')
        
    # Check if score is float type
    if not isinstance(generated.get('score'), float):
        try:
            generated['score'] = float(generated['score'])
        except (TypeError, ValueError):
            raise ValueError(f'The score value could not be converted to a float type.: {generated["score"]}')

    print(f'generated: {generated}')

    # Extract token information
    usage = response.response_metadata.get('token_usage', {})
    total_tokens = usage.get('total_tokens', 0)

    # Save the summary to the database
    log.session.summary = memory.buffer
    log.session.save()

    ExamEvaluation.objects.create(
        exam_log=log,
        score=generated['score'],
        feedback=generated['explanation'],
        token_count=total_tokens,
    )

    return generated['score'], generated['explanation']
