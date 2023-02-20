from app import app
import requests
import concurrent.futures

GITHUB_TOKEN = app.config.get('GITHUB_TOKEN')

def fetch_repo_langs(url):
    headers = {'Authorization' : f'token {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    return r.json()

def fetch_all_repo_langs(url_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_languages, url_list)
        return results
