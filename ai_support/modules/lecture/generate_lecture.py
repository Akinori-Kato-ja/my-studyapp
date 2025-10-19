from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from ai_support.ai_chain import get_conversation_chain



def generate_lecture(title):
    conversation = get_conversation_chain()
    response1 = conversation.predict(input=(
        'You are an excellent teacher.'
        f'Please give a lecture based on the title <{title}>'
    ))
    print(response1)
    return response1

generate_lecture('Pythonのforループ')
