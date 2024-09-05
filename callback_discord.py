# api.py
from fastapi import FastAPI
import requests
# import config

# import discord
# from discord.ext import commands
# from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Request, HTTPException, Response
from starlette.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

# ---------------------api------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------main page as docs----------------------------
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    # response = RedirectResponse(url='/docs')
    response = RedirectResponse(url='/api/v2/docs')
    return response

# ------------------------------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.get("/auth/login", tags=["Dashboard"])
async def login():
    return RedirectResponse(url="https://discord.com/oauth2/authorize?client_id=1276380605981921330&redirect_uri=http://127.0.0.1:8001/auth/callback&scope=identify%20guilds&response_type=code&state=hdsafljasdfsdfa")

@app.get("/auth/callback/", tags=["Dashboard"])
async def callback(code: str):
    print('code:-',code)
    if not code:
        raise HTTPException(status_code=400, detail="Code not provided")

    data = {
        "client_id": "1276380605981921330",
        "client_secret": "pICakApmcxsv4WknH5K_O0KHnA1x0cKi",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8001/auth/callback",
    }
    print('data:-',data)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/x-www-form-urlencoded",
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    print("dicord api response:", response.status_code)

    response.raise_for_status()

    token_response = TokenResponse(**response.json())
    print("token_response:",token_response)

    # Store token in local storage
    # This part cannot be directly implemented in FastAPI as it's a server-side framework.
    # You can send the token back to the client and store it in the browser's local storage using JavaScript.

    # Fetch user
    user_response = requests.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {token_response.access_token}"})
    user_response.raise_for_status()
    user_data = user_response.json()
    print('user_data:-',user_data)

    # Fetch Guilds
    guilds_response = requests.get("https://discord.com/api/users/@me/guilds", headers={"Authorization": f"Bearer {token_response.access_token}"})
    guilds_response.raise_for_status()
    guilds_data = guilds_response.json()
    print('guilds_data:-',guilds_data)
    # [{'id': '1264832793536630816', 'name': 'AIGAEA', 'icon': 'a7d5c0eb6a8a19bbde81011b3e235675', 'banner': None, 'owner': True, 'permissions': 2147483647, 'permissions_new': '2251799813685247', 'features': ['COMMUNITY', 'NEWS']}

    guilds = [guild for guild in guilds_data if guild["permissions"] == 2147483647]
    data = {"user": user_data, "guilds": guilds}
    print('data:-',data)

    return data

if __name__ == "__main__":
    # app.run(host=config.HOST, port=config.PORT)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 
