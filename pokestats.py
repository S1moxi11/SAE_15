import requests
import math
import heapq
from utils.download_cache import *
from utils.trad import *
import webbrowser

def req(ch:str):
    return requests.get(ch).json()

"""def get_dataset():
    L=[]
    for i in download("https://pokeapi.co/api/v2/pokemon/?limit=1302")["results"]:
        L.append(download_poke_cached(i["url"].split("/")[-2]))"""


def compute_statistics(level=100):
    """Cette fonction renvoie un dictionnaire avec 
    le nom du pokemon en clé ainsi ses pc en valeur pour tous les pokémons"""
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

"""print(compute_statistics)"""

top_10 = heapq.nlargest(10, compute_statistics().items(), key=lambda x: x[1])
"""print(top_10)"""

def trad_list(L):
    nvL=[]
    for i in L:
        nvL.append(((trad(req("https://pokeapi.co/api/v2/pokemon/"+i[0])["species"]["url"]),i[0]),i[1]))
    return nvL
    
"""print(trad_list(top_10))"""

def img(L):
    dico={}
    nrml=None
    shiny=None
    for i in L:
        for keys, val in req("https://pokeapi.co/api/v2/pokemon-form/"+i[0][1])["sprites"].items():
            if keys == "front_default":
                nrml=val
            elif keys == "front_shiny":
                shiny=val
            dico[i[0][0]]=[nrml, shiny]
    return dico


print(img(trad_list(top_10)))


def types_pokemons():
    pass

def moyenne_types():
    pass


def poke_to_md(data: dict, filename: str) -> None:
    # A completer

    with open(filename,'w') as f:
        f.write("A completer")
    pass


"""webbrowser.open("page_poke.html")"""



"""Donner la moyenne des pc des pokemons 
ayant le plus de pcs en fonction de leurs types"""