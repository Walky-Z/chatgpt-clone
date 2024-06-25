from cgitb import text
from itertools import count
from pyexpat import model
from wsgiref.simple_server import sys_version
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from sympy import total_degree
import tiktoken

import streamlit as st
from streamlit_chat import message
import requests


# Load .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

def count_tokens(string: str, model_name="gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_external_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def get_tokens():
    params = {
        'ip_address': ip_adress,
        'tokens_used': 0
    }
    response = requests.post(url='http://127.0.0.1:8000/process_request', params=params).json()
    print(response)
    return response['remaining_tokens'], response['initial_tokens']

def update_tokens(text: st.text, bar: st.progress):
    remaining, initial = get_tokens()
    per_remaining_tokens = remaining/initial
    text.text(f"Remaining Tokens : {remaining}/{initial}")
    bar.progress(per_remaining_tokens)


ip_adress = get_external_ip()
print(ip_adress)

st.set_page_config(
    page_title='You Custom Assistant',
    page_icon='🤖'
)
st.subheader('Your Custom Assistant 🤖')

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_message = st.text_input(label='System role')
    #user_prompt = st.text_input(label='Send a prompt')
    user_prompt = st.text_area("Send a prompt :", height=200, key="text_area")
    ip = {'ip_address': ip_adress}
    remaining, initial = get_tokens()
    per_remaining_tokens = remaining/initial
    remaing_text = st.text(f"Remaining Tokens : {remaining}/{initial}")
    progress_bar = st.progress(per_remaining_tokens)

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
            )
        # st.write(st.sess ion_state.messages)
    if user_prompt:
        human_message = HumanMessage(content=user_prompt)

        st.session_state.messages.append(human_message)

        construct_tokens = count_tokens(str(st.session_state.messages)[1:-1])




        params = {
            'ip_address': ip_adress,
            'tokens_used': construct_tokens
        }
        response = requests.post(url='http://127.0.0.1:8000/process_request', params=params).json()

        if response["valid_request"]:
            with st.spinner('Working on your request ...'):
                call_chatgpt = chat(st.session_state.messages)
            ai_message = AIMessage(content=call_chatgpt.content)
        else:
             ai_message = AIMessage(content="Not enough tokens for your request")


        st.session_state.messages.append(ai_message)

        # Count tokens after adding the AI response
        #total_tokens =sum([count_tokens(message.content) for message in st.session_state.messages])
        total_tokens = construct_tokens + count_tokens(ai_message.content)

        update_tokens(remaing_text, progress_bar)

        print(f'Nombre total de tokens: {total_tokens}')
        print(st.session_state.messages)

#st.session_state.messages
# message('this is chatgpt', is_user=False)
# message('this is the user', is_user=True)

if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

for i, msg in enumerate(st.session_state.messages[1:]):
    if i%2 == 0:
        message(msg.content, is_user=True, key=f'{i} + 🙂')
    else:
        message(msg.content, is_user=False, key=f'{i} + 🤖')
