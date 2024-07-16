import os
secret_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'secrets.toml')



##################  VARIABLES  ##################

# GCP Project
GCP_PROJECT=os.environ.get("GCP_PROJECT")
GCP_REGION=os.environ.get("GCP_REGION")

# Cloud Storage
BUCKET_NAME=os.environ.get("BUCKET_NAME")

# BigQuery
BQ_REGION=os.environ.get("BQ_REGION")
BQ_DATASET=os.environ.get("BQ_DATASET")

SQL_ENDPOINT = os.environ.get("SQL_ENDPOINT")
SQL_USERNAME = os.environ.get("SQL_USERNAME")
SQL_PWD = os.environ.get("SQL_PWD")
SQL_DATABASE = os.environ.get("SQL_DATABASE")
DEFAULT_DB = os.environ.get("DEFAULT_DB")
RDS_PORT = os.environ.get("RDS_PORT")
