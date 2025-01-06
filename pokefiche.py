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

    with open(filename, 'w') as f:
        f.write(f"# <center class='title'>HEY ! VOICI UNE FICHE SUR {str(trad(data['species']['url'])).upper()}</center>\n\n")
        f.write("## Informations principales\n")
        f.write(f"- **Poids :** {dico['weight']} kg\n")
        f.write(f"- **Taille :** {dico['height']} m\n")
        f.write(f"- **Type(s) :** {types.strip()}\n")
        f.write(f"- **Points de vie (HP) :** {dico['hp']}\n")
        f.write(f"- **Puissance d'attaque :** {dico['attack']}\n")
        f.write(f"- **Points de défense :** {dico['defense']}\n")
        f.write(f"- **Vitesse :** {dico['speed']}\n\n")
        if type(data["sprites"]["front_default"]) == str :
            f.write("![alt text]("+str(data["sprites"]["front_default"])+")")

            



def fiche_pokemon(id: int) -> None:
    poke_to_md(download_poke(id), "page_poke.md")
    convert("page_poke.md","page_poke.html")


fiche_pokemon(args.poke)

webbrowser.open("page_poke.html")