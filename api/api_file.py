from fastapi import FastAPI, HTTPException, Request
import uvicorn
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI()

# Utilisation de defaultdict pour simuler la base de données en mémoire
default_tokens = 1000
db = defaultdict(lambda: {'tokens': default_tokens, 'reset_time': datetime.now() + timedelta(days=1)})

# @app.get("/tokens_status")
# def tokens_status(ip_address: str):
#     data = db[ip_address]
#     return {"remaining_tokens": data['tokens'], "initial_tokens": default_tokens}


@app.post("/process_request")
async def process_request(ip_address: str, tokens_used: int):
    data = db[ip_address]
    if datetime.now() >= data['reset_time']:
        data['tokens'] = default_tokens  # Reset quotidien
        data['reset_time'] = datetime.now() + timedelta(days=1)

    if data['tokens'] >= tokens_used:
        data['tokens'] -= tokens_used  # Décompte des tokens
        # Ici, vous traiteriez la requête et généreriez la réponse
        #return {"message": "Requête traitée avec succès", "remaining_tokens": data['tokens']}
        return {"remaining_tokens": data['tokens'], "initial_tokens": default_tokens, "valid_request": True}
    else:
        return {"remaining_tokens": data['tokens'], "initial_tokens": default_tokens, "valid_request": False}
        #raise HTTPException(status_code=429, detail="Token limit reached")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
