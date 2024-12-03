import requests
import math
import heapq

def req(ch:str):
    return requests.get(ch).json()

dicopoke = req("https://pokeapi.co/api/v2/")

dracofeu = req("https://pokeapi.co/api/v2/pokemon/charizard")

"""print("La taille de dracofeu est de : " + str(req("https://pokeapi.co/api/v2/pokemon/charizard")["height"]))
"""

def max_pc(level=100):
    dico={}
    nom,sta,vhp,vat,vdef=0,0,0,0,0
    for i in req("https://pokeapi.co/api/v2/pokemon/?limit=1302")["results"]:
        for keys, val in req(i["url"]).items():
            if keys == "forms" :
                nom = val[0]["name"]
            if keys == "stats" :
                for i in val:
                    if i["stat"]["name"] == "hp":
                        vhp = i["base_stat"]
                    elif i["stat"]["name"] == "attack":
                        vat = i["base_stat"]
                    elif i["stat"]["name"] == "defense":
                        vdef = i["base_stat"]
                sta = (0.01 * math.sqrt(vhp * vat * vdef)) * level
        dico[nom]=round(sta)

    return dico

"""print(max_pc())"""

top_10 = heapq.nlargest(10, max_pc().items(), key=lambda x: x[1])
print(top_10)