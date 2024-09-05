from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from requests_oauthlib import OAuth1Session
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = 'deipp7UeQM4DY3xGxgHspyE3y' #os.getenv('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = 'bVKoVtIpCBKIByvSQKKklJwwDBqpF5G4dqZY1uBdu6OhIDVfKh' #os.getenv('TWITTER_CONSUMER_SECRET')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/auth/login")
async def request_token():
    """Obtain a request token to start the sign-in process."""
    oauth = OAuth1Session(
                        client_key=CONSUMER_KEY, 
                        client_secret=CONSUMER_SECRET, 
                        callback_uri='http://127.0.0.1:8001/auth/callback',
                    )
    try:
        fetch_response = oauth.fetch_request_token('https://api.twitter.com/oauth/request_token')
        print(f"fetch_response: {fetch_response}")

        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        print(f"resource_owner_key: {resource_owner_key}")
        print(f"resource_owner_secret: {resource_owner_secret}")

        # Redirect user to Twitter for authorization
        authorization_url = oauth.authorization_url('https://api.twitter.com/oauth/authenticate')
        print(f"authorization_url: {authorization_url}")

        return {"authorization_url": authorization_url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/auth/callback")
async def twitter_callback(oauth_token: str, oauth_verifier: str):
    """Handle the callback from Twitter with oauth_token and oauth_verifier."""
    
    print(f"oauth_token: {oauth_token}")
    print(f"oauth_verifier: {oauth_verifier}")
    
    oauth = OAuth1Session(
                        CONSUMER_KEY, 
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=oauth_token, 
                        verifier=oauth_verifier
                    )
    try:
        tokens = oauth.fetch_access_token('https://api.twitter.com/oauth/access_token')
        print(f"tokens: {tokens}")

        access_token = tokens['oauth_token']
        access_token_secret = tokens['oauth_token_secret']
        # Use access_token and access_token_secret to make Twitter API calls
        print(f"access_token: {access_token}")
        print(f"access_token_secret: {access_token_secret}")
        
        # 授权成功跳转
        return {}
        # return RedirectResponse('https://luxuryverse-d.vercel.app/register?twitter=1')
        #return {"access_token": access_token, "access_token_secret": access_token_secret}
    except Exception as e:
        return {"error": str(e)}

@app.get("/auth/get-user-details")
async def get_user_details(access_token: str, access_token_secret: str, include_email: bool = Query(default=True)):
    """Fetch extended user details from Twitter including the email if requested."""
    
    print(f"access_token: {access_token}")
    print(f"access_token_secret: {access_token_secret}")
    print(f"include_email: {include_email}")
    
    oauth = OAuth1Session(
                        CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=access_token,
                        resource_owner_secret=access_token_secret
                    )

    params = {
        "include_email": "true" if include_email else "false",
        "skip_status": "true",  # Adjust this as needed to include/exclude status
        "include_entities": "true"
    }
    response = oauth.get("https://api.twitter.com/1.1/account/verify_credentials.json", params=params)
    if response.status_code == 200:
        user_data = response.json()
        print("user_data:", user_data)
        # return {
        #     "id": user_data.get("id_str"),
        #     "name": user_data.get("name"),
        #     "screen_name": user_data.get("screen_name"),
        #     "location": user_data.get("location"),
        #     "description": user_data.get("description"),
        #     "url": user_data.get("url"),
        #     "entities": user_data.get("entities"),
        #     "protected": user_data.get("protected"),
        #     "followers_count": user_data.get("followers_count"),
        #     "friends_count": user_data.get("friends_count"),
        #     "listed_count": user_data.get("listed_count"),
        #     "created_at": user_data.get("created_at"),
        #     "favourites_count": user_data.get("favourites_count"),
        #     "geo_enabled": user_data.get("geo_enabled"),
        #     "verified": user_data.get("verified"),
        #     "statuses_count": user_data.get("statuses_count"),
        #     "lang": user_data.get("lang"),
        #     "status": user_data.get("status"),
        #     "profile_image_url_https": user_data.get("profile_image_url_https"),
        #     "email": user_data.get("email")  # This may be None if not available or not permitted
        # }
    else:
        print("response:",response.json())
        return {"error": "Failed to fetch user details", "status_code": response.status_code}

    params = {
        "screen_name": "CPangtou,aigaea",
    }
    response = oauth.get('https://api.twitter.com/1.1/friendships/lookup.json', params=params).json()
    print("response:",response)

    # if response.status_code == 200:

    # response = oauth.get("https://api.twitter.com/1.1/friendships/lookup.json?screen_name=CPangtou,aigaea", params=params)
    # print("response:",response)
    # if response.status_code == 200:
    #     follower_data = response.json()
    #     print("follower_data:", follower_data)
    # else:
    #     print("response:",response.json())
    #     return {"error": "Failed to fetch user details", "status_code": response.status_code}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 