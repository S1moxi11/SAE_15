import requests
from utils.download_cache import *
"""import argparse

parser = argparse.ArgumentParser()""" 

# A COMPLETER

id_choice=input("Entrez l'id ou le nom en anglais du pokémon sur lequel vous souhaitez avoir des informations : ")

def req(ch:str):
    return requests.get(ch).json()

def stats_poke(id):
    data=download_poke_cached(id)
    dico={}
    dico["height"]=data["height"]
    dico["weight"]=data["weight"]
    for stats in data["stats"]:
        if stats["stat"]["name"] == "hp":
            dico["hp"] = stats["base_stat"]
        elif stats["stat"]["name"] == "attack":
            dico["attack"] = stats["base_stat"]
        elif stats["stat"]["name"] == "defense":
            dico["defense"] = stats["base_stat"]
        elif stats["stat"]["name"] == "speed":
            dico["speed"] = stats["base_stat"]
    nb=1
    for i in data["types"]:
        dico["type "+str(nb)]=i["type"]["name"]
        nb+=1
    print('\nVoici les informations sur '+data["forms"][0]["name"]+" :")
    return dico


"""print(stats_poke(646))"""
print(stats_poke(id_choice))
print("\nVoici une photo du pokémon :\n" + download_poke_cached(id_choice)["sprites"]["front_default"]+"\n")

