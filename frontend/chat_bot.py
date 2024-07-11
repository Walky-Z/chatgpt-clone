
import streamlit as st
import requests
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from frontend.manage_tokens import *

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)


def chat_bot(ip_adress):
        system_message = st.text_input(label='System role')
        #user_prompt = st.text_input(label='Send a prompt')
        user_prompt = st.text_area("Send a prompt :", height=200, key="text_area")
        remaining, initial = get_tokens(ip_adress)
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

            update_tokens(remaing_text, progress_bar, ip_adress)

            print(f'Nombre total de tokens: {total_tokens}')
            print(st.session_state.messages)
