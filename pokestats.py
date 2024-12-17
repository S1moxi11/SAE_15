import requests
import math
import heapq
from utils.download_cache import *
from utils.trad import *
from utils.md_to_html import *
import webbrowser
from collections import Counter


def req(ch:str):
    """fait une requête HTTP GET à l'URL donnée et renvoie la réponse en format JSON. Arg = URL à interroger."""
    return requests.get(ch).json()


def get_dataset(id : int):
    """cherche dans le cache"""
    return download_poke_cached(id)


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
"""top_10 = heapq.nlargest(10, compute_statistics().items(), key=lambda x: x[1])"""
"""top_50 = heapq.nlargest(50, compute_statistics().items(), key=lambda x: x[1])"""
"""print(top_10)"""

def trad_list(L):
    """traduis le nom / le type"""
    nvL=[]
    for i in L:
        nvL.append(((trad(req("https://pokeapi.co/api/v2/pokemon/"+i[0])["species"]["url"]),i[0]),i[1]))
    return nvL
    
"""print(trad_list(top_10))
"""
def img(L):
    """Renvoie un dictionnaire aves les photos normal et shiny du poke -> nom poke : photo normal , photo shiny"""
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


"""print(img(trad_list(top_10)))"""

def types_pokemons(data):
    """Renvoie un dictionnaire des types du pokemon -> type n : type"""
    dico={}
    nvdico={}
    nb=1
    for i in data["types"]:
        dico["type "+str(nb)]=trad(i["type"]["url"])
        nb+=1
    types=""
    for key, value in dico.items():
        if key.startswith("type"):
            types += value.upper()+" "
    nvdico[trad(data["species"]["url"])]=dico
    return nvdico

"""print(types_pokemons(get_dataset(25)))
"""
def moyenne_types(L):
    """Cette fonction renvoie le nombre de fois ou on croise un type dans le dictionnaire des pokemons ayant le plus de pc"""
    type_counter = Counter()
    for el in L:
        types_dict = types_pokemons(get_dataset(req("https://pokeapi.co/api/v2/pokemon/"+str(el[0][1]))["id"]))
        for types in types_dict.values():
            type_counter[types['type 1']] += 1
            if 'type 2' in types:
                type_counter[types['type 2']] += 1

    return dict(type_counter)
    

"""print(moyenne_types(trad_list(top_10)))"""
"""leplus_types=heapq.nlargest(3, moyenne_types(trad_list(top_10)).items(), key=lambda x: x[1])"""
"""leplus_types=heapq.nlargest(3, moyenne_types(trad_list(top_50)).items(), key=lambda x: x[1])"""
"""print(leplus_types)"""
# Ici on renvoie les trois types les plus rencontrés dans la liste des 50 pokemons ayant le plus de pcs


def top_cmb(sur_cb:int, cb_types:int):
    """cette fonction renvoie les n types rencontrés dans les n pokemons ayant le plus de pc"""
    top_n = heapq.nlargest(sur_cb, compute_statistics().items(), key=lambda x: x[1])
    return heapq.nlargest(cb_types, moyenne_types(trad_list(top_n)).items(), key=lambda x: x[1])

"""print(top_cmb(100,10))"""


def poke_to_md(sur_cb:int, cb_types:int, filename: str) -> None:
    L = top_cmb(sur_cb, cb_types)
    with open(filename,'w') as f:
        f.write("# <center> HEY ! VOICI LA LISTE DES "+str(cb_types).upper()+" TYPES QUE L'ON RETROUVE LE PLUS DANS LES "+str(sur_cb)+" POKEMONS AYANT LE PLUS DE POINTS DE COMBAT"+"</center> \n <br><br>")
        for i in range(len(L)):
            f.write("- Le "+str(i+1)+"e type est : "+ L[i][0] + " avec "+ str(L[i][1]) + " occurences !" +"\n <br><br>")
            

def fiche_pokemon(sur_cb:int, cb_types:int) -> None:
    poke_to_md(sur_cb, cb_types, "page_stats.md")
    convert("page_stats.md","page_stats.html")


fiche_pokemon(100,10)

webbrowser.open("page_stats.html")