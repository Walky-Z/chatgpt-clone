import psycopg2
from psycopg2 import OperationalError
import uuid
from api.params import *
from frontend.st_auth import *
from api.gcp_data import hash_password
from api.params import SQL_DATABASE, SQL_ENDPOINT, SQL_PWD, SQL_USERNAME, DEFAULT_DB
from psycopg2 import sql, OperationalError

def create_database():
    connection = None
    try:
        # Connexion à la base de données par défaut
        connection = psycopg2.connect(
            host=SQL_ENDPOINT,
            user=SQL_USERNAME,
            password=SQL_PWD,
            dbname=DEFAULT_DB,
            port=RDS_PORT
        )
        connection.autocommit = True

        cursor = connection.cursor()
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [SQL_DATABASE])

        if cursor.fetchone():
            print(f"Database {SQL_DATABASE} existe déjà.")
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(SQL_DATABASE)))
            print(f"Database {SQL_DATABASE} créée avec succès.")

        cursor.close()

    except OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

# Connexion à la base de données
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=SQL_ENDPOINT,
            user=SQL_USERNAME,
            password=SQL_PWD,
            dbname=SQL_DATABASE
        )
        return connection
    except OperationalError as e:
        print(f"OperationalError: {e}")
    except Exception as e:
        print(f"Error: {e}")


def create_db():
    query = """
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id UUID PRIMARY KEY,
        user VARCHAR(255) UNIQUE NOT NULL,
        pwd VARCHAR(255) NOT NULL,
        tokens VARCHAR(255)
    );
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Table créée avec succès")

def check_user(user, pwd):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT pwd FROM utilisateurs
    WHERE user = %s
    """
    cursor.execute(query, (user,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        hashed_password = result[0]
        return hashed_password == hash_password(pwd)
    return False

def add_user(user, pwd, tokens):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO utilisateurs (id, user, pwd, tokens)
    VALUES (%s, %s, %s, %s)
    """
    pwd_hash = hash_password(pwd)
    try:
        cursor.execute(query, (str(uuid.uuid4()), user, pwd_hash, tokens))
        conn.commit()
        st.success("Utilisateur ajouté avec succès")
    except psycopg2.IntegrityError as e:
        conn.rollback()
        st.error("Un utilisateur avec ce nom d'utilisateur existe déjà.")
    cursor.close()
    conn.close()
