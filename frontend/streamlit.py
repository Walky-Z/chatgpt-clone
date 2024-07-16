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
from api.gcp_data import *
from api.psql_data import *

def disable():
    st.session_state.disabled = True

def refresh():
    st.session_state.refresh = True

def init_db():
    #create_dataset()
    create_database()
    create_db()
    return True


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False



# Load .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
#     st.error("La variable d'environnement GOOGLE_APPLICATION_CREDENTIALS n'est pas définie.")
# else:
#     st.success("Les identifiants Google Cloud sont configurés.")

init_db()

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

# Initialiser l'état de session pour le rafraîchissement
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

if 'username' not in st.session_state:
    st.session_state.username = None



with st.sidebar:
    # Boutons pour afficher/masquer les formulaires
    col1, col2 = st.columns(2)
    if st.session_state.logged_in == False:
        with col1:
            if st.button("Login"):
                st.session_state.show_login = not st.session_state.show_login
                st.session_state.show_create_user = False

        with col2:
            if st.button("Créer un utilisateur"):
                st.session_state.show_create_user = not st.session_state.show_create_user
                st.session_state.show_login = False

    # Affichage conditionnel du formulaire de connexion
    if st.session_state.show_create_user:
        show_create_user_form()

    if st.session_state.show_login:
        log = show_login_form()
        if log[0]:
            st.session_state.username = log[1]
            st.session_state.logged_in = True
            st.session_state.show_login = False
            st.experimental_rerun()


    print(f'show_login : {st.session_state.show_login}')
    print(f'logged_in : {st.session_state.logged_in}')

    if st.session_state.logged_in:
        st.write(f"Bienvenue {st.session_state.username}, dans votre tableau de bord!")
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
