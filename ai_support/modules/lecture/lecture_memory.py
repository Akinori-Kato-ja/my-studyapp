from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI


# Initialize summary memory with existing summary data
def get_summary_memory(existing_summary: str='') -> ConversationSummaryMemory:
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    memory = ConversationSummaryMemory(llm=llm)
    if existing_summary:
        memory.buffer = existing_summary
    return memory
