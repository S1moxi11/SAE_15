import requests


def trad(url: str) -> str:
    t=requests.get(url).json()
    for i in t["names"]:
        if i["language"]["name"]=="fr":
            return i["name"]