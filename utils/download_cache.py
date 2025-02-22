import json
import requests
import os

def download(url: str) -> dict:
    dl=requests.get(url)
    dl.raise_for_status()
    return dl.json()

def download_poke_cached(nom: str) -> dict:
    if not os.path.isdir('cache'):
        os.mkdir("cache")
    cache_path= f"cache/{nom}.json"
    
    if os.path.isfile(cache_path):
        with open(cache_path,"r") as f:
            f_data = json.load(f)
        return f_data
    else:
        url = f"https://pokeapi.co/api/v2/pokemon/{nom}/"
        f_data=download(url)
        f = open(cache_path,"w")
        json.dump(f_data,f)
        f.close()
        return f_data