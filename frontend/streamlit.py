from cgitb import text
from itertools import count
from pyexpat import model
from wsgiref.simple_server import sys_version

from langchain.schema import SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory
from sympy import total_degree

import streamlit as st
from streamlit_chat import message
from frontend.st_auth import *
from frontend.chat_bot import chat_bot
from frontend.manage_tokens import get_external_ip

def disable():
    st.session_state.disabled = True

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False



# Load .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)




ip_adress = get_external_ip()
print(ip_adress)

st.set_page_config(
    page_title='You Custom Assistant',
    page_icon='🤖'
)
st.subheader('Your Custom Assistant 🤖')


if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialisation de l'état de l'application
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

if 'show_create_user' not in st.session_state:
    st.session_state.show_create_user = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False




with st.sidebar:
    # Boutons pour afficher/masquer les formulaires
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.show_login = not st.session_state.show_login
            st.session_state.show_create_user = False

    with col2:
        if st.button("Créer un utilisateur"):
            st.session_state.show_create_user = not st.session_state.show_create_user
            st.session_state.show_login = False

    # Affichage conditionnel du formulaire de connexion
    if st.session_state.show_login and not st.session_state.logged_in:
        show_login_form()

    if st.session_state.show_create_user:
        show_create_user_form()

    chat_bot(ip_adress)

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
