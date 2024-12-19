import requests
from utils.download_cache import *
from utils.md_to_html import *
from utils.trad import *
import argparse
import webbrowser

parser = argparse.ArgumentParser()
parser.add_argument("poke", help="Entrez l'ID ou le nom d'un pokémon en anglais")
args = parser.parse_args()



def req(ch:str):
    return requests.get(ch).json()

def download_poke(id: int) -> dict:
   return req("https://pokeapi.co/api/v2/pokemon/"+str(id))

def poke_to_md(data: dict, filename: str) -> None:
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
        dico["type "+str(nb)]=trad(i["type"]["url"])
        nb+=1
    types=""
    for key, value in dico.items():
        if key.startswith("type"):
            types += value.upper()+" "

    with open(filename,'w') as f:

        f.write("# <center> HEY ! VOICI UNE FICHE SUR "+str(trad(data["species"]["url"])).upper()+"</center> \n <br><br>")
        f.write("- Son poids est de : "+str(dico["weight"])+"\n <br><br>")
        f.write("- Sa taille est de : "+str(dico["height"])+"\n <br><br>")
        f.write("- Son/ses type(s) sont : "+ types +"\n <br><br>")
        f.write("- Son nombre de points de vie est de : "+str(dico["hp"])+"\n <br><br>")
        f.write("- Sa puissance d'attaque est de : "+str(dico["attack"])+"\n <br><br>")
        f.write("- Ses points de defense sont de : "+str(dico["defense"])+"\n <br><br>")
        f.write("- Sa vitesse est de : "+str(dico["height"])+"\n <br><br><br>")
        f.write("![alt text]("+data["sprites"]["front_default"]+")")



def fiche_pokemon(id: int) -> None:
    poke_to_md(download_poke(id), "page_poke.md")
    convert("page_poke.md","page_poke.html")


fiche_pokemon(args.poke)

webbrowser.open("page_poke.html")