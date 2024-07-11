import toml
import hashlib
from api.params import *
import streamlit as st


# Charger les secrets existants
def load_secrets():
    try:
        with open(secret_path, "r") as f:
            secrets = toml.load(f)
    except FileNotFoundError:
        secrets = {}
    return secrets

# Sauvegarder les secrets
def save_secrets(secrets):
    with open(secret_path, "w") as f:
        toml.dump(secrets, f)

# Fonction pour hacher les mots de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction pour afficher le formulaire de connexion
def show_login_form():
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button("Se connecter")

        if submit_button:
            secrets = load_secrets()
            hashed_password = hash_password(password)
            if username in secrets and secrets[username] == hashed_password:
                st.success(f"Bienvenue, {username}!")
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Fonction pour afficher le formulaire de création d'utilisateur
def show_create_user_form():
    with st.form("create_user_form"):
        new_username = st.text_input("Nouveau nom d'utilisateur")
        new_password = st.text_input("Nouveau mot de passe", type="password")
        create_button = st.form_submit_button("Créer l'utilisateur")

        if create_button:
            if new_username and new_password:
                secrets = load_secrets()
                secrets[new_username] = hash_password(new_password)
                save_secrets(secrets)
                st.success(f"Utilisateur {new_username} créé avec succès!")
            else:
                st.error("Veuillez remplir tous les champs.")
