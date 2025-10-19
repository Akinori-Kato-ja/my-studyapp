from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        model='gpt-4o-mini',
        temperature=0.7,
        max_completion_tokens=1000,
    )

def get_conversation_chain():
    memory = ConversationBufferMemory()
    llm = get_llm()
    return ConversationChain(llm=llm, memory=memory, verbose=True)
