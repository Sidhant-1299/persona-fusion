import pandas as pd
import requests

from apify_client import ApifyClient
import os
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


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

# =========================================================
# CREDENTIALS CONFIGURATION
# =========================================================

load_dotenv()

# all credetials are stored in .env file and accessed using os.getenv
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY","").strip()
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY","").strip()
X_SECRET_KEY = os.getenv("X_SECRET_KEY","").strip()
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN","").strip()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN","").strip()

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

def setup_youtube_api() -> tuple[requests.Session, str]:
    # need to append ?key=YOUTUBE_API_KEY for session
    BASE_API_URL = "https://www.googleapis.com/youtube/v3"
    headers = {"Accept": 'application/json'}
    session = requests.Session()
    session.headers.update(headers)
    return session, BASE_API_URL

def setup_X_api() -> tuple[requests.Session, str]:
    BASE_API_URL = "https://api.x.com/2"
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}",
        "Accept": "application/json"
    }
    session = requests.Session()
    session.headers.update(headers)
    return session, BASE_API_URL


def setup_apify_client() -> ApifyClient:
    if not APIFY_API_TOKEN:
        raise ValueError("APIFY_API_TOKEN not found in environment.")
    return ApifyClient(APIFY_API_TOKEN)

def run_apify_actor(actor_id: str, run_input: dict) -> list[dict]:
    client = setup_apify_client()
    run = client.actor(actor_id).call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())

    return items

# =========================================================
# DATA COLLECTION FUNCTIONS
# =========================================================

def get_instagram_data(username: str) -> dict:
    url = "https://i.instagram.com/api/v1/users/web_profile_info/"
    headers = {
        "User-Agent": "Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/"
    }
    params = {"username": username}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return {
            "success": True,
            "platform": "instagram",
            "handle": username,
            "raw": response.json(),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "instagram",
            "handle": username,
            "raw": None,
            "error": str(e)
        }


def get_x_data(username: str) -> dict:
    session, base_url = setup_X_api()
    url = f"{base_url}/users/by/username/{username}"
    params = {
        "user.fields": "id,name,username,description,public_metrics,verified,created_at,location"
    }

    try:
        r = session.get(url, params=params, timeout=15)
        r.raise_for_status()
        return {
            "success": True,
            "platform": "x",
            "handle": username,
            "raw": r.json(),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "x",
            "handle": username,
            "raw": None,
            "error": str(e)
        }

def get_wikipedia_data(wiki_name: str) -> dict:
    session, base_url = setup_wikipedia_REST_api()
    url = f"{base_url}/page/summary/{wiki_name}"

    try:
        r = session.get(url, timeout=15)
        r.raise_for_status()
        return {
            "success": True,
            "platform": "wikipedia",
            "handle": wiki_name,
            "raw": r.json(),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "wikipedia",
            "handle": wiki_name,
            "raw": None,
            "error": str(e)
        }
    


def get_youtube_data(handle: str) -> dict:
    session, base_url = setup_youtube_api()
    url = f"{base_url}/channels"
    params = {
        "part": "snippet,statistics",
        "forHandle": handle,
        "key": YOUTUBE_API_KEY
    }

    try:
        r = session.get(url, params=params, timeout=15)
        r.raise_for_status()
        return {
            "success": True,
            "platform": "youtube",
            "handle": handle,
            "raw": r.json(),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "youtube",
            "handle": handle,
            "raw": None,
            "error": str(e)
        }


def get_facebook_data_apify(handle: str) -> dict:
    try:
        items = run_apify_actor(
            actor_id="apify/facebook-pages-scraper",
            run_input={
                "startUrls": [{"url": f"https://www.facebook.com/{handle}"}]
            }
        )

        return {
            "success": True,
            "platform": "facebook",
            "handle": handle,
            "raw": items,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "platform": "facebook",
            "handle": handle,
            "raw": None,
            "error": str(e)
        }
    

# =========================================================
# DATA NORMALIZER
# =========================================================

def empty_normalized_record() -> dict:
    return {
        "profile_name": None,
        "username": None,
        "profile_url": None,
        "description": None,
        "followers_count": None,
        "following_count": None,
        "content_count": None,
        "verified": None
    }


def normalize_wikipedia_data(result: dict) -> dict:
    record = empty_normalized_record()

    if not result["success"] or not result["raw"]:
        return record

    raw = result["raw"]
    record["profile_name"] = raw.get("title")
    record["username"] = raw.get("title")
    record["profile_url"] = raw.get("content_urls", {}).get("desktop", {}).get("page")
    record["description"] = raw.get("extract")
    return record


def normalize_x_data(result: dict) -> dict:
    record = empty_normalized_record()

    if not result["success"] or not result["raw"]:
        return record

    user = result["raw"].get("data", {})
    metrics = user.get("public_metrics", {})

    record["profile_name"] = user.get("name")
    record["username"] = user.get("username")
    record["profile_url"] = f"https://x.com/{user.get('username')}" if user.get("username") else None
    record["description"] = user.get("description")
    record["followers_count"] = metrics.get("followers_count")
    record["following_count"] = metrics.get("following_count")
    record["content_count"] = metrics.get("tweet_count")
    record["verified"] = user.get("verified")
    return record


def normalize_youtube_data(result: dict) -> dict:
    record = empty_normalized_record()

    if not result["success"] or not result["raw"]:
        return record

    items = result["raw"].get("items", [])
    if not items:
        return record

    ch = items[0]
    snippet = ch.get("snippet", {})
    stats = ch.get("statistics", {})

    record["profile_name"] = snippet.get("title")
    record["username"] = result["handle"]
    record["profile_url"] = f"https://www.youtube.com/@{result['handle']}" if result.get("handle") else None
    record["description"] = snippet.get("description")
    record["followers_count"] = stats.get("subscriberCount")
    record["content_count"] = stats.get("videoCount")
    return record


def normalize_instagram_data(result: dict) -> dict:
    record = empty_normalized_record()

    if not result["success"] or not result["raw"]:
        return record

    user = result["raw"].get("data", {}).get("user", {})

    if not user:
        return record

    record["profile_name"] = user.get("full_name")
    record["username"] = user.get("username")
    record["profile_url"] = f"https://www.instagram.com/{user.get('username')}/" if user.get("username") else None
    record["description"] = user.get("biography")
    record["followers_count"] = user.get("edge_followed_by", {}).get("count")
    record["following_count"] = user.get("edge_follow", {}).get("count")
    record["content_count"] = user.get("edge_owner_to_timeline_media", {}).get("count")
    record["verified"] = user.get("is_verified")
    return record


def normalize_facebook_data_apify(result: dict) -> dict:
    record = empty_normalized_record()

    if not result["success"] or not result["raw"]:
        return record

    item = result["raw"][0]

    record["profile_name"] = item.get("title") or item.get("pageName")
    record["username"] = item.get("pageName") or result.get("handle")
    record["profile_url"] = item.get("pageUrl") or item.get("facebookUrl")
    record["description"] = item.get("intro")

    record["followers_count"] = item.get("followers")
    record["following_count"] = item.get("followings")

    # use likes as content_count fallback only if nothing better exists
    record["content_count"] = item.get("likes")

    # actor doesn't seem to return a verified field
    record["verified"] = None

    return record




# =========================================================
# UNIFIED DATA BUILDER
# =========================================================

def build_unified_row(
    person_key: str,
    wiki_data: dict,
    x_data: dict,
    yt_data: dict,
    ig_data: dict,
    fb_data: dict
) -> dict:
    person = PUBLIC_FIGURES[person_key]

    return {
        "person_key": person_key,
        "canonical_name": wiki_data["profile_name"] or person_key.title(),

        "wiki_name": person["wiki_name"],
        "wiki_url": wiki_data["profile_url"],
        "wiki_description": wiki_data["description"],

        "x_handle": person["x_handle"],
        "x_name": x_data["profile_name"],
        "x_url": x_data["profile_url"],
        "x_description": x_data["description"],
        "x_followers": x_data["followers_count"],
        "x_following": x_data["following_count"],
        "x_posts": x_data["content_count"],
        "x_verified": x_data["verified"],

        "youtube_handle": person["youtube_handle"],
        "youtube_name": yt_data["profile_name"],
        "youtube_url": yt_data["profile_url"],
        "youtube_description": yt_data["description"],
        "youtube_subscribers": yt_data["followers_count"],
        "youtube_videos": yt_data["content_count"],

        "instagram_handle": person["instagram_handle"],
        "instagram_name": ig_data["profile_name"],
        "instagram_url": ig_data["profile_url"],
        "instagram_description": ig_data["description"],
        "instagram_followers": ig_data["followers_count"],
        "instagram_following": ig_data["following_count"],
        "instagram_posts": ig_data["content_count"],
        "instagram_verified": ig_data["verified"],

        "facebook_handle": person["facebook_handle"],
        "facebook_name": fb_data["profile_name"],
        "facebook_url": fb_data["profile_url"],
        "facebook_description": fb_data["description"],
        "facebook_followers": fb_data["followers_count"],
        "facebook_following": fb_data["following_count"],
        "facebook_content_count": fb_data["content_count"],
        "facebook_verified": fb_data["verified"],
    }


# =========================================================
# MAIN COLLECTOR
# =========================================================

def collect_data(person_key: str) -> dict:
    if person_key not in PUBLIC_FIGURES:
        raise ValueError(f"{person_key} not found in PUBLIC_FIGURES")

    person = PUBLIC_FIGURES[person_key]

    wiki_raw = get_wikipedia_data(person["wiki_name"])
    x_raw = get_x_data(person["x_handle"])
    yt_raw = get_youtube_data(person["youtube_handle"])

    try:
        ig_raw = get_instagram_data(person["instagram_handle"])
    except Exception as e:
        ig_raw = {
            "success": False,
            "platform": "instagram",
            "handle": person["instagram_handle"],
            "raw": None,
            "error": str(e)
        }

    try:
        fb_raw = get_facebook_data_apify(person["facebook_handle"])
    except Exception as e:
        fb_raw = {
            "success": False,
            "platform": "facebook",
            "handle": person["facebook_handle"],
            "raw": None,
            "error": str(e)
        }

    wiki_norm = normalize_wikipedia_data(wiki_raw)
    x_norm = normalize_x_data(x_raw)
    yt_norm = normalize_youtube_data(yt_raw)
    ig_norm = normalize_instagram_data(ig_raw)
    fb_norm = normalize_facebook_data_apify(fb_raw)

    unified = build_unified_row(
        person_key=person_key,
        wiki_data=wiki_norm,
        x_data=x_norm,
        yt_data=yt_norm,
        ig_data=ig_norm,
        fb_data=fb_norm
    )

    return {
        "raw": {
            "wikipedia": wiki_raw,
            "x": x_raw,
            "youtube": yt_raw,
            "instagram": ig_raw,
            "facebook": fb_raw
        },
        "normalized": {
            "wikipedia": wiki_norm,
            "x": x_norm,
            "youtube": yt_norm,
            "instagram": ig_norm,
            "facebook": fb_norm
        },
        "unified": unified
    }


def collect_all_data() -> pd.DataFrame:
    rows = []

    for person_key in PUBLIC_FIGURES:
        print(f"Collecting: {person_key}")
        try:
            result = collect_data(person_key)
            rows.append(result["unified"])
        except Exception as e:
            print(f"Error collecting {person_key}: {e}")

    return pd.DataFrame(rows)




if __name__ == "__main__":
    df = collect_all_data()
    print(df.head())
    df.to_csv("public_figures_unified.csv", index=False)

