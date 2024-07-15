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
