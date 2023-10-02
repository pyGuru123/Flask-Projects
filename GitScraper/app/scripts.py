from app import app
import requests
import concurrent.futures

GITHUB_TOKEN = app.config.get('GITHUB_TOKEN')

### For User Class

def fetch_repo_langs(url):
    """Fetches programming languages used in a user's single repo """
    headers = {'Authorization' : f'token {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    return r.json()

def fetch_all_repo_langs(url_list):
    """Fetches programming languages used in user's all single repos"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_repo_langs, url_list)
        return results

def fetch_top_langs(url_list):
    """Fetches the top languages with their percentage"""
    langs_result = fetch_all_repo_langs(url_list)
    top_languages = {}
    total = 0
    for result in langs_result:
        for language in result:
            if language not in top_languages:
                top_languages[language] = result[language]
            else:
                top_languages[language] += result[language]
                
            total += result[language]
        
    top_lang_perc = {}
    for language in sorted(top_languages.items(), key = lambda x : x[1], reverse=True)[:6]:
        perc = round((language[1] / total) * 100, 2)
        top_lang_perc[language[0]] = perc
        
    return top_lang_perc

def fetch_repo_stats(username):
    """Fetches Repo stats of a user profile
        * Top Languages used
        * Most starred repos
        * Most forked repos
    """
    url = f"https://api.github.com/users/{username}/repos"
    try:
        r = requests.get(url)
        data = r.json()
        url_list = []
        star_list = []
        fork_list = []
        for repo in data:
            if not repo['fork']:
                url_list.append(repo['languages_url'])
                star_list.append((repo['name'], repo['stargazers_count']))
                fork_list.append((repo['name'], repo['forks_count']))
                
        top_langs = fetch_top_langs(url_list)
        top_starred = sorted(star_list, key = lambda x : x[1], reverse=True)[:5]
        top_forked = sorted(fork_list, key = lambda x : x[1], reverse=True)[:5]

        data = {
            "top_languages" : top_langs,
            "most_starred" : top_starred,
            "most_forked" : top_forked
        }
        
        return data
    except Exception as e:
        print(e)
        return None

### For Repository Class

def fetch_repo_lines(username, repo):
    url = f"https://api.codetabs.com/v1/loc?github={username}/{repo}"
    r = requests.get(url)
    return list(filter(lambda dct : dct['language'] == 'Total', r.json()))[0]