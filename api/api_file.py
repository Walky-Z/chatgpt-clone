from fastapi import FastAPI, HTTPException, Request
import uvicorn
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

# Utilisation de defaultdict pour simuler la base de données en mémoire
db = defaultdict(lambda: {'tokens': 1000, 'reset_time': datetime.now() + timedelta(days=1)})

@app.post("/process_request/{ip_address}")
async def process_request(ip_address: str, prompt: str, response_length_estimate: int):
    data = db[ip_address]
    if datetime.now() >= data['reset_time']:
        data['tokens'] = 1000  # Reset quotidien
        data['reset_time'] = datetime.now() + timedelta(days=1)

    total_tokens = len(prompt.split()) + response_length_estimate  # Estimation simplifiée

    if data['tokens'] >= total_tokens:
        data['tokens'] -= total_tokens  # Décompte des tokens
        # Ici, vous traiteriez la requête et généreriez la réponse
        return {"message": "Requête traitée avec succès", "remaining_tokens": data['tokens']}
    else:
        raise HTTPException(status_code=429, detail="Token limit reached")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
