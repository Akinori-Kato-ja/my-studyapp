from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


def custom_prompt():
    prompt_text = (
        'Please summarize the conversation into three sections: "Question," "Answer," and "Evaluation."\n'
        'Current summary:\n'
        '{summary}\n'
        'New lines:\n'
        '{new_lines}\n'
        'Please write your updated summary in the following format:\n'
        '- Question:\n'
        '- Answer:\n'
        '- Evaluation:\n'
    )
    return PromptTemplate.from_template(prompt_text)


# Summary of questions asked so far
def get_summary_memory(existing_summary: str='') -> ConversationSummaryMemory:
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    memory = ConversationSummaryMemory(
        llm=llm,
        summary_prompt=custom_prompt())
    
    if existing_summary:
        memory.buffer = existing_summary
    return memory

