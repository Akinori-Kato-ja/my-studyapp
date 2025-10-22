from langchain.chains.conversation.base import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from ai_support.ai_chain import get_llm
from ai_support.modules.lecture.lecture_memory import get_summary_memory
from lecture.models import LectureSession, LectureLog



def generate_lecture(topic: str, user_input: str=None) -> str:
    llm = get_llm()
    memory = get_summary_memory()
    chain = ConversationChain(llm=llm, memory=memory, verbose=True)

    if not user_input:
        user_input = (
            'You are a good teacher, so please give your lecture based on the title.'
            f'Title: {topic}'
            'The output must follow the rules below.'
            '1.First, list the lecture topics.'
            '2.Insert line breaks where necessary to make it easier to read.'
            '3.If you include examples such as programming code, they must be separated from the text.'
        )

    # generate
    response = chain.invoke({'input': user_input})
    print(response)

    # Save the summary to the database
    # session.summary = memory.buffer
    # session.save()

    # Record logs in the database
    # LectureLog.objects.create(
    #     session=session,
    #     role='user',
    #     message=user_input,
    # )
    # LectureLog.objects.create(
    #     session=session,
    #     role='ai',
    #     message=response
    # )

    return response

topic = 'Pythonのループ処理'
generate_lecture(topic)

