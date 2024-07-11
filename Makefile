run_streamlit:
	streamlit run frontend/streamlit.py

run_api:
	uvicorn api.api_file:app --reload
