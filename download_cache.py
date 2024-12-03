import json
import requests
import os

def download(url: str) -> dict:
    dl=requests.get(url)
    dl.raise_for_status()
    return dl.json()

def download_poke_cached(id: int) -> dict:
    
    cache_path= f"cache/{id}.json"
    
    if os.path.isfile(cache_path):
        with open(cache_path,"r") as f:
            f_data = json.load(f)
        return f_data
    else:
        url = f"https://pokeapi.co/api/v2/pokemon/{id}/"
        f_data=download(url)