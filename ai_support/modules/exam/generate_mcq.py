from langchain.chains.conversation.base import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from ai_chain import get_llm
from modules.exam.exam_memory import get_summary_memory
from exam.models import ExamSession, ExamLog, ExamEvaluation


def generate_mcq(session: ExamSession):
    llm = get_llm()
    memory = get_summary_memory(session.summary)
    chain = ConversationChain(llm=llm, memory=memory)

    if session.main_topic:
        sub_topics = session.main_topic.sub_topics.all()
        exam_topics = [sub.sub_topic for sub in sub_topics]
        prompt_text = (
            'You are a good teacher, Please create several new multiple-choice questions about the following topics.\n'
            f'topics: {', '.join(exam_topics)}\n'
            'The output must follow the rules below.\n'
            '1.Avoid repeating or overly similar questions.\n'
            '2.Insert line breaks where necessary to make it easier to read.\n'
            '3.If you include examples such as programming code, they must be separated from the text.\n'
            '4.Please output in the language used by the user, such as the language used in the topics.\n'
        )

        response = chain.invoke({'input': prompt_text})


        
    elif session.sub_topic:
        pass


if __name__ == '__main__':
    exam_session = ExamSession.objects.filter(id=1)