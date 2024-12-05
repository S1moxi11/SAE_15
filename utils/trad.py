import requests


def name_trad(url: str) -> str:
    t=requests.get(url).json()
    f=requests.get(t["species"]["url"]).json()
    for i in f["names"]:
        if i["language"]["name"]=="fr":
            return i["name"]

def type_trad(url: str) -> str:
    t=requests.get(url).json()
    f=requests.get(t["types"][0]["type"]["url"]).json()
    for i in f["names"]:
        if i["language"]["name"]=="fr":
            return i["name"]