import pandas as pd
import numpy as np
import requests

import os
from typing import List
from dotenv import load_dotenv


# =========================================================
# PUBLIC FIGURE HANDLES CONFIGURATION
# =========================================================
PUBLIC_FIGURES = {
    "lebron james": {
        "wiki_name": "LeBron_James",
        "x_handle": "KingJames",
        "instagram_handle": "kingjames",
        "facebook_handle": "LeBron",
        "youtube_handle": "lebronjamescom" 
    },
    "cristiano ronaldo": {
        "wiki_name": "Cristiano_Ronaldo",
        "x_handle": "Cristiano",
        "instagram_handle": "cristiano",
        "facebook_handle": "Cristiano",
        "youtube_handle": "cristiano"   
    },
    "erling haaland": {
        "wiki_name": "Erling_Haaland",
        "x_handle": "ErlingHaaland",
        "instagram_handle": "erling",
        "facebook_handle": "erlinghaaland",
        "youtube_handle": "erling"
    },
    "giannis antetokounmpo": {
        "wiki_name": "Giannis_Antetokounmpo",
        "x_handle": "Giannis_An34",
        "instagram_handle": "giannis_an34",
        "facebook_handle": "GreekFreakOfficial",
        "youtube_handle": "GiannisAntetokounmpo"
    },

    "roger federer": {
        "wiki_name": "Roger_Federer",
        "x_handle": "rogerfederer",
        "instagram_handle": "rogerfederer",
        "facebook_handle": "Federer",   
        "youtube_handle": "rogerfederer"
    },
    "stephen curry": {
        "wiki_name": "Stephen_Curry",
        "x_handle": "StephenCurry30",
        "instagram_handle": "stephencurry30",
        "facebook_handle": "StephenCurryOfficial",
        "youtube_handle": "stephcurry"
    },
    "kylian mbappé": {
        "wiki_name": "Kylian_Mbappé",
        "x_handle": "KMbappe",
        "instagram_handle": "k.mbappe",
        "facebook_handle": "kylianmbappeofficiel",   
        "youtube_handle": "KylianMbappe"
    },
    "neymar jr": {
        "wiki_name": "Neymar",
        "x_handle": "neymarjr",
        "instagram_handle": "neymarjr",
        "facebook_handle": "neymarjr",
        "youtube_handle": "NeymarJrReal"
    },
    "serena williams": {
        "wiki_name": "Serena_Williams",
        "x_handle": "serenawilliams",
        "instagram_handle": "serenawilliams",
        "facebook_handle": "SerenaWilliams",
        "youtube_handle": "SerenaWilliams"
    },
    "novak djokovic": {
        "wiki_name": "Novak_Djokovic",
        "x_handle": "DjokerNole",
        "instagram_handle": "djokernole",
        "facebook_handle": "djokovicofficial",
        "youtube_handle": "DjokerNole"
    }
}

# =========================================================
# CREDENTIALS CONFIGURATION
# =========================================================

load_dotenv()

# all credetials are stored in .env file and accessed using os.getenv
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_SECRET_KEY = os.getenv("X_SECRET_KEY")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")


# =========================================================
# API SETUP
# =========================================================

def setup_wikipedia_REST_api()-> tuple[requests.Session, str]:
    seneca_email = "srkhati@myseneca.ca"
    # setting up header according to Wikipedia documentation
    headers = {
        'User-Agent': seneca_email,
        "Accept": 'application/json'
    }
    REQ_LIMIT = 200 # wikipedia limits to 200 req/s
    BASE_API_URL = 'https://en.wikipedia.org/api/rest_v1'
    session = requests.Session()
    session.headers.update(headers)
    return session, BASE_API_URL

def setup_youtube_api() -> list[requests.Session, str]:
    # need to append ?key=YOUTUBE_API_KEY for session
    BASE_API_URL = "https://www.googleapis.com/youtube/v3"
    headers = {"Accept": 'application/json'}
    session = requests.Session()
    session.headers.update(headers)
    return session, BASE_API_URL

def setup_X_api():
    BASE_API_URL = "https://api.x.com/2/users/by/username/xdevelopers"
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}", "Accept": 'application/json'}
    session = requests.Session()
    session.headers.update(headers)
    return session, BASE_API_URL



# =========================================================
# UTILITIES
# =========================================================


# session, BASE_API_URL = setup_wikipedia_REST_api()
# print(session.get(f"{BASE_API_URL}/page/summary/{PUBLIC_FIGURES['lebron james']['wiki_name']}").json())