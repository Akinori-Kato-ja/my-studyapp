from langchain.chains.conversation.base import ConversationChain
from ai_support.ai_chain import get_llm
from ai_support.modules.exam.exam_memory import get_summary_memory
from exam.models import ExamSession, ExamLog, ExamEvaluation
from .exam_prompts import get_main_mcq_prompt, get_sub_mcq_prompt


def generate_mcq(session: ExamSession) -> tuple[int, str]:
    llm = get_llm()
    memory = get_summary_memory(session.summary)

    # If the Session is a main_topic, all sub_topics that belong to it are obtained and used as the test range.
    if session.main_topic:
        sub_topics = session.main_topic.sub_topics.all()
        exam_topics = ', '.join([sub.sub_topic for sub in sub_topics])
        prompt = get_main_mcq_prompt(exam_topics)
    elif session.sub_topic:
        exam_topic = session.sub_topic
        prompt = get_sub_mcq_prompt(exam_topic)
    else:
        print('Failed to get learning topics.')
        return None

    # Generate
    response = llm.invoke(prompt)

    print(f'response[content]: {response.content}')
    print(f'response[metadata]: {response.response_metadata}')

    # Extract token information
    usage = response.response_metadata.get('token_usage', {})
    total_tokens = usage.get('total_tokens', 0)

    # Save the summary to the database
    session.summary = memory.buffer
    session.save()

    # Record logs in the database
    exam_log = ExamLog.objects.create(
        session=session,
        question=response.content,
        answer='', # Initialization
        token_count=total_tokens,
    )
    session.current_question_number = exam_log.question_number

    return session.current_question_number ,response.content
