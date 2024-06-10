run_streamlit:
	streamlit run frontend/custom_chatgpt.py

run_api:
	uvicorn api.api_file:app --reload
