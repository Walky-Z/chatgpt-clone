import pandas as pd
import uuid
import bcrypt
import streamlit as st
from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path
from api.params import *
from frontend.st_auth import *

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_dataset():
    client = bigquery.Client(project=GCP_PROJECT)
    dataset_id = f"{GCP_PROJECT}.{BQ_DATASET}"
    try:
        client.get_dataset(dataset_id)  # Vérifie si le dataset existe
        print(f"Dataset {BQ_DATASET} existe déjà.")
    except:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = BQ_REGION
        client.create_dataset(dataset)  # Crée le dataset
        print(f"Dataset {BQ_DATASET} créé avec succès.")

def load_data_to_bq(
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool
    ) -> None:
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
    print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

    # Load data onto full_table_name

    # 🎯 HINT for "*** TypeError: expected bytes, int found":
    # After preprocessing the data, your original column names are gone (print it to check),
    # so ensure that your column names are *strings* that start with either
    # a *letter* or an *underscore*, as BQ does not accept anything else

    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

    client = bigquery.Client()

    # Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # Load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete


    print(f"✅ Data saved to bigquery, with shape {data.shape}")

def create_db_bq():
    query=f"""
        CREATE TABLE IF NOT EXISTS `{GCP_PROJECT}.{BQ_DATASET}.utilisateurs` (
        id STRING,
        nom_utilisateur STRING,
        mot_de_passe STRING,
        tokens INT64
        );
    """
    # Connexion à BigQuery
    client = bigquery.Client(project=GCP_PROJECT)
    query_job = client.query(query)

    # Attente de l'achèvement de la requête
    query_job.result()
    print("Table créée avec succès")


def add_user_bq(user, pwd, tokens=1000):
    pwd_hash = hash_password(pwd)
    client = bigquery.Client(project=GCP_PROJECT)
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.utilisateurs"
    rows_to_insert = [
        {u"id": str(uuid.uuid4()), u"nom_utilisateur": user, u"mot_de_passe": pwd_hash, u"tokens": tokens}
    ] # uuid.uuid4() Permet d'avoir des id uniques
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        st.error(f"Erreur lors de l'insertion des données : {errors}")
    else:
        st.success("Utilisateur ajouté avec succès")

def check_user_bq(user, pwd):
    client = bigquery.Client(project=GCP_PROJECT)
    query = f"""
    SELECT mot_de_passe FROM `{GCP_PROJECT}.{BQ_DATASET}.utilisateurs`
    WHERE nom_utilisateur = '{user}'
    """
    query_job = client.query(query)
    results = query_job.result()

    for row in results:
        if bcrypt.checkpw(pwd.encode('utf-8'), row.mot_de_passe.encode('utf-8')):
            return True
    return False
