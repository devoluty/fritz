import requests
from base64 import b64encode

import os
from dotenv import load_dotenv
load_dotenv()


def get_response_data(response):
    try:
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"An error occurred while parsing the response: {e}")
        return str(e)


def get_token(client_id, client_secret):
	auth_string = b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
	auth_options = {
		"url": "https://accounts.spotify.com/api/token",
		"headers": {
			"Authorization": f"Basic {auth_string}"
		},
		"data": {
			"grant_type": "client_credentials"
		}
	}
	response = requests.post(**auth_options)

	return get_response_data(response)


def get_releases(token, country, limit):
    headers = {
    	"Accept": "application/json",
    	"Content-Type": "application/json",
    	"Authorization": f"Bearer {token}",
    }   
    params = {
    	"country": country,
    	"limit": limit,
    }   
    response = requests.get("https://api.spotify.com/v1/browse/new-releases", headers=headers, params=params)   
    return get_response_data(response)


def main():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    try:
        token = get_token(client_id, client_secret)
        if token:
            print(token)
            new_releases = get_releases(token['access_token'], "US", 5)
            if new_releases:
                # do something with the new releases
                return new_releases['albums']['items']
                
    except Exception as e:
        print(f"An error occurred: {e}")
