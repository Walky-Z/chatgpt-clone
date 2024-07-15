run_streamlit:
	streamlit run frontend/streamlit.py

run_api:
	uvicorn api.api_file:app --reload

gcp_connect:
	@gcloud auth login
	@gcloud config set project wagon-bootcamp-414210
