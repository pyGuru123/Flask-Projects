import re
import requests
from bs4 import BeautifulSoup

class User:
    """A python wrapper to scrape any github profile"""
    def __init__(self, username:str=None):
        self.url = f"https://github.com/{username}"
        try:
            response = requests.get(self.url)
            self.soup = BeautifulSoup(response.text, "html.parser")
        except:
            print("Username not found")
            raise Exception("Username not found")

    def __str__(self) -> str:
        return f"User({self.fullname})"

    @property
    def username(self) -> str:
        """Return username of the user"""
        fullname = self.soup.select_one("[class*='p-nickname vcard-username']")
        return fullname.text.strip()

    @property
    def fullname(self) -> str:
        """Returns the fullname of the user"""
        fullname = self.soup.select_one("[class*='p-name vcard-fullname d-block']")
        return fullname.text.strip()

    @property
    def avatar(self) -> str:
        """Returns the profile pic url"""
        url = self.soup.select_one("[class*='avatar avatar-user']")
        return url['src']

    @property
    def followers(self) -> str:
        """Returns total number of followers of the user"""
        followers = self.soup.select("[class*='text-bold color-fg-default']")
        return followers[0].text

    @property
    def following(self) -> str:
        """Returns the number of accounts user had followed"""
        following = self.soup.select("[class*='text-bold color-fg-default']")
        return following[1].text

    @property
    def bio(self) -> [str, None]:
        """Returns the bio of the user"""
        bio = self.soup.select_one("[class*='p-note user-profile-bio']")
        if bio:
            return bio.text.strip()
        return None

    @property
    def location(self) -> [str, None]:
        """Returns the location of the user"""
        location = self.soup.select_one("[itemprop='homeLocation']")
        if location:
            return location.text.strip()
        return None

    @property
    def repositories(self) -> str:
        """Returns the total number of repositories of the user"""
        repos = self.soup.select("[class*='UnderlineNav-item']")[1].text.strip()
        return repos.split("\n")[1].strip()

    @property
    def readme(self) -> [str, None]:
        """Returns the readme article of the profile"""
        try:
            readme = self.soup.select_one("[class*='markdown-body entry-content']").text
            return "".join(filter(lambda ele: ele != '', readme.splitlines()))
        except AttributeError:
            return None

    @property
    def contributions(self) -> str:
        """Returns total number of contributions this year"""
        contributions = self.soup.select_one("[class*='js-yearly-contributions']")
        return contributions.find('h2').text.split()[0]

    def get_pinned_repos(self) -> [list, None]:
        """Return all the pinned repos of the user"""
        repos = self.soup.find_all("span", class_="repo")
        if repos:
            return [repo.text for repo in repos]
        return None

    def get_full_info(self) -> dict:
        """Returns the complete scraped user info"""
        data = {
            "username" : self.username,
            "fullname" : self.fullname,
            "avatar" : self.avatar,
            "followers" : self.followers,
            "following" : self.following,
            "bio" : self.bio,
            "location" : self.location,
            "repositories" : self.repositories,
            "readme" : self.readme,
            "contributions" : self.contributions,
            "pinned" : self.get_pinned_repos()
        }

        return data

class Repository:
    """A python wrapper to scrape any github repository"""
    def __init__(self, repo:str=None):
        try:
            response = requests.get(repo)
            self.soup = BeautifulSoup(response.text, "html.parser")
        except:
            print("Username not found")
            raise Exception("Repository not found")

    def __str__(self) -> str:
        return f"Repository({self.reponame})"

    @property
    def reponame(self) -> str:
        """Returns the fullname of the repository"""
        reponame = self.soup.select_one("[class*='mr-2 flex-self-stretch']")
        return reponame.text.strip()

    @property
    def author(self) -> str:
        """Returns the author of the repository"""
        author = self.soup.select_one("[class*='author flex-self-stretch']")
        return  author.text.strip()

    @property
    def about(self) -> str:
        """Returns the about of the repository"""
        try:
            about = self.soup.select_one("[class*='f4 my-3']")
            return about.text.strip()
        except:
            return None

    @property
    def weblink(self) -> str:
        """Returns the website link of the repository"""
        try:
            link = self.soup.select_one("[class*='my-3 d-flex flex-items-center']")
            return link.text.strip()
        except:
            return None
        
    @property
    def topics(self) -> list[str]:
        """Returns the topics listed under a repository"""
        try:
            topics = self.soup.select("[class*='topic-tag topic-tag-link']")
            return [topic.text.strip() for topic in topics]
        except:
            return []

    @property
    def issues(self) -> str:
        """Returns the number of issues in a repository"""
        issues = self.soup.select_one("[id*='issues-repo-tab-count']")
        return issues.text.strip()

    @property
    def pullrequests(self) -> str:
        """Returns the number of pull requests in a repository"""
        prs = self.soup.select_one("[id*='pull-requests-repo-tab-count']")
        return prs.text.strip()

    @property
    def forks(self) -> str:
        """Returns the number of forks of a repository"""
        forks = self.soup.select_one("[id*='repo-network-counter']")
        return forks.text.strip()

    @property
    def stars(self) -> str:
        """Returns the number of stars on a repository"""
        stars = self.soup.select_one("[id*='repo-stars-counter-star']")
        return stars.text.strip()

    @property
    def watching(self) -> str:
        """Returns the number of watchers on a repository"""
        watching = self.soup.select_one("[id*='repo-network-counter']")
        return watching.text.strip()

    @property
    def commits(self) -> str:
        """Returns the number of commits on main branch of a repository"""
        commits = self.soup.select_one("[class*='ml-0 ml-md-3']")
        return ''.join(re.findall('\d+', commits.text))

    @property
    def repotype(self) -> str:
        """Returns repository type - public / private"""
        repotype = self.soup.select_one("[class*='Label Label--secondary v-align-middle mr-1']")
        return repotype.text.strip()

    @property
    def languages(self) -> dict:
        """Returns the languages used in the repository"""
        try: 
            languages = {}
            langs = self.soup.select("[class*='d-inline-flex flex-items-center flex-nowrap Link--secondary no-underline text-small mr-3']")
            for lang in langs:
                datalist = lang.text.strip().split('\n')
                languages[datalist[0]] = datalist[1].strip('%')

            return languages
        except:
            return {}

    def get_full_info(self) -> dict:
        """Returns the complete scraped user info"""
        data = {
            "reponame" : self.reponame,
            "author" : self.author,
            "about" : self.about,
            "weblink" : self.weblink,
            "topics" : self.topics,
            "issues" : self.issues,
            "pullrequests" : self.pullrequests,
            "forks" : self.forks,
            "stars" : self.stars,
            "watching" : self.watching,
            "commits" : self.commits,
            "repotype" : self.repotype,
            "languages" : self.languages
        }

        return data