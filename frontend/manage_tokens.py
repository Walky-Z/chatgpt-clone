
import tiktoken
import requests
import streamlit as st

def count_tokens(string: str, model_name="gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_external_ip():
    response = requests.get('https://api.ipify.org')
    return response.text

def get_tokens(ip):
    params = {
        'ip_address': ip,
        'tokens_used': 0
    }
    response = requests.post(url='http://127.0.0.1:8000/process_request', params=params).json()
    print(response)
    return response['remaining_tokens'], response['initial_tokens']

def update_tokens(text: st.text, bar: st.progress, ip):
    remaining, initial = get_tokens(ip)
    per_remaining_tokens = remaining/initial
    text.text(f"Remaining Tokens : {remaining}/{initial}")
    bar.progress(per_remaining_tokens)
