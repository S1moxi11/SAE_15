import requests
import math
import heapq
from utils.download_cache import *

def req(ch:str):
    return requests.get(ch).json()


def max_pc(level=100):
    dico = {}
    
    for i in download("https://pokeapi.co/api/v2/pokemon/?limit=1302")["results"]:
        nom, sta, vhp, vat, vdef = "", 0, 0, 0, 0
        
        poke_data = download_poke_cached(i["url"].split("/")[-2])
        nom = poke_data["name"]
        
        for stats in poke_data["stats"]:
            if stats["stat"]["name"] == "hp":
                vhp = stats["base_stat"]
            elif stats["stat"]["name"] == "attack":
                vat = stats["base_stat"]
            elif stats["stat"]["name"] == "defense":
                vdef = stats["base_stat"]

        sta = (0.01 * math.sqrt(vhp * vat * vdef)) * level
        dico[nom] = round(sta)
    
    return dico


"""print(max_pc())"""

top_10 = heapq.nlargest(10, max_pc().items(), key=lambda x: x[1])
"""print(top_10)"""

def img(L):
    dico={}
    nrml=None
    shiny=None
    for i in L:
        for keys, val in req("https://pokeapi.co/api/v2/pokemon-form/"+i[0])["sprites"].items():
            if keys == "front_default":
                nrml=val
            elif keys == "front_shiny":
                shiny=val
            dico[i[0]]=[nrml, shiny]
    return dico

print(img(top_10))