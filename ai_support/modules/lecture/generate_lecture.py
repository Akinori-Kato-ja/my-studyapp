from langchain.chains.conversation.base import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from ai_support.ai_chain import get_llm
from ai_support.modules.lecture.lecture_memory import get_summary_memory
from lecture.models import LectureSession, LectureLog


def generate_lecture(session: LectureSession, user_input: str=None) -> str:
    llm = get_llm()
    memory = get_summary_memory(session.summary)
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)
    system_input = None

    if not user_input:
        system_input = (
            'You are a good teacher, so please give your lecture based on the title.\n'
            f'Title: {session.sub_topic.sub_topic}\n'
            'The output must follow the rules below.\n'
            '1.First, list the lecture topics.\n'
            '2.Insert line breaks where necessary to make it easier to read.\n'
            '3.If you include examples such as programming code, they must be separated from the text.\n'
            '4.Please output in the language that the user uses.\n'
        )

        # generate
        response = chain.invoke({'input': system_input})
    else:
        # generate
        response = chain.invoke({'input': user_input})

    print(f'response: {response}')
    print(f'response[response]: {response["response"]}')

    # Save the summary to the database
    session.summary = memory.buffer
    session.save()

    # Record logs in the database
    message = system_input or user_input
    role = 'master' if system_input else 'user'
    LectureLog.objects.create(
        session=session,
        role=role,
        message=message,
    )
    LectureLog.objects.create(
        session=session,
        role='ai',
        message=response['response']
    )

    return response['response']
