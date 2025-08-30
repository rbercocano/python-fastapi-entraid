# Python FastAPI API Secured with Entra ID (Service Principal)

This project demonstrates a **FastAPI API** secured with **OAuth 2.0** using a **Service Principal** (client credentials flow). It includes:

- Acquisition of JWT tokens from Microsoft Entra ID.
- Validation of tokens in the API.
- Example REST Client requests to test the API.

---

## **1. Prerequisites**

- **Python 3.10+**  
  [Download Python](https://www.python.org/downloads/)

- **VS Code**  
  [Download VS Code](https://code.visualstudio.com/)

- **VS Code Extensions**  
  - Python (`ms-python.python`)  
  - REST Client (`humao.rest-client`)

- **pip dependencies**  
  ```bash
  pip install fastapi uvicorn python-dotenv msal requests python-jose
  ```

### Entra ID Setup
- Create an **App Registration** for your API.  
  - Note the **Application (client) ID** — this will be used as the audience (`aud`) in your API.  

- Create a **Service Principal** (client credentials) for authentication.  
  - Note the **Client ID** and **Client Secret** — these will be used by clients to request a token.  

- **No API permissions are required** for the Service Principal if it’s only used to authenticate and get a JWT for your API.  

- Optionally, grant **admin consent** if you plan to extend scopes in the future, but it is **not needed** for basic SP authentication.


---

## **2. Project Structure**

```
project/
├── config/
│   └── .env                # Environment variables
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── api_calls.http           # REST Client calls
└── README.md
```

---

## **3. Configuration**

Create `.env` in `config/`:

```env
TENANT_ID=<your-tenant-id>
API_CLIENT_ID=<api-app-registration-client-id>
SP_CLIENT_ID=<service-principal-client-id>
SP_CLIENT_SECRET=<service-principal-client-secret>
SCOPE=api://<api-app-registration-client-id>/.default
```

> Replace `<...>` with your real values.

---

## **4. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **5. Run the API**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Health endpoint: `http://localhost:8000/health`  
- Secure endpoint: `http://localhost:8000/secure-data`  
- Acquire token using SP: `http://localhost:8000/get-token`

---

## **6. Debugging in VS Code**

1. Open **Run and Debug** (`Ctrl+Shift+D`).  
2. Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", "8000"
      ],
      "envFile": "${workspaceFolder}/config/.env",
      "jinja": true
    }
  ]
}
```

3. Select **Python: FastAPI** and press **F5** to start in debug mode.  
4. Set breakpoints in `app.py` and debug requests as they arrive.

---

## **7. Testing with REST Client**

1. Open `api_calls.http` in VS Code.  
2. Update placeholders with real values:

```http
### Step 1: Get Access Token
POST https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token
Content-Type: application/x-www-form-urlencoded

client_id=<SP_CLIENT_ID>&scope=api://<API_CLIENT_ID>/.default&client_secret=<SP_CLIENT_SECRET>&grant_type=client_credentials

### Step 2: Call Secure API
GET http://localhost:8000/secure-data
Authorization: Bearer <ACCESS_TOKEN_HERE>
```

3. Click **“Send Request”** above the POST request.  
4. Copy the `access_token` from the response.  
5. Paste it in the GET request header and **send request**.  
6. You should see a JSON response indicating successful authentication.

---

## **8. Optional: Environment Variables in REST Client**

Create `.vscode/rest-client.env.json`:

```json
{
  "local": {
    "tenant_id": "<YOUR_TENANT_ID>",
    "sp_client_id": "<YOUR_SP_CLIENT_ID>",
    "sp_client_secret": "<YOUR_SP_CLIENT_SECRET>",
    "api_client_id": "<YOUR_API_CLIENT_ID>"
  }
}
```

Then use `{{variable_name}}` in `api_calls.http` for easier reuse.

---

## **9. Notes**

- Tokens expire in ~1 hour — you must request a new token to call the API.  
- In production (e.g., Azure App Service), store SP secrets in **App Settings** instead of `.env`.  
- Debugging allows inspecting the JWT payload and API flow.
