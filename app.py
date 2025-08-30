from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# Load env
load_dotenv(dotenv_path="./config/.env")

TENANT_ID = os.getenv("TENANT_ID")
API_CLIENT_ID = os.getenv("API_CLIENT_ID")  # The API's App Registration

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

app = FastAPI()
bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    jwks_uri = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
    jwks = requests.get(jwks_uri).json()
    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == header["kid"])
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=API_CLIENT_ID)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/secure-api")
def secure_data(user=Depends(verify_token)):
    return {"message": "You are authenticated!", "user": user}

@app.get("/health")
def health():
    return {"status": "running"}
